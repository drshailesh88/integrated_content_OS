/**
 * @fileoverview This module provides utilities for robust error handling.
 * It defines structures for error context, options for handling errors,
 * and mappings for classifying errors. The main `ErrorHandler` class
 * offers static methods for consistent error processing, logging, and transformation.
 * @module src/utils/internal/errorHandler
 */
import { SpanStatusCode, trace } from "@opentelemetry/api";
import { BaseErrorCode, McpError } from "../../types-global/errors.js";
import { generateUUID, sanitizeInputForLogging } from "../index.js";
import { logger } from "./logger.js";
/**
 * Maps standard JavaScript error constructor names to `BaseErrorCode` values.
 * @private
 */
const ERROR_TYPE_MAPPINGS = {
    SyntaxError: BaseErrorCode.VALIDATION_ERROR,
    TypeError: BaseErrorCode.VALIDATION_ERROR,
    ReferenceError: BaseErrorCode.INTERNAL_ERROR,
    RangeError: BaseErrorCode.VALIDATION_ERROR,
    URIError: BaseErrorCode.VALIDATION_ERROR,
    EvalError: BaseErrorCode.INTERNAL_ERROR,
};
/**
 * Array of `BaseErrorMapping` rules to classify errors by message/name patterns.
 * Order matters: more specific patterns should precede generic ones.
 * @private
 */
const COMMON_ERROR_PATTERNS = [
    {
        pattern: /auth|unauthorized|unauthenticated|not.*logged.*in|invalid.*token|expired.*token/i,
        errorCode: BaseErrorCode.UNAUTHORIZED,
    },
    {
        pattern: /permission|forbidden|access.*denied|not.*allowed/i,
        errorCode: BaseErrorCode.FORBIDDEN,
    },
    {
        pattern: /not found|missing|no such|doesn't exist|couldn't find/i,
        errorCode: BaseErrorCode.NOT_FOUND,
    },
    {
        pattern: /invalid|validation|malformed|bad request|wrong format|missing required/i,
        errorCode: BaseErrorCode.VALIDATION_ERROR,
    },
    {
        pattern: /conflict|already exists|duplicate|unique constraint/i,
        errorCode: BaseErrorCode.CONFLICT,
    },
    {
        pattern: /rate limit|too many requests|throttled/i,
        errorCode: BaseErrorCode.RATE_LIMITED,
    },
    {
        pattern: /timeout|timed out|deadline exceeded/i,
        errorCode: BaseErrorCode.TIMEOUT,
    },
    {
        pattern: /service unavailable|bad gateway|gateway timeout|upstream error/i,
        errorCode: BaseErrorCode.SERVICE_UNAVAILABLE,
    },
];
/**
 * Creates a "safe" RegExp for testing error messages.
 * Ensures case-insensitivity and removes the global flag.
 * @param pattern - The string or RegExp pattern.
 * @returns A new RegExp instance.
 * @private
 */
function createSafeRegex(pattern) {
    if (pattern instanceof RegExp) {
        let flags = pattern.flags.replace("g", "");
        if (!flags.includes("i")) {
            flags += "i";
        }
        return new RegExp(pattern.source, flags);
    }
    return new RegExp(pattern, "i");
}
/**
 * Retrieves a descriptive name for an error object or value.
 * @param error - The error object or value.
 * @returns A string representing the error's name or type.
 * @private
 */
function getErrorName(error) {
    if (error instanceof Error) {
        return error.name || "Error";
    }
    if (error === null) {
        return "NullValueEncountered";
    }
    if (error === undefined) {
        return "UndefinedValueEncountered";
    }
    if (typeof error === "object" &&
        error !== null &&
        error.constructor &&
        typeof error.constructor.name === "string" &&
        error.constructor.name !== "Object") {
        return `${error.constructor.name}Encountered`;
    }
    return `${typeof error}Encountered`;
}
/**
 * Extracts a message string from an error object or value.
 * @param error - The error object or value.
 * @returns The error message string.
 * @private
 */
function getErrorMessage(error) {
    if (error instanceof Error) {
        return error.message;
    }
    if (error === null) {
        return "Null value encountered as error";
    }
    if (error === undefined) {
        return "Undefined value encountered as error";
    }
    if (typeof error === "string") {
        return error;
    }
    try {
        const str = String(error);
        if (str === "[object Object]" && error !== null) {
            try {
                return `Non-Error object encountered: ${JSON.stringify(error)}`;
            }
            catch {
                return `Unstringifyable non-Error object encountered (constructor: ${error.constructor?.name || "Unknown"})`;
            }
        }
        return str;
    }
    catch (e) {
        return `Error converting error to string: ${e instanceof Error ? e.message : "Unknown conversion error"}`;
    }
}
/**
 * A utility class providing static methods for comprehensive error handling.
 */
