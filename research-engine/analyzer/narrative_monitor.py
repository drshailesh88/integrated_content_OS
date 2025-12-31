#!/usr/bin/env python3
"""
Narrative Monitor - Track beliefs patients absorb before clinic visits

The "Shadow Medical School" hypothesis: Patients learn cardiology from YouTube
before seeing a cardiologist. This module tracks what they learn and identifies
correction opportunities.

Functions:
1. Track which narratives each channel promotes
2. Identify specific claims that need correction
3. Match narratives to seed ideas for content opportunities
4. Generate debunk content suggestions
5. Create "response to" video ideas

Usage:
    python narrative_monitor.py                    # Full narrative analysis
    python narrative_monitor.py --narrative ldl_skepticism  # Filter by narrative
    python narrative_monitor.py --debunk           # Generate debunk ideas
    python narrative_monitor.py --export           # Export for content calendar
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

# Narrative detection keywords
NARRATIVE_KEYWORDS = {
    "ldl_skepticism": [
        "ldl doesn't cause", "ldl is not the problem", "ldl myth",
        "cholesterol is not bad", "ldl doesn't matter", "ldl hypothesis is wrong",
        "cholesterol myth", "ldl is not atherogenic", "forget about ldl",
        "ldl is essential", "high ldl is fine", "ldl skeptic"
    ],
    "statin_fear": [
        "statin side effects", "statins are dangerous", "never take statins",
        "statins cause", "avoid statins", "statin damage", "muscle pain from",
        "statins don't work", "quit statins", "stop statin", "statin harm",
        "natural alternative to statin"
    ],
    "insulin_primacy": [
        "insulin is the real problem", "insulin resistance causes heart",
        "it's not cholesterol it's insulin", "fix insulin first",
        "insulin drives atherosclerosis", "hyperinsulinemia is the cause",
        "insulin not ldl", "metabolic syndrome is the key"
    ],
    "fasting_absolutism": [
        "fasting can reverse", "fasting heals everything", "autophagy will fix",
        "just fast", "intermittent fasting cures", "72 hour fast",
        "fasting reverses heart disease", "fasting clears arteries"
    ],
    "exercise_compensation": [
        "exercise will clear plaque", "exercise can compensate",
        "athletes don't need", "if you exercise you don't need",
        "exercise reverses atherosclerosis", "cardio clears arteries"
    ],
    "supplement_superiority": [
        "this supplement is better than", "natural alternative to medication",
        "supplement instead of drug", "vitamin better than statin",
        "omega 3 replaces", "coq10 instead of", "berberine better than metformin"
    ],
    "seed_oil_villain": [
        "seed oils cause", "avoid vegetable oils", "omega 6 causes heart",
        "industrial oils are poison", "seed oils are inflammatory",
        "canola oil is toxic", "soybean oil causes"
    ],
    "fear_mongering": [
        "doctors are hiding", "big pharma doesn't want", "they won't tell you",
        "secret cure", "doctors lie about", "medical establishment hides",
        "suppressed study shows", "mainstream medicine is wrong"
    ]
}

# Claim patterns that indicate specific debunkable assertions
CLAIM_PATTERNS = {
    "ldl_causality_denial": [
        r"ldl.*doesn't.*cause.*heart|ldl.*not.*cause.*atherosclerosis",
        r"cholesterol.*myth|lipid.*hypothesis.*debunked"
    ],
    "statin_blanket_rejection": [
        r"never.*take.*statin|always.*avoid.*statin",
        r"statin.*kill|statin.*poison"
    ],
    "fasting_cure_all": [
        r"fasting.*cure.*everything|fasting.*reverse.*all",
        r"autophagy.*fix.*anything"
    ],
    "insulin_sole_cause": [
        r"only.*insulin.*matters|insulin.*only.*cause",
        r"forget.*cholesterol.*focus.*insulin"
    ]
}


def load_channels():
    """Load target channels with narrative classifications."""
    channels_file = DATA_DIR / "target_channels.json"
    if channels_file.exists():
        with open(channels_file, "r") as f:
            return json.load(f)
    return {}


def load_scraped_data():
    """Load scraped videos and comments."""
    data = {"videos": [], "comments": []}

    # Load videos
    latest_videos = SCRAPED_DIR / "latest_scrape.json"
    if latest_videos.exists():
        with open(latest_videos, "r") as f:
            meta = json.load(f)
        videos_file = Path(meta.get("file", ""))
        if videos_file.exists():
            with open(videos_file, "r") as f:
                data["videos"] = json.load(f)

    # Load comments
    latest_comments = SCRAPED_DIR / "latest_comments.json"
    if latest_comments.exists():
        with open(latest_comments, "r") as f:
            meta = json.load(f)
        comments_file = Path(meta.get("file", ""))
        if comments_file.exists():
            with open(comments_file, "r") as f:
                comment_data = json.load(f)
                data["comments"] = comment_data.get("all_comments", [])

    return data


def load_seed_ideas():
    """Load seed ideas for matching."""
    seed_file = DATA_DIR / "seed-ideas.json"
    if seed_file.exists():
        with open(seed_file, "r") as f:
            return json.load(f)
    return []


def detect_narratives_in_text(text):
    """Detect which narratives are present in text."""
    text_lower = text.lower()
    detected = []

    for narrative, keywords in NARRATIVE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected.append({
                    "narrative": narrative,
                    "keyword_matched": keyword,
                    "context": text[:200]
                })
                break  # One match per narrative is enough

    return detected


def detect_claims_in_text(text):
    """Detect specific debunkable claims using regex patterns."""
    text_lower = text.lower()
    detected = []

    for claim_type, patterns in CLAIM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                detected.append({
                    "claim_type": claim_type,
                    "pattern_matched": pattern,
                    "text_sample": text[:300]
                })
                break

    return detected


def analyze_channel_narratives(channels_data, scraped_data):
    """Analyze which channels are promoting which narratives based on scraped content."""
    channel_analysis = {}

    # First, get expected narratives from channel config
    all_channels = []
    for category_key in channels_data:
        if isinstance(channels_data[category_key], list):
            all_channels.extend(channels_data[category_key])

    for channel in all_channels:
        if not isinstance(channel, dict):
            continue

        channel_name = channel.get("name", "")
        channel_analysis[channel_name] = {
            "expected_narratives": channel.get("narrative_types", []),
            "strategic_action": channel.get("strategic_action", "monitor"),
            "influence_rating": channel.get("influence_rating", 0),
            "subscriber_estimate": channel.get("subscriber_estimate", "unknown"),
            "detected_narratives": defaultdict(int),
            "detected_claims": [],
            "video_samples": [],
            "total_videos_analyzed": 0
        }

    # Analyze scraped videos
    for video in scraped_data["videos"]:
        channel_name = video.get("channel_name", "")
        title = video.get("title", "")
        description = video.get("description", "")
        combined_text = f"{title} {description}"

        # Find matching channel
        matched_channel = None
        for ch_name in channel_analysis:
            if ch_name.lower() in channel_name.lower() or channel_name.lower() in ch_name.lower():
                matched_channel = ch_name
                break

        if matched_channel:
            channel_analysis[matched_channel]["total_videos_analyzed"] += 1

            # Detect narratives
            narratives = detect_narratives_in_text(combined_text)
            for n in narratives:
                channel_analysis[matched_channel]["detected_narratives"][n["narrative"]] += 1

            # Detect specific claims
            claims = detect_claims_in_text(combined_text)
            for c in claims:
                c["video_title"] = title
                c["video_url"] = video.get("url", "")
                channel_analysis[matched_channel]["detected_claims"].append(c)

            # Store sample videos for high-narrative content
            if narratives:
                channel_analysis[matched_channel]["video_samples"].append({
                    "title": title,
                    "url": video.get("url", ""),
                    "views": video.get("views", 0),
                    "narratives_detected": [n["narrative"] for n in narratives]
                })

    # Convert defaultdicts
    for ch in channel_analysis:
        channel_analysis[ch]["detected_narratives"] = dict(channel_analysis[ch]["detected_narratives"])

    return channel_analysis


def get_narrative_prevalence(channel_analysis):
    """Calculate overall narrative prevalence across all channels."""
    prevalence = defaultdict(lambda: {
        "total_mentions": 0,
        "channels_promoting": [],
        "high_influence_channels": [],
        "total_reach": 0  # Sum of influence ratings
    })

    for channel_name, data in channel_analysis.items():
        for narrative, count in data["detected_narratives"].items():
            prevalence[narrative]["total_mentions"] += count
            prevalence[narrative]["channels_promoting"].append(channel_name)
            prevalence[narrative]["total_reach"] += data["influence_rating"]

            if data["influence_rating"] >= 4:
                prevalence[narrative]["high_influence_channels"].append(channel_name)

        # Also count expected narratives (from channel config)
        for narrative in data["expected_narratives"]:
            if channel_name not in prevalence[narrative]["channels_promoting"]:
                prevalence[narrative]["channels_promoting"].append(channel_name)
                prevalence[narrative]["total_reach"] += data["influence_rating"]
                if data["influence_rating"] >= 4:
                    prevalence[narrative]["high_influence_channels"].append(channel_name)

    return dict(prevalence)


def generate_debunk_ideas(narrative_prevalence, seed_ideas, channels_data):
    """Generate debunk content ideas by matching narratives to seed ideas."""
    debunk_ideas = []

    # Map narratives to relevant seed categories
    NARRATIVE_TO_SEEDS = {
        "ldl_skepticism": ["biomarkers", "medications", "risk-factors"],
        "statin_fear": ["medications", "risk-factors"],
        "insulin_primacy": ["biomarkers", "comorbidities", "lifestyle"],
        "fasting_absolutism": ["lifestyle", "nutrition", "prevention"],
        "supplement_superiority": ["medications", "nutrition"],
        "seed_oil_villain": ["nutrition", "lifestyle"],
        "exercise_compensation": ["lifestyle", "prevention"]
    }

    # Debunk templates
    DEBUNK_TEMPLATES = {
        "direct_correction": "What {channel} Gets Wrong About {topic}",
        "evidence_synthesis": "The Truth About {topic}: What 50 Studies Actually Show",
        "patient_perspective": "Should You Stop Your {topic}? A Cardiologist Explains",
        "common_myths": "5 Myths About {topic} That Could Cost You Your Life",
        "gentle_correction": "{topic}: What YouTube Gets Right AND Wrong",
        "indian_context": "{topic} for Indians: Why Generic Advice Doesn't Work"
    }

    # Sort narratives by prevalence/influence
    sorted_narratives = sorted(
        narrative_prevalence.items(),
        key=lambda x: x[1]["total_reach"],
        reverse=True
    )

    for narrative, data in sorted_narratives:
        relevant_categories = NARRATIVE_TO_SEEDS.get(narrative, [])

        # Find matching seed ideas
        matching_seeds = [
            s for s in seed_ideas
            if s.get("category") in relevant_categories
        ]

        for seed in matching_seeds[:5]:  # Top 5 per narrative
            # Determine best template
            if data["high_influence_channels"]:
                template_key = "direct_correction"
                primary_channel = data["high_influence_channels"][0]
            else:
                template_key = "evidence_synthesis"
                primary_channel = None

            title_template = DEBUNK_TEMPLATES[template_key]
            title = title_template.format(
                channel=primary_channel,
                topic=seed.get("idea", "")
            )

            debunk_ideas.append({
                "title_idea": title,
                "narrative_addressed": narrative,
                "seed_id": seed.get("id"),
                "seed_idea": seed.get("idea"),
                "category": seed.get("category"),
                "channels_to_counter": data["high_influence_channels"][:3],
                "priority_score": data["total_reach"] * len(matching_seeds),
                "template_used": template_key,
                "hinglish_hook": generate_hinglish_hook(narrative, seed.get("idea"))
            })

    # Sort by priority
    debunk_ideas.sort(key=lambda x: x["priority_score"], reverse=True)

    return debunk_ideas


def generate_hinglish_hook(narrative, topic):
    """Generate Hinglish hooks for debunk videos."""
    hooks = {
        "ldl_skepticism": f"Aapko YouTube pe bataya gaya ki LDL kharab nahi hai? Dekhiye science kya kehti hai about {topic}...",
        "statin_fear": f"Statin se darr lagta hai? {topic} ke baare mein poori sachai suniye...",
        "insulin_primacy": f"Sirf insulin fix karna kaafi hai? {topic} ka pura picture samajhiye...",
        "fasting_absolutism": f"Fasting se sab theek ho jayega? {topic} mein nuance zaroori hai...",
        "supplement_superiority": f"Supplement dawai se better hai? {topic} ka evidence dekhte hain...",
        "seed_oil_villain": f"Seed oil se heart disease? {topic} ki research actually kya kehti hai..."
    }
    return hooks.get(narrative, f"Dekhiye {topic} ke baare mein kya confusion hai...")


def generate_response_videos(channel_analysis, channels_data):
    """Generate specific 'response to' video ideas for high-performing misinformation."""
    response_ideas = []

    # Get debunk priority from channels config
    debunk_priority = channels_data.get("debunk_priority", {})
    high_priority = debunk_priority.get("high", [])

    for channel_name, data in channel_analysis.items():
        if channel_name not in high_priority:
            continue

        # Get high-performing videos with narratives
        high_perf_videos = sorted(
            data["video_samples"],
            key=lambda x: x.get("views", 0),
            reverse=True
        )[:5]

        for video in high_perf_videos:
            if not video.get("narratives_detected"):
                continue

            response_ideas.append({
                "type": "response_video",
                "original_channel": channel_name,
                "original_title": video.get("title"),
                "original_url": video.get("url"),
                "original_views": video.get("views", 0),
                "narratives_to_address": video.get("narratives_detected", []),
                "suggested_title": f"Cardiologist Reacts: {video.get('title', '')[:50]}...",
                "hinglish_title": f"Cardiologist ki Response: {video.get('title', '')[:40]}... kya sach hai?"
            })

    # Sort by original views (higher views = more people misinformed = higher priority)
    response_ideas.sort(key=lambda x: x["original_views"], reverse=True)

    return response_ideas


def export_analysis(channel_analysis, narrative_prevalence, debunk_ideas, response_ideas, output_path):
    """Export full analysis for content calendar integration."""
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "channels_analyzed": len(channel_analysis),
            "narratives_tracked": len(NARRATIVE_KEYWORDS),
            "debunk_ideas_generated": len(debunk_ideas),
            "response_videos_suggested": len(response_ideas)
        },
        "narrative_threat_ranking": [],
        "channel_analysis": channel_analysis,
        "narrative_prevalence": narrative_prevalence,
        "debunk_ideas": debunk_ideas[:50],
        "response_videos": response_ideas[:20],
        "content_calendar_items": []
    }

    # Create threat ranking
    for narrative, data in sorted(
        narrative_prevalence.items(),
        key=lambda x: x[1]["total_reach"],
        reverse=True
    ):
        export_data["narrative_threat_ranking"].append({
            "narrative": narrative,
            "threat_level": "HIGH" if data["total_reach"] >= 15 else "MEDIUM" if data["total_reach"] >= 8 else "LOW",
            "total_reach": data["total_reach"],
            "channels_count": len(data["channels_promoting"]),
            "description": NARRATIVE_KEYWORDS.get(narrative, [""])[0] if narrative in NARRATIVE_KEYWORDS else ""
        })

    # Generate content calendar items
    for idea in debunk_ideas[:10]:
        export_data["content_calendar_items"].append({
            "type": "debunk",
            "title": idea["title_idea"],
            "narrative": idea["narrative_addressed"],
            "priority": "HIGH" if idea["priority_score"] > 100 else "MEDIUM"
        })

    for resp in response_ideas[:5]:
        export_data["content_calendar_items"].append({
            "type": "response",
            "title": resp["suggested_title"],
            "original_url": resp["original_url"],
            "priority": "HIGH" if resp["original_views"] > 100000 else "MEDIUM"
        })

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(export_data, f, indent=2)

    return export_data


def main():
    parser = argparse.ArgumentParser(description="Monitor narratives in the shadow medical school")
    parser.add_argument("--narrative", type=str, help="Filter by specific narrative type")
    parser.add_argument("--debunk", action="store_true", help="Generate debunk content ideas")
    parser.add_argument("--response", action="store_true", help="Generate response video ideas")
    parser.add_argument("--export", action="store_true", help="Export full analysis")
    parser.add_argument("--threats", action="store_true", help="Show narrative threat ranking")
    args = parser.parse_args()

    print("Loading data...")
    channels_data = load_channels()
    scraped_data = load_scraped_data()
    seed_ideas = load_seed_ideas()

    print(f"Channels configured: {sum(len(v) for v in channels_data.values() if isinstance(v, list))}")
    print(f"Videos scraped: {len(scraped_data['videos'])}")
    print(f"Seed ideas loaded: {len(seed_ideas)}")

    print("\nAnalyzing channel narratives...")
    channel_analysis = analyze_channel_narratives(channels_data, scraped_data)

    print("Calculating narrative prevalence...")
    narrative_prevalence = get_narrative_prevalence(channel_analysis)

    # Show threat ranking
    if args.threats or not any([args.debunk, args.response, args.export]):
        print(f"\n{'='*70}")
        print("NARRATIVE THREAT RANKING (by total channel reach)")
        print(f"{'='*70}")

        for narrative, data in sorted(
            narrative_prevalence.items(),
            key=lambda x: x[1]["total_reach"],
            reverse=True
        ):
            if args.narrative and narrative != args.narrative:
                continue

            threat = "HIGH" if data["total_reach"] >= 15 else "MEDIUM" if data["total_reach"] >= 8 else "LOW"
            print(f"\n{narrative.upper().replace('_', ' ')}")
            print(f"  Threat Level: {threat}")
            print(f"  Total Reach Score: {data['total_reach']}")
            print(f"  Channels Promoting: {len(data['channels_promoting'])}")
            if data["high_influence_channels"]:
                print(f"  High-Influence Channels: {', '.join(data['high_influence_channels'][:3])}")

    # Generate debunk ideas
    if args.debunk or args.export:
        print(f"\n{'='*70}")
        print("DEBUNK CONTENT IDEAS")
        print(f"{'='*70}")

        debunk_ideas = generate_debunk_ideas(narrative_prevalence, seed_ideas, channels_data)

        for i, idea in enumerate(debunk_ideas[:15], 1):
            print(f"\n{i}. {idea['title_idea']}")
            print(f"   Addresses: {idea['narrative_addressed']}")
            print(f"   Counters: {', '.join(idea['channels_to_counter'][:2])}")
            print(f"   Priority: {idea['priority_score']}")
            print(f"   Hook: {idea['hinglish_hook'][:80]}...")
    else:
        debunk_ideas = []

    # Generate response videos
    if args.response or args.export:
        print(f"\n{'='*70}")
        print("RESPONSE VIDEO IDEAS")
        print(f"{'='*70}")

        response_ideas = generate_response_videos(channel_analysis, channels_data)

        for i, resp in enumerate(response_ideas[:10], 1):
            print(f"\n{i}. RESPOND TO: {resp['original_channel']}")
            print(f"   Original: {resp['original_title'][:60]}...")
            print(f"   Views: {resp['original_views']:,}")
            print(f"   Your Title: {resp['suggested_title'][:60]}...")
            print(f"   Narratives: {', '.join(resp['narratives_to_address'])}")
    else:
        response_ideas = []

    # Export
    if args.export:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"narrative_analysis_{timestamp}.json"

        # Regenerate if not already done
        if not debunk_ideas:
            debunk_ideas = generate_debunk_ideas(narrative_prevalence, seed_ideas, channels_data)
        if not response_ideas:
            response_ideas = generate_response_videos(channel_analysis, channels_data)

        export_data = export_analysis(
            channel_analysis, narrative_prevalence,
            debunk_ideas, response_ideas, output_file
        )

        print(f"\n{'='*70}")
        print(f"EXPORTED TO: {output_file}")
        print(f"{'='*70}")
        print(f"Threat ranking items: {len(export_data['narrative_threat_ranking'])}")
        print(f"Debunk ideas: {len(export_data['debunk_ideas'])}")
        print(f"Response videos: {len(export_data['response_videos'])}")
        print(f"Calendar items: {len(export_data['content_calendar_items'])}")


if __name__ == "__main__":
    main()
