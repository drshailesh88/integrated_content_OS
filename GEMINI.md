# Dr. Shailesh Singh - Integrated Content Operating System

**Single Source of Truth** for all content creation, research, and writing.
Works with: Antigravity, VS Code, Cursor, Claude Code, **Gemini CLI**.

---

## ACTIVE PROJECT HANDOVERS

> **Check these first if resuming multi-session work:**

| Project | Handover File | Status |
|---------|---------------|--------|
| **Carousel Generator v2** | `CAROUSEL-V2-VISUAL-OVERHAUL-HANDOVER.md` | ✅ COMPLETE - Production Ready |
| **Infographic System** | `INFOGRAPHIC-SYSTEM-HANDOVER.md` | ✅ COMPLETE - Production Ready |

*To resume: Read the handover file first, then continue from "Current Progress" section.*

---

## GEMINI: YOUR ROLE IN THIS SYSTEM

> **CONTEXT FOR GEMINI CLI**
> You are Gemini, operating as a **parallel writer** in this integrated content system. You share this codebase with Claude Code. The user may switch between you and Claude on-demand based on availability, cost, or task fit.
>
> **YOUR STRENGTHS:** Long-context processing, research synthesis, fact-checking, image generation via native API.
>
> **AUTHENTICATION:** You are running on the user's **Gemini Advanced Pro subscription** (OAuth login via `gemini auth login`), NOT API billing. No API key is used for your operation.
>
> **SKILL ROUTING:** See `SKILL-CATALOG.md` for purpose-based skill lookup ("I want to do X → use skill Y").

---

## COORDINATION WITH CLAUDE CODE

### On-Demand Switching Model
The user runs **both Gemini CLI and Claude Code** and switches based on:
- Whichever terminal is free
- Task fit (you excel at research, long documents)
- All models run on Pro subscriptions (no per-token billing)

### Avoiding Conflicts
1. **Check before writing:** If working on a file, check if it was recently modified
2. **Announce your work:** Start by stating what file/task you're working on
3. **Use handover.md:** If stopping mid-task, update `handover.md` with current state
4. **Respect ownership:** If Claude is mid-task on a file, wait or work on something else

### When to Use Gemini (You) vs Claude
| Task | Best Model | Why |
|------|-----------|-----|
| Research synthesis | **Gemini** | Long context, fact-checking |
| Newsletter drafts | **Gemini** | 1M token context for research |
| Image generation | **Gemini** | Native Gemini API |
| Fact-checking content | **Gemini** | Grounded in search |
| YouTube scripts (Hinglish) | Claude | Voice training in CLAUDE.md |
| Twitter threads | Either | Both work well |
| Code editing/debugging | Claude | Better tool use |
| Trial editorials | Either | Both trained on voice |

---

## WHAT YOU CAN DO (Complete Capabilities)

| Capability | How | Skills/Tools |
|------------|-----|--------------|
| **Write YouTube Scripts** | Hinglish, Peter Attia style | `youtube-script-master`, `hook-generator` |
| **Write Twitter Content** | Eric Topol + Ground Truths | `x-post-creator-skill`, `cardiology-tweet-writer` |
| **Write Newsletters** | Topol style, anti-AI | `cardiology-newsletter-writer`, `medical-newsletter-writer` |
| **Write Editorials** | JACC style, trial analysis | `cardiology-editorial`, `cardiology-trial-editorial` |
| **Research PubMed** | Python scripts (MCP may differ) | `pubmed-database`, NCBI API |
| **Research Guidelines** | RAG from AstraDB | `knowledge-pipeline`, ACC/ESC/ADA |
| **Find Trending Topics** | Google Trends, Reddit, Perplexity | `social-media-trends-research` |
| **Predict Viral Content** | ML scoring | `viral-content-predictor` |
| **Generate Images** | Blog headers, infographics, animated viz | `infographic-generator` (6 templates), `antv_infographic` (200+ templates), `vizzu_animations` (animated data), `g2_charts` (grammar-based), `lida_quick_viz` (prototyping), `gemini-imagegen` (YOUR native tool) |
| **Long Document Writing** | Chapters, deep research | `academic-chapter-writer`, `deep-researcher` |
| **Quick Topic Research** | 5-min McKinsey brief | `quick-topic-researcher` |
| **Track Competitors** | Topol/Attia/Indian channels | `influencer-analyzer` |
| **Optimize SEO** | 3-agent P0/P1/P2 audit | `content-seo-optimizer` |
| **Score Content Ideas** | Multi-model consensus | `ensemble-content-scorer` |

