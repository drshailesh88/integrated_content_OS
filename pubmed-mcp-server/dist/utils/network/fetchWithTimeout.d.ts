/**
 * @fileoverview Provides a utility function to make fetch requests with a specified timeout.
 * @module src/utils/network/fetchWithTimeout
 */
import type { RequestContext } from "../internal/requestContext.js";
/**
 * Options for the fetchWithTimeout utility.
 * Extends standard RequestInit but omits 'signal' as it's handled internally.
 */
export type FetchWithTimeoutOptions = Omit<RequestInit, "signal">;
/**
 * Fetches a resource with a specified timeout.
 *
 * @param url - The URL to fetch.
 * @param timeoutMs - The timeout duration in milliseconds.
 * @param context - The request context for logging.
 * @param options - Optional fetch options (RequestInit), excluding 'signal'.
 * @returns A promise that resolves to the Response object.
 * @throws {McpError} If the request times out or another fetch-related error occurs.
 */
export declare function fetchWithTimeout(url: string | URL, timeoutMs: number, context: RequestContext, options?: FetchWithTimeoutOptions): Promise<Response>;
//# sourceMappingURL=fetchWithTimeout.d.ts.map