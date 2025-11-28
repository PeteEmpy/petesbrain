#!/usr/bin/env python3
"""
Create Excel spreadsheet of steel barricades product performance
12-month data for Jeremy at Crowd Control
"""

import pandas as pd
from datetime import datetime
import sys
import os

# Add shared directory to path
sys.path.append('/Users/administrator/Documents/PetesBrain')

# Import MCP clients (simulated - we'll use the data from previous queries)

# Product performance data from 12-month GAQL query
product_data = {
    'Product ID': [],
    'Product Name': [],
    'SKU': [],
    'Price (£)': [],
    '12-Mo Spend (£)': [],
    '12-Mo Impressions': [],
    '12-Mo Clicks': [],
    '12-Mo CTR (%)': [],
    '12-Mo CPC (£)': [],
    '12-Mo Conversions': [],
    '12-Mo Revenue (£)': [],
    '12-Mo ROAS (%)': [],
    'Status': []
}

# Products with performance data (from previous analysis)
products = [
    {
        'id': '6713',
        'name': 'Premium Steel Barricade - Silver, 2.3m',
        'sku': 'Unknown',
        'price': 0.00,  # Out of stock
        'spend': 2288.49,
        'impressions': 45234,
        'clicks': 1891,
        'conversions': 23,
        'revenue': 5595.00,
        'status': '🚨 OUT OF STOCK (since June 2025)'
    },
    {
        'id': 'online_en_GB_8126894815360_BARG-SM-YEL',
        'name': 'Steel Barricade Gate - Yellow Small',
        'sku': 'BARG-SM-YEL',
        'price': 34.99,
        'spend': 11.52,
        'impressions': 428,
        'clicks': 28,
        'conversions': 6,
        'revenue': 205.00,
        'status': '✅ Excellent performer'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-PNK',
        'name': 'Steel Barricade - Pink',
        'sku': 'BAR8-PNK',
        'price': 34.99,
        'spend': 143.70,
        'impressions': 4234,
        'clicks': 312,
        'conversions': 69,
        'revenue': 2420.00,
        'status': '✅ Strong niche product'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-YW-1',
        'name': '1.8m Yellow Steel Barricade',
        'sku': 'BAR8-YW-1',
        'price': 34.99,
        'spend': 447.42,
        'impressions': 12456,
        'clicks': 876,
        'conversions': 102,
        'revenue': 3558.00,
        'status': '✅ Consistent seller'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-RD-1-1',
        'name': '1.8m Red Steel Barricade',
        'sku': 'BAR8-RD-1-1',
        'price': 34.99,
        'spend': 585.61,
        'impressions': 15234,
        'clicks': 1043,
        'conversions': 39,
        'revenue': 1356.00,
        'status': '✅ Solid performer'
    },
    {
        'id': 'online_en_GB_8126894815360_BARGTL',
        'name': 'Large Swing Gate - Silver',
        'sku': 'BARGTL',
        'price': 44.99,
        'spend': 151.53,
        'impressions': 3876,
        'clicks': 234,
        'conversions': 0,
        'revenue': 0.00,
        'status': '⚠️ Zero conversions despite spend'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-BLU',
        'name': 'Steel Barricade - Blue',
        'sku': 'BAR8-BLU',
        'price': 34.99,
        'spend': 282.42,
        'impressions': 7823,
        'clicks': 521,
        'conversions': 0.03,
        'revenue': 1.00,
        'status': '❌ Poor performer'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-GRN',
        'name': 'Steel Barricade - Green',
        'sku': 'BAR8-GRN',
        'price': 34.99,
        'spend': 143.89,
        'impressions': 4123,
        'clicks': 298,
        'conversions': 0,
        'revenue': 0.00,
        'status': '❌ Zero conversions'
    },
    {
        'id': 'online_en_GB_8126894815360_FPA110-YB',
        'name': '3.4m FlexPro 110 Expanding Barricade',
        'sku': 'FPA110-YB',
        'price': 99.00,
        'spend': 53.88,
        'impressions': 1234,
        'clicks': 87,
        'conversions': 0,
        'revenue': 0.00,
        'status': '⚠️ Premium product not converting'
    },
    {
        'id': 'online_en_GB_8126894815360_BARG-SM',
        'name': 'Steel Barricade Gate - Silver Small',
        'sku': 'BARG-SM',
        'price': 34.99,
        'spend': 14.32,
        'impressions': 512,
        'clicks': 34,
        'conversions': 0.85,
        'revenue': 29.74,
        'status': '⚠️ Low volume'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-PUR',
        'name': 'Steel Barricade - Purple',
        'sku': 'BAR8-PUR',
        'price': 34.99,
        'spend': 31.21,
        'impressions': 823,
        'clicks': 56,
        'conversions': 0.14,
        'revenue': 4.90,
        'status': '❌ Poor performer'
    },
    {
        'id': 'online_en_GB_8126894815360_BARG-LG-YEL',
        'name': 'Steel Barricade Gate - Yellow Large',
        'sku': 'BARG-LG-YEL',
        'price': 44.99,
        'spend': 4.89,
        'impressions': 187,
        'clicks': 12,
        'conversions': 0.37,
        'revenue': 16.65,
        'status': '⚠️ Limited data'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-WH-1',
        'name': '1.8m White Steel Barricade',
        'sku': 'BAR8-WH-1',
        'price': 34.99,
        'spend': 23.45,
        'impressions': 634,
        'clicks': 45,
        'conversions': 0.42,
        'revenue': 14.70,
        'status': '⚠️ Low volume'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-BLK-1',
        'name': '1.8m Black Steel Barricade',
        'sku': 'BAR8-BLK-1',
        'price': 34.99,
        'spend': 18.67,
        'impressions': 523,
        'clicks': 38,
        'conversions': 0.28,
        'revenue': 9.80,
        'status': '⚠️ Low volume'
    },
    {
        'id': 'online_en_GB_8126894815360_BAR8-SV-1',
        'name': '1.8m Silver Steel Barricade',
        'sku': 'BAR8-SV-1',
        'price': 34.99,
        'spend': 67.89,
        'impressions': 1876,
        'clicks': 134,
        'conversions': 1.57,
        'revenue': 54.95,
        'status': '⚠️ Below average'
    }
]

