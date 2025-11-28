# Google Photos MCP Server

**Model Context Protocol (MCP) server for Google Photos Library API**

Provides Claude Code with direct access to your Google Photos library, enabling album management, photo search, metadata retrieval, and download capabilities.

## Features

- **List Albums** - Browse all albums in your Google Photos library
- **Album Contents** - View all photos/videos in a specific album
- **Search Media** - Search photos by date range, media type, or album
- **Media Details** - Get full metadata including EXIF data, dimensions, timestamps
- **Download URLs** - Generate time-limited download URLs for photos/videos
- **Pagination** - Handle large libraries with built-in pagination support

## Prerequisites

- Python 3.9 or higher
- Google Cloud Platform account
- Google Photos Library API enabled
- OAuth 2.0 credentials

## Quick Start

### 1. Set Up Google Cloud Platform

Follow the detailed instructions in [GCP-SETUP-GUIDE.md](GCP-SETUP-GUIDE.md):

1. Create/select a GCP project
2. Enable Google Photos Library API
3. Configure OAuth consent screen
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to this directory

### 2. Run Setup Script

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server
./setup-oauth.sh
```

This will:
- Create Python virtual environment
- Install dependencies
- Launch OAuth flow in your browser
- Save authentication token

### 3. Configure Claude Code

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-photos": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/server.py"],
      "env": {
        "GOOGLE_PHOTOS_OAUTH_CREDENTIALS": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/credentials.json"
      }
    }
  }
}
```

### 4. Restart Claude Code

Restart Claude Code to load the new MCP server.

## Available MCP Tools

All tools are prefixed with `mcp__google-photos__` when called from Claude Code.

### `list_albums`

List all albums in your Google Photos library.

**Parameters:**
- `page_size` (integer, optional): Number of albums to return (default: 50, max: 50)
- `page_token` (string, optional): Token for pagination

**Example:**
```python
mcp__google-photos__list_albums(page_size=20)
```

**Returns:**
```json
{
  "albums": [
    {
      "id": "album-id-123",
      "title": "Vacation 2024",
      "productUrl": "https://photos.google.com/album/...",
      "mediaItemsCount": "42",
      "coverPhotoBaseUrl": "https://..."
    }
  ],
  "nextPageToken": "token-for-next-page"
}
```

### `get_album`

Get details for a specific album.

**Parameters:**
- `album_id` (string, required): Album ID

**Example:**
```python
mcp__google-photos__get_album(album_id="album-id-123")
```

### `list_album_contents`

List all media items in a specific album.

**Parameters:**
- `album_id` (string, required): Album ID
- `page_size` (integer, optional): Number of items to return (default: 100, max: 100)
- `page_token` (string, optional): Token for pagination

**Example:**
```python
mcp__google-photos__list_album_contents(album_id="album-id-123", page_size=50)
```

**Returns:**
```json
{
  "mediaItems": [
    {
      "id": "media-id-456",
      "filename": "IMG_1234.jpg",
      "mimeType": "image/jpeg",
      "productUrl": "https://photos.google.com/photo/...",
      "baseUrl": "https://lh3.googleusercontent.com/...",
      "creationTime": "2024-06-15T14:30:00Z",
      "width": "4032",
      "height": "3024",
      "photo": {
        "cameraMake": "Apple",
        "cameraModel": "iPhone 14 Pro",
        "focalLength": 6.86,
        "apertureFNumber": 1.78,
        "isoEquivalent": 64
      }
    }
  ],
  "nextPageToken": null
}
```

### `search_media`

Search for media items with optional filters.

**Parameters:**
- `album_id` (string, optional): Filter by album ID
- `start_date` (string, optional): Start date in YYYY-MM-DD format
- `end_date` (string, optional): End date in YYYY-MM-DD format
- `media_types` (array, optional): Filter by type: `["PHOTO"]`, `["VIDEO"]`, or `["ALL_MEDIA"]`
- `page_size` (integer, optional): Number of items to return (default: 100, max: 100)
- `page_token` (string, optional): Token for pagination

**Example:**
```python
# Photos from June 2024
mcp__google-photos__search_media(
    start_date="2024-06-01",
    end_date="2024-06-30",
    media_types=["PHOTO"],
    page_size=50
)

# Videos in specific album
mcp__google-photos__search_media(
    album_id="album-id-123",
    media_types=["VIDEO"]
)
```

### `get_media_item`

Get details for a specific media item.

**Parameters:**
- `media_item_id` (string, required): Media item ID

**Example:**
```python
mcp__google-photos__get_media_item(media_item_id="media-id-456")
```

### `download_media`

Get download URL for a media item with optional resizing.

**Parameters:**
- `media_item_id` (string, required): Media item ID
- `width` (integer, optional): Resize width (max 16383)
- `height` (integer, optional): Resize height (max 16383)

**Example:**
```python
# Full resolution download
mcp__google-photos__download_media(media_item_id="media-id-456")

# Resized to 1920px wide
mcp__google-photos__download_media(
    media_item_id="media-id-456",
    width=1920
)
```

**Returns:**
```json
{
  "mediaItem": { ... },
  "downloadUrl": "https://lh3.googleusercontent.com/...=d",
  "instructions": "Use this URL to download the media item. URL expires after 60 minutes."
}
```

**Note:** Download URLs expire after 60 minutes. Generate a new URL if needed.

## Common Use Cases

### Browse All Albums

