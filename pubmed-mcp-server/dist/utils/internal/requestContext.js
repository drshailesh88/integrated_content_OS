/**
 * @fileoverview Utilities for creating and managing request contexts.
 * A request context is an object carrying a unique ID, timestamp, and other
 * relevant data for logging, tracing, and processing. It also defines
 * configuration and operational context structures.
 * @module src/utils/internal/requestContext
 */
import { trace } from "@opentelemetry/api";
import { generateUUID } from "../index.js";
import { logger } from "./logger.js";
/**
 * Singleton-like service object for managing request context operations.
 * @private
 */
const requestContextServiceInstance = {
    /**
     * Internal configuration store for the service.
     */
    config: {},
    /**
     * Configures the request context service with new settings.
     * Merges the provided partial configuration with existing settings.
     *
     * @param config - A partial `ContextConfig` object containing settings to update or add.
     * @returns A shallow copy of the newly updated configuration.
     */
    configure(config) {
        this.config = {
            ...this.config,
            ...config,
        };
        const logContext = this.createRequestContext({
            operation: "RequestContextService.configure",
            newConfigState: { ...this.config },
        });
        logger.debug("RequestContextService configuration updated", logContext);
        return { ...this.config };
    },
    /**
     * Retrieves a shallow copy of the current service configuration.
     * This prevents direct mutation of the internal configuration state.
     *
     * @returns A shallow copy of the current `ContextConfig`.
     */
    getConfig() {
        return { ...this.config };
    },
    /**
     * Creates a new {@link RequestContext} instance.
     * Each context is assigned a unique `requestId` (UUID) and a current `timestamp` (ISO 8601).
     * Additional custom properties can be merged into the context.
     *
     * @param additionalContext - An optional record of key-value pairs to be
     *   included in the created request context.
     * @returns A new `RequestContext` object.
     */
    createRequestContext(additionalContext = {}) {
        const requestId = generateUUID();
        const timestamp = new Date().toISOString();
        const context = {
            requestId,
            timestamp,
            ...additionalContext,
        };
        // --- OpenTelemetry Integration ---
        // Automatically inject active trace and span IDs into the context for correlation.
        const activeSpan = trace.getActiveSpan();
        if (activeSpan) {
            const spanContext = activeSpan.spanContext();
            context.traceId = spanContext.traceId;
            context.spanId = spanContext.spanId;
        }
        // --- End OpenTelemetry Integration ---
        return context;
    },
};
/**
 * Primary export for request context functionalities.
 * This service provides methods to create and manage {@link RequestContext} instances,
 * which are essential for logging, tracing, and correlating operations.
 */
export const requestContextService = requestContextServiceInstance;
//# sourceMappingURL=requestContext.js.map