#!/usr/bin/env python3
"""
Correlate Google Ads performance with enrollment data by country
Calculate ROAS, CPA, and identify optimization opportunities
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv

# File paths
STANDARDIZED_ENROLLMENTS = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/enrolments/NDA-International-Enrolments-STANDARDIZED.json")
GOOGLE_ADS_RAW_DATA = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/data/google-ads-country-performance-aug-nov-2025.json")
OUTPUT_CORRELATION_CSV = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/data/country-correlation-analysis.csv")
OUTPUT_RECOMMENDATIONS = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/documents/country-budget-recommendations.md")

# Assumptions for ROAS calculation
AVERAGE_COURSE_FEE_GBP = 3500  # Estimate - needs validation with client
ENROLLMENT_CONVERSION_RATE = 0.15  # 15% of applications convert to enrollments (estimate)

# Google Ads geo target ID to country name mapping
GEO_COUNTRY_MAPPING = {
    2356: "India",
    2826: "United Kingdom",
    2682: "Saudi Arabia",
    2012: "Algeria",
    2144: "Sri Lanka",
    2764: "Thailand",
    2784: "United Arab Emirates",
    2512: "Oman",
    2414: "Kuwait",
    2710: "South Africa",
    2634: "Qatar",
    2048: "Bahrain",
    2458: "Malaysia",
    2894: "Zambia",
    2840: "United States",
    2124: "Canada",
    2858: "Uruguay",
    2702: "Singapore",
    2300: "Greece",
    2392: "Japan",
    2376: "Israel",
    2196: "Cyprus",
    2372: "Ireland",
    2528: "Netherlands",
    2156: "China",
    2276: "Germany",
    2250: "France",
    2470: "Malta",
    2724: "Spain",
    2752: "Sweden",
    2380: "Italy",
    2348: "Hungary",
    2428: "Latvia",
    2756: "Switzerland",
    2040: "Austria",
    2208: "Denmark",
    2352: "Iceland",
}

# Google Ads data (from previous query - Aug 1 - Nov 3, 2025)
GOOGLE_ADS_DATA = {
    "India": {"impressions": 13361984, "clicks": 134842, "cost_micros": 8475425577, "conversions": 26.848289},
    "Saudi Arabia": {"impressions": 2336407, "clicks": 13685, "cost_micros": 7602739456, "conversions": 9.685432},
    "Algeria": {"impressions": 2210203, "clicks": 32888, "cost_micros": 1903636509, "conversions": 12.861394},
    "Sri Lanka": {"impressions": 2053970, "clicks": 22221, "cost_micros": 841107505, "conversions": 3.0},
    "Thailand": {"impressions": 1537294, "clicks": 3482, "cost_micros": 912472583, "conversions": 1.0},
    "United Arab Emirates": {"impressions": 1473490, "clicks": 10343, "cost_micros": 17337896552, "conversions": 31.957929},
    "United Kingdom": {"impressions": 1378727, "clicks": 21653, "cost_micros": 46609577710, "conversions": 396.708147},
    "Oman": {"impressions": 1007842, "clicks": 5531, "cost_micros": 1120775201, "conversions": 0.0},
    "Kuwait": {"impressions": 853405, "clicks": 4334, "cost_micros": 2057318672, "conversions": 9.5},
    "South Africa": {"impressions": 821623, "clicks": 12621, "cost_micros": 2973521565, "conversions": 12.0},
    "Qatar": {"impressions": 622033, "clicks": 3446, "cost_micros": 1995498723, "conversions": 0.949695},
    "Bahrain": {"impressions": 489048, "clicks": 2371, "cost_micros": 786797570, "conversions": 1.0},
    "Malaysia": {"impressions": 486234, "clicks": 3407, "cost_micros": 375906848, "conversions": 0.0},
    "Zambia": {"impressions": 395437, "clicks": 8406, "cost_micros": 1053365405, "conversions": 8.3301},
    "United States": {"impressions": 266634, "clicks": 2245, "cost_micros": 6516150269, "conversions": 26.0},
    "Canada": {"impressions": 112069, "clicks": 695, "cost_micros": 1272145103, "conversions": 1.0},
    "Uruguay": {"impressions": 29427, "clicks": 163, "cost_micros": 16446290, "conversions": 0.0},
    "Singapore": {"impressions": 28458, "clicks": 943, "cost_micros": 1580258383, "conversions": 0.0},
    "Greece": {"impressions": 18918, "clicks": 237, "cost_micros": 198211643, "conversions": 0.0},
    "Japan": {"impressions": 18779, "clicks": 160, "cost_micros": 99975777, "conversions": 0.0},
    "Israel": {"impressions": 16950, "clicks": 149, "cost_micros": 102201877, "conversions": 0.0},
    "Cyprus": {"impressions": 15894, "clicks": 522, "cost_micros": 733486301, "conversions": 0.0},
    "Ireland": {"impressions": 14732, "clicks": 154, "cost_micros": 267378280, "conversions": 1.0},
    "Netherlands": {"impressions": 13398, "clicks": 502, "cost_micros": 919280750, "conversions": 0.0},
    "China": {"impressions": 13093, "clicks": 174, "cost_micros": 48379301, "conversions": 0.0},
    "Germany": {"impressions": 12931, "clicks": 384, "cost_micros": 711702364, "conversions": 0.0},
    "France": {"impressions": 12879, "clicks": 334, "cost_micros": 711633154, "conversions": 1.0},
    "Malta": {"impressions": 8815, "clicks": 297, "cost_micros": 241141746, "conversions": 0.0},
    "Spain": {"impressions": 8748, "clicks": 151, "cost_micros": 258495184, "conversions": 3.0},
    "Sweden": {"impressions": 7847, "clicks": 166, "cost_micros": 369957664, "conversions": 20.0},
    "Italy": {"impressions": 7551, "clicks": 116, "cost_micros": 147574614, "conversions": 0.0},
    "Hungary": {"impressions": 7316, "clicks": 93, "cost_micros": 68471932, "conversions": 0.0},
    "Latvia": {"impressions": 5733, "clicks": 64, "cost_micros": 37954460, "conversions": 0.0},
    "Switzerland": {"impressions": 4351, "clicks": 194, "cost_micros": 418323013, "conversions": 1.0},
    "Austria": {"impressions": 4231, "clicks": 123, "cost_micros": 213864988, "conversions": 0.0},
    "Denmark": {"impressions": 3772, "clicks": 62, "cost_micros": 75711452, "conversions": 0.0},
    "Iceland": {"impressions": 2274, "clicks": 51, "cost_micros": 64501512, "conversions": 0.0},
}

def load_enrollment_data():
    """Load standardized enrollment data"""
    with open(STANDARDIZED_ENROLLMENTS, 'r') as f:
        data = json.load(f)

    # Count enrollments by country (Aug-Nov 2025 only)
    country_enrollments = defaultdict(int)

    for enrollment in data['enrollments']:
        # Parse date
        if enrollment['date']:
            try:
                # Handle different date formats
                date_str = enrollment['date']

                # Handle "YYYY-MM-DD HH:MM:SS" format
                if ' ' in date_str:
                    date_str = date_str.split()[0]

                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        enroll_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # Can't parse date, skip
                    continue

                # Only count Aug-Nov 2025 enrollments
                if enroll_date >= datetime(2025, 8, 1) and enroll_date <= datetime(2025, 11, 3):
                    country_enrollments[enrollment['standard_country']] += 1

            except Exception as e:
                continue

    return country_enrollments

def correlate_data():
    """Correlate Google Ads with enrollment data"""

    print("="*80)
    print("COUNTRY CORRELATION ANALYSIS: Google Ads Performance vs Enrollments")
    print("="*80)
    print(f"\nPeriod: August 1 - November 3, 2025 (3 months)")
    print(f"Average Course Fee: £{AVERAGE_COURSE_FEE_GBP:,.2f} (estimate)")
    print(f"Enrollment Conversion Rate: {ENROLLMENT_CONVERSION_RATE*100:.1f}% (estimate)\n")

    # Load enrollment data
    print("Loading enrollment data...")
    enrollment_counts = load_enrollment_data()
    print(f"✓ Loaded enrollment data for {len(enrollment_counts)} countries\n")

    # Build correlation dataset
    correlation_data = []

    # Get all unique countries from both sources
    all_countries = set(GOOGLE_ADS_DATA.keys()) | set(enrollment_counts.keys())

    for country in sorted(all_countries):
        ads_data = GOOGLE_ADS_DATA.get(country, {})
        enrollment_count = enrollment_counts.get(country, 0)

        # Google Ads metrics
        impressions = ads_data.get('impressions', 0)
        clicks = ads_data.get('clicks', 0)
        cost_micros = ads_data.get('cost_micros', 0)
        conversions = ads_data.get('conversions', 0)

        # Convert cost to GBP
        cost_gbp = cost_micros / 1_000_000

        # Calculate metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (cost_gbp / clicks) if clicks > 0 else 0
        cpa_conversion = (cost_gbp / conversions) if conversions > 0 else 0

        # Estimated enrollments from conversions (not actual enrollments)
        estimated_enrollments = conversions * ENROLLMENT_CONVERSION_RATE

        # Revenue calculations
        estimated_revenue = estimated_enrollments * AVERAGE_COURSE_FEE_GBP
        actual_revenue = enrollment_count * AVERAGE_COURSE_FEE_GBP

        # ROAS calculations
        estimated_roas = (estimated_revenue / cost_gbp * 100) if cost_gbp > 0 else 0
        actual_roas = (actual_revenue / cost_gbp * 100) if cost_gbp > 0 else 0

        # CPA calculations
        cpa_estimated = (cost_gbp / estimated_enrollments) if estimated_enrollments > 0 else 0
        cpa_actual = (cost_gbp / enrollment_count) if enrollment_count > 0 else 0

        # Determine opportunity category
        if impressions > 0 and enrollment_count > 0:
            category = "Active & Converting"
        elif impressions > 0 and enrollment_count == 0:
            category = "Ads Active, No Enrollments"
        elif impressions == 0 and enrollment_count > 0:
            category = "Expansion Opportunity"
        else:
            category = "No Activity"

        # Performance tier
        if impressions > 1000000:
            tier = "Tier 1: High Volume"
        elif impressions > 100000:
            tier = "Tier 2: Medium Volume"
        elif impressions > 0:
            tier = "Tier 3: Low Volume"
        else:
            tier = "Tier 4: No Ads"

        row = {
            "country": country,
            "tier": tier,
            "category": category,
            "impressions": impressions,
            "clicks": clicks,
            "spend_gbp": round(cost_gbp, 2),
            "conversions": round(conversions, 2),
            "ctr_percent": round(ctr, 2),
            "cpc_gbp": round(cpc, 2),
            "cpa_conversion_gbp": round(cpa_conversion, 2),
            "estimated_enrollments": round(estimated_enrollments, 2),
            "actual_enrollments": enrollment_count,
            "estimated_revenue_gbp": round(estimated_revenue, 2),
            "actual_revenue_gbp": round(actual_revenue, 2),
            "estimated_roas_percent": round(estimated_roas, 0),
            "actual_roas_percent": round(actual_roas, 0),
            "cpa_estimated_gbp": round(cpa_estimated, 2),
            "cpa_actual_gbp": round(cpa_actual, 2),
        }

        correlation_data.append(row)

    return correlation_data

def save_correlation_csv(data):
    """Save correlation data to CSV"""

    # Create data directory if it doesn't exist
    Path(OUTPUT_CORRELATION_CSV).parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_CORRELATION_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✓ Correlation data saved: {OUTPUT_CORRELATION_CSV}\n")

def generate_recommendations(data):
    """Generate budget recommendations based on correlation analysis"""

    # Sort by different criteria for recommendations
    high_roas = [d for d in data if d['actual_roas_percent'] > 0]
    high_roas.sort(key=lambda x: x['actual_roas_percent'], reverse=True)

    opportunity_gaps = [d for d in data if d['impressions'] > 100000 and d['actual_enrollments'] == 0]
    opportunity_gaps.sort(key=lambda x: x['spend_gbp'], reverse=True)

    expansion_opps = [d for d in data if d['impressions'] == 0 and d['actual_enrollments'] > 0]
    expansion_opps.sort(key=lambda x: x['actual_enrollments'], reverse=True)

    low_cpa = [d for d in data if d['cpa_actual_gbp'] > 0]
    low_cpa.sort(key=lambda x: x['cpa_actual_gbp'])

    # Generate markdown report
    report = f"""# NDA Country Budget Recommendations
