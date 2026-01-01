/**
 * @fileoverview Logic for the pubmed_fetch_contents MCP tool.
 * Handles EFetch queries for specific PMIDs and formats the results.
 * This tool can fetch various details from PubMed including abstracts, full XML,
 * MEDLINE text, and citation data.
 * @module src/mcp-server/tools/pubmedFetchContents/logic
 */

import { z } from "zod";
import { getNcbiService } from "../../../services/NCBI/core/ncbiService.js";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  ParsedArticle,
  XmlMedlineCitation,
  XmlPubmedArticleSet,
} from "../../../types-global/pubmedXml.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import {
  ensureArray,
  extractAbstractText,
  extractArticleDates,
  extractAuthors,
  extractDoi,
  extractGrants,
  extractJournalInfo,
  extractKeywords,
  extractMeshTerms,
  extractPmid,
  extractPublicationTypes,
  getText,
} from "../../../services/NCBI/parsing/index.js";

export const PubMedFetchContentsInputSchema = z
  .object({
    pmids: z
      .array(z.string().regex(/^\d+$/))
      .max(200, "Max 200 PMIDs per call if not using history.")
      .optional()
      .describe(
        "An array of PubMed Unique Identifiers (PMIDs) to fetch. Use this OR queryKey/webEnv.",
      ),
    queryKey: z
      .string()
      .optional()
      .describe(
        "Query key from ESearch history. Requires webEnv. Use this OR pmids.",
      ),
    webEnv: z
      .string()
      .optional()
      .describe(
        "Web environment from ESearch history. Requires queryKey. Use this OR pmids.",
      ),
    retstart: z
      .number()
      .int()
      .min(0)
      .optional()
      .describe(
        "0-based index of the first record to retrieve. Used with queryKey/webEnv.",
      ),
    retmax: z
      .number()
      .int()
      .min(1)
      .optional()
      .describe(
        "Maximum number of records to retrieve. Used with queryKey/webEnv.",
      ),
    detailLevel: z
      .enum(["abstract_plus", "full_xml", "medline_text", "citation_data"])
      .optional()
      .default("abstract_plus")
      .describe(
        "Specifies the level of detail for the fetched content. Options: 'abstract_plus' (parsed details), 'full_xml' (raw PubMedArticle XML), 'medline_text' (MEDLINE format), 'citation_data' (minimal citation data). Defaults to 'abstract_plus'.",
      ),
    includeMeshTerms: z
      .boolean()
      .optional()
      .default(true)
      .describe(
        "Include MeSH terms in 'abstract_plus' and 'citation_data' results. Default: true.",
      ),
    includeGrantInfo: z
      .boolean()
      .optional()
      .default(false)
      .describe(
        "Include grant info in 'abstract_plus' results. Default: false.",
      ),
    outputFormat: z
      .enum(["json", "raw_text"])
      .optional()
      .default("json")
      .describe(
        "Output format. 'json' (default) wraps data in a JSON object. 'raw_text' returns raw text for 'medline_text' or 'full_xml' detail levels.",
      ),
  })
  .superRefine((data, ctx) => {
    if (data.queryKey && !data.webEnv) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "webEnv is required if queryKey is provided.",
        path: ["webEnv"],
      });
    }
    if (!data.queryKey && data.webEnv) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "queryKey is required if webEnv is provided.",
        path: ["queryKey"],
      });
    }
    if (
      (!data.pmids || data.pmids.length === 0) &&
      !(data.queryKey && data.webEnv)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          "Either pmids (non-empty array) or both queryKey and webEnv must be provided.",
        path: ["pmids"],
      });
    }
    if (data.pmids && data.pmids.length > 0 && (data.queryKey || data.webEnv)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          "Cannot use pmids and queryKey/webEnv simultaneously. Please choose one method.",
        path: ["pmids"],
      });
    }
    if (
      (data.retstart !== undefined || data.retmax !== undefined) &&
      !(data.queryKey && data.webEnv)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "retstart/retmax can only be used with queryKey and webEnv.",
        path: ["retstart"],
      });
    }
  });

export type PubMedFetchContentsInput = z.infer<
  typeof PubMedFetchContentsInputSchema
>;

export type PubMedFetchContentsOutput = {
  content: string;
  articlesReturned: number;
  eFetchUrl: string;
};

interface EFetchServiceParams {
  db: string;
  id?: string;
  query_key?: string;
  WebEnv?: string;
  retmode?: "xml" | "text";
  rettype?: string;
  retstart?: string;
  retmax?: string;
  [key: string]: string | undefined;
}

