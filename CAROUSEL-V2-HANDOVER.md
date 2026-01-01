# Carousel Generator v2 - Project Handover

**Project**: World-Class Instagram Carousel Generator
**Status**: PLANNING COMPLETE - Ready for Implementation
**Last Updated**: 2026-01-01
**Location**: `/Users/shaileshsingh/integrated cowriting system/`

---

## Quick Context for New Sessions

**Read this first to understand the project:**

We are building the **best possible Instagram carousel generator** - one that combines AI content intelligence, multi-tool visual generation, and professional design systems. This is an enhancement to the existing basic `carousel-generator` skill.

**Key Goal**: Topic → AI Research → Structured Content → Beautiful Slides → PNG Output

---

## Research Summary (Completed)

### Tools Discovered

| Tool | Purpose | URL | Priority |
|------|---------|-----|----------|
| **Vercel Satori** | React/JSX → PNG (5x faster than Puppeteer) | github.com/vercel/satori | HIGH |
| **shadcn/ui** | Production-ready React components | ui.shadcn.com | HIGH |
| **Health Icons** | 500+ free medical SVG icons | healthicons.org | HIGH |
| **Microsoft LIDA** | LLM-powered data visualization | github.com/microsoft/lida | MEDIUM |
| **Anthropic Frontend Design Skill** | Distinctive UI generation | Built into Claude Code | HIGH |
| **html-to-image** | DOM → PNG conversion | github.com/bubkoo/html-to-image | MEDIUM |

### Design Standards (Research-Backed)

| Standard | Value | Source |
|----------|-------|--------|
| Optimal Aspect Ratio | 4:5 (1080×1350px) | 10% higher engagement than 1:1 |
| Slide Count | 8-10 slides | Highest engagement |
| First Slide Impact | 80% of engagement | Hook determines success |
| Contrast Ratio | 4.5:1 minimum | WCAG AA compliance |
| Typography | 36px+ headlines, 24-30px body | Mobile readability |
| Text Density | ≤15 words per slide | Optimal scannability |

### Existing Assets to Leverage

| Asset | Location | Use For |
|-------|----------|---------|
| cardiology-visual-system | `skills/cardiology/cardiology-visual-system/` | Fal.ai, Gemini, Plotly routing |
| gemini-imagegen | `skills/cardiology/gemini-imagegen/` | Infographic generation |
| carousel-generator (v1) | `skills/cardiology/carousel-generator/` | Basic Pillow code reference |
| Brand colors | `skills/cardiology/carousel-generator/references/brand-specs.md` | Color palette |
| Content frameworks | `skills/cardiology/carousel-generator/knowledge-base/frameworks/` | 4A, 10 Magical Ways |

---

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Templates** | All 10 types | Full coverage for any content type |
| **Tech Stack** | Hybrid (Satori + Pillow) | Best of both: speed + simplicity |
| **Aspect Ratio** | Both (4:5 + 1:1) | Instagram optimized + multi-platform |
| **Color Mode** | Dynamic (AI-selected) | AI picks light/dark per slide |
| **Icon Style** | Mixed | Outline for decorative, filled for key points |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CAROUSEL GENERATOR v2                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  INPUT LAYER                                                  │
│  ├── Topic only ("GLP-1 for weight loss")                    │
│  ├── Long-form content (newsletter, script, thread)          │
│  └── Structured JSON (slides already defined)                │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  CONTENT INTELLIGENCE (Claude/GPT-4o-mini)                   │
│  ├── Research via PubMed MCP + AstraDB RAG                   │
│  ├── Classify: 4A Framework (Actionable/Analytical/etc.)     │
│  ├── Select template type (Tips/Stats/Story/Compare)         │
│  ├── Structure into 8-10 slides with hook + CTA              │
│  └── Output: Structured JSON with slide specs                │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  VISUAL GENERATION LAYER (Multi-Tool Routing)                │
│  ├── Standard slides → Satori (React→PNG, 5x faster)         │
│  ├── Infographics → Gemini API (medical accuracy)            │
│  ├── Data slides → Plotly/LIDA (charts, forest plots)        │
│  ├── Hero images → Fal.ai (lifestyle photos)                 │
│  └── Icons → Health Icons (free, SVG, medical)               │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  TEMPLATE LIBRARY (10 Designs)                                │
│  ├── HookSlide (bold question, surprising stat)              │
│  ├── TipsSlide (numbered list with icons)                    │
│  ├── StatsSlide (big number + context)                       │
│  ├── ComparisonSlide (before/after, vs)                      │
│  ├── StorySlide (patient narrative, quote)                   │
│  ├── DataSlide (chart, graph, forest plot)                   │
│  ├── StepsSlide (process with arrows)                        │
│  ├── MythSlide (crossed-out myth + truth)                    │
│  ├── QuoteSlide (expert opinion)                             │
│  └── CTASlide (follow, save, share)                          │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  QUALITY GATES                                                │
│  ├── WCAG AA contrast check (4.5:1 ratio)                    │
│  ├── Text density check (≤15 words per slide)                │
│  ├── Anti-AI voice verification                              │
│  ├── Brand consistency (design tokens)                       │
│  └── Mobile preview generation                               │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  OUTPUT                                                       │
│  ├── 8-10 PNG slides (both 4:5 and 1:1 versions)             │
│  ├── Caption suggestions per slide                           │
│  ├── Alt text for accessibility                              │
│  ├── Hashtag recommendations                                 │
│  └── Preview composite image                                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure (To Be Created)

