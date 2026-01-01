/**
 * @fileoverview Registration for the pubmed_fetch_contents MCP tool.
 * @module src/mcp-server/tools/pubmedFetchContents/registration
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  ErrorHandler,
  logger,
  RequestContext,
  requestContextService,
} from "../../../utils/index.js";
import {
  PubMedFetchContentsInput,
  PubMedFetchContentsInputSchema,
  pubMedFetchContentsLogic,
} from "./logic.js";

/**
 * Registers the pubmed_fetch_contents tool with the MCP server.
 * @param server - The McpServer instance.
 */
export async function registerPubMedFetchContentsTool(
  server: McpServer,
): Promise<void> {
  const operation = "registerPubMedFetchContentsTool";
  const toolName = "pubmed_fetch_contents";
  const toolDescription =
    "Fetches detailed information from PubMed using NCBI EFetch. Can be used with a direct list of PMIDs or with queryKey/webEnv from an ESearch history entry. Supports pagination (retstart, retmax) when using history. Available 'detailLevel' options: 'abstract_plus' (parsed details), 'full_xml' (raw PubMedArticle XML), 'medline_text' (MEDLINE format), or 'citation_data' (minimal citation data). Returns a JSON object containing results, any PMIDs not found (if applicable), and EFetch details.";

  const context = requestContextService.createRequestContext({ operation });

  await ErrorHandler.tryCatch(
    async () => {
      server.tool(
        toolName,
        toolDescription,
        PubMedFetchContentsInputSchema._def.schema.shape,
        async (
          input: PubMedFetchContentsInput,
          toolContext: unknown,
        ): Promise<CallToolResult> => {
          const richContext: RequestContext =
            requestContextService.createRequestContext({
              parentRequestId: context.requestId,
              operation: "pubMedFetchContentsToolHandler",
              mcpToolContext: toolContext,
              input,
            });

          try {
            const result = await pubMedFetchContentsLogic(input, richContext);
            return {
              content: [{ type: "text", text: result.content }],
              isError: false,
            };
          } catch (error) {
            const handledError = ErrorHandler.handleError(error, {
              operation: "pubMedFetchContentsToolHandler",
              context: richContext,
              input,
              rethrow: false,
            });

            const mcpError =
              handledError instanceof McpError
                ? handledError
                : new McpError(
                    BaseErrorCode.INTERNAL_ERROR,
                    "An unexpected error occurred while fetching PubMed content.",
                    {
                      originalErrorName: handledError.name,
                      originalErrorMessage: handledError.message,
                    },
                  );

            return {
              content: [
                {
                  type: "text",
                  text: JSON.stringify({
                    error: {
                      code: mcpError.code,
                      message: mcpError.message,
                      details: mcpError.details,
                    },
                  }),
                },
              ],
              isError: true,
            };
          }
        },
      );

      logger.notice(`Tool '${toolName}' registered.`, context);
    },
    {
      operation,
      context,
      errorCode: BaseErrorCode.INITIALIZATION_FAILED,
      critical: true,
    },
  );
}
