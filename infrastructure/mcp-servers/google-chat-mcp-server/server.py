from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import sys
import logging
import requests

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# OAuth module will be imported lazily inside tool functions to prevent
# startup popups when tokens are expired

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('google_chat_server')

mcp = FastMCP("Google Chat Controller")

# Server startup
logger.info("Starting Google Chat MCP Server...")

# Base API URL
BASE_URL = "https://chat.googleapis.com/v1"


@mcp.tool
def list_spaces(
    page_size: int = 100,
    page_token: Optional[str] = None,
    filter_query: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """List all Google Chat spaces (conversations) accessible to the authenticated user.

    Args:
        page_size: Number of spaces to return (default: 100, max: 1000)
        page_token: Token for pagination (from previous response)
        filter_query: Optional filter (e.g., "spaceType = SPACE")

    Returns:
        Dictionary with list of spaces and optional nextPageToken for pagination
        Each space includes: name, displayName, spaceType, spaceThreadingSettings
    """
    if ctx:
        ctx.info(f"Listing Google Chat spaces (page_size: {page_size})...")

    try:
        # Import OAuth module lazily (only when tool is actually called)
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter_query:
            params["filter"] = filter_query

        response = requests.get(f"{BASE_URL}/spaces", headers=headers, params=params)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to list spaces: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            num_spaces = len(result.get('spaces', []))
            ctx.info(f"Successfully retrieved {num_spaces} spaces")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error listing spaces: {str(e)}")
        raise


@mcp.tool
def get_space(
    space_name: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get details for a specific Google Chat space.

    Args:
        space_name: Space resource name (e.g., "spaces/AAAAAAAAAAA")

    Returns:
        Space details including name, displayName, spaceType, createTime, etc.
    """
    if ctx:
        ctx.info(f"Getting space details for {space_name}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        response = requests.get(f"{BASE_URL}/{space_name}", headers=headers)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to get space: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            ctx.info(f"Successfully retrieved space: {result.get('displayName', 'N/A')}")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error getting space: {str(e)}")
        raise


@mcp.tool
def list_messages(
    space_name: str,
    page_size: int = 100,
    page_token: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """List messages in a Google Chat space.

    Args:
        space_name: Space resource name (e.g., "spaces/AAAAAAAAAAA")
        page_size: Number of messages to return (default: 100, max: 1000)
        page_token: Token for pagination (from previous response)
        filter_query: Optional filter (e.g., "createTime > '2025-01-01T00:00:00Z'")
        order_by: Optional ordering (e.g., "createTime desc")

    Returns:
        Dictionary with list of messages and optional nextPageToken
        Each message includes: name, sender, text, createTime, thread, attachments
    """
    if ctx:
        ctx.info(f"Listing messages in space {space_name}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter_query:
            params["filter"] = filter_query
        if order_by:
            params["orderBy"] = order_by

        response = requests.get(
            f"{BASE_URL}/{space_name}/messages",
            headers=headers,
            params=params
        )

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to list messages: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            num_messages = len(result.get('messages', []))
            ctx.info(f"Successfully retrieved {num_messages} messages")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error listing messages: {str(e)}")
        raise


@mcp.tool
def get_message(
    message_name: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get a specific message from Google Chat.

    Args:
        message_name: Message resource name (e.g., "spaces/AAAAAAAAAAA/messages/BBBBBBB.CCCCCC")

    Returns:
        Message details including name, sender, text, createTime, thread, attachments
    """
    if ctx:
        ctx.info(f"Getting message {message_name}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        response = requests.get(f"{BASE_URL}/{message_name}", headers=headers)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to get message: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            ctx.info(f"Successfully retrieved message")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error getting message: {str(e)}")
        raise


@mcp.tool
def create_message(
    space_name: str,
    text: str,
    thread_key: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send a message to a Google Chat space.

    Args:
        space_name: Space resource name (e.g., "spaces/AAAAAAAAAAA")
        text: Message text content
        thread_key: Optional thread key to reply to specific thread

    Returns:
        Created message details including name, sender, text, createTime
    """
    if ctx:
        ctx.info(f"Creating message in space {space_name}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        payload = {"text": text}

        params = {}
        if thread_key:
            params["threadKey"] = thread_key

        response = requests.post(
            f"{BASE_URL}/{space_name}/messages",
            headers=headers,
            json=payload,
            params=params
        )

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to create message: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            ctx.info(f"Successfully created message: {result.get('name', 'N/A')}")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error creating message: {str(e)}")
        raise


@mcp.tool
def list_members(
    space_name: str,
    page_size: int = 100,
    page_token: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """List members of a Google Chat space.

    Args:
        space_name: Space resource name (e.g., "spaces/AAAAAAAAAAA")
        page_size: Number of members to return (default: 100, max: 1000)
        page_token: Token for pagination (from previous response)

    Returns:
        Dictionary with list of members and optional nextPageToken
        Each member includes: name, state, role, createTime, member (user details)
    """
    if ctx:
        ctx.info(f"Listing members in space {space_name}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            f"{BASE_URL}/{space_name}/members",
            headers=headers,
            params=params
        )

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to list members: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            num_members = len(result.get('memberships', []))
            ctx.info(f"Successfully retrieved {num_members} members")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error listing members: {str(e)}")
        raise


@mcp.tool
def search_spaces(
    query: str,
    page_size: int = 100,
    ctx: Context = None
) -> Dict[str, Any]:
    """Search Google Chat spaces by query.

    Args:
        query: Search query string
        page_size: Number of results to return (default: 100)

    Returns:
        Dictionary with matching spaces
    """
    if ctx:
        ctx.info(f"Searching spaces with query: {query}...")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        # Use list_spaces with filter
        params = {
            "pageSize": page_size,
            "filter": f"displayName:'{query}'"
        }

        response = requests.get(f"{BASE_URL}/spaces", headers=headers, params=params)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to search spaces: {response.status_code} {response.reason}")
            return {
                "error": f"API error: {response.status_code} {response.reason}",
                "details": response.text
            }

        result = response.json()

        if ctx:
            num_results = len(result.get('spaces', []))
            ctx.info(f"Search returned {num_results} results")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Error searching spaces: {str(e)}")
        raise


# Server startup
if __name__ == "__main__":
    print("Starting Google Chat MCP Server...")
    mcp.run(transport="stdio")
