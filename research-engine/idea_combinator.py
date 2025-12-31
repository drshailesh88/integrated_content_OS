#!/usr/bin/env python3
"""
Idea Combinator for Dr. Shailesh Content System
Combines seed ideas with modifiers to generate prioritized content ideas

Usage:
    python idea_combinator.py --seeds ./data/seed-ideas.json --modifiers ./data/modifiers.json
    python idea_combinator.py --generate-sample  # Create sample data files
"""

import os
import json
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from itertools import product


# Content pillars for filtering
CONTENT_PILLARS = [
    "evidence-based-education",
    "patient-empowerment",
    "lifestyle-medicine",
    "medical-literacy",
    "stories-case-studies"
]

# Audience archetypes for targeting
ARCHETYPES = [
    "heart-patients",
    "lifestyle-disease-group",
    "proactive-biohackers",
    "health-enthusiasts",
    "caregivers",
    "young-anxious"
]

# Awareness levels
AWARENESS_LEVELS = [
    "unaware",
    "problem-aware",
    "solution-aware",
    "product-aware",
    "most-aware"
]


def load_json(file_path: str) -> List[Dict]:
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: List[Dict], file_path: str):
    """Save to JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_combinations(seeds: List[Dict], modifiers: List[Dict],
                          limit: int = None) -> List[Dict]:
    """
    Generate idea combinations from seeds and modifiers
    Uses smart filtering to avoid explosion of combinations
    """

    combinations = []
    combo_id = 0

    for seed in seeds:
        seed_text = seed.get('idea', seed.get('title', ''))
        seed_category = seed.get('category', 'general')
        seed_pillar = seed.get('pillar', 'evidence-based-education')
        seed_archetypes = seed.get('archetypes', ['health-enthusiasts'])

        # Only combine with relevant modifiers
        for modifier in modifiers:
            mod_text = modifier.get('modifier', modifier.get('text', ''))
            mod_type = modifier.get('type', 'format')
            mod_compatible = modifier.get('compatible_pillars', CONTENT_PILLARS)

            # Skip incompatible combinations
            if seed_pillar not in mod_compatible:
                continue

            combo_id += 1

            # Generate combined title
            combined_title = f"{seed_text} ({mod_text})"

            combinations.append({
                'id': f'combo_{combo_id:05d}',
                'seed_id': seed.get('id', ''),
                'modifier_id': modifier.get('id', ''),
                'seed_idea': seed_text,
                'modifier': mod_text,
                'combined_title': combined_title,
                'category': seed_category,
                'pillar': seed_pillar,
                'archetypes': seed_archetypes,
                'modifier_type': mod_type,
                'priority_score': 0,  # To be filled by scoring
                'created_at': datetime.now().isoformat()
            })

            if limit and len(combinations) >= limit:
                return combinations

    return combinations


def prioritize_combinations(combinations: List[Dict],
                           priority_archetypes: List[str] = None,
                           priority_pillars: List[str] = None) -> List[Dict]:
    """
    Score and prioritize combinations based on criteria
    """

    priority_archetypes = priority_archetypes or ['heart-patients', 'lifestyle-disease-group']
    priority_pillars = priority_pillars or ['evidence-based-education', 'patient-empowerment']

    for combo in combinations:
        score = 0

        # Archetype alignment (max 40 points)
        combo_archetypes = combo.get('archetypes', [])
        archetype_match = len(set(combo_archetypes) & set(priority_archetypes))
        score += archetype_match * 20

        # Pillar alignment (max 30 points)
        if combo.get('pillar') in priority_pillars:
            score += 30

        # Modifier type bonus (max 20 points)
        mod_type = combo.get('modifier_type', '')
        type_scores = {
            'myth-busting': 20,
            'data-driven': 18,
            'story': 15,
            'how-to': 12,
            'list': 10,
            'comparison': 8,
            'format': 5
        }
        score += type_scores.get(mod_type, 5)

        # Random factor for variety (max 10 points)
        score += random.randint(0, 10)

        combo['priority_score'] = score

    # Sort by priority score
    combinations.sort(key=lambda x: x['priority_score'], reverse=True)

    return combinations


def select_for_research(combinations: List[Dict],
                        count: int = 500,
                        ensure_diversity: bool = True) -> List[Dict]:
    """
    Select top combinations for research, ensuring diversity
    """

    if not ensure_diversity:
        return combinations[:count]

    selected = []
    used_seeds = set()
    used_modifiers = set()

    # First pass: pick diverse combinations
    for combo in combinations:
        seed_id = combo.get('seed_id', '')
        mod_id = combo.get('modifier_id', '')

        # Allow each seed max 3 times, each modifier max 10 times
        seed_count = sum(1 for s in selected if s.get('seed_id') == seed_id)
        mod_count = sum(1 for s in selected if s.get('modifier_id') == mod_id)

        if seed_count < 3 and mod_count < 10:
            selected.append(combo)

        if len(selected) >= count:
            break

    # Second pass: fill remaining with top-scored
    if len(selected) < count:
        remaining = [c for c in combinations if c not in selected]
        selected.extend(remaining[:count - len(selected)])

    return selected


def generate_sample_data(output_dir: str):
    """Generate sample seed ideas and modifiers JSON files"""

    # Sample seed ideas (subset - full list would have 934)
    sample_seeds = [
        {"id": "seed_001", "idea": "Statin side effects", "category": "medications", "pillar": "medical-literacy", "archetypes": ["heart-patients", "lifestyle-disease-group"]},
        {"id": "seed_002", "idea": "Walking vs gym for heart health", "category": "exercise", "pillar": "lifestyle-medicine", "archetypes": ["health-enthusiasts", "young-anxious"]},
        {"id": "seed_003", "idea": "Desi ghee and heart disease", "category": "diet", "pillar": "evidence-based-education", "archetypes": ["health-enthusiasts", "caregivers"]},
        {"id": "seed_004", "idea": "BP ki goli lifetime?", "category": "medications", "pillar": "patient-empowerment", "archetypes": ["lifestyle-disease-group", "heart-patients"]},
        {"id": "seed_005", "idea": "Heart attack warning signs", "category": "emergency", "pillar": "medical-literacy", "archetypes": ["caregivers", "heart-patients", "young-anxious"]},
        {"id": "seed_006", "idea": "Cholesterol normal but still heart attack", "category": "risk-factors", "pillar": "evidence-based-education", "archetypes": ["proactive-biohackers", "health-enthusiasts"]},
        {"id": "seed_007", "idea": "Stress and heart disease connection", "category": "mental-health", "pillar": "lifestyle-medicine", "archetypes": ["young-anxious", "lifestyle-disease-group"]},
        {"id": "seed_008", "idea": "Stent ke baad kya khaana chahiye", "category": "recovery", "pillar": "patient-empowerment", "archetypes": ["heart-patients", "caregivers"]},
        {"id": "seed_009", "idea": "Young age mein heart attack kyun", "category": "prevention", "pillar": "evidence-based-education", "archetypes": ["young-anxious", "health-enthusiasts"]},
        {"id": "seed_010", "idea": "ApoB vs LDL - which matters more", "category": "biomarkers", "pillar": "evidence-based-education", "archetypes": ["proactive-biohackers"]}
    ]

    # Sample modifiers
    sample_modifiers = [
        {"id": "mod_001", "modifier": "myth-busting", "type": "myth-busting", "compatible_pillars": ["evidence-based-education", "medical-literacy"]},
        {"id": "mod_002", "modifier": "5 facts you didn't know", "type": "list", "compatible_pillars": CONTENT_PILLARS},
        {"id": "mod_003", "modifier": "research study breakdown", "type": "data-driven", "compatible_pillars": ["evidence-based-education"]},
        {"id": "mod_004", "modifier": "patient case study", "type": "story", "compatible_pillars": ["stories-case-studies", "patient-empowerment"]},
        {"id": "mod_005", "modifier": "step-by-step guide", "type": "how-to", "compatible_pillars": ["lifestyle-medicine", "patient-empowerment"]},
        {"id": "mod_006", "modifier": "vs comparison", "type": "comparison", "compatible_pillars": CONTENT_PILLARS},
        {"id": "mod_007", "modifier": "what doctors don't tell you", "type": "myth-busting", "compatible_pillars": ["evidence-based-education", "patient-empowerment"]},
        {"id": "mod_008", "modifier": "in 10 minutes", "type": "format", "compatible_pillars": CONTENT_PILLARS},
        {"id": "mod_009", "modifier": "for beginners", "type": "format", "compatible_pillars": ["lifestyle-medicine", "medical-literacy"]},
        {"id": "mod_010", "modifier": "latest 2024 research", "type": "data-driven", "compatible_pillars": ["evidence-based-education"]}
    ]

    save_json(sample_seeds, os.path.join(output_dir, 'seed-ideas.json'))
    save_json(sample_modifiers, os.path.join(output_dir, 'modifiers.json'))

    print(f"✅ Sample data generated in {output_dir}")
    print(f"   - seed-ideas.json ({len(sample_seeds)} ideas)")
    print(f"   - modifiers.json ({len(sample_modifiers)} modifiers)")
    print(f"\n   Replace these with your full lists (934 seeds, 200+ modifiers)")


def main():
    parser = argparse.ArgumentParser(description='Idea Combinator')
    parser.add_argument('--seeds', help='Path to seed ideas JSON')
    parser.add_argument('--modifiers', help='Path to modifiers JSON')
    parser.add_argument('--output', default='./output/', help='Output directory')
    parser.add_argument('--limit', type=int, help='Limit total combinations')
    parser.add_argument('--select', type=int, default=500, help='Number to select for research')
    parser.add_argument('--generate-sample', action='store_true', help='Generate sample data files')

    args = parser.parse_args()

    if args.generate_sample:
        generate_sample_data(args.output or './data/')
        return

    if not args.seeds or not args.modifiers:
        print("Error: --seeds and --modifiers required (or use --generate-sample)")
        parser.print_help()
        return

    # Load data
    seeds = load_json(args.seeds)
    modifiers = load_json(args.modifiers)

    print(f"Loaded {len(seeds)} seed ideas and {len(modifiers)} modifiers")

    # Generate combinations
    combinations = generate_combinations(seeds, modifiers, limit=args.limit)
    print(f"Generated {len(combinations)} combinations")

    # Prioritize
    prioritized = prioritize_combinations(combinations)

    # Select for research
    selected = select_for_research(prioritized, count=args.select)

    # Save outputs
    os.makedirs(args.output, exist_ok=True)

    all_combos_file = os.path.join(args.output, 'all_combinations.json')
    selected_file = os.path.join(args.output, 'selected_for_research.json')

    save_json(prioritized, all_combos_file)
    save_json(selected, selected_file)

    print(f"\n✅ Combination complete!")
    print(f"   All combinations: {all_combos_file} ({len(prioritized)} ideas)")
    print(f"   Selected for research: {selected_file} ({len(selected)} ideas)")

    # Show top 10
    print(f"\n📊 Top 10 ideas by priority:")
    for i, combo in enumerate(selected[:10], 1):
        print(f"   {i}. [{combo['priority_score']}] {combo['combined_title'][:60]}...")


if __name__ == '__main__':
    main()
