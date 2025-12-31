#!/usr/bin/env python3
"""
Demand Signals Analyzer - Extract what audiences WANT from scraped data

Analyzes:
- Questions people ask (demand for answers)
- Pain points and struggles (opportunity for solutions)
- Topic popularity (views vs. engagement)
- Content gaps (high demand, low supply)

Usage:
    python demand_signals.py                    # Analyze latest scraped data
    python demand_signals.py --export brief     # Export as content brief
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

try:
    from textblob import TextBlob
except ImportError:
    import os
    os.system("pip install textblob")
    from textblob import TextBlob

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"


def load_latest_data():
    """Load latest scraped videos and comments."""
    data = {
        "videos": [],
        "comments": [],
        "questions": [],
        "pain_points": []
    }

    # Load videos
    latest_videos = SCRAPED_DIR / "latest_scrape.json"
    if latest_videos.exists():
        with open(latest_videos, "r") as f:
            meta = json.load(f)
        videos_file = Path(meta["file"])
        if videos_file.exists():
            with open(videos_file, "r") as f:
                data["videos"] = json.load(f)

    # Load comments
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
                data["pain_points"] = comment_data.get("top_pain_points", [])

    return data


def extract_topics_from_titles(videos):
    """Extract topic patterns from video titles."""
    # Common cardiology/health terms to look for
    topic_patterns = {
        "biomarkers": ["cholesterol", "ldl", "hdl", "triglyceride", "apo b", "lp(a)", "hba1c", "crp", "troponin"],
        "conditions": ["heart attack", "stroke", "hypertension", "bp", "blood pressure", "diabetes", "afib", "arrhythmia"],
        "treatments": ["statin", "medication", "surgery", "angioplasty", "stent", "bypass", "cabg"],
        "lifestyle": ["diet", "exercise", "weight", "sleep", "stress", "smoking", "alcohol"],
        "tests": ["ecg", "echo", "stress test", "angiography", "ct scan", "cac score"],
    }

    topic_counts = defaultdict(lambda: {"count": 0, "total_views": 0, "videos": []})

    for video in videos:
        title = video.get("title", "").lower()
        views = video.get("views", 0)

        for category, keywords in topic_patterns.items():
            for keyword in keywords:
                if keyword in title:
                    topic_counts[keyword]["count"] += 1
                    topic_counts[keyword]["total_views"] += views
                    topic_counts[keyword]["videos"].append({
                        "title": video.get("title"),
                        "views": views,
                        "channel": video.get("channel_name")
                    })

    # Calculate average views per topic
    for topic, data in topic_counts.items():
        data["avg_views"] = data["total_views"] // data["count"] if data["count"] > 0 else 0

    return dict(topic_counts)


def extract_question_themes(questions):
    """Cluster questions into themes."""
    themes = {
        "how_to": [],
        "what_is": [],
        "why": [],
        "when_to": [],
        "side_effects": [],
        "comparison": [],
        "personal_situation": [],
        "diet_nutrition": [],
        "medication": [],
        "symptoms": [],
    }

    for q in questions:
        text = q["question"].lower()

        if any(w in text for w in ["how to", "how do", "how can", "kaise"]):
            themes["how_to"].append(q)
        elif any(w in text for w in ["what is", "what are", "kya hai", "kya hota"]):
            themes["what_is"].append(q)
        elif any(w in text for w in ["why", "kyun", "kyu"]):
            themes["why"].append(q)
        elif any(w in text for w in ["when", "kab"]):
            themes["when_to"].append(q)
        elif any(w in text for w in ["side effect", "reaction", "problem"]):
            themes["side_effects"].append(q)
        elif any(w in text for w in [" vs ", "better", "compare", "difference"]):
            themes["comparison"].append(q)
        elif any(w in text for w in ["my", "mera", "mere", "i have", "mujhe"]):
            themes["personal_situation"].append(q)
        elif any(w in text for w in ["eat", "food", "diet", "khana", "nutrition"]):
            themes["diet_nutrition"].append(q)
        elif any(w in text for w in ["medicine", "tablet", "drug", "dawai"]):
            themes["medication"].append(q)
        elif any(w in text for w in ["symptom", "sign", "feel", "pain", "dard"]):
            themes["symptoms"].append(q)

    # Sort each theme by likes
    for theme in themes:
        themes[theme].sort(key=lambda x: x.get("likes", 0), reverse=True)

    return themes


def analyze_content_performance(videos):
    """Analyze what content performs best."""
    # Group by channel type
    by_type = defaultdict(list)
    for video in videos:
        by_type[video.get("channel_type", "unknown")].append(video)

    performance = {}
    for channel_type, type_videos in by_type.items():
        if not type_videos:
            continue

        views = [v.get("views", 0) for v in type_videos]
        durations = [v.get("duration_seconds", 0) for v in type_videos if v.get("duration_seconds", 0) > 0]

        performance[channel_type] = {
            "total_videos": len(type_videos),
            "total_views": sum(views),
            "avg_views": sum(views) // len(views) if views else 0,
            "max_views": max(views) if views else 0,
            "avg_duration_seconds": sum(durations) // len(durations) if durations else 0,
            "top_videos": sorted(type_videos, key=lambda x: x.get("views", 0), reverse=True)[:10]
        }

    return performance


def find_content_gaps(videos, questions, seed_ideas_file=None):
    """
    Find gaps: topics with high question demand but low video coverage.
    """
    # Load seed ideas for matching
    seed_ideas = []
    seed_file = DATA_DIR / "seed-ideas.json"
    if seed_file.exists():
        with open(seed_file, "r") as f:
            seed_ideas = json.load(f)

    # Extract all video titles
    video_titles = " ".join([v.get("title", "").lower() for v in videos])

    # Count seed idea mentions in questions vs videos
    gaps = []
    for seed in seed_ideas:
        idea = seed.get("idea", "").lower()
        idea_words = idea.split()

        # Check if idea appears in questions (demand)
        question_mentions = sum(1 for q in questions if idea in q.get("question", "").lower())

        # Check if idea appears in existing videos (supply)
        video_mentions = video_titles.count(idea)

        # High demand (questions) + low supply (videos) = GAP
        if question_mentions > 0:
            gap_score = question_mentions / (video_mentions + 1)  # Avoid division by zero
            gaps.append({
                "seed_idea": seed.get("idea"),
                "category": seed.get("category"),
                "question_demand": question_mentions,
                "video_supply": video_mentions,
                "gap_score": round(gap_score, 2),
                "sample_questions": [q["question"] for q in questions if idea in q.get("question", "").lower()][:3]
            })

    # Sort by gap score
    gaps.sort(key=lambda x: x["gap_score"], reverse=True)

    return gaps


def generate_content_brief(demand_data):
    """Generate actionable content brief from demand analysis."""
    brief = {
        "generated_at": datetime.now().isoformat(),
        "summary": {},
        "high_priority_topics": [],
        "question_opportunities": [],
        "gap_opportunities": [],
        "audience_pain_points": [],
        "recommendations": []
    }

    # Summary stats
    brief["summary"] = {
        "videos_analyzed": len(demand_data.get("videos", [])),
        "comments_analyzed": len(demand_data.get("comments", [])),
        "questions_found": len(demand_data.get("questions", [])),
        "pain_points_found": len(demand_data.get("pain_points", []))
    }

    # High priority topics (most views)
    topics = extract_topics_from_titles(demand_data.get("videos", []))
    sorted_topics = sorted(topics.items(), key=lambda x: x[1]["avg_views"], reverse=True)
    brief["high_priority_topics"] = [
        {
            "topic": topic,
            "avg_views": data["avg_views"],
            "video_count": data["count"],
            "top_video": data["videos"][0] if data["videos"] else None
        }
        for topic, data in sorted_topics[:20]
    ]

    # Question opportunities (most liked questions)
    question_themes = extract_question_themes(demand_data.get("questions", []))
    brief["question_opportunities"] = {
        theme: [{"question": q["question"], "likes": q["likes"]} for q in qs[:5]]
        for theme, qs in question_themes.items()
        if qs
    }

    # Gap opportunities
    gaps = find_content_gaps(
        demand_data.get("videos", []),
        demand_data.get("questions", [])
    )
    brief["gap_opportunities"] = gaps[:20]

    # Pain points
    brief["audience_pain_points"] = [
        {"text": p["text"], "likes": p["likes"]}
        for p in demand_data.get("pain_points", [])[:20]
    ]

    # Recommendations
    brief["recommendations"] = [
        f"Create content on '{gaps[0]['seed_idea']}' - high question demand, low video supply" if gaps else None,
        f"Focus on '{sorted_topics[0][0]}' topic - avg {sorted_topics[0][1]['avg_views']:,} views" if sorted_topics else None,
        f"Address '{question_themes['how_to'][0]['question'][:50]}...' - {question_themes['how_to'][0]['likes']} likes" if question_themes.get("how_to") else None,
    ]
    brief["recommendations"] = [r for r in brief["recommendations"] if r]

    return brief


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze demand signals from scraped data")
    parser.add_argument("--export", type=str, choices=["brief", "full", "json"],
                        default="brief", help="Export format")
    args = parser.parse_args()

    print("Loading scraped data...")
    data = load_latest_data()

    if not data["videos"] and not data["comments"]:
        print("No scraped data found. Run channel_scraper.py and comment_scraper.py first.")
        return

    print(f"Loaded {len(data['videos'])} videos, {len(data['comments'])} comments")

    # Generate analysis
    print("\nAnalyzing demand signals...")

    brief = generate_content_brief(data)

    # Save output
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = OUTPUT_DIR / f"demand_analysis_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(brief, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print("DEMAND ANALYSIS SUMMARY")
    print(f"{'='*60}")

    print(f"\nVideos analyzed: {brief['summary']['videos_analyzed']}")
    print(f"Comments analyzed: {brief['summary']['comments_analyzed']}")

    print(f"\n--- TOP PERFORMING TOPICS ---")
    for topic in brief["high_priority_topics"][:10]:
        print(f"  {topic['topic']}: {topic['avg_views']:,} avg views ({topic['video_count']} videos)")

    print(f"\n--- CONTENT GAPS (High demand, low supply) ---")
    for gap in brief["gap_opportunities"][:10]:
        print(f"  {gap['seed_idea']}: gap_score={gap['gap_score']} (demand={gap['question_demand']}, supply={gap['video_supply']})")

    print(f"\n--- TOP AUDIENCE QUESTIONS ---")
    for theme, questions in list(brief["question_opportunities"].items())[:5]:
        if questions:
            print(f"\n  [{theme}]")
            for q in questions[:3]:
                text = q["question"][:70] + "..." if len(q["question"]) > 70 else q["question"]
                print(f"    - [{q['likes']} likes] {text}")

    print(f"\n--- RECOMMENDATIONS ---")
    for i, rec in enumerate(brief["recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\nFull analysis saved to: {output_file}")


if __name__ == "__main__":
    main()
