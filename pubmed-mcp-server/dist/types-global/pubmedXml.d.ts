/**
 * @fileoverview Global TypeScript type definitions for PubMed XML structures.
 * These types are used for parsing data returned by NCBI E-utilities,
 * particularly from EFetch for PubMed articles and ESummary.
 * @module src/types-global/pubmedXml
 */
export interface XmlTextElement {
    "#text"?: string;
    [key: string]: unknown;
}
export type XmlPMID = XmlTextElement;
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
    Identifier?: XmlTextElement[];
    CollectiveName?: XmlTextElement;
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
    _EIdType?: string;
    _ValidYN?: "Y" | "N";
}
export interface XmlArticleId extends XmlTextElement {
    _IdType?: string;
}
export interface XmlArticleIdList {
    ArticleId: XmlArticleId[] | XmlArticleId;
}
export interface XmlAbstractText extends XmlTextElement {
    Label?: string;
    NlmCategory?: string;
}
export interface XmlAbstract {
    AbstractText: XmlAbstractText[] | XmlAbstractText;
    CopyrightInformation?: XmlTextElement;
}
export interface XmlPagination {
    MedlinePgn?: XmlTextElement;
    StartPage?: XmlTextElement;
    EndPage?: XmlTextElement;
}
export interface XmlPubDate {
    Year?: XmlTextElement;
    Month?: XmlTextElement;
    Day?: XmlTextElement;
    MedlineDate?: XmlTextElement;
}
export interface XmlJournalIssue {
    Volume?: XmlTextElement;
    Issue?: XmlTextElement;
    PubDate?: XmlPubDate;
    _CitedMedium?: string;
}
export interface XmlJournal {
    ISSN?: XmlTextElement & {
        _IssnType?: string;
    };
    JournalIssue?: XmlJournalIssue;
    Title?: XmlTextElement;
    ISOAbbreviation?: XmlTextElement;
}
export interface XmlArticle {
    Journal?: XmlJournal;
    ArticleTitle?: XmlTextElement | string;
    Pagination?: XmlPagination;
    ELocationID?: XmlELocationID[] | XmlELocationID;
    Abstract?: XmlAbstract;
    AuthorList?: XmlAuthorList;
    Language?: XmlTextElement[] | XmlTextElement;
    GrantList?: XmlGrantList;
    PublicationTypeList?: XmlPublicationTypeList;
    ArticleDate?: XmlArticleDate[] | XmlArticleDate;
    ArticleIdList?: XmlArticleIdList;
    KeywordList?: XmlKeywordList[] | XmlKeywordList;
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
    _MajorTopicYN?: "Y" | "N";
}
export interface XmlMeshHeadingList {
    MeshHeading: XmlMeshHeading[] | XmlMeshHeading;
}
export interface XmlKeyword extends XmlTextElement {
    _MajorTopicYN?: "Y" | "N";
    _Owner?: string;
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
    KeywordList?: XmlKeywordList[] | XmlKeywordList;
    GeneralNote?: (XmlTextElement & {
        _Owner?: string;
    })[];
    CitationSubset?: XmlTextElement[] | XmlTextElement;
    MedlinePgn?: XmlTextElement;
    _Owner?: string;
    _Status?: string;
}
export interface XmlPubmedArticle {
    MedlineCitation: XmlMedlineCitation;
    PubmedData?: {
        History?: {
            PubMedPubDate: (XmlArticleDate & {
                _PubStatus?: string;
            })[];
        };
        PublicationStatus?: XmlTextElement;
        ArticleIdList?: XmlArticleIdList;
        ReferenceList?: unknown;
    };
}
export interface XmlPubmedArticleSet {
    PubmedArticle?: XmlPubmedArticle[] | XmlPubmedArticle;
    DeleteCitation?: {
        PMID: XmlPMID[] | XmlPMID;
    };
}
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
    articleDates?: ParsedArticleDate[];
}
/**
 * Represents a raw author entry as parsed from ESummary XML.
 * This type accounts for potential inconsistencies in property naming (e.g., Name/name)
 * and structure directly from the XML-to-JavaScript conversion.
 * It is intended for use as an intermediate type before normalization into ESummaryAuthor.
 */
export interface XmlESummaryAuthorRaw {
    Name?: string;
    name?: string;
    AuthType?: string;
    authtype?: string;
    ClusterId?: string;
    clusterid?: string;
    "#text"?: string;
    [key: string]: unknown;
}
/**
 * Represents a normalized author entry after parsing from ESummary data.
 * This is the clean, canonical structure for application use.
 */
export interface ESummaryAuthor {
    name: string;
    authtype?: string;
    clusterid?: string;
}
export interface ESummaryArticleId {
    idtype: string;
    idtypen: number;
    value: string;
    [key: string]: unknown;
}
export interface ESummaryHistory {
    pubstatus: string;
    date: string;
}
export interface ESummaryItem {
    "#text"?: string;
    Item?: ESummaryItem[] | ESummaryItem;
    _Name: string;
    _Type: "String" | "Integer" | "Date" | "List" | "Structure" | "Unknown" | "ERROR";
    [key: string]: unknown;
}
export interface ESummaryDocSumOldXml {
    Id: string;
    Item: ESummaryItem[];
}
export interface ESummaryDocumentSummary {
    "@_uid": string;
    PubDate?: string;
    EPubDate?: string;
    Source?: string;
    Authors?: XmlESummaryAuthorRaw[] | {
        Author: XmlESummaryAuthorRaw[] | XmlESummaryAuthorRaw;
    } | string;
    LastAuthor?: string;
    Title?: string;
    SortTitle?: string;
    Volume?: string;
    Issue?: string;
    Pages?: string;
    Lang?: string[];
    ISSN?: string;
    ESSN?: string;
    PubType?: string[];
    RecordStatus?: string;
    PubStatus?: string;
    ArticleIds?: ESummaryArticleId[] | {
        ArticleId: ESummaryArticleId[] | ESummaryArticleId;
    };
    History?: ESummaryHistory[] | {
        PubMedPubDate: ESummaryHistory[] | ESummaryHistory;
    };
    References?: unknown[];
    Attributes?: string[];
    DOI?: string;
    FullJournalName?: string;
    SO?: string;
    [key: string]: unknown;
}
export interface ESummaryDocumentSummarySet {
    DocumentSummary: ESummaryDocumentSummary[] | ESummaryDocumentSummary;
}
export interface ESummaryResult {
    DocSum?: ESummaryDocSumOldXml[] | ESummaryDocSumOldXml;
    DocumentSummarySet?: ESummaryDocumentSummarySet;
    ERROR?: string;
    [key: string]: unknown;
}
export interface ESummaryResponseContainer {
    eSummaryResult: ESummaryResult;
}
export interface ParsedBriefSummary {
    pmid: string;
    title?: string;
    authors?: string;
    source?: string;
    pubDate?: string;
    epubDate?: string;
    doi?: string;
}
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
    TranslationStack?: unknown;
    QueryTranslation: string;
    ErrorList?: ESearchErrorList;
    WarningList?: ESearchWarningList;
}
export interface ESearchResponseContainer {
    eSearchResult: ESearchResultContent;
}
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
export interface EFetchArticleSet {
    articles: ParsedArticle[];
}
//# sourceMappingURL=pubmedXml.d.ts.map