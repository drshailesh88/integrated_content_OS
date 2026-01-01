import { BaseErrorCode } from "../../types-global/errors.js";
/**
 * Defines a generic structure for providing context with errors.
 * This context can include identifiers like `requestId` or any other relevant
 * key-value pairs that aid in debugging or understanding the error's circumstances.
 */
export interface ErrorContext {
    /**
     * A unique identifier for the request or operation during which the error occurred.
     * Useful for tracing errors through logs and distributed systems.
     */
    requestId?: string;
    /**
     * Allows for arbitrary additional context information.
     * Keys are strings, and values can be of any type.
     */
    [key: string]: unknown;
}
/**
 * Configuration options for the `ErrorHandler.handleError` method.
 * These options control how an error is processed, logged, and whether it's rethrown.
 */
export interface ErrorHandlerOptions {
    /**
     * The context of the operation that caused the error.
     * This can include `requestId` and other relevant debugging information.
     */
    context?: ErrorContext;
    /**
     * A descriptive name of the operation being performed when the error occurred.
     * This helps in identifying the source or nature of the error in logs.
     * Example: "UserLogin", "ProcessPayment", "FetchUserProfile".
     */
    operation: string;
    /**
     * The input data or parameters that were being processed when the error occurred.
     * This input will be sanitized before logging to prevent sensitive data exposure.
     */
    input?: unknown;
    /**
     * If true, the (potentially transformed) error will be rethrown after handling.
     * Defaults to `false`.
     */
    rethrow?: boolean;
    /**
     * A specific `BaseErrorCode` to assign to the error, overriding any
     * automatically determined error code.
     */
    errorCode?: BaseErrorCode;
    /**
     * A custom function to map or transform the original error into a new `Error` instance.
     * If provided, this function is used instead of the default `McpError` creation.
     * @param error - The original error that occurred.
     * @returns The transformed error.
     */
    errorMapper?: (error: unknown) => Error;
    /**
     * If true, stack traces will be included in the logs.
     * Defaults to `true`.
     */
    includeStack?: boolean;
    /**
     * If true, indicates that the error is critical and might require immediate attention
     * or could lead to system instability. This is primarily for logging and alerting.
     * Defaults to `false`.
     */
    critical?: boolean;
}
/**
 * Defines a basic rule for mapping errors based on patterns.
 * Used internally by `COMMON_ERROR_PATTERNS` and as a base for `ErrorMapping`.
 */
export interface BaseErrorMapping {
    /**
     * A string or regular expression to match against the error message.
     * If a string is provided, it's typically used for substring matching (case-insensitive).
     */
    pattern: string | RegExp;
    /**
     * The `BaseErrorCode` to assign if the pattern matches.
     */
    errorCode: BaseErrorCode;
    /**
     * An optional custom message template for the mapped error.
     * (Note: This property is defined but not directly used by `ErrorHandler.determineErrorCode`
     * which focuses on `errorCode`. It's more relevant for custom mapping logic.)
     */
    messageTemplate?: string;
}
/**
 * Extends `BaseErrorMapping` to include a factory function for creating
 * specific error instances and additional context for the mapping.
 * Used by `ErrorHandler.mapError`.
 * @template T The type of `Error` this mapping will produce, defaults to `Error`.
 */
export interface ErrorMapping<T extends Error = Error> extends BaseErrorMapping {
    /**
     * A factory function that creates and returns an instance of the mapped error type `T`.
     * @param error - The original error that occurred.
     * @param context - Optional additional context provided in the mapping rule.
     * @returns The newly created error instance.
     */
    factory: (error: unknown, context?: Record<string, unknown>) => T;
    /**
     * Additional static context to be merged or passed to the `factory` function
     * when this mapping rule is applied.
     */
    additionalContext?: Record<string, unknown>;
}
/**
 * A utility class providing static methods for comprehensive error handling.
 */
export declare class ErrorHandler {
    /**
     * Determines an appropriate `BaseErrorCode` for a given error.
     * Checks `McpError` instances, `ERROR_TYPE_MAPPINGS`, and `COMMON_ERROR_PATTERNS`.
     * Defaults to `BaseErrorCode.INTERNAL_ERROR`.
     * @param error - The error instance or value to classify.
     * @returns The determined error code.
     */
    static determineErrorCode(error: unknown): BaseErrorCode;
    /**
     * Handles an error with consistent logging and optional transformation.
     * Sanitizes input, determines error code, logs details, and can rethrow.
     * @param error - The error instance or value that occurred.
     * @param options - Configuration for handling the error.
     * @returns The handled (and potentially transformed) error instance.
     */
    static handleError(error: unknown, options: ErrorHandlerOptions): Error;
    /**
     * Maps an error to a specific error type `T` based on `ErrorMapping` rules.
     * Returns original/default error if no mapping matches.
     * @template T The target error type, extending `Error`.
     * @param error - The error instance or value to map.
     * @param mappings - An array of mapping rules to apply.
     * @param defaultFactory - Optional factory for a default error if no mapping matches.
     * @returns The mapped error of type `T`, or the original/defaulted error.
     */
    static mapError<T extends Error>(error: unknown, mappings: ReadonlyArray<ErrorMapping<T>>, defaultFactory?: (error: unknown, context?: Record<string, unknown>) => T): T | Error;
    /**
     * Formats an error into a consistent object structure for API responses or structured logging.
     * @param error - The error instance or value to format.
     * @returns A structured representation of the error.
     */
    static formatError(error: unknown): Record<string, unknown>;
    /**
     * Safely executes a function (sync or async) and handles errors using `ErrorHandler.handleError`.
     * The error is always rethrown.
     * @template T The expected return type of the function `fn`.
     * @param fn - The function to execute.
     * @param options - Error handling options (excluding `rethrow`).
     * @returns A promise resolving with the result of `fn` if successful.
     * @throws {McpError | Error} The error processed by `ErrorHandler.handleError`.
     * @example
     * ```typescript
     * async function fetchData(userId: string, context: RequestContext) {
     *   return ErrorHandler.tryCatch(
     *     async () => {
     *       const response = await fetch(`/api/users/${userId}`);
     *       if (!response.ok) throw new Error(`Failed to fetch user: ${response.status}`);
     *       return response.json();
     *     },
     *     { operation: 'fetchUserData', context, input: { userId } }
     *   );
     * }
     * ```
     */
    static tryCatch<T>(fn: () => Promise<T> | T, options: Omit<ErrorHandlerOptions, "rethrow">): Promise<T>;
}
//# sourceMappingURL=errorHandler.d.ts.map