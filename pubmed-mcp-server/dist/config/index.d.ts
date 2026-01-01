/**
 * @fileoverview Loads, validates, and exports application configuration.
 * This module centralizes configuration management, sourcing values from
 * environment variables and `package.json`. It uses Zod for schema validation
 * to ensure type safety and correctness of configuration parameters.
 *
 * @module src/config/index
 */
export declare const config: {
    pkg: {
        name: string;
        version: string;
        description: string;
    };
    mcpServerName: string;
    mcpServerVersion: string;
    mcpServerDescription: string;
    logLevel: string;
    logsPath: string | null;
    environment: string;
    mcpTransportType: "stdio" | "http";
    mcpSessionMode: "stateless" | "stateful" | "auto";
    mcpHttpPort: number;
    mcpHttpHost: string;
    mcpHttpEndpointPath: string;
    mcpHttpMaxPortRetries: number;
    mcpHttpPortRetryDelayMs: number;
    mcpStatefulSessionStaleTimeoutMs: number;
    mcpAllowedOrigins: string[] | undefined;
    mcpAuthMode: "jwt" | "oauth" | "none";
    mcpAuthSecretKey: string | undefined;
    oauthIssuerUrl: string | undefined;
    oauthJwksUri: string | undefined;
    oauthAudience: string | undefined;
    devMcpClientId: string | undefined;
    devMcpScopes: string[] | undefined;
    ncbiApiKey: string | undefined;
    ncbiToolIdentifier: string;
    ncbiAdminEmail: string | undefined;
    ncbiRequestDelayMs: number;
    ncbiMaxRetries: number;
    openTelemetry: {
        enabled: boolean;
        serviceName: string;
        serviceVersion: string;
        tracesEndpoint: string | undefined;
        metricsEndpoint: string | undefined;
        samplingRatio: number;
        logLevel: "NONE" | "ERROR" | "WARN" | "INFO" | "DEBUG" | "VERBOSE" | "ALL";
    };
};
export declare const logLevel: string;
export declare const environment: string;
//# sourceMappingURL=index.d.ts.map