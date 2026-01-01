import { AuthStrategy } from "./strategies/authStrategy.js";
/**
 * Creates and returns an authentication strategy instance based on the
 * application's configuration (`config.mcpAuthMode`).
 *
 * @returns An instance of a class that implements the `AuthStrategy` interface,
 *          or `null` if authentication is disabled (`none`).
 * @throws {Error} If the auth mode is unknown or misconfigured.
 */
export declare function createAuthStrategy(): AuthStrategy | null;
//# sourceMappingURL=authFactory.d.ts.map