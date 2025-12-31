"""
Portable RAG System

A production-ready hybrid retrieval-augmented generation system.

Components:
- AdvancedRetriever: Full-featured retrieval with 10 techniques
- HybridRetriever: Basic hybrid retrieval (dense + sparse + rerank)
- KnowledgeSynthesizer: LLM-based knowledge synthesis
- RAGSystem: Complete end-to-end pipeline
"""

from .retriever import HybridRetriever
from .advanced_retriever import AdvancedRetriever
from .synthesizer import KnowledgeSynthesizer
from .query import RAGSystem

__all__ = [
    "HybridRetriever",
    "AdvancedRetriever", 
    "KnowledgeSynthesizer",
    "RAGSystem"
]

__version__ = "1.0.0"
