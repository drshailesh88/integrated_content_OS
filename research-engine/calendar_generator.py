#!/usr/bin/env python3
"""
Content Calendar Generator
Converts ranked ideas into a 100-day content calendar

Usage:
    python calendar_generator.py --input ./output/ranked_ideas.json --days 100
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


def load_ranked_ideas(file_path: str) -> List[Dict]:
    """Load ranked ideas from research output"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_calendar(ranked_ideas: List[Dict],
                      num_days: int = 100,
                      start_date: datetime = None,
                      videos_per_week: int = 3) -> Dict:
    """
    Generate content calendar from ranked ideas

    Args:
        ranked_ideas: List of ideas sorted by score
        num_days: Number of days to plan
        start_date: Starting date (default: today)
        videos_per_week: Target videos per week
    """

    start_date = start_date or datetime.now()

    # Calculate posting days (Mon, Wed, Fri by default)
    posting_days = [0, 2, 4]  # Monday, Wednesday, Friday

    calendar = {
        'generated_at': datetime.now().isoformat(),
        'start_date': start_date.isoformat(),
        'end_date': (start_date + timedelta(days=num_days)).isoformat(),
        'total_videos': 0,
        'schedule': [],
        'by_week': [],
        'by_pillar': {},
        'by_archetype': {}
    }

    current_date = start_date
    idea_index = 0
    week_number = 1
    current_week = []

    while (current_date - start_date).days < num_days and idea_index < len(ranked_ideas):
        # Check if this is a posting day
        if current_date.weekday() in posting_days:
            idea = ranked_ideas[idea_index]

            entry = {
                'date': current_date.strftime('%Y-%m-%d'),
                'day_of_week': current_date.strftime('%A'),
                'week': week_number,
                'idea_id': idea.get('idea_id', idea.get('id', '')),
                'title': idea.get('combined_title', idea.get('seed_idea', '')),
                'seed_idea': idea.get('seed_idea', ''),
                'modifier': idea.get('modifier', ''),
                'score': idea.get('scores', {}).get('total', idea.get('priority_score', 0)),
                'pillar': idea.get('pillar', 'general'),
                'archetypes': idea.get('archetypes', []),
                'status': 'planned',
                'notes': ''
            }

            calendar['schedule'].append(entry)
            current_week.append(entry)
            idea_index += 1
            calendar['total_videos'] += 1

            # Track by pillar
            pillar = entry['pillar']
            if pillar not in calendar['by_pillar']:
                calendar['by_pillar'][pillar] = []
            calendar['by_pillar'][pillar].append(entry['idea_id'])

            # Track by archetype
            for arch in entry['archetypes']:
                if arch not in calendar['by_archetype']:
                    calendar['by_archetype'][arch] = []
                calendar['by_archetype'][arch].append(entry['idea_id'])

        # Move to next day
        current_date += timedelta(days=1)

        # Check for week boundary
        if current_date.weekday() == 0 and current_week:  # Monday
            calendar['by_week'].append({
                'week': week_number,
                'start_date': current_week[0]['date'],
                'videos': current_week
            })
            week_number += 1
            current_week = []

    # Add final partial week
    if current_week:
        calendar['by_week'].append({
            'week': week_number,
            'start_date': current_week[0]['date'],
            'videos': current_week
        })

    return calendar


