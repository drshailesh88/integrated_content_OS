/**
 * @fileoverview Logic for the pubmed_search_articles MCP tool.
 * Handles constructing ESearch and ESummary queries, interacting with
 * the NcbiService, and formatting the results.
 * @module src/mcp-server/tools/pubmedSearchArticles/logic
 */
import { z } from "zod";
import { ParsedBriefSummary } from "../../../types-global/pubmedXml.js";
import { RequestContext } from "../../../utils/index.js";
export declare const PubMedSearchArticlesInputSchema: z.ZodObject<{
    queryTerm: z.ZodString;
    maxResults: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    sortBy: z.ZodDefault<z.ZodOptional<z.ZodEnum<["relevance", "pub_date", "author", "journal_name"]>>>;
    dateRange: z.ZodOptional<z.ZodObject<{
        minDate: z.ZodOptional<z.ZodString>;
        maxDate: z.ZodOptional<z.ZodString>;
        dateType: z.ZodDefault<z.ZodOptional<z.ZodEnum<["pdat", "mdat", "edat"]>>>;
    }, "strip", z.ZodTypeAny, {
        dateType: "pdat" | "mdat" | "edat";
        minDate?: string | undefined;
        maxDate?: string | undefined;
    }, {
        minDate?: string | undefined;
        maxDate?: string | undefined;
        dateType?: "pdat" | "mdat" | "edat" | undefined;
    }>>;
    filterByPublicationTypes: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    fetchBriefSummaries: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
}, "strip", z.ZodTypeAny, {
    queryTerm: string;
    maxResults: number;
    sortBy: "author" | "relevance" | "pub_date" | "journal_name";
    fetchBriefSummaries: number;
    dateRange?: {
        dateType: "pdat" | "mdat" | "edat";
        minDate?: string | undefined;
        maxDate?: string | undefined;
    } | undefined;
    filterByPublicationTypes?: string[] | undefined;
}, {
    queryTerm: string;
    maxResults?: number | undefined;
    sortBy?: "author" | "relevance" | "pub_date" | "journal_name" | undefined;
    dateRange?: {
        minDate?: string | undefined;
        maxDate?: string | undefined;
        dateType?: "pdat" | "mdat" | "edat" | undefined;
    } | undefined;
    filterByPublicationTypes?: string[] | undefined;
    fetchBriefSummaries?: number | undefined;
}>;
export type PubMedSearchArticlesInput = z.infer<typeof PubMedSearchArticlesInputSchema>;
export type PubMedSearchArticlesOutput = {
    searchParameters: PubMedSearchArticlesInput;
    effectiveESearchTerm: string;
    totalFound: number;
    retrievedPmidCount: number;
    pmids: string[];
    briefSummaries: ParsedBriefSummary[];
    eSearchUrl: string;
    eSummaryUrl?: string;
};
export declare function pubmedSearchArticlesLogic(input: PubMedSearchArticlesInput, parentRequestContext: RequestContext): Promise<PubMedSearchArticlesOutput>;
//# sourceMappingURL=logic.d.ts.map