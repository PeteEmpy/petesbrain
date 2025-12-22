#!/usr/bin/env python3
"""
YouTube Video Monitor

Monitors YouTube channels for new videos in e-commerce, PPC, and digital marketing.
Extracts video metadata and transcripts, scores them for relevance, and adds
relevant ones to the knowledge base inbox for automated processing.

Runs automatically daily via LaunchAgent.
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
import anthropic
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain.nosync")
INBOX_DIR = PROJECT_ROOT / "roksys/knowledge-base/_inbox/documents"
STATE_FILE = PROJECT_ROOT / "data/state/youtube-monitor-state.json"
LOG_FILE = PROJECT_ROOT / "data/cache/youtube-monitor.log"

# Minimum relevance score (0-10) to import video
MIN_RELEVANCE_SCORE = 7

# YouTube API Key
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyDowdeXxrfH2TLrgxfxM70_javptOVYv4U')

# YouTube Channels - Load from config file
def load_channels():
    """Load channel list from channels.json config file"""
    channels_file = PROJECT_ROOT / "agents/youtube-monitor/channels.json"

    if channels_file.exists():
        with open(channels_file, 'r') as f:
            config = json.load(f)
            return {ch['name']: ch['channel_id'] for ch in config.get('channels', [])}

    # Fallback if config file doesn't exist
    return {
        "Common Thread Collective": "UCjtbFqsqVORPBJMein0zLWQ",
    }

YOUTUBE_CHANNELS = load_channels()

# How far back to check for new videos (in days)
LOOKBACK_DAYS = 60  # TEMPORARY: One-time historical import


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    print(log_entry.strip())

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_state():
    """Load previously processed video IDs"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_videos": [], "last_run": None}


def save_state(state):
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_channel_videos(channel_id, days_back=7):
    """Fetch recent videos from a YouTube channel"""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Calculate date threshold
        published_after = (datetime.now() - timedelta(days=days_back)).isoformat() + 'Z'

        # Search for videos
        search_request = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=50,
            order='date',
            type='video',
            publishedAfter=published_after
        )
        search_response = search_request.execute()

        videos = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']

            videos.append({
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'published_at': snippet['publishedAt'],
                'channel_title': snippet['channelTitle'],
                'url': f'https://www.youtube.com/watch?v={video_id}'
            })

        return videos

    except Exception as e:
        log_message(f"Error fetching videos from channel {channel_id}: {e}")
        return []


def get_video_transcript(video_id):
    """Extract transcript from a YouTube video"""
    try:
        # Configure Webshare residential proxy to avoid YouTube IP blocking
        proxy_config = WebshareProxyConfig(
            proxy_username=os.environ.get('WEBSHARE_USERNAME', 'uqrstquu'),
            proxy_password=os.environ.get('WEBSHARE_PASSWORD', '4j1lf3un5zp5'),
            filter_ip_locations=["gb", "us"]  # UK/US residential IPs only
        )

        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

        # Fetch transcript (prefer English)
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])

        # Get transcript data
        transcript_data = list(fetched_transcript)

        # Get full text
        full_text = ' '.join([snippet.text for snippet in transcript_data])

        return {
            'language': fetched_transcript.language,
            'is_auto_generated': fetched_transcript.is_generated,
            'full_text': full_text,
            'word_count': len(full_text.split())
        }

    except TranscriptsDisabled:
        log_message(f"Transcripts disabled for video {video_id}")
        return None
    except NoTranscriptFound:
        log_message(f"No transcript found for video {video_id}")
        return None
    except VideoUnavailable:
        log_message(f"Video {video_id} unavailable")
        return None
    except Exception as e:
        log_message(f"Error fetching transcript for {video_id}: {e}")
        return None


def score_video_relevance(title, description, transcript_preview, channel_name=""):
    """Use Claude to score video relevance for e-commerce/PPC knowledge base"""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return 0, None

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analyse this YouTube video for relevance to a Google Ads / PPC / E-commerce knowledge base.

Title: {title}
Channel: {channel_name}
Description: {description}
Transcript Preview (first 2000 chars): {transcript_preview[:2000]}

SCORING CRITERIA (0-10 scale):

9-10: CRITICAL - Must-have content
- Official Google Ads announcements or deep dives
- Original research with quantified e-commerce data
- Advanced strategic frameworks from industry leaders
- Major platform updates affecting campaign management

7-8: HIGH VALUE - Strongly relevant
- Tactical how-to guides for Google Ads/PPC
- E-commerce strategy insights with case studies
- Performance analysis methodologies
- Budget/bidding/targeting optimisation techniques

5-6: MODERATE - Possibly useful
- General e-commerce trends
- Adjacent topics (analytics, CRO, email marketing)
- Beginner-level PPC content
- Industry news without actionable insights

3-4: LOW - Tangentially related
- Generic marketing advice
- Platform overviews without depth
- Content for other industries

0-2: IRRELEVANT - Not useful
- Completely unrelated to e-commerce/PPC
- Personal vlogs, entertainment content
- Outdated tactics

