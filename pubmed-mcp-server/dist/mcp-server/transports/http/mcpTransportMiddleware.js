/**
 * @fileoverview Hono middleware for handling MCP transport logic.
 * This middleware encapsulates the logic for processing MCP requests,
 * delegating to the appropriate transport manager, and preparing the
 * response for Hono to send.
 * @module src/mcp-server/transports/http/mcpTransportMiddleware
 */
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import { createMiddleware } from "hono/factory";
import { config } from "../../../config/index.js";
import { requestContextService } from "../../../utils/index.js";
import { StatelessTransportManager } from "../core/statelessTransportManager.js";
/**
 * Converts a Fetch API Headers object to Node.js IncomingHttpHeaders.
 * @param headers - The Headers object to convert.
 * @returns An object compatible with IncomingHttpHeaders.
 */
function toIncomingHttpHeaders(headers) {
    const result = {};
    headers.forEach((value, key) => {
        result[key] = value;
    });
    return result;
}
/**
 * Handles a stateless request by creating an ephemeral transport manager.
 * @param createServerInstanceFn - Function to create an McpServer instance.
 * @param headers - The request headers.
 * @param body - The request body.
 * @param context - The request context.
 * @returns A promise resolving with the transport response.
 */
async function handleStatelessRequest(createServerInstanceFn, headers, body, context) {
    const getMcpServer = async () => (await createServerInstanceFn()).server;
    const statelessManager = new StatelessTransportManager(getMcpServer);
    return statelessManager.handleRequest(toIncomingHttpHeaders(headers), body, context);
}
export const mcpTransportMiddleware = (transportManager, createServerInstanceFn) => {
    return createMiddleware(async (c, next) => {
        const sessionId = c.req.header("mcp-session-id");
        const context = requestContextService.createRequestContext({
            operation: "mcpTransportMiddleware",
            sessionId,
        });
        const body = await c.req.json();
        let response;
        if (isInitializeRequest(body)) {
            if (config.mcpSessionMode === "stateless") {
                response = await handleStatelessRequest(createServerInstanceFn, c.req.raw.headers, body, context);
            }
            else {
                response = await transportManager.initializeAndHandle(toIncomingHttpHeaders(c.req.raw.headers), body, context);
            }
        }
        else {
            if (sessionId) {
                response = await transportManager.handleRequest(toIncomingHttpHeaders(c.req.raw.headers), body, context, sessionId);
            }
            else {
                response = await handleStatelessRequest(createServerInstanceFn, c.req.raw.headers, body, context);
            }
        }
        c.set("mcpResponse", response);
        await next();
    });
};
//# sourceMappingURL=mcpTransportMiddleware.js.map