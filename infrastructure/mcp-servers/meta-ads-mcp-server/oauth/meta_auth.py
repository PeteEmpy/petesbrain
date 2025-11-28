"""
Meta Marketing API OAuth Authentication

This module handles OAuth 2.0 authentication for Meta Marketing API,
following the pattern established in the Google Ads MCP server.
"""

import os
import json
import logging
import webbrowser
import http.server
import socketserver
import urllib.parse
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

import requests

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# Constants
META_API_VERSION = "v22.0"
META_GRAPH_URL = f"https://graph.facebook.com/{META_API_VERSION}"
OAUTH_REDIRECT_URI = "http://localhost:8080/"
OAUTH_CALLBACK_PORT = 8080

# Environment variables
META_APP_ID = os.environ.get("META_APP_ID")
META_APP_SECRET = os.environ.get("META_APP_SECRET")
META_TOKEN_PATH = os.environ.get("META_TOKEN_PATH")

def format_account_id(account_id: str) -> str:
    """
    Format Meta Ad Account ID to ensure it starts with 'act_'.
    
    Args:
        account_id: The account ID (with or without 'act_' prefix)
    
    Returns:
        str: Account ID with 'act_' prefix
    """
    account_id = str(account_id).strip()
    if account_id.startswith('act_'):
        return account_id
    return f'act_{account_id}'


class OAuthCallbackHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for OAuth callback requests."""
    
    authorization_code = None
    
    def log_message(self, format, *args):
        """Suppress request logs."""
        pass
    
    def do_GET(self):
        """Handle the OAuth callback."""
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        if 'code' in query_params:
            OAuthCallbackHandler.authorization_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            success_html = """
            <html>
            <head><title>Authentication Successful</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #4267B2;">✅ Authentication Successful!</h1>
                <p>You can now close this window and return to Claude Desktop.</p>
                <p style="color: #666; font-size: 14px;">Meta Ads MCP Server is ready to use.</p>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_html = """
            <html>
            <head><title>Authentication Failed</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #E4405F;">❌ Authentication Failed</h1>
                <p>No authorization code received. Please try again.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())


def get_token_path() -> str:
    """Get the path where the OAuth token should be stored."""
    if META_TOKEN_PATH:
        return META_TOKEN_PATH
    
    # Default to same directory as this module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(current_dir), 'meta_ads_token.json')


def load_token() -> Optional[Dict[str, Any]]:
    """
    Load the stored OAuth token from disk.
    
    Returns:
        Dict with token data or None if no valid token exists
    """
    token_path = get_token_path()
    
    if not os.path.exists(token_path):
        logger.info(f"No token file found at {token_path}")
        return None
    
    try:
        with open(token_path, 'r') as f:
            token_data = json.load(f)
        
        logger.info(f"Loaded existing token from {token_path}")
        return token_data
    except Exception as e:
        logger.warning(f"Error loading token: {e}")
        return None


def save_token(token_data: Dict[str, Any]) -> None:
    """
    Save OAuth token to disk.
    
    Args:
        token_data: Token data to save
    """
    token_path = get_token_path()
    
    try:
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        # Set secure file permissions
        os.chmod(token_path, 0o600)
        logger.info(f"Token saved to {token_path}")
    except Exception as e:
        logger.error(f"Error saving token: {e}")
        raise


def is_token_valid(token_data: Dict[str, Any]) -> bool:
    """
    Check if the stored token is still valid.
    
    Args:
        token_data: Token data to validate
    
    Returns:
        bool: True if token is valid and not expired
    """
    if not token_data or 'access_token' not in token_data:
        return False
    
    # Check if token has expiry information
    if 'expires_at' in token_data:
        expires_at = datetime.fromisoformat(token_data['expires_at'])
        if datetime.now() >= expires_at:
            logger.info("Token has expired")
            return False
    
    return True


def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access token.
    
    Args:
        code: Authorization code from OAuth callback
    
    Returns:
        Dict with access token and metadata
    """
    if not META_APP_ID or not META_APP_SECRET:
        raise ValueError(
            "META_APP_ID and META_APP_SECRET must be set in environment variables"
        )
    
    token_url = f"{META_GRAPH_URL}/oauth/access_token"
    params = {
        'client_id': META_APP_ID,
        'client_secret': META_APP_SECRET,
        'redirect_uri': OAUTH_REDIRECT_URI,
        'code': code
    }
    
    logger.info("Exchanging authorization code for access token")
    response = requests.get(token_url, params=params)
    
    if not response.ok:
        error_msg = f"Token exchange failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    token_data = response.json()
    
    # Add expiry timestamp if expires_in is provided
    if 'expires_in' in token_data:
        expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
        token_data['expires_at'] = expires_at.isoformat()
    
    logger.info("Successfully obtained access token")
    return token_data


