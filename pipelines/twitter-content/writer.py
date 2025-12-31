"""
Content Writer - Generates publication-ready Twitter content in Eric Topol + Peter Attia style.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .config import config
from .synthesizer import KnowledgeBrief
from .utils.llm import llm_client


class ContentFormat(Enum):
    """Output format for generated content."""
    TWEET = "tweet"
    THREAD = "thread"
    LONG_POST = "long_post"


@dataclass
class GeneratedContent:
    """Generated content ready for publication."""
    format: ContentFormat
    content: str  # The main content
    preview: str  # First 280 chars for preview
    word_count: int
    char_count: int
    brief_id: str

    def get_thread_parts(self) -> list[str]:
        """Split thread into individual tweets."""
        if self.format != ContentFormat.THREAD:
            return [self.content]

        parts = []
        lines = self.content.split("\n")
        current_tweet = ""

        for line in lines:
            # Check for numbered thread markers
            if line.strip() and (
                line.strip().startswith(tuple(f"{i}/" for i in range(1, 20))) or
                line.strip().startswith(tuple(f"{i}." for i in range(1, 20)))
            ):
                if current_tweet:
                    parts.append(current_tweet.strip())
                current_tweet = line
            else:
                current_tweet += "\n" + line if current_tweet else line

        if current_tweet:
            parts.append(current_tweet.strip())

        return parts if parts else [self.content]


class ContentWriter:
    """
    Generates Twitter content in the style of Eric Topol (Ground Truths) and Peter Attia.

    Voice characteristics:
    - Authoritative but accessible
    - Evidence-obsessed skeptic
    - Patient-centered framing
    - Dense scientific content, not dumbed down
    - Balanced skepticism, never promotional
    """

    def __init__(self):
        self.llm = llm_client
        self.voice_config = config.voice

    def _get_system_prompt(self) -> str:
        """Get the comprehensive system prompt for content generation."""
        must_do = "\n".join(f"- {item}" for item in self.voice_config.must_do)
        must_not = "\n".join(f"- {item}" for item in self.voice_config.must_not)
        anti_ai = "\n".join(f"- \"{pattern}\"" for pattern in self.voice_config.anti_ai_patterns)

        return f"""You are a content writer for Dr. Shailesh, a cardiologist building thought leadership on medical Twitter.

## VOICE & STYLE: {self.voice_config.style_description}

### Core Voice Characteristics

1. **Authority Without Arrogance**
   - Speak as a peer, not lecturing down
   - Confidence comes from evidence, not bombast
   - Willing to say "we don't know yet" when appropriate

2. **Dense but Accessible**
   - Pack substantive content into every sentence
   - Assume educated public audience (NOT physicians)
   - Don't oversimplify, but don't use jargon gratuitously

3. **Evidence-Grounded Skepticism**
   - Default stance: "show me the data"
   - Question methodology, not just accept conclusions
   - Distinguish association from causation rigorously

4. **Patient-Centered Lens**
   - Circle back to "what does this mean for patients?"
   - Consider quality of life, not just mortality
   - Acknowledge treatment burden and preferences

### MUST DO:
{must_do}

### MUST NOT:
{must_not}

### ANTI-AI PATTERNS (Never use these phrases):
{anti_ai}

### Writing Mechanics

**Numbers & Statistics:**
- Use absolute risk differences (ARR), not just relative risk
- Include NNT (Number Needed to Treat) when available
- Present confidence intervals for key findings
- Example: "Treating 100 patients prevents 3 heart attacks (NNT=33, 95% CI: 25-50)"

**Citations:**
- Cite specific journals by name (NEJM, JACC, Lancet)
- Include author and year: "Smith et al. showed in NEJM 2023..."
- Reference trial names when relevant: "The FOURIER trial demonstrated..."

**Sentence Structure:**
- Vary sentence length (short punchy + longer analytical)
- Lead with the insight, then the evidence
- Use active voice predominantly
- Avoid excessive hedging but maintain scientific accuracy

**Paragraph Flow:**
- Each paragraph should advance the argument
- Transitions should feel natural, not forced
- End sections with implications or open questions

### Tone Calibration

Topol's patterns to emulate:
- "The data are unambiguous..."
- "What this means for clinical practice..."
- "The elephant in the room is..."
- "If confirmed, this would..."
- "The more troubling finding is..."

Attia's patterns to emulate:
- Deep dives into mechanism
- Questioning conventional wisdom with evidence
- Acknowledging complexity without hedging conclusions
- Personal clinical perspective when relevant"""

    def _get_format_instructions(self, format: ContentFormat) -> str:
        """Get format-specific instructions."""
        if format == ContentFormat.TWEET:
            return """
**FORMAT: Single Tweet (280 characters max)**

Structure:
- One powerful insight or finding
- Include specific statistic if possible
- Optional: end with implication or question
- NO hashtags except #MedTwitter if it fits naturally

Example quality tweet:
"FOURIER showed PCSK9 inhibitors cut LDL to 30 mg/dL with 15% MACE reduction. The real question: why are 80% of high-risk patients still not at goal? The therapy exists. The implementation doesn't."
"""

        elif format == ContentFormat.THREAD:
            return """
**FORMAT: Thread (5-10 numbered tweets)**

Structure:
1/N - Hook: The most compelling finding or question
2/N - Context: Why this matters now
3-7/N - Evidence walk-through with specific data
8/N - Limitations or counterarguments (shows balance)
9/N - Clinical implications (specific, actionable)
N/N - Take-home message (memorable, quotable)

