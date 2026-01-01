import { NodeSDK } from "@opentelemetry/sdk-node";
export declare let sdk: NodeSDK | null;
/**
 * Gracefully shuts down the OpenTelemetry SDK.
 * This function is called during the application's shutdown sequence.
 */
export declare function shutdownOpenTelemetry(): Promise<void>;
//# sourceMappingURL=instrumentation.d.ts.map