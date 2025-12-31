#!/usr/bin/env python3
"""
Comment Scraper - Download comments from YouTube videos
Uses youtube-comment-downloader (no API key required)

Usage:
    python comment_scraper.py                           # Scrape comments from latest video scrape
    python comment_scraper.py --video VIDEO_ID          # Scrape single video
    python comment_scraper.py --top 50                  # Scrape top 50 videos by views
    python comment_scraper.py --channel "Peter Attia"   # Scrape videos from specific channel
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import re

try:
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
except ImportError:
    print("Installing youtube-comment-downloader...")
    os.system("pip install youtube-comment-downloader")
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCRAPED_DIR = DATA_DIR / "scraped"


def load_latest_videos():
    """Load the most recent video scrape."""
    latest_file = SCRAPED_DIR / "latest_scrape.json"
    if not latest_file.exists():
        print("No video scrape found. Run channel_scraper.py first.")
        return []

    with open(latest_file, "r") as f:
        latest = json.load(f)

    videos_file = Path(latest["file"])
    if not videos_file.exists():
        print(f"Videos file not found: {videos_file}")
        return []

    with open(videos_file, "r") as f:
        return json.load(f)


def scrape_comments(video_id, max_comments=200):
    """
    Scrape comments from a single video.

    Returns list of comment dicts with text, author, likes, etc.
    """
    comments = []
    downloader = YoutubeCommentDownloader()

    try:
        comment_generator = downloader.get_comments_from_url(
            f"https://www.youtube.com/watch?v={video_id}",
            sort_by=SORT_BY_POPULAR
        )

        for i, comment in enumerate(comment_generator):
            if i >= max_comments:
                break

            comments.append({
                "text": comment.get("text", ""),
                "author": comment.get("author", ""),
                "likes": comment.get("votes", 0),
                "time": comment.get("time", ""),
                "is_reply": comment.get("reply", False),
                "video_id": video_id
            })

    except Exception as e:
        print(f"    Error scraping comments for {video_id}: {str(e)}")

    return comments


def extract_questions(comments):
    """Extract questions from comments (demand signals)."""
    questions = []
    question_patterns = [
        r'\?',  # Contains question mark
        r'^(what|how|why|when|where|which|can|should|does|is|are|will|would)\s',  # Starts with question word
        r'(kya|kaise|kyun|kab|kahan|kaun|kya)\s',  # Hindi question words
    ]

    for comment in comments:
        text = comment["text"].lower()
        for pattern in question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                questions.append({
                    "question": comment["text"],
                    "likes": comment["likes"],
                    "video_id": comment["video_id"]
                })
                break

    # Sort by likes (most popular questions first)
    questions.sort(key=lambda x: x["likes"], reverse=True)
    return questions


def extract_pain_points(comments):
    """Extract pain points and concerns from comments."""
    pain_keywords = [
        # English
        "problem", "issue", "difficult", "hard", "struggle", "confused",
        "worried", "scared", "fear", "afraid", "help", "please",
        "don't understand", "not clear", "side effect", "risk",
        # Hindi
        "problem", "dikkat", "mushkil", "pareshan", "dar", "darr",
        "samajh nahi", "kya karu", "help", "please"
    ]

    pain_points = []
    for comment in comments:
        text = comment["text"].lower()
        for keyword in pain_keywords:
            if keyword in text:
                pain_points.append({
                    "text": comment["text"],
                    "keyword_matched": keyword,
                    "likes": comment["likes"],
                    "video_id": comment["video_id"]
                })
                break

    pain_points.sort(key=lambda x: x["likes"], reverse=True)
    return pain_points


def main():
    parser = argparse.ArgumentParser(description="Scrape YouTube video comments")
    parser.add_argument("--video", type=str, help="Scrape single video by ID")
    parser.add_argument("--top", type=int, default=30, help="Scrape top N videos by views")
    parser.add_argument("--channel", type=str, help="Filter by channel name")
    parser.add_argument("--max-comments", type=int, default=200, help="Max comments per video")
    parser.add_argument("--type", type=str, choices=["competition", "inspiration", "all"],
                        default="all", help="Filter by channel type")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.video:
        # Single video mode
        print(f"Scraping comments for video: {args.video}")
        comments = scrape_comments(args.video, args.max_comments)
        print(f"Scraped {len(comments)} comments")

        # Save
        output_file = SCRAPED_DIR / f"comments_{args.video}_{timestamp}.json"
        with open(output_file, "w") as f:
            json.dump({
                "video_id": args.video,
                "comments": comments,
                "questions": extract_questions(comments),
                "pain_points": extract_pain_points(comments)
            }, f, indent=2)
        print(f"Saved to: {output_file}")
        return

    # Multi-video mode from scraped data
    videos = load_latest_videos()
    if not videos:
        return

    # Filter videos
    if args.channel:
        videos = [v for v in videos if args.channel.lower() in v["channel_name"].lower()]
    if args.type != "all":
        videos = [v for v in videos if v.get("channel_type") == args.type]

    # Sort by views and take top N
    videos.sort(key=lambda x: x.get("views", 0), reverse=True)
    videos = videos[:args.top]

    print(f"\nWill scrape comments from {len(videos)} videos")
    print(f"Max {args.max_comments} comments per video\n")

    # Scrape comments
    all_comments = []
    video_comments = {}

    for i, video in enumerate(videos):
        video_id = video["video_id"]
        title = video.get("title", "Unknown")[:50]
        views = video.get("views", 0)

        print(f"[{i+1}/{len(videos)}] {title}... ({views:,} views)")

        comments = scrape_comments(video_id, args.max_comments)
        print(f"    Got {len(comments)} comments")

        # Add video metadata to each comment
        for comment in comments:
            comment["video_title"] = video.get("title", "")
            comment["video_views"] = views
            comment["channel_name"] = video.get("channel_name", "")
            comment["channel_type"] = video.get("channel_type", "")

        all_comments.extend(comments)
        video_comments[video_id] = {
            "video_title": video.get("title", ""),
            "video_views": views,
            "channel_name": video.get("channel_name", ""),
            "comments": comments
        }

    # Extract insights
    all_questions = extract_questions(all_comments)
    all_pain_points = extract_pain_points(all_comments)

    # Save comprehensive results
    results = {
        "timestamp": timestamp,
        "videos_scraped": len(videos),
        "total_comments": len(all_comments),
        "total_questions": len(all_questions),
        "total_pain_points": len(all_pain_points),
        "top_questions": all_questions[:100],  # Top 100 by likes
        "top_pain_points": all_pain_points[:100],
        "by_video": video_comments,
        "all_comments": all_comments
    }

    output_file = SCRAPED_DIR / f"comments_analysis_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    # Save latest pointer
    latest_file = SCRAPED_DIR / "latest_comments.json"
    with open(latest_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "file": str(output_file),
            "videos_scraped": len(videos),
            "total_comments": len(all_comments)
        }, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print("COMMENT SCRAPE SUMMARY")
    print(f"{'='*60}")
    print(f"Videos analyzed: {len(videos)}")
    print(f"Total comments: {len(all_comments)}")
    print(f"Questions found: {len(all_questions)}")
    print(f"Pain points found: {len(all_pain_points)}")

    print(f"\nTop 10 Questions (by likes):")
    for i, q in enumerate(all_questions[:10], 1):
        text = q["question"][:80] + "..." if len(q["question"]) > 80 else q["question"]
        print(f"  {i}. [{q['likes']} likes] {text}")

    print(f"\nTop 10 Pain Points:")
    for i, p in enumerate(all_pain_points[:10], 1):
        text = p["text"][:80] + "..." if len(p["text"]) > 80 else p["text"]
        print(f"  {i}. [{p['likes']} likes] {text}")

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