```
skills/cardiology/carousel-generator-v2/
├── SKILL.md
├── tokens/
│   └── brand-tokens.json
├── templates/
│   ├── react/
│   │   ├── HookSlide.jsx
│   │   ├── TipsSlide.jsx
│   │   ├── StatsSlide.jsx
│   │   ├── ComparisonSlide.jsx
│   │   ├── StorySlide.jsx
│   │   ├── DataSlide.jsx
│   │   ├── StepsSlide.jsx
│   │   ├── MythSlide.jsx
│   │   ├── QuoteSlide.jsx
│   │   └── CTASlide.jsx
│   └── variants/
│       ├── light.json
│       ├── dark.json
│       └── minimal.json
├── assets/
│   ├── icons/ (Health Icons SVG)
│   ├── fonts/ (Inter font family)
│   └── backgrounds/
├── scripts/
│   ├── carousel_generator.py (main orchestrator)
│   ├── content_structurer.py (AI content layer)
│   ├── visual_router.py (tool selection)
│   ├── satori_renderer.py (React→PNG)
│   ├── pillow_renderer.py (fallback)
│   ├── quality_checker.py (QA automation)
│   └── hooks_generator.py (first slide hooks)
├── services/
│   └── satori-service/ (Node.js)
│       ├── package.json
│       └── index.js
├── references/
│   ├── design-standards.md
│   ├── hook-patterns.md
│   ├── template-guide.md
│   └── accessibility-checklist.md
└── output/
    └── carousels/
```

---

## Implementation Phases

### Phase 1: Foundation
- [ ] Create `carousel-generator-v2/` directory structure
- [ ] Create `tokens/brand-tokens.json` with colors, typography, spacing
- [ ] Download Health Icons (heart, medication, exercise, food, symptoms, procedures)
- [ ] Set up Inter font family
- [ ] Create base Python module structure
- [ ] Create SKILL.md documentation

### Phase 2: Template Library (All 10)
- [ ] HookSlide - Bold hook, curiosity gap
- [ ] TipsSlide - Numbered tips with icons
- [ ] StatsSlide - Big number + context
- [ ] ComparisonSlide - Before/after, vs layout
- [ ] StorySlide - Patient narrative, quote
- [ ] DataSlide - Plotly chart integration
- [ ] StepsSlide - Process with arrows
- [ ] MythSlide - Crossed myth + truth
- [ ] QuoteSlide - Expert opinion
- [ ] CTASlide - Action buttons, handle

### Phase 3: Rendering Engine
- [ ] Build Satori Node.js service (React→PNG)
- [ ] Create Pillow fallback renderer
- [ ] Implement visual router (slide type → tool)
- [ ] Add dual aspect ratio generation (4:5 + 1:1)
- [ ] Test rendering pipeline end-to-end

### Phase 4: Content Intelligence
- [ ] Content structurer (topic/longform → slides)
- [ ] 4A Framework classifier
- [ ] Hook generator with patterns
- [ ] PubMed/RAG integration for research
- [ ] Dynamic color mode selector

### Phase 5: Quality Assurance
- [ ] WCAG AA contrast checker
- [ ] Text density validator
- [ ] Anti-AI voice checker
- [ ] Brand consistency validator
- [ ] Mobile preview generator

### Phase 6: Integration
- [ ] Content-OS integration (forward + backward modes)
- [ ] CLI interface
- [ ] Batch generation support
- [ ] Caption and hashtag generator
- [ ] Documentation and examples

