# ROK Experiments - CSV Export System

**Last Updated**: October 30, 2025

This directory contains automated CSV exports from the "ROK | Experiments" Google Sheet.

## Purpose: Client Analysis Context 🎯

**This is a KEY reference for understanding client account performance changes.**

### How Multiple Sources Work Together

**Complete Analysis** = Product Performance + Experiments + Tasks + Change History + Platform Updates + External Factors

| Priority | Data Source | What It Tells You | Example | Timing | Access |
|----------|-------------|-------------------|---------|--------|--------|
| **#1** | **Product Performance** | Which products drove the change | "SKU 287 revenue dropped £680/week" | Immediate | Via MCP GAQL queries |
| **#2** | **Experiment Notes** | Strategic intent: what/why/expected | "Started BMPM search campaign, expect +£200/week" | Immediate | This CSV file |
| **#3** | **Completed Tasks** | Implementation details: how/when/status | "Created 3 ad groups, added 15 keywords, Oct 21" | Immediate | tasks-completed.md |
| **#4** | **Google Ads Change History** | What ACTUALLY changed in account | "3 ad groups paused Oct 19, 3:42 PM" | Immediate | Via MCP or Google Ads UI |
| **#5** | **Knowledge Base** | Google platform updates, algorithm changes | "Smart Bidding update rolled out Oct 1" | **2-4 weeks delayed** | knowledge-base/ |
| **#6** | **External Factors** | Client business changes, market conditions | "Stock shortages, seasonal demand" | Varies | Emails, meetings, CONTEXT.md |
| - | **Together** | Most complete picture possible | Product + intent + execution + platform + market | - | - |

**CRITICAL for e-commerce**: Product-level performance is #1 priority. Account-level metrics hide the story. Always check which products drove the change BEFORE looking at account changes.

**Why product-level matters**:
- Account shows: "Revenue -10%" (scary, unclear)
- Product level reveals: "Top product (20% of revenue) went out of stock" (clear, actionable)
- Without product data, you might waste time looking for account changes that don't exist

**How to access product performance**:
```python
# Via MCP Google Ads API (GAQL query)
mcp__google-ads__run_gaql(
    customer_id="4941701449",
    query="""
        SELECT
            segments.product_item_id,
            segments.product_title,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.conversions_value DESC
    """
)
```

**Important**: Even with all these sources, **not all performance factors are measurable or logged**. This framework provides the most complete picture available, but acknowledge unknown variables exist.

### When Analyzing Client Performance

**Always cross-reference ALL sources**:
- **Why did performance spike/drop?** → Check experiment notes for strategic changes on that date
- **What ACTUALLY changed in the account?** → Check Google Ads change history to verify
- **How was it implemented?** → Check completed tasks for tactical details
- **Was there a Google update?** → Check Knowledge Base for platform changes 2-4 weeks prior (delayed impact)
- **What was expected?** → Read experiment note's prediction
- **What was the status?** → Check task notes for caveats (e.g., "awaiting client approval")
- **Did it work?** → Compare actual results to expectations
- **What changed recently?** → Review last 30 days: experiments, tasks, change history, AND platform updates
- **Are there unmeasured factors?** → Acknowledge what might NOT be captured (see "Other Factors" below)

**Example Analysis**:
> "Revenue improved 20% starting Oct 15. Checking all sources:
> - Experiments: No strategic changes that week ✗
> - Tasks: No implementation work Oct 10-20 ✗
> - Knowledge Base: Smart Bidding update rolled out Oct 1 ✓
> - Conclusion: Improvement likely due to Google platform update (2-week learning period aligns)"

**Use Cases**:
- 📊 **Weekly Analysis** - Reference recent experiments to explain performance changes
- 📈 **Monthly Reports** - Summarize which experiments succeeded/failed
- 🔍 **Spike Investigation** - "Revenue jumped 40% on Oct 21" → Check experiments from that date
- 📅 **Annual Reviews** - Track long-term impact of strategic changes
- 💡 **Client Communication** - Explain results with context ("As we discussed when we started X...")

**ALWAYS check this sheet when analyzing client performance!**

### Other Factors That May Affect Performance

Even with all documented sources, many factors can impact Google Ads performance that are **difficult or impossible to measure**:

**🏪 Client Website & Business**:
- Website speed/performance changes
- Checkout flow modifications
- Payment gateway issues
- Product availability/stock levels
- Shipping cost changes
- Returns/refund policy updates
- Customer service quality
- Brand reputation events

**📱 Technical & Tracking**:
- Conversion tracking accuracy
- Tag manager changes
- Cross-domain tracking issues
- Cookie consent implementation
- iOS privacy changes (ATT)
- Browser updates (third-party cookie blocking)
- Server-side tracking drift

**🌍 Market & External**:
- Competitor activity (pricing, promotions, new entrants)
- Seasonal demand fluctuations
- Economic conditions (inflation, consumer confidence)
- Weather events
- Industry trends
- Media coverage/PR events
- Social media virality

**🎯 Google Ads Ecosystem**:
- Quality Score changes (not always visible)
- Ad Rank competition shifts
- Auction dynamics (more/fewer competitors)
- Geographic performance shifts
- Device/browser performance changes
- Ad format updates (Google Surfaces, Discover, etc.)
- Automated recommendations applied
- Policy enforcement changes

**👥 Audience Behavior**:
- Search behavior shifts
- Customer lifetime value changes
- New vs returning customer mix
- Geographic mix shifts
- Time of day patterns
- Intent quality changes

