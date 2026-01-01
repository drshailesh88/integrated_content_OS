# pubmed-mcp-server: Developer Guide & Architectural Standards

**Effective Date:** 2025-08-01
**Version:** 2.3

## Preamble

This document constitutes the official mandate governing all development practices, architectural patterns, and operational procedures for the `pubmed-mcp-server`. It is the single source of truth for ensuring code quality, consistency, and long-term maintainability. Adherence to these standards is not optional; it is a condition of all development activity.

## I. Core Architectural Principles

The architecture is founded upon a strict separation of concerns to guarantee modularity, testability, and operational clarity. These principles are non-negotiable.

### 1. The Logic Throws, The Handler Catches

This is the immutable cornerstone of the error-handling and control-flow strategy.

- **Core Logic (`logic.ts`):** This layer's sole responsibility is the execution of business logic. It shall be pure, self-contained, and stateless where possible. If an operational or validation error occurs (e.g., failed validation, API error), it **must** terminate its execution by throwing a structured `McpError`. Logic files **must not** contain `try...catch` blocks for the purpose of formatting a final response.
- **Handlers (`registration.ts`, Transports):** This layer's responsibility is to interface with the transport layer (e.g., MCP, HTTP), invoke core logic, and manage the final response lifecycle. It **must** wrap every call to the logic layer in a `try...catch` block. This is the exclusive location where errors are caught, processed by the `ErrorHandler`, and formatted into a definitive `CallToolResult` or HTTP response.

### 2. Structured, Traceable Operations

Every operation must be fully traceable from initiation to completion via structured logging and context propagation.

- **`RequestContext`**: Any significant operation shall be initiated by creating a `RequestContext` via `requestContextService.createRequestContext()`. This context, containing a unique `requestId`, must be passed as an argument through the entire call stack of the operation.
- **`Logger`**: All logging shall be performed through the centralized `logger` singleton. Every log entry must include the `RequestContext` to ensure traceability.

### 3. Comprehensive Observability (OpenTelemetry)

The system shall be fully observable out-of-the-box through integrated, comprehensive OpenTelemetry (OTel) instrumentation.

- **Automatic Instrumentation:** The OTel SDK is initialized at the application's entry point (`src/index.ts`) **before any other module is imported**. This ensures that all supported libraries (e.g., HTTP, DNS) are automatically instrumented for distributed tracing.
- **Trace-Aware Context:** The `RequestContext` is automatically enriched with the active `traceId` and `spanId` from OTel. This links every log entry directly to a specific trace, enabling seamless correlation between logs, traces, and metrics.
- **Error-Trace Correlation:** The central `ErrorHandler` automatically records exceptions on the active OTel span and sets its status to `ERROR`. This ensures that every handled error is visible and searchable within the distributed trace, providing a complete picture of the failure.
- **Performance Spans:** Utilities should be used to create detailed spans for every tool call, capturing critical performance metrics (duration, success status, error codes) as attributes. This provides granular insight into the performance of individual tools.

### 4. Application Lifecycle and Execution Flow

This section outlines the complete operational flow of the application, from initial startup to the execution of a tool's core logic. Understanding this sequence is critical for contextualizing the role of each component.

**A. Server Startup Sequence (Executed Once)**

1.  **Observability Initialization (`src/utils/telemetry/instrumentation.ts`):** The very first import in `src/index.ts` is the OpenTelemetry instrumentation module. This initializes the OTel SDK, sets up exporters, and patches supported libraries for automatic tracing.
2.  **Entry Point (`src/index.ts`):** The application is launched. This script performs the first-level setup, initializes the logger, calls `initializeAndStartServer()`, and establishes global process listeners for graceful shutdown.
3.  **Server Orchestration (`src/mcp-server/server.ts`):** This script orchestrates the creation and configuration of the MCP server, importing and calling the `register...` function from every tool and resource.
4.  **Tool Registration (`src/mcp-server/tools/toolName/registration.ts`):** During startup, each `register...` function is executed, calling `server.registerTool()` and providing the tool's metadata and runtime handler function.

**B. Tool Execution Sequence (Executed for Each Tool Call)**

