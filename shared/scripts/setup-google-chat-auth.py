#!/usr/bin/env python3
"""
Setup Google Chat API Authentication

Re-authenticates with Google Chat API scopes using existing OAuth credentials.
"""

import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/tasks",  # Keep existing scopes
    "https://www.googleapis.com/auth/calendar.readonly"  # Keep existing scopes
]

def setup_chat_auth():
    """Setup Google Chat API authentication"""
    token_path = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server" / "token.json"
    credentials_path = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server" / "credentials.json"
    
    if not credentials_path.exists():
        print(f"❌ Credentials file not found at: {credentials_path}")
        print("   Please ensure credentials.json exists")
        return False
    
    print("=" * 60)
    print("  Google Chat API Authentication Setup")
    print("=" * 60)
    print()
    print(f"Credentials: {credentials_path}")
    print(f"Token will be saved to: {token_path}")
    print()
    print("This will open a browser window for authentication.")
    print("Please authorize the Chat API scopes.")
    print()
    
    try:
        # Check if we have existing token
        creds = None
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                if creds.valid:
                    print("✅ Existing token is valid with Chat API scopes!")
                    return True
            except Exception as e:
                print(f"⚠️  Existing token doesn't have Chat scopes: {e}")
                print("   Will re-authenticate...")
                print()
        
        # Run OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path), 
            SCOPES
        )
        
        print("Opening browser for authentication...")
        creds = flow.run_local_server(port=0)
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
        
        print()
        print("✅ Authentication successful!")
        print(f"   Token saved to: {token_path}")
        print()
        print("You can now use the Google Chat processors.")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_chat_auth()
    sys.exit(0 if success else 1)

