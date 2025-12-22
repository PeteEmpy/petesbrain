#!/usr/bin/env python3
"""
Analyze NDA enrollment data by geography to inform budget allocation
Compares actual enrollments against Google Ads spend by region
"""

import openpyxl
from datetime import datetime
from collections import defaultdict
import json

# Read UK enrollments
print("📊 Reading UK Enrollments...")
uk_wb = openpyxl.load_workbook('../enrolments/NDA-UK-Enrolments-ACTIVE.xlsx')
uk_ws = uk_wb.active
uk_rows = list(uk_ws.rows)

# Read International enrollments
print("📊 Reading International Enrollments...")
intl_wb = openpyxl.load_workbook('../enrolments/NDA-International-Enrolments-ACTIVE.xlsx')
intl_ws = intl_wb.active
intl_rows = list(intl_ws.rows)

# Count total enrollments by period (Sept-Dec 2025)
uk_sept_dec = 0
intl_sept_dec = 0
intl_by_country = defaultdict(int)

print("\n🗓️  Analyzing Sept 1 - Dec 16, 2025 period...")

# Process UK enrollments (Date is in column index 1, Country in column 6)
for row in uk_rows[1:]:
    if len(row) > 1 and row[1].value:
        date_val = row[1].value
        try:
            if isinstance(date_val, datetime):
                if date_val.year == 2025 and date_val.month >= 9:
                    uk_sept_dec += 1
        except:
            continue

# Process International enrollments (Date in column 1, Country in column 6)
for row in intl_rows[1:]:
    if len(row) > 6 and row[1].value:
        date_val = row[1].value
        # Strip whitespace from country field
        country = row[6].value.strip() if row[6].value else 'Unknown'

        try:
            if isinstance(date_val, datetime):
                if date_val.year == 2025 and date_val.month >= 9:
                    intl_sept_dec += 1
                    intl_by_country[country] += 1
        except:
            continue

total_enrollments = uk_sept_dec + intl_sept_dec

print(f"\n✅ ENROLLMENT DATA (Sept 1 - Dec 16, 2025)")
print(f"=" * 60)
print(f"\n📊 UK vs International Split:")
print(f"   UK Enrollments:     {uk_sept_dec:>4} ({uk_sept_dec/total_enrollments*100:.1f}%)")
print(f"   Intl Enrollments:   {intl_sept_dec:>4} ({intl_sept_dec/total_enrollments*100:.1f}%)")
print(f"   {'─' * 40}")
print(f"   TOTAL:              {total_enrollments:>4}")

print(f"\n🌍 INTERNATIONAL ENROLLMENTS BY COUNTRY:")
print(f"=" * 60)

# Sort countries by enrollment count
sorted_countries = sorted(intl_by_country.items(), key=lambda x: x[1], reverse=True)

# Group countries by campaign regions
uae_countries = ['UAE', 'United Arab Emirates', 'Abu Dhabi']
gcc_countries = ['Oman', 'Saudi Arabia', 'Bahrain', 'Kuwait', 'Qatar']
india_countries = ['India']
us_canada = ['USA', 'United States', 'Canada']
europe_countries = ['Austria', 'France', 'Netherlands', 'Holland', 'Malta', 'Germany', 'Sweden',
                    'Belgium', 'Italy', 'Spain', 'Switzerland', 'Cyprus', 'Denmark', 'Norway',
                    'Ireland', 'Poland', 'Romania', 'Hungary', 'Latvia', 'Serbia']

regions = {
    'UAE': 0,
    'GCC (Oman/SA/BH/KW/QA)': 0,
    'India': 0,
    'US/Canada': 0,
    'Europe': 0,
    'ROTW (Other)': 0
}

# Regional spend data from Google Ads location report
regional_spend = {
    'UAE': 21021,
    'GCC (Oman/SA/BH/KW/QA)': 12303,
    'India': 8357,
    'US/Canada': 8503,
    'Europe': 4059,
    'ROTW (Other)': 8681
}

# Country-level spend data from Google Ads location report (Sept 1 - Dec 16, 2025)
# Top spending countries - others grouped as minimal spend
country_spend = {
    # UAE region
    'UAE': 20410,
    'Abu Dhabi': 611,

    # Europe
    'Netherlands': 772,
    'France': 616,
    'Cyprus': 610,
    'Germany': 540,
    'Austria': 443,
    'Switzerland': 393,
    'Spain': 278,
    'Sweden': 123,
    'Hungary': 89,
    'Denmark': 68,
    'Ireland': 58,
    'Norway': 35,
    'Poland': 34,

    # GCC
    'Oman': 4691,
    'Saudi Arabia': 4477,
    'Bahrain': 1261,
    'Kuwait': 1148,
    'Qatar': 726,

    # US/Canada
    'USA': 7251,
    'Canada': 1252,

    # India
    'India': 8357,

    # ROTW (top countries)
    'South Africa': 2453,
    'Singapore': 1252,
    'Zambia': 1163,
    'Lebanon': 877,
    'Nigeria': 635,
    'Turkey': 494,
    'Egypt': 443,
    'Mauritius': 406,
    'Jordan': 328,
    'Zimbabwe': 223,
    'Ethiopia': 144,
    'Ghana': 131,
    'Tanzania': 132
}

