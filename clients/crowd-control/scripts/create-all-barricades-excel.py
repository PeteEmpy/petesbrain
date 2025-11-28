#!/usr/bin/env python3
"""
Create Excel spreadsheet of ALL barricades product performance
12-month data for Jeremy at Crowd Control
"""

import pandas as pd
from datetime import datetime
import json

# Google Ads performance data (from GAQL query)
ads_performance = {
    "6735": {"impressions": 308854, "clicks": 2136, "cost": 7040.03, "conversions": 51.59, "revenue": 9663.05},
    "6733": {"impressions": 96500, "clicks": 490, "cost": 2305.27, "conversions": 21.06, "revenue": 5583.50},
    "6713": {"impressions": 139906, "clicks": 1092, "cost": 2285.19, "conversions": 12.00, "revenue": 4711.24},
    "6734": {"impressions": 122000, "clicks": 373, "cost": 1582.53, "conversions": 5.50, "revenue": 1473.00},
    "65432": {"impressions": 62801, "clicks": 226, "cost": 984.72, "conversions": 4.32, "revenue": 1576.42},
    "65447": {"impressions": 45463, "clicks": 152, "cost": 644.09, "conversions": 2.99, "revenue": 577.68},
    "62922": {"impressions": 67314, "clicks": 281, "cost": 611.11, "conversions": 0.08, "revenue": 50.03},
    "62919": {"impressions": 119887, "clicks": 569, "cost": 447.46, "conversions": 4.00, "revenue": 3558.38},
    "67092": {"impressions": 61807, "clicks": 145, "cost": 264.57, "conversions": 0.00, "revenue": 0.00},
    "6724": {"impressions": 97198, "clicks": 206, "cost": 154.11, "conversions": 0.00, "revenue": 0.00},
    "6081": {"impressions": 23916, "clicks": 132, "cost": 147.96, "conversions": 0.00, "revenue": 0.00},
    "67096": {"impressions": 7152, "clicks": 57, "cost": 145.53, "conversions": 1.35, "revenue": 616.77},
    "67094": {"impressions": 27553, "clicks": 105, "cost": 144.28, "conversions": 0.00, "revenue": 0.00},
    "6082": {"impressions": 9358, "clicks": 13, "cost": 54.66, "conversions": 0.00, "revenue": 0.00},
    "67256": {"impressions": 4775, "clicks": 28, "cost": 54.49, "conversions": 0.00, "revenue": 0.00},
    "67098": {"impressions": 4367, "clicks": 28, "cost": 47.85, "conversions": 0.00, "revenue": 0.00},
    "61151": {"impressions": 5791, "clicks": 6, "cost": 46.59, "conversions": 0.00, "revenue": 0.00},
    "67247": {"impressions": 7738, "clicks": 17, "cost": 42.86, "conversions": 0.50, "revenue": 37.20},
    "67251": {"impressions": 6323, "clicks": 16, "cost": 21.64, "conversions": 0.00, "revenue": 0.00},
    "67253": {"impressions": 1585, "clicks": 6, "cost": 11.52, "conversions": 0.00, "revenue": 0.00},
    "6089": {"impressions": 1262, "clicks": 4, "cost": 7.05, "conversions": 0.00, "revenue": 0.00},
    "68257": {"impressions": 102, "clicks": 1, "cost": 4.47, "conversions": 0.00, "revenue": 0.00},
    "8192": {"impressions": 570, "clicks": 2, "cost": 3.65, "conversions": 0.00, "revenue": 0.00},
    "68273": {"impressions": 50, "clicks": 0, "cost": 0.00, "conversions": 0.00, "revenue": 0.00},
    "62947": {"impressions": 80, "clicks": 0, "cost": 0.00, "conversions": 0.00, "revenue": 0.00}
}