Respond with JSON only:
{{
  "score": <number 0-10>,
  "reasoning": "<1-2 sentence explanation>",
  "category": "<Google Ads|Performance Max|E-commerce|Digital Marketing|Other>",
  "key_topics": ["<topic1>", "<topic2>", "<topic3>"]
}}"""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text.strip()

        # Remove markdown code blocks if present
        if result_text.startswith('```'):
            result_text = result_text.split('\n', 1)[1]
            result_text = result_text.rsplit('\n```', 1)[0]

        result = json.loads(result_text)

        score = float(result.get('score', 0))
        reasoning = result.get('reasoning', 'No reasoning provided')
        category = result.get('category', 'Other')
        key_topics = result.get('key_topics', [])

        return score, reasoning, category, key_topics

    except Exception as e:
        log_message(f"Error scoring video relevance: {e}")
        return 0, None, "Error", []


def create_knowledge_base_article(video_data, transcript_data, score, reasoning, category, key_topics):
    """Create a formatted markdown article for the knowledge base"""

    # Generate filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    title_slug = video_data['title'][:60].lower()
    title_slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in title_slug)
    title_slug = '-'.join(title_slug.split())

    filename = f"{date_str}_{category.lower().replace(' ', '-')}_{title_slug}.md"

    # Format published date
    try:
        pub_date = datetime.fromisoformat(video_data['published_at'].replace('Z', '+00:00'))
        published = pub_date.strftime("%a, %d %b %Y %H:%M:%S %z")
    except:
        published = video_data['published_at']

    # Create YAML frontmatter
    frontmatter = f"""---
source: {video_data['channel_title']} (YouTube)
url: {video_data['url']}
published: {published}
relevance_score: {int(score)}
primary_topic: {', '.join(key_topics[:3]) if key_topics else video_data['title']}
fetched: {datetime.now().isoformat()}
category: {category}
author: {video_data['channel_title']}
tags: YouTube, {', '.join(key_topics)}
video_id: {video_data['video_id']}
transcript_word_count: {transcript_data['word_count'] if transcript_data else 0}
transcript_language: {transcript_data['language'] if transcript_data else 'N/A'}
---

# {video_data['title']}

**Source**: {video_data['channel_title']} (YouTube)
**URL**: {video_data['url']}
**Published**: {published}
**Relevance Score**: {int(score)}/10
**Category**: {category}

## Description

{video_data['description']}

## AI Relevance Assessment

{reasoning}

**Key Topics**: {', '.join(key_topics)}

## Transcript

{transcript_data['full_text'] if transcript_data else 'Transcript not available'}

---

*Video added to knowledge base: {date_str}*
*Auto-generated by YouTube Monitor Agent*
"""

    return filename, frontmatter


def process_video(video, state):
    """Process a single video: check if new, extract transcript, score, and save"""

    video_id = video['video_id']

    # Skip if already processed
    if video_id in state['processed_videos']:
        return False

    log_message(f"Processing video: {video['title']}")

    # Get transcript
    transcript_data = get_video_transcript(video_id)

    if not transcript_data:
        log_message(f"Skipping {video['title']} - no transcript available")
        state['processed_videos'].append(video_id)
        return False

    # Score relevance
    score, reasoning, category, key_topics = score_video_relevance(
        video['title'],
        video['description'],
        transcript_data['full_text'],
        video['channel_title']
    )

    log_message(f"Score: {score}/10 - {reasoning}")

    # Check if meets threshold
    if score < MIN_RELEVANCE_SCORE:
        log_message(f"Below threshold ({MIN_RELEVANCE_SCORE}), skipping")
        state['processed_videos'].append(video_id)
        return False

    # Create knowledge base article
    filename, content = create_knowledge_base_article(
        video, transcript_data, score, reasoning, category, key_topics
    )

    # Save to inbox
    filepath = INBOX_DIR / filename
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    log_message(f"✅ Added to KB: {filename}")

    # Mark as processed
    state['processed_videos'].append(video_id)

    return True


def main():
    """Main execution"""
    log_message("=" * 60)
    log_message("YouTube Monitor Agent - Starting")
    log_message("=" * 60)

    # Load state
    state = load_state()

    total_added = 0

    # Process each channel
    for channel_name, channel_id in YOUTUBE_CHANNELS.items():
        log_message(f"\nChecking channel: {channel_name}")

        # Get recent videos
        videos = get_channel_videos(channel_id, days_back=LOOKBACK_DAYS)
        log_message(f"Found {len(videos)} recent videos")

        # Process each video
        for video in videos:
            try:
                if process_video(video, state):
                    total_added += 1
            except Exception as e:
                log_message(f"Error processing video {video['video_id']}: {e}")

            # Rate limiting: wait 10 minutes between videos to avoid YouTube blocks
            # PERMANENT - NEVER reduce below 5 minutes (YouTube will block IP)
            time.sleep(600)

    # Update state
    state['last_run'] = datetime.now().isoformat()

    # Keep only last 1000 processed videos to prevent state file growing forever
    if len(state['processed_videos']) > 1000:
        state['processed_videos'] = state['processed_videos'][-1000:]

    save_state(state)

    log_message(f"\n{'=' * 60}")
    log_message(f"YouTube Monitor Agent - Complete")
    log_message(f"Videos added to knowledge base: {total_added}")
    log_message(f"{'=' * 60}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        log_message(f"FATAL ERROR: {e}")
        import traceback
        log_message(traceback.format_exc())
        sys.exit(1)
