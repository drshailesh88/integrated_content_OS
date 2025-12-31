"""
PubMed Fetcher
Fetches recent cardiology articles from PubMed using the NCBI E-utilities API.
Includes fallback journal-specific queries for journals with broken RSS feeds.
"""

import requests
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '..')
from config import (
    PUBMED_SEARCH_URL, PUBMED_FETCH_URL, PUBMED_SEARCH_QUERY,
    PUBMED_MAX_RESULTS, NCBI_API_KEY, REQUEST_TIMEOUT
)

# =============================================================================
# FALLBACK JOURNALS - For journals with broken/blocked RSS feeds
# Uses PubMed journal-specific queries to fetch articles
# =============================================================================

FALLBACK_JOURNALS = [
    # JACC Family (blocked by Cloudflare)
    {
        "id": "jacc",
        "name": "JACC",
        "pubmed_query": '"J Am Coll Cardiol"[journal]',
        "tier": "cardiology",
        "max_results": 15
    },
    {
        "id": "jacc-interventions",
        "name": "JACC Cardiovascular Interventions",
        "pubmed_query": '"JACC Cardiovasc Interv"[journal]',
        "tier": "interventional",
        "max_results": 10
    },
    {
        "id": "jacc-hf",
        "name": "JACC Heart Failure",
        "pubmed_query": '"JACC Heart Fail"[journal]',
        "tier": "heartfailure",
        "max_results": 10
    },
    {
        "id": "jacc-imaging",
        "name": "JACC Cardiovascular Imaging",
        "pubmed_query": '"JACC Cardiovasc Imaging"[journal]',
        "tier": "imaging",
        "max_results": 10
    },
    # European Heart Journal (OUP - sometimes blocked)
    {
        "id": "ehj",
        "name": "European Heart Journal",
        "pubmed_query": '"Eur Heart J"[journal]',
        "tier": "cardiology",
        "max_results": 15
    },
    # European Journal of Preventive Cardiology
    {
        "id": "ejpc",
        "name": "European Journal of Preventive Cardiology",
        "pubmed_query": '"Eur J Prev Cardiol"[journal]',
        "tier": "prevention",
        "max_results": 10
    },
    # EuroIntervention (often blocked)
    {
        "id": "eurointervention",
        "name": "EuroIntervention",
        "pubmed_query": '"EuroIntervention"[journal]',
        "tier": "interventional",
        "max_results": 10
    },
]


