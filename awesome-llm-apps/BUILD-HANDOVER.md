# BUILD HANDOVER - Awesome LLM Apps Integration

**Last Updated:** 2026-01-01
**Status:** ✅ ALL 6 SKILLS COMPLETE + SYSTEM FILES UPDATED
**Next Action:** Use the skills! System is now fully aware.

### System Files Updated (2026-01-01)
All context files now include the 6 new skills:
- ✅ CLAUDE.md - Updated (52 Cardiology Skills, 187+ total)
- ✅ GEMINI.md - Updated
- ✅ AGENTS.md - Updated
- ✅ SKILL-CATALOG.md - Updated with purpose-based lookup for all 6 new skills

---

## QUICK RESUME

After `/clear`, tell Claude:
```
Read /Users/shaileshsingh/integrated cowriting system/awesome-llm-apps/BUILD-HANDOVER.md and continue from where we left off.
```

---

## STRATEGIC CONTEXT

### Who This Is For
Dr. Shailesh Singh - Interventional Cardiologist building thought leadership through content.

### Core Principle
**AI amplifies YOU, never replaces YOU.**
- AI researches → YOU synthesize
- AI drafts → YOU refine
- AI optimizes → YOUR content gets found
- AI analyzes → YOU improve

### What We're NOT Doing
- AI voices pretending to be Dr. Singh
- AI-generated podcasts replacing his presence
- Anything that dilutes authentic human expertise

### What We ARE Doing
- Research amplification (faster, deeper research)
- SEO optimization (content gets discovered)
- Competitor analysis (know where to differentiate)
- Delivery improvement (analyze recordings for improvement)
- Multi-model scoring (better content predictions)
- Future: Multilingual accessibility narration (clearly labeled, not pretending to be him)

---

## DIRECTORY STRUCTURE (Post-Cleanup)

```
/Users/shaileshsingh/integrated cowriting system/awesome-llm-apps/
├── advanced_ai_agents/multi_agent_apps/
│   ├── agent_teams/
│   │   ├── ai_competitor_intelligence_agent_team/  → cardiology-influencer-analyzer
│   │   └── ai_seo_audit_team/                      → content-seo-optimizer
│   ├── ai_domain_deep_research_agent/              → cardiology-deep-dive-researcher
│   ├── ai_news_and_podcast_agents/beifong/         → FUTURE (voice/multilingual)
│   ├── ai_Self-Evolving_agent/                     → FUTURE (adaptive prompts)
│   ├── ai_speech_trainer_agent/                    → video-delivery-coach
│   ├── multi_agent_researcher/                     → parallel-literature-search
│   └── product_launch_intelligence_agent/          → FUTURE (drug tracking)
├── ai_agent_framework_crash_course/                → Learning patterns (sequential, parallel, loop)
├── starter_ai_agents/
│   └── mixture_of_agents/                          → ensemble-content-scorer
└── voice_ai_agents/                                → FUTURE (multilingual narration)
```

---

## 6 SKILLS TO BUILD

### Skill 1: quick-topic-researcher (was: cardiology-deep-dive-researcher)
**Status:** ✅ COMPLETE
**Priority:** 1
**Source:** `advanced_ai_agents/multi_agent_apps/ai_domain_deep_research_agent/`
**Output Location:** `skills/cardiology/quick-topic-researcher/`

**What It Does:**
- Takes a topic (e.g., "SGLT2 inhibitors in HFpEF")
- Generates 5 specific research questions
- Parallel PubMed + Perplexity search
- Outputs McKinsey-style brief in 5 minutes
- Ready for video/content prep

**Renamed to `quick-topic-researcher`** to differentiate from existing `deep-researcher` skill (which is comprehensive, file-based, 30+ min).

**Files Created:**
- `skills/cardiology/quick-topic-researcher/SKILL.md` - Full documentation
- `skills/cardiology/quick-topic-researcher/scripts/quick_research.py` - CLI script
- `skills/cardiology/quick-topic-researcher/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Use quick-topic-researcher for GLP-1 agonists in heart failure"

# CLI
python skills/cardiology/quick-topic-researcher/scripts/quick_research.py \
    --topic "GLP-1 agonists in heart failure" --domain "Cardiology"
```

**Dependencies (already have most):**
```python
pip install anthropic python-dotenv rich
```

---

