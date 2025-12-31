# Skill Catalog: Purpose-Based Lookup

**Last Updated:** 2025-12-29

> When you want to do X, use skill Y. This is Claude's reference for routing your requests to the right skill.

---

## Quick Lookup: "I want to..."

### Write a TWEET / X Post

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Single tweet with references | `x-post-creator-skill` | 6 frameworks + citations, Eric Topol voice |
| Batch of 10 tweets | `cardiology-tweet-writer` | Seeds × modifiers system, feedback loop |
| Data-heavy long post (2000+ chars) | `cremieux-cardio` | Evidence-first, 3-4 studies deep, Rajesh persona |
| Thread (5-10 tweets) | `twitter-longform-medical` | Topol + Cremieux synthesis, with visuals |

**Default choice:** `x-post-creator-skill` for single posts, `cardiology-tweet-writer` for batch generation.

---

### Write a NEWSLETTER

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Patient-facing newsletter | `medical-newsletter-writer` | PDF trend analysis, engagement prediction, Topol voice |
| Doctor-facing newsletter | `cardiology-newsletter-writer` | Topic discovery, deeper technical content |

**Default choice:** `medical-newsletter-writer` for B2C, `cardiology-newsletter-writer` for B2B.

---

### Write an EDITORIAL / Opinion Piece

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| 500-word trial commentary | `cardiology-editorial` | Hybrid scoring (rules + LLM), full/abstract workflows |
| Trial discovery + editorial + infographic | `cardiology-trial-editorial` | Includes importance scoring, HTML visual |
| Transform rough thoughts into polished piece | `cardiology-topol-writer` | Thought dump → structured editorial |

**Default choice:** `cardiology-editorial` for quick takes, `cardiology-trial-editorial` for comprehensive trial coverage.

---

### Write a YOUTUBE SCRIPT

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Data-driven Hinglish script | `youtube-script-master` | **PRIMARY** - Uses research-engine data, 6-point voice check |
| Script from seeds + modifiers | `cardiology-youtube-scriptwriter` | Alternative approach, social listening integrated |

**Default choice:** `youtube-script-master` - it's the unified, data-driven approach.

---

### Write LONG-FORM Content

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Textbook chapter (5,000-15,000 words) | `academic-chapter-writer` | Vancouver citations, approval workflow |
| Science for general audience | `cardiology-science-for-people` | Rigorous but accessible, statistics translated |
| General cardiology content | `cardiology-writer` | Flexible, all-purpose |

---

### RESEARCH a Topic

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| PubMed search (direct API) | `pubmed-database` | MeSH terms, field tags, citation export |
| RAG + PubMed parallel | `knowledge-pipeline` | Vector search + BM25 + reranking, guidelines included |
| Comprehensive 6-step research | `deep-researcher` | Definition → exploratory → deep dive → validation → synthesis |
| Real-time web search | `perplexity-search` | AI-powered, multiple models, current events |
| Clinical trials search | `clinicaltrials-database` | ClinicalTrials.gov API |

**Default choice:** Always start with `PubMed MCP tools` (mandatory), then `knowledge-pipeline` for RAG synthesis.

---

### Find TRENDING Topics

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Programmatic trends (Google/Reddit) | `social-media-trends-research` | pytrends + Reddit scraper + Perplexity |
| Multi-platform viral patterns | `content-marketing-social-listening` | 10+ platforms, knowledge gaps, demand scoring |
| Platform-specific with outlines | `content-trend-researcher` | Intent analysis, generates content outlines |

**Default choice:** `social-media-trends-research` for quick trend check, `content-trend-researcher` for content planning.

---

### POLISH / Improve Content

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Remove AI tells | `authentic-voice` | 5 deadly patterns, vocabulary swaps, humanization |
| Pre-publish QA | `content-reflection` | 6 dimensions: rigor, voice, positioning, audience, risk, engagement |
| Evidence quality check | `scientific-critical-thinking` | GRADE framework, bias detection, logical fallacies |
| Full manuscript review | `peer-review` | 7-stage systematic review, CONSORT/STROBE compliance |
| Statistical validation | `statistical-analysis` | Effect sizes, CI, NNT/NNH, clinical vs statistical significance |

**Default polish chain:** `authentic-voice` → `content-reflection` → `scientific-critical-thinking`

---

### REPURPOSE Content

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Multi-format adaptation | `cardiology-content-repurposer` | 4A framework, articles → tweets → threads → blogs |

---

### Generate VISUALS

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Auto-route to best tool | `cardiology-visual-system` | Routes to Fal.ai/Gemini/Mermaid/Plotly based on request |
| Photo-realistic images | → Fal.ai | Blog headers, lifestyle photos |
| Infographics, illustrations | → Gemini | Medical illustrations, educational graphics |
| Flowcharts, algorithms | → Mermaid | Clinical pathways, decision trees |
| Data charts | → Plotly | Trial results, statistics |
| Instagram carousels | `content-os` | 1080x1080px carousel generator |

**Default choice:** Just describe what you want - `cardiology-visual-system` auto-routes.

---

### Use OTHER AI Models

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Route to GPT-4o, Gemini, Grok, GLM | `multi-model-writer` | 6 LLM routing, cost-optimized |
| Use ChatGPT Plus / Gemini Advanced | `browser-automation` | Playwright MCP, web interface automation |

---

### Analyze CONTENT Performance

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Predict viral potential | `viral-content-predictor` | ML scoring, trend research, content blueprint |
| Analyze YouTube comments | `youtube-comment-analyzer` | Scrape 2000+ comments, free LLM analysis |

---

### Counter MISINFORMATION

