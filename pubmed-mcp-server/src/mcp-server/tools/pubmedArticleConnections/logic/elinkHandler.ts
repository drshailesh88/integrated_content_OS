/**
 * @fileoverview Handles ELink requests and enriches results with ESummary data
 * for the pubmedArticleConnections tool.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/elinkHandler
 */

import { getNcbiService } from "../../../../services/NCBI/core/ncbiService.js";
import type {
  ESummaryResult,
  ParsedBriefSummary,
} from "../../../../types-global/pubmedXml.js";
import { logger, RequestContext } from "../../../../utils/index.js";
import { extractBriefSummaries } from "../../../../services/NCBI/parsing/index.js";
import { ensureArray } from "../../../../services/NCBI/parsing/xmlGenericHelpers.js"; // Added import
import type { PubMedArticleConnectionsInput } from "./index.js";
import type { ToolOutputData } from "./types.js";

// Local interface for the structure of an ELink 'Link' item
interface XmlELinkItem {
  Id: string | number | { "#text"?: string | number }; // Allow number for Id
  Score?: string | number | { "#text"?: string | number }; // Allow number for Score
}

interface ELinkResult {
  eLinkResult?: {
    LinkSet?: {
      LinkSetDb?: {
        LinkName?: string;
        Link?: XmlELinkItem[];
      }[];
      LinkSetDbHistory?: {
        QueryKey?: string;
      }[];
      WebEnv?: string;
    };
    ERROR?: string;
  }[];
}

