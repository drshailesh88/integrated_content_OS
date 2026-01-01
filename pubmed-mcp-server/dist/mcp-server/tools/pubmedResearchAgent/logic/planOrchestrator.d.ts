/**
 * @fileoverview Orchestrates the generation of the research plan outline
 * by directly mapping detailed client inputs to a structured output format.
 * Omits sections/steps if no relevant input is provided.
 * @module pubmedResearchAgent/logic/planOrchestrator
 */
import { RequestContext } from "../../../../utils/index.js";
import type { PubMedResearchAgentInput } from "./inputSchema.js";
import type { PubMedResearchPlanGeneratedOutput } from "./outputTypes.js";
export declare function generateFullResearchPlanOutline(input: PubMedResearchAgentInput, parentRequestContext: RequestContext): PubMedResearchPlanGeneratedOutput;
//# sourceMappingURL=planOrchestrator.d.ts.map