/**
 * @fileoverview Handles citation formatting for the pubmedArticleConnections tool.
 * Fetches article details using EFetch and formats them into various citation styles.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/citationFormatter
 */

import Cite from "citation-js";
import { getNcbiService } from "../../../../services/NCBI/core/ncbiService.js";
import type {
  XmlPubmedArticle,
  XmlPubmedArticleSet,
} from "../../../../types-global/pubmedXml.js";
import {
  logger,
  RequestContext,
  requestContextService,
} from "../../../../utils/index.js";
import {
  extractAuthors,
  extractDoi,
  extractJournalInfo,
  extractPmid,
  getText,
} from "../../../../services/NCBI/parsing/index.js";
import { ensureArray } from "../../../../services/NCBI/parsing/index.js";
import type { PubMedArticleConnectionsInput } from "./index.js";
import type { ToolOutputData } from "./types.js";

// Main handler for citation formats
export async function handleCitationFormats(
  input: PubMedArticleConnectionsInput,
  outputData: ToolOutputData,
  context: RequestContext,
): Promise<void> {
  const eFetchParams = {
    db: "pubmed",
    id: input.sourcePmid,
    retmode: "xml" as const,
  };

  const eFetchBaseUrl =
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi";
  const searchParamsString = new URLSearchParams(
    eFetchParams as Record<string, string>,
  ).toString();
  outputData.eUtilityUrl = `${eFetchBaseUrl}?${searchParamsString}`;

  const ncbiService = getNcbiService();
  const eFetchResult: { PubmedArticleSet?: XmlPubmedArticleSet } =
    (await ncbiService.eFetch(eFetchParams, context)) as {
      PubmedArticleSet?: XmlPubmedArticleSet;
    };

  const pubmedArticles = ensureArray<XmlPubmedArticle>(
    eFetchResult?.PubmedArticleSet?.PubmedArticle as
      | XmlPubmedArticle
      | XmlPubmedArticle[]
      | undefined,
  );

  if (pubmedArticles.length === 0) {
    outputData.message =
      "Could not retrieve article details for citation formatting.";
    logger.warning(outputData.message, context);
    return;
  }

  const article: XmlPubmedArticle = pubmedArticles[0]!;
  const csl = pubmedArticleToCsl(article, context);
  const cite = new Cite(csl);

  if (input.citationStyles?.includes("ris")) {
    outputData.citations.ris = cite.format("ris");
  }
  if (input.citationStyles?.includes("bibtex")) {
    outputData.citations.bibtex = cite.format("bibtex");
  }
  if (input.citationStyles?.includes("apa_string")) {
    outputData.citations.apa_string = cite.format("bibliography", {
      format: "text",
      template: "apa",
    });
  }
  if (input.citationStyles?.includes("mla_string")) {
    outputData.citations.mla_string = cite.format("bibliography", {
      format: "text",
      template: "mla",
    });
  }
  outputData.retrievedCount = 1;
}

/**
 * Converts an XML PubMed Article object to a CSL-JSON object.
 * @param article The PubMed article in XML format.
 * @param context The request context for logging.
 * @returns A CSL-JSON object compatible with citation-js.
 */
function pubmedArticleToCsl(
  article: XmlPubmedArticle,
  context: RequestContext,
): Record<string, unknown> {
  const medlineCitation = article.MedlineCitation;
  const articleDetails = medlineCitation?.Article;
  const pmid = extractPmid(medlineCitation);

  const cslContext = requestContextService.createRequestContext({
    ...context,
    pmid,
  });
  logger.debug("Converting PubMed XML to CSL-JSON", cslContext);

  if (!articleDetails) {
    logger.warning("Article details not found for CSL conversion", cslContext);
    return { id: pmid || "unknown", title: "Article details not found" };
  }

  const authors = extractAuthors(articleDetails.AuthorList);
  const journalInfo = extractJournalInfo(
    articleDetails.Journal,
    medlineCitation,
  );
  const title = getText(articleDetails.ArticleTitle);
  const doi = extractDoi(articleDetails);

  const cslAuthors = authors.map((author) =>
    author.collectiveName
      ? { literal: author.collectiveName }
      : { family: author.lastName, given: author.firstName },
  );

  const dateParts: (number | string)[] = [];
  if (journalInfo?.publicationDate?.year) {
    dateParts.push(parseInt(journalInfo.publicationDate.year, 10));
    if (journalInfo.publicationDate.month) {
      // Convert month name/number to number
      const monthNumber = new Date(
        `${journalInfo.publicationDate.month} 1, 2000`,
      ).getMonth();
      if (!isNaN(monthNumber)) {
        dateParts.push(monthNumber + 1);
        if (journalInfo.publicationDate.day) {
          dateParts.push(parseInt(journalInfo.publicationDate.day, 10));
        }
      }
    }
  }

  const cslData: Record<string, unknown> = {
    id: pmid,
    type: "article-journal",
    title: title,
    author: cslAuthors,
    issued: {
      "date-parts": [dateParts],
    },
    "container-title": journalInfo?.title,
    volume: journalInfo?.volume,
    issue: journalInfo?.issue,
    page: journalInfo?.pages,
    DOI: doi,
    PMID: pmid,
    URL: pmid ? `https://pubmed.ncbi.nlm.nih.gov/${pmid}` : undefined,
  };

  // Clean up any undefined/null properties
  for (const [key, value] of Object.entries(cslData)) {
    if (value === undefined || value === null) {
      delete (cslData as Record<string, unknown>)[key];
    }
  }

  return cslData;
}
