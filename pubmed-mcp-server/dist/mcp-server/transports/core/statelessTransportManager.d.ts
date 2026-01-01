/**
 * @fileoverview Implements a stateless transport manager for the MCP SDK.
 *
 * This manager handles single, ephemeral MCP operations. For each incoming request,
 * it dynamically creates a temporary McpServer and transport instance, processes the
 * request, and then immediately schedules the resources for cleanup. This approach
 * is ideal for simple, one-off tool calls that do not require persistent session state.
 *
 * The key challenge addressed here is bridging the Node.js-centric MCP SDK with
 * modern, Web Standards-based frameworks like Hono. This is achieved by deferring
 * resource cleanup until the response stream has been fully consumed by the web
 * framework, preventing premature closure and truncated responses.
 *
 * @module src/mcp-server/transports/core/statelessTransportManager
 */
import type { IncomingHttpHeaders } from "http";
import { RequestContext } from "../../../utils/index.js";
import { BaseTransportManager } from "./baseTransportManager.js";
import { TransportResponse } from "./transportTypes.js";
/**
 * Manages ephemeral, single-request MCP operations.
 */
export declare class StatelessTransportManager extends BaseTransportManager {
    /**
     * Handles a single, stateless MCP request.
     *
     * This method orchestrates the creation of temporary server and transport instances,
     * handles the request, and ensures resources are cleaned up only after the
     * response stream is closed.
     *
     * @param headers - The incoming request headers.
     * @param body - The parsed body of the request.
     * @param context - The request context for logging and tracing.
     * @returns A promise resolving to a streaming TransportResponse.
     */
    handleRequest(headers: IncomingHttpHeaders, body: unknown, context: RequestContext): Promise<TransportResponse>;
    /**
     * Attaches listeners to the response stream to trigger resource cleanup
     * only after the stream has been fully consumed or has errored.
     *
     * @param stream - The response stream bridge.
     * @param server - The ephemeral McpServer instance.
     * @param transport - The ephemeral transport instance.
     * @param context - The request context for logging.
     */
    private setupDeferredCleanup;
    /**
     * Performs the actual cleanup of ephemeral resources.
     * This method is designed to be "fire-and-forget".
     */
    private cleanup;
    /**
     * Shuts down the manager. For the stateless manager, this is a no-op
     * as there are no persistent resources to manage.
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=statelessTransportManager.d.ts.map