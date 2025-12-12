#!/usr/bin/env python3
"""
Re-authenticate Google OAuth with expanded scopes

This script re-authenticates the OAuth token with all necessary scopes:
- Google Tasks (read/write)
- Google Calendar (read-only)
- Gmail (read/write/label/send) - includes all Gmail permissions

Run this when you need to add new API scopes to the existing OAuth setup.
"""

import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Expanded scopes for all PetesBrain integrations
SCOPES = [
    'https://www.googleapis.com/auth/tasks',           # Google Tasks (read/write)
    'https://www.googleapis.com/auth/calendar.readonly',  # Google Calendar (read)
    'https://www.googleapis.com/auth/gmail.modify',     # Gmail (read/write/label) - includes all Gmail permissions
]

def reauth_google_oauth():
    """Re-authenticate with expanded scopes"""

    # Paths
    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "infrastructure/mcp-servers/google-tasks-mcp-server/credentials.json"
    token_path = project_root / "infrastructure/mcp-servers/google-tasks-mcp-server/token.json"

    print("=" * 70)
    print("GOOGLE OAUTH RE-AUTHENTICATION")
    print("=" * 70)
    print()
    print(f"Credentials: {credentials_path}")
    print(f"Token: {token_path}")
    print()
    print("Scopes being requested:")
    for scope in SCOPES:
        print(f"  - {scope}")
    print()

    if not credentials_path.exists():
        print(f"❌ Error: credentials.json not found at {credentials_path}")
        print()
        print("Please ensure OAuth credentials are set up:")
        print("  1. Go to Google Cloud Console")
        print("  2. Create OAuth 2.0 credentials")
        print(f"  3. Save as {credentials_path}")
        sys.exit(1)

    # Remove old token if it exists
    if token_path.exists():
        print(f"🗑️  Removing old token: {token_path}")
        token_path.unlink()
        print()

    # Run OAuth flow
    print("🔐 Starting OAuth flow...")
    print()
    print("👉 A browser window will open for authentication")
    print("   Please sign in and grant permissions")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(
        str(credentials_path),
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    # Save new token
    print("✅ Authentication successful!")
    print()
    print(f"💾 Saving new token to: {token_path}")

    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())

    print()
    print("=" * 70)
    print("✅ RE-AUTHENTICATION COMPLETE")
    print("=" * 70)
    print()
    print("The following services are now available:")
    print("  ✓ Google Tasks (read/write)")
    print("  ✓ Google Calendar (read-only)")
    print("  ✓ Gmail (read/write/label/send)")
    print()
    print("You can now run:")
    print("  - Daily briefing agent")
    print("  - Task generation scripts")
    print("  - Calendar integration scripts")
    print()

if __name__ == "__main__":
    try:
        reauth_google_oauth()
    except KeyboardInterrupt:
        print("\n\n⚠️  Authentication cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during authentication: {e}")
        sys.exit(1)
