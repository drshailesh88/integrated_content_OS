/**
 * @fileoverview Handles citation formatting for the pubmedArticleConnections tool.
 * Fetches article details using EFetch and formats them into various citation styles.
 * @module src/mcp-server/tools/pubmedArticleConnections/logic/citationFormatter
 */
import { RequestContext } from "../../../../utils/index.js";
import type { PubMedArticleConnectionsInput } from "./index.js";
import type { ToolOutputData } from "./types.js";
export declare function handleCitationFormats(input: PubMedArticleConnectionsInput, outputData: ToolOutputData, context: RequestContext): Promise<void>;
//# sourceMappingURL=citationFormatter.d.ts.map