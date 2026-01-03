#!/usr/bin/env python3
"""
Simple Notion publisher for Claude Code workflow.
Usage: python publish.py "Title" "Content" --platform "Twitter/X"
"""

import argparse
import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from notion_publisher import publish_to_notion, NotionPublishError


def main():
    parser = argparse.ArgumentParser(
        description="Publish content to Notion from Claude Code"
    )
    parser.add_argument("title", help="Content title")
    parser.add_argument("content", help="Content body (markdown supported)")
    parser.add_argument("--platform", default="Multi-Platform", help="Platform (Twitter/X, YouTube, Newsletter, etc.)")
    parser.add_argument("--status", default="Draft", help="Status (Draft, Final, Published)")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--type", dest="output_type", help="Output type (thread, script, newsletter, etc.)")

    args = parser.parse_args()

    # Parse tags
    tags = []
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    # Word count
    word_count = len(args.content.split())

    print(f"\n📤 Publishing to Notion...")
    print(f"   Title: {args.title}")
    print(f"   Platform: {args.platform}")
    print(f"   Words: {word_count}")
    print(f"   Tags: {', '.join(tags) if tags else 'None'}")
    print()

    try:
        page_url = publish_to_notion(
            title=args.title,
            content=args.content,
            platform=args.platform,
            status=args.status,
            tags=tags,
            output_type=args.output_type,
            word_count=word_count,
            source_pipeline="claude-code"
        )

        print(f"✅ SUCCESS! Published to Notion")
        print(f"🔗 {page_url}")
        print(f"\n📱 Check your Notion mobile app!")

        # Check if email notification was configured
        if os.getenv("NOTION_NOTIFY_EMAIL"):
            print(f"📧 Email sent to {os.getenv('NOTION_NOTIFY_EMAIL')}")
        else:
            print(f"💡 Tip: Set NOTION_NOTIFY_EMAIL in .env for mobile notifications")

        return 0

    except NotionPublishError as e:
        print(f"\n❌ FAILED: {e}")
        print()
        print("🔧 Setup required:")
        print("   1. Get Notion API key: https://www.notion.so/my-integrations")
        print("   2. Create a Notion database")
        print("   3. Add to .env file:")
        print("      NOTION_API_KEY=your_key")
        print("      NOTION_DATABASE_ID=your_database_id")
        print("      NOTION_NOTIFY_EMAIL=your_email@gmail.com")
        return 1


if __name__ == "__main__":
    sys.exit(main())