# All barricade products from WooCommerce (organized by category)
all_products = [
    # Steel Barricades - Active
    {"id": "62919", "name": "1.8m Yellow Steel Barricade", "sku": "BAR8-YW-1", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "62922", "name": "Steel Barricade In Red – 1.8m", "sku": "BAR8-RD-1-1", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "6713", "name": "Steel Barricade In Silver - 1.8m", "sku": "BAR8-GY", "price": 29.99, "category": "Steel Barricade", "status": "outofstock"},
    {"id": "67092", "name": "Steel Barricade In Blue - 1.8m", "sku": "BAR8-BLU", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "67094", "name": "Steel Barricade In Green - 1.8m", "sku": "BAR8-GRN", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "67096", "name": "Steel Barricade In Pink - 1.8m", "sku": "BAR8-PNK", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "67098", "name": "Steel Barricade In Purple - 1.8m", "sku": "BAR8-PUR", "price": 34.99, "category": "Steel Barricade", "status": "instock"},
    {"id": "62947", "name": "Steel Barricade in Orange - 1.8m", "sku": "BAR8-OR-1-1-1", "price": 34.99, "category": "Steel Barricade", "status": "outofstock"},

    # Steel Barricade Gates
    {"id": "67253", "name": "Steel Barricade Gate In Yellow-Small (0.9m)", "sku": "BARG-SM-YEL", "price": 34.99, "category": "Steel Gate", "status": "instock"},
    {"id": "6081", "name": "Steel Barricade Gate In Silver-Small (0.9m)", "sku": "BARG-SM", "price": 34.99, "category": "Steel Gate", "status": "instock"},
    {"id": "67256", "name": "Steel Barricade Gate In Red-Small (0.9m)", "sku": "BARG-SM-RD", "price": 34.99, "category": "Steel Gate", "status": "instock"},
    {"id": "67247", "name": "Steel Barricade Gate In Yellow-Large (1.8m)", "sku": "BARGTL-YEL", "price": 44.99, "category": "Steel Gate", "status": "instock"},
    {"id": "6724", "name": "Steel Barricade Gate In Silver-Large (1.8m)", "sku": "BARGTL", "price": 44.99, "category": "Steel Gate", "status": "instock"},
    {"id": "67251", "name": "Steel Barricade Gate In Red-Large (1.8m)", "sku": "BARGTL-RD", "price": 44.99, "category": "Steel Gate", "status": "instock"},

    # Expanding Barricades - Metal (FlexPro)
    {"id": "6082", "name": "3.4m FlexPro 110 Expanding Barricade - Yellow", "sku": "FPA110-YB", "price": 99.00, "category": "Expanding - Metal", "status": "instock"},
    {"id": "61151", "name": "3.4m FlexPro 110 Expanding Barricade - Red", "sku": "FPA110-RW", "price": 99.00, "category": "Expanding - Metal", "status": "instock"},
    {"id": "6733", "name": "4.8m FlexPro 160 Expanding Barricade - Yellow", "sku": "FPA160-YB", "price": 145.00, "category": "Expanding - Metal", "status": "instock"},
    {"id": "6734", "name": "4.8m FlexPro 160 Expanding Barricade - Red", "sku": "FPA160-RW", "price": 145.00, "category": "Expanding - Metal", "status": "instock"},

    # Expanding Barricades - Plastic
    {"id": "6735", "name": "3.5m FlexMaster 110 Expanding Barricade - Yellow", "sku": "FM110-YB", "price": 79.00, "category": "Expanding - Plastic", "status": "instock"},
    {"id": "65447", "name": "3.4m Flex Gate Expanding Barricade - Yellow/Black", "sku": "FG10YB", "price": 85.00, "category": "Expanding - Plastic", "status": "instock"},
    {"id": "65432", "name": "3.4m Flex Gate Expanding Barricade - Red/White", "sku": "FG10RW", "price": 85.00, "category": "Expanding - Plastic", "status": "outofstock"},
    {"id": "6736", "name": "2.3m FlexMaster 75 Expanding Barricade - Red", "sku": "FM75-RD", "price": 59.00, "category": "Expanding - Plastic", "status": "outofstock"},
    {"id": "7966", "name": "3.4m Yellow Expandable Mobile Barrier", "sku": "EXP-BARRICADE-MOBILE", "price": 149.00, "category": "Expanding - Plastic", "status": "outofstock"},

    # Post and Panel Barricades
    {"id": "68257", "name": "1.2m Black Post and Panel Barricade Bundle", "sku": "PNL4834B-BUN", "price": 275.00, "category": "Post & Panel", "status": "instock"},
    {"id": "68273", "name": "1.2m Satin Stainless Post and Panel Bundle", "sku": "PNL4834SS-BUN", "price": 285.00, "category": "Post & Panel", "status": "instock"},
    {"id": "68421", "name": "1.8m Black Post and Panel Barricade Bundle", "sku": "PNL7234B-BUN", "price": 315.00, "category": "Post & Panel", "status": "outofstock"},
    {"id": "68427", "name": "1.8m Satin Post and Panel Barricade Bundle", "sku": "PNL7234SA-BUN", "price": 325.00, "category": "Post & Panel", "status": "outofstock"},

    # Barricade Bundles & Accessories
    {"id": "8192", "name": "30 Pack With Cart - 1.8m Steel Barricades", "sku": "BAR-30PK", "price": 1349.00, "category": "Bundle", "status": "outofstock"},
    {"id": "6089", "name": "Barricade Storage Cart - 30 Capacity", "sku": "BAR-CART", "price": 450.00, "category": "Accessory", "status": "outofstock"},

    # Heavy Duty 8.5ft Steel Barricades (Draft/Inactive)
    {"id": "6700", "name": "8.5ft Steel Barricade Heavy Duty Black", "sku": "BAR8-BK", "price": 88.00, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6711", "name": "8.5ft Steel Barricade Heavy Duty Orange", "sku": "BAR8-OR", "price": 87.95, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6712", "name": "8.5ft Steel Barricade Heavy Duty Red", "sku": "BAR8-RD", "price": 88.00, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6714", "name": "8.5ft Steel Barricade Heavy Duty Blue", "sku": "BAR8-BL", "price": 88.00, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6715", "name": "8.5ft Steel Barricade Heavy Duty Green", "sku": "BAR8-GN", "price": 88.00, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6716", "name": "8.5ft Steel Barricade Heavy Duty White", "sku": "BAR8-WH", "price": 88.45, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6717", "name": "8.5ft Steel Barricade Heavy Duty Silver", "sku": "BAR8-SR", "price": 79.95, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "7915", "name": "8.5ft Heavy Duty Pre-Galvanized Steel", "sku": "CCC-BARR-HD-6_5", "price": 71.95, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "7910", "name": "8.5ft Economy Steel Hot Dipped Galvanized", "sku": "CCC-BARR-HD", "price": 69.95, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "7908", "name": "8.5ft Economy Steel Pre-Galvanized", "sku": "CCC-BARR-PG", "price": 59.95, "category": "Steel - 8.5ft", "status": "outofstock"},
    {"id": "6075", "name": "8.5ft Steel Barricade Galvanized", "sku": "BAR8-GD", "price": 82.00, "category": "Steel - 8.5ft", "status": "outofstock"},

    # Plastic Barricades 6.5ft (Draft/Inactive)
    {"id": "7420", "name": "6.5 FT Plastic Barricade Black", "sku": "BARPL6-BK", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7422", "name": "6.5 FT Plastic Barricade Orange", "sku": "BARPL6-OR", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7423", "name": "6.5 FT Plastic Barricade Yellow", "sku": "BARPL6-YW", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7424", "name": "6.5 FT Plastic Barricade Red", "sku": "BARPL6-RD", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7425", "name": "6.5 FT Plastic Barricade Blue", "sku": "BARPL6-BL", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7426", "name": "6.5 FT Plastic Barricade Green", "sku": "BARPL6-GN", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7427", "name": "6.5 FT Plastic Barricade White", "sku": "BARPL6-WH", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},
    {"id": "7411", "name": "6.5 FT Plastic Barricade Gray", "sku": "BARPL6-GY", "price": 158.00, "category": "Plastic - 6.5ft", "status": "outofstock"},

    # Barricade Bundle Packs (Draft/Inactive)
    {"id": "8051", "name": "30 Pack - 8.5 FT Heavy Duty Steel Barricades", "sku": "N/A", "price": 3249.00, "category": "Bundle", "status": "outofstock"},
    {"id": "8050", "name": "20 Pack - 8.5 FT Heavy Duty Steel Barricades", "sku": "N/A", "price": 2298.00, "category": "Bundle", "status": "outofstock"},
    {"id": "8045", "name": "10 Pack - 8.5 FT Heavy Duty Steel Barricades", "sku": "N/A", "price": 1248.00, "category": "Bundle", "status": "outofstock"},
]

