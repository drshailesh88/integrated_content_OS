#!/usr/bin/env python3
"""
Chunked YouTube Comment Analyzer - CLI Tool

Analyzes YouTube comments using map-reduce approach with free LLMs.
Outputs results to a file (preserves Claude context window).

Usage:
    # Analyze a single video by ID
    python analyze_chunked.py VIDEO_ID

    # Analyze from latest comment scrape
    python analyze_chunked.py --latest

    # Analyze from a specific file
    python analyze_chunked.py --file data/scraped/comments_xxx.json

    # Use specific model
    python analyze_chunked.py VIDEO_ID --model qwen-2.5-72b

    # Force map-reduce even for small sets
    python analyze_chunked.py VIDEO_ID --force-map-reduce

Examples:
    python analyze_chunked.py dQw4w9WgXcQ
    python analyze_chunked.py --latest --force-map-reduce
    python analyze_chunked.py --file data/scraped/comments_analysis_20241214.json
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from llm.chunked_analyzer import ChunkedAnalyzer, FREE_MODELS
from dataclasses import asdict

# Paths
DATA_DIR = SCRIPT_DIR / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


def scrape_video_comments(video_id: str, max_comments: int = 2000) -> list:
    """Scrape comments from a YouTube video."""
    try:
        from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
    except ImportError:
        print("Installing youtube-comment-downloader...")
        os.system("pip install youtube-comment-downloader")
        from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

    print(f"\nScraping comments for video: {video_id}")
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

            if i % 100 == 0 and i > 0:
                print(f"  Scraped {i} comments...")

            comments.append({
                "text": comment.get("text", ""),
                "author": comment.get("author", ""),
                "likes": comment.get("votes", 0),
                "time": comment.get("time", ""),
                "is_reply": comment.get("reply", False),
                "video_id": video_id
            })

    except Exception as e:
        print(f"Error scraping comments: {e}")
        return []

    print(f"  Scraped {len(comments)} comments total")
    return comments


def load_latest_comments() -> tuple:
    """Load comments from the latest comment scrape."""
    latest_file = SCRAPED_DIR / "latest_comments.json"

    if not latest_file.exists():
        print("No latest comments file found. Run comment_scraper.py first or provide --video.")
        return None, None

    with open(latest_file, "r") as f:
        latest = json.load(f)

    comments_file = Path(latest["file"])
    if not comments_file.exists():
        print(f"Comments file not found: {comments_file}")
        return None, None

    with open(comments_file, "r") as f:
        data = json.load(f)

    # Extract all comments
    all_comments = data.get("all_comments", [])
    if not all_comments and "by_video" in data:
        # Flatten from by_video structure
        for video_data in data["by_video"].values():
            all_comments.extend(video_data.get("comments", []))

    return all_comments, latest


def load_comments_from_file(filepath: str) -> list:
    """Load comments from a JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    # Handle different file structures
    if "all_comments" in data:
        return data["all_comments"]
    elif "comments" in data:
        return data["comments"]
    elif "by_video" in data:
        all_comments = []
        for video_data in data["by_video"].values():
            all_comments.extend(video_data.get("comments", []))
        return all_comments
    else:
        # Assume it's a list
        return data if isinstance(data, list) else []


