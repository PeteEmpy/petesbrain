#!/usr/bin/env python3
"""
Generate HTML report with styled tables for Devonshire Hotels Paid Search
Tables can be screenshot and inserted into Google Slides

Usage:
    python3 generate_html_report.py --month 2025-10
"""

import argparse
import os
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate HTML report for Devonshire Hotels Paid Search'
    )
    parser.add_argument(
        '--month',
        type=str,
        required=True,
        help='Month to generate report for (YYYY-MM format, e.g., 2025-10)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output HTML file path (default: devonshire-paid-search-YYYY-MM.html)'
    )
    return parser.parse_args()


def generate_html(month_str: str) -> str:
    """Generate HTML report with styled tables."""

    year, month = map(int, month_str.split('-'))
    month_name = datetime(year, month, 1).strftime('%B %Y')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devonshire Hotels - Paid Search Report - {month_name}</title>
    <style>
        :root {{
            --primary: #00333d;  /* Estate Blue */
            --surface-1: #ffffff;
            --surface-2: #f5f5f5;
            --border: #d0d0d0;
            --text-primary: #000000;
            --text-secondary: #666666;
            --stone: #E5E3DB;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.4;
            color: var(--text-primary);
            background: white;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
        }}

        h1 {{
            color: var(--primary);
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: bold;
        }}

        h2 {{
            color: var(--primary);
            font-size: 20px;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: bold;
        }}

        .report-meta {{
            color: var(--text-secondary);
            font-size: 13px;
            margin-bottom: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            margin-bottom: 25px;
            background: white;
            font-size: 14px;
        }}

        th {{
            background-color: var(--primary);
            color: white;
            padding: 10px 12px;
            text-align: left;
            font-weight: bold;
            font-size: 14px;
            border: 1px solid var(--border);
        }}

        td {{
            padding: 10px 12px;
            border: 1px solid var(--border);
            font-size: 14px;
            background-color: var(--stone);
        }}

        tr:hover td {{
            background-color: #ddd;
        }}

        .metric-value {{
            font-weight: bold;
        }}

        .positive {{
            color: #2e7d32;
            font-weight: bold;
        }}

        .negative {{
            color: #c62828;
            font-weight: bold;
        }}

        .warning {{
            color: #f57c00;
            font-weight: bold;
        }}

        .notes {{
            font-size: 13px;
            color: var(--text-primary);
            margin-top: 10px;
            margin-bottom: 20px;
            padding: 12px;
            background: #f9f9f9;
            border-left: 3px solid var(--primary);
        }}

        @media print {{
            body {{
                background: white;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Devonshire Hotels - Paid Search Report</h1>
        <div class="report-meta">
            <strong>{month_name}</strong> | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>

        <!-- Executive Summary -->
        <h2>Executive Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Budget</td>
                    <td class="metric-value">£11,730.00</td>
                </tr>
                <tr>
                    <td>Actual Spend</td>
                    <td class="metric-value">£10,112.94</td>
                </tr>
                <tr>
                    <td>Variance</td>
                    <td class="metric-value positive">£954.07 under budget (8.13%)</td>
                </tr>
                <tr>
                    <td>Pacing</td>
                    <td class="metric-value positive">91.87%</td>
                </tr>
                <tr>
                    <td>Total Revenue</td>
                    <td class="metric-value">£58,693.89</td>
                </tr>
                <tr>
                    <td>ROAS</td>
                    <td class="metric-value positive">5.80x</td>
                </tr>
                <tr>
                    <td>Total Conversions</td>
                    <td class="metric-value">132.58</td>
                </tr>
                <tr>
                    <td>Impressions</td>
                    <td class="metric-value">228,733</td>
                </tr>
                <tr>
                    <td>Clicks</td>
                    <td class="metric-value">23,026</td>
                </tr>
                <tr>
                    <td>Average CTR</td>
                    <td class="metric-value">10.07%</td>
                </tr>
            </tbody>
        </table>

        <!-- Hotels - Top Performers -->
        <h2>Hotels - Top Performers by ROAS</h2>
        <table>
            <thead>
                <tr>
                    <th>Property</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>Conversions</th>
                    <th>ROAS</th>
                    <th>Clicks</th>
                    <th>CTR</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Devonshire Arms</strong></td>
                    <td>£1,389.34</td>
                    <td>£12,628.09</td>
                    <td>33.58</td>
                    <td class="metric-value positive">9.09x</td>
                    <td>3,988</td>
                    <td>30.32%</td>
                </tr>
                <tr>
                    <td><strong>Cavendish</strong></td>
                    <td>£1,355.35</td>
                    <td>£8,851.42</td>
                    <td>14.75</td>
                    <td class="metric-value positive">6.53x</td>
                    <td>3,790</td>
                    <td>35.64%</td>
                </tr>
                <tr>
                    <td><strong>P Max All</strong></td>
                    <td>£2,585.01</td>
                    <td>£16,065.68</td>
                    <td>34.17</td>
                    <td class="metric-value positive">6.21x</td>
                    <td>4,685</td>
                    <td>3.28%</td>
                </tr>
                <tr>
                    <td><strong>Locations (Chatsworth)</strong></td>
                    <td>£537.12</td>
                    <td>£2,902.00</td>
                    <td>4.00</td>
                    <td class="metric-value positive">5.40x</td>
                    <td>1,003</td>
                    <td>10.76%</td>
                </tr>
                <tr>
                    <td><strong>Beeley Inn</strong></td>
                    <td>£1,023.30</td>
                    <td>£4,634.33</td>
                    <td>11.33</td>
                    <td class="metric-value positive">4.53x</td>
                    <td>1,745</td>
                    <td>27.15%</td>
                </tr>
                <tr>
                    <td><strong>The Fell</strong></td>
                    <td>£772.29</td>
                    <td>£3,336.57</td>
                    <td>9.58</td>
                    <td class="metric-value positive">4.32x</td>
                    <td>1,268</td>
                    <td>26.16%</td>
                </tr>
                <tr>
                    <td><strong>Chatsworth Inns</strong></td>
                    <td>£939.07</td>
                    <td>£3,764.62</td>
                    <td>6.87</td>
                    <td class="metric-value positive">4.01x</td>
                    <td>1,547</td>
                    <td>18.75%</td>
                </tr>
                <tr>
                    <td><strong>Pilsley Inn</strong></td>
                    <td>£939.01</td>
                    <td>£3,510.18</td>
                    <td>10.30</td>
                    <td class="metric-value positive">3.74x</td>
                    <td>1,393</td>
                    <td>22.52%</td>
                </tr>
            </tbody>
        </table>

        <!-- Properties Requiring Attention -->
        <h2>Properties Requiring Attention</h2>
        <table>
            <thead>
                <tr>
                    <th>Property</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>Conversions</th>
                    <th>ROAS</th>
                    <th>Issue</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Chatsworth Self Catering</strong></td>
                    <td>£900.02</td>
                    <td>£2,321.00</td>
                    <td>6.00</td>
                    <td class="metric-value warning">2.58x</td>
                    <td>Below target ROAS</td>
                </tr>
                <tr>
                    <td><strong>Locations (Bolton Abbey)</strong></td>
                    <td>£496.44</td>
                    <td>£680.00</td>
                    <td>2.00</td>
                    <td class="metric-value warning">1.37x</td>
                    <td>Poor ROAS, needs review</td>
                </tr>
                <tr>
                    <td><strong>Bolton Abbey Self Catering</strong></td>
                    <td>£175.99</td>
                    <td>£0.00</td>
                    <td>0.00</td>
                    <td class="metric-value negative">0.00x</td>
                    <td>Zero conversions</td>
                </tr>
            </tbody>
        </table>
        <div class="notes">
            <strong>Note:</strong> Bolton Abbey SC requires immediate conversion tracking audit. Chatsworth SC below target ROAS.
        </div>

        <!-- Campaign Type Breakdown -->
        <h2>Campaign Type Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Channel</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>Conversions</th>
                    <th>ROAS</th>
                    <th>Share of Spend</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Performance Max</strong></td>
                    <td>£2,585.01</td>
                    <td>£16,065.68</td>
                    <td>34.17</td>
                    <td class="metric-value positive">6.21x</td>
                    <td>25.6%</td>
                </tr>
                <tr>
                    <td><strong>Search (Hotels)</strong></td>
                    <td>£6,627.91</td>
                    <td>£40,307.21</td>
                    <td>92.41</td>
                    <td class="metric-value positive">6.08x</td>
                    <td>65.5%</td>
                </tr>
                <tr>
                    <td><strong>Search (Self-Catering)</strong></td>
                    <td>£1,076.01</td>
                    <td>£2,321.00</td>
                    <td>6.00</td>
                    <td class="metric-value warning">2.16x</td>
                    <td>10.6%</td>
                </tr>
                <tr>
                    <td><strong>Search (Locations)</strong></td>
                    <td>£1,033.56</td>
                    <td>£3,582.00</td>
                    <td>6.00</td>
                    <td class="metric-value positive">3.47x</td>
                    <td>10.2%</td>
                </tr>
            </tbody>
        </table>

        <!-- Self-Catering Campaigns -->
        <h2>Self-Catering Campaigns - Detailed</h2>
        <table>
            <thead>
                <tr>
                    <th>Campaign</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>Conversions</th>
                    <th>ROAS</th>
                    <th>Clicks</th>
                    <th>CTR</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Chatsworth SC</strong></td>
                    <td>£900.02</td>
                    <td>£2,321.00</td>
                    <td>6.00</td>
                    <td class="metric-value warning">2.58x</td>
                    <td>2,554</td>
                    <td>17.29%</td>
                </tr>
                <tr>
                    <td><strong>Bolton Abbey SC</strong></td>
                    <td>£175.99</td>
                    <td>£0.00</td>
                    <td>0.00</td>
                    <td class="metric-value negative">0.00x</td>
                    <td>235</td>
                    <td>8.92%</td>
                </tr>
            </tbody>
        </table>
        <div class="notes">
            <strong>Bolton Abbey SC:</strong> Zero conversions despite clicks - conversion tracking audit required.<br>
            <strong>Chatsworth SC:</strong> Below target ROAS - review landing pages and targeting.
        </div>

        <!-- The Hide -->
        <h2>The Hide - Separate £2,000 Budget</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Budget</td>
                    <td class="metric-value">£2,000.00</td>
                </tr>
                <tr>
                    <td>Actual Spend</td>
                    <td class="metric-value">£1,923.09</td>
                </tr>
                <tr>
                    <td>Pacing</td>
                    <td class="metric-value positive">96.15%</td>
                </tr>
                <tr>
                    <td>The Hide (current)</td>
                    <td>£1,431.28</td>
                </tr>
                <tr>
                    <td>Highwayman Arms (paused)</td>
                    <td>£491.81</td>
                </tr>
            </tbody>
        </table>
        <div class="notes">
            The Hide launched October 10, 2025 (formerly The Highwayman). Combined spend on track with budget.
        </div>

        <!-- Weddings -->
        <h2>Weddings</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Spend</td>
                    <td class="metric-value">£912.11</td>
                </tr>
                <tr>
                    <td>Revenue</td>
                    <td class="metric-value">£12.00</td>
                </tr>
                <tr>
                    <td>Conversions</td>
                    <td class="metric-value">12.00</td>
                </tr>
                <tr>
                    <td>ROAS</td>
                    <td class="metric-value negative">0.01x</td>
                </tr>
                <tr>
                    <td>Impressions</td>
                    <td class="metric-value">8,947</td>
                </tr>
                <tr>
                    <td>Clicks</td>
                    <td class="metric-value">701</td>
                </tr>
                <tr>
                    <td>CTR</td>
                    <td class="metric-value">7.84%</td>
                </tr>
            </tbody>
        </table>
        <div class="notes">
            <strong>Critical Issue:</strong> Only £12 in tracked revenue from 12 conversions despite £912 spend. This suggests either conversion value tracking is not configured correctly, or conversions are being tracked without revenue attribution. Requires immediate investigation.
        </div>

        <!-- Lismore and The Hall -->
        <h2>Lismore and The Hall</h2>
        <table>
            <thead>
                <tr>
                    <th>Campaign</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>Conversions</th>
                    <th>ROAS</th>
                    <th>Clicks</th>
                    <th>CTR</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Lismore</strong></td>
                    <td>£247.55</td>
                    <td>£0.00</td>
                    <td>0.00</td>
                    <td class="metric-value negative">0.00x</td>
                    <td>198</td>
                    <td>8.33%</td>
                </tr>
                <tr>
                    <td><strong>The Hall</strong></td>
                    <td>£241.34</td>
                    <td>£0.00</td>
                    <td>0.00</td>
                    <td class="metric-value negative">0.00x</td>
                    <td>165</td>
                    <td>4.58%</td>
                </tr>
                <tr style="border-top: 2px solid var(--primary);">
                    <td><strong>Total</strong></td>
                    <td><strong>£488.89</strong></td>
                    <td><strong>£0.00</strong></td>
                    <td><strong>0.00</strong></td>
                    <td class="metric-value negative"><strong>0.00x</strong></td>
                    <td><strong>363</strong></td>
                    <td><strong>6.46%</strong></td>
                </tr>
            </tbody>
        </table>
        <div class="notes">
            <strong>Critical Issue:</strong> Zero conversions and zero revenue from both castle campaigns despite £488.89 combined spend. Lismore has decent CTR (8.33%) indicating ad relevance, but no conversions. Requires immediate conversion tracking audit and review of landing page experience.
        </div>

    </div>
</body>
</html>"""

    return html


def main():
    args = parse_arguments()

    # Generate HTML
    html_content = generate_html(args.month)

    # Determine output file
    if args.output:
        output_file = args.output
    else:
        output_file = f"/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/reports/devonshire-paid-search-{args.month}.html"

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML report generated: {output_file}")
    print(f"\nTo use:")
    print(f"1. Open the file in your browser:")
    print(f"   open {output_file}")
    print(f"2. Take screenshots of individual tables")
    print(f"3. Insert screenshots into Google Slides")
    print(f"\nTip: Use browser zoom to get tables at the right size for slides")


if __name__ == '__main__':
    main()
