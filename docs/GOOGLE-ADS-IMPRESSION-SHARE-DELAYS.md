# Google Ads Impression Share Reporting Delays

**Status**: ✅ Documented  
**Date**: November 9, 2025  
**Issue Type**: Data Reporting Delay

---

## Problem

Impression share data in Google Ads can have reporting delays, particularly on Fridays. This can lead to false alarms when analyzing campaign performance.

---

## Evidence

### Cross-Account Analysis (Nov 9, 2025)

Analysis of 8 client accounts over 14 days shows consistent Friday impression share dips:

| Client | Friday Avg IS | Other Days Avg IS | Difference |
|--------|---------------|-------------------|------------|
| **Accessories for the Home** | 45.5% | 57.3% | **-11.8pp** 🔴 |
| Tree2Mydoor | 30.6% | 37.1% | -6.5pp 🟡 |
| Uno Lighting | 58.6% | 65.9% | -7.3pp 🟡 |
| Just Bin Bags | 50.3% | 58.0% | -7.7pp 🟡 |

### Google Ads Documentation

According to Google Ads support:
- Impression share updates less frequently than other metrics (clicks, impressions)
- Can take up to 48 hours to fully populate
- Some reports calculate once daily
- Known delays have occurred historically (e.g., August 2022)

---

## Impact

### False Alarms

When impression share drops on Friday, it may appear to be a performance issue when it's actually incomplete data:

- **Nov 7, 2025**: Accessories for the Home P-Max campaign showed 10% impression share drop
- **Analysis**: Cross-account check revealed Friday dips are systematic
- **Conclusion**: Likely data reporting delay, not actual performance problem

### Analysis Timing

- **Don't analyze Friday impression share data immediately**
- **Wait 48-72 hours** for data to fully populate
- **Re-check on Monday/Tuesday** for accurate analysis

---

## Best Practices

### When Analyzing Impression Share

1. **Avoid Friday Analysis**: Don't make decisions based on Friday impression share data
2. **Wait 48-72 Hours**: Allow time for data to fully populate
3. **Cross-Account Validation**: Check if other accounts show similar Friday dips
4. **Use Other Metrics**: Rely on clicks, impressions, cost, conversions (updated faster)
5. **Historical Comparison**: Compare with previous Fridays to identify patterns

### Scripts Available

- **`check-friday-is-patterns.py`**: Analyzes Friday impression share patterns across multiple clients
- **Location**: `clients/accessories-for-the-home/scripts/check-friday-is-patterns.py`

---

## Related Issues

- **Accessories for the Home P-Max Campaign** (Nov 7, 2025): Friday impression share drop initially appeared critical, but cross-account analysis revealed systematic Friday dips
- **ROAS Impact Analysis** (Nov 5-9, 2025): Preliminary analysis flagged impression share drop, but data may not have been fully populated

---

## References

- Google Ads Support: [Impression Share Reporting](https://support.google.com/google-ads/answer/2544985)
- Google Ads Developer Blog: [Impression Share Data Updates](https://ads-developers.googleblog.com/2017/11/search-impression-share-data-will-be.html)
- Cross-Account Analysis: `clients/accessories-for-the-home/audits/20251109-friday-is-pattern-analysis.json`

---

**Last Updated**: November 9, 2025  
**Next Review**: When new Friday dips are observed