def search_pubmed(query: str = None, max_results: int = None) -> Dict:
    """
    Search PubMed for articles matching the query.
    
    Args:
        query: PubMed search query. Uses default cardiology query if not provided.
        max_results: Maximum number of results. Uses config default if not provided.
        
    Returns:
        Dictionary with WebEnv, query_key, and count for fetching results
    """
    if query is None:
        query = PUBMED_SEARCH_QUERY
    if max_results is None:
        max_results = PUBMED_MAX_RESULTS
    
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "usehistory": "y"
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    
    try:
        response = requests.get(
            PUBMED_SEARCH_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        result = data.get("esearchresult", {})
        return {
            "webenv": result.get("webenv"),
            "query_key": result.get("querykey"),
            "count": int(result.get("count", 0)),
            "ids": result.get("idlist", [])
        }
    except Exception as e:
        print(f"  ✗ PubMed search error: {e}")
        return {"webenv": None, "query_key": None, "count": 0, "ids": []}


def fetch_abstracts(webenv: str, query_key: str, count: int) -> str:
    """
    Fetch full abstracts using the WebEnv from search.
    
    Args:
        webenv: WebEnv token from search
        query_key: Query key from search
        count: Number of results to fetch
        
    Returns:
        XML string of abstract data
    """
    params = {
        "db": "pubmed",
        "WebEnv": webenv,
        "query_key": query_key,
        "retmode": "xml",
        "rettype": "abstract",
        "retmax": count
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    
    try:
        response = requests.get(
            PUBMED_FETCH_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  ✗ PubMed fetch error: {e}")
        return ""


def parse_pubmed_xml(xml_content: str, override_journal: str = None, override_tier: str = None) -> List[Dict]:
    """
    Parse PubMed XML response into article dictionaries.
    
    Args:
        xml_content: XML string from efetch
        override_journal: Optional journal name to use (for display consistency)
        override_tier: Optional tier to assign
        
    Returns:
        List of article dictionaries
    """
    articles = []
    
    try:
        root = ET.fromstring(xml_content)
        
        for article_elem in root.findall(".//PubmedArticle"):
            try:
                # Extract article data
                medline = article_elem.find(".//MedlineCitation")
                if medline is None:
                    continue
                
                article_data = medline.find(".//Article")
                if article_data is None:
                    continue
                
                # Title
                title_elem = article_data.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None and title_elem.text else ""
                
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
                
                # Journal
                if override_journal:
                    journal = override_journal
                else:
                    journal_elem = article_data.find(".//Journal/Title")
                    journal = journal_elem.text if journal_elem is not None and journal_elem.text else ""
                    # Short journal name
                    journal_abbrev = article_data.find(".//Journal/ISOAbbreviation")
                    if journal_abbrev is not None and journal_abbrev.text:
                        journal = journal_abbrev.text
                
                # Authors
                author_list = []
                for author in article_data.findall(".//AuthorList/Author"):
                    lastname = author.find("LastName")
                    initials = author.find("Initials")
                    if lastname is not None and lastname.text:
                        name = lastname.text
                        if initials is not None and initials.text:
                            name += f" {initials.text}"
                        author_list.append(name)
                
                if len(author_list) > 3:
                    authors = f"{author_list[0]}, {author_list[1]}, et al"
                else:
                    authors = ", ".join(author_list)
                
                # Date
                pub_date = ""
                date_elem = article_data.find(".//Journal/JournalIssue/PubDate")
                if date_elem is not None:
                    year = date_elem.find("Year")
                    month = date_elem.find("Month")
                    day = date_elem.find("Day")
                    if year is not None and year.text:
                        pub_date = year.text
                        if month is not None and month.text:
                            pub_date += f"-{month.text}"
                            if day is not None and day.text:
                                pub_date += f"-{day.text}"
                
                # PMID
                pmid_elem = medline.find(".//PMID")
                pmid = pmid_elem.text if pmid_elem is not None else ""
                
                # DOI
                doi = ""
                for id_elem in article_elem.findall(".//ArticleIdList/ArticleId"):
                    if id_elem.get("IdType") == "doi":
                        doi = id_elem.text if id_elem.text else ""
                        break
                
                # Build article dict
                article = {
                    "source": "pubmed",
                    "title": title,
                    "abstract": abstract,
                    "journal": journal,
                    "tier": override_tier if override_tier else "pubmed",
                    "pub_date": pub_date,
                    "authors": authors,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                    "doi": doi,
                    "pmid": pmid
                }
                
                # Only add if we have title and abstract
                if title and abstract:
                    articles.append(article)
                    
            except Exception as e:
                # Skip problematic articles
                continue
                
    except ET.ParseError as e:
        print(f"  ✗ XML parsing error: {e}")
    
    return articles


def fetch_journal_articles(journal_config: Dict, days_back: int = 7) -> List[Dict]:
    """
    Fetch articles from a specific journal via PubMed.
    
    Args:
        journal_config: Dictionary with name, pubmed_query, tier, max_results
        days_back: How many days back to search (default 7)
        
    Returns:
        List of article dictionaries
    """
    # Build date-limited query using explicit date range (more reliable)
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    date_filter = f'AND ("{start_date.strftime("%Y/%m/%d")}"[PDAT] : "{end_date.strftime("%Y/%m/%d")}"[PDAT])'
    query = f"{journal_config['pubmed_query']} {date_filter}"
    max_results = journal_config.get('max_results', 10)
    
    # Search
    search_result = search_pubmed(query, max_results)
    
    if not search_result["webenv"] or search_result["count"] == 0:
        return []
    
    # Fetch abstracts
    xml_content = fetch_abstracts(
        search_result["webenv"],
        search_result["query_key"],
        min(search_result["count"], max_results)
    )
    
    if not xml_content:
        return []
    
    # Parse with journal override
    articles = parse_pubmed_xml(
        xml_content, 
        override_journal=journal_config['name'],
        override_tier=journal_config['tier']
    )
    
    return articles


def fetch_fallback_journals(journals: List[Dict] = None, days_back: int = 7) -> List[Dict]:
    """
    Fetch articles from all fallback journals (those with broken RSS feeds).
    
    Args:
        journals: List of journal configs. Uses FALLBACK_JOURNALS if not provided.
        days_back: How many days back to search
        
    Returns:
        List of all fetched articles
    """
    if journals is None:
        journals = FALLBACK_JOURNALS
    
    print(f"\n📚 Fetching from fallback journals via PubMed ({len(journals)} journals)...")
    print("-" * 40)
    
    all_articles = []
    successful = 0
    
    for journal in journals:
        articles = fetch_journal_articles(journal, days_back)
        if articles:
            successful += 1
            all_articles.extend(articles)
            print(f"  ✓ {journal['name']}: {len(articles)} articles")
        else:
            print(f"  ○ {journal['name']}: No recent articles")
    
    print("-" * 40)
    print(f"📊 Fallback journals: {len(all_articles)} articles from {successful}/{len(journals)} journals\n")
    
    return all_articles


def fetch_pubmed_articles(query: str = None, max_results: int = None) -> List[Dict]:
    """
    Main function to fetch articles from PubMed (general cardiology query).
    
    Args:
        query: PubMed search query (optional)
        max_results: Maximum number of results (optional)
        
    Returns:
        List of article dictionaries
    """
    print(f"\n🔬 Fetching PubMed articles (general cardiology)...")
    print("-" * 40)
    
    # Step 1: Search
    search_result = search_pubmed(query, max_results)
    
    if not search_result["webenv"]:
        print("  ○ No results from PubMed search")
        return []
    
    print(f"  ✓ Found {search_result['count']} matching articles")
    
    # Step 2: Fetch abstracts
    xml_content = fetch_abstracts(
        search_result["webenv"],
        search_result["query_key"],
        min(search_result["count"], max_results or PUBMED_MAX_RESULTS)
    )
    
    if not xml_content:
        print("  ○ Could not fetch abstracts")
        return []
    
    # Step 3: Parse XML
    articles = parse_pubmed_xml(xml_content)
    
    print(f"  ✓ Parsed {len(articles)} articles with abstracts")
    print("-" * 40)
    print(f"📊 General PubMed: {len(articles)} articles\n")
    
    return articles


def fetch_all_pubmed(include_fallback: bool = True, days_back: int = 7) -> List[Dict]:
    """
    Fetch all PubMed articles: general query + fallback journals.
    
    Args:
        include_fallback: Whether to fetch from fallback journals
        days_back: Days back for fallback journal search
        
    Returns:
        Combined list of all articles
    """
    all_articles = []
    
    # Fetch general cardiology articles
    general = fetch_pubmed_articles()
    all_articles.extend(general)
    
    # Fetch from fallback journals (JACC, EHJ, etc.)
    if include_fallback:
        fallback = fetch_fallback_journals(days_back=days_back)
        all_articles.extend(fallback)
    
    return all_articles


if __name__ == "__main__":
    # Test the fetcher with fallback journals
    print("=" * 60)
    print("Testing PubMed Fetcher with Fallback Journals")
    print("=" * 60)
    
    # Test general query
    general_articles = fetch_pubmed_articles()
    
    # Test fallback journals
    fallback_articles = fetch_fallback_journals()
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {len(general_articles)} general + {len(fallback_articles)} fallback = {len(general_articles) + len(fallback_articles)} articles")
    print("=" * 60)
    
    print("\n📝 Sample JACC articles:")
    jacc_articles = [a for a in fallback_articles if 'JACC' in a['journal']]
    for article in jacc_articles[:3]:
        print(f"\n  Title: {article['title'][:60]}...")
        print(f"  Journal: {article['journal']}")
        print(f"  PMID: {article.get('pmid', 'N/A')}")

