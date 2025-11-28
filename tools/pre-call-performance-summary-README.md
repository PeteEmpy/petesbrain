# Pre-Call Performance Summary

Quick Google Ads performance snapshot for client calls - shows last 7 days performance with week-over-week and year-over-year comparisons. **Automatically opens in your browser for easy viewing.**

## Overview

This tool provides a concise performance summary perfect for reviewing just before a client call. It shows:

- **Last 7 days** performance metrics (revenue, spend, ROAS, conversions, CPA, CVR)
- **Week-over-week** comparison (vs previous 7 days)
- **Year-over-year** comparison (vs same period last year)
- **Key successes and failures** automatically highlighted
- **Beautiful HTML report** that opens automatically in your browser

## Usage

```bash
# Show all active clients
python tools/pre-call-performance-summary.py

# Show specific client
python tools/pre-call-performance-summary.py accessories-for-the-home
python tools/pre-call-performance-summary.py go-glean
```

## What Happens

1. **Fetches performance data** from Google Ads API
2. **Generates HTML report** with styled, professional layout
3. **Saves report** to `tools/pre-call-reports/` directory
4. **Opens automatically** in your default browser
5. **Prints summary** to console as well

## Output Format

The HTML report displays:
- **Current 7-day metrics** in a clean card layout
- **Week-over-week changes** with visual indicators (↑/↓/→) and color coding
- **Year-over-year changes** in comparison tables
- **Key successes** (green cards) - significant improvements
- **Key concerns** (red cards) - significant declines

The report is fully self-contained (no external dependencies) and can be:
- Viewed offline
- Shared with team members
- Printed or saved as PDF
- Screenshot for presentations

## Requirements

- Google Ads API access configured
- Client configuration in `shared/data/google-ads-clients.json`
- Python environment with required dependencies
- Default web browser installed

## Example Output

The browser will show a professional report with:
- Gradient header with client name and date range
- Metric cards showing key performance indicators
- Comparison tables with color-coded changes
- Insight cards highlighting successes and concerns

## Additional Features

### 🧪 Recent Experiments & Tests
- Shows experiments logged in the last 30 days from `roksys/spreadsheets/rok-experiments-client-notes.csv`
- Displays experiment notes with dates
- Highlights review dates (upcoming or overdue)
- Perfect for discussing recent strategy changes with clients

### 📦 Product Issues & Changes
- **Price Changes**: Shows significant price changes (>5%) from the last 7 days
  - Displays product name, old/new prices, and percentage change
  - Color-coded (red for increases, green for decreases)
- **Product Disapprovals**: Lists currently disapproved products from Merchant Center
  - Shows disapproval reasons
  - Helps identify feed issues affecting campaign performance

## Notes

- Handles missing historical data gracefully
- Works across all active clients configured in `google-ads-clients.json`
- Automatically flags significant changes (>10% revenue, >10pp ROAS, >15% conversions/CPA)
- HTML reports are saved with timestamps for reference
- Reports are saved in `tools/pre-call-reports/` directory
- Product issues require Product Impact Analyzer data (price changes and disapprovals)
- Experiments require `rok-experiments-client-notes.csv` file

