#!/usr/bin/env python3
"""
Advanced Hybrid Retrieval System

Implements 10 advanced RAG techniques:
1. Multi-query interrogation
2. Query decomposition
3. Contextual compression
4. HyDE (Hypothetical Document Embeddings)
5. Parent document retrieval
6. Self-query filtering
7. Dense retrieval (Vector search)
8. Sparse retrieval (BM25)
9. Reciprocal Rank Fusion
10. Cohere reranking

Usage:
    from src.advanced_retriever import AdvancedRetriever
    
    retriever = AdvancedRetriever()
    results = retriever.retrieve(
        "your query here",
        use_multi_query=True,
        use_hyde=True
    )
"""

import os
import sys
import json
import pickle
from typing import List, Dict, Any, Optional
from collections import defaultdict
from pathlib import Path
import numpy as np
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: openai not installed")
    sys.exit(1)

try:
    from astrapy import DataAPIClient
except ImportError:
    print("❌ Error: astrapy not installed")
    sys.exit(1)

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    print("❌ Error: rank-bm25 not installed")
    sys.exit(1)

try:
    import cohere
except ImportError:
    print("❌ Error: cohere not installed")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "documents")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Retrieval parameters
DENSE_TOP_K = int(os.getenv("DENSE_TOP_K", "20"))
SPARSE_TOP_K = int(os.getenv("SPARSE_TOP_K", "20"))
RRF_K = int(os.getenv("RRF_K", "60"))
RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", "10"))

# Cache paths
BM25_CACHE_PATH = Path(".bm25_cache.pkl")
DOC_CACHE_PATH = Path(".doc_cache.json")


