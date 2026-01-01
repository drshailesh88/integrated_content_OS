# Visual System Upgrade - Session Handover

**Project:** World-Class Publication Graphics System
**Goal:** Nature/JACC/NEJM-quality visuals for medical content
**Owner:** Dr. Shailesh Singh
**Last Updated:** 2026-01-01 (Session 10 - Phase 3.1 library expansion)

---

## TL;DR - CONTEXT FOR NEW SESSION

> **What is this?** Building a publication-grade visual design system for Dr. Shailesh Singh's cardiology content. Think Nature/JACC/NEJM quality graphics.

> **What's done?** Phase 1 + Phase 2 COMPLETE - design tokens, Satori infographics, svg_diagrams (drawsvg) diagrams, Plotly charts, Component Library (6 components), SVG Infographic Templates (5 templates), Architecture Diagrams (9 diagram types: HF/ACS/AF pathways, CONSORT/PRISMA/methodology flows, healthcare system/cardiology dept/data pipeline), plus Satori carousel templates integrated into carousel-generator-v2. Phase 3.1 Manim library + catalog built (30 scenes).

> **What's next?** Phase 3.1 expanded: Manim scene library + catalog in place. Next: render remaining scenes, add more anatomy/physiology, or harden the carousel-generator-v2 Satori pipeline for production use.

## COMPREHENSIVE STATUS SUMMARY (SESSION 10)

**Vision:** A publication-grade graphics pipeline matching Nature/JACC/NEJM standards for cardiology content.

**Achieved to Date (Phases 1–3.1):**
- **Foundation (Phase 1):** Design tokens + WCAG validation, Satori React→SVG→PNG (5 templates + carousel templates), drawsvg diagrams, Plotly standardization (300 DPI, tokenized colors, WCAG checks).
- **Design System (Phase 2):** Component library (6 components), SVG infographic templates (5), architecture diagrams (9 types).
- **Carousel integration:** Satori renderer integrated in `carousel-generator-v2` with visual router routing.
- **Manim (Phase 3.1):** Dedicated venv, primitives/templates, **30-scene catalog** across core categories, CLI with catalog listing, router integration for `animation_scene`.

**Outputs:** Test outputs already generated across Satori, drawsvg, Plotly, templates, arch diagrams, and Manim (`outputs/` folders).

**Remaining Work (Phases 3.1+):**
- Render and QA the full Manim catalog; expand anatomy/physiology modules.
- Harden `carousel-generator-v2` (QA defaults, routing heuristics, docs).
- Add Helvetica/Arial font files to Satori.
- Build Phase 3.2 `react-pdf` pipeline for full article PDFs.
- Phase 4 router upgrades (quality checks, cost/time estimation, batch generation).

### Key File Locations:
```
/Users/shaileshsingh/integrated cowriting system/
├── VISUAL-SYSTEM-HANDOVER.md           # THIS FILE - read first
├── skills/cardiology/
│   ├── visual-design-system/           # ✅ Phase 1 + Phase 2 COMPLETE
│   │   ├── tokens/                     # Design tokens (colors, typography, spacing)
│   │   ├── satori/                     # React → SVG → PNG (5 templates)
│   │   │   ├── carousel-templates/     # Carousel slide templates (hook/myth/stat/tips/cta)
│   │   ├── manim_animations/           # 🚧 Phase 3.1 - Manim library + catalog (30 scenes)
│   │   ├── svg_diagrams/               # Python SVG (diagrams, charts, flows)
│   │   ├── components/                 # ✅ Phase 2.1 - Unified Component Library
│   │   │   ├── stat_card.py            # StatCard - Big numbers
│   │   │   ├── comparison.py           # ComparisonChart - Side-by-side
│   │   │   ├── forest_plot.py          # ForestPlot - Meta-analysis
│   │   │   ├── timeline.py             # Timeline - Patient journeys
│   │   │   ├── process_flow.py         # ProcessFlow - Treatment algorithms
│   │   │   └── data_table.py           # DataTable - Publication tables
│   │   ├── svglue_templates/           # ✅ Phase 2.2 - SVG Infographic Templates
│   │   │   ├── template_renderer.py    # lxml-based renderer
│   │   │   └── templates/              # 5 SVG templates
│   │   ├── arch_diagrams/              # ✅ Phase 2.3 - Architecture Diagrams
│   │   │   ├── __init__.py             # Lazy imports (avoids circular import)
│   │   │   ├── treatment_pathways.py   # HF, ACS, AF clinical algorithms
│   │   │   ├── research_flows.py       # CONSORT, PRISMA, methodology
│   │   │   └── healthcare_arch.py      # Healthcare system, cardiology dept
│   │   └── SKILL.md                    # Full documentation
│   ├── cardiology-visual-system/       # ✅ Phase 1.4 (Plotly integration)
│       └── scripts/plotly_charts.py    # 300 DPI, WCAG validation
│   └── carousel-generator-v2/          # Satori bridge for carousel rendering
│       └── scripts/satori_renderer.py  # Uses visual-design-system/satori/renderer.js
```

---

## IMMEDIATE NEXT STEPS (START HERE)

> **Phase 2 is COMPLETE!** All foundation + design system phases done. 9 architecture diagram types built and tested. Carousel-generator-v2 already integrates Satori templates. Phase 3.1 Manim library + catalog added (30 scenes) with router integration. Next: render QA pack, add more anatomy/physiology, or production hardening.

