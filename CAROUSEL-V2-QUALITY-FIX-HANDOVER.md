# Carousel Generator v2 - Quality Fix Handover

**Date**: 2026-01-01
**Status**: ✅ COMPLETED - Content quality fixed
**Priority**: DONE

> **SUPERSEDED BY:** `CAROUSEL-V2-VISUAL-OVERHAUL-HANDOVER.md`
> Content quality issues fixed. Now need visual design overhaul.
> Use the new handover file for next session.

---

## COMPLETED WORK (2026-01-01)

1. ✅ Created `content_database.py` with 9 cardiology topics
2. ✅ Fixed `hooks_generator.py` topic normalization
3. ✅ Updated `content_structurer.py` to use content database
4. ✅ Created `carousel_employee.py` with 5 operation modes
5. ✅ Tested all modes - content generation works

**Next:** Visual design overhaul (see new handover file)

---

## ORIGINAL HANDOVER (For Reference)

---

## QUICK RESUME

```
"Read CAROUSEL-V2-QUALITY-FIX-HANDOVER.md and fix the content quality issues in carousel generator v2"
```

---

## WHAT EXISTS (DO NOT REBUILD)

The carousel generator v2 is fully built and functional at:
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/carousel-generator-v2/
```

### Working Components
| Component | File | Status |
|-----------|------|--------|
| Data Models | `scripts/models.py` | Complete - 10 slide types |
| Brand Tokens | `tokens/brand-tokens.json` | Updated with correct colors |
| Pillow Renderer | `scripts/pillow_renderer.py` | Complete - renders all slide types |
| Content Structurer | `scripts/content_structurer.py` | Works but outputs placeholders |
| Hooks Generator | `scripts/hooks_generator.py` | Works but has phrasing issues |
| Quality Checker | `scripts/quality_checker.py` | Complete - anti-AI, contrast, density |
| Visual Router | `scripts/visual_router.py` | Complete - routes to Pillow/Plotly/Gemini |
| Main Generator | `scripts/carousel_generator.py` | Complete - CLI works |

### Brand Colors (CORRECT - Just Updated)
```
Primary Teal:    #16697A (deep calm - titles, dark backgrounds)
Secondary Teal:  #218380 (panel backgrounds, risk boxes)
Accent Coral:    #EF5350 (CTAs, highlights - vivid)
Soft Aqua:       #E8F5F4 (background wash)
Neutral White:   #F9FAFB (cards, containers)
Text Gray:       #2F3E46 (body copy - warm dark)
Alert Red:       #E74C3C (emergencies, emphasis)
```

---

## PROBLEMS TO FIX

### Problem 1: Placeholder Content (HIGH PRIORITY)

**Current Output:**
```
MYTH: "A common Statin myths misconception"
TRUTH: "What the research actually shows"
STATS: "Evidence matters for your health"
```

**Expected Output:**
```
MYTH: "Statins cause muscle pain in most people"
TRUTH: "Only 5-10% experience muscle symptoms. Nocebo effect accounts for most complaints."
STATS: "25% reduction in major cardiovascular events"
```

**Root Cause:** `content_structurer.py` lines 290-340 use placeholder text when no `ResearchResult` is provided.

**Fix Needed:**
1. Add a content database with real cardiology facts
2. OR integrate with PubMed MCP to fetch real data
3. OR use Claude API to generate topic-specific content

### Problem 2: Awkward Hook Phrasing (MEDIUM PRIORITY)

**Current Output:**
```
"3 things about statin myths you didn't know"
"What if everything you know about 5 statin myths is wrong?"
```

**Expected Output:**
```
"5 statin myths debunked by science"
"The truth about statins your doctor won't tell you"
```

**Root Cause:** `hooks_generator.py` inserts `{topic}` literally into patterns. When topic = "statin myths", it creates "statin myths myths".

**Fix Needed:**
1. Parse topic to extract core subject (e.g., "statin myths" → "statins")
2. Improve pattern matching to avoid redundancy
3. Add topic normalization function

### Problem 3: Empty Space on Slides (LOW PRIORITY)

**Current:** Myth slides have too much white space because content is short placeholders.

**Fix:** Will resolve automatically when real content is added.

---

## PROPOSED SOLUTION

### Option A: Hardcoded Content Database (Fast)

Create `scripts/content_database.py` with curated cardiology content:

```python
STATIN_CONTENT = {
    "myths": [
        {"myth": "Statins cause muscle pain in most people",
         "truth": "Only 5-10% experience symptoms. Nocebo effect is significant."},
        {"myth": "Statins damage your liver",
         "truth": "Liver damage is rare (<1%). Benefits outweigh risks."},
        {"myth": "Natural alternatives work just as well",
         "truth": "No supplement matches statin efficacy for CV risk reduction."},
    ],
    "stats": [
        {"value": "25%", "label": "reduction in major CV events"},
        {"value": "50%", "label": "of patients stop within 1 year"},
    ],
    "hooks": [
        "5 statin myths that could cost you your life",
        "What cardiologists wish you knew about statins",
    ]
}
```

Topics to cover: statins, LDL, GLP-1, blood pressure, heart attack, CAC, diabetes, cholesterol

### Option B: Claude API Integration (Better Quality)

Modify `content_structurer.py` to call Claude for content generation:

```python
def generate_content_with_ai(self, topic: str, template: str) -> ResearchResult:
    """Use Claude to generate topic-specific content."""
    prompt = f"""Generate carousel content for: {topic}
    Template: {template}

    Return JSON with:
    - 3-5 specific myths with evidence-based truths
    - 2-3 statistics with sources
    - Key points for tips slides
    """
    # Call Claude API
    # Parse response into ResearchResult
