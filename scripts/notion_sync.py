#!/usr/bin/env python3
"""
Sync local output files to the Notion Content Library.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable, List, Optional, Set

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT_DIR / "output" / "notion_push_log.jsonl"
DEFAULT_EXTENSIONS = {".md", ".markdown", ".txt", ".json"}
DEFAULT_PATHS = [
    ROOT_DIR / "output",
    ROOT_DIR / "research-engine" / "output",
    ROOT_DIR / "research-engine" / "content-calendar",
    ROOT_DIR / "research-engine" / "data" / "scraped",
]


def normalize_local_path(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return str(candidate.relative_to(ROOT_DIR))
        except ValueError:
            return str(candidate)
    return str(candidate)


def load_published_paths(log_path: Path) -> Set[str]:
    published: Set[str] = set()
    if not log_path.exists():
        return published
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            local_path = normalize_local_path(entry.get("local_path"))
            if local_path:
                published.add(local_path)
    return published


def iter_files(paths: Iterable[Path], extensions: Set[str]) -> List[Path]:
    files: List[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            if path.suffix.lower() in extensions:
                files.append(path)
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file():
                continue
            if candidate.name == "notion_push_log.jsonl":
                continue
            if candidate.suffix.lower() in extensions:
                files.append(candidate)
    return files


def detect_source_pipeline(path: Path) -> str:
    path_str = str(path).lower()
    if "twitter-content" in path_str:
        return "twitter-content"
    if "journal-fetch" in path_str or "digests" in path_str:
        return "journal-fetch"
    if "rag-pipeline" in path_str:
        return "rag-pipeline"
    if "research-engine" in path_str:
        return "research-engine"
    return "manual"


def detect_output_type(path: Path) -> str:
    name = path.name.lower()
    if "digest" in name:
        return "Digest"
    if "calendar" in name:
        return "Research Note"
    if path.suffix.lower() == ".json":
        return "Research Note"
    return "Other"


def file_to_content(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".json":
        return f"```json\n{text}\n```"
    return text


def resolve_paths(paths: Optional[List[str]]) -> List[Path]:
    if not paths:
        return DEFAULT_PATHS
    resolved = []
    for raw in paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = ROOT_DIR / candidate
        resolved.append(candidate)
    return resolved


def should_auto_publish(force: bool) -> bool:
    if force:
        return True
    return os.getenv("NOTION_AUTO_PUBLISH", "").lower() in {"1", "true", "yes"}


def parse_tags(tag_string: Optional[str]) -> List[str]:
    if not tag_string:
        return []
    return [tag.strip() for tag in tag_string.split(",") if tag.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync output files to Notion")
    parser.add_argument("--path", action="append", help="File or directory to sync (repeatable)")
    parser.add_argument("--ext", action="append", help="File extension to include (repeatable)")
    parser.add_argument("--status", default=None, help="Notion status (Draft/Final/Published)")
    parser.add_argument("--platform", default=None, help="Notion platform label")
    parser.add_argument("--tags", default=None, help="Comma-separated tags")
    parser.add_argument("--force", action="store_true", help="Publish even if auto publish is disabled")
    parser.add_argument("--dry-run", action="store_true", help="List files without publishing")
    args = parser.parse_args()

    load_dotenv()

    if not should_auto_publish(args.force):
        print("Notion auto-publish disabled. Set NOTION_AUTO_PUBLISH=1 or use --force.")
        return

    extensions = DEFAULT_EXTENSIONS.copy()
    if args.ext:
        extensions = {ext if ext.startswith(".") else f".{ext}" for ext in args.ext}

    target_paths = resolve_paths(args.path)
    files = iter_files(target_paths, extensions)
    if not files:
        print("No matching files found.")
        return

    published_paths = load_published_paths(LOG_PATH)
    tags = parse_tags(args.tags)
    max_kb = None
    if os.getenv("NOTION_MAX_FILE_KB"):
        try:
            max_kb = int(os.getenv("NOTION_MAX_FILE_KB"))
        except ValueError:
            max_kb = None

    try:
        from scripts.notion_publisher import publish_to_notion, extract_title_from_markdown
    except Exception:
        import sys

        sys.path.insert(0, str(ROOT_DIR))
        from scripts.notion_publisher import publish_to_notion, extract_title_from_markdown

    for path in files:
        relative_path = normalize_local_path(path)
        if relative_path in published_paths:
            continue

        if max_kb is not None:
            size_kb = int(path.stat().st_size / 1024)
            if size_kb > max_kb:
                print(f"Skipping {relative_path} ({size_kb} KB > {max_kb} KB limit)")
                continue

        content = file_to_content(path)
        title = extract_title_from_markdown(content, fallback=path.stem)
        output_type = detect_output_type(path)
        source_pipeline = detect_source_pipeline(path)
        platform = args.platform or os.getenv("NOTION_DEFAULT_PLATFORM") or "Other"
        status = args.status or os.getenv("NOTION_DEFAULT_STATUS") or "Draft"

        if args.dry_run:
            print(f"[DRY RUN] {relative_path}")
            continue

        try:
            publish_to_notion(
                title=title,
                content=content,
                platform=platform,
                status=status,
                tags=tags,
                output_type=output_type,
                source_pipeline=source_pipeline,
                word_count=len(content.split()),
                local_path=relative_path,
            )
        except Exception as exc:
            print(f"Notion publish failed for {relative_path}: {exc}")


if __name__ == "__main__":
    main()
