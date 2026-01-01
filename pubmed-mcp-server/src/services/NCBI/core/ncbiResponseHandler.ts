/**
 * @fileoverview Handles parsing of NCBI E-utility responses and NCBI-specific error extraction.
 * @module src/services/NCBI/core/ncbiResponseHandler
 */

import { AxiosResponse } from "axios";
import { XMLParser, XMLValidator } from "fast-xml-parser";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";
import { NcbiRequestOptions } from "./ncbiConstants.js";

export class NcbiResponseHandler {
  private xmlParser: XMLParser;

  constructor() {
    this.xmlParser = new XMLParser({
      ignoreAttributes: false,
      attributeNamePrefix: "@_",
      parseTagValue: true, // auto-convert numbers, booleans if possible
      isArray: (_name, jpath) => {
        // Common NCBI list tags - expand as needed
        const arrayTags = [
          "IdList.Id",
          "eSearchResult.IdList.Id",
          "PubmedArticleSet.PubmedArticle",
          "PubmedArticleSet.DeleteCitation.PMID",
          "AuthorList.Author",
          "MeshHeadingList.MeshHeading",
          "GrantList.Grant",
          "KeywordList.Keyword",
          "PublicationTypeList.PublicationType",
          "LinkSet.LinkSetDb.Link",
          "Link.Id",
          "DbInfo.FieldList.Field",
          "DbInfo.LinkList.Link",
          "DocSum.Item", // For ESummary v2.0 JSON-like XML
        ];
        return arrayTags.includes(jpath);
      },
    });
  }

  private extractNcbiErrorMessages(
    parsedXml: Record<string, unknown>,
  ): string[] {
    const messages: string[] = [];
    // Order matters for specificity if multiple error types could exist
    const errorPaths = [
      "eLinkResult.ERROR",
      "eSummaryResult.ERROR",
      "eSearchResult.ErrorList.PhraseNotFound",
      "eSearchResult.ErrorList.FieldNotFound",
      "PubmedArticleSet.ErrorList.CannotRetrievePMID", // More specific error
      "ERROR", // Generic top-level error
    ];

    for (const path of errorPaths) {
      let errorSource: unknown = parsedXml;
      const parts = path.split(".");
      for (const part of parts) {
        if (
          errorSource &&
          typeof errorSource === "object" &&
          part in errorSource
        ) {
          errorSource = (errorSource as Record<string, unknown>)[part];
        } else {
          errorSource = undefined;
          break;
        }
      }

      if (errorSource) {
        const items = Array.isArray(errorSource) ? errorSource : [errorSource];
        for (const item of items) {
          if (typeof item === "string") {
            messages.push(item);
          } else if (item && typeof item["#text"] === "string") {
            messages.push(item["#text"]);
          }
        }
      }
    }

    // Handle warnings if no primary errors found
    if (messages.length === 0) {
      const warningPaths = [
        "eSearchResult.WarningList.QuotedPhraseNotFound",
        "eSearchResult.WarningList.OutputMessage",
      ];
      for (const path of warningPaths) {
        let warningSource: unknown = parsedXml;
        const parts = path.split(".");
        for (const part of parts) {
          if (
            warningSource &&
            typeof warningSource === "object" &&
            part in warningSource
          ) {
            warningSource = (warningSource as Record<string, unknown>)[part];
          } else {
            warningSource = undefined;
            break;
          }
        }
        if (warningSource) {
          const items = Array.isArray(warningSource)
            ? warningSource
            : [warningSource];
          for (const item of items) {
            if (typeof item === "string") {
              messages.push(`Warning: ${item}`);
            } else if (item && typeof item["#text"] === "string") {
              messages.push(`Warning: ${item["#text"]}`);
            }
          }
        }
      }
    }
    return messages.length > 0
      ? messages
      : ["Unknown NCBI API error structure."];
  }

