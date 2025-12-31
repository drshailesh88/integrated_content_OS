# RAG Techniques Explained

This document explains the 10 advanced RAG techniques implemented in this system.

## Overview

The system implements a complete retrieval-augmented generation pipeline with multiple layers of enhancement:

```
Query → Preprocessing → Retrieval → Fusion → Reranking → Synthesis → Response
```

## Techniques

### 1. Multi-Query Interrogation

**What it does:** Generates multiple variations of the original query to improve recall.

**Why it helps:** Different phrasings capture different relevant documents. A query about "machine learning models" might miss documents that discuss "ML algorithms" or "statistical learning systems".

**Implementation:**
```python
queries = retriever.generate_multi_queries(
    "What is deep learning?", 
    num_queries=3
)
# Returns: ["What is deep learning?", "How do neural networks learn?", "Deep learning fundamentals"]
```

**Cost:** ~$0.0001 per query (GPT-4o-mini)

---

### 2. Query Decomposition

**What it does:** Breaks complex queries into simpler sub-queries.

**Why it helps:** Complex questions often require information from multiple topics. Breaking them down ensures each aspect is covered.

**Example:**
- Original: "How does transfer learning improve model performance on small datasets?"
- Sub-queries:
  - "What is transfer learning?"
  - "How does transfer learning work?"
  - "Benefits of transfer learning for small datasets"

**When to use:** Enable for complex, multi-part questions.

---

### 3. HyDE (Hypothetical Document Embeddings)

**What it does:** Generates a hypothetical answer, then embeds that answer to search for similar real documents.

**Why it helps:** The hypothetical answer uses the same language patterns as real documents, improving semantic matching.

**Process:**
1. Query: "What is the learning rate in neural networks?"
2. Generate hypothetical answer: "The learning rate is a hyperparameter that controls how much to change the model in response to the estimated error each time the model weights are updated..."
3. Embed the hypothetical answer
4. Search for similar real documents

**Cost:** ~$0.0002 per query

---

### 4. Self-Query Filtering

**What it does:** Extracts metadata filters from natural language queries.

**Why it helps:** Narrows search to relevant document subsets.

**Example:**
- Query: "What did the 2023 guidelines say about this topic?"
- Extracted filter: `{"year": 2023, "type": "guideline"}`

**Supported filters:** source, year, type, topic

---

### 5. Dense Retrieval (Vector Search)

**What it does:** Semantic search using embeddings.

**How it works:**
1. Convert query to embedding vector (1536 dimensions)
2. Find documents with highest cosine similarity
3. Return top-k results

**Strengths:** Captures semantic meaning, handles synonyms and paraphrasing.

**Weaknesses:** May miss exact keyword matches.

---

### 6. Sparse Retrieval (BM25)

**What it does:** Keyword-based search using BM25 algorithm.

**How it works:**
1. Tokenize query and documents
2. Score based on term frequency and inverse document frequency
3. Return top-k results

**Strengths:** Excellent for exact matches, technical terms, names.

**Weaknesses:** Misses semantic similarity (synonyms).

---

### 7. Reciprocal Rank Fusion (RRF)

**What it does:** Combines results from multiple retrieval methods.

**Formula:**
```
RRF_score(d) = Σ 1/(k + rank_i(d))
```

Where `k` is a constant (default: 60) and `rank_i(d)` is the rank of document `d` in retrieval method `i`.

**Why it works:** Documents that appear in multiple result sets get boosted, while noise from individual methods is reduced.

**Example:**
- Document appears at rank 3 in dense and rank 5 in sparse
- RRF score = 1/(60+3) + 1/(60+5) = 0.0159 + 0.0154 = 0.0313

---

### 8. Cohere Reranking

**What it does:** Neural reranking of fused results.

**How it works:**
1. Take top ~40 results from RRF
2. Send to Cohere's cross-encoder model
3. Model scores each (query, document) pair
4. Return top-k by relevance score

**Why it's effective:** Cross-encoders consider query and document together, understanding nuanced relevance that embedding similarity misses.

**Model:** `rerank-english-v3.0`

**Cost:** ~$0.001 per search

---

### 9. Contextual Compression

**What it does:** Extracts only relevant sentences from each chunk.

**Why it helps:**
- Reduces noise in context
- Allows more chunks in synthesis prompt
- Improves synthesis quality

**Process:**
1. For each retrieved chunk
2. LLM extracts only query-relevant sentences
3. Compressed chunks used for synthesis

**When to use:** For highest quality (slower, ~$0.0005 per chunk)

---

### 10. LLM Synthesis

**What it does:** Generates a comprehensive answer from retrieved chunks.

**Features:**
- Structured output with sections
- Source attribution
- Handles conflicting information
- Admits gaps in knowledge

**Model:** GPT-4o-mini (cost-efficient, factual)

**Cost:** ~$0.001-0.005 per synthesis

---

## Technique Selection Guide

| Scenario | Recommended Settings |
|----------|---------------------|
| Quick factual lookup | `use_multi_query=False, use_hyde=False` |
| General questions | `use_multi_query=True, use_hyde=True` (default) |
| Complex questions | Add `use_decomposition=True` |
| Highest quality | Add `use_compression=True` |
| Debugging retrieval | `skip_synthesis=True` |

## Cost Estimates

| Technique | Cost per Query |
|-----------|---------------|
| Multi-query | ~$0.0001 |
| HyDE | ~$0.0002 |
| Embeddings | ~$0.00002 |
| Reranking | ~$0.001 |
| Compression | ~$0.0005/chunk |
| Synthesis | ~$0.002 |
| **Total (default)** | **~$0.003** |
| **Total (all features)** | **~$0.01** |

## Further Reading

- [RAG Best Practices](https://www.anthropic.com/research/long-context-prompting)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [HyDE Paper](https://arxiv.org/abs/2212.10496)
- [Cohere Rerank](https://docs.cohere.com/docs/rerank)
