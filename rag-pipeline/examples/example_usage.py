#!/usr/bin/env python3
"""
Example Usage Patterns for Portable RAG System

This file demonstrates various ways to use the RAG system.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()


def example_basic_query():
    """Basic query with default settings."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Query")
    print("=" * 60)
    
    from query import RAGSystem
    
    rag = RAGSystem(verbose=True)
    result = rag.query("What is machine learning?")
    rag.display_result(result)


def example_advanced_query():
    """Advanced query with all techniques enabled."""
    print("\n" + "=" * 60)
    print("Example 2: Advanced Query (All Techniques)")
    print("=" * 60)
    
    from query import RAGSystem
    
    rag = RAGSystem(verbose=True)
    result = rag.query(
        question="What are the best practices for training neural networks?",
        top_k=15,
        use_multi_query=True,
        use_decomposition=True,  # Break into sub-queries
        use_hyde=True,           # Hypothetical document embeddings
        use_compression=True     # Contextual compression
    )
    rag.display_result(result)


def example_retrieval_only():
    """Get only retrieved chunks without synthesis."""
    print("\n" + "=" * 60)
    print("Example 3: Retrieval Only (No Synthesis)")
    print("=" * 60)
    
    from advanced_retriever import AdvancedRetriever
    
    retriever = AdvancedRetriever(verbose=True)
    chunks = retriever.retrieve(
        "What is deep learning?",
        top_k=5,
        use_multi_query=True,
        use_hyde=True
    )
    
    print("\nRetrieved Chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n{i}. Score: {chunk.get('rerank_score', 0):.4f}")
        print(f"   {chunk['content'][:200]}...")


def example_custom_synthesis():
    """Use custom synthesis prompt."""
    print("\n" + "=" * 60)
    print("Example 4: Custom Synthesis Prompt")
    print("=" * 60)
    
    from advanced_retriever import AdvancedRetriever
    from synthesizer import KnowledgeSynthesizer
    
    # Custom prompt for Q&A style output
    custom_prompt = """Based on the following sources, answer the question in a clear, concise manner.

Question: {query}

Sources:
{chunks}

Answer (2-3 paragraphs, cite sources):"""
    
    retriever = AdvancedRetriever()
    synthesizer = KnowledgeSynthesizer(custom_prompt=custom_prompt)
    
    chunks = retriever.retrieve("What are embeddings?", top_k=5)
    result = synthesizer.synthesize("What are embeddings?", chunks, verbose=True)
    
    print("\nSynthesis:")
    print(result["synthesis"])


def example_save_results():
    """Save results to JSON file."""
    print("\n" + "=" * 60)
    print("Example 5: Save Results to File")
    print("=" * 60)
    
    from query import RAGSystem
    
    rag = RAGSystem(verbose=False)
    result = rag.query(
        "What is transfer learning?",
        save_to="output_example.json"
    )
    
    print(f"Results saved to output_example.json")
    print(f"Cost: ${result.get('cost_usd', 0):.6f}")


def example_batch_queries():
    """Process multiple queries."""
    print("\n" + "=" * 60)
    print("Example 6: Batch Queries")
    print("=" * 60)
    
    from query import RAGSystem
    
    queries = [
        "What is supervised learning?",
        "What is unsupervised learning?",
        "What is reinforcement learning?"
    ]
    
    rag = RAGSystem(verbose=False)
    
    total_cost = 0
    for query in queries:
        result = rag.query(query, top_k=5)
        total_cost += result.get('cost_usd', 0)
        print(f"✓ {query[:40]}... (${result.get('cost_usd', 0):.6f})")
    
    print(f"\nTotal cost for {len(queries)} queries: ${total_cost:.6f}")


def example_direct_components():
    """Use components directly for maximum control."""
    print("\n" + "=" * 60)
    print("Example 7: Direct Component Usage")
    print("=" * 60)
    
    from retriever import HybridRetriever
    from synthesizer import KnowledgeSynthesizer
    
    # Use basic retriever
    retriever = HybridRetriever(verbose=True)
    
    # Retrieve with basic hybrid search
    chunks = retriever.retrieve(
        "What is gradient descent?",
        top_k=5,
        use_reranking=True
    )
    
    # Synthesize
    synthesizer = KnowledgeSynthesizer()
    result = synthesizer.synthesize("What is gradient descent?", chunks)
    
    print("\nSynthesis Preview:")
    print(result["synthesis"][:500] + "...")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Portable RAG System - Example Usage")
    print("=" * 60)
    
    # Check if we have documents in the database
    print("\n⚠️  Note: These examples require documents to be ingested first.")
    print("   Run: python src/ingest_documents.py --folder /path/to/pdfs\n")
    
    # Uncomment the examples you want to run:
    
    # example_basic_query()
    # example_advanced_query()
    # example_retrieval_only()
    # example_custom_synthesis()
    # example_save_results()
    # example_batch_queries()
    # example_direct_components()
    
    print("\n✅ Uncomment examples in main() to run them!")


if __name__ == "__main__":
    main()
