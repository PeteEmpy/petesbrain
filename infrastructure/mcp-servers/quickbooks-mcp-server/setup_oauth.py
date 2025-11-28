#!/usr/bin/env python3
"""
QuickBooks OAuth 2.0 Setup Script

Run this script to authenticate with QuickBooks Online and obtain OAuth tokens.
"""

import os
import json
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('QUICKBOOKS_CLIENT_ID')
CLIENT_SECRET = os.getenv('QUICKBOOKS_CLIENT_SECRET')
REDIRECT_URI = os.getenv('QUICKBOOKS_REDIRECT_URI', 'http://localhost:8000/callback')
SCOPES = 'com.intuit.quickbooks.accounting'

# QuickBooks OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://appcenter.intuit.com/connect/oauth2'
TOKEN_URL = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'

# Storage
TOKEN_FILE = 'token.json'
auth_code = None
realm_id = None


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP server handler to receive OAuth callback"""
    
    def do_GET(self):
        """Handle GET request from OAuth callback"""
        global auth_code, realm_id
        
        # Parse the callback URL
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            realm_id = params.get('realmId', [None])[0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>QuickBooks OAuth Success</title></head>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        else:
            # Send error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error = params.get('error', ['Unknown error'])[0]
            self.wfile.write(f"""
                <html>
                <head><title>QuickBooks OAuth Error</title></head>
                <body>
                    <h1>Authentication Failed</h1>
                    <p>Error: {error}</p>
                </body>
                </html>
            """.encode())
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def get_authorization_url():
    """Generate the OAuth authorization URL"""
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPES,
        'state': 'security_token_' + os.urandom(8).hex()
    }
    
    url = f"{AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    return url


def exchange_code_for_token(code, realm_id):
    """Exchange authorization code for access token"""
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        TOKEN_URL,
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    
    if not response.ok:
        raise Exception(f"Token exchange failed: {response.status_code} - {response.text}")
    
    token_data = response.json()
    
    # Calculate expiration times
    expires_at = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
    refresh_expires_at = (datetime.now() + timedelta(seconds=token_data.get('x_refresh_token_expires_in', 8726400))).isoformat()
    
    # Store token data
    tokens = {
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
        'token_type': token_data['token_type'],
        'expires_at': expires_at,
        'refresh_expires_at': refresh_expires_at,
        'realmId': realm_id,
        'created_at': datetime.now().isoformat()
    }
    
    return tokens


def save_tokens(tokens):
    """Save tokens to file"""
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    print(f"\n✓ Tokens saved to {TOKEN_FILE}")


def main():
    """Main OAuth setup flow"""
    print("=" * 60)
    print("QuickBooks Online OAuth 2.0 Setup")
    print("=" * 60)
    
    # Check for required credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        print("\n❌ Error: Missing QuickBooks credentials!")
        print("\nPlease set the following environment variables:")
        print("  - QUICKBOOKS_CLIENT_ID")
        print("  - QUICKBOOKS_CLIENT_SECRET")
        print("\nYou can get these from: https://developer.intuit.com/app/developer/myapps")
        return
    
    print(f"\nClient ID: {CLIENT_ID[:10]}...{CLIENT_ID[-5:]}")
    print(f"Redirect URI: {REDIRECT_URI}")
    print(f"Scopes: {SCOPES}")
    
    # Start local server to receive callback
    print("\n📡 Starting local callback server on port 8000...")
    server = HTTPServer(('localhost', 8000), CallbackHandler)
    
    # Open authorization URL in browser
    auth_url = get_authorization_url()
    print("\n🌐 Opening authorization URL in your browser...")
    print(f"   {auth_url}\n")
    webbrowser.open(auth_url)
    
    print("⏳ Waiting for authorization callback...")
    print("   (Please complete the authorization in your browser)\n")
    
    # Wait for one request (the callback)
    server.handle_request()
    
    # Check if we got the authorization code
    if not auth_code:
        print("\n❌ Failed to receive authorization code")
        return
    
    if not realm_id:
        print("\n⚠️  Warning: No realm ID received")
    
    print(f"\n✓ Authorization code received")
    if realm_id:
        print(f"✓ Company ID (Realm ID): {realm_id}")
    
    # Exchange code for token
    print("\n🔄 Exchanging authorization code for access token...")
    try:
        tokens = exchange_code_for_token(auth_code, realm_id)
        save_tokens(tokens)
        
        print("\n" + "=" * 60)
        print("✅ QuickBooks OAuth Setup Complete!")
        print("=" * 60)
        print(f"\nAccess Token: {tokens['access_token'][:20]}...")
        print(f"Refresh Token: {tokens['refresh_token'][:20]}...")
        print(f"Expires At: {tokens['expires_at']}")
        if realm_id:
            print(f"Company ID: {realm_id}")
        
        print("\n📝 Next Steps:")
        print("  1. The server.py script will now be able to access QuickBooks")
        print("  2. Tokens will be automatically refreshed when needed")
        print("  3. Run the server with: python server.py")
        
    except Exception as e:
        print(f"\n❌ Error exchanging code for token: {str(e)}")


if __name__ == "__main__":
    main()