```
Read VISUAL-SYSTEM-HANDOVER.md and continue with Phase 3.1: Manim animations (render + expand scene library).

Phases 1.1-1.4, 2.1, 2.2, and 2.3 are ALL COMPLETE.

Next options:
- Phase 3.1: Render QA pack for the 30-scene Manim catalog + expand anatomy/physiology
- Harden carousel-generator-v2 Satori pipeline (QA, defaults, docs)
- Phase 3.2: react-pdf for complete article PDFs
- Add Helvetica/Arial font files to Satori for true journal typography
- Phase 4: visual router upgrades + batch generation
```

### Quick Verification (run these first to confirm system works):

```bash
# Test design tokens
cd "/Users/shaileshsingh/integrated cowriting system/skills/cardiology/visual-design-system"
python scripts/token_validator.py

# Test Satori infographic generation
cd satori && node renderer.js --list
node renderer.js --template stat-card --data '{"value":"42%","label":"Test"}' -o ../outputs/verify.png

# Test svg_diagrams (drawsvg) diagrams
cd svg_diagrams && python medical_diagrams.py

# Test architecture diagrams (Phase 2.3)
cd ../arch_diagrams && python treatment_pathways.py
python research_flows.py
python healthcare_arch.py

# Test Manim scenes (Phase 3.1 - dry run, no render)
cd .. && python scripts/render_manim.py mechanism --quality l --format mp4 --dry-run --manim-bin skills/cardiology/visual-design-system/.venv-manim
python scripts/render_manim.py --list

# Test Plotly with design tokens (Phase 1.4)
cd "../../cardiology-visual-system/scripts"
python plotly_charts.py demo --quality-report --output-dir ../outputs
python plotly_charts.py demo --png --output-dir ../outputs
```

### Phase 1.4 Implementation (COMPLETED):

1. ✅ Import design tokens from `visual-design-system/tokens/index.py`
2. ✅ Apply `get_plotly_template()` as default template
3. ✅ Force 300 DPI export (4x scale = 3200×2400px)
4. ✅ Replace hardcoded colors with token-based colors
5. ✅ Add accessible color pairs for treatment/control comparisons
6. ✅ Add WCAG contrast validation on every export
7. ✅ Update CLI with `--quality-report` and `--png` flags

---

## WHAT'S ALREADY BUILT (DO NOT REBUILD)

### Phase 1.1: Design Token System ✅ COMPLETE

**Location:** `skills/cardiology/visual-design-system/tokens/`

| File | Purpose |
|------|---------|
| `colors.json` | Nature-compliant palette, WCAG AA, colorblind-safe |
| `typography.json` | Helvetica/Arial, 5-8pt for figures |
| `spacing.json` | 4px grid, layout spacing |
| `shadows.json` | Elevation scale |
| `index.py` | API: `get_color()`, `get_accessible_pair()`, `validate_contrast()` |
| `__init__.py` | Package exports |

**Scripts:** `scripts/token_validator.py` - WCAG validation CLI

### Phase 1.2: Satori Infographics ✅ COMPLETE

**Location:** `skills/cardiology/visual-design-system/satori/`

| File | Purpose |
|------|---------|
| `renderer.js` | React → SVG → PNG pipeline with 5 templates |
| `package.json` | npm dependencies |
| `fonts/Roboto-*.ttf` | Bundled fonts (Helvetica/Arial supported if added) |
| `carousel-templates/` | Carousel slide templates (hook/myth/stat/tips/cta) |

**Templates available:** `stat-card`, `comparison`, `process-flow`, `trial-summary`, `key-finding`  
**Carousel templates:** `carousel-hook`, `carousel-myth`, `carousel-stat`, `carousel-tips`, `carousel-cta`

**Python wrapper:** `scripts/generate_infographic.py`

**Test outputs in:** `outputs/*.png` and `outputs/*.svg`

### Phase 1.3: svg_diagrams (drawsvg) Integration ✅ COMPLETE

**Location:** `skills/cardiology/visual-design-system/svg_diagrams/`

| Module | Functions |
|--------|-----------|
| `medical_diagrams.py` | `heart_simple`, `ecg_wave`, `cardiac_conduction`, `organ_icon` |
| `data_charts.py` | `bar_chart`, `grouped_bar_chart`, `line_chart`, `forest_plot` |
| `process_flows.py` | `treatment_algorithm`, `patient_journey`, `study_flow`, `simple_process_flow` |

### Phase 1.4: Plotly Standardization ✅ COMPLETE

**Location:** `skills/cardiology/cardiology-visual-system/scripts/plotly_charts.py`

| Feature | Implementation |
|---------|----------------|
| Token Import | Auto-loads from `visual-design-system/tokens/` |
| 300 DPI Export | `scale=4` → 3200×2400px output |
| WCAG Validation | Contrast checks on every `save_chart()` |
| Colorblind-Safe | Paul Tol palette, accessible pairs |
| CLI | `--quality-report`, `--png`, `--output-dir` flags |

**Test command:**
```bash
cd "/Users/shaileshsingh/integrated cowriting system/skills/cardiology/cardiology-visual-system/scripts"
python plotly_charts.py demo --quality-report --png --output-dir ../outputs
```

---

## QUICK RESUME CHECKLIST

> **Read this first when resuming a session**

