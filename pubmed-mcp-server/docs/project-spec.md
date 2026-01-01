---

## MCP Server for PubMed Exploration: Project Specification

**Version:** 1.0.0 (Aligned with `pubmed-mcp-server` v1.0.0)
**MCP Specification Compliance:** 2025-03-26

**1. Project Vision & Goal**

To create an MCP server, "pubmed-mcp-server," that acts as an intelligent and robust gateway for Large Language Models (LLMs) and other applications to programmatically search, retrieve, and process information from the PubMed database via NCBI E-utilities. This server will abstract the complexities of E-utilities, enforce NCBI best practices, provide structured data and actions, and offer enhanced functionalities beyond raw E-utility calls. It leverages the `mcp-ts-template` foundation for core MCP functionalities and utilities.

**2. Core MCP Server Configuration**

-   **Server Name:** `pubmed-mcp-server` (as defined in `package.json` and `src/config/index.ts`)
-   **Version:** `1.0.0` (initial, from `package.json`)
-   **Transport:**
    -   Primarily designed for **HTTP transport** (`MCP_TRANSPORT_TYPE=http`) using Streamable HTTP Server-Sent Events (SSE) for communication, running an Express server. This is recommended for remote access and robust session management.
    -   Supports **stdio transport** (`MCP_TRANSPORT_TYPE=stdio`) for local or embedded use cases.
    -   Configuration via environment variables:
        -   `MCP_TRANSPORT_TYPE`: `"http"` or `"stdio"`.
        -   `MCP_HTTP_PORT`, `MCP_HTTP_HOST`: For HTTP transport.
        -   `MCP_ALLOWED_ORIGINS`: For HTTP CORS configuration.
-   **Authentication & Authorization (HTTP Transport):**
    -   **JWT Authentication:** Mandatory for HTTP transport, configured via `MCP_AUTH_SECRET_KEY`. Implemented in `src/mcp-server/transports/authentication/authMiddleware.ts`.
    -   **Origin Validation:** `originCheckMiddleware` using `MCP_ALLOWED_ORIGINS`.
-   **NCBI E-utilities Configuration (via Environment Variables):**
    -   `NCBI_API_KEY`: **Essential.** The server's primary NCBI API Key for higher rate limits.
    -   `NCBI_TOOL_IDENTIFIER`: Tool name sent to NCBI (e.g., "pubmed-mcp-server/1.0.0"). Defaults to `pubmed-mcp-server/<version>`.
    -   `NCBI_ADMIN_EMAIL`: Administrator's email for NCBI contact.
    -   `NCBI_REQUEST_DELAY_MS`: Milliseconds to wait between NCBI requests (e.g., 100 for API key, ensuring <10 requests/sec).
    -   `NCBI_MAX_RETRIES`: Max retries for failed NCBI requests.
    -   The server automatically includes `api_key`, `tool`, and `email` parameters in all E-utility requests, managed by `ncbiService.ts`.
-   **Logging:**
    -   Configured via `MCP_LOG_LEVEL` and `LOGS_DIR`.
    -   Uses the structured logger from `src/utils/internal/logger.ts`, compliant with MCP spec.
-   **SDK Usage:**
    -   Tools and resources are defined using the high-level SDK abstractions:
        -   `server.tool(name, description, zodSchemaShape, handler)`
        -   `server.resource(regName, template, metadata, handler)`
    -   This ensures type safety, automatic schema generation, and simplified protocol adherence.

**2.1. Adherence to NCBI Guidelines**
This server is designed to strictly adhere to NCBI E-utility usage policies, including:
-   Mandatory use of a registered API Key (`NCBI_API_KEY`).
-   Transmission of `tool` (`NCBI_TOOL_IDENTIFIER`) and `email` (`NCBI_ADMIN_EMAIL`) parameters with every request.
-   Respecting request rate limits (not exceeding 10 requests per second with an API key, or 3 per second without). This is managed by the internal `ncbiService.ts` through request queuing and delays.
-   The server does not facilitate bulk downloading or redistribution of PubMed data in a manner that would violate NCBI policies. Users of the MCP server are also expected to comply with NCBI's terms of service.

