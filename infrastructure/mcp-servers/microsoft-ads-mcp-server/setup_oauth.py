#!/usr/bin/env python3
"""
Microsoft Ads OAuth Setup Helper

This script helps you complete the OAuth flow to get your refresh token.
"""

import urllib.parse
import requests
import sys
from pathlib import Path

def print_auth_url():
    """Print the authorization URL for the user to visit."""
    print("=" * 60)
    print("Microsoft Ads OAuth Setup")
    print("=" * 60)
    print()
    
    client_id = input("Enter your Azure App Client ID: ").strip()
    
    if not client_id:
        print("Error: Client ID is required")
        sys.exit(1)
    
    redirect_uri = "http://localhost:8080"
    scope = "https://ads.microsoft.com/msads.manage offline_access"
    
    auth_url = (
        f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
        f"response_mode=query&"
        f"scope={urllib.parse.quote(scope)}"
    )
    
    print()
    print("Step 1: Visit this URL in your browser:")
    print("-" * 60)
    print(auth_url)
    print("-" * 60)
    print()
    print("Step 2: After authorization, you'll be redirected to:")
    print(f"  {redirect_uri}?code=AUTHORIZATION_CODE")
    print()
    print("Step 3: Copy the 'code' parameter from the URL")
    print()
    
    return client_id

def exchange_code_for_token(client_id: str):
    """Exchange authorization code for refresh token."""
    client_secret = input("Enter your Azure App Client Secret: ").strip()
    
    if not client_secret:
        print("Error: Client Secret is required")
        sys.exit(1)
    
    code = input("Enter the authorization code from the redirect URL: ").strip()
    
    if not code:
        print("Error: Authorization code is required")
        sys.exit(1)
    
    redirect_uri = "http://localhost:8080"
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'scope': 'https://ads.microsoft.com/msads.manage offline_access'
    }
    
    print()
    print("Exchanging authorization code for tokens...")
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        
        tokens = response.json()
        
        print()
        print("=" * 60)
        print("✅ Success! Tokens retrieved")
        print("=" * 60)
        print()
        print("Add these to your .env file:")
        print("-" * 60)
        print(f"MICROSOFT_ADS_CLIENT_ID={client_id}")
        print(f"MICROSOFT_ADS_CLIENT_SECRET={client_secret}")
        print(f"MICROSOFT_ADS_REFRESH_TOKEN={tokens.get('refresh_token')}")
        print("-" * 60)
        print()
        print("⚠️  Save the refresh token securely - you'll need it for the MCP server!")
        print()
        
        # Optionally save to .env.example
        env_file = Path(__file__).parent / ".env.example"
        if env_file.exists():
            save = input("Save to .env.example? (y/n): ").strip().lower()
            if save == 'y':
                # Note: This would require updating the file, but we'll just show it
                print("Update .env.example manually with the values above")
        
    except requests.exceptions.RequestException as e:
        print()
        print("=" * 60)
        print("❌ Error exchanging code for token")
        print("=" * 60)
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    print()
    client_id = print_auth_url()
    print()
    proceed = input("Press Enter after you've copied the authorization code, or 'q' to quit: ")
    
    if proceed.lower() != 'q':
        exchange_code_for_token(client_id)

