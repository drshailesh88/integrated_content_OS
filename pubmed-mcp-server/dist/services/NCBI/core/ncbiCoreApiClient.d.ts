/**
 * @fileoverview Core client for making HTTP requests to NCBI E-utilities.
 * Handles request construction, API key injection, retries, and basic error handling.
 * @module src/services/NCBI/core/ncbiCoreApiClient
 */
import { AxiosResponse } from "axios";
import { RequestContext } from "../../../utils/index.js";
import { NcbiRequestParams, NcbiRequestOptions } from "./ncbiConstants.js";
export declare class NcbiCoreApiClient {
    private axiosInstance;
    constructor();
    /**
     * Makes an HTTP request to the specified NCBI E-utility endpoint.
     * Handles parameter assembly, API key injection, GET/POST selection, and retries.
     * @param endpoint The E-utility endpoint (e.g., "esearch", "efetch").
     * @param params The parameters for the E-utility.
     * @param context The request context for logging.
     * @param options Options for the request, like retmode and whether to use POST.
     * @param retries The current retry attempt number.
     * @returns A Promise resolving to the raw AxiosResponse.
     * @throws {McpError} If the request fails after all retries or an unexpected error occurs.
     */
    makeRequest(endpoint: string, params: NcbiRequestParams, context: RequestContext, options?: NcbiRequestOptions): Promise<AxiosResponse>;
}
//# sourceMappingURL=ncbiCoreApiClient.d.ts.map