**3. MCP Tools**

Tools encapsulate E-utility calls, adding value through processing, structuring, and providing LLM-friendly inputs/outputs. Handlers will utilize `RequestContext` for correlation and `ErrorHandler.tryCatch` for robust error management. All interactions with NCBI E-utilities are managed by the `ncbiService.ts`.

**3.1. Tool: `searchPubMedArticles`**

-   **Description:** Searches PubMed for articles matching a query term. Returns PMIDs, metadata, and optional brief summaries using ESummary v2.0.
-   **Underlying E-utilities:** `ESearch` (primary, with `usehistory=y` if summaries are fetched), `ESummary` (optional, `version="2.0"`).
-   **Registration:** `src/mcp-server/tools/searchPubMedArticles/registration.ts`
-   **Logic:** `src/mcp-server/tools/searchPubMedArticles/logic.ts`
-   **Input Parameters (Zod Schema Shape - to be used with `server.tool`):**
    ```typescript
    // Shape for Zod schema, e.g., in searchPubMedArticlesLogic.ts
    // import { z } from 'zod';
    // export const SearchPubMedArticlesInputSchema = z.object({
    {
      queryTerm: z.string().min(3, "Query term must be at least 3 characters"),
      maxResults: z.number().int().positive().optional().default(20).max(1000, "Max results per query. ESearch's retmax is used."),
      sortBy: z.enum([ // Directly supported ESearch sort options for PubMed
        "relevance",      // Default, "Best Match"
        "pub_date",       // Publication Date
        "author",         // First Author
        "journal_name"    // Journal Name
      ]).optional().default("relevance").describe("Note: Other sorting (e.g., last_author, title) may require client-side implementation or be future server enhancements."),
      dateRange: z.object({
        minDate: z.string().regex(/^\d{4}(\/\d{2}(\/\d{2})?)?$/, "YYYY, YYYY/MM, or YYYY/MM/DD").optional(),
        maxDate: z.string().regex(/^\d{4}(\/\d{2}(\/\d{2})?)?$/, "YYYY, YYYY/MM, or YYYY/MM/DD").optional(),
        dateType: z.enum(["pdat", "mdat", "edat"]).optional().default("pdat") // pdat: Publication Date, mdat: Modification Date, edat: Entrez Date
      }).optional().describe("Defines a date range for the search."),
      filterByPublicationTypes: z.array(z.string()).optional().describe("e.g., ['Review', 'Clinical Trial']. Server maps to Entrez query syntax (e.g., \"Review\"[Publication Type])."),
      fetchBriefSummaries: z.number().int().min(0).max(100).optional().default(0).describe("Number of top PMIDs for ESummary v2.0. 0 to disable. Max 100 for this tool.")
    }
    // });
    ```
-   **Handler Logic (Conceptual - implemented in `logic.ts`):**
    1.  Utilize `requestContext` for logging and error tracking.
    2.  Construct `ESearch` `term` parameter by combining `queryTerm`, `dateRange` (using `mindate`, `maxdate`, `datetype`), and `filterByPublicationTypes` (e.g., `queryTerm AND "Review"[Publication Type]`). Apply input sanitization (`src/utils/security/sanitization.ts`) to `queryTerm`.
    3.  Call `ncbiService.ts` to execute `ESearch`. If `fetchBriefSummaries > 0`, `usehistory=y` will be set for `ESearch`. Parameters will include `db=pubmed`, `term`, `retmax=maxResults`, `sort=sortBy`.
    4.  Parse `ESearch` response (PMIDs, `WebEnv`, `QueryKey`, total count).
    5.  If `fetchBriefSummaries > 0` and PMIDs are found, call `ncbiService.ts` for `ESummary` using the `WebEnv`, `QueryKey`, and the first `fetchBriefSummaries` PMIDs (or all if fewer than requested). `ESummary` will use `version="2.0"`.
    6.  Parse `ESummary` response (DocSums).
    7.  Format output as `CallToolResult`. Errors are thrown as `McpError`.
