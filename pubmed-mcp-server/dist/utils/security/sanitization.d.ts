import sanitizeHtml from "sanitize-html";
/**
 * Defines options for path sanitization to control how file paths are processed and validated.
 */
export interface PathSanitizeOptions {
    /** If provided, restricts sanitized paths to be relative to this directory. */
    rootDir?: string;
    /** If true, normalizes Windows backslashes to POSIX forward slashes. */
    toPosix?: boolean;
    /** If true, absolute paths are permitted (subject to `rootDir`). Default: false. */
    allowAbsolute?: boolean;
}
/**
 * Contains information about a path sanitization operation.
 */
export interface SanitizedPathInfo {
    /** The final sanitized and normalized path string. */
    sanitizedPath: string;
    /** The original path string before any processing. */
    originalInput: string;
    /** True if the input path was absolute after initial normalization. */
    wasAbsolute: boolean;
    /** True if an absolute path was converted to relative due to `allowAbsolute: false`. */
    convertedToRelative: boolean;
    /** The effective options used for sanitization, including defaults. */
    optionsUsed: PathSanitizeOptions;
}
/**
 * Defines options for context-specific string sanitization.
 */
export interface SanitizeStringOptions {
    /** The context in which the string will be used. 'javascript' is disallowed. */
    context?: "text" | "html" | "attribute" | "url" | "javascript";
    /** Custom allowed HTML tags if `context` is 'html'. */
    allowedTags?: string[];
    /** Custom allowed HTML attributes if `context` is 'html'. */
    allowedAttributes?: Record<string, string[]>;
}
/**
 * Configuration options for HTML sanitization, mirroring `sanitize-html` library options.
 */
export interface HtmlSanitizeConfig {
    /** An array of allowed HTML tag names. */
    allowedTags?: string[];
    /** Specifies allowed attributes, either globally or per tag. */
    allowedAttributes?: sanitizeHtml.IOptions["allowedAttributes"];
    /** If true, HTML comments are preserved. */
    preserveComments?: boolean;
    /** Custom functions to transform tags during sanitization. */
    transformTags?: sanitizeHtml.IOptions["transformTags"];
}
/**
 * A singleton class providing various methods for input sanitization.
 * Aims to protect against common vulnerabilities like XSS and path traversal.
 */