1.  **Transport Layer:** The server's transport receives an incoming tool call request, and an OTel span is automatically created.
2.  **Server Core:** The `McpServer` instance parses the request, validates it against the registered input schema, and invokes the corresponding handler function.
3.  **Handler Execution (`registration.ts`):** The handler function creates a new `RequestContext`, begins a `try...catch` block, and calls the core logic function.
4.  **Logic Execution (`logic.ts`):** The logic function runs, performing its business logic. It returns a structured response on success or **throws** a structured `McpError` on failure.
5.  **Response Handling (`registration.ts`):** The `try...catch` block handles the outcome, formatting a success or error `CallToolResult` and ensuring the error is logged and traced via the `ErrorHandler`.
6.  **Final Transmission:** The server core sends the formatted response back to the client.

## II. Tool Development Workflow

This section mandates the workflow for creating and modifying all tools. Deviation is not permitted.

### A. File and Directory Structure

Each tool shall reside in its own directory within `src/mcp-server/tools/` and follow this structure:

- **`toolName/`**
  - **`index.ts`**: A barrel file that exports only the `register...` function from `registration.ts`.
  - **`logic.ts`**: Contains the core business logic. It **must** define and export the tool's Zod input schema, all inferred TypeScript types (input and output), and the main logic function.
  - **`registration.ts`**: Registers the tool with the MCP server. It imports from `logic.ts` and implements the "Handler" role.
  - **`logic/` (Optional Subdirectory)**: For complex tools, logic can be broken down into smaller files within this directory, orchestrated by the main `logic.ts`.

### B. The Canonical Pattern

The following pattern is the authoritative implementation and shall be used as the template for all new tool development. The `PubMedFetchContents` tool is a project-specific implementation of this standard.

**Step 1: Define Schema and Logic (`logic.ts`)**
The `logic.ts` file defines the tool's contract and its pure function.

