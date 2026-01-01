/**
 * @fileoverview Global TypeScript type definitions for PubMed XML structures.
 * These types are used for parsing data returned by NCBI E-utilities,
 * particularly from EFetch for PubMed articles and ESummary.
 * @module src/types-global/pubmedXml
 */

// Basic type for elements that primarily contain text but might have attributes
export interface XmlTextElement {
  "#text"?: string;
  [key: string]: unknown; // For attributes like _UI, _MajorTopicYN, _EIdType, _ValidYN, _IdType, Label, NlmCategory, _DateType
}

// Specific XML element types based on PubMed DTD (simplified)

export type XmlPMID = XmlTextElement; // e.g., <PMID Version="1">12345</PMID>

export interface XmlArticleDate extends XmlTextElement {
  Year?: XmlTextElement;
  Month?: XmlTextElement;
  Day?: XmlTextElement;
  _DateType?: string;
}

export interface XmlAuthor {
  LastName?: XmlTextElement;
  ForeName?: XmlTextElement;
  Initials?: XmlTextElement;
  AffiliationInfo?: {
    Affiliation?: XmlTextElement;
  }[];
  Identifier?: XmlTextElement[]; // For ORCID etc.
  CollectiveName?: XmlTextElement; // For group authors
}

export interface XmlAuthorList {
  Author?: XmlAuthor[] | XmlAuthor;
  _CompleteYN?: "Y" | "N";
}

export interface XmlPublicationType extends XmlTextElement {
  _UI?: string;
}

export interface XmlPublicationTypeList {
  PublicationType: XmlPublicationType[] | XmlPublicationType;
}

export interface XmlELocationID extends XmlTextElement {
  _EIdType?: string; // "doi", "pii"
  _ValidYN?: "Y" | "N";
}

export interface XmlArticleId extends XmlTextElement {
  _IdType?: string; // "doi", "pubmed", "pmc", "mid", etc.
}

export interface XmlArticleIdList {
  ArticleId: XmlArticleId[] | XmlArticleId;
}

export interface XmlAbstractText extends XmlTextElement {
  Label?: string;
  NlmCategory?: string; // e.g., "BACKGROUND", "METHODS", "RESULTS", "CONCLUSIONS"
}

export interface XmlAbstract {
  AbstractText: XmlAbstractText[] | XmlAbstractText;
  CopyrightInformation?: XmlTextElement;
}

export interface XmlPagination {
  MedlinePgn?: XmlTextElement; // e.g., "10-5" or "e123"
  StartPage?: XmlTextElement;
  EndPage?: XmlTextElement;
}

export interface XmlPubDate {
  Year?: XmlTextElement;
  Month?: XmlTextElement;
  Day?: XmlTextElement;
  MedlineDate?: XmlTextElement; // e.g., "2000 Spring", "1999-2000"
}

export interface XmlJournalIssue {
  Volume?: XmlTextElement;
  Issue?: XmlTextElement;
  PubDate?: XmlPubDate;
  _CitedMedium?: string; // "Internet" or "Print"
}

export interface XmlJournal {
  ISSN?: XmlTextElement & { _IssnType?: string };
  JournalIssue?: XmlJournalIssue;
  Title?: XmlTextElement; // Full Journal Title
  ISOAbbreviation?: XmlTextElement; // Journal Abbreviation
}

export interface XmlArticle {
  Journal?: XmlJournal;
  ArticleTitle?: XmlTextElement | string; // Can be just string or object with #text
  Pagination?: XmlPagination;
  ELocationID?: XmlELocationID[] | XmlELocationID;
  Abstract?: XmlAbstract;
  AuthorList?: XmlAuthorList;
  Language?: XmlTextElement[] | XmlTextElement; // Array of languages
  GrantList?: XmlGrantList;
  PublicationTypeList?: XmlPublicationTypeList;
  ArticleDate?: XmlArticleDate[] | XmlArticleDate;
  ArticleIdList?: XmlArticleIdList;
  KeywordList?: XmlKeywordList[] | XmlKeywordList; // Can have multiple KeywordList elements
  // Other elements like VernacularTitle, DataBankList, etc.
}

export interface XmlMeshQualifierName extends XmlTextElement {
  _UI?: string;
  _MajorTopicYN?: "Y" | "N";
}
export interface XmlMeshDescriptorName extends XmlTextElement {
  _UI?: string;
  _MajorTopicYN?: "Y" | "N";
}

export interface XmlMeshHeading {
  DescriptorName: XmlMeshDescriptorName;
  QualifierName?: XmlMeshQualifierName[] | XmlMeshQualifierName;
  _MajorTopicYN?: "Y" | "N"; // Can also be at the root of MeshHeading
}

export interface XmlMeshHeadingList {
  MeshHeading: XmlMeshHeading[] | XmlMeshHeading;
}

