/**
 * @fileoverview Provides utility functions for parsing natural language date strings
 * into Date objects or detailed parsing results using the `chrono-node` library.
 * @module src/utils/parsing/dateParser
 */
import * as chrono from "chrono-node";
import { RequestContext } from "../index.js";
/**
 * Parses a natural language date string into a JavaScript Date object.
 * Uses `chrono.parseDate` for lenient parsing of various date formats.
 *
 * @param text - The natural language date string to parse.
 * @param context - The request context for logging and error tracking.
 * @param refDate - Optional reference date for parsing relative dates. Defaults to current date/time.
 * @returns A promise resolving with a Date object or `null` if parsing fails.
 * @throws {McpError} If an unexpected error occurs during parsing.
 * @private
 */
export declare function parseDateString(text: string, context: RequestContext, refDate?: Date): Promise<Date | null>;
/**
 * Parses a natural language date string and returns detailed parsing results.
 * Provides more information than just the Date object, including matched text and components.
 *
 * @param text - The natural language date string to parse.
 * @param context - The request context for logging and error tracking.
 * @param refDate - Optional reference date for parsing relative dates. Defaults to current date/time.
 * @returns A promise resolving with an array of `chrono.ParsedResult` objects. Empty if no dates found.
 * @throws {McpError} If an unexpected error occurs during parsing.
 * @private
 */
export declare function parseDateStringDetailed(text: string, context: RequestContext, refDate?: Date): Promise<chrono.ParsedResult[]>;
/**
 * An object providing date parsing functionalities.
 *
 * @example
 * ```typescript
 * import { dateParser, requestContextService } from './utils'; // Assuming utils/index.js exports these
 * const context = requestContextService.createRequestContext({ operation: 'TestDateParsing' });
 *
 * async function testParsing() {
 *   const dateObj = await dateParser.parseDate("next Friday at 3pm", context);
 *   if (dateObj) {
 *     console.log("Parsed Date:", dateObj.toISOString());
 *   }
 *
 *   const detailedResults = await dateParser.parse("Meeting on 2024-12-25 and another one tomorrow", context);
 *   detailedResults.forEach(result => {
 *     console.log("Detailed Result:", result.text, result.start.date());
 *   });
 * }
 * testParsing();
 * ```
 */
export declare const dateParser: {
    /**
     * Parses a natural language date string and returns detailed parsing results
     * from `chrono-node`.
     * @param text - The natural language date string to parse.
     * @param context - The request context for logging and error tracking.
     * @param refDate - Optional reference date for parsing relative dates.
     * @returns A promise resolving with an array of `chrono.ParsedResult` objects.
     */
    parse: typeof parseDateStringDetailed;
    /**
     * Parses a natural language date string into a single JavaScript Date object.
     * @param text - The natural language date string to parse.
     * @param context - The request context for logging and error tracking.
     * @param refDate - Optional reference date for parsing relative dates.
     * @returns A promise resolving with a Date object or `null`.
     */
    parseDate: typeof parseDateString;
};
//# sourceMappingURL=dateParser.d.ts.map