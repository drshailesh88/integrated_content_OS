"""
AstraDB Client for RAG
Interfaces with AstraDB to retrieve relevant medical guidelines and textbook snippets.
"""

import os
import logging
from typing import List, Dict, Optional
from astrapy import DataAPIClient
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "guidelines")


class AstraRAGClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        
        if ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_API_ENDPOINT:
            try:
                self.client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
                self.db = self.client.get_database_by_api_endpoint(ASTRA_DB_API_ENDPOINT)
                self.collection = self.db.get_collection(ASTRA_DB_COLLECTION)
                logger.info(f"Successfully connected to AstraDB collection: {ASTRA_DB_COLLECTION}")
            except Exception as e:
                logger.error(f"Failed to connect to AstraDB: {e}")
        else:
            logger.warning("AstraDB credentials not found in environment variables. RAG features will be disabled.")

    def query_guidelines(self, text: str, limit: int = 3) -> List[str]:
        """
        Query the vector database for relevant guideline snippets.
        
        Args:
            text: The search query (e.g., article title or abstract)
            limit: Number of snippets to retrieve
            
        Returns:
            List of text snippets
        """
        if not self.collection:
            return []
            
        try:
            # Perform vector search
            # Note: This assumes the collection has a vector index and uses the standard 'text' field
            results = self.collection.find(
                sort={"$vectorize": text},
                limit=limit,
                projection={"text": 1, "content": 1, "metadata": 1}
            )
            
            snippets = []
            for doc in results:
                # Try common content field names
                snippet = doc.get("text") or doc.get("content")
                if snippet:
                    snippets.append(snippet)
                elif "metadata" in doc and isinstance(doc["metadata"], dict):
                    # Fallback to metadata if text is nested
                    snippet = doc["metadata"].get("text") or doc["metadata"].get("content")
                    if snippet:
                        snippets.append(snippet)
            
            return snippets
        except Exception as e:
            logger.error(f"Error querying AstraDB: {e}")
            return []


# Singleton instance
_rag_client = None

def get_rag_client():
    global _rag_client
    if _rag_client is None:
        _rag_client = AstraRAGClient()
    return _rag_client

def query_guidelines(text: str, limit: int = 3) -> List[str]:
    """Helper function to query guidelines."""
    client = get_rag_client()
    return client.query_guidelines(text, limit)


if __name__ == "__main__":
    # Simple test run
    print("Testing AstraDB Connection...")
    results = query_guidelines("Statin therapy in elderly patients", limit=2)
    if results:
        print(f"Found {len(results)} relevant snippets:")
        for i, s in enumerate(results):
            print(f"\nSnippet {i+1}: {s[:200]}...")
    else:
        print("No snippets found or connection failed.")
