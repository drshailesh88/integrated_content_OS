# Session Handover - 2026-01-01

**Session Goal:** Fix the disconnected skill awareness system and connect the HR department to main context files.

---

## QUICK RESUME

After `/clear`, tell Claude:

```
Read /Users/shaileshsingh/integrated cowriting system/SESSION-HANDOVER-2026-01-01.md and continue from where we left off.
```

---

## WHAT WE'RE BUILDING

A connected skill ecosystem where:
1. **sync_skills.py** scans disk for actual skills
2. **capability-registry.json** becomes the single source of truth
3. **generate_context.py** auto-updates CLAUDE.md, GEMINI.md, AGENTS.md, SKILL-CATALOG.md
4. The HR department (system-awareness) is connected to everything

### Architecture Diagram

```
ACTUAL SKILLS ON DISK
        │
        ▼
  sync_skills.py (auto-scanner)
        │
        ▼
capability-registry.json (SINGLE SOURCE OF TRUTH)
        │
        ▼
  generate_context.py
        │
        ├──► CLAUDE.md
        ├──► GEMINI.md
        ├──► AGENTS.md
        └──► SKILL-CATALOG.md
```

---

## COMPLETED TASKS

### 1. Built 6 New Skills from awesome-llm-apps (100% Complete)

All skills are in `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/`:

| Skill | Location | Status |
|-------|----------|--------|
| quick-topic-researcher | `skills/cardiology/quick-topic-researcher/` | ✅ Complete |
| content-seo-optimizer | `skills/cardiology/content-seo-optimizer/` | ✅ Complete |
| influencer-analyzer | `skills/cardiology/influencer-analyzer/` | ✅ Complete |
| video-delivery-coach | `skills/cardiology/video-delivery-coach/` | ✅ Complete |
| parallel-literature-search | `skills/cardiology/parallel-literature-search/` | ✅ Complete |
| ensemble-content-scorer | `skills/cardiology/ensemble-content-scorer/` | ✅ Complete |

### 2. Updated Static Context Files (100% Complete)

| File | Changes Made |
|------|-------------|
| CLAUDE.md | ✅ Updated skill count (52 cardiology, 187+ total), added Research Amplification section, added quick reference entries |
| GEMINI.md | ✅ Updated skill count, added Research Amplification section, added capabilities |
| AGENTS.md | ✅ Updated skill count, added Research Amplification section, added capabilities |
| SKILL-CATALOG.md | ✅ Added 5 new purpose-based sections, 2 new workflow templates |

### 3. Cleaned awesome-llm-apps Directory (100% Complete)

- Location: `/Users/shaileshsingh/integrated cowriting system/awesome-llm-apps/`
- Reduced from 200+ to 42 relevant directories
- Kept: Voice/audio for future multilingual, framework patterns, research agents
- Removed: Gaming, finance, travel, irrelevant domains
- Handover file: `awesome-llm-apps/BUILD-HANDOVER.md`

---

## IN PROGRESS TASKS

### 4. Update capability-registry.json (50% Complete)

**File:** `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/data/capability-registry.json`

**Done:**
- ✅ Updated metadata (version 1.1.0, dates, counts, auto_sync_enabled flag)
- ✅ Added new category "research-amplification"

**Not Done:**
- ❌ Add the 6 new skill entries to the "skills" array
- ❌ Update coverage_matrix with new skills

**Next Step:** Add these 6 skill entries after "authentic-voice" in the skills array:

```json
{
  "id": "quick-topic-researcher",
  "name": "Quick Topic Researcher",
  "category": "cardiology",
  "subcategory": "research-amplification/quick-research",
  "description": "5-min topic mastery: 5 questions → parallel PubMed search → McKinsey brief",
  "inputs": ["topic", "domain"],
  "outputs": ["research_brief", "pmids", "key_findings"],
  "dependencies": ["pubmed-database", "perplexity-search"],
  "use_cases": ["video_prep", "quick_research", "topic_mastery"],
  "coverage": ["research", "video-prep", "cardiology"],
  "has_scripts": true,
  "scripts": ["quick_research.py"],
  "complexity": "medium",
  "usage_count": 0,
  "last_used": null
},
{
  "id": "content-seo-optimizer",
  "name": "Content SEO Optimizer",
  "category": "cardiology",
  "subcategory": "research-amplification/seo",
  "description": "3-agent SEO pipeline: Page Auditor → SERP Analyst → Optimizer with P0/P1/P2 recommendations",
  "inputs": ["url", "keyword"],
  "outputs": ["seo_audit", "competitor_analysis", "prioritized_fixes"],
  "dependencies": [],
  "use_cases": ["seo_audit", "content_optimization", "organic_reach"],
  "coverage": ["seo", "content-optimization", "marketing"],
  "has_scripts": true,
  "scripts": ["seo_audit.py"],
  "complexity": "high",
  "usage_count": 0,
  "last_used": null
},
{
  "id": "influencer-analyzer",
  "name": "Influencer Analyzer",
  "category": "cardiology",
  "subcategory": "research-amplification/competitor-analysis",
  "description": "Track Topol/Attia/competitors, find content gaps, compare strategies",
  "inputs": ["influencer_name", "platform", "comparison_list"],
  "outputs": ["content_analysis", "gap_report", "recommendations"],
  "dependencies": ["perplexity-search"],
  "use_cases": ["competitor_tracking", "gap_analysis", "content_strategy"],
  "coverage": ["competitor-analysis", "content-strategy", "cardiology"],
  "has_scripts": true,
  "scripts": ["analyze_influencer.py"],
  "complexity": "medium",
  "usage_count": 0,
  "last_used": null
},
{
  "id": "video-delivery-coach",
  "name": "Video Delivery Coach",
  "category": "cardiology",
  "subcategory": "research-amplification/delivery-coaching",
  "description": "Analyze video recordings: voice (WPM, pitch, fillers), facial (optional), 5-dimension scoring",
  "inputs": ["video_path", "full_analysis_flag"],
  "outputs": ["voice_analysis", "facial_analysis", "coaching_feedback", "score"],
  "dependencies": [],
  "use_cases": ["video_improvement", "delivery_coaching", "hinglish_delivery"],
  "coverage": ["video", "coaching", "improvement"],
  "has_scripts": true,
  "scripts": ["analyze_video.py"],
  "complexity": "high",
  "usage_count": 0,
  "last_used": null
},
{
  "id": "parallel-literature-search",
  "name": "Parallel Literature Search",
  "category": "cardiology",
  "subcategory": "research-amplification/quick-research",
  "description": "PubMed + Perplexity + RAG in parallel, 30-second evidence gathering",
  "inputs": ["query", "sources"],
  "outputs": ["unified_findings", "citations", "synthesis"],
  "dependencies": ["pubmed-database", "perplexity-search", "knowledge-pipeline"],
  "use_cases": ["evidence_gathering", "parallel_search", "research"],
  "coverage": ["research", "literature", "evidence"],
  "has_scripts": true,
  "scripts": ["parallel_search.py"],
  "complexity": "medium",
  "usage_count": 0,
  "last_used": null
},
{
  "id": "ensemble-content-scorer",
  "name": "Ensemble Content Scorer",
  "category": "cardiology",
  "subcategory": "research-amplification/scoring",
  "description": "Multi-model consensus scoring (Claude + GPT + Gemini) for content ideas",
  "inputs": ["content_idea", "ideas_batch"],
  "outputs": ["consensus_score", "model_scores", "verdict", "recommendations"],
  "dependencies": ["multi-model-writer"],
  "use_cases": ["content_scoring", "idea_validation", "viral_prediction"],
  "coverage": ["scoring", "content-strategy", "multi-model"],
  "has_scripts": true,
  "scripts": ["score_content.py"],
  "complexity": "medium",
  "usage_count": 0,
  "last_used": null
}
```

---

## PENDING TASKS

### 5. Build sync_skills.py (0% Complete)

**Location to create:** `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/sync_skills.py`

**Purpose:** Auto-discover skills from disk and update capability-registry.json

**Functionality:**
1. Scan `skills/cardiology/` and `skills/scientific/` for directories with SKILL.md
2. Parse each SKILL.md for metadata (name, description, inputs, outputs)
3. Update capability-registry.json with discovered skills
4. Report: new skills found, missing skills, changes

### 6. Build generate_context.py (0% Complete)

**Location to create:** `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/generate_context.py`

**Purpose:** Regenerate skill sections in context files from capability-registry.json

**Functionality:**
1. Read capability-registry.json
2. Generate skill inventory markdown tables
3. Update relevant sections in CLAUDE.md, GEMINI.md, AGENTS.md
4. Update SKILL-CATALOG.md with purpose-based routing

### 7. Update system-awareness SKILL.md (0% Complete)

Add documentation for the new connected workflow:
- How sync_skills.py works
- How generate_context.py works
- The full pipeline from disk → registry → context files

### 8. Test Full Pipeline (0% Complete)

Run the complete flow:
1. Add a test skill directory
2. Run sync_skills.py
3. Verify capability-registry.json updated
4. Run generate_context.py
5. Verify context files updated
6. Remove test skill

---

## FILE LOCATIONS

| File | Path |
|------|------|
| This Handover | `/Users/shaileshsingh/integrated cowriting system/SESSION-HANDOVER-2026-01-01.md` |
| capability-registry.json | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/data/capability-registry.json` |
| system-awareness SKILL.md | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/SKILL.md` |
| CLAUDE.md | `/Users/shaileshsingh/integrated cowriting system/CLAUDE.md` |
| SKILL-CATALOG.md | `/Users/shaileshsingh/integrated cowriting system/SKILL-CATALOG.md` |
| awesome-llm-apps handover | `/Users/shaileshsingh/integrated cowriting system/awesome-llm-apps/BUILD-HANDOVER.md` |

---

## SKILL COUNTS (Current State)

| Location | Actual Count | Documented Count |
|----------|--------------|------------------|
| skills/cardiology/ | ~56 directories | 52 in CLAUDE.md |
| skills/scientific/ | 135 directories | 135 in CLAUDE.md |
| capability-registry.json | 15 sample entries | Should have all |

---

## NEXT STEPS (In Order)

1. **Complete capability-registry.json update** - Add the 6 new skill entries (JSON above)
2. **Build sync_skills.py** - Auto-discovery script
3. **Build generate_context.py** - Context file regeneration
4. **Update system-awareness SKILL.md** - Document new workflow
5. **Test the pipeline** - End-to-end verification

---

## CONTEXT FOR CLAUDE

The user is Dr. Shailesh Singh, an interventional cardiologist building a thought leadership content system. Key principles:

- **AI amplifies, never replaces** - No fake voices, no AI pretending to be him
- **Connected systems** - HR department should feed context files automatically
- **Single source of truth** - capability-registry.json is the master

The awesome-llm-apps repository was cloned to extract useful patterns. 6 skills were built from it. Now we're connecting the skill awareness system so new skills are auto-discovered.

---

*Session paused: 2026-01-01*
*Resume by reading this file and continuing from "NEXT STEPS"*
