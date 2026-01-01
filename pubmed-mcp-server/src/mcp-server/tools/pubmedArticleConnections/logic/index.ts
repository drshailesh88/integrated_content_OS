/**
 * @fileoverview Main logic handler for the 'pubmed_article_connections' MCP tool.
 * Orchestrates calls to ELink or citation formatting handlers.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/index
 */

import { z } from "zod";
import { BaseErrorCode, McpError } from "../../../../types-global/errors.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../../utils/index.js";
import { handleCitationFormats } from "./citationFormatter.js";
import { handleELinkRelationships } from "./elinkHandler.js";
import type { ToolOutputData } from "./types.js";

/**
 * Zod schema for the input parameters of the 'pubmed_article_connections' tool.
 */
export const PubMedArticleConnectionsInputSchema = z.object({
  sourcePmid: z
    .string()
    .regex(/^\d+$/)
    .describe(
      "The PubMed Unique Identifier (PMID) of the source article for which to find connections or format citations. This PMID must be a valid number string.",
    ),
  relationshipType: z
    .enum([
      "pubmed_similar_articles",
      "pubmed_citedin",
      "pubmed_references",
      "citation_formats",
    ])
    .default("pubmed_similar_articles")
    .describe(
      "Specifies the type of connection or action: 'pubmed_similar_articles' (finds similar articles), 'pubmed_citedin' (finds citing articles), 'pubmed_references' (finds referenced articles), or 'citation_formats' (retrieves formatted citations).",
    ),
  maxRelatedResults: z
    .number()
    .int()
    .positive()
    .max(50, "Maximum 50 related results can be requested.")
    .optional()
    .default(5)
    .describe(
      "Maximum number of related articles to retrieve for relationship-based searches. Default is 5, max is 50.",
    ),
  citationStyles: z
    .array(z.enum(["ris", "bibtex", "apa_string", "mla_string"]))
    .optional()
    .default(["ris"])
    .describe(
      "An array of citation styles to format the source article into when 'relationshipType' is 'citation_formats'. Supported styles: 'ris', 'bibtex', 'apa_string', 'mla_string'. Default is ['ris'].",
    ),
});

/**
 * Type alias for the validated input of the 'pubmed_article_connections' tool.
 */
export type PubMedArticleConnectionsInput = z.infer<
  typeof PubMedArticleConnectionsInputSchema
>;

/**
 * Main handler for the 'pubmed_article_connections' tool.
 * @param {PubMedArticleConnectionsInput} input - Validated input parameters.
 * @param {RequestContext} context - The request context for this tool invocation.
 * @returns {Promise<ToolOutputData>} The result of the tool call.
 */
export async function handlePubMedArticleConnections(
  input: PubMedArticleConnectionsInput,
  context: RequestContext,
): Promise<ToolOutputData> {
  const toolLogicContext = requestContextService.createRequestContext({
    parentRequestId: context.requestId,
    operation: "handlePubMedArticleConnections",
    toolName: "pubmed_article_connections",
    input: sanitizeInputForLogging(input),
  });

  logger.info("Executing pubmed_article_connections tool", toolLogicContext);

  const outputData: ToolOutputData = {
    sourcePmid: input.sourcePmid,
    relationshipType: input.relationshipType,
    relatedArticles: [],
    citations: {},
    retrievedCount: 0,
    eUtilityUrl: undefined,
    message: undefined,
  };

  switch (input.relationshipType) {
    case "pubmed_similar_articles":
    case "pubmed_citedin":
    case "pubmed_references":
      await handleELinkRelationships(input, outputData, toolLogicContext);
      break;
    case "citation_formats":
      await handleCitationFormats(input, outputData, toolLogicContext);
      break;
    default:
      throw new McpError(
        BaseErrorCode.VALIDATION_ERROR,
        `Unsupported relationshipType: ${input.relationshipType}`,
        { ...toolLogicContext, receivedType: input.relationshipType },
      );
  }

  if (
    outputData.retrievedCount === 0 &&
    !outputData.message &&
    (input.relationshipType !== "citation_formats" ||
      Object.keys(outputData.citations).length === 0)
  ) {
    outputData.message = "No results found for the given parameters.";
  }

  logger.notice("Successfully executed pubmed_article_connections tool.", {
    ...toolLogicContext,
    relationshipType: input.relationshipType,
    retrievedCount: outputData.retrievedCount,
    citationsGenerated: Object.keys(outputData.citations).length,
  });

  return outputData;
}
