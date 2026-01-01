/**
 * @fileoverview Provides a high-fidelity bridge between the MCP SDK's Node.js-style
 * streamable HTTP transport and Hono's Web Standards-based streaming response.
 * This class is essential for adapting the Node.js `http.ServerResponse` API
 * to a format consumable by modern web frameworks.
 * @module src/mcp-server/transports/core/honoNodeBridge
 */
import { PassThrough } from "stream";
import type { OutgoingHttpHeaders } from "http";
/**
 * A mock `http.ServerResponse` that pipes all written data to a `PassThrough` stream.
 *
 * This class serves as a critical compatibility layer, emulating the behavior of a
 * Node.js `ServerResponse` to capture status codes, headers, and the response body.
 * The captured data can then be used to construct a Web-standard `Response` object,
 * for instance in a Hono application. It pays close attention to the timing of when
 * headers are considered "sent" to mimic Node.js behavior accurately.
 */
export declare class HonoStreamResponse extends PassThrough {
    statusCode: number;
    headers: OutgoingHttpHeaders;
    private _headersSent;
    constructor();
    /**
     * A getter that reports whether the headers have been sent.
     * In this emulation, headers are considered sent the first time `write()` or `end()` is called.
     */
    get headersSent(): boolean;
    /**
     * Sets the status code and headers for the response, mimicking `http.ServerResponse.writeHead`.
     *
     * @param statusCode - The HTTP status code.
     * @param statusMessageOrHeaders - An optional status message (string) or headers object.
     * @param headers - An optional headers object, used if the second argument is a status message.
     * @returns The instance of the class for chaining.
     */
    writeHead(statusCode: number, statusMessageOrHeaders?: string | OutgoingHttpHeaders, headers?: OutgoingHttpHeaders): this;
    /**
     * Sets a single header value.
     *
     * @param name - The name of the header.
     * @param value - The value of the header.
     * @returns The instance of the class for chaining.
     */
    setHeader(name: string, value: string | number | string[]): this;
    /**
     * Gets a header that has been queued for the response.
     * @param name - The name of the header.
     * @returns The value of the header, or undefined if not set.
     */
    getHeader(name: string): string | number | string[] | undefined;
    /**
     * Returns a copy of the current outgoing headers.
     */
    getHeaders(): OutgoingHttpHeaders;
    /**
     * Removes a header that has been queued for the response.
     * @param name - The name of the header to remove.
     */
    removeHeader(name: string): void;
    /**
     * A private helper to mark headers as sent. This is called implicitly
     * before any part of the body is written.
     */
    private ensureHeadersSent;
    /**
     * Writes a chunk of the response body, mimicking `http.ServerResponse.write`.
     * This is the first point where headers are implicitly flushed.
     */
    write(chunk: unknown, encodingOrCallback?: BufferEncoding | ((error: Error | null | undefined) => void), callback?: (error: Error | null | undefined) => void): boolean;
    /**
     * Finishes sending the response, mimicking `http.ServerResponse.end`.
     * This also implicitly flushes headers if they haven't been sent yet.
     */
    end(chunk?: unknown, encodingOrCallback?: BufferEncoding | (() => void), callback?: () => void): this;
}
//# sourceMappingURL=honoNodeBridge.d.ts.map