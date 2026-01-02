#!/usr/bin/env python3
"""
Research Engine Integration - Bridge between research-engine and content pipelines.

This module provides a unified API for accessing research-engine outputs
and integrating them with other skills and pipelines.

Features:
- Load content gaps from gap_finder
- Load demand signals for topic prioritization
- Load view predictions for content scoring
- Export research findings to Content-OS orchestrator
- Trigger research pipeline from other skills

Usage:
    from research_integration import ResearchIntegration

    research = ResearchIntegration()
    gaps = research.get_content_gaps(min_score=5)
    signals = research.get_demand_signals("statins")
    topics = research.suggest_topics(count=10)
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RESEARCH_ENGINE_DIR = PROJECT_ROOT / "research-engine"
RESEARCH_DATA_DIR = RESEARCH_ENGINE_DIR / "data"
RESEARCH_OUTPUT_DIR = RESEARCH_ENGINE_DIR / "output"
SCRAPED_DIR = RESEARCH_DATA_DIR / "scraped"


@dataclass
class ContentGap:
    """A content gap identified by the research engine."""
    topic: str
    category: str
    gap_score: float
    reason: str
    competition_coverage: str = "low"
    demand_signal: Optional[str] = None
    suggested_angle: Optional[str] = None
    priority: str = "medium"


@dataclass
class DemandSignal:
    """A demand signal from audience research."""
    topic: str
    signal_type: str  # question, comment, search
    source: str
    frequency: int = 1
    sentiment: str = "neutral"
    example_text: Optional[str] = None


@dataclass
class TopicSuggestion:
    """A suggested topic for content creation."""
    topic: str
    score: float
    sources: List[str] = field(default_factory=list)
    gaps: List[ContentGap] = field(default_factory=list)
    signals: List[DemandSignal] = field(default_factory=list)
    suggested_formats: List[str] = field(default_factory=list)


class ResearchIntegration:
    """Integration layer for research-engine data."""

    def __init__(self, auto_load: bool = True):
        """
        Initialize research integration.

        Args:
            auto_load: Whether to automatically load available data
        """
        self.gaps: List[ContentGap] = []
        self.signals: List[DemandSignal] = []
        self.videos: List[Dict] = []
        self.seed_ideas: List[Dict] = []
        self.channels: Dict = {}

        if auto_load:
            self._load_available_data()

    def _load_available_data(self):
        """Load all available research data."""
        self._load_gaps()
        self._load_seed_ideas()
        self._load_channels()
        self._load_scraped_videos()

    def _load_gaps(self):
        """Load content gaps from gap_finder output."""
        gaps_file = RESEARCH_OUTPUT_DIR / "content_gaps.json"
        if not gaps_file.exists():
            return

        try:
            with open(gaps_file, "r") as f:
                data = json.load(f)

            for gap_data in data.get("gaps", []):
                gap = ContentGap(
                    topic=gap_data.get("topic", ""),
                    category=gap_data.get("category", "general"),
                    gap_score=gap_data.get("score", 0),
                    reason=gap_data.get("reason", ""),
                    competition_coverage=gap_data.get("coverage", "low"),
                    demand_signal=gap_data.get("demand_signal"),
                    suggested_angle=gap_data.get("angle"),
                    priority=self._score_to_priority(gap_data.get("score", 0))
                )
                self.gaps.append(gap)
        except Exception as e:
            print(f"Warning: Could not load gaps: {e}")

    def _load_seed_ideas(self):
        """Load seed ideas from research data."""
        seed_file = RESEARCH_DATA_DIR / "seed-ideas.json"
        if seed_file.exists():
            try:
                with open(seed_file, "r") as f:
                    self.seed_ideas = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load seed ideas: {e}")

    def _load_channels(self):
        """Load target channels config."""
        channels_file = RESEARCH_DATA_DIR / "target_channels.json"
        if channels_file.exists():
            try:
                with open(channels_file, "r") as f:
                    self.channels = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load channels: {e}")

    def _load_scraped_videos(self):
        """Load latest scraped videos."""
        latest_file = SCRAPED_DIR / "latest_scrape.json"
        if not latest_file.exists():
            return

        try:
            with open(latest_file, "r") as f:
                meta = json.load(f)

            videos_file = Path(meta.get("file", ""))
            if videos_file.exists():
                with open(videos_file, "r") as f:
                    self.videos = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load videos: {e}")

    def _score_to_priority(self, score: float) -> str:
        """Convert gap score to priority level."""
        if score >= 8:
            return "high"
        elif score >= 5:
            return "medium"
        else:
            return "low"

    def get_content_gaps(self, min_score: float = 0,
                        category: Optional[str] = None,
                        priority: Optional[str] = None,
                        limit: int = 50) -> List[ContentGap]:
        """
        Get content gaps matching criteria.

        Args:
            min_score: Minimum gap score
            category: Filter by category
            priority: Filter by priority (high/medium/low)
            limit: Maximum gaps to return

        Returns:
            List of ContentGap objects
        """
        filtered = []

        for gap in self.gaps:
            if gap.gap_score < min_score:
                continue
            if category and gap.category.lower() != category.lower():
                continue
            if priority and gap.priority != priority:
                continue
            filtered.append(gap)

        # Sort by score descending
        filtered.sort(key=lambda x: x.gap_score, reverse=True)
        return filtered[:limit]

    def get_demand_signals(self, topic: str = None,
                          signal_type: str = None) -> List[DemandSignal]:
        """
        Get demand signals, optionally filtered by topic.

        Args:
            topic: Filter by topic (partial match)
            signal_type: Filter by signal type

        Returns:
            List of DemandSignal objects
        """
        # Load from demand analysis output
        signals_file = RESEARCH_OUTPUT_DIR / "demand_analysis.json"
        if not signals_file.exists():
            return []

        try:
            with open(signals_file, "r") as f:
                data = json.load(f)

            signals = []
            for signal_data in data.get("signals", []):
                signal = DemandSignal(
                    topic=signal_data.get("topic", ""),
                    signal_type=signal_data.get("type", "question"),
                    source=signal_data.get("source", ""),
                    frequency=signal_data.get("count", 1),
                    sentiment=signal_data.get("sentiment", "neutral"),
                    example_text=signal_data.get("example")
                )

                # Filter
                if topic and topic.lower() not in signal.topic.lower():
                    continue
                if signal_type and signal.signal_type != signal_type:
                    continue

                signals.append(signal)

            return signals

        except Exception as e:
            print(f"Warning: Could not load demand signals: {e}")
            return []

    def suggest_topics(self, count: int = 10,
                      categories: List[str] = None) -> List[TopicSuggestion]:
        """
        Suggest topics based on gaps, demand signals, and seed ideas.

        Args:
            count: Number of topics to suggest
            categories: Filter by categories

        Returns:
            List of TopicSuggestion objects
        """
        suggestions = []

        # Get high-priority gaps
        high_gaps = self.get_content_gaps(min_score=6, limit=count * 2)

        for gap in high_gaps:
            if categories and gap.category not in categories:
                continue

            suggestion = TopicSuggestion(
                topic=gap.topic,
                score=gap.gap_score,
                sources=["gap_finder"],
                gaps=[gap],
                suggested_formats=self._suggest_formats(gap)
            )
            suggestions.append(suggestion)

        # Add from seed ideas if needed
        if len(suggestions) < count and self.seed_ideas:
            for seed in self.seed_ideas:
                if len(suggestions) >= count:
                    break

                # Check if already in suggestions
                topic = seed.get("topic", "")
                if any(s.topic.lower() == topic.lower() for s in suggestions):
                    continue

                suggestion = TopicSuggestion(
                    topic=topic,
                    score=seed.get("priority", 5),
                    sources=["seed_ideas"],
                    suggested_formats=seed.get("formats", ["youtube", "carousel"])
                )
                suggestions.append(suggestion)

        # Sort by score
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:count]

    def _suggest_formats(self, gap: ContentGap) -> List[str]:
        """Suggest content formats based on gap characteristics."""
        formats = []

        # Always suggest these for high-score gaps
        if gap.gap_score >= 7:
            formats.extend(["youtube", "newsletter", "carousel"])

        # Myth-busting topics → carousels work well
        if "myth" in gap.topic.lower() or "debunk" in gap.reason.lower():
            if "carousel" not in formats:
                formats.append("carousel")

        # Data-heavy topics → infographics
        if "data" in gap.topic.lower() or "statistic" in gap.reason.lower():
            formats.append("infographic")

        # Questions → short-form
        if gap.demand_signal and "question" in gap.demand_signal:
            formats.extend(["tweet", "thread"])

        return formats if formats else ["youtube", "carousel"]

    def get_competitor_topics(self, channel_type: str = "competition") -> List[str]:
        """
        Get topics covered by competitor channels.

        Args:
            channel_type: Type of channels (competition, inspiration, belief_seeder)

        Returns:
            List of topics
        """
        topics = set()

        for video in self.videos:
            channel = video.get("channel", {})
            if channel.get("type", "") == channel_type:
                title = video.get("title", "")
                topics.add(title)

        return list(topics)

    def get_belief_seeder_narratives(self) -> Dict[str, List[str]]:
        """
        Get dangerous narratives from belief-seeder channels.

        Returns:
            Dict mapping narrative type to list of video titles
        """
        narratives = self.channels.get("narrative_types", {})
        seeder_videos = {}

        for narrative_type, description in narratives.items():
            seeder_videos[narrative_type] = []

        # Match videos to narrative types (simplified)
        for video in self.videos:
            channel = video.get("channel", {})
            if channel.get("type") == "belief_seeder":
                title = video.get("title", "").lower()

                # Simple keyword matching
                if "statin" in title:
                    seeder_videos.get("statin_fear", []).append(video.get("title"))
                if "ldl" in title or "cholesterol" in title:
                    seeder_videos.get("ldl_skepticism", []).append(video.get("title"))
                if "fasting" in title:
                    seeder_videos.get("fasting_absolutism", []).append(video.get("title"))

        return seeder_videos

    def run_research_pipeline(self, quick: bool = True) -> bool:
        """
        Trigger the research-engine pipeline.

        Args:
            quick: Use quick mode (fewer videos)

        Returns:
            True if successful
        """
        pipeline_script = RESEARCH_ENGINE_DIR / "run_pipeline.py"
        if not pipeline_script.exists():
            print("Error: run_pipeline.py not found")
            return False

        cmd = [sys.executable, str(pipeline_script)]
        if quick:
            cmd.append("--quick")

        try:
            result = subprocess.run(cmd, cwd=str(RESEARCH_ENGINE_DIR))
            return result.returncode == 0
        except Exception as e:
            print(f"Error running pipeline: {e}")
            return False

    def export_for_content_os(self, output_path: Optional[Path] = None) -> Path:
        """
        Export research findings for Content-OS orchestrator.

        Args:
            output_path: Custom output path

        Returns:
            Path to exported file
        """
        output_path = output_path or (RESEARCH_OUTPUT_DIR / "content_os_research.json")

        export_data = {
            "generated_at": datetime.now().isoformat(),
            "gaps": [
                {
                    "topic": g.topic,
                    "category": g.category,
                    "score": g.gap_score,
                    "reason": g.reason,
                    "priority": g.priority,
                    "suggested_formats": self._suggest_formats(g)
                }
                for g in self.get_content_gaps(min_score=5, limit=20)
            ],
            "suggested_topics": [
                {
                    "topic": s.topic,
                    "score": s.score,
                    "sources": s.sources,
                    "formats": s.suggested_formats
                }
                for s in self.suggest_topics(count=15)
            ],
            "belief_seeder_narratives": self.get_belief_seeder_narratives(),
            "seed_ideas_count": len(self.seed_ideas),
            "videos_scraped": len(self.videos)
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)

        return output_path

    def get_topics_for_pipeline(self, pipeline: str,
                               count: int = 10) -> List[str]:
        """
        Get suggested topics for a specific pipeline.

        Args:
            pipeline: Pipeline name (twitter-content, carousel, youtube)
            count: Number of topics

        Returns:
            List of topic strings
        """
        format_map = {
            "twitter-content": ["tweet", "thread"],
            "carousel": ["carousel", "infographic"],
            "youtube": ["youtube", "video"],
            "newsletter": ["newsletter", "blog"]
        }

        target_formats = format_map.get(pipeline, [])

        suggestions = self.suggest_topics(count=count * 2)

        # Filter by formats
        matching = []
        for s in suggestions:
            if any(f in target_formats for f in s.suggested_formats):
                matching.append(s.topic)
                if len(matching) >= count:
                    break

        return matching


def main():
    """CLI for research integration."""
    import argparse

    parser = argparse.ArgumentParser(description="Research Engine Integration")
    parser.add_argument("--gaps", action="store_true", help="Show content gaps")
    parser.add_argument("--topics", action="store_true", help="Suggest topics")
    parser.add_argument("--export", action="store_true", help="Export for Content-OS")
    parser.add_argument("--run-pipeline", action="store_true", help="Run research pipeline")
    parser.add_argument("--quick", action="store_true", help="Quick mode for pipeline")
    parser.add_argument("--count", type=int, default=10, help="Number of items")
    parser.add_argument("--min-score", type=float, default=5, help="Minimum gap score")

    args = parser.parse_args()

    research = ResearchIntegration()

    if args.run_pipeline:
        print("Running research pipeline...")
        success = research.run_research_pipeline(quick=args.quick)
        print(f"Pipeline {'completed' if success else 'failed'}")
        return

    if args.gaps:
        print(f"\nContent Gaps (min_score={args.min_score}):\n")
        gaps = research.get_content_gaps(min_score=args.min_score, limit=args.count)
        for i, gap in enumerate(gaps, 1):
            print(f"{i}. [{gap.priority.upper()}] {gap.topic}")
            print(f"   Score: {gap.gap_score}, Category: {gap.category}")
            print(f"   Reason: {gap.reason[:60]}...")
            print()

    if args.topics:
        print(f"\nSuggested Topics:\n")
        topics = research.suggest_topics(count=args.count)
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic.topic} (score: {topic.score})")
            print(f"   Formats: {', '.join(topic.suggested_formats)}")
            print()

    if args.export:
        path = research.export_for_content_os()
        print(f"Exported to: {path}")


if __name__ == "__main__":
    main()