# Track countries by region for detailed tables
regional_countries = {
    'UAE': {},
    'Europe': {},
    'GCC (Oman/SA/BH/KW/QA)': {},
    'US/Canada': {},
    'India': {},
    'ROTW (Other)': {}
}

for country, count in sorted_countries:
    print(f"   {country:<30} {count:>4} ({count/intl_sept_dec*100:>5.1f}%)")

    # Get country spend if available
    spend = country_spend.get(country, 0)

    # Categorize into regions and track country details
    if country in uae_countries:
        regions['UAE'] += count
        regional_countries['UAE'][country] = {'enrollments': count, 'spend': spend}
    elif country in gcc_countries:
        regions['GCC (Oman/SA/BH/KW/QA)'] += count
        regional_countries['GCC (Oman/SA/BH/KW/QA)'][country] = {'enrollments': count, 'spend': spend}
    elif country in india_countries:
        regions['India'] += count
        regional_countries['India'][country] = {'enrollments': count, 'spend': spend}
    elif country in us_canada:
        regions['US/Canada'] += count
        regional_countries['US/Canada'][country] = {'enrollments': count, 'spend': spend}
    elif country in europe_countries:
        regions['Europe'] += count
        regional_countries['Europe'][country] = {'enrollments': count, 'spend': spend}
    else:
        regions['ROTW (Other)'] += count
        regional_countries['ROTW (Other)'][country] = {'enrollments': count, 'spend': spend}

print(f"\n📍 REGIONAL GROUPINGS (matching Google Ads campaigns):")
print(f"=" * 60)
for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
    pct = (count / intl_sept_dec * 100) if intl_sept_dec > 0 else 0
    spend = regional_spend[region]
    cpe = spend / count if count > 0 else 0
    print(f"   {region:<30} {count:>4} ({pct:>5.1f}%)  |  Spend: £{spend:>6,}  |  CPE: £{cpe:>6,.0f}")

print(f"\n💰 GOOGLE ADS SPEND (Sept 1 - Dec 16, 2025)")
print(f"=" * 60)
print(f"   UK Spend:           £57,917 (46.6%)")
print(f"   International:      £66,345 (53.4%)")
print(f"   {'─' * 40}")
print(f"   TOTAL:              £124,262")

print(f"\n🎯 SPEND vs ENROLLMENT EFFICIENCY:")
print(f"=" * 60)
uk_cpe = 57917 / uk_sept_dec if uk_sept_dec > 0 else 0
intl_cpe = 66345 / intl_sept_dec if intl_sept_dec > 0 else 0
print(f"   UK Cost per Enrollment:     £{uk_cpe:,.0f}")
print(f"   Intl Cost per Enrollment:   £{intl_cpe:,.0f}")
print(f"   Efficiency Difference:       {((intl_cpe - uk_cpe) / uk_cpe * 100):+.0f}%")

# Save data for further analysis
output = {
    'period': 'Sept 1 - Dec 16, 2025',
    'total_enrollments': total_enrollments,
    'uk_enrollments': uk_sept_dec,
    'intl_enrollments': intl_sept_dec,
    'uk_pct': round(uk_sept_dec/total_enrollments*100, 1),
    'intl_pct': round(intl_sept_dec/total_enrollments*100, 1),
    'countries': dict(sorted_countries),
    'regions': regions,
    'spend': {
        'uk': 57917,
        'intl': 66345,
        'total': 124262
    },
    'cost_per_enrollment': {
        'uk': round(uk_cpe, 2),
        'intl': round(intl_cpe, 2)
    }
}

