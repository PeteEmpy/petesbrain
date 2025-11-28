# QuickBooks MCP Server - Features Overview

## 🎯 What You Get

A direct connection from Claude (in Cursor) to your QuickBooks Online data, enabling natural language financial reporting.

## 📊 Available Reports

### Core Financial Statements

| Report | Description | Key Use Cases |
|--------|-------------|---------------|
| **Profit & Loss** | Revenue and expenses | Monthly performance, YoY comparison, budget variance |
| **Balance Sheet** | Assets, liabilities, equity | Financial position, liquidity analysis, net worth |
| **Cash Flow** | Money in/out by category | Cash management, forecasting, working capital |
| **General Ledger** | Transaction-level details | Audit trails, account reconciliation, deep dives |

### Management Reports

| Report | Description | Key Use Cases |
|--------|-------------|---------------|
| **AR Aging** | Customer payment status | Collections priority, cash flow forecasting, credit decisions |
| **AP Aging** | Vendor bill status | Payment scheduling, cash planning, vendor relationships |

## 🔍 Data Query Capabilities

### Chart of Accounts
- Filter by account type (Bank, Income, Expense, Asset, Liability, Equity)
- Search by account name
- Get account balances and details

### Transactions
- Query by type (Invoice, Bill, Payment, Purchase, Sales Receipt, etc.)
- Filter by date range
- Get transaction details

### Company Information
- Company name and legal name
- Contact information
- Company ID and settings

## 💬 Natural Language Interface

Just ask in plain English:

```
✅ "Get the P&L for this year"
✅ "Which customers owe us money?"
✅ "Show me the balance sheet"
✅ "List all expense accounts"
✅ "Compare this quarter to last quarter"
```

No need to remember API endpoints, SQL queries, or report parameters!

## 🛠️ Technical Features

### OAuth 2.0 Authentication
- ✅ Secure token management
- ✅ Auto-refreshing access tokens
- ✅ 100-day refresh token validity
- ✅ Local token storage (never in git)

### Report Customization
- ✅ Flexible date ranges (any start/end date)
- ✅ Accounting method (Accrual or Cash basis)
- ✅ Summarization options (Total, Month, Quarter, Year)
- ✅ Custom aging periods for AR/AP

### Developer Experience
- ✅ FastMCP framework (modern Python MCP server)
- ✅ Interactive OAuth setup script
- ✅ Connection testing utility
- ✅ Comprehensive error handling
- ✅ Automatic rate limit handling

### Documentation
- ✅ Complete setup guide (README.md)
- ✅ Quick start (5 minutes to first query)
- ✅ Setup checklist (verify everything works)
- ✅ Example queries (50+ natural language examples)
- ✅ Troubleshooting guide

## 📈 Report Parameters

### Date Ranges
```python
# Specific dates
start_date: "2024-01-01"
end_date: "2024-12-31"

# Relative dates (you say it naturally)
"this year"      → 2024-01-01 to today
"last month"     → Previous month's start/end
"Q4 2024"        → 2024-10-01 to 2024-12-31
"this quarter"   → Current quarter's dates
```

### Accounting Methods
```python
accounting_method: "Accrual"  # Revenue/expense when earned/incurred (default)
accounting_method: "Cash"     # Revenue/expense when money changes hands
```

### Summarization (P&L)
```python
summarize_column_by: "Total"    # Single total column (default)
summarize_column_by: "Month"    # Break down by month
summarize_column_by: "Quarter"  # Break down by quarter  
summarize_column_by: "Year"     # Break down by year
```

### Aging Periods (AR/AP)
```python
num_periods: 4           # Number of aging buckets (default: 4)
aging_period: 30         # Days per bucket (default: 30)
aging_method: "Current"  # Age from current date (default)
```

## 🔐 Security Features

- **OAuth 2.0** - Industry standard authentication
- **Local tokens** - Stored on your machine only
- **Read-only** - Cannot modify QuickBooks data
- **Environment variables** - Secrets never in code
- **Gitignore rules** - Credentials never committed
- **Token refresh** - Automatic, no re-auth needed for 100 days

## 📊 API Limits

QuickBooks Online API:
- **500 requests/minute** per company
- **5,000 requests/hour** per company

The server handles these limits automatically.

## 🎨 Report Output Format

All reports return structured JSON data that Claude can:
- Summarize in natural language
- Format as tables
- Compare across periods
- Combine with other data sources
- Export to other formats

Example P&L structure:
```json
{
  "success": true,
  "report_name": "Profit & Loss",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "accounting_method": "Accrual",
  "data": {
    "Header": {
      "ReportName": "ProfitAndLoss",
      "StartPeriod": "2024-01-01",
      "EndPeriod": "2024-12-31"
    },
    "Rows": [
      {
        "Header": { "ColData": [{"value": "Income"}] },
        "Rows": [...]
      },
      {
        "Header": { "ColData": [{"value": "Expenses"}] },
        "Rows": [...]
      }
    ]
  }
}
```