function parsePubMedArticleSet(
  xmlData: unknown,
  input: PubMedFetchContentsInput,
  parentContext: RequestContext,
): ParsedArticle[] {
  const articles: ParsedArticle[] = [];
  const operationContext = requestContextService.createRequestContext({
    parentRequestId: parentContext.requestId,
    operation: "parsePubMedArticleSet",
  });

  if (
    !xmlData ||
    typeof xmlData !== "object" ||
    !("PubmedArticleSet" in xmlData)
  ) {
    throw new McpError(
      BaseErrorCode.PARSING_ERROR,
      "Invalid or unexpected structure for xmlData in parsePubMedArticleSet.",
      {
        ...operationContext,
        xmlDataType: typeof xmlData,
        xmlDataPreview: sanitizeInputForLogging(
          JSON.stringify(xmlData).substring(0, 200),
        ),
      },
    );
  }

  const typedXmlData = xmlData as { PubmedArticleSet?: XmlPubmedArticleSet };
  const articleSet = typedXmlData.PubmedArticleSet;

  if (!articleSet || !articleSet.PubmedArticle) {
    logger.warning(
      "PubmedArticleSet or PubmedArticle array not found in EFetch XML response.",
      operationContext,
    );
    return articles;
  }

  const pubmedArticlesXml = ensureArray(articleSet.PubmedArticle);

  for (const articleXml of pubmedArticlesXml) {
    if (!articleXml || typeof articleXml !== "object") continue;

    const medlineCitation: XmlMedlineCitation | undefined =
      articleXml.MedlineCitation;
    if (!medlineCitation) continue;

    const pmid = extractPmid(medlineCitation);
    if (!pmid) continue;

    const articleNode = medlineCitation.Article;
    const parsedArticle: ParsedArticle = {
      pmid: pmid,
      title: articleNode?.ArticleTitle
        ? getText(articleNode.ArticleTitle)
        : undefined,
      abstractText: articleNode?.Abstract
        ? extractAbstractText(articleNode.Abstract)
        : undefined,
      authors: articleNode?.AuthorList
        ? extractAuthors(articleNode.AuthorList)
        : undefined,
      journalInfo: articleNode?.Journal
        ? extractJournalInfo(articleNode.Journal, medlineCitation)
        : undefined,
      publicationTypes: articleNode?.PublicationTypeList
        ? extractPublicationTypes(articleNode.PublicationTypeList)
        : undefined,
      keywords: articleNode?.KeywordList
        ? extractKeywords(articleNode.KeywordList)
        : undefined,
      doi: articleNode ? extractDoi(articleNode) : undefined,
      articleDates: articleNode?.ArticleDate
        ? extractArticleDates(articleNode)
        : undefined,
    };

    if (input.includeMeshTerms) {
      parsedArticle.meshTerms = medlineCitation.MeshHeadingList
        ? extractMeshTerms(medlineCitation.MeshHeadingList)
        : undefined;
    }

    if (input.includeGrantInfo) {
      parsedArticle.grantList = articleNode?.GrantList
        ? extractGrants(articleNode.GrantList)
        : undefined;
    }

    articles.push(parsedArticle);
  }
  return articles;
}

