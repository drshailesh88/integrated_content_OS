# System Awareness - The Self-Evolving Skill Manager

> **Meta-Skill**: This skill manages all other skills. It observes gaps, proposes new capabilities, and helps the system evolve.

## Philosophy

This system operates like an **HR department** for your content operating system:
- **Workforce Planning**: Detects when capabilities are missing
- **Job Descriptions**: Defines what new skills should do
- **Recruitment**: Proposes and helps build new skills
- **Performance Reviews**: Tracks which skills are used and effective

## The Self-Awareness Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│     │  OBSERVE │─────▶│  ANALYZE │─────▶│  PROPOSE │              │
│     │          │      │          │      │          │              │
│     │ Log gaps │      │ Patterns │      │ New skill│              │
│     │ & wishes │      │ & priority│     │ specs    │              │
│     └──────────┘      └──────────┘      └──────────┘              │
│           ▲                                   │                    │
│           │                                   ▼                    │
│     ┌──────────┐                        ┌──────────┐              │
│     │  LEARN   │◀───────────────────────│  REVIEW  │              │
│     │          │                        │          │              │
│     │ From     │                        │ Human    │              │
│     │ outcomes │                        │ approves │              │
│     └──────────┘                        └──────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Log a Gap (When something couldn't be done)

```bash
# When you encounter something the system can't do:
python scripts/gap_logger.py "I need to analyze ECG waveforms from images"

# With more context:
python scripts/gap_logger.py \
  --request "Analyze ECG images for abnormalities" \
  --context "User uploaded 12-lead ECG, wanted automated interpretation" \
  --category "medical-imaging" \
  --urgency "high"
```

### 2. Analyze Gaps (Weekly review)

```bash
# See all logged gaps:
python scripts/gap_analyzer.py --list

# Analyze patterns and prioritize:
python scripts/gap_analyzer.py --analyze

# Generate priority report:
python scripts/gap_analyzer.py --report
```

### 3. Propose a New Skill

```bash
# Generate a skill proposal from a gap:
python scripts/skill_proposer.py --gap-id "gap_2024_001"

# Or describe what you need:
python scripts/skill_proposer.py \
  --name "ecg-image-analyzer" \
  --purpose "Analyze ECG images for rhythm abnormalities" \
  --inputs "ECG image file (PNG/JPG)" \
  --outputs "Structured analysis with findings"
```

---

## Core Components

### 1. Capability Registry (`data/capability-registry.json`)

A structured database of all 184+ skills with their:
- **Inputs**: What they accept
- **Outputs**: What they produce
- **Dependencies**: What they need to work
- **Use Cases**: When to use them
- **Coverage**: What domains they serve

```json
{
  "skills": [
    {
      "id": "youtube-script-master",
      "category": "cardiology/content-creation",
      "inputs": ["topic", "research_data", "target_duration"],
      "outputs": ["hinglish_script", "hooks", "cta_suggestions"],
      "dependencies": ["research-engine", "knowledge-pipeline"],
      "use_cases": ["youtube_content", "hinglish_video", "educational_script"],
      "coverage": ["cardiology", "patient-education", "hinglish"],
      "last_used": "2024-12-31",
      "usage_count": 47
    }
  ]
}
```

### 2. Gap Log (`data/gap-log.json`)

Records every unmet need:

```json
{
  "gaps": [
    {
      "id": "gap_2024_001",
      "timestamp": "2024-12-31T10:30:00",
      "request": "Analyze ECG waveform from uploaded image",
      "context": "User uploaded 12-lead ECG, wanted P-wave, QRS, ST analysis",
      "category": "medical-imaging",
      "urgency": "medium",
      "frequency": 3,
      "similar_requests": ["ecg interpretation", "arrhythmia detection"],
      "potential_skill": "ecg-image-analyzer",
      "status": "open"
    }
  ]
}
```

### 3. Skill Backlog (`data/skill-backlog.json`)

Prioritized list of skills to build (your "open positions"):

```json
{
  "backlog": [
    {
      "id": "backlog_001",
      "proposed_skill": "ecg-image-analyzer",
      "priority": "high",
      "gap_count": 5,
      "estimated_impact": "high",
      "complexity": "medium",
      "dependencies_available": true,
      "proposed_by": "gap_analyzer",
      "status": "pending_approval",
      "spec_generated": true,
      "spec_path": "data/skill-templates/ecg-image-analyzer-spec.md"
    }
  ]
}
```

---

## Gap Detection Patterns

The system recognizes these patterns as skill gaps:

### Pattern 1: Direct Failure
```
User: "Can you analyze this ECG image?"
Claude: "I don't have a skill for medical image analysis..."
→ LOG: Gap detected - medical-imaging capability missing
```

### Pattern 2: Manual Workaround
```
User: "Let me manually extract the data and paste it..."
→ LOG: Gap detected - automation opportunity for data extraction
```

### Pattern 3: External Tool Request
```
User: "I'll use [external tool] for this part"
→ LOG: Gap detected - capability exists externally but not internally
```

### Pattern 4: Repeated Questions
```
User asks about "podcast transcription" 4 times in 2 weeks
→ LOG: Gap detected - high-frequency unmet need
```

### Pattern 5: Wishful Thinking
```
User: "I wish the system could automatically..."
→ LOG: Gap detected - explicit user desire
```

---

## How to Log Gaps (For Claude)

When you (Claude) encounter something you cannot do, use this protocol:

### Immediate Logging (During Conversation)

When you hit a capability gap, note it in the response:

```
I notice we don't have a skill for [X]. I'm logging this as a potential gap.

**Gap Logged:**
- Request: [what was asked]
- Category: [domain]
- Potential Skill: [suggested name]

You can review gaps with: `python scripts/gap_analyzer.py --list`
```

### End-of-Session Gap Review

At the end of complex sessions, summarize any gaps encountered:

```
## Session Gap Summary

| Gap | Category | Urgency | Potential Skill |
|-----|----------|---------|-----------------|
| ECG image analysis | medical-imaging | high | ecg-image-analyzer |
| Podcast transcription | media-processing | medium | audio-transcriber |

Run `python scripts/gap_analyzer.py --session-review` to add these to the backlog.
```

---

## Skill Proposal Format

When proposing a new skill, use this template:

```markdown
# Proposed Skill: [skill-name]

## Gap Analysis
- **Gap ID(s)**: gap_2024_001, gap_2024_007
- **Request Frequency**: 5 times in 2 weeks
- **User Impact**: High (blocks common workflow)

## Skill Specification

### Purpose
[One sentence describing what this skill does]

### Inputs
- Input 1: [type] - [description]
- Input 2: [type] - [description]

### Outputs
- Output 1: [type] - [description]

### Dependencies
- [ ] Existing skill: [name]
- [ ] API: [name]
- [ ] Library: [name]

### Use Cases
1. [Primary use case]
2. [Secondary use case]

### Estimated Complexity
- [ ] Simple (documentation only)
- [ ] Medium (docs + reference files)
- [ ] Complex (docs + scripts + API integration)

### Similar Skills (to learn from)
- [existing-skill-1]: [what to borrow]
- [existing-skill-2]: [what to borrow]

## Recommendation
**BUILD / DEFER / MERGE with [existing-skill]**

Rationale: [why this recommendation]
```

---

## Integration with Claude

### Automatic Gap Detection Triggers

Claude should log gaps when:

1. **"I can't"** - Any statement of inability
2. **"This would require"** - Identifying missing capability
3. **"You'll need to use"** - Pointing to external tools
4. **"If we had"** - Wishful capability statements
5. **User frustration** - Repeated attempts at same task

### Gap Logging Command

When Claude detects a gap, append to conversation:

```
📋 **Gap Logged**: [brief description]
Category: [category] | Urgency: [low/medium/high]
```

### Weekly Review Prompt

Add to weekly workflow:

```
"Review the skill gap log and propose any new skills that should be built this week."
```

---

## Governance & Approval

### Gap → Skill Pipeline

```
1. GAP LOGGED
   ↓
2. PATTERN DETECTED (3+ similar requests)
   ↓
3. PROPOSAL GENERATED (skill_proposer.py)
   ↓
4. HUMAN REVIEW (you approve/reject/modify)
   ↓
5. SKILL BUILT (if approved)
   ↓
6. REGISTRY UPDATED (capability-registry.json)
   ↓
7. SKILL DEPLOYED (available for use)
```

### Approval Criteria

Before approving a new skill, consider:

- [ ] **Frequency**: Is this needed often enough?
- [ ] **Impact**: Does it unblock important workflows?
- [ ] **Feasibility**: Can we actually build this?
- [ ] **Overlap**: Does an existing skill already do this?
- [ ] **Maintenance**: Can we keep this updated?

---

## Commands Reference

```bash
# Gap Management
python scripts/gap_logger.py "description"        # Log a new gap
python scripts/gap_analyzer.py --list             # List all gaps
python scripts/gap_analyzer.py --analyze          # Analyze patterns
python scripts/gap_analyzer.py --report           # Generate priority report

# Skill Proposals
python scripts/skill_proposer.py --gap-id "id"    # Propose from gap
python scripts/skill_proposer.py --interactive    # Interactive proposal builder

# Registry
python scripts/registry_updater.py --scan         # Scan for new skills
python scripts/registry_updater.py --stats        # Show usage statistics
python scripts/registry_updater.py --unused       # Find unused skills
```

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

---

## Complete HR Pipeline (End-to-End)

The system now has a **fully integrated pipeline** from gap detection to skill deployment:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        THE COMPLETE HR LOOP                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. GAP DETECTED                                                                │
│     └─► gap_logger.py → gap-log.json                                           │
│                                                                                 │
│  2. GAPS ANALYZED                                                               │
│     └─► gap_analyzer.py → patterns, priorities                                 │
│                                                                                 │
│  3. SKILL PROPOSED                                                              │
│     └─► skill_proposer.py → skill-templates/*.md                               │
│                                                                                 │
│  4. SKILL BUILT ★ (one command)                                                │
│     └─► skill_builder.py → skills/cardiology/[name]/                           │
│         ├── Creates SKILL.md                                                   │
│         ├── Creates scripts/ & references/                                     │
│         ├── Marks gap as resolved                                              │
│         └── Archives proposal                                                  │
│                                                                                 │
│  5. SYSTEM SYNCED (auto-runs)                                                  │
│     └─► sync_skills.py → capability-registry.json                              │
│                                                                                 │
│  6. CONTEXT UPDATED (auto-runs)                                                │
│     └─► generate_context.py → CLAUDE.md, GEMINI.md, etc.                       │
│                                                                                 │
│  7. SKILL AVAILABLE ✓                                                          │
│     └─► Ready to use in next conversation                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Quick Commands

```bash
# Log a gap
python scripts/gap_logger.py "I need to analyze ECG images"

# Analyze gaps and find patterns
python scripts/gap_analyzer.py --report

# Create a proposal from a gap
python scripts/skill_proposer.py --gap-id gap_xxxx

# BUILD the skill (one command does everything)
python scripts/skill_builder.py --proposal ecg-analyzer-proposal.md

# Or build directly from a gap (skip proposal step)
python scripts/skill_builder.py --from-gap gap_xxxx

# Or build directly with name and purpose
python scripts/skill_builder.py --name "ecg-analyzer" --purpose "Analyze ECG images"
```

### Skill Builder Options

```bash
python skill_builder.py --list-proposals    # See pending proposals
python skill_builder.py --list-gaps         # See open gaps
python skill_builder.py --proposal FILE     # Build from proposal
python skill_builder.py --from-gap ID       # Build from gap (fast path)
python skill_builder.py --name X --purpose Y # Build directly
python skill_builder.py --no-sync           # Skip auto-sync (manual control)
```

---

## Files in This Skill

```
system-awareness/
├── SKILL.md                         # This file
├── data/
│   ├── capability-registry.json     # All 190+ skills inventory
│   ├── gap-log.json                 # Logged capability gaps
│   ├── skill-backlog.json           # Prioritized build queue
│   └── skill-templates/             # Skill proposals
│       ├── approved/                # Archived approved proposals
│       └── *-proposal.md            # Pending proposals
├── scripts/
│   ├── gap_logger.py                # Log unmet requests
│   ├── gap_analyzer.py              # Analyze gap patterns
│   ├── skill_proposer.py            # Generate skill proposals
│   ├── skill_builder.py             # ★ BUILD skills (the missing piece)
│   ├── sync_skills.py               # Discover skills from disk
│   └── generate_context.py          # Update context files
└── references/
    ├── skill-anatomy.md             # What makes a good skill
    └── gap-patterns.md              # Common gap pattern recognition
```

---

## Philosophy: The Living System

This system embodies a key principle: **software should grow with its users**.

Instead of static capabilities, this creates:
- **Adaptive**: Learns what's missing from real usage
- **Transparent**: You see exactly what gaps exist
- **Collaborative**: Human approves, system builds
- **Sustainable**: Only builds what's truly needed

The goal isn't to build every possible skill. It's to build the **right** skills at the **right** time based on **real** needs.

---

*"The best systems don't just serve users—they learn from them."*
