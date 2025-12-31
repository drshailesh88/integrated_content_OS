# COMPREHENSIVE HANDOVER - Integrated Content Operating System
**Last Updated:** 2025-12-31
**Sessions:** System Integration → Environment Setup → **Multi-LLM Setup**

---

## LATEST SESSION: Multi-LLM Parallel Writing Setup (2025-12-31)

### What Was Accomplished

#### 1. Created GEMINI.md for Gemini CLI ✅

Created parallel context file for Gemini CLI at `GEMINI.md`:
- Same skills, pipelines, voice standards as CLAUDE.md
- Added coordination section for working alongside Claude Code
- Highlighted Gemini-specific strengths (long context, research, images)
- Added session management and handover protocols

#### 2. Multi-LLM Coordination System ✅

| Model | Context File | Strengths |
|-------|-------------|-----------|
| **Claude Code** | `CLAUDE.md` | Tool use, code editing, YouTube scripts |
| **Gemini CLI** | `GEMINI.md` | Research, long docs, images, free tier |
| **Codex CLI** | `AGENTS.md` | Script execution, structured content, batch generation |

**Switching Model:** On-demand - use whichever is available/appropriate

#### 4. Created AGENTS.md for Codex CLI ✅

Converted Codex from code-only to content writer:
- Same skills, pipelines, voice standards
- Explicit instruction that it's a WRITER not coder
- Highlighted its strengths: script execution, structured output, batch processing
- Coordination with Claude and Gemini

#### 3. Created Sync Script ✅

`scripts/sync_llm_contexts.py` - Keeps CLAUDE.md and GEMINI.md in sync:
```bash
python scripts/sync_llm_contexts.py --check          # Check sync status
python scripts/sync_llm_contexts.py --show-diff      # Show differences
python scripts/sync_llm_contexts.py --update-gemini  # Sync from CLAUDE.md
```

**Sections that sync:** Skills, Pipelines, Directory Structure, Voice Standards, API Keys
**Sections that DON'T sync:** Model-specific instructions, coordination, strengths

---

## MULTI-LLM COORDINATION (3 MODELS)

### How It Works
1. **Claude Code, Gemini CLI, and Codex CLI** can all be used in parallel
2. **Check this handover.md** at the start of any session
3. **Update handover.md** when switching or stopping mid-task
4. **Don't overwrite** files another model is actively editing

### The Three Writers

| Model | Context File | Cost | Strengths |
|-------|-------------|------|-----------|
| **Claude Code** | `CLAUDE.md` | $20/mo Pro | Voice accuracy, tool use, YouTube scripts |
| **Gemini CLI** | `GEMINI.md` | FREE / $20 Pro | Long context, research, images |
| **Codex CLI** | `AGENTS.md` | $20/mo (ChatGPT Pro) | Script execution, structured content, batch |

### Task Routing Suggestions

| Task | Best Model | Why |
|------|-----------|-----|
| YouTube scripts (Hinglish) | Claude | Voice training |
| Research synthesis | Gemini | 1M token context, grounding |
| Newsletter drafts | Gemini | Long document handling |
| Image generation | Gemini | Native API |
| Structured editorials | **Codex** | Analytical, tables, data |
| Batch tweet generation | **Codex** | Efficient bulk output |
| Script execution | **Codex** | Code execution ability |
| Code editing | Claude | Better tool use |
| Twitter threads | Any | All capable |
| Trial analysis | Codex or Claude | Both trained |

### Handover Format (When Switching)
```markdown
## Active Work: [Date/Time]
**Model:** [Claude/Gemini]

### Completed
- [x] Task 1

### In Progress
- [ ] Task 2 - stopped at: [description]
  - File: path/to/file
  - Next step: [what to do]
```

---

## PREVIOUS SESSION: Environment & Security Setup (2025-12-29)

### What Was Accomplished

#### 1. Environment Variables Configured ✅

Created `.env` with **35 configuration values** covering all services:

