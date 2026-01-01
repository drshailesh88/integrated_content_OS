/**
 * @fileoverview Helper functions for parsing ESummary results from NCBI.
 * Handles different ESummary XML structures and formats the data into
 * consistent ParsedBriefSummary objects.
 * @module src/services/NCBI/parsing/eSummaryResultParser
 */
import { ESummaryResult, ParsedBriefSummary, ESummaryAuthor as XmlESummaryAuthor } from "../../../types-global/pubmedXml.js";
import { RequestContext } from "../../../utils/index.js";
/**
 * Formats an array of ESummary authors into a string.
 * Limits to the first 3 authors and adds "et al." if more exist.
 * @param authors - Array of ESummary author objects (normalized).
 * @returns A string like "Doe J, Smith A, Brown B, et al." or empty if no authors.
 */
export declare function formatESummaryAuthors(authors?: XmlESummaryAuthor[]): string;
/**
 * Standardizes date strings from ESummary to "YYYY-MM-DD" format.
 * Uses the dateParser utility.
 * @param dateStr - Date string from ESummary (e.g., "2023/01/15", "2023 Jan 15", "2023").
 * @param parentContext - Optional parent request context for logging.
 * @returns A promise resolving to a standardized date string ("YYYY-MM-DD") or undefined if parsing fails.
 */
export declare function standardizeESummaryDate(dateStr?: string, parentContext?: RequestContext): Promise<string | undefined>;
/**
 * Extracts and formats brief summaries from ESummary XML result.
 * Handles both DocumentSummarySet (newer) and older DocSum structures.
 * Asynchronously standardizes dates.
 * @param eSummaryResult - The parsed XML object from ESummary (eSummaryResult part).
 * @param context - Request context for logging and passing to date standardization.
 * @returns A promise resolving to an array of parsed brief summary objects.
 */
export declare function extractBriefSummaries(eSummaryResult?: ESummaryResult, context?: RequestContext): Promise<ParsedBriefSummary[]>;
//# sourceMappingURL=eSummaryResultParser.d.ts.map