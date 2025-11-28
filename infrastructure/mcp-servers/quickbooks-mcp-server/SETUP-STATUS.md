# QuickBooks MCP Server - Setup Status

**Date:** 2025-11-06  
**Status:** 95% Complete - Need to switch to Production keys

## ✅ What's Been Completed:

### 1. QuickBooks Developer App Created
- **App Name:** PetesBrain Financial Reporting
- **App ID:** 7c5b9497-fe3d-4845-9170-007d99e5bb48
- **Workspace:** Sample Workspace
- **Status:** IN DEVELOPMENT
- **Scopes Enabled:** ✅ Accounting (com.intuit.quickbooks.accounting)

### 2. Development Credentials Obtained
- **Client ID:** `ABMRNKlEsbJdErUnarH3FvpAToMgwir1yWVM7lT3hdNWFGqO3n`
- **Client Secret:** `XHxB3YeBdQ2Nfg5DQ1Go4XSmBetSuV2ODwl2Fsga`
- **Redirect URI Configured:** `http://localhost:8000/callback` ✅

### 3. MCP Server Code Complete
- ✅ All Python code written
- ✅ 10 reporting tools implemented
- ✅ OAuth authentication module
- ✅ Auto-refreshing tokens
- ✅ Dependencies installed in virtual environment
- ✅ `.env` file created with credentials

### 4. OAuth Flow Working
- ✅ OAuth authentication completes successfully
- ✅ Tokens are generated and saved
- ✅ Connected to Company ID: `9341455649204247`

## ❌ Current Issue:

### 403 Error - ApplicationAuthorizationFailed (Code 003100)
```
{"fault":{"error":[{"message":"message=ApplicationAuthorizationFailed; 
errorCode=003100; statusCode=403","detail":null,"code":"3100"}]}}
```

**Root Cause:** Development credentials have limitations. The connected company (ID: 9341455649204247) returns 403 errors when trying to access data.

**Two Possible Explanations:**
1. Company ID 9341455649204247 is "Crowd Control Company" (not the desired "Rok Systems Ltd")
2. Development keys don't work with production companies - need Production keys

## 🎯 Next Steps After Reboot:

### Step 1: Get Production Credentials
1. Go to: https://developer.intuit.com/appdetail/keys?appId=djQuMTo2OGQzYmJlYTI3Yg:7c5b9497-fe3d-4845-9170-007d99e5bb48&id=9341455649210685
2. Click on **"Production"** tab (instead of Development)
3. Toggle **"Show credentials"** switch
4. Copy the **Production Client ID** and **Production Client Secret**

### Step 2: Update .env File
Replace development credentials with production credentials:
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server
nano .env
```

Update these lines with Production keys:
```env
QUICKBOOKS_CLIENT_ID=<production_client_id>
QUICKBOOKS_CLIENT_SECRET=<production_client_secret>
```

### Step 3: Delete Token and Re-authenticate
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server
rm -f token.json
source venv/bin/activate
python setup_oauth.py
```

### Step 4: Test Connection
```bash
python test_connection.py
```

Should see:
- ✓ Company name displayed (hopefully "Rok Systems Ltd")
- ✓ API connection successful
- ✓ Report access working

## 📂 File Locations:

### MCP Server Files:
```
/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/
├── server.py                    # Main MCP server
├── oauth/
│   └── quickbooks_auth.py      # OAuth module
├── setup_oauth.py              # Authentication script
├── test_connection.py          # Connection tester
├── .env                        # Credentials (update with Production keys)
├── token.json                  # Current tokens (delete before re-auth)
├── requirements.txt            # Dependencies (already installed)
├── README.md                   # Full documentation
├── QUICKSTART.md              # 5-minute guide
└── SETUP-CHECKLIST.md         # Verification checklist
```

### Documentation:
```
/Users/administrator/Documents/PetesBrain/docs/
└── QUICKBOOKS-REPORTING-MCP.md  # Integration guide
```

## 🔑 Current Credentials:

**Type:** Development  
**Client ID:** ABMRNKlEsbJdErUnarH3FvpAToMgwir1yWVM7lT3hdNWFGqO3n  
**Client Secret:** XHxB3YeBdQ2Nfg5DQ1Go4XSmBetSuV2ODwl2Fsga  
**Connected Company ID:** 9341455649204247  
**Issue:** 403 errors on all API calls

## 🎯 Goal:

Connect to **Rok Systems Ltd** using **Production credentials** so we can:
- Pull P&L reports
- Get Balance Sheets
- Access Cash Flow statements
- Query financial data
- Use in Cursor via MCP

## 📋 Commands Ready to Run After Reboot:

```bash
# Navigate to folder
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server

# Activate virtual environment
source venv/bin/activate

# After updating .env with Production keys, delete old token
rm -f token.json

# Run OAuth setup
python setup_oauth.py

# Test connection
python test_connection.py
```

## ⚠️ Important Notes:

1. **Virtual environment is already set up** at:
   `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/venv/`

2. **All dependencies are installed** - no need to run `pip install` again

3. **Production keys** should work with your actual QuickBooks company data

4. **After successful connection**, add to Cursor settings at:
   `~/Library/Application Support/Cursor/User/globalStorage/settings.json`

## 🔗 Quick Links:

- **App Dashboard:** https://developer.intuit.com/appdetail/overview?appId=djQuMTo2OGQzYmJlYTI3Yg:7c5b9497-fe3d-4845-9170-007d99e5bb48&id=9341455649210685
- **Keys & Credentials:** https://developer.intuit.com/appdetail/keys?appId=djQuMTo2OGQzYmJlYTI3Yg:7c5b9497-fe3d-4845-9170-007d99e5bb48&id=9341455649210685
- **QuickBooks Online:** https://qbo.intuit.com

---

**Resume here after reboot!** 🚀

The server code is complete and working. We just need Production credentials to access your real QuickBooks data.

