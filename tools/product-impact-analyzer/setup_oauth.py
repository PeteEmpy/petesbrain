#!/usr/bin/env python3
"""
OAuth Setup for Merchant Center Access

Run this once to authenticate and get a refresh token.
The refresh token allows automated access without repeated logins.

Usage:
    python3 setup_oauth.py
"""

import json
import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# OAuth 2.0 scopes for Content API access
SCOPES = ['https://www.googleapis.com/auth/content']

def setup_oauth():
    """
    Run OAuth flow to get user credentials
    """
    print("="*80)
    print("MERCHANT CENTER OAUTH SETUP")
    print("="*80)
    print()

    # Check if we already have credentials
    creds_file = Path(__file__).parent / 'oauth_credentials.json'

    if creds_file.exists():
        print(f"⚠️  Existing credentials found at {creds_file}")
        response = input("Do you want to re-authenticate? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing credentials. Exiting.")
            return

    # Get client secrets file path
    client_secrets_file = Path(__file__).parent / 'client_secrets.json'

    if not client_secrets_file.exists():
        print("❌ ERROR: client_secrets.json not found!")
        print()
        print("You need to create OAuth 2.0 credentials in Google Cloud Console:")
        print()
        print("1. Go to: https://console.cloud.google.com/apis/credentials?project=257130067085")
        print("2. Click 'CREATE CREDENTIALS' → 'OAuth client ID'")
        print("3. Application type: 'Desktop app'")
        print("4. Name: 'Product Impact Analyzer'")
        print("5. Click 'CREATE'")
        print("6. Click 'DOWNLOAD JSON'")
        print("7. Save as 'client_secrets.json' in this directory")
        print()
        return

    print("Starting OAuth flow...")
    print()
    print("A browser window will open. Please:")
    print("1. Log in with your Google account")
    print("2. Grant access to 'Content API for Shopping'")
    print("3. You'll be redirected to a success page")
    print()
    print("TIP: Use your Google Ads MANAGER account for access to all clients")
    print()
    print("Opening browser in 3 seconds...")
    print()

    import time
    time.sleep(3)

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        str(client_secrets_file),
        SCOPES,
        redirect_uri='http://localhost:8080/'
    )

    # This will open a browser window
    creds = flow.run_local_server(port=8080)

    # Save credentials
    creds_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    with open(creds_file, 'w') as f:
        json.dump(creds_data, f, indent=2)

    print()
    print("="*80)
    print("✅ SUCCESS!")
    print("="*80)
    print()
    print(f"Credentials saved to: {creds_file}")
    print()
    print("The product feed tracker will now use these credentials automatically.")
    print()
    print("To test:")
    print("  python3 product_feed_tracker.py")
    print()


if __name__ == "__main__":
    setup_oauth()
