from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import logging
import requests
from datetime import datetime

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Get environment variables
BING_API_KEY = os.environ.get("BING_API_KEY")
BING_API_ENDPOINT = os.environ.get("BING_API_ENDPOINT", "https://api.bing.microsoft.com/v7.0")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('bing_search_server')

mcp = FastMCP("Bing Search Tools")

# Server startup
logger.info("Starting Bing Search MCP Server...")

def make_api_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict:
    """
    Make a request to Bing Search API.
    
    Args:
        endpoint: API endpoint (e.g., 'search', 'images', 'news', 'videos')
        params: Query parameters
        
    Returns:
        Dict: API response
    """
    if not BING_API_KEY:
        raise ValueError("BING_API_KEY must be set in environment variables.")
    
    url = f"{BING_API_ENDPOINT}/{endpoint}"
    headers = {
        'Ocp-Apim-Subscription-Key': BING_API_KEY,
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params or {})
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        raise

@mcp.tool
def web_search(
    query: str,
    count: Optional[int] = 10,
    offset: Optional[int] = 0,
    market: Optional[str] = "en-US",
    safe_search: Optional[str] = "Moderate",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Search the web using Bing Search API.
    
    Args:
        query: Search query string
        count: Number of results to return (1-50, default: 10)
        offset: Number of results to skip (default: 0)
        market: Market code (e.g., 'en-US', 'en-GB', default: 'en-US')
        safe_search: Safe search level ('Off', 'Moderate', 'Strict', default: 'Moderate')
    """
    if ctx:
        ctx.info(f"Searching web for: '{query}'")
    
    try:
        params = {
            'q': query,
            'count': min(max(count or 10, 1), 50),  # Clamp between 1-50
            'offset': max(offset or 0, 0),
            'mkt': market,
            'safeSearch': safe_search
        }
        
        response = make_api_request('search', params)
        
        results = []
        if 'webPages' in response and 'value' in response['webPages']:
            for item in response['webPages']['value']:
                results.append({
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayUrl', ''),
                    'date_published': item.get('datePublished'),
                    'date_last_crawled': item.get('dateLastCrawled')
                })
        
        total_estimated_matches = response.get('webPages', {}).get('totalEstimatedMatches', 0)
        
        if ctx:
            ctx.info(f"Found {len(results)} result(s) (estimated {total_estimated_matches} total)")
        
        return {
            'query': query,
            'results': results,
            'count': len(results),
            'total_estimated_matches': total_estimated_matches,
            'market': market
        }
        
    except Exception as e:
        if ctx:
            ctx.error(f"Failed to search web: {str(e)}")
        raise

@mcp.tool
def image_search(
    query: str,
    count: Optional[int] = 20,
    offset: Optional[int] = 0,
    market: Optional[str] = "en-US",
    image_type: Optional[str] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    license: Optional[str] = None,
    safe_search: Optional[str] = "Moderate",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Search for images using Bing Image Search API.
    
    Args:
        query: Search query string
        count: Number of results to return (1-150, default: 20)
        offset: Number of results to skip (default: 0)
        market: Market code (e.g., 'en-US', 'en-GB', default: 'en-US')
        image_type: Image type ('AnimatedGif', 'Clipart', 'Line', 'Photo', 'Shopping', 'Transparent')
        size: Image size ('Small', 'Medium', 'Large', 'Wallpaper', 'All')
        color: Color filter ('ColorOnly', 'Monochrome', 'Black', 'Blue', 'Red', 'Yellow', 'Green', 'Orange', 'Pink', 'Purple', 'Brown', 'Grey', 'White', 'Teal')
        license: License filter ('Public', 'Share', 'ShareCommercially', 'Modify', 'ModifyCommercially', 'All')
        safe_search: Safe search level ('Off', 'Moderate', 'Strict', default: 'Moderate')
    """
    if ctx:
        ctx.info(f"Searching images for: '{query}'")
    
    try:
        params = {
            'q': query,
            'count': min(max(count or 20, 1), 150),  # Clamp between 1-150
            'offset': max(offset or 0, 0),
            'mkt': market,
            'safeSearch': safe_search
        }
        
        if image_type:
            params['imageType'] = image_type
        if size:
            params['size'] = size
        if color:
            params['color'] = color
        if license:
            params['license'] = license
        
        response = make_api_request('images/search', params)
        
        results = []
        if 'value' in response:
            for item in response['value']:
                results.append({
                    'name': item.get('name', ''),
                    'content_url': item.get('contentUrl', ''),
                    'thumbnail_url': item.get('thumbnailUrl', ''),
                    'host_page_url': item.get('hostPageUrl', ''),
                    'width': item.get('width'),
                    'height': item.get('height'),
                    'content_size': item.get('contentSize'),
                    'encoding_format': item.get('encodingFormat'),
                    'date_published': item.get('datePublished')
                })
        
        total_estimated_matches = response.get('totalEstimatedMatches', 0)
        
        if ctx:
            ctx.info(f"Found {len(results)} image(s) (estimated {total_estimated_matches} total)")
        
        return {
            'query': query,
            'results': results,
            'count': len(results),
            'total_estimated_matches': total_estimated_matches,
            'market': market
        }
        
    except Exception as e:
        if ctx:
            ctx.error(f"Failed to search images: {str(e)}")
        raise

@mcp.tool
def news_search(
    query: str,
    count: Optional[int] = 10,
    offset: Optional[int] = 0,
    market: Optional[str] = "en-US",
    category: Optional[str] = None,
    safe_search: Optional[str] = "Moderate",
    sort_by: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Search for news articles using Bing News Search API.
    
    Args:
        query: Search query string
        count: Number of results to return (1-100, default: 10)
        offset: Number of results to skip (default: 0)
        market: Market code (e.g., 'en-US', 'en-GB', default: 'en-US')
        category: News category ('Business', 'Entertainment', 'Health', 'Politics', 'ScienceAndTechnology', 'Sports', 'US', 'World', 'Entertainment_Music', 'Entertainment_Tv')
        safe_search: Safe search level ('Off', 'Moderate', 'Strict', default: 'Moderate')
        sort_by: Sort order ('Date' for newest first, 'Relevance' for most relevant)
    """
    if ctx:
        ctx.info(f"Searching news for: '{query}'")
    
    try:
        params = {
            'q': query,
            'count': min(max(count or 10, 1), 100),  # Clamp between 1-100
            'offset': max(offset or 0, 0),
            'mkt': market,
            'safeSearch': safe_search
        }
        
        if category:
            params['category'] = category
        if sort_by:
            params['sortBy'] = sort_by
        
        response = make_api_request('news/search', params)
        
        results = []
        if 'value' in response:
            for item in response['value']:
                results.append({
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                    'description': item.get('description', ''),
                    'provider': item.get('provider', []),
                    'date_published': item.get('datePublished'),
                    'category': item.get('category'),
                    'headline': item.get('headline', ''),
                    'image': item.get('image', {})
                })
        
        total_estimated_matches = response.get('totalEstimatedMatches', 0)
        
        if ctx:
            ctx.info(f"Found {len(results)} news article(s) (estimated {total_estimated_matches} total)")
        
        return {
            'query': query,
            'results': results,
            'count': len(results),
            'total_estimated_matches': total_estimated_matches,
            'market': market
        }
        
    except Exception as e:
        if ctx:
            ctx.error(f"Failed to search news: {str(e)}")
        raise

@mcp.tool
def video_search(
    query: str,
    count: Optional[int] = 20,
    offset: Optional[int] = 0,
    market: Optional[str] = "en-US",
    resolution: Optional[str] = None,
    video_length: Optional[str] = None,
    pricing: Optional[str] = None,
    safe_search: Optional[str] = "Moderate",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Search for videos using Bing Video Search API.
    
    Args:
        query: Search query string
        count: Number of results to return (1-105, default: 20)
        offset: Number of results to skip (default: 0)
        market: Market code (e.g., 'en-US', 'en-GB', default: 'en-US')
        resolution: Video resolution ('All', '480p', '720p', '1080p')
        video_length: Video length ('All', 'Short' (< 5 min), 'Medium' (5-20 min), 'Long' (> 20 min))
        pricing: Pricing filter ('All', 'Free', 'Paid')
        safe_search: Safe search level ('Off', 'Moderate', 'Strict', default: 'Moderate')
    """
    if ctx:
        ctx.info(f"Searching videos for: '{query}'")
    
    try:
        params = {
            'q': query,
            'count': min(max(count or 20, 1), 105),  # Clamp between 1-105
            'offset': max(offset or 0, 0),
            'mkt': market,
            'safeSearch': safe_search
        }
        
        if resolution:
            params['resolution'] = resolution
        if video_length:
            params['videoLength'] = video_length
        if pricing:
            params['pricing'] = pricing
        
        response = make_api_request('videos/search', params)
        
        results = []
        if 'value' in response:
            for item in response['value']:
                results.append({
                    'name': item.get('name', ''),
                    'content_url': item.get('contentUrl', ''),
                    'host_page_url': item.get('hostPageUrl', ''),
                    'thumbnail_url': item.get('thumbnailUrl', {}).get('contentUrl', ''),
                    'duration': item.get('duration'),
                    'view_count': item.get('viewCount'),
                    'publisher': item.get('publisher', []),
                    'date_published': item.get('datePublished'),
                    'width': item.get('width'),
                    'height': item.get('height')
                })
        
        total_estimated_matches = response.get('totalEstimatedMatches', 0)
        
        if ctx:
            ctx.info(f"Found {len(results)} video(s) (estimated {total_estimated_matches} total)")
        
        return {
            'query': query,
            'results': results,
            'count': len(results),
            'total_estimated_matches': total_estimated_matches,
            'market': market
        }
        
    except Exception as e:
        if ctx:
            ctx.error(f"Failed to search videos: {str(e)}")
        raise

@mcp.tool
def trending_topics(
    market: Optional[str] = "en-US",
    category: Optional[str] = None,
    count: Optional[int] = 10,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get trending topics using Bing Trending Topics API.
    
    Args:
        market: Market code (e.g., 'en-US', 'en-GB', default: 'en-US')
        category: Category filter ('Business', 'Entertainment', 'Health', 'Politics', 'ScienceAndTechnology', 'Sports', 'US', 'World')
        count: Number of topics to return (1-20, default: 10)
    """
    if ctx:
        ctx.info(f"Fetching trending topics for market: {market}")
    
    try:
        params = {
            'mkt': market,
            'count': min(max(count or 10, 1), 20)  # Clamp between 1-20
        }
        
        if category:
            params['category'] = category
        
        response = make_api_request('news/trendingtopics', params)
        
        topics = []
        if 'value' in response:
            for item in response['value']:
                topics.append({
                    'name': item.get('name', ''),
                    'query': item.get('query', {}).get('text', ''),
                    'image': item.get('image', {}),
                    'news_search_url': item.get('newsSearchUrl', ''),
                    'web_search_url': item.get('webSearchUrl', '')
                })
        
        if ctx:
            ctx.info(f"Found {len(topics)} trending topic(s)")
        
        return {
            'market': market,
            'topics': topics,
            'count': len(topics)
        }
        
    except Exception as e:
        if ctx:
            ctx.error(f"Failed to get trending topics: {str(e)}")
        raise

if __name__ == "__main__":
    mcp.run()

