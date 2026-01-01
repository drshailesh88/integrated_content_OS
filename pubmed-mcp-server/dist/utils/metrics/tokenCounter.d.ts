/**
 * @fileoverview Provides utility functions for counting tokens in text and chat messages
 * using the `tiktoken` library, specifically configured for 'gpt-4o' tokenization.
 * These functions are essential for managing token limits and estimating costs
 * when interacting with language models.
 * @module src/utils/metrics/tokenCounter
 */
import { ChatCompletionMessageParam } from "openai/resources/chat/completions";
import { RequestContext } from "../index.js";
/**
 * Calculates the number of tokens for a given text string using the
 * tokenizer specified by `TOKENIZATION_MODEL`.
 * Wraps tokenization in `ErrorHandler.tryCatch` for robust error management.
 *
 * @param text - The input text to tokenize.
 * @param context - Optional request context for logging and error handling.
 * @returns A promise that resolves with the number of tokens in the text.
 * @throws {McpError} If tokenization fails.
 */
export declare function countTokens(text: string, context?: RequestContext): Promise<number>;
/**
 * Calculates the estimated number of tokens for an array of chat messages.
 * Uses the tokenizer specified by `TOKENIZATION_MODEL` and accounts for
 * special tokens and message overhead according to OpenAI's guidelines.
 *
 * For multi-part content, only text parts are currently tokenized.
 *
 * Reference: {@link https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb}
 *
 * @param messages - An array of chat messages.
 * @param context - Optional request context for logging and error handling.
 * @returns A promise that resolves with the estimated total number of tokens.
 * @throws {McpError} If tokenization fails.
 */
export declare function countChatTokens(messages: ReadonlyArray<ChatCompletionMessageParam>, context?: RequestContext): Promise<number>;
//# sourceMappingURL=tokenCounter.d.ts.map