export async function handleELinkRelationships(
  input: PubMedArticleConnectionsInput,
  outputData: ToolOutputData,
  context: RequestContext,
): Promise<void> {
  const eLinkParams: Record<string, string> = {
    dbfrom: "pubmed",
    db: "pubmed",
    id: input.sourcePmid,
    retmode: "xml",
    // cmd and linkname will be set below based on relationshipType
  };

  switch (input.relationshipType) {
    case "pubmed_citedin":
      eLinkParams.cmd = "neighbor_history";
      eLinkParams.linkname = "pubmed_pubmed_citedin";
      break;
    case "pubmed_references":
      eLinkParams.cmd = "neighbor_history";
      eLinkParams.linkname = "pubmed_pubmed_refs";
      break;
    case "pubmed_similar_articles":
    default: // Default to similar articles
      eLinkParams.cmd = "neighbor_score";
      // No linkname is explicitly needed for neighbor_score when dbfrom and db are pubmed
      break;
  }

  const tempUrl = new URL(
    "https://dummy.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi",
  );
  Object.keys(eLinkParams).forEach((key) =>
    tempUrl.searchParams.append(key, String(eLinkParams[key])),
  );
  outputData.eUtilityUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?${tempUrl.search.substring(1)}`;

  const ncbiService = getNcbiService();
  const eLinkResult: ELinkResult = (await ncbiService.eLink(
    eLinkParams,
    context,
  )) as ELinkResult;

  // Log the full eLinkResult for debugging
  logger.debug("Raw eLinkResult from ncbiService:", {
    ...context,
    eLinkResultString: JSON.stringify(eLinkResult, null, 2),
  });

  // Use ensureArray for robust handling of potentially single or array eLinkResult
  const eLinkResultsArray = ensureArray(eLinkResult?.eLinkResult);
  const firstELinkResult = eLinkResultsArray[0];

  // Use ensureArray for LinkSet as well
  const linkSetsArray = ensureArray(firstELinkResult?.LinkSet);
  const linkSet = linkSetsArray[0];

  let foundPmids: { pmid: string; score?: number }[] = [];

  if (firstELinkResult?.ERROR) {
    const errorMsg =
      typeof firstELinkResult.ERROR === "string"
        ? firstELinkResult.ERROR
        : JSON.stringify(firstELinkResult.ERROR);
    logger.warning(`ELink returned an error: ${errorMsg}`, context);
    outputData.message = `ELink error: ${errorMsg}`;
    outputData.retrievedCount = 0;
    return;
  }

  if (linkSet?.LinkSetDbHistory) {
    // Handle cmd=neighbor_history response (citedin, references)
    const history = Array.isArray(linkSet.LinkSetDbHistory)
      ? linkSet.LinkSetDbHistory[0]
      : linkSet.LinkSetDbHistory;

    if (history?.QueryKey && firstELinkResult?.LinkSet?.WebEnv) {
      const eSearchParams = {
        db: "pubmed",
        query_key: history.QueryKey,
        WebEnv: firstELinkResult.LinkSet.WebEnv,
        retmode: "xml",
        retmax: input.maxRelatedResults * 2, // Fetch a bit more to allow filtering sourcePmid
      };
      const eSearchResult: { eSearchResult?: { IdList?: { Id?: unknown } } } =
        (await ncbiService.eSearch(eSearchParams, context)) as {
          eSearchResult?: { IdList?: { Id?: unknown } };
        };
      if (eSearchResult?.eSearchResult?.IdList?.Id) {
        const ids = ensureArray(eSearchResult.eSearchResult.IdList.Id);
        foundPmids = ids
          .map((idNode: string | number | { "#text"?: string | number }) => {
            // Allow number for idNode
            let pmidVal: string | number | undefined;
            if (typeof idNode === "object" && idNode !== null) {
              pmidVal = idNode["#text"];
            } else {
              pmidVal = idNode;
            }
            return {
              pmid: pmidVal !== undefined ? String(pmidVal) : "",
              // No scores from this ESearch path
            };
          })
          .filter(
            (item: { pmid: string }) =>
              item.pmid && item.pmid !== input.sourcePmid && item.pmid !== "0",
          );
      }
    }
  } else if (linkSet?.LinkSetDb) {
    // Handle cmd=neighbor_score response (similar_articles)
    const linkSetDbArray = Array.isArray(linkSet.LinkSetDb)
      ? linkSet.LinkSetDb
      : [linkSet.LinkSetDb];

    const targetLinkSetDbEntry = linkSetDbArray.find(
      (db) => db.LinkName === "pubmed_pubmed",
    );

    if (targetLinkSetDbEntry?.Link) {
      const links = ensureArray(targetLinkSetDbEntry.Link); // Use ensureArray here too
      foundPmids = links
        .map((link: XmlELinkItem) => {
          let pmidValue: string | number | undefined;
          if (typeof link.Id === "object" && link.Id !== null) {
            pmidValue = link.Id["#text"];
          } else if (link.Id !== undefined) {
            pmidValue = link.Id;
          }

          let scoreValue: string | number | undefined;
          if (typeof link.Score === "object" && link.Score !== null) {
            scoreValue = link.Score["#text"];
          } else if (link.Score !== undefined) {
            scoreValue = link.Score;
          }

          const pmidString = pmidValue !== undefined ? String(pmidValue) : "";

          return {
            pmid: pmidString,
            score: scoreValue !== undefined ? Number(scoreValue) : undefined,
          };
        })
        .filter(
          (item: { pmid: string; score?: number }) =>
            item.pmid && item.pmid !== input.sourcePmid && item.pmid !== "0",
        );
    }
  }

  if (foundPmids.length === 0) {
    logger.warning(
      "No related PMIDs found after ELink/ESearch processing.",
      context,
    );
    outputData.message = "No related articles found or ELink error."; // Generic message if no PMIDs
    outputData.retrievedCount = 0;
    return;
  }

  logger.debug(
    "Found PMIDs after initial parsing and filtering (before sort):",
    {
      ...context,
      foundPmidsCount: foundPmids.length,
      firstFewFoundPmids: foundPmids.slice(0, 3),
    },
  );

  if (foundPmids.every((p) => p.score !== undefined)) {
    foundPmids.sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
  }

  logger.debug("Found PMIDs after sorting:", {
    ...context,
    sortedFoundPmidsCount: foundPmids.length,
    firstFewSortedFoundPmids: foundPmids.slice(0, 3),
  });

  const pmidsToEnrich = foundPmids
    .slice(0, input.maxRelatedResults)
    .map((p) => p.pmid);

  logger.debug("PMIDs to enrich with ESummary:", {
    ...context,
    pmidsToEnrichCount: pmidsToEnrich.length,
    pmidsToEnrichList: pmidsToEnrich,
  });

  if (pmidsToEnrich.length > 0) {
    try {
      const summaryParams = {
        db: "pubmed",
        id: pmidsToEnrich.join(","),
        version: "2.0",
        retmode: "xml",
      };
      const summaryResultContainer: {
        eSummaryResult?: ESummaryResult;
        result?: ESummaryResult;
      } = (await ncbiService.eSummary(summaryParams, context)) as {
        eSummaryResult?: ESummaryResult;
        result?: ESummaryResult;
      };
      const summaryResult: ESummaryResult | undefined =
        summaryResultContainer?.eSummaryResult ||
        summaryResultContainer?.result ||
        summaryResultContainer;

      if (summaryResult) {
        const briefSummaries: ParsedBriefSummary[] =
          await extractBriefSummaries(summaryResult, context);
        const pmidDetailsMap = new Map<string, ParsedBriefSummary>();
        briefSummaries.forEach((bs) => pmidDetailsMap.set(bs.pmid, bs));

        outputData.relatedArticles = foundPmids
          .filter((p) => pmidsToEnrich.includes(p.pmid))
          .map((p) => {
            const details = pmidDetailsMap.get(p.pmid);
            return {
              pmid: p.pmid,
              title: details?.title,
              authors: details?.authors,
              score: p.score,
              linkUrl: `https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/`,
            };
          })
          .slice(0, input.maxRelatedResults);
      } else {
        logger.warning(
          "ESummary did not return usable data for enrichment.",
          context,
        );
        outputData.relatedArticles = foundPmids
          .slice(0, input.maxRelatedResults)
          .map((p) => ({
            pmid: p.pmid,
            score: p.score,
            linkUrl: `https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/`,
          }));
      }
    } catch (summaryError: unknown) {
      logger.error(
        "Failed to enrich related articles with summaries",
        summaryError instanceof Error
          ? summaryError
          : new Error(String(summaryError)),
        context,
      );
      outputData.relatedArticles = foundPmids
        .slice(0, input.maxRelatedResults)
        .map((p) => ({
          pmid: p.pmid,
          score: p.score,
          linkUrl: `https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/`,
        }));
    }
  }
  outputData.retrievedCount = outputData.relatedArticles.length;
}
