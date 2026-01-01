/**
 * @fileoverview Constants and shared type definitions for NCBI E-utility interactions.
 * @module src/services/NCBI/core/ncbiConstants
 */

export const NCBI_EUTILS_BASE_URL =
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils";

/**
 * Interface for common NCBI E-utility request parameters.
 * Specific E-utilities will have additional parameters.
 */
export interface NcbiRequestParams {
  db?: string; // Target database (e.g., "pubmed", "pmc"). Optional for EInfo to list all databases.
  [key: string]: string | number | undefined; // Allows for other E-utility specific parameters
}

/**
 * Interface for options controlling how NCBI requests are made and responses are handled.
 */
export interface NcbiRequestOptions {
  retmode?: "xml" | "json" | "text"; // Desired response format
  rettype?: string; // Specific type of data to return (e.g., "abstract", "medline")
  usePost?: boolean; // Hint to use HTTP POST for large payloads (e.g., many IDs)
  returnRawXml?: boolean; // If true and retmode is 'xml', returns the raw XML string instead of parsed object (after error checking)
}
