#!/usr/bin/env python3
"""
Medical Content Engine - Main Pipeline
Orchestrates the full content generation workflow.

Usage:
    python main.py                  # Full run
    python main.py --test           # Test mode (3 articles only)
    python main.py --no-email       # Skip email sending
    python main.py --no-slack       # Skip Slack notification
    python main.py --feeds-only     # Only fetch, don't generate content
    python main.py --save           # Save intermediate results to JSON
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import RSS_FEEDS
from fetchers.rss_fetcher import fetch_all_rss
from fetchers.pubmed_fetcher import fetch_pubmed_articles, fetch_fallback_journals
from ai.triage import triage_articles
from ai.content_generator import generate_all_content
from delivery.email_sender import send_digest_email
from delivery.slack_sender import send_digest_notification
from delivery.markdown_writer import save_markdown_digest


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Medical Content Engine - Generate medical content for Dr. Shailesh Singh"
    )
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Test mode: process only 3 articles'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email'
    )
    parser.add_argument(
        '--no-slack',
        action='store_true',
        help='Skip Slack notification'
    )
    parser.add_argument(
        '--feeds-only',
        action='store_true',
        help='Only fetch articles, skip AI processing and delivery'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save intermediate results to JSON files'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output/digests',
        help='Directory for output files'
    )
    parser.add_argument(
        '--max-articles',
        type=int,
        default=50,
        help='Maximum articles to process (default: 50)'
    )
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Save output as Obsidian-compatible Markdown file'
    )
    parser.add_argument(
        '--notion',
        action='store_true',
        help='Publish output to Notion'
    )
    parser.add_argument(
        '--notion-status',
        type=str,
        default=None,
        help='Notion status (Draft/Final/Published)'
    )
    parser.add_argument(
        '--notion-tags',
        type=str,
        default=None,
        help='Comma-separated tags for Notion'
    )
    parser.add_argument(
        '--notion-platform',
        type=str,
        default=None,
        help='Override Notion platform label'
    )
    parser.add_argument(
        '--notion-title',
        type=str,
        default=None,
        help='Override Notion page title'
    )
    return parser.parse_args()


def save_json(data: any, filename: str, output_dir: str):
    """Save data to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  💾 Saved: {filepath}")


def parse_tags(tag_string: Optional[str]) -> List[str]:
    if not tag_string:
        return []
    return [tag.strip() for tag in tag_string.split(",") if tag.strip()]


def should_publish_to_notion(flag: bool) -> bool:
    return flag or os.getenv("NOTION_AUTO_PUBLISH", "").lower() in {"1", "true", "yes"}