-   **Output Content (MCP `content` array - example):**
    ```json
    [{
      "type": "application/json",
      "data": {
        "searchParameters": {
          "queryTerm": "original queryTerm input",
          "maxResults": 20,
          "sortBy": "relevance",
          "fetchBriefSummaries": 5 // example
        },
        "effectiveESearchTerm": "precision oncology AND (2023[pdat]) AND (\"Review\"[Publication Type])",
        "totalFound": 12345,
        "retrievedPmidCount": 20, // from ESearch
        "pmids": ["35394430", "35358407", "..."], // up to maxResults
        "briefSummaries": [ // up to fetchBriefSummaries
          {
            "pmid": "35394430",
            "title": "Example Title 1",
            "authors": "Doe J, Smith A.", // Simplified author string from ESummary
            "source": "J Example Sci. 2023 Mar",
            "pubDate": "2023-03-15", // Standardized
            "epubDate": "2023-02-01"
          }
        ],
        "eSearchUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=...",
        "eSummaryUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&version=2.0&id=..." // if called
      }
    }]
    ```

**3.2. Tool: `fetchArticleDetails`**

-   **Description:** Retrieves detailed information for a list of PMIDs with flexible content control using EFetch.
-   **Underlying E-utility:** `EFetch`.
-   **Registration:** `src/mcp-server/tools/fetchArticleDetails/registration.ts`
-   **Logic:** `src/mcp-server/tools/fetchArticleDetails/logic.ts`
-   **Input Parameters (Zod Schema Shape):**
    ```typescript
    // import { z } from 'zod';
    // export const FetchArticleDetailsInputSchema = z.object({
    {
      pmids: z.array(z.string().regex(/^\d+$/)).min(1, "At least one PMID is required").max(200, "Max 200 PMIDs per call. Server uses HTTP POST for larger lists if necessary."),
      detailLevel: z.enum([
        "abstract_plus", // Server-parsed: Title, abstract, authors, journal, pub_date, keywords, DOI from EFetch XML.
        "full_xml",      // Raw PubMedArticle XML from EFetch (retmode=xml).
        "medline_text",  // MEDLINE formatted text from EFetch (retmode=text, rettype=medline).
        "citation_data"  // Server-parsed minimal data for citation from EFetch XML.
      ]).optional().default("abstract_plus"),
      includeMeshTerms: z.boolean().optional().default(true).describe("Applies to 'abstract_plus' and 'citation_data' if parsed from XML."),
      includeGrantInfo: z.boolean().optional().default(false).describe("Applies to 'abstract_plus' if parsed from XML.")
    }
    // });
    ```
-   **Handler Logic (Conceptual):**
    1.  Determine `EFetch` `rettype` and `retmode` based on `detailLevel`:
        *   `abstract_plus`, `full_xml`, `citation_data`: `db=pubmed`, `retmode=xml`. (Default `rettype` for PubMed XML is suitable).
        *   `medline_text`: `db=pubmed`, `retmode=text`, `rettype=medline`.
    2.  `ncbiService.ts` handles sending PMIDs. For > ~200 PMIDs, it should use HTTP POST with `EFetch`.
    3.  Call `ncbiService.ts` for `EFetch`.
    4.  If `detailLevel` is `abstract_plus` or `citation_data`, robustly parse the XML response. This includes standardizing author lists, publication dates, and extracting MeSH/Grant info if requested. This is a core value-add of the tool.
    5.  Format output as `CallToolResult`.