---

## QUICK REFERENCE: COMMON TASKS

### "Research [topic] thoroughly"
```bash
# Use your strength: long-context research synthesis
# Read multiple skill files, combine knowledge

# 1. Check PubMed
python rag-pipeline/src/knowledge_pipeline.py --query "topic"

# 2. Read relevant skills
cat skills/cardiology/knowledge-pipeline/SKILL.md

# 3. Synthesize into comprehensive brief
```

### "Write a newsletter about [topic]"
→ Read `skills/cardiology/cardiology-newsletter-writer/SKILL.md`
→ Use Eric Topol voice from `context-profiles/voice-dna.md`
→ Follow anti-AI guidelines (no "it's important to note", no em dashes)

### "Write a YouTube script"
→ Read `skills/cardiology/youtube-script-master/SKILL.md`
→ 70% Hindi / 30% English (Hinglish)
→ Peter Attia style, warm authority

### "Generate an image"
```bash
# You have native Gemini image generation
python skills/cardiology/gemini-imagegen/scripts/generate_image.py "description"
```

### "Find what's trending"
```bash
python skills/cardiology/social-media-trends-research/scripts/trend_research.py \
  --keywords "cardiology" "heart health" --subreddits "cardiology"
```

---

## VOICE STANDARDS (CRITICAL)

| Content Type | Voice | Language |
|--------------|-------|----------|
| YouTube | Peter Attia speaking Hinglish | 70% Hindi / 30% English |
| Twitter/Writing | Eric Topol Ground Truths | English |
| B2B (Doctors) | JACC editorial style | English |

### Anti-AI Guidelines (MANDATORY)
**NEVER USE:**
- "It's important to note"
- "In conclusion"
- "stands as a testament"
- "Groundbreaking", "game-changing"
- Excessive em dashes (—)
- "delve", "leverage", "landscape"

**ALWAYS USE:**
- Specific data (HR 0.82, 95% CI 0.71-0.94)
- Journal names (NEJM, Lancet, JACC)
- Natural sentence flow
- First-person insights where appropriate

### Voice Reference Files
- `context-profiles/voice-dna.md` - Complete voice DNA
- `context-profiles/icp.md` - 6 audience archetypes
- `context-profiles/business-profile.md` - Channel strategy

---

## COMPLETE SKILLS INVENTORY (193+ Skills)

**NEW:** 4 visualization frameworks integrated (AntV Infographic, Vizzu, G2, LIDA)

### Cardiology Skills (59 Skills)
**Location:** `skills/cardiology/`


#### YouTube & Hinglish Content
| Skill | Purpose |
|-------|---------|
| `cardiology-youtube-scriptwriter` | Complete workflow from "Hello" to finished script. Combin... |
| `debunk-script-writer` | > Location: `/.claude/skills/youtube-script-master/SKILL.... |
| `hook-generator` | Metadata - Name: hook-generator - Version: 1.0 - Purpose:... |
| `youtube-script-hinglish` | > Location: `/.claude/skills/youtube-script-master/SKILL.... |
| `youtube-script-master` | Data-driven Hinglish YouTube scripts (15-30 min) |

#### Twitter/X & Social Media
| Skill | Purpose |
|-------|---------|
| `cardiology-content-repurposer` | Overview |
| `cardiology-tweet-writer` | Simplified tweet generation with seed + modifier permutation |
| `cremieux-cardio` | You're a cardiologist with a point of view, writing for s... |
| `twitter-longform-medical` | Write data-driven, evidence-first long-form Twitter conte... |
| `x-post-creator-skill` | Twitter thought leadership with frameworks (batches of 10) |

