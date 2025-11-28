#!/bin/bash
# Quick OAuth Setup for Monthly Report Generator
# This script helps you set up OAuth authentication for Google Slides API

set -e

echo "=========================================="
echo "OAuth Setup for Monthly Report Generator"
echo "=========================================="
echo ""

CREDENTIALS_DIR="$HOME/Documents/PetesBrain/shared/credentials"
OAUTH_FILE="$CREDENTIALS_DIR/google-slides-oauth.json"
TOKEN_FILE="$CREDENTIALS_DIR/google-slides-token.json"

echo "Step 1: Create OAuth Client ID"
echo "--------------------------------"
echo ""
echo "1. Go to: https://console.cloud.google.com/apis/credentials"
echo "2. Make sure 'PetesBrain Email Sync' project is selected"
echo "3. Click 'CREATE CREDENTIALS' → 'OAuth client ID'"
echo "4. If prompted to configure OAuth consent screen:"
echo "   - User Type: External"
echo "   - App name: PetesBrain Reports"
echo "   - User support email: Your email"
echo "   - Developer contact: Your email"
echo "   - Click SAVE AND CONTINUE through all steps"
echo "   - Add your email as a test user"
echo ""
echo "5. Back at Create OAuth client ID:"
echo "   - Application type: Desktop app"
echo "   - Name: monthly-report-generator"
echo "   - Click CREATE"
echo ""
echo "6. Click DOWNLOAD JSON (download icon)"
echo "7. The file will save to your Downloads folder"
echo ""
read -p "Press ENTER when you've downloaded the OAuth credentials JSON file..."

echo ""
echo "Step 2: Move OAuth Credentials"
echo "-------------------------------"
echo ""

# Find the most recent client_secret JSON in Downloads
DOWNLOAD_FILE=$(ls -t ~/Downloads/client_secret_*.json 2>/dev/null | head -1)

if [ -z "$DOWNLOAD_FILE" ]; then
    echo "❌ Could not find client_secret_*.json in Downloads folder"
    echo ""
    echo "Please manually move the file:"
    echo "  mv ~/Downloads/client_secret_*.json $OAUTH_FILE"
    exit 1
fi

echo "Found: $DOWNLOAD_FILE"
mv "$DOWNLOAD_FILE" "$OAUTH_FILE"
echo "✅ Moved to: $OAUTH_FILE"

echo ""
echo "Step 3: Test Authentication"
echo "----------------------------"
echo ""
echo "When you run the generator script for the first time, it will:"
echo "1. Open your browser"
echo "2. Ask you to sign in with your Google account"
echo "3. Ask you to authorize the app"
echo "4. Save the token for future use"
echo ""
echo "This is a ONE-TIME process. Future runs will use the saved token."
echo ""
echo "✅ OAuth setup complete!"
echo ""
echo "Next step: Run the generator script"
echo "  cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator"
echo "  .venv/bin/python3 generate_devonshire_slides.py --month 2025-10"
echo ""