## Based on Google Ads & Enrollment Correlation Analysis

**Period Analyzed:** August 1 - November 3, 2025 (3 months)
**Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Key Assumptions

⚠️ **IMPORTANT: Validate these assumptions with client before implementing recommendations**

- **Average Course Fee**: £{AVERAGE_COURSE_FEE_GBP:,.2f}
- **Enrollment Conversion Rate**: {ENROLLMENT_CONVERSION_RATE*100:.1f}% (applications to enrollments)
- **Attribution Model**: Direct attribution (enrollment date matches Google Ads period)
- **Data Completeness**: Enrollment data may have lag (students enroll weeks after ad click)

---

## Executive Summary

**Total Google Ads Performance (Aug-Nov 2025)**:
- **Spend**: £{sum(d['spend_gbp'] for d in data):,.2f}
- **Conversions**: {sum(d['conversions'] for d in data):.1f}
- **Actual Enrollments**: {sum(d['actual_enrollments'] for d in data):,}
- **Estimated Revenue**: £{sum(d['actual_revenue_gbp'] for d in data):,.2f}
- **Overall ROAS**: {(sum(d['actual_revenue_gbp'] for d in data) / sum(d['spend_gbp'] for d in data) * 100) if sum(d['spend_gbp'] for d in data) > 0 else 0:.0f}%