export async function pubMedFetchContentsLogic(
  input: PubMedFetchContentsInput,
  parentRequestContext: RequestContext,
): Promise<PubMedFetchContentsOutput> {
  const toolLogicContext = requestContextService.createRequestContext({
    parentRequestId: parentRequestContext.requestId,
    operation: "pubMedFetchContentsLogic",
    input: sanitizeInputForLogging(input),
  });

  const validationResult = PubMedFetchContentsInputSchema.safeParse(input);
  if (!validationResult.success) {
    throw new McpError(
      BaseErrorCode.VALIDATION_ERROR,
      validationResult.error.errors[0]?.message || "Invalid input",
      { ...toolLogicContext, details: validationResult.error.flatten() },
    );
  }

  const ncbiService = getNcbiService();
  logger.info("Executing pubmed_fetch_contents tool", toolLogicContext);

  const eFetchParams: EFetchServiceParams = { db: "pubmed" };

  if (input.queryKey && input.webEnv) {
    eFetchParams.query_key = input.queryKey;
    eFetchParams.WebEnv = input.webEnv;
    if (input.retstart !== undefined)
      eFetchParams.retstart = String(input.retstart);
    if (input.retmax !== undefined) eFetchParams.retmax = String(input.retmax);
  } else if (input.pmids && input.pmids.length > 0) {
    eFetchParams.id = input.pmids.join(",");
  }

  let serviceRetmode: "xml" | "text" = "xml";
  let rettype: string | undefined;

  switch (input.detailLevel) {
    case "full_xml":
      serviceRetmode = "xml";
      break;
    case "medline_text":
      serviceRetmode = "text";
      rettype = "medline";
      break;
    case "abstract_plus":
    case "citation_data":
      serviceRetmode = "xml";
      break;
  }
  eFetchParams.retmode = serviceRetmode;
  if (rettype) eFetchParams.rettype = rettype;

  const eFetchBase =
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi";
  const eFetchQueryString = new URLSearchParams(
    eFetchParams as Record<string, string>,
  ).toString();
  const eFetchUrl = `${eFetchBase}?${eFetchQueryString}`;

  const shouldReturnRawXml =
    input.detailLevel === "full_xml" && input.outputFormat === "raw_text";

  const eFetchResponseData = await ncbiService.eFetch(
    eFetchParams,
    toolLogicContext,
    { retmode: serviceRetmode, rettype, returnRawXml: shouldReturnRawXml },
  );

  let finalOutputText: string;
  let articlesCount = 0;

  if (input.detailLevel === "medline_text") {
    const medlineText = String(eFetchResponseData);
    const foundPmidsInMedline = new Set<string>();
    const pmidRegex = /^PMID- (\d+)/gm;
    let match;
    while ((match = pmidRegex.exec(medlineText)) !== null) {
      if (match[1]) {
        foundPmidsInMedline.add(match[1]);
      }
    }
    articlesCount = foundPmidsInMedline.size;

    if (input.outputFormat === "raw_text") {
      finalOutputText = medlineText;
    } else {
      const notFoundPmids =
        input.pmids?.filter((pmid) => !foundPmidsInMedline.has(pmid)) || [];
      finalOutputText = JSON.stringify({
        requestedPmids: input.pmids || "N/A (history query)",
        articles: [{ medlineText }],
        notFoundPmids,
        eFetchDetails: { urls: [eFetchUrl] },
      });
    }
  } else if (input.detailLevel === "full_xml") {
    const articlesXml = ensureArray(
      (eFetchResponseData as { PubmedArticleSet?: XmlPubmedArticleSet })
        ?.PubmedArticleSet?.PubmedArticle || [],
    );
    articlesCount = articlesXml.length;
    if (input.outputFormat === "raw_text") {
      // Note: Raw XML output is requested, but we still parse to get an accurate count.
      // This is a trade-off for robustness over performance in this specific case.
      finalOutputText = String(eFetchResponseData);
    } else {
      const foundPmidsInXml = new Set<string>();
      const articlesPayload = articlesXml.map((articleXml) => {
        const pmid = extractPmid(articleXml.MedlineCitation) || "unknown_pmid";
        if (pmid !== "unknown_pmid") foundPmidsInXml.add(pmid);
        return { pmid, fullXmlContent: articleXml };
      });
      const notFoundPmids =
        input.pmids?.filter((pmid) => !foundPmidsInXml.has(pmid)) || [];
      finalOutputText = JSON.stringify({
        requestedPmids: input.pmids || "N/A (history query)",
        articles: articlesPayload,
        notFoundPmids,
        eFetchDetails: { urls: [eFetchUrl] },
      });
    }
  } else {
    const parsedArticles = parsePubMedArticleSet(
      eFetchResponseData as XmlPubmedArticleSet,
      input,
      toolLogicContext,
    );
    articlesCount = parsedArticles.length;
    const foundPmids = new Set(parsedArticles.map((p) => p.pmid));
    const notFoundPmids =
      input.pmids?.filter((pmid) => !foundPmids.has(pmid)) || [];

    let articlesToReturn: ParsedArticle[] | Record<string, unknown>[] =
      parsedArticles;
    if (input.detailLevel === "citation_data") {
      articlesToReturn = parsedArticles.map((article) => ({
        pmid: article.pmid,
        title: article.title,
        authors: article.authors?.map((a) => ({
          lastName: a.lastName,
          initials: a.initials,
        })),
        journalInfo: {
          title: article.journalInfo?.title,
          isoAbbreviation: article.journalInfo?.isoAbbreviation,
          volume: article.journalInfo?.volume,
          issue: article.journalInfo?.issue,
          pages: article.journalInfo?.pages,
          year: article.journalInfo?.publicationDate?.year,
        },
        doi: article.doi,
        ...(input.includeMeshTerms && { meshTerms: article.meshTerms }),
      }));
    }
    finalOutputText = JSON.stringify({
      requestedPmids: input.pmids || "N/A (history query)",
      articles: articlesToReturn,
      notFoundPmids,
      eFetchDetails: { urls: [eFetchUrl] },
    });
  }

  logger.notice("Successfully executed pubmed_fetch_contents tool.", {
    ...toolLogicContext,
    articlesReturned: articlesCount,
  });

  return {
    content: finalOutputText,
    articlesReturned: articlesCount,
    eFetchUrl,
  };
}
