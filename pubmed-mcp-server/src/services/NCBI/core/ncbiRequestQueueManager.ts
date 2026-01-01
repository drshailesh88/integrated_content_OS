/**
 * @fileoverview Manages a queue for NCBI E-utility requests to ensure compliance with rate limits.
 * @module src/services/NCBI/core/ncbiRequestQueueManager
 */

import { config } from "../../../config/index.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import { NcbiRequestParams } from "./ncbiConstants.js";

/**
 * Interface for a queued NCBI request.
 */
export interface QueuedRequest<T = unknown> {
  resolve: (value: T | PromiseLike<T>) => void;
  reject: (reason?: unknown) => void;
  task: () => Promise<T>; // The actual function that makes the API call
  context: RequestContext;
  endpoint: string; // For logging purposes
  params: NcbiRequestParams; // For logging purposes
}

export class NcbiRequestQueueManager {
  private requestQueue: QueuedRequest[] = [];
  private isProcessingQueue = false;
  private lastRequestTime = 0;

  constructor() {
    // The constructor is kept for future initializations, if any.
  }

  /**
   * Processes the request queue, ensuring delays between requests to respect NCBI rate limits.
   */
  private async processQueue(): Promise<void> {
    if (this.isProcessingQueue || this.requestQueue.length === 0) {
      return;
    }
    this.isProcessingQueue = true;

    const requestItem = this.requestQueue.shift();
    if (!requestItem) {
      this.isProcessingQueue = false;
      return;
    }

    const { resolve, reject, task, context, endpoint, params } = requestItem;

    try {
      const now = Date.now();
      const timeSinceLastRequest = now - this.lastRequestTime;
      const delayNeeded = config.ncbiRequestDelayMs - timeSinceLastRequest;

      if (delayNeeded > 0) {
        logger.debug(
          `Delaying NCBI request by ${delayNeeded}ms to respect rate limit.`,
          requestContextService.createRequestContext({
            ...context,
            operation: "NCBI_RateLimitDelay",
            delayNeeded,
            endpoint,
          }),
        );
        await new Promise((r) => setTimeout(r, delayNeeded));
      }

      this.lastRequestTime = Date.now();
      logger.info(
        `Executing NCBI request via queue: ${endpoint}`,
        requestContextService.createRequestContext({
          ...context,
          operation: "NCBI_ExecuteFromQueue",
          endpoint,
          params: sanitizeInputForLogging(params),
        }),
      );
      const result = await task();
      resolve(result);
    } catch (error: unknown) {
      const err = error as Error;
      logger.error(
        "Error processing NCBI request from queue",
        err,
        requestContextService.createRequestContext({
          ...context,
          operation: "NCBI_QueueError",
          endpoint,
          params: sanitizeInputForLogging(params),
          errorMessage: err?.message,
        }),
      );
      reject(err);
    } finally {
      this.isProcessingQueue = false;
      if (this.requestQueue.length > 0) {
        // Ensure processQueue is called without awaiting it here to prevent deep stacks
        Promise.resolve().then(() => this.processQueue());
      }
    }
  }

  /**
   * Enqueues a task (an NCBI API call) to be processed.
   * @param task A function that returns a Promise resolving to the API call result.
   * @param context The request context for logging and correlation.
   * @param endpoint The NCBI endpoint being called (e.g., "esearch", "efetch").
   * @param params The parameters for the NCBI request.
   * @returns A Promise that resolves or rejects with the result of the task.
   */
  public enqueueRequest<T>(
    task: () => Promise<T>,
    context: RequestContext,
    endpoint: string,
    params: NcbiRequestParams,
  ): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      this.requestQueue.push({
        resolve: (value: unknown) => resolve(value as T),
        reject: (reason?: unknown) => reject(reason),
        task,
        context,
        endpoint,
        params,
      });
      if (!this.isProcessingQueue) {
        // Ensure processQueue is called without awaiting it here
        Promise.resolve().then(() => this.processQueue());
      }
    });
  }
}