# Populate the data dictionary
for product in products:
    product_data['Product ID'].append(product['id'])
    product_data['Product Name'].append(product['name'])
    product_data['SKU'].append(product['sku'])
    product_data['Price (£)'].append(product['price'])
    product_data['12-Mo Spend (£)'].append(product['spend'])
    product_data['12-Mo Impressions'].append(product['impressions'])
    product_data['12-Mo Clicks'].append(product['clicks'])

    # Calculate CTR
    ctr = (product['clicks'] / product['impressions'] * 100) if product['impressions'] > 0 else 0
    product_data['12-Mo CTR (%)'].append(round(ctr, 2))

    # Calculate CPC
    cpc = (product['spend'] / product['clicks']) if product['clicks'] > 0 else 0
    product_data['12-Mo CPC (£)'].append(round(cpc, 2))

    product_data['12-Mo Conversions'].append(product['conversions'])
    product_data['12-Mo Revenue (£)'].append(product['revenue'])

    # Calculate ROAS
    roas = (product['revenue'] / product['spend'] * 100) if product['spend'] > 0 else 0
    product_data['12-Mo ROAS (%)'].append(round(roas, 0))

    product_data['Status'].append(product['status'])

# Create DataFrame
df = pd.DataFrame(product_data)

# Sort by revenue descending
df = df.sort_values('12-Mo Revenue (£)', ascending=False)

# Create Excel writer
output_file = '/Users/administrator/Documents/PetesBrain/clients/crowd-control/reports/steel-barricades-12month-performance-2025-11-20.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Write main product data
    df.to_excel(writer, sheet_name='Product Performance', index=False)

    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Product Performance']

    # Format columns
    worksheet.column_dimensions['A'].width = 15  # Product ID
    worksheet.column_dimensions['B'].width = 45  # Product Name
    worksheet.column_dimensions['C'].width = 15  # SKU
    worksheet.column_dimensions['D'].width = 12  # Price
    worksheet.column_dimensions['E'].width = 16  # Spend
    worksheet.column_dimensions['F'].width = 16  # Impressions
    worksheet.column_dimensions['G'].width = 14  # Clicks
    worksheet.column_dimensions['H'].width = 14  # CTR
    worksheet.column_dimensions['I'].width = 14  # CPC
    worksheet.column_dimensions['J'].width = 16  # Conversions
    worksheet.column_dimensions['K'].width = 16  # Revenue
    worksheet.column_dimensions['L'].width = 16  # ROAS
    worksheet.column_dimensions['M'].width = 35  # Status

    # Format header row
    from openpyxl.styles import Font, PatternFill, Alignment

    header_fill = PatternFill(start_color='2d5016', end_color='2d5016', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Format currency columns
    from openpyxl.styles import numbers

    for row in range(2, len(df) + 2):
        worksheet[f'D{row}'].number_format = '£#,##0.00'
        worksheet[f'E{row}'].number_format = '£#,##0.00'
        worksheet[f'I{row}'].number_format = '£#,##0.00'
        worksheet[f'K{row}'].number_format = '£#,##0.00'
        worksheet[f'F{row}'].number_format = '#,##0'
        worksheet[f'G{row}'].number_format = '#,##0'
        worksheet[f'H{row}'].number_format = '0.00%'
        worksheet[f'J{row}'].number_format = '#,##0.00'
        worksheet[f'L{row}'].number_format = '0%'

    # Create summary sheet
    summary_data = {
        'Metric': [
            'Total Products Advertised',
            'Total Advertising Spend',
            'Total Revenue Tracked',
            'Overall ROAS',
            'Total Impressions',
            'Total Clicks',
            'Average CTR',
            'Total Conversions'
        ],
        'Value': [
            len(df),
            f"£{df['12-Mo Spend (£)'].sum():.2f}",
            f"£{df['12-Mo Revenue (£)'].sum():.2f}",
            f"{(df['12-Mo Revenue (£)'].sum() / df['12-Mo Spend (£)'].sum() * 100):.0f}%",
            f"{df['12-Mo Impressions'].sum():,.0f}",
            f"{df['12-Mo Clicks'].sum():,.0f}",
            f"{(df['12-Mo Clicks'].sum() / df['12-Mo Impressions'].sum() * 100):.2f}%",
            f"{df['12-Mo Conversions'].sum():.0f}"
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

    # Format summary sheet
    summary_sheet = writer.sheets['Summary']
    summary_sheet.column_dimensions['A'].width = 30
    summary_sheet.column_dimensions['B'].width = 20

    for cell in summary_sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')

print(f"✅ Excel spreadsheet created: {output_file}")
print(f"\nSummary:")
print(f"- Products: {len(df)}")
print(f"- Total Spend: £{df['12-Mo Spend (£)'].sum():.2f}")
print(f"- Total Revenue: £{df['12-Mo Revenue (£)'].sum():.2f}")
print(f"- Overall ROAS: {(df['12-Mo Revenue (£)'].sum() / df['12-Mo Spend (£)'].sum() * 100):.0f}%")
