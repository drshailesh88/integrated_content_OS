/**
 * @fileoverview Registers the 'pubmed_article_connections' tool with the MCP server.
 * This tool finds articles related to a source PMID or retrieves citation formats.
 * @module src/mcp-server/tools/pubmedArticleConnections/registration
 */
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
/**
 * Registers the 'pubmed_article_connections' tool with the given MCP server instance.
 * @param {McpServer} server - The MCP server instance.
 */
export declare function registerPubMedArticleConnectionsTool(server: McpServer): Promise<void>;
//# sourceMappingURL=registration.d.ts.map