-   **Output Content (MCP `content` array - example for `abstract_plus`):**
    ```json
    [{
      "type": "application/json", // or "application/xml" for full_xml, "text/plain" for medline_text
      "data": { // For abstract_plus
        "requestedPmids": ["35394430"],
        "articles": [
          {
            "pmid": "35394430",
            "title": "Example Title 1",
            "abstractText": "This is the abstract...",
            "authors": [
              { "lastName": "Doe", "firstName": "John", "initials": "J", "affiliation": "University of Science" }
            ],
            "journalInfo": {
              "title": "Journal of Example Science", "isoAbbreviation": "J Ex Sci", "volume": "10", "issue": "2", "pages": "100-110",
              "publicationDate": { "year": 2023, "month": "Mar", "day": 15, "medlineDate": "2023 Mar" } // Standardized
            },
            "publicationTypes": ["Journal Article", "Review"],
            "keywords": ["keyword1", "keyword2"], // From KeywordList or MeSH
            "meshTerms": [ // if includeMeshTerms is true
              { "descriptorName": "Neoplasms", "qualifierName": "therapy", "isMajorTopic": true, "ui": "D009369" }
            ],
            "grantList": [ // if includeGrantInfo is true
              { "grantId": "R01 CA123456", "agency": "NCI NIH HHS", "country": "United States" }
            ],
            "doi": "10.xxxx/xxxxxx"
          }
        ],
        "notFoundPmids": [],
        "eFetchDetails": {
          "urls": ["https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=..."],
          "requestMethod": "GET" // or POST
        }
      }
    }]
    ```

**3.3. Tool: `getArticleRelationships`**

-   **Description:** Finds articles related to a source PMID (e.g., similar articles in PubMed, articles citing it, or articles it references) or retrieves citation formats.
-   **Underlying E-utilities:** `ELink` (primary), `EFetch` (for citation formats).
-   **Registration:** `src/mcp-server/tools/getArticleRelationships/registration.ts`
-   **Logic:** `src/mcp-server/tools/getArticleRelationships/logic.ts`
-   **Input Parameters (Zod Schema Shape):**
    ```typescript
    // import { z } from 'zod';
    // export const GetArticleRelationshipsInputSchema = z.object({
    {
      sourcePmid: z.string().regex(/^\d+$/).describe("Primary PMID for relationship lookup."),
      relationshipType: z.enum([
        "pubmed_similar_articles",  // Uses ELink cmd=neighbor, dbfrom=pubmed, db=pubmed
        "pubmed_citedin",           // Articles in PubMed that cite this PMID (ELink cmd=neighbor, linkname=pubmed_pubmed_citedin)
        "pubmed_references",        // Articles in PubMed referenced by this PMID (ELink cmd=neighbor, linkname=pubmed_pubmed_refs)
        "citation_formats"          // Fetch citation data for server-side formatting
      ]).default("pubmed_similar_articles"),
      maxRelatedResults: z.number().int().positive().optional().default(5).max(50).describe("Applies to relationship types returning multiple PMIDs. Server truncates ELink results if necessary."),
      citationStyles: z.array(z.enum(["ris", "bibtex", "apa_string", "mla_string"])).optional().default(["ris"]).describe("For 'citation_formats' type. Formatting is server-side.")
    }
    // });
    ```
-   **Handler Logic (Conceptual):**
    1.  Based on `relationshipType`:
        *   `pubmed_similar_articles`: Call `ncbiService.ts` for `ELink` with `dbfrom=pubmed`, `db=pubmed`, `cmd=neighbor`, `id=sourcePmid`.
        *   `pubmed_citedin`: Call `ncbiService.ts` for `ELink` with `dbfrom=pubmed`, `db=pubmed`, `cmd=neighbor`, `id=sourcePmid`, `linkname=pubmed_pubmed_citedin`.
        *   `pubmed_references`: Call `ncbiService.ts` for `ELink` with `dbfrom=pubmed`, `db=pubmed`, `cmd=neighbor`, `id=sourcePmid`, `linkname=pubmed_pubmed_refs`.
        *   `citation_formats`: Call `ncbiService.ts` for `EFetch` (`db=pubmed`, `id=sourcePmid`, `retmode=xml`). The server then parses this XML and generates the requested citation strings.
    2.  Parse `ELink` XML response for linked PMIDs and scores (if available).
    3.  If PMIDs are returned from `ELink`, the server may optionally enrich the top `maxRelatedResults` with brief details by making an internal call to a simplified version of `fetchArticleDetails` logic (e.g., fetching only title and authors).
    4.  Format output as `CallToolResult`.
