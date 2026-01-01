/**
 * @fileoverview Shared type definitions for the pubmedArticleConnections tool logic.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/types
 */
import type { PubMedArticleConnectionsInput } from "./index.js";
export interface RelatedArticle {
    pmid: string;
    title?: string;
    authors?: string;
    score?: number;
    linkUrl: string;
}
export interface CitationOutput {
    ris?: string;
    bibtex?: string;
    apa_string?: string;
    mla_string?: string;
}
export interface ToolOutputData {
    sourcePmid: string;
    relationshipType: PubMedArticleConnectionsInput["relationshipType"];
    relatedArticles: RelatedArticle[];
    citations: CitationOutput;
    retrievedCount: number;
    eUtilityUrl?: string;
    message?: string;
}
//# sourceMappingURL=types.d.ts.map