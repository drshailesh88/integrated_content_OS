/**
 * @fileoverview Core logic invocation for the pubmed_research_agent tool.
 * This tool generates a structured research plan outline with instructive placeholders,
 * designed to be completed by a calling LLM (the MCP Client).
 * @module pubmedResearchAgent/logic
 */
import { RequestContext } from "../../../utils/index.js";
import { PubMedResearchAgentInput, PubMedResearchPlanGeneratedOutput } from "./logic/index.js";
export declare function pubmedResearchAgentLogic(input: PubMedResearchAgentInput, parentRequestContext: RequestContext): Promise<PubMedResearchPlanGeneratedOutput>;
//# sourceMappingURL=logic.d.ts.map