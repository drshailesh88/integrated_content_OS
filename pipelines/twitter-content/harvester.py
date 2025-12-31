"""
Idea Harvester - Scrapes tweets from medical influencers and extracts content ideas.
"""

from dataclasses import dataclass
from typing import Optional

from .config import config, INSPIRATION_ACCOUNTS
from .utils.apify import apify_client, Tweet
from .utils.llm import llm_client


@dataclass
class ContentIdea:
    """Represents a harvested content idea."""
    id: str
    original_tweet: Tweet
    research_question: str
    pubmed_query: str
    rag_keywords: list[str]
    topic_category: str
    engagement_score: int

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "original_tweet": {
                "text": self.original_tweet.text,
                "url": self.original_tweet.url,
                "author": self.original_tweet.author_handle,
                "engagement": self.original_tweet.engagement_score,
            },
            "research_question": self.research_question,
            "pubmed_query": self.pubmed_query,
            "rag_keywords": self.rag_keywords,
            "topic_category": self.topic_category,
        }


class IdeaHarvester:
    """
    Harvests content ideas from medical Twitter influencers.
    Extracts high-engagement tweets and generates research questions.
    """

    def __init__(self):
        self.apify = apify_client
        self.llm = llm_client
        self.inspiration_accounts = INSPIRATION_ACCOUNTS

    async def harvest_ideas(
        self,
        accounts: Optional[list[dict]] = None,
        max_tweets_per_account: int = 50,
        min_engagement: int = 50,
        top_n: int = 10,
    ) -> list[ContentIdea]:
        """
        Harvest content ideas from inspiration accounts.

        Args:
            accounts: List of accounts to scrape (uses default if None)
            max_tweets_per_account: Max tweets per account
            min_engagement: Minimum engagement score
            top_n: Number of top ideas to return

        Returns:
            List of ContentIdea objects
        """
        accounts = accounts or self.inspiration_accounts

        # Scrape tweets
        print(f"Scraping tweets from {len(accounts)} accounts...")
        all_tweets = await self.apify.scrape_inspiration_accounts(
            accounts=accounts,
            max_tweets_per_account=max_tweets_per_account,
        )

        # Filter and rank
        top_tweets = self.apify.filter_and_rank_tweets(
            tweets=all_tweets,
            min_engagement=min_engagement,
            top_n=top_n * 2,  # Get extra to account for filtering
        )

        # Generate research questions for top tweets
        ideas = []
        for i, tweet in enumerate(top_tweets[:top_n]):
            try:
                idea = await self._extract_idea_from_tweet(tweet, i + 1)
                if idea:
                    ideas.append(idea)
                    print(f"Extracted idea {len(ideas)}: {idea.research_question[:60]}...")
            except Exception as e:
                print(f"Error extracting idea from tweet: {e}")
                continue

        return ideas

    async def _extract_idea_from_tweet(
        self,
        tweet: Tweet,
        index: int,
    ) -> Optional[ContentIdea]:
        """
        Extract a content idea from a tweet using LLM.

        Args:
            tweet: The source tweet
            index: Idea index for ID generation

        Returns:
            ContentIdea object or None if extraction fails
        """
        system_prompt = """You are a medical content strategist helping a cardiologist create thought leadership content.
Analyze tweets from medical influencers and extract actionable content ideas.

Your output must be valid JSON with these fields:
- research_question: A clear question that can be researched (1-2 sentences)
- pubmed_query: A PubMed search query to find relevant literature
- rag_keywords: List of 3-5 keywords for searching a medical knowledge base
- topic_category: One of [cardiology, heart_failure, lipids, prevention, nutrition, lifestyle, devices, trials, guidelines]
- is_suitable: boolean - true if this is suitable for thought leadership content"""

        prompt = f"""Analyze this tweet and extract a content idea for a cardiology thought leader:

Tweet by @{tweet.author_handle}:
"{tweet.text}"

Engagement: {tweet.engagement_score} (likes + 2*retweets)

Generate a research question and search parameters that would allow creating an evidence-based, thought leadership post on this topic.

Output valid JSON only."""

        try:
            result = await self.llm.generate_json(
                prompt=prompt,
                system_prompt=system_prompt,
            )

            if not result.get("is_suitable", True):
                return None

            return ContentIdea(
                id=f"idea-{index:03d}",
                original_tweet=tweet,
                research_question=result.get("research_question", ""),
                pubmed_query=result.get("pubmed_query", ""),
                rag_keywords=result.get("rag_keywords", []),
                topic_category=result.get("topic_category", "cardiology"),
                engagement_score=tweet.engagement_score,
            )

        except Exception as e:
            print(f"Error generating idea: {e}")
            return None

    async def create_direct_idea(self, question: str) -> ContentIdea:
        """
        Create a content idea from a direct question (bypass Twitter harvesting).

        Args:
            question: The research question to explore

        Returns:
            ContentIdea object
        """
        system_prompt = """You are a medical content strategist helping a cardiologist create thought leadership content.
Generate search parameters for researching a medical topic.

Your output must be valid JSON with these fields:
- pubmed_query: A PubMed search query to find relevant literature
- rag_keywords: List of 3-5 keywords for searching a medical knowledge base
- topic_category: One of [cardiology, heart_failure, lipids, prevention, nutrition, lifestyle, devices, trials, guidelines]"""

        prompt = f"""Generate research parameters for this question:

"{question}"

Output valid JSON only."""

        result = await self.llm.generate_json(
            prompt=prompt,
            system_prompt=system_prompt,
        )

        # Create a dummy tweet for direct ideas
        from datetime import datetime
        dummy_tweet = Tweet(
            id="direct",
            text=question,
            url="",
            author_handle="user",
            author_name="Direct Input",
            created_at=datetime.now(),
            likes=0,
            retweets=0,
            replies=0,
        )

        return ContentIdea(
            id="idea-direct",
            original_tweet=dummy_tweet,
            research_question=question,
            pubmed_query=result.get("pubmed_query", question),
            rag_keywords=result.get("rag_keywords", question.split()[:5]),
            topic_category=result.get("topic_category", "cardiology"),
            engagement_score=0,
        )


# Factory function
def create_harvester() -> IdeaHarvester:
    return IdeaHarvester()