-   **Output Content (MCP `content` array - example for `pubmed_similar_articles`):**
    ```json
    [{
      "type": "application/json",
      "data": {
        "sourcePmid": "35394430",
        "relationshipType": "pubmed_similar_articles",
        "relatedArticles": [ // Max 'maxRelatedResults'
          { "pmid": "9876543", "title": "Related Article Title", "authors": "Smith J, et al.", "score": 0.85, "linkUrl": "https://pubmed.ncbi.nlm.nih.gov/9876543/" }
        ],
        "citations": {}, // Populated if relationshipType is 'citation_formats'
        "retrievedCount": 1, // Number of related articles returned
        "eLinkUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?..." // Example ELink URL
      }
    }]
    ```

**4. MCP Resources**

Resources provide descriptive data about the server or PubMed. Handlers will use `RequestContext` and `ErrorHandler`.

**4.1. Resource: `serverInfo`**

-   **Description:** Provides comprehensive information about the `pubmed-mcp-server`, configuration, NCBI compliance, and status.
-   **URI:** `pubmed-connect://info` (Example URI, can be adjusted)
-   **Registration:** `src/mcp-server/resources/serverInfo/registration.ts`
-   **Logic:** `src/mcp-server/resources/serverInfo/logic.ts`
-   **Handler Logic (Conceptual):**
    1.  Assemble data from `src/config/index.ts` (server version, admin email, tool ID).
    2.  Include dynamic status (e.g., last NCBI connectivity check via `ncbiService.ts`).
    3.  Return data structured as JSON, Base64 encoded in the `blob` field of `ResourceContent`.
-   **Output Content (MCP `contents` array, `blob` is Base64 of JSON below):**
    ```json
    {
      "serverName": "pubmed-mcp-server",
      "serverVersion": "1.0.0",
      "description": "MCP Server for intelligent PubMed access via NCBI E-utilities.",
      "contactEmail": "configured_admin@example.com",
      "mcpSpecVersion": "2025-03-26",
      "ncbiCompliance": {
        "apiUsageStatus": "NCBI API Key in use",
        "toolIdentifier": "pubmed-mcp-server/1.0.0",
        "ncbiUsagePolicyUrl": "https://www.ncbi.nlm.nih.gov/books/NBK25497/", // E-utilities Help
        "currentRateLimitAdherence": "Targeting <10 requests/sec (with API key) via request queuing."
      },
      "supportedEutilities": ["ESearch", "EFetch", "ESummary", "ELink", "EInfo"],
      "operationalStatus": {
        "lastNcbiConnectivityCheck": "2025-05-24T01:00:00.000Z",
        "ncbiStatus": "Nominal", // Based on last successful NCBI interaction
        "internalQueueLength": 0 // Current length of the NCBI request queue
      },
      "documentationUrl": "./docs/project-spec.md"
    }
    ```

**4.2. Resource: `getPubMedStats`**

-   **Description:** Retrieves general statistics about the PubMed database using `EInfo`.
-   **URI:** `pubmed-connect://stats/pubmed` (Example URI)
-   **Underlying E-utility:** `EInfo`.
-   **Registration:** `src/mcp-server/resources/getPubMedStats/registration.ts`
-   **Logic:** `src/mcp-server/resources/getPubMedStats/logic.ts`
-   **Handler Logic (Conceptual):**
    1.  Call `ncbiService.ts` for `EInfo` (`db=pubmed`).
    2.  Parse XML response for key statistics (record count, last update, field list).
    3.  Return data structured as JSON, Base64 encoded in `blob`.
-   **Output Content (MCP `contents` array, `blob` is Base64 of JSON below):**
    ```json
    {
      "databaseName": "PubMed",
      "menuName": "PubMed", // From EInfo
      "description": "PubMed comprises more than XX million citations...", // From EInfo
      "totalRecordCount": 36000000, // From EInfo <Count>
      "lastUpdate": "2025-05-23T10:00:00Z", // From EInfo <LastUpdate>
      "availableSearchFields": [ // Parsed from EInfo <FieldList>
        { "name": "ALL", "fullName": "All Fields", "description": "All terms from all searchable fields", "isDate": false, "isNumerical": false, "termCount": "123456789" },
        { "name": "UID", "fullName": "UID", "description": "Unique identifier", "isDate": false, "isNumerical": true, "termCount": "36000000" }
        // ... other relevant fields
      ],
      "availableLinkNames": [ // Parsed from EInfo <LinkList>
        { "name": "pubmed_pubmed_citedin", "description": "Cited In", "dbTo": "pubmed" }
        // ... other relevant links
      ],
      "eInfoUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed"
    }
    ```

**5. Key Implementation Considerations**

-   **NCBI Interaction Service (`src/services/ncbiService.ts` - to be created):**
    -   Centralize all E-utility calls.
    -   Manage API key, tool, email parameters.
    -   Implement robust **rate limiting via a request queue** based on `NCBI_REQUEST_DELAY_MS` to ensure compliance across all concurrent MCP requests.
    -   Handle retries (`NCBI_MAX_RETRIES`) with appropriate backoff.
    -   Intelligently use HTTP GET or POST based on payload size (e.g., number of PMIDs for `EFetch`).
    -   Parse NCBI XML/JSON responses, including NCBI error structures (e.g., `<ERROR>` tags in XML), translating them to structured data or specific `McpError` instances.
    -   Manage `usehistory=y`, `WebEnv`, and `query_key` for multi-step E-utility operations.
-   **XML Parsing:** Use a reliable library (e.g., `fast-xml-parser`) wrapped in utility functions within `src/utils/parsing/` or the `ncbiService` for different E-utility response structures (ESearch, ESummary v2.0, EFetch PubMedArticleSet, ELink, EInfo).
-   **Error Handling:**
    -   Utilize `ErrorHandler.tryCatch` from `src/utils/internal/errorHandler.ts`.
    -   Define specific `McpError` codes in `src/types-global/errors.ts` for NCBI-related issues (e.g., `NCBI_API_ERROR`, `NCBI_PARSING_ERROR`, `NCBI_RATE_LIMIT_WARNING`, `NCBI_QUERY_ERROR`).
-   **Logging:** Leverage `logger` from `src/utils/internal/logger.ts` with `RequestContext` for detailed and correlated logging of operations, NCBI requests (including constructed URLs and parameters), responses, and errors.
-   **Input Sanitization:** Use `sanitization` utilities from `src/utils/security/sanitization.ts` for all user/client-provided inputs, especially query terms, to prevent injection or malformed Entrez queries.
-   **Asynchronous Operations:** All handlers involving NCBI calls must be `async` and manage promises correctly.
-   **Configuration Management:** Centralized in `src/config/index.ts`, loading from environment variables with clear validation.
-   **Caching (Future Consideration - v1.1+):** Implement caching for frequently requested, non-volatile E-utility responses (e.g., `EFetch` for specific PMIDs, `EInfo`) to improve performance and reduce NCBI load, with appropriate Time-To-Live (TTL) strategies.
-   **Testing:**
    -   Unit tests for individual logic functions, parsers, and utility components.
    -   Integration tests mocking `ncbiService.ts` calls to verify tool/resource handlers.
    -   Consider contract testing for the `ncbiService.ts` against known NCBI E-utility response schemas.
-   **Documentation:**
    -   JSDoc for all functions, classes, and types.
    -   This `project-spec.md` serves as the primary functional specification.
    -   `README.md` for setup, environment variable configuration, and usage examples.

**6. File Structure (Key Locations)**

-   **Main Entry:** `src/index.ts`
-   **Server Setup:** `src/mcp-server/server.ts` (creates McpServer instance, registers tools/resources)
-   **Configuration:** `src/config/index.ts`
-   **Core Utilities:** `src/utils/` (logging, error handling, parsing, security)
-   **Global Types:** `src/types-global/` (especially `errors.ts`)
-   **NCBI Service:** `src/services/ncbiService.ts` (to be created)
-   **Tools Implementation:** `src/mcp-server/tools/<toolName>/`
    -   `logic.ts` (handler function, Zod schema definition)
    -   `registration.ts` (calls `server.tool()`)
    -   `index.ts` (exports registration)
-   **Resources Implementation:** `src/mcp-server/resources/<resourceName>/`
    -   `logic.ts` (handler function)
    -   `registration.ts` (calls `server.resource()`)
    -   `index.ts` (exports registration)

---
