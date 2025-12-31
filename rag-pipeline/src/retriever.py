#!/usr/bin/env python3
"""
Hybrid Retriever

Implements a 4-layer retrieval system:
1. Dense retrieval (Vector search via AstraDB)
2. Sparse retrieval (BM25 keyword matching)
3. Reciprocal Rank Fusion (RRF) to combine results
4. Cohere reranking for final top-k selection

Usage:
    from src.retriever import HybridRetriever
    
    retriever = HybridRetriever()
    results = retriever.retrieve("your query here", top_k=10)
"""

import os
import sys
from typing import List, Dict, Any
from collections import defaultdict
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


class HybridRetriever:
    """Hybrid retrieval combining dense, sparse, and reranking."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the retriever with all necessary clients."""
        self.verbose = verbose
        
        if self.verbose:
            print("🔧 Initializing Hybrid Retriever...")
        
        # OpenAI client for embeddings
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # AstraDB client for vector search
        client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
        self.astra_db = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT)
        self.collection = self.astra_db.get_collection(ASTRA_DB_COLLECTION)
        
        # Cohere client for reranking
        self.cohere_client = cohere.Client(api_key=COHERE_API_KEY)
        
        # BM25 index (built on first query)
        self.bm25 = None
        self.documents = []
        self.doc_ids = []
        self.doc_metadata = {}
        
        if self.verbose:
            print("✅ Hybrid Retriever initialized")
    
    def build_bm25_index(self):
        """Build BM25 index from all documents in AstraDB."""
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
        
        if self.verbose:
            print(f"✅ BM25 index built ({len(self.documents)} documents)")
    
    def dense_retrieve(self, query: str, k: int = DENSE_TOP_K) -> List[Dict[str, Any]]:
        """Dense retrieval using vector similarity search."""
        # Generate query embedding
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
        query_embedding = response.data[0].embedding
        
        # Vector search in AstraDB
        results = self.collection.find(
            {},
            sort={"$vector": query_embedding},
            limit=k,
            projection={"content": 1, "metadata": 1, "_id": 1}
        )
        
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
    
    def sparse_retrieve(self, query: str, k: int = SPARSE_TOP_K) -> List[Dict[str, Any]]:
        """Sparse retrieval using BM25 keyword matching."""
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
    
    def reciprocal_rank_fusion(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]],
        k: int = RRF_K
    ) -> List[Dict[str, Any]]:
        """Combine dense and sparse results using Reciprocal Rank Fusion."""
        # RRF formula: score = sum(1 / (k + rank))
        rrf_scores = defaultdict(float)
        doc_map = {}
        
        for doc in dense_results:
            doc_id = doc["id"]
            rank = doc["dense_rank"]
            rrf_scores[doc_id] += 1 / (k + rank)
            doc_map[doc_id] = doc
        
        for doc in sparse_results:
            doc_id = doc["id"]
            rank = doc["sparse_rank"]
            rrf_scores[doc_id] += 1 / (k + rank)
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
        
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        fused_results = []
        for doc_id, rrf_score in sorted_docs:
            doc = doc_map[doc_id]
            doc["rrf_score"] = rrf_score
            fused_results.append(doc)
        
        return fused_results
    
    def rerank(
        self,
        query: str,
        fused_results: List[Dict[str, Any]],
        top_k: int = RERANK_TOP_K
    ) -> List[Dict[str, Any]]:
        """Rerank results using Cohere's reranking model."""
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
    
    def retrieve(
        self,
        query: str,
        top_k: int = RERANK_TOP_K,
        use_reranking: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Full hybrid retrieval pipeline.
        
        Args:
            query: The search query
            top_k: Number of final results to return
            use_reranking: Whether to use Cohere reranking
        
        Returns:
            List of top-k most relevant documents with metadata
        """
        if self.verbose:
            print(f"\n🔍 Query: {query}")
            print("=" * 60)
        
        # Step 1: Dense retrieval
        if self.verbose:
            print("1️⃣ Dense retrieval (Vector search)...")
        dense_results = self.dense_retrieve(query, k=DENSE_TOP_K)
        if self.verbose:
            print(f"   Found {len(dense_results)} results")
        
        # Step 2: Sparse retrieval
        if self.verbose:
            print("2️⃣ Sparse retrieval (BM25)...")
        sparse_results = self.sparse_retrieve(query, k=SPARSE_TOP_K)
        if self.verbose:
            print(f"   Found {len(sparse_results)} results")
        
        # Step 3: Reciprocal Rank Fusion
        if self.verbose:
            print("3️⃣ Reciprocal Rank Fusion...")
        fused_results = self.reciprocal_rank_fusion(dense_results, sparse_results)
        if self.verbose:
            print(f"   Combined to {len(fused_results)} unique results")
        
        # Step 4: Reranking (optional)
        if use_reranking:
            if self.verbose:
                print(f"4️⃣ Reranking to top {top_k}...")
            final_results = self.rerank(query, fused_results, top_k=top_k)
        else:
            final_results = fused_results[:top_k]
        
        if self.verbose:
            print(f"✅ Final {len(final_results)} results")
            print("=" * 60)
        
        return final_results


def main():
    """Test the hybrid retriever."""
    print("=" * 60)
    print("🧪 Testing Hybrid Retriever")
    print("=" * 60)
    
    retriever = HybridRetriever(verbose=True)
    
    test_query = "What are the best practices?"
    print(f"\n📝 Test Query: {test_query}\n")
    
    results = retriever.retrieve(test_query, top_k=5)
    
    print("\n📊 Top Results:")
    print("=" * 60)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [Score: {result.get('rerank_score', 0):.4f}]")
        print(f"   Source: {result.get('metadata', {}).get('source', 'Unknown')}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