def get_long_lived_token(short_token: str) -> Dict[str, Any]:
    """
    Exchange short-lived token for long-lived token (60 days).
    
    Args:
        short_token: Short-lived access token
    
    Returns:
        Dict with long-lived access token and metadata
    """
    if not META_APP_ID or not META_APP_SECRET:
        raise ValueError(
            "META_APP_ID and META_APP_SECRET must be set in environment variables"
        )
    
    exchange_url = f"{META_GRAPH_URL}/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': META_APP_ID,
        'client_secret': META_APP_SECRET,
        'fb_exchange_token': short_token
    }
    
    logger.info("Exchanging for long-lived token")
    response = requests.get(exchange_url, params=params)
    
    if not response.ok:
        error_msg = f"Long-lived token exchange failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    token_data = response.json()
    
    # Add expiry timestamp (60 days)
    if 'expires_in' in token_data:
        expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
        token_data['expires_at'] = expires_at.isoformat()
    
    logger.info("Successfully obtained long-lived token")
    return token_data


def run_oauth_flow() -> str:
    """
    Run the OAuth 2.0 authorization flow.
    
    Returns:
        str: Access token
    """
    if not META_APP_ID:
        raise ValueError("META_APP_ID must be set in environment variables")
    
    # Build authorization URL
    auth_params = {
        'client_id': META_APP_ID,
        'redirect_uri': OAUTH_REDIRECT_URI,
        'scope': 'ads_read',  # Request only ads_read for now
        'response_type': 'code'
    }
    
    auth_url = f"https://www.facebook.com/{META_API_VERSION}/dialog/oauth?" + \
               urllib.parse.urlencode(auth_params)
    
    logger.info("Starting OAuth authorization flow")
    logger.info(f"Opening browser to: {auth_url}")
    
    # Open browser for user authorization
    webbrowser.open(auth_url)
    
    # Start local server to receive callback
    logger.info(f"Starting local server on port {OAUTH_CALLBACK_PORT}")
    OAuthCallbackHandler.authorization_code = None
    
    with socketserver.TCPServer(("", OAUTH_CALLBACK_PORT), OAuthCallbackHandler) as httpd:
        # Wait for one request (the OAuth callback)
        httpd.handle_request()
    
    if not OAuthCallbackHandler.authorization_code:
        raise Exception("No authorization code received from OAuth callback")
    
    # Exchange code for token
    token_data = exchange_code_for_token(OAuthCallbackHandler.authorization_code)
    
    # Exchange for long-lived token
    if 'access_token' in token_data:
        token_data = get_long_lived_token(token_data['access_token'])
    
    return token_data['access_token']


def get_oauth_credentials() -> str:
    """
    Get OAuth access token, running the auth flow if needed.
    
    This is the main entry point for authentication. It will:
    1. Check for META_ACCESS_TOKEN environment variable (manual token)
    2. Check for existing valid token
    3. Run OAuth flow if no valid token exists
    4. Cache the token for future use
    
    Returns:
        str: Valid access token
    """
    # FALLBACK: Check for manually provided token via environment variable
    manual_token = os.environ.get('META_ACCESS_TOKEN')
    if manual_token:
        logger.info("Using manually provided META_ACCESS_TOKEN from environment")
        return manual_token.strip()
    
    # Try to load existing token
    token_data = load_token()
    
    if token_data and is_token_valid(token_data):
        logger.info("Using existing valid token")
        return token_data['access_token']
    
    logger.info("No valid token found, starting OAuth flow")
    
    # Run OAuth flow to get new token
    access_token = run_oauth_flow()
    
    # Save the token
    token_data = {
        'access_token': access_token,
        'token_type': 'bearer',
        'obtained_at': datetime.now().isoformat()
    }
    save_token(token_data)
    
    return access_token


def get_headers_with_auto_token() -> Dict[str, str]:
    """
    Get API headers with automatically managed token.
    
    Returns:
        Dict with headers including Authorization
    """
    access_token = get_oauth_credentials()
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    return headers, access_token


def debug_token(access_token: str) -> Dict[str, Any]:
    """
    Debug an access token to check its validity and permissions.
    
    Args:
        access_token: Token to debug
    
    Returns:
        Dict with token debug information
    """
    if not META_APP_ID or not META_APP_SECRET:
        raise ValueError(
            "META_APP_ID and META_APP_SECRET must be set in environment variables"
        )
    
    debug_url = f"{META_GRAPH_URL}/debug_token"
    params = {
        'input_token': access_token,
        'access_token': f"{META_APP_ID}|{META_APP_SECRET}"
    }
    
    response = requests.get(debug_url, params=params)
    
    if not response.ok:
        error_msg = f"Token debug failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    return response.json()