| Category | Keys Added |
|----------|------------|
| **LLM Providers** | Anthropic (2), OpenAI, OpenRouter (2), Gemini (2), xAI, Groq, Perplexity, Cohere |
| **Research** | NCBI/PubMed, AstraDB (4 params), Tavily |
| **Data/Automation** | Airtable (2), Apify, Bright Data, Supadata |
| **YouTube/Video** | YouTube API (2), FAL.AI |
| **Development** | GitHub, LangSmith (+ tracing config) |
| **Email** | Gmail SMTP (user + app password) |
| **Browser Automation** | ChatGPT email, Gemini email |

#### 2. Security Infrastructure Created ✅

- **Created `.gitignore`** - Protects `.env` and other secrets from git commits
- **File permissions** set to owner-only (`-rw-------`)

#### 3. Security Audit Completed ✅

Ran multi-agent security scan (4 parallel haiku agents) to find exposed secrets.

**Findings Fixed:**
| File | Issue | Resolution |
|------|-------|------------|
| `workflows/BUILD-THIS-PROJECT.md` | Real OpenRouter, Slack, NCBI keys exposed | Replaced with placeholders |
| `workflows/MEDICAL-CONTENT-ENGINE-SPEC.md` | Real API keys + hardcoded email | Replaced with `${VAR_NAME}` references |
| Code examples in docs | Hardcoded email addresses | Changed to `os.getenv()` pattern |

**Safe (No Action Needed):**
- All Python/JS code already uses `os.getenv()` correctly
- `.mcp.json` uses `${NCBI_API_KEY}` placeholder correctly
- `.env.example` contains only template placeholders

#### 4. User Decisions Made

- **Slack integration:** Will NOT be used (to be changed later)
- **API key method:** User provided keys via conversation (acceptable for dev keys)
- **Gmail SMTP:** App password added for email workflows

---

## SOURCE OF TRUTH

**SINGLE LOCATION:** `/Users/shaileshsingh/integrated cowriting system/`

This directory is now the **ONLY** place for all content creation, research, and writing tools. Works with Antigravity, VS Code, Cursor, and Claude Code.

**Master Instructions:** Read `CLAUDE.md` first - contains complete system documentation.

---

## WHAT WAS ACCOMPLISHED THIS SESSION

### 1. Full System Integration Complete ✅

Consolidated 40+ scattered directories into ONE unified system:

| Component | Source | Destination | Status |
|-----------|--------|-------------|--------|
| 135 Scientific Skills | `Downloads/claude-scientific-skills-main.zip` | `skills/scientific/` | ✅ Installed |
| 33 Cardiology Skills | `Downloads/*.skill` + `cowriting system/.claude/skills/` | `skills/cardiology/` | ✅ Installed |
| Twitter Pipeline | `new twitter content system/` | `pipelines/twitter-content/` | ✅ Copied |
| YouTube Research | `cowriting system/research-engine/` | `research-engine/` | ✅ Copied |
| RAG Pipeline | `cowriting system/rag-pipeline/` | `rag-pipeline/` | ✅ Copied |
| Antigravity Workflows | `fetch journal articles/workflows/` | `workflows/` | ✅ Copied |
| Context Profiles | `cowriting system/context-profiles/` | `context-profiles/` | ✅ Copied |
| PubMed MCP | Configuration created | `.mcp.json` | ✅ Configured |

### 2. Created Master CLAUDE.md ✅

Comprehensive documentation covering:
- System architecture diagram
- All 3 pipelines (Twitter, YouTube, Journal)
- PubMed MCP integration (MANDATORY)
- AstraDB RAG integration (MANDATORY)
- All 168 skills documented
- Content workflows
- API keys required
- Anti-AI guidelines
- Quick start guide

### 3. Directory Structure Created ✅

```
integrated cowriting system/
├── CLAUDE.md                    # Master instructions
├── .mcp.json                    # PubMed MCP config
├── .env.example                 # API keys template
├── requirements.txt             # Dependencies
├── skills/
│   ├── scientific/              # 135 skills (alphafold, biopython, etc.)
│   └── cardiology/              # 33 skills (youtube-script-master, etc.)
├── pipelines/
│   └── twitter-content/         # Tweet fetching & generation
├── research-engine/             # YouTube research (35+ channels)
├── rag-pipeline/                # AstraDB RAG (8 techniques)
├── workflows/                   # 4 Antigravity/n8n workflows
└── context-profiles/            # Voice DNA, ICP, business profile
```

---

## USER DECISIONS MADE (CRITICAL)