```

### Option C: PubMed Integration (Most Accurate)

Already have PubMed MCP. Wire it into content generation:

```python
def research_topic(self, topic: str) -> ResearchResult:
    """Research topic via PubMed before generating content."""
    # Search PubMed for topic
    # Extract key statistics
    # Build evidence-based content
```

---

## FILES TO MODIFY

### 1. `scripts/content_structurer.py`

**Current:** Uses placeholder content when no research provided
**Change:** Add content generation/lookup before using placeholders

Key sections:
- Line 270-280: TIPS slide generation
- Line 290-300: MYTH slide generation
- Line 280-290: STATS slide generation

### 2. `scripts/hooks_generator.py`

**Current:** `{topic}` inserted literally
**Change:** Add topic normalization

```python
def normalize_topic(self, topic: str) -> str:
    """Extract core subject from topic string."""
    # "5 statin myths" → "statins"
    # "GLP-1 weight loss" → "GLP-1"
    # Remove numbers, common words like "myths", "tips", etc.
```

### 3. NEW: `scripts/content_database.py`

Create hardcoded content for common cardiology topics.

---

## TEST COMMANDS

After fixing, test with:

```bash
cd "/Users/shaileshsingh/integrated cowriting system/skills/cardiology/carousel-generator-v2"

# Test statin myths
python -m scripts.carousel_generator "Statin myths" --template myth_busting

# Test GLP-1 tips
python -m scripts.carousel_generator "GLP-1 for weight loss" --template tips_5

# Test with quality report
python -m scripts.carousel_generator "Blood pressure" --template tips_5 --quality-report
```

**Success Criteria:**
1. No placeholder text in output
2. Hook doesn't repeat topic words awkwardly
3. Myths have specific claims with evidence-based rebuttals
4. Stats show real numbers with context

---

## DIRECTORY STRUCTURE

```
skills/cardiology/carousel-generator-v2/
├── SKILL.md                      # Documentation
├── tokens/
│   └── brand-tokens.json         # Brand colors (UPDATED)
├── assets/
│   ├── icons/                    # 21 SVG icons
│   └── fonts/                    # Inter font family
├── references/
│   ├── design-standards.md
│   └── hook-patterns.md
├── scripts/
│   ├── __init__.py
│   ├── models.py                 # Data models
│   ├── tokens.py                 # Token utilities
│   ├── pillow_renderer.py        # Visual rendering
│   ├── carousel_generator.py     # Main orchestrator
│   ├── content_structurer.py     # NEEDS FIX - placeholder content
│   ├── hooks_generator.py        # NEEDS FIX - awkward phrasing
│   ├── quality_checker.py        # QA automation
│   ├── visual_router.py          # Multi-tool routing
│   └── content_database.py       # TO CREATE - curated content
└── output/carousels/             # Generated output
```

---

## EXAMPLE OUTPUT COMPARISON

### Current (Bad)
```
Slide 1: "3 things about statin myths you didn't know"
Slide 2: MYTH: "A common Statin myths misconception"
         TRUTH: "What the research actually shows"
Slide 3: MYTH: "A common Statin myths misconception"
         TRUTH: "What the research actually shows"
```

### Expected (Good)
```
Slide 1: "5 statin myths debunked"
Slide 2: MYTH: "Statins cause muscle pain in most people"
         TRUTH: "Only 5-10% experience symptoms. Most is nocebo effect."
Slide 3: MYTH: "Statins damage your liver"
         TRUTH: "Liver damage is extremely rare (<1%). Routine monitoring not needed."
```

---

## RECOMMENDED APPROACH

1. **Start with Option A** (content database) - fast to implement, immediate improvement
2. **Then add Option B** (Claude API) - for topics not in database
3. **Finally add Option C** (PubMed) - for maximum accuracy

This gives you:
- Immediate fix with curated content
- Fallback to AI generation
- Research-backed accuracy when needed

---

## CONTEXT FOR NEXT SESSION

**Goal:** Make carousel generator produce publication-ready content, not placeholders.

**User:** Dr. Shailesh Singh, cardiologist creating Instagram educational content.

**Voice:** Eric Topol style - evidence-based, specific data, no fluff.

**Key Topics:** Statins, LDL cholesterol, GLP-1/Ozempic, blood pressure, heart attacks, CAC scoring, diabetes-cardio connection.

**Anti-AI Requirements:** No generic phrases, specific numbers with sources, natural language.

---

**End of Handover - Fix content quality to make this production-ready**
