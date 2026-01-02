#!/usr/bin/env python3
"""
Quick content generator - Direct mode (no Twitter scraping needed).

Usage:
    python generate.py "Your research question here"
    python generate.py "Your question" --format tweet
    python generate.py "Your question" --format thread
    python generate.py "Your question" --format long_post
"""

import asyncio
import argparse
import os
import sys

sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()


async def main():
    parser = argparse.ArgumentParser(
        description='Generate evidence-based medical content from a research question'
    )
    parser.add_argument(
        'question',
        help='The research question to explore'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['tweet', 'thread', 'long_post'],
        default='thread',
        help='Output format (default: thread)'
    )
    parser.add_argument(
        '--save', '-s',
        help='Save output to file'
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

    args = parser.parse_args()

    # Import from local modules (not src/ subdirectory)
    try:
        from .pipeline import create_pipeline
        from .writer import ContentFormat
    except ImportError:
        from pipeline import create_pipeline
        from writer import ContentFormat

    format_map = {
        'tweet': ContentFormat.TWEET,
        'thread': ContentFormat.THREAD,
        'long_post': ContentFormat.LONG_POST,
    }

    print()
    print('=' * 60)
    print('MEDICAL CONTENT GENERATOR')
    print('=' * 60)
    print()
    print(f'Question: {args.question}')
    print(f'Format: {args.format}')
    print()

    pipeline = create_pipeline()
    result = await pipeline.process_direct_question(
        question=args.question,
        format=format_map[args.format],
    )

    if result:
        print()
        print('=' * 60)
        print('GENERATED CONTENT')
        print('=' * 60)
        print()
        print(result.content.content)
        print()
        print('-' * 40)
        print(f'Format: {result.content.format.value}')
        print(f'Words: {result.content.word_count}')
        print(f'Sources: {result.research.total_sources}')
        print(f'Citations: {len(result.brief.citations)}')

        if args.save:
            result.save_to_file(args.save)
            print(f'\nSaved to: {args.save}')

        auto_publish = os.getenv("NOTION_AUTO_PUBLISH", "").lower() in {"1", "true", "yes"}
        should_publish = args.notion or auto_publish
        if should_publish:
            try:
                from scripts.notion_publisher import publish_to_notion, parse_tags

                page_url = publish_to_notion(
                    title=args.notion_title or args.question,
                    content=result.content.content,
                    platform=args.notion_platform or "Twitter/X",
                    status=args.notion_status or "Draft",
                    tags=parse_tags(args.notion_tags),
                    output_type=result.content.format.value,
                    source_pipeline="twitter-content",
                    word_count=result.content.word_count,
                    local_path=args.save,
                    citations=result.brief.citations,
                    research_question=args.question,
                )
                print(f'\nNotion published: {page_url}')
            except Exception as e:
                print(f'\nNotion publish failed: {e}')
    else:
        print('Failed to generate content')
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
