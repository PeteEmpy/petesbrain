#!/usr/bin/env python3
"""
Google Photos MCP Server

Provides access to Google Photos Library API through MCP protocol.
Supports listing albums, searching media, downloading photos, and metadata retrieval.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Any, Optional
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# File paths
SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / 'token.json'
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'

# Check for credentials file from environment or default location
if 'GOOGLE_PHOTOS_OAUTH_CREDENTIALS' in os.environ:
    CREDENTIALS_FILE = Path(os.environ['GOOGLE_PHOTOS_OAUTH_CREDENTIALS'])

class GooglePhotosService:
    """Wrapper for Google Photos Library API"""

    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Handle OAuth 2.0 authentication"""
        # Load existing token
        if TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        # Refresh or get new token
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("Refreshing expired token")
                self.creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {CREDENTIALS_FILE}\n"
                        "Please run setup-oauth.sh first or set GOOGLE_PHOTOS_OAUTH_CREDENTIALS"
                    )

                logger.info("Starting OAuth flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save token
            TOKEN_FILE.write_text(self.creds.to_json())
            logger.info(f"Token saved to {TOKEN_FILE}")

        # Build service
        self.service = build('photoslibrary', 'v1', credentials=self.creds, static_discovery=False)
        logger.info("Google Photos service initialized")

    def list_albums(self, page_size: int = 50, page_token: Optional[str] = None) -> dict:
        """List all albums"""
        try:
            request = self.service.albums().list(
                pageSize=page_size,
                pageToken=page_token
            )
            response = request.execute()

            albums = response.get('albums', [])
            next_page_token = response.get('nextPageToken')

            return {
                'albums': [
                    {
                        'id': album.get('id'),
                        'title': album.get('title'),
                        'productUrl': album.get('productUrl'),
                        'mediaItemsCount': album.get('mediaItemsCount', 'Unknown'),
                        'coverPhotoBaseUrl': album.get('coverPhotoBaseUrl')
                    }
                    for album in albums
                ],
                'nextPageToken': next_page_token
            }
        except HttpError as e:
            logger.error(f"Error listing albums: {e}")
            raise

    def get_album(self, album_id: str) -> dict:
        """Get album details"""
        try:
            request = self.service.albums().get(albumId=album_id)
            album = request.execute()

            return {
                'id': album.get('id'),
                'title': album.get('title'),
                'productUrl': album.get('productUrl'),
                'mediaItemsCount': album.get('mediaItemsCount', 'Unknown'),
                'coverPhotoBaseUrl': album.get('coverPhotoBaseUrl')
            }
        except HttpError as e:
            logger.error(f"Error getting album: {e}")
            raise

    def list_album_contents(self, album_id: str, page_size: int = 100, page_token: Optional[str] = None) -> dict:
        """List all media items in an album"""
        try:
            body = {
                'albumId': album_id,
                'pageSize': page_size
            }
            if page_token:
                body['pageToken'] = page_token

            request = self.service.mediaItems().search(body=body)
            response = request.execute()

            media_items = response.get('mediaItems', [])
            next_page_token = response.get('nextPageToken')

            return {
                'mediaItems': [self._format_media_item(item) for item in media_items],
                'nextPageToken': next_page_token
            }
        except HttpError as e:
            logger.error(f"Error listing album contents: {e}")
            raise

    def search_media(
        self,
        album_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        media_types: Optional[list] = None,
        page_size: int = 100,
        page_token: Optional[str] = None
    ) -> dict:
        """Search for media items with filters"""
        try:
            body = {'pageSize': page_size}

            if page_token:
                body['pageToken'] = page_token

            if album_id:
                body['albumId'] = album_id

            # Build filters
            filters = {}

            if start_date or end_date:
                date_filter = {'ranges': [{}]}
                if start_date:
                    date_parts = start_date.split('-')
                    date_filter['ranges'][0]['startDate'] = {
                        'year': int(date_parts[0]),
                        'month': int(date_parts[1]),
                        'day': int(date_parts[2])
                    }
                if end_date:
                    date_parts = end_date.split('-')
                    date_filter['ranges'][0]['endDate'] = {
                        'year': int(date_parts[0]),
                        'month': int(date_parts[1]),
                        'day': int(date_parts[2])
                    }
                filters['dateFilter'] = date_filter

            if media_types:
                filters['mediaTypeFilter'] = {'mediaTypes': media_types}

            if filters:
                body['filters'] = filters

            request = self.service.mediaItems().search(body=body)
            response = request.execute()

            media_items = response.get('mediaItems', [])
            next_page_token = response.get('nextPageToken')

            return {
                'mediaItems': [self._format_media_item(item) for item in media_items],
                'nextPageToken': next_page_token
            }
        except HttpError as e:
            logger.error(f"Error searching media: {e}")
            raise

    def get_media_item(self, media_item_id: str) -> dict:
        """Get details for a specific media item"""
        try:
            request = self.service.mediaItems().get(mediaItemId=media_item_id)
            item = request.execute()

            return self._format_media_item(item)
        except HttpError as e:
            logger.error(f"Error getting media item: {e}")
            raise

    def _format_media_item(self, item: dict) -> dict:
        """Format media item response"""
        metadata = item.get('mediaMetadata', {})

        formatted = {
            'id': item.get('id'),
            'filename': item.get('filename'),
            'mimeType': item.get('mimeType'),
            'productUrl': item.get('productUrl'),
            'baseUrl': item.get('baseUrl'),
            'creationTime': metadata.get('creationTime'),
            'width': metadata.get('width'),
            'height': metadata.get('height')
        }

        # Add photo-specific metadata
        if 'photo' in metadata:
            formatted['photo'] = {
                'cameraMake': metadata['photo'].get('cameraMake'),
                'cameraModel': metadata['photo'].get('cameraModel'),
                'focalLength': metadata['photo'].get('focalLength'),
                'apertureFNumber': metadata['photo'].get('apertureFNumber'),
                'isoEquivalent': metadata['photo'].get('isoEquivalent')
            }

        # Add video-specific metadata
        if 'video' in metadata:
            formatted['video'] = {
                'fps': metadata['video'].get('fps'),
                'status': metadata['video'].get('status')
            }

        return formatted


# Initialize MCP server
app = Server("google-photos")
photos_service = GooglePhotosService()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="list_albums",
            description="List all albums in Google Photos library",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of albums to return (default: 50, max: 50)",
                        "default": 50
                    },
                    "page_token": {
                        "type": "string",
                        "description": "Token for pagination (from previous response)"
                    }
                }
            }
        ),
        Tool(
            name="get_album",
            description="Get details for a specific album",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "string",
                        "description": "Album ID"
                    }
                },
                "required": ["album_id"]
            }
        ),
        Tool(
            name="list_album_contents",
            description="List all media items in a specific album",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "string",
                        "description": "Album ID"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of items to return (default: 100, max: 100)",
                        "default": 100
                    },
                    "page_token": {
                        "type": "string",
                        "description": "Token for pagination"
                    }
                },
                "required": ["album_id"]
            }
        ),
        Tool(
            name="search_media",
            description="Search for media items with optional filters (date range, media type, album)",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "string",
                        "description": "Optional: Filter by album ID"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Optional: Start date (YYYY-MM-DD format)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional: End date (YYYY-MM-DD format)"
                    },
                    "media_types": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["ALL_MEDIA", "VIDEO", "PHOTO"]},
                        "description": "Optional: Filter by media type"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of items to return (default: 100, max: 100)",
                        "default": 100
                    },
                    "page_token": {
                        "type": "string",
                        "description": "Token for pagination"
                    }
                }
            }
        ),
        Tool(
            name="get_media_item",
            description="Get details for a specific media item (photo or video)",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_item_id": {
                        "type": "string",
                        "description": "Media item ID"
                    }
                },
                "required": ["media_item_id"]
            }
        ),
        Tool(
            name="download_media",
            description="Get download URL for a media item (append =d to baseUrl to download)",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_item_id": {
                        "type": "string",
                        "description": "Media item ID"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Optional: Resize width (max 16383)"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Optional: Resize height (max 16383)"
                    }
                },
                "required": ["media_item_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "list_albums":
            result = photos_service.list_albums(
                page_size=arguments.get('page_size', 50),
                page_token=arguments.get('page_token')
            )

        elif name == "get_album":
            result = photos_service.get_album(arguments['album_id'])

        elif name == "list_album_contents":
            result = photos_service.list_album_contents(
                album_id=arguments['album_id'],
                page_size=arguments.get('page_size', 100),
                page_token=arguments.get('page_token')
            )

        elif name == "search_media":
            result = photos_service.search_media(
                album_id=arguments.get('album_id'),
                start_date=arguments.get('start_date'),
                end_date=arguments.get('end_date'),
                media_types=arguments.get('media_types'),
                page_size=arguments.get('page_size', 100),
                page_token=arguments.get('page_token')
            )

        elif name == "get_media_item":
            result = photos_service.get_media_item(arguments['media_item_id'])

        elif name == "download_media":
            item = photos_service.get_media_item(arguments['media_item_id'])
            base_url = item['baseUrl']

            # Build download URL
            params = []
            if arguments.get('width'):
                params.append(f"w{arguments['width']}")
            if arguments.get('height'):
                params.append(f"h{arguments['height']}")

            download_url = f"{base_url}=d"
            if params:
                download_url = f"{base_url}={'-'.join(params)}-d"

            result = {
                'mediaItem': item,
                'downloadUrl': download_url,
                'instructions': 'Use this URL to download the media item. URL expires after 60 minutes.'
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
