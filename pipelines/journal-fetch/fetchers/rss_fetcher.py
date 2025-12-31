"""
RSS Feed Fetcher
Fetches articles from medical journal RSS feeds using feedparser.
"""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import sys
sys.path.insert(0, '..')
from config import RSS_FEEDS, RSS_FETCH_TIMEOUT


def parse_date(entry) -> Optional[str]:
    """Extract publication date from RSS entry."""
    date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
    
    for field in date_fields:
        if hasattr(entry, field) and getattr(entry, field):
            try:
                parsed = getattr(entry, field)
                return datetime(*parsed[:6]).strftime('%Y-%m-%d')
            except:
                pass
    
    # Try string parsing as fallback
    for field in ['published', 'updated', 'created']:
        if hasattr(entry, field) and getattr(entry, field):
            return getattr(entry, field)[:10]  # Just get date part
    
    return datetime.now().strftime('%Y-%m-%d')


def extract_abstract(entry) -> str:
    """Extract abstract/summary from RSS entry."""
    # Try different fields for abstract content
    if hasattr(entry, 'summary') and entry.summary:
        return entry.summary
    if hasattr(entry, 'description') and entry.description:
        return entry.description
    if hasattr(entry, 'content') and entry.content:
        # content is usually a list
        if isinstance(entry.content, list) and len(entry.content) > 0:
            return entry.content[0].get('value', '')
    return ""


def extract_authors(entry) -> str:
    """Extract author names from RSS entry."""
    if hasattr(entry, 'authors') and entry.authors:
        if isinstance(entry.authors, list):
            names = [a.get('name', '') for a in entry.authors if a.get('name')]
            if names:
                if len(names) > 3:
                    return f"{names[0]}, {names[1]}, et al"
                return ", ".join(names)
    if hasattr(entry, 'author') and entry.author:
        return entry.author
    return ""


def extract_doi(entry) -> str:
    """Extract DOI from RSS entry."""
    # Check link for DOI
    if hasattr(entry, 'link') and entry.link:
        if 'doi.org' in entry.link:
            return entry.link.split('doi.org/')[-1]
    
    # Check id field
    if hasattr(entry, 'id') and entry.id:
        if 'doi' in entry.id.lower():
            parts = entry.id.split('/')
            if len(parts) >= 2:
                return '/'.join(parts[-2:])
    
    return ""


def fetch_single_feed(feed_config: Dict) -> List[Dict]:
    """
    Fetch articles from a single RSS feed.
    
    Args:
        feed_config: Dictionary with id, name, url, tier
        
    Returns:
        List of article dictionaries
    """
    articles = []
    
    try:
        # Parse the feed with timeout
        feed = feedparser.parse(
            feed_config['url'],
            request_headers={'User-Agent': 'Medical-Content-Engine/1.0'}
        )
        
        # Check for errors
        if feed.bozo and not feed.entries:
            print(f"  ⚠ {feed_config['name']}: Feed parsing error")
            return []
        
        # Process entries (limit to recent ones)
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for entry in feed.entries[:20]:  # Limit to first 20 entries
            try:
                article = {
                    "source": "rss",
                    "title": entry.get('title', 'Untitled'),
                    "abstract": extract_abstract(entry),
                    "journal": feed_config['name'],
                    "tier": feed_config['tier'],
                    "pub_date": parse_date(entry),
                    "authors": extract_authors(entry),
                    "url": entry.get('link', ''),
                    "doi": extract_doi(entry),
                    "feed_id": feed_config['id']
                }
                
                # Only include if we have a title and some content
                if article['title'] and article['title'] != 'Untitled':
                    articles.append(article)
                    
            except Exception as e:
                # Skip problematic entries silently
                continue
        
        if articles:
            print(f"  ✓ {feed_config['name']}: {len(articles)} articles")
        else:
            print(f"  ○ {feed_config['name']}: No articles")
            
    except Exception as e:
        print(f"  ✗ {feed_config['name']}: {str(e)[:50]}")
    
    return articles


def fetch_all_rss(feeds: List[Dict] = None, max_per_feed: int = 10) -> List[Dict]:
    """
    Fetch articles from all configured RSS feeds.
    
    Args:
        feeds: Optional list of feed configs. Uses RSS_FEEDS from config if not provided.
        max_per_feed: Maximum articles to return per feed
        
    Returns:
        List of all fetched articles
    """
    if feeds is None:
        feeds = RSS_FEEDS
    
    print(f"\n📡 Fetching RSS feeds ({len(feeds)} sources)...")
    print("-" * 40)
    
    all_articles = []
    successful_feeds = 0
    
    for feed in feeds:
        articles = fetch_single_feed(feed)
        if articles:
            successful_feeds += 1
            # Limit per feed
            all_articles.extend(articles[:max_per_feed])
        
        # Small delay to be nice to servers
        time.sleep(0.5)
    
    print("-" * 40)
    print(f"📊 Total: {len(all_articles)} articles from {successful_feeds}/{len(feeds)} feeds\n")
    
    return all_articles


def fetch_feeds_by_tier(tier: str) -> List[Dict]:
    """
    Fetch articles from feeds of a specific tier only.
    
    Args:
        tier: One of 'general', 'cardiology', 'interventional', 'heartfailure', 'imaging', 'prevention', 'research'
        
    Returns:
        List of articles from that tier
    """
    tier_feeds = [f for f in RSS_FEEDS if f['tier'] == tier]
    return fetch_all_rss(feeds=tier_feeds)


if __name__ == "__main__":
    # Test the fetcher
    articles = fetch_all_rss()
    
    print("\n📝 Sample articles:")
    for article in articles[:3]:
        print(f"\n  Title: {article['title'][:60]}...")
        print(f"  Journal: {article['journal']}")
        print(f"  Abstract: {article['abstract'][:100]}..." if article['abstract'] else "  Abstract: N/A")