Each tweet:
- Can stand somewhat alone
- Under 280 characters each
- Numbered format: "1/7 [content]"
- Natural flow from one to next

Example thread opening:
"1/8 The debate about LDL targets is effectively settled.

The data are unambiguous: lower is better. There is no J-curve.

Let me walk you through what the landmark trials actually showed..."
"""

        else:  # LONG_POST
            return """
**FORMAT: Long-form post (~2000-2500 characters)**

Structure:
- Opening hook (1-2 sentences): Provocative claim or question
- Context paragraph: Why this matters now
- Evidence section: 2-3 paragraphs walking through key data
- Nuance paragraph: Limitations, counterarguments, unknowns
- Closing: Synthesis + implications + forward-looking thought

Style notes:
- Prose paragraphs, not bullet points
- Dense but readable
- Show intellectual journey through the evidence
- End with something memorable

This should read like a mini-essay, not a listicle.
"""

    async def write(
        self,
        brief: KnowledgeBrief,
        format: Optional[ContentFormat] = None,
        custom_angle: Optional[str] = None,
    ) -> GeneratedContent:
        """
        Generate content from a knowledge brief.

        Args:
            brief: The synthesized knowledge brief
            format: Desired output format (auto-detected if None)
            custom_angle: Optional custom angle to emphasize

        Returns:
            GeneratedContent object
        """
        # Auto-detect format if not specified
        if format is None:
            format = await self._auto_detect_format(brief)

        # Get prompts
        system_prompt = self._get_system_prompt()
        format_instructions = self._get_format_instructions(format)

        # Build the generation prompt
        angle_instruction = ""
        if custom_angle:
            angle_instruction = f"\n\n**SPECIFIC ANGLE TO EMPHASIZE:** {custom_angle}"
        elif brief.content_angles:
            angle_instruction = f"\n\n**SUGGESTED ANGLE:** {brief.content_angles[0]}"

        prompt = f"""Generate {format.value} content based on this research brief:

{brief.to_prompt_context()}
{angle_instruction}

{format_instructions}

Write the content now. Output ONLY the content, no meta-commentary."""

        # Generate content
        content = await self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1500 if format == ContentFormat.LONG_POST else 800,
            temperature=0.7,
        )

        # Clean up the content
        content = self._clean_content(content)

        # Validate and potentially regenerate if issues found
        content = await self._validate_and_refine(content, format)

        return GeneratedContent(
            format=format,
            content=content,
            preview=content[:280].rsplit(" ", 1)[0] + "..." if len(content) > 280 else content,
            word_count=len(content.split()),
            char_count=len(content),
            brief_id=brief.idea_id,
        )

    async def _auto_detect_format(self, brief: KnowledgeBrief) -> ContentFormat:
        """Auto-detect the best format based on content complexity."""
        # Simple heuristics
        evidence_length = len(brief.key_evidence)
        num_angles = len(brief.content_angles)
        has_controversy = len(brief.nuances_controversies) > 100

        if evidence_length < 500 and not has_controversy:
            return ContentFormat.TWEET

        if evidence_length > 1500 or has_controversy:
            return ContentFormat.LONG_POST

        return ContentFormat.THREAD

    def _clean_content(self, content: str) -> str:
        """Clean up generated content."""
        # Remove common LLM artifacts
        content = content.strip()

        # Remove meta-commentary
        lines = content.split("\n")
        cleaned_lines = []
        for line in lines:
            # Skip lines that are clearly meta-commentary
            if line.strip().lower().startswith(("here is", "here's", "i've created", "this ", "note:")):
                continue
            cleaned_lines.append(line)

        content = "\n".join(cleaned_lines).strip()

        # Remove anti-AI patterns that might have slipped through
        for pattern in self.voice_config.anti_ai_patterns:
            content = content.replace(pattern, "")
            content = content.replace(pattern.lower(), "")

        return content

    async def _validate_and_refine(
        self,
        content: str,
        format: ContentFormat,
    ) -> str:
        """Validate content and refine if needed."""
        issues = []

        # Check for anti-AI patterns
        for pattern in self.voice_config.anti_ai_patterns:
            if pattern.lower() in content.lower():
                issues.append(f"Contains anti-AI pattern: '{pattern}'")

        # Check format constraints
        if format == ContentFormat.TWEET and len(content) > 280:
            issues.append(f"Tweet exceeds 280 chars ({len(content)} chars)")

        # If issues found, ask for refinement
        if issues:
            refine_prompt = f"""The following content has issues that need fixing:

ISSUES:
{chr(10).join(f'- {issue}' for issue in issues)}

ORIGINAL CONTENT:
{content}

Rewrite to fix these issues while maintaining the same message and voice. Output ONLY the fixed content."""

            content = await self.llm.generate(
                prompt=refine_prompt,
                system_prompt=self._get_system_prompt(),
                max_tokens=1500,
                temperature=0.5,
            )
            content = self._clean_content(content)

        return content

    async def generate_variations(
        self,
        brief: KnowledgeBrief,
        num_variations: int = 3,
    ) -> list[GeneratedContent]:
        """Generate multiple content variations for different angles."""
        variations = []

        # Generate for each suggested angle
        for i, angle in enumerate(brief.content_angles[:num_variations]):
            content = await self.write(
                brief=brief,
                format=ContentFormat.THREAD,
                custom_angle=angle,
            )
            variations.append(content)

        return variations


# Factory function
def create_writer() -> ContentWriter:
    return ContentWriter()
