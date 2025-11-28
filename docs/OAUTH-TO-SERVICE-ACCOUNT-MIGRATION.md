# OAuth to Service Account Migration Guide

**Problem**: OAuth tokens expire every ~7 days causing browser popups and silent failures in automated tasks.

**Solution**: Migrate to Service Account authentication for all Google services.

## Current Authentication Status

### ✅ Already Using Service Accounts (No Issues)
- **Google Sheets** - `shared/mcp-servers/google-sheets-mcp-server/credentials.json`
- **Google Ads** - `~/google-ads.yaml`
- **Email Sync** - `shared/email-sync/credentials.json`

### ⚠️ Using OAuth (Needs Migration)
- **Google Tasks MCP** - `shared/mcp-servers/google-tasks-mcp-server/token.json`
- **Google Drive MCP** - `shared/mcp-servers/google-drive-mcp-server/` (OAuth based)
- **Google Photos MCP** - `shared/mcp-servers/google-photos-mcp-server/token.json`
- **Various Scripts** - Some scripts using `token.json` files

## Migration Steps

### Step 1: Create/Use Existing Service Account

You likely already have a service account from Google Sheets setup. Let's use that:

```bash
# Check if service account exists
ls -la /Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json
```

**If you need to create a new service account**:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (or create one)
3. Navigate to: **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
5. Name: "PetesBrain Automation"
6. Grant roles: **Editor** (or specific API roles)
7. Click **Keys** → **Add Key** → **JSON**
8. Save as `shared/service-account-credentials.json`

### Step 2: Enable Required APIs

In Google Cloud Console, enable these APIs for your project:
- ✅ Google Tasks API
- ✅ Google Drive API
- ✅ Google Photos Library API
- ✅ Google Sheets API (already enabled)
- ✅ Gmail API (if using email sync)

