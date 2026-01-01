/**
 * @fileoverview Provides a utility for performance monitoring of tool execution.
 * This module introduces a higher-order function to wrap tool logic, measure its
 * execution time, and log a structured metrics event.
 * @module src/utils/internal/performance
 */
import { RequestContext } from "./requestContext.js";
/**
 * A higher-order function that wraps a tool's core logic to measure its performance
 * and log a structured metrics event upon completion.
 *
 * @template T The expected return type of the tool's logic function.
 * @param toolLogicFn - The asynchronous tool logic function to be executed and measured.
 * @param context - The request context for the operation, used for logging and tracing.
 * @param inputPayload - The input payload to the tool for size calculation.
 * @returns A promise that resolves with the result of the tool logic function.
 * @throws Re-throws any error caught from the tool logic function after logging the failure.
 */
export declare function measureToolExecution<T>(toolLogicFn: () => Promise<T>, context: RequestContext & {
    toolName: string;
}, inputPayload: unknown): Promise<T>;
//# sourceMappingURL=performance.d.ts.map