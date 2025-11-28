# OAuth Quick Start - 5 Minutes to Working Slides

This replaces the service account approach with OAuth, which works immediately without complex permission setup.

## What Changed

**Before (Service Account)**: Required domain-wide delegation setup, couldn't create files
**Now (OAuth)**: One-time browser login, works immediately

## Setup (5 minutes)

### Step 1: Run Setup Script

```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
./setup-oauth.sh
```

The script will guide you through:

1. **Creating OAuth Client ID** in Google Cloud Console:
   - Go to https://console.cloud.google.com/apis/credentials
   - Select "PetesBrain Email Sync" project
   - Click "CREATE CREDENTIALS" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     * User Type: External
     * App name: PetesBrain Reports
     * Add your email as test user
   - Application type: **Desktop app**
   - Name: monthly-report-generator
   - Click CREATE and DOWNLOAD JSON

2. **Move credentials** (script does this automatically):
   - Moves `client_secret_*.json` to `google-slides-oauth.json`

### Step 2: First Run (One-Time Authentication)

```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
.venv/bin/python3 generate_devonshire_slides.py --month 2025-10
```

**What happens**:
1. Script opens your browser
2. You sign in with your Google account
3. You authorize "PetesBrain Reports" to access Slides and Drive
4. Token saved to `google-slides-token.json`
5. Presentation created with formatted tables

**Future runs**: Token is reused, no browser needed.

## Usage

After initial setup, generating reports is one command:

```bash
.venv/bin/python3 generate_devonshire_slides.py --month 2025-11
```

Replace `2025-11` with the month you want.

## What You Get

✅ **Estate Blue (#00333D) headers** with white text
✅ **Stone (#E5E3DB) backgrounds** for data cells
✅ **Editable native tables** (not images)
✅ **Professional formatting** matching September deck
✅ **Works immediately** - no admin permissions needed

## Troubleshooting

### "Credentials file not found"

Make sure you ran `./setup-oauth.sh` and downloaded the OAuth credentials.

Expected file: `~/Documents/PetesBrain/shared/credentials/google-slides-oauth.json`

### "Access blocked: PetesBrain Reports has not completed the verification"

This is expected for internal tools. Click "Advanced" → "Go to PetesBrain Reports (unsafe)" to proceed.

This is safe - it's your own app accessing your own account.

### Browser doesn't open

The script will print a URL. Copy and paste it into your browser manually.

## Technical Details

**OAuth Flow**:
1. First run: Opens browser for authorization
2. Token saved: `~/Documents/PetesBrain/shared/credentials/google-slides-token.json`
3. Future runs: Token refreshed automatically

**Permissions**:
- `presentations` - Create and edit Google Slides
- `drive.file` - Manage files created by the app

**Token Expiry**: Refresh token lasts indefinitely, access token refreshed automatically.

## Time Saved

- **Setup**: 5 minutes (one-time)
- **Monthly usage**: 2 minutes
- **vs Manual**: Save 2-3 hours per month
- **Annual savings**: ~30 hours

---

**Last Updated**: 2025-11-02
**Status**: Production Ready ✅
