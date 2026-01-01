/**
 * @fileoverview Service for interacting with NCBI E-utilities.
 * This module centralizes all communication with NCBI's E-utility APIs,
 * handling request construction, API key management, rate limiting,
 * retries, and parsing of XML/JSON responses. It aims to provide a robust
 * and compliant interface for other parts of the pubmed-mcp-server to
 * access PubMed data.
 * @module src/services/NCBI/core/ncbiService
 */

import {
  ESearchResult,
  EFetchArticleSet,
  ESearchResponseContainer,
} from "../../../types-global/pubmedXml.js";
import {
  logger,
  RequestContext,
  requestContextService,
} from "../../../utils/index.js";
import { NcbiRequestParams, NcbiRequestOptions } from "./ncbiConstants.js";
import { NcbiCoreApiClient } from "./ncbiCoreApiClient.js";
import { NcbiRequestQueueManager } from "./ncbiRequestQueueManager.js";
import { NcbiResponseHandler } from "./ncbiResponseHandler.js";

export class NcbiService {
  private queueManager: NcbiRequestQueueManager;
  private apiClient: NcbiCoreApiClient;
  private responseHandler: NcbiResponseHandler;

  constructor() {
    this.queueManager = new NcbiRequestQueueManager();
    this.apiClient = new NcbiCoreApiClient();
    this.responseHandler = new NcbiResponseHandler();
  }

  private async performNcbiRequest<T>(
    endpoint: string,
    params: NcbiRequestParams,
    context: RequestContext,
    options: NcbiRequestOptions = {},
  ): Promise<T> {
    const task = async () => {
      const rawResponse = await this.apiClient.makeRequest(
        endpoint,
        params,
        context,
        options,
      );
      return this.responseHandler.parseAndHandleResponse<T>(
        rawResponse,
        endpoint,
        context,
        options,
      );
    };

    return this.queueManager.enqueueRequest<T>(task, context, endpoint, params);
  }

  public async eSearch(
    params: NcbiRequestParams,
    context: RequestContext,
  ): Promise<ESearchResult> {
    const response = await this.performNcbiRequest<ESearchResponseContainer>(
      "esearch",
      params,
      context,
      {
        retmode: "xml",
      },
    );

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

  public async eSummary(
    params: NcbiRequestParams,
    context: RequestContext,
  ): Promise<unknown> {
    // Determine retmode based on params, default to xml
    const retmode =
      params.version === "2.0" && params.retmode === "json" ? "json" : "xml";
    return this.performNcbiRequest("esummary", params, context, { retmode });
  }

  public async eFetch(
    params: NcbiRequestParams,
    context: RequestContext,
    options: NcbiRequestOptions = { retmode: "xml" }, // Default retmode for eFetch
  ): Promise<EFetchArticleSet> {
    // Determine if POST should be used based on number of IDs
    const usePost =
      typeof params.id === "string" && params.id.split(",").length > 200;
    const fetchOptions = { ...options, usePost };

    return this.performNcbiRequest<EFetchArticleSet>(
      "efetch",
      params,
      context,
      fetchOptions,
    );
  }

  public async eLink(
    params: NcbiRequestParams,
    context: RequestContext,
  ): Promise<unknown> {
    return this.performNcbiRequest("elink", params, context, {
      retmode: "xml",
    });
  }

  public async eInfo(
    params: NcbiRequestParams,
    context: RequestContext,
  ): Promise<unknown> {
    return this.performNcbiRequest("einfo", params, context, {
      retmode: "xml",
    });
  }
}

let ncbiServiceInstance: NcbiService;

export function getNcbiService(): NcbiService {
  if (!ncbiServiceInstance) {
    ncbiServiceInstance = new NcbiService();
    logger.debug(
      "NcbiService lazily initialized.",
      requestContextService.createRequestContext({
        service: "NcbiService",
        operation: "getNcbiServiceInstance",
      }),
    );
  }
  return ncbiServiceInstance;
}
