/**
 * @fileoverview Manages a queue for NCBI E-utility requests to ensure compliance with rate limits.
 * @module src/services/NCBI/core/ncbiRequestQueueManager
 */
import { RequestContext } from "../../../utils/index.js";
import { NcbiRequestParams } from "./ncbiConstants.js";
/**
 * Interface for a queued NCBI request.
 */
export interface QueuedRequest<T = unknown> {
    resolve: (value: T | PromiseLike<T>) => void;
    reject: (reason?: unknown) => void;
    task: () => Promise<T>;
    context: RequestContext;
    endpoint: string;
    params: NcbiRequestParams;
}
export declare class NcbiRequestQueueManager {
    private requestQueue;
    private isProcessingQueue;
    private lastRequestTime;
    constructor();
    /**
     * Processes the request queue, ensuring delays between requests to respect NCBI rate limits.
     */
    private processQueue;
    /**
     * Enqueues a task (an NCBI API call) to be processed.
     * @param task A function that returns a Promise resolving to the API call result.
     * @param context The request context for logging and correlation.
     * @param endpoint The NCBI endpoint being called (e.g., "esearch", "efetch").
     * @param params The parameters for the NCBI request.
     * @returns A Promise that resolves or rejects with the result of the task.
     */
    enqueueRequest<T>(task: () => Promise<T>, context: RequestContext, endpoint: string, params: NcbiRequestParams): Promise<T>;
}
//# sourceMappingURL=ncbiRequestQueueManager.d.ts.map