**🔄 Cross-Channel Effects**:
- Other marketing channels (email, social, SEO)
- Brand awareness campaigns
- Offline advertising
- PR and media coverage
- Influencer marketing
- Affiliate programs

**When performance changes and none of the documented sources explain it**:
- State what you checked: "Checked experiments, tasks, change history, and platform updates - no changes found that explain this performance shift."
- **Do NOT speculate** about unmeasured factors unless you have evidence
- Instead: "Unable to determine cause from available data. Recommend monitoring to see if pattern continues."
- If you DO have evidence (from emails, client communication, etc.), cite it specifically: "Per Oct 12 email, client launched Instagram campaign which may have increased brand awareness."
- Monitor for patterns: If it persists, investigate further
- Suggest next steps: "Recommend checking with client for any undocumented business changes, website updates, or external campaigns."

## Workflow (Hybrid Approach)

**NEW ENTRIES** → Written directly to Google Sheets via MCP API
**CSV FILES** → Backup + local search (exported every 6 hours)

### Writing New Entries ✍️

New experiment notes are written **directly to Google Sheets** using the MCP API:
```python
# Claude Code writes directly to Google Sheets (immediate)
mcp__google-sheets__write_cells(...)
```

**Benefits**: Immediate availability, no sync delay, single source of truth.

### Reading Data 📖

**Option 1: CSV Files** (Fast, offline, local search)
- Good for: Grep, scripts, bulk analysis, offline work
- Freshness: Up to 6 hours old

**Option 2: Google Sheets API** (Live, always current)
- Good for: Real-time data, recent entries (< 6 hours)
- Freshness: Always current

**IMPORTANT**: CSV files are **READ-ONLY**. Changes will be overwritten on next export.

## Files

- **`rok-experiments-client-notes.csv`** - Client notes log with timestamps, client names, experiment notes, and tags
- **`rok-experiments-client-list.csv`** - Simple list of all ROK clients
- **`google-sheets-export.log`** - Export activity log
- **`google-sheets-export-error.log`** - Error log (if any errors occur)

## Update Schedule

The CSV files are **automatically updated every 6 hours** (4 times per day).

Export times: **12:00 AM, 6:00 AM, 12:00 PM, 6:00 PM** (approximately)

## How It Works

A macOS `launchd` job runs the export script automatically:

- **Script**: `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`
- **LaunchAgent**: `~/Library/LaunchAgents/com.roksys.google-sheets-export.plist`
- **Source Sheet**: [ROK | Experiments](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)

## Manual Commands

### Run Export Manually
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server
GOOGLE_APPLICATION_CREDENTIALS=credentials.json .venv/bin/python export_experiments_sheet.py
```

### Check Scheduled Job Status
```bash
launchctl list | grep com.roksys.google-sheets-export
```

### View Recent Export Logs
```bash
tail -20 /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/google-sheets-export.log
```

### Stop Scheduled Exports
```bash
launchctl unload ~/Library/LaunchAgents/com.roksys.google-sheets-export.plist
```

### Restart Scheduled Exports
```bash
launchctl load ~/Library/LaunchAgents/com.roksys.google-sheets-export.plist
```

### Change Export Frequency

Edit `~/Library/LaunchAgents/com.roksys.google-sheets-export.plist` and modify the `StartInterval` value:
- Every hour: `3600`
- Every 6 hours: `21600` (current)
- Every 12 hours: `43200`
- Daily: `86400`

After editing, reload the job:
```bash
launchctl unload ~/Library/LaunchAgents/com.roksys.google-sheets-export.plist
launchctl load ~/Library/LaunchAgents/com.roksys.google-sheets-export.plist
```

## Usage in Client Analysis

These CSV files are now available for Claude Code to read when analyzing client Google Ads performance. The experiment notes provide context about recent campaign changes, budget adjustments, and optimization tests across all ROK clients.

### Example Usage
```bash
# Read client notes
cat rok-experiments-client-notes.csv

# Find notes for specific client
grep "Tree2mydoor" rok-experiments-client-notes.csv

# Count experiments by client
tail -n +2 rok-experiments-client-notes.csv | cut -d',' -f2 | sort | uniq -c
```

## Troubleshooting

### Check if exports are running
```bash
ls -lht /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/
```
Files should be updated every 6 hours.

### View error log
```bash
cat /Users/administrator/Documents/PetesBrain/roksys/spreadsheets/google-sheets-export-error.log
```

### Test Google Sheets credentials
```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server
test -f credentials.json && echo "Credentials exist" || echo "Credentials missing"
```

## Data Freshness

**CSV files**: Up to 6 hours old (exports run at 12 AM, 6 AM, 12 PM, 6 PM)
**Google Sheets**: Always current (live)

**Example**:
- 2:00 PM: New entry added via API → Available in Google Sheets immediately
- 2:00 PM: CSV still shows data from 12:00 PM export
- 6:00 PM: Export runs → CSV now includes 2:00 PM entry

## Why Keep CSV Export?

1. ✅ **Local backup** - Recover if Google Sheet deleted
2. ✅ **Fast search** - Grep without API calls
3. ✅ **Offline access** - Work without internet
4. ✅ **Version control** - Track changes via git
5. ✅ **Bulk processing** - Scripts can read locally

---

**Last Updated**: October 30, 2025
**Maintained By**: ROK Systems / Pete's Brain
