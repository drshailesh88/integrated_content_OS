/**
 * @fileoverview Provides utility functions for authorization, specifically for
 * checking token scopes against required permissions for a given operation.
 * @module src/mcp-server/transports/auth/core/authUtils
 */
/**
 * Checks if the current authentication context contains all the specified scopes.
 * This function is designed to be called within tool or resource handlers to
 * enforce scope-based access control. It retrieves the authentication information
 * from `authContext` (AsyncLocalStorage).
 *
 * @param requiredScopes - An array of scope strings that are mandatory for the operation.
 * @throws {McpError} Throws an error with `BaseErrorCode.INTERNAL_ERROR` if the
 *   authentication context is missing, which indicates a server configuration issue.
 * @throws {McpError} Throws an error with `BaseErrorCode.FORBIDDEN` if one or
 *   more required scopes are not present in the validated token.
 */
export declare function withRequiredScopes(requiredScopes: string[]): void;
//# sourceMappingURL=authUtils.d.ts.map