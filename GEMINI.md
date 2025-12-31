# Dr. Shailesh Singh - Integrated Content Operating System

**Single Source of Truth** for all content creation, research, and writing.
Works with: Antigravity, VS Code, Cursor, Claude Code, **Gemini CLI**.

---

## GEMINI: YOUR ROLE IN THIS SYSTEM

> **CONTEXT FOR GEMINI CLI**
> You are Gemini, operating as a **parallel writer** in this integrated content system. You share this codebase with Claude Code. The user may switch between you and Claude on-demand based on availability, cost, or task fit.
>
> **YOUR STRENGTHS:** Long-context processing, research synthesis, fact-checking, free tier availability, image generation via native API.
>
> **SKILL ROUTING:** See `SKILL-CATALOG.md` for purpose-based skill lookup ("I want to do X → use skill Y").

---

## COORDINATION WITH CLAUDE CODE

### On-Demand Switching Model
The user runs **both Gemini CLI and Claude Code** and switches based on:
- Whichever terminal is free
- Cost optimization (you have free tier)
- Task fit (you excel at research, long documents)

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
| **Generate Images** | Blog headers, infographics | `gemini-imagegen` (YOUR native tool) |
| **Long Document Writing** | Chapters, deep research | `academic-chapter-writer`, `deep-researcher` |

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

## COMPLETE SKILLS INVENTORY (181+ Skills)

### Cardiology Skills (46 Skills)
**Location:** `skills/cardiology/`

#### YouTube & Hinglish Content
| Skill | Purpose |
|-------|---------|
| `youtube-script-master` | Data-driven Hinglish scripts, 15-30 min |
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
| `cardiology-content-repurposer` | Multi-platform adaptation |

#### Newsletters & Editorials
| Skill | Purpose |
|-------|---------|
| `cardiology-newsletter-writer` | Newsletter + anti-AI guidelines |
| `medical-newsletter-writer` | Topol style guide + workflow |
| `cardiology-editorial` | Eric Topol style, hybrid scoring |
| `cardiology-trial-editorial` | Trial analysis + scoring script |
| `cardiology-topol-writer` | Transform thought dumps |
| `academic-chapter-writer` | 5,000-15,000 word chapters (YOUR STRENGTH) |
| `cardiology-science-for-people` | General audience writing |

#### Research & Discovery
| Skill | Purpose |
|-------|---------|
| `social-media-trends-research` | pytrends + Reddit + Perplexity |
| `viral-content-predictor` | ML prediction + analysis |
| `knowledge-pipeline` | RAG + PubMed synthesis |
| `deep-researcher` | Multi-layered research (YOUR STRENGTH) |
| `perplexity-search` | AI-powered web search |
| `literature-review` | Systematic reviews |

#### Quality & Voice
| Skill | Purpose |
|-------|---------|
| `authentic-voice` | AI detection elimination |
| `content-reflection` | Pre-publish QA |

#### Visual Content
| Skill | Purpose |
|-------|---------|
| `cardiology-visual-system` | Auto-routes to best tool |
| `gemini-imagegen` | Gemini API images (YOUR NATIVE TOOL) |

### Scientific Skills (135 Skills)
**Location:** `skills/scientific/`

**Databases:** alphafold, biorxiv, chembl, clinicaltrials, clinvar, cosmic, drugbank, ensembl, gnomad, gwas-catalog, kegg, pdb, pubmed, reactome, string, uniprot

**Bioinformatics:** biopython, scanpy, anndata, cellxgene-census, deepchem, genomics-tools

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

## API KEYS (.env)

You have access to these via environment variables:

```env
# MANDATORY
NCBI_API_KEY                    # PubMed
GOOGLE_API_KEY                  # Gemini (YOUR API)
ASTRA_DB_API_ENDPOINT           # RAG
ASTRA_DB_APPLICATION_TOKEN      # RAG

# Other LLMs (for multi-model-writer)
ANTHROPIC_API_KEY               # Claude
OPENAI_API_KEY                  # GPT
OPENROUTER_API_KEY              # Multiple models

# Visual
FAL_KEY                         # Fal.ai
GEMINI_API_KEY                  # Gemini images (YOU)

# Scraping
APIFY_API_KEY                   # Twitter scraping
```

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

*This is Dr. Shailesh Singh's integrated content operating system. You (Gemini) are a parallel writer alongside Claude Code. Use your strengths: long context, research synthesis, image generation, and free tier availability.*
