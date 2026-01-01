import { RequestContext } from "../index.js";
/**
 * Enum mirroring `partial-json`'s `Allow` constants. These specify
 * what types of partial JSON structures are permissible during parsing.
 * They can be combined using bitwise OR (e.g., `Allow.STR | Allow.OBJ`).
 *
 * The available properties are:
 * - `STR`: Allow partial string.
 * - `NUM`: Allow partial number.
 * - `ARR`: Allow partial array.
 * - `OBJ`: Allow partial object.
 * - `NULL`: Allow partial null.
 * - `BOOL`: Allow partial boolean.
 * - `NAN`: Allow partial NaN. (Note: Standard JSON does not support NaN)
 * - `INFINITY`: Allow partial Infinity. (Note: Standard JSON does not support Infinity)
 * - `_INFINITY`: Allow partial -Infinity. (Note: Standard JSON does not support -Infinity)
 * - `INF`: Allow both partial Infinity and -Infinity.
 * - `SPECIAL`: Allow all special values (NaN, Infinity, -Infinity).
 * - `ATOM`: Allow all atomic values (strings, numbers, booleans, null, special values).
 * - `COLLECTION`: Allow all collection values (objects, arrays).
 * - `ALL`: Allow all value types to be partial (default for `partial-json`'s parse).
 * @see {@link https://github.com/promplate/partial-json-parser-js} for more details.
 */
export declare const Allow: {
    STR: number;
    NUM: number;
    ARR: number;
    OBJ: number;
    NULL: number;
    BOOL: number;
    NAN: number;
    INFINITY: number;
    _INFINITY: number;
    INF: number;
    SPECIAL: number;
    ATOM: number;
    COLLECTION: number;
    ALL: number;
};
/**
 * Utility class for parsing potentially partial JSON strings.
 * Wraps the 'partial-json' library for robust JSON parsing, handling
 * incomplete structures and optional <think> blocks from LLMs.
 */
export declare class JsonParser {
    /**
     * Parses a JSON string, which may be partial or prefixed with a <think> block.
     * If a <think> block is present, its content is logged, and parsing proceeds on the
     * remainder. Uses 'partial-json' to handle incomplete JSON.
     *
     * @template T The expected type of the parsed JSON object. Defaults to `any`.
     * @param jsonString - The JSON string to parse.
     * @param allowPartial - Bitwise OR combination of `Allow` constants specifying permissible
     *   partial JSON types. Defaults to `Allow.ALL`.
     * @param context - Optional `RequestContext` for logging and error correlation.
     * @returns The parsed JavaScript value.
     * @throws {McpError} If the string is empty after processing or if `partial-json` fails.
     */
    parse<T = unknown>(jsonString: string, allowPartial?: number, context?: RequestContext): T;
}
/**
 * Singleton instance of the `JsonParser`.
 * Use this instance to parse JSON strings, with support for partial JSON and <think> blocks.
 * @example
 * ```typescript
 * import { jsonParser, Allow, requestContextService } from './utils';
 * const context = requestContextService.createRequestContext({ operation: 'TestJsonParsing' });
 *
 * const fullJson = '{"key": "value"}';
 * const parsedFull = jsonParser.parse(fullJson, Allow.ALL, context);
 * console.log(parsedFull); // Output: { key: 'value' }
 *
 * const partialObject = '<think>This is a thought.</think>{"key": "value", "arr": [1,';
 * try {
 *   const parsedPartial = jsonParser.parse(partialObject, undefined, context);
 *   console.log(parsedPartial);
 * } catch (e) {
 *   console.error("Parsing partial object failed:", e);
 * }
 * ```
 */
export declare const jsonParser: JsonParser;
//# sourceMappingURL=jsonParser.d.ts.map