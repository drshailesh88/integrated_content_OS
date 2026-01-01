/**
 * @fileoverview Implements a stateful transport manager for the MCP SDK.
 *
 * This manager handles multiple, persistent MCP sessions. It creates and maintains
 * a dedicated McpServer and StreamableHTTPServerTransport instance for each session,
 * allowing for stateful, multi-turn interactions. It includes robust mechanisms for
 * session lifecycle management, including garbage collection of stale sessions and
 * concurrency controls to prevent race conditions.
 *
 * SCALABILITY NOTE: This manager maintains all session state in local process memory.
 * For horizontal scaling across multiple server instances, a load balancer with
 * sticky sessions (session affinity) is required to ensure that all requests for a
 * given session are routed to the same process instance that holds that session's state.
 *
 * @module src/mcp-server/transports/core/statefulTransportManager
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { IncomingHttpHeaders } from "http";
import { RequestContext } from "../../../utils/index.js";
import { BaseTransportManager } from "./baseTransportManager.js";
import { StatefulTransportManager as IStatefulTransportManager, TransportResponse, TransportSession } from "./transportTypes.js";
/**
 * Defines the configuration options for the StatefulTransportManager.
 */
export interface StatefulTransportOptions {
    staleSessionTimeoutMs: number;
    mcpHttpEndpointPath: string;
}
/**
 * Manages persistent, stateful MCP sessions.
 */
export declare class StatefulTransportManager extends BaseTransportManager implements IStatefulTransportManager {
    private readonly transports;
    private readonly servers;
    private readonly sessions;
    private readonly garbageCollector;
    private readonly options;
    /**
     * @param createServerInstanceFn - A factory function to create new McpServer instances.
     * @param options - Configuration options for the manager.
     */
    constructor(createServerInstanceFn: () => Promise<McpServer>, options: StatefulTransportOptions);
    /**
     * Initializes a new stateful session and handles the first request.
     *
     * @param headers - The incoming request headers.
     * @param body - The parsed body of the request.
     * @param context - The request context.
     * @returns A promise resolving to a streaming TransportResponse with a session ID.
     */
    initializeAndHandle(headers: IncomingHttpHeaders, body: unknown, context: RequestContext): Promise<TransportResponse>;
    /**
     * Handles a subsequent request for an existing stateful session.
     */
    handleRequest(headers: IncomingHttpHeaders, body: unknown, context: RequestContext, sessionId?: string): Promise<TransportResponse>;
    /**
     * Handles a request to explicitly delete a session.
     */
    handleDeleteRequest(sessionId: string, context: RequestContext): Promise<TransportResponse>;
    /**
     * Retrieves information about a specific session.
     */
    getSession(sessionId: string): TransportSession | undefined;
    /**
     * Gracefully shuts down the manager, closing all active sessions.
     */
    shutdown(): Promise<void>;
    /**
     * Closes a single session and releases its associated resources.
     */
    private closeSession;
    /**
     * Periodically runs to find and clean up stale, inactive sessions.
     */
    private cleanupStaleSessions;
}
//# sourceMappingURL=statefulTransportManager.d.ts.map