```typescript
/**
 * @fileoverview Logic for the pubmed_fetch_contents MCP tool.
 * Handles EFetch queries for specific PMIDs and formats the results.
 * This tool can fetch various details from PubMed including abstracts, full XML,
 * MEDLINE text, and citation data.
 * @module src/mcp-server/tools/pubmedFetchContents/logic
 */

import { z } from "zod";
import { getNcbiService } from "../../../services/NCBI/core/ncbiService.js";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  ParsedArticle,
  XmlMedlineCitation,
  XmlPubmedArticleSet,
} from "../../../types-global/pubmedXml.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import {
  ensureArray,
  extractAbstractText,
  extractArticleDates,
  extractAuthors,
  extractDoi,
  extractGrants,
  extractJournalInfo,
  extractKeywords,
  extractMeshTerms,
  extractPmid,
  extractPublicationTypes,
  getText,
} from "../../../services/NCBI/parsing/index.js";

export const PubMedFetchContentsInputSchema = z
  .object({
    pmids: z
      .array(z.string().regex(/^\d+$/))
      .max(200, "Max 200 PMIDs per call if not using history.")
      .optional()
      .describe(
        "An array of PubMed Unique Identifiers (PMIDs) for which to fetch content. Use this OR queryKey/webEnv.",
      ),
    queryKey: z
      .string()
      .optional()
      .describe(
        "Query key from ESearch history server. If used, webEnv must also be provided. Use this OR pmids.",
      ),
    webEnv: z
      .string()
      .optional()
      .describe(
        "Web environment from ESearch history server. If used, queryKey must also be provided. Use this OR pmids.",
      ),
    retstart: z
      .number()
      .int()
      .min(0)
      .optional()
      .describe(
        "Sequential index of the first record to retrieve (0-based). Used with queryKey/webEnv.",
      ),
    retmax: z
      .number()
      .int()
      .min(1)
      .optional()
      .describe(
        "Maximum number of records to retrieve. Used with queryKey/webEnv.",
      ),
    detailLevel: z
      .enum(["abstract_plus", "full_xml", "medline_text", "citation_data"])
      .optional()
      .default("abstract_plus")
      .describe(
        "Specifies the level of detail for the fetched content. Options: 'abstract_plus' (parsed details including abstract, authors, journal, DOI, etc.), 'full_xml' (raw PubMedArticle XML), 'medline_text' (MEDLINE format), 'citation_data' (minimal parsed data for citations). Defaults to 'abstract_plus'.",
      ),
    includeMeshTerms: z
      .boolean()
      .optional()
      .default(true)
      .describe(
        "Applies to 'abstract_plus' and 'citation_data' if parsed from XML.",
      ),
    includeGrantInfo: z
      .boolean()
      .optional()
      .default(false)
      .describe("Applies to 'abstract_plus' if parsed from XML."),
    outputFormat: z
      .enum(["json", "raw_text"])
      .optional()
      .default("json")
      .describe(
        "Specifies the final output format of the tool. \n- 'json' (default): Wraps the data in a standard JSON object. \n- 'raw_text': Returns raw text for 'medline_text' or 'full_xml' detailLevels. For other detailLevels, 'outputFormat' defaults to 'json'.",
      ),
  })
  .superRefine((data, ctx) => {
    if (data.queryKey && !data.webEnv) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "webEnv is required if queryKey is provided.",
        path: ["webEnv"],
      });
    }
    if (!data.queryKey && data.webEnv) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "queryKey is required if webEnv is provided.",
        path: ["queryKey"],
      });
    }
    if (
      (!data.pmids || data.pmids.length === 0) &&
      !(data.queryKey && data.webEnv)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          "Either pmids (non-empty array) or both queryKey and webEnv must be provided.",
        path: ["pmids"],
      });
    }
    if (data.pmids && data.pmids.length > 0 && (data.queryKey || data.webEnv)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          "Cannot use pmids and queryKey/webEnv simultaneously. Please choose one method.",
        path: ["pmids"],
      });
    }
    if (
      (data.retstart !== undefined || data.retmax !== undefined) &&
      !(data.queryKey && data.webEnv)
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "retstart/retmax can only be used with queryKey and webEnv.",
        path: ["retstart"],
      });
    }
  });

export type PubMedFetchContentsInput = z.infer<
  typeof PubMedFetchContentsInputSchema
>;

export type PubMedFetchContentsOutput = {
  content: string;
  articlesReturned: number;
  eFetchUrl: string;
};

interface EFetchServiceParams {
  db: string;
  id?: string;
  query_key?: string;
  WebEnv?: string;
  retmode?: "xml" | "text";
  rettype?: string;
  retstart?: string;
  retmax?: string;
  [key: string]: string | undefined;
}

function parsePubMedArticleSet(
  xmlData: unknown,
  input: PubMedFetchContentsInput,
  parentContext: RequestContext,
): ParsedArticle[] {
  const articles: ParsedArticle[] = [];
  const operationContext = requestContextService.createRequestContext({
    parentRequestId: parentContext.requestId,
    operation: "parsePubMedArticleSet",
  });

  if (
    !xmlData ||
    typeof xmlData !== "object" ||
    !("PubmedArticleSet" in xmlData)
  ) {
    throw new McpError(
      BaseErrorCode.PARSING_ERROR,
      "Invalid or unexpected structure for xmlData in parsePubMedArticleSet.",
      {
        ...operationContext,
        xmlDataType: typeof xmlData,
        xmlDataPreview: sanitizeInputForLogging(
          JSON.stringify(xmlData).substring(0, 200),
        ),
      },
    );
  }

  const typedXmlData = xmlData as { PubmedArticleSet?: XmlPubmedArticleSet };
  const articleSet = typedXmlData.PubmedArticleSet;

  if (!articleSet || !articleSet.PubmedArticle) {
    logger.warning(
      "PubmedArticleSet or PubmedArticle array not found in EFetch XML response.",
      operationContext,
    );
    return articles;
  }

  const pubmedArticlesXml = ensureArray(articleSet.PubmedArticle);

  for (const articleXml of pubmedArticlesXml) {
    if (!articleXml || typeof articleXml !== "object") continue;

    const medlineCitation: XmlMedlineCitation | undefined =
      articleXml.MedlineCitation;
    if (!medlineCitation) continue;

    const pmid = extractPmid(medlineCitation);
    if (!pmid) continue;

    const articleNode = medlineCitation.Article;
    const parsedArticle: ParsedArticle = {
      pmid: pmid,
      title: articleNode?.ArticleTitle
        ? getText(articleNode.ArticleTitle)
        : undefined,
      abstractText: articleNode?.Abstract
        ? extractAbstractText(articleNode.Abstract)
        : undefined,
      authors: articleNode?.AuthorList
        ? extractAuthors(articleNode.AuthorList)
        : undefined,
      journalInfo: articleNode?.Journal
        ? extractJournalInfo(articleNode.Journal, medlineCitation)
        : undefined,
      publicationTypes: articleNode?.PublicationTypeList
        ? extractPublicationTypes(articleNode.PublicationTypeList)
        : undefined,
      keywords: articleNode?.KeywordList
        ? extractKeywords(articleNode.KeywordList)
        : undefined,
      doi: articleNode ? extractDoi(articleNode) : undefined,
      articleDates: articleNode?.ArticleDate
        ? extractArticleDates(articleNode)
        : undefined,
    };

    if (input.includeMeshTerms) {
      parsedArticle.meshTerms = medlineCitation.MeshHeadingList
        ? extractMeshTerms(medlineCitation.MeshHeadingList)
        : undefined;
    }

    if (input.includeGrantInfo) {
      parsedArticle.grantList = articleNode?.GrantList
        ? extractGrants(articleNode.GrantList)
        : undefined;
    }

    articles.push(parsedArticle);
  }
  return articles;
}

export async function pubMedFetchContentsLogic(
  input: PubMedFetchContentsInput,
  parentRequestContext: RequestContext,
): Promise<PubMedFetchContentsOutput> {
  const toolLogicContext = requestContextService.createRequestContext({
    parentRequestId: parentRequestContext.requestId,
    operation: "pubMedFetchContentsLogic",
    input: sanitizeInputForLogging(input),
  });

  const validationResult = PubMedFetchContentsInputSchema.safeParse(input);
  if (!validationResult.success) {
    throw new McpError(
      BaseErrorCode.VALIDATION_ERROR,
      validationResult.error.errors[0]?.message || "Invalid input",
      { ...toolLogicContext, details: validationResult.error.flatten() },
    );
  }

  const ncbiService = getNcbiService();
  logger.info("Executing pubmed_fetch_contents tool", toolLogicContext);

  const eFetchParams: EFetchServiceParams = { db: "pubmed" };

  if (input.queryKey && input.webEnv) {
    eFetchParams.query_key = input.queryKey;
    eFetchParams.WebEnv = input.webEnv;
    if (input.retstart !== undefined)
      eFetchParams.retstart = String(input.retstart);
    if (input.retmax !== undefined) eFetchParams.retmax = String(input.retmax);
  } else if (input.pmids && input.pmids.length > 0) {
    eFetchParams.id = input.pmids.join(",");
  }

  let serviceRetmode: "xml" | "text" = "xml";
  let rettype: string | undefined;

  switch (input.detailLevel) {
    case "full_xml":
      serviceRetmode = "xml";
      break;
    case "medline_text":
      serviceRetmode = "text";
      rettype = "medline";
      break;
    case "abstract_plus":
    case "citation_data":
      serviceRetmode = "xml";
      break;
  }
  eFetchParams.retmode = serviceRetmode;
  if (rettype) eFetchParams.rettype = rettype;

  const eFetchBase =
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi";
  const eFetchQueryString = new URLSearchParams(
    eFetchParams as Record<string, string>,
  ).toString();
  const eFetchUrl = `${eFetchBase}?${eFetchQueryString}`;

  const shouldReturnRawXml =
    input.detailLevel === "full_xml" && input.outputFormat === "raw_text";

  const eFetchResponseData = await ncbiService.eFetch(
    eFetchParams,
    toolLogicContext,
    { retmode: serviceRetmode, rettype, returnRawXml: shouldReturnRawXml },
  );

  let finalOutputText: string;
  let articlesCount = 0;

  if (input.detailLevel === "medline_text") {
    const medlineText = String(eFetchResponseData);
    const foundPmidsInMedline = new Set<string>();
    const pmidRegex = /^PMID- (\d+)/gm;
    let match;
    while ((match = pmidRegex.exec(medlineText)) !== null) {
      if (match[1]) {
        foundPmidsInMedline.add(match[1]);
      }
    }
    articlesCount = foundPmidsInMedline.size;

    if (input.outputFormat === "raw_text") {
      finalOutputText = medlineText;
    } else {
      const notFoundPmids =
        input.pmids?.filter((pmid) => !foundPmidsInMedline.has(pmid)) || [];
      finalOutputText = JSON.stringify({
        requestedPmids: input.pmids || "N/A (history query)",
        articles: [{ medlineText }],
        notFoundPmids,
        eFetchDetails: { urls: [eFetchUrl] },
      });
    }
  } else if (input.detailLevel === "full_xml") {
    const articlesXml = ensureArray(
      (eFetchResponseData as any)?.PubmedArticleSet?.PubmedArticle || [],
    );
    articlesCount = articlesXml.length;
    if (input.outputFormat === "raw_text") {
      // Note: Raw XML output is requested, but we still parse to get an accurate count.
      // This is a trade-off for robustness over performance in this specific case.
      finalOutputText = String(eFetchResponseData);
    } else {
      const foundPmidsInXml = new Set<string>();
      const articlesPayload = articlesXml.map((articleXml) => {
        const pmid = extractPmid(articleXml.MedlineCitation) || "unknown_pmid";
        if (pmid !== "unknown_pmid") foundPmidsInXml.add(pmid);
        return { pmid, fullXmlContent: articleXml };
      });
      const notFoundPmids =
        input.pmids?.filter((pmid) => !foundPmidsInXml.has(pmid)) || [];
      finalOutputText = JSON.stringify({
        requestedPmids: input.pmids || "N/A (history query)",
        articles: articlesPayload,
        notFoundPmids,
        eFetchDetails: { urls: [eFetchUrl] },
      });
    }
  } else {
    const parsedArticles = parsePubMedArticleSet(
      eFetchResponseData as XmlPubmedArticleSet,
      input,
      toolLogicContext,
    );
    articlesCount = parsedArticles.length;
    const foundPmids = new Set(parsedArticles.map((p) => p.pmid));
    const notFoundPmids =
      input.pmids?.filter((pmid) => !foundPmids.has(pmid)) || [];

    let articlesToReturn: any = parsedArticles;
    if (input.detailLevel === "citation_data") {
      articlesToReturn = parsedArticles.map((article) => ({
        pmid: article.pmid,
        title: article.title,
        authors: article.authors?.map((a) => ({
          lastName: a.lastName,
          initials: a.initials,
        })),
        journalInfo: {
          title: article.journalInfo?.title,
          isoAbbreviation: article.journalInfo?.isoAbbreviation,
          volume: article.journalInfo?.volume,
          issue: article.journalInfo?.issue,
          pages: article.journalInfo?.pages,
          year: article.journalInfo?.publicationDate?.year,
        },
        doi: article.doi,
        ...(input.includeMeshTerms && { meshTerms: article.meshTerms }),
      }));
    }
    finalOutputText = JSON.stringify({
      requestedPmids: input.pmids || "N/A (history query)",
      articles: articlesToReturn,
      notFoundPmids,
      eFetchDetails: { urls: [eFetchUrl] },
    });
  }

  logger.notice("Successfully executed pubmed_fetch_contents tool.", {
    ...toolLogicContext,
    articlesReturned: articlesCount,
  });

  return {
    content: finalOutputText,
    articlesReturned: articlesCount,
    eFetchUrl,
  };
}
```

