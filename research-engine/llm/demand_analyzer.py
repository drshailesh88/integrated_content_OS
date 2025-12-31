#!/usr/bin/env python3
"""
Demand Analyzer

Uses free LLMs via OpenRouter to analyze YouTube comments and extract demand signals.
This preserves Opus context for the actual script writing phase.

Usage:
    from llm.demand_analyzer import DemandAnalyzer

    analyzer = DemandAnalyzer()
    demand_brief = analyzer.analyze_comments(comments)
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.openrouter_client import OpenRouterClient


class DemandAnalyzer:
    """Analyzes YouTube comments to extract demand signals using free LLMs."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.client = OpenRouterClient(verbose=verbose)

        if verbose:
            print("✅ Demand Analyzer initialized")

    def extract_questions(self, comments: List[str]) -> List[Dict[str, Any]]:
        """
        Extract questions and requests from comments.

        Returns list of:
        {
            "question": "the question",
            "topic": "categorized topic",
            "urgency": "high/medium/low",
            "count": approximate frequency
        }
        """
        if not comments:
            return []

        # Batch comments (free LLMs have token limits)
        batch_size = 50
        all_questions = []

        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            comments_text = "\n".join([f"- {c[:300]}" for c in batch])

            prompt = f"""Analyze these YouTube comments from cardiology videos.
Extract the QUESTIONS and REQUESTS people are asking.

COMMENTS:
{comments_text}

Return JSON with this structure:
{{
  "questions": [
    {{
      "question": "What people are asking",
      "topic": "Category (e.g., cholesterol, diet, medications, symptoms, lifestyle)",
      "urgency": "high/medium/low based on emotional language",
      "frequency": "common/occasional/rare"
    }}
  ]
}}

Focus on:
- Direct questions
- Implicit requests ("I wish someone would explain...")
- Confusion signals ("I don't understand...")
- Concerns and fears

Return ONLY valid JSON."""

            response = self.client.complete_json(
                prompt,
                system_prompt="You are a demand analysis expert. Extract audience questions accurately. Return valid JSON only."
            )

            if response and "questions" in response:
                all_questions.extend(response["questions"])

        return all_questions

    def identify_pain_points(self, comments: List[str]) -> List[Dict[str, Any]]:
        """
        Identify emotional pain points and frustrations.

        Returns list of:
        {
            "pain_point": "description",
            "emotion": "fear/frustration/confusion/anxiety",
            "content_opportunity": "how to address this"
        }
        """
        if not comments:
            return []

        # Sample comments to stay within token limits
        sample = comments[:100] if len(comments) > 100 else comments
        comments_text = "\n".join([f"- {c[:200]}" for c in sample])

        prompt = f"""Analyze these YouTube comments for emotional pain points.

COMMENTS:
{comments_text}

Return JSON with this structure:
{{
  "pain_points": [
    {{
      "pain_point": "What's causing distress",
      "emotion": "fear/frustration/confusion/anxiety/anger/hope",
      "example_phrase": "Quote from comments",
      "content_opportunity": "How a video could address this"
    }}
  ]
}}

Look for:
- Fear about health outcomes
- Frustration with conflicting information
- Confusion about medical advice
- Anxiety about symptoms
- Distrust of mainstream medicine
- Hope for alternatives

Return ONLY valid JSON."""

        response = self.client.complete_json(
            prompt,
            system_prompt="You are an empathy analyst. Identify emotional needs in audience comments. Return valid JSON only."
        )

        if response and "pain_points" in response:
            return response["pain_points"]
        return []

    def score_topic_demand(
        self,
        topic: str,
        questions: List[Dict],
        view_data: Dict = None
    ) -> Dict[str, Any]:
        """
        Score demand for a specific topic.

        Returns:
        {
            "topic": topic,
            "demand_score": 0-100,
            "question_count": number of related questions,
            "emotional_intensity": low/medium/high,
            "competition_level": low/medium/high,
            "recommendation": "create/skip/monitor"
        }
        """
        # Filter questions for this topic
        topic_lower = topic.lower()
        related_questions = [
            q for q in questions
            if topic_lower in q.get("topic", "").lower() or
               topic_lower in q.get("question", "").lower()
        ]

        question_count = len(related_questions)

        # Calculate urgency distribution
        high_urgency = sum(1 for q in related_questions if q.get("urgency") == "high")

        # Base score on question frequency
        demand_score = min(100, question_count * 10)

        # Boost for high urgency
        if high_urgency > 0:
            demand_score = min(100, demand_score + high_urgency * 5)

        # Boost for view data if available
        if view_data and view_data.get("avg_views", 0) > 100000:
            demand_score = min(100, demand_score + 20)

        # Determine emotional intensity
        if high_urgency > 3:
            emotional_intensity = "high"
        elif high_urgency > 0:
            emotional_intensity = "medium"
        else:
            emotional_intensity = "low"

        # Recommendation
        if demand_score >= 70:
            recommendation = "create"
        elif demand_score >= 40:
            recommendation = "monitor"
        else:
            recommendation = "skip"

        return {
            "topic": topic,
            "demand_score": demand_score,
            "question_count": question_count,
            "related_questions": related_questions[:5],  # Top 5
            "emotional_intensity": emotional_intensity,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }

    def generate_demand_brief(
        self,
        comments: List[str],
        seed_topics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive demand brief from comments.

        This is the main output used by the script writing phase.
        """
        if self.verbose:
            print(f"\n📊 Analyzing {len(comments)} comments...")

        # Extract questions
        if self.verbose:
            print("   Extracting questions...")
        questions = self.extract_questions(comments)

        # Identify pain points
        if self.verbose:
            print("   Identifying pain points...")
        pain_points = self.identify_pain_points(comments)

        # Score topics if provided
        topic_scores = []
        if seed_topics:
            if self.verbose:
                print(f"   Scoring {len(seed_topics)} topics...")
            for topic in seed_topics:
                score = self.score_topic_demand(topic, questions)
                topic_scores.append(score)

            # Sort by demand score
            topic_scores.sort(key=lambda x: x["demand_score"], reverse=True)

        # Generate summary using LLM
        if self.verbose:
            print("   Generating summary...")

        summary_prompt = f"""Based on this demand analysis, write a brief summary.

QUESTIONS FOUND ({len(questions)}):
{json.dumps(questions[:10], indent=2)}

PAIN POINTS ({len(pain_points)}):
{json.dumps(pain_points[:5], indent=2)}

TOP TOPICS BY DEMAND:
{json.dumps([{"topic": t["topic"], "score": t["demand_score"]} for t in topic_scores[:10]], indent=2) if topic_scores else "Not scored"}

Write a 2-3 paragraph summary of:
1. What the audience wants most
2. Their emotional state and concerns
3. Top content opportunities

Be specific and actionable."""

        summary = self.client.complete(
            summary_prompt,
            system_prompt="You are a content strategist. Summarize demand signals for a YouTube creator."
        )

        demand_brief = {
            "timestamp": datetime.now().isoformat(),
            "comments_analyzed": len(comments),
            "questions": questions,
            "pain_points": pain_points,
            "topic_scores": topic_scores,
            "summary": summary or "Analysis complete. See detailed data above.",
            "top_opportunities": [
                t["topic"] for t in topic_scores[:5]
                if t.get("recommendation") == "create"
            ] if topic_scores else []
        }

        if self.verbose:
            print(f"\n✅ Demand brief generated")
            print(f"   Questions: {len(questions)}")
            print(f"   Pain points: {len(pain_points)}")
            print(f"   Top opportunities: {demand_brief['top_opportunities']}")

        return demand_brief

    def save_brief(self, brief: Dict, output_path: str = None):
        """Save demand brief to JSON file."""
        if output_path is None:
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "demand_brief.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(brief, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"💾 Saved to {output_path}")


def main():
    """Test the demand analyzer."""
    print("=" * 50)
    print("Testing Demand Analyzer")
    print("=" * 50)

    analyzer = DemandAnalyzer(verbose=True)

    # Sample comments for testing
    test_comments = [
        "What is the ideal cholesterol level for someone with family history of heart disease?",
        "I'm so scared about my high LDL, my doctor wants to put me on statins but I've heard they're dangerous",
        "Can you please make a video about heart attack symptoms in women? My mother had one and we didn't recognize it",
        "Why do some doctors say eggs are fine and others say to avoid them? So confusing!",
        "I've been doing intermittent fasting - is it good or bad for the heart?",
        "Please explain Apo B, I keep hearing about it but my doctor never tests for it",
        "What diet is best for reversing heart disease? Keto? Mediterranean? Plant-based?",
        "My father had bypass surgery at 50, am I doomed to have the same fate?",
        "Can stress really cause heart attacks? I have a very stressful job",
        "What supplements actually help heart health? There's so much conflicting info"
    ]

    # Test with sample topics
    test_topics = ["cholesterol", "diet", "statins", "stress", "family history"]

    brief = analyzer.generate_demand_brief(test_comments, test_topics)

    print("\n" + "=" * 50)
    print("DEMAND BRIEF")
    print("=" * 50)
    print(json.dumps(brief, indent=2))

    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