#### Newsletters & Editorials
| Skill | Purpose |
|-------|---------|
| `academic-chapter-writer` | Transform topics into publishable textbook chapters with ... |
| `cardiology-editorial` | This skill transforms you into a specialized cardiology e... |
| `cardiology-newsletter-writer` | Newsletter creation with Topol style + anti-AI guidelines |
| `cardiology-science-for-people` | Write rigorous cardiology science that real people actual... |
| `cardiology-topol-writer` | Transform unstructured thought dumps into polished cardio... |
| `cardiology-trial-editorial` | Landmark trial editorials with scoring + infographics |
| `cardiology-writer` | Transform unstructured thought dumps into polished cardio... |
| `medical-newsletter-writer` | Create high-quality, evidence-based medical newsletters i... |

#### Research & Discovery
| Skill | Purpose |
|-------|---------|
| `citation-management` | Systematic citation management for accurate referencing i... |
| `clinicaltrials-database` | Query the U.S. National Library of Medicine's clinical tr... |
| `content-marketing-social-listening` | Overview |
| `content-research-writer` | This skill acts as your writing partner, helping you rese... |
| `content-trend-researcher` | A comprehensive content research and analysis skill desig... |
| `deep-researcher` | Comprehensive research methodology with file-based tracki... |
| `knowledge-pipeline` | RAG system for AstraDB guidelines + PubMed synthesis |
| `literature-review` | Comprehensive, systematic literature reviews following ri... |
| `perplexity-search` | Overview |
| `research-synthesizer` | Metadata - Name: research-synthesizer - Version: 1.0 - Pu... |
| `social-media-trends-research` | Zero-cost trend research using pytrends + Reddit + Perple... |
| `viral-content-predictor` | ML-based viral potential scoring (0-100) |

