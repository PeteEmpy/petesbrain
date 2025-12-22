#!/usr/bin/env python3
"""
Quick script to verify year-over-year revenue for email to Sam
Compares 17 Nov - 16 Dec (2024 vs 2025)
"""

import httpx
import xml.etree.ElementTree as ET
from datetime import datetime

# PrestaShop credentials
SHOP_URL = "https://accessoriesforthehome.co.uk"
API_KEY = "JU6R2RG7RW77UETJSTIP39UKE4V84HGC"
API_URL = f"{SHOP_URL}/api"

def get_orders(date_from, date_to):
    """Get orders for a date range"""
    params = {
        'display': 'full',
        'filter[invoice_date]': f'[{date_from} 00:00:00,{date_to} 23:59:59]'
    }

    response = httpx.get(
        f"{API_URL}/orders",
        params=params,
        auth=(API_KEY, ''),
        timeout=30.0
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    orders = []
    for order_elem in root.findall('.//order'):
        order = {
            'id': order_elem.find('id').text,
            'reference': order_elem.find('reference').text,
            'current_state': order_elem.find('current_state').text,
            'total_paid_tax_excl': float(order_elem.find('total_paid_tax_excl').text or 0),
            'total_paid_tax_incl': float(order_elem.find('total_paid_tax_incl').text or 0),
            'invoice_date': order_elem.find('invoice_date').text,
        }
        orders.append(order)

    return orders

# This year: 17 Nov 2025 - 16 Dec 2025
print("Fetching orders for THIS YEAR (17 Nov 2025 - 16 Dec 2025)...")
orders_2025 = get_orders('2025-11-17', '2025-12-16')
revenue_2025_excl = sum(order['total_paid_tax_excl'] for order in orders_2025)
revenue_2025_incl = sum(order['total_paid_tax_incl'] for order in orders_2025)
count_2025 = len(orders_2025)

print(f"✓ Found {count_2025} orders")
print(f"  Tax Excl: £{revenue_2025_excl:,.2f}")
print(f"  Tax Incl: £{revenue_2025_incl:,.2f}\n")

# Last year: 17 Nov 2024 - 16 Dec 2024
print("Fetching orders for LAST YEAR (17 Nov 2024 - 16 Dec 2024)...")
orders_2024 = get_orders('2024-11-17', '2024-12-16')
revenue_2024_excl = sum(order['total_paid_tax_excl'] for order in orders_2024)
revenue_2024_incl = sum(order['total_paid_tax_incl'] for order in orders_2024)
count_2024 = len(orders_2024)

print(f"✓ Found {count_2024} orders")
print(f"  Tax Excl: £{revenue_2024_excl:,.2f}")
print(f"  Tax Incl: £{revenue_2024_incl:,.2f}\n")

# Calculate changes (using TAX EXCLUSIVE to match PrestaShop dashboard)
revenue_change_excl = revenue_2025_excl - revenue_2024_excl
revenue_change_pct_excl = (revenue_change_excl / revenue_2024_excl * 100) if revenue_2024_excl > 0 else 0
order_change = count_2025 - count_2024
order_change_pct = (order_change / count_2024 * 100) if count_2024 > 0 else 0

print("=" * 70)
print("YEAR-OVER-YEAR COMPARISON (17 Nov - 16 Dec) - TAX EXCLUSIVE")
print("=" * 70)
print(f"\nRevenue (Tax Excl - matches PrestaShop dashboard):")
print(f"  This Year:  £{revenue_2025_excl:,.2f}")
print(f"  Last Year:  £{revenue_2024_excl:,.2f}")
print(f"  Change:     £{revenue_change_excl:+,.2f} ({revenue_change_pct_excl:+.0f}%)")

print(f"\nRevenue (Tax Incl - for reference):")
print(f"  This Year:  £{revenue_2025_incl:,.2f}")
print(f"  Last Year:  £{revenue_2024_incl:,.2f}")

print(f"\nOrders:")
print(f"  This Year:  {count_2025}")
print(f"  Last Year:  {count_2024}")
print(f"  Change:     {order_change:+} ({order_change_pct:+.0f}%)")

# Order status breakdown
print(f"\nOrder Status Breakdown (This Year):")
status_counts = {}
for order in orders_2025:
    status = order['current_state']
    status_counts[status] = status_counts.get(status, 0) + 1
for status, count in sorted(status_counts.items()):
    print(f"  State {status}: {count} orders")

# Verification for email
print("\n" + "=" * 70)
print("PRESTASHOP DASHBOARD VERIFICATION")
print("=" * 70)
print(f"Dashboard shows: £101,337.19 (Tax excl.), 400 orders")
print(f"Script shows:    £{revenue_2025_excl:,.2f} (Tax excl.), {count_2025} orders")
print(f"Difference:      £{revenue_2025_excl - 101337.19:+,.2f}, {count_2025 - 400:+} orders")
