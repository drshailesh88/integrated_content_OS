/**
 * @fileoverview Registration for the pubmed_research_agent tool.
 * @module pubmedResearchAgent/registration
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
import { pubmedResearchAgentLogic } from "./logic.js";
import {
  PubMedResearchAgentInput,
  PubMedResearchAgentInputSchema,
} from "./logic/index.js";

/**
 * Registers the pubmed_research_agent tool with the MCP server.
 * @param server - The McpServer instance.
 */
export async function registerPubMedResearchAgentTool(
  server: McpServer,
): Promise<void> {
  const operation = "registerPubMedResearchAgentTool";
  const toolName = "pubmed_research_agent";
  const toolDescription =
    "Generates a standardized JSON research plan outline from component details you provide. It accepts granular inputs for all research phases (conception, data collection, analysis, dissemination, cross-cutting concerns). If `include_detailed_prompts_for_agent` is true, the output plan will embed instructive prompts and detailed guidance notes to aid the research agent. The tool's primary function is to organize and structure your rough ideas into a formal, machine-readable plan. This plan is intended for further processing; as the research agent, you should then utilize your full suite of tools (e.g., file manipulation, `get_pubmed_article_connections` for literature/data search via PMID) to execute the outlined research, tailored to the user's request.";
  const context = requestContextService.createRequestContext({ operation });

  await ErrorHandler.tryCatch(
    async () => {
      server.tool(
        toolName,
        toolDescription,
        PubMedResearchAgentInputSchema.shape,
        async (
          input: PubMedResearchAgentInput,
          mcpProvidedContext: unknown,
        ): Promise<CallToolResult> => {
          const richContext: RequestContext =
            requestContextService.createRequestContext({
              parentRequestId: context.requestId,
              operation: "pubmedResearchAgentToolHandler",
              mcpToolContext: mcpProvidedContext,
              input,
            });

          try {
            const result = await pubmedResearchAgentLogic(input, richContext);
            return {
              content: [
                { type: "text", text: JSON.stringify(result, null, 2) },
              ],
              isError: false,
            };
          } catch (error) {
            const handledError = ErrorHandler.handleError(error, {
              operation: "pubmedResearchAgentToolHandler",
              context: richContext,
              input,
              rethrow: false,
            });

            const mcpError =
              handledError instanceof McpError
                ? handledError
                : new McpError(
                    BaseErrorCode.INTERNAL_ERROR,
                    "An unexpected error occurred while generating the research plan.",
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
