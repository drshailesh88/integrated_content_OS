# Portable RAG System

A production-ready, hybrid Retrieval-Augmented Generation (RAG) system that you can take anywhere.

## Features

- **Hybrid Retrieval**: Combines dense (vector) + sparse (BM25) search with Reciprocal Rank Fusion
- **Advanced Techniques**: Multi-query, HyDE, query decomposition, self-query filtering
- **Neural Reranking**: Cohere reranking for high-precision results
- **LLM Synthesis**: GPT-4o-mini for cost-efficient knowledge synthesis
- **Vector Database**: AstraDB (DataStax) for scalable vector storage
- **PDF Ingestion**: Adaptive chunking with rich metadata extraction

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         QUERY PIPELINE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Query ──► Multi-Query ──► HyDE ──► Dense + Sparse ──► RRF ──►      │
│            Generation      Embed    Retrieval          Fusion        │
│                                                                      │
│         ──► Cohere Rerank ──► Contextual Compress ──► LLM Synthesis │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       INGESTION PIPELINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PDFs ──► Adaptive Chunking ──► Metadata Extraction ──► Embeddings  │
│                                                                      │
│       ──► AstraDB Vector Storage                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required API keys:
- **OpenAI**: For embeddings and synthesis
- **AstraDB**: For vector storage
- **Cohere**: For reranking

### 3. Setup Database

```bash
python src/setup_database.py
```

### 4. Ingest Documents

```bash
python src/ingest_documents.py --folder /path/to/your/pdfs
```

### 5. Query

```bash
python src/query.py "What are the best practices for X?"
```

## Project Structure

```
portable-rag-system/
├── src/
│   ├── setup_database.py      # AstraDB collection setup
│   ├── ingest_documents.py    # PDF ingestion pipeline
│   ├── retriever.py           # Hybrid retrieval (basic)
│   ├── advanced_retriever.py  # Advanced retrieval (10 techniques)
│   ├── synthesizer.py         # LLM synthesis engine
│   └── query.py               # Main query interface
├── examples/
│   └── example_usage.py       # Example usage patterns
├── docs/
│   └── TECHNIQUES.md          # Detailed technique explanations
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Configuration Options

### Retrieval Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DENSE_TOP_K` | 20 | Vector search results |
| `SPARSE_TOP_K` | 20 | BM25 results |
| `RRF_K` | 60 | RRF fusion constant |
| `RERANK_TOP_K` | 10 | Final results after reranking |

### Chunking Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | 1024 | Tokens per chunk |
| `CHUNK_OVERLAP` | 150 | Overlap between chunks |

### Query Options

```python
from src.advanced_retriever import AdvancedRetriever

retriever = AdvancedRetriever()
results = retriever.retrieve(
    query="Your question here",
    top_k=10,
    use_multi_query=True,    # Generate query variations
    use_decomposition=False, # Break into sub-queries
    use_hyde=True,           # Hypothetical document embeddings
    use_self_query=True,     # Extract metadata filters
    use_compression=False    # Contextual compression (slower)
)
```

## API Costs (Estimates)

| Component | Model | Cost |
|-----------|-------|------|
| Embeddings | text-embedding-3-small | $0.02 / 1M tokens |
| Synthesis | GPT-4o-mini | $0.15 / 1M input, $0.60 / 1M output |
| Reranking | Cohere rerank-english-v3.0 | $1.00 / 1K searches |

## Customization

### Using a Different Vector Database

Replace `setup_database.py` and modify the retrieval methods in `retriever.py`. The system is designed to be modular - just implement these methods:
- `dense_retrieve(query, k)` → List of documents
- `sparse_retrieve(query, k)` → List of documents

### Using Different Embeddings

Change `EMBEDDING_MODEL` in the config and update `EMBEDDING_DIMENSION` to match.

### Using a Different LLM

Modify `synthesizer.py` to use your preferred LLM API.

## License

MIT License - Use freely in your projects.

## Acknowledgments

Built with:
- [AstraDB](https://www.datastax.com/products/datastax-astra) - Vector database
- [OpenAI](https://openai.com/) - Embeddings & LLM
- [Cohere](https://cohere.com/) - Reranking
- [LangChain](https://langchain.com/) - Text processing
