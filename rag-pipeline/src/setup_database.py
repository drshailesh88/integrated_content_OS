#!/usr/bin/env python3
"""
AstraDB Setup for RAG System

Creates and configures the vector collection for document storage.

Usage:
    python src/setup_database.py
"""

import os
import sys
from typing import Any
from dotenv import load_dotenv

try:
    from astrapy import DataAPIClient
    from astrapy.constants import VectorMetric
    from astrapy.info import CollectionDefinition
except ImportError:
    print("❌ Error: astrapy not installed")
    print("Install with: pip install astrapy")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "documents")

# Embedding configuration (OpenAI text-embedding-3-small)
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))


def validate_credentials() -> bool:
    """Validate that all required credentials are present."""
    missing = []
    
    if not ASTRA_DB_APPLICATION_TOKEN:
        missing.append("ASTRA_DB_APPLICATION_TOKEN")
    if not ASTRA_DB_API_ENDPOINT:
        missing.append("ASTRA_DB_API_ENDPOINT")
    
    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease add these to your .env file")
        return False
    
    return True


def connect_to_astradb() -> Any:
    """Connect to AstraDB and return the database instance."""
    try:
        print("🔌 Connecting to AstraDB...")
        client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
        database = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT)
        print("✅ Connected to AstraDB")
        return database
    except Exception as e:
        print(f"❌ Failed to connect to AstraDB: {str(e)}")
        sys.exit(1)


def create_collection(database: Any, force_recreate: bool = False) -> Any:
    """Create the vector collection."""
    try:
        print(f"\n📦 Setting up collection: {ASTRA_DB_COLLECTION}")
        
        existing_collections = database.list_collection_names()
        
        if ASTRA_DB_COLLECTION in existing_collections:
            if force_recreate:
                print(f"🗑️  Deleting existing collection...")
                database.drop_collection(ASTRA_DB_COLLECTION)
            else:
                print(f"✅ Collection '{ASTRA_DB_COLLECTION}' already exists")
                return database.get_collection(ASTRA_DB_COLLECTION)
        
        # Create collection with vector configuration
        collection_definition = (
            CollectionDefinition.builder()
            .set_vector_dimension(EMBEDDING_DIMENSION)
            .set_vector_metric(VectorMetric.COSINE)
            .build()
        )
        
        collection = database.create_collection(
            name=ASTRA_DB_COLLECTION,
            definition=collection_definition
        )
        
        print(f"✅ Created collection: {ASTRA_DB_COLLECTION}")
        print(f"   - Dimension: {EMBEDDING_DIMENSION}")
        print(f"   - Metric: Cosine Similarity")
        
        return collection
    
    except Exception as e:
        print(f"❌ Failed to create collection: {str(e)}")
        sys.exit(1)


def test_collection(collection: Any) -> None:
    """Test the collection with a dummy document."""
    try:
        print("\n🧪 Testing collection...")
        
        test_doc = {
            "_id": "test-doc-001",
            "$vector": [0.1] * EMBEDDING_DIMENSION,
            "content": "This is a test document.",
            "metadata": {"source": "test", "page": 1}
        }
        
        collection.insert_one(test_doc)
        result = collection.find_one({"_id": "test-doc-001"})
        
        if result:
            print("✅ Test document inserted and retrieved successfully")
        
        collection.delete_one({"_id": "test-doc-001"})
        print("✅ Test document cleaned up")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)


def display_info(database: Any) -> None:
    """Display collection information."""
    print("\n📊 Database Collections:")
    print("=" * 50)
    
    for name in database.list_collection_names():
        print(f"  📦 {name}")
    
    print("=" * 50)


def main():
    """Main setup function."""
    print("=" * 50)
    print("🚀 RAG System - Database Setup")
    print("=" * 50)
    
    if not validate_credentials():
        sys.exit(1)
    
    database = connect_to_astradb()
    collection = create_collection(database)
    test_collection(collection)
    display_info(database)
    
    print("\n✅ Setup Complete!")
    print("\nNext: Run 'python src/ingest_documents.py' to add documents")


if __name__ == "__main__":
    main()