#### Research Amplification
| Skill | Purpose |
|-------|---------|
| `content-seo-optimizer` | 3-agent SEO pipeline: scrapes content → analyzes SERP → P... |
| `ensemble-content-scorer` | Multi-model consensus scoring: Claude + GPT-4o + Gemini s... |
| `influencer-analyzer` | Track Topol, Attia, York Cardiology, Indian channels. Dis... |
| `parallel-literature-search` | Parallel search across PubMed + Perplexity + RAG. All sou... |
| `quick-topic-researcher` | 5-min topic mastery: generates 5 questions → parallel Pub... |
| `research-paper-extractor` | Extract structured data from cardiology research paper PD... |
| `video-delivery-coach` | Analyze video recordings: voice (pace, pitch), facial (em... |

#### Quality & Voice
| Skill | Purpose |
|-------|---------|
| `authentic-voice` | AI detection avoidance and human-sounding content verific... |
| `content-reflection` | A rigorous pre-publication review system that evaluates c... |
| `scientific-critical-thinking` | Systematic evaluation of research rigor through methodolo... |

#### Visual Content
| Skill | Purpose |
|-------|---------|
| `cardiology-visual-system` | Intelligent routing to optimal visual tool (Fal.ai, Gemin... |
| `carousel-generator` | Generate branded Instagram carousels (1080x1080px) from t... |
| `carousel-generator-v2` | World-class Instagram carousel generator with AI content ... |
| `gemini-imagegen` | Generate and edit images using Google's Gemini API. The e... |
| `infographic-generator` | Publication-grade infographics from the visual-design-system templates |

#### Multi-Model & Utilities
| Skill | Purpose |
|-------|---------|
| `article-extractor` | This skill extracts the main content from web articles an... |
| `browser-automation` | Use your ChatGPT Plus and Gemini Advanced subscriptions t... |
| `content-os` | The "produce everything" button. Give one seed idea → get... |
| `mcp-management` | Skill for managing and interacting with Model Context Pro... |
| `multi-model-writer` | Unified routing to 6 LLM models (Claude, GPT, Gemini, Gro... |
| `system-awareness` | Philosophy |

#### Other
| Skill | Purpose |
|-------|---------|
| `analyze-ecg-waveforms-uploaded` | Analyze ECG waveforms from uploaded images to detect arrh... |
| `clinical-decision-support` | Generate professional clinical decision support documents... |
| `clinical-reports` | Professional clinical documentation covering case reports... |
| `peer-review` | Systematic framework for conducting rigorous peer review ... |
| `scientific-writing` | Core skill for producing research manuscripts, evidence-b... |
| `statistical-analysis` | Rigorous statistical analysis guidance for interpreting a... |
| `transcribe-audio-podcast-interviews` | Transcribe audio from podcast interviews |
| `visual-design-system` | Purpose: Publication-grade design tokens and utilities fo... |
| `youtube-comment-analyzer` | Trigger phrases: - "Analyze comments for [URL]" - "Analyz... |

### Scientific Skills (134 Skills)
**Location:** `skills/scientific/`

Located in `skills/scientific/`

**Databases:** alphafold-database, biorxiv-database, brenda-database, chembl-database, clinicaltrials-database, clinpgx-database, clinvar-database, cosmic-database, drugbank-database, ena-database, ensembl-database, fda-database, gene-database, geo-database, gwas-database, hmdb-database

**Bioinformatics:** anndata, biomni, biopython, bioservices, latchbio-integration, scanpy, scikit-bio, scvi-tools

**Data Science:** dask, geopandas, plotly, pytorch-lightning, scikit-learn, scikit-survival, statsmodels, torch_geometric, torchdrug

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

### 2. YouTube Research Pipeline
**Location:** `research-engine/`

```bash
python run_pipeline.py          # Full (30 min)
python run_pipeline.py --quick  # Quick (10 min)
python calendar_generator.py --show-next 5
```

**35+ Tracked Channels** across competition, inspiration, and belief-seeders.

**8 Dangerous Narratives:** ldl_skepticism, statin_fear, insulin_primacy, fasting_absolutism, supplement_superiority, seed_oil_villain, exercise_compensation, fear_mongering

### 3. Journal Fetching Pipeline
**Location:** `pipelines/journal-fetch/`

**20+ Journals:** NEJM, Lancet, JAMA, BMJ, JACC, Circulation, EHJ, etc.

---

## RAG & RESEARCH INFRASTRUCTURE

### Knowledge Pipeline
```bash
# Query the RAG system
python rag-pipeline/src/knowledge_pipeline.py --query "SGLT2 inhibitors heart failure"
```

**Sources:**
- ACC Guidelines (Heart Failure, Lipids, Chest Pain)
- ESC Guidelines (All Cardiology)
- ADA Guidelines (Diabetes/Cardio)
- Medical Textbooks (Braunwald, etc.)

**Techniques:** Vector Search, HyDE, Hybrid Retrieval, Cohere Reranking, Multi-Query

### PubMed Research
```bash
# Use the pubmed skill
python skills/scientific/pubmed-database/scripts/search.py --query "statin therapy" --max 10
```

---

## DIRECTORY STRUCTURE

```
integrated cowriting system/
├── CLAUDE.md                    # Claude Code context
├── GEMINI.md                    # THIS FILE - Gemini CLI context
├── SKILL-CATALOG.md             # Skill routing guide
├── .env                         # 35+ API keys
├── requirements.txt
│
├── skills/
│   ├── scientific/              # 135 skills
│   └── cardiology/              # 46 skills
│       ├── youtube-script-master/
│       ├── x-post-creator-skill/
│       ├── cardiology-newsletter-writer/
│       ├── gemini-imagegen/           # Your native image tool
│       ├── knowledge-pipeline/
│       └── ... (40 more)
│
├── pipelines/
│   ├── twitter-content/
│   ├── journal-fetch/
│   └── youtube-research/
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
├── context-profiles/            # Voice DNA, ICP, Business
│   ├── voice-dna.md
│   ├── icp.md
│   └── business-profile.md
│
└── handover.md                  # Session state (CHECK THIS FIRST)
```

---

## AUTHENTICATION

### Your Login (Gemini CLI)
You operate on the user's **Gemini Advanced Pro subscription**, authenticated via OAuth:
```bash
# Already authenticated - no action needed
gemini auth login  # If re-auth needed, opens browser for Google account
```

**You do NOT use `GOOGLE_API_KEY` or `GEMINI_API_KEY` for your operation.** Those keys in `.env` are only for Python scripts that call the Gemini API directly (like `gemini-imagegen`).

### API Keys in .env (For Python Scripts Only)
These environment variables are used by **research pipelines and scripts**, not by your CLI:

```env
# Research Infrastructure (used by Python scripts)
NCBI_API_KEY                    # PubMed API for knowledge-pipeline
ASTRA_DB_API_ENDPOINT           # RAG vector database
ASTRA_DB_APPLICATION_TOKEN      # RAG authentication

# Image Generation Scripts
GOOGLE_API_KEY                  # For gemini-imagegen Python script
FAL_KEY                         # For fal.ai image generation

# Multi-Model Router (for multi-model-writer skill)
ANTHROPIC_API_KEY               # Claude API
OPENAI_API_KEY                  # GPT API
OPENROUTER_API_KEY              # Multiple models

# Scraping
APIFY_API_KEY                   # Twitter scraping
```

**Key distinction:**
- **Gemini CLI (you)** = Pro subscription via OAuth
- **Python scripts** = API keys from .env

---

## GEMINI-SPECIFIC STRENGTHS TO LEVERAGE

### 1. Long Context (1M tokens)
You can process entire skill directories at once:
```bash
# Read multiple files for deep context
cat skills/cardiology/*/SKILL.md
```

### 2. Grounded Research
Use your search grounding for fact-checking:
- Verify statistics before including them
- Cross-reference with multiple sources
- Flag any conflicting data

### 3. Native Image Generation
```bash
python skills/cardiology/gemini-imagegen/scripts/generate_image.py "Heart anatomy infographic"
```

### 4. Code Execution
You can run Python scripts directly like Claude Code.

---

## SESSION MANAGEMENT

### Starting a Session
1. **Check handover.md first** - See if Claude left any in-progress work
2. **Read SKILL-CATALOG.md** - For task routing
3. **Ask what to work on** - User directs the task

### Ending a Session / Switching to Claude
1. **Update handover.md** with current state
2. **List any incomplete tasks**
3. **Save any generated content** to appropriate location

### Handover Format
```markdown
## Session: [Date/Time]
**Model:** Gemini CLI

### Completed
- [x] Task 1
- [x] Task 2

### In Progress
- [ ] Task 3 - stopped at: [description]
  - File: path/to/file
  - Next step: [what to do next]

### Notes for Claude
- [Any context needed]
```

---

## FRESH MACHINE SETUP (REQUIRED FOR PUBMED MCP)

1. Create `.env` from `.env.example` and set `NCBI_API_KEY`.
2. Install PubMed MCP dependencies:
   ```bash
   cd pubmed-mcp-server
   npm install
   ```
3. MCP config is already wired in `.mcp.json` and points to `pubmed-mcp-server/dist/index.js`.

---

## QUICK START EXAMPLES

```bash
# 1. Find trending cardiology topics
python skills/cardiology/social-media-trends-research/scripts/trend_research.py \
  --keywords "cardiology" "statins" --subreddits "cardiology"

# 2. Generate a newsletter draft
# Read the skill first
cat skills/cardiology/cardiology-newsletter-writer/SKILL.md
# Then write following the guidelines

# 3. Research a topic deeply
python rag-pipeline/src/knowledge_pipeline.py --query "GLP-1 agonists"

# 4. Generate an image (your native strength)
python skills/cardiology/gemini-imagegen/scripts/generate_image.py "Heart anatomy"

# 5. Check what Claude was working on
cat handover.md
```

---

## IMPORTANT REMINDERS

1. **Always check handover.md** at session start
2. **Follow voice standards** - No AI-sounding phrases
3. **Update handover.md** when stopping mid-task
4. **Use your strengths** - Long context, research, images
5. **Coordinate with Claude** - Don't overwrite active work

---

*This is Dr. Shailesh Singh's integrated content operating system. You (Gemini) are a parallel writer alongside Claude Code, running on a Gemini Advanced Pro subscription. Use your strengths: long context, research synthesis, and image generation.*
