# Meta Ads MCP Server - Detailed Setup Guide

This guide provides comprehensive step-by-step instructions for setting up the Meta Ads MCP Server with OAuth authentication.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Meta for Developers Configuration](#meta-for-developers-configuration)
3. [Application Setup](#application-setup)
4. [Environment Configuration](#environment-configuration)
5. [Testing Your Setup](#testing-your-setup)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Accounts

- **Facebook/Meta Account** - Personal or business account with admin access
- **Meta Business Manager** - Business account with ad accounts
- **Meta for Developers Account** - Developer account (free)

### Required Software

- **Python 3.10 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **Text editor** (for editing configuration files)

### Required Access

- **Ad Account Access** - Admin or Advertiser role on at least one ad account
- **Business Manager Access** - Access to the business that owns the ad accounts

## Meta for Developers Configuration

### Step 1: Create a Meta App

1. **Navigate to Meta for Developers**
   - Open https://developers.facebook.com/
   - Sign in with your Facebook account

2. **Access My Apps**
   - Click "My Apps" in the top navigation
   - Or go directly to https://developers.facebook.com/apps

3. **Create New App**
   - Click "Create App" button
   - You'll see several app type options

4. **Select App Type**
   - Choose **"Business"** as the app type
   - This is required for Marketing API access
   - Click "Next"

5. **Fill in App Details**
   ```
   Display Name: Meta Ads MCP
   App Contact Email: your-email@example.com
   Business Account: [Select your business]
   ```
   - If you don't have a business account, create one first
   - Click "Create App"

6. **Complete Security Check**
   - Enter your Facebook password if prompted
   - Complete any security verification

7. **Note Your App ID**
   - Once created, you'll see your **App ID** on the dashboard
   - Copy this ID - you'll need it later

### Step 2: Configure Basic Settings

1. **Navigate to Settings**
   - In your app dashboard, click "Settings" in left sidebar
   - Then click "Basic"

2. **Copy App Credentials**
   - **App ID**: Already copied (see above)
   - **App Secret**: Click "Show" to reveal, then copy
   - ⚠️ **Keep these credentials secure!**

3. **Add App Domains**
   - Scroll to "App Domains"
   - Add: `localhost`

4. **Add Platform**
   - Scroll to "Add Platform" section at bottom
   - Click "Add Platform"
   - Select **"Website"**
   - Site URL: `http://localhost:8080/`
   - Click "Save Changes"

5. **Privacy Policy (Optional but Recommended)**
   - Add a privacy policy URL if you have one
   - For internal use, you can use a simple statement

### Step 3: Enable Marketing API

1. **Add Product**
   - In left sidebar, click "+ Add Product"
   - Find **"Marketing API"**
   - Click "Set Up"

2. **Configure Marketing API**
   - You'll see the Marketing API dashboard
   - Click "Tools" in the Marketing API section

3. **Token Generation (for Testing)**
   - Go to "Tools" → "Token Generator"
   - Select your app
   - Select permissions:
     - ✅ `ads_read`
     - ✅ `ads_management`
     - ✅ `business_management`
   - This generates a test token (optional - OAuth will create the real one)

### Step 4: Configure OAuth Settings

1. **Navigate to OAuth Settings**
   - Settings → Basic → scroll to "OAuth" section

2. **Valid OAuth Redirect URIs**
   - Add: `http://localhost:8080/`
   - This must match exactly (including trailing slash)
   - Click "Save Changes"

3. **Client OAuth Settings**
   - Ensure these are enabled:
     - ✅ Client OAuth Login: **Yes**
     - ✅ Web OAuth Login: **Yes**
     - ✅ Enforce HTTPS: **No** (for local development)

### Step 5: App Review and Permissions

1. **Navigate to App Review**
   - Click "App Review" in left sidebar
   - Then "Permissions and Features"

2. **Required Permissions**
   - These should already be available for Business apps:
     - `ads_read` - Read ad account data
     - `ads_management` - Manage ad campaigns
     - `business_management` - Access business info

3. **Check Permission Status**
   - If permissions show as "Requires Review", you may need to submit for review
   - For internal business use, permissions are usually auto-approved

### Step 6: Make App Live

1. **Switch App Mode**
   - At the top of the dashboard, you'll see a toggle
   - It will show "Development" mode by default
   - Click the toggle to switch to **"Live"** mode

2. **Review Checklist**
   - Meta may show a checklist of requirements
   - For a business app with Marketing API, requirements are minimal:
     - ✅ App icon (optional but recommended)
     - ✅ Privacy policy URL (optional for internal use)
     - ✅ Terms of Service URL (optional for internal use)

3. **Confirm Live Status**
   - The toggle should now show "Live" with a green indicator
   - Your app can now access production ad accounts

## Application Setup

### Step 1: Navigate to Project Directory

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/meta-ads-mcp-server
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Verify creation
ls -la venv/
```

Expected output: You should see `bin/`, `lib/`, `include/` directories

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Collecting fastmcp>=2.8.0
Collecting requests>=2.32.3
Collecting python-dotenv>=1.0.0
...
Successfully installed fastmcp-2.8.0 requests-2.32.3 python-dotenv-1.0.0
```

### Step 5: Verify Installation

```bash
python -c "import fastmcp; import requests; print('All dependencies installed successfully!')"
```

## Environment Configuration

### Step 1: Create .env File

```bash
# Copy the example file
cp env.example .env
```

### Step 2: Edit .env File

Open `.env` in your text editor:

```bash
nano .env
# or
vim .env
# or use any text editor
```

### Step 3: Add Your Credentials

Replace the placeholder values with your actual credentials:

```bash
# Meta (Facebook) Ads API Configuration

# Required: Meta App ID from Meta for Developers
META_APP_ID=1234567890123456

# Required: Meta App Secret from Meta for Developers
META_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Optional: Custom path to store OAuth token
# Leave commented out to use default location
# META_TOKEN_PATH=/custom/path/to/meta_ads_token.json
```

**Where to find these values:**
- `META_APP_ID`: Meta for Developers → Your App → Settings → Basic → App ID
- `META_APP_SECRET`: Meta for Developers → Your App → Settings → Basic → App Secret (click "Show")

### Step 4: Secure Your .env File

```bash
# Set restrictive permissions
chmod 600 .env

# Verify permissions
ls -l .env
```

Expected output: `-rw-------` (owner read/write only)

### Step 5: Verify Configuration

```bash
# Test that environment variables load correctly
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('App ID:', os.getenv('META_APP_ID')[:4] + '...' if os.getenv('META_APP_ID') else 'Not set')"
```

Expected output: `App ID: 1234...` (showing first 4 digits)

## Testing Your Setup

### Step 1: Test OAuth Module

```bash
# Test OAuth imports
python -c "from oauth.meta_auth import get_oauth_credentials; print('OAuth module loaded successfully!')"
```

### Step 2: Test Server Startup

```bash
# Start server in test mode (will exit immediately)
python server.py --help 2>&1 | head -n 5
```

### Step 3: Test Complete Authentication Flow

```bash
# Run a test authentication
python -c "
from oauth.meta_auth import get_oauth_credentials
print('Testing OAuth flow...')
token = get_oauth_credentials()
print(f'✅ Authentication successful! Token: {token[:20]}...')
"
```

**What should happen:**
1. Your browser opens to Facebook login
2. You see "Meta Ads MCP would like to access your account"
3. You click "Continue" or "Allow"
4. Browser shows "✅ Authentication Successful!"
5. Terminal shows success message
6. A `meta_ads_token.json` file is created

### Step 4: Verify Token Storage

```bash
# Check token file exists
ls -l meta_ads_token.json

# Verify token structure (without exposing token)
python -c "
import json
with open('meta_ads_token.json', 'r') as f:
    data = json.load(f)
print('Token file structure:')
print('- Has access_token:', 'access_token' in data)
print('- Has token_type:', 'token_type' in data)
print('- Has obtained_at:', 'obtained_at' in data)
"
```

Expected output:
```
Token file structure:
- Has access_token: True
- Has token_type: True
- Has obtained_at: True
```

### Step 5: Test API Access

```bash
# Test listing ad accounts
python -c "
from oauth.meta_auth import get_headers_with_auto_token
import requests

headers, access_token = get_headers_with_auto_token()
url = 'https://graph.facebook.com/v22.0/me/adaccounts'
params = {'access_token': access_token, 'fields': 'account_id,name'}
response = requests.get(url, params=params)

if response.ok:
    data = response.json()
    print(f'✅ API access successful!')
    print(f'Found {len(data.get(\"data\", []))} ad accounts')
else:
    print(f'❌ API error: {response.status_code} - {response.text}')
"
```

Expected output:
```
✅ API access successful!
Found 3 ad accounts
```

## Troubleshooting

### Issue: "Invalid App ID or Secret"

**Cause:** Incorrect credentials in `.env` file

**Solution:**
1. Verify App ID and Secret in Meta for Developers
2. Check for extra spaces or quotes in `.env`
3. Ensure `.env` file is in the correct directory
4. Reload environment: `source venv/bin/activate`

### Issue: "Redirect URI Mismatch"

**Cause:** OAuth redirect URI not configured correctly

**Solution:**
1. Go to Meta for Developers → Your App → Settings → Basic
2. Under "OAuth Settings", verify:
   - Valid OAuth Redirect URIs includes: `http://localhost:8080/`
   - Exact match including trailing slash
3. Under "Website" platform, verify:
   - Site URL: `http://localhost:8080/`
4. Save changes and try again

### Issue: "App Not in Live Mode"

**Cause:** App is still in Development mode

**Solution:**
1. Go to Meta for Developers → Your App
2. Toggle at top of page from "Development" to "Live"
3. Confirm the switch
4. Try authentication again

### Issue: "Permissions Error"

**Cause:** Missing required permissions

**Solution:**
1. Go to Meta for Developers → Your App → App Review
2. Check "Permissions and Features"
3. Ensure these are approved:
   - `ads_read`
   - `ads_management`
   - `business_management`
4. If not approved, click "Request" for each

### Issue: "No Ad Accounts Found"

**Cause:** Authenticated user doesn't have ad account access

**Solution:**
1. Verify the Facebook account you're using has ad account access
2. Go to Meta Business Manager → Ad Accounts
3. Check you have at least "Advertiser" role
4. Try authenticating again with the correct account

### Issue: "Token Expired"

**Cause:** Token exceeded 60-day validity

**Solution:**
```bash
# Delete old token
rm meta_ads_token.json

# Re-authenticate
python -c "from oauth.meta_auth import get_oauth_credentials; get_oauth_credentials()"
```

### Issue: "Port Already in Use"

**Cause:** Port 8080 is being used by another application

**Solution:**
1. Find and stop the process using port 8080:
   ```bash
   lsof -i :8080
   kill -9 [PID]
   ```
2. Or modify the port in `oauth/meta_auth.py`:
   ```python
   OAUTH_CALLBACK_PORT = 8081  # Change to available port
   ```
3. Update redirect URI in Meta for Developers to match

### Issue: "Module Not Found"

**Cause:** Dependencies not installed or wrong Python environment

**Solution:**
```bash
# Verify you're in venv
which python
# Should show: /Users/.../meta-ads-mcp-server/venv/bin/python

# If not, activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

Once setup is complete:

1. **Configure Claude Desktop** - See README.md for integration steps
2. **Test with Claude** - Try basic commands like "List my Meta ad accounts"
3. **Read QUICKSTART.md** - Learn PetesBrain-specific workflows
4. **Explore API** - Check the resource documentation in server.py

## Support Resources

- **Meta for Developers Docs**: https://developers.facebook.com/docs/marketing-api
- **Marketing API Reference**: https://developers.facebook.com/docs/marketing-api/reference
- **OAuth Documentation**: https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow
- **Business Manager Help**: https://www.facebook.com/business/help

## Security Checklist

Before going live, verify:

- [ ] `.env` file has secure permissions (600)
- [ ] `meta_ads_token.json` is gitignored
- [ ] App Secret is never logged or printed
- [ ] Token file is in a secure location
- [ ] Access is limited to necessary users
- [ ] Regular token rotation is scheduled
- [ ] Audit logs are enabled in Business Manager

---

**Setup Complete!** 🎉

Your Meta Ads MCP Server is now configured and ready to use with Claude Desktop and PetesBrain.

