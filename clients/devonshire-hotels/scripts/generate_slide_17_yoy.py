#!/usr/bin/env python3
"""
Generate Slide 17: Year-over-Year Performance Charts
Pulls data directly from Google Ads API via MCP
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Devonshire account
CUSTOMER_ID = "5898250490"

# Campaign filter (excluding Hide/Highwayman)
CAMPAIGN_FILTER = """
  AND campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND campaign.status IN ('ENABLED', 'PAUSED')
"""

def run_gaql_query(start_date, end_date):
    """Run GAQL query via Google Ads MCP"""
    query = f"""
    SELECT
      segments.month,
      metrics.cost_micros,
      metrics.conversions_by_conversion_date,
      metrics.conversions_value_by_conversion_date,
      metrics.impressions,
      metrics.clicks
    FROM campaign
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
      {CAMPAIGN_FILTER}
    """

    # This would be called via MCP in the actual implementation
    # For now, return structure
    return query

def generate_yoy_data():
    """Generate YoY comparison data for all months"""

    months_2024 = [
        ("2024-01-01", "2024-01-31", "Jan"),
        ("2024-02-01", "2024-02-29", "Feb"),
        ("2024-03-01", "2024-03-31", "Mar"),
        ("2024-04-01", "2024-04-30", "Apr"),
        ("2024-05-01", "2024-05-31", "May"),
        ("2024-06-01", "2024-06-30", "Jun"),
        ("2024-07-01", "2024-07-31", "Jul"),
        ("2024-08-01", "2024-08-31", "Aug"),
        ("2024-09-01", "2024-09-30", "Sep"),
        ("2024-10-01", "2024-10-31", "Oct"),
        ("2024-11-01", "2024-11-30", "Nov"),
        ("2024-12-01", "2024-12-31", "Dec"),
    ]

    months_2025 = [
        ("2025-01-01", "2025-01-31", "Jan"),
        ("2025-02-01", "2025-02-28", "Feb"),
        ("2025-03-01", "2025-03-31", "Mar"),
        ("2025-04-01", "2025-04-30", "Apr"),
        ("2025-05-01", "2025-05-31", "May"),
        ("2025-06-01", "2025-06-30", "Jun"),
        ("2025-07-01", "2025-07-31", "Jul"),
        ("2025-08-01", "2025-08-31", "Aug"),
        ("2025-09-01", "2025-09-30", "Sep"),
        ("2025-10-01", "2025-10-31", "Oct"),
        ("2025-11-01", "2025-11-30", "Nov"),
        ("2025-12-01", "2025-12-31", "Dec"),
    ]

    return months_2024, months_2025

def generate_html_chart(data_2024, data_2025, output_path):
    """Generate HTML with YoY comparison charts"""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devonshire YoY Performance - Slide 17</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --estate-blue: #00333D;
            --stone: #E5E3DB;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: white;
            padding: 40px;
            margin: 0;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            color: var(--estate-blue);
            font-size: 36px;
            margin-bottom: 40px;
            font-weight: bold;
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 40px;
            margin-bottom: 40px;
        }

        .chart-container {
            background: var(--stone);
            padding: 20px;
            border-radius: 8px;
            border: 2px solid var(--estate-blue);
        }

        .chart-title {
            color: var(--estate-blue);
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }

        canvas {
            max-height: 300px;
        }

        .footer-note {
            margin-top: 40px;
            padding: 20px;
            background: var(--stone);
            border-left: 4px solid var(--estate-blue);
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Property Campaign Performance - Year over Year</h1>

        <!-- Percentage Change Charts -->
        <h2 style="color: var(--estate-blue); font-size: 24px; margin-bottom: 20px;">% Change (2024 vs 2025)</h2>
        <div class="chart-grid">
            <div class="chart-container">
                <div class="chart-title">CTR % Change</div>
                <canvas id="ctrPctChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversion Rate % Change</div>
                <canvas id="convRatePctChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversions % Change</div>
                <canvas id="convPctChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversion Value % Change</div>
                <canvas id="convValuePctChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Cost % Change</div>
                <canvas id="costPctChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">ROAS % Change</div>
                <canvas id="roasPctChart"></canvas>
            </div>
        </div>

        <!-- Absolute Values Charts -->
        <h2 style="color: var(--estate-blue); font-size: 24px; margin: 40px 0 20px;">Absolute Values (2024 vs 2025)</h2>
        <div class="chart-grid">
            <div class="chart-container">
                <div class="chart-title">CTR</div>
                <canvas id="ctrAbsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversion Rate</div>
                <canvas id="convRateAbsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversions</div>
                <canvas id="convAbsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Conversion Value</div>
                <canvas id="convValueAbsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Cost</div>
                <canvas id="costAbsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">ROAS</div>
                <canvas id="roasAbsChart"></canvas>
            </div>
        </div>

        <div class="footer-note">
            <strong>Year-over-Year Comparison</strong> - Main Hotel Properties (excluding Castles, Weddings & The Hide)
            <br>All conversions and conversion values use "by conversion time" metrics
        </div>
    </div>

    <script>
        // Chart.js configuration and data will be inserted here
        // This is a template - actual data from Google Ads MCP
    </script>
</body>
</html>"""

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✅ HTML template created: {output_path}")
    print("⚠️  Note: This is a template. Actual data needs to be fetched via Google Ads MCP")
    print("    and Chart.js data inserted into the script section")

if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "Monthly Report Slides"
    output_path = output_dir / "Slide 17 October 25.html"

    print("🔄 Generating Slide 17: Year-over-Year Performance...")
    print(f"📊 Customer ID: {CUSTOMER_ID}")
    print(f"🎯 Campaign Filter: Properties (excluding Hide/Highwayman)")
    print()

    # Generate HTML template
    generate_html_chart({}, {}, output_path)

    print()
    print("📝 Next Steps:")
    print("1. This script needs to be enhanced to:")
    print("   - Call Google Ads MCP for each month of 2024 and 2025")
    print("   - Calculate CTR, Conv Rate, ROAS from raw metrics")
    print("   - Generate Chart.js data arrays")
    print("   - Insert data into HTML template")
    print()
    print("2. For now, use the existing Devonshire Dashboard.app")
    print("3. Future enhancement: Fully automate with MCP data")
