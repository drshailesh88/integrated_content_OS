# Twitter Content System for Dr. Shailesh - Project Specification

## Executive Summary

Build a Python-based content generation system for a cardiologist thought leader. The system harvests content ideas from medical Twitter influencers, researches them using dual pipelines (PubMed + personal knowledge base in AstraDB), synthesizes findings, and generates publication-ready Twitter content (tweets, threads, long posts).

**Voice/Positioning:** Peter Attia's intellectual rigor + Eric Topol's scientific accuracy (Ground Truths style). Content for educated public, NOT physicians. Not dumbed down. Not oversimplified. Q1 journal-backed.

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         TWITTER CONTENT SYSTEM                                  │
│                         Code-Based Implementation                               │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   HARVEST    │───►│   RESEARCH   │───►│  SYNTHESIZE  │───►│    WRITE     │  │
│  │              │    │   PARALLEL   │    │              │    │              │  │
│  │  - Apify     │    │  - PubMed    │    │  - Merge     │    │  - Format    │  │
│  │  - Twitter   │    │  - AstraDB   │    │  - Brief     │    │  - Voice     │  │
│  │  - Filter    │    │    RAG       │    │  - Angles    │    │  - Output    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                                                 │
│  ════════════════════════════════════════════════════════════════════════════  │
│                              INFRASTRUCTURE                                     │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   AstraDB    │    │   OpenAI     │    │  OpenRouter  │    │    Apify     │  │
│  │  (Vectors)   │    │ (Embeddings) │    │   (LLMs)     │    │  (Twitter)   │  │
│  │              │    │              │    │              │    │              │  │
│  │ - ACC/ESC    │    │ text-embed-  │    │ Claude 3.5   │    │ Tweet        │  │
│  │ - ADA        │    │ ding-3-small │    │ Sonnet       │    │ Scraper V2   │  │
│  │ - Textbooks  │    │              │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Idea Harvester (`harvester.py`)

**Purpose:** Scrape tweets from medical influencers, extract high-potential content ideas.

**Inspiration Accounts (Dynamic List):**
```python
INSPIRATION_ACCOUNTS = [
    {"handle": "paddygbarrett", "name": "Dr Paddy Barrett"},
    {"handle": "DrLipid", "name": "Dr Thomas Dayspring"},
    {"handle": "davidludwigmd", "name": "Dr David Ludwig"},
    {"handle": "NutritionMadeS1", "name": "Dr Gil Carvalho"},
    {"handle": "scottissacmd", "name": "Dr Scott Issac"},
    # Easy to add/remove
]
```

**Functionality:**
- Use Apify Tweet Scraper V2 API to fetch recent tweets
- Filter: Skip retweets, replies, tweets < 80 chars
- Rank by engagement (likes + retweets*2)
- Extract top N ideas (default: 3)
- Use LLM to generate research questions from tweets

**Output:**
```python
{
    "id": "idea-123",
    "original_tweet": {
        "text": "...",
        "url": "...",
        "engagement": 450,
        "author": "paddygbarrett"
    },
    "research_question": "What is the evidence for...",
    "pubmed_query": "(heart failure) AND (SGLT2)...",
    "rag_keywords": ["SGLT2", "HFpEF", "dapagliflozin"]
}
```

---

### 2. Dual Research Pipeline (`researcher.py`)

**Purpose:** Research each idea using two parallel pipelines, merge results.

#### Pipeline A: PubMed Search

**Q1 Journal Filter (CRITICAL):**
```python
Q1_JOURNALS = [
    "N Engl J Med",
    "Lancet",
    "JAMA",
    "Circulation",
    "Eur Heart J",
    "JACC",
    "BMJ",
    "Ann Intern Med"
]
```

**Process:**
1. Build PubMed query with journal filter + date filter (last 5 years)
2. Use NCBI E-utilities: esearch → efetch
3. Parse XML, extract: PMID, title, abstract, authors, journal, year
4. Flag Q1 journals
5. Format citations: "Smith et al. NEJM. 2023"

#### Pipeline B: AstraDB RAG

**Knowledge Base Contents:**
- ACC Guidelines (heart failure, lipids, etc.)
- ESC Guidelines (all cardiology)
- ADA Guidelines (diabetes/cardio)
- Medical textbooks (user has ingested these)

**Process (HyDE-enhanced):**
1. Generate hypothetical document using LLM (what would the perfect guideline say?)
2. Embed using OpenAI text-embedding-3-small
3. Vector search AstraDB collection `medical_knowledge`
4. Filter by similarity threshold (≥0.65)
5. Return relevant chunks with source metadata

**AstraDB Collection Schema:**
```python
{
    "_id": "chunk-uuid",
    "content": "The ACC recommends...",  # or "text"
    "source_name": "ACC Guidelines 2023",
    "source_type": "guideline",  # or "textbook"
    "chapter": "Heart Failure",
    "section": "Pharmacotherapy",
    "$vector": [0.123, ...]  # 1536 dimensions
}
```

#### Merge Strategy: Reciprocal Rank Fusion (Optional)

If implementing sophisticated ranking:
```python
def rrf_score(rank, k=60):
    return 1 / (k + rank)
```

---

### 3. Knowledge Synthesizer (`synthesizer.py`)

**Purpose:** Combine research from both pipelines into actionable knowledge brief.

**LLM Prompt Structure:**
```
You are a medical knowledge synthesizer creating a research brief for a cardiologist content creator.

INPUTS:
- Research Question: {question}
- PubMed Articles: {pubmed_results}
- Guideline/Textbook Knowledge: {rag_results}

OUTPUT FORMAT:

## EXECUTIVE SUMMARY
[2-3 sentences - the key insight]

## KEY EVIDENCE FROM LITERATURE
- [Citation]: [Finding with statistics]
- ...

## GUIDELINE PERSPECTIVE
- What ACC/ESC/ADA say
- Class of recommendation, level of evidence if available

## NUANCES & CONTROVERSIES
- Areas of debate
- Where evidence conflicts with practice

## CONTENT ANGLES
1. [Specific angle for social media]
2. [Another angle]
3. [Third angle]

## CITATIONS
[Formatted references]
```

**Model:** Claude 3.5 Sonnet via OpenRouter (or direct Anthropic API)

---

### 4. Content Writer (`writer.py`)

**Purpose:** Generate publication-ready Twitter content from research brief.

**Voice Configuration:**
```python
VOICE_CONFIG = {
    "style": "Peter Attia rigor + Eric Topol accuracy",
    "tone": "Authoritative but not condescending",
    "audience": "Educated public, NOT physicians",
    "goal": "Position as thought leader in cardiology",

    "MUST_DO": [
        "Cite specific Q1 journals by name",
        "Include statistics, effect sizes, NNT when available",
        "Present nuanced takes on complex topics",
        "Reference guidelines with class/level",
        "Be scholarly but accessible"
    ],

    "MUST_NOT": [
        "Oversimplify",
        "Give medical advice",
        "Use clickbait language",
        "Use hashtags (except #MedTwitter occasionally)",
        "Hedge excessively"
    ]
}
```

**Output Formats:**

| Format | When | Structure |
|--------|------|-----------|
| `tweet` | Single insight | 280 chars max |
| `thread` | Complex topic | 5-10 numbered tweets |
| `long_post` | Deep dive | 2500 chars, mini-essay |

**Auto-Format Selection:**
LLM decides based on:
- Topic complexity
- Amount of evidence
- Engagement potential

---

### 5. Main Pipeline (`pipeline.py`)

**Purpose:** Orchestrate the full flow.

```python
class ContentPipeline:
    def __init__(self, config):
        self.harvester = IdeaHarvester(config)
        self.researcher = DualResearcher(config)
        self.synthesizer = KnowledgeSynthesizer(config)
        self.writer = ContentWriter(config)

    def run_full_pipeline(self, mode="harvest"):
        """
        Modes:
        - "harvest": Scrape Twitter → Research → Write
        - "direct": Take question directly → Research → Write
        """
        if mode == "harvest":
            ideas = self.harvester.harvest_ideas()
        else:
            ideas = [self.create_direct_idea(question)]

        results = []
        for idea in ideas:
            # Parallel research
            pubmed_results = self.researcher.search_pubmed(idea)
            rag_results = self.researcher.search_astradb(idea)

            # Synthesize
            brief = self.synthesizer.synthesize(
                idea, pubmed_results, rag_results
            )

            # Write content
            content = self.writer.write(brief)

            results.append({
                "idea": idea,
                "research": {"pubmed": pubmed_results, "rag": rag_results},
                "synthesis": brief,
                "content": content
            })

        return results
```

---

## API Keys Required

```env
# Apify (Twitter scraping)
APIFY_API_KEY=your_key

# OpenRouter (LLMs - Claude 3.5 Sonnet)
OPENROUTER_API_KEY=your_key

# OpenAI (Embeddings only)
OPENAI_API_KEY=your_key

# AstraDB (Vector database)
ASTRA_DB_API_ENDPOINT=https://xxx.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:xxx
ASTRA_DB_KEYSPACE=default_keyspace

# Optional: Direct Anthropic
ANTHROPIC_API_KEY=your_key

# NCBI (PubMed) - optional but recommended
NCBI_API_KEY=your_key
```

---

## Existing AstraDB Setup

The user has ALREADY ingested into AstraDB:
- ACC Guidelines
- ESC Guidelines
- ADA Guidelines
- Medical textbooks

Collection name: `medical_knowledge` (verify with user)
Embedding model used: `text-embedding-3-small` (verify with user)

Reference implementation for RAG: https://github.com/drshailesh88/dr-shailesh-content-os
- See `tools/rag-query.py`
- See `tools/hybrid_retriever.py`
- See `tools/advanced_retriever.py`

Key patterns from that repo:
- HyDE (Hypothetical Document Embedding)
- Hybrid retrieval (dense + sparse)
- Cohere reranking (optional)

---

## User Interface Options

