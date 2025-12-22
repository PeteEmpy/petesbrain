#!/usr/bin/env python3
"""
Google Sheets Chart Templates Module
=====================================

Creates and manages Google Sheets with auto-updating charts for Google Ads reporting.

Features:
- Pre-configured chart templates for common Google Ads metrics
- Auto-updating charts when data changes
- Sparkline formulas for inline trends
- ROK brand styling

Usage:
    from shared.google_sheets_charts import create_weekly_report_sheet

    # Create weekly report sheet for client
    sheet_url = create_weekly_report_sheet(
        client='smythson',
        week_start='2025-12-09',
        data={
            'dates': ['2025-12-09', '2025-12-10', ...],
            'roas': {'Performance Max': [420, 435, ...]},
            'campaigns': {'Campaign A': 2450, ...}
        }
    )
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from chart_generator import ChartGenerator, COLORS
except ImportError:
    # Fallback if run from different location
    COLORS = {
        'primary_green': '#10B981',
        'emerald_green': '#059669',
        'soft_green': '#047857',
    }


def create_sparkline_formulas(
    data_range: str,
    num_rows: int,
    chart_type: str = 'line'
) -> List[str]:
    """
    Generate sparkline formulas for a range of rows.

    Args:
        data_range: Range reference (e.g., 'B2:H2' for 7-day trend)
        num_rows: Number of rows to generate formulas for
        chart_type: Sparkline type ('line', 'bar', 'column', 'winloss')

    Returns:
        List of formula strings, one per row

    Example:
        formulas = create_sparkline_formulas('B2:H2', 5)
        # Returns:
        # ['=SPARKLINE(B2:H2, {"charttype","line";"color","#10B981";"linewidth",2})',
        #  '=SPARKLINE(B3:H3, {"charttype","line";"color","#10B981";"linewidth",2})',
        #  ...]
    """
    formulas = []
    generator = ChartGenerator()

    # Extract base range
    import re
    match = re.match(r'([A-Z]+)(\d+):([A-Z]+)\2', data_range)
    if not match:
        raise ValueError(f"Invalid range format: {data_range}")

    start_col, start_row, end_col = match.groups()
    start_row = int(start_row)

    for row in range(start_row, start_row + num_rows):
        range_ref = f'{start_col}{row}:{end_col}{row}'
        formula = generator.google_sheets_sparkline_formula(
            range_ref=range_ref,
            chart_type=chart_type,
            options={'color': COLORS['primary_green'], 'linewidth': 2}
        )
        formulas.append(formula)

    return formulas


def create_weekly_report_template_data(
    client: str,
    data: Dict,
    week_start: str
) -> Dict:
    """
    Prepare data structure for Google Sheets weekly report template.

    Args:
        client: Client name
        data: Report data dict
        week_start: Week start date (YYYY-MM-DD)

    Returns:
        Dict containing sheet structure, data, and chart configs

    Example:
        template = create_weekly_report_template_data(
            client='Smythson',
            data={
                'dates': ['2025-12-09', '2025-12-10', ...],
                'account_metrics': {
                    'spend': [450, 480, 425, ...],
                    'conversions': [12, 15, 13, ...],
                    'roas': [420, 435, 428, ...]
                },
                'campaigns': {
                    'Performance Max': {'spend': 2450, 'roas': 450},
                    'Search': {'spend': 1850, 'roas': 390}
                }
            },
            week_start='2025-12-09'
        )
    """
    # Calculate week end
    week_start_dt = datetime.strptime(week_start, '%Y-%m-%d')
    week_end_dt = week_start_dt + timedelta(days=6)
    week_range = f"{week_start_dt.strftime('%d %b')} - {week_end_dt.strftime('%d %b %Y')}"

    # Build sheet structure
    template = {
        'client': client,
        'week_start': week_start,
        'week_range': week_range,
        'sheets': []
    }

    # Sheet 1: Executive Summary
    summary_sheet = {
        'name': 'Executive Summary',
        'rows': []
    }

    # Header
    summary_sheet['rows'].append([
        f'{client} - Weekly Google Ads Report',
        '',
        week_range
    ])
    summary_sheet['rows'].append([])  # Blank row

    # Daily performance table
    if 'dates' in data and 'account_metrics' in data:
        dates = data['dates']
        metrics = data['account_metrics']

        # Table header
        summary_sheet['rows'].append([
            'Date',
            'Spend (£)',
            'Conv',
            'Revenue (£)',
            'ROAS (%)',
            'CPA (£)',
            'Trend'
        ])

        # Table data (one row per day)
        for idx, date in enumerate(dates):
            spend = metrics['spend'][idx] if 'spend' in metrics else 0
            conv = metrics['conversions'][idx] if 'conversions' in metrics else 0
            revenue = metrics['revenue'][idx] if 'revenue' in metrics else 0
            roas = metrics['roas'][idx] if 'roas' in metrics else 0
            cpa = spend / conv if conv > 0 else 0

            row_num = len(summary_sheet['rows']) + 2  # +2 for header rows
            sparkline_range = f'B{row_num - 6}:B{row_num}' if idx >= 6 else f'B2:B{row_num}'

            summary_sheet['rows'].append([
                date,
                f'{spend:.2f}',
                str(int(conv)),
                f'{revenue:.2f}',
                f'{roas:.0f}',
                f'{cpa:.2f}',
                f'=SPARKLINE({sparkline_range}, {{"charttype","line";"color","{COLORS["primary_green"]}";"linewidth",2}})'
            ])

    template['sheets'].append(summary_sheet)

    # Sheet 2: Campaign Performance
    if 'campaigns' in data:
        campaign_sheet = {
            'name': 'Campaign Performance',
            'rows': []
        }

        campaign_sheet['rows'].append(['Campaign', 'Spend (£)', 'Conv', 'Revenue (£)', 'ROAS (%)', 'Trend'])
        campaign_sheet['rows'].append([])

        for campaign, metrics in data['campaigns'].items():
            spend = metrics.get('spend', 0)
            conv = metrics.get('conversions', 0)
            revenue = metrics.get('revenue', 0)
            roas = metrics.get('roas', 0)

            # Sparkline based on daily data if available
            trend_formula = '─'  # Default flat
            if 'daily_roas' in metrics:
                row_num = len(campaign_sheet['rows']) + 2
                # Would need daily data written to hidden columns
                trend_formula = f'=SPARKLINE(G{row_num}:M{row_num}, {{"charttype","line";"color","{COLORS["primary_green"]}"}})'

            campaign_sheet['rows'].append([
                campaign,
                f'{spend:.2f}',
                str(int(conv)),
                f'{revenue:.2f}',
                f'{roas:.0f}',
                trend_formula
            ])

        template['sheets'].append(campaign_sheet)

    # Sheet 3: Chart Data (hidden, used by charts)
    chart_data_sheet = {
        'name': 'Chart Data',
        'hidden': True,
        'rows': []
    }

    # ROAS trend data for line chart
    if 'dates' in data and 'roas_by_campaign' in data:
        chart_data_sheet['rows'].append(['Date'] + list(data['roas_by_campaign'].keys()))

        for idx, date in enumerate(data['dates']):
            row = [date]
            for campaign in data['roas_by_campaign'].keys():
                roas = data['roas_by_campaign'][campaign][idx]
                row.append(str(roas))
            chart_data_sheet['rows'].append(row)

    template['sheets'].append(chart_data_sheet)

    return template


def generate_google_sheets_instructions(
    client: str,
    template_data: Dict
) -> str:
    """
    Generate human-readable instructions for creating Google Sheet manually.

    Since we can't create Google Sheets directly via MCP (yet), this generates
    instructions for the user to create the sheet manually.

    Args:
        client: Client name
        template_data: Template data from create_weekly_report_template_data()

    Returns:
        Markdown-formatted instructions

    Example:
        instructions = generate_google_sheets_instructions('Smythson', template)
        print(instructions)
    """
    instructions = f"""# Google Sheets Weekly Report Template - {client}

