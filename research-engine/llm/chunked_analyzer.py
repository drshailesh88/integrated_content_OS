#!/usr/bin/env python3
"""
Chunked Comment Analyzer - Map-Reduce for Large Comment Sets

Solves the problem of free LLMs not being able to handle 2000+ comments.
Splits comments into chunks, analyzes in parallel, then synthesizes.

Usage:
    from llm.chunked_analyzer import ChunkedAnalyzer

    analyzer = ChunkedAnalyzer()
    results = analyzer.analyze(comments)  # Auto-selects quick vs map-reduce
"""

import os
import json
import re
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    requests = None

load_dotenv()

# =============================================================================
# FREE MODELS (Updated Dec 2024)
# =============================================================================
FREE_MODELS = {
    "llama-3.3-70b": "meta-llama/llama-3.3-70b-instruct:free",
    "qwen-2.5-72b": "qwen/qwen-2.5-72b-instruct:free",
    "gemini-2-flash": "google/gemini-2.0-flash-exp:free",
    "grok-2": "x-ai/grok-2-1212:free",
    "deepseek-r1": "deepseek/deepseek-r1:free",
    "mistral-small": "mistralai/mistral-small-24b-instruct-2501:free",
    "gemma-3-27b": "google/gemma-3-27b-it:free",
}

# Default models for each stage
DEFAULT_CHUNK_MODEL = FREE_MODELS["llama-3.3-70b"]
DEFAULT_SYNTHESIS_MODEL = FREE_MODELS["qwen-2.5-72b"]


# =============================================================================
# DATA CLASSES
# =============================================================================
@dataclass
class Comment:
    text: str
    author: str = ""
    likes: int = 0
    time: str = ""
    video_id: str = ""
    video_title: str = ""


@dataclass
class ChunkResult:
    chunk_index: int
    questions: List[str]
    myths: List[str]
    pain_points: List[str]
    demands: List[str]
    sentiment: Dict[str, int]
    key_insights: List[str]
    error: Optional[str] = None


@dataclass
class AnalysisResult:
    top_questions: List[Dict[str, Any]]
    top_myths: List[Dict[str, Any]]
    top_pain_points: List[Dict[str, Any]]
    content_demands: List[Dict[str, Any]]
    overall_sentiment: Dict[str, Any]
    recommendations: Dict[str, List[str]]
    stats: Dict[str, Any]


# =============================================================================
# SPAM FILTERING
# =============================================================================
SPAM_PATTERNS = [
    r"^(first|second|third)!?$",
    r"^nice\s*(video|vid|one)?!?$",
    r"^(great|awesome|amazing|cool)!?$",
    r"^(subscribe|sub)\s*(to\s*me)?",
    r"^(like|liked)!?$",
    r"^(hi|hello|hey)!?$",
    r"check\s*(out)?\s*my\s*(channel|video)",
    r"^\d+:\d+$",  # Just timestamps
]


def filter_spam(text: str, min_length: int = 15) -> bool:
    """Return True if comment should be KEPT (is not spam)."""
    text = text.strip()

    if len(text) < min_length:
        return False

    for pattern in SPAM_PATTERNS:
        if re.match(pattern, text, re.IGNORECASE):
            return False

    return True


def filter_comments(comments: List[Dict], min_length: int = 15) -> List[Dict]:
    """Filter out spam and low-value comments."""
    return [c for c in comments if filter_spam(c.get("text", ""), min_length)]


def sort_by_engagement(comments: List[Dict]) -> List[Dict]:
    """Sort comments by engagement (likes + replies)."""
    return sorted(
        comments,
        key=lambda c: c.get("likes", 0) + c.get("reply_count", 0) * 2,
        reverse=True
    )


# =============================================================================
# CHUNKING
# =============================================================================
def chunk_comments(
    comments: List[Dict],
    chunk_size: int = 100,
    max_chunks: int = 20,
    filter_spam_: bool = True,
    prioritize_by_likes: bool = True
) -> List[List[Dict]]:
    """Split comments into chunks for parallel processing."""

    # Step 1: Filter spam
    if filter_spam_:
        comments = filter_comments(comments)

    # Step 2: Sort by engagement
    if prioritize_by_likes:
        comments = sort_by_engagement(comments)

    # Step 3: Limit total comments
    max_comments = chunk_size * max_chunks
    if len(comments) > max_comments:
        comments = comments[:max_comments]

    # Step 4: Split into chunks
    chunks = []
    for i in range(0, len(comments), chunk_size):
        chunks.append(comments[i:i + chunk_size])

    return chunks