### Skill 2: content-seo-optimizer
**Status:** ✅ COMPLETE
**Priority:** 2
**Source:** `advanced_ai_agents/multi_agent_apps/agent_teams/ai_seo_audit_team/`
**Output Location:** `skills/cardiology/content-seo-optimizer/`

**What It Does:**
- 3-agent pipeline: Page Auditor → SERP Analyst → Optimization Advisor
- Scrapes content, analyzes competitors, generates P0/P1/P2 recommendations
- Medical content-specific optimizations (E-E-A-T, authority signals)

**Files Created:**
- `skills/cardiology/content-seo-optimizer/SKILL.md` - Full documentation
- `skills/cardiology/content-seo-optimizer/scripts/seo_audit.py` - CLI script
- `skills/cardiology/content-seo-optimizer/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Audit SEO for https://yoursite.com/article"

# CLI
python skills/cardiology/content-seo-optimizer/scripts/seo_audit.py \
    --url "https://yoursite.com/article"
```

**Dependencies:**
```python
pip install anthropic python-dotenv rich requests beautifulsoup4
```

---

### Skill 3: influencer-analyzer
**Status:** ✅ COMPLETE
**Priority:** 3
**Source:** `advanced_ai_agents/multi_agent_apps/agent_teams/ai_competitor_intelligence_agent_team/`
**Output Location:** `skills/cardiology/influencer-analyzer/`

**What It Does:**
- Analyzes cardiology influencers (Topol, Attia, York Cardiology, Indian channels)
- Compares content strategies across multiple influencers
- Finds content gaps in the cardiology space
- Topic-specific coverage analysis
- Pre-configured influencer profiles

**Files Created:**
- `skills/cardiology/influencer-analyzer/SKILL.md` - Full documentation
- `skills/cardiology/influencer-analyzer/scripts/analyze_influencer.py` - CLI script
- `skills/cardiology/influencer-analyzer/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Analyze what Eric Topol is posting about"
"Find gaps in cardiology content"
"Compare Topol, Attia, and York Cardiology"

# CLI
python skills/cardiology/influencer-analyzer/scripts/analyze_influencer.py --name "Eric Topol"
python skills/cardiology/influencer-analyzer/scripts/analyze_influencer.py --compare "Topol,Attia"
python skills/cardiology/influencer-analyzer/scripts/analyze_influencer.py --gaps
python skills/cardiology/influencer-analyzer/scripts/analyze_influencer.py --list
```

**Dependencies (already have most):**
```python
pip install anthropic python-dotenv rich
```

---

### Skill 4: video-delivery-coach
**Status:** ✅ COMPLETE
**Priority:** 4
**Source:** `advanced_ai_agents/multi_agent_apps/ai_speech_trainer_agent/`
**Output Location:** `skills/cardiology/video-delivery-coach/`

**What It Does:**
- Analyzes video/audio recordings before publishing
- Voice: Speech rate (WPM), pitch variation, volume, filler words
- Facial: Eye contact, emotion timeline, smile detection (optional --full mode)
- 5-dimension scoring rubric (1-5 each, max 25)
- Hinglish-specific feedback (code-switching, cultural phrases)

**Files Created:**
- `skills/cardiology/video-delivery-coach/SKILL.md` - Full documentation
- `skills/cardiology/video-delivery-coach/scripts/analyze_video.py` - CLI script
- `skills/cardiology/video-delivery-coach/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Analyze my video at /path/to/recording.mp4"

# CLI - Voice only (lightweight)
python skills/cardiology/video-delivery-coach/scripts/analyze_video.py \
    --video "/path/to/video.mp4"

# CLI - Full analysis (requires heavy deps)
python skills/cardiology/video-delivery-coach/scripts/analyze_video.py \
    --video "/path/to/video.mp4" --full
```

**Dependencies:**
```python
# Core (lightweight)
pip install librosa moviepy faster-whisper anthropic rich

# Optional for --full mode
pip install opencv-python mediapipe deepface tf-keras
```

---

### Skill 5: parallel-literature-search
**Status:** ✅ COMPLETE
**Priority:** 5
**Source:** `advanced_ai_agents/multi_agent_apps/multi_agent_researcher/`
**Output Location:** `skills/cardiology/parallel-literature-search/`

**What It Does:**
- Parallel search across PubMed, Perplexity, and RAG
- Uses ThreadPoolExecutor for concurrent searches
- Synthesizes findings with citations
- 30-60 second evidence gathering