**Step 2: Register the Tool and Handle All Outcomes (`registration.ts`)**
The `registration.ts` file acts as the handler, connecting the logic to the server and ensuring stability.

```typescript
/**
 * @fileoverview Registration for the pubmed_fetch_contents MCP tool.
 * @module src/mcp-server/tools/pubmedFetchContents/registration
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  ErrorHandler,
  logger,
  RequestContext,
  requestContextService,
} from "../../../utils/index.js";
import {
  PubMedFetchContentsInput,
  PubMedFetchContentsInputSchema,
  pubMedFetchContentsLogic,
} from "./logic.js";

/**
 * Registers the pubmed_fetch_contents tool with the MCP server.
 * @param server - The McpServer instance.
 */
export async function registerPubMedFetchContentsTool(
  server: McpServer,
): Promise<void> {
  const operation = "registerPubMedFetchContentsTool";
  const toolName = "pubmed_fetch_contents";
  const toolDescription =
    "Fetches detailed information from PubMed using NCBI EFetch. Can be used with a direct list of PMIDs or with queryKey/webEnv from an ESearch history entry. Supports pagination (retstart, retmax) when using history. Available 'detailLevel' options: 'abstract_plus' (parsed title, abstract, authors, journal, keywords, DOI, optional MeSH/grant info), 'full_xml' (JSON representation of the PubMedArticle XML structure), 'medline_text' (MEDLINE format), or 'citation_data' (minimal data for citations). Returns a JSON object containing results, any PMIDs not found (if applicable), and EFetch details.";

  const context = requestContextService.createRequestContext({ operation });

  await ErrorHandler.tryCatch(
    async () => {
      server.tool(
        toolName,
        toolDescription,
        PubMedFetchContentsInputSchema._def.schema.shape,
        async (
          input: PubMedFetchContentsInput,
          toolContext: any,
        ): Promise<CallToolResult> => {
          const richContext: RequestContext =
            requestContextService.createRequestContext({
              parentRequestId: context.requestId,
              operation: "pubMedFetchContentsToolHandler",
              mcpToolContext: toolContext,
              input,
            });

          try {
            const result = await pubMedFetchContentsLogic(input, richContext);
            return {
              content: [{ type: "text", text: result.content }],
              isError: false,
            };
          } catch (error) {
            const handledError = ErrorHandler.handleError(error, {
              operation: "pubMedFetchContentsToolHandler",
              context: richContext,
              input,
              rethrow: false,
            });

            const mcpError =
              handledError instanceof McpError
                ? handledError
                : new McpError(
                    BaseErrorCode.INTERNAL_ERROR,
                    "An unexpected error occurred while fetching PubMed content.",
                    {
                      originalErrorName: handledError.name,
                      originalErrorMessage: handledError.message,
                    },
                  );

            return {
              content: [
                {
                  type: "text",
                  text: JSON.stringify({
                    error: {
                      code: mcpError.code,
                      message: mcpError.message,
                      details: mcpError.details,
                    },
                  }),
                },
              ],
              isError: true,
            };
          }
        },
      );

      logger.notice(`Tool '${toolName}' registered.`, context);
    },
    {
      operation,
      context,
      errorCode: BaseErrorCode.INITIALIZATION_FAILED,
      critical: true,
    },
  );
}
```

