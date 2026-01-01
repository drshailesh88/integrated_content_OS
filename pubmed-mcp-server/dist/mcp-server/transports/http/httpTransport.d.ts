/**
 * @fileoverview Configures and starts the HTTP MCP transport using Hono.
 * This file has been refactored to correctly integrate Hono's streaming
 * capabilities with the Model Context Protocol SDK's transport layer.
 * @module src/mcp-server/transports/http/httpTransport
 */
import { ServerType } from "@hono/node-server";
import { Hono } from "hono";
import { RequestContext } from "../../../utils/index.js";
import { ServerInstanceInfo } from "../../server.js";
import { TransportManager } from "../core/transportTypes.js";
import { HonoNodeBindings } from "./httpTypes.js";
export declare function createHttpApp(transportManager: TransportManager, createServerInstanceFn: () => Promise<ServerInstanceInfo>, parentContext: RequestContext): Hono<{
    Bindings: HonoNodeBindings;
}>;
export declare function startHttpTransport(createServerInstanceFn: () => Promise<ServerInstanceInfo>, parentContext: RequestContext): Promise<{
    app: Hono<{
        Bindings: HonoNodeBindings;
    }>;
    server: ServerType;
    transportManager: TransportManager;
}>;
//# sourceMappingURL=httpTransport.d.ts.map