- [x] Phase 1.1: Design Token System - COMPLETE
- [x] Phase 1.2: Satori Integration - COMPLETE
- [x] Phase 1.3: svg_diagrams (drawsvg) Integration - COMPLETE
- [x] Phase 1.4: Plotly Standardization - COMPLETE
- [x] Phase 2.1: Component Library - COMPLETE (6 components)
- [x] Phase 2.2: SVG Infographic Templates - COMPLETE (5 templates)
- [x] Phase 2.3: mingrammer/diagrams Integration - COMPLETE (9 diagram types)
- [ ] Phase 3.1: Manim Animations - **IN PROGRESS** (30-scene catalog built)
- [ ] Phase 3.2: react-pdf Pipeline
- [ ] Update this file before context window < 20%

---

## PROJECT VISION

Transform the existing visual generation system into a **publication-grade graphics pipeline** that produces visuals matching the quality standards of Nature, JACC, NEJM, and The Lancet.

**Why this matters:**
- Content is rigorously written - graphics must match
- Visuals signal thought leadership and authority
- Poor graphics undermine credibility
- We want to look like the thought leaders we aim to be

---

## CURRENT SYSTEM STATE

### What Exists (skills/cardiology/)

| Tool | Location | Status | Capability |
|------|----------|--------|------------|
| **Fal.ai** | `cardiology-visual-system/scripts/fal_image.py` | Working | Blog photos, lifestyle images |
| **Gemini** | `gemini-imagegen/scripts/` | API key commented | Infographics, medical illustrations |
| **Plotly** | `cardiology-visual-system/scripts/plotly_charts.py` | Working | Charts, forest plots |
| **Satori** | `visual-design-system/satori/renderer.js` | Working | Infographics + carousel templates |
| **Manim** | `visual-design-system/manim_animations/` | In progress | 30-scene library + catalog (venv + router integration) |
| **Mermaid** | MCP integrated | Working | Flowcharts, diagrams |
| **Marp** | Templates exist | Working | Slide decks |
| **Pillow** | `carousel-generator-v2/scripts/pillow_renderer.py` | Working | Carousel slides (10 types) |
| **Visual Router** | `carousel-generator-v2/scripts/visual_router.py` | Working | Routes slides to tools |

### API Keys Status (.env)
```
FAL_KEY=<configured and active>
GEMINI_API_KEY=<commented out - needs enabling>
GOOGLE_API_KEY=<commented out>
```

---

## GAP ANALYSIS

| Capability | Current | Target (Nature Standard) | Priority |
|------------|---------|--------------------------|----------|
| Typography | Helvetica/Arial in tokens; Satori falls back to Roboto until fonts added | Helvetica/Arial, 5-8pt | P0 |
| Colors | Tokenized + WCAG checks | RGB, 4.5:1 contrast, colorblind-safe | P0 |
| Data viz export | PNG at 300 DPI + HTML (Plotly) | Static PDF/PNG at 300 DPI | P0 |
| Infographics | Satori + SVG templates | Template-based (consistent) | P1 |
| Diagrams | Mermaid + svg_diagrams + arch_diagrams | + Architectural, process, hand-drawn | P1 |
| Animations | Library + catalog (30 scenes) | Manim for explanatory | P2 |
| PDF reports | None | react-pdf with charts | P2 |
| Design tokens | Centralized token system | Centralized token system | P0 |

---

## IMPLEMENTATION ROADMAP

### Phase 1: Foundation (CURRENT)

#### 1.1 Design Token System
**Location:** `skills/cardiology/visual-design-system/tokens/`

Create centralized design tokens for:
- Colors (Nature-compliant, colorblind-safe)
- Typography (Helvetica/Arial, 5-8pt range)
- Spacing (consistent grid system)
- Shadows (subtle, professional)

**Files to create:**
```
visual-design-system/
├── tokens/
│   ├── colors.json         # Color palette
│   ├── typography.json     # Font specs
│   ├── spacing.json        # Grid system
│   └── index.py            # Token loader
├── scripts/
│   ├── token_validator.py  # Validate WCAG compliance
│   └── apply_tokens.py     # Apply to existing tools
└── SKILL.md
```

#### 1.2 Satori Integration
**Purpose:** React → SVG → PNG pipeline for programmatic infographics

**Dependencies:**
```bash
npm install satori @resvg/resvg-js sharp
```

**Files to create:**
```
visual-design-system/
├── satori/
│   ├── renderer.js         # Main Satori renderer
│   ├── carousel-templates/ # Carousel slide templates
│   └── fonts/              # Roboto bundled (Helvetica/Arial optional)
└── scripts/
    └── generate_infographic.py  # Python wrapper
```

#### 1.3 svg_diagrams (drawsvg) Integration
**Purpose:** Pure Python SVG generation for diagrams

**Dependencies:**
```bash
pip install drawsvg cairosvg
```

**Files to create:**
```
visual-design-system/
├── svg_diagrams/
│   ├── medical_diagrams.py    # Heart, organs, pathways
│   ├── data_charts.py         # Charts without Plotly
│   ├── process_flows.py       # Step-by-step diagrams
│   └── templates/             # Reusable SVG components
```

#### 1.4 Plotly Standardization
**Modify:** `cardiology-visual-system/scripts/plotly_charts.py`

Changes needed:
- Force 300 DPI export
- Apply Nature color palette
- Helvetica/Arial fonts
- Remove interactive elements for print
- Add WCAG contrast validation

---

### Phase 2: Design System

#### 2.1 Component Library
Build shadcn-inspired components for medical/scientific use:
- StatCard - Big number + context
- ComparisonChart - Side-by-side
- ForestPlot - Meta-analysis standard
- TimelineDiagram - Patient journey
- ProcessFlow - Treatment algorithms
- DataTable - Publication-ready tables