---

## 🏆 Top Performing Countries (Best ROAS)

These countries show the highest return on Google Ads spend. **Prioritize budget increases here.**

"""

    for idx, country_data in enumerate(high_roas[:10], 1):
        report += f"""### {idx}. {country_data['country']}
- **ROAS**: {country_data['actual_roas_percent']:.0f}%
- **Spend**: £{country_data['spend_gbp']:,.2f}
- **Actual Enrollments**: {country_data['actual_enrollments']}
- **Revenue**: £{country_data['actual_revenue_gbp']:,.2f}
- **CPA**: £{country_data['cpa_actual_gbp']:,.2f}
- **Recommendation**: {'✅ Increase budget 50-100%' if country_data['actual_roas_percent'] > 500 else '✅ Increase budget 25-50%'}

"""

    report += """---

## ⚠️ Opportunity Gaps (High Spend, No Enrollments)

These countries received significant Google Ads impressions but show **zero actual enrollments**. Investigate and optimize or exclude.

"""

    for idx, country_data in enumerate(opportunity_gaps[:10], 1):
        report += f"""### {idx}. {country_data['country']}
- **Impressions**: {country_data['impressions']:,}
- **Spend**: £{country_data['spend_gbp']:,.2f}
- **Conversions**: {country_data['conversions']}
- **Actual Enrollments**: 0
- **Issue**: High ad activity but no enrollments
- **Recommendation**: {'🛑 Pause campaigns or add geo-exclusion' if country_data['spend_gbp'] > 500 else '⚠️ Monitor and optimize targeting'}