| If you want... | Use this skill | Notes |
|----------------|----------------|-------|
| Debunk dangerous narratives | `debunk-script-writer` | 8 narratives: LDL skepticism, statin fear, etc. |

---

## Workflow Templates (Optional)

Use these when you want a structured approach. Skip them when you want to work freeform.

### Newsletter Workflow
```
1. RESEARCH
   - PubMed MCP → find recent evidence
   - knowledge-pipeline → pull guideline context

2. DRAFT
   - medical-newsletter-writer (B2C) or cardiology-newsletter-writer (B2B)

3. POLISH
   - authentic-voice → remove AI patterns

4. FACT-CHECK
   - scientific-critical-thinking → verify claims

5. FINAL QA
   - content-reflection → pre-publish check
```

### Twitter Content Workflow
```
1. TREND CHECK (optional)
   - social-media-trends-research → what's hot

2. RESEARCH
   - PubMed MCP → mandatory citations
   - knowledge-pipeline → guideline context

3. WRITE
   - x-post-creator-skill (single) or cardiology-tweet-writer (batch)

4. POLISH
   - authentic-voice → humanize
```

### Editorial Workflow
```
1. FIND TRIAL
   - cardiology-trial-editorial → discovery + importance scoring

2. RESEARCH
   - PubMed MCP → related studies
   - pubmed_article_connections → similar articles, citations

3. WRITE
   - cardiology-editorial → 500-word commentary

4. VISUAL (optional)
   - cardiology-visual-system → infographic

5. FACT-CHECK
   - scientific-critical-thinking → evidence quality
```

### YouTube Script Workflow
```
1. RESEARCH PHASE
   - research-engine → run_pipeline.py --quick
   - viral-content-predictor → score topic

2. WRITE
   - youtube-script-master → Hinglish script

3. POLISH
   - authentic-voice → natural speech patterns
   - content-reflection → audience fit check
```

---

## Scientific Skills Quick Reference

These 135 skills in `skills/scientific/` are specialized. Key ones for content work:

| Skill | When to use |
|-------|-------------|
| `peer-review` | Full manuscript critique, 7-stage systematic review |
| `scientific-critical-thinking` | Evaluate evidence quality, detect bias, GRADE framework |
| `literature-review` | Systematic reviews, PICO framework, thematic synthesis |
| `statistical-analysis` | Interpret trial statistics, effect sizes, clinical significance |
| `scientific-writing` | IMRAD structure, reporting guidelines (CONSORT, STROBE) |
| `citation-management` | Format references (AMA, Vancouver, APA, BibTeX) |

---

## Overlap Resolution Guide

When multiple skills could work, here's how to choose:

### YouTube Scripts
- **youtube-script-master**: When you have research-engine data, want data-driven approach
- **cardiology-youtube-scriptwriter**: When starting from scratch with seed ideas

### Newsletters
- **medical-newsletter-writer**: Patient audience, engagement prediction needed
- **cardiology-newsletter-writer**: Doctor audience, deeper technical analysis

### Editorials
- **cardiology-editorial**: Quick commentary on a known trial
- **cardiology-trial-editorial**: Need to discover important trials first

### Twitter
- **x-post-creator-skill**: Single polished post with citations
- **cardiology-tweet-writer**: Batch generation (10 at a time)
- **cremieux-cardio**: Data-heavy, evidence-obsessed long post
- **twitter-longform-medical**: Multi-tweet thread with narrative

### Polish/QA
- **authentic-voice**: Focus on removing AI detection patterns
- **content-reflection**: Broader QA (audience fit, positioning, risk)
- **scientific-critical-thinking**: Deep evidence evaluation
- **peer-review**: Full manuscript-level review

---

## Voice Standards Reference

| Content Type | Voice | Key Traits |
|--------------|-------|------------|
| YouTube | Peter Attia + Hinglish | 70% Hindi / 30% English, intellectual depth |
| Twitter/Writing | Eric Topol (Ground Truths) | Evidence-first, Q1 citations, specific stats |
| B2B (Doctors) | JACC editorial | Technical, guideline-referenced, peer-level |
| B2C (Patients) | Science-for-people | Rigorous but accessible, stats translated |

### Anti-AI Patterns (Enforced Everywhere)
**NEVER use:**
- "It's important to note"
- "In conclusion"
- "Stands as a testament"
- "Delve" / "Groundbreaking" / "Game-changer"
- Excessive em dashes
- "In today's world"

**ALWAYS use:**
- Specific data (HR, NNT, CI)
- Journal names
- First-person insights
- Natural sentence variety
- Contractions

---

## Pipelines Quick Reference

| Pipeline | Command | Purpose |
|----------|---------|---------|
| Twitter Content | `python pipelines/twitter-content/generate.py "question"` | Question → researched tweet |
| Twitter Harvest | `python pipelines/twitter-content/main.py harvest` | Scrape influencers → generate |
| Journal Fetch | `python pipelines/journal-fetch/main.py --markdown` | Daily digest |
| YouTube Research | `python research-engine/run_pipeline.py --quick` | Competitive analysis (10 min) |
| Content Calendar | `python research-engine/calendar_generator.py --show-next 5` | Next topics |

---

## How to Use This Catalog

1. **Tell me what you want to create** - "I want to write a newsletter about GLP-1"
2. **I'll route to the right skill** - Using this catalog as reference
3. **We'll apply polish chain if needed** - authentic-voice → content-reflection → fact-check
4. **If output isn't right consistently** - We update the skill's system prompt together

You don't need to memorize this. Just describe your intent, and I'll handle the routing.

---

*This catalog is Claude's routing reference. Updated as skills evolve.*
