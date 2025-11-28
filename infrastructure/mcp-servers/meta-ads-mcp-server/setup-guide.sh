#!/bin/bash
# Meta Ads MCP Server Setup Guide
# This script provides interactive setup assistance

set -e

echo "=========================================="
echo "Meta Ads MCP Server Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "server.py" ]; then
    echo "❌ Error: Please run this script from the meta-ads-mcp-server directory"
    exit 1
fi

echo "✅ Directory check passed"
echo ""

# Step 1: Meta App Creation
echo "📋 STEP 1: Meta Business App"
echo "----------------------------------------"
echo "You need to create a Meta Business App:"
echo ""
echo "1. Go to: https://developers.facebook.com/"
echo "2. Click 'My Apps' → 'Create App'"
echo "3. Select 'Business' as app type"
echo "4. Fill in:"
echo "   - Display Name: Meta Ads MCP"
echo "   - App Contact Email: [your email]"
echo "   - Business Account: [your business]"
echo "5. Click 'Create App'"
echo ""
read -p "Have you created the app? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please create the app first, then run this script again."
    exit 0
fi

echo "✅ App created"
echo ""

# Step 2: Get credentials
echo "📋 STEP 2: Get App Credentials"
echo "----------------------------------------"
echo "In your Meta app dashboard:"
echo "1. Go to Settings → Basic"
echo "2. Copy your App ID"
echo "3. Click 'Show' next to App Secret and copy it"
echo ""
read -p "Enter your App ID: " APP_ID
read -p "Enter your App Secret: " APP_SECRET
echo ""

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "❌ Error: App ID and Secret are required"
    exit 1
fi

echo "✅ Credentials captured"
echo ""

# Step 3: Configure OAuth
echo "📋 STEP 3: Configure OAuth Settings"
echo "----------------------------------------"
echo "In your Meta app dashboard:"
echo "1. Go to Settings → Basic"
echo "2. Scroll to 'Add Platform' → Select 'Website'"
echo "3. Site URL: http://localhost:8080/"
echo "4. Under OAuth Settings:"
echo "   - Valid OAuth Redirect URIs: http://localhost:8080/"
echo "5. Save Changes"
echo ""
read -p "Have you configured OAuth? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please configure OAuth first, then run this script again."
    exit 0
fi

echo "✅ OAuth configured"
echo ""

# Step 4: Enable Marketing API
echo "📋 STEP 4: Enable Marketing API"
echo "----------------------------------------"
echo "In your Meta app dashboard:"
echo "1. Click '+ Add Product'"
echo "2. Find 'Marketing API'"
echo "3. Click 'Set Up'"
echo ""
read -p "Have you enabled Marketing API? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please enable Marketing API first, then run this script again."
    exit 0
fi

echo "✅ Marketing API enabled"
echo ""

# Step 5: Set app to Live
echo "📋 STEP 5: Switch App to Live Mode"
echo "----------------------------------------"
echo "At the top of your app dashboard:"
echo "1. Toggle from 'Development' to 'Live'"
echo "2. Confirm the switch"
echo ""
read -p "Have you set the app to Live? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please set app to Live first, then run this script again."
    exit 0
fi

echo "✅ App is Live"
echo ""

# Step 6: Create .env file
echo "📋 STEP 6: Creating .env File"
echo "----------------------------------------"

cat > .env << EOF
# Meta (Facebook) Ads API Configuration

# Required: Meta App ID from Meta for Developers
META_APP_ID=$APP_ID

# Required: Meta App Secret from Meta for Developers
META_APP_SECRET=$APP_SECRET

# Optional: Custom path to store OAuth token
# If not specified, defaults to meta_ads_token.json in the project directory
# META_TOKEN_PATH=/custom/path/to/meta_ads_token.json
EOF

chmod 600 .env

echo "✅ .env file created with secure permissions"
echo ""

# Step 7: Create virtual environment
echo "📋 STEP 7: Creating Virtual Environment"
echo "----------------------------------------"

if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Recreate it? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Step 8: Install dependencies
echo "📋 STEP 8: Installing Dependencies"
echo "----------------------------------------"

source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Step 9: Test imports
echo "📋 STEP 9: Testing Module Imports"
echo "----------------------------------------"

python -c "
from oauth.meta_auth import get_oauth_credentials
from dotenv import load_dotenv
import os

load_dotenv()

app_id = os.getenv('META_APP_ID')
app_secret = os.getenv('META_APP_SECRET')

if not app_id or not app_secret:
    print('❌ Error: Credentials not loaded')
    exit(1)

print('✅ Modules imported successfully')
print(f'✅ App ID loaded: {app_id[:4]}...')
print('✅ App Secret loaded: [hidden]')
"

echo ""

# Final instructions
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Restart Claude Desktop to load the server"
echo ""
echo "2. Test authentication in Claude:"
echo "   \"List all my Meta ad accounts\""
echo ""
echo "3. Complete OAuth flow in browser"
echo ""
echo "4. Your token will be saved to: meta_ads_token.json"
echo ""
echo "For troubleshooting, see:"
echo "  - README.md (usage guide)"
echo "  - SETUP.md (detailed setup)"
echo "  - QUICKSTART.md (PetesBrain integration)"
echo ""
echo "=========================================="
echo ""