"""

    report += """---

## 🎯 Expansion Opportunities (High Enrollments, Low/No Ads)

These countries show strong enrollment numbers but **minimal or no Google Ads activity**. Potential high-ROI expansion markets.

"""

    for idx, country_data in enumerate(expansion_opps[:10], 1):
        report += f"""### {idx}. {country_data['country']}
- **Actual Enrollments**: {country_data['actual_enrollments']}
- **Google Ads Spend**: £{country_data['spend_gbp']:,.2f}
- **Revenue**: £{country_data['actual_revenue_gbp']:,.2f}
- **Current Impressions**: {country_data['impressions']:,}
- **Recommendation**: {'🚀 Launch dedicated campaign (high priority)' if country_data['actual_enrollments'] > 10 else '🔍 Test with small budget (£300-500/month)'}

"""

    report += """---

## 💰 Most Efficient Markets (Lowest CPA)

Countries with the lowest cost per actual enrollment. **These markets are highly efficient.**

"""

    for idx, country_data in enumerate(low_cpa[:10], 1):
        report += f"""### {idx}. {country_data['country']}
- **CPA (Actual)**: £{country_data['cpa_actual_gbp']:,.2f}
- **Enrollments**: {country_data['actual_enrollments']}
- **Spend**: £{country_data['spend_gbp']:,.2f}
- **ROAS**: {country_data['actual_roas_percent']:.0f}%
- **Recommendation**: ✅ Maintain or increase budget

