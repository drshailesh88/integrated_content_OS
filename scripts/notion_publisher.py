#!/usr/bin/env python3
"""
Publish content to a Notion database.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Iterable, List, Optional

import requests
from dotenv import load_dotenv


NOTION_VERSION = "2022-06-28"
NOTION_API_BASE = "https://api.notion.com/v1"
MAX_RICH_TEXT_CHARS = 1800
MAX_BLOCKS_PER_REQUEST = 100


class NotionPublishError(RuntimeError):
    """Raised when a Notion publish request fails."""


def normalize_notion_id(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    candidate = value.strip()
    if candidate.startswith("http"):
        candidate = candidate.split("?")[0].split("/")[-1]
    candidate = candidate.replace("-", "")
    match = re.search(r"[0-9a-fA-F]{32}", candidate)
    if not match:
        return value.strip()
    raw = match.group(0)
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"


def notion_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def chunk_text(text: str, size: int = MAX_RICH_TEXT_CHARS) -> List[str]:
    if text is None:
        return []
    text = str(text)
    if not text:
        return []
    return [text[i:i + size] for i in range(0, len(text), size)]


def rich_text(text: Optional[str]) -> list:
    if text is None:
        return []
    return [{"type": "text", "text": {"content": chunk}} for chunk in chunk_text(text)]


def make_text_block(block_type: str, text: str) -> dict:
    return {"type": block_type, block_type: {"rich_text": rich_text(text)}}


def make_code_block(code: str) -> dict:
    return {"type": "code", "code": {"rich_text": rich_text(code), "language": "plain text"}}


def markdown_to_blocks(markdown: str) -> list:
    if not markdown:
        return []

    blocks = []
    in_code_block = False
    code_lines: List[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code_block:
                blocks.append(make_code_block("\n".join(code_lines)))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        if not stripped:
            continue

        if stripped in ("---", "***", "___"):
            blocks.append({"type": "divider", "divider": {}})
            continue

        if stripped.startswith("### "):
            blocks.append(make_text_block("heading_3", stripped[4:]))
            continue
        if stripped.startswith("## "):
            blocks.append(make_text_block("heading_2", stripped[3:]))
            continue
        if stripped.startswith("# "):
            blocks.append(make_text_block("heading_1", stripped[2:]))
            continue
        if stripped.startswith("> "):
            blocks.append(make_text_block("quote", stripped[2:]))
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append(make_text_block("bulleted_list_item", stripped[2:]))
            continue

        match = re.match(r"^\d+\.\s+(.*)", stripped)
        if match:
            blocks.append(make_text_block("numbered_list_item", match.group(1)))
            continue

        blocks.append(make_text_block("paragraph", stripped))

    if in_code_block and code_lines:
        blocks.append(make_code_block("\n".join(code_lines)))

    return blocks


def append_blocks(token: str, page_id: str, blocks: list) -> None:
    headers = notion_headers(token)
    for i in range(0, len(blocks), MAX_BLOCKS_PER_REQUEST):
        payload = {"children": blocks[i:i + MAX_BLOCKS_PER_REQUEST]}
        response = requests.patch(
            f"{NOTION_API_BASE}/blocks/{page_id}/children",
            headers=headers,
            json=payload,
            timeout=30,
        )
        if not response.ok:
            raise NotionPublishError(f"Append failed: {response.status_code} {response.text}")


def create_page(
    token: str,
    database_id: str,
    properties: dict,
    blocks: list,
) -> dict:
    headers = notion_headers(token)
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }

    if blocks:
        payload["children"] = blocks[:MAX_BLOCKS_PER_REQUEST]

    response = requests.post(
        f"{NOTION_API_BASE}/pages",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not response.ok:
        raise NotionPublishError(f"Create failed: {response.status_code} {response.text}")

    page = response.json()
    if blocks and len(blocks) > MAX_BLOCKS_PER_REQUEST:
        append_blocks(token, page["id"], blocks[MAX_BLOCKS_PER_REQUEST:])

    return page


def build_properties(
    title: str,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[Iterable[str]] = None,
    output_type: Optional[str] = None,
    source_pipeline: Optional[str] = None,
    word_count: Optional[int] = None,
    date: Optional[str] = None,
    local_path: Optional[str] = None,
    citations: Optional[str] = None,
    research_question: Optional[str] = None,
) -> dict:
    properties = {"Title": {"title": rich_text(title)}}

    if platform:
        properties["Platform"] = {"select": {"name": platform}}
    if status:
        properties["Status"] = {"select": {"name": status}}
    if output_type:
        properties["Output Type"] = {"select": {"name": output_type}}
    if source_pipeline:
        properties["Source Pipeline"] = {"select": {"name": source_pipeline}}
    if date:
        properties["Date"] = {"date": {"start": date}}
    if word_count is not None:
        properties["Word Count"] = {"number": word_count}
    if local_path:
        properties["Local Path"] = {"rich_text": rich_text(local_path)}
    if citations:
        properties["Citations"] = {"rich_text": rich_text(citations)}
    if research_question:
        properties["Research Question"] = {"rich_text": rich_text(research_question)}

    if tags:
        clean_tags = [tag.strip() for tag in tags if tag and tag.strip()]
        if clean_tags:
            properties["Tags"] = {"multi_select": [{"name": tag} for tag in clean_tags]}

    return properties


def extract_title_from_markdown(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return fallback


def parse_tags(tag_string: Optional[str]) -> List[str]:
    if not tag_string:
        return []
    return [tag.strip() for tag in tag_string.split(",") if tag.strip()]


def log_push(entry: dict, log_path: str = "output/notion_push_log.jsonl") -> None:
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def send_notification_email(to_email: str, subject: str, body: str) -> bool:
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_user or not gmail_password:
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        return True
    except smtplib.SMTPException:
        return False


def publish_to_notion(
    title: str,
    content: str,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[Iterable[str]] = None,
    output_type: Optional[str] = None,
    source_pipeline: Optional[str] = None,
    word_count: Optional[int] = None,
    local_path: Optional[str] = None,
    citations: Optional[Iterable[str]] = None,
    research_question: Optional[str] = None,
    date: Optional[str] = None,
    database_id: Optional[str] = None,
    dry_run: bool = False,
) -> str:
    load_dotenv()

    token = os.getenv("NOTION_API_KEY")
    database_id = normalize_notion_id(database_id or os.getenv("NOTION_DATABASE_ID"))

    if not token or not database_id:
        raise NotionPublishError("Missing NOTION_API_KEY or NOTION_DATABASE_ID")

    platform = platform or os.getenv("NOTION_DEFAULT_PLATFORM")
    status = status or os.getenv("NOTION_DEFAULT_STATUS")
    output_type = output_type or os.getenv("NOTION_DEFAULT_OUTPUT_TYPE")
    source_pipeline = source_pipeline or os.getenv("NOTION_DEFAULT_SOURCE_PIPELINE")
    date = date or datetime.now().date().isoformat()

    citation_text = None
    if citations:
        citation_text = "\n".join([str(cite) for cite in citations if cite])

    properties = build_properties(
        title=title,
        platform=platform,
        status=status,
        tags=tags,
        output_type=output_type,
        source_pipeline=source_pipeline,
        word_count=word_count,
        date=date,
        local_path=local_path,
        citations=citation_text,
        research_question=research_question,
    )

    blocks = markdown_to_blocks(content)

    if dry_run:
        return "dry-run"

    page = create_page(token, database_id, properties, blocks)
    page_url = page.get("url", "")

    log_push(
        {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "title": title,
            "page_id": page.get("id"),
            "page_url": page_url,
            "platform": platform,
            "status": status,
            "output_type": output_type,
            "source_pipeline": source_pipeline,
            "local_path": local_path,
        }
    )

    notify_email = os.getenv("NOTION_NOTIFY_EMAIL")
    if notify_email:
        send_notification_email(
            notify_email,
            f"Notion publish: {title}",
            f"Title: {title}\nURL: {page_url}\nSource: {source_pipeline or 'unknown'}\n",
        )

    return page_url


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish content to a Notion database")
    parser.add_argument("--title", help="Title for the Notion page")
    parser.add_argument("--content", help="Content to publish (plain text/markdown)")
    parser.add_argument("--file", help="Read content from a markdown file")
    parser.add_argument("--platform", help="Platform label (e.g., Twitter/X)")
    parser.add_argument("--status", help="Status (Draft/Final/Published)")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--output-type", help="Output type (thread, script, digest, etc.)")
    parser.add_argument("--source", help="Source pipeline identifier")
    parser.add_argument("--local-path", help="Local file path to store in Notion")
    parser.add_argument("--word-count", type=int, help="Override word count")
    parser.add_argument("--date", help="ISO date for the entry (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without publishing")

    args = parser.parse_args()

    content = args.content
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            content = handle.read()

    if not content:
        raise SystemExit("Provide --content or --file")

    title = args.title or extract_title_from_markdown(content, fallback="Untitled")
    tags = parse_tags(args.tags)
    word_count = args.word_count if args.word_count is not None else len(content.split())

    page_url = publish_to_notion(
        title=title,
        content=content,
        platform=args.platform,
        status=args.status,
        tags=tags,
        output_type=args.output_type,
        source_pipeline=args.source,
        word_count=word_count,
        local_path=args.local_path,
        date=args.date,
        dry_run=args.dry_run,
    )

    print(f"Published: {page_url}")


if __name__ == "__main__":
    main()