**Files Created:**
- `skills/cardiology/parallel-literature-search/SKILL.md` - Full documentation
- `skills/cardiology/parallel-literature-search/scripts/parallel_search.py` - CLI script
- `skills/cardiology/parallel-literature-search/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Parallel search: SGLT2 inhibitors in HFpEF"

# CLI
python skills/cardiology/parallel-literature-search/scripts/parallel_search.py \
    --query "SGLT2 inhibitors heart failure"
```

**Dependencies:**
```python
pip install anthropic python-dotenv rich
# PubMed/Perplexity via MCP
```

---

### Skill 6: ensemble-content-scorer
**Status:** ✅ COMPLETE
**Priority:** 6
**Source:** `starter_ai_agents/mixture_of_agents/`
**Output Location:** `skills/cardiology/ensemble-content-scorer/`

**What It Does:**
- Multi-model consensus scoring (Claude, GPT-4o, Gemini)
- Parallel API calls with ThreadPoolExecutor
- 6-dimension scoring (Relevance, Novelty, Expertise, Engagement, Shareability, Evergreen)
- Aggregated verdict with consensus analysis
- Batch scoring for multiple ideas

**Files Created:**
- `skills/cardiology/ensemble-content-scorer/SKILL.md` - Full documentation
- `skills/cardiology/ensemble-content-scorer/scripts/score_content.py` - CLI script
- `skills/cardiology/ensemble-content-scorer/requirements.txt` - Dependencies

**Usage:**
```
# In Claude Code (recommended)
"Ensemble score: Statins myth-busting for Indian audience"

# CLI - Single idea
python skills/cardiology/ensemble-content-scorer/scripts/score_content.py \
    --idea "Statins myth-busting"

# CLI - Batch scoring
python skills/cardiology/ensemble-content-scorer/scripts/score_content.py \
    --ideas "GLP-1 explained" "Statin myths" "CAC scoring"
```

**Dependencies:**
```python
pip install anthropic openai google-generativeai python-dotenv rich
```

---

## BUILD STATUS TRACKER

| # | Skill | Status | Started | Completed | Notes |
|---|-------|--------|---------|-----------|-------|
| 1 | quick-topic-researcher | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | Renamed from cardiology-deep-dive-researcher |
| 2 | content-seo-optimizer | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | 3-agent SEO pipeline |
| 3 | influencer-analyzer | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | Competitor/influencer tracking |
| 4 | video-delivery-coach | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | Voice + facial analysis |
| 5 | parallel-literature-search | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | Parallel multi-source search |
| 6 | ensemble-content-scorer | ✅ COMPLETE | 2026-01-01 | 2026-01-01 | Multi-model consensus scoring |

---

## EXISTING SYSTEM INTEGRATION POINTS

### Skills Directory
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/
```

### Skill Template Structure
Each new skill should follow this pattern:
```
skill-name/
├── SKILL.md           # Skill documentation
├── scripts/           # Python scripts
│   └── main.py
├── references/        # Reference materials
└── requirements.txt   # Dependencies
```

### Existing Skills to Integrate With
- `viral-content-predictor` → Use ensemble-content-scorer to enhance
- `research-engine` → Feed competitor insights from influencer-analyzer
- `knowledge-pipeline` → Connect parallel-literature-search output
- `youtube-script-master` → Use deep-dive-researcher for topic prep

### API Keys Location
```
/Users/shaileshsingh/integrated cowriting system/.env
```

### MCP Configuration
```
/Users/shaileshsingh/integrated cowriting system/.mcp.json
```

---

## DEPENDENCIES TO INSTALL (All Skills)

```bash
# Core frameworks
pip install agno>=2.2.10
pip install google-adk

# Research
pip install tavily-python
pip install composio-agno
pip install exa-py

# Scraping
pip install firecrawl-py>=4.6.0

# Video/Audio Analysis
pip install deepface
pip install mediapipe
pip install faster-whisper
pip install librosa

