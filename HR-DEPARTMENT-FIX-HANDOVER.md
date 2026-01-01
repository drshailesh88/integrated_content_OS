# HR DEPARTMENT FIX - Complete Handover

**Created:** 2026-01-01
**Purpose:** Fix the disconnected skill awareness system (HR Department)
**Priority:** HIGH - Complete this before any other work

---

## INSTRUCTIONS FOR CLAUDE (READ THIS FIRST)

When you resume this session:

1. **DO NOT scan the codebase** - This file has everything you need
2. **DO NOT use Task/Explore agents** - They consume context unnecessarily
3. **FOLLOW THE STEPS BELOW IN ORDER** - They are precise and complete
4. **USE EDIT/WRITE TOOLS DIRECTLY** - All file paths and content are provided

---

## THE PROBLEM (WHY WE'RE DOING THIS)

The "HR Department" (system-awareness skill) is disconnected from the actual system:

```
CURRENT STATE (BROKEN):

skills/ directory          capability-registry.json       CLAUDE.md/GEMINI.md/AGENTS.md
├── 56 actual skills  ───X───  15 sample entries   ───X───  Manually maintained
                         │                            │
                    NO SYNC                      NO SYNC
                         │                            │
                    STALE DATA                  MANUAL DRIFT
```

**Result:** The system doesn't know its own capabilities. Gap detection is broken. Adding skills requires editing 4+ files manually.

---

## THE SOLUTION (WHAT WE'RE BUILDING)

```
TARGET STATE (FIXED):

skills/ directory
├── skill-1/SKILL.md
├── skill-2/SKILL.md
└── ...
        │
        ▼
   sync_skills.py (auto-discovers skills from disk)
        │
        ▼
capability-registry.json (SINGLE SOURCE OF TRUTH)
        │
        ▼
   generate_context.py (auto-updates context files)
        │
        ├──► CLAUDE.md (skill sections auto-generated)
        ├──► GEMINI.md (skill sections auto-generated)
        ├──► AGENTS.md (skill sections auto-generated)
        └──► SKILL-CATALOG.md (auto-generated)
```

---

## TASK CHECKLIST

| # | Task | Status | Time Est. |
|---|------|--------|-----------|
| 1 | Add 6 skill entries to capability-registry.json | ❌ NOT DONE | 5 min |
| 2 | Build sync_skills.py | ❌ NOT DONE | 15 min |
| 3 | Build generate_context.py | ❌ NOT DONE | 15 min |
| 4 | Update system-awareness SKILL.md | ❌ NOT DONE | 10 min |
| 5 | Test the pipeline end-to-end | ❌ NOT DONE | 10 min |

---

## TASK 1: Add 6 Skill Entries to capability-registry.json

### File Path
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/data/capability-registry.json
```

### What to Do
Add these 6 entries to the `"skills"` array after the `"authentic-voice"` entry (around line 226).

### Exact JSON to Insert

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
    },
```

### Also Update coverage_matrix

In the same file, update `coverage_matrix.domains.cardiology` to include the new skills:

```json
"cardiology": ["youtube-script-master", "x-post-creator-skill", "cardiology-newsletter-writer", "cardiology-trial-editorial", "cardiology-visual-system", "quick-topic-researcher", "content-seo-optimizer", "influencer-analyzer", "video-delivery-coach", "parallel-literature-search", "ensemble-content-scorer"]
```

And add to `coverage_matrix.outputs.analysis`:

```json
"analysis": ["viral-content-predictor", "cardiology-trial-editorial", "ensemble-content-scorer", "influencer-analyzer", "content-seo-optimizer"]
```

---

## TASK 2: Build sync_skills.py

