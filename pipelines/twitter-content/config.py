"""
Configuration management for the Twitter Content System.
Loads environment variables and provides centralized settings.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ApifyConfig:
    """Apify API configuration for Twitter scraping."""
    api_key: str = field(default_factory=lambda: os.getenv("APIFY_API_KEY", ""))
    actor_id: str = "61RPP7dywgiy0JPD0"  # Tweet Scraper V2 (apidojo/tweet-scraper)
    max_tweets_per_account: int = 50
    include_replies: bool = False
    include_retweets: bool = False


@dataclass
class LLMConfig:
    """LLM configuration for content generation."""
    # OpenRouter
    openrouter_api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_model: str = "anthropic/claude-3.5-sonnet"

    # Direct Anthropic (fallback)
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # Settings
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class OpenAIConfig:
    """OpenAI configuration for embeddings."""
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536


@dataclass
class AstraDBConfig:
    """AstraDB configuration for vector database."""
    api_endpoint: str = field(default_factory=lambda: os.getenv("ASTRA_DB_API_ENDPOINT", ""))
    application_token: str = field(default_factory=lambda: os.getenv("ASTRA_DB_APPLICATION_TOKEN", ""))
    collection_name: str = field(default_factory=lambda: os.getenv("ASTRA_DB_COLLECTION", "medical_knowledge"))
    similarity_threshold: float = 0.65
    top_k: int = 10


@dataclass
class GeminiConfig:
    """Gemini API configuration for cheap/fast content generation."""
    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    model: str = "gemini-2.5-flash"  # Latest Gemini 2.5 Flash
    # Cost: ~$0.15/1M input, $0.60/1M output (~20-50x cheaper than Claude Sonnet)


@dataclass
class PubMedConfig:
    """PubMed/NCBI configuration."""
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("NCBI_API_KEY"))
    email: str = field(default_factory=lambda: os.getenv("NCBI_EMAIL", "user@example.com"))
    tool_name: str = "TwitterContentSystem"
    max_results: int = 20
    date_range_years: int = 5  # Search last 5 years


# Inspiration accounts for content harvesting
INSPIRATION_ACCOUNTS = [
    {"handle": "paddygbarrett", "name": "Dr Paddy Barrett"},
    {"handle": "DrLipid", "name": "Dr Thomas Dayspring"},
    {"handle": "davidludwigmd", "name": "Dr David Ludwig"},
    {"handle": "NutritionMadeS1", "name": "Dr Gil Carvalho"},
    {"handle": "scottissacmd", "name": "Dr Scott Issac"},
    {"handle": "EricTopol", "name": "Dr Eric Topol"},
    {"handle": "anaborgesmd", "name": "Dr Ana Borges"},
    {"handle": "caraborelli", "name": "Dr Cara Borelli"},
]

# Q1 Cardiology journals for PubMed filtering
Q1_JOURNALS = [
    "N Engl J Med",
    "Lancet",
    "JAMA",
    "Circulation",
    "Eur Heart J",
    "J Am Coll Cardiol",  # JACC
    "JACC Cardiovasc Interv",
    "BMJ",
    "Ann Intern Med",
    "JAMA Cardiol",
    "Circ Cardiovasc Interv",
    "JAMA Intern Med",
    "Nat Med",
]

# Journal abbreviation mapping for better matching
JOURNAL_ABBREVIATIONS = {
    "nejm": "N Engl J Med",
    "lancet": "Lancet",
    "jama": "JAMA",
    "circulation": "Circulation",
    "ehj": "Eur Heart J",
    "jacc": "J Am Coll Cardiol",
    "bmj": "BMJ",
}


@dataclass
class VoiceConfig:
    """Voice configuration for content generation - Peter Attia + Eric Topol style."""

    style_description: str = "Peter Attia's intellectual rigor + Eric Topol's scientific accuracy"
    tone: str = "Authoritative but not condescending"
    audience: str = "Educated public, NOT physicians"
    goal: str = "Position as thought leader in cardiology"

    must_do: list = field(default_factory=lambda: [
        "Cite specific Q1 journals by name",
        "Include statistics, effect sizes, NNT when available",
        "Present nuanced takes on complex topics",
        "Reference guidelines with class/level when applicable",
        "Be scholarly but accessible",
        "Use absolute risk differences, not just relative risk",
        "Acknowledge limitations and uncertainties",
    ])

    must_not: list = field(default_factory=lambda: [
        "Oversimplify complex medical concepts",
        "Give direct medical advice",
        "Use clickbait language",
        "Use excessive hashtags (except #MedTwitter occasionally)",
        "Hedge excessively with weak language",
        "Use promotional phrases like 'game changer' or 'paradigm shift'",
        "Make claims without evidence",
    ])

    anti_ai_patterns: list = field(default_factory=lambda: [
        "It's important to note",
        "It's worth mentioning",
        "stands as a testament",
        "plays a vital role",
        "In conclusion",
        "To summarize",
        "Moving forward",
        "At the end of the day",
        "This begs the question",
        "needless to say",
    ])


@dataclass
class Config:
    """Main configuration container."""
    apify: ApifyConfig = field(default_factory=ApifyConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    astradb: AstraDBConfig = field(default_factory=AstraDBConfig)
    pubmed: PubMedConfig = field(default_factory=PubMedConfig)
    gemini: GeminiConfig = field(default_factory=GeminiConfig)
    voice: VoiceConfig = field(default_factory=VoiceConfig)

    # Output settings
    default_format: str = "thread"  # tweet, thread, long_post
    max_ideas_to_process: int = 3

    def validate(self) -> list[str]:
        """Validate configuration and return list of missing/invalid items."""
        issues = []

        if not self.apify.api_key:
            issues.append("APIFY_API_KEY not set")

        if not self.llm.openrouter_api_key and not self.llm.anthropic_api_key:
            issues.append("Neither OPENROUTER_API_KEY nor ANTHROPIC_API_KEY set")

        if not self.openai.api_key:
            issues.append("OPENAI_API_KEY not set (needed for embeddings)")

        if not self.astradb.api_endpoint or not self.astradb.application_token:
            issues.append("AstraDB credentials not fully configured")

        return issues


# Global config instance
config = Config()
