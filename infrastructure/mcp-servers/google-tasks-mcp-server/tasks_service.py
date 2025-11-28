"""Google Tasks API Service"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/tasks"]


def tasks_service():
    """Create and return a Google Tasks service instance using OAuth."""
    # Get the directory where this file is located
    server_dir = Path(__file__).parent
    token_path = server_dir / "token.json"
    credentials_path = server_dir / "credentials.json"

    creds = None

    # Load existing token if available
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            # Token file exists but is invalid - will re-authenticate
            print(f"Warning: Could not load existing token: {e}")
            creds = None

    # If no valid credentials, refresh or get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                # Try to refresh the token
                creds.refresh(Request())
                # Save refreshed token immediately
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
            except Exception as e:
                # Refresh failed - need to re-authenticate
                print(f"Token refresh failed: {e}")
                print("Re-authenticating...")
                if not credentials_path.exists():
                    raise ValueError(
                        f"OAuth credentials file not found at {credentials_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save new credentials
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
        else:
            # No token or no refresh token - need initial auth
            if not credentials_path.exists():
                raise ValueError(
                    f"OAuth credentials file not found at {credentials_path}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save credentials
            with open(token_path, "w") as token_file:
                token_file.write(creds.to_json())

    service = build("tasks", "v1", credentials=creds)
    return service
