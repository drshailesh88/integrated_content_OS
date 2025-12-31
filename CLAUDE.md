# Dr. Shailesh Singh - Integrated Content Operating System

**Single Source of Truth** for all content creation, research, and writing.
Works with: Antigravity, VS Code, Cursor, Claude Code.

---

## CLAUDE: YOUR SUPERPOWERS

> **REMEMBER THIS AFTER EVERY /clear**
> You are Claude, the DEFAULT writer in this system. You have access to 181+ skills, 3 research pipelines, 6 LLM models, and comprehensive social media research tools. The user NEVER needs to leave this cowriting system.
>
> **SKILL ROUTING:** See `SKILL-CATALOG.md` for purpose-based skill lookup ("I want to do X → use skill Y"). Use it to route user requests to the right skill.

### What You Can Do (Complete Capabilities)

| Capability | How | Skills/Tools |
|------------|-----|--------------|
| **Write YouTube Scripts** | Hinglish, Peter Attia style | `youtube-script-master`, `hook-generator` |
| **Write Twitter Content** | Eric Topol + Ground Truths | `x-post-creator-skill`, `cardiology-tweet-writer`, `cremieux-cardio` |
| **Write Newsletters** | Topol style, anti-AI | `cardiology-newsletter-writer`, `medical-newsletter-writer` |
| **Write Editorials** | JACC style, trial analysis | `cardiology-editorial`, `cardiology-trial-editorial` |
| **Research PubMed** | MCP tools, citations | PubMed MCP (MANDATORY) |
| **Research Guidelines** | RAG from AstraDB | `knowledge-pipeline`, ACC/ESC/ADA |
| **Find Trending Topics** | Google Trends, Reddit, Perplexity | `social-media-trends-research`, `perplexity-search` |
| **Predict Viral Content** | ML scoring | `viral-content-predictor` |
| **Generate Images** | Blog headers, infographics | `cardiology-visual-system`, `gemini-imagegen` |
| **Use Other AI Models** | GPT-4o, Gemini, Grok, GLM | `multi-model-writer`, `browser-automation` |
| **Repurpose Content** | Multi-platform adaptation | `cardiology-content-repurposer` |
| **Analyze YouTube Comments** | Just give me a URL | `youtube-comment-analyzer` |
| **PRODUCE ALL CONTENT** | One topic → ALL formats | `content-os` (MASTER SKILL) |

---

## CONTENT OS: THE "PRODUCE EVERYTHING" BUTTON

> **When you say "Content OS: [topic]"** → I produce ALL content types from that one idea.

### Forward Mode (Seed → All Content)
```
"Content OS: Statins myth-busting for Indians"

OUTPUT:
├── Long-form (Quality Passed - Full Pipeline)
│   ├── YouTube script (Hinglish)
│   ├── Newsletter B2C (patients)
│   ├── Newsletter B2B (doctors)
│   ├── Editorial (Eric Topol style)
│   └── Blog post
│
├── Short-form (Accuracy Checked - Quick Pass)
│   ├── 5-10 tweets
│   ├── 1 thread
│   └── Carousel content
│
└── Visual
    └── Instagram carousel slides
```

### Backward Mode (Long-form → Split)
```
"Content OS: [paste your blog/script]"

OUTPUT:
├── 5-10 tweets (key points)
├── 1 thread (condensed)
├── Carousel slides
└── Snippets (quotables)
```

### Quality Gates
- **Long-form English**: Full quality pipeline (scientific rigor, peer review, reflection, anti-AI)
- **Short-form**: Quick accuracy pass (no data misinterpretation)

### Customization
```
"Content OS: Statins - only YouTube and tweets"
"Content OS: GLP-1 - skip editorial"
"Content OS: CAC scoring - long-form only"
```

---

## QUICK REFERENCE: COMMON TASKS

### "Analyze comments for [YouTube URL]"
→ Just give me any YouTube URL or video ID
→ I'll scrape 2000+ comments, analyze with free LLMs, and show you insights
→ Example: "Analyze comments for https://youtube.com/watch?v=xyz"