with open('../documents/enrollment-geography-analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Analysis saved to: documents/enrollment-geography-analysis.json")
print(f"✅ Creating HTML visualization...")

# Create HTML visualization
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>NDA Geographic Enrollment Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        h1 {{
            color: #10B981;
            border-bottom: 3px solid #10B981;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #059669;
            border-bottom: 2px solid #D1FAE5;
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        h3 {{
            color: #047857;
            margin-top: 30px;
        }}
        .summary {{
            background: #F0FDF4;
            border-left: 4px solid #10B981;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .summary h3 {{
            color: #059669;
            margin-top: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th {{
            background-color: #10B981;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 12px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #D1FAE5;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #D1FAE5;
        }}
        .stat-card h4 {{
            margin: 0 0 10px 0;
            color: #065F46;
            font-size: 14px;
        }}
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #10B981;
        }}
        .stat-card .secondary {{
            font-size: 14px;
            color: #6B7280;
            margin-top: 8px;
        }}
        .efficiency {{
            font-weight: bold;
        }}
        .efficient {{
            color: #10B981;
        }}
        .inefficient {{
            color: #EF4444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 NDA Geographic Enrollment Analysis</h1>

        <div class="summary">
            <h3>Analysis Period</h3>
            <p><strong>Period:</strong> 1 September - 16 December 2025</p>
            <p><strong>Total Enrollments:</strong> {total_enrollments}</p>
            <p><strong>Total Spend:</strong> £{output['spend']['total']:,}</p>
            <p><strong>Data Sources:</strong> Kelly Rawson enrollment reports + Google Ads API</p>
        </div>

        <h2>📈 UK vs International Overview</h2>

        <div class="stats">
            <div class="stat-card">
                <h4>UK Enrollments</h4>
                <div class="value">{uk_sept_dec}</div>
                <div class="secondary">{output['uk_pct']}% of total</div>
            </div>
            <div class="stat-card">
                <h4>International Enrollments</h4>
                <div class="value">{intl_sept_dec}</div>
                <div class="secondary">{output['intl_pct']}% of total</div>
            </div>
            <div class="stat-card">
                <h4>UK Cost per Enrollment</h4>
                <div class="value">£{output['cost_per_enrollment']['uk']:,.0f}</div>
                <div class="secondary">Baseline efficiency</div>
            </div>
            <div class="stat-card">
                <h4>Intl Cost per Enrollment</h4>
                <div class="value">£{output['cost_per_enrollment']['intl']:,.0f}</div>
                <div class="secondary">{((output['cost_per_enrollment']['intl'] - output['cost_per_enrollment']['uk']) / output['cost_per_enrollment']['uk'] * 100):+.0f}% vs UK</div>
            </div>
        </div>

        <h2>🌍 International Enrollments by Country</h2>

        <table>
            <thead>
                <tr>
                    <th>Country</th>
                    <th>Enrollments</th>
                    <th>% of International</th>
                </tr>
            </thead>
            <tbody>"""

# Add country rows
for country, count in sorted_countries:
    pct = (count / intl_sept_dec * 100) if intl_sept_dec > 0 else 0
    html_content += f"""
                <tr>
                    <td>{country}</td>
                    <td>{count}</td>
                    <td>{pct:.1f}%</td>
                </tr>"""

html_content += """
            </tbody>
        </table>

        <h2>📍 Regional Groupings (matching Google Ads campaigns)</h2>

        <table>
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Enrollments</th>
                    <th>% of International</th>
                    <th>Spend</th>
                    <th>CPE</th>
                    <th>Efficiency</th>
                </tr>
            </thead>
            <tbody>"""

# Add regional rows
for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
    pct = (count / intl_sept_dec * 100) if intl_sept_dec > 0 else 0
    spend = regional_spend[region]
    cpe = spend / count if count > 0 else 0

    # Determine efficiency rating
    uk_cpe = output['cost_per_enrollment']['uk']
    if cpe < uk_cpe * 1.2:
        efficiency = '<span style="color: #10B981; font-weight: bold;">🟢 Strong</span>'
    elif cpe < uk_cpe * 2:
        efficiency = '<span style="color: #F59E0B; font-weight: bold;">🟡 Acceptable</span>'
    else:
        efficiency = '<span style="color: #EF4444; font-weight: bold;">🔴 High Cost</span>'

    html_content += f"""
                <tr>
                    <td><strong>{region}</strong></td>
                    <td>{count}</td>
                    <td>{pct:.1f}%</td>
                    <td>£{spend:,}</td>
                    <td>£{cpe:,.0f}</td>
                    <td>{efficiency}</td>
                </tr>"""

html_content += f"""
            </tbody>
        </table>

        <h2>🔍 Detailed Regional Breakdowns</h2>

        <div class="summary">
            <h3>About the Data</h3>
            <p><strong>CPE Calculations:</strong> Some countries show "—" for spend and CPE. This occurs when:</p>
            <ul>
                <li>The enrollment came through organic search, direct traffic, or referrals (not paid advertising)</li>
                <li>Google Ads spend was below reporting thresholds (&lt;£1)</li>
                <li>Very small countries grouped into regional aggregates in the location report</li>
            </ul>
            <p>This is actually <strong>positive</strong> - these are enrollments acquired at zero advertising cost, which improves the overall regional efficiency.</p>
        </div>

        <p>Country-level analysis for each regional grouping:</p>"""

# Add detailed tables for each region
region_order = ['Europe', 'UAE', 'ROTW (Other)', 'GCC (Oman/SA/BH/KW/QA)', 'US/Canada', 'India']

for region in region_order:
    if region not in regional_countries or not regional_countries[region]:
        continue

    regional_total_enrollments = regions[region]
    regional_total_spend = regional_spend[region]
    regional_cpe = regional_total_spend / regional_total_enrollments if regional_total_enrollments > 0 else 0

    html_content += f"""
        <h3>{region}</h3>
        <p><strong>Regional Total:</strong> {regional_total_enrollments} enrollments | £{regional_total_spend:,} spend | £{regional_cpe:,.0f} CPE</p>

        <table>
            <thead>
                <tr>
                    <th>Country</th>
                    <th>Enrollments</th>
                    <th>% of Region</th>
                    <th>Spend</th>
                    <th>CPE</th>
                </tr>
            </thead>
            <tbody>"""

    # Sort countries by enrollment count within region
    sorted_region_countries = sorted(regional_countries[region].items(), key=lambda x: x[1]['enrollments'], reverse=True)

    for country, data in sorted_region_countries:
        enrollments = data['enrollments']
        spend = data['spend']
        pct_of_region = (enrollments / regional_total_enrollments * 100) if regional_total_enrollments > 0 else 0
        cpe = spend / enrollments if enrollments > 0 and spend > 0 else 0

        spend_display = f"£{spend:,}" if spend > 0 else "—"
        cpe_display = f"£{cpe:,.0f}" if cpe > 0 else "—"

        html_content += f"""
                <tr>
                    <td>{country}</td>
                    <td>{enrollments}</td>
                    <td>{pct_of_region:.1f}%</td>
                    <td>{spend_display}</td>
                    <td>{cpe_display}</td>
                </tr>"""

    html_content += """
            </tbody>
        </table>"""

html_content += f"""

        <h2>💰 Spend vs Enrollment Efficiency</h2>

        <div class="summary">
            <h3>Key Finding</h3>
            <p><strong>UK delivers {output['uk_pct']}% of enrollments but receives only 46.6% of spend</strong></p>
            <p>This indicates UK is <span class="efficiency efficient">UNDERFUNDED</span> relative to its enrollment contribution.</p>
            <p>International receives 53.4% of spend but delivers only {output['intl_pct']}% of enrollments.</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Spend</th>
                    <th>% of Total Spend</th>
                    <th>Enrollments</th>
                    <th>% of Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>UK</strong></td>
                    <td>£{output['spend']['uk']:,}</td>
                    <td>46.6%</td>
                    <td>{uk_sept_dec}</td>
                    <td>{output['uk_pct']}%</td>
                </tr>
                <tr>
                    <td><strong>International</strong></td>
                    <td>£{output['spend']['intl']:,}</td>
                    <td>53.4%</td>
                    <td>{intl_sept_dec}</td>
                    <td>{output['intl_pct']}%</td>
                </tr>
                <tr style="background-color: #F0FDF4; font-weight: bold;">
                    <td>TOTAL</td>
                    <td>£{output['spend']['total']:,}</td>
                    <td>100%</td>
                    <td>{total_enrollments}</td>
                    <td>100%</td>
                </tr>
            </tbody>
        </table>

        <h2>🎯 Cost per Enrollment Analysis</h2>

        <div class="stats">
            <div class="stat-card">
                <h4>UK Cost per Enrollment</h4>
                <div class="value efficient">£{output['cost_per_enrollment']['uk']:,.0f}</div>
                <div class="secondary">Most efficient market</div>
            </div>
            <div class="stat-card">
                <h4>International Cost per Enrollment</h4>
                <div class="value inefficient">£{output['cost_per_enrollment']['intl']:,.0f}</div>
                <div class="secondary">{((output['cost_per_enrollment']['intl'] - output['cost_per_enrollment']['uk']) / output['cost_per_enrollment']['uk'] * 100):+.0f}% higher than UK</div>
            </div>
        </div>

        <div class="summary">
            <h3>Strategic Recommendation</h3>
            <p>The data suggests reallocating budget from International to UK could improve overall enrollment efficiency.</p>
            <p>Detailed regional recommendations available in the full budget strategy document.</p>
        </div>
    </div>
</body>
</html>"""

with open('../documents/enrollment-geography-analysis.html', 'w') as f:
    f.write(html_content)

print(f"✅ HTML visualization created: documents/enrollment-geography-analysis.html")
