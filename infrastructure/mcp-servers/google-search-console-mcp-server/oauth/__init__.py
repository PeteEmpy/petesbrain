"""
Google Search Console OAuth Authentication
"""

from .google_auth import get_oauth_credentials, get_headers_with_auto_token

__all__ = ['get_oauth_credentials', 'get_headers_with_auto_token']