"""

    report += """---

## Recommended Budget Reallocation

### Phase 1: Immediate Actions (Week 1)

1. **Pause/Exclude Low Performers**:
"""

    for country_data in opportunity_gaps[:5]:
        if country_data['spend_gbp'] > 500:
            report += f"   - {country_data['country']}: £{country_data['spend_gbp']:,.2f} spend, 0 enrollments → **Pause or exclude**\n"

    report += f"""
   **Budget Freed**: ~£{sum(d['spend_gbp'] for d in opportunity_gaps[:5] if d['spend_gbp'] > 500):,.2f}/month

2. **Increase Top Performers**:
"""

    for country_data in high_roas[:3]:
        increase_pct = 50 if country_data['actual_roas_percent'] > 500 else 25
        increase_gbp = country_data['spend_gbp'] * (increase_pct / 100)
        report += f"   - {country_data['country']}: {country_data['actual_roas_percent']:.0f}% ROAS → **Increase by {increase_pct}%** (+£{increase_gbp:,.2f}/month)\n"

    report += """
### Phase 2: Expansion Testing (Weeks 2-4)

Launch small test campaigns in high-enrollment markets with no current ads:

"""

    for country_data in expansion_opps[:5]:
        if country_data['actual_enrollments'] > 5:
            report += f"""- **{country_data['country']}**: {country_data['actual_enrollments']} enrollments (£{country_data['actual_revenue_gbp']:,.2f} revenue)
  - Test Budget: £300-500/month
  - Campaign Structure: Similar to successful {high_roas[0]['country']} campaign
  - Expected ROAS: 300-500% (based on organic enrollment success)

"""

    report += """### Phase 3: Optimization (Month 2+)

1. **Review Phase 2 test results** after 30 days
2. **Scale winners** (ROAS >400%)
3. **Pause losers** (ROAS <200%)
4. **Implement Phase 2 expansion** for next tier countries

---

## Next Steps: Data Validation Required

⚠️ **Before implementing these recommendations, validate:**

1. **Average Course Fee by Country**: Does pricing vary by geography?
2. **Enrollment Attribution Lag**: How long from ad click to enrollment? (may need 60-90 day window)
3. **Conversion Tracking Accuracy**: Are all enrollments properly attributed to Google Ads?
4. **Enrollment vs Application Rate**: Is 15% conversion rate accurate across all countries?

**Recommended Action**: Meet with client to review assumptions and gather additional revenue data.

---

## Files Generated

- Correlation Dataset (CSV): `{OUTPUT_CORRELATION_CSV}`
- This Report: `{OUTPUT_RECOMMENDATIONS}`

---

**Prepared by:** Claude Code (Roksys AI Analysis)
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Contact:** Peter Empson - petere@roksys.co.uk
"""

    return report

def main():
    # Run correlation
    correlation_data = correlate_data()

    # Save CSV
    save_correlation_csv(correlation_data)

    # Generate recommendations
    print("Generating budget recommendations...")
    recommendations = generate_recommendations(correlation_data)

    # Create documents directory if it doesn't exist
    Path(OUTPUT_RECOMMENDATIONS).parent.mkdir(parents=True, exist_ok=True)

    # Save recommendations
    with open(OUTPUT_RECOMMENDATIONS, 'w') as f:
        f.write(recommendations)

    print(f"✓ Recommendations saved: {OUTPUT_RECOMMENDATIONS}\n")

    print("="*80)
    print("✓ CORRELATION ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nGenerated files:")
    print(f"  1. {OUTPUT_CORRELATION_CSV}")
    print(f"  2. {OUTPUT_RECOMMENDATIONS}")
    print(f"\nNext: Review recommendations with client to validate assumptions")

if __name__ == '__main__':
    main()