def comments_to_text(comments: List[Dict]) -> str:
    """Convert comments to text format for LLM."""
    lines = []
    for i, c in enumerate(comments, 1):
        likes = f" [{c.get('likes', 0)} likes]" if c.get('likes') else ""
        lines.append(f"[{i}]{likes} {c.get('text', '')}")
    return "\n---\n".join(lines)


# =============================================================================
# PROMPTS
# =============================================================================
def get_chunk_prompt(comments_text: str, chunk_index: int, total_chunks: int) -> str:
    return f"""You are analyzing YouTube comments for a CARDIOLOGY medical education channel.

CHUNK {chunk_index + 1} OF {total_chunks}

Analyze these comments and extract:

1. QUESTIONS: What are viewers asking? What do they want to know?
2. MYTHS: What misconceptions or false beliefs do viewers have?
3. PAIN POINTS: What frustrations, fears, or problems do viewers express?
4. DEMANDS: What content are viewers requesting? What do they want covered?
5. SENTIMENT: Count positive, negative, and neutral comments
6. KEY INSIGHTS: Any other notable patterns or observations

COMMENTS:
{comments_text}

RESPOND WITH JSON ONLY. NO MARKDOWN. NO EXPLANATIONS.

{{
  "questions": ["question 1", "question 2", "question 3"],
  "myths": ["myth 1", "myth 2"],
  "painPoints": ["pain point 1", "pain point 2"],
  "demands": ["demand 1", "demand 2"],
  "sentiment": {{"positive": 0, "negative": 0, "neutral": 0}},
  "keyInsights": ["insight 1", "insight 2"]
}}"""


def get_synthesis_prompt(chunk_results: List[Dict]) -> str:
    results_json = json.dumps(chunk_results, indent=2)

    return f"""You are a content strategy expert for a CARDIOLOGY YouTube channel.

You have analysis results from {len(chunk_results)} chunks of YouTube comments.
Your job is to SYNTHESIZE these into ONE comprehensive report.

CHUNK RESULTS:
{results_json}

Create a unified analysis with:

1. TOP QUESTIONS (deduplicated, ranked by how often they appear)
   - Include urgency level (high/medium/low)
   - High = many people asking, indicates major knowledge gap

2. TOP MYTHS (deduplicated, ranked by prevalence)
   - Include danger level (high/medium/low)
   - High = could lead to harmful health decisions

3. TOP PAIN POINTS (deduplicated, ranked by frequency)
   - Note if emotional (fear/anxiety based)

4. CONTENT DEMANDS (what viewers want)
   - Suggest content type (video, short, series)

5. OVERALL SENTIMENT
   - Aggregate the sentiment counts
   - Write a brief summary of viewer mood

6. RECOMMENDATIONS
   - mustAddress: Topics you MUST cover based on audience needs
   - contentGaps: What's missing that viewers clearly need
   - viralPotentialTopics: Topics with high engagement potential
   - warningsToAvoid: Things that upset viewers or backfire

RESPOND WITH JSON ONLY:

{{
  "topQuestions": [
    {{"question": "...", "frequency": 5, "urgency": "high"}}
  ],
  "topMyths": [
    {{"myth": "...", "prevalence": 4, "dangerLevel": "high"}}
  ],
  "topPainPoints": [
    {{"painPoint": "...", "frequency": 3, "emotional": true}}
  ],
  "contentDemands": [
    {{"demand": "...", "frequency": 3, "contentType": "video"}}
  ],
  "overallSentiment": {{
    "positive": 0,
    "negative": 0,
    "neutral": 0,
    "summary": "..."
  }},
  "recommendations": {{
    "mustAddress": ["..."],
    "contentGaps": ["..."],
    "viralPotentialTopics": ["..."],
    "warningsToAvoid": ["..."]
  }}
}}"""


# =============================================================================
# LLM CALLS
# =============================================================================
def call_openrouter(
    prompt: str,
    model: str,
    api_key: str,
    retries: int = 2,
    timeout: int = 90
) -> Optional[str]:
    """Call OpenRouter API with retry logic."""

    if not requests:
        raise ImportError("requests library not installed")

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/drshailesh88",
                    "X-Title": "Dr Shailesh YouTube Analyzer"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert analyst. Always respond with valid JSON only. No markdown, no explanations."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 4000,
                    "temperature": 0.3
                },
                timeout=timeout
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")

            elif response.status_code == 429:
                # Rate limited - wait and retry
                time.sleep(2 ** attempt)
                continue

            else:
                print(f"    API error {response.status_code}: {response.text[:200]}")
                continue

        except Exception as e:
            if attempt == retries:
                raise e
            time.sleep(1 * (attempt + 1))

    return None


def parse_json_response(response: str) -> Dict:
    """Parse JSON from LLM response, handling markdown code blocks."""
    cleaned = response.strip()

    # Remove markdown code blocks
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract JSON object
        match = re.search(r'\{[\s\S]*\}', cleaned)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Failed to parse JSON: {cleaned[:200]}...")


