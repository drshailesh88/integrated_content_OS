#!/usr/bin/env python3
"""
MASTER PIPELINE - Data-Powered Content Research Engine

Runs the complete pipeline:
1. Scrape competition & inspiration channels
2. Download comments from top videos
3. Analyze demand signals
4. Train view prediction model
5. Find content gaps
6. Generate prioritized content calendar

Usage:
    python run_pipeline.py                  # Run full pipeline
    python run_pipeline.py --scrape-only    # Just scrape, no analysis
    python run_pipeline.py --analyze-only   # Just analyze existing data
    python run_pipeline.py --quick          # Quick mode (fewer videos)
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
SCRAPER_DIR = SCRIPT_DIR / "scraper"
ANALYZER_DIR = SCRIPT_DIR / "analyzer"
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_DIR = SCRIPT_DIR / "output"
ROOT_DIR = SCRIPT_DIR.parent


def should_publish_to_notion() -> bool:
    return os.getenv("NOTION_AUTO_PUBLISH", "").lower() in {"1", "true", "yes"}


def sync_outputs_to_notion(paths):
    sync_script = ROOT_DIR / "scripts" / "notion_sync.py"
    if not sync_script.exists():
        print("Notion sync skipped: scripts/notion_sync.py not found.")
        return
    cmd = [sys.executable, str(sync_script)]
    for path in paths:
        cmd.extend(["--path", str(path)])
    subprocess.run(cmd, cwd=str(ROOT_DIR))


def run_command(cmd, description):
    """Run a command and handle output."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR))

    if result.returncode != 0:
        print(f"WARNING: {description} returned non-zero exit code")
        return False
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = ["scrapetube", "youtube_comment_downloader", "sklearn", "textblob"]
    missing = []

    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print("Missing dependencies. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r",
                       str(SCRIPT_DIR.parent / "requirements.txt")])


def run_full_pipeline(args):
    """Run the complete data pipeline."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║         DR. SHAILESH CONTENT RESEARCH ENGINE                      ║
║         Data-Powered Content Pipeline                              ║
╠══════════════════════════════════════════════════════════════════╣
║  Timestamp: {timestamp}                                       ║
║  Mode: {'QUICK' if args.quick else 'FULL'}                                                         ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    # Set limits based on mode
    video_limit = 30 if args.quick else 100
    comment_limit = 100 if args.quick else 200
    top_videos = 15 if args.quick else 30

    steps_completed = []
    steps_failed = []

    # PHASE 1: SCRAPE
    if not args.analyze_only:
        print("\n" + "="*60)
        print("PHASE 1: SCRAPING YOUTUBE DATA")
        print("="*60)

        # Scrape channels
        success = run_command(
            [sys.executable, str(SCRAPER_DIR / "channel_scraper.py"),
             "--limit", str(video_limit)],
            "Scraping competition & inspiration channels"
        )
        if success:
            steps_completed.append("Channel scraping")
        else:
            steps_failed.append("Channel scraping")

        # Scrape comments
        success = run_command(
            [sys.executable, str(SCRAPER_DIR / "comment_scraper.py"),
             "--top", str(top_videos),
             "--max-comments", str(comment_limit)],
            "Downloading comments from top videos"
        )
        if success:
            steps_completed.append("Comment scraping")
        else:
            steps_failed.append("Comment scraping")

    # PHASE 2: ANALYZE
    if not args.scrape_only:
        print("\n" + "="*60)
        print("PHASE 2: ANALYZING DATA")
        print("="*60)

        # Demand signals
        success = run_command(
            [sys.executable, str(ANALYZER_DIR / "demand_signals.py")],
            "Analyzing demand signals"
        )
        if success:
            steps_completed.append("Demand analysis")
        else:
            steps_failed.append("Demand analysis")

        # Train view predictor
        success = run_command(
            [sys.executable, str(ANALYZER_DIR / "view_predictor.py"), "--train"],
            "Training view prediction model"
        )
        if success:
            steps_completed.append("View predictor training")
        else:
            steps_failed.append("View predictor training")

        # Find gaps
        success = run_command(
            [sys.executable, str(ANALYZER_DIR / "gap_finder.py"),
             "--export", "--top", "30"],
            "Finding content gaps"
        )
        if success:
            steps_completed.append("Gap analysis")
        else:
            steps_failed.append("Gap analysis")

    # SUMMARY
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                      PIPELINE COMPLETE                            ║
╠══════════════════════════════════════════════════════════════════╣
║  Steps completed: {len(steps_completed)}                                               ║
║  Steps failed: {len(steps_failed)}                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Completed:                                                       ║""")

    for step in steps_completed:
        print(f"║    ✓ {step:<55} ║")

    if steps_failed:
        print("║  Failed:                                                        ║")
        for step in steps_failed:
            print(f"║    ✗ {step:<55} ║")

    print(f"""╠══════════════════════════════════════════════════════════════════╣
║  OUTPUT FILES:                                                    ║
║    • {str(DATA_DIR / 'scraped' / 'latest_scrape.json'):<54} ║
║    • {str(DATA_DIR / 'scraped' / 'latest_comments.json'):<54} ║
║    • {str(OUTPUT_DIR / 'demand_analysis_*.json'):<54} ║
║    • {str(OUTPUT_DIR / 'content_gaps_*.json'):<54} ║
╠══════════════════════════════════════════════════════════════════╣
║  NEXT STEPS:                                                      ║
║    1. Review content_gaps_*.json for top opportunities            ║
║    2. Use view_predictor.py to score specific ideas               ║
║    3. Run /new-script in Claude Code to write scripts             ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    if should_publish_to_notion():
        sync_outputs_to_notion([OUTPUT_DIR, DATA_DIR / "scraped"])


def main():
    parser = argparse.ArgumentParser(description="Run the content research pipeline")
    parser.add_argument("--scrape-only", action="store_true",
                       help="Only scrape data, skip analysis")
    parser.add_argument("--analyze-only", action="store_true",
                       help="Only analyze existing data")
    parser.add_argument("--quick", action="store_true",
                       help="Quick mode with reduced data")
    args = parser.parse_args()

    # Ensure output directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "scraped").mkdir(exist_ok=True)
    (DATA_DIR / "models").mkdir(exist_ok=True)

    # Check dependencies
    check_dependencies()

    # Run pipeline
    run_full_pipeline(args)


if __name__ == "__main__":
    main()
