/**
 * @fileoverview Core client for making HTTP requests to NCBI E-utilities.
 * Handles request construction, API key injection, retries, and basic error handling.
 * @module src/services/NCBI/core/ncbiCoreApiClient
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { config } from "../../../config/index.js";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import {
  NCBI_EUTILS_BASE_URL,
  NcbiRequestParams,
  NcbiRequestOptions,
} from "./ncbiConstants.js";

export class NcbiCoreApiClient {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      timeout: 30000, // 30 seconds timeout for NCBI requests
    });
  }

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
  public async makeRequest(
    endpoint: string,
    params: NcbiRequestParams,
    context: RequestContext,
    options: NcbiRequestOptions = {},
  ): Promise<AxiosResponse> {
    const rawParams: Record<string, string | number | undefined> = {
      tool: config.ncbiToolIdentifier,
      email: config.ncbiAdminEmail,
      api_key: config.ncbiApiKey,
      ...params,
    };

    const finalParams: Record<string, string> = {};
    for (const key in rawParams) {
      if (Object.prototype.hasOwnProperty.call(rawParams, key)) {
        const value = rawParams[key];
        if (value !== undefined && value !== null) {
          finalParams[key] = String(value);
        }
      }
    }

    const requestConfig: AxiosRequestConfig = {
      method: options.usePost ? "POST" : "GET",
      url: `${NCBI_EUTILS_BASE_URL}/${endpoint}.fcgi`,
    };

    if (options.usePost) {
      requestConfig.data = new URLSearchParams(finalParams).toString();
      requestConfig.headers = {
        "Content-Type": "application/x-www-form-urlencoded",
      };
    } else {
      requestConfig.params = finalParams;
    }

    for (let attempt = 0; attempt <= config.ncbiMaxRetries; attempt++) {
      try {
        logger.debug(
          `Making NCBI HTTP request: ${requestConfig.method} ${requestConfig.url}`,
          requestContextService.createRequestContext({
            ...context,
            operation: "NCBI_HttpRequest",
            endpoint,
            method: requestConfig.method,
            requestParams: sanitizeInputForLogging(finalParams),
            attempt: attempt + 1,
          }),
        );
        const response: AxiosResponse = await this.axiosInstance(requestConfig);
        return response;
      } catch (error: unknown) {
        const err = error as Error;
        if (attempt < config.ncbiMaxRetries) {
          const retryDelay = Math.pow(2, attempt) * 200;
          logger.warning(
            `NCBI request to ${endpoint} failed. Retrying (${attempt + 1}/${config.ncbiMaxRetries}) in ${retryDelay}ms...`,
            requestContextService.createRequestContext({
              ...context,
              operation: "NCBI_HttpRequestRetry",
              endpoint,
              error: err.message,
              retryCount: attempt + 1,
              maxRetries: config.ncbiMaxRetries,
              delay: retryDelay,
            }),
          );
          await new Promise((r) => setTimeout(r, retryDelay));
          continue; // Continue to the next iteration of the loop
        }

        // If all retries are exhausted, handle the final error
        if (axios.isAxiosError(error)) {
          logger.error(
            `Axios error during NCBI request to ${endpoint} after ${attempt} retries`,
            error,
            requestContextService.createRequestContext({
              ...context,
              operation: "NCBI_AxiosError",
              endpoint,
              status: error.response?.status,
              responseData: sanitizeInputForLogging(error.response?.data),
            }),
          );
          throw new McpError(
            BaseErrorCode.NCBI_SERVICE_UNAVAILABLE,
            `NCBI request failed: ${error.message}`,
            {
              endpoint,
              status: error.response?.status,
              details: error.response?.data
                ? String(error.response.data).substring(0, 500)
                : undefined,
            },
          );
        }
        if (error instanceof McpError) throw error;

        logger.error(
          `Unexpected error during NCBI request to ${endpoint} after ${attempt} retries`,
          err,
          requestContextService.createRequestContext({
            ...context,
            operation: "NCBI_UnexpectedError",
            endpoint,
            errorMessage: err.message,
          }),
        );
        throw new McpError(
          BaseErrorCode.INTERNAL_ERROR,
          `Unexpected error communicating with NCBI: ${err.message}`,
          { endpoint },
        );
      }
    }
    // This line should theoretically be unreachable, but it satisfies TypeScript's need
    // for a return path if the loop completes without returning or throwing.
    throw new McpError(
      BaseErrorCode.INTERNAL_ERROR,
      "Request failed after all retries.",
      { endpoint },
    );
  }
}
