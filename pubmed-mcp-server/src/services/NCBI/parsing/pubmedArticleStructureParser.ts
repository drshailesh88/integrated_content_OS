/**
 * @fileoverview Helper functions for parsing detailed PubMed Article XML structures,
 * typically from EFetch results.
 * @module src/services/NCBI/parsing/pubmedArticleStructureParser
 */

import {
  XmlAbstractText,
  XmlArticle,
  XmlArticleDate,
  XmlAuthor,
  XmlAuthorList,
  XmlGrant,
  XmlGrantList,
  XmlJournal,
  XmlKeyword,
  XmlKeywordList,
  XmlMedlineCitation,
  XmlMeshHeading,
  XmlMeshHeadingList,
  XmlPublicationType,
  XmlPublicationTypeList,
  ParsedArticleAuthor,
  ParsedJournalInfo,
  ParsedMeshTerm,
  ParsedGrant,
  ParsedArticleDate,
} from "../../../types-global/pubmedXml.js";
import { ensureArray, getText, getAttribute } from "./xmlGenericHelpers.js";

/**
 * Extracts and formats author information from XML.
 * @param authorListXml - The XML AuthorList element.
 * @returns An array of formatted author objects.
 */
export function extractAuthors(
  authorListXml?: XmlAuthorList,
): ParsedArticleAuthor[] {
  if (!authorListXml) return [];
  const authors = ensureArray(authorListXml.Author);
  return authors.map((auth: XmlAuthor) => {
    const collectiveName = getText(auth.CollectiveName);
    if (collectiveName) {
      return { collectiveName };
    }

    let affiliation = "";
    const affiliations = ensureArray(auth.AffiliationInfo);
    if (affiliations.length > 0) {
      affiliation = getText(affiliations[0]?.Affiliation);
    }
    return {
      lastName: getText(auth.LastName),
      firstName: getText(auth.ForeName), // XML uses ForeName
      initials: getText(auth.Initials),
      affiliation: affiliation || undefined, // Ensure undefined if empty
    };
  });
}

/**
 * Extracts and formats journal information from XML.
 * @param journalXml - The XML Journal element from an Article.
 * @param medlineCitationXml - The XML MedlineCitation element (for MedlinePgn).
 * @returns Formatted journal information.
 */
export function extractJournalInfo(
  journalXml?: XmlJournal,
  medlineCitationXml?: XmlMedlineCitation,
): ParsedJournalInfo | undefined {
  if (!journalXml) return undefined;

  const pubDate = journalXml.JournalIssue?.PubDate;
  const year = getText(
    pubDate?.Year,
    getText(pubDate?.MedlineDate, "").match(/\d{4}/)?.[0],
  );

  return {
    title: getText(journalXml.Title),
    isoAbbreviation: getText(journalXml.ISOAbbreviation),
    volume: getText(journalXml.JournalIssue?.Volume),
    issue: getText(journalXml.JournalIssue?.Issue),
    pages:
      getText(medlineCitationXml?.MedlinePgn) ||
      getText(medlineCitationXml?.Article?.Pagination?.MedlinePgn),
    publicationDate: {
      year: year || undefined,
      month: getText(pubDate?.Month) || undefined,
      day: getText(pubDate?.Day) || undefined,
      medlineDate: getText(pubDate?.MedlineDate) || undefined,
    },
  };
}

/**
 * Extracts and formats MeSH terms from XML.
 * @param meshHeadingListXml - The XML MeshHeadingList element.
 * @returns An array of formatted MeSH term objects.
 */
export function extractMeshTerms(
  meshHeadingListXml?: XmlMeshHeadingList,
): ParsedMeshTerm[] {
  if (!meshHeadingListXml) return [];
  const meshHeadings = ensureArray(meshHeadingListXml.MeshHeading);
  return meshHeadings.map((mh: XmlMeshHeading) => {
    const qualifiers = ensureArray(mh.QualifierName);
    const firstQualifier = qualifiers[0];

    // Check MajorTopicYN at DescriptorName, QualifierName, and the root MeshHeading element
    const isMajorDescriptor =
      getAttribute(mh.DescriptorName, "MajorTopicYN") === "Y";
    const isMajorQualifier = firstQualifier
      ? getAttribute(firstQualifier, "MajorTopicYN") === "Y"
      : false;
    // Some schemas might place MajorTopicYN directly on MeshHeading if no qualifiers
    const isMajorRoot = getAttribute(mh, "MajorTopicYN") === "Y";

    return {
      descriptorName: getText(mh.DescriptorName),
      descriptorUi: getAttribute(mh.DescriptorName, "UI"),
      qualifierName: firstQualifier ? getText(firstQualifier) : undefined,
      qualifierUi: firstQualifier
        ? getAttribute(firstQualifier, "UI")
        : undefined,
      isMajorTopic: isMajorRoot || isMajorDescriptor || isMajorQualifier,
    };
  });
}

/**
 * Extracts and formats grant information from XML.
 * @param grantListXml - The XML GrantList element.
 * @returns An array of formatted grant objects.
 */