export interface XmlKeyword extends XmlTextElement {
  _MajorTopicYN?: "Y" | "N";
  _Owner?: string; // NLM, NLM-AUTO, PIP, KIE, NOTNLM, NASA, HHS
}

export interface XmlKeywordList {
  Keyword: XmlKeyword[] | XmlKeyword;
  _Owner?: string;
}

export interface XmlGrant {
  GrantID?: XmlTextElement;
  Acronym?: XmlTextElement;
  Agency?: XmlTextElement;
  Country?: XmlTextElement;
}

export interface XmlGrantList {
  Grant: XmlGrant[] | XmlGrant;
  _CompleteYN?: "Y" | "N";
}

export interface XmlMedlineCitation {
  PMID: XmlPMID;
  DateCreated?: XmlArticleDate;
  DateCompleted?: XmlArticleDate;
  DateRevised?: XmlArticleDate;
  Article?: XmlArticle;
  MeshHeadingList?: XmlMeshHeadingList;
  KeywordList?: XmlKeywordList[] | XmlKeywordList; // Can be an array of KeywordList
  GeneralNote?: (XmlTextElement & { _Owner?: string })[];
  CitationSubset?: XmlTextElement[] | XmlTextElement;
  MedlinePgn?: XmlTextElement; // For page numbers, sometimes here
  // Other elements like CommentsCorrectionsList, GeneSymbolList, etc.
  _Owner?: string; // e.g., "NLM", "NASA", "PIP", "KIE", "HSR", "HMD", "NOTNLM"
  _Status?: string; // e.g., "MEDLINE", "PubMed-not-MEDLINE", "In-Data-Review", "In-Process", "Publisher", "Completed"
}

export interface XmlPubmedArticle {
  MedlineCitation: XmlMedlineCitation;
  PubmedData?: {
    History?: {
      PubMedPubDate: (XmlArticleDate & { _PubStatus?: string })[];
    };
    PublicationStatus?: XmlTextElement;
    ArticleIdList?: XmlArticleIdList; // ArticleIdList can also be under PubmedData
    ReferenceList?: unknown; // Complex structure for references
  };
}

export interface XmlPubmedArticleSet {
  PubmedArticle?: XmlPubmedArticle[] | XmlPubmedArticle;
  DeleteCitation?: {
    PMID: XmlPMID[] | XmlPMID;
  };
  // Can also contain ErrorList or other elements if the request had issues
}

// Parsed object types (for application use, derived from XML types)

export interface ParsedArticleAuthor {
  lastName?: string;
  firstName?: string;
  initials?: string;
  affiliation?: string;
  collectiveName?: string;
}

export interface ParsedArticleDate {
  dateType?: string;
  year?: string;
  month?: string;
  day?: string;
}

export interface ParsedJournalPublicationDate {
  year?: string;
  month?: string;
  day?: string;
  medlineDate?: string;
}

export interface ParsedJournalInfo {
  title?: string;
  isoAbbreviation?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  publicationDate?: ParsedJournalPublicationDate;
}

export interface ParsedMeshTerm {
  descriptorName?: string;
  descriptorUi?: string;
  qualifierName?: string;
  qualifierUi?: string;
  isMajorTopic: boolean;
}

export interface ParsedGrant {
  grantId?: string;
  agency?: string;
  country?: string;
}

export interface ParsedArticle {
  pmid: string;
  title?: string;
  abstractText?: string;
  authors?: ParsedArticleAuthor[];
  journalInfo?: ParsedJournalInfo;
  publicationTypes?: string[];
  keywords?: string[];
  meshTerms?: ParsedMeshTerm[];
  grantList?: ParsedGrant[];
  doi?: string;
  articleDates?: ParsedArticleDate[]; // Dates like 'received', 'accepted', 'revised'
  // Add other fields as needed, e.g., language, publication status
}

// ESummary specific types
// Based on ESummary v2.0 XML (DocSum) and JSON-like XML structure
// This is a common structure, but individual fields can vary.

/**
 * Represents a raw author entry as parsed from ESummary XML.
 * This type accounts for potential inconsistencies in property naming (e.g., Name/name)
 * and structure directly from the XML-to-JavaScript conversion.
 * It is intended for use as an intermediate type before normalization into ESummaryAuthor.
 */
export interface XmlESummaryAuthorRaw {
  Name?: string; // Primary name field (often "LastName Initials")
  name?: string; // Alternative casing for name

  AuthType?: string; // Author type (e.g., "Author")
  authtype?: string; // Alternative casing

  ClusterId?: string; // Cluster ID
  clusterid?: string; // Alternative casing

  "#text"?: string; // If the author is represented as a simple text node

  // Allow other properties as NCBI XML can be unpredictable
  [key: string]: unknown;
}

/**
 * Represents a normalized author entry after parsing from ESummary data.
 * This is the clean, canonical structure for application use.
 */
export interface ESummaryAuthor {
  name: string; // Standardized: "LastName Initials"
  authtype?: string; // Standardized: e.g., "Author"
  clusterid?: string; // Standardized
}

