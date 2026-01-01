/**
 * @fileoverview Logic for the pubmed_fetch_contents MCP tool.
 * Handles EFetch queries for specific PMIDs and formats the results.
 * This tool can fetch various details from PubMed including abstracts, full XML,
 * MEDLINE text, and citation data.
 * @module src/mcp-server/tools/pubmedFetchContents/logic
 */
import { z } from "zod";
import { RequestContext } from "../../../utils/index.js";
export declare const PubMedFetchContentsInputSchema: z.ZodEffects<z.ZodObject<{
    pmids: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    queryKey: z.ZodOptional<z.ZodString>;
    webEnv: z.ZodOptional<z.ZodString>;
    retstart: z.ZodOptional<z.ZodNumber>;
    retmax: z.ZodOptional<z.ZodNumber>;
    detailLevel: z.ZodDefault<z.ZodOptional<z.ZodEnum<["abstract_plus", "full_xml", "medline_text", "citation_data"]>>>;
    includeMeshTerms: z.ZodDefault<z.ZodOptional<z.ZodBoolean>>;
    includeGrantInfo: z.ZodDefault<z.ZodOptional<z.ZodBoolean>>;
    outputFormat: z.ZodDefault<z.ZodOptional<z.ZodEnum<["json", "raw_text"]>>>;
}, "strip", z.ZodTypeAny, {
    detailLevel: "abstract_plus" | "full_xml" | "medline_text" | "citation_data";
    includeMeshTerms: boolean;
    includeGrantInfo: boolean;
    outputFormat: "json" | "raw_text";
    queryKey?: string | undefined;
    webEnv?: string | undefined;
    retmax?: number | undefined;
    retstart?: number | undefined;
    pmids?: string[] | undefined;
}, {
    queryKey?: string | undefined;
    webEnv?: string | undefined;
    retmax?: number | undefined;
    retstart?: number | undefined;
    pmids?: string[] | undefined;
    detailLevel?: "abstract_plus" | "full_xml" | "medline_text" | "citation_data" | undefined;
    includeMeshTerms?: boolean | undefined;
    includeGrantInfo?: boolean | undefined;
    outputFormat?: "json" | "raw_text" | undefined;
}>, {
    detailLevel: "abstract_plus" | "full_xml" | "medline_text" | "citation_data";
    includeMeshTerms: boolean;
    includeGrantInfo: boolean;
    outputFormat: "json" | "raw_text";
    queryKey?: string | undefined;
    webEnv?: string | undefined;
    retmax?: number | undefined;
    retstart?: number | undefined;
    pmids?: string[] | undefined;
}, {
    queryKey?: string | undefined;
    webEnv?: string | undefined;
    retmax?: number | undefined;
    retstart?: number | undefined;
    pmids?: string[] | undefined;
    detailLevel?: "abstract_plus" | "full_xml" | "medline_text" | "citation_data" | undefined;
    includeMeshTerms?: boolean | undefined;
    includeGrantInfo?: boolean | undefined;
    outputFormat?: "json" | "raw_text" | undefined;
}>;
export type PubMedFetchContentsInput = z.infer<typeof PubMedFetchContentsInputSchema>;
export type PubMedFetchContentsOutput = {
    content: string;
    articlesReturned: number;
    eFetchUrl: string;
};
export declare function pubMedFetchContentsLogic(input: PubMedFetchContentsInput, parentRequestContext: RequestContext): Promise<PubMedFetchContentsOutput>;
//# sourceMappingURL=logic.d.ts.map