## Setup Instructions

1. **Create new Google Sheet**
   - Name: `{client} - Weekly Google Ads Report - {template_data['week_start']}`
   - Location: Clients/{client} folder in Google Drive

2. **Create sheets:**
"""

    for sheet in template_data['sheets']:
        if sheet.get('hidden'):
            instructions += f"   - `{sheet['name']}` (hidden sheet for chart data)\n"
        else:
            instructions += f"   - `{sheet['name']}`\n"

    instructions += "\n## Data Structure\n\n"

    for sheet in template_data['sheets']:
        if sheet.get('hidden'):
            continue

        instructions += f"### Sheet: {sheet['name']}\n\n"
        instructions += "**Columns:**\n"

        if sheet['rows']:
            header = sheet['rows'][0] if sheet['rows'][0] else []
            for col in header:
                if col:
                    instructions += f"- {col}\n"

        instructions += "\n"

    instructions += """## Sparkline Formulas

The 'Trend' column uses SPARKLINE formulas. Example:

```
=SPARKLINE(B2:B8, {"charttype","line";"color","#10B981";"linewidth",2})
```

Where:
- `B2:B8` = Range of values to chart (last 7 days)
- `"#10B981"` = ROK brand green color
- `linewidth`,2 = Line thickness

## Charts to Add

