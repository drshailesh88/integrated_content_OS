#!/usr/bin/env python3
"""
Create a Notion database for content publishing.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import requests
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from notion_publisher import normalize_notion_id, notion_headers, NotionPublishError


def database_properties() -> dict:
    return {
        "Title": {"title": {}},
        "Platform": {
            "select": {
                "options": [
                    {"name": "Twitter/X"},
                    {"name": "Newsletter"},
                    {"name": "YouTube"},
                    {"name": "Editorial"},
                    {"name": "Email"},
                    {"name": "Blog"},
                    {"name": "Book"},
                    {"name": "LinkedIn"},
                    {"name": "Other"},
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Draft"},
                    {"name": "Final"},
                    {"name": "Published"},
                ]
            }
        },
        "Tags": {"multi_select": {"options": []}},
        "Output Type": {
            "select": {
                "options": [
                    {"name": "Tweet"},
                    {"name": "Thread"},
                    {"name": "Long Post"},
                    {"name": "Newsletter"},
                    {"name": "Script"},
                    {"name": "Editorial"},
                    {"name": "Digest"},
                    {"name": "Research Note"},
                    {"name": "Other"},
                ]
            }
        },
        "Source Pipeline": {
            "select": {
                "options": [
                    {"name": "twitter-content"},
                    {"name": "journal-fetch"},
                    {"name": "research-engine"},
                    {"name": "rag-pipeline"},
                    {"name": "manual"},
                ]
            }
        },
        "Date": {"date": {}},
        "Word Count": {"number": {"format": "number"}},
        "Local Path": {"rich_text": {}},
        "Citations": {"rich_text": {}},
        "Research Question": {"rich_text": {}},
    }


def create_database(token: str, parent_id: str, title: str) -> dict:
    payload = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": database_properties(),
    }

    response = requests.post(
        "https://api.notion.com/v1/databases",
        headers=notion_headers(token),
        json=payload,
        timeout=30,
    )
    if not response.ok:
        raise NotionPublishError(f"Create database failed: {response.status_code} {response.text}")

    return response.json()


def resolve_parent_id(parent_arg: Optional[str]) -> str:
    if parent_arg:
        return normalize_notion_id(parent_arg)
    env_parent = os.getenv("NOTION_PARENT_PAGE_ID") or os.getenv("NOTION_PARENT_PAGE_URL")
    return normalize_notion_id(env_parent)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Notion database for content output")
    parser.add_argument("--parent", help="Parent page ID or URL where the database will live")
    parser.add_argument("--title", default="Content Library", help="Database title")
    parser.add_argument("--dry-run", action="store_true", help="Validate without creating")
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv("NOTION_API_KEY")
    if not token:
        raise SystemExit("Missing NOTION_API_KEY in .env")

    parent_id = resolve_parent_id(args.parent)
    if not parent_id:
        raise SystemExit("Missing parent page ID. Provide --parent or set NOTION_PARENT_PAGE_ID.")

    if args.dry_run:
        print("Dry run OK. Parent page ID resolved.")
        return

    database = create_database(token, parent_id, args.title)
    print("Database created.")
    print(f"Database ID: {database.get('id')}")
    print(f"Database URL: {database.get('url')}")
    print("Add NOTION_DATABASE_ID to your .env file.")


if __name__ == "__main__":
    main()