### "Find what's trending in cardiology"
```bash
# Option 1: Use social-media-trends-research skill
python skills/cardiology/social-media-trends-research/scripts/trend_research.py \
  --keywords "cardiology" "heart health" --subreddits "cardiology" "health"

# Option 2: Ask me to use Perplexity
"What's trending on Twitter about cardiology this week?"
```

### "Write a tweet about [topic]"
→ Use `x-post-creator-skill` or `cardiology-tweet-writer`
→ I'll research with PubMed first, then write in Eric Topol voice

### "Write a YouTube script"
→ Use `youtube-script-master` (requires research-engine data first)
→ 70% Hindi / 30% English, Peter Attia style

### "Analyze a clinical trial"
→ Use `cardiology-trial-editorial` with scoring script
→ Hybrid scoring: rules + LLM, 0-19 point scale

### "Create an image for my blog"
→ Use `cardiology-visual-system` (auto-routes to best tool)
→ Fal.ai for photos, Gemini for infographics, Mermaid for flowcharts

---

## YOUR MULTI-MODEL ARSENAL

| Model | How to Use | Cost | Best For |
|-------|-----------|------|----------|
| **Claude (YOU)** | Default - just write | Subscription | All medical content, accuracy |
| **GPT-4o-mini** | `router.write(prompt, model="gpt-4o-mini")` | $0.60/M | Quick drafts |
| **GPT-4o** | `router.write(prompt, model="gpt-4o")` | $10/M | Quality alternative |
| **Gemini** | `router.write(prompt, model="gemini")` | FREE | Research, fact-checking |
| **Grok** | `router.write(prompt, model="grok")` | $15/M | X/Twitter trends |
| **GLM-4.7** | `router.write(prompt, model="glm-4.7")` | $0.10/M | Bulk generation |

**Usage:**
```python
from skills.cardiology.multi_model_writer.model_router import ModelRouter
router = ModelRouter()
response = router.write("prompt", model="gpt-4o")  # or gemini, grok, glm-4.7
```

---

## SOCIAL MEDIA RESEARCH STACK (Zero Cost)

### Your Research Tools

| Platform | Tool | How to Use | Cost |
|----------|------|------------|------|
| **Google Trends** | pytrends | `trend_research.py --keywords "topic"` | FREE |
| **Reddit** | reddit_scraper.py | `--subreddits "health"` | FREE |
| **Twitter/X** | Perplexity MCP | Ask: "What's viral on Twitter about..." | FREE |
| **TikTok** | Perplexity MCP | Ask: "TikTok trends about..." | FREE |
| **YouTube** | research-engine | `run_pipeline.py --quick` | FREE |
| **LinkedIn** | Perplexity MCP | Ask: "LinkedIn discussions about..." | FREE |

### Quick Trend Research
```python
from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=330)  # India timezone
pytrends.build_payload(['heart health'], timeframe='now 7-d', geo='IN')

# Rising queries = viral opportunities
related = pytrends.related_queries()
print(related['heart health']['rising'])

time.sleep(5)  # Rate limiting
```

### Research Workflow
```
1. Google Trends (pytrends) → Find rising keywords
2. Reddit (reddit_scraper) → See community discussions
3. Perplexity MCP → Twitter/TikTok/YouTube trends
4. research-engine → Competitor analysis (35+ channels)
5. viral-content-predictor → Score content ideas
```

---

## COMPLETE SKILLS INVENTORY (181+ Skills)

### Cardiology Skills (46 Skills)

#### YouTube & Hinglish Content
| Skill | Purpose |
|-------|---------|
| `youtube-script-master` | **MAIN** - Data-driven Hinglish scripts, 15-30 min |
| `youtube-script-hinglish` | Hinglish voice patterns |
| `debunk-script-writer` | Counter misinformation, 8 narratives |
| `hook-generator` | Viral hooks for YouTube |

