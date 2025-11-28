# QuickBooks MCP Server - Example Queries

Once your QuickBooks MCP server is set up in Cursor, you can ask these natural language questions. Claude will automatically use the appropriate tools to fetch the data.

## Financial Statements

### Profit & Loss (Income Statement)

```
Get the profit and loss report for this year
```
```
Show me P&L for Q4 2024
```
```
Get profit and loss from January 1 to March 31, 2024
```
```
Show me monthly P&L for the last 6 months
```
```
Compare this month's P&L to last month
```
```
Get the P&L using cash basis accounting
```

### Balance Sheet

```
Show me the current balance sheet
```
```
Get the balance sheet as of December 31, 2024
```
```
What's our balance sheet today?
```
```
Show me assets, liabilities, and equity as of last month
```

### Cash Flow

```
Get the cash flow statement for this year
```
```
Show cash flow for Q1 2024
```
```
Get cash flow from January to June 2024
```
```
How is our cash flow looking this quarter?
```

### General Ledger

```
Get general ledger entries for this month
```
```
Show me all GL entries from January 1 to January 31
```
```
Get the general ledger for last month
```
```
Show me recent general ledger activity
```

## Aging Reports

### Accounts Receivable

```
Show me the accounts receivable aging report
```
```
Which customers owe us money?
```
```
Get AR aging as of today
```
```
Show me overdue customer invoices
```
```
What's our current AR aging by customer?
```

### Accounts Payable

```
Show me accounts payable aging
```
```
Which bills do we need to pay soon?
```
```
Get AP aging report
```
```
Show me what we owe to vendors
```

## Chart of Accounts

### All Accounts

```
List all accounts in QuickBooks
```
```
Show me the chart of accounts
```
```
Get all accounts
```

### By Account Type

```
Show me all bank accounts
```
```
List all income accounts
```
```
Get all expense accounts
```
```
Show me asset accounts
```
```
List all liability accounts
```
```
Get equity accounts
```

### By Name

```
Find accounts with "advertising" in the name
```
```
Show me accounts related to payroll
```
```
Get the rent expense account
```

## Transactions

### Invoices

```
Get all invoices from last month
```
```
Show me recent invoices
```
```
List invoices from Q4 2024
```
```
Get invoices from January 1 to January 31
```

### Bills

```
Show me all bills from last month
```
```
Get recent bills
```
```
List bills from this quarter
```

### Payments

```
Get all payments from last month
```
```
Show me recent customer payments
```
```
List payments received in January
```

### Purchases

```
Show me all purchases from last month
```
```
Get recent purchase transactions
```

### Sales Receipts

```
Get sales receipts from last month
```
```
Show me recent sales receipts
```

## Company Information

```
Get company information
```
```
What's our QuickBooks company name?
```
```
Show me company details
```
```
What company are we connected to?
```

## Advanced Queries

### Comparative Analysis

```
Compare this year's revenue to last year
```
```
Show me year-over-year P&L comparison
```
```
How does this quarter compare to last quarter?
```
```
Compare monthly revenue for the last 6 months
```

### Specific Date Ranges

```
Get P&L for fiscal year 2024 (April 2024 to March 2025)
```
```
Show me financial data for the summer months (June-August)
```
```
Get Q3 2024 financial statements
```

### Multiple Reports

```
Get both P&L and Balance Sheet for this year
```
```
Show me P&L, Balance Sheet, and Cash Flow for Q4 2024
```
```
Get all major financial statements for this month
```

### Custom Analysis

```
What's our current cash position?
```
> (Queries balance sheet and highlights cash/bank accounts)

```
Are we profitable this year?
```
> (Gets P&L and analyzes net income)

```
How much do customers owe us vs. what we owe vendors?
```
> (Gets both AR and AP aging reports)

```
Show me our top expense categories this year
```
> (Gets P&L and ranks expenses)

## Report Parameters You Can Specify

### Date Formats
Always use **YYYY-MM-DD** format:
- `2024-01-01` (January 1, 2024)
- `2024-12-31` (December 31, 2024)

### Accounting Methods
- **Accrual basis** (default) - Revenue/expenses when earned/incurred
- **Cash basis** - Revenue/expenses when money changes hands

Example:
```
Get P&L using cash basis accounting
Get balance sheet using accrual method
```

### Time Summarization (P&L)
- **Total** - Single column total (default)
- **Month** - Break down by month
- **Quarter** - Break down by quarter
- **Year** - Break down by year

Example:
```
Get P&L by month for this year
Show me quarterly P&L for 2024
```

### Aging Periods
- Default: 4 periods of 30 days each (0-30, 31-60, 61-90, 90+)

Example:
```
Get AR aging with 5 periods of 30 days
```

## Combining with Other Data

Since you're in PetesBrain, you can combine QuickBooks data with other sources:

```
Compare QuickBooks revenue to Google Ads spend this month
```
> (Uses QuickBooks MCP + Google Ads MCP)

```
Show me profitability by client and compare to ad performance
```
> (Combines QuickBooks data with client performance data)

```
Get our actual expenses and compare to the budget
```
> (QuickBooks actual + budget tracking sheets)

## Tips for Better Queries

### Be Specific with Dates
❌ "Show me last month's P&L"  
✅ "Get P&L for October 2024" or "Get P&L from 2024-10-01 to 2024-10-31"

### Specify the Report Type
❌ "Show me financials"  
✅ "Get the P&L report" or "Show me the balance sheet"

### Use Natural Language
✅ All of these work:
- "Get the profit and loss report"
- "Show me P&L"
- "What's our income statement?"
- "How profitable are we?"

### Request Multiple Views
✅ "Show me P&L by month and compare to last year"
✅ "Get balance sheet and cash flow for Q4"

## Testing Your Setup

Try these simple queries first to verify everything works:

1. **Basic test:**
   ```
   Get company information
   ```

2. **Simple report:**
   ```
   Get the P&L for this year
   ```

3. **With parameters:**
   ```
   Get balance sheet as of December 31, 2024
   ```

4. **Data query:**
   ```
   List all bank accounts
   ```

If these work, you're all set! 🎉

## Troubleshooting Queries

**"I don't have access to that report"**
- Make sure your QuickBooks plan supports that report
- Verify OAuth scope includes "Accounting"

**"Invalid date format"**
- Use YYYY-MM-DD format (e.g., 2024-01-15)

**"No data returned"**
- Check if you have data in QuickBooks for that period
- Verify you're connected to the right company

**"Token expired"**
- Run: `python setup_oauth.py` to re-authenticate

---

## More Examples Needed?

If you want examples for a specific use case, just ask:
- "Show me how to query for [specific thing]"
- "How do I get [specific report]?"
- "Can you pull [specific data]?"

Claude will use the available tools to fetch what you need!

