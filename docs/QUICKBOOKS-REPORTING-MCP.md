# QuickBooks Reporting MCP Server

**Status:** ✅ Ready for Setup  
**Type:** MCP Server  
**Purpose:** Financial reporting and accounting data queries from QuickBooks Online  
**Created:** 2025-11-06  

## Overview

The QuickBooks Reporting MCP Server provides direct access to QuickBooks Online financial reports and accounting data through Claude in Cursor. This enables natural language queries for financial reporting, eliminating the need to log into QuickBooks for basic reporting needs.

## What This Enables

### Financial Reports (Read-Only)
- **Profit & Loss (P&L)** - Income statements with flexible date ranges
- **Balance Sheet** - Assets, liabilities, and equity snapshots
- **Cash Flow Statement** - Operating, investing, and financing activities
- **General Ledger** - Detailed transaction-level records
- **AR/AP Aging** - Customer and vendor payment analysis

### Data Queries
- **Chart of Accounts** - Account listings and filtering
- **Transactions** - Query invoices, bills, payments, etc.
- **Company Info** - Basic company profile data

### Example Use Cases
- "Show me P&L for Q4 2024 broken down by month"
- "What's our current cash position?"
- "Which customers have overdue invoices?"
- "Get all expense transactions from last month"
- "Compare this year's revenue to last year"

## Architecture

```
Claude (in Cursor)
    ↓
QuickBooks MCP Server (Python/FastMCP)
    ↓
QuickBooks Online API (OAuth 2.0)
    ↓
Your QuickBooks Data
```

### Components

1. **server.py** - Main FastMCP server with 10+ reporting tools
2. **oauth/quickbooks_auth.py** - Auto-refreshing OAuth token management
3. **setup_oauth.py** - Interactive authentication setup
4. **test_connection.py** - Connection verification utility

### Token Management

- **Access tokens:** Valid for 1 hour, auto-refresh
- **Refresh tokens:** Valid for 100 days
- **Storage:** Local `token.json` file (gitignored)
- **Security:** Never committed to version control

## Setup Requirements

### Prerequisites
1. QuickBooks Online subscription (any plan)
2. QuickBooks Developer account (free)
3. Python 3.8+
4. Cursor with MCP support

### Time to Setup
- **First time:** ~10 minutes
- **Re-authentication:** ~2 minutes (every ~100 days)

## Quick Setup Guide

### 1. Create QuickBooks Developer App

```
https://developer.intuit.com/app/developer/myapps
→ Create an app
→ QuickBooks Online and Payments
→ Keys & OAuth → Note credentials
→ Add redirect URI: http://localhost:8000/callback
→ Scopes → Enable "Accounting"
```

### 2. Configure Server

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server

# Install
pip install -r requirements.txt

# Configure
cp env.example .env
nano .env  # Add your Client ID and Secret
```

### 3. Authenticate

```bash
python setup_oauth.py
# Browser opens → Login → Select company → Authorize
```

### 4. Test Connection

```bash
python test_connection.py
# Should show all green checkmarks ✓
```

### 5. Add to Cursor

Edit: `~/Library/Application Support/Cursor/User/globalStorage/settings.json`

```json
{
  "mcpServers": {
    "quickbooks-reporting": {
      "command": "python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/server.py"
      ],
      "env": {
        "QUICKBOOKS_CLIENT_ID": "your_client_id",
        "QUICKBOOKS_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

Restart Cursor → Ready to use!

## Available Tools

The server provides these MCP tools that Claude can call:

### Financial Reports

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_profit_and_loss` | P&L statement | start_date, end_date, summarize_by |
| `get_balance_sheet` | Balance sheet | report_date, accounting_method |
| `get_cash_flow` | Cash flow statement | start_date, end_date |
| `get_general_ledger` | GL entries | start_date, end_date |
| `get_accounts_receivable_aging` | AR aging | report_date, num_periods |
| `get_accounts_payable_aging` | AP aging | report_date, num_periods |

### Data Queries

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `query_accounts` | Chart of accounts | account_type, account_name |
| `query_transactions` | Transaction search | transaction_type, date_range |
| `get_company_info` | Company details | (none) |

## Usage Examples

### Natural Language Queries

Once set up, you can ask Claude (in Cursor):

```
Financial Overview:
- "Get the P&L for this year"
- "Show me the balance sheet as of today"
- "What's our cash flow statement for Q4?"

Time Comparisons:
- "Compare this month's revenue to last month"
- "Show me year-over-year P&L"
- "Get monthly P&L for the last 6 months"

Specific Analysis:
- "Which customers owe us money?" (AR aging)
- "What bills do we need to pay soon?" (AP aging)
- "Show me all expense accounts"
- "Get recent invoices"

Deep Dives:
- "Show me general ledger entries for January"
- "Find all transactions in the Advertising account"
- "What's our current accounts payable balance?"
```

### Date Formats

All dates use **YYYY-MM-DD** format:
- `2024-01-01` (January 1, 2024)
- `2024-12-31` (December 31, 2024)

### Accounting Methods

- **Accrual** - Revenue/expenses when earned/incurred (default)
- **Cash** - Revenue/expenses when money changes hands

## Integration with PetesBrain

### Synergy with Existing Systems

**Budget Monitoring**
- Combine with `/agents/budget-tracking/` scripts
- Compare actual (QuickBooks) vs. planned (Google Sheets) spend
- Automate variance reporting

**Client Reporting**
- Pull QuickBooks data for client profitability analysis
- Include in weekly client performance reports
- Track campaign spend vs. actual costs

**Performance Monitoring**
- Feed financial data into performance dashboards
- Alert on unusual expenses or revenue changes
- Integrate with `/agents/performance-monitoring/`

### Potential Workflows

1. **Daily Financial Snapshot**
   - Pull current cash position
   - Check AR aging
   - Alert on overdue invoices
   - Combine with daily briefing system

2. **Monthly Close Automation**
   - Generate P&L, Balance Sheet, Cash Flow
   - Compare to previous months
   - Export to Google Sheets for analysis
   - Auto-generate financial commentary

3. **Client Profitability**
   - Query project/client-specific transactions
   - Calculate client ROI
   - Include in client performance reports

## Security & Best Practices

### Security
- ✅ Tokens stored locally, never in git
- ✅ OAuth 2.0 with auto-refresh
- ✅ Read-only access (no data modification)
- ✅ Client ID/Secret in environment variables
- ✅ All files with secrets in `.gitignore`

### API Limits
- **500 requests/minute** per company
- **5,000 requests/hour** per company
- Server handles rate limiting gracefully

### Maintenance
- **Re-authenticate every ~100 days** (refresh token expiry)
- **Monitor API usage** in Intuit Developer dashboard
- **Rotate credentials** periodically for security

## Troubleshooting

### Common Issues

**"Token file not found"**
```bash
# Solution:
python setup_oauth.py
```

**"Invalid token" or "Token expired"**
```bash
# Solution:
python setup_oauth.py  # Re-authenticate
```

**"Permission denied"**
- Check that "Accounting" scope is enabled in QuickBooks app
- Verify you selected the correct company during OAuth

**Port 8000 already in use**
- Change port in `.env`: `QUICKBOOKS_REDIRECT_URI=http://localhost:8001/callback`
- Update redirect URI in QuickBooks Developer Portal to match

### Verification Steps

1. Check environment variables: `cat .env`
2. Check token exists: `ls -la token.json`
3. Test connection: `python test_connection.py`
4. Check Cursor logs: Look for MCP server startup errors

## Files & Locations

```
/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/
├── server.py                    # Main MCP server
├── oauth/
│   ├── __init__.py
│   └── quickbooks_auth.py      # OAuth token management
├── setup_oauth.py              # Authentication setup
├── test_connection.py          # Connection verification
├── requirements.txt            # Python dependencies
├── .env                        # Your credentials (not in git)
├── token.json                  # OAuth tokens (not in git)
├── .gitignore                  # Security rules
├── README.md                   # Full documentation
├── QUICKSTART.md              # 5-minute setup guide
└── SETUP-CHECKLIST.md         # Setup verification
```

## Limitations

### Current Scope
- ✅ All standard financial reports
- ✅ Chart of accounts queries
- ✅ Transaction queries
- ❌ Data modification (invoices, bills, etc.)
- ❌ Multi-company (one token = one company)
- ❌ QuickBooks Desktop (Online only)

### Can Be Added
- Write operations (create invoices, bills, etc.)
- Custom report definitions
- Advanced filtering and sorting
- Batch operations
- Multi-company support
- Automated scheduled reporting

## Next Steps

### Immediate
1. Follow [QUICKSTART.md](../shared/mcp-servers/quickbooks-mcp-server/QUICKSTART.md)
2. Authenticate with QuickBooks
3. Test basic queries
4. Add to Cursor configuration

### Future Enhancements
- Integrate with budget tracking agents
- Create automated monthly financial reports
- Build client profitability dashboard
- Add financial KPI monitoring
- Create expense anomaly detection
- Build cash flow forecasting

## Resources

### Documentation
- **Full Setup:** `/shared/mcp-servers/quickbooks-mcp-server/README.md`
- **Quick Start:** `/shared/mcp-servers/quickbooks-mcp-server/QUICKSTART.md`
- **Setup Checklist:** `/shared/mcp-servers/quickbooks-mcp-server/SETUP-CHECKLIST.md`

### External Links
- [QuickBooks Developer Portal](https://developer.intuit.com)
- [QuickBooks API Docs](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [OAuth 2.0 Guide](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0)

### Support
- Test connection: `python test_connection.py`
- Check API status: [Intuit Status Page](https://status.developer.intuit.com)
- Review logs: Check Cursor developer console

## Status & Next Actions

**Current Status:** ✅ **Complete & Ready for Setup**

**Completed:**
- [x] MCP server implementation
- [x] OAuth authentication flow
- [x] All major financial reports
- [x] Transaction queries
- [x] Auto-refreshing tokens
- [x] Setup scripts and testing
- [x] Comprehensive documentation

**To Do (User):**
1. [ ] Create QuickBooks Developer app
2. [ ] Configure `.env` with credentials
3. [ ] Run `setup_oauth.py` to authenticate
4. [ ] Add to Cursor MCP configuration
5. [ ] Test with sample queries

**Estimated Setup Time:** 10 minutes

---

**Created:** 2025-11-06  
**Last Updated:** 2025-11-06  
**Version:** 1.0.0  
**Maintainer:** PetesBrain System  
**Category:** Integrations / MCP Servers / Financial Tools

