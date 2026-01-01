/**
 * @fileoverview Generic helper functions for parsing XML data, particularly
 * structures from fast-xml-parser.
 * @module src/services/NCBI/parsing/xmlGenericHelpers
 */
/**
 * Ensures that the input is an array. If it's not an array, it wraps it in one.
 * Handles undefined or null by returning an empty array.
 * @param item - The item to ensure is an array.
 * @returns An array containing the item, or an empty array if item is null/undefined.
 * @template T - The type of the items in the array.
 */
export declare function ensureArray<T>(item: T | T[] | undefined | null): T[];
/**
 * Safely extracts text content from an XML element, which might be a string or an object with a "#text" property.
 * Handles cases where #text might be a number or boolean by converting to string.
 * @param element - The XML element (string, object with #text, or undefined).
 * @param defaultValue - The value to return if text cannot be extracted. Defaults to an empty string.
 * @returns The text content or the default value.
 */
export declare function getText(element: unknown, defaultValue?: string): string;
/**
 * Safely extracts an attribute value from an XML element.
 * Assumes attributes are prefixed with "@_" by fast-xml-parser.
 * @param element - The XML element object.
 * @param attributeName - The name of the attribute (e.g., "_UI", "_MajorTopicYN", without the "@_" prefix).
 * @param defaultValue - The value to return if the attribute is not found. Defaults to an empty string.
 * @returns The attribute value or the default value.
 */
export declare function getAttribute(element: unknown, attributeName: string, // e.g., "UI", "MajorTopicYN"
defaultValue?: string): string;
//# sourceMappingURL=xmlGenericHelpers.d.ts.map