#### Twitter/X & Social Media
| Skill | Purpose |
|-------|---------|
| `x-post-creator-skill` | Twitter posts with frameworks + 6 references |
| `cardiology-tweet-writer` | Tweet writing + seed ideas + modifiers |
| `cremieux-cardio` | Data-driven posts with visualizations |
| `twitter-longform-medical` | Long-form threads |
| `cardiology-content-repurposer` | Multi-platform adaptation + templates |

#### Newsletters & Editorials
| Skill | Purpose |
|-------|---------|
| `cardiology-newsletter-writer` | Newsletter + anti-AI guidelines |
| `medical-newsletter-writer` | Topol style guide + workflow |
| `cardiology-editorial` | Eric Topol style, hybrid scoring |
| `cardiology-trial-editorial` | Trial analysis + scoring script |
| `cardiology-topol-writer` | Transform thought dumps |
| `academic-chapter-writer` | 5,000-15,000 word chapters |
| `cardiology-science-for-people` | General audience writing |
| `cardiology-writer` | General cardiology content |

#### Research & Discovery
| Skill | Purpose |
|-------|---------|
| `social-media-trends-research` | **NEW** - pytrends + Reddit + Perplexity |
| `viral-content-predictor` | ML prediction + analysis script |
| `content-trend-researcher` | 10+ platform analysis |
| `content-marketing-social-listening` | Viral opportunity discovery |
| `perplexity-search` | AI-powered web search |
| `deep-researcher` | Multi-layered research |
| `content-research-writer` | Research + writing partner |
| `knowledge-pipeline` | RAG + PubMed synthesis |
| `pubmed-database` | PubMed searches |
| `clinicaltrials-database` | Clinical trials |
| `literature-review` | Systematic reviews |
| `research-synthesizer` | Knowledge synthesis |
| `citation-management` | Reference handling |

#### Quality & Voice
| Skill | Purpose |
|-------|---------|
| `authentic-voice` | AI detection elimination |
| `content-reflection` | Pre-publish QA |
| `scientific-critical-thinking` | Evidence analysis |

#### Visual Content
| Skill | Purpose |
|-------|---------|
| `cardiology-visual-system` | Auto-routes to best tool |
| `gemini-imagegen` | Gemini API images |

#### Multi-Model & Utilities
| Skill | Purpose |
|-------|---------|
| `multi-model-writer` | 6 LLM routing |
| `browser-automation` | ChatGPT/Gemini web |
| `article-extractor` | Clean URL extraction |
| `mcp-management` | MCP server management |
| `content-os` | System orchestration |

### Scientific Skills (135 Skills)
Located in `skills/scientific/`

**Databases:** alphafold, biorxiv, chembl, clinicaltrials, clinvar, cosmic, drugbank, ensembl, gnomad, gwas-catalog, kegg, pdb, pubmed, reactome, string, uniprot

**Bioinformatics:** biopython, scanpy, anndata, cellxgene-census, deepchem, genomics-tools, mafft, nextflow, samtools

**Data Science:** dask, pandas-workflows, plotly, polars, pytorch, scikit-learn, scipy, seaborn, statsmodels

---

## PIPELINES

### 1. Twitter Content Pipeline
**Location:** `pipelines/twitter-content/`

```bash
# Direct question
python pipelines/twitter-content/generate.py "GLP-1 cardiovascular effects?"

# Harvest from influencers
python pipelines/twitter-content/main.py harvest
```

**Flow:** HARVEST → RESEARCH (PubMed + AstraDB) → SYNTHESIZE → WRITE

**Inspiration Accounts:** @EricTopol, @paddygbarrett, @DrLipid, @davidludwigmd, @NutritionMadeS1, @scottissacmd

### 2. YouTube Research Pipeline
**Location:** `research-engine/`

```bash
python run_pipeline.py          # Full (30 min)
python run_pipeline.py --quick  # Quick (10 min)
python calendar_generator.py --show-next 5
```