## III. Resource Development Workflow

The workflow for creating Resources mirrors that of Tools, with a focus on data retrieval. Structure is identical but located under `src/mcp-server/resources/`. Registration shall use `server.resource()` and the handler must return an object conforming to the `{ contents: [{ uri, blob, mimeType }] }` structure.

## IV. External Service Integration

Interaction with any external service (e.g., NCBI APIs) shall be encapsulated within a singleton provider class in the `src/services/` directory. The singleton instance shall be imported directly into the `logic.ts` file where it is required. This applies to the `ncbiRequestQueueManager` and any other external clients.

## V. Code Quality and Documentation Mandates

- **JSDoc**: Every file shall begin with a `@fileoverview` and `@module` block. All exported functions, types, and classes shall have complete JSDoc comments.
- **LLM-Facing Descriptions**: The tool's `title`, `description`, and all parameter descriptions defined in Zod schemas (`.describe()`) are transmitted directly to the LLM. They must be written with the LLM as the primary audience—descriptive, concise, and explicit about requirements and constraints.
- **Clarity Over Brevity**: Write self-documenting code with meaningful variable and function names.
- **Immutability**: Prefer functional approaches and immutable data structures to prevent side effects.
- **Formatting**: All code must be formatted using Prettier (`npm run format`) prior to being committed.

