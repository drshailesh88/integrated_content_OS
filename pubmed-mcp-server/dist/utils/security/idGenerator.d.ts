/**
 * Defines the structure for configuring entity prefixes.
 * Keys are entity type names (e.g., "project", "task"), and values are their corresponding ID prefixes (e.g., "PROJ", "TASK").
 */
export interface EntityPrefixConfig {
    [key: string]: string;
}
/**
 * Defines options for customizing ID generation.
 */
export interface IdGenerationOptions {
    length?: number;
    separator?: string;
    charset?: string;
}
/**
 * A generic ID Generator class for creating and managing unique, prefixed identifiers.
 * Allows defining custom prefixes, generating random strings, and validating/normalizing IDs.
 */
export declare class IdGenerator {
    /**
     * Default character set for the random part of the ID.
     * @private
     */
    private static DEFAULT_CHARSET;
    /**
     * Default separator character between prefix and random part.
     * @private
     */
    private static DEFAULT_SEPARATOR;
    /**
     * Default length for the random part of the ID.
     * @private
     */
    private static DEFAULT_LENGTH;
    /**
     * Stores the mapping of entity types to their prefixes.
     * @private
     */
    private entityPrefixes;
    /**
     * Stores a reverse mapping from prefixes (case-insensitive) to entity types.
     * @private
     */
    private prefixToEntityType;
    /**
     * Constructs an `IdGenerator` instance.
     * @param entityPrefixes - An initial map of entity types to their prefixes.
     */
    constructor(entityPrefixes?: EntityPrefixConfig);
    /**
     * Sets or updates the entity prefix configuration and rebuilds the internal reverse lookup map.
     * @param entityPrefixes - A map where keys are entity type names and values are their desired ID prefixes.
     */
    setEntityPrefixes(entityPrefixes: EntityPrefixConfig): void;
    /**
     * Retrieves a copy of the current entity prefix configuration.
     * @returns The current entity prefix configuration.
     */
    getEntityPrefixes(): EntityPrefixConfig;
    /**
     * Generates a cryptographically secure random string.
     * @param length - The desired length of the random string. Defaults to `IdGenerator.DEFAULT_LENGTH`.
     * @param charset - The character set to use. Defaults to `IdGenerator.DEFAULT_CHARSET`.
     * @returns The generated random string.
     */
    generateRandomString(length?: number, charset?: string): string;
    /**
     * Generates a unique ID, optionally prepended with a prefix.
     * @param prefix - An optional prefix for the ID.
     * @param options - Optional parameters for ID generation (length, separator, charset).
     * @returns A unique identifier string.
     */
    generate(prefix?: string, options?: IdGenerationOptions): string;
    /**
     * Generates a unique ID for a specified entity type, using its configured prefix.
     * @param entityType - The type of entity (must be registered).
     * @param options - Optional parameters for ID generation.
     * @returns A unique identifier string for the entity (e.g., "PROJ_A6B3J0").
     * @throws {McpError} If the `entityType` is not registered.
     */
    generateForEntity(entityType: string, options?: IdGenerationOptions): string;
    /**
     * Validates if an ID conforms to the expected format for a specific entity type.
     * @param id - The ID string to validate.
     * @param entityType - The expected entity type of the ID.
     * @param options - Optional parameters used during generation for validation consistency.
     *                  The `charset` from these options will be used for validation.
     * @returns `true` if the ID is valid, `false` otherwise.
     */
    isValid(id: string, entityType: string, options?: IdGenerationOptions): boolean;
    /**
     * Escapes special characters in a string for use in a regular expression.
     * @param str - The string to escape.
     * @returns The escaped string.
     * @private
     */
    private escapeRegex;
    /**
     * Strips the prefix and separator from an ID string.
     * @param id - The ID string (e.g., "PROJ_A6B3J0").
     * @param separator - The separator used in the ID. Defaults to `IdGenerator.DEFAULT_SEPARATOR`.
     * @returns The ID part without the prefix, or the original ID if separator not found.
     */
    stripPrefix(id: string, separator?: string): string;
    /**
     * Determines the entity type from an ID string by its prefix (case-insensitive).
     * @param id - The ID string (e.g., "PROJ_A6B3J0").
     * @param separator - The separator used in the ID. Defaults to `IdGenerator.DEFAULT_SEPARATOR`.
     * @returns The determined entity type.
     * @throws {McpError} If ID format is invalid or prefix is unknown.
     */
    getEntityType(id: string, separator?: string): string;
    /**
     * Normalizes an entity ID to ensure the prefix matches the registered case
     * and the random part is uppercase. Note: This assumes the charset characters
     * have a meaningful uppercase version if case-insensitivity is desired for the random part.
     * For default charset (A-Z0-9), this is fine. For custom charsets, behavior might vary.
     * @param id - The ID to normalize (e.g., "proj_a6b3j0").
     * @param separator - The separator used in the ID. Defaults to `IdGenerator.DEFAULT_SEPARATOR`.
     * @returns The normalized ID (e.g., "PROJ_A6B3J0").
     * @throws {McpError} If the entity type cannot be determined from the ID.
     */
    normalize(id: string, separator?: string): string;
}
/**
 * Default singleton instance of the `IdGenerator`.
 * Initialize with `idGenerator.setEntityPrefixes({})` to configure.
 */
export declare const idGenerator: IdGenerator;
/**
 * Generates a standard Version 4 UUID (Universally Unique Identifier).
 * Uses the Node.js `crypto` module. This function is independent of the IdGenerator instance
 * to prevent circular dependencies when used by other utilities like requestContextService.
 * @returns A new UUID string.
 */
export declare const generateUUID: () => string;
//# sourceMappingURL=idGenerator.d.ts.map