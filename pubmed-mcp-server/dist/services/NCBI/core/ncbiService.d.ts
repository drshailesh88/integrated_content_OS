/**
 * @fileoverview Service for interacting with NCBI E-utilities.
 * This module centralizes all communication with NCBI's E-utility APIs,
 * handling request construction, API key management, rate limiting,
 * retries, and parsing of XML/JSON responses. It aims to provide a robust
 * and compliant interface for other parts of the pubmed-mcp-server to
 * access PubMed data.
 * @module src/services/NCBI/core/ncbiService
 */
import { ESearchResult, EFetchArticleSet } from "../../../types-global/pubmedXml.js";
import { RequestContext } from "../../../utils/index.js";
import { NcbiRequestParams, NcbiRequestOptions } from "./ncbiConstants.js";
export declare class NcbiService {
    private queueManager;
    private apiClient;
    private responseHandler;
    constructor();
    private performNcbiRequest;
    eSearch(params: NcbiRequestParams, context: RequestContext): Promise<ESearchResult>;
    eSummary(params: NcbiRequestParams, context: RequestContext): Promise<unknown>;
    eFetch(params: NcbiRequestParams, context: RequestContext, options?: NcbiRequestOptions): Promise<EFetchArticleSet>;
    eLink(params: NcbiRequestParams, context: RequestContext): Promise<unknown>;
    eInfo(params: NcbiRequestParams, context: RequestContext): Promise<unknown>;
}
export declare function getNcbiService(): NcbiService;
//# sourceMappingURL=ncbiService.d.ts.map