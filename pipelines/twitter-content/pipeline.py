"""
Main Pipeline - Orchestrates the full content generation flow.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json

from .config import config
from .harvester import IdeaHarvester, ContentIdea, create_harvester
from .researcher import DualResearcher, ResearchResults, create_researcher
from .synthesizer import KnowledgeSynthesizer, KnowledgeBrief, create_synthesizer
from .writer import ContentWriter, ContentFormat, GeneratedContent, create_writer


@dataclass
class PipelineResult:
    """Complete result from pipeline execution."""
    idea: ContentIdea
    research: ResearchResults
    brief: KnowledgeBrief
    content: GeneratedContent
    timestamp: datetime

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "idea": self.idea.to_dict(),
            "research": {
                "pubmed_count": len(self.research.pubmed_articles),
                "rag_count": len(self.research.rag_results),
                "pubmed_summary": self.research.get_pubmed_summary(),
                "rag_summary": self.research.get_rag_summary(),
            },
            "brief": {
                "executive_summary": self.brief.executive_summary,
                "content_angles": self.brief.content_angles,
                "citations": self.brief.citations,
            },
            "content": {
                "format": self.content.format.value,
                "content": self.content.content,
                "word_count": self.content.word_count,
                "char_count": self.content.char_count,
            },
            "timestamp": self.timestamp.isoformat(),
        }

    def save_to_file(self, filepath: str):
        """Save result to JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


class ContentPipeline:
    """
    Orchestrates the full content generation pipeline:
    1. Harvest ideas from Twitter OR take direct questions
    2. Research using PubMed + AstraDB RAG
    3. Synthesize into knowledge briefs
    4. Generate publication-ready content
    """

    def __init__(self):
        self.harvester = create_harvester()
        self.researcher = create_researcher()
        self.synthesizer = create_synthesizer()
        self.writer = create_writer()

    async def run_full_pipeline(
        self,
        mode: str = "harvest",
        question: Optional[str] = None,
        max_ideas: int = 3,
        content_format: Optional[ContentFormat] = None,
    ) -> list[PipelineResult]:
        """
        Run the complete pipeline.

        Args:
            mode: "harvest" to scrape Twitter, "direct" to use a question
            question: Required if mode is "direct"
            max_ideas: Maximum number of ideas to process
            content_format: Desired output format (auto-detected if None)

        Returns:
            List of PipelineResult objects
        """
        # Phase 1: Get ideas
        if mode == "harvest":
            print("\n" + "="*60)
            print("PHASE 1: HARVESTING IDEAS FROM TWITTER")
            print("="*60)
            ideas = await self.harvester.harvest_ideas(top_n=max_ideas)
        elif mode == "direct":
            if not question:
                raise ValueError("Question required for direct mode")
            print("\n" + "="*60)
            print("PHASE 1: CREATING IDEA FROM DIRECT QUESTION")
            print("="*60)
            idea = await self.harvester.create_direct_idea(question)
            ideas = [idea]
        else:
            raise ValueError(f"Unknown mode: {mode}")

        if not ideas:
            print("No ideas found to process.")
            return []

        print(f"\nProcessing {len(ideas)} ideas...")

        # Process each idea through the pipeline
        results = []
        for i, idea in enumerate(ideas, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING IDEA {i}/{len(ideas)}: {idea.research_question[:50]}...")
            print("="*60)

            try:
                result = await self._process_idea(idea, content_format)
                results.append(result)
                print(f"\n✓ Successfully generated {result.content.format.value} content")
                print(f"  Word count: {result.content.word_count}")
                print(f"  Sources: {result.research.total_sources}")
            except Exception as e:
                print(f"\n✗ Error processing idea: {e}")
                continue

        return results

    async def _process_idea(
        self,
        idea: ContentIdea,
        content_format: Optional[ContentFormat] = None,
    ) -> PipelineResult:
        """Process a single idea through the pipeline."""
        # Phase 2: Research
        print("\n→ Phase 2: Researching...")
        research = await self.researcher.research(idea)
        print(f"  Found {len(research.pubmed_articles)} PubMed articles")
        print(f"  Found {len(research.rag_results)} guideline/textbook chunks")

        # Phase 3: Synthesize
        print("\n→ Phase 3: Synthesizing...")
        brief = await self.synthesizer.synthesize(research)
        print(f"  Generated brief with {len(brief.content_angles)} content angles")

        # Phase 4: Write
        print("\n→ Phase 4: Writing content...")
        content = await self.writer.write(brief, format=content_format)

        return PipelineResult(
            idea=idea,
            research=research,
            brief=brief,
            content=content,
            timestamp=datetime.now(),
        )

    async def process_direct_question(
        self,
        question: str,
        format: Optional[ContentFormat] = None,
    ) -> PipelineResult:
        """
        Quick method to process a direct question.

        Args:
            question: The research question
            format: Desired output format

        Returns:
            Single PipelineResult
        """
        results = await self.run_full_pipeline(
            mode="direct",
            question=question,
            content_format=format,
        )
        return results[0] if results else None

    async def harvest_and_process(
        self,
        max_ideas: int = 3,
        format: Optional[ContentFormat] = None,
    ) -> list[PipelineResult]:
        """
        Harvest ideas from Twitter and process them.

        Args:
            max_ideas: Number of ideas to process
            format: Desired output format

        Returns:
            List of PipelineResult objects
        """
        return await self.run_full_pipeline(
            mode="harvest",
            max_ideas=max_ideas,
            content_format=format,
        )


# Factory function
def create_pipeline() -> ContentPipeline:
    return ContentPipeline()


# Convenience functions for direct usage
async def generate_from_question(
    question: str,
    format: Optional[str] = None,
) -> GeneratedContent:
    """
    Generate content from a direct question.

    Args:
        question: The research question
        format: "tweet", "thread", or "long_post"

    Returns:
        GeneratedContent object
    """
    pipeline = create_pipeline()
    content_format = ContentFormat(format) if format else None
    result = await pipeline.process_direct_question(question, content_format)
    return result.content if result else None


async def harvest_and_generate(max_ideas: int = 3) -> list[GeneratedContent]:
    """
    Harvest ideas from Twitter and generate content.

    Args:
        max_ideas: Number of ideas to process

    Returns:
        List of GeneratedContent objects
    """
    pipeline = create_pipeline()
    results = await pipeline.harvest_and_process(max_ideas=max_ideas)
    return [r.content for r in results]