export interface ESummaryArticleId {
  idtype: string; // e.g., "pubmed", "doi", "pmc"
  idtypen: number;
  value: string;
  [key: string]: unknown; // For other attributes like _IdType (if parsed differently)
}

export interface ESummaryHistory {
  pubstatus: string; // e.g., "pubmed", "medline", "entrez"
  date: string; // Date string
}

// For the older DocSum <Item Name="..." Type="..."> structure
export interface ESummaryItem {
  "#text"?: string; // Value of the item
  Item?: ESummaryItem[] | ESummaryItem; // For nested lists
  _Name: string;
  _Type:
    | "String"
    | "Integer"
    | "Date"
    | "List"
    | "Structure"
    | "Unknown"
    | "ERROR";
  [key: string]: unknown; // Other attributes like idtype for ArticleIds
}

export interface ESummaryDocSumOldXml {
  Id: string; // PMID
  Item: ESummaryItem[];
}

// For the newer DocumentSummarySet structure (often from retmode=xml with version=2.0)
export interface ESummaryDocumentSummary {
  "@_uid": string; // PMID
  PubDate?: string;
  EPubDate?: string;
  Source?: string;
  Authors?:
    | XmlESummaryAuthorRaw[] // Array of raw author entries
    | { Author: XmlESummaryAuthorRaw[] | XmlESummaryAuthorRaw } // Object containing raw author entries
    | string; // Or a simple string for authors
  LastAuthor?: string;
  Title?: string;
  SortTitle?: string;
  Volume?: string;
  Issue?: string;
  Pages?: string;
  Lang?: string[];
  ISSN?: string;
  ESSN?: string;
  PubType?: string[]; // Array of publication types
  RecordStatus?: string;
  PubStatus?: string;
  ArticleIds?:
    | ESummaryArticleId[]
    | { ArticleId: ESummaryArticleId[] | ESummaryArticleId };
  History?:
    | ESummaryHistory[]
    | { PubMedPubDate: ESummaryHistory[] | ESummaryHistory };
  References?: unknown[]; // Usually empty or complex
  Attributes?: string[];
  DOI?: string; // Sometimes directly available
  FullJournalName?: string;
  SO?: string; // Source Abbreviation
  [key: string]: unknown; // For other dynamic fields
}

export interface ESummaryDocumentSummarySet {
  DocumentSummary: ESummaryDocumentSummary[] | ESummaryDocumentSummary;
}

export interface ESummaryResult {
  DocSum?: ESummaryDocSumOldXml[] | ESummaryDocSumOldXml; // Older XML format
  DocumentSummarySet?: ESummaryDocumentSummarySet; // Newer XML format
  ERROR?: string; // Error message if present
  [key: string]: unknown; // For other potential top-level elements like 'dbinfo'
}

export interface ESummaryResponseContainer {
  eSummaryResult: ESummaryResult;
  // header?: unknown; // If there's a header part in the response
}

// Parsed brief summary (application-level)
export interface ParsedBriefSummary {
  pmid: string;
  title?: string;
  authors?: string; // Formatted string
  source?: string;
  pubDate?: string; // Standardized YYYY-MM-DD
  epubDate?: string; // Standardized YYYY-MM-DD
  doi?: string;
}

// ESearch specific types
export interface ESearchResultIdList {
  Id: string[];
}

export interface ESearchTranslation {
  From: string;
  To: string;
}

export interface ESearchTranslationSet {
  Translation: ESearchTranslation[];
}

export interface ESearchWarningList {
  PhraseNotFound?: string[];
  QuotedPhraseNotFound?: string[];
  OutputMessage?: string[];
  FieldNotFound?: string[];
}
export interface ESearchErrorList {
  PhraseNotFound?: string[];
  FieldNotFound?: string[];
}

export interface ESearchResultContent {
  Count: string;
  RetMax: string;
  RetStart: string;
  QueryKey?: string;
  WebEnv?: string;
  IdList?: ESearchResultIdList;
  TranslationSet?: ESearchTranslationSet;
  TranslationStack?: unknown; // Usually complex, define if needed
  QueryTranslation: string;
  ErrorList?: ESearchErrorList;
  WarningList?: ESearchWarningList;
}

export interface ESearchResponseContainer {
  eSearchResult: ESearchResultContent;
  // header?: unknown;
}

// Fully parsed and typed result for ESearch
export interface ESearchResult {
  count: number;
  retmax: number;
  retstart: number;
  queryKey?: string;
  webEnv?: string;
  idList: string[];
  queryTranslation: string;
  errorList?: ESearchErrorList;
  warningList?: ESearchWarningList;
}

// Fully parsed and typed result for EFetch
export interface EFetchArticleSet {
  articles: ParsedArticle[];
  // Add any other top-level fields from the parsed EFetch result if necessary
}