# =============================================================================
# CHUNKED ANALYZER
# =============================================================================
class ChunkedAnalyzer:
    """Map-Reduce analyzer for large comment sets."""

    def __init__(
        self,
        chunk_model: str = DEFAULT_CHUNK_MODEL,
        synthesis_model: str = DEFAULT_SYNTHESIS_MODEL,
        chunk_size: int = 100,
        max_chunks: int = 20,
        max_concurrent: int = 5,
        verbose: bool = True
    ):
        self.chunk_model = chunk_model
        self.synthesis_model = synthesis_model
        self.chunk_size = chunk_size
        self.max_chunks = max_chunks
        self.max_concurrent = max_concurrent
        self.verbose = verbose
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

    def log(self, msg: str):
        if self.verbose:
            print(msg)

    def analyze_chunk(self, comments: List[Dict], chunk_index: int, total_chunks: int) -> ChunkResult:
        """Analyze a single chunk of comments."""
        comments_text = comments_to_text(comments)
        prompt = get_chunk_prompt(comments_text, chunk_index, total_chunks)

        try:
            response = call_openrouter(prompt, self.chunk_model, self.api_key)
            if not response:
                return ChunkResult(
                    chunk_index=chunk_index,
                    questions=[], myths=[], pain_points=[], demands=[],
                    sentiment={"positive": 0, "negative": 0, "neutral": 0},
                    key_insights=[],
                    error="No response from LLM"
                )

            parsed = parse_json_response(response)

            return ChunkResult(
                chunk_index=chunk_index,
                questions=parsed.get("questions", []),
                myths=parsed.get("myths", []),
                pain_points=parsed.get("painPoints", []),
                demands=parsed.get("demands", []),
                sentiment=parsed.get("sentiment", {"positive": 0, "negative": 0, "neutral": 0}),
                key_insights=parsed.get("keyInsights", [])
            )

        except Exception as e:
            return ChunkResult(
                chunk_index=chunk_index,
                questions=[], myths=[], pain_points=[], demands=[],
                sentiment={"positive": 0, "negative": 0, "neutral": 0},
                key_insights=[],
                error=str(e)
            )

    def analyze_map_reduce(self, comments: List[Dict]) -> AnalysisResult:
        """Full map-reduce analysis for large comment sets."""
        start_time = time.time()

        self.log(f"\nStarting map-reduce analysis of {len(comments)} comments")
        self.log(f"Chunk model: {self.chunk_model}")
        self.log(f"Synthesis model: {self.synthesis_model}")

        # Step 1: Chunk
        chunks = chunk_comments(
            comments,
            chunk_size=self.chunk_size,
            max_chunks=self.max_chunks
        )

        total_filtered = sum(len(c) for c in chunks)
        self.log(f"Chunked into {len(chunks)} chunks ({total_filtered} comments after filtering)")

        if not chunks:
            raise ValueError("No valid comments after filtering")

        # Step 2: MAP - Analyze chunks in parallel
        self.log("\n[MAP PHASE] Analyzing chunks...")
        chunk_results = []

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = {
                executor.submit(self.analyze_chunk, chunk, i, len(chunks)): i
                for i, chunk in enumerate(chunks)
            }

            for future in as_completed(futures):
                chunk_idx = futures[future]
                try:
                    result = future.result()
                    chunk_results.append(result)
                    status = "ERROR" if result.error else "OK"
                    self.log(f"  Chunk {chunk_idx + 1}/{len(chunks)}: {status}")
                except Exception as e:
                    self.log(f"  Chunk {chunk_idx + 1}/{len(chunks)}: FAILED - {e}")

        # Sort by chunk index
        chunk_results.sort(key=lambda r: r.chunk_index)

        successful = [r for r in chunk_results if not r.error]
        self.log(f"\nMAP complete: {len(successful)}/{len(chunks)} chunks successful")

        if not successful:
            raise ValueError("All chunk analyses failed")

        # Step 3: REDUCE - Synthesize results
        self.log("\n[REDUCE PHASE] Synthesizing results...")

        # Convert to dicts for JSON serialization
        chunk_dicts = [asdict(r) for r in successful]
        synthesis_prompt = get_synthesis_prompt(chunk_dicts)

        synthesis_response = call_openrouter(
            synthesis_prompt,
            self.synthesis_model,
            self.api_key,
            retries=2
        )

        if not synthesis_response:
            raise ValueError("Synthesis failed - no response")

        synthesized = parse_json_response(synthesis_response)

        processing_time = time.time() - start_time
        self.log(f"\nAnalysis complete in {processing_time:.1f}s")

        return AnalysisResult(
            top_questions=synthesized.get("topQuestions", []),
            top_myths=synthesized.get("topMyths", []),
            top_pain_points=synthesized.get("topPainPoints", []),
            content_demands=synthesized.get("contentDemands", []),
            overall_sentiment=synthesized.get("overallSentiment", {}),
            recommendations=synthesized.get("recommendations", {}),
            stats={
                "total_comments": len(comments),
                "analyzed_comments": total_filtered,
                "chunks_processed": len(successful),
                "processing_time_seconds": round(processing_time, 1),
                "chunk_model": self.chunk_model,
                "synthesis_model": self.synthesis_model
            }
        )

    def analyze_quick(self, comments: List[Dict]) -> AnalysisResult:
        """Quick single-call analysis for smaller comment sets (<500)."""
        start_time = time.time()

        # Filter and limit
        filtered = filter_comments(comments)
        filtered = sort_by_engagement(filtered)[:500]

        self.log(f"\nQuick analysis of {len(filtered)} comments (filtered from {len(comments)})")

        comments_text = comments_to_text(filtered)

        prompt = f"""Analyze these {len(filtered)} YouTube comments for a CARDIOLOGY channel.

COMMENTS:
{comments_text}

Provide comprehensive analysis as JSON:

{{
  "topQuestions": [{{"question": "...", "frequency": 1, "urgency": "high|medium|low"}}],
  "topMyths": [{{"myth": "...", "prevalence": 1, "dangerLevel": "high|medium|low"}}],
  "topPainPoints": [{{"painPoint": "...", "frequency": 1, "emotional": true|false}}],
  "contentDemands": [{{"demand": "...", "frequency": 1, "contentType": "video|short|series"}}],
  "overallSentiment": {{"positive": 0, "negative": 0, "neutral": 0, "summary": "..."}},
  "recommendations": {{
    "mustAddress": ["..."],
    "contentGaps": ["..."],
    "viralPotentialTopics": ["..."],
    "warningsToAvoid": ["..."]
  }}
}}

JSON ONLY. NO MARKDOWN."""

        response = call_openrouter(prompt, self.chunk_model, self.api_key)
        if not response:
            raise ValueError("No response from LLM")

        result = parse_json_response(response)
        processing_time = time.time() - start_time

        return AnalysisResult(
            top_questions=result.get("topQuestions", []),
            top_myths=result.get("topMyths", []),
            top_pain_points=result.get("topPainPoints", []),
            content_demands=result.get("contentDemands", []),
            overall_sentiment=result.get("overallSentiment", {}),
            recommendations=result.get("recommendations", {}),
            stats={
                "total_comments": len(comments),
                "analyzed_comments": len(filtered),
                "chunks_processed": 1,
                "processing_time_seconds": round(processing_time, 1),
                "method": "quick",
                "model": self.chunk_model
            }
        )

    def analyze(self, comments: List[Dict], force_method: str = None) -> AnalysisResult:
        """
        Auto-select analysis method based on comment count.

        Args:
            comments: List of comment dicts with 'text' key
            force_method: 'quick' or 'map-reduce' to override auto-selection

        Returns:
            AnalysisResult with comprehensive insights
        """
        threshold = 500

        if force_method == "quick":
            return self.analyze_quick(comments)
        elif force_method == "map-reduce":
            return self.analyze_map_reduce(comments)

        # Auto-select
        if len(comments) <= threshold:
            self.log(f"Using QUICK analysis for {len(comments)} comments")
            return self.analyze_quick(comments)
        else:
            self.log(f"Using MAP-REDUCE for {len(comments)} comments")
            return self.analyze_map_reduce(comments)


# =============================================================================
# MAIN (for testing)
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Chunked Analyzer - Test")
    print("=" * 60)

    # Test with sample comments
    test_comments = [
        {"text": "What is the best diet for heart patients?", "likes": 45},
        {"text": "I heard statins cause muscle pain, is that true?", "likes": 32},
        {"text": "My father had a heart attack, should I get tested?", "likes": 28},
        {"text": "Can you do a video on LDL vs HDL cholesterol?", "likes": 55},
        {"text": "Nice video!", "likes": 5},  # Will be filtered as spam
        {"text": "I'm scared of taking blood thinners, what are the risks?", "likes": 40},
        {"text": "First!", "likes": 2},  # Will be filtered as spam
        {"text": "What exercises are safe after angioplasty?", "likes": 38},
    ]

    try:
        analyzer = ChunkedAnalyzer(verbose=True)
        result = analyzer.analyze(test_comments, force_method="quick")

        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(json.dumps(asdict(result), indent=2))

    except Exception as e:
        print(f"Error: {e}")
