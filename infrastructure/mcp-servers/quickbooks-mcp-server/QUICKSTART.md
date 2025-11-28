# QuickBooks MCP Server - Quick Start

Get up and running with QuickBooks reporting in 5 minutes.

## Step 1: Create QuickBooks App (2 minutes)

1. Go to https://developer.intuit.com/app/developer/myapps
2. Click **"Create an app"** → Select **"QuickBooks Online and Payments"**
3. Fill in:
   - App Name: `PetesBrain QuickBooks`
   - Description: `Financial reporting MCP server`
4. Go to **Keys & OAuth** tab:
   - Copy your **Client ID** and **Client Secret**
   - Add Redirect URI: `http://localhost:8000/callback`
5. Go to **Scopes** tab:
   - Enable: ✅ **Accounting**

## Step 2: Install & Configure (1 minute)

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env

# Edit .env with your credentials
nano .env
```

Paste your credentials:
```env
QUICKBOOKS_CLIENT_ID=your_client_id_from_step_1
QUICKBOOKS_CLIENT_SECRET=your_client_secret_from_step_1
QUICKBOOKS_REDIRECT_URI=http://localhost:8000/callback
```

## Step 3: Authenticate (1 minute)

```bash
python setup_oauth.py
```

- Browser will open automatically
- Log in to QuickBooks
- Select your company
- Click "Authorize"
- Done! ✅

## Step 4: Add to Cursor (1 minute)

Edit Cursor settings: `~/Library/Application Support/Cursor/User/globalStorage/settings.json`

Add:
```json
{
  "mcpServers": {
    "quickbooks-reporting": {
      "command": "python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/server.py"],
      "env": {
        "QUICKBOOKS_CLIENT_ID": "your_client_id",
        "QUICKBOOKS_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

Restart Cursor.

## Step 5: Test It! (30 seconds)

In Cursor, try asking:

> "Get the profit and loss report for this year"

> "Show me the current balance sheet"

> "What's our accounts receivable aging?"

That's it! 🎉

## Quick Commands

```bash
# Re-authenticate (tokens expire after 100 days)
python setup_oauth.py

# Test the server directly
python server.py

# Check if tokens are valid
cat token.json
```

## What You Can Ask

### Financial Reports
- "Get P&L for Q4 2024"
- "Show balance sheet as of December 31"
- "Get cash flow statement for last 6 months"
- "Show general ledger for January"
- "What's the AR aging report?"

### Data Queries
- "List all bank accounts"
- "Show me recent invoices"
- "Get company information"
- "Find expense accounts"

## Troubleshooting

**Error: Token file not found**
→ Run: `python setup_oauth.py`

**Error: Port 8000 in use**
→ Change port in `.env` to `8001` (update redirect URI in QuickBooks app too)

**Browser doesn't open**
→ Copy the URL from terminal and paste in browser

**Need help?**
→ Check the full README.md for detailed documentation

---

**Next Steps:**
- Read [README.md](./README.md) for complete documentation
- Explore all available reports and tools
- Set up automated reporting workflows

