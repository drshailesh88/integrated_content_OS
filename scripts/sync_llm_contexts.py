#!/usr/bin/env python3
"""
Sync LLM Context Files (CLAUDE.md ↔ GEMINI.md ↔ AGENTS.md)

This script helps keep the shared sections between all three context files in sync.

Sections that SHOULD be synced (identical content):
- Skills inventory
- Pipelines
- Directory structure
- Voice standards
- API keys reference

Sections that are MODEL-SPECIFIC (don't sync):
- Opening context (different for each model)
- Coordination instructions
- Model-specific strengths
- Session management

Usage:
    python scripts/sync_llm_contexts.py --check          # Check if files are in sync
    python scripts/sync_llm_contexts.py --show-diff      # Show differences
    python scripts/sync_llm_contexts.py --update-all     # Update GEMINI.md and AGENTS.md from CLAUDE.md
    python scripts/sync_llm_contexts.py --update-gemini  # Update GEMINI.md only
    python scripts/sync_llm_contexts.py --update-agents  # Update AGENTS.md only
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# Sections that should be kept in sync
SYNC_SECTIONS = [
    "COMPLETE SKILLS INVENTORY",
    "PIPELINES",
    "DIRECTORY STRUCTURE",
    "VOICE STANDARDS",
    "API KEYS",
]

# Sections that are model-specific (don't sync)
MODEL_SPECIFIC_SECTIONS = {
    "CLAUDE.md": [
        "CLAUDE: YOUR SUPERPOWERS",
        "YOUR MULTI-MODEL ARSENAL",
        "CONTEXT WINDOW MANAGEMENT",
    ],
    "GEMINI.md": [
        "GEMINI: YOUR ROLE IN THIS SYSTEM",
        "COORDINATION WITH CLAUDE CODE",
        "GEMINI-SPECIFIC STRENGTHS",
        "SESSION MANAGEMENT",
    ]
}


def get_project_root():
    """Get the project root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent


def read_file(filepath):
    """Read a file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_section(content, section_name):
    """Extract a section from markdown content."""
    # Match ## SECTION_NAME or variations
    pattern = rf'^##\s+{re.escape(section_name)}.*?(?=^##\s|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return None


def check_sync(claude_content, gemini_content):
    """Check if sync sections are identical."""
    differences = []

    for section in SYNC_SECTIONS:
        claude_section = extract_section(claude_content, section)
        gemini_section = extract_section(gemini_content, section)

        if claude_section is None:
            differences.append(f"  - {section}: Missing in CLAUDE.md")
        elif gemini_section is None:
            differences.append(f"  - {section}: Missing in GEMINI.md")
        elif claude_section != gemini_section:
            differences.append(f"  - {section}: Content differs")

    return differences


def show_diff(claude_content, gemini_content):
    """Show detailed differences between files."""
    print("\n" + "="*60)
    print("SECTION COMPARISON")
    print("="*60)

    for section in SYNC_SECTIONS:
        claude_section = extract_section(claude_content, section)
        gemini_section = extract_section(gemini_content, section)

        print(f"\n## {section}")
        print("-"*40)

        if claude_section == gemini_section:
            print("  [SYNCED] Sections are identical")
        else:
            if claude_section:
                claude_lines = len(claude_section.split('\n'))
                print(f"  CLAUDE.md: {claude_lines} lines")
            else:
                print("  CLAUDE.md: MISSING")

            if gemini_section:
                gemini_lines = len(gemini_section.split('\n'))
                print(f"  GEMINI.md: {gemini_lines} lines")
            else:
                print("  GEMINI.md: MISSING")


def update_gemini_from_claude(project_root):
    """Update GEMINI.md sync sections from CLAUDE.md."""
    claude_path = project_root / "CLAUDE.md"
    gemini_path = project_root / "GEMINI.md"

    claude_content = read_file(claude_path)
    gemini_content = read_file(gemini_path)

    updated_content = gemini_content
    updates_made = []

    for section in SYNC_SECTIONS:
        claude_section = extract_section(claude_content, section)

        if claude_section:
            # Find and replace in GEMINI.md
            pattern = rf'^##\s+{re.escape(section)}.*?(?=^##\s|\Z)'
            if re.search(pattern, gemini_content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
                updated_content = re.sub(
                    pattern,
                    claude_section,
                    updated_content,
                    flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
                )
                updates_made.append(section)

    if updates_made:
        # Backup original
        backup_path = gemini_path.with_suffix('.md.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(gemini_content)

        # Write updated content
        with open(gemini_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return updates_made, str(backup_path)

    return [], None


def update_file_from_claude(project_root, target_filename):
    """Update a target file's sync sections from CLAUDE.md."""
    claude_path = project_root / "CLAUDE.md"
    target_path = project_root / target_filename

    if not target_path.exists():
        print(f"  Warning: {target_filename} not found, skipping")
        return [], None

    claude_content = read_file(claude_path)
    target_content = read_file(target_path)

    updated_content = target_content
    updates_made = []

    for section in SYNC_SECTIONS:
        claude_section = extract_section(claude_content, section)

        if claude_section:
            pattern = rf'^##\s+{re.escape(section)}.*?(?=^##\s|\Z)'
            if re.search(pattern, target_content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
                updated_content = re.sub(
                    pattern,
                    claude_section,
                    updated_content,
                    flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
                )
                updates_made.append(section)

    if updates_made:
        backup_path = target_path.with_suffix('.md.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(target_content)

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return updates_made, str(backup_path)

    return [], None


def main():
    parser = argparse.ArgumentParser(description="Sync LLM context files")
    parser.add_argument('--check', action='store_true', help='Check if files are in sync')
    parser.add_argument('--show-diff', action='store_true', help='Show differences')
    parser.add_argument('--update-gemini', action='store_true', help='Update GEMINI.md from CLAUDE.md')
    parser.add_argument('--update-agents', action='store_true', help='Update AGENTS.md from CLAUDE.md')
    parser.add_argument('--update-all', action='store_true', help='Update both GEMINI.md and AGENTS.md')
    args = parser.parse_args()

    project_root = get_project_root()
    claude_path = project_root / "CLAUDE.md"
    gemini_path = project_root / "GEMINI.md"
    agents_path = project_root / "AGENTS.md"

    if not claude_path.exists():
        print(f"Error: CLAUDE.md not found at {claude_path}")
        return 1

    claude_content = read_file(claude_path)

    # Check which files exist
    files_to_check = []
    if gemini_path.exists():
        files_to_check.append(("GEMINI.md", read_file(gemini_path)))
    if agents_path.exists():
        files_to_check.append(("AGENTS.md", read_file(agents_path)))

    if args.check or (not args.show_diff and not args.update_gemini and not args.update_agents and not args.update_all):
        print("\nChecking sync status...")
        print(f"  CLAUDE.md: {len(claude_content)} chars")

        all_synced = True
        for filename, content in files_to_check:
            print(f"  {filename}: {len(content)} chars")
            differences = check_sync(claude_content, content)
            if differences:
                print(f"\n[!] {filename} is OUT OF SYNC:")
                for diff in differences:
                    print(diff)
                all_synced = False

        if all_synced:
            print("\n[OK] All files are in sync")
            return 0
        else:
            print("\nRun with --update-all to sync all files from CLAUDE.md")
            return 1

    if args.show_diff:
        for filename, content in files_to_check:
            print(f"\n=== Comparing CLAUDE.md with {filename} ===")
            show_diff(claude_content, content)
        return 0

    if args.update_gemini or args.update_all:
        print("\nUpdating GEMINI.md from CLAUDE.md...")
        updates, backup = update_file_from_claude(project_root, "GEMINI.md")
        if updates:
            print(f"  Updated {len(updates)} sections, backup: {backup}")
        else:
            print("  No updates needed")

    if args.update_agents or args.update_all:
        print("\nUpdating AGENTS.md from CLAUDE.md...")
        updates, backup = update_file_from_claude(project_root, "AGENTS.md")
        if updates:
            print(f"  Updated {len(updates)} sections, backup: {backup}")
        else:
            print("  No updates needed")

    print("\n[OK] Sync complete")
    return 0


if __name__ == "__main__":
    exit(main())