## 🚀 Performance

- **Fast**: Direct API calls, no intermediary services
- **Efficient**: Only fetches requested data
- **Cached**: Claude can reference previous queries in conversation
- **Reliable**: Auto-retry on transient errors

## 🔄 Integration with PetesBrain

### Potential Workflows

**Daily Financial Check-In**
```
Morning briefing includes:
- Current cash position
- Outstanding AR
- Recent transactions
- Budget variance
```

**Monthly Close Automation**
```
Automated monthly:
- Generate all financial statements
- Compare to previous periods
- Export to Google Sheets
- Flag anomalies
```

**Client Profitability**
```
Per-client analysis:
- Revenue by client (from QuickBooks)
- Ad spend by client (from Google Ads MCP)
- Calculate ROI
- Include in client reports
```

**Budget Monitoring**
```
Compare:
- Planned budget (Google Sheets)
- Actual spend (QuickBooks)
- Ad platform spend (Google/Meta Ads)
- Alert on variances
```

## 🎯 Use Cases by Role

### For Business Owners
- Quick financial snapshots without logging into QuickBooks
- Month-over-month and year-over-year comparisons
- Cash flow monitoring
- Customer payment tracking

### For Accountants
- Fast access to any report for client questions
- General ledger queries for reconciliation
- Transaction lookups without QuickBooks interface
- Period-end reporting automation

### For Analysts
- Extract data for deeper analysis in other tools
- Combine QuickBooks data with other data sources
- Create custom reports and dashboards
- Automate recurring analysis

### For Operations
- Monitor AR aging for collections
- Track AP aging for payment planning
- Verify transaction details
- Check account balances

## 📋 Supported QuickBooks Plans

Works with all QuickBooks Online plans:
- ✅ Simple Start
- ✅ Essentials
- ✅ Plus
- ✅ Advanced

Note: Some advanced reports may require higher-tier plans.

## ❌ Current Limitations

### Not Included (But Could Be Added)
- ❌ Creating/editing transactions (invoices, bills, etc.)
- ❌ Modifying chart of accounts
- ❌ Custom report definitions
- ❌ Attachments and files
- ❌ Multi-company support (one token = one company)

### Not Supported
- ❌ QuickBooks Desktop (different API)
- ❌ Historical data before your subscription start
- ❌ Deleted/voided transactions (unless specifically queried)

## 🆚 Comparison to Alternatives

| Feature | QuickBooks MCP | QuickBooks Web | Export to Excel |
|---------|----------------|----------------|-----------------|
| Natural language queries | ✅ | ❌ | ❌ |
| No login required | ✅ | ❌ | ❌ |
| Custom date ranges | ✅ | ✅ | Manual |
| Combine with other data | ✅ | ❌ | Manual |
| Automation ready | ✅ | ❌ | Partial |
| Real-time data | ✅ | ✅ | ❌ |
| Cost | Free (API) | Subscription | Subscription |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete documentation and reference |
| `QUICKSTART.md` | 5-minute setup guide |
| `SETUP-CHECKLIST.md` | Step-by-step verification |
| `EXAMPLE-QUERIES.md` | 50+ natural language examples |
| `FEATURES-OVERVIEW.md` | This file - visual feature summary |

## 🎓 Learning Curve

```
Setup Time:      █████░░░░░  10 minutes
First Query:     ██░░░░░░░░  30 seconds
Mastery:         ███░░░░░░░  1 hour of experimentation
```

**Why so easy?**
- Natural language interface (no syntax to learn)
- Comprehensive examples provided
- Interactive setup script
- Built-in testing tools
- Detailed error messages

## ✨ What Makes This Special

1. **Natural Language** - Ask questions like you would a colleague
2. **No Context Switching** - Stay in Cursor, no need to open QuickBooks
3. **Real-Time** - Always current data, no exports or imports
4. **Secure** - OAuth 2.0, read-only, local tokens
5. **Extendable** - Combine with other MCP servers and data sources
6. **Documented** - Extensive guides and examples
7. **Tested** - Built-in connection testing
8. **Automated** - Auto-refreshing tokens, error handling

## 🚦 Status

**Current State:** ✅ **Ready for Production Use**

- [x] Core implementation complete
- [x] All major reports implemented
- [x] OAuth flow working
- [x] Documentation complete
- [x] Testing tools provided
- [x] Integration guide written
- [ ] Your setup (10 minutes)
- [ ] Your first query (30 seconds)

## 🎉 Ready to Get Started?

1. **Quick Setup:** Read `QUICKSTART.md` (5 minutes)
2. **Full Details:** Read `README.md` (detailed reference)
3. **Verify Setup:** Use `SETUP-CHECKLIST.md` (step-by-step)
4. **Try Queries:** See `EXAMPLE-QUERIES.md` (50+ examples)

---

**Questions?** Check the README.md or just ask Claude in Cursor after setup!

