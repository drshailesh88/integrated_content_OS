"""
PubMed/NCBI E-utilities client for searching medical literature.
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import httpx

from ..config import config, Q1_JOURNALS


@dataclass
class PubMedArticle:
    """Represents a PubMed article."""
    pmid: str
    title: str
    abstract: str
    authors: list[str]
    journal: str
    year: str
    doi: Optional[str] = None
    pmcid: Optional[str] = None
    is_q1_journal: bool = False

    def get_citation(self) -> str:
        """Generate formatted citation string."""
        first_author = self.authors[0] if self.authors else "Unknown"
        if len(self.authors) > 1:
            first_author += " et al."
        return f"{first_author}. {self.journal}. {self.year}"

    def get_full_citation(self) -> str:
        """Generate full citation with DOI."""
        citation = self.get_citation()
        if self.doi:
            citation += f" DOI: {self.doi}"
        return citation


class PubMedClient:
    """Client for NCBI E-utilities API."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self):
        self.config = config.pubmed
        self.q1_journals = Q1_JOURNALS

    def _get_base_params(self) -> dict:
        """Get base parameters for all requests."""
        params = {
            "tool": self.config.tool_name,
            "email": self.config.email,
        }
        if self.config.api_key:
            params["api_key"] = self.config.api_key
        return params

    async def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        date_range_years: Optional[int] = None,
        filter_q1_journals: bool = True,
    ) -> list[str]:
        """
        Search PubMed and return list of PMIDs.

        Args:
            query: Search query
            max_results: Maximum number of results
            date_range_years: Limit to articles from last N years
            filter_q1_journals: If True, filter to Q1 journals only

        Returns:
            List of PMIDs
        """
        max_results = max_results or self.config.max_results
        date_range_years = date_range_years or self.config.date_range_years

        # Build query with journal filter
        if filter_q1_journals:
            journal_filter = " OR ".join([f'"{j}"[Journal]' for j in self.q1_journals])
            query = f"({query}) AND ({journal_filter})"

        # Add date filter
        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range_years * 365)
        date_filter = f'{start_date.strftime("%Y/%m/%d")}:{end_date.strftime("%Y/%m/%d")}[Date - Publication]'
        query = f"({query}) AND ({date_filter})"

        params = self._get_base_params()
        params.update({
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
            "sort": "relevance",
        })

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/esearch.fcgi", params=params)
            response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.text)
        pmids = [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text]
        return pmids

    async def fetch_articles(self, pmids: list[str]) -> list[PubMedArticle]:
        """
        Fetch article details for given PMIDs.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of PubMedArticle objects
        """
        if not pmids:
            return []

        params = self._get_base_params()
        params.update({
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
        })

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(f"{self.BASE_URL}/efetch.fcgi", params=params)
            response.raise_for_status()

        return self._parse_articles(response.text)

    def _parse_articles(self, xml_text: str) -> list[PubMedArticle]:
        """Parse efetch XML response into PubMedArticle objects."""
        articles = []
        root = ET.fromstring(xml_text)

        for article_elem in root.findall(".//PubmedArticle"):
            try:
                # Get PMID
                pmid = article_elem.findtext(".//PMID", "")

                # Get article data
                medline = article_elem.find(".//MedlineCitation/Article")
                if medline is None:
                    continue

                # Title
                title = medline.findtext("ArticleTitle", "")

                # Abstract
                abstract_parts = medline.findall(".//Abstract/AbstractText")
                abstract = " ".join([
                    (part.get("Label", "") + ": " if part.get("Label") else "") + (part.text or "")
                    for part in abstract_parts
                ])

                # Authors
                authors = []
                for author in medline.findall(".//AuthorList/Author"):
                    last_name = author.findtext("LastName", "")
                    fore_name = author.findtext("ForeName", "")
                    if last_name:
                        authors.append(f"{last_name} {fore_name}".strip())

                # Journal
                journal = medline.findtext(".//Journal/Title", "")
                journal_abbrev = medline.findtext(".//Journal/ISOAbbreviation", "")

                # Year
                pub_date = medline.find(".//Journal/JournalIssue/PubDate")
                year = ""
                if pub_date is not None:
                    year = pub_date.findtext("Year", "")
                    if not year:
                        medline_date = pub_date.findtext("MedlineDate", "")
                        if medline_date:
                            year = medline_date[:4]

                # DOI
                doi = None
                for article_id in article_elem.findall(".//ArticleIdList/ArticleId"):
                    if article_id.get("IdType") == "doi":
                        doi = article_id.text

                # PMCID
                pmcid = None
                for article_id in article_elem.findall(".//ArticleIdList/ArticleId"):
                    if article_id.get("IdType") == "pmc":
                        pmcid = article_id.text

                # Check if Q1 journal
                is_q1 = any(
                    q1.lower() in journal.lower() or q1.lower() in (journal_abbrev or "").lower()
                    for q1 in self.q1_journals
                )

                articles.append(PubMedArticle(
                    pmid=pmid,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    journal=journal or journal_abbrev,
                    year=year,
                    doi=doi,
                    pmcid=pmcid,
                    is_q1_journal=is_q1,
                ))

            except Exception as e:
                # Skip malformed articles
                print(f"Warning: Could not parse article: {e}")
                continue

        return articles

    async def search_and_fetch(
        self,
        query: str,
        max_results: Optional[int] = None,
        filter_q1_journals: bool = True,
    ) -> list[PubMedArticle]:
        """
        Search PubMed and fetch full article details.

        Args:
            query: Search query
            max_results: Maximum number of results
            filter_q1_journals: If True, filter to Q1 journals

        Returns:
            List of PubMedArticle objects
        """
        pmids = await self.search(
            query=query,
            max_results=max_results,
            filter_q1_journals=filter_q1_journals,
        )
        if not pmids:
            return []

        return await self.fetch_articles(pmids)


# Singleton instance
pubmed_client = PubMedClient()
