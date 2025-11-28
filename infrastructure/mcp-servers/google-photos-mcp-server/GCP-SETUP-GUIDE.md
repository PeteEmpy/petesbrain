# Google Cloud Platform Setup Guide

Follow these steps to enable the Google Photos Library API and create OAuth credentials.

## Step 1: Create/Select GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Either select an existing project or create a new one:
   - Click project dropdown at top
   - Click "New Project"
   - Name: "PetesBrain Google Photos" (or similar)
   - Click "Create"

## Step 2: Enable Google Photos Library API

1. In the Google Cloud Console, navigate to **APIs & Services > Library**
2. Search for "Google Photos Library API"
3. Click on it
4. Click **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Select **External** user type (unless you have Google Workspace)
3. Click **Create**
4. Fill in required fields:
   - **App name**: "PetesBrain Google Photos Access"
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **Save and Continue**
6. **Scopes** page:
   - Click **Add or Remove Scopes**
   - Search for "photoslibrary"
   - Select: `https://www.googleapis.com/auth/photoslibrary.readonly`
   - Click **Update**
   - Click **Save and Continue**
7. **Test users** page:
   - Click **Add Users**
   - Add your Google account email
   - Click **Save and Continue**
8. Review and click **Back to Dashboard**

## Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Application type: **Desktop app**
4. Name: "Google Photos MCP Server"
5. Click **Create**
6. **Download JSON**:
   - Click the download button (⬇) next to your newly created OAuth client
   - Save the file as `credentials.json`
   - Move it to: `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/credentials.json`

## Step 5: Verify File Location

```bash
ls -la /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/credentials.json
```

You should see the credentials.json file.

## Important Notes

- **OAuth App Status**: Your app will be in "Testing" mode initially. This is fine for personal use.
- **Test Users**: Only accounts added as test users can authenticate (in Testing mode)
- **Scopes**: We're using `photoslibrary.readonly` for read-only access (safe)
- **Token Refresh**: The OAuth token will auto-refresh, no manual intervention needed

## Scopes Explained

- `https://www.googleapis.com/auth/photoslibrary.readonly` - Read-only access to:
  - Albums
  - Media items (photos/videos)
  - Metadata
  - Search functionality

## Next Steps

After completing these steps, return to the terminal and continue with the MCP server setup.
