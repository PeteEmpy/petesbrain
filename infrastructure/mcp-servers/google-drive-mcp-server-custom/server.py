from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import sys
import logging
import requests
import json
import base64

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# OAuth module will be imported lazily inside tool functions to prevent
# startup popups when tokens are expired

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('google_drive_server')

mcp = FastMCP("Google Drive Tools")

# Server startup
logger.info("Starting Google Drive MCP Server...")

@mcp.tool
def search(
    query: str = "",
    page_size: int = 50,
    page_token: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Search for files and folders in Google Drive cloud storage.

    Use this tool to find documents, spreadsheets, presentations, folders, and any other files
    stored in the user's Google Drive account. Supports full Drive API query syntax for
    filtering by name, type, owner, modification date, and more.

    Args:
        query: Search query using Drive API syntax (e.g., "name contains 'budget'",
               "mimeType='application/pdf'", "modifiedTime > '2025-01-01'")
               Leave empty to list all files.
        page_size: Number of results per page (default 50, max 100)
        page_token: Token for retrieving next page of results (from previous search)

    Returns:
        Dictionary containing list of files with metadata (id, name, mimeType, createdTime,
        modifiedTime, size, webViewLink, owners) and optional nextPageToken for pagination
    """
    if ctx:
        ctx.info(f"Searching Drive with query: {query or 'all files'}")

    try:
        # Import OAuth module lazily (only when tool is actually called)
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        params = {
            'pageSize': min(page_size, 100),
            'fields': 'nextPageToken, files(id, name, mimeType, parents, createdTime, modifiedTime, size, webViewLink, owners)'
        }

        if query:
            params['q'] = query

        if page_token:
            params['pageToken'] = page_token

        response = requests.get(
            'https://www.googleapis.com/drive/v3/files',
            headers=headers,
            params=params
        )

        if not response.ok:
            error_msg = f"Drive API error: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info(f"Found {len(result.get('files', []))} files")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Search failed: {str(e)}")
        raise


@mcp.tool
def create_text_file(
    name: str,
    content: str,
    parent_folder_id: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new text or markdown file

    Args:
        name: File name (.txt or .md)
        content: File content
        parent_folder_id: Optional parent folder ID

    Returns:
        Details of the created file
    """
    if ctx:
        ctx.info(f"Creating file: {name}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        # Determine MIME type
        mime_type = 'text/markdown' if name.endswith('.md') else 'text/plain'

        metadata = {
            'name': name,
            'mimeType': mime_type
        }

        if parent_folder_id:
            metadata['parents'] = [parent_folder_id]

        # Multipart upload
        boundary = '-------314159265358979323846'
        delimiter = f'\r\n--{boundary}\r\n'
        close_delim = f'\r\n--{boundary}--'

        multipart_body = (
            delimiter +
            'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
            json.dumps(metadata) +
            delimiter +
            f'Content-Type: {mime_type}\r\n\r\n' +
            content +
            close_delim
        )

        upload_headers = headers.copy()
        upload_headers['Content-Type'] = f'multipart/related; boundary={boundary}'

        response = requests.post(
            'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
            headers=upload_headers,
            data=multipart_body.encode('utf-8')
        )

        if not response.ok:
            error_msg = f"Failed to create file: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info(f"File created successfully: {result.get('id')}")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Create file failed: {str(e)}")
        raise


@mcp.tool
def update_text_file(
    file_id: str,
    content: str,
    name: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Update an existing text or markdown file

    Args:
        file_id: ID of the file to update
        content: New file content
        name: Optional new name (.txt or .md)

    Returns:
        Updated file details
    """
    if ctx:
        ctx.info(f"Updating file: {file_id}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        # Get current file metadata
        file_info = requests.get(
            f'https://www.googleapis.com/drive/v3/files/{file_id}',
            headers=headers,
            params={'fields': 'name,mimeType'}
        ).json()

        mime_type = file_info.get('mimeType', 'text/plain')

        metadata = {}
        if name:
            metadata['name'] = name
            if name.endswith('.md'):
                metadata['mimeType'] = 'text/markdown'
            elif name.endswith('.txt'):
                metadata['mimeType'] = 'text/plain'

        # Multipart upload for update
        boundary = '-------314159265358979323846'
        delimiter = f'\r\n--{boundary}\r\n'
        close_delim = f'\r\n--{boundary}--'

        multipart_body = (
            delimiter +
            'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
            json.dumps(metadata) +
            delimiter +
            f'Content-Type: {mime_type}\r\n\r\n' +
            content +
            close_delim
        )

        upload_headers = headers.copy()
        upload_headers['Content-Type'] = f'multipart/related; boundary={boundary}'

        response = requests.patch(
            f'https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=multipart',
            headers=upload_headers,
            data=multipart_body.encode('utf-8')
        )

        if not response.ok:
            error_msg = f"Failed to update file: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info(f"File updated successfully")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Update file failed: {str(e)}")
        raise


@mcp.tool
def create_folder(
    name: str,
    parent: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new folder in Google Drive

    Args:
        name: Folder name
        parent: Optional parent folder ID or path

    Returns:
        Details of the created folder
    """
    if ctx:
        ctx.info(f"Creating folder: {name}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent:
            metadata['parents'] = [parent]

        response = requests.post(
            'https://www.googleapis.com/drive/v3/files',
            headers=headers,
            json=metadata
        )

        if not response.ok:
            error_msg = f"Failed to create folder: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info(f"Folder created: {result.get('id')}")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Create folder failed: {str(e)}")
        raise


@mcp.tool
def list_folder(
    folder_id: str = None,
    page_size: int = 50,
    page_token: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """List contents of a folder (defaults to root)

    Args:
        folder_id: Folder ID
        page_size: Items to return (default 50, max 100)
        page_token: Token for next page

    Returns:
        Files and folders in the specified folder
    """
    if ctx:
        ctx.info(f"Listing folder: {folder_id or 'root'}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        query = f"'{folder_id or 'root'}' in parents and trashed=false"

        params = {
            'q': query,
            'pageSize': min(page_size, 100),
            'fields': 'nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink)'
        }

        if page_token:
            params['pageToken'] = page_token

        response = requests.get(
            'https://www.googleapis.com/drive/v3/files',
            headers=headers,
            params=params
        )

        if not response.ok:
            error_msg = f"Failed to list folder: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info(f"Found {len(result.get('files', []))} items")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"List folder failed: {str(e)}")
        raise


@mcp.tool
def delete_item(
    item_id: str,
    ctx: Context = None
) -> str:
    """Move a file or folder to trash (can be restored from Google Drive trash)

    Args:
        item_id: ID of the item to delete

    Returns:
        Confirmation message
    """
    if ctx:
        ctx.info(f"Deleting item: {item_id}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        response = requests.delete(
            f'https://www.googleapis.com/drive/v3/files/{item_id}',
            headers=headers
        )

        if not response.ok:
            error_msg = f"Failed to delete: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return f"Error: {error_msg}"

        if ctx:
            ctx.info("Item deleted successfully")

        return f"Item {item_id} moved to trash successfully"

    except Exception as e:
        if ctx:
            ctx.error(f"Delete failed: {str(e)}")
        raise


@mcp.tool
def rename_item(
    item_id: str,
    new_name: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Rename a file or folder

    Args:
        item_id: ID of the item to rename
        new_name: New name

    Returns:
        Updated item details
    """
    if ctx:
        ctx.info(f"Renaming item {item_id} to {new_name}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        response = requests.patch(
            f'https://www.googleapis.com/drive/v3/files/{item_id}',
            headers=headers,
            json={'name': new_name}
        )

        if not response.ok:
            error_msg = f"Failed to rename: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info("Item renamed successfully")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Rename failed: {str(e)}")
        raise


@mcp.tool
def move_item(
    item_id: str,
    destination_folder_id: str = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Move a file or folder

    Args:
        item_id: ID of the item to move
        destination_folder_id: Destination folder ID

    Returns:
        Updated item details
    """
    if ctx:
        ctx.info(f"Moving item {item_id} to folder {destination_folder_id or 'root'}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        # Get current parents
        file_info = requests.get(
            f'https://www.googleapis.com/drive/v3/files/{item_id}',
            headers=headers,
            params={'fields': 'parents'}
        ).json()

        previous_parents = ','.join(file_info.get('parents', []))

        params = {
            'addParents': destination_folder_id or 'root',
            'removeParents': previous_parents,
            'fields': 'id, name, parents'
        }

        response = requests.patch(
            f'https://www.googleapis.com/drive/v3/files/{item_id}',
            headers=headers,
            params=params
        )

        if not response.ok:
            error_msg = f"Failed to move: {response.status_code} {response.reason}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg, "details": response.text}

        result = response.json()

        if ctx:
            ctx.info("Item moved successfully")

        return result

    except Exception as e:
        if ctx:
            ctx.error(f"Move failed: {str(e)}")
        raise


@mcp.tool
def get_file_content(
    file_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get content of a text file

    Args:
        file_id: File ID

    Returns:
        File content and metadata
    """
    if ctx:
        ctx.info(f"Getting content of file: {file_id}")

    try:
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        # Get file metadata
        metadata_response = requests.get(
            f'https://www.googleapis.com/drive/v3/files/{file_id}',
            headers=headers,
            params={'fields': 'id, name, mimeType, size'}
        )

        if not metadata_response.ok:
            error_msg = f"Failed to get file metadata: {metadata_response.status_code}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg}

        metadata = metadata_response.json()

        # Get file content
        content_response = requests.get(
            f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media',
            headers=headers
        )

        if not content_response.ok:
            error_msg = f"Failed to get file content: {content_response.status_code}"
            if ctx:
                ctx.error(error_msg)
            return {"error": error_msg}

        content = content_response.text

        if ctx:
            ctx.info(f"Retrieved {len(content)} characters")

        return {
            "metadata": metadata,
            "content": content
        }

    except Exception as e:
        if ctx:
            ctx.error(f"Get content failed: {str(e)}")
        raise


# Server startup
if __name__ == "__main__":
    print("Starting Google Drive MCP Server...")
    print("Ensure GOOGLE_DRIVE_OAUTH_CONFIG_PATH environment variable is set.")
    logger.info("Google Drive MCP Server starting")
    mcp.run(transport="stdio")
