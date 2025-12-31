"""
Dual Research Pipeline - PubMed + AstraDB RAG
"""

import asyncio
from dataclasses import dataclass
from typing import Optional

from .harvester import ContentIdea
from .utils.pubmed import pubmed_client, PubMedArticle
from .utils.astradb import astradb_client, RAGResult


@dataclass
class ResearchResults:
    """Combined research results from both pipelines."""
    idea: ContentIdea
    pubmed_articles: list[PubMedArticle]
    rag_results: list[RAGResult]

    @property
    def has_pubmed_results(self) -> bool:
        return len(self.pubmed_articles) > 0

    @property
    def has_rag_results(self) -> bool:
        return len(self.rag_results) > 0

    @property
    def total_sources(self) -> int:
        return len(self.pubmed_articles) + len(self.rag_results)

    def get_pubmed_summary(self) -> str:
        """Get summary of PubMed results."""
        if not self.pubmed_articles:
            return "No PubMed articles found."

        lines = []
        for i, article in enumerate(self.pubmed_articles[:5], 1):
            q1_marker = "[Q1] " if article.is_q1_journal else ""
            lines.append(f"{i}. {q1_marker}{article.get_citation()}")
            lines.append(f"   Title: {article.title[:100]}...")
        return "\n".join(lines)

    def get_rag_summary(self) -> str:
        """Get summary of RAG results."""
        if not self.rag_results:
            return "No guideline/textbook content found."

        lines = []
        for i, result in enumerate(self.rag_results[:5], 1):
            lines.append(f"{i}. [{result.source_type.upper()}] {result.source_name}")
            if result.chapter:
                lines.append(f"   Chapter: {result.chapter}")
            lines.append(f"   Similarity: {result.similarity:.2%}")
        return "\n".join(lines)


class DualResearcher:
    """
    Executes parallel research pipelines:
    1. PubMed - Q1 journal literature search
    2. AstraDB RAG - Guidelines and textbook search
    """

    def __init__(self):
        self.pubmed = pubmed_client
        self.astradb = astradb_client

    async def research(
        self,
        idea: ContentIdea,
        pubmed_max_results: int = 10,
        rag_top_k: int = 8,
    ) -> ResearchResults:
        """
        Execute parallel research on an idea.

        Args:
            idea: The content idea to research
            pubmed_max_results: Max PubMed results
            rag_top_k: Max RAG results

        Returns:
            Combined ResearchResults
        """
        # Run both pipelines in parallel
        pubmed_task = self.search_pubmed(idea, max_results=pubmed_max_results)
        rag_task = self.search_rag(idea, top_k=rag_top_k)

        pubmed_articles, rag_results = await asyncio.gather(
            pubmed_task,
            rag_task,
            return_exceptions=True,
        )

        # Handle exceptions gracefully
        if isinstance(pubmed_articles, Exception):
            print(f"PubMed search error: {pubmed_articles}")
            pubmed_articles = []

        if isinstance(rag_results, Exception):
            print(f"RAG search error: {rag_results}")
            rag_results = []

        return ResearchResults(
            idea=idea,
            pubmed_articles=pubmed_articles,
            rag_results=rag_results,
        )

    async def search_pubmed(
        self,
        idea: ContentIdea,
        max_results: int = 10,
    ) -> list[PubMedArticle]:
        """
        Search PubMed for relevant Q1 journal articles.

        Args:
            idea: Content idea with pubmed_query
            max_results: Maximum results to return

        Returns:
            List of PubMedArticle objects
        """
        print(f"Searching PubMed: {idea.pubmed_query[:60]}...")

        articles = await self.pubmed.search_and_fetch(
            query=idea.pubmed_query,
            max_results=max_results,
            filter_q1_journals=True,
        )

        # Sort by Q1 status and recency
        articles.sort(
            key=lambda a: (a.is_q1_journal, a.year or "0000"),
            reverse=True,
        )

        print(f"Found {len(articles)} PubMed articles ({sum(1 for a in articles if a.is_q1_journal)} from Q1 journals)")
        return articles

    async def search_rag(
        self,
        idea: ContentIdea,
        top_k: int = 8,
    ) -> list[RAGResult]:
        """
        Search AstraDB for relevant guidelines and textbook content.

        Args:
            idea: Content idea with rag_keywords
            top_k: Number of results to return

        Returns:
            List of RAGResult objects
        """
        # Build query from research question and keywords
        query = f"{idea.research_question} {' '.join(idea.rag_keywords)}"
        print(f"Searching knowledge base: {query[:60]}...")

        # Use multi-query with variations for better coverage
        queries = [
            idea.research_question,
            " ".join(idea.rag_keywords),
            f"guidelines {idea.topic_category} {idea.rag_keywords[0] if idea.rag_keywords else ''}",
        ]

        results = await self.astradb.multi_query(
            queries=queries,
            top_k=top_k,
        )

        # Separate guidelines and textbook results
        guidelines = [r for r in results if r.source_type == "guideline"]
        textbooks = [r for r in results if r.source_type == "textbook"]

        print(f"Found {len(guidelines)} guideline chunks, {len(textbooks)} textbook chunks")
        return results

    async def research_multiple(
        self,
        ideas: list[ContentIdea],
    ) -> list[ResearchResults]:
        """
        Research multiple ideas in parallel.

        Args:
            ideas: List of content ideas

        Returns:
            List of ResearchResults
        """
        tasks = [self.research(idea) for idea in ideas]
        return await asyncio.gather(*tasks)


# Factory function
def create_researcher() -> DualResearcher:
    return DualResearcher()
