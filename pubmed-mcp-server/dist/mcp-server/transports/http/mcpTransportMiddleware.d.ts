/**
 * @fileoverview Hono middleware for handling MCP transport logic.
 * This middleware encapsulates the logic for processing MCP requests,
 * delegating to the appropriate transport manager, and preparing the
 * response for Hono to send.
 * @module src/mcp-server/transports/http/mcpTransportMiddleware
 */
import { MiddlewareHandler } from "hono";
import { ServerInstanceInfo } from "../../server.js";
import { TransportManager, TransportResponse } from "../core/transportTypes.js";
import { HonoNodeBindings } from "./httpTypes.js";
/**
 * Creates a Hono middleware for handling MCP POST requests.
 * @param transportManager - The main transport manager (usually stateful).
 * @param createServerInstanceFn - Function to create an McpServer instance.
 * @returns A Hono middleware function.
 */
type McpMiddlewareEnv = {
    Variables: {
        mcpResponse: TransportResponse;
    };
};
export declare const mcpTransportMiddleware: (transportManager: TransportManager, createServerInstanceFn: () => Promise<ServerInstanceInfo>) => MiddlewareHandler<McpMiddlewareEnv & {
    Bindings: HonoNodeBindings;
}>;
export {};
//# sourceMappingURL=mcpTransportMiddleware.d.ts.map