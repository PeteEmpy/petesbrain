# Product Impact Analyzer

Analyzes product feed changes and correlates them with Google Ads Shopping performance to identify what changes helped or hurt performance.

## Quick Start

### 🤖 Phase 2 - Fully Automated (Recommended)

**One-command setup** for weekly automated analysis:

```bash
cd tools/product-impact-analyzer
./setup_automation.sh
```

This sets up:
- ✅ Weekly automated runs (Tuesday 9 AM)
- ✅ HTML email reports
- ✅ Trend analysis and anomaly detection
- ✅ Historical tracking

**See [PHASE2.md](PHASE2.md) for complete Phase 2 documentation.**

### 🧑‍💻 Phase 1 - Claude-Assisted (Still Available)

Just ask Claude Code:

```
Run the product impact analysis
```

That's it! Claude will:
1. Fetch product changes from your Google Sheet
2. Pull Google Ads performance data for all clients
3. Run the analysis
4. Show you a summary and write detailed results to the "Impact Analysis" sheet

### What You'll Get

**Text Summary** (shown immediately):
- Top 10 most impactful changes per client
- Revenue impact (£ and %)
- Click changes
- Impact flags (📈 strong positive, 🟢 positive, 🟠 negative, 📉 strong negative)

**Detailed Report** (written to Sheets):
- Every product change tracked
- Before/after metrics (clicks, conversions, revenue, cost)
- Statistical comparisons
- Export-ready format for client reports

### Tuesday Reminder

You'll get an email every Tuesday morning reminding you to run the analysis. The email contains:
- Simple instruction: "Ask Claude: Run the product impact analysis"
- Link to this documentation
- Last run date (if available)

## Configuration

Edit `config.json` to customize:

### Analysis Settings

```json
"analysis_settings": {
  "comparison_window_days": 7,        // Compare 7 days before vs 7 days after
  "min_clicks_threshold": 10,         // Ignore products with <10 clicks
  "significance_threshold_percent": 20 // Flag changes >20%
}
```

### Client Settings

```json
"clients": [
  {
    "name": "Tree2mydoor",
    "merchant_id": "107469209",
    "google_ads_customer_id": "4941701449",
    "enabled": true    // Set to false to exclude from analysis
  }
]
```

### Alert Settings

```json
"alert_settings": {
  "email_enabled": true,
  "email_to": "your-email@example.com",
  "alert_on_negative_impact": true,
  "alert_threshold_revenue_loss": 100  // Alert if any product loses >£100
}
```

## Understanding the Output

### Impact Flags

- 📈 **Strong Positive**: Revenue increased >£100
- 🟢 **Positive**: Revenue increased £0-100
- ⚪ **Minimal**: Revenue change <£10 (not significant)
- 🟠 **Negative**: Revenue decreased £0-100
- 📉 **Strong Negative**: Revenue decreased >£100

### Metrics Explained

**Before/After Comparison**:
- **Impressions**: How many times product ad was shown
- **Clicks**: How many times users clicked
- **CTR**: Click-through rate (clicks/impressions)
- **Conversions**: Purchases tracked
- **Revenue**: Total conversion value
- **Cost**: Ad spend
- **ROAS**: Return on ad spend (revenue/cost)

**Change Metrics**:
- **Revenue Change %**: Percentage increase/decrease in revenue
- **Revenue Change £**: Absolute £ change
- **Clicks Change %**: Percentage increase/decrease in clicks

## Examples

### Example 1: Price Increase Hurts Conversions

```
📉 287: The Olive Tree Gift - Large (5L pot, 80cm height)
   Revenue: £-180.00 (-35.5%)
   Clicks: 422 → 301 (-28.7%)

Analysis: Price increased £34.99 → £39.99 (14% increase)
Impact: CTR stayed similar, but conversion rate dropped significantly
Recommendation: Consider reverting price or adding free shipping
```

### Example 2: Title Optimization Works

```
📈 281: Mini Olive Tree Gift - 20-25cm Tall in a 1L Pot - Hand Gift Wrapped
   Revenue: £+245.00 (+42.3%)
   Clicks: 156 → 218 (+39.7%)

Analysis: Title changed from "Mini Olive Tree" to include size/wrapping details
Impact: More specific title improved CTR and conversions
Recommendation: Apply similar title format to other products
```

### Example 3: Product Removal/Re-add (Feed Sync Issue)

```
⚪ 593: Lemon Tree Gift - Large 5L pot, 50-60cm High
   Revenue: £0.00 (no change)
   Clicks: 0 → 0 (product not active during analysis window)

Analysis: Product removed then re-added same day (feed sync issue)
Impact: Likely lost impressions during ~2-4 hour gap
Recommendation: Investigate Shopify feed sync stability
```

## Troubleshooting

### "No significant impacts detected"

This could mean:
1. No changes happened recently (>7 days ago)
2. Changes are too recent (<7 days) to have after-period data
3. Products had low traffic (<10 clicks threshold)
4. Changes were truly minimal

### "No ads data for client X"

Check:
1. Client is enabled in config.json
2. Google Ads customer ID is correct
3. Client has active Shopping campaigns

### Product IDs don't match

The analyzer handles different ID formats automatically:
- Sheets: `287`, `3539`
- Ads: `00287`, `03539`

If matches still fail, check the Merchant Center feed to verify product IDs.

## Phase 2 - Full Automation ✅ COMPLETE

**NEW**: Fully automated weekly analysis!

Features:
- ✅ Runs automatically every Tuesday at 9 AM (no asking needed)
- ✅ Sends professional HTML email reports automatically
- ✅ Tracks trends over time with historical analysis
- ✅ Statistical anomaly detection with severity classification
- ✅ Predictive insights from trend analysis

**Setup**: `./setup_automation.sh`
**Documentation**: See [PHASE2.md](PHASE2.md)

---

## Real-Time Monitoring ✅ NEW!

**Immediate alerts for critical changes**

Features:
- 🚨 Daily checks at 10 AM
- 📧 Instant email alerts for revenue drops >£500
- 💡 Opportunity alerts for revenue spikes
- ⚠️ Missing product detection
- 💬 Optional Slack integration

**What You Get**:
- "Product 287 revenue dropped £680 today - investigate!"
- "15 products disappeared from feed - sync issue?"
- Smart alerting (business hours only, no spam)

**Setup**: `./setup_monitoring.sh`
**Documentation**: See [MONITORING.md](MONITORING.md)

---

## Support

For issues or questions:
1. Check this README
2. Review `config.json` settings
3. Ask Claude: "Why isn't the impact analyzer working?"
