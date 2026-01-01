import { RequestContext } from "./requestContext.js";
/**
 * Defines the supported logging levels based on RFC 5424 Syslog severity levels,
 * as used by the Model Context Protocol (MCP).
 * Levels are: 'debug'(7), 'info'(6), 'notice'(5), 'warning'(4), 'error'(3), 'crit'(2), 'alert'(1), 'emerg'(0).
 * Lower numeric values indicate higher severity.
 */
export type McpLogLevel = "debug" | "info" | "notice" | "warning" | "error" | "crit" | "alert" | "emerg";
/**
 * Interface for the payload of an MCP log notification.
 * This structure is used when sending log data via MCP `notifications/message`.
 */
export interface McpLogPayload {
    message: string;
    context?: RequestContext;
    error?: {
        message: string;
        stack?: string;
    };
    [key: string]: unknown;
}
/**
 * Type for the `data` parameter of the `McpNotificationSender` function.
 */
export type McpNotificationData = McpLogPayload | Record<string, unknown>;
/**
 * Defines the signature for a function that can send MCP log notifications.
 * This function is typically provided by the MCP server instance.
 * @param level - The severity level of the log message.
 * @param data - The payload of the log notification.
 * @param loggerName - An optional name or identifier for the logger/server.
 */
export type McpNotificationSender = (level: McpLogLevel, data: McpNotificationData, loggerName?: string) => void;
/**
 * Singleton Logger class that wraps Winston for robust logging.
 * Supports file logging, conditional console logging, and MCP notifications.
 */
export declare class Logger {
    private static instance;
    private winstonLogger?;
    private interactionLogger?;
    private initialized;
    private mcpNotificationSender?;
    private currentMcpLevel;
    private currentWinstonLevel;
    private readonly MCP_NOTIFICATION_STACK_TRACE_MAX_LENGTH;
    private readonly LOG_FILE_MAX_SIZE;
    private readonly LOG_MAX_FILES;
    /** @private */
    private constructor();
    /**
     * Initializes the Winston logger instance.
     * Should be called once at application startup.
     * @param level - The initial minimum MCP log level.
     */
    initialize(level?: McpLogLevel): Promise<void>;
    /**
     * Sets the function used to send MCP 'notifications/message'.
     * @param sender - The function to call for sending notifications, or undefined to disable.
     */
    setMcpNotificationSender(sender: McpNotificationSender | undefined): void;
    /**
     * Dynamically sets the minimum logging level.
     * @param newLevel - The new minimum MCP log level to set.
     */
    setLevel(newLevel: McpLogLevel): void;
    /**
     * Configures the console transport based on the current log level and TTY status.
     * Adds or removes the console transport as needed.
     * @returns {{ enabled: boolean, message: string | null }} Status of console logging.
     * @private
     */
    private _configureConsoleTransport;
    /**
     * Gets the singleton instance of the Logger.
     * @returns The singleton Logger instance.
     */
    static getInstance(): Logger;
    /**
     * Resets the singleton instance.
     * This is intended for use in testing environments only.
     */
    static resetForTesting(): void;
    /**
     * Ensures the logger has been initialized.
     * @returns True if initialized, false otherwise.
     * @private
     */
    private ensureInitialized;
    /**
     * Centralized log processing method.
     * @param level - The MCP severity level of the message.
     * @param msg - The main log message.
     * @param context - Optional request context for the log.
     * @param error - Optional error object associated with the log.
     * @private
     */
    private log;
    /** Logs a message at the 'debug' level. */
    debug(msg: string, context?: RequestContext): void;
    /** Logs a message at the 'info' level. */
    info(msg: string, context?: RequestContext): void;
    /** Logs a message at the 'notice' level. */
    notice(msg: string, context?: RequestContext): void;
    /** Logs a message at the 'warning' level. */
    warning(msg: string, context?: RequestContext): void;
    /**
     * Logs a message at the 'error' level.
     * @param msg - The main log message.
     * @param err - Optional. Error object or RequestContext.
     * @param context - Optional. RequestContext if `err` is an Error.
     */
    error(msg: string, err?: Error | RequestContext, context?: RequestContext): void;
    /**
     * Logs a message at the 'crit' (critical) level.
     * @param msg - The main log message.
     * @param err - Optional. Error object or RequestContext.
     * @param context - Optional. RequestContext if `err` is an Error.
     */
    crit(msg: string, err?: Error | RequestContext, context?: RequestContext): void;
    /**
     * Logs a message at the 'alert' level.
     * @param msg - The main log message.
     * @param err - Optional. Error object or RequestContext.
     * @param context - Optional. RequestContext if `err` is an Error.
     */
    alert(msg: string, err?: Error | RequestContext, context?: RequestContext): void;
    /**
     * Logs a message at the 'emerg' (emergency) level.
     * @param msg - The main log message.
     * @param err - Optional. Error object or RequestContext.
     * @param context - Optional. RequestContext if `err` is an Error.
     */
    emerg(msg: string, err?: Error | RequestContext, context?: RequestContext): void;
    /**
     * Logs a message at the 'emerg' (emergency) level, typically for fatal errors.
     * @param msg - The main log message.
     * @param err - Optional. Error object or RequestContext.
     * @param context - Optional. RequestContext if `err` is an Error.
     */
    fatal(msg: string, err?: Error | RequestContext, context?: RequestContext): void;
    /**
     * Logs a structured interaction object to a dedicated file.
     * @param interactionName - A name for the interaction type (e.g., 'OpenRouterIO').
     * @param data - The structured data to log.
     */
    logInteraction(interactionName: string, data: Record<string, unknown>): void;
}
/**
 * The singleton instance of the Logger.
 * Use this instance for all logging operations.
 */
export declare const logger: Logger;
//# sourceMappingURL=logger.d.ts.map