#### 2.2 Infographic Templates (svglue)
Create Inkscape templates with placeholder IDs:
- Trial Results Summary
- Drug Mechanism Explainer
- Patient Statistics Dashboard
- Before/After Comparison
- Risk Factor Visualization

#### 2.3 Diagrams Integration
Add mingrammer/diagrams for:
- Treatment pathways
- Healthcare system architecture
- Research methodology flows

---

### Phase 3: Advanced

#### 3.1 Manim for Animations (IN PROGRESS)
- 30-scene catalog across cardiometabolic, ACS/CAD, arrhythmia, imaging, statistics, devices, anatomy
- Primitives/templates for axes, step curves, flow blocks, timelines, anatomy modules
- CLI + visual router integration (`animation_scene` routing)

#### 3.2 react-pdf Pipeline
- Generate complete article PDFs
- Embedded charts and figures
- Publication-ready formatting

---

### Phase 4: Polish

#### 4.1 Visual Router Upgrade
Enhance `carousel-generator-v2/scripts/visual_router.py`:
- Route by content type (data → Plotly, process → Diagrams, etc.)
- Quality validation before output
- Cost/time estimation

#### 4.2 Batch Generation
- One command → all visuals for an article
- Consistent styling across all outputs
- Automatic naming and organization

---

## DESIGN SPECIFICATIONS

### Color Palette (Nature-Compliant)

```json
{
  "primary": {
    "navy": "#1e3a5f",
    "blue": "#2d6a9f",
    "teal": "#48a9a6"
  },
  "semantic": {
    "success": "#4caf50",
    "warning": "#ff9800",
    "danger": "#f44336",
    "neutral": "#607d8b"
  },
  "accessible_pairs": {
    "comparison_1": ["#0077bb", "#ee7733"],
    "comparison_2": ["#009988", "#cc3311"],
    "comparison_3": ["#33bbee", "#ee3377"]
  },
  "backgrounds": {
    "light": "#f8f9fa",
    "dark": "#1a1a2e"
  }
}
```

### Typography Specifications

```json
{
  "fonts": {
    "primary": "Helvetica, Arial, sans-serif",
    "monospace": "Courier, monospace"
  },
  "sizes": {
    "panel_label": "8pt",
    "body_max": "7pt",
    "body_min": "5pt",
    "stat_number": "24pt",
    "axis_label": "6pt"
  },
  "weights": {
    "panel_label": "bold",
    "body": "regular"
  }
}
```

### Resolution Standards

| Output Type | Resolution | Format |
|-------------|------------|--------|
| Print/Journal | 300 DPI | PDF, TIFF |
| Web | 150 DPI | PNG, SVG |
| Social Media | 72 DPI | PNG, JPG |
| Presentation | 150 DPI | PNG |

---

## RESEARCH FINDINGS

### Tools to Integrate

| Tool | Purpose | Link | Priority |
|------|---------|------|----------|
| **Satori** | React → SVG → PNG | github.com/vercel/satori | P0 |
| **drawsvg** | Python SVG generation | github.com/cduck/drawsvg | P0 |
| **shadcn Charts** | React chart components | ui.shadcn.com/charts | P1 |
| **Diagrams** | Architecture as code | github.com/mingrammer/diagrams | P1 |
| **Excalidraw** | Hand-drawn diagrams | github.com/excalidraw/excalidraw | P1 |
| **tldraw** | Whiteboard SDK | github.com/tldraw/tldraw | P2 |
| **Manim** | Math animations | github.com/3b1b/manim | P2 |
| **svglue** | Template-based SVG | github.com/mbr/svglue | P1 |
| **react-pdf** | PDF generation | react-pdf.org | P2 |
| **Observable Plot** | High-level D3 | observablehq.com/plot | P2 |