def save_results(result, source: str, output_path: Path = None):
    """Save analysis results to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if output_path is None:
        output_path = OUTPUT_DIR / f"chunked_analysis_{source}_{timestamp}.json"

    result_dict = asdict(result) if hasattr(result, '__dataclass_fields__') else result

    # Add metadata
    output_data = {
        "timestamp": timestamp,
        "source": source,
        "analysis": result_dict
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    return output_path


def print_summary(result):
    """Print a summary of the analysis results."""
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)

    # Stats
    stats = result.stats if hasattr(result, 'stats') else result.get("stats", {})
    print(f"\nComments analyzed: {stats.get('analyzed_comments', 'N/A')} / {stats.get('total_comments', 'N/A')}")
    print(f"Chunks processed: {stats.get('chunks_processed', 'N/A')}")
    print(f"Processing time: {stats.get('processing_time_seconds', 'N/A')}s")

    # Top Questions
    questions = result.top_questions if hasattr(result, 'top_questions') else result.get("top_questions", [])
    print(f"\n--- TOP QUESTIONS ({len(questions)}) ---")
    for i, q in enumerate(questions[:5], 1):
        question = q.get("question", str(q))
        urgency = q.get("urgency", "")
        freq = q.get("frequency", "")
        print(f"  {i}. [{urgency}] {question} (freq: {freq})")

    # Top Myths
    myths = result.top_myths if hasattr(result, 'top_myths') else result.get("top_myths", [])
    print(f"\n--- TOP MYTHS ({len(myths)}) ---")
    for i, m in enumerate(myths[:5], 1):
        myth = m.get("myth", str(m))
        danger = m.get("dangerLevel", "")
        print(f"  {i}. [{danger}] {myth}")

    # Pain Points
    pain_points = result.top_pain_points if hasattr(result, 'top_pain_points') else result.get("top_pain_points", [])
    print(f"\n--- TOP PAIN POINTS ({len(pain_points)}) ---")
    for i, p in enumerate(pain_points[:5], 1):
        point = p.get("painPoint", str(p))
        emotional = " [EMOTIONAL]" if p.get("emotional") else ""
        print(f"  {i}. {point}{emotional}")

    # Content Demands
    demands = result.content_demands if hasattr(result, 'content_demands') else result.get("content_demands", [])
    print(f"\n--- CONTENT DEMANDS ({len(demands)}) ---")
    for i, d in enumerate(demands[:5], 1):
        demand = d.get("demand", str(d))
        content_type = d.get("contentType", "")
        print(f"  {i}. [{content_type}] {demand}")

    # Recommendations
    recs = result.recommendations if hasattr(result, 'recommendations') else result.get("recommendations", {})
    print(f"\n--- RECOMMENDATIONS ---")
    print(f"  Must Address: {', '.join(recs.get('mustAddress', [])[:3])}")
    print(f"  Content Gaps: {', '.join(recs.get('contentGaps', [])[:3])}")
    print(f"  Viral Potential: {', '.join(recs.get('viralPotentialTopics', [])[:3])}")

    # Overall Sentiment
    sentiment = result.overall_sentiment if hasattr(result, 'overall_sentiment') else result.get("overall_sentiment", {})
    print(f"\n--- SENTIMENT ---")
    print(f"  Positive: {sentiment.get('positive', 0)} | Negative: {sentiment.get('negative', 0)} | Neutral: {sentiment.get('neutral', 0)}")
    print(f"  Summary: {sentiment.get('summary', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze YouTube comments with map-reduce approach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_chunked.py dQw4w9WgXcQ           # Analyze single video
  python analyze_chunked.py --latest              # Use latest scrape
  python analyze_chunked.py --file comments.json  # Use specific file

Available models:
  llama-3.3-70b (default), qwen-2.5-72b, gemini-2-flash,
  grok-2, deepseek-r1, mistral-small, gemma-3-27b
        """
    )

    parser.add_argument("video_id", nargs="?", help="YouTube video ID to analyze")
    parser.add_argument("--latest", action="store_true", help="Use latest comment scrape")
    parser.add_argument("--file", type=str, help="Path to comments JSON file")
    parser.add_argument("--model", type=str, default="llama-3.3-70b",
                        choices=list(FREE_MODELS.keys()),
                        help="Model to use for analysis")
    parser.add_argument("--synthesis-model", type=str, default="qwen-2.5-72b",
                        choices=list(FREE_MODELS.keys()),
                        help="Model to use for synthesis")
    parser.add_argument("--force-map-reduce", action="store_true",
                        help="Force map-reduce even for small comment sets")
    parser.add_argument("--force-quick", action="store_true",
                        help="Force quick analysis even for large sets")
    parser.add_argument("--max-comments", type=int, default=2000,
                        help="Max comments to scrape (default: 2000)")
    parser.add_argument("--chunk-size", type=int, default=100,
                        help="Comments per chunk (default: 100)")
    parser.add_argument("--max-chunks", type=int, default=20,
                        help="Max chunks to process (default: 20)")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    # Validate arguments
    if not args.video_id and not args.latest and not args.file:
        parser.error("Provide video_id, --latest, or --file")

    print("=" * 70)
    print("CHUNKED YOUTUBE COMMENT ANALYZER")
    print("=" * 70)

    # Load or scrape comments
    comments = []
    source = ""

    if args.video_id:
        source = args.video_id
        comments = scrape_video_comments(args.video_id, args.max_comments)
    elif args.file:
        source = Path(args.file).stem
        print(f"\nLoading comments from: {args.file}")
        comments = load_comments_from_file(args.file)
        print(f"  Loaded {len(comments)} comments")
    elif args.latest:
        comments, latest_meta = load_latest_comments()
        if comments:
            source = "latest_scrape"
            print(f"\nLoaded {len(comments)} comments from latest scrape")

    if not comments:
        print("\nNo comments to analyze. Exiting.")
        sys.exit(1)

    # Determine method
    force_method = None
    if args.force_map_reduce:
        force_method = "map-reduce"
    elif args.force_quick:
        force_method = "quick"

    # Initialize analyzer
    try:
        analyzer = ChunkedAnalyzer(
            chunk_model=FREE_MODELS[args.model],
            synthesis_model=FREE_MODELS[args.synthesis_model],
            chunk_size=args.chunk_size,
            max_chunks=args.max_chunks,
            verbose=not args.quiet
        )
    except ValueError as e:
        print(f"\nError: {e}")
        print("Make sure OPENROUTER_API_KEY is set in your environment or .env file")
        sys.exit(1)

    # Run analysis
    try:
        result = analyzer.analyze(comments, force_method=force_method)
    except Exception as e:
        print(f"\nAnalysis failed: {e}")
        sys.exit(1)

    # Save results
    output_path = Path(args.output) if args.output else None
    saved_path = save_results(result, source, output_path)
    print(f"\n Results saved to: {saved_path}")

    # Print summary
    if not args.quiet:
        print_summary(result)

    print("\n" + "=" * 70)
    print("DONE - Results saved. Read the output file to bring into Claude context.")
    print("=" * 70)


if __name__ == "__main__":
    main()