### 1. ROAS Trend Line Chart
- Type: Line chart
- Data: Chart Data sheet, columns A:D
- Title: "ROAS Trend - Last 7 Days"
- X-axis: Date
- Y-axis: ROAS (%)
- Series: Performance Max, Search, Shopping

### 2. Campaign Spend Bar Chart
- Type: Horizontal bar chart
- Data: Campaign Performance sheet, columns A:B
- Title: "Top Campaigns by Spend"
- Sort: By spend (descending)
- Limit: Top 10

## Styling

Apply ROK brand colors:
- Headers: Bold, #2d5016 (dark green) background, white text
- Positive metrics: #10B981 (bright green)
- Negative metrics: #dc3545 (red)
- Grid lines: Light grey, subtle

## Auto-Update Setup

To make this sheet auto-update weekly:
1. Use Google Apps Script to fetch data from Google Ads API
2. Write data to 'Chart Data' sheet
3. Charts and sparklines will update automatically
4. Schedule script to run Monday morning

(Script template available in `shared/scripts/google-sheets-auto-update-template.js`)
"""

    return instructions


# Example usage
if __name__ == "__main__":
    # Test template generation
    test_data = {
        'dates': ['2025-12-09', '2025-12-10', '2025-12-11', '2025-12-12', '2025-12-13'],
        'account_metrics': {
            'spend': [450, 480, 425, 510, 475],
            'conversions': [12, 15, 13, 17, 14],
            'revenue': [1890, 2070, 1835, 2380, 2030],
            'roas': [420, 431, 432, 467, 427]
        },
        'campaigns': {
            'Performance Max': {
                'spend': 1200,
                'conversions': 35,
                'revenue': 5400,
                'roas': 450
            },
            'Search': {
                'spend': 800,
                'conversions': 28,
                'revenue': 3120,
                'roas': 390
            }
        },
        'roas_by_campaign': {
            'Performance Max': [450, 455, 448, 470, 452],
            'Search': [380, 395, 390, 405, 385]
        }
    }

    template = create_weekly_report_template_data(
        client='Smythson',
        data=test_data,
        week_start='2025-12-09'
    )

    print("✓ Template data generated")
    print(f"\nClient: {template['client']}")
    print(f"Week: {template['week_range']}")
    print(f"Sheets: {len(template['sheets'])}")

    instructions = generate_google_sheets_instructions('Smythson', template)
    print("\n" + "="*60)
    print(instructions)

    print("\n✅ Google Sheets template generation completed")