### Napkin.ai Learnings
- Text-to-visual in <10 seconds
- Smart template selection
- No API (can't integrate directly)
- We replicate the UX with our tools

### Nature Journal Standards
- Font: Helvetica or Arial only
- Panel labels: 8pt bold lowercase
- Text: 5-7pt range
- Colors: RGB, avoid red-green
- Contrast: ≥4.5:1
- Resolution: 300 DPI minimum
- No 3D histograms
- No decorative icons

---

## FILE STRUCTURE (TARGET)

```
skills/cardiology/visual-design-system/
├── SKILL.md                    # Main documentation
├── tokens/
│   ├── colors.json             # Color palette
│   ├── typography.json         # Font specifications
│   ├── spacing.json            # Grid system
│   ├── shadows.json            # Shadow definitions
│   └── index.py                # Token loader utility
├── satori/
│   ├── renderer.js             # Main Satori renderer
│   ├── package.json            # Node dependencies
│   ├── carousel-templates/     # hook/myth/stat/tips/cta
│   └── fonts/
│       ├── Roboto-Regular.ttf
│       └── Roboto-Bold.ttf
├── svg_diagrams/
│   ├── __init__.py
│   ├── medical_diagrams.py     # Anatomy, organs
│   ├── data_charts.py          # Non-Plotly charts
│   ├── process_flows.py        # Flowcharts
│   ├── icons.py                # Medical icon set
│   └── templates/
│       └── base_elements.py    # Reusable components
├── arch_diagrams/
│   ├── treatment_pathways.py   # Clinical pathways
│   ├── research_flows.py       # Study methodology
│   └── healthcare_arch.py      # System diagrams
├── scripts/
│   ├── generate_infographic.py # Main generation CLI
│   ├── token_validator.py      # WCAG validation
│   ├── batch_generator.py      # Multi-visual generation
│   ├── export_utils.py         # Format conversion
│   └── quality_checker.py      # Pre-export validation
├── references/
│   ├── nature_guidelines.md    # Journal specs
│   ├── color_palettes.md       # Approved palettes
│   └── template_catalog.md     # Available templates
└── outputs/                    # Generated files
    └── .gitkeep
```

---

## CURRENT PROGRESS

### Session 1: 2026-01-01

**Completed:**
- [x] Full codebase exploration (5 Haiku agents)
- [x] Research: Napkin.ai, GitHub repos, shadcn, Nature guidelines
- [x] Gap analysis: Current vs. publication standard
- [x] Created implementation roadmap (4 phases)
- [x] Created this handover file

### Session 2: 2026-01-01

**Completed:**
- [x] **Phase 1.1: Design Token System** - COMPLETE
  - [x] Created `skills/cardiology/visual-design-system/` directory structure
  - [x] Implemented `tokens/colors.json` - Nature-compliant palette with:
    - Primary colors (navy, blue, teal) - all WCAG AA compliant
    - Semantic colors (success, warning, danger, neutral)
    - 7-color categorical palette (Paul Tol colorblind-safe)
    - Sequential and diverging palettes
    - 4 pre-validated accessible pairs for comparisons
    - Clinical outcome colors (mortality, hospitalization, etc.)
    - Forest plot colors
  - [x] Implemented `tokens/typography.json` - Nature specs:
    - Helvetica/Arial font family
    - 5-8pt sizes for figure elements
    - Infographic and social media sizes
  - [x] Implemented `tokens/spacing.json`:
    - 4px grid system
    - Layout-specific spacing (figure, chart, carousel)
    - Stroke widths and border radii
  - [x] Implemented `tokens/shadows.json`:
    - Elevation scale (none for figures, xs-xl for infographics)
  - [x] Created `tokens/index.py` - Full API:
    - `get_tokens()`, `get_color()`, `get_accessible_pair()`
    - `validate_contrast()`, `get_color_palette()`
    - Plotly template generator
    - Matplotlib style generator
  - [x] Created `scripts/token_validator.py`:
    - WCAG contrast validation
    - Colorblind safety checks
    - Typography and spacing validation
    - Full CLI with reporting
  - [x] Created `SKILL.md` documentation
  - [x] Validation passed: 31 PASS, 3 WARN (acceptable), 0 FAIL

- [x] **Phase 1.2: Satori Integration** - COMPLETE
  - [x] Installed npm dependencies: satori, @resvg/resvg-js, sharp
  - [x] Downloaded Roboto fonts (TTF) from Google Fonts CDN
  - [x] Created `satori/renderer.js` - full React → SVG → PNG pipeline
  - [x] Implemented 5 templates:
    - `stat-card` - Big numbers with context
    - `comparison` - Side-by-side treatment vs control
    - `process-flow` - Step-by-step algorithms
    - `trial-summary` - Clinical trial results
    - `key-finding` - Highlighted findings with icons
  - [x] Created `scripts/generate_infographic.py` - Python wrapper
  - [x] All templates tested and generating successfully
  - [x] Both PNG and SVG outputs working
  - [x] Updated SKILL.md with Satori documentation

**Generated Test Outputs:**
```
outputs/
├── test-stat-card.png    (47KB)
├── test-comparison.png   (58KB)
├── test-process.png      (57KB)
├── test-trial.png        (66KB)
├── test-finding.png      (51KB)
└── [+ SVG versions]
```

### Session 3: 2026-01-01

**Completed:**
- [x] **Phase 1.3: svg_diagrams (drawsvg) Integration** - COMPLETE
  - [x] Installed drawsvg and cairosvg dependencies
  - [x] Created `svg_diagrams/__init__.py` with lazy imports (avoids circular import)
  - [x] Created `svg_diagrams/medical_diagrams.py`:
    - `heart_simple()` - 4-chamber heart with vessels, labels, highlighting
    - `ecg_wave()` - Normal sinus rhythm, atrial fibrillation patterns
    - `cardiac_conduction()` - SA/AV node, bundle branches, Purkinje fibers
    - `organ_icon()` - Heart, brain, lungs, kidney, liver icons
  - [x] Created `svg_diagrams/data_charts.py`:
    - `bar_chart()` - Vertical/horizontal bars with error bars
    - `grouped_bar_chart()` - Multi-series comparisons
    - `line_chart()` - Time series with multiple lines
    - `forest_plot()` - Meta-analysis with pooled estimate
  - [x] Created `svg_diagrams/process_flows.py`:
    - `treatment_algorithm()` - Clinical pathways with decision nodes
    - `patient_journey()` - Timeline with stages and events
    - `study_flow()` - CONSORT-style enrollment diagrams
    - `simple_process_flow()` - Chevron/step flows
  - [x] All modules tested and generating 16 PNG outputs
  - [x] Updated SKILL.md with complete svg_diagrams (drawsvg) documentation
  - [x] All diagrams use design tokens for colors, fonts, spacing

**Generated Test Outputs (Session 3):**
```
outputs/
├── heart_diagram.png      (26KB) - Heart anatomy
├── ecg_normal.png         (12KB) - ECG waveform
├── conduction_system.png  (21KB) - Conduction system
├── icon_heart.png         (2KB)  - Organ icons
├── icon_brain.png         (3KB)
├── icon_lungs.png         (2KB)
├── icon_kidney.png        (3KB)
├── icon_liver.png         (2KB)
├── bar_chart.png          (12KB) - Data charts
├── grouped_bar_chart.png  (10KB)
├── line_chart.png         (23KB)
├── forest_plot.png        (19KB)
├── treatment_algorithm.png (20KB) - Process flows
├── patient_journey.png    (14KB)
├── study_flow.png         (17KB)
└── simple_process.png     (9KB)
```

### Session 4: 2026-01-01

**Completed:**
- [x] **Phase 1.4: Plotly Standardization** - COMPLETE
  - [x] Added design token import from `visual-design-system/tokens/index.py`
  - [x] Replaced hardcoded colors with token-based `_get_medical_colors()` and `_get_medical_palette()`
  - [x] Added `_get_treatment_control_colors()` for accessible color pairs
  - [x] Updated `apply_medical_theme()` to use Plotly template from tokens
  - [x] Fixed Modern Plotly API compatibility (`title.font` instead of `titlefont`)
  - [x] Updated `save_chart()` for 300 DPI export (scale=4, 3200×2400px output)
  - [x] Added `validate_chart_accessibility()` - WCAG contrast checks on every export
  - [x] Added `print_quality_report()` - comprehensive publication standards report
  - [x] Added `get_publication_settings()` - programmatic access to settings
  - [x] Updated CLI with `--quality-report`, `--png`, `--output-dir` flags
  - [x] Updated `create_comparison_bars()` to use colorblind-safe pairs
  - [x] Updated `demo_trial_results()` to use accessible colors
  - [x] Updated SKILL.md with Plotly documentation
  - [x] Updated handover file

**Generated Test Outputs (Session 4):**
```
cardiology-visual-system/outputs/
├── demo_trial_results.png    (213KB) - Treatment vs control comparison
├── demo_trial_results.html   (9KB)
├── demo_forest_plot.png      (239KB) - Meta-analysis forest plot
├── demo_forest_plot.html     (10KB)
├── demo_trends.png           (305KB) - Time trend line chart
└── demo_trends.html          (9KB)
```

**Phase 1 COMPLETE!** All foundation work done:
→ Design tokens, Satori, svg_diagrams (drawsvg), Plotly standardization

### Session 5: 2026-01-01

**Completed:**
- [x] **Phase 2.1: Component Library** - COMPLETE
  - [x] Created `components/` directory with unified API
  - [x] Built `base.py` with abstract Component class and multi-backend support
  - [x] Built `stat_card.py` - Big numbers with context (Satori/drawsvg)
  - [x] Built `comparison.py` - Side-by-side comparisons (Satori/Plotly/drawsvg)
  - [x] Built `forest_plot.py` - Meta-analysis visualization (Plotly/drawsvg)
  - [x] Built `timeline.py` - Patient journeys (drawsvg/Satori)
  - [x] Built `process_flow.py` - Treatment algorithms (Satori/drawsvg)
  - [x] Built `data_table.py` - Publication-ready tables (drawsvg/Plotly)
  - [x] Renamed local `drawsvg/` to `svg_diagrams/` to avoid package shadowing
  - [x] Added `get_drawsvg()` helper for clean package imports
  - [x] Updated SKILL.md with Component Library documentation
  - [x] All 6 components tested and generating outputs

**Generated Test Outputs (Session 5):**
```
outputs/
├── test-stat-card.png     (20KB) - StatCard component
├── test-comparison.png    (24KB) - ComparisonChart component
├── test-forest.png        (17KB) - ForestPlot component
├── test-timeline.png      (25KB) - Timeline component
├── test-process.png       (14KB) - ProcessFlow component
└── test-table.png         (21KB) - DataTable component
```

**Phase 2.1 COMPLETE!** Component Library with 6 reusable components:
→ StatCard, ComparisonChart, ForestPlot, Timeline, ProcessFlow, DataTable
→ Each component supports multiple backends (Satori, Plotly, drawsvg)
→ Unified Python API with consistent interface

### Session 6: 2026-01-01

**Completed:**
- [x] **Phase 2.2: SVG Infographic Templates** - COMPLETE
  - [x] Installed svglue and lxml dependencies
  - [x] Created `svglue_templates/` directory (renamed from svglue to avoid package shadowing)
  - [x] Built 5 SVG templates with placeholder IDs:
    - `trial_results.svg` - Clinical trial summary card
    - `drug_mechanism.svg` - Mechanism of action explainer (4-step pathway)
    - `patient_stats.svg` - Patient demographics dashboard
    - `before_after.svg` - Before/after comparison layout
    - `risk_factors.svg` - Risk factor breakdown with bar charts
  - [x] Created `template_renderer.py` using lxml (more flexible than svglue)
  - [x] All 5 templates tested and generating SVG + PNG outputs
  - [x] Updated SKILL.md with complete Phase 2.2 documentation
  - [x] Updated handover file

**Generated Test Outputs (Session 6):**
```
outputs/
├── demo_trial_results.svg    (5KB)  - Trial summary infographic
├── demo_trial_results.png    (92KB)
├── demo_drug_mechanism.svg   (6KB)  - MOA explainer
├── demo_drug_mechanism.png   (127KB)
├── demo_patient_stats.svg    (7KB)  - Demographics dashboard
├── demo_patient_stats.png    (110KB)
├── demo_before_after.svg     (6KB)  - Before/after comparison
├── demo_before_after.png     (108KB)
├── demo_risk_factors.svg     (7KB)  - Risk factors visualization
└── demo_risk_factors.png     (111KB)
```

**Phase 2.2 COMPLETE!** SVG Infographic Templates with 5 templates:
→ trial_results, drug_mechanism, patient_stats, before_after, risk_factors
→ Uses lxml for direct SVG manipulation (more flexible than svglue)
→ CLI and Python API for rendering
→ PNG export at 2x scale (1600×1200)

### Session 7: 2026-01-01

**Completed:**
- [x] **Phase 2.3: mingrammer/diagrams Integration** - COMPLETE
  - [x] Installed `diagrams` package (v0.25.1) - already had graphviz via Homebrew
  - [x] Created `arch_diagrams/` directory (named to avoid shadowing `diagrams` package)
  - [x] Built `arch_diagrams/__init__.py` with lazy imports (prevents circular import)
  - [x] Built `arch_diagrams/treatment_pathways.py`:
    - `create_treatment_pathway()` - Generic clinical pathway builder
    - `create_heart_failure_pathway()` - HFrEF guideline algorithm
    - `create_acs_pathway()` - Acute Coronary Syndrome management
    - `create_af_pathway()` - Atrial Fibrillation treatment pathway
  - [x] Built `arch_diagrams/research_flows.py`:
    - `create_study_flow()` - Generic study flow builder
    - `create_consort_diagram()` - Clinical trial enrollment (CONSORT standard)
    - `create_prisma_diagram()` - Systematic review flow (PRISMA standard)
    - `create_methodology_flow()` - Research methodology visualization
  - [x] Built `arch_diagrams/healthcare_arch.py`:
    - `create_healthcare_system()` - Hospital/health system architecture
    - `create_cardiology_department()` - Cardiology dept structure
    - `create_data_pipeline()` - Clinical data pipeline visualization
  - [x] All 9 diagram types tested and generating successfully
  - [x] Uses local color palette matching design tokens
  - [x] Publication-quality styling with ortho splines
  - [x] Updated SKILL.md with complete Phase 2.3 documentation
  - [x] Updated handover file

**Generated Test Outputs (Session 7):**
```
outputs/
├── heart_failure_pathway.png    (67KB) - HFrEF treatment algorithm
├── acs_pathway.png              (82KB) - ACS management pathway
├── af_pathway.png               (79KB) - AF treatment pathway
├── consort_diagram.png          (52KB) - Clinical trial enrollment
├── prisma_diagram.png           (47KB) - Systematic review flow
├── methodology_flow.png         (31KB) - Research methodology
├── healthcare_system.png        (55KB) - Hospital architecture
├── cardiology_department.png    (77KB) - Cardiology dept structure
└── data_pipeline.png            (56KB) - Clinical data pipeline
```

### Session 8: 2026-01-01

**Completed:**
- [x] Added Satori carousel templates (`carousel-hook`, `carousel-myth`, `carousel-stat`, `carousel-tips`, `carousel-cta`)
- [x] Integrated carousel-generator-v2 with Satori via `scripts/satori_renderer.py`
- [x] Carousel test outputs generated in `carousel-generator-v2/outputs/`

**Phase 2 COMPLETE!** All design system phases done:
→ 9 architecture diagram types (3 pathways, 3 research flows, 3 system diagrams)
→ Uses mingrammer/diagrams for architecture-as-code
→ Lazy imports avoid circular import with diagrams package
→ Local color palette for publication consistency
→ Next: Continue Phase 3.1 (Manim) or harden carousel-generator-v2 Satori pipeline

---

### Session 9: 2026-01-01

**Completed:**
- [x] **Phase 3.1 scaffolding** - Manim animations started
- [x] Added `manim_animations/theme.py` (tokens-based colors + fonts)
- [x] Added `manim_animations/scenes.py` with 3 starter scenes:
  - Mechanism of Action flow
  - Kaplan-Meier survival curves
  - ECG normal sinus rhythm waveform
- [x] Added `scripts/render_manim.py` CLI wrapper (quality, format, output dir)
- [x] Installed Manim and rendered first low-quality test clip
- [x] Installed Manim into dedicated venv: `visual-design-system/.venv-manim`
- [x] Integrated Manim into carousel visual router (animation_scene routing)
- [x] Updated SKILL.md and handover

**Next (Phase 3.1):**
- Render remaining scenes (Kaplan-Meier, ECG)
- Add additional scenes (MOA variants, statistics explainer, anatomy)
- Expand router support (more Manim scenes + slide schema usage)

**Generated Test Outputs (Session 9):**
```
skills/cardiology/visual-design-system/outputs/manim/videos/scenes/1080p30/
└── MechanismOfActionScene.mp4
```

---

### Session 10: 2026-01-01

**Completed:**
- [x] Added Manim primitives + templates (`primitives.py`, `templates.py`)
- [x] Expanded scene library across six core categories (30 total scenes)
- [x] Added `scene_catalog.json` registry
- [x] Updated Manim CLI + visual router to read from scene catalog
- [x] Updated docs and handover

**Next (Phase 3.1):**
- Render remaining scenes from the catalog
- Add more anatomy and physiology modules
- Add a second batch of scenes once priorities are specified

---

## DEPENDENCIES TO INSTALL

### Python
```bash
pip install drawsvg cairosvg svgwrite pillow kaleido
pip install diagrams  # mingrammer diagrams
python -m venv skills/cardiology/visual-design-system/.venv-manim
skills/cardiology/visual-design-system/.venv-manim/bin/python -m pip install manim
```

### Node.js (for Satori)
```bash
npm install satori @resvg/resvg-js sharp
```

### System (macOS)
```bash
brew install graphviz  # Required for diagrams
brew install cairo     # Required for cairosvg
```

---

## CONTEXT FOR AI ASSISTANTS

### When Resuming This Project:

1. **Read "IMMEDIATE NEXT STEPS" section at top** - Has exact commands to verify and continue
2. **Phase 1 + Phase 2 are complete** - do not rebuild foundational work
3. **Phase 3.1 in progress** - Continue Manim animations or production hardening for carousel pipeline
4. **Use existing design tokens** - Import from `tokens/index.py`
5. **Update this file before session ends** - Keep the handover current
6. **Manim routing** - `carousel-generator-v2` routes slides with `animation_scene` to Manim (venv at `visual-design-system/.venv-manim`)
7. **Scene catalog** - `manim_animations/scene_catalog.json` is the registry for all Manim scenes
8. **Animations are opt-in** - Only slides with `animation_scene` render as Manim; otherwise static renderers are used

### Key File Paths:

```
/Users/shaileshsingh/integrated cowriting system/
├── VISUAL-SYSTEM-HANDOVER.md          # This file
├── skills/cardiology/visual-design-system/
│   ├── SKILL.md                       # Full documentation
│   ├── tokens/                        # ✅ Design tokens (COMPLETE)
│   │   ├── colors.json
│   │   ├── typography.json
│   │   ├── spacing.json
│   │   ├── shadows.json
│   │   └── index.py                   # Token API
│   ├── satori/                        # ✅ Infographic pipeline (COMPLETE)
│   │   ├── renderer.js                # 5 templates + carousel templates
│   │   ├── carousel-templates/        # hook/myth/stat/tips/cta
│   │   └── fonts/Roboto-*.ttf
│   ├── svg_diagrams/                  # ✅ Python SVG generation (COMPLETE)
│   │   ├── __init__.py                # Package with lazy imports
│   │   ├── medical_diagrams.py        # heart_simple, ecg_wave, etc.
│   │   ├── data_charts.py             # bar_chart, forest_plot, etc.
│   │   └── process_flows.py           # treatment_algorithm, etc.
│   ├── manim_animations/              # 🚧 Manim scenes (Phase 3.1)
│   │   ├── scenes.py                  # Scene library (catalog-driven)
│   │   ├── primitives.py              # Axes, flow blocks, anatomy modules
│   │   ├── templates.py               # Base scene templates
│   │   ├── scene_catalog.json         # Scene registry
│   │   └── theme.py                   # Tokens-based style
│   ├── scripts/
│   │   ├── token_validator.py         # ✅ WCAG validator
│   │   ├── generate_infographic.py    # ✅ Python wrapper
│   │   └── render_manim.py            # 🚧 Manim CLI wrapper
│   └── outputs/                       # Generated test files (30+ files)
```

### How to Use Existing Tokens in New Code:

```python
import sys
sys.path.insert(0, '/Users/shaileshsingh/integrated cowriting system/skills/cardiology/visual-design-system')

from tokens.index import get_color, get_accessible_pair, get_color_palette

# Get colors
navy = get_color("primary.navy")  # "#1e3a5f"
palette = get_color_palette("categorical")  # 7 colorblind-safe colors
treatment, control = get_accessible_pair("treatment_control")
```

**The Goal:** Every visual we produce should look like it was created by Nature's design team.

---

## NOTES & DECISIONS

### Design Decisions Made:
1. **Helvetica/Arial only** - Per Nature guidelines (Roboto bundled; add Helvetica/Arial files for true match)
2. **RGB color mode** - Better saturation, smaller files
3. **300 DPI minimum** - Publication standard
4. **No red-green contrast** - Colorblind accessibility
5. **Satori over alternatives** - Full React/Tailwind support, Vercel-backed

### Open Questions:
- Should we support dark mode for web visuals?
- Do we need CMYK export for print journals?
- Should Manim animations be optional or core?

---

---

## SESSION LOG

| Session | Date | Completed |
|---------|------|-----------|
| 1 | 2026-01-01 | Research, gap analysis, roadmap, handover file |
| 2 | 2026-01-01 | Phase 1.1 (tokens) + Phase 1.2 (Satori) - both working |
| 3 | 2026-01-01 | Phase 1.3 (svg_diagrams/drawsvg) - 16 diagram types, all tested |
| 4 | 2026-01-01 | Phase 1.4 (Plotly) - 300 DPI, WCAG validation, colorblind-safe |
| 5 | 2026-01-01 | Phase 2.1 (Component Library) - 6 reusable components |
| 6 | 2026-01-01 | Phase 2.2 (SVG Templates) - 5 infographic templates |
| 7 | 2026-01-01 | Phase 2.3 (Architecture Diagrams) - 9 diagram types via mingrammer/diagrams |
| 8 | 2026-01-01 | Handover sync: carousel Satori templates + carousel-generator-v2 integration noted |
| 9 | 2026-01-01 | Phase 3.1 started: Manim scaffolding (theme, scenes, CLI) |
| 10 | 2026-01-01 | Phase 3.1 expansion: Manim primitives, catalog, scene library |

---

*Last session ended: 2026-01-01*
*PHASE 2 COMPLETE - All design system phases done (tokens, Satori, svg_diagrams/drawsvg, Plotly, components, templates, arch diagrams)*
*PHASE 3.1 ACTIVE - Manim library (30 scenes) + catalog + router integration in place*
*Next: Render QA pack for Manim catalog or harden carousel-generator-v2 Satori pipeline*
*To resume: `Read VISUAL-SYSTEM-HANDOVER.md and continue Phase 3.1`*
