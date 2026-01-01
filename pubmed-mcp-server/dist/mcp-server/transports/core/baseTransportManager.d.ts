/**
 * @fileoverview Abstract base class for transport managers.
 * @module src/mcp-server/transports/core/baseTransportManager
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { IncomingHttpHeaders } from "http";
import { RequestContext } from "../../../utils/index.js";
import { TransportManager, TransportResponse } from "./transportTypes.js";
/**
 * Abstract base class for transport managers, providing common functionality.
 */
export declare abstract class BaseTransportManager implements TransportManager {
    protected readonly createServerInstanceFn: () => Promise<McpServer>;
    constructor(createServerInstanceFn: () => Promise<McpServer>);
    abstract handleRequest(headers: IncomingHttpHeaders, body: unknown, context: RequestContext, sessionId?: string): Promise<TransportResponse>;
    abstract shutdown(): Promise<void>;
}
//# sourceMappingURL=baseTransportManager.d.ts.map