export function extractGrants(grantListXml?: XmlGrantList): ParsedGrant[] {
  if (!grantListXml) return [];
  const grants = ensureArray(grantListXml.Grant);
  return grants.map((g: XmlGrant) => ({
    grantId: getText(g.GrantID) || undefined,
    agency: getText(g.Agency) || undefined,
    country: getText(g.Country) || undefined,
  }));
}

/**
 * Extracts DOI from various possible locations in the XML.
 * Prioritizes ELocationID with ValidYN="Y", then any ELocationID, then ArticleIdList.
 * @param articleXml - The XML Article element.
 * @returns The DOI string or undefined.
 */
export function extractDoi(articleXml?: XmlArticle): string | undefined {
  if (!articleXml) return undefined;

  // Check ELocationID first
  const eLocationIDs = ensureArray(articleXml.ELocationID);
  // Prioritize valid DOI
  for (const eloc of eLocationIDs) {
    if (
      getAttribute(eloc, "EIdType") === "doi" &&
      getAttribute(eloc, "ValidYN") === "Y"
    ) {
      const doi = getText(eloc);
      if (doi) return doi;
    }
  }
  // Fallback to any DOI in ELocationID
  for (const eloc of eLocationIDs) {
    if (getAttribute(eloc, "EIdType") === "doi") {
      const doi = getText(eloc);
      if (doi) return doi;
    }
  }

  // Check ArticleIdList as a secondary source
  const articleIds = ensureArray(articleXml.ArticleIdList?.ArticleId);
  for (const aid of articleIds) {
    if (getAttribute(aid, "IdType") === "doi") {
      const doi = getText(aid);
      if (doi) return doi;
    }
  }
  return undefined;
}

/**
 * Extracts publication types from XML.
 * @param publicationTypeListXml - The XML PublicationTypeList element.
 * @returns An array of publication type strings.
 */
export function extractPublicationTypes(
  publicationTypeListXml?: XmlPublicationTypeList,
): string[] {
  if (!publicationTypeListXml) return [];
  const pubTypes = ensureArray(publicationTypeListXml.PublicationType);
  return pubTypes.map((pt: XmlPublicationType) => getText(pt)).filter(Boolean);
}

/**
 * Extracts keywords from XML. Handles single or multiple KeywordList elements.
 * @param keywordListsXml - The XML KeywordList element or an array of them.
 * @returns An array of keyword strings.
 */
export function extractKeywords(
  keywordListsXml?: XmlKeywordList[] | XmlKeywordList,
): string[] {
  if (!keywordListsXml) return [];
  const lists = ensureArray(keywordListsXml);
  const allKeywords: string[] = [];
  for (const list of lists) {
    const keywords = ensureArray(list.Keyword);
    keywords.forEach((kw: XmlKeyword) => {
      const keywordText = getText(kw);
      if (keywordText) {
        allKeywords.push(keywordText);
      }
    });
  }
  return allKeywords;
}

/**
 * Extracts abstract text from XML. Handles structured abstracts by concatenating sections.
 * If AbstractText is an array, joins them. If it's a single object/string, uses it directly.
 * Prefixes with Label if present.
 * @param abstractXml - The XML Abstract element from an Article.
 * @returns The abstract text string, or undefined if not found or empty.
 */
export function extractAbstractText(
  abstractXml?: XmlArticle["Abstract"],
): string | undefined {
  if (!abstractXml || !abstractXml.AbstractText) return undefined;

  const abstractTexts = ensureArray(abstractXml.AbstractText);
  if (abstractTexts.length === 0) return undefined;

  const processedTexts = abstractTexts
    .map((at: XmlAbstractText | string) => {
      // AbstractText can be string directly or object
      if (typeof at === "string") {
        return at;
      }
      // If it's an object, it should have #text or Label
      const sectionText = getText(at); // Handles at["#text"]
      const label = getAttribute(at, "Label");
      if (label && sectionText) {
        return `${label.trim()}: ${sectionText.trim()}`;
      }
      return sectionText.trim();
    })
    .filter(Boolean); // Remove any empty strings resulting from empty sections

  if (processedTexts.length === 0) return undefined;

  return processedTexts.join("\n\n").trim() || undefined; // Join sections with double newline
}

/**
 * Extracts PMID from MedlineCitation.
 * @param medlineCitationXml - The XML MedlineCitation element.
 * @returns The PMID string or undefined.
 */
export function extractPmid(
  medlineCitationXml?: XmlMedlineCitation,
): string | undefined {
  if (!medlineCitationXml || !medlineCitationXml.PMID) return undefined;
  return getText(medlineCitationXml.PMID);
}

/**
 * Extracts article dates from XML.
 * @param articleXml - The XML Article element.
 * @returns An array of parsed article dates.
 */
export function extractArticleDates(
  articleXml?: XmlArticle,
): ParsedArticleDate[] {
  if (!articleXml || !articleXml.ArticleDate) return [];
  const articleDatesXml = ensureArray(articleXml.ArticleDate);
  return articleDatesXml.map((ad: XmlArticleDate) => ({
    dateType: getAttribute(ad, "DateType"),
    year: getText(ad.Year),
    month: getText(ad.Month),
    day: getText(ad.Day),
  }));
}
