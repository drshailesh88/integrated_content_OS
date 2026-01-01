/**
 * @fileoverview Defines standardized error codes, a custom error class, and related schemas
 * for handling errors within the Model Context Protocol (MCP) server and its components.
 * This module provides a structured way to represent and communicate errors, ensuring
 * consistency and clarity for both server-side operations and client-side error handling.
 * @module src/types-global/errors
 */
import { z } from "zod";
/**
 * Defines a comprehensive set of standardized error codes for common issues encountered
 * within MCP servers, tools, or related operations. These codes are designed to help
 * clients and developers programmatically understand the nature of an error, facilitating
 * more precise error handling and debugging.
 */
export declare enum BaseErrorCode {
    /** Access denied due to invalid credentials or lack of authentication. */
    UNAUTHORIZED = "UNAUTHORIZED",
    /** Access denied despite valid authentication, due to insufficient permissions. */
    FORBIDDEN = "FORBIDDEN",
    /** The requested resource or entity could not be found. */
    NOT_FOUND = "NOT_FOUND",
    /** The request could not be completed due to a conflict with the current state of the resource. */
    CONFLICT = "CONFLICT",
    /** The request failed due to invalid input parameters or data. */
    VALIDATION_ERROR = "VALIDATION_ERROR",
    /** The provided input is invalid, but not necessarily a schema validation failure. */
    INVALID_INPUT = "INVALID_INPUT",
    /** An error occurred while parsing input data (e.g., date string, JSON). */
    PARSING_ERROR = "PARSING_ERROR",
    /** The request was rejected because the client has exceeded rate limits. */
    RATE_LIMITED = "RATE_LIMITED",
    /** The request timed out before a response could be generated. */
    TIMEOUT = "TIMEOUT",
    /** The service is temporarily unavailable, possibly due to maintenance or overload. */
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE",
    /** An unexpected error occurred on the server side. */
    INTERNAL_ERROR = "INTERNAL_ERROR",
    /** An error occurred, but the specific cause is unknown or cannot be categorized. */
    UNKNOWN_ERROR = "UNKNOWN_ERROR",
    /** An error occurred during the loading or validation of configuration data. */
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR",
    /** An error occurred during the initialization phase of a service or module. */
    INITIALIZATION_FAILED = "INITIALIZATION_FAILED",
    /** An error was returned by the NCBI E-utilities API. */
    NCBI_API_ERROR = "NCBI_API_ERROR",
    /** An error occurred while parsing a response from NCBI (e.g., XML, JSON). */
    NCBI_PARSING_ERROR = "NCBI_PARSING_ERROR",
    /** A warning or notice related to NCBI rate limits. */
    NCBI_RATE_LIMIT_WARNING = "NCBI_RATE_LIMIT_WARNING",
    /** An error related to the construction or validity of an NCBI E-utility query. */
    NCBI_QUERY_ERROR = "NCBI_QUERY_ERROR",
    /** NCBI service temporarily unavailable or returned a server-side error. */
    NCBI_SERVICE_UNAVAILABLE = "NCBI_SERVICE_UNAVAILABLE"
}
/**
 * Custom error class for MCP-specific errors, extending the built-in `Error` class.
 * It standardizes error reporting by encapsulating a `BaseErrorCode`, a descriptive
 * human-readable message, and optional structured details for more context.
 *
 * This class is central to error handling within the MCP framework, allowing for
 * consistent error creation and propagation.
 */
export declare class McpError extends Error {
    /**
     * The standardized error code from {@link BaseErrorCode}.
     */
    readonly code: BaseErrorCode;
    /**
     * Optional additional details or context about the error.
     * This can be any structured data that helps in understanding or debugging the error.
     */
    readonly details?: Record<string, unknown>;
    /**
     * Creates an instance of McpError.
     *
     * @param code - The standardized error code that categorizes the error.
     * @param message - A human-readable description of the error.
     * @param details - Optional. A record containing additional structured details about the error.
     */
    constructor(code: BaseErrorCode, message: string, details?: Record<string, unknown>);
}
/**
 * Zod schema for validating error objects. This schema can be used for:
 * - Validating error structures when parsing error responses from external services.
 * - Ensuring consistency when creating or handling error objects internally.
 * - Generating TypeScript types for error objects.
 *
 * The schema enforces the presence of a `code` (from {@link BaseErrorCode}) and a `message`,
 * and allows for optional `details`.
 */
export declare const ErrorSchema: z.ZodObject<{
    /**
     * The error code, corresponding to one of the {@link BaseErrorCode} enum values.
     * This field is required and helps in programmatically identifying the error type.
     */
    code: z.ZodNativeEnum<typeof BaseErrorCode>;
    /**
     * A human-readable, descriptive message explaining the error.
     * This field is required and provides context to developers or users.
     */
    message: z.ZodString;
    /**
     * Optional. A record containing additional structured details or context about the error.
     * This can include things like invalid field names, specific values that caused issues, or other relevant data.
     */
    details: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
}, "strip", z.ZodTypeAny, {
    code: BaseErrorCode;
    message: string;
    details?: Record<string, unknown> | undefined;
}, {
    code: BaseErrorCode;
    message: string;
    details?: Record<string, unknown> | undefined;
}>;
/**
 * TypeScript type inferred from the {@link ErrorSchema}.
 * This type represents the structure of a validated error object, commonly used
 * for error responses or when passing error information within the application.
 */
export type ErrorResponse = z.infer<typeof ErrorSchema>;
//# sourceMappingURL=errors.d.ts.map