  /**
   * Parses the raw AxiosResponse data based on retmode and checks for NCBI-specific errors.
   * @param response The raw AxiosResponse from an NCBI E-utility call.
   * @param endpoint The E-utility endpoint for context.
   * @param context The request context for logging.
   * @param options The original request options, particularly `retmode`.
   * @returns The parsed data (object for XML/JSON, string for text).
   * @throws {McpError} If parsing fails or NCBI reports an error in the response body.
   */
  public parseAndHandleResponse<T>(
    response: AxiosResponse,
    endpoint: string,
    context: RequestContext,
    options: NcbiRequestOptions,
  ): T {
    const responseData = response.data;
    const operationContext = requestContextService.createRequestContext({
      ...context,
      operation: "NCBI_ParseResponse",
      endpoint,
      retmode: options.retmode,
    });

    if (options.retmode === "text") {
      logger.debug("Received text response from NCBI.", operationContext);
      return responseData as T;
    }

    if (options.retmode === "xml") {
      logger.debug(
        "Attempting to parse XML response from NCBI.",
        operationContext,
      );
      if (
        typeof responseData !== "string" ||
        XMLValidator.validate(responseData) !== true
      ) {
        logger.error(
          "Invalid or non-string XML response from NCBI",
          new Error("Invalid XML structure"),
          {
            ...operationContext,
            responseSnippet: String(responseData).substring(0, 500),
          },
        );
        throw new McpError(
          BaseErrorCode.NCBI_PARSING_ERROR,
          "Received invalid XML from NCBI.",
          { endpoint, responseSnippet: String(responseData).substring(0, 200) },
        );
      }

      // Always parse for error checking, even if returning raw XML
      const parsedXml = this.xmlParser.parse(responseData);

      // Check for error indicators within the parsed XML structure
      if (
        parsedXml.eSearchResult?.ErrorList ||
        parsedXml.eLinkResult?.ERROR ||
        parsedXml.eSummaryResult?.ERROR ||
        parsedXml.PubmedArticleSet?.ErrorList || // Check for ErrorList specifically
        parsedXml.ERROR // Generic top-level error
      ) {
        const errorMessages = this.extractNcbiErrorMessages(parsedXml);
        logger.error(
          "NCBI API returned an error in XML response",
          new Error(errorMessages.join("; ")),
          {
            ...operationContext,
            errors: errorMessages,
            parsedXml: sanitizeInputForLogging(parsedXml), // Log the parsed structure for error diagnosis
          },
        );
        throw new McpError(
          BaseErrorCode.NCBI_API_ERROR,
          `NCBI API Error: ${errorMessages.join("; ")}`,
          { endpoint, ncbiErrors: errorMessages },
        );
      }

      // If raw XML is requested and no errors were found, return the original string
      if (options.returnRawXml) {
        logger.debug(
          "Successfully validated XML response. Returning raw XML string as requested.",
          operationContext,
        );
        return responseData as T; // responseData is the raw XML string
      }

      logger.debug(
        "Successfully parsed XML response. Returning parsed object.",
        operationContext,
      );
      return parsedXml as T; // Return the parsed object by default
    }

    if (options.retmode === "json") {
      logger.debug("Handling JSON response from NCBI.", operationContext);
      // Assuming responseData is already parsed by Axios if Content-Type was application/json
      if (
        typeof responseData === "object" &&
        responseData !== null &&
        responseData.error
      ) {
        const errorMessage = String(responseData.error);
        logger.error(
          "NCBI API returned an error in JSON response",
          new Error(errorMessage),
          {
            ...operationContext,
            error: errorMessage,
            responseData: sanitizeInputForLogging(responseData),
          },
        );
        throw new McpError(
          BaseErrorCode.NCBI_API_ERROR,
          `NCBI API Error: ${errorMessage}`,
          { endpoint, ncbiError: errorMessage },
        );
      }
      logger.debug("Successfully processed JSON response.", operationContext);
      return responseData as T;
    }

    // Fallback for unknown retmode or if retmode is undefined
    logger.warning(
      `Response received with unspecified or unhandled retmode: ${options.retmode}. Returning raw data.`,
      operationContext,
    );
    return responseData as T;
  }
}