def export_markdown(calendar: Dict, output_path: str):
    """Export calendar as markdown for Obsidian"""

    lines = [
        "# Content Calendar",
        "",
        f"**Generated**: {calendar['generated_at'][:10]}",
        f"**Period**: {calendar['start_date'][:10]} to {calendar['end_date'][:10]}",
        f"**Total Videos**: {calendar['total_videos']}",
        "",
        "---",
        "",
        "## Weekly Schedule",
        ""
    ]

    for week in calendar['by_week']:
        lines.append(f"### Week {week['week']} (Starting {week['start_date']})")
        lines.append("")
        lines.append("| Day | Title | Score | Status |")
        lines.append("|-----|-------|-------|--------|")

        for video in week['videos']:
            title = video['title'][:50] + '...' if len(video['title']) > 50 else video['title']
            lines.append(f"| {video['day_of_week'][:3]} {video['date'][5:]} | {title} | {video['score']:.1f} | {video['status']} |")

        lines.append("")

    # Pillar breakdown
    lines.extend([
        "---",
        "",
        "## By Content Pillar",
        ""
    ])

    for pillar, ids in calendar['by_pillar'].items():
        lines.append(f"- **{pillar}**: {len(ids)} videos")

    # Archetype breakdown
    lines.extend([
        "",
        "## By Audience",
        ""
    ])

    for arch, ids in calendar['by_archetype'].items():
        lines.append(f"- **{arch}**: {len(ids)} videos")

    lines.extend([
        "",
        "---",
        "",
        "*Generated by Dr. Shailesh Content System*"
    ])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def export_idea_briefs(calendar: Dict, output_dir: str, ranked_ideas: List[Dict]):
    """Generate individual idea brief files"""

    briefs_dir = os.path.join(output_dir, 'idea-briefs')
    os.makedirs(briefs_dir, exist_ok=True)

    # Create lookup for full idea data
    idea_lookup = {i.get('idea_id', i.get('id', '')): i for i in ranked_ideas}

    for entry in calendar['schedule']:
        idea_id = entry['idea_id']
        full_idea = idea_lookup.get(idea_id, {})

        lines = [
            f"# {entry['title']}",
            "",
            f"**Scheduled**: {entry['date']} ({entry['day_of_week']})",
            f"**Status**: {entry['status']}",
            "",
            "---",
            "",
            "## Idea Details",
            "",
            f"- **Seed Idea**: {entry['seed_idea']}",
            f"- **Modifier**: {entry['modifier']}",
            f"- **Score**: {entry['score']:.1f}/10",
            f"- **Pillar**: {entry['pillar']}",
            f"- **Target Audience**: {', '.join(entry['archetypes'])}",
            "",
            "## Research Summary",
            ""
        ]

        # Add research data if available
        if 'total_views' in full_idea:
            lines.extend([
                f"- **Total Views (Top 10)**: {full_idea.get('total_views', 'N/A'):,}",
                f"- **Avg Views**: {full_idea.get('avg_views', 0):,.0f}",
                ""
            ])

        # Gap analysis
        gaps = full_idea.get('gap_analysis', {})
        if gaps:
            lines.extend([
                "### Content Gaps Identified",
                ""
            ])
            gap_labels = {
                'hinglish_gap': 'Hinglish content gap',
                'recency_gap': 'Recent content gap',
                'depth_gap': 'In-depth content gap',
                'authority_gap': 'Medical authority gap',
                'india_context_gap': 'India context gap'
            }
            for gap_key, gap_label in gap_labels.items():
                if gaps.get(gap_key):
                    lines.append(f"- ✅ {gap_label}")
            lines.append("")

        # Comment themes
        themes = full_idea.get('comment_themes', [])
        if themes:
            lines.extend([
                "### Audience Questions (from comments)",
                ""
            ])
            for theme in themes[:5]:
                lines.append(f"- {theme}")
            lines.append("")

        # Template sections
        lines.extend([
            "---",
            "",
            "## Script Outline",
            "",
            "### Hook",
            "- [ ] TODO: Write hook",
            "",
            "### Key Points",
            "1. [ ] Point 1",
            "2. [ ] Point 2",
            "3. [ ] Point 3",
            "",
            "### CTA",
            "- [ ] TODO: Define call to action",
            "",
            "---",
            "",
            "## Notes",
            "",
            "_Add your notes here..._",
            ""
        ])

        # Save brief
        brief_file = os.path.join(briefs_dir, f"{idea_id}.md")
        with open(brief_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    print(f"   Generated {len(calendar['schedule'])} idea briefs in {briefs_dir}")


def main():
    parser = argparse.ArgumentParser(description='Content Calendar Generator')
    parser.add_argument('--input', required=True, help='Path to ranked ideas JSON')
    parser.add_argument('--output', default='../content-calendar/', help='Output directory')
    parser.add_argument('--days', type=int, default=100, help='Number of days to plan')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--videos-per-week', type=int, default=3, help='Videos per week')

    args = parser.parse_args()

    # Load ranked ideas
    ranked_ideas = load_ranked_ideas(args.input)
    print(f"Loaded {len(ranked_ideas)} ranked ideas")

    # Parse start date
    start_date = None
    if args.start_date:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')

    # Generate calendar
    calendar = generate_calendar(
        ranked_ideas,
        num_days=args.days,
        start_date=start_date,
        videos_per_week=args.videos_per_week
    )

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Save JSON
    json_output = os.path.join(args.output, 'calendar.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(calendar, f, indent=2, ensure_ascii=False)

    # Export markdown
    md_output = os.path.join(args.output, '100-day-calendar.md')
    export_markdown(calendar, md_output)

    # Generate idea briefs
    export_idea_briefs(calendar, args.output, ranked_ideas)

    print(f"\n✅ Calendar generated!")
    print(f"   JSON: {json_output}")
    print(f"   Markdown: {md_output}")
    print(f"   Total videos planned: {calendar['total_videos']}")
    print(f"   Weeks covered: {len(calendar['by_week'])}")


if __name__ == '__main__':
    main()
