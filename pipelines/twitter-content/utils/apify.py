"""
Apify client for Twitter scraping using Tweet Scraper V2.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import httpx

from ..config import config, INSPIRATION_ACCOUNTS


@dataclass
class Tweet:
    """Represents a scraped tweet."""
    id: str
    text: str
    url: str
    author_handle: str
    author_name: str
    created_at: datetime
    likes: int
    retweets: int
    replies: int

    @property
    def engagement_score(self) -> int:
        """Calculate engagement score (likes + 2*retweets)."""
        return self.likes + (self.retweets * 2)


class ApifyClient:
    """Client for Apify Tweet Scraper V2 actor."""

    BASE_URL = "https://api.apify.com/v2"

    def __init__(self):
        self.config = config.apify
        self.inspiration_accounts = INSPIRATION_ACCOUNTS

    def _get_headers(self) -> dict:
        """Get headers for Apify API requests."""
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    async def scrape_account(
        self,
        handle: str,
        max_tweets: Optional[int] = None,
    ) -> list[Tweet]:
        """
        Scrape tweets from a specific Twitter account.

        Args:
            handle: Twitter handle (without @)
            max_tweets: Maximum tweets to fetch

        Returns:
            List of Tweet objects
        """
        max_tweets = max_tweets or self.config.max_tweets_per_account

        # Run the actor
        run_input = {
            "handles": [handle],
            "tweetsDesired": max_tweets,
            "includeReplies": self.config.include_replies,
            "includeRetweets": self.config.include_retweets,
        }

        # Start actor run
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.BASE_URL}/acts/{self.config.actor_id}/runs",
                headers=self._get_headers(),
                json=run_input,
                params={"waitForFinish": 120},  # Wait up to 2 minutes
            )
            response.raise_for_status()
            run_data = response.json()

        # Get run results
        run_id = run_data["data"]["id"]
        default_dataset_id = run_data["data"]["defaultDatasetId"]

        # Fetch dataset items
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/datasets/{default_dataset_id}/items",
                headers=self._get_headers(),
                params={"format": "json"},
            )
            response.raise_for_status()
            items = response.json()

        # Parse tweets
        tweets = []
        for item in items:
            try:
                tweet = self._parse_tweet(item, handle)
                if tweet:
                    tweets.append(tweet)
            except Exception as e:
                print(f"Warning: Could not parse tweet: {e}")
                continue

        return tweets

    def _parse_tweet(self, item: dict, handle: str) -> Optional[Tweet]:
        """Parse a raw tweet item into a Tweet object."""
        text = item.get("full_text", item.get("text", ""))

        # Skip short tweets
        if len(text) < 80:
            return None

        # Parse created_at
        created_at_str = item.get("created_at", "")
        try:
            # Twitter date format: "Tue Dec 10 12:00:00 +0000 2024"
            created_at = datetime.strptime(
                created_at_str,
                "%a %b %d %H:%M:%S %z %Y"
            )
        except (ValueError, TypeError):
            created_at = datetime.now()

        # Get author info
        user = item.get("user", {})
        author_handle = user.get("screen_name", handle)
        author_name = user.get("name", handle)

        return Tweet(
            id=item.get("id_str", item.get("id", "")),
            text=text,
            url=f"https://twitter.com/{author_handle}/status/{item.get('id_str', '')}",
            author_handle=author_handle,
            author_name=author_name,
            created_at=created_at,
            likes=item.get("favorite_count", 0),
            retweets=item.get("retweet_count", 0),
            replies=item.get("reply_count", 0),
        )

    async def scrape_inspiration_accounts(
        self,
        accounts: Optional[list[dict]] = None,
        max_tweets_per_account: Optional[int] = None,
    ) -> list[Tweet]:
        """
        Scrape tweets from all inspiration accounts.

        Args:
            accounts: List of account dicts with 'handle' and 'name' keys
            max_tweets_per_account: Max tweets per account

        Returns:
            Combined list of tweets from all accounts
        """
        accounts = accounts or self.inspiration_accounts
        all_tweets = []

        for account in accounts:
            try:
                tweets = await self.scrape_account(
                    handle=account["handle"],
                    max_tweets=max_tweets_per_account,
                )
                all_tweets.extend(tweets)
                print(f"Scraped {len(tweets)} tweets from @{account['handle']}")
            except Exception as e:
                print(f"Error scraping @{account['handle']}: {e}")
                continue

            # Small delay between accounts to be nice to the API
            await asyncio.sleep(1)

        return all_tweets

    def filter_and_rank_tweets(
        self,
        tweets: list[Tweet],
        min_engagement: int = 50,
        top_n: int = 20,
    ) -> list[Tweet]:
        """
        Filter and rank tweets by engagement.

        Args:
            tweets: List of tweets to filter
            min_engagement: Minimum engagement score
            top_n: Number of top tweets to return

        Returns:
            Filtered and ranked tweets
        """
        # Filter by minimum engagement
        filtered = [t for t in tweets if t.engagement_score >= min_engagement]

        # Sort by engagement
        filtered.sort(key=lambda t: t.engagement_score, reverse=True)

        return filtered[:top_n]


# Singleton instance
apify_client = ApifyClient()
