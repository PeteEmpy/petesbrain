# Superspace Scripts

Client-specific automation and monitoring scripts for Superspace Google Ads account management.

## Budget Monitoring

### `monitor-us-budget.py`

Tracks daily spend against new budget targets (Nov 13, 2025 increase: £12,010/day total).

**Purpose:**
- Monitor daily spend pacing vs. target budgets
- Track conversions and revenue (no ROAS calculations)
- Identify underspending or overspending early
- Campaign-level spend breakdown

**Budget Targets (as of Nov 13, 2025):**
- Shopping Branded: £4,500/day
- P Max Brand Excluded: £2,700/day
- Shopping Brand Excluded: £2,200/day
- Search Brand Inclusion: £1,200/day
- Search Generics: £790/day
- Demand Gen main: £450/day
- Demand Gen Retargeting: £150/day
- **Total: £12,010/day**

**Usage:**

```bash
# Run with default 7-day lookback
GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml \
  shared/email-sync/.venv/bin/python3 \
  clients/superspace/scripts/monitor-us-budget.py

# Run with custom lookback period
GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml \
  shared/email-sync/.venv/bin/python3 \
  clients/superspace/scripts/monitor-us-budget.py --days 14
```

**Output Sections:**

1. **Daily Spend Breakdown** - Shows spend, variance vs target, pacing %, conversions, and revenue per day
2. **Campaign Performance** - Period totals by campaign with budget allocation %
3. **Key Insights** - Automated alerts for underspending/overspending with recommended actions

**Pacing Indicators:**
- ✅ Green: 90-110% of target (on track)
- ⚠️ Yellow: 80-120% of target (acceptable range)
- 🔴 Red: <80% or >120% (needs attention)

**When to Run:**
- Daily during Black Friday/Cyber Monday period (Nov 13 - Dec 2)
- Weekly during normal periods
- On-demand when checking budget performance

**Notes:**
- Script pulls data via Google Ads API (requires GOOGLE_ADS_CONFIGURATION_FILE_PATH)
- Uses shared/email-sync venv for dependencies
- Filters to US campaigns only (campaign.name LIKE '%US%')
- Currency is GBP (account currency)

**Monitoring Context:**
- Budget increase implemented: Nov 13, 2025 (from ~£5,000/day to £12,010/day = 140% increase)
- Reason: Core campaign CR at 4.88-5.35%, stock availability, Black Friday/Cyber Monday prep
- Target ROAS: Holding at 550% (not reduced)
- Logged in: `/Users/administrator/Documents/PetesBrain/roksys/spreadsheets/rok-experiments-client-notes.csv`

---

## Future Scripts

Additional scripts may be added here for:
- Weekly performance summaries
- Stock level integration
- Conversion rate tracking
- Product feed monitoring

---

**Last Updated:** 2025-11-13
**Contact:** petere@roksys.co.uk