# Build the data
product_data = {
    'Product ID': [],
    'Product Name': [],
    'SKU': [],
    'Category': [],
    'Price (£)': [],
    'Stock Status': [],
    '12-Mo Spend (£)': [],
    '12-Mo Impressions': [],
    '12-Mo Clicks': [],
    '12-Mo CTR (%)': [],
    '12-Mo CPC (£)': [],
    '12-Mo Conversions': [],
    '12-Mo Revenue (£)': [],
    '12-Mo ROAS (%)': [],
    'Performance Notes': []
}

for product in all_products:
    product_id = str(product['id'])

    product_data['Product ID'].append(product_id)
    product_data['Product Name'].append(product['name'])
    product_data['SKU'].append(product['sku'])
    product_data['Category'].append(product['category'])
    product_data['Price (£)'].append(product['price'])
    product_data['Stock Status'].append('In Stock' if product['status'] == 'instock' else 'Out of Stock')

    # Get performance data
    if product_id in ads_performance:
        perf = ads_performance[product_id]
        spend = perf['cost']
        impressions = perf['impressions']
        clicks = perf['clicks']
        conversions = perf['conversions']
        revenue = perf['revenue']

        product_data['12-Mo Spend (£)'].append(spend)
        product_data['12-Mo Impressions'].append(impressions)
        product_data['12-Mo Clicks'].append(clicks)

        # Calculate CTR
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        product_data['12-Mo CTR (%)'].append(round(ctr, 2))

        # Calculate CPC
        cpc = (spend / clicks) if clicks > 0 else 0
        product_data['12-Mo CPC (£)'].append(round(cpc, 2))

        product_data['12-Mo Conversions'].append(conversions)
        product_data['12-Mo Revenue (£)'].append(revenue)

        # Calculate ROAS
        roas = (revenue / spend * 100) if spend > 0 else 0
        product_data['12-Mo ROAS (%)'].append(round(roas, 0))

        # Performance notes
        if revenue > 5000:
            notes = "⭐ Top performer"
        elif revenue > 1000:
            notes = "✅ Strong performer"
        elif spend > 100 and revenue < 100:
            notes = "❌ Poor performer - consider pausing"
        elif spend > 0 and revenue == 0:
            notes = "⚠️ No conversions"
        elif spend > 0:
            notes = "⚠️ Below average"
        else:
            notes = "No data"
        product_data['Performance Notes'].append(notes)
    else:
        # No ad spend
        product_data['12-Mo Spend (£)'].append(0)
        product_data['12-Mo Impressions'].append(0)
        product_data['12-Mo Clicks'].append(0)
        product_data['12-Mo CTR (%)'].append(0)
        product_data['12-Mo CPC (£)'].append(0)
        product_data['12-Mo Conversions'].append(0)
        product_data['12-Mo Revenue (£)'].append(0)
        product_data['12-Mo ROAS (%)'].append(0)
        product_data['Performance Notes'].append("Not advertised")