export declare class Sanitization {
    /** @private */
    private static instance;
    /**
     * Default list of field names considered sensitive for log redaction.
     * Case-insensitive matching is applied.
     * @private
     */
    private sensitiveFields;
    /**
     * Default configuration for HTML sanitization.
     * @private
     */
    private defaultHtmlSanitizeConfig;
    /** @private */
    private constructor();
    /**
     * Retrieves the singleton instance of the `Sanitization` class.
     * @returns The singleton `Sanitization` instance.
     */
    static getInstance(): Sanitization;
    /**
     * Sets or extends the list of sensitive field names for log sanitization.
     * @param fields - An array of field names to add to the sensitive list.
     */
    setSensitiveFields(fields: string[]): void;
    /**
     * Gets a copy of the current list of sensitive field names.
     * @returns An array of sensitive field names.
     */
    getSensitiveFields(): string[];
    /**
     * Sanitizes an HTML string by removing potentially malicious tags and attributes.
     * @param input - The HTML string to sanitize.
     * @param config - Optional custom configuration for `sanitize-html`.
     * @returns The sanitized HTML string. Returns an empty string if input is falsy.
     */
    sanitizeHtml(input: string, config?: HtmlSanitizeConfig): string;
    /**
     * Sanitizes a string based on its intended context (e.g., HTML, URL, text).
     * **Important:** `context: 'javascript'` is disallowed due to security risks.
     *
     * @param input - The string to sanitize.
     * @param options - Options specifying the sanitization context.
     * @returns The sanitized string. Returns an empty string if input is falsy.
     * @throws {McpError} If `options.context` is 'javascript', or URL validation fails.
     */
    sanitizeString(input: string, options?: SanitizeStringOptions): string;
    /**
     * Converts attribute format for `sanitizeHtml`.
     * @param attrs - Attributes in `{ tagName: ['attr1'] }` format.
     * @returns Attributes in `sanitize-html` expected format.
     * @private
     */
    private convertAttributesFormat;
    /**
     * Sanitizes a URL string by validating its format and protocol.
     * @param input - The URL string to sanitize.
     * @param allowedProtocols - Array of allowed URL protocols. Default: `['http', 'https']`.
     * @returns The sanitized and trimmed URL string.
     * @throws {McpError} If the URL is invalid or uses a disallowed protocol.
     */
    sanitizeUrl(input: string, allowedProtocols?: string[]): string;
    /**
     * Sanitizes a file path to prevent path traversal and normalize format.
     * @param input - The file path string to sanitize.
     * @param options - Options to control sanitization behavior.
     * @returns An object with the sanitized path and sanitization metadata.
     * @throws {McpError} If the path is invalid or unsafe.
     */
    sanitizePath(input: string, options?: PathSanitizeOptions): SanitizedPathInfo;
    /**
     * Sanitizes a JSON string by parsing it to validate its format.
     * Optionally checks if the JSON string exceeds a maximum allowed size.
     * @template T The expected type of the parsed JSON object. Defaults to `unknown`.
     * @param input - The JSON string to sanitize/validate.
     * @param maxSize - Optional maximum allowed size of the JSON string in bytes.
     * @returns The parsed JavaScript object.
     * @throws {McpError} If input is not a string, too large, or invalid JSON.
     */
    sanitizeJson<T = unknown>(input: string, maxSize?: number): T;
    /**
     * Validates and sanitizes a numeric input, converting strings to numbers.
     * Clamps the number to `min`/`max` if provided.
     * @param input - The number or string to validate and sanitize.
     * @param min - Minimum allowed value (inclusive).
     * @param max - Maximum allowed value (inclusive).
     * @returns The sanitized (and potentially clamped) number.
     * @throws {McpError} If input is not a valid number, NaN, or Infinity.
     */
    sanitizeNumber(input: number | string, min?: number, max?: number): number;
    /**
     * Sanitizes input for logging by redacting sensitive fields.
     * Creates a deep clone and replaces values of fields matching `this.sensitiveFields`
     * (case-insensitive substring match) with "[REDACTED]".
     *
     * It uses `structuredClone` if available for a high-fidelity deep clone.
     * If `structuredClone` is not available (e.g., in older Node.js environments),
     * it falls back to `JSON.parse(JSON.stringify(input))`. This fallback has limitations:
     * - `Date` objects are converted to ISO date strings.
     * - `undefined` values within objects are removed.
     * - `Map`, `Set`, `RegExp` objects are converted to empty objects (`{}`).
     * - Functions are removed.
     * - `BigInt` values will throw an error during `JSON.stringify` unless a `toJSON` method is provided.
     * - Circular references will cause `JSON.stringify` to throw an error.
     *
     * @param input - The input data to sanitize for logging.
     * @returns A sanitized (deep cloned) version of the input, safe for logging.
     *   Returns original input if not object/array, or "[Log Sanitization Failed]" on error.
     */
    sanitizeForLogging(input: unknown): unknown;
    /**
     * Recursively redacts sensitive fields in an object or array in place.
     * @param obj - The object or array to redact.
     * @private
     */
    private redactSensitiveFields;
}
/**
 * Singleton instance of the `Sanitization` class.
 * Use this for all input sanitization tasks.
 */
export declare const sanitization: Sanitization;
/**
 * Convenience function calling `sanitization.sanitizeForLogging`.
 * @param input - The input data to sanitize.
 * @returns A sanitized version of the input, safe for logging.
 */
export declare const sanitizeInputForLogging: (input: unknown) => unknown;
//# sourceMappingURL=sanitization.d.ts.map