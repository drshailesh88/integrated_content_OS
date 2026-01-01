/**
 * @fileoverview Constants and shared type definitions for NCBI E-utility interactions.
 * @module src/services/NCBI/core/ncbiConstants
 */
export declare const NCBI_EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils";
/**
 * Interface for common NCBI E-utility request parameters.
 * Specific E-utilities will have additional parameters.
 */
export interface NcbiRequestParams {
    db?: string;
    [key: string]: string | number | undefined;
}
/**
 * Interface for options controlling how NCBI requests are made and responses are handled.
 */
export interface NcbiRequestOptions {
    retmode?: "xml" | "json" | "text";
    rettype?: string;
    usePost?: boolean;
    returnRawXml?: boolean;
}
//# sourceMappingURL=ncbiConstants.d.ts.map