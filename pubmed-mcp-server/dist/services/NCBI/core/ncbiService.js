/**
 * @fileoverview Service for interacting with NCBI E-utilities.
 * This module centralizes all communication with NCBI's E-utility APIs,
 * handling request construction, API key management, rate limiting,
 * retries, and parsing of XML/JSON responses. It aims to provide a robust
 * and compliant interface for other parts of the pubmed-mcp-server to
 * access PubMed data.
 * @module src/services/NCBI/core/ncbiService
 */
import { logger, requestContextService, } from "../../../utils/index.js";
import { NcbiCoreApiClient } from "./ncbiCoreApiClient.js";
import { NcbiRequestQueueManager } from "./ncbiRequestQueueManager.js";
import { NcbiResponseHandler } from "./ncbiResponseHandler.js";
export class NcbiService {
    queueManager;
    apiClient;
    responseHandler;
    constructor() {
        this.queueManager = new NcbiRequestQueueManager();
        this.apiClient = new NcbiCoreApiClient();
        this.responseHandler = new NcbiResponseHandler();
    }
    async performNcbiRequest(endpoint, params, context, options = {}) {
        const task = async () => {
            const rawResponse = await this.apiClient.makeRequest(endpoint, params, context, options);
            return this.responseHandler.parseAndHandleResponse(rawResponse, endpoint, context, options);
        };
        return this.queueManager.enqueueRequest(task, context, endpoint, params);
    }
    async eSearch(params, context) {
        const response = await this.performNcbiRequest("esearch", params, context, {
            retmode: "xml",
        });
        const esResult = response.eSearchResult;
        return {
            count: parseInt(esResult.Count, 10) || 0,
            retmax: parseInt(esResult.RetMax, 10) || 0,
            retstart: parseInt(esResult.RetStart, 10) || 0,
            queryKey: esResult.QueryKey,
            webEnv: esResult.WebEnv,
            idList: esResult.IdList?.Id || [],
            queryTranslation: esResult.QueryTranslation,
            errorList: esResult.ErrorList,
            warningList: esResult.WarningList,
        };
    }
    async eSummary(params, context) {
        // Determine retmode based on params, default to xml
        const retmode = params.version === "2.0" && params.retmode === "json" ? "json" : "xml";
        return this.performNcbiRequest("esummary", params, context, { retmode });
    }
    async eFetch(params, context, options = { retmode: "xml" }) {
        // Determine if POST should be used based on number of IDs
        const usePost = typeof params.id === "string" && params.id.split(",").length > 200;
        const fetchOptions = { ...options, usePost };
        return this.performNcbiRequest("efetch", params, context, fetchOptions);
    }
    async eLink(params, context) {
        return this.performNcbiRequest("elink", params, context, {
            retmode: "xml",
        });
    }
    async eInfo(params, context) {
        return this.performNcbiRequest("einfo", params, context, {
            retmode: "xml",
        });
    }
}
let ncbiServiceInstance;
export function getNcbiService() {
    if (!ncbiServiceInstance) {
        ncbiServiceInstance = new NcbiService();
        logger.debug("NcbiService lazily initialized.", requestContextService.createRequestContext({
            service: "NcbiService",
            operation: "getNcbiServiceInstance",
        }));
    }
    return ncbiServiceInstance;
}
//# sourceMappingURL=ncbiService.js.map