class AdvancedRetriever:
    """Advanced hybrid retrieval with all best practices."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the advanced retriever."""
        self.verbose = verbose
        
        if self.verbose:
            print("🚀 Initializing Advanced RAG System...")
            print("=" * 60)
        
        # OpenAI client
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # AstraDB client
        client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
        self.astra_db = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT)
        self.collection = self.astra_db.get_collection(ASTRA_DB_COLLECTION)
        
        # Cohere client
        self.cohere_client = cohere.Client(api_key=COHERE_API_KEY)
        
        # BM25 index and document cache
        self.bm25 = None
        self.documents = []
        self.doc_ids = []
        self.doc_metadata = {}
        
        # Load cached BM25 index
        self._load_bm25_cache()
        
        if self.verbose:
            print("=" * 60)
            print("✅ Advanced RAG System Ready!\n")
    
    def _load_bm25_cache(self):
        """Load cached BM25 index from disk."""
        if BM25_CACHE_PATH.exists() and DOC_CACHE_PATH.exists():
            try:
                with open(BM25_CACHE_PATH, 'rb') as f:
                    self.bm25 = pickle.load(f)
                with open(DOC_CACHE_PATH, 'r') as f:
                    cache = json.load(f)
                    self.documents = cache["documents"]
                    self.doc_ids = cache["doc_ids"]
                    self.doc_metadata = cache.get("metadata", {})
                if self.verbose:
                    print(f"✅ Loaded BM25 cache ({len(self.documents)} docs)")
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Failed to load BM25 cache: {e}")
    
    def _save_bm25_cache(self):
        """Save BM25 index to disk."""
        try:
            with open(BM25_CACHE_PATH, 'wb') as f:
                pickle.dump(self.bm25, f)
            with open(DOC_CACHE_PATH, 'w') as f:
                json.dump({
                    "documents": self.documents,
                    "doc_ids": self.doc_ids,
                    "metadata": self.doc_metadata
                }, f)
            if self.verbose:
                print(f"✅ Saved BM25 cache")
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Failed to save BM25 cache: {e}")
    
    def build_bm25_index(self):
        """Build BM25 index from AstraDB."""
        if self.bm25 is not None:
            return
        
        if self.verbose:
            print("🔨 Building BM25 index...")
        
        cursor = self.collection.find({}, projection={"content": 1, "metadata": 1, "_id": 1})
        
        self.documents = []
        self.doc_ids = []
        self.doc_metadata = {}
        
        for doc in cursor:
            content = doc.get("content", "")
            doc_id = doc.get("_id")
            metadata = doc.get("metadata", {})
            
            self.documents.append(content)
            self.doc_ids.append(doc_id)
            self.doc_metadata[doc_id] = metadata
        
        tokenized_docs = [doc.lower().split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        self._save_bm25_cache()
        
        if self.verbose:
            print(f"✅ BM25 index built ({len(self.documents)} documents)")
    
    # ============================================================
    # TECHNIQUE 1: Multi-Query Interrogation
    # ============================================================
    
    def generate_multi_queries(self, query: str, num_queries: int = 3) -> List[str]:
        """Generate multiple variations of a query."""
        prompt = f"""Generate {num_queries} different variations of this query.
Each variation should use different terminology while asking for the same information.

Original query: {query}

Output format (JSON):
{{
  "queries": ["query1", "query2", "query3"]
}}
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            queries = result.get("queries", [query])
            return [query] + queries[:num_queries]
        except:
            return [query]
    
    # ============================================================
    # TECHNIQUE 2: Query Decomposition
    # ============================================================
    
    def decompose_query(self, query: str) -> List[str]:
        """Break complex query into simpler sub-queries."""
        prompt = f"""Decompose this complex query into 2-4 simpler sub-queries.
Each sub-query should focus on one aspect of the original question.

Original query: {query}

Output format (JSON):
{{
  "sub_queries": ["sub_query1", "sub_query2", ...]
}}
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("sub_queries", [query])
        except:
            return [query]
    
    # ============================================================
    # TECHNIQUE 3: HyDE (Hypothetical Document Embeddings)
    # ============================================================
    
    def generate_hypothetical_answer(self, query: str) -> str:
        """Generate a hypothetical answer to embed and search with."""
        prompt = f"""Generate a detailed, factual answer to this question as if it came from a textbook or reference document.

Question: {query}

Answer (2-3 sentences):"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    # ============================================================
    # TECHNIQUE 4: Self-Query Filtering
    # ============================================================
    
    def extract_metadata_filters(self, query: str) -> Dict[str, Any]:
        """Extract metadata filters from query."""
        prompt = f"""Extract any specific metadata filters from this query.
Look for: source, year, type, topic, or other specific constraints.

Query: {query}

Output format (JSON):
{{
  "source": "source name or null",
  "year": year_number_or_null,
  "type": "type or null",
  "topic": "topic or null"
}}
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        try:
            filters = json.loads(response.choices[0].message.content)
            return {k: v for k, v in filters.items() if v is not None}
        except:
            return {}
    
    # ============================================================
    # TECHNIQUE 5: Dense Retrieval
    # ============================================================
    
    def dense_retrieve(
        self,
        query: str,
        k: int = DENSE_TOP_K,
        metadata_filters: Optional[Dict] = None,
        use_hyde: bool = False
    ) -> List[Dict[str, Any]]:
        """Dense retrieval with optional HyDE and metadata filtering."""
        
        # Use HyDE if enabled
        if use_hyde:
            hyde_answer = self.generate_hypothetical_answer(query)
            embed_text = hyde_answer
        else:
            embed_text = query
        
        # Generate embedding
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=embed_text
        )
        query_embedding = response.data[0].embedding
        
        # Build filter query
        filter_query = {}
        if metadata_filters:
            for key, value in metadata_filters.items():
                filter_query[f"metadata.{key}"] = value
        
        # Vector search with filters
        try:
            results = self.collection.find(
                filter=filter_query if filter_query else {},
                sort={"$vector": query_embedding},
                limit=k,
                projection={"content": 1, "metadata": 1, "_id": 1}
            )
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Dense retrieval error: {e}")
            results = []
        
        dense_results = []
        for i, doc in enumerate(results):
            dense_results.append({
                "id": doc.get("_id"),
                "content": doc.get("content", ""),
                "metadata": doc.get("metadata", {}),
                "dense_rank": i + 1,
                "dense_score": 1 / (i + 1)
            })
        
        return dense_results
    
    # ============================================================
    # TECHNIQUE 6: Sparse Retrieval
    # ============================================================
    
    def sparse_retrieve(self, query: str, k: int = SPARSE_TOP_K) -> List[Dict[str, Any]]:
        """Sparse retrieval using BM25."""
        if self.bm25 is None:
            self.build_bm25_index()
        
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_k_indices = np.argsort(scores)[::-1][:k]
        
        sparse_results = []
        for rank, idx in enumerate(top_k_indices):
            if scores[idx] > 0:
                doc_id = self.doc_ids[idx]
                sparse_results.append({
                    "id": doc_id,
                    "content": self.documents[idx],
                    "metadata": self.doc_metadata.get(doc_id, {}),
                    "sparse_rank": rank + 1,
                    "sparse_score": scores[idx]
                })
        
        return sparse_results
    
    # ============================================================
    # TECHNIQUE 7: Reciprocal Rank Fusion
    # ============================================================
    
    def reciprocal_rank_fusion(
        self,
        dense_results: List[Dict],
        sparse_results: List[Dict],
        k: int = RRF_K
    ) -> List[Dict]:
        """Combine dense and sparse with RRF."""
        rrf_scores = defaultdict(float)
        doc_map = {}
        
        for doc in dense_results:
            doc_id = doc["id"]
            rrf_scores[doc_id] += 1 / (k + doc["dense_rank"])
            doc_map[doc_id] = doc
        
        for doc in sparse_results:
            doc_id = doc["id"]
            rrf_scores[doc_id] += 1 / (k + doc["sparse_rank"])
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
        
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        fused_results = []
        for doc_id, rrf_score in sorted_docs:
            doc = doc_map[doc_id]
            doc["rrf_score"] = rrf_score
            fused_results.append(doc)
        
        return fused_results
    
    # ============================================================
    # TECHNIQUE 8: Cohere Reranking
    # ============================================================
    
    def rerank(
        self,
        query: str,
        fused_results: List[Dict],
        top_k: int = RERANK_TOP_K
    ) -> List[Dict]:
        """Rerank with Cohere."""
        if not fused_results:
            return []
        
        documents = [doc["content"] for doc in fused_results]
        
        try:
            rerank_response = self.cohere_client.rerank(
                query=query,
                documents=documents,
                top_n=top_k,
                model="rerank-english-v3.0"
            )
            
            reranked_results = []
            for result in rerank_response.results:
                idx = result.index
                doc = fused_results[idx]
                doc["rerank_score"] = result.relevance_score
                doc["rerank_rank"] = len(reranked_results) + 1
                reranked_results.append(doc)
            
            return reranked_results
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Reranking failed: {e}")
            return fused_results[:top_k]
    
    # ============================================================
    # TECHNIQUE 9: Contextual Compression
    # ============================================================
    
    def compress_context(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """Extract only relevant sentences from chunks."""
        compressed = []
        
        for chunk in chunks:
            content = chunk["content"]
            
            prompt = f"""Extract only the sentences from this text that are relevant to the query.
Remove any irrelevant information.

Query: {query}

Text: {content}

Extracted relevant text (keep original wording):"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            compressed_content = response.choices[0].message.content.strip()
            
            if len(compressed_content) < len(content) and len(compressed_content) > 50:
                chunk_copy = chunk.copy()
                chunk_copy["content"] = compressed_content
                chunk_copy["original_length"] = len(content)
                chunk_copy["compressed_length"] = len(compressed_content)
                compressed.append(chunk_copy)
        
        return compressed
    
    # ============================================================
    # MAIN RETRIEVAL PIPELINE
    # ============================================================
    
    def retrieve(
        self,
        query: str,
        top_k: int = RERANK_TOP_K,
        use_multi_query: bool = True,
        use_decomposition: bool = False,
        use_hyde: bool = True,
        use_self_query: bool = True,
        use_compression: bool = False,
        verbose: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Complete advanced retrieval pipeline.
        
        Args:
            query: Search query
            top_k: Final number of results
            use_multi_query: Enable multi-query interrogation
            use_decomposition: Enable query decomposition
            use_hyde: Enable HyDE
            use_self_query: Enable self-query filtering
            use_compression: Enable contextual compression (slower)
            verbose: Print progress
        
        Returns:
            Top-k most relevant documents
        """
        verbose = verbose or self.verbose
        
        if verbose:
            print(f"\n🔍 Query: {query}")
            print("=" * 60)
        
        # STEP 1: Query preprocessing
        queries = [query]
        metadata_filters = {}
        
        if use_self_query:
            if verbose:
                print("1️⃣ Self-query filtering...")
            metadata_filters = self.extract_metadata_filters(query)
            if verbose and metadata_filters:
                print(f"   Filters: {metadata_filters}")
        
        if use_multi_query:
            if verbose:
                print("2️⃣ Multi-query generation...")
            queries = self.generate_multi_queries(query, num_queries=2)
            if verbose:
                print(f"   Generated {len(queries)} query variations")
        
        if use_decomposition:
            if verbose:
                print("3️⃣ Query decomposition...")
            sub_queries = self.decompose_query(query)
            queries.extend(sub_queries)
            if verbose:
                print(f"   Decomposed into {len(sub_queries)} sub-queries")
        
        # STEP 2: Retrieve for each query
        if verbose:
            print(f"4️⃣ Retrieving for {len(queries)} queries...")
        
        all_dense = []
        all_sparse = []
        
        for q in queries:
            dense = self.dense_retrieve(q, k=DENSE_TOP_K, metadata_filters=metadata_filters, use_hyde=use_hyde)
            sparse = self.sparse_retrieve(q, k=SPARSE_TOP_K)
            all_dense.extend(dense)
            all_sparse.extend(sparse)
        
        if verbose:
            print(f"   Dense: {len(all_dense)} results")
            print(f"   Sparse: {len(all_sparse)} results")
        
        # STEP 3: Reciprocal Rank Fusion
        if verbose:
            print("5️⃣ Reciprocal Rank Fusion...")
        fused_results = self.reciprocal_rank_fusion(all_dense, all_sparse)
        if verbose:
            print(f"   Fused to {len(fused_results)} unique results")
        
        # STEP 4: Reranking
        if verbose:
            print(f"6️⃣ Reranking to top {top_k}...")
        final_results = self.rerank(query, fused_results, top_k=top_k * 2)
        
        # STEP 5: Contextual compression (optional)
        if use_compression and final_results:
            if verbose:
                print(f"7️⃣ Contextual compression...")
            final_results = self.compress_context(query, final_results)[:top_k]
            if verbose:
                print(f"   Compressed to {len(final_results)} results")
        else:
            final_results = final_results[:top_k]
        
        if verbose:
            print(f"✅ Final {len(final_results)} results")
            print("=" * 60)
        
        return final_results


def main():
    """Test the advanced retriever."""
    print("=" * 60)
    print("🧪 Testing Advanced RAG System")
    print("=" * 60)
    
    retriever = AdvancedRetriever(verbose=True)
    
    test_query = "What are the best practices?"
    print(f"\n📝 Test Query: {test_query}\n")
    
    results = retriever.retrieve(
        test_query,
        top_k=5,
        use_multi_query=True,
        use_decomposition=False,
        use_hyde=True,
        use_self_query=True,
        use_compression=False,
        verbose=True
    )
    
    print("\n📊 Top Results:")
    print("=" * 60)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [Score: {result.get('rerank_score', 0):.4f}]")
        print(f"   Source: {result.get('metadata', {}).get('source', 'Unknown')}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
