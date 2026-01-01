/**
 * @fileoverview Handles ELink requests and enriches results with ESummary data
 * for the pubmedArticleConnections tool.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/elinkHandler
 */
import { RequestContext } from "../../../../utils/index.js";
import type { PubMedArticleConnectionsInput } from "./index.js";
import type { ToolOutputData } from "./types.js";
export declare function handleELinkRelationships(input: PubMedArticleConnectionsInput, outputData: ToolOutputData, context: RequestContext): Promise<void>;
//# sourceMappingURL=elinkHandler.d.ts.map