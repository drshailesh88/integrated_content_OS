#!/usr/bin/env python3
"""
YouTube Research Engine for Dr. Shailesh Content System
Researches content ideas using YouTube Data API and yt-dlp

Usage:
    python youtube_researcher.py --idea "statin side effects" --output ./output/
    python youtube_researcher.py --batch ./data/seed-ideas.json --top 50
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# Optional: YouTube Data API
try:
    from googleapiclient.discovery import build
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("Warning: google-api-python-client not installed. Using yt-dlp only.")

load_dotenv()

@dataclass
class VideoData:
    """Data structure for a single video"""
    video_id: str
    title: str
    channel: str
    channel_id: str
    views: int
    likes: int
    comments: int
    published_at: str
    duration: str
    description: str
    tags: List[str]
    transcript: Optional[str] = None
    top_comments: Optional[List[str]] = None


@dataclass
class ResearchResult:
    """Research result for a single idea"""
    idea_id: str
    seed_idea: str
    modifier: str
    search_query: str
    researched_at: str
    videos: List[VideoData]
    total_views: int
    avg_views: float
    comment_themes: List[str]
    gap_analysis: Dict
    scores: Dict


class YouTubeResearcher:
    """Main research engine class"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.youtube = None

        if YOUTUBE_API_AVAILABLE and self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search YouTube for videos matching query"""

        if self.youtube:
            return self._search_with_api(query, max_results)
        else:
            return self._search_with_ytdlp(query, max_results)

    def _search_with_api(self, query: str, max_results: int) -> List[Dict]:
        """Search using YouTube Data API"""
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                relevanceLanguage='hi',  # Prioritize Hindi content
                order='relevance'
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

            if not video_ids:
                return []

            # Get detailed stats
            videos_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()

            results = []
            for item in videos_response.get('items', []):
                snippet = item['snippet']
                stats = item.get('statistics', {})

                results.append({
                    'video_id': item['id'],
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'channel_id': snippet['channelId'],
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'published_at': snippet['publishedAt'],
                    'duration': item['contentDetails']['duration'],
                    'description': snippet.get('description', ''),
                    'tags': snippet.get('tags', [])
                })

            return results

        except Exception as e:
            print(f"API search error: {e}")
            return self._search_with_ytdlp(query, max_results)

    def _search_with_ytdlp(self, query: str, max_results: int) -> List[Dict]:
        """Search using yt-dlp (fallback)"""
        try:
            cmd = [
                'yt-dlp',
                f'ytsearch{max_results}:{query}',
                '--dump-json',
                '--flat-playlist',
                '--no-warnings'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                print(f"yt-dlp search error: {result.stderr}")
                return []

            videos = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        videos.append({
                            'video_id': data.get('id', ''),
                            'title': data.get('title', ''),
                            'channel': data.get('channel', data.get('uploader', '')),
                            'channel_id': data.get('channel_id', ''),
                            'views': data.get('view_count', 0) or 0,
                            'likes': data.get('like_count', 0) or 0,
                            'comments': data.get('comment_count', 0) or 0,
                            'published_at': data.get('upload_date', ''),
                            'duration': str(data.get('duration', 0)),
                            'description': data.get('description', ''),
                            'tags': data.get('tags', []) or []
                        })
                    except json.JSONDecodeError:
                        continue

            return videos

        except subprocess.TimeoutExpired:
            print("yt-dlp search timed out")
            return []
        except Exception as e:
            print(f"yt-dlp search error: {e}")
            return []

    def get_transcript(self, video_id: str) -> Optional[str]:
        """Get video transcript using yt-dlp"""
        try:
            cmd = [
                'yt-dlp',
                f'https://www.youtube.com/watch?v={video_id}',
                '--write-auto-sub',
                '--sub-lang', 'en,hi',
                '--skip-download',
                '--output', '/tmp/%(id)s',
                '--no-warnings'
            ]

            subprocess.run(cmd, capture_output=True, timeout=30)

            # Try to read subtitle file
            for ext in ['.en.vtt', '.hi.vtt', '.en.srt', '.hi.srt']:
                sub_file = f'/tmp/{video_id}{ext}'
                if os.path.exists(sub_file):
                    with open(sub_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    os.remove(sub_file)
                    return self._clean_transcript(content)

            return None

        except Exception as e:
            print(f"Transcript error for {video_id}: {e}")
            return None

    def _clean_transcript(self, raw: str) -> str:
        """Clean VTT/SRT transcript to plain text"""
        lines = raw.split('\n')
        text_lines = []

        for line in lines:
            line = line.strip()
            # Skip timing lines, headers, etc.
            if not line or '-->' in line or line.startswith('WEBVTT') or line.isdigit():
                continue
            # Remove HTML tags
            import re
            line = re.sub(r'<[^>]+>', '', line)
            if line and line not in text_lines[-1:]:  # Avoid duplicates
                text_lines.append(line)

        return ' '.join(text_lines)

    def get_comments(self, video_id: str, max_comments: int = 50) -> List[str]:
        """Get top comments for a video"""
        if not self.youtube:
            return []

        try:
            response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_comments,
                order='relevance',
                textFormat='plainText'
            ).execute()

            comments = []
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            return comments

        except Exception as e:
            print(f"Comments error for {video_id}: {e}")
            return []

    def research_idea(self, seed_idea: str, modifier: str = "",
                     idea_id: str = None) -> ResearchResult:
        """Full research pipeline for a single idea"""

        # Build search query
        query = f"{seed_idea} {modifier}".strip()
        search_query = f"{query} heart health cardiology Hindi"

        print(f"Researching: {query}")

        # Search videos
        raw_videos = self.search_videos(search_query, max_results=10)

        # Enrich with transcripts and comments (top 3 only to save quota)
        videos = []
        for i, v in enumerate(raw_videos):
            video = VideoData(**v)

            if i < 3:  # Only get details for top 3
                video.transcript = self.get_transcript(v['video_id'])
                video.top_comments = self.get_comments(v['video_id'], 20)

            videos.append(video)

        # Calculate metrics
        total_views = sum(v.views for v in videos)
        avg_views = total_views / len(videos) if videos else 0

        # Basic gap analysis
        gap_analysis = self._analyze_gaps(videos, seed_idea)

        # Score the idea
        scores = self._score_idea(videos, gap_analysis)

        # Extract comment themes
        all_comments = []
        for v in videos:
            if v.top_comments:
                all_comments.extend(v.top_comments)
        comment_themes = self._extract_themes(all_comments)

        return ResearchResult(
            idea_id=idea_id or f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            seed_idea=seed_idea,
            modifier=modifier,
            search_query=search_query,
            researched_at=datetime.now().isoformat(),
            videos=[asdict(v) for v in videos],
            total_views=total_views,
            avg_views=avg_views,
            comment_themes=comment_themes,
            gap_analysis=gap_analysis,
            scores=scores
        )

    def _analyze_gaps(self, videos: List[VideoData], seed_idea: str) -> Dict:
        """Identify content gaps in existing videos"""

        gaps = {
            'hinglish_gap': True,  # Assume gap until proven otherwise
            'recency_gap': True,
            'depth_gap': True,
            'authority_gap': True,
            'india_context_gap': True
        }

        one_year_ago = datetime.now() - timedelta(days=365)

        for v in videos:
            title_lower = v.title.lower()

            # Check for Hindi/Hinglish content
            if any(hindi_word in title_lower for hindi_word in ['kaise', 'kya', 'kyun', 'hai', 'nahi']):
                gaps['hinglish_gap'] = False

            # Check recency
            try:
                pub_date = datetime.fromisoformat(v.published_at.replace('Z', '+00:00'))
                if pub_date.replace(tzinfo=None) > one_year_ago:
                    gaps['recency_gap'] = False
            except:
                pass

            # Check for doctor/medical authority
            if any(word in v.channel.lower() for word in ['dr', 'doctor', 'medical', 'health']):
                gaps['authority_gap'] = False

            # Check for India context
            if any(word in title_lower for word in ['india', 'indian', 'desi', 'hindi']):
                gaps['india_context_gap'] = False

        # Count gaps
        gaps['gap_count'] = sum(1 for v in gaps.values() if v is True and isinstance(v, bool))

        return gaps

    def _score_idea(self, videos: List[VideoData], gap_analysis: Dict) -> Dict:
        """Score the idea on multiple dimensions"""

        if not videos:
            return {'demand': 0, 'gap': 0, 'competition': 0, 'total': 0}

        # Demand score (based on views)
        total_views = sum(v.views for v in videos)
        if total_views > 2000000:
            demand = 10
        elif total_views > 1000000:
            demand = 8
        elif total_views > 500000:
            demand = 6
        elif total_views > 100000:
            demand = 4
        else:
            demand = 2

        # Gap score (more gaps = better opportunity)
        gap_count = gap_analysis.get('gap_count', 0)
        gap = min(gap_count * 2, 10)

        # Competition score (inverse - less competition = higher score)
        avg_views = total_views / len(videos)
        if avg_views < 50000:
            competition = 8  # Low competition, good
        elif avg_views < 200000:
            competition = 6
        elif avg_views < 500000:
            competition = 4
        else:
            competition = 2  # High competition, harder

        # Total score
        total = (demand * 0.3) + (gap * 0.4) + (competition * 0.3)

        return {
            'demand': demand,
            'gap': gap,
            'competition': competition,
            'total': round(total, 2)
        }

    def _extract_themes(self, comments: List[str], max_themes: int = 5) -> List[str]:
        """Extract common themes from comments (simple keyword approach)"""

        if not comments:
            return []

        # Common question patterns
        question_words = ['kya', 'kaise', 'kyun', 'kab', 'kitna', 'what', 'how', 'why', 'when']

        themes = []
        for comment in comments[:30]:  # Sample first 30
            comment_lower = comment.lower()

            # Check if it's a question
            if '?' in comment or any(qw in comment_lower for qw in question_words):
                # Truncate long comments
                theme = comment[:100] + '...' if len(comment) > 100 else comment
                if theme not in themes:
                    themes.append(theme)

        return themes[:max_themes]


def batch_research(ideas_file: str, output_dir: str, top_n: int = None):
    """Process multiple ideas from a JSON file"""

    with open(ideas_file, 'r', encoding='utf-8') as f:
        ideas = json.load(f)

    if top_n:
        ideas = ideas[:top_n]

    researcher = YouTubeResearcher()
    results = []

    for i, idea in enumerate(ideas, 1):
        print(f"\n[{i}/{len(ideas)}] Processing...")

        result = researcher.research_idea(
            seed_idea=idea.get('seed_idea', idea.get('title', '')),
            modifier=idea.get('modifier', ''),
            idea_id=idea.get('id', f'idea_{i:04d}')
        )

        results.append(asdict(result))

        # Save incrementally
        output_file = os.path.join(output_dir, 'research_results.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    # Generate ranked list
    ranked = sorted(results, key=lambda x: x['scores']['total'], reverse=True)

    ranked_file = os.path.join(output_dir, 'ranked_ideas.json')
    with open(ranked_file, 'w', encoding='utf-8') as f:
        json.dump(ranked, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Research complete! {len(results)} ideas processed.")
    print(f"   Results: {output_file}")
    print(f"   Ranked: {ranked_file}")

    return ranked


def main():
    parser = argparse.ArgumentParser(description='YouTube Research Engine')
    parser.add_argument('--idea', help='Single idea to research')
    parser.add_argument('--modifier', default='', help='Modifier for the idea')
    parser.add_argument('--batch', help='JSON file with multiple ideas')
    parser.add_argument('--top', type=int, help='Only process top N ideas')
    parser.add_argument('--output', default='./output/', help='Output directory')

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.batch:
        batch_research(args.batch, args.output, args.top)
    elif args.idea:
        researcher = YouTubeResearcher()
        result = researcher.research_idea(args.idea, args.modifier)

        output_file = os.path.join(args.output, f'{result.idea_id}.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)

        print(f"\n✅ Research complete!")
        print(f"   Score: {result.scores['total']}/10")
        print(f"   Demand: {result.scores['demand']}/10")
        print(f"   Gap: {result.scores['gap']}/10")
        print(f"   Output: {output_file}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
