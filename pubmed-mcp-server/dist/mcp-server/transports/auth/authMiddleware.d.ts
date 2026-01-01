/**
 * @fileoverview Defines a unified Hono middleware for authentication.
 * This middleware is strategy-agnostic. It extracts a Bearer token,
 * delegates verification to the provided authentication strategy, and
 * populates the async-local storage context with the resulting auth info.
 * @module src/mcp-server/transports/auth/authMiddleware
 */
import type { HttpBindings } from "@hono/node-server";
import type { Context, Next } from "hono";
import type { AuthStrategy } from "./strategies/authStrategy.js";
/**
 * Creates a Hono middleware function that enforces authentication using a given strategy.
 *
 * @param strategy - An instance of a class that implements the `AuthStrategy` interface.
 * @returns A Hono middleware function.
 */
export declare function createAuthMiddleware(strategy: AuthStrategy): (c: Context<{
    Bindings: HttpBindings;
}>, next: Next) => Promise<void>;
//# sourceMappingURL=authMiddleware.d.ts.map