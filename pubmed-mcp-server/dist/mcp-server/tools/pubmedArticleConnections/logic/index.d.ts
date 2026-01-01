/**
 * @fileoverview Main logic handler for the 'pubmed_article_connections' MCP tool.
 * Orchestrates calls to ELink or citation formatting handlers.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/index
 */
import { z } from "zod";
import { RequestContext } from "../../../../utils/index.js";
import type { ToolOutputData } from "./types.js";
/**
 * Zod schema for the input parameters of the 'pubmed_article_connections' tool.
 */
export declare const PubMedArticleConnectionsInputSchema: z.ZodObject<{
    sourcePmid: z.ZodString;
    relationshipType: z.ZodDefault<z.ZodEnum<["pubmed_similar_articles", "pubmed_citedin", "pubmed_references", "citation_formats"]>>;
    maxRelatedResults: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    citationStyles: z.ZodDefault<z.ZodOptional<z.ZodArray<z.ZodEnum<["ris", "bibtex", "apa_string", "mla_string"]>, "many">>>;
}, "strip", z.ZodTypeAny, {
    sourcePmid: string;
    relationshipType: "pubmed_similar_articles" | "pubmed_citedin" | "pubmed_references" | "citation_formats";
    maxRelatedResults: number;
    citationStyles: ("ris" | "bibtex" | "apa_string" | "mla_string")[];
}, {
    sourcePmid: string;
    relationshipType?: "pubmed_similar_articles" | "pubmed_citedin" | "pubmed_references" | "citation_formats" | undefined;
    maxRelatedResults?: number | undefined;
    citationStyles?: ("ris" | "bibtex" | "apa_string" | "mla_string")[] | undefined;
}>;
/**
 * Type alias for the validated input of the 'pubmed_article_connections' tool.
 */
export type PubMedArticleConnectionsInput = z.infer<typeof PubMedArticleConnectionsInputSchema>;
/**
 * Main handler for the 'pubmed_article_connections' tool.
 * @param {PubMedArticleConnectionsInput} input - Validated input parameters.
 * @param {RequestContext} context - The request context for this tool invocation.
 * @returns {Promise<ToolOutputData>} The result of the tool call.
 */
export declare function handlePubMedArticleConnections(input: PubMedArticleConnectionsInput, context: RequestContext): Promise<ToolOutputData>;
//# sourceMappingURL=index.d.ts.map