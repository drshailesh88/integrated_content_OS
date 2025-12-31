"""
AstraDB client for RAG queries against the medical knowledge base.
Uses HyDE (Hypothetical Document Embedding) for improved retrieval.
"""

from dataclasses import dataclass
from typing import Optional
import httpx

from ..config import config
from .llm import llm_client


@dataclass
class RAGResult:
    """Represents a RAG retrieval result."""
    content: str
    source_name: str
    source_type: str  # "guideline" or "textbook"
    chapter: Optional[str] = None
    section: Optional[str] = None
    similarity: float = 0.0

    def get_citation(self) -> str:
        """Generate citation string."""
        parts = [self.source_name]
        if self.chapter:
            parts.append(f"Chapter: {self.chapter}")
        if self.section:
            parts.append(f"Section: {self.section}")
        return " | ".join(parts)


class AstraDBClient:
    """
    Client for AstraDB vector database queries.
    Uses the medical_knowledge collection with pre-ingested guidelines and textbooks.
    """

    def __init__(self):
        self.config = config.astradb
        self.llm = llm_client

    def _get_headers(self) -> dict:
        """Get headers for AstraDB API requests."""
        return {
            "Token": self.config.application_token,
            "Content-Type": "application/json",
        }

    def _get_base_url(self) -> str:
        """Get base URL for the collection."""
        return f"{self.config.api_endpoint}/api/json/v1/default_keyspace/{self.config.collection_name}"

    async def generate_hyde_document(self, query: str) -> str:
        """
        Generate a hypothetical document that would answer the query.
        This improves retrieval by matching against expected answer style.

        Args:
            query: The search query

        Returns:
            Hypothetical document text
        """
        system_prompt = """You are a medical knowledge expert specializing in cardiology.
Given a query, generate a hypothetical passage that would perfectly answer it.
Write in the style of medical guidelines (ACC/ESC/ADA) or textbook content.
Be specific, include typical guideline language like class/level of evidence.
Keep the response under 200 words."""

        prompt = f"""Generate a hypothetical medical guideline or textbook passage that would answer this query:

Query: {query}

Write a passage that sounds like it came from ACC/ESC guidelines or a cardiology textbook."""

        return await self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=300,
            temperature=0.3,
        )

    async def query(
        self,
        query: str,
        use_hyde: bool = True,
        top_k: Optional[int] = None,
        filter_source_type: Optional[str] = None,
    ) -> list[RAGResult]:
        """
        Query the medical knowledge base using vector similarity search.

        Args:
            query: Search query
            use_hyde: Use HyDE for improved retrieval
            top_k: Number of results to return
            filter_source_type: Filter by "guideline" or "textbook"

        Returns:
            List of RAGResult objects
        """
        top_k = top_k or self.config.top_k

        # Generate embedding
        if use_hyde:
            hyde_doc = await self.generate_hyde_document(query)
            embed_text = f"{query}\n\n{hyde_doc}"
        else:
            embed_text = query

        embedding = await self.llm.get_embedding(embed_text)

        # Build query payload
        payload = {
            "find": {
                "sort": {"$vector": embedding},
                "options": {
                    "limit": top_k,
                    "includeSimilarity": True,
                },
            }
        }

        # Add filter if specified
        if filter_source_type:
            payload["find"]["filter"] = {"source_type": filter_source_type}

        # Execute query
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self._get_base_url(),
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        # Parse results
        results = []
        for doc in data.get("data", {}).get("documents", []):
            similarity = doc.get("$similarity", 0.0)

            # Skip low-similarity results
            if similarity < self.config.similarity_threshold:
                continue

            results.append(RAGResult(
                content=doc.get("content", doc.get("text", "")),
                source_name=doc.get("source_name", "Unknown"),
                source_type=doc.get("source_type", "unknown"),
                chapter=doc.get("chapter"),
                section=doc.get("section"),
                similarity=similarity,
            ))

        return results

    async def query_guidelines(self, query: str, top_k: int = 5) -> list[RAGResult]:
        """Query only guideline documents (ACC/ESC/ADA)."""
        return await self.query(
            query=query,
            top_k=top_k,
            filter_source_type="guideline",
        )

    async def query_textbooks(self, query: str, top_k: int = 5) -> list[RAGResult]:
        """Query only textbook documents."""
        return await self.query(
            query=query,
            top_k=top_k,
            filter_source_type="textbook",
        )

    async def multi_query(
        self,
        queries: list[str],
        top_k: int = 5,
    ) -> list[RAGResult]:
        """
        Execute multiple queries and merge results using reciprocal rank fusion.

        Args:
            queries: List of query variations
            top_k: Results per query

        Returns:
            Merged and deduplicated results
        """
        all_results = []
        seen_content = set()

        for query in queries:
            results = await self.query(query=query, top_k=top_k)
            for result in results:
                # Deduplicate by content hash
                content_hash = hash(result.content[:100])
                if content_hash not in seen_content:
                    seen_content.add(content_hash)
                    all_results.append(result)

        # Sort by similarity
        all_results.sort(key=lambda x: x.similarity, reverse=True)
        return all_results[:top_k]


# Singleton instance
astradb_client = AstraDBClient()
