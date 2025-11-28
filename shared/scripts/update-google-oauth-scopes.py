#!/usr/bin/env python3
"""
Update Google OAuth token to include Calendar scope

This script re-authenticates the Google Tasks OAuth token to also include
Calendar API access, allowing the daily briefing to fetch calendar events.
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define scopes
SCOPES = [
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def main():
    print("=" * 70)
    print("Google OAuth Scope Updater")
    print("=" * 70)
    print()
    print("This will re-authenticate your Google account to add Calendar access")
    print("to the existing Tasks OAuth token.")
    print()
    print("Scopes to be requested:")
    print("  - Google Tasks (read/write)")
    print("  - Google Calendar (read-only)")
    print()

    # Paths
    project_root = Path(__file__).parent.parent.parent
    token_dir = project_root / 'shared' / 'mcp-servers' / 'google-tasks-mcp-server'
    token_path = token_dir / 'token.json'
    credentials_path = token_dir / 'credentials.json'

    if not credentials_path.exists():
        print(f"❌ Error: credentials.json not found at {credentials_path}")
        print()
        print("You need to set up Google OAuth credentials first.")
        print("See: https://developers.google.com/workspace/guides/create-credentials")
        return 1

    # Remove existing token to force re-auth
    if token_path.exists():
        print(f"🗑️  Removing old token: {token_path}")
        token_path.unlink()

    # Run OAuth flow
    print()
    print("🔐 Starting OAuth flow...")
    print("   Your browser will open to authenticate with Google")
    print()

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path),
            scopes=SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save the credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

        print()
        print("✅ Success! Token updated with new scopes:")
        print(f"   📄 Token saved to: {token_path}")
        print()
        print("Scopes granted:")
        for scope in creds.scopes:
            print(f"   ✓ {scope}")
        print()
        print("Daily briefing can now access your calendar!")
        print()

        return 0

    except Exception as e:
        print()
        print(f"❌ Error during OAuth flow: {e}")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