export class ErrorHandler {
    /**
     * Determines an appropriate `BaseErrorCode` for a given error.
     * Checks `McpError` instances, `ERROR_TYPE_MAPPINGS`, and `COMMON_ERROR_PATTERNS`.
     * Defaults to `BaseErrorCode.INTERNAL_ERROR`.
     * @param error - The error instance or value to classify.
     * @returns The determined error code.
     */
    static determineErrorCode(error) {
        if (error instanceof McpError) {
            return error.code;
        }
        const errorName = getErrorName(error);
        const errorMessage = getErrorMessage(error);
        const mappedFromType = ERROR_TYPE_MAPPINGS[errorName];
        if (mappedFromType) {
            return mappedFromType;
        }
        for (const mapping of COMMON_ERROR_PATTERNS) {
            const regex = createSafeRegex(mapping.pattern);
            if (regex.test(errorMessage) || regex.test(errorName)) {
                return mapping.errorCode;
            }
        }
        return BaseErrorCode.INTERNAL_ERROR;
    }
    /**
     * Handles an error with consistent logging and optional transformation.
     * Sanitizes input, determines error code, logs details, and can rethrow.
     * @param error - The error instance or value that occurred.
     * @param options - Configuration for handling the error.
     * @returns The handled (and potentially transformed) error instance.
     */
    static handleError(error, options) {
        // --- OpenTelemetry Integration ---
        const activeSpan = trace.getActiveSpan();
        if (activeSpan) {
            if (error instanceof Error) {
                activeSpan.recordException(error);
            }
            activeSpan.setStatus({
                code: SpanStatusCode.ERROR,
                message: error instanceof Error ? error.message : String(error),
            });
        }
        // --- End OpenTelemetry Integration ---
        const { context = {}, operation, input, rethrow = false, errorCode: explicitErrorCode, includeStack = true, critical = false, errorMapper, } = options;
        const sanitizedInput = input !== undefined ? sanitizeInputForLogging(input) : undefined;
        const originalErrorName = getErrorName(error);
        const originalErrorMessage = getErrorMessage(error);
        const originalStack = error instanceof Error ? error.stack : undefined;
        let finalError;
        let loggedErrorCode;
        const errorDetailsSeed = error instanceof McpError &&
            typeof error.details === "object" &&
            error.details !== null
            ? { ...error.details }
            : {};
        const consolidatedDetails = {
            ...errorDetailsSeed,
            ...context,
            originalErrorName,
            originalMessage: originalErrorMessage,
        };
        if (originalStack &&
            !(error instanceof McpError && error.details?.originalStack)) {
            consolidatedDetails.originalStack = originalStack;
        }
        const cause = error instanceof Error ? error : undefined;
        if (error instanceof McpError) {
            loggedErrorCode = error.code;
            finalError = errorMapper
                ? errorMapper(error)
                : new McpError(error.code, error.message, {
                    ...consolidatedDetails,
                    cause,
                });
        }
        else {
            loggedErrorCode =
                explicitErrorCode || ErrorHandler.determineErrorCode(error);
            const message = `Error in ${operation}: ${originalErrorMessage}`;
            finalError = errorMapper
                ? errorMapper(error)
                : new McpError(loggedErrorCode, message, {
                    ...consolidatedDetails,
                    cause,
                });
        }
        if (finalError !== error &&
            error instanceof Error &&
            finalError instanceof Error &&
            !finalError.stack &&
            error.stack) {
            finalError.stack = error.stack;
        }
        const logRequestId = typeof context.requestId === "string" && context.requestId
            ? context.requestId
            : generateUUID();
        const logTimestamp = typeof context.timestamp === "string" && context.timestamp
            ? context.timestamp
            : new Date().toISOString();
        const logPayload = {
            ...Object.fromEntries(Object.entries(context).filter(([key]) => key !== "requestId" && key !== "timestamp")),
            requestId: logRequestId,
            timestamp: logTimestamp,
            operation,
            input: sanitizedInput,
            critical,
            errorCode: loggedErrorCode,
            originalErrorType: originalErrorName,
            finalErrorType: getErrorName(finalError),
        };
        if (finalError instanceof McpError && finalError.details) {
            logPayload.errorDetails = finalError.details;
        }
        else {
            logPayload.errorDetails = consolidatedDetails;
        }
        if (includeStack) {
            const stack = finalError instanceof Error ? finalError.stack : originalStack;
            if (stack) {
                logPayload.stack = stack;
            }
        }
        logger.error(finalError.message || originalErrorMessage, logPayload);
        if (rethrow) {
            throw finalError;
        }
        return finalError;
    }
    /**
     * Maps an error to a specific error type `T` based on `ErrorMapping` rules.
     * Returns original/default error if no mapping matches.
     * @template T The target error type, extending `Error`.
     * @param error - The error instance or value to map.
     * @param mappings - An array of mapping rules to apply.
     * @param defaultFactory - Optional factory for a default error if no mapping matches.
     * @returns The mapped error of type `T`, or the original/defaulted error.
     */
    static mapError(error, mappings, defaultFactory) {
        const errorMessage = getErrorMessage(error);
        const errorName = getErrorName(error);
        for (const mapping of mappings) {
            const regex = createSafeRegex(mapping.pattern);
            if (regex.test(errorMessage) || regex.test(errorName)) {
                return mapping.factory(error, mapping.additionalContext);
            }
        }
        if (defaultFactory) {
            return defaultFactory(error);
        }
        return error instanceof Error ? error : new Error(String(error));
    }
    /**
     * Formats an error into a consistent object structure for API responses or structured logging.
     * @param error - The error instance or value to format.
     * @returns A structured representation of the error.
     */
    static formatError(error) {
        if (error instanceof McpError) {
            return {
                code: error.code,
                message: error.message,
                details: typeof error.details === "object" && error.details !== null
                    ? error.details
                    : {},
            };
        }
        if (error instanceof Error) {
            return {
                code: ErrorHandler.determineErrorCode(error),
                message: error.message,
                details: { errorType: error.name || "Error" },
            };
        }
        return {
            code: BaseErrorCode.UNKNOWN_ERROR,
            message: getErrorMessage(error),
            details: { errorType: getErrorName(error) },
        };
    }
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
    static async tryCatch(fn, options) {
        try {
            return await Promise.resolve(fn());
        }
        catch (error) {
            // ErrorHandler.handleError will return the error to be thrown.
            throw ErrorHandler.handleError(error, { ...options, rethrow: true });
        }
    }
}
//# sourceMappingURL=errorHandler.js.map