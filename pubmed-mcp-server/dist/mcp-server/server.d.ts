/**
 * @fileoverview Main entry point for the MCP (Model Context Protocol) server.
 * This file orchestrates the server's lifecycle:
 * 1. Initializes the core `McpServer` instance (from `@modelcontextprotocol/sdk`) with its identity and capabilities.
 * 2. Registers available resources and tools, making them discoverable and usable by clients.
 * 3. Selects and starts the appropriate communication transport (stdio or Streamable HTTP)
 *    based on configuration.
 * 4. Handles top-level error management during startup.
 *
 * @module src/mcp-server/server
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import http from "http";
type SdkToolSpec = Parameters<McpServer["registerTool"]>[1];
type ServerIdentity = ConstructorParameters<typeof McpServer>[0];
type McpServerOptions = NonNullable<ConstructorParameters<typeof McpServer>[1]>;
export interface DescribedTool extends SdkToolSpec {
    title: string;
}
export interface ServerInstanceInfo {
    server: McpServer;
    tools: DescribedTool[];
    identity: ServerIdentity;
    options: McpServerOptions;
}
/**
 * Main application entry point. Initializes and starts the MCP server.
 */
export declare function initializeAndStartServer(): Promise<McpServer | http.Server>;
export {};
//# sourceMappingURL=server.d.ts.map