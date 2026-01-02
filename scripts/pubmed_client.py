"""
PubMed Client - Standalone NCBI E-utilities wrapper

A reusable Python module for searching and fetching PubMed articles.
Can be imported by any skill in the integrated content OS.

Usage:
    from scripts.pubmed_client import PubMedClient

    client = PubMedClient()
    results = client.search("SGLT2 inhibitors heart failure")
    articles = client.fetch_articles(results["ids"])

Environment:
    NCBI_API_KEY: Optional but recommended for higher rate limits
"""

import os
import time
import requests
from typing import List, Dict, Any, Optional
from xml.etree import ElementTree as ET
from dataclasses import dataclass, asdict
from datetime import datetime


# NCBI E-utilities endpoints
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_LINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# Rate limiting (without API key: 3 requests/sec, with key: 10 requests/sec)
DEFAULT_TIMEOUT = 30
MIN_REQUEST_INTERVAL = 0.35  # ~3 requests/sec


@dataclass
class PubMedArticle:
    """Structured representation of a PubMed article."""
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    pub_date: str
    doi: str = ""
    pmc_id: str = ""
    keywords: List[str] = None
    mesh_terms: List[str] = None

    def __post_init__(self):
        self.keywords = self.keywords or []
        self.mesh_terms = self.mesh_terms or []

    @property
    def url(self) -> str:
        return f"https://pubmed.ncbi.nlm.nih.gov/{self.pmid}/"

    @property
    def citation(self) -> str:
        """Generate a short citation."""
        first_author = self.authors[0] if self.authors else "Unknown"
        if len(self.authors) > 1:
            first_author += " et al"
        year = self.pub_date[:4] if self.pub_date else ""
        return f"{first_author}. {self.journal}. {year}."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PubMedClient:
    """
    Client for interacting with PubMed via NCBI E-utilities.

    Features:
    - Search articles with boolean queries
    - Fetch full article details including abstracts
    - Get related articles (similar, cited by, references)
    - Rate limiting built-in
    """

    def __init__(self, api_key: str = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize PubMed client.

        Args:
            api_key: NCBI API key. If not provided, uses NCBI_API_KEY env var.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or os.environ.get("NCBI_API_KEY")
        self.timeout = timeout
        self._last_request_time = 0

    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed)
        self._last_request_time = time.time()

    def _get_params(self, **kwargs) -> Dict[str, str]:
        """Build request params with API key if available."""
        params = {"db": "pubmed", **kwargs}
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    def search(
        self,
        query: str,
        max_results: int = 20,
        sort: str = "relevance",
        min_date: str = None,
        max_date: str = None
    ) -> Dict[str, Any]:
        """
        Search PubMed for articles.

        Args:
            query: PubMed search query (supports boolean operators)
            max_results: Maximum number of results (default 20, max 10000)
            sort: Sort order - "relevance" or "pub_date"
            min_date: Minimum publication date (YYYY/MM/DD)
            max_date: Maximum publication date (YYYY/MM/DD)

        Returns:
            Dict with 'ids' (list of PMIDs), 'count' (total matches),
            'webenv' and 'query_key' for pagination

        Example:
            results = client.search("SGLT2 heart failure", max_results=10)
            print(f"Found {results['count']} articles")
        """
        self._rate_limit()

        params = self._get_params(
            term=query,
            retmax=min(max_results, 10000),
            retmode="json",
            usehistory="y",
            sort=sort
        )

        if min_date:
            params["mindate"] = min_date
        if max_date:
            params["maxdate"] = max_date
        if min_date or max_date:
            params["datetype"] = "pdat"

        try:
            response = requests.get(
                PUBMED_SEARCH_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            result = data.get("esearchresult", {})
            return {
                "ids": result.get("idlist", []),
                "count": int(result.get("count", 0)),
                "webenv": result.get("webenv"),
                "query_key": result.get("querykey"),
                "query": query
            }
        except Exception as e:
            return {"ids": [], "count": 0, "error": str(e)}

    def fetch_articles(
        self,
        pmids: List[str],
        include_mesh: bool = False
    ) -> List[PubMedArticle]:
        """
        Fetch full article details for given PMIDs.

        Args:
            pmids: List of PubMed IDs
            include_mesh: Whether to include MeSH terms (slower)

        Returns:
            List of PubMedArticle objects with full details
        """
        if not pmids:
            return []

        self._rate_limit()

        params = self._get_params(
            id=",".join(pmids),
            retmode="xml",
            rettype="abstract"
        )

        try:
            response = requests.get(
                PUBMED_FETCH_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return self._parse_articles_xml(response.text, include_mesh)
        except Exception as e:
            print(f"PubMed fetch error: {e}")
            return []

    def search_and_fetch(
        self,
        query: str,
        max_results: int = 10,
        **search_kwargs
    ) -> List[PubMedArticle]:
        """
        Convenience method: search and fetch in one call.

        Args:
            query: Search query
            max_results: Maximum articles to return
            **search_kwargs: Additional args passed to search()

        Returns:
            List of PubMedArticle objects
        """
        results = self.search(query, max_results=max_results, **search_kwargs)
        if results.get("error"):
            return []
        return self.fetch_articles(results["ids"])

    def get_related_articles(
        self,
        pmid: str,
        link_type: str = "pubmed_pubmed",
        max_results: int = 10
    ) -> List[str]:
        """
        Get related article PMIDs.

        Args:
            pmid: Source article PMID
            link_type: Type of relationship
                - "pubmed_pubmed": Similar articles (default)
                - "pubmed_pubmed_citedin": Articles citing this one
                - "pubmed_pubmed_refs": References in this article

        Returns:
            List of related PMIDs
        """
        self._rate_limit()

        params = self._get_params(
            dbfrom="pubmed",
            id=pmid,
            linkname=link_type,
            retmode="json"
        )

        try:
            response = requests.get(
                PUBMED_LINK_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            linksets = data.get("linksets", [])
            if not linksets:
                return []

            links = linksets[0].get("linksetdbs", [])
            if not links:
                return []

            ids = links[0].get("links", [])
            return [str(id_) for id_ in ids[:max_results]]
        except Exception as e:
            return []

    def _parse_articles_xml(
        self,
        xml_content: str,
        include_mesh: bool = False
    ) -> List[PubMedArticle]:
        """Parse PubMed XML response into article objects."""
        articles = []

        try:
            root = ET.fromstring(xml_content)

            for article_elem in root.findall(".//PubmedArticle"):
                try:
                    article = self._parse_single_article(article_elem, include_mesh)
                    if article:
                        articles.append(article)
                except Exception:
                    continue

        except ET.ParseError:
            pass

        return articles

    def _parse_single_article(
        self,
        elem: ET.Element,
        include_mesh: bool
    ) -> Optional[PubMedArticle]:
        """Parse a single PubmedArticle XML element."""
        medline = elem.find(".//MedlineCitation")
        if medline is None:
            return None

        article_data = medline.find(".//Article")
        if article_data is None:
            return None

        # PMID
        pmid_elem = medline.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else ""
        if not pmid:
            return None

        # Title
        title_elem = article_data.find(".//ArticleTitle")
        title = self._get_text(title_elem)

        # Abstract
        abstract_parts = []
        abstract_elem = article_data.find(".//Abstract")
        if abstract_elem is not None:
            for text in abstract_elem.findall(".//AbstractText"):
                if text.text:
                    label = text.get("Label", "")
                    if label:
                        abstract_parts.append(f"{label}: {text.text}")
                    else:
                        abstract_parts.append(text.text)
        abstract = " ".join(abstract_parts)

        # Authors
        authors = []
        for author in article_data.findall(".//AuthorList/Author"):
            lastname = self._get_text(author.find("LastName"))
            initials = self._get_text(author.find("Initials"))
            if lastname:
                name = f"{lastname} {initials}" if initials else lastname
                authors.append(name)

        # Journal
        journal_elem = article_data.find(".//Journal/ISOAbbreviation")
        if journal_elem is None:
            journal_elem = article_data.find(".//Journal/Title")
        journal = self._get_text(journal_elem)

        # Publication date
        pub_date = ""
        date_elem = article_data.find(".//Journal/JournalIssue/PubDate")
        if date_elem is not None:
            year = self._get_text(date_elem.find("Year"))
            month = self._get_text(date_elem.find("Month"))
            day = self._get_text(date_elem.find("Day"))
            if year:
                pub_date = year
                if month:
                    pub_date += f"-{month}"
                    if day:
                        pub_date += f"-{day}"

        # DOI
        doi = ""
        for id_elem in elem.findall(".//ArticleIdList/ArticleId"):
            if id_elem.get("IdType") == "doi":
                doi = id_elem.text or ""
                break

        # PMC ID
        pmc_id = ""
        for id_elem in elem.findall(".//ArticleIdList/ArticleId"):
            if id_elem.get("IdType") == "pmc":
                pmc_id = id_elem.text or ""
                break

        # Keywords
        keywords = []
        for kw in article_data.findall(".//KeywordList/Keyword"):
            if kw.text:
                keywords.append(kw.text)

        # MeSH terms (if requested)
        mesh_terms = []
        if include_mesh:
            for mesh in medline.findall(".//MeshHeadingList/MeshHeading/DescriptorName"):
                if mesh.text:
                    mesh_terms.append(mesh.text)

        return PubMedArticle(
            pmid=pmid,
            title=title,
            abstract=abstract,
            authors=authors,
            journal=journal,
            pub_date=pub_date,
            doi=doi,
            pmc_id=pmc_id,
            keywords=keywords,
            mesh_terms=mesh_terms
        )

    @staticmethod
    def _get_text(elem: Optional[ET.Element]) -> str:
        """Safely get text from an XML element."""
        return elem.text.strip() if elem is not None and elem.text else ""


# Convenience function for quick searches
def search_pubmed(
    query: str,
    max_results: int = 10,
    fetch: bool = True
) -> List[Dict[str, Any]]:
    """
    Quick function to search PubMed and optionally fetch full details.

    Args:
        query: Search query
        max_results: Maximum results
        fetch: If True, return full article details; if False, just PMIDs

    Returns:
        List of article dictionaries or PMIDs
    """
    client = PubMedClient()

    if fetch:
        articles = client.search_and_fetch(query, max_results)
        return [a.to_dict() for a in articles]
    else:
        results = client.search(query, max_results)
        return results.get("ids", [])


if __name__ == "__main__":
    # Test the client
    print("=" * 60)
    print("PubMed Client Test")
    print("=" * 60)

    client = PubMedClient()

    # Test search
    print("\n1. Searching for SGLT2 heart failure articles...")
    results = client.search("SGLT2 inhibitors heart failure", max_results=5)
    print(f"   Found {results['count']} total matches, fetched {len(results['ids'])} IDs")

    # Test fetch
    if results["ids"]:
        print("\n2. Fetching full article details...")
        articles = client.fetch_articles(results["ids"][:3])
        for article in articles:
            print(f"\n   Title: {article.title[:60]}...")
            print(f"   Journal: {article.journal}")
            print(f"   Citation: {article.citation}")
            print(f"   URL: {article.url}")

    # Test convenience function
    print("\n3. Testing convenience function...")
    quick_results = search_pubmed("GLP-1 cardiovascular", max_results=3)
    print(f"   Got {len(quick_results)} articles")
    if quick_results:
        print(f"   First: {quick_results[0]['title'][:50]}...")

    print("\n" + "=" * 60)
    print("Test complete!")
