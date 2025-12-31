#!/usr/bin/env python3
"""
Unified RAG Query Interface

Complete end-to-end RAG pipeline:
1. Hybrid retrieval (Vector + BM25 + RRF + Cohere reranking)
2. LLM synthesis
3. Optional save to file

Usage:
    python src/query.py "What are the best practices for X?"
    python src/query.py "Your question" --top-k 15 --save output.json
    python src/query.py "Complex question" --decompose --compress
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import components
try:
    from advanced_retriever import AdvancedRetriever
    from synthesizer import KnowledgeSynthesizer
except ImportError:
    print("❌ Error: Could not import RAG components")
    print("Make sure advanced_retriever.py and synthesizer.py are in the src/ directory")
    sys.exit(1)


class RAGSystem:
    """Complete RAG system for knowledge retrieval and synthesis."""
    
    def __init__(self, verbose: bool = False, use_advanced: bool = True):
        """Initialize the RAG system."""
        self.verbose = verbose
        self.use_advanced = use_advanced
        
        if self.verbose:
            print("🚀 Initializing RAG System...")
            print("=" * 60)
        
        # Initialize retriever
        self.retriever = AdvancedRetriever(verbose=verbose)
        
        # Initialize synthesizer
        self.synthesizer = KnowledgeSynthesizer()
        
        if self.verbose:
            print("=" * 60)
            print("✅ RAG System Ready!\n")
    
    def query(
        self,
        question: str,
        top_k: int = 10,
        save_to: str = None,
        use_multi_query: bool = True,
        use_decomposition: bool = False,
        use_hyde: bool = True,
        use_compression: bool = False,
        skip_synthesis: bool = False
    ) -> dict:
        """
        Query the RAG system with advanced techniques.
        
        Args:
            question: Question to answer
            top_k: Number of chunks to retrieve
            save_to: Optional path to save the result
            use_multi_query: Enable multi-query interrogation
            use_decomposition: Enable query decomposition
            use_hyde: Enable HyDE
            use_compression: Enable contextual compression (slower)
            skip_synthesis: Return only retrieved chunks without synthesis
        
        Returns:
            Dict with synthesis, sources, and metadata
        """
        if self.verbose:
            print(f"\n❓ Question: {question}")
            print("=" * 60)
        
        # Step 1: Advanced hybrid retrieval
        if self.verbose:
            print("\n🔍 Step 1: Advanced Hybrid Retrieval")
            print("-" * 60)
        
        chunks = self.retriever.retrieve(
            question,
            top_k=top_k,
            use_multi_query=use_multi_query,
            use_decomposition=use_decomposition,
            use_hyde=use_hyde,
            use_self_query=True,
            use_compression=use_compression,
            verbose=self.verbose
        )
        
        if not chunks:
            print("⚠️  No relevant information found")
            return {
                "question": question,
                "answer": "No relevant information found in the knowledge base.",
                "sources": [],
                "cost_usd": 0
            }
        
        # Return early if skipping synthesis
        if skip_synthesis:
            return {
                "question": question,
                "chunks": chunks,
                "num_chunks": len(chunks),
                "synthesis_skipped": True
            }
        
        # Step 2: Synthesis
        if self.verbose:
            print(f"\n🔬 Step 2: Knowledge Synthesis")
            print("-" * 60)
        
        result = self.synthesizer.synthesize(question, chunks, verbose=self.verbose)
        
        # Step 3: Save if requested
        if save_to:
            self.synthesizer.save_synthesis(result, save_to)
        
        return result
    
    def display_result(self, result: dict):
        """Display the RAG result in a formatted way."""
        print("\n" + "=" * 60)
        print("📄 KNOWLEDGE BRIEF")
        print("=" * 60)
        print(f"\nQuery: {result.get('query', 'N/A')}")
        print(f"\n{result.get('synthesis', 'No synthesis available')}")
        print("\n" + "=" * 60)
        print("📚 SOURCES USED:")
        print("=" * 60)
        
        for i, source in enumerate(result.get('sources_used', []), 1):
            print(f"{i}. {source.get('source', 'Unknown')}")
            if source.get('year'):
                print(f"   Year: {source['year']}")
            print(f"   Type: {source.get('type', 'unknown')}")
        
        print("\n" + "=" * 60)
        print("💰 COST BREAKDOWN:")
        print("=" * 60)
        tokens = result.get('tokens', {})
        print(f"Input tokens:  {tokens.get('input', 0):,}")
        print(f"Output tokens: {tokens.get('output', 0):,}")
        print(f"Total cost:    ${result.get('cost_usd', 0):.6f}")
        print("=" * 60)
    
    def display_chunks(self, result: dict):
        """Display retrieved chunks without synthesis."""
        print("\n" + "=" * 60)
        print("📚 RETRIEVED CHUNKS")
        print("=" * 60)
        
        for i, chunk in enumerate(result.get('chunks', []), 1):
            print(f"\n{i}. [Score: {chunk.get('rerank_score', 0):.4f}]")
            source = chunk.get('metadata', {}).get('source', 'Unknown')
            page = chunk.get('metadata', {}).get('page', 'N/A')
            print(f"   Source: {source}, Page: {page}")
            print(f"   Content: {chunk['content'][:200]}...")
            print("-" * 60)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Query the RAG system for knowledge synthesis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/query.py "What is machine learning?"
  python src/query.py "Complex topic" --decompose
  python src/query.py "Question" --top-k 15 --save result.json
  python src/query.py "Question" --chunks-only
        """
    )
    
    parser.add_argument(
        "query",
        type=str,
        help="Question to answer"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of chunks to retrieve (default: 10)"
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Path to save the result (JSON)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output (just the synthesis)"
    )
    parser.add_argument(
        "--no-multi-query",
        action="store_true",
        help="Disable multi-query interrogation"
    )
    parser.add_argument(
        "--decompose",
        action="store_true",
        help="Enable query decomposition (for complex queries)"
    )
    parser.add_argument(
        "--no-hyde",
        action="store_true",
        help="Disable HyDE (hypothetical document embeddings)"
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Enable contextual compression (slower but better)"
    )
    parser.add_argument(
        "--chunks-only",
        action="store_true",
        help="Return only retrieved chunks without synthesis"
    )
    
    args = parser.parse_args()
    
    # Initialize RAG system
    rag = RAGSystem(verbose=not args.quiet)
    
    # Query with advanced options
    result = rag.query(
        question=args.query,
        top_k=args.top_k,
        save_to=args.save,
        use_multi_query=not args.no_multi_query,
        use_decomposition=args.decompose,
        use_hyde=not args.no_hyde,
        use_compression=args.compress,
        skip_synthesis=args.chunks_only
    )
    
    # Display result
    if args.quiet:
        if args.chunks_only:
            for chunk in result.get('chunks', []):
                print(f"---\n{chunk['content']}\n")
        else:
            print(result.get('synthesis', 'No synthesis available'))
    else:
        if args.chunks_only:
            rag.display_chunks(result)
        else:
            rag.display_result(result)


if __name__ == "__main__":
    main()
