import { RequestContext } from "../index.js";
/**
 * Defines configuration options for the {@link RateLimiter}.
 */
export interface RateLimitConfig {
    /** Time window in milliseconds. */
    windowMs: number;
    /** Maximum number of requests allowed in the window. */
    maxRequests: number;
    /** Custom error message template. Can include `{waitTime}` placeholder. */
    errorMessage?: string;
    /** If true, skip rate limiting in development. */
    skipInDevelopment?: boolean;
    /** Optional function to generate a custom key for rate limiting. */
    keyGenerator?: (identifier: string, context?: RequestContext) => string;
    /** How often, in milliseconds, to clean up expired entries. */
    cleanupInterval?: number;
}
/**
 * Represents an individual entry for tracking requests against a rate limit key.
 */
export interface RateLimitEntry {
    /** Current request count. */
    count: number;
    /** When the window resets (timestamp in milliseconds). */
    resetTime: number;
}
/**
 * A generic rate limiter class using an in-memory store.
 * Controls frequency of operations based on unique keys.
 */
export declare class RateLimiter {
    private config;
    /**
     * Stores current request counts and reset times for each key.
     * @private
     */
    private limits;
    /**
     * Timer ID for periodic cleanup.
     * @private
     */
    private cleanupTimer;
    /**
     * Default configuration values.
     * @private
     */
    private static DEFAULT_CONFIG;
    /**
     * Creates a new `RateLimiter` instance.
     * @param config - Configuration options, merged with defaults.
     */
    constructor(config: RateLimitConfig);
    /**
     * Starts the periodic timer to clean up expired rate limit entries.
     * @private
     */
    private startCleanupTimer;
    /**
     * Removes expired rate limit entries from the store.
     * @private
     */
    private cleanupExpiredEntries;
    /**
     * Updates the configuration of the rate limiter instance.
     * @param config - New configuration options to merge.
     */
    configure(config: Partial<RateLimitConfig>): void;
    /**
     * Retrieves a copy of the current rate limiter configuration.
     * @returns The current configuration.
     */
    getConfig(): RateLimitConfig;
    /**
     * Resets all rate limits by clearing the internal store.
     */
    reset(): void;
    /**
     * Checks if a request exceeds the configured rate limit.
     * Throws an `McpError` if the limit is exceeded.
     *
     * @param key - A unique identifier for the request source.
     * @param context - Optional request context for custom key generation.
     * @throws {McpError} If the rate limit is exceeded.
     */
    check(key: string, context?: RequestContext): void;
    /**
     * Retrieves the current rate limit status for a specific key.
     * @param key - The rate limit key.
     * @returns Status object or `null` if no entry exists.
     */
    getStatus(key: string): {
        current: number;
        limit: number;
        remaining: number;
        resetTime: number;
    } | null;
    /**
     * Stops the cleanup timer and clears all rate limit entries.
     * Call when the rate limiter is no longer needed.
     */
    dispose(): void;
}
/**
 * Default singleton instance of the `RateLimiter`.
 * Initialized with default configuration. Use `rateLimiter.configure({})` to customize.
 */
export declare const rateLimiter: RateLimiter;
//# sourceMappingURL=rateLimiter.d.ts.map