### Option A: CLI (Simplest)
```bash
# Harvest mode - scrape Twitter, process top 3 ideas
python main.py harvest

# Direct question mode
python main.py direct "What is the evidence for PCSK9 inhibitors?"

# Specify format
python main.py direct "..." --format thread
```

### Option B: Streamlit Web UI
Simple interface with:
- Text input for direct questions
- Checkboxes for inspiration accounts
- Output display with copy buttons
- History of generated content

### Option C: Slack Integration
- Slash command: `/content "question"`
- Daily digest to channel
- Interactive buttons for format selection

---

## File Structure

```
twitter-content-system/
├── src/
│   ├── __init__.py
│   ├── config.py           # All configuration, API keys, accounts list
│   ├── harvester.py        # Twitter scraping via Apify
│   ├── researcher.py       # Dual pipeline: PubMed + AstraDB
│   ├── synthesizer.py      # Knowledge synthesis
│   ├── writer.py           # Content generation
│   ├── pipeline.py         # Main orchestration
│   └── utils/
│       ├── pubmed.py       # PubMed API helpers
│       ├── astradb.py      # AstraDB/RAG helpers
│       ├── llm.py          # LLM API wrappers
│       └── apify.py        # Apify API helpers
├── main.py                 # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## Requirements

```
# Core
python>=3.10
requests
httpx
python-dotenv

# AstraDB
astrapy>=1.0.0

# Embeddings
openai>=1.0.0

# LLM
anthropic  # or use openrouter via requests

# PubMed XML parsing
lxml
xmltodict

# Optional: Better RAG
langchain
langchain-community
sentence-transformers
cohere  # for reranking

# Optional: Web UI
streamlit

# Optional: Async
asyncio
aiohttp
```

---

## Sample Output

**Input:** Tweet from @DrLipid about LDL targets

**Research Brief:**
```
## EXECUTIVE SUMMARY
Aggressive LDL lowering (<55 mg/dL) in high-risk patients reduces cardiovascular
events by ~25% compared to moderate targets, with no J-curve observed in major trials.

## KEY EVIDENCE
- Giugliano et al. Lancet 2017 (FOURIER): PCSK9i reduced LDL to 30 mg/dL,
  15% relative risk reduction in MACE
- Sabatine et al. NEJM 2017: No increase in adverse events at very low LDL
- Cannon et al. NEJM 2015 (IMPROVE-IT): Adding ezetimibe to statin reduced
  events by 6.4% absolute

## GUIDELINE PERSPECTIVE
- ESC 2021: LDL <55 mg/dL for very high risk (Class I, Level A)
- ACC 2018: Consider <70 mg/dL, intensify if needed

## NUANCES
- Debate: Is there a floor? Some data suggests <20 mg/dL still safe
- Practice gap: Many high-risk patients not at goal despite available therapies

## CONTENT ANGLES
1. "The lower the better" - what the data actually shows
2. Why your cardiologist might not be aggressive enough
3. The PCSK9 inhibitor revolution - 5 years later
```

**Generated Thread:**
```
1/7 The debate about "how low should LDL go" is effectively settled.

The data is unambiguous: lower is better. There is no J-curve.

Let me walk you through what the landmark trials actually showed...

2/7 FOURIER (Lancet 2017) took 27,000 patients already on statins and added
evolocumab (a PCSK9 inhibitor).

LDL dropped to 30 mg/dL.

Result: 15% reduction in heart attacks, strokes, and cardiovascular death.

3/7 ...
```

---

## Key Design Principles

1. **Modularity:** Each component is independent, testable
2. **Parallel Research:** PubMed and RAG run concurrently
3. **Quality over Quantity:** Q1 journals only, high-similarity RAG results only
4. **Voice Consistency:** Prompts encode the Peter Attia/Eric Topol style
5. **Dynamic Configuration:** Easy to add/remove inspiration accounts
6. **Graceful Degradation:** Works even if one pipeline fails

---

## Success Criteria

1. Pipeline runs end-to-end without manual intervention
2. Research pulls from BOTH PubMed AND AstraDB
3. Content cites specific journals and statistics
4. Voice matches Peter Attia/Eric Topol style
5. Output is publication-ready (minimal editing needed)
6. Easy to add new inspiration accounts
7. Can handle both "harvest" and "direct question" modes

---

## Next Steps for Implementation

1. Set up project structure
2. Implement config management with .env
3. Build Apify harvester
4. Build PubMed researcher
5. Build AstraDB RAG researcher (use patterns from dr-shailesh-content-os)
6. Build synthesizer with Claude prompts
7. Build writer with voice configuration
8. Create main pipeline orchestration
9. Add CLI interface
10. Test end-to-end
11. Optional: Add Streamlit UI

---

## Reference Links

- Apify Tweet Scraper: https://apify.com/apidojo/tweet-scraper
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25500/
- AstraDB Python: https://docs.datastax.com/en/astra/astra-db-vector/
- OpenRouter API: https://openrouter.ai/docs
- User's RAG reference: https://github.com/drshailesh88/dr-shailesh-content-os