## VI. Security Mandates

- **Input Sanitization**: All input from any external source must be treated as untrusted and validated with Zod. Use `sanitization` utilities where appropriate.
- **Secrets Management**: All secrets (API keys, auth keys) **must** be loaded exclusively from environment variables via the `config` module. Never hardcode secrets.
- **Authentication & Authorization**: The server's authentication mode is configured via environment variables. Tools requiring specific permissions shall be protected by checking scopes within the tool handler.
- **Rate Limiting**: Respect the rate limits of external services like NCBI. Use the centralized `rateLimiter` and `ncbiRequestQueueManager`.

## VII. Testing Mandates

A `tests/` directory should mirror the `src/` directory structure. All tests shall be written using Vitest, following an **integration-testing-first principle**.

- **Principle**: Tests shall prioritize validating the complete flow from input to output, including real dependencies, over mocked unit testing. Heavy mocking is explicitly discouraged.
- **Methodology**:
  - **Real Dependencies**: Use actual service instances and data flows. For uncontrollable external services, use test doubles that simulate realistic behavior.
  - **Error Flow Testing**: Test actual error conditions by triggering real failure states, not by mocking errors.
  - **Protocol Compliance**: All MCP transport tests must validate actual MCP protocol compliance.
- **Controlled Mocking**: When mocking is necessary, it must be surgical, justified, and documented. Mock only truly external, uncontrollable dependencies.
- **Test Organization**:
  - `tests/mcp-server/tools/toolName/integration.test.ts`
  - `tests/mcp-server/tools/toolName/logic.test.ts`
- **Running Tests**:
  - `npm test`: Run all tests.
  - `npm test:watch`: Run tests in watch mode.
  - `npm test:coverage`: Run tests and generate a coverage report.

This guide is the single source of truth for development standards. All code reviews will be conducted against these principles.
