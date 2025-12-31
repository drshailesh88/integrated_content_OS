#!/usr/bin/env python3
"""
Channel Scraper - Scrape all videos from target YouTube channels
Uses scrapetube (no API key required)

Usage:
    python channel_scraper.py                    # Scrape all channels
    python channel_scraper.py --channel "Peter Attia"  # Scrape specific channel
    python channel_scraper.py --limit 50         # Limit videos per channel
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

try:
    import scrapetube
except ImportError:
    print("Installing scrapetube...")
    os.system("pip install scrapetube")
    import scrapetube

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
CHANNELS_FILE = DATA_DIR / "target_channels.json"


def load_channels():
    """Load target channels configuration."""
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)


def extract_channel_identifier(channel_config):
    """Extract channel ID or URL for scrapetube."""
    if channel_config.get("channel_id"):
        return {"channel_id": channel_config["channel_id"]}
    elif channel_config.get("channel_url"):
        # Extract handle or ID from URL
        url = channel_config["channel_url"]
        if "/@" in url:
            # Handle format: https://www.youtube.com/@ChannelName
            handle = url.split("/@")[1].split("/")[0]
            return {"channel_url": url}
        elif "/channel/" in url:
            channel_id = url.split("/channel/")[1].split("/")[0]
            return {"channel_id": channel_id}
    return None


def scrape_channel(channel_config, limit=100, sleep=2):
    """
    Scrape all videos from a single channel.

    Returns list of video metadata dicts.
    """
    name = channel_config["name"]
    print(f"\n{'='*60}")
    print(f"Scraping: {name}")
    print(f"{'='*60}")

    identifier = extract_channel_identifier(channel_config)
    if not identifier:
        print(f"  ERROR: Could not extract channel identifier for {name}")
        return []

    videos = []
    try:
        # Get videos using scrapetube
        video_generator = scrapetube.get_channel(
            **identifier,
            limit=limit,
            sleep=sleep,
            sort_by="popular"  # Get most popular first for better data
        )

        for i, video in enumerate(video_generator):
            video_data = {
                "video_id": video.get("videoId"),
                "title": video.get("title", {}).get("runs", [{}])[0].get("text", ""),
                "views": parse_view_count(video.get("viewCountText", {}).get("simpleText", "0")),
                "views_raw": video.get("viewCountText", {}).get("simpleText", ""),
                "published": video.get("publishedTimeText", {}).get("simpleText", ""),
                "duration": video.get("lengthText", {}).get("simpleText", ""),
                "duration_seconds": parse_duration(video.get("lengthText", {}).get("simpleText", "")),
                "thumbnail": video.get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", ""),
                "channel_name": name,
                "channel_type": channel_config.get("type", "unknown"),
                "channel_language": channel_config.get("language", "unknown"),
                "channel_niche": channel_config.get("niche", "unknown"),
            }
            videos.append(video_data)

            if (i + 1) % 10 == 0:
                print(f"  Scraped {i + 1} videos...")

        print(f"  Total: {len(videos)} videos scraped")

    except Exception as e:
        print(f"  ERROR scraping {name}: {str(e)}")
        return []

    return videos


def parse_view_count(view_text):
    """Convert '1.2M views' to integer."""
    if not view_text:
        return 0

    view_text = view_text.lower().replace("views", "").replace(",", "").strip()

    try:
        if "m" in view_text:
            return int(float(view_text.replace("m", "")) * 1_000_000)
        elif "k" in view_text:
            return int(float(view_text.replace("k", "")) * 1_000)
        elif "b" in view_text:
            return int(float(view_text.replace("b", "")) * 1_000_000_000)
        else:
            return int(view_text)
    except:
        return 0


def parse_duration(duration_text):
    """Convert '10:30' or '1:10:30' to seconds."""
    if not duration_text:
        return 0

    try:
        parts = duration_text.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    except:
        return 0


def save_results(all_videos, channel_videos):
    """Save scraped data to JSON files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save combined dataset
    combined_file = SCRAPED_DIR / f"all_videos_{timestamp}.json"
    with open(combined_file, "w") as f:
        json.dump(all_videos, f, indent=2)
    print(f"\nSaved {len(all_videos)} total videos to: {combined_file}")

    # Save per-channel files
    for channel_name, videos in channel_videos.items():
        safe_name = channel_name.replace(" ", "_").replace("/", "_")
        channel_file = SCRAPED_DIR / f"channel_{safe_name}_{timestamp}.json"
        with open(channel_file, "w") as f:
            json.dump(videos, f, indent=2)
        print(f"Saved {len(videos)} videos for {channel_name}")

    # Save latest pointer (for easy access)
    latest_file = SCRAPED_DIR / "latest_scrape.json"
    with open(latest_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "total_videos": len(all_videos),
            "channels_scraped": list(channel_videos.keys()),
            "file": str(combined_file)
        }, f, indent=2)

    return combined_file


def main():
    parser = argparse.ArgumentParser(description="Scrape YouTube channels for video data")
    parser.add_argument("--channel", type=str, help="Scrape specific channel by name")
    parser.add_argument("--limit", type=int, default=100, help="Max videos per channel")
    parser.add_argument("--sleep", type=float, default=2, help="Sleep between requests")
    parser.add_argument("--type", type=str, choices=["competition", "inspiration", "all"],
                        default="all", help="Which channel types to scrape")
    args = parser.parse_args()

    # Load channel config
    config = load_channels()

    # Build channel list
    channels_to_scrape = []

    if args.channel:
        # Find specific channel
        for group in ["competition_hindi", "inspiration_english"]:
            for ch in config.get(group, []):
                if args.channel.lower() in ch["name"].lower():
                    channels_to_scrape.append(ch)
    else:
        # Scrape by type
        if args.type in ["competition", "all"]:
            channels_to_scrape.extend(config.get("competition_hindi", []))
        if args.type in ["inspiration", "all"]:
            channels_to_scrape.extend(config.get("inspiration_english", []))

    if not channels_to_scrape:
        print("No channels found to scrape!")
        sys.exit(1)

    print(f"\nWill scrape {len(channels_to_scrape)} channels with limit={args.limit}")
    print(f"Channels: {[ch['name'] for ch in channels_to_scrape]}")

    # Scrape each channel
    all_videos = []
    channel_videos = {}

    for channel in channels_to_scrape:
        videos = scrape_channel(channel, limit=args.limit, sleep=args.sleep)
        all_videos.extend(videos)
        channel_videos[channel["name"]] = videos

    # Save results
    if all_videos:
        save_results(all_videos, channel_videos)

        # Print summary
        print(f"\n{'='*60}")
        print("SCRAPE SUMMARY")
        print(f"{'='*60}")
        print(f"Total videos scraped: {len(all_videos)}")
        print(f"Total views across all videos: {sum(v['views'] for v in all_videos):,}")
        print("\nBy channel:")
        for name, videos in channel_videos.items():
            total_views = sum(v['views'] for v in videos)
            avg_views = total_views // len(videos) if videos else 0
            print(f"  {name}: {len(videos)} videos, {total_views:,} total views, {avg_views:,} avg")
    else:
        print("\nNo videos scraped!")


if __name__ == "__main__":
    main()