**35+ Tracked Channels:**
- Competition: Dr Navin Agrawal, Cardiac Second Opinion
- Anti-patterns: SAAOL, Dr Biswaroop Roy Chowdhury
- Inspiration: Peter Attia, York Cardiology, Medlife Crisis
- Belief Seeders: Dr Eric Berg, Dr Ken Berry, Dr Sten Ekberg

**8 Dangerous Narratives:** ldl_skepticism, statin_fear, insulin_primacy, fasting_absolutism, supplement_superiority, seed_oil_villain, exercise_compensation, fear_mongering

### 3. Journal Fetching Pipeline
**Location:** `workflows/` (Antigravity/n8n)

**20+ Journals:**
- Tier 1: NEJM, Lancet, JAMA, BMJ
- Tier 2: JACC, Circulation, European Heart Journal
- Tier 3: JACC Interventions, EuroIntervention
- Tier 4: JACC Heart Failure, JACC Imaging

---

## MANDATORY RESEARCH LAYER

### PubMed MCP (REQUIRED)
**NOTHING goes out without PubMed verification.**

```python
# Use MCP tools for every piece of content
pubmed_search_articles(queryTerm="SGLT2 heart failure", maxResults=10)
pubmed_fetch_contents(pmids=["12345678"])
pubmed_article_connections(sourcePmid="12345678", relationshipType="pubmed_similar_articles")
```

### AstraDB RAG (REQUIRED)
**All medical content must reference guidelines.**

- ACC Guidelines (Heart Failure, Lipids, Chest Pain)
- ESC Guidelines (All Cardiology)
- ADA Guidelines (Diabetes/Cardio)
- Medical Textbooks (Braunwald, etc.)

**8 RAG Techniques:** Vector Search, HyDE, Hybrid Retrieval, Cohere Reranking, Multi-Query, Parent-Child Chunking, Contextual Compression, Self-Query

---

## VISUAL CONTENT SYSTEM

| You Ask For | Tool | Output |
|-------------|------|--------|
| Blog header, lifestyle photo | **Fal.ai** | PNG |
| Infographic, medical illustration | **Gemini** | PNG/JPG |
| Flowchart, algorithm | **Mermaid** | SVG/PNG |
| Presentation, slides | **Marp** | PPTX/PDF |
| Data chart, trial results | **Plotly** | Interactive HTML |

```bash
# Gemini image
python skills/cardiology/gemini-imagegen/scripts/generate_image.py "description"

# Fal.ai blog image
python skills/cardiology/cardiology-visual-system/scripts/fal_image.py "description"
```

---

## VOICE STANDARDS

| Content Type | Voice | Language |
|--------------|-------|----------|
| YouTube | Peter Attia speaking Hinglish | 70% Hindi / 30% English |
| Twitter/Writing | Eric Topol Ground Truths | English |
| B2B (Doctors) | JACC editorial style | English |

### Anti-AI Guidelines
**NEVER:** "It's important to note", "In conclusion", "stands as a testament", em dash overuse, "Groundbreaking"

**ALWAYS:** Specific data, journal names, natural sentences, first-person insights, HR/NNT/CI statistics

---

## DIRECTORY STRUCTURE

```
integrated cowriting system/
├── CLAUDE.md                    # This file
├── .mcp.json                    # PubMed MCP config
├── .env                         # 35+ API keys
├── requirements.txt
│
├── skills/
│   ├── scientific/              # 135 skills
│   └── cardiology/              # 46 skills
│       ├── social-media-trends-research/  # NEW: Trend research
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       ├── trend_research.py      # CLI for trends
│       │       └── reddit_scraper.py      # No-API Reddit
│       ├── viral-content-predictor/       # ML prediction
│       │   ├── SKILL.md
│       │   ├── references/
│       │   └── scripts/analyze_content_ideas.py
│       ├── x-post-creator-skill/          # Twitter with frameworks
│       ├── cardiology-tweet-writer/       # Tweet templates
│       ├── cardiology-trial-editorial/    # Trial scoring
│       │   └── scripts/score_trial.py
│       ├── youtube-script-master/         # Hinglish scripts
│       ├── multi-model-writer/            # 6 LLM routing
│       ├── cardiology-visual-system/      # Image routing
│       └── ... (40 more)
│
├── pipelines/
│   ├── twitter-content/         # HARVEST → RESEARCH → WRITE
│   ├── journal-fetch/           # Daily digest
│   └── youtube-research/        # research-engine
│
├── research-engine/             # 35+ channel analysis
│   ├── run_pipeline.py
│   ├── scraper/
│   ├── analyzer/
│   └── calendar_generator.py
│
├── rag-pipeline/                # AstraDB RAG
│   └── src/knowledge_pipeline.py
│
├── workflows/                   # n8n/Antigravity
│   └── *.json
│
└── context-profiles/            # Voice DNA, ICP, Business
    ├── voice-dna.md
    ├── icp.md
    └── business-profile.md
```

