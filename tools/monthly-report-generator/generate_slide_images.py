#!/usr/bin/env python3
"""
Generate slide images for Devonshire Hotels monthly report
Matches September 2025 deck format with Estate Blue and Stone brand colors
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
import numpy as np
from datetime import datetime
import os

# Brand colors
ESTATE_BLUE = '#00333D'
STONE = '#E5E3DB'
WHITE = '#FFFFFF'
GREEN = '#4CAF50'
RED = '#F44336'
DARK_GRAY = '#333333'

# Output directory
OUTPUT_DIR = '/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/reports/october-2025-images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# October 2025 data
DATA = {
    'executive_summary': {
        'total_revenue': 64697.55,
        'overall_roas': 5.82,
        'total_spend': 11112.94,
        'total_conversions': 142.33,
        'impressions': 228733,
        'clicks': 23026,
        'ctr': 10.07
    },
    'hotels_top_performers': [
        # Consolidated figures: Search campaigns + PMax asset groups
        {'rank': 1, 'property': 'Devonshire Arms', 'revenue': 20993.02, 'spend': 2377.90, 'roas': 8.83, 'conversions': 53.67},
        {'rank': 2, 'property': 'Cavendish', 'revenue': 15546.18, 'spend': 2370.33, 'roas': 6.56, 'conversions': 26.75},
        {'rank': 3, 'property': 'Pilsley Inn', 'revenue': 6025.59, 'spend': 945.91, 'roas': 6.37, 'conversions': 12.21},
        {'rank': 4, 'property': 'Beeley Inn', 'revenue': 5050.33, 'spend': 1043.29, 'roas': 4.84, 'conversions': 12.33},
        {'rank': 5, 'property': 'The Fell', 'revenue': 5523.54, 'spend': 1326.87, 'roas': 4.16, 'conversions': 14.67},
    ],
    'pmax_results': [
        # PMax asset group performance (October 2025) - sorted by ROAS
        {'rank': 1, 'property': 'Devonshire Arms', 'revenue': 7424.94, 'spend': 988.57, 'roas': 7.51, 'conversions': 19.08},
        {'rank': 2, 'property': 'Cavendish', 'revenue': 6694.76, 'spend': 1014.98, 'roas': 6.59, 'conversions': 12.0},
        {'rank': 3, 'property': 'Pilsley Inn', 'revenue': 2387.65, 'spend': 6.90, 'roas': 346.04, 'conversions': 1.41},
        {'rank': 4, 'property': 'The Fell', 'revenue': 1220.31, 'spend': 554.57, 'roas': 2.20, 'conversions': 3.42},
        {'rank': 5, 'property': 'Beeley Inn', 'revenue': 0.00, 'spend': 19.99, 'roas': 0.00, 'conversions': 0.0},
    ],
    'search_results': [
        # Search campaign performance (October 2025) - HOTELS ONLY (excludes self-catering & locations)
        {'rank': 1, 'property': 'Devonshire Arms Hotel', 'revenue': 13568.09, 'spend': 1389.34, 'roas': 9.77, 'conversions': 34.58},
        {'rank': 2, 'property': 'The Cavendish Hotel', 'revenue': 8851.42, 'spend': 1355.35, 'roas': 6.53, 'conversions': 14.75},
        {'rank': 3, 'property': 'The Beeley Inn', 'revenue': 5050.33, 'spend': 1023.30, 'roas': 4.94, 'conversions': 12.33},
        {'rank': 4, 'property': 'The Fell', 'revenue': 4303.23, 'spend': 772.29, 'roas': 5.57, 'conversions': 11.25},
        {'rank': 5, 'property': 'Chatsworth Estate Hotels', 'revenue': 3764.62, 'spend': 939.07, 'roas': 4.01, 'conversions': 6.87},
        {'rank': 6, 'property': 'The Pilsley Inn', 'revenue': 3637.94, 'spend': 939.01, 'roas': 3.87, 'conversions': 10.80},
    ],
    'locations': [
        # Location-based Search campaigns (October 2025)
        {'rank': 1, 'campaign': 'Chatsworth Escapes Locations', 'revenue': 3069.26, 'spend': 537.12, 'roas': 5.71, 'conversions': 4.83},
        {'rank': 2, 'campaign': 'Bolton Abbey Escapes Locations', 'revenue': 680.00, 'spend': 496.44, 'roas': 1.37, 'conversions': 2.00},
    ],
    'self_catering': [
        # Chatsworth Escapes Self Catering campaign
        {'ad_group': 'Chatsworth Estate Cottages', 'impressions': 4185, 'clicks': 1101, 'ctr': 26.31, 'spend': 314, 'revenue': 1195, 'roas': 3.80},
        {'ad_group': 'Chatsworth Self Catering', 'impressions': 3152, 'clicks': 587, 'ctr': 18.62, 'spend': 220, 'revenue': 1569, 'roas': 7.12},
        {'ad_group': 'Peak District Cottages', 'impressions': 4928, 'clicks': 278, 'ctr': 5.64, 'spend': 232, 'revenue': 374, 'roas': 1.62},
        {'ad_group': 'Shepherds Huts', 'impressions': 1233, 'clicks': 240, 'ctr': 19.46, 'spend': 72, 'revenue': 0, 'roas': 0.00},
        {'ad_group': 'Hunting Tower', 'impressions': 1171, 'clicks': 322, 'ctr': 27.50, 'spend': 55, 'revenue': 326, 'roas': 5.96},
        {'ad_group': 'Russian Cottage', 'impressions': 104, 'clicks': 26, 'ctr': 25.00, 'spend': 8, 'revenue': 0, 'roas': 0.00},
        # Bolton Abbey Escapes Self Catering campaign
        {'ad_group': 'Yorkshire Cottages', 'impressions': 2636, 'clicks': 235, 'ctr': 8.92, 'spend': 176, 'revenue': 581, 'roas': 3.30},
    ],
    'the_hide': [
        {'campaign': 'The Hide', 'impressions': 15355, 'clicks': 2709, 'ctr': 17.64, 'spend': 1460, 'revenue': 1176, 'roas': 0.81, 'conversions': 3.00},
        {'campaign': 'Highwayman Arms', 'impressions': 6751, 'clicks': 571, 'ctr': 8.46, 'spend': 492, 'revenue': 1340, 'roas': 2.72, 'conversions': 8.67},
    ],
    'weddings': [
        {'ad_group': 'Luxury Wedding', 'impressions': 2305, 'clicks': 186, 'ctr': 8.07, 'spend': 283, 'revenue': 5, 'roas': 0.02, 'conversions': 5.00},
        {'ad_group': 'Wedding', 'impressions': 2495, 'clicks': 234, 'ctr': 9.38, 'spend': 276, 'revenue': 2, 'roas': 0.01, 'conversions': 2.00},
        {'ad_group': 'Getting Married', 'impressions': 2374, 'clicks': 179, 'ctr': 7.54, 'spend': 212, 'revenue': 3, 'roas': 0.01, 'conversions': 3.00},
        {'ad_group': 'Wedding Venues', 'impressions': 1285, 'clicks': 82, 'ctr': 6.38, 'spend': 110, 'revenue': 2, 'roas': 0.02, 'conversions': 2.00},
        {'ad_group': 'Countryside Wedding', 'impressions': 200, 'clicks': 12, 'ctr': 6.00, 'spend': 16, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
        {'ad_group': 'Wedding Hotels', 'impressions': 104, 'clicks': 3, 'ctr': 2.88, 'spend': 8, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
        {'ad_group': 'Wedding Packages', 'impressions': 139, 'clicks': 3, 'ctr': 2.16, 'spend': 4, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
        {'ad_group': 'Weddings Yorkshire', 'impressions': 34, 'clicks': 1, 'ctr': 2.94, 'spend': 1, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
    ],
    'lismore_hall': [
        # Lismore campaigns
        {'campaign': 'Lismore', 'ad_group': 'Lismore Castle', 'impressions': 2376, 'clicks': 198, 'ctr': 8.33, 'spend': 248, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
        # The Hall campaigns
        {'campaign': 'The Hall', 'ad_group': 'Search - The Hall', 'impressions': 1960, 'clicks': 103, 'ctr': 5.26, 'spend': 147, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
        {'campaign': 'The Hall', 'ad_group': 'Search - Mansion Rental', 'impressions': 1644, 'clicks': 62, 'ctr': 3.77, 'spend': 95, 'revenue': 0, 'roas': 0.00, 'conversions': 0.00},
    ]
}


def create_metric_boxes(title, output_file):
    """Create Oct vs Sept comparison boxes (Page 16 style from September deck)"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # September 2025 data (actual September data from Google Ads API)
    sept_revenue = 82555.55
    sept_roas = 8.58
    sept_spend = 9626.74
    sept_conversions = 152.50
    sept_impressions = 6667  # Estimated daily average
    sept_ctr = 10.79

    # October data
    oct_revenue = 64698
    oct_roas = 5.82
    oct_spend = 11113
    oct_conversions = 142.33
    oct_impressions = 7378  # Daily average: 228733/31
    oct_ctr = 10.07

    # Calculate changes
    revenue_change = ((oct_revenue - sept_revenue) / sept_revenue) * 100
    roas_change = ((oct_roas - sept_roas) / sept_roas) * 100
    spend_change = ((oct_spend - sept_spend) / sept_spend) * 100
    conv_change = ((oct_conversions - sept_conversions) / sept_conversions) * 100
    imp_change = ((oct_impressions - sept_impressions) / sept_impressions) * 100
    ctr_change = ((oct_ctr - sept_ctr) / sept_ctr) * 100

    # Revenue box
    revenue_box = mpatches.FancyBboxPatch((0.1, 1.2), 0.8, 0.6,
                                          boxstyle="round,pad=0.02",
                                          edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(revenue_box)
    ax.text(0.5, 1.7, f'£{oct_revenue:,}', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(0.5, 1.5, 'Total Revenue', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if revenue_change < 0 else '↑'
    change_color = RED if revenue_change < 0 else GREEN
    ax.text(0.5, 1.35, f'{arrow} {abs(revenue_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(0.5, 1.24, f'vs Sept: £{sept_revenue:,}', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # ROAS box
    roas_box = mpatches.FancyBboxPatch((1.1, 1.2), 0.8, 0.6,
                                       boxstyle="round,pad=0.02",
                                       edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(roas_box)
    ax.text(1.5, 1.7, f'{oct_roas:.2f}x', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(1.5, 1.5, 'Overall ROAS', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if roas_change < 0 else '↑'
    change_color = RED if roas_change < 0 else GREEN
    ax.text(1.5, 1.35, f'{arrow} {abs(roas_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(1.5, 1.24, f'vs Sept: {sept_roas:.2f}x', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # Spend box
    spend_box = mpatches.FancyBboxPatch((2.1, 1.2), 0.8, 0.6,
                                        boxstyle="round,pad=0.02",
                                        edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(spend_box)
    ax.text(2.5, 1.7, f'£{oct_spend:,}', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(2.5, 1.5, 'Total Spend', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if spend_change < 0 else '↑'
    change_color = GREEN if spend_change < 0 else RED  # Lower spend is good
    ax.text(2.5, 1.35, f'{arrow} {abs(spend_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(2.5, 1.24, f'vs Sept: £{sept_spend:,}', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # Bookings box
    conv_box = mpatches.FancyBboxPatch((0.1, 0.4), 0.8, 0.6,
                                       boxstyle="round,pad=0.02",
                                       edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(conv_box)
    ax.text(0.5, 0.9, f'{oct_conversions:.1f}', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(0.5, 0.7, 'Total Bookings', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if conv_change < 0 else '↑'
    change_color = RED if conv_change < 0 else GREEN
    ax.text(0.5, 0.55, f'{arrow} {abs(conv_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(0.5, 0.44, f'vs Sept: {sept_conversions:.1f}', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # Impressions box
    imp_box = mpatches.FancyBboxPatch((1.1, 0.4), 0.8, 0.6,
                                      boxstyle="round,pad=0.02",
                                      edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(imp_box)
    ax.text(1.5, 0.9, f'{oct_impressions:,}', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(1.5, 0.7, 'Daily Impressions', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if imp_change < 0 else '↑'
    change_color = RED if imp_change < 0 else GREEN
    ax.text(1.5, 0.55, f'{arrow} {abs(imp_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(1.5, 0.44, f'vs Sept: {sept_impressions:,}', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # CTR box
    ctr_box = mpatches.FancyBboxPatch((2.1, 0.4), 0.8, 0.6,
                                      boxstyle="round,pad=0.02",
                                      edgecolor=STONE, facecolor=WHITE, linewidth=2)
    ax.add_patch(ctr_box)
    ax.text(2.5, 0.9, f'{oct_ctr:.2f}%', fontsize=32, weight='bold', color=ESTATE_BLUE, ha='center')
    ax.text(2.5, 0.7, 'Overall CTR', fontsize=14, color=DARK_GRAY, ha='center')
    arrow = '↓' if ctr_change < 0 else '↑'
    change_color = RED if ctr_change < 0 else GREEN
    ax.text(2.5, 0.55, f'{arrow} {abs(ctr_change):.1f}%', fontsize=16, weight='bold', color=change_color, ha='center')
    ax.text(2.5, 0.44, f'vs Sept: {sept_ctr:.2f}%', fontsize=9, color=DARK_GRAY, ha='center', style='italic')

    # Add footnote explaining data sources
    footnote_text = ("Data: Hotels (Devonshire Arms, Cavendish, Pilsley Inn, Beeley Inn, The Fell), PMax All, Location campaigns, Self-catering\n"
                    "Excludes: Weddings, Lismore, The Hall, The Hide, Highwayman | Date range: October 1-31, 2025")
    ax.text(1.5, 0.08, footnote_text,
            fontsize=8,
            color='#666666',
            ha='center',
            va='bottom',
            style='italic')

    plt.title(title, fontsize=20, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_hotel_table(title, data, output_file):
    """Create individual hotels breakdown table (Page 20 style)"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')

    # Table data
    headers = ['Rank', 'Property', 'Total Revenue', 'Total Spend', 'Avg ROAS', 'Total Bookings']
    rows = []
    for item in data:
        rows.append([
            item['rank'],
            item['property'],
            f"£{item['revenue']:,.0f}",
            f"£{item['spend']:,.0f}",
            f"{item['roas']:.2f}x",
            f"{item['conversions']:.1f}"
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='center',
                     colWidths=[0.08, 0.35, 0.18, 0.15, 0.12, 0.12])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | Metrics: conversions_by_conversion_date"
    plt.figtext(0.5, 0.02, footnote_text, ha='center', fontsize=8, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_profitability_chart(title, data, output_file):
    """Create profitability bar chart (Page 22 style)"""
    fig, ax = plt.subplots(figsize=(12, 7))

    properties = [item['property'] for item in data]
    roas_values = [item['roas'] for item in data]

    # Create Estate Blue gradient (lighten from left to right)
    n_bars = len(properties)
    colors = []
    for i in range(n_bars):
        # Lighten Estate Blue progressively (0 = darkest, n-1 = lightest)
        # Mix Estate Blue with white in increasing proportions
        ratio = i / (n_bars - 1) if n_bars > 1 else 0
        # Estate Blue: #00333D (RGB: 0, 51, 61)
        r = int(0 + (255 - 0) * ratio * 0.5)  # Lighten towards white
        g = int(51 + (255 - 51) * ratio * 0.5)
        b = int(61 + (255 - 61) * ratio * 0.5)
        colors.append(f'#{r:02x}{g:02x}{b:02x}')

    bars = ax.bar(properties, roas_values, color=colors, edgecolor=ESTATE_BLUE, linewidth=1.5)

    ax.set_ylabel('Combined ROAS', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    ax.set_ylim(0, max(roas_values) * 1.2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Rotate x labels
    plt.xticks(rotation=45, ha='right')

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | Combined PMax + Search ROAS by property"
    plt.figtext(0.5, 0.02, footnote_text, ha='center', fontsize=8, color='#666666', style='italic')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_location_table(title, data, output_file):
    """Create location campaigns table (Page 23 style)"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Rank', 'Campaign', 'Revenue', 'Spend', 'ROAS', 'Bookings', 'Impressions', 'Clicks', 'CTR']
    rows = []
    for item in data:
        rows.append([
            item['rank'],
            item['campaign'],
            f"£{item['revenue']:,}",
            f"£{item['spend']}",
            f"{item['roas']:.2f}x",
            f"{item['conversions']:.1f}",
            '—',  # Not in dataset
            '—',
            '—'
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='center',
                     colWidths=[0.06, 0.35, 0.12, 0.10, 0.08, 0.12, 0.12, 0.08, 0.08])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.8)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | Bolton Abbey & Chatsworth Escapes location-based campaigns | Metrics: conversions_by_conversion_date"
    plt.figtext(0.5, 0.02, footnote_text, ha='center', fontsize=8, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_self_catering_table(title, data, output_file):
    """Create self-catering table (Page 25 style)"""
    fig, ax = plt.subplots(figsize=(14, 8))  # Increased height for 7 ad groups
    ax.axis('tight')
    ax.axis('off')

    headers = ['Ad Group', 'Impressions', 'Clicks', 'CTR', 'Spend', 'Revenue', 'ROAS']
    rows = []
    for item in data:
        rows.append([
            item['ad_group'],
            f"{item['impressions']:,}",
            f"{item['clicks']:,}",
            f"{item['ctr']:.2f}%",
            f"£{item['spend']}",
            f"£{item['revenue']:,}" if item['revenue'] > 0 else '£0',
            f"{item['roas']:.2f}x" if item['roas'] > 0 else '0.00x'
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='center',
                     colWidths=[0.28, 0.13, 0.10, 0.08, 0.12, 0.12, 0.10])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add footnote
    footnote_text = ("Data: October 1-31, 2025 | Ad groups from Chatsworth Escapes Self Catering and Bolton Abbey Escapes Self Catering campaigns\n"
                    "Includes all 7 active ad groups: Chatsworth Estate Cottages, Chatsworth Self Catering, Peak District Cottages, Shepherds Huts, Hunting Tower, Russian Cottage, Yorkshire Cottages")
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=7, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_the_hide_table(title, data, output_file):
    """Create The Hide table (Page 25 style - formerly Highwayman)"""
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Campaign', 'Impressions', 'Clicks', 'CTR', 'Spend', 'Revenue', 'ROAS', 'Bookings']
    rows = []
    for item in data:
        rows.append([
            item['campaign'],
            f"{item['impressions']:,}",
            f"{item['clicks']:,}",
            f"{item['ctr']:.2f}%",
            f"£{item['spend']:,}",
            f"£{item['revenue']:,}",
            f"{item['roas']:.2f}x",
            f"{item['conversions']:.2f}"
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='upper center',
                     colWidths=[0.22, 0.13, 0.10, 0.08, 0.12, 0.12, 0.10, 0.13],
                     bbox=[0, 0.35, 1, 0.65])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.8)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add note about tracking below the table
    note_text = ("Note: The Hide launched 10th October. Conversion tracking setup is being investigated.\n"
                 "Tracked performance may not reflect actual bookings.")
    ax.text(0.5, 0.15, note_text,
            transform=ax.transAxes,
            fontsize=10,
            color=DARK_GRAY,
            ha='center',
            va='center',
            style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF9E6', edgecolor='#E0E0E0', linewidth=1))

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | The Hide campaign (launched Oct 10) + Highwayman Arms campaign | Metrics: conversions_by_conversion_date"
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=7, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_weddings_table(title, data, output_file):
    """Create Weddings table (Page 26 style from September deck)"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Ad Group', 'Impressions', 'Clicks', 'CTR', 'Spend', 'Revenue', 'ROAS', 'Bookings']
    rows = []
    for item in data:
        rows.append([
            item['ad_group'],
            f"{item['impressions']:,}",
            f"{item['clicks']:,}",
            f"{item['ctr']:.2f}%",
            f"£{item['spend']:,}",
            f"£{item['revenue']:,}",
            f"{item['roas']:.2f}x",
            f"{item['conversions']:.2f}"
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='center',
                     colWidths=[0.22, 0.13, 0.10, 0.08, 0.12, 0.12, 0.10, 0.13])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.2)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | Chatsworth Weddings campaign | 8 ad groups (Luxury Wedding, Wedding, Getting Married, Wedding Venues, Countryside Wedding, Wedding Hotels, Wedding Packages, Weddings Yorkshire)"
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=7, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_lismore_hall_table(title, data, output_file):
    """Create Lismore and The Hall table (Page 27 style from September deck)"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Campaign', 'Ad Group', 'Impressions', 'Clicks', 'CTR', 'Spend', 'Revenue', 'ROAS', 'Bookings']
    rows = []
    for item in data:
        rows.append([
            item['campaign'],
            item['ad_group'],
            f"{item['impressions']:,}",
            f"{item['clicks']:,}",
            f"{item['ctr']:.2f}%",
            f"£{item['spend']:,}",
            f"£{item['revenue']:,}",
            f"{item['roas']:.2f}x",
            f"{item['conversions']:.2f}"
        ])

    table = ax.table(cellText=rows, colLabels=headers, cellLoc='left', loc='center',
                     colWidths=[0.14, 0.20, 0.12, 0.09, 0.08, 0.11, 0.11, 0.08, 0.11])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.8)

    # Style headers
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(ESTATE_BLUE)
        cell.set_text_props(weight='bold', color=WHITE)

    # Style data rows
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(STONE)
            cell.set_edgecolor('#CCCCCC')

    # Add footnote
    footnote_text = "Data: October 1-31, 2025 | Lismore campaign (1 ad group) + The Hall campaign (2 ad groups: Search - The Hall, Search - Mansion Rental)"
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=7, color='#666666', style='italic')

    plt.title(title, fontsize=16, weight='bold', color=ESTATE_BLUE, pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_hide_highwayman_trends(title, output_file):
    """Create Hide/Highwayman trends charts (3 across each row)"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from datetime import datetime

    # Historical data from Jan-Oct 2025
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    clicks = [2502, 2095, 2200, 1637, 1116, 1095, 1128, 972, 964, 3280]
    ctr = [20.44, 18.00, 14.03, 14.08, 11.67, 8.82, 9.33, 13.13, 11.99, 14.84]
    roas = [1.50, 2.08, 1.88, 1.55, 2.40, 3.00, 2.84, 1.05, 3.37, 1.29]
    conversions = [14.00, 28.00, 33.00, 18.00, 11.00, 16.00, 13.50, 4.40, 14.50, 11.67]
    conv_rate = [0.56, 1.34, 1.50, 1.10, 0.99, 1.46, 1.20, 0.45, 1.50, 0.36]
    spend = [2203.02, 2465.77, 2734.18, 1796.46, 1173.10, 1046.20, 1275.47, 713.24, 833.35, 1951.73]

    # The Hide launched in October (month index 9)
    hide_launch_index = 9

    fig = plt.figure(figsize=(14, 8))

    # Create 6 subplots: 3 on top row, 3 on bottom row
    # Top row
    ax1 = plt.subplot(2, 3, 1)  # Clicks
    ax2 = plt.subplot(2, 3, 2)  # CTR
    ax3 = plt.subplot(2, 3, 3)  # ROAS
    # Bottom row
    ax4 = plt.subplot(2, 3, 4)  # Conversions
    ax5 = plt.subplot(2, 3, 5)  # Conversion Rate
    ax6 = plt.subplot(2, 3, 6)  # Spend

    axes = [
        (ax1, clicks, 'Clicks', 'Clicks', False, False),
        (ax2, ctr, 'CTR (%)', 'CTR', True, False),
        (ax3, roas, 'ROAS', 'ROAS (x)', False, False),
        (ax4, conversions, 'Bookings', 'Bookings', False, False),
        (ax5, conv_rate, 'Conversion Rate (%)', 'Conv. Rate', True, False),
        (ax6, spend, 'Spend (£)', 'Spend', False, True)
    ]

    for ax, data, ylabel, chart_title, is_percentage, is_currency in axes:
        # Plot line
        ax.plot(range(len(months)), data, color=ESTATE_BLUE, linewidth=2.5, marker='o', markersize=6)

        # Add vertical line at Hide launch (October)
        ax.axvline(x=hide_launch_index, color='#FF6B6B', linestyle='--', linewidth=2, alpha=0.7, label='Hide Launch')

        # Styling
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(months, fontsize=9)
        ax.set_ylabel(ylabel, fontsize=10, color=DARK_GRAY)
        ax.set_title(chart_title, fontsize=12, weight='bold', color=ESTATE_BLUE, pad=10)
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CCCCCC')
        ax.spines['bottom'].set_color('#CCCCCC')

        # Format y-axis
        if is_percentage:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}%'))
        elif chart_title == 'ROAS':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}x'))
        elif is_currency:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'£{y:,.0f}'))
        else:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y):,}'))

    # Add overall title
    fig.suptitle(title, fontsize=16, weight='bold', color=ESTATE_BLUE, y=0.98)

    # Add legend for Hide launch line (only once, in top right chart)
    ax3.legend(loc='upper right', fontsize=9, framealpha=0.9)

    # Add footnote
    footnote_text = ("Data: January-October 2025 (monthly) | Consolidated performance for The Hide + Highwayman Arms campaigns\n"
                    "Red dashed line marks The Hide launch (October 10, 2025) | Metrics: conversions_by_conversion_date")
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=7, color='#666666', style='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


def create_yoy_comparison(title, output_file):
    """Create year-over-year comparison charts (6 metrics in 2x3 grid)"""

    # October 2024 data
    oct_2024_spend = 1388.83
    oct_2024_revenue = 4639.50
    oct_2024_roas = 3.34
    oct_2024_conversions = 12.0
    oct_2024_daily_impressions = 6692
    oct_2024_ctr = 1.52

    # October 2025 data
    oct_2025_spend = 11113
    oct_2025_revenue = 64698
    oct_2025_roas = 5.82
    oct_2025_conversions = 142.33
    oct_2025_daily_impressions = 7378
    oct_2025_ctr = 10.07

    # Calculate YoY changes
    spend_change = ((oct_2025_spend - oct_2024_spend) / oct_2024_spend) * 100
    revenue_change = ((oct_2025_revenue - oct_2024_revenue) / oct_2024_revenue) * 100
    roas_change = ((oct_2025_roas - oct_2024_roas) / oct_2024_roas) * 100
    conv_change = ((oct_2025_conversions - oct_2024_conversions) / oct_2024_conversions) * 100
    imp_change = ((oct_2025_daily_impressions - oct_2024_daily_impressions) / oct_2024_daily_impressions) * 100
    ctr_change = ((oct_2025_ctr - oct_2024_ctr) / oct_2024_ctr) * 100

    # Create 2x3 grid
    fig = plt.figure(figsize=(16, 10))

    # Define 6 charts with their data
    charts = [
        ('Daily Impressions', [oct_2024_daily_impressions, oct_2025_daily_impressions], imp_change, False, False),
        ('CTR', [oct_2024_ctr, oct_2025_ctr], ctr_change, True, False),
        ('Spend', [oct_2024_spend, oct_2025_spend], spend_change, False, True),
        ('Revenue', [oct_2024_revenue, oct_2025_revenue], revenue_change, False, True),
        ('ROAS', [oct_2024_roas, oct_2025_roas], roas_change, False, False),
        ('Conversions', [oct_2024_conversions, oct_2025_conversions], conv_change, False, False),
    ]

    for idx, (metric_name, values, yoy_change, is_percentage, is_currency) in enumerate(charts, 1):
        ax = plt.subplot(2, 3, idx)

        # Bar chart
        years = ['Oct 2024', 'Oct 2025']
        bars = ax.bar(years, values, color=[ESTATE_BLUE, '#4A9EBE'], edgecolor=ESTATE_BLUE, linewidth=1.5, width=0.5)

        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            if is_percentage:
                label_text = f'{val:.2f}%'
            elif is_currency:
                label_text = f'£{val:,.0f}'
            elif metric_name == 'ROAS':
                label_text = f'{val:.2f}x'
            elif metric_name == 'Conversions':
                label_text = f'{val:.1f}'
            else:
                label_text = f'{int(val):,}'

            ax.text(bar.get_x() + bar.get_width()/2., height,
                   label_text,
                   ha='center', va='bottom', fontsize=11, weight='bold', color=ESTATE_BLUE)

        # Add YoY change annotation
        arrow = '↑' if yoy_change > 0 else '↓'
        change_color = GREEN if yoy_change > 0 else RED
        ax.text(0.5, 0.95, f'{arrow} {abs(yoy_change):.1f}% YoY',
               transform=ax.transAxes,
               ha='center', va='top',
               fontsize=13, weight='bold', color=change_color,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=change_color, linewidth=2))

        # Styling
        ax.set_title(metric_name, fontsize=14, weight='bold', color=ESTATE_BLUE, pad=15)
        ax.set_ylim(0, max(values) * 1.25)
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CCCCCC')
        ax.spines['bottom'].set_color('#CCCCCC')

        # Format y-axis
        if is_percentage:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}%'))
        elif metric_name == 'ROAS':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}x'))
        elif is_currency:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'£{y:,.0f}'))
        elif metric_name == 'Conversions':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}'))
        else:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y):,}'))

    # Add overall title
    fig.suptitle(title, fontsize=18, weight='bold', color=ESTATE_BLUE, y=0.98)

    # Add footnote
    footnote_text = ("Data: Core hotel properties only (excludes self-catering, weddings, specialty properties)\n"
                    "Oct 2024: £1,389 spend, £4,640 revenue | Oct 2025: £11,113 spend, £64,698 revenue | Metrics: conversions_by_conversion_date")
    plt.figtext(0.5, 0.01, footnote_text, ha='center', fontsize=8, color='#666666', style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_file}")


# Generate all images
if __name__ == '__main__':
    print("Generating October 2025 slide images...")

    # Page 16 style - Metric boxes
    create_metric_boxes(
        'Core Hotel Properties - October 2025',
        os.path.join(OUTPUT_DIR, '01-metric-boxes.png')
    )

    # Page 20 style - Hotels breakdown
    create_hotel_table(
        'Hotels - Individual Property Performance',
        DATA['hotels_top_performers'],
        os.path.join(OUTPUT_DIR, '02-hotels-breakdown.png')
    )

    # Page 21 style - Performance Max table
    create_hotel_table(
        'Performance Max Campaign Results',
        DATA['pmax_results'],
        os.path.join(OUTPUT_DIR, '03-pmax-results.png')
    )

    # Page 21 style - Search Campaign table
    create_hotel_table(
        'Search Campaign Results',
        DATA['search_results'],
        os.path.join(OUTPUT_DIR, '04-search-results.png')
    )

    # Page 22 style - Profitability chart
    create_profitability_chart(
        'Hotels - Overall Profitability',
        DATA['hotels_top_performers'],
        os.path.join(OUTPUT_DIR, '05-profitability-chart.png')
    )

    # Page 23 style - Location campaigns
    create_location_table(
        'Location Based Search Campaigns',
        DATA['locations'],
        os.path.join(OUTPUT_DIR, '06-locations-table.png')
    )

    # Page 25 style - Self-catering
    create_self_catering_table(
        'Self Catering Campaign Performance',
        DATA['self_catering'],
        os.path.join(OUTPUT_DIR, '07-self-catering-table.png')
    )

    # Page 25 style - The Hide (formerly Highwayman)
    create_the_hide_table(
        'The Hide / Highwayman',
        DATA['the_hide'],
        os.path.join(OUTPUT_DIR, '08-the-hide-table.png')
    )

    # Hide/Highwayman Trends (Jan-Oct 2025)
    create_hide_highwayman_trends(
        'The Hide & Highwayman Arms - Performance Trends (Jan-Oct 2025)',
        os.path.join(OUTPUT_DIR, '08a-hide-highwayman-trends.png')
    )

    # Page 26 style - Weddings
    create_weddings_table(
        'Weddings',
        DATA['weddings'],
        os.path.join(OUTPUT_DIR, '09-weddings-table.png')
    )

    # Page 27 style - Lismore and The Hall
    create_lismore_hall_table(
        'Lismore and The Hall',
        DATA['lismore_hall'],
        os.path.join(OUTPUT_DIR, '10-lismore-hall-table.png')
    )

    # NEW: Year-over-Year Comparison (Slide 17 style)
    create_yoy_comparison(
        'Year-over-Year Performance (October 2024 vs October 2025)',
        os.path.join(OUTPUT_DIR, '11-yoy-comparison.png')
    )

    print(f"\nAll images saved to: {OUTPUT_DIR}")
    print("Ready to insert into Google Slides!")