---

## Dependencies

### Python
```
pillow>=10.0.0
httpx>=0.24.0
pydantic>=2.0.0
plotly>=5.0.0
kaleido>=0.2.0  # Plotly export
```

### Node.js (Satori Service)
```json
{
  "dependencies": {
    "@vercel/og": "^0.6.0",
    "satori": "^0.10.0",
    "satori-html": "^0.3.0",
    "@resvg/resvg-js": "^2.6.0"
  }
}
```

### External APIs (Already Configured)
- Gemini API
- Fal.ai
- OpenRouter/Claude
- PubMed MCP

---

## Brand Specifications

### Colors
```json
{
  "primary": "#207178",      // Deep Teal - titles, CTAs
  "secondary": "#E4F1EF",    // Mist Aqua - backgrounds
  "accent": "#F28C81",       // Warm Coral - icons, highlights
  "neutral_light": "#F8F9FA", // Off-White - alt backgrounds
  "neutral_dark": "#333333",  // Charcoal - body text
  "alert": "#E63946"         // Heart Red - emphasis
}
```

### Typography
- **Headline**: Inter Bold, 48px
- **Subheadline**: Inter SemiBold, 36px
- **Body**: Inter Regular, 28px
- **Caption**: Inter Medium, 22px

### Dimensions
- **4:5 Instagram**: 1080×1350px
- **1:1 Square**: 1080×1080px
- **Margin**: 80px
- **Padding**: 40px

---

## Current Progress

| Phase | Status | Notes |
|-------|--------|-------|
| Research | COMPLETE | 6 agents used, comprehensive findings |
| Planning | COMPLETE | Full architecture designed |
| Decisions | COMPLETE | All choices made by user |
| Phase 1: Foundation | NOT STARTED | Next to implement |
| Phase 2: Templates | NOT STARTED | |
| Phase 3: Rendering | NOT STARTED | |
| Phase 4: Intelligence | NOT STARTED | |
| Phase 5: Quality | NOT STARTED | |
| Phase 6: Integration | NOT STARTED | |

---

## How to Resume This Project

1. **Read this file first** to get full context
2. **Check "Current Progress"** section above
3. **Start with the first uncompleted phase**
4. **Update this file** after completing each phase/task

### Quick Start Commands for Next Session

```
# In Claude Code, say:
"Read the carousel v2 handover file and continue implementation from where we left off"

# Or more specifically:
"Read /Users/shaileshsingh/integrated cowriting system/CAROUSEL-V2-HANDOVER.md and start Phase 1: Foundation"
```

---

## Reference Documents

| Document | Location | Contains |
|----------|----------|----------|
| Full Plan | `/Users/shaileshsingh/.claude/plans/polymorphic-greeting-pumpkin.md` | Detailed implementation plan |
| Existing Carousel | `skills/cardiology/carousel-generator/` | Current v1 code reference |
| Visual System | `skills/cardiology/cardiology-visual-system/SKILL.md` | Existing visual tools |
| Content Frameworks | `skills/cardiology/carousel-generator/knowledge-base/frameworks/content-frameworks.md` | 4A, 10 Magical Ways |
| Brand Specs | `skills/cardiology/carousel-generator/references/brand-specs.md` | Colors, typography |
| Archetypes | `skills/cardiology/carousel-generator/knowledge-base/audience/archetypes.md` | 6 audience types |

---

## Key Research Findings (Preserved)

### GitHub Repos to Reference
1. **vercel/satori** - React to SVG/PNG
2. **microsoft/lida** - LLM data viz
3. **FranciscoMoretti/carousel-generator** - LinkedIn carousel
4. **Davronov-Alimardon/canva-clone** - Full SaaS reference
5. **fabricjs/fabric.js** - Canvas library
6. **presenton/presenton** - Open-source Gamma alternative

### Best Practices Summary
- 4:5 aspect ratio for Instagram
- 8-10 slides optimal
- First slide hook is critical
- WCAG 4.5:1 contrast
- ≤15 words per slide
- Mixed format (images + data) = 2.33% engagement

### Cost Estimate
- ~$0.04-0.10 per carousel
- Content structuring: ~$0.01 (GPT-4o-mini)
- Infographics: FREE (Gemini)
- Standard slides: FREE (Satori)
- Hero images: ~$0.03 (Fal.ai, if needed)

---

**End of Handover Document**

*Update this file after each session to track progress.*
