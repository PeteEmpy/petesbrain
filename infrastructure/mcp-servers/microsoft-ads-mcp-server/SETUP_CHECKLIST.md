# Microsoft Ads MCP Server Setup Checklist

## Prerequisites
- [ ] Python 3.10+ installed
- [ ] Microsoft Advertising account created
- [ ] Azure account (for App Registration)

## Step 1: Azure App Registration
- [ ] Created Azure App Registration
- [ ] Noted Application (Client) ID → `MICROSOFT_ADS_CLIENT_ID`
- [ ] Created Client Secret → `MICROSOFT_ADS_CLIENT_SECRET`
- [ ] Configured Redirect URI: `http://localhost:8080`
- [ ] Added API permissions:
  - [ ] `ads.manage` (Delegated)
  - [ ] `offline_access` (Delegated)
- [ ] Granted admin consent (if admin)

## Step 2: Microsoft Advertising API
- [ ] Signed in to Microsoft Advertising
- [ ] Navigated to Tools → API Center
- [ ] Applied for Developer Token
- [ ] Received Developer Token → `MICROSOFT_ADS_DEVELOPER_TOKEN`

## Step 3: OAuth Authentication
- [ ] Ran authorization URL script to get authorization code
- [ ] Exchanged authorization code for refresh token
- [ ] Saved Refresh Token → `MICROSOFT_ADS_REFRESH_TOKEN`

## Step 4: Installation
- [ ] Created virtual environment: `python3 -m venv .venv`
- [ ] Activated virtual environment: `source .venv/bin/activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Created `.env` file from `env.example`
- [ ] Added all credentials to `.env`:
  - [ ] `MICROSOFT_ADS_CLIENT_ID`
  - [ ] `MICROSOFT_ADS_CLIENT_SECRET`
  - [ ] `MICROSOFT_ADS_DEVELOPER_TOKEN`
  - [ ] `MICROSOFT_ADS_REFRESH_TOKEN`
  - [ ] `MICROSOFT_ADS_CUSTOMER_ID` (optional)

## Step 5: Configuration
- [ ] Added server to `.mcp.json`
- [ ] Set secure file permissions: `chmod 600 .env`
- [ ] Verified all paths are absolute

## Step 6: Testing
- [ ] Restarted Claude Desktop
- [ ] Tested: "List all my Microsoft Ads accounts"
- [ ] Verified accounts are listed correctly
- [ ] Tested campaign retrieval
- [ ] Tested performance reporting

## Troubleshooting
If issues occur:
- [ ] Check `.env` file exists and has correct values
- [ ] Verify virtual environment is activated
- [ ] Check Python version: `python3 --version` (should be 3.10+)
- [ ] Verify all dependencies installed: `pip list`
- [ ] Check Claude Desktop logs for errors
- [ ] Verify Azure App Registration permissions
- [ ] Confirm Developer Token is valid

## Security Checklist
- [ ] `.env` file is in `.gitignore`
- [ ] File permissions set: `chmod 600 .env`
- [ ] Credentials not committed to version control
- [ ] Refresh token stored securely
- [ ] API permissions are minimal required