# Already have
# - anthropic, openai, google-generativeai
# - perplexity via openrouter
```

---

## API KEYS NEEDED

| Key | Purpose | Status | Cost |
|-----|---------|--------|------|
| TAVILY_API_KEY | Web search | ❌ Needed | Free tier available |
| FIRECRAWL_API_KEY | Web scraping | ❌ Needed | $19/mo, free tier |
| COMPOSIO_API_KEY | Google Docs | ❌ Needed | Free tier |
| EXA_API_KEY | Semantic search | ❌ Optional | Free tier |
| All others | Already configured | ✅ Have | - |

---

## CURRENT SESSION NOTES

### Session 1 (2026-01-01)
- Cloned awesome-llm-apps repository
- Analyzed entire codebase with 6 parallel agents
- Made strategic decision: AI amplifies, never replaces
- Identified 6 skills to build
- Cleaned up directory (200+ → 42 directories)
- User confirmed voice/audio kept for future multilingual use
- Created this handover file
- **Built Skill 1: quick-topic-researcher**
  - Studied source: `ai_domain_deep_research_agent/`
  - Renamed to differentiate from existing `deep-researcher`
  - Created SKILL.md with full documentation
  - Created CLI script `quick_research.py`
  - Uses PubMed MCP + Perplexity for parallel research
  - Outputs McKinsey-style briefs in 5 minutes
- **Built Skill 2: content-seo-optimizer**
  - Studied source: `ai_seo_audit_team/`
  - 3-agent pipeline: Page Auditor → SERP Analyst → Optimizer
  - Medical content-specific (E-E-A-T, authority signals)
  - Created SKILL.md with full documentation
  - Created CLI script `seo_audit.py` with BeautifulSoup scraping
  - Generates P0/P1/P2 prioritized recommendations
- **Built Skill 3: influencer-analyzer**
  - Studied source: `ai_competitor_intelligence_agent_team/`
  - Pre-configured profiles for Topol, Attia, York Cardiology, Dr Navin Agrawal, SAAOL (anti-pattern)
  - CLI with 4 modes: analyze, compare, gaps, topic
  - Created SKILL.md with full documentation
  - Created CLI script `analyze_influencer.py`
- **Built Skill 4: video-delivery-coach**
  - Studied source: `ai_speech_trainer_agent/`
  - Voice analysis: librosa + faster-whisper (transcription, WPM, pitch, volume, fillers)
  - Facial analysis: OpenCV + DeepFace + Mediapipe (optional --full mode)
  - 5-dimension scoring rubric with Claude coaching
  - Hinglish-specific feedback
  - Created SKILL.md, CLI script, requirements.txt
- **Built Skill 5: parallel-literature-search**
  - Studied source: `multi_agent_researcher/`
  - Parallel search: PubMed + Perplexity + RAG simultaneously
  - Uses ThreadPoolExecutor for concurrent execution
  - Synthesizes with Claude into unified report
  - Created SKILL.md, CLI script, requirements.txt
- **Built Skill 6: ensemble-content-scorer**
  - Studied source: `mixture_of_agents/`
  - Multi-model scoring: Claude + GPT-4o + Gemini in parallel
  - 6-dimension scoring with consensus aggregation
  - Batch scoring for multiple ideas
  - Created SKILL.md, CLI script, requirements.txt
- **ALL 6 SKILLS COMPLETE!**

---

## NOTES FOR NEXT SESSION

All skills have been built! To use them:

1. **quick-topic-researcher**: "Use quick-topic-researcher for GLP-1 in heart failure"
2. **content-seo-optimizer**: "Audit SEO for https://yoursite.com/article"
3. **influencer-analyzer**: "Analyze what Eric Topol is posting about"
4. **video-delivery-coach**: "Analyze my video at /path/to/recording.mp4"
5. **parallel-literature-search**: "Parallel search: SGLT2 inhibitors in HFpEF"
6. **ensemble-content-scorer**: "Ensemble score: Statins myth-busting"

---

## QUICK COMMANDS

```bash
# Navigate to project
cd "/Users/shaileshsingh/integrated cowriting system"

# Navigate to awesome-llm-apps
cd "/Users/shaileshsingh/integrated cowriting system/awesome-llm-apps"

# Navigate to cardiology skills
cd "/Users/shaileshsingh/integrated cowriting system/skills/cardiology"

# Check source for skill 1
cat "/Users/shaileshsingh/integrated cowriting system/awesome-llm-apps/advanced_ai_agents/multi_agent_apps/ai_domain_deep_research_agent/domain_deep_research.py"
```

---

*This file is the single source of truth for the awesome-llm-apps integration project.*
