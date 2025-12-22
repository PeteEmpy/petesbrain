from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import sys
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('youtube_server')

mcp = FastMCP("YouTube Tools")

# Server startup
logger.info("Starting YouTube MCP Server...")

def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return as-is if already an ID.

    Supports formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - VIDEO_ID (direct ID)
    """
    if 'youtube.com/watch?v=' in url_or_id:
        # Extract from full URL
        return url_or_id.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url_or_id:
        # Extract from short URL
        return url_or_id.split('youtu.be/')[1].split('?')[0]
    else:
        # Assume it's already a video ID
        return url_or_id

@mcp.tool
def get_video_info(
    video_url: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get metadata for a YouTube video including title, channel, description, and publish date.

    Args:
        video_url: YouTube video URL (https://www.youtube.com/watch?v=...) or video ID
        ctx: MCP context for logging

    Returns:
        Dictionary with video metadata: title, channelTitle, description, publishedAt, tags, etc.

    Example:
        get_video_info("https://www.youtube.com/watch?v=YFYwZ-kG_5U")
    """
    if ctx:
        ctx.info(f"Fetching video info for {video_url}...")

    try:
        # Import googleapiclient lazily (only when tool is called)
        from googleapiclient.discovery import build

        # Extract video ID
        video_id = extract_video_id(video_url)

        # Get API key from environment
        api_key = os.environ.get('YOUTUBE_API_KEY')
        if not api_key:
            raise Exception("YOUTUBE_API_KEY not found in environment variables")

        # Build YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Request video details
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        response = request.execute()

        if not response.get('items'):
            raise Exception(f"Video not found: {video_id}")

        video = response['items'][0]
        snippet = video['snippet']
        content_details = video['contentDetails']
        statistics = video['statistics']

        result = {
            'videoId': video_id,
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'title': snippet.get('title'),
            'channelTitle': snippet.get('channelTitle'),
            'channelId': snippet.get('channelId'),
            'description': snippet.get('description'),
            'publishedAt': snippet.get('publishedAt'),
            'tags': snippet.get('tags', []),
            'categoryId': snippet.get('categoryId'),
            'duration': content_details.get('duration'),
            'viewCount': statistics.get('viewCount'),
            'likeCount': statistics.get('likeCount'),
            'commentCount': statistics.get('commentCount'),
            'thumbnails': snippet.get('thumbnails', {})
        }

        if ctx:
            ctx.info(f"Successfully fetched info for: {result['title']}")

        return result

    except Exception as e:
        logger.error(f"Error fetching video info: {str(e)}")
        if ctx:
            ctx.error(f"Error: {str(e)}")
        raise

@mcp.tool
def get_transcript(
    video_url: str,
    languages: List[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get transcript/captions for a YouTube video.

    Args:
        video_url: YouTube video URL (https://www.youtube.com/watch?v=...) or video ID
        languages: Optional list of language codes to try (e.g., ['en', 'en-GB']). Defaults to ['en']
        ctx: MCP context for logging

    Returns:
        Dictionary with transcript text, language, and whether it's auto-generated

    Example:
        get_transcript("https://www.youtube.com/watch?v=YFYwZ-kG_5U")
        get_transcript("YFYwZ-kG_5U", languages=['en', 'en-GB'])
    """
    if ctx:
        ctx.info(f"Fetching transcript for {video_url}...")

    # Default to English if no languages specified
    if languages is None:
        languages = ['en']

    try:
        # Extract video ID
        video_id = extract_video_id(video_url)

        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to find transcript in preferred languages
        transcript = None
        is_auto_generated = False
        language_code = None

        # First try manually created transcripts
        try:
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    language_code = lang
                    is_auto_generated = False
                    break
                except NoTranscriptFound:
                    continue
        except Exception:
            pass

        # If no manual transcript, try auto-generated
        if transcript is None:
            try:
                for lang in languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        language_code = lang
                        is_auto_generated = True
                        break
                    except NoTranscriptFound:
                        continue
            except Exception:
                pass

        # If still no transcript, just get any available transcript
        if transcript is None:
            available_transcripts = list(transcript_list)
            if not available_transcripts:
                raise Exception("No transcripts available for this video")

            transcript = available_transcripts[0]
            language_code = transcript.language_code
            is_auto_generated = transcript.is_generated

        # Fetch the transcript text
        transcript_data = transcript.fetch()

        # Combine all transcript segments into full text
        full_text = ' '.join([entry['text'] for entry in transcript_data])

        # Also provide structured segments for detailed analysis
        segments = [
            {
                'text': entry['text'],
                'start': entry['start'],
                'duration': entry['duration']
            }
            for entry in transcript_data
        ]

        result = {
            'videoId': video_id,
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'language': language_code,
            'isAutoGenerated': is_auto_generated,
            'fullText': full_text,
            'segments': segments,
            'segmentCount': len(segments),
            'wordCount': len(full_text.split())
        }

        if ctx:
            ctx.info(f"Successfully fetched transcript ({len(segments)} segments, {result['wordCount']} words)")

        return result

    except TranscriptsDisabled:
        error_msg = "Transcripts are disabled for this video"
        logger.error(error_msg)
        if ctx:
            ctx.error(error_msg)
        raise Exception(error_msg)

    except NoTranscriptFound:
        error_msg = f"No transcript found in languages: {languages}"
        logger.error(error_msg)
        if ctx:
            ctx.error(error_msg)
        raise Exception(error_msg)

    except VideoUnavailable:
        error_msg = "Video is unavailable"
        logger.error(error_msg)
        if ctx:
            ctx.error(error_msg)
        raise Exception(error_msg)

    except Exception as e:
        logger.error(f"Error fetching transcript: {str(e)}")
        if ctx:
            ctx.error(f"Error: {str(e)}")
        raise
