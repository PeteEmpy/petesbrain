"""
Google Drive OAuth Authentication - integrated into tool calls
"""

import os
import json
import requests
import logging
from typing import Dict, Any

# Google Auth libraries
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# Constants - Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

# Environment variables
GOOGLE_DRIVE_OAUTH_CONFIG_PATH = os.environ.get("GOOGLE_DRIVE_OAUTH_CONFIG_PATH")

def get_oauth_credentials():
    """Get and refresh OAuth user credentials for Google Drive."""
    if not GOOGLE_DRIVE_OAUTH_CONFIG_PATH:
        raise ValueError(
            "GOOGLE_DRIVE_OAUTH_CONFIG_PATH environment variable not set. "
            "Please set it to point to your OAuth credentials JSON file."
        )

    if not os.path.exists(GOOGLE_DRIVE_OAUTH_CONFIG_PATH):
        raise FileNotFoundError(f"OAuth config file not found: {GOOGLE_DRIVE_OAUTH_CONFIG_PATH}")

    creds = None

    # Path to store the token - use MCP server directory for reliability
    server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(server_dir, 'token.json')

    # Load existing token if it exists
    if os.path.exists(token_path):
        try:
            logger.info(f"Loading existing OAuth token from {token_path}")
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            logger.warning(f"Error loading existing token: {e}")
            creds = None

    # Check if credentials are valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Refreshing expired OAuth token")
                creds.refresh(Request())
                logger.info("Token successfully refreshed")
            except RefreshError as e:
                logger.warning(f"Token refresh failed: {e}, will get new token")
                creds = None
            except Exception as e:
                logger.error(f"Unexpected error refreshing token: {e}")
                raise

        # Need new credentials - run OAuth flow
        if not creds:
            logger.info("Starting OAuth authentication flow")

            try:
                # Load client configuration
                with open(GOOGLE_DRIVE_OAUTH_CONFIG_PATH, 'r') as f:
                    client_config = json.load(f)

                # Create flow
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)

                # Run OAuth flow with automatic local server
                try:
                    creds = flow.run_local_server(port=0)
                    logger.info("OAuth flow completed successfully using local server")
                except Exception as e:
                    logger.warning(f"Local server failed: {e}, falling back to console")
                    creds = flow.run_console()
                    logger.info("OAuth flow completed successfully using console")

            except Exception as e:
                logger.error(f"OAuth flow failed: {e}")
                raise

        # Save the credentials
        if creds:
            try:
                logger.info(f"Saving credentials to {token_path}")
                os.makedirs(os.path.dirname(token_path), exist_ok=True)
                with open(token_path, 'w') as f:
                    f.write(creds.to_json())

                # Verify the token was actually written
                if os.path.exists(token_path):
                    logger.info(f"✅ Credentials saved successfully to {token_path}")
                else:
                    raise Exception(f"Token file not found after write: {token_path}")

            except Exception as e:
                logger.error(f"❌ CRITICAL: Could not save credentials: {e}")
                logger.error(f"Token will not persist. OAuth will be required again next time.")
                # Don't raise - allow current session to work, but warn user

    return creds

def get_headers_with_auto_token() -> Dict[str, str]:
    """Get API headers with automatically managed token - integrated OAuth for Google Drive."""
    # This will automatically trigger OAuth flow if needed
    creds = get_oauth_credentials()

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }

    return headers