### What User WANTS:
1. ✅ PubMed MCP - **MANDATORY** for all content (no citation management needed separately)
2. ✅ AstraDB RAG - **MANDATORY** for guidelines/textbooks
3. ✅ Tweet Fetching System - via Apify (8 medical influencers)
4. ✅ Journal Fetching - via Antigravity workflows (20+ journals)
5. ✅ YouTube Research System - 35+ channels, 8 narratives tracked
6. ✅ ALL 135 Scientific Skills from GitHub repo
7. ✅ ALL Cardiology Skills (33 total)
8. ✅ This directory as SINGLE SOURCE OF TRUTH
9. ✅ Works with Antigravity, VS Code, Cursor

### What User DOES NOT WANT:
1. ❌ DeepResearch Draft Auditor - NOT needed
2. ❌ Medical Ghostwriter's memory/citation features - NOT needed
3. ❌ Separate hallucination detection - NOT needed (PubMed provides real citations)

---

## SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTEGRATED CONTENT OPERATING SYSTEM                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐           │
│  │  TWITTER SYSTEM  │  │  YOUTUBE SYSTEM  │  │  JOURNAL SYSTEM  │           │
│  │  Apify Scraping  │  │  35+ Channels    │  │  20+ Journals    │           │
│  │  8 Influencers   │  │  8 Narratives    │  │  B2C/B2B Triage  │           │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘           │
│           │                     │                     │                      │
│           └─────────────────────┼─────────────────────┘                      │
│                                 │                                            │
│                    ┌────────────▼────────────┐                               │
│                    │     RESEARCH LAYER      │                               │
│                    ├─────────────────────────┤                               │
│                    │  PubMed MCP (MANDATORY) │                               │
│                    │  AstraDB RAG (MANDATORY)│                               │
│                    └────────────┬────────────┘                               │
│                                 │                                            │
│                    ┌────────────▼────────────┐                               │
│                    │     168 SKILLS          │                               │
│                    │  135 Scientific         │                               │
│                    │  33 Cardiology          │                               │
│                    └─────────────────────────┘                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## VOICE STANDARDS (Important)

| Content Type | Voice Model | Language |
|--------------|-------------|----------|
| YouTube | Peter Attia speaking Hinglish | 70% Hindi / 30% English |
| Twitter/Writing | Eric Topol Ground Truths | English |
| B2B (Doctors) | JACC editorial style | English |

---

## WHAT IS PENDING

### 1. Environment Setup ✅ COMPLETE
- [x] Created `.env` with 35 configuration values
- [x] Created `.gitignore` to protect secrets
- [x] Security audit completed - all exposed secrets fixed
- [x] Gmail SMTP configured with app password

### 2. Test Pipelines
- [ ] Test Twitter pipeline: `python pipelines/twitter-content/generate.py "test question"`
- [ ] Test YouTube research: `python research-engine/run_pipeline.py --quick`
- [ ] Test RAG pipeline: Import and run knowledge_pipeline
- [ ] Test Antigravity workflows in n8n

### 3. Potential Cleanup (User Decision Required)
- [ ] Delete old redundant directories (40+ scattered across system)
- [ ] User to confirm which old directories can be deleted

### 4. Refinements (Future)
- [ ] Refine skills as needed
- [ ] Add custom slash commands
- [ ] Set up daily automation schedules
- [ ] Replace Slack integration with alternative (user decision pending)

---

## KEY FILES TO READ

| File | Purpose |
|------|---------|
| `CLAUDE.md` | **READ FIRST** - Complete system documentation |
| `.env` | All 35 API keys and configuration (PROTECTED - in .gitignore) |
| `.gitignore` | Protects secrets from git commits |
| `.mcp.json` | PubMed MCP server configuration |
| `.env.example` | Template for required API keys |
| `workflows/MEDICAL-CONTENT-ENGINE-SPEC.md` | Journal fetching spec |
| `workflows/PROJECT-SPEC-TWITTER-CONTENT-SYSTEM.md` | Twitter system spec |
| `context-profiles/voice-dna.md` | Voice guidelines |

---

## ORIGINAL DIRECTORIES (For Reference)

These were the source directories for the integration:

| Directory | What Was Taken | Status |
|-----------|----------------|--------|
| `/Users/shaileshsingh/cowriting system/` | Research engine, RAG, skills, context profiles | Integrated ✅ |
| `/Users/shaileshsingh/new twitter content system/` | Twitter pipeline | Integrated ✅ |
| `/Users/shaileshsingh/fetch journal articles/` | Antigravity workflows, specs | Integrated ✅ |
| `/Users/shaileshsingh/Downloads/claude-scientific-skills-main.zip` | 135 scientific skills | Extracted ✅ |
| `/Users/shaileshsingh/Downloads/*.skill` | 8 cardiology skill files | Copied ✅ |
| `/Users/shaileshsingh/pubmed-mcp-server/` | MCP server (referenced in .mcp.json) | Configured ✅ |

---

## PIPELINES SUMMARY

### 1. Twitter Content Pipeline
**Location:** `pipelines/twitter-content/`
**Flow:** HARVEST → RESEARCH → SYNTHESIZE → WRITE
**Files:** harvester.py, researcher.py, synthesizer.py, writer.py, pipeline.py
**Usage:**
```bash
python pipelines/twitter-content/generate.py "Your question"
python pipelines/twitter-content/main.py harvest
```

### 2. YouTube Research Pipeline
**Location:** `research-engine/`
**Components:** Channel scraper, comment scraper, demand signals, narrative monitor, gap finder, view predictor, calendar generator
**Usage:**
```bash
python research-engine/run_pipeline.py --quick
python research-engine/analyzer/narrative_monitor.py --debunk
```

### 3. Journal Fetching Pipeline
**Location:** `workflows/` (Antigravity/n8n JSON files)
**Workflows:**
- unified-twitter-content-pipeline.json
- medical-content-engine.json
- medical-content-engine-v2.json
- medical-journal-digest.json

---

## SKILLS INVENTORY

### Scientific Skills (135) - `skills/scientific/`
Databases, bioinformatics, data science, lab tools including:
- alphafold-database, biopython, biorxiv-database, chembl-database
- clinicaltrials-database, clinvar-database, pubmed-database
- deepchem, scanpy, pytorch, scikit-learn, and 125+ more

### Cardiology Skills (33) - `skills/cardiology/`
- **YouTube:** youtube-script-master, youtube-script-hinglish, debunk-script-writer, hook-generator
- **Writing:** cardiology-editorial, cardiology-newsletter-writer, cardiology-trial-editorial, x-post-creator-skill
- **Research:** pubmed-database, clinicaltrials-database, literature-review, citation-management
- **Quality:** authentic-voice, content-reflection, scientific-critical-thinking

---

## HOW TO CONTINUE NEXT SESSION

```
1. Open: /Users/shaileshsingh/integrated cowriting system/
2. Read: CLAUDE.md (master instructions)
3. Read: handover.md (this file)
4. Set up: .env file with API keys
5. Test: Run pipelines to verify everything works
6. Optionally: Confirm deletion of old directories
```

---

## CRITICAL REMINDERS

1. **PubMed MCP is MANDATORY** - Nothing goes out without PubMed verification
2. **AstraDB RAG is MANDATORY** - All content must reference knowledge base
3. **This is the SINGLE SOURCE OF TRUTH** - Don't create content elsewhere
4. **Works with:** Antigravity, VS Code, Cursor, Claude Code
5. **168 Skills available** - 135 scientific + 33 cardiology

---

## CONTEXT WINDOW PROTOCOL

When context < 20%:
1. STOP current work
2. Create comprehensive handover.md
3. Inform user
4. Wait for new session

---

## SESSION HISTORY

| Date | Session | Key Accomplishments |
|------|---------|---------------------|
| 2025-12-29 | System Integration | Consolidated 40+ directories, created CLAUDE.md, installed 168 skills |
| 2025-12-29 | Environment & Security | Created .env (35 keys), .gitignore, security audit, fixed exposed secrets |
| 2025-12-31 | Multi-LLM Setup | Created GEMINI.md + AGENTS.md, 3-model parallel system, sync script |

---

**End of Handover**
*Last Updated: 2025-12-31*
*Latest Session: Multi-LLM Parallel Writing Setup*
*Next: Test Gemini CLI with GEMINI.md, test pipelines, explore parallel writing workflows*
