# QuickBooks Online MCP Server

A Model Context Protocol (MCP) server for QuickBooks Online integration, focused on financial reporting and data queries.

## Features

### Financial Reports
- **Profit & Loss (P&L)** - Income statement with customizable date ranges and summarization
- **Balance Sheet** - Assets, liabilities, and equity at any point in time
- **Cash Flow Statement** - Operating, investing, and financing activities
- **General Ledger** - Detailed transaction-level accounting records
- **Accounts Receivable Aging** - Customer payment status and aging analysis
- **Accounts Payable Aging** - Vendor bill status and aging analysis

### Data Queries
- **Chart of Accounts** - Query and filter accounts by type and name
- **Transactions** - Query invoices, bills, payments, and other transactions
- **Company Info** - Retrieve company profile and settings

## Prerequisites

1. **QuickBooks Online Account** (any plan - Simple Start, Essentials, Plus, or Advanced)
2. **QuickBooks Developer Account** - Free at [developer.intuit.com](https://developer.intuit.com)
3. **Python 3.8+** installed on your system

## Quick Start

### 1. Create QuickBooks App

1. Go to [Intuit Developer Portal](https://developer.intuit.com/app/developer/myapps)
2. Click **"Create an app"**
3. Select **"QuickBooks Online and Payments"**
4. Fill in app details:
   - **App Name**: PetesBrain QuickBooks Integration (or your choice)
   - **Description**: MCP server for financial reporting
5. Under **Keys & OAuth**:
   - Note your **Client ID** and **Client Secret**
   - Add redirect URI: `http://localhost:8000/callback`
6. Under **Scopes**, enable:
   - ✅ Accounting (com.intuit.quickbooks.accounting)

### 2. Install Dependencies

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit .env and add your credentials
nano .env
```

Add your credentials:
```env
QUICKBOOKS_CLIENT_ID=your_client_id_here
QUICKBOOKS_CLIENT_SECRET=your_client_secret_here
QUICKBOOKS_REDIRECT_URI=http://localhost:8000/callback
QUICKBOOKS_ENVIRONMENT=production
```

### 4. Authenticate with QuickBooks

```bash
python setup_oauth.py
```

This will:
1. Start a local server on port 8000
2. Open your browser to QuickBooks authorization page
3. Ask you to select which QuickBooks company to connect
4. Receive and store OAuth tokens
5. Save tokens to `token.json` (auto-refreshing)

### 5. Add to Cursor MCP Configuration

Add this server to your Cursor settings (`~/Library/Application Support/Cursor/User/globalStorage/settings.json`):

```json
{
  "mcpServers": {
    "quickbooks-reporting": {
      "command": "python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/quickbooks-mcp-server/server.py"
      ],
      "env": {
        "QUICKBOOKS_CLIENT_ID": "your_client_id_here",
        "QUICKBOOKS_CLIENT_SECRET": "your_client_secret_here"
      }
    }
  }
}
```

### 6. Restart Cursor

Restart Cursor to load the new MCP server.

## Available Tools

Once connected, you can ask Claude to pull any of these reports:

### Financial Reports

**Profit & Loss**
```
Get the P&L report for this year
Get profit and loss for Q4 2024
Show me P&L by month for the last quarter
```

**Balance Sheet**
```
Get the current balance sheet
Show me the balance sheet as of December 31, 2024
What's our balance sheet today?
```

**Cash Flow**
```
Get the cash flow statement for this year
Show cash flow for the last 6 months
```

**General Ledger**
```
Get general ledger entries for this month
Show me all GL entries from January 1 to January 31
```

**AR/AP Aging**
```
Show accounts receivable aging
What's the current AP aging report?
Show me which customers owe us money
```

### Data Queries

**Chart of Accounts**
```
List all bank accounts
Show me all income accounts
Find accounts with "advertising" in the name
```

**Transactions**
```
Get all invoices from last month
Show me recent bills
List payments from Q4 2024
```

**Company Info**
```
Get company information
What's our QuickBooks company name?
```

## How It Works

### OAuth Token Management

- **Access tokens** are valid for 1 hour
- **Refresh tokens** are valid for 100 days
- The server **automatically refreshes** tokens when they expire
- You'll need to re-authenticate every ~100 days

### Report Parameters

All reports support:
- **Date ranges**: Flexible start/end dates (YYYY-MM-DD format)
- **Accounting method**: Accrual or Cash basis
- **Summarization**: Total, Month, Quarter, Year (for P&L)

### Rate Limits

QuickBooks API limits:
- **500 requests per minute** per company
- **5,000 requests per hour** per company
- The server handles rate limiting gracefully

## Troubleshooting

### "Token file not found" Error

**Solution**: Run `python setup_oauth.py` to authenticate

### "Invalid token" Error

**Solution**: Tokens expired. Run `python setup_oauth.py` again to re-authenticate

### "Realm ID not found" Error

**Solution**: Your token file is missing the company ID. Re-run OAuth setup

### "Permission denied" Error

**Solution**: Make sure your QuickBooks app has the Accounting scope enabled

### OAuth Callback Not Working

**Common Issues**:
1. Port 8000 is already in use - change the port in both `.env` and your app settings
2. Firewall blocking localhost - temporarily disable or allow Python
3. Wrong redirect URI - must match exactly in both places

## Security Best Practices

1. **Never commit** `.env` or `token.json` to version control (already in `.gitignore`)
2. **Rotate credentials** periodically in the Intuit Developer Portal
3. **Use environment variables** for production deployments
4. **Monitor API usage** in the Intuit Developer dashboard

## Development

### File Structure

```
quickbooks-mcp-server/
├── server.py              # Main MCP server with reporting tools
├── oauth/
│   ├── __init__.py
│   └── quickbooks_auth.py # OAuth token management
├── setup_oauth.py         # Interactive OAuth setup script
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (not in git)
├── token.json            # OAuth tokens (not in git)
└── README.md             # This file
```

### Adding New Reports

To add a new report type, add a tool to `server.py`:

```python
@mcp.tool()
def get_custom_report(
    start_date: str = None,
    end_date: str = None
) -> Dict[str, Any]:
    """
    Get custom report from QuickBooks.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dict containing report data
    """
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    
    result = make_api_request('reports/YourReportName', params=params)
    return {"success": True, "data": result}
```

## API Reference

### QuickBooks Online API Documentation

- [Main Docs](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [Reports API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/report)
- [OAuth 2.0 Guide](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0)

## Support

### Common Questions

**Q: Can I connect to multiple QuickBooks companies?**  
A: Not simultaneously with one token file. You'd need separate configurations per company.

**Q: Does this work with QuickBooks Desktop?**  
A: No, this is for QuickBooks Online only. Desktop uses a different API.

**Q: Can I create invoices or modify data?**  
A: Currently this is read-only for reporting. Write capabilities can be added if needed.

**Q: Is this free?**  
A: Yes! QuickBooks Online API is free to use. You just need a QBO subscription.

**Q: How often do reports update?**  
A: Reports reflect real-time data from QuickBooks Online.

## License

This MCP server follows the PetesBrain project license.

## Contributing

To contribute improvements:
1. Test your changes with a sandbox QuickBooks company
2. Document any new tools or features
3. Update this README with usage examples

## Changelog

### v1.0.0 (2025-11-06)
- Initial release
- Core financial reports (P&L, Balance Sheet, Cash Flow)
- Aging reports (AR/AP)
- General Ledger query
- Chart of Accounts and Transaction queries
- Auto-refreshing OAuth tokens
- Interactive setup script

