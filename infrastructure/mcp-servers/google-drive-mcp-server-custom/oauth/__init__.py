"""
OAuth module for Google Drive authentication.
"""

from .google_auth import (
    get_headers_with_auto_token,
    get_oauth_credentials
)

__all__ = [
    'get_headers_with_auto_token',
    'get_oauth_credentials'
]

# Version information
__version__ = "1.0.0"
__author__ = "Google Drive MCP Server Contributors"
__description__ = "OAuth 2.0 authentication module for Google Drive API"
