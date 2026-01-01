/**
 * @fileoverview Handles parsing of NCBI E-utility responses and NCBI-specific error extraction.
 * @module src/services/NCBI/core/ncbiResponseHandler
 */
import { AxiosResponse } from "axios";
import { RequestContext } from "../../../utils/index.js";
import { NcbiRequestOptions } from "./ncbiConstants.js";
export declare class NcbiResponseHandler {
    private xmlParser;
    constructor();
    private extractNcbiErrorMessages;
    /**
     * Parses the raw AxiosResponse data based on retmode and checks for NCBI-specific errors.
     * @param response The raw AxiosResponse from an NCBI E-utility call.
     * @param endpoint The E-utility endpoint for context.
     * @param context The request context for logging.
     * @param options The original request options, particularly `retmode`.
     * @returns The parsed data (object for XML/JSON, string for text).
     * @throws {McpError} If parsing fails or NCBI reports an error in the response body.
     */
    parseAndHandleResponse<T>(response: AxiosResponse, endpoint: string, context: RequestContext, options: NcbiRequestOptions): T;
}
//# sourceMappingURL=ncbiResponseHandler.d.ts.map