"""
QuickBooks OAuth 2.0 Authentication Module

Handles OAuth token management for QuickBooks Online API.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple
import requests

logger = logging.getLogger('quickbooks_auth')

# File paths for token storage
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'token.json')

def load_tokens() -> Dict:
    """Load OAuth tokens from file."""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(
            f"Token file not found: {TOKEN_FILE}\n"
            "Please run setup_oauth.py first to authenticate."
        )
    
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)


def save_tokens(tokens: Dict) -> None:
    """Save OAuth tokens to file."""
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    logger.info("Tokens saved successfully")


def refresh_access_token() -> Dict:
    """
    Refresh the access token using the refresh token.
    
    Returns:
        Dict with new token data
    """
    logger.info("Refreshing access token...")
    
    tokens = load_tokens()
    client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
    client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Missing QuickBooks credentials. Please set QUICKBOOKS_CLIENT_ID "
            "and QUICKBOOKS_CLIENT_SECRET environment variables."
        )
    
    # Prepare refresh request
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens.get('refresh_token')
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Make refresh request with basic auth
    response = requests.post(
        token_url,
        data=data,
        headers=headers,
        auth=(client_id, client_secret)
    )
    
    if not response.ok:
        error_msg = f"Token refresh failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    new_tokens = response.json()
    
    # Update tokens with new values
    tokens['access_token'] = new_tokens['access_token']
    tokens['refresh_token'] = new_tokens['refresh_token']
    tokens['expires_at'] = (datetime.now() + timedelta(seconds=new_tokens['expires_in'])).isoformat()
    tokens['refresh_expires_at'] = (datetime.now() + timedelta(seconds=new_tokens.get('x_refresh_token_expires_in', 8726400))).isoformat()
    
    save_tokens(tokens)
    logger.info("Access token refreshed successfully")
    
    return tokens


def is_token_expired(tokens: Dict) -> bool:
    """
    Check if the access token is expired or will expire soon.
    
    Args:
        tokens: Dict containing token data with 'expires_at' field
    
    Returns:
        True if token is expired or expires within 5 minutes
    """
    if 'expires_at' not in tokens:
        return True
    
    expires_at = datetime.fromisoformat(tokens['expires_at'])
    # Consider token expired if it expires within 5 minutes
    buffer_time = timedelta(minutes=5)
    
    return datetime.now() >= (expires_at - buffer_time)


def get_valid_token() -> str:
    """
    Get a valid access token, refreshing if necessary.
    
    Returns:
        Valid access token string
    """
    tokens = load_tokens()
    
    if is_token_expired(tokens):
        logger.info("Token expired or expiring soon, refreshing...")
        tokens = refresh_access_token()
    
    return tokens['access_token']


def get_headers_with_auto_token() -> Dict[str, str]:
    """
    Get HTTP headers with a valid access token, automatically refreshing if needed.
    
    Returns:
        Dict of headers including Authorization
    """
    access_token = get_valid_token()
    
    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def get_realm_id() -> str:
    """
    Get the QuickBooks company (realm) ID from stored tokens.
    
    Returns:
        Realm ID string
    """
    tokens = load_tokens()
    realm_id = tokens.get('realmId')
    
    if not realm_id:
        raise ValueError(
            "Realm ID not found in token file. "
            "Please run setup_oauth.py to authenticate."
        )
    
    return realm_id


def revoke_token() -> bool:
    """
    Revoke the current access token.
    
    Returns:
        True if revocation successful
    """
    logger.info("Revoking access token...")
    
    tokens = load_tokens()
    client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
    client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
    
    revoke_url = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
    
    data = {
        'token': tokens.get('access_token')
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        revoke_url,
        data=data,
        headers=headers,
        auth=(client_id, client_secret)
    )
    
    if response.ok:
        logger.info("Token revoked successfully")
        return True
    else:
        logger.error(f"Token revocation failed: {response.status_code} - {response.text}")
        return False

