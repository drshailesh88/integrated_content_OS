/**
 * @fileoverview Configures and starts the HTTP MCP transport using Hono.
 * This file has been refactored to correctly integrate Hono's streaming
 * capabilities with the Model Context Protocol SDK's transport layer.
 * @module src/mcp-server/transports/http/httpTransport
 */
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { stream } from "hono/streaming";
import http from "http";
import { config } from "../../../config/index.js";
import { logger, rateLimiter, requestContextService, } from "../../../utils/index.js";
import { createAuthMiddleware, createAuthStrategy } from "../auth/index.js";
import { StatelessTransportManager } from "../core/statelessTransportManager.js";
import { StatefulTransportManager } from "./../core/statefulTransportManager.js";
import { httpErrorHandler } from "./httpErrorHandler.js";
import { mcpTransportMiddleware } from "./mcpTransportMiddleware.js";
const HTTP_PORT = config.mcpHttpPort;
const HTTP_HOST = config.mcpHttpHost;
const MCP_ENDPOINT_PATH = config.mcpHttpEndpointPath;
/**
 * Extracts the client IP address from the request, prioritizing common proxy headers.
 * @param c - The Hono context object.
 * @returns The client's IP address or a default string if not found.
 */
function getClientIp(c) {
    const forwardedFor = c.req.header("x-forwarded-for");
    return ((forwardedFor?.split(",")[0] ?? "").trim() ||
        c.req.header("x-real-ip") ||
        "unknown_ip");
}
/**
 * Converts a Fetch API Headers object to Node.js IncomingHttpHeaders.
 * Hono uses Fetch API Headers, but the underlying transport managers expect
 * Node's native IncomingHttpHeaders.
 * @param headers - The Headers object to convert.
 * @returns An object compatible with IncomingHttpHeaders.
 */