### File Path to Create
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/sync_skills.py
```

### Complete Script

```python
#!/usr/bin/env python3
"""
sync_skills.py - Auto-discover skills from disk and update capability-registry.json

Usage:
    python sync_skills.py                    # Scan and report differences
    python sync_skills.py --update           # Actually update the registry
    python sync_skills.py --verbose          # Show detailed output
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
REGISTRY_PATH = DATA_DIR / "capability-registry.json"
SKILLS_ROOT = Path("/Users/shaileshsingh/integrated cowriting system/skills")

CARDIOLOGY_DIR = SKILLS_ROOT / "cardiology"
SCIENTIFIC_DIR = SKILLS_ROOT / "scientific"


def parse_skill_md(skill_path: Path) -> Optional[Dict]:
    """Parse a SKILL.md file to extract metadata."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Warning: Could not read {skill_md}: {e}")
        return None

    skill_id = skill_path.name

    # Extract name from first heading
    name_match = re.search(r'^#\s+(.+?)(?:\s*[-–—]\s*.+)?$', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else skill_id.replace('-', ' ').title()

    # Extract description from first paragraph after heading
    desc_match = re.search(r'^#.+?\n+(?:>\s*.+?\n+)?(.+?)(?:\n\n|\n#)', content, re.MULTILINE | re.DOTALL)
    description = ""
    if desc_match:
        description = desc_match.group(1).strip()
        description = re.sub(r'\s+', ' ', description)[:200]  # Limit length

    # Check for scripts directory
    scripts_dir = skill_path / "scripts"
    has_scripts = scripts_dir.exists() and any(scripts_dir.glob("*.py"))
    scripts = [f.name for f in scripts_dir.glob("*.py")] if has_scripts else []

    # Determine category from parent directory
    if "cardiology" in str(skill_path):
        category = "cardiology"
    elif "scientific" in str(skill_path):
        category = "scientific"
    else:
        category = "other"

    # Estimate complexity
    complexity = "low"
    if has_scripts:
        complexity = "medium"
        if len(scripts) > 2:
            complexity = "high"

    # Check for references directory
    refs_dir = skill_path / "references"
    has_references = refs_dir.exists() and any(refs_dir.iterdir())

    return {
        "id": skill_id,
        "name": name,
        "category": category,
        "subcategory": f"{category}/general",
        "description": description if description else f"Skill for {skill_id}",
        "inputs": [],
        "outputs": [],
        "dependencies": [],
        "use_cases": [],
        "coverage": [category],
        "has_scripts": has_scripts,
        "scripts": scripts,
        "has_references": has_references,
        "complexity": complexity,
        "usage_count": 0,
        "last_used": None,
        "auto_discovered": True,
        "discovered_at": datetime.now().isoformat()
    }


def scan_skills_directory(directory: Path) -> List[Dict]:
    """Scan a directory for skills (directories containing SKILL.md)."""
    skills = []

    if not directory.exists():
        print(f"  Warning: Directory does not exist: {directory}")
        return skills

    for item in directory.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_data = parse_skill_md(item)
            if skill_data:
                skills.append(skill_data)

    return skills


def load_registry() -> Dict:
    """Load the current capability registry."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"metadata": {}, "categories": {}, "skills": [], "coverage_matrix": {}, "gap_indicators": {}}


def save_registry(registry: Dict) -> None:
    """Save the capability registry."""
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def compare_skills(disk_skills: List[Dict], registry_skills: List[Dict]) -> Tuple[List[Dict], List[Dict], List[str]]:
    """Compare disk skills with registry skills."""
    disk_ids = {s['id'] for s in disk_skills}
    registry_ids = {s['id'] for s in registry_skills}

    new_skills = [s for s in disk_skills if s['id'] not in registry_ids]
    missing_from_disk = [s['id'] for s in registry_skills if s['id'] not in disk_ids]
    existing = [s for s in disk_skills if s['id'] in registry_ids]

    return new_skills, existing, missing_from_disk


def main():
    parser = argparse.ArgumentParser(description="Sync skills from disk to capability registry")
    parser.add_argument('--update', action='store_true', help="Actually update the registry")
    parser.add_argument('--verbose', '-v', action='store_true', help="Verbose output")
    args = parser.parse_args()

    print("=" * 60)
    print("SKILL SYNC - Scanning disk for skills")
    print("=" * 60)

    # Scan directories
    print("\n📂 Scanning cardiology skills...")
    cardiology_skills = scan_skills_directory(CARDIOLOGY_DIR)
    print(f"   Found: {len(cardiology_skills)} skills")

    print("\n📂 Scanning scientific skills...")
    scientific_skills = scan_skills_directory(SCIENTIFIC_DIR)
    print(f"   Found: {len(scientific_skills)} skills")

    all_disk_skills = cardiology_skills + scientific_skills
    print(f"\n📊 Total skills on disk: {len(all_disk_skills)}")

    # Load registry
    print("\n📋 Loading capability registry...")
    registry = load_registry()
    registry_skills = registry.get('skills', [])
    print(f"   Registry has: {len(registry_skills)} skills")

    # Compare
    new_skills, existing, missing = compare_skills(all_disk_skills, registry_skills)

    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)

    print(f"\n✅ Skills in registry and on disk: {len(existing)}")
    print(f"🆕 NEW skills (on disk, not in registry): {len(new_skills)}")
    print(f"⚠️  MISSING from disk (in registry only): {len(missing)}")

    if args.verbose or new_skills:
        print("\n--- NEW SKILLS ---")
        for s in new_skills:
            print(f"  + {s['id']} ({s['category']})")
            if args.verbose:
                print(f"    Description: {s['description'][:80]}...")

    if args.verbose and missing:
        print("\n--- MISSING FROM DISK ---")
        for sid in missing:
            print(f"  - {sid}")

    # Update if requested
    if args.update and new_skills:
        print("\n" + "=" * 60)
        print("UPDATING REGISTRY")
        print("=" * 60)

        # Add new skills
        for skill in new_skills:
            registry['skills'].append(skill)
            print(f"  ✅ Added: {skill['id']}")

        # Update metadata
        registry['metadata']['last_sync'] = datetime.now().strftime('%Y-%m-%d')
        registry['metadata']['total_skills'] = len(registry['skills'])
        registry['metadata']['cardiology_skills'] = len([s for s in registry['skills'] if s['category'] == 'cardiology'])
        registry['metadata']['scientific_skills'] = len([s for s in registry['skills'] if s['category'] == 'scientific'])

        # Save
        save_registry(registry)
        print(f"\n💾 Registry saved with {len(registry['skills'])} skills")

    elif new_skills and not args.update:
        print("\n💡 Run with --update to add new skills to registry")

    print("\n✨ Sync complete!")
    return 0


if __name__ == "__main__":
    exit(main())
```

---

## TASK 3: Build generate_context.py

### File Path to Create
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/generate_context.py
```

### Complete Script

```python
#!/usr/bin/env python3
"""
generate_context.py - Generate skill sections for context files from capability-registry.json

Usage:
    python generate_context.py                    # Preview what would be generated
    python generate_context.py --update           # Actually update context files
    python generate_context.py --file CLAUDE.md   # Update specific file only
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
REGISTRY_PATH = DATA_DIR / "capability-registry.json"
PROJECT_ROOT = Path("/Users/shaileshsingh/integrated cowriting system")

# Context files to update
CONTEXT_FILES = {
    "CLAUDE.md": PROJECT_ROOT / "CLAUDE.md",
    "GEMINI.md": PROJECT_ROOT / "GEMINI.md",
    "AGENTS.md": PROJECT_ROOT / "AGENTS.md",
    "SKILL-CATALOG.md": PROJECT_ROOT / "SKILL-CATALOG.md"
}

# Section markers
SECTION_START = "<!-- AUTO-GENERATED SKILLS START -->"
SECTION_END = "<!-- AUTO-GENERATED SKILLS END -->"


def load_registry() -> Dict:
    """Load the capability registry."""
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_skills_table(skills: List[Dict], category_filter: str = None) -> str:
    """Generate a markdown table of skills."""
    if category_filter:
        skills = [s for s in skills if s.get('category') == category_filter]

    if not skills:
        return "_No skills in this category_\n"

    lines = ["| Skill | Purpose |", "|-------|---------|"]

    for skill in sorted(skills, key=lambda x: x['id']):
        name = f"`{skill['id']}`"
        desc = skill.get('description', '')[:80]
        if len(skill.get('description', '')) > 80:
            desc += "..."
        lines.append(f"| {name} | {desc} |")

    return "\n".join(lines) + "\n"


def generate_skills_by_subcategory(skills: List[Dict], category: str) -> str:
    """Generate skills organized by subcategory."""
    filtered = [s for s in skills if s.get('category') == category]

    # Group by subcategory
    by_subcat = {}
    for skill in filtered:
        subcat = skill.get('subcategory', 'general')
        # Extract the part after the slash
        if '/' in subcat:
            subcat = subcat.split('/')[-1]
        subcat = subcat.replace('-', ' ').title()

        if subcat not in by_subcat:
            by_subcat[subcat] = []
        by_subcat[subcat].append(skill)

    lines = []
    for subcat, subcat_skills in sorted(by_subcat.items()):
        lines.append(f"\n#### {subcat}")
        lines.append("| Skill | Purpose |")
        lines.append("|-------|---------|")
        for skill in sorted(subcat_skills, key=lambda x: x['id']):
            desc = skill.get('description', '')[:60]
            if len(skill.get('description', '')) > 60:
                desc += "..."
            lines.append(f"| `{skill['id']}` | {desc} |")

    return "\n".join(lines) + "\n"


def generate_skill_catalog(skills: List[Dict]) -> str:
    """Generate content for SKILL-CATALOG.md."""
    lines = [
        "# Skill Catalog - Purpose-Based Lookup",
        "",
        "> **Quick Reference:** Find the right skill for your task",
        "",
        f"_Auto-generated from capability-registry.json on {datetime.now().strftime('%Y-%m-%d')}_",
        "",
        "---",
        "",
        "## Cardiology Skills",
        ""
    ]

    lines.append(generate_skills_by_subcategory(skills, 'cardiology'))

    lines.extend([
        "",
        "---",
        "",
        "## Scientific Skills",
        ""
    ])

    lines.append(generate_skills_by_subcategory(skills, 'scientific'))

    return "\n".join(lines)


def generate_context_section(skills: List[Dict], file_type: str) -> str:
    """Generate the skills section for a context file."""
    cardiology = [s for s in skills if s.get('category') == 'cardiology']
    scientific = [s for s in skills if s.get('category') == 'scientific']

    lines = [
        SECTION_START,
        "",
        f"## COMPLETE SKILLS INVENTORY ({len(skills)}+ Skills)",
        "",
        f"_Auto-generated on {datetime.now().strftime('%Y-%m-%d')} - DO NOT EDIT MANUALLY_",
        "",
        f"### Cardiology Skills ({len(cardiology)} Skills)",
        "**Location:** `skills/cardiology/`",
        ""
    ]

    lines.append(generate_skills_by_subcategory(skills, 'cardiology'))

    lines.extend([
        "",
        f"### Scientific Skills ({len(scientific)} Skills)",
        "**Location:** `skills/scientific/`",
        "",
        "Databases, bioinformatics, data science tools. Full inventory in capability-registry.json.",
        "",
        SECTION_END
    ])

    return "\n".join(lines)


def update_context_file(file_path: Path, new_section: str) -> bool:
    """Update a context file with the new skills section."""
    if not file_path.exists():
        print(f"  Warning: File does not exist: {file_path}")
        return False

    content = file_path.read_text(encoding='utf-8')

    # Check if markers exist
    if SECTION_START in content and SECTION_END in content:
        # Replace existing section
        pattern = re.escape(SECTION_START) + r'.*?' + re.escape(SECTION_END)
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    else:
        # Markers don't exist - inform user
        print(f"  ⚠️  No auto-generated section markers found in {file_path.name}")
        print(f"      Add these markers where you want the skills section:")
        print(f"      {SECTION_START}")
        print(f"      {SECTION_END}")
        return False

    file_path.write_text(new_content, encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate skills sections for context files")
    parser.add_argument('--update', action='store_true', help="Actually update the files")
    parser.add_argument('--file', type=str, help="Update specific file only")
    parser.add_argument('--preview', action='store_true', help="Preview generated content")
    args = parser.parse_args()

    print("=" * 60)
    print("GENERATE CONTEXT - Building skills sections")
    print("=" * 60)

    # Load registry
    print("\n📋 Loading capability registry...")
    registry = load_registry()
    skills = registry.get('skills', [])
    print(f"   Found: {len(skills)} skills")

    cardiology_count = len([s for s in skills if s.get('category') == 'cardiology'])
    scientific_count = len([s for s in skills if s.get('category') == 'scientific'])
    print(f"   Cardiology: {cardiology_count}, Scientific: {scientific_count}")

    # Generate sections
    print("\n📝 Generating content...")

    if args.preview:
        section = generate_context_section(skills, "preview")
        print("\n" + "=" * 40)
        print("PREVIEW:")
        print("=" * 40)
        print(section)
        return 0

    if args.update:
        print("\n📂 Updating context files...")

        files_to_update = CONTEXT_FILES
        if args.file:
            if args.file in CONTEXT_FILES:
                files_to_update = {args.file: CONTEXT_FILES[args.file]}
            else:
                print(f"  Error: Unknown file {args.file}")
                print(f"  Available: {', '.join(CONTEXT_FILES.keys())}")
                return 1

        for name, path in files_to_update.items():
            if name == "SKILL-CATALOG.md":
                content = generate_skill_catalog(skills)
                path.write_text(content, encoding='utf-8')
                print(f"  ✅ Updated: {name} (full rewrite)")
            else:
                section = generate_context_section(skills, name)
                if update_context_file(path, section):
                    print(f"  ✅ Updated: {name}")
                else:
                    print(f"  ⏭️  Skipped: {name} (no markers)")

        print("\n💾 Context files updated!")
    else:
        print("\n💡 Run with --update to modify files")
        print("   Run with --preview to see generated content")

    print("\n✨ Complete!")
    return 0


if __name__ == "__main__":
    exit(main())
```

---

## TASK 4: Update system-awareness SKILL.md

### File Path
```
/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/SKILL.md
```

### What to Add

Add this new section after the "Commands Reference" section (around line 360):

```markdown
---

## Connected Sync Architecture

The system-awareness skill now maintains a **connected pipeline** from disk to context files.

### The Sync Pipeline

```
skills/cardiology/*          skills/scientific/*
        │                           │
        └───────────┬───────────────┘
                    │
                    ▼
            sync_skills.py
     (Scans directories for SKILL.md)
                    │
                    ▼
        capability-registry.json
         (SINGLE SOURCE OF TRUTH)
                    │
                    ▼
          generate_context.py
     (Rebuilds context file sections)
                    │
        ┌───────────┼───────────┬───────────────┐
        ▼           ▼           ▼               ▼
   CLAUDE.md   GEMINI.md   AGENTS.md   SKILL-CATALOG.md
```

### Sync Commands

```bash
# Discover new skills from disk
python scripts/sync_skills.py              # Report only
python scripts/sync_skills.py --update     # Add to registry

# Regenerate context files
python scripts/generate_context.py --preview   # See what would be generated
python scripts/generate_context.py --update    # Update all context files

# Full sync pipeline
python scripts/sync_skills.py --update && python scripts/generate_context.py --update
```

### When to Run

- **After adding a new skill**: Run full pipeline
- **Weekly maintenance**: Run `sync_skills.py` to check for drift
- **Before major sessions**: Ensure registry is current

### Auto-Generated Section Markers

Context files (CLAUDE.md, GEMINI.md, AGENTS.md) must contain these markers for auto-update:

```markdown
<!-- AUTO-GENERATED SKILLS START -->
... skills content here ...
<!-- AUTO-GENERATED SKILLS END -->
```

Content between these markers will be replaced by `generate_context.py`.
```

---

## TASK 5: Test the Pipeline

After completing Tasks 1-4, run this test:

### Test Commands

```bash
cd "/Users/shaileshsingh/integrated cowriting system"

# 1. Verify registry has new skills
python -c "import json; r=json.load(open('skills/cardiology/system-awareness/data/capability-registry.json')); print(f'Skills in registry: {len(r[\"skills\"])}')"

# 2. Run sync to find any new skills
python skills/cardiology/system-awareness/scripts/sync_skills.py --verbose

# 3. Preview context generation
python skills/cardiology/system-awareness/scripts/generate_context.py --preview
```

### Expected Results

1. Registry should have 21+ skills (15 original + 6 new)
2. sync_skills.py should find many more skills on disk
3. generate_context.py should show the skills table

---

## KEY FILE PATHS (Quick Reference)

| File | Absolute Path |
|------|---------------|
| capability-registry.json | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/data/capability-registry.json` |
| sync_skills.py | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/sync_skills.py` |
| generate_context.py | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/scripts/generate_context.py` |
| system-awareness SKILL.md | `/Users/shaileshsingh/integrated cowriting system/skills/cardiology/system-awareness/SKILL.md` |
| CLAUDE.md | `/Users/shaileshsingh/integrated cowriting system/CLAUDE.md` |
| GEMINI.md | `/Users/shaileshsingh/integrated cowriting system/GEMINI.md` |
| AGENTS.md | `/Users/shaileshsingh/integrated cowriting system/AGENTS.md` |
| SKILL-CATALOG.md | `/Users/shaileshsingh/integrated cowriting system/SKILL-CATALOG.md` |

---

## WHAT NOT TO DO

1. **DO NOT** scan the full codebase - it wastes context
2. **DO NOT** use Task/Explore agents - this handover has everything
3. **DO NOT** read CLAUDE.md, GEMINI.md, AGENTS.md - they're not needed for this task
4. **DO NOT** try to understand the full system - just fix the HR department

---

## SUCCESS CRITERIA

When done, you should be able to:

1. Run `sync_skills.py --update` and it discovers all skills from disk
2. Run `generate_context.py --update` and it updates context files
3. Adding a new skill directory with SKILL.md auto-appears in registry after sync
4. capability-registry.json has 50+ skills (not just 15 samples)

---

## RESUME PROMPT

When you start a fresh session, tell Claude:

```
Read /Users/shaileshsingh/integrated\ cowriting\ system/HR-DEPARTMENT-FIX-HANDOVER.md and complete Tasks 1-5 in order. Do not scan the codebase. The handover file has everything you need.
```

---

*Handover created: 2026-01-01*
*Purpose: Fix HR Department (system-awareness) sync architecture*
*Estimated time to complete: 45 minutes*
