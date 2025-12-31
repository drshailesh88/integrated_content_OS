"""
Knowledge Synthesizer - Merges research from both pipelines into actionable briefs.
"""

from dataclasses import dataclass

from .researcher import ResearchResults
from .utils.llm import llm_client


@dataclass
class KnowledgeBrief:
    """Synthesized knowledge brief for content creation."""
    idea_id: str
    research_question: str
    executive_summary: str
    key_evidence: str
    guideline_perspective: str
    nuances_controversies: str
    content_angles: list[str]
    citations: list[str]
    raw_synthesis: str

    def to_prompt_context(self) -> str:
        """Format brief for use in content generation prompts."""
        return f"""## RESEARCH BRIEF

### Research Question
{self.research_question}

### Executive Summary
{self.executive_summary}

### Key Evidence from Literature
{self.key_evidence}

### Guideline Perspective
{self.guideline_perspective}

### Nuances & Controversies
{self.nuances_controversies}

### Suggested Content Angles
{chr(10).join(f'- {angle}' for angle in self.content_angles)}

### Citations
{chr(10).join(f'- {cite}' for cite in self.citations)}
"""


class KnowledgeSynthesizer:
    """
    Synthesizes research from PubMed and RAG pipelines into actionable knowledge briefs.
    """

    def __init__(self):
        self.llm = llm_client

    async def synthesize(self, research: ResearchResults) -> KnowledgeBrief:
        """
        Synthesize research results into a knowledge brief.

        Args:
            research: Combined research results

        Returns:
            KnowledgeBrief object
        """
        # Format PubMed articles for prompt
        pubmed_context = self._format_pubmed_for_synthesis(research.pubmed_articles)

        # Format RAG results for prompt
        rag_context = self._format_rag_for_synthesis(research.rag_results)

        # Generate synthesis
        system_prompt = """You are a medical knowledge synthesizer creating a research brief for a cardiologist content creator.

Your task is to merge evidence from peer-reviewed literature (PubMed) with clinical guidelines and textbook knowledge into an actionable brief.

Focus on:
- What the evidence actually shows (with specific statistics)
- Where guidelines and evidence align or conflict
- Nuanced interpretations that demonstrate deep expertise
- Multiple content angles for thought leadership

Be specific with citations and statistics. Never make claims without evidence."""

        prompt = f"""Create a comprehensive research brief for this topic:

## RESEARCH QUESTION
{research.idea.research_question}

## PUBMED LITERATURE
{pubmed_context}

## GUIDELINE & TEXTBOOK KNOWLEDGE
{rag_context}

---

Synthesize this into a structured brief with:

1. **EXECUTIVE SUMMARY** (2-3 sentences capturing the key insight)

2. **KEY EVIDENCE FROM LITERATURE** (bullet points with specific findings and citations)

3. **GUIDELINE PERSPECTIVE** (what ACC/ESC/ADA guidelines say, with class/level if available)

4. **NUANCES & CONTROVERSIES** (areas of debate, evidence-practice gaps)

5. **CONTENT ANGLES** (3 specific angles for social media thought leadership)

6. **FORMATTED CITATIONS** (Author et al. Journal. Year format)

Output the brief in markdown format."""

        synthesis = await self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.4,
        )

        # Parse the synthesis into structured brief
        return self._parse_synthesis(
            synthesis=synthesis,
            research=research,
        )

    def _format_pubmed_for_synthesis(self, articles: list) -> str:
        """Format PubMed articles for synthesis prompt."""
        if not articles:
            return "No peer-reviewed articles found."

        lines = []
        for i, article in enumerate(articles[:8], 1):
            q1_marker = "[Q1 JOURNAL] " if article.is_q1_journal else ""
            lines.append(f"""
### Article {i}: {q1_marker}{article.title}
- **Citation**: {article.get_citation()}
- **PMID**: {article.pmid}
- **DOI**: {article.doi or 'N/A'}
- **Abstract**: {article.abstract[:800]}...
""")
        return "\n".join(lines)

    def _format_rag_for_synthesis(self, results: list) -> str:
        """Format RAG results for synthesis prompt."""
        if not results:
            return "No guideline or textbook content found."

        lines = []
        for i, result in enumerate(results[:6], 1):
            source_info = f"{result.source_name}"
            if result.chapter:
                source_info += f" | {result.chapter}"
            if result.section:
                source_info += f" | {result.section}"

            lines.append(f"""
### Source {i}: [{result.source_type.upper()}] {source_info}
**Relevance**: {result.similarity:.1%}
**Content**:
{result.content[:600]}...
""")
        return "\n".join(lines)

    def _parse_synthesis(
        self,
        synthesis: str,
        research: ResearchResults,
    ) -> KnowledgeBrief:
        """Parse synthesis text into structured KnowledgeBrief."""
        # Extract sections (simple parsing)
        def extract_section(text: str, header: str, next_headers: list[str]) -> str:
            header_lower = header.lower()
            for pattern in [f"**{header}**", f"## {header}", f"### {header}", header]:
                if pattern.lower() in text.lower():
                    start = text.lower().find(pattern.lower())
                    # Find the next section
                    end = len(text)
                    for next_header in next_headers:
                        for next_pattern in [f"**{next_header}**", f"## {next_header}", f"### {next_header}"]:
                            next_pos = text.lower().find(next_pattern.lower(), start + len(pattern))
                            if next_pos > 0 and next_pos < end:
                                end = next_pos
                    return text[start + len(pattern):end].strip()
            return ""

        sections = ["EXECUTIVE SUMMARY", "KEY EVIDENCE", "GUIDELINE PERSPECTIVE",
                    "NUANCES", "CONTENT ANGLES", "CITATIONS"]

        executive_summary = extract_section(synthesis, "EXECUTIVE SUMMARY", sections)
        key_evidence = extract_section(synthesis, "KEY EVIDENCE", sections)
        guideline_perspective = extract_section(synthesis, "GUIDELINE PERSPECTIVE", sections)
        nuances = extract_section(synthesis, "NUANCES", sections)
        angles_text = extract_section(synthesis, "CONTENT ANGLES", sections)
        citations_text = extract_section(synthesis, "CITATIONS", sections)

        # Parse content angles
        content_angles = []
        for line in angles_text.split("\n"):
            line = line.strip()
            if line and (line.startswith("-") or line.startswith("*") or line[0].isdigit()):
                angle = line.lstrip("-*0123456789. ")
                if angle:
                    content_angles.append(angle)

        # Parse citations
        citations = []
        for line in citations_text.split("\n"):
            line = line.strip()
            if line and (line.startswith("-") or line.startswith("*") or line[0].isdigit()):
                citation = line.lstrip("-*0123456789. ")
                if citation:
                    citations.append(citation)

        # Add missing citations from PubMed articles
        for article in research.pubmed_articles[:5]:
            cite = article.get_full_citation()
            if not any(article.pmid in c for c in citations):
                citations.append(f"{cite} (PMID: {article.pmid})")

        return KnowledgeBrief(
            idea_id=research.idea.id,
            research_question=research.idea.research_question,
            executive_summary=executive_summary or synthesis[:200],
            key_evidence=key_evidence or "See synthesis above.",
            guideline_perspective=guideline_perspective or "Guidelines not specifically addressed.",
            nuances_controversies=nuances or "Further research needed.",
            content_angles=content_angles[:3] if content_angles else ["Evidence-based analysis of the topic"],
            citations=citations,
            raw_synthesis=synthesis,
        )


# Factory function
def create_synthesizer() -> KnowledgeSynthesizer:
    return KnowledgeSynthesizer()
