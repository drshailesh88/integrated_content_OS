/**
 * @fileoverview Registers the 'pubmed_generate_chart' tool with the MCP server.
 * This tool now accepts parameterized input for generating charts.
 * @module src/mcp-server/tools/pubmedGenerateChart/registration
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
  PubMedGenerateChartInput,
  PubMedGenerateChartInputSchema,
  pubmedGenerateChartLogic,
} from "./logic.js";

export async function registerPubMedGenerateChartTool(
  server: McpServer,
): Promise<void> {
  const operation = "registerPubMedGenerateChartTool";
  const toolName = "pubmed_generate_chart";
  const toolDescription =
    "Generates a customizable chart (PNG) from structured data. Supports various plot types and requires data values and field mappings for axes. Returns a Base64-encoded PNG image.";
  const context = requestContextService.createRequestContext({ operation });

  await ErrorHandler.tryCatch(
    async () => {
      server.tool(
        toolName,
        toolDescription,
        PubMedGenerateChartInputSchema.shape,
        async (
          input: PubMedGenerateChartInput,
          mcpProvidedContext: unknown,
        ): Promise<CallToolResult> => {
          const richContext: RequestContext =
            requestContextService.createRequestContext({
              parentRequestId: context.requestId,
              operation: "pubmedGenerateChartToolHandler",
              mcpToolContext: mcpProvidedContext,
              input,
            });

          try {
            const result = await pubmedGenerateChartLogic(input, richContext);
            return {
              content: [
                {
                  type: "image",
                  data: result.base64Data,
                  mimeType: "image/png",
                },
              ],
              isError: false,
            };
          } catch (error) {
            const handledError = ErrorHandler.handleError(error, {
              operation: "pubmedGenerateChartToolHandler",
              context: richContext,
              input,
              rethrow: false,
            });

            const mcpError =
              handledError instanceof McpError
                ? handledError
                : new McpError(
                    BaseErrorCode.INTERNAL_ERROR,
                    "An unexpected error occurred while generating the chart.",
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
