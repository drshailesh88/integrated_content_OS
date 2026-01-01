/**
 * @fileoverview Helper functions for parsing detailed PubMed Article XML structures,
 * typically from EFetch results.
 * @module src/services/NCBI/parsing/pubmedArticleStructureParser
 */
import { XmlArticle, XmlAuthorList, XmlGrantList, XmlJournal, XmlKeywordList, XmlMedlineCitation, XmlMeshHeadingList, XmlPublicationTypeList, ParsedArticleAuthor, ParsedJournalInfo, ParsedMeshTerm, ParsedGrant, ParsedArticleDate } from "../../../types-global/pubmedXml.js";
/**
 * Extracts and formats author information from XML.
 * @param authorListXml - The XML AuthorList element.
 * @returns An array of formatted author objects.
 */
export declare function extractAuthors(authorListXml?: XmlAuthorList): ParsedArticleAuthor[];
/**
 * Extracts and formats journal information from XML.
 * @param journalXml - The XML Journal element from an Article.
 * @param medlineCitationXml - The XML MedlineCitation element (for MedlinePgn).
 * @returns Formatted journal information.
 */
export declare function extractJournalInfo(journalXml?: XmlJournal, medlineCitationXml?: XmlMedlineCitation): ParsedJournalInfo | undefined;
/**
 * Extracts and formats MeSH terms from XML.
 * @param meshHeadingListXml - The XML MeshHeadingList element.
 * @returns An array of formatted MeSH term objects.
 */
export declare function extractMeshTerms(meshHeadingListXml?: XmlMeshHeadingList): ParsedMeshTerm[];
/**
 * Extracts and formats grant information from XML.
 * @param grantListXml - The XML GrantList element.
 * @returns An array of formatted grant objects.
 */
export declare function extractGrants(grantListXml?: XmlGrantList): ParsedGrant[];
/**
 * Extracts DOI from various possible locations in the XML.
 * Prioritizes ELocationID with ValidYN="Y", then any ELocationID, then ArticleIdList.
 * @param articleXml - The XML Article element.
 * @returns The DOI string or undefined.
 */
export declare function extractDoi(articleXml?: XmlArticle): string | undefined;
/**
 * Extracts publication types from XML.
 * @param publicationTypeListXml - The XML PublicationTypeList element.
 * @returns An array of publication type strings.
 */
export declare function extractPublicationTypes(publicationTypeListXml?: XmlPublicationTypeList): string[];
/**
 * Extracts keywords from XML. Handles single or multiple KeywordList elements.
 * @param keywordListsXml - The XML KeywordList element or an array of them.
 * @returns An array of keyword strings.
 */
export declare function extractKeywords(keywordListsXml?: XmlKeywordList[] | XmlKeywordList): string[];
/**
 * Extracts abstract text from XML. Handles structured abstracts by concatenating sections.
 * If AbstractText is an array, joins them. If it's a single object/string, uses it directly.
 * Prefixes with Label if present.
 * @param abstractXml - The XML Abstract element from an Article.
 * @returns The abstract text string, or undefined if not found or empty.
 */
export declare function extractAbstractText(abstractXml?: XmlArticle["Abstract"]): string | undefined;
/**
 * Extracts PMID from MedlineCitation.
 * @param medlineCitationXml - The XML MedlineCitation element.
 * @returns The PMID string or undefined.
 */
export declare function extractPmid(medlineCitationXml?: XmlMedlineCitation): string | undefined;
/**
 * Extracts article dates from XML.
 * @param articleXml - The XML Article element.
 * @returns An array of parsed article dates.
 */
export declare function extractArticleDates(articleXml?: XmlArticle): ParsedArticleDate[];
//# sourceMappingURL=pubmedArticleStructureParser.d.ts.map