---

## API KEYS (.env)

```env
# MANDATORY
NCBI_API_KEY=your_key              # PubMed
ASTRA_DB_API_ENDPOINT=https://...  # RAG
ASTRA_DB_APPLICATION_TOKEN=...     # RAG

# LLM (35+ configured)
ANTHROPIC_API_KEY=your_key
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key            # Gemini (FREE)
XAI_API_KEY=your_key               # Grok
ZAI_API_KEY=your_key               # GLM-4.7

# Visual
FAL_KEY=your_key
GEMINI_API_KEY=your_key

# Scraping
APIFY_API_KEY=your_key

# Optional
COHERE_API_KEY=your_key            # Reranking
PERPLEXITY_API_KEY=your_key
```

---

## SYSTEM AWARENESS (Self-Evolving Capability)

This system can **detect its own capability gaps** and propose new skills. Think of it as an HR department for your content system.

### When You Can't Do Something

When you (Claude) encounter a capability gap, log it:

```
📋 **Gap Logged**: [brief description]
Category: [category] | Urgency: [low/medium/high]
```

Or use the CLI:
```bash
python skills/cardiology/system-awareness/scripts/gap_logger.py "I need to analyze ECG images"
```

### Weekly Gap Review

```bash
# See all capability gaps
python skills/cardiology/system-awareness/scripts/gap_analyzer.py --list

# Analyze patterns and get priority report
python skills/cardiology/system-awareness/scripts/gap_analyzer.py --report

# Top 5 priority gaps to address
python skills/cardiology/system-awareness/scripts/gap_analyzer.py --top 5
```

### Propose New Skills

```bash
# Generate skill proposal from a gap
python skills/cardiology/system-awareness/scripts/skill_proposer.py --gap-id "gap_2024_001"

# Interactive skill proposal
python skills/cardiology/system-awareness/scripts/skill_proposer.py --interactive
```

### The Self-Awareness Loop

```
OBSERVE (Log gaps) → ANALYZE (Find patterns) → PROPOSE (Skill specs) → REVIEW (You approve) → BUILD → LEARN
```

**See full documentation:** `skills/cardiology/system-awareness/SKILL.md`

---

## CONTEXT WINDOW MANAGEMENT

When context < 20%:
1. STOP current work
2. Create handover.md with current state
3. Inform user
4. Wait for new session

---

## QUICK START EXAMPLES

```bash
# 1. Find trending cardiology topics
python skills/cardiology/social-media-trends-research/scripts/trend_research.py \
  --keywords "cardiology" "statins" --subreddits "cardiology"

# 2. Research a topic
# Ask: "Research GLP-1 agonists using PubMed and knowledge pipeline"

# 3. Write Twitter content
python pipelines/twitter-content/generate.py "What are statin side effects?"

# 4. YouTube research
python research-engine/run_pipeline.py --quick

# 5. Generate image
python skills/cardiology/gemini-imagegen/scripts/generate_image.py "Heart anatomy"
```

---

*This is Dr. Shailesh Singh's integrated content operating system - 181+ skills, 3 pipelines, 6 LLMs, complete social media research, all in one place.*
