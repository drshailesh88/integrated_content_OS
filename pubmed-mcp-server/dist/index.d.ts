#!/usr/bin/env node
/**
 * @fileoverview Main entry point for the MCP TypeScript Template application.
 * This script initializes the configuration, sets up the logger, starts the
 * MCP server (either via STDIO or HTTP transport), and handles graceful
 * shutdown on process signals or unhandled errors.
 *
 * The script uses an Immediately Invoked Function Expression (IIFE) with async/await
 * to manage the asynchronous nature of server startup and shutdown.
 *
 * Key operations:
 * 1. Import necessary modules and utilities.
 * 2. Define a `shutdown` function for graceful server termination.
 * 3. Define a `start` function to:
 *    - Initialize the logger with the configured log level.
 *    - Create a startup request context for logging and correlation.
 *    - Initialize and start the MCP server transport (stdio or http).
 *    - Set up global error handlers (uncaughtException, unhandledRejection)
 *      and signal handlers (SIGTERM, SIGINT) to trigger graceful shutdown.
 * 4. Execute the `start` function within an async IIFE.
 *
 * @module src/index
 */
export {};
//# sourceMappingURL=index.d.ts.map