**Enable via Console**: [API Library](https://console.cloud.google.com/apis/library)

Or via command line:
```bash
gcloud services enable tasks.googleapis.com
gcloud services enable drive.googleapis.com
gcloud services enable photoslibrary.googleapis.com
```

### Step 3: Grant Service Account Access

**CRITICAL**: Service accounts can't access your personal Google data by default. You must:

#### For Google Tasks
**Option A**: Share task lists with service account email (easier, works immediately)
1. Get service account email from credentials file:
   ```bash
   cat shared/email-sync/credentials.json | grep client_email
   ```
   Example: `petesbrain-automation@your-project.iam.gserviceaccount.com`

2. Unfortunately, **Google Tasks doesn't support sharing with service accounts** ❌
   - Google Tasks is user-specific and can't be accessed by service accounts
   - **You MUST use OAuth for Google Tasks**

**Workaround**: Keep OAuth for Google Tasks, but make it more reliable (see Step 4 below)

#### For Google Drive
**Option B**: Domain-wide delegation (if you have Google Workspace)
1. Grant service account domain-wide delegation
2. Authorize scopes in Workspace admin

**Option A**: Share specific files/folders with service account
1. Get service account email: `cat shared/email-sync/credentials.json | grep client_email`
2. Share each Google Drive folder/file with this email address
3. Grant "Editor" or "Viewer" permissions

#### For Google Photos
Service accounts **cannot access Google Photos** ❌
- Google Photos API only works with OAuth user authentication
- **You MUST use OAuth for Google Photos**

### Step 4: Make OAuth More Reliable

Since Google Tasks and Google Photos **require OAuth**, let's make it work better:

#### Solution A: Long-Lived Refresh Tokens

Update OAuth apps to request "offline access" and store refresh tokens properly:

**For Google Tasks MCP**:
```python
# In tasks_service.py, ensure this is present:
flow = InstalledAppFlow.from_client_secrets_file(
    str(credentials_path),
    SCOPES,
    redirect_uri='http://localhost:8080'  # Consistent redirect
)
flow.run_local_server(port=8080, access_type='offline', prompt='consent')
```

The `access_type='offline'` ensures you get a refresh token that works for ~6 months.

#### Solution B: Pre-Authorize Once

Run a setup script to authorize all services at once:

```bash
# Create setup script
cat > shared/scripts/setup-oauth.sh << 'EOF'
#!/bin/bash

echo "=== OAuth Setup for Pete's Brain ==="
echo ""
echo "This will authorize all OAuth-based services once."
echo "Tokens will be refreshed automatically for ~6 months."
echo ""

# Google Tasks
echo "1. Authorizing Google Tasks..."
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server
.venv/bin/python -c "from tasks_service import tasks_service; tasks_service()"

# Google Drive
echo "2. Authorizing Google Drive..."
export GOOGLE_DRIVE_OAUTH_CREDENTIALS="/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json"
npx -y @piotr-agier/google-drive-mcp auth

# Google Photos
echo "3. Authorizing Google Photos..."
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server
.venv/bin/python server.py

echo ""
echo "✅ OAuth setup complete!"
echo "Tokens stored and will auto-refresh for ~6 months"
EOF

chmod +x shared/scripts/setup-oauth.sh
```

Run this once:
```bash
./shared/scripts/setup-oauth.sh
```

### Step 5: Update Services to Use Service Account Where Possible

#### Migrate Google Drive (If Possible)

**Check if you can use service account for your use case**:
- If you're only accessing files you own → Share them with service account
- If you're accessing shared drives → Add service account as member
- If you need broad access → Requires domain-wide delegation (Workspace only)

**Update Google Drive MCP to use service account**:

Edit `.mcp.json`:
```json
"google-drive": {
  "command": "npx",
  "args": ["-y", "@google-cloud/mcp-drive"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json"
  }
}
```

**Note**: The `@piotr-agier/google-drive-mcp` package only supports OAuth. You'd need to switch to a service-account-compatible package.

### Step 6: Consolidate Service Account Credentials

**Single source of truth**:
```bash
# Use the same service account everywhere
export SERVICE_ACCOUNT_PATH="/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json"

# Update all configs to point to this file
# Example: .mcp.json, LaunchAgents, scripts
```

## Recommended Configuration

### Final `.mcp.json` Setup

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json"
      }
    },
    "google-tasks": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/server.py"],
      "env": {
        "OAUTH_TOKEN_PATH": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/token.json"
      }
    },
    "google-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-ads-mcp-server/server.py"],
      "env": {
        "GOOGLE_ADS_YAML": "/Users/administrator/google-ads.yaml"
      }
    }
  }
}
```

## Summary: What You Can't Migrate

**OAuth Required (Can't Use Service Account)**:
- ❌ **Google Tasks** - API doesn't support service accounts
- ❌ **Google Photos** - API only works with user OAuth

**Solution**: Make OAuth reliable with refresh tokens + periodic re-authorization (every 6 months)

**Service Account Works**:
- ✅ **Google Sheets** - Already working
- ✅ **Google Drive** - If you share files with service account
- ✅ **Gmail** - Service account with domain-wide delegation
- ✅ **Google Ads** - Using YAML config (not OAuth)

## Testing After Migration

```bash
# Test each service manually
# Google Tasks
cd shared/mcp-servers/google-tasks-mcp-server
.venv/bin/python -c "from tasks_service import tasks_service; service = tasks_service(); print('✅ Google Tasks working')"

# Google Sheets (should already work)
cd shared/mcp-servers/google-sheets-mcp-server
GOOGLE_APPLICATION_CREDENTIALS=credentials.json .venv/bin/python server.py

# Check LaunchAgents still work
launchctl start com.petesbrain.tasks-monitor
cat ~/.petesbrain-tasks-monitor.log | tail -20
```

## Monitoring OAuth Health

Create a monitoring script:
```bash
#!/bin/bash
# shared/scripts/check-oauth-health.sh

echo "=== OAuth Token Health Check ==="
echo ""

for token in shared/mcp-servers/*/token.json; do
  if [ -f "$token" ]; then
    echo "Checking: $token"
    # Check if token is expired (requires jq)
    expiry=$(jq -r .expiry "$token" 2>/dev/null || echo "unknown")
    echo "  Expiry: $expiry"
  fi
done

echo ""
echo "Run ./shared/scripts/setup-oauth.sh to refresh all tokens"
```

## Quarterly Maintenance (Optional)

Add to calendar: **Re-authorize OAuth every 6 months**

```bash
# Set reminder for April 2026
# Run: ./shared/scripts/setup-oauth.sh
```
