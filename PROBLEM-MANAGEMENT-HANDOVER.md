# Problem Management Handover

**Last Updated**: 2026-01-02
**Status**: Active Problem Tracking
**Total Issues Identified**: 85+

---

## QUICK REFERENCE: Critical Blockers

| # | Problem | Location | Severity | Fix Time | Status |
|---|---------|----------|----------|----------|--------|
| 1 | PubMed MCP never called from skills | 30+ skills | CRITICAL | 8 hrs | Open |
| 2 | HR scripts have hardcoded Mac paths | system-awareness/scripts/ | CRITICAL | 1 hr | Open |
| 3 | Twitter pipeline import paths broken | pipelines/twitter-content/ | CRITICAL | 30 min | Open |
| 4 | visual_router.py type mismatch crash | carousel-generator-v2 | CRITICAL | 30 min | Open |
| 5 | Duplicate token systems (colors) | visual-design-system vs carousel-v2 | HIGH | 2 hrs | Open |

---

## TABLE OF CONTENTS

1. [PubMed MCP Integration Issues](#1-pubmed-mcp-integration-issues)
2. [Content Engine Issues](#2-content-engine-issues)
3. [Cardiology Skills Issues](#3-cardiology-skills-issues)
4. [HR Department (System-Awareness) Issues](#4-hr-department-issues)
5. [Visual Design System Issues](#5-visual-design-system-issues)
6. [Carousel Generator Issues](#6-carousel-generator-issues)
7. [Scientific Skills Issues](#7-scientific-skills-issues)
8. [Pipeline Integration Issues](#8-pipeline-integration-issues)
9. [Change Log](#9-change-log)

---

## 1. PUBMED MCP INTEGRATION ISSUES

### Summary
- **MCP Server Status**: Built and configured correctly
- **Skills Claiming PubMed**: 38 skills (67%)
- **Skills Actually Using PubMed**: 1 (journal-fetch pipeline only)
- **Skills with Stubbed/Fake PubMed**: 4 (use simulation instead)

### Critical Gap: No Python-to-MCP Bridge

The PubMed MCP server is built (`pubmed-mcp-server/dist/index.js`) but NO skill actually calls it from Python automation.

**Available MCP Tools (5):**
- `pubmed_search_articles`
- `pubmed_fetch_contents`
- `pubmed_article_connections`
- `pubmed_research_agent`
- `pubmed_generate_chart`

### Skills Claiming PubMed But NOT Implementing It

| Skill | File:Line | Claim | Reality |
|-------|-----------|-------|---------|
| cardiology-newsletter-writer | SKILL.md:39-42 | Uses PubMed MCP | No scripts, manual only |
| cardiology-trial-editorial | SKILL.md:139 | "ALWAYS use PubMed" | score_trial.py has no API calls |
| cardiology-editorial | SKILL.md:139,374-375 | PubMed integration | Zero scripts exist |
| youtube-script-master | SKILL.md:3 | RAG + PubMed | No implementation |
| knowledge-pipeline | SKILL.md | PubMed synthesis | Architecture only, no code |
| quick-topic-researcher | scripts/quick_research.py:93-96 | MCP calls | Falls back to simulation |
| parallel-literature-search | scripts/parallel_search.py:90-143 | PubMed search | SIMULATION ONLY |
| hooks_generator.py | :267-269 | PubMed stats | TODO comment, returns empty |
| carousel_employee.py | :344 | pubmed_search | Commented out, never runs |
| deep-researcher | SKILL.md | PubMed MCP | Documentation only |
| pubmed-database | SKILL.md | PubMed wrapper | **Ironic: dedicated skill, no code** |

### Files Using Fake Data Instead of Real PubMed

| File | Line | Issue |
|------|------|-------|
| `parallel-literature-search/scripts/parallel_search.py` | 91-143 | `search_pubmed_simulation()` - fakes results |
| `quick-topic-researcher/scripts/quick_research.py` | 133-144 | CLI mode uses Claude's knowledge, not API |
| `carousel-generator-v2/scripts/hooks_generator.py` | 267-271 | Returns empty TopicStats |

### Working Implementation (Exception)

`pipelines/journal-fetch/fetchers/pubmed_fetcher.py` uses direct NCBI E-utilities API (not MCP) and works.

### Action Items

- [ ] P0: Create Python-to-MCP bridge utility
- [ ] P0: Implement actual PubMed calls in hooks_generator.py
- [ ] P1: Replace parallel_search.py simulation with real API
- [ ] P1: Wire quick_research.py to use MCP
- [ ] P2: Audit all 38 claiming skills and document which need real integration

---

## 2. CONTENT ENGINE ISSUES

### Content Database

| Issue | Location | Severity |
|-------|----------|----------|
| Only 9 topics covered | content_database.py:674-709 | Medium |
| Missing: PCSK9, ARNI, ezetimibe, bempedoic acid, inclisiran | - | Medium |
| Statistics too verbose for slides | content_database.py:89-96 | Low |
| Sources missing PMIDs | content_database.py:115 | Medium |

### Hooks Generator

| Issue | Location | Severity |
|-------|----------|----------|
| PubMed integration stubbed | hooks_generator.py:267-269 | HIGH |
| Normalized topic never passed | hooks_generator.py:389-390,445 | Medium |
| Quality score weights authority too low | hooks_generator.py:284-326 | Low |
| A/B variations don't use best hooks | hooks_generator.py:479-536 | Low |

### Content Structurer

| Issue | Location | Severity |
|-------|----------|----------|
| PubMed never called | content_structurer.py:27-40 | HIGH |
| Longform extraction too simple | content_structurer.py:428-453 | Medium |
| Topic normalization incomplete | content_structurer.py:487-504 | Low |

---

## 3. CARDIOLOGY SKILLS ISSUES

### Summary Statistics
- **Total Skills**: 61
- **With scripts/ directory**: 20 (33%)
- **With references/ directory**: 27 (44%)
- **Documentation-only (no scripts)**: 30+ skills

### Skills with Deprecated Naming (lowercase skill.md)

| Skill | Status | Action |
|-------|--------|--------|
| debunk-script-writer | Integrated into youtube-script-master | Mark deprecated |
| hook-generator | Integrated into youtube-script-master | Mark deprecated |
| research-synthesizer | Superseded | Mark deprecated |
| youtube-script-hinglish | Superseded by youtube-script-master | Mark deprecated |

### Skills Missing Implementation

These have SKILL.md but NO scripts:

| Skill | Purpose | Priority |
|-------|---------|----------|
| clinical-decision-support | GRADE evidence CDS | Medium |
| clinical-reports | Professional documentation | Medium |
| peer-review | Systematic peer review | Low |
| scientific-writing | Research manuscripts | Low |
| academic-chapter-writer | Textbook chapters | Low |
| cardiology-writer | Thought dumps → content | Low |
| literature-review | Systematic reviews | Medium |
| citation-management | Reference management | Low |
| article-extractor | Web article extraction | Low |
| browser-automation | ChatGPT/Gemini browser | Low |
| youtube-comment-analyzer | Comment analysis | Medium |

### Skills with Missing Reference Files

| Skill | Missing Files | Impact |
|-------|---------------|--------|
| x-post-creator-skill | seed-ideas.md, modifiers.md, copywriting-frameworks.md | HIGH - workflow broken |
| cardiology-tweet-writer | seed-ideas.md, modifiers.md, feedback-log.md | HIGH - workflow broken |

### Duplicate/Confusing Skills

| Skills | Issue |
|--------|-------|
| cardiology-writer + cardiology-topol-writer | Similar purpose, unclear difference |
| carousel-generator + carousel-generator-v2 | v1 still exists, no deprecation notice |
| quick-topic-researcher + content-trend-researcher | Overlapping purpose |

---

## 4. HR DEPARTMENT ISSUES

### System-Awareness Skill Status

**Overall**: 70% Complete - core gap logging works, skill building blocked

### Working Components (Steps 1-3)

| Script | Status | Lines | Function |
|--------|--------|-------|----------|
| gap_logger.py | WORKING | 287 | Log capability gaps |
| gap_analyzer.py | WORKING | 373 | Analyze and prioritize |
| skill_proposer.py | WORKING | 423 | Generate skill proposals |

### Broken Components (Steps 4-7)

| Script | Issue | Line | Fix Required |
|--------|-------|------|--------------|
| skill_builder.py | Hardcoded Mac path | 33-35 | Change to relative path |
| sync_skills.py | Hardcoded Mac path | 46-49 | Change to relative path |
| generate_context.py | Hardcoded Mac path | 29,33-36 | Change to relative path |

**Current Broken Path:**
```python
SKILLS_ROOT = Path("/Users/shaileshsingh/integrated cowriting system/skills")
```

**Should Be:**
```python
SKILLS_ROOT = Path(__file__).parent.parent.parent.parent / "skills"
```

### Data Files Status

| File | Status | Notes |
|------|--------|-------|
| gap-log.json | Working | 4 gaps logged, categories assigned |
| capability-registry.json | Working | 193 skills registered |
| skill-backlog.json | Exists | Not actively used |
| skill-templates/ | Working | Proposal workflow functional |

---

## 5. VISUAL DESIGN SYSTEM ISSUES

### Token Inconsistency (CRITICAL)

| Token File | Navy Color | Primary | Issue |
|------------|------------|---------|-------|
| visual-design-system/tokens/colors.json | #1e3a5f | #16697A | Different values |
| carousel-generator-v2/tokens/brand-tokens.json | #16697A | #16697A | Different source |

**Action**: Merge into single source of truth

### Duplicate Image Generation Code

| Location | Lines | Model | Issue |
|----------|-------|-------|-------|
| cardiology-visual-system/scripts/gemini_infographic.py | 278 | gemini-2.0-flash-exp | Implementation A |
| gemini-imagegen/SKILL.md | - | gemini-2.0-flash-exp | Different doc |
| carousel-generator-v2 | - | Implied | Third copy |

**Action**: Consolidate into single implementation

### Manim Issues

| Issue | Location | Severity |
|-------|----------|----------|
| Return type bug | render_manim.py:46 | HIGH |
| Manim not in global Python | System | Medium |
| No wrapper script | - | Low |

**Fix for render_manim.py:46:**
```python
# Current (wrong):
return str(candidate) if candidate.exists() else (None, False), False

# Fixed:
return (str(candidate), False) if candidate.exists() else (None, False)
```

### Icon Manifest Incomplete

| Metric | Count | Issue |
|--------|-------|-------|
| SVG files available | 251 | - |
| Icons in manifest | 51 | 200 icons not catalogued |
| cardiology-curated/ | Empty | Directory exists but unused |

### Fragile Imports in cardiology-visual-system

| File | Line | Issue |
|------|------|-------|
| plotly_charts.py | 37-51 | Path construction fragile |
| gemini_infographic.py | - | No __init__.py for proper import |
| fal_image.py | - | Medical safeguards not reused elsewhere |

---

## 6. CAROUSEL GENERATOR ISSUES

### React/Puppeteer Renderer

| Issue | Location | Severity |
|-------|----------|----------|
| Vite startup race condition | render.js:26-70 | Medium |
| Static build fallback broken | render.js:95-113 | HIGH |
| 800ms hardcoded delay | render.js:143 | Low |
| Puppeteer profile pollution | render.js:239-260 | Low |

### Python Bridge

| Issue | Location | Severity |
|-------|----------|----------|
| Icon normalization incomplete (~15 icons) | puppeteer_renderer.py:84-109 | Medium |
| Context/source split fragile | puppeteer_renderer.py:111-127 | Medium |
| Quote icon unvalidated | puppeteer_renderer.py:219 | Low |
| 60s timeout too short | puppeteer_renderer.py:319 | Medium |

### Quality Checker (CRITICAL BUGS)

| Issue | Location | Severity |
|-------|----------|----------|
| **check_anti_ai() type mismatch** | quality_checker.py:93 vs visual_router.py:654 | CRITICAL |
| Anti-AI regex false positives | quality_checker.py:51-52 | Medium |
| Em-dash detection too strict | quality_checker.py:103-105 | Low |
| Only 3 checks in run_all_checks() | quality_checker.py:181-214 | Medium |

**Type Mismatch Fix:**
```python
# visual_router.py:654 calls:
checker.check_anti_ai(slide)  # SlideContent object

# quality_checker.py:93 expects:
def check_anti_ai(text: str)  # String

# Fix: Extract text from slide first
checker.check_anti_ai(slide.get_text())
```

### Visual Router

| Issue | Location | Severity |
|-------|----------|----------|
| **render_line_chart() MISSING** | visual_router.py:330-382 | CRITICAL |
| Satori availability check weak | visual_router.py:94-114 | Low |
| Exception handling too broad | visual_router.py:650,662 | Medium |

---

## 7. SCIENTIFIC SKILLS ISSUES

### Summary Statistics
- **Total Skills**: 135
- **With SKILL.md**: 134 (99.3%)
- **With scripts/**: 63 (47%)
- **With references/**: 129 (96%)

### Integration Gap

Only 1 cardiology skill references scientific skills (system-awareness). 134 scientific skills are effectively orphaned from the cardiology content system.

### Skills Needing Verification

| Skill | Lines | Issue |
|-------|-------|-------|
| PyHealth | 178 | Clinical NLP, minimal docs |
| PyDicom | 179 | DICOM imaging, stub only |
| Pymoo | 181 | Multi-objective optimization, minimal |
| adaptyv | 114 | Cloud lab, API-only |
| transformers | 157 | Basic HuggingFace wrapper |

### Documentation-Only Skills (70+ skills)

These have SKILL.md but no scripts/ - may be intentional for wrapper libraries but needs verification.

---

## 8. PIPELINE INTEGRATION ISSUES

### Twitter Content Pipeline (BROKEN)

| Issue | Location | Fix |
|-------|----------|-----|
| Import paths broken | main.py:32-34 | Change `from src.xxx` to `from xxx` |
| Files not in src/ | Root level | Either move files or fix imports |

### Journal Fetch Pipeline

| Issue | Location | Fix |
|-------|----------|-----|
| dotenv missing | main.py:28 | `pip install python-dotenv` |

### Research Engine (ISOLATED)

- Not integrated with twitter-content or journal-fetch
- Uses OpenRouter instead of same LLM routing
- Content gap analysis not fed into content generation

### RAG Pipeline (ORPHANED)

- Complete advanced retrieval exists
- Twitter-content uses direct HTTP client instead
- No hybrid retrieval used in pipelines

### Missing Dependencies (System-Wide)

```bash
pip install typer rich anthropic openai astrapy feedparser scrapetube python-dotenv
```

---

## 9. CHANGE LOG

### 2026-01-02 - Initial Assessment

**Created by**: Claude Code Session
**Branch**: claude/finish-visual-system-dSlJh

**Analysis Completed:**
- [x] PubMed MCP integration audit
- [x] All 61 cardiology skills reviewed
- [x] HR department (system-awareness) analyzed
- [x] Visual/design skills evaluated
- [x] 135 scientific skills catalogued
- [x] Pipeline integration checked

**Critical Issues Identified:**
1. PubMed MCP built but never called (30+ skills affected)
2. HR scripts hardcoded to Mac paths (3 scripts broken)
3. Twitter pipeline import paths broken
4. visual_router.py type mismatch crashes quality checks
5. Duplicate token systems cause brand inconsistency

**Files Created:**
- `PROBLEM-MANAGEMENT-HANDOVER.md` (this file)

---

## PRIORITY MATRIX

### P0 - Fix Immediately (Crashes/Blockers)

| # | Issue | File | Time |
|---|-------|------|------|
| 1 | visual_router.py type mismatch | :654 | 30 min |
| 2 | render_line_chart() missing | :330 | 2 hrs |
| 3 | HR scripts hardcoded paths | 3 files | 1 hr |
| 4 | Twitter pipeline imports | main.py | 30 min |
| 5 | render_manim.py tuple bug | :46 | 10 min |

### P1 - Fix This Sprint (Core Functionality)

| # | Issue | Impact | Time |
|---|-------|--------|------|
| 1 | Wire PubMed MCP to skills | No real research data | 8 hrs |
| 2 | Merge token systems | Brand inconsistency | 2 hrs |
| 3 | Install system dependencies | Pipelines fail | 30 min |
| 4 | Fix x-post-creator references | Workflow broken | 1 hr |

### P2 - Fix This Month (Quality)

| # | Issue | Impact | Time |
|---|-------|--------|------|
| 1 | Expand content database | Limited topics | 4 hrs |
| 2 | Consolidate image generation | Code duplication | 3 hrs |
| 3 | Complete icon manifest | 200 icons unmapped | 2 hrs |
| 4 | Mark deprecated skills | Confusion | 1 hr |

### P3 - Backlog (Nice to Have)

| # | Issue | Impact |
|---|-------|--------|
| 1 | Wire scientific skills to cardiology | Feature gap |
| 2 | Add missing skill scripts | Documentation-only |
| 3 | Create integration tests | Quality assurance |
| 4 | Unify LLM routing | Architecture cleanup |

---

## HOW TO USE THIS DOCUMENT

### When Fixing Issues

1. Find the issue in the relevant section
2. Note the file:line reference
3. Make the fix
4. Update the Change Log with:
   - Date
   - What was fixed
   - Files modified
   - New status (Fixed/Partial/Blocked)

### When Discovering New Issues

1. Add to the appropriate section
2. Include file:line reference
3. Assign severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Add to Priority Matrix if P0/P1
5. Log in Change Log

### Weekly Review

1. Check P0 items - should be 0
2. Review P1 progress
3. Promote P2 items if capacity
4. Update statistics in Quick Reference

---

*This document tracks all identified problems in the integrated content OS. Update it as issues are fixed or new ones discovered.*