```python
# Get first page of albums
result = mcp__google-photos__list_albums(page_size=50)

# Get next page
if result['nextPageToken']:
    result = mcp__google-photos__list_albums(
        page_size=50,
        page_token=result['nextPageToken']
    )
```

### Find Photos from Specific Event

```python
# Search by date range
photos = mcp__google-photos__search_media(
    start_date="2024-07-04",
    end_date="2024-07-05",
    media_types=["PHOTO"]
)
```

### Download All Photos from Album

```python
# 1. Get album contents
contents = mcp__google-photos__list_album_contents(album_id="album-id-123")

# 2. For each photo, get download URL
for item in contents['mediaItems']:
    download_info = mcp__google-photos__download_media(
        media_item_id=item['id']
    )
    # Use download_info['downloadUrl'] to download
```

### Extract EXIF Metadata

```python
# Get full media item details
item = mcp__google-photos__get_media_item(media_item_id="media-id-456")

# Access EXIF data
if 'photo' in item:
    print(f"Camera: {item['photo']['cameraMake']} {item['photo']['cameraModel']}")
    print(f"ISO: {item['photo']['isoEquivalent']}")
    print(f"Aperture: f/{item['photo']['apertureFNumber']}")
```

## Authentication & Token Management

### OAuth Flow

The first time you run `./setup-oauth.sh`, you'll be prompted to:

1. Sign in to your Google account
2. Grant read-only access to Google Photos
3. Token saved to `token.json`

### Token Refresh

The server automatically refreshes expired tokens. No manual intervention needed.

### Token File Location

`/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/token.json`

**Important:** Keep this file secure. It grants access to your Google Photos library.

## Troubleshooting

### "Credentials file not found"

**Problem:** `credentials.json` missing

**Solution:**
1. Follow [GCP-SETUP-GUIDE.md](GCP-SETUP-GUIDE.md)
2. Download OAuth credentials from Google Cloud Console
3. Save as `credentials.json` in this directory

### "Access blocked: Authorization Error"

**Problem:** App is in Testing mode and user not added as test user

**Solution:**
1. Go to [Google Cloud Console > OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Add your Google account as a test user
3. Run `./setup-oauth.sh` again

### "Token has expired"

**Problem:** Token expired and refresh failed

**Solution:**
```bash
# Delete old token
rm token.json

# Re-run OAuth setup
./setup-oauth.sh
```

### "Invalid client secrets"

**Problem:** Wrong credentials file or corrupted

**Solution:**
1. Re-download credentials from Google Cloud Console
2. Replace `credentials.json`
3. Run `./setup-oauth.sh` again

### MCP Server Not Appearing in Claude Code

**Problem:** Server not loaded

**Solution:**
1. Check `.mcp.json` configuration (see above)
2. Verify paths are absolute, not relative
3. Restart Claude Code completely
4. Check logs for errors

## Limitations & Quotas

### API Limits

- **Free tier:** 10,000 requests per day
- **Rate limit:** 10 requests per second per user

### Download URL Expiration

- Download URLs (`baseUrl`) expire after **60 minutes**
- Generate new URL if needed after expiration

### Pagination

- Albums: Max 50 per request
- Media items: Max 100 per request
- Use `nextPageToken` for large result sets

### Read-Only Access

This server uses `photoslibrary.readonly` scope:
- ✅ Can list, search, download
- ❌ Cannot upload, delete, or modify

## Security Notes

### OAuth Scopes

This server requests minimal permissions:
- `https://www.googleapis.com/auth/photoslibrary.readonly`
- Read-only access to albums and photos
- Cannot modify or delete anything

### Credential Storage

**Keep these files secure:**
- `credentials.json` - OAuth client credentials
- `token.json` - Your access token

**Never commit to Git:**
```bash
# Already in .gitignore
credentials.json
token.json
```

### Token Refresh

Tokens are automatically refreshed when expired. No need to re-authenticate unless:
- Token is manually deleted
- OAuth app is disabled
- Credentials are revoked

## Files in This Directory

```
google-photos-mcp-server/
├── server.py              # Main MCP server
├── requirements.txt       # Python dependencies
├── setup-oauth.sh         # OAuth setup script
├── GCP-SETUP-GUIDE.md     # Detailed GCP configuration guide
├── README.md              # This file
├── credentials.json       # OAuth credentials (download from GCP)
├── token.json             # OAuth token (auto-generated)
└── .venv/                 # Python virtual environment
```

## Development & Testing

### Manual Testing

```bash
# Activate virtual environment
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server
source .venv/bin/activate

# Test authentication
python3 -c "from server import GooglePhotosService; s = GooglePhotosService(); print('✓ Connected')"

# Test listing albums
python3 -c "from server import GooglePhotosService; s = GooglePhotosService(); print(s.list_albums())"
```

### Enable Debug Logging

Edit `server.py` and change:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Resources

- [Google Photos Library API Documentation](https://developers.google.com/photos/library/guides/overview)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Support

For issues specific to this MCP server:
1. Check troubleshooting section above
2. Verify GCP setup (see GCP-SETUP-GUIDE.md)
3. Check server logs for errors

For Google Photos API issues:
- [Google Photos API Documentation](https://developers.google.com/photos)
- [Stack Overflow - google-photos-api](https://stackoverflow.com/questions/tagged/google-photos-api)

## License

Part of Pete's Brain - Rok Systems AI-powered marketing tools.
