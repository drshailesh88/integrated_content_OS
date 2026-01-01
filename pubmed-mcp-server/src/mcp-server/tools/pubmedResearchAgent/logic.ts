/**
 * @fileoverview Core logic invocation for the pubmed_research_agent tool.
 * This tool generates a structured research plan outline with instructive placeholders,
 * designed to be completed by a calling LLM (the MCP Client).
 * @module pubmedResearchAgent/logic
 */

import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import {
  generateFullResearchPlanOutline,
  PubMedResearchAgentInput,
  PubMedResearchPlanGeneratedOutput,
} from "./logic/index.js";

export async function pubmedResearchAgentLogic(
  input: PubMedResearchAgentInput,
  parentRequestContext: RequestContext,
): Promise<PubMedResearchPlanGeneratedOutput> {
  const operationContext = requestContextService.createRequestContext({
    parentRequestId: parentRequestContext.requestId,
    operation: "pubmedResearchAgentLogicExecution",
    input: sanitizeInputForLogging(input),
  });

  logger.info(
    `Executing 'pubmed_research_agent' to generate research plan outline. Keywords: ${input.research_keywords.join(
      ", ",
    )}`,
    operationContext,
  );

  const researchPlanOutline = generateFullResearchPlanOutline(
    input,
    operationContext,
  );

  logger.notice("Successfully generated research plan outline.", {
    ...operationContext,
    projectTitle: input.project_title_suggestion,
  });

  return researchPlanOutline;
}
