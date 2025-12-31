#!/usr/bin/env python3
"""
Parallel Knowledge Pipeline

Dual-pipeline research system that queries BOTH in parallel:
1. RAG Pipeline - Textbooks & guidelines from AstraDB vector store
2. PubMed Pipeline - Latest research via PubMed MCP server

Usage:
    from src.knowledge_pipeline import KnowledgePipeline

    pipeline = KnowledgePipeline()
    results = pipeline.research("What are the optimal LDL targets for high-risk patients?")

Note: This is for RESEARCH/EVIDENCE gathering only.
      Perplexity is used separately for social listening and demand assessment.
"""

import os
import sys
import json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment
load_dotenv()

# Import RAG components
try:
    from advanced_retriever import AdvancedRetriever
    from synthesizer import KnowledgeSynthesizer
except ImportError:
    print("Warning: RAG components not available")
    AdvancedRetriever = None
    KnowledgeSynthesizer = None

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NCBI_API_KEY = os.getenv("NCBI_API_key")

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import requests
except ImportError:
    requests = None


class RAGPipeline:
    """Retrieves knowledge from AstraDB vector store (textbooks/guidelines)."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.retriever = None
        self.synthesizer = None

        if AdvancedRetriever:
            try:
                self.retriever = AdvancedRetriever(verbose=verbose)
                self.synthesizer = KnowledgeSynthesizer()
                if verbose:
                    print("✅ RAG Pipeline initialized (AstraDB)")
            except Exception as e:
                print(f"⚠️ RAG Pipeline init failed: {e}")

    def query(
        self,
        question: str,
        top_k: int = 10,
        synthesize: bool = False
    ) -> Dict[str, Any]:
        """Query the RAG system for textbook/guideline knowledge."""
        if not self.retriever:
            return {"error": "RAG not available", "chunks": [], "source": "rag"}

        try:
            chunks = self.retriever.retrieve(
                question,
                top_k=top_k,
                use_multi_query=True,
                use_hyde=True,
                use_self_query=True,
                verbose=self.verbose
            )

            result = {
                "source": "rag_textbooks_guidelines",
                "query": question,
                "chunks": chunks,
                "num_results": len(chunks),
                "timestamp": datetime.now().isoformat()
            }

            if synthesize and chunks and self.synthesizer:
                synthesis = self.synthesizer.synthesize(question, chunks, verbose=self.verbose)
                result["synthesis"] = synthesis.get("synthesis", "")

            return result

        except Exception as e:
            return {"error": str(e), "chunks": [], "source": "rag"}


class PubMedPipeline:
    """
    Retrieves knowledge from PubMed via NCBI E-utilities API.

    This is a direct API implementation. The PubMed MCP server
    can also be used when available in Claude Code context.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.api_key = NCBI_API_KEY
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

        if verbose:
            if self.api_key:
                print("✅ PubMed Pipeline initialized (NCBI API)")
            else:
                print("⚠️ PubMed Pipeline: No API key (rate limited)")

    def search(
        self,
        query: str,
        max_results: int = 10,
        sort: str = "relevance"
    ) -> List[str]:
        """Search PubMed and return PMIDs."""
        if not requests:
            return []

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": sort,
            "retmode": "json"
        }

        if self.api_key:
            params["api_key"] = self.api_key

        try:
            response = requests.get(
                f"{self.base_url}/esearch.fcgi",
                params=params,
                timeout=30
            )
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            if self.verbose:
                print(f"⚠️ PubMed search failed: {e}")
            return []

    def fetch_abstracts(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """Fetch abstracts for given PMIDs."""
        if not pmids or not requests:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "abstract",
            "retmode": "xml"
        }

        if self.api_key:
            params["api_key"] = self.api_key

        try:
            response = requests.get(
                f"{self.base_url}/efetch.fcgi",
                params=params,
                timeout=30
            )

            # Parse XML response (simplified)
            articles = self._parse_pubmed_xml(response.text)
            return articles

        except Exception as e:
            if self.verbose:
                print(f"⚠️ PubMed fetch failed: {e}")
            return []

    def _parse_pubmed_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        """Parse PubMed XML response into structured data."""
        import re

        articles = []

        # Extract article blocks
        article_blocks = re.findall(
            r'<PubmedArticle>(.*?)</PubmedArticle>',
            xml_text,
            re.DOTALL
        )

        for block in article_blocks:
            article = {}

            # PMID
            pmid_match = re.search(r'<PMID[^>]*>(\d+)</PMID>', block)
            if pmid_match:
                article["pmid"] = pmid_match.group(1)

            # Title
            title_match = re.search(r'<ArticleTitle>(.+?)</ArticleTitle>', block, re.DOTALL)
            if title_match:
                article["title"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

            # Abstract
            abstract_match = re.search(r'<AbstractText[^>]*>(.+?)</AbstractText>', block, re.DOTALL)
            if abstract_match:
                article["abstract"] = re.sub(r'<[^>]+>', '', abstract_match.group(1)).strip()

            # Journal
            journal_match = re.search(r'<Title>(.+?)</Title>', block)
            if journal_match:
                article["journal"] = journal_match.group(1)

            # Year
            year_match = re.search(r'<PubDate>.*?<Year>(\d{4})</Year>', block, re.DOTALL)
            if year_match:
                article["year"] = year_match.group(1)

            # Authors (first 3)
            authors = re.findall(r'<LastName>(.+?)</LastName>', block)[:3]
            if authors:
                article["authors"] = authors

            if article.get("pmid"):
                articles.append(article)

        return articles

    def query(
        self,
        question: str,
        max_results: int = 10,
        search_type: str = "relevance"
    ) -> Dict[str, Any]:
        """
        Query PubMed for research articles.

        Args:
            question: Search query
            max_results: Number of results to return
            search_type: "relevance" or "date"
        """
        if self.verbose:
            print(f"🔍 Searching PubMed: {question[:50]}...")

        # Search for PMIDs
        pmids = self.search(question, max_results, sort=search_type)

        if not pmids:
            return {
                "source": "pubmed",
                "query": question,
                "articles": [],
                "num_results": 0,
                "timestamp": datetime.now().isoformat()
            }

        # Fetch abstracts
        articles = self.fetch_abstracts(pmids)

        if self.verbose:
            print(f"   Found {len(articles)} articles")

        return {
            "source": "pubmed",
            "query": question,
            "articles": articles,
            "num_results": len(articles),
            "timestamp": datetime.now().isoformat()
        }


class KnowledgePipeline:
    """
    Parallel Knowledge Pipeline

    Queries BOTH in parallel:
    - RAG (textbooks/guidelines from AstraDB)
    - PubMed (latest research via NCBI API)

    Use this BEFORE writing evidence-based content.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.rag = RAGPipeline(verbose=verbose)
        self.pubmed = PubMedPipeline(verbose=verbose)
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY) if OpenAI and OPENAI_API_KEY else None

        if verbose:
            print("=" * 50)
            print("✅ Knowledge Pipeline Ready")
            print("   - RAG: Textbooks & Guidelines")
            print("   - PubMed: Latest Research")
            print("=" * 50)

    def research_parallel(
        self,
        question: str,
        rag_top_k: int = 10,
        pubmed_max: int = 10
    ) -> Dict[str, Any]:
        """
        Run RAG and PubMed pipelines in PARALLEL.

        Returns combined results from:
        - RAG: Textbooks and guidelines from vector store
        - PubMed: Latest research articles
        """
        results = {
            "query": question,
            "timestamp": datetime.now().isoformat(),
            "pipelines": {}
        }

        # Run pipelines in parallel using threads
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                "rag": executor.submit(self.rag.query, question, rag_top_k, False),
                "pubmed": executor.submit(self.pubmed.query, question, pubmed_max)
            }

            for name, future in futures.items():
                try:
                    results["pipelines"][name] = future.result(timeout=60)
                except Exception as e:
                    results["pipelines"][name] = {"error": str(e)}

        # Add summary stats
        results["summary"] = self._summarize_results(results["pipelines"])

        return results

    def _summarize_results(self, pipelines: Dict) -> Dict[str, Any]:
        """Summarize what was found across pipelines."""
        summary = {
            "rag_chunks": 0,
            "pubmed_articles": 0,
            "total_sources": 0
        }

        if "rag" in pipelines:
            rag = pipelines["rag"]
            summary["rag_chunks"] = rag.get("num_results", len(rag.get("chunks", [])))

        if "pubmed" in pipelines:
            pubmed = pipelines["pubmed"]
            summary["pubmed_articles"] = pubmed.get("num_results", len(pubmed.get("articles", [])))

        summary["total_sources"] = summary["rag_chunks"] + summary["pubmed_articles"]

        return summary

    def build_knowledge_context(
        self,
        question: str,
        max_rag_chunks: int = 8,
        max_pubmed_articles: int = 5
    ) -> str:
        """
        Build a unified knowledge context from RAG + PubMed.

        Returns a formatted string ready for use in writing prompts.
        """
        results = self.research_parallel(question, rag_top_k=max_rag_chunks, pubmed_max=max_pubmed_articles)

        context_parts = []

        # RAG Context (Textbooks/Guidelines)
        rag_data = results["pipelines"].get("rag", {})
        chunks = rag_data.get("chunks", [])

        if chunks:
            context_parts.append("## FROM TEXTBOOKS & GUIDELINES (RAG)")
            context_parts.append("-" * 50)

            for i, chunk in enumerate(chunks[:max_rag_chunks], 1):
                source = chunk.get("metadata", {}).get("source", "Unknown")
                page = chunk.get("metadata", {}).get("page", "N/A")
                content = chunk.get("content", "")
                score = chunk.get("rerank_score", 0)

                context_parts.append(f"\n[Source {i}: {source}, Page {page}] (Score: {score:.3f})")
                context_parts.append(content)
                context_parts.append("")

        # PubMed Context (Latest Research)
        pubmed_data = results["pipelines"].get("pubmed", {})
        articles = pubmed_data.get("articles", [])

        if articles:
            context_parts.append("\n## FROM PUBMED (Latest Research)")
            context_parts.append("-" * 50)

            for i, article in enumerate(articles[:max_pubmed_articles], 1):
                pmid = article.get("pmid", "Unknown")
                title = article.get("title", "No title")
                journal = article.get("journal", "Unknown journal")
                year = article.get("year", "N/A")
                authors = article.get("authors", [])
                abstract = article.get("abstract", "No abstract available")

                author_str = ", ".join(authors[:3])
                if len(authors) > 3:
                    author_str += " et al."

                context_parts.append(f"\n[{i}] PMID: {pmid}")
                context_parts.append(f"    {author_str} ({year})")
                context_parts.append(f"    {title}")
                context_parts.append(f"    {journal}")
                context_parts.append(f"    Abstract: {abstract[:500]}...")
                context_parts.append("")

        # Summary
        summary = results.get("summary", {})
        context_parts.append("\n" + "=" * 50)
        context_parts.append("KNOWLEDGE SUMMARY")
        context_parts.append(f"- RAG chunks (textbooks/guidelines): {summary.get('rag_chunks', 0)}")
        context_parts.append(f"- PubMed articles (latest research): {summary.get('pubmed_articles', 0)}")
        context_parts.append(f"- Total sources: {summary.get('total_sources', 0)}")
        context_parts.append("=" * 50)

        return "\n".join(context_parts)

    def synthesize_knowledge(
        self,
        question: str,
        context: str = None
    ) -> str:
        """
        Synthesize knowledge from RAG + PubMed into a coherent brief.

        If context not provided, will run research_parallel first.
        """
        if context is None:
            context = self.build_knowledge_context(question)

        if not self.openai_client:
            return context  # Return raw context if no LLM available

        prompt = f"""You are synthesizing knowledge from textbooks/guidelines (RAG) and latest PubMed research for a cardiologist writing thought leadership content.

QUESTION: {question}

KNOWLEDGE FROM DUAL SOURCES:
{context}

YOUR TASK:
Synthesize this information into a comprehensive, evidence-based knowledge brief.

Structure:
1. **Established Knowledge** (from textbooks/guidelines)
2. **Latest Research** (from PubMed)
3. **Key Data Points** (specific numbers, statistics, trial names)
4. **Areas of Consensus** (where sources agree)
5. **Areas of Uncertainty** (where evidence is evolving)
6. **Citation Summary** (key references to cite)

Rules:
- Prioritize guidelines (RAG) for established recommendations
- Use PubMed for recent updates and emerging evidence
- Note when sources conflict
- Be specific with numbers, statistics, and trial names
- Do NOT add information beyond what sources provide
"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a medical knowledge synthesizer for cardiology content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Synthesis failed: {e}\n\nRaw Context:\n{context}"


def main():
    """Test the knowledge pipeline."""
    print("=" * 60)
    print("Testing Parallel Knowledge Pipeline (RAG + PubMed)")
    print("=" * 60)

    pipeline = KnowledgePipeline(verbose=True)

    test_question = "What are the current LDL cholesterol targets for patients with established cardiovascular disease?"

    print(f"\nQuestion: {test_question}")
    print("-" * 60)

    # Build knowledge context
    print("\n1. Building knowledge context (RAG + PubMed in parallel)...")
    context = pipeline.build_knowledge_context(test_question)
    print(context[:2000] + "..." if len(context) > 2000 else context)

    # Synthesize
    print("\n2. Synthesizing knowledge...")
    synthesis = pipeline.synthesize_knowledge(test_question, context)
    print(synthesis)

    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