# Create DataFrame
df = pd.DataFrame(product_data)

# Sort by spend descending
df = df.sort_values('12-Mo Spend (£)', ascending=False)

# Create Excel writer
output_file = '/Users/administrator/Documents/PetesBrain/clients/crowd-control/reports/all-barricades-12month-performance-2025-11-20.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Write main product data
    df.to_excel(writer, sheet_name='All Barricades', index=False)

    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['All Barricades']

    # Format columns
    worksheet.column_dimensions['A'].width = 12  # Product ID
    worksheet.column_dimensions['B'].width = 50  # Product Name
    worksheet.column_dimensions['C'].width = 18  # SKU
    worksheet.column_dimensions['D'].width = 18  # Category
    worksheet.column_dimensions['E'].width = 12  # Price
    worksheet.column_dimensions['F'].width = 14  # Stock Status
    worksheet.column_dimensions['G'].width = 16  # Spend
    worksheet.column_dimensions['H'].width = 16  # Impressions
    worksheet.column_dimensions['I'].width = 14  # Clicks
    worksheet.column_dimensions['J'].width = 14  # CTR
    worksheet.column_dimensions['K'].width = 14  # CPC
    worksheet.column_dimensions['L'].width = 16  # Conversions
    worksheet.column_dimensions['M'].width = 16  # Revenue
    worksheet.column_dimensions['N'].width = 16  # ROAS
    worksheet.column_dimensions['O'].width = 35  # Performance Notes

    # Format header row
    from openpyxl.styles import Font, PatternFill, Alignment

    header_fill = PatternFill(start_color='2d5016', end_color='2d5016', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Format currency and number columns
    from openpyxl.styles import numbers

    for row in range(2, len(df) + 2):
        worksheet[f'E{row}'].number_format = '£#,##0.00'
        worksheet[f'G{row}'].number_format = '£#,##0.00'
        worksheet[f'H{row}'].number_format = '#,##0'
        worksheet[f'I{row}'].number_format = '#,##0'
        worksheet[f'J{row}'].number_format = '0.00%'
        worksheet[f'K{row}'].number_format = '£#,##0.00'
        worksheet[f'L{row}'].number_format = '#,##0.00'
        worksheet[f'M{row}'].number_format = '£#,##0.00'
        worksheet[f'N{row}'].number_format = '0%'

    # Create summary by category sheet
    category_summary = df.groupby('Category').agg({
        'Product ID': 'count',
        '12-Mo Spend (£)': 'sum',
        '12-Mo Impressions': 'sum',
        '12-Mo Clicks': 'sum',
        '12-Mo Conversions': 'sum',
        '12-Mo Revenue (£)': 'sum'
    }).reset_index()

    category_summary.columns = ['Category', 'Products', 'Total Spend (£)', 'Total Impressions', 'Total Clicks', 'Total Conversions', 'Total Revenue (£)']
    category_summary['ROAS (%)'] = ((category_summary['Total Revenue (£)'] / category_summary['Total Spend (£)'] * 100).fillna(0)).round(0)
    category_summary = category_summary.sort_values('Total Spend (£)', ascending=False)

    category_summary.to_excel(writer, sheet_name='Summary by Category', index=False)

    # Format summary sheet
    summary_sheet = writer.sheets['Summary by Category']
    summary_sheet.column_dimensions['A'].width = 20
    summary_sheet.column_dimensions['B'].width = 12
    summary_sheet.column_dimensions['C'].width = 18
    summary_sheet.column_dimensions['D'].width = 18
    summary_sheet.column_dimensions['E'].width = 16
    summary_sheet.column_dimensions['F'].width = 18
    summary_sheet.column_dimensions['G'].width = 18
    summary_sheet.column_dimensions['H'].width = 14

    for cell in summary_sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for row in range(2, len(category_summary) + 2):
        summary_sheet[f'C{row}'].number_format = '£#,##0.00'
        summary_sheet[f'D{row}'].number_format = '#,##0'
        summary_sheet[f'E{row}'].number_format = '#,##0'
        summary_sheet[f'F{row}'].number_format = '#,##0.00'
        summary_sheet[f'G{row}'].number_format = '£#,##0.00'
        summary_sheet[f'H{row}'].number_format = '0%'

    # Create overall summary sheet
    total_products = len(df)
    total_advertised = len(df[df['12-Mo Spend (£)'] > 0])
    total_spend = df['12-Mo Spend (£)'].sum()
    total_revenue = df['12-Mo Revenue (£)'].sum()
    overall_roas = (total_revenue / total_spend * 100) if total_spend > 0 else 0
    total_impressions = df['12-Mo Impressions'].sum()
    total_clicks = df['12-Mo Clicks'].sum()
    total_conversions = df['12-Mo Conversions'].sum()

    summary_data = {
        'Metric': [
            'Total Barricade Products',
            'Products Advertised (received spend)',
            'Products Not Advertised',
            'Total Advertising Spend',
            'Total Revenue Tracked',
            'Overall ROAS',
            'Total Impressions',
            'Total Clicks',
            'Average CTR',
            'Total Conversions',
            'Average Cost Per Conversion'
        ],
        'Value': [
            total_products,
            total_advertised,
            total_products - total_advertised,
            f"£{total_spend:.2f}",
            f"£{total_revenue:.2f}",
            f"{overall_roas:.0f}%",
            f"{total_impressions:,.0f}",
            f"{total_clicks:,.0f}",
            f"{(total_clicks / total_impressions * 100):.2f}%" if total_impressions > 0 else "0%",
            f"{total_conversions:.0f}",
            f"£{(total_spend / total_conversions):.2f}" if total_conversions > 0 else "N/A"
        ]
    }

    overall_df = pd.DataFrame(summary_data)
    overall_df.to_excel(writer, sheet_name='Overall Summary', index=False)

    # Format overall summary sheet
    overall_sheet = writer.sheets['Overall Summary']
    overall_sheet.column_dimensions['A'].width = 35
    overall_sheet.column_dimensions['B'].width = 25

    for cell in overall_sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')

print(f"✅ Excel spreadsheet created: {output_file}")
print(f"\nOverall Summary:")
print(f"- Total Barricade Products: {total_products}")
print(f"- Products Advertised: {total_advertised}")
print(f"- Total Spend: £{total_spend:.2f}")
print(f"- Total Revenue: £{total_revenue:.2f}")
print(f"- Overall ROAS: {overall_roas:.0f}%")
print(f"\nTop 3 Categories by Spend:")
for idx, row in category_summary.head(3).iterrows():
    print(f"  {row['Category']}: £{row['Total Spend (£)']:.2f} → £{row['Total Revenue (£)']:.2f} ({row['ROAS (%)']:.0f}% ROAS)")
