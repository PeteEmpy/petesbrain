# Google Photos MCP Server - Quick Start

Get up and running with the Google Photos MCP server in 10 minutes.

## Prerequisites Checklist

- [ ] Google account with Google Photos
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Internet connection
- [ ] 10 minutes of time

## Setup Steps

### 1. Google Cloud Platform Setup (5 minutes)

Open [GCP-SETUP-GUIDE.md](GCP-SETUP-GUIDE.md) and follow these steps:

1. **Create GCP project** or select existing
2. **Enable API**: Google Photos Library API
3. **OAuth consent screen**:
   - App name: "PetesBrain Google Photos"
   - Add your email as test user
4. **Create credentials**: OAuth 2.0 Desktop app
5. **Download** `credentials.json` to this folder

**Result:** You should have `credentials.json` in this directory.

### 2. Run Setup Script (3 minutes)

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server
./setup-oauth.sh
```

**What happens:**
1. Creates Python virtual environment
2. Installs dependencies
3. Opens browser for Google sign-in
4. You grant permission (read-only access)
5. Token saved to `token.json`

**Result:** You'll see "✅ SUCCESS! OAuth authentication complete."

### 3. Update .mcp.json (1 minute)

Add this to `.mcp.json` in the PetesBrain root:

```json
{
  "mcpServers": {
    "google-photos": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/server.py"],
      "env": {
        "GOOGLE_PHOTOS_OAUTH_CREDENTIALS": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-photos-mcp-server/credentials.json"
      }
    }
  }
}
```

**Don't forget the comma** after the previous server entry!

### 4. Restart Claude Code (1 minute)

Fully quit and restart Claude Code to load the new MCP server.

## Test It Works

In Claude Code, try these commands:

### Test 1: List Albums
```
Show me all my Google Photos albums
```

Claude will call `mcp__google-photos__list_albums` and display your albums.

### Test 2: Search Recent Photos
```
Find photos I took in the last week
```

Claude will calculate dates and call `mcp__google-photos__search_media`.

### Test 3: Get Photo Details
```
Show me details about album [album-name]
```

## Common First-Time Issues

### "credentials.json not found"

**Fix:** Download OAuth credentials from Google Cloud Console
- Go to APIs & Services > Credentials
- Download the OAuth 2.0 Client ID you created
- Save as `credentials.json` in this folder

### "Access blocked: Authorization Error"

**Fix:** Add yourself as test user
- Go to APIs & Services > OAuth consent screen
- Scroll to "Test users"
- Click "+ ADD USERS"
- Add your Google account email
- Try `./setup-oauth.sh` again

### "Token expired"

**Fix:** Delete and regenerate
```bash
rm token.json
./setup-oauth.sh
```

### MCP tools not showing up

**Fix:** Check Claude Code loaded the server
- Verify `.mcp.json` has correct paths (absolute, not relative)
- Restart Claude Code completely (quit, not just refresh)
- Check for typos in server name

## What You Can Do Now

### Browse Your Library
```
List all my Google Photos albums
```

### Search by Date
```
Find photos from July 2024
```

### Get Album Contents
```
Show me all photos in my "Vacation 2024" album
```

### Download Photos
```
Get download URL for photo [photo-id]
```

### Check EXIF Data
```
What camera was used to take photo [photo-id]?
```

## Next Steps

- Read [README.md](README.md) for complete tool documentation
- Explore all available MCP tools
- See [GCP-SETUP-GUIDE.md](GCP-SETUP-GUIDE.md) for advanced configuration

## Quick Reference

**Files:**
- `credentials.json` - OAuth client credentials (download from GCP)
- `token.json` - Your access token (auto-generated, auto-refreshed)
- `.venv/` - Python virtual environment

**Commands:**
```bash
# Re-run OAuth setup
./setup-oauth.sh

# Test authentication manually
source .venv/bin/activate
python3 -c "from server import GooglePhotosService; s = GooglePhotosService(); print('✓ OK')"

# View your token
cat token.json | python3 -m json.tool
```

**MCP Tools:**
- `mcp__google-photos__list_albums`
- `mcp__google-photos__get_album`
- `mcp__google-photos__list_album_contents`
- `mcp__google-photos__search_media`
- `mcp__google-photos__get_media_item`
- `mcp__google-photos__download_media`

## Help

- **Detailed docs:** [README.md](README.md)
- **GCP setup:** [GCP-SETUP-GUIDE.md](GCP-SETUP-GUIDE.md)
- **Troubleshooting:** See README.md "Troubleshooting" section

---

**Total setup time:** ~10 minutes
**Difficulty:** Easy (mostly clicking through Google Cloud Console)
**Result:** Full Google Photos access in Claude Code
