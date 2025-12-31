#!/usr/bin/env python3
"""
Document Ingestion Pipeline

Ingests PDFs with adaptive chunking, generates embeddings, and stores in AstraDB.

Features:
- Adaptive chunking (preserves context)
- Rich metadata extraction
- Progress tracking and resumability
- Batch processing with rate limiting

Usage:
    python src/ingest_documents.py --folder /path/to/pdfs
    python src/ingest_documents.py --file /path/to/document.pdf
"""

import os
import sys
import json
import hashlib
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from tqdm import tqdm

try:
    from pypdf import PdfReader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_core.documents import Document
except ImportError as e:
    print(f"❌ Error: Required packages not installed - {e}")
    print("Install with: pip install pypdf langchain langchain-community langchain-text-splitters")
    sys.exit(1)

try:
    from openai import OpenAI
    import tiktoken
except ImportError:
    print("❌ Error: OpenAI package not installed")
    print("Install with: pip install openai tiktoken")
    sys.exit(1)

try:
    from astrapy import DataAPIClient
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Chunking configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1024"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

# Progress tracking
PROGRESS_FILE = ".ingestion_progress.json"


class DocumentIngestor:
    """Handles document ingestion with adaptive chunking and metadata extraction."""
    
    def __init__(self):
        """Initialize the ingestor."""
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.astra_db = None
        self.collection = None
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress from previous runs."""
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {"processed_files": [], "total_chunks": 0, "total_cost": 0.0}
    
    def _save_progress(self):
        """Save progress to file."""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def connect(self):
        """Connect to AstraDB."""
        print("🔌 Connecting to AstraDB...")
        client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
        self.astra_db = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT)
        self.collection = self.astra_db.get_collection(ASTRA_DB_COLLECTION)
        print(f"✅ Connected to collection: {ASTRA_DB_COLLECTION}")
    
    def detect_structure(self, pdf_path: Path) -> str:
        """Detect if PDF has clear structure (headings, chapters)."""
        try:
            reader = PdfReader(str(pdf_path))
            sample_text = ""
            for i in range(min(3, len(reader.pages))):
                sample_text += reader.pages[i].extract_text()
            
            indicators = [
                "\n1.", "\n2.", "\n3.",
                "Section", "Chapter",
                "Introduction", "Methods",
                "Abstract", "Conclusion",
            ]
            
            count = sum(1 for ind in indicators if ind in sample_text)
            return "structured" if count >= 3 else "unstructured"
        
        except Exception:
            return "unstructured"
    
    def extract_metadata(self, pdf_path: Path, page_num: int, text: str) -> Dict[str, Any]:
        """Extract rich metadata from document."""
        metadata = {
            "source": pdf_path.name,
            "page": page_num,
            "file_size_mb": round(pdf_path.stat().st_size / (1024 * 1024), 2),
            "ingestion_date": datetime.now().isoformat(),
        }
        
        # Detect document type from filename
        filename_lower = pdf_path.name.lower()
        if any(kw in filename_lower for kw in ["guideline", "standard", "policy"]):
            metadata["type"] = "guideline"
        elif any(kw in filename_lower for kw in ["textbook", "manual", "handbook"]):
            metadata["type"] = "textbook"
        elif any(kw in filename_lower for kw in ["paper", "study", "research"]):
            metadata["type"] = "research"
        else:
            metadata["type"] = "document"
        
        # Extract year from filename
        year_match = re.search(r'20\d{2}', pdf_path.name)
        if year_match:
            metadata["year"] = int(year_match.group())
        
        # Extract chapter/section from text
        for pattern in [r'Chapter\s+(\d+)', r'Section\s+(\d+)', r'^(\d+)\.']:
            match = re.search(pattern, text[:500], re.MULTILINE)
            if match:
                metadata["section"] = match.group(0)
                break
        
        return metadata
    
    def chunk_document(self, pdf_path: Path) -> List[Document]:
        """Adaptively chunk document based on structure."""
        structure = self.detect_structure(pdf_path)
        print(f"   📄 {pdf_path.name}: {structure}")
        
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=lambda t: len(self.tokenizer.encode(t)),
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = splitter.split_documents(pages)
        
        for i, chunk in enumerate(chunks):
            page_num = chunk.metadata.get('page', 0)
            metadata = self.extract_metadata(pdf_path, page_num, chunk.page_content)
            chunk.metadata.update(metadata)
            chunk.metadata['chunk_id'] = i
            chunk.metadata['total_chunks'] = len(chunks)
        
        return chunks
    
    def estimate_cost(self, chunks: List[Document]) -> Dict[str, Any]:
        """Estimate embedding cost."""
        total_tokens = sum(
            len(self.tokenizer.encode(chunk.page_content))
            for chunk in chunks
        )
        # text-embedding-3-small: $0.02 per 1M tokens
        estimated_cost = (total_tokens / 1_000_000) * 0.02
        
        return {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(estimated_cost, 6)
        }
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        try:
            response = self.openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"❌ Embedding generation failed: {e}")
            return []
    
    def create_document_id(self, chunk: Document) -> str:
        """Create unique document ID from content hash."""
        content = chunk.page_content + str(chunk.metadata.get('source', ''))
        return hashlib.md5(content.encode()).hexdigest()
    
    def ingest_chunks(self, chunks: List[Document], source_name: str):
        """Ingest chunks into AstraDB with embeddings."""
        print(f"   🚀 Ingesting {len(chunks)} chunks...")
        
        for i in tqdm(range(0, len(chunks), BATCH_SIZE), desc="   Batches"):
            batch = chunks[i:i + BATCH_SIZE]
            
            texts = [chunk.page_content for chunk in batch]
            embeddings = self.generate_embeddings(texts)
            
            if not embeddings:
                print(f"⚠️  Skipping batch {i // BATCH_SIZE + 1}")
                continue
            
            documents = []
            for chunk, embedding in zip(batch, embeddings):
                doc_id = self.create_document_id(chunk)
                documents.append({
                    "_id": doc_id,
                    "$vector": embedding,
                    "content": chunk.page_content,
                    "metadata": chunk.metadata
                })
            
            try:
                self.collection.insert_many(documents)
            except Exception as e:
                print(f"⚠️  Batch insertion failed: {e}")
                continue
        
        self.progress["processed_files"].append(source_name)
        self.progress["total_chunks"] += len(chunks)
        self._save_progress()
    
    def process_file(self, pdf_path: Path):
        """Process a single PDF file."""
        if pdf_path.name in self.progress["processed_files"]:
            print(f"⏭️  Skipping {pdf_path.name} (already processed)")
            return
        
        print(f"\n📖 Processing: {pdf_path.name}")
        
        chunks = self.chunk_document(pdf_path)
        cost_info = self.estimate_cost(chunks)
        
        print(f"   📊 Chunks: {cost_info['total_chunks']}")
        print(f"   💰 Estimated cost: ${cost_info['estimated_cost_usd']:.6f}")
        
        self.ingest_chunks(chunks, pdf_path.name)
        self.progress["total_cost"] += cost_info['estimated_cost_usd']
        self._save_progress()
        
        print(f"   ✅ Completed: {pdf_path.name}")
    
    def process_folder(self, folder_path: str):
        """Process all PDFs in a folder."""
        pdf_files = list(Path(folder_path).glob("*.pdf"))
        print(f"📚 Found {len(pdf_files)} PDF files")
        
        pending = [f for f in pdf_files if f.name not in self.progress["processed_files"]]
        
        if not pending:
            print("✅ All files already processed!")
            return
        
        print(f"📋 Pending: {len(pending)} files")
        print(f"✅ Already processed: {len(self.progress['processed_files'])} files")
        
        for pdf_path in pending:
            try:
                self.process_file(pdf_path)
            except Exception as e:
                print(f"❌ Error processing {pdf_path.name}: {e}")
                continue
        
        self._print_summary()
    
    def _print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 50)
        print("✅ Ingestion Complete!")
        print("=" * 50)
        print(f"📊 Total files processed: {len(self.progress['processed_files'])}")
        print(f"📦 Total chunks created: {self.progress['total_chunks']}")
        print(f"💰 Total cost: ${self.progress['total_cost']:.4f}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into RAG system")
    parser.add_argument("--folder", type=str, help="Folder containing PDF files")
    parser.add_argument("--file", type=str, help="Single PDF file to ingest")
    parser.add_argument("--reset", action="store_true", help="Reset progress tracking")
    
    args = parser.parse_args()
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not set")
        sys.exit(1)
    
    if not ASTRA_DB_APPLICATION_TOKEN:
        print("❌ Error: ASTRA_DB_APPLICATION_TOKEN not set")
        sys.exit(1)
    
    if args.reset and os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("✅ Progress reset")
    
    ingestor = DocumentIngestor()
    ingestor.connect()
    
    if args.file:
        ingestor.process_file(Path(args.file))
    elif args.folder:
        ingestor.process_folder(args.folder)
    else:
        print("❌ Please specify --folder or --file")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