async function isPortInUse(port, host, parentContext) {
    const context = { ...parentContext, operation: "isPortInUse", port, host };
    logger.debug(`Checking if port ${port} is in use...`, context);
    return new Promise((resolve) => {
        const tempServer = http.createServer();
        tempServer
            .once("error", (err) => {
            const inUse = err.code === "EADDRINUSE";
            logger.debug(`Port check resulted in error: ${err.code}. Port in use: ${inUse}`, context);
            resolve(inUse);
        })
            .once("listening", () => {
            logger.debug(`Successfully bound to port ${port} temporarily. Port is not in use.`, context);
            tempServer.close(() => resolve(false));
        })
            .listen(port, host);
    });
}
function startHttpServerWithRetry(app, initialPort, host, maxRetries, parentContext) {
    const startContext = {
        ...parentContext,
        operation: "startHttpServerWithRetry",
    };
    logger.info(`Attempting to start HTTP server on port ${initialPort} with ${maxRetries} retries.`, startContext);
    return new Promise((resolve, reject) => {
        const tryBind = (port, attempt) => {
            const attemptContext = { ...startContext, port, attempt };
            if (attempt > maxRetries + 1) {
                const error = new Error(`Failed to bind to any port after ${maxRetries} retries.`);
                logger.fatal(error.message, attemptContext);
                return reject(error);
            }
            isPortInUse(port, host, attemptContext)
                .then((inUse) => {
                if (inUse) {
                    logger.warning(`Port ${port} is in use, retrying on port ${port + 1}...`, attemptContext);
                    setTimeout(() => tryBind(port + 1, attempt + 1), config.mcpHttpPortRetryDelayMs);
                    return;
                }
                try {
                    const serverInstance = serve({ fetch: app.fetch, port, hostname: host }, (info) => {
                        const serverAddress = `http://${info.address}:${info.port}${MCP_ENDPOINT_PATH}`;
                        logger.info(`HTTP transport listening at ${serverAddress}`, {
                            ...attemptContext,
                            address: serverAddress,
                            sessionMode: config.mcpSessionMode,
                        });
                        if (process.stdout.isTTY) {
                            console.log(`\n🚀 MCP Server running at: ${serverAddress}`);
                            console.log(`   Session Mode: ${config.mcpSessionMode}\n`);
                        }
                    });
                    resolve(serverInstance);
                }
                catch (err) {
                    if (err &&
                        typeof err === "object" &&
                        "code" in err &&
                        err.code !== "EADDRINUSE") {
                        const errorToLog = err instanceof Error ? err : new Error(String(err));
                        logger.error("An unexpected error occurred while starting the server.", errorToLog, attemptContext);
                        return reject(err);
                    }
                    logger.warning(`Encountered EADDRINUSE race condition on port ${port}, retrying...`, attemptContext);
                    setTimeout(() => tryBind(port + 1, attempt + 1), config.mcpHttpPortRetryDelayMs);
                }
            })
                .catch((err) => {
                const error = err instanceof Error ? err : new Error(String(err));
                logger.fatal("Failed to check if port is in use.", error, attemptContext);
                reject(err);
            });
        };
        tryBind(initialPort, 1);
    });
}
function createTransportManager(createServerInstanceFn, sessionMode, context) {
    const opContext = {
        ...context,
        operation: "createTransportManager",
        sessionMode,
    };
    logger.info(`Creating transport manager for session mode: ${sessionMode}`, opContext);
    const statefulOptions = {
        staleSessionTimeoutMs: config.mcpStatefulSessionStaleTimeoutMs,
        mcpHttpEndpointPath: config.mcpHttpEndpointPath,
    };
    const getMcpServer = async () => (await createServerInstanceFn()).server;
    switch (sessionMode) {
        case "stateless":
            return new StatelessTransportManager(getMcpServer);
        case "stateful":
            return new StatefulTransportManager(getMcpServer, statefulOptions);
        case "auto":
        default:
            logger.info("Defaulting to 'auto' mode (stateful with stateless fallback).", opContext);
            return new StatefulTransportManager(getMcpServer, statefulOptions);
    }
}
export function createHttpApp(transportManager, createServerInstanceFn, parentContext) {
    const app = new Hono();
    const transportContext = {
        ...parentContext,
        component: "HttpTransportSetup",
    };
    logger.info("Creating Hono HTTP application.", transportContext);
    app.use("*", cors({
        origin: config.mcpAllowedOrigins || [],
        allowMethods: ["GET", "POST", "DELETE", "OPTIONS"],
        allowHeaders: [
            "Content-Type",
            "Mcp-Session-Id",
            "Last-Event-ID",
            "Authorization",
        ],
        credentials: true,
    }));
    app.use("*", async (c, next) => {
        c.env.outgoing.setHeader("X-Content-Type-Options", "nosniff");
        await next();
    });
    app.use(MCP_ENDPOINT_PATH, async (c, next) => {
        const clientIp = getClientIp(c);
        const context = requestContextService.createRequestContext({
            operation: "httpRateLimitCheck",
            ipAddress: clientIp,
        });
        try {
            rateLimiter.check(clientIp, context);
            logger.debug("Rate limit check passed.", context);
        }
        catch (error) {
            logger.warning("Rate limit check failed.", {
                ...context,
                error: error instanceof Error ? error.message : String(error),
            });
            throw error;
        }
        await next();
    });
    const authStrategy = createAuthStrategy();
    if (authStrategy) {
        logger.info("Authentication strategy found, enabling auth middleware.", transportContext);
        app.use(MCP_ENDPOINT_PATH, createAuthMiddleware(authStrategy));
    }
    else {
        logger.info("No authentication strategy found, auth middleware disabled.", transportContext);
    }
    app.onError(httpErrorHandler);
    app.get("/healthz", (c) => {
        return c.json({
            status: "ok",
            timestamp: new Date().toISOString(),
        });
    });
    app.get(MCP_ENDPOINT_PATH, async (c) => {
        const sessionId = c.req.header("mcp-session-id");
        if (sessionId) {
            return c.text("GET requests to existing sessions are not supported.", 405);
        }
        // Since this is a stateless endpoint, we create a temporary instance
        // to report on the server's configuration.
        const { tools, identity, options } = await createServerInstanceFn();
        const effectiveSessionMode = transportManager instanceof StatefulTransportManager
            ? "stateful"
            : "stateless";
        return c.json({
            status: "ok",
            server: {
                name: identity.name,
                version: identity.version,
                description: identity.description || "No description provided.",
                nodeVersion: process.version,
                environment: config.environment,
                capabilities: options.capabilities,
            },
            sessionMode: {
                configured: config.mcpSessionMode,
                effective: effectiveSessionMode,
            },
            tools: tools,
            message: "Server is running. POST to this endpoint to execute a tool call.",
        });
    });
    app.post(MCP_ENDPOINT_PATH, mcpTransportMiddleware(transportManager, createServerInstanceFn), (c) => {
        const response = c.get("mcpResponse");
        if (response.sessionId) {
            c.header("Mcp-Session-Id", response.sessionId);
        }
        response.headers.forEach((value, key) => {
            c.header(key, value);
        });
        c.status(response.statusCode);
        if (response.type === "stream") {
            return stream(c, async (s) => {
                await s.pipe(response.stream);
            });
        }
        else {
            const body = typeof response.body === "object" && response.body !== null
                ? response.body
                : { body: response.body };
            return c.json(body);
        }
    });
    app.delete(MCP_ENDPOINT_PATH, async (c) => {
        const sessionId = c.req.header("mcp-session-id");
        const context = requestContextService.createRequestContext({
            ...transportContext,
            operation: "handleDeleteRequest",
            sessionId,
        });
        if (sessionId) {
            if (transportManager instanceof StatefulTransportManager) {
                const response = await transportManager.handleDeleteRequest(sessionId, context);
                if (response.type === "buffered") {
                    const body = typeof response.body === "object" && response.body !== null
                        ? response.body
                        : { body: response.body };
                    return c.json(body, response.statusCode);
                }
                // Fallback for unexpected stream response on DELETE
                return c.body(null, response.statusCode);
            }
            else {
                return c.json({
                    error: "Method Not Allowed",
                    message: "DELETE operations are not supported in this mode.",
                }, 405);
            }
        }
        else {
            return c.json({
                status: "stateless_mode",
                message: "No sessions to delete in stateless mode",
            });
        }
    });
    logger.info("Hono application setup complete.", transportContext);
    return app;
}
export async function startHttpTransport(createServerInstanceFn, parentContext) {
    const transportContext = {
        ...parentContext,
        component: "HttpTransportStart",
    };
    logger.info("Starting HTTP transport.", transportContext);
    const transportManager = createTransportManager(createServerInstanceFn, config.mcpSessionMode, transportContext);
    const app = createHttpApp(transportManager, createServerInstanceFn, transportContext);
    const server = await startHttpServerWithRetry(app, HTTP_PORT, HTTP_HOST, config.mcpHttpMaxPortRetries, transportContext);
    logger.info("HTTP transport started successfully.", transportContext);
    return { app, server, transportManager };
}
//# sourceMappingURL=httpTransport.js.map