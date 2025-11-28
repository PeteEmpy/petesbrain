# Quick Start Guide

## Initial Setup (One-Time, 2 minutes)

### Step 1: Set Up Tuesday Reminder

Run this command once:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_reminder.sh
```

It will ask for your email address and set up automatic Tuesday reminders.

### Step 2: Update Your Email in Config (Optional)

Edit `config.json` and set your email for alerts:

```json
"alert_settings": {
  "email_to": "your-email@example.com"
}
```

That's it! Setup complete.

## Weekly Usage (Every Tuesday)

### When You Get the Reminder Email

1. **Open Claude Code** (you're probably already here!)

2. **Say this exactly**:
   ```
   Run the product impact analysis
   ```

3. **Wait 2-5 minutes** while Claude:
   - Fetches product changes from your Google Sheet
   - Pulls Google Ads performance data
   - Analyzes impact
   - Generates reports

4. **Review the summary** Claude shows you

5. **Check the detailed report** in your Google Sheet:
   - Open: [Your Product Feed Monitor Sheet](https://docs.google.com/spreadsheets/d/1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q/)
   - Go to tab: **"Impact Analysis"**
   - Export for client reports as needed

## What to Look For

### 📉 Strong Negative Impacts
- Revenue drop >£100
- **Action needed**: Investigate cause, consider reverting changes

### 🟠 Negative Impacts
- Revenue drop £0-100
- **Monitor**: Watch for trends, may need attention

### 🟢 Positive Impacts
- Revenue increase
- **Learn from it**: Apply successful changes to similar products

### ⚪ Minimal/No Impact
- No significant performance change
- **Note**: Track for future reference

## Common Scenarios

### Scenario 1: Price Change Impact

```
📉 Product 287: Olive Tree Gift
   Revenue: £-180 (-35%)

What to do:
1. Check price history in Merchant Center
2. Compare to competitor pricing
3. Consider: Revert price OR add value (free shipping)
4. Document in client notes
```

### Scenario 2: Title Optimization Success

```
📈 Product 281: Mini Olive Tree Gift
   Revenue: £+245 (+42%)

What to do:
1. Review what changed in the title
2. Apply same format to similar products
3. Document best practices
4. Share success with client
```

### Scenario 3: Out of Stock / Feed Issues

```
⚪ Multiple products showing REMOVED then NEW

What to do:
1. Check for Shopify feed sync issues
2. Review with client's tech team
3. Monitor for recurring pattern
4. Document in client notes
```

## Pro Tips

### For Client Reports

The "Impact Analysis" sheet tab is export-ready:
- Copy relevant rows
- Paste into client report
- Add your analysis/recommendations

### For Quick Checks

Ask Claude follow-up questions:
- "Which client had the most negative impacts?"
- "Show me all Tree2mydoor changes"
- "What were the biggest revenue changes?"

### For Investigations

Drill deeper on specific products:
- "Pull detailed metrics for product 287"
- "Compare this to last month"
- "Check if this is a seasonal pattern"

## Troubleshooting

### "No data to analyze"
- Check that product changes exist in Outliers Report
- Verify changes are recent (within comparison window)

### "Can't find Google Ads data"
- Verify client is enabled in config.json
- Check Google Ads customer ID is correct

### "Reminder email not arriving"
- Check spam folder
- Run test: `./send_reminder.sh`
- Verify launchd job: `launchctl list | grep product-impact`

## Questions?

Just ask Claude:
- "How do I use the impact analyzer?"
- "What does this metric mean?"
- "Can you explain this result?"

---

**Next Steps After First Run**:
1. Review the output
2. Share insights with clients
3. Come back next Tuesday!