def run_pipeline(args):
    """Run the full content pipeline."""
    start_time = datetime.now()
    date_str = start_time.strftime('%Y-%m-%d')
    
    print("\n" + "=" * 60)
    print("🏥 MEDICAL CONTENT ENGINE")
    print(f"   Dr. Shailesh Singh | {start_time.strftime('%B %d, %Y %H:%M')}")
    print("=" * 60)
    
    if args.test:
        print("\n⚠️  TEST MODE - Processing limited articles\n")
    
    # =========================================================================
    # STEP 1: Fetch Articles
    # =========================================================================
    print("\n📚 STEP 1: FETCHING ARTICLES")
    print("=" * 60)
    
    # Fetch from RSS feeds
    rss_articles = fetch_all_rss(max_per_feed=5 if args.test else 10)
    
    # Fetch from PubMed (general cardiology query)
    pubmed_articles = fetch_pubmed_articles(max_results=5 if args.test else 15)
    
    # Fetch from fallback journals (JACC, EHJ, EuroIntervention, etc.)
    # These journals have blocked RSS feeds, so we fetch via PubMed instead
    fallback_articles = fetch_fallback_journals(days_back=7 if not args.test else 14)
    
    # Combine all articles
    all_articles = rss_articles + pubmed_articles + fallback_articles
    
    print(f"\n📊 Total articles fetched: {len(all_articles)}")
    print(f"   - RSS feeds: {len(rss_articles)}")
    print(f"   - PubMed general: {len(pubmed_articles)}")
    print(f"   - Fallback journals (JACC, EHJ, etc.): {len(fallback_articles)}")
    
    if len(all_articles) == 0:
        print("\n❌ No articles fetched. Check internet connection and feed URLs.")
        return
    
    # Limit articles for processing
    max_articles = 3 if args.test else args.max_articles
    if len(all_articles) > max_articles:
        print(f"\n⚠️  Limiting to {max_articles} articles for processing")
        all_articles = all_articles[:max_articles]
    
    # Save fetched articles
    if args.save:
        save_json(all_articles, f'fetched_{date_str}.json', args.output_dir)
    
    # Stop here if feeds-only mode
    if args.feeds_only:
        print("\n✅ Feeds-only mode complete. Skipping AI processing.")
        return
    
    # =========================================================================
    # STEP 2: Triage Articles
    # =========================================================================
    print("\n🤖 STEP 2: AI TRIAGE")
    print("=" * 60)
    
    triaged = triage_articles(all_articles, min_confidence=5)
    
    b2c_count = len(triaged['b2c'])
    b2b_count = len(triaged['b2b'])
    skip_count = len(triaged['skip'])
    
    print(f"\n📊 Triage Results:")
    print(f"   - B2C (Public): {b2c_count}")
    print(f"   - B2B (Doctors): {b2b_count}")
    print(f"   - Skipped: {skip_count}")
    
    if b2c_count == 0 and b2b_count == 0:
        print("\n⚠️  No articles classified for content generation.")
        return
    
    # Save triaged articles
    if args.save:
        save_json(triaged, f'triaged_{date_str}.json', args.output_dir)
    
    # =========================================================================
    # STEP 3: Generate Content
    # =========================================================================
    print("\n✍️  STEP 3: CONTENT GENERATION")
    print("=" * 60)
    
    triaged = generate_all_content(triaged)
    
    # Count successful generations
    b2c_generated = sum(1 for a in triaged['b2c'] if a.get('generated_content'))
    b2b_generated = sum(1 for a in triaged['b2b'] if a.get('generated_content'))
    
    print(f"\n📊 Generation Results:")
    print(f"   - B2C: {b2c_generated}/{b2c_count} articles")
    print(f"   - B2B: {b2b_generated}/{b2b_count} articles")
    
    # Save generated content
    if args.save:
        save_json(triaged, f'generated_{date_str}.json', args.output_dir)
    
    # =========================================================================
    # STEP 4: Deliver Content
    # =========================================================================
    print("\n📤 STEP 4: DELIVERY")
    print("=" * 60)
    
    # Save Markdown digest (for Obsidian)
    markdown_path = None
    publish_to_notion = should_publish_to_notion(args.notion)
    if args.markdown or publish_to_notion:
        markdown_path = save_markdown_digest(triaged, args.output_dir)
        if args.markdown:
            print(f"\n  📝 Markdown saved: {markdown_path}")

    # Publish to Notion
    if publish_to_notion and markdown_path:
        try:
            from scripts.notion_publisher import publish_to_notion

            with open(markdown_path, "r", encoding="utf-8") as handle:
                markdown_content = handle.read()

            page_url = publish_to_notion(
                title=args.notion_title or f"Medical Digest {date_str}",
                content=markdown_content,
                platform=args.notion_platform or "Newsletter",
                status=args.notion_status or "Draft",
                tags=parse_tags(args.notion_tags),
                output_type="Digest",
                source_pipeline="journal-fetch",
                word_count=len(markdown_content.split()),
                local_path=markdown_path,
            )
            print(f"\n  📝 Notion published: {page_url}")
        except Exception as e:
            print(f"\n  ⚠️  Notion publish failed: {e}")
    
    # Send email
    if not args.no_email:
        send_digest_email(triaged)
    else:
        print("\n  ⏭️  Email skipped (--no-email)")
    
    # Send Slack notification
    if not args.no_slack:
        send_digest_notification(triaged)
    else:
        print("\n  ⏭️  Slack skipped (--no-slack)")
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Articles fetched: {len(all_articles)}")
    print(f"   - B2C content generated: {b2c_generated}")
    print(f"   - B2B content generated: {b2b_generated}")
    print(f"   - Duration: {duration:.1f} seconds")
    print(f"\n🕐 Completed at: {end_time.strftime('%H:%M:%S')}")
    print("=" * 60 + "\n")


def main():
    """Main entry point."""
    args = parse_args()
    
    try:
        run_pipeline(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
