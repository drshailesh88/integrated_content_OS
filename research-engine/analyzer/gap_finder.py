#!/usr/bin/env python3
"""
Gap Finder - Identify content gaps where demand exceeds supply

Gaps are found by:
1. Topics with questions but few/no videos
2. Topics covered in English but not Hindi/Hinglish
3. Recent medical advances not yet covered
4. High engagement topics from inspiration channels not in competition
5. CORRECTION OPPORTUNITIES: Misinformation from belief-seeder channels that needs addressing

Usage:
    python gap_finder.py                        # Find all gaps
    python gap_finder.py --category biomarkers  # Filter by seed category
    python gap_finder.py --min-score 5          # Filter by minimum gap score
    python gap_finder.py --corrections          # Focus on correction opportunities
    python gap_finder.py --export               # Export gaps for content calendar
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import argparse

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"


def load_data():
    """Load all relevant data for gap analysis."""
    data = {
        "seed_ideas": [],
        "modifiers": [],
        "videos": [],
        "comments": [],
        "questions": [],
        "channels": {},
        "belief_seeders": [],
        "narrative_types": {}
    }

    # Load seed ideas
    seed_file = DATA_DIR / "seed-ideas.json"
    if seed_file.exists():
        with open(seed_file, "r") as f:
            data["seed_ideas"] = json.load(f)

    # Load modifiers
    mod_file = DATA_DIR / "modifiers.json"
    if mod_file.exists():
        with open(mod_file, "r") as f:
            data["modifiers"] = json.load(f)

    # Load target channels (includes belief seeders and narrative types)
    channels_file = DATA_DIR / "target_channels.json"
    if channels_file.exists():
        with open(channels_file, "r") as f:
            data["channels"] = json.load(f)
            data["narrative_types"] = data["channels"].get("narrative_types", {})
            # Extract belief seeder channels
            for category in ["adjacent_giants", "functional_medicine_broadcasters",
                           "indian_mega_channels", "diet_wars_channels", "longevity_biohacker_channels"]:
                if category in data["channels"]:
                    for ch in data["channels"][category]:
                        if ch.get("type") == "belief_seeder" or ch.get("strategic_action") == "debunk_directly":
                            data["belief_seeders"].append(ch)

    # Load scraped videos
    latest_videos = SCRAPED_DIR / "latest_scrape.json"
    if latest_videos.exists():
        with open(latest_videos, "r") as f:
            meta = json.load(f)
        videos_file = Path(meta["file"])
        if videos_file.exists():
            with open(videos_file, "r") as f:
                data["videos"] = json.load(f)

    # Load comments/questions
    latest_comments = SCRAPED_DIR / "latest_comments.json"
    if latest_comments.exists():
        with open(latest_comments, "r") as f:
            meta = json.load(f)
        comments_file = Path(meta["file"])
        if comments_file.exists():
            with open(comments_file, "r") as f:
                comment_data = json.load(f)
                data["comments"] = comment_data.get("all_comments", [])
                data["questions"] = comment_data.get("top_questions", [])

    return data


def calculate_gap_score(seed_idea, data, verbose=False):
    """
    Calculate gap score for a seed idea.

    Gap Score = (Demand Signals) / (Supply + 1)

    Demand signals:
    - Questions mentioning this topic
    - Comments with pain points about this topic
    - High-performing inspiration channel videos on this topic

    Supply:
    - Existing Hindi/competition videos on this topic
    """
    idea_lower = seed_idea.get("idea", "").lower()
    idea_words = idea_lower.split()

    # Initialize scores
    demand_score = 0
    supply_score = 0
    details = {
        "questions_found": 0,
        "hindi_videos": 0,
        "english_videos": 0,
        "inspiration_avg_views": 0,
        "sample_questions": [],
        "sample_videos": []
    }

    # DEMAND: Count questions mentioning this topic
    for question in data["questions"]:
        q_text = question.get("question", "").lower()
        if idea_lower in q_text or all(w in q_text for w in idea_words if len(w) > 3):
            demand_score += 1 + (question.get("likes", 0) / 10)  # Weight by likes
            details["questions_found"] += 1
            if len(details["sample_questions"]) < 3:
                details["sample_questions"].append(question.get("question", "")[:100])

    # DEMAND: Check inspiration channel performance on this topic
    inspiration_videos = []
    for video in data["videos"]:
        title_lower = video.get("title", "").lower()
        if video.get("channel_type") == "inspiration":
            if idea_lower in title_lower or all(w in title_lower for w in idea_words if len(w) > 3):
                inspiration_videos.append(video)
                demand_score += video.get("views", 0) / 100000  # Normalize

    if inspiration_videos:
        details["english_videos"] = len(inspiration_videos)
        details["inspiration_avg_views"] = sum(v.get("views", 0) for v in inspiration_videos) // len(inspiration_videos)

    # SUPPLY: Count Hindi/competition videos
    hindi_videos = []
    for video in data["videos"]:
        title_lower = video.get("title", "").lower()
        if video.get("channel_language") == "hindi" or video.get("channel_type") == "competition":
            if idea_lower in title_lower or all(w in title_lower for w in idea_words if len(w) > 3):
                supply_score += 1
                hindi_videos.append(video)

    details["hindi_videos"] = len(hindi_videos)
    if hindi_videos:
        details["sample_videos"] = [v.get("title", "")[:60] for v in hindi_videos[:3]]

    # Calculate final gap score
    # High demand + low supply = high gap score
    gap_score = demand_score / (supply_score + 1)

    # Bonus for topics covered in English but NOT in Hindi (language gap)
    if details["english_videos"] > 0 and details["hindi_videos"] == 0:
        gap_score *= 1.5  # 50% bonus for language gaps

    # Bonus for topics with many questions (proven demand)
    if details["questions_found"] >= 3:
        gap_score *= 1.3

    return {
        "seed_id": seed_idea.get("id"),
        "idea": seed_idea.get("idea"),
        "category": seed_idea.get("category"),
        "pillar": seed_idea.get("pillar"),
        "archetypes": seed_idea.get("archetypes", []),
        "gap_score": round(gap_score, 2),
        "demand_score": round(demand_score, 2),
        "supply_score": supply_score,
        "details": details,
        "opportunity_type": classify_opportunity(details)
    }


def classify_opportunity(details):
    """Classify the type of gap opportunity."""
    # Check for correction opportunity first (highest priority for health content)
    if details.get("correction_score", 0) >= 3:
        return "CORRECTION_OPPORTUNITY"  # Misinformation needs addressing
    elif details["english_videos"] > 0 and details["hindi_videos"] == 0:
        return "LANGUAGE_GAP"  # Covered in English, not Hindi
    elif details["questions_found"] >= 3 and details["hindi_videos"] == 0:
        return "DEMAND_GAP"  # High question demand, no supply
    elif details["inspiration_avg_views"] > 100000 and details["hindi_videos"] == 0:
        return "PROVEN_TOPIC"  # Proven in English, untapped in Hindi
    elif details["hindi_videos"] > 0 and details["questions_found"] >= 3:
        return "IMPROVEMENT_OPPORTUNITY"  # Exists but can be done better
    else:
        return "GENERAL"


# Narrative to seed category mapping for correction opportunities
NARRATIVE_SEED_MAPPING = {
    "ldl_skepticism": ["biomarkers", "medications", "risk-factors"],
    "statin_fear": ["medications", "risk-factors", "prevention"],
    "insulin_primacy": ["biomarkers", "comorbidities", "lifestyle", "nutrition"],
    "fasting_absolutism": ["lifestyle", "nutrition", "prevention"],
    "supplement_superiority": ["medications", "nutrition"],
    "seed_oil_villain": ["nutrition", "lifestyle"],
    "exercise_compensation": ["lifestyle", "prevention"],
    "fear_mongering": ["medications", "procedures", "diagnostics"]
}


def find_correction_opportunities(data):
    """
    Find correction opportunities - topics where belief-seeder channels
    have high-performing content that promotes problematic narratives.

    These are PRIORITY content opportunities because they address
    active misinformation reaching large audiences.
    """
    correction_opportunities = []

    belief_seeder_names = {ch["name"].lower() for ch in data["belief_seeders"]}

    # Map channels to their narratives
    channel_narratives = {}
    for ch in data["belief_seeders"]:
        channel_narratives[ch["name"].lower()] = ch.get("narrative_types", [])

    # Find high-performing videos from belief seeders
    for video in data["videos"]:
        channel_name = video.get("channel_name", "").lower()

        # Check if from a belief seeder
        is_belief_seeder = any(bs in channel_name or channel_name in bs
                              for bs in belief_seeder_names)

        if not is_belief_seeder:
            continue

        views = video.get("views", 0)
        if views < 50000:  # Only care about high-reach misinformation
            continue

        # Get narratives this channel promotes
        narratives = []
        for bs_name, narrs in channel_narratives.items():
            if bs_name in channel_name or channel_name in bs_name:
                narratives = narrs
                break

        # Find relevant seed ideas for correction
        relevant_seeds = []
        for narrative in narratives:
            categories = NARRATIVE_SEED_MAPPING.get(narrative, [])
            for seed in data["seed_ideas"]:
                if seed.get("category") in categories:
                    # Check if video title relates to seed idea
                    title_lower = video.get("title", "").lower()
                    idea_lower = seed.get("idea", "").lower()
                    if any(word in title_lower for word in idea_lower.split() if len(word) > 4):
                        relevant_seeds.append({
                            "seed_id": seed.get("id"),
                            "idea": seed.get("idea"),
                            "category": seed.get("category"),
                            "narrative_match": narrative
                        })

        if relevant_seeds:
            correction_opportunities.append({
                "source_video": {
                    "title": video.get("title"),
                    "channel": video.get("channel_name"),
                    "views": views,
                    "url": video.get("url", "")
                },
                "narratives_promoted": narratives,
                "correction_seeds": relevant_seeds[:3],  # Top 3 matches
                "priority_score": views / 10000 * len(narratives),
                "suggested_formats": get_correction_formats(narratives, views)
            })

    # Sort by priority (high views + multiple narratives = higher priority)
    correction_opportunities.sort(key=lambda x: x["priority_score"], reverse=True)

    return correction_opportunities


def get_correction_formats(narratives, views):
    """Suggest content formats based on narrative type and reach."""
    formats = []

    if views > 500000:
        formats.append({
            "format": "direct_response",
            "title_template": "Cardiologist Reacts: {original_title}",
            "notes": "High reach justifies direct response"
        })

    if "ldl_skepticism" in narratives or "statin_fear" in narratives:
        formats.append({
            "format": "evidence_synthesis",
            "title_template": "The Truth About {topic}: 50 Studies Reviewed",
            "notes": "Strong evidence base for correction"
        })

    if "fasting_absolutism" in narratives or "insulin_primacy" in narratives:
        formats.append({
            "format": "gentle_correction",
            "title_template": "{topic}: What YouTube Gets Right AND Wrong",
            "notes": "Partial truth requires nuanced approach"
        })

    formats.append({
        "format": "indian_context",
        "title_template": "{topic} for Indians: Why Generic Advice Doesn't Work",
        "notes": "Differentiate with Indian-specific framing"
    })

    return formats


def find_all_gaps(data, min_score=0, category_filter=None):
    """Find gaps for all seed ideas."""
    gaps = []

    for seed in data["seed_ideas"]:
        if category_filter and seed.get("category") != category_filter:
            continue

        gap = calculate_gap_score(seed, data)

        if gap["gap_score"] >= min_score:
            gaps.append(gap)

    # Sort by gap score
    gaps.sort(key=lambda x: x["gap_score"], reverse=True)

    return gaps


def find_modifier_gaps(data, top_seeds):
    """For top gap seeds, find which modifiers would work best."""
    modifier_opportunities = []

    for seed_gap in top_seeds[:20]:  # Top 20 seeds
        seed_idea = seed_gap["idea"].lower()

        # Find relevant modifiers based on archetypes
        relevant_modifiers = []
        for mod in data["modifiers"]:
            # Match demographics to seed archetypes
            if any(arch in mod.get("modifier", "").lower()
                   for arch in seed_gap.get("archetypes", [])):
                relevant_modifiers.append(mod)

        # Check which modifier combinations aren't covered
        for mod in relevant_modifiers[:5]:  # Top 5 relevant modifiers
            combo_text = f"{seed_idea} {mod.get('modifier', '')}".lower()

            # Check if this combo exists in videos
            exists = any(
                seed_idea in v.get("title", "").lower() and
                mod.get("modifier", "").lower()[:10] in v.get("title", "").lower()
                for v in data["videos"]
            )

            if not exists:
                modifier_opportunities.append({
                    "seed": seed_gap["idea"],
                    "modifier": mod.get("modifier"),
                    "modifier_category": mod.get("category"),
                    "combined_title_idea": f"{seed_gap['idea']} for {mod.get('modifier')}",
                    "base_gap_score": seed_gap["gap_score"]
                })

    return modifier_opportunities


def export_gaps(gaps, modifier_gaps, output_path, correction_opps=None):
    """Export gaps for content calendar integration."""
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_gaps": len(gaps),
        "by_opportunity_type": defaultdict(list),
        "top_50_gaps": gaps[:50],
        "modifier_combinations": modifier_gaps[:30],
        "by_category": defaultdict(list),
        "quick_wins": [],  # Easy to create, high potential
        "strategic_bets": [],  # Require more effort, very high potential
        "correction_opportunities": correction_opps[:20] if correction_opps else []
    }

    # Organize by type
    for gap in gaps:
        export_data["by_opportunity_type"][gap["opportunity_type"]].append(gap)
        export_data["by_category"][gap["category"]].append(gap)

    # Identify quick wins (language gaps with proven English performance)
    export_data["quick_wins"] = [
        g for g in gaps
        if g["opportunity_type"] == "LANGUAGE_GAP"
        and g["details"]["inspiration_avg_views"] > 50000
    ][:10]

    # Identify strategic bets (high question demand)
    export_data["strategic_bets"] = [
        g for g in gaps
        if g["details"]["questions_found"] >= 5
    ][:10]

    # Convert defaultdicts to regular dicts for JSON
    export_data["by_opportunity_type"] = dict(export_data["by_opportunity_type"])
    export_data["by_category"] = dict(export_data["by_category"])

    with open(output_path, "w") as f:
        json.dump(export_data, f, indent=2)

    return export_data


def main():
    parser = argparse.ArgumentParser(description="Find content gaps for your seed ideas")
    parser.add_argument("--category", type=str, help="Filter by seed category")
    parser.add_argument("--min-score", type=float, default=0, help="Minimum gap score")
    parser.add_argument("--export", action="store_true", help="Export gaps to file")
    parser.add_argument("--top", type=int, default=20, help="Show top N gaps")
    parser.add_argument("--corrections", action="store_true", help="Focus on correction opportunities")
    args = parser.parse_args()

    print("Loading data...")
    data = load_data()

    print(f"Loaded: {len(data['seed_ideas'])} seeds, {len(data['videos'])} videos, {len(data['questions'])} questions")
    print(f"Belief seeder channels tracked: {len(data['belief_seeders'])}")

    if not data["videos"]:
        print("\nWARNING: No scraped videos found.")
        print("Run channel_scraper.py first for better gap analysis.")
        print("Proceeding with seed ideas only...\n")

    print("\nFinding content gaps...")
    gaps = find_all_gaps(data, min_score=args.min_score, category_filter=args.category)

    print(f"\nFound {len(gaps)} gaps (min_score={args.min_score})")

    # Find correction opportunities
    correction_opps = find_correction_opportunities(data)
    print(f"Found {len(correction_opps)} correction opportunities")

    # Find modifier combinations
    modifier_gaps = find_modifier_gaps(data, gaps)

    # If --corrections flag, show correction opportunities first
    if args.corrections:
        print(f"\n{'='*70}")
        print("CORRECTION OPPORTUNITIES (Misinformation to Address)")
        print(f"{'='*70}")

        for i, opp in enumerate(correction_opps[:args.top], 1):
            print(f"\n{i}. SOURCE: {opp['source_video']['channel']}")
            print(f"   Video: \"{opp['source_video']['title'][:60]}...\"")
            print(f"   Views: {opp['source_video']['views']:,}")
            print(f"   Narratives: {', '.join(opp['narratives_promoted'])}")
            print(f"   Priority Score: {opp['priority_score']:.1f}")
            print(f"   Correction Seeds:")
            for seed in opp['correction_seeds'][:2]:
                print(f"     - {seed['idea']} ({seed['narrative_match']})")
            print(f"   Suggested Formats:")
            for fmt in opp['suggested_formats'][:2]:
                print(f"     - {fmt['format']}: {fmt['title_template']}")

        print(f"\n{'='*70}")
        print("Use these with the debunk-script-writer skill")
        print(f"{'='*70}")
        return

    # Print results
    print(f"\n{'='*70}")
    print(f"TOP {args.top} CONTENT GAPS")
    print(f"{'='*70}")

    for i, gap in enumerate(gaps[:args.top], 1):
        print(f"\n{i}. {gap['idea']}")
        print(f"   Category: {gap['category']} | Pillar: {gap['pillar']}")
        print(f"   Gap Score: {gap['gap_score']} | Type: {gap['opportunity_type']}")
        print(f"   Demand: {gap['demand_score']} | Supply: {gap['supply_score']}")
        if gap['details']['questions_found']:
            print(f"   Questions found: {gap['details']['questions_found']}")
        if gap['details']['english_videos']:
            print(f"   English videos: {gap['details']['english_videos']} (avg {gap['details']['inspiration_avg_views']:,} views)")
        if gap['details']['sample_questions']:
            print(f"   Sample question: \"{gap['details']['sample_questions'][0][:60]}...\"")

    # Print opportunity breakdown
    print(f"\n{'='*70}")
    print("GAP TYPES BREAKDOWN")
    print(f"{'='*70}")

    type_counts = defaultdict(int)
    for gap in gaps:
        type_counts[gap["opportunity_type"]] += 1

    for gap_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {gap_type}: {count}")

    # Print modifier combinations
    if modifier_gaps:
        print(f"\n{'='*70}")
        print("TOP MODIFIER COMBINATIONS")
        print(f"{'='*70}")
        for combo in modifier_gaps[:10]:
            print(f"  • {combo['combined_title_idea']}")

    # Export if requested
    if args.export:
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"content_gaps_{timestamp}.json"
        export_data = export_gaps(gaps, modifier_gaps, output_file, correction_opps)

        print(f"\n{'='*70}")
        print(f"EXPORTED TO: {output_file}")
        print(f"{'='*70}")
        print(f"Quick wins: {len(export_data['quick_wins'])}")
        print(f"Strategic bets: {len(export_data['strategic_bets'])}")
        print(f"Correction opportunities: {len(export_data['correction_opportunities'])}")


if __name__ == "__main__":
    main()
