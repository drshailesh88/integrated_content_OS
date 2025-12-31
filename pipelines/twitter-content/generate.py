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

    args = parser.parse_args()

    from src.pipeline import create_pipeline
    from src.writer import ContentFormat

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
    else:
        print('Failed to generate content')
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
