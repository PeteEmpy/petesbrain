#!/usr/bin/env python3
"""
Quick script to check Godshot WooCommerce sales for Nov 5, 2025
"""
import requests
from datetime import datetime, timedelta
import json

# WooCommerce API credentials (from .mcp.json)
SITE_URL = "https://mygodshot.com"
CONSUMER_KEY = "ck_d1906a0a64cdc4f9b365d67c6757c0b603335402"
CONSUMER_SECRET = "cs_ebcb7f623c95498adf6138feb81ce79a8c10530a"

def get_orders_for_date(date_str):
    """Get orders for a specific date"""

    # Date range for the query (start of day to end of day)
    after = f"{date_str}T00:00:00"
    before = f"{date_str}T23:59:59"

    url = f"{SITE_URL}/wp-json/wc/v3/orders"

    params = {
        'after': after,
        'before': before,
        'per_page': 100,
        'status': 'any'  # Get all order statuses
    }

    response = requests.get(
        url,
        auth=(CONSUMER_KEY, CONSUMER_SECRET),
        params=params
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

def main():
    # Check Nov 5, 2025 and surrounding days
    dates = ["2025-11-04", "2025-11-05", "2025-11-06"]

    print("\n" + "="*70)
    print("GODSHOT WOOCOMMERCE SALES VERIFICATION")
    print("="*70 + "\n")

    for date_str in dates:
        orders = get_orders_for_date(date_str)

        total_revenue = 0
        order_count = len(orders)

        completed_orders = []
        pending_orders = []

        for order in orders:
            status = order.get('status', 'unknown')
            order_total = float(order.get('total', 0))

            if status in ['completed', 'processing']:
                completed_orders.append(order)
                total_revenue += order_total
            else:
                pending_orders.append(order)

        print(f"📅 {date_str}")
        print(f"   Total Orders: {order_count}")
        print(f"   Completed/Processing: {len(completed_orders)}")
        print(f"   Other Status: {len(pending_orders)}")
        print(f"   💰 Revenue: £{total_revenue:.2f}")

        if completed_orders:
            print(f"\n   Completed Orders:")
            for order in completed_orders:
                print(f"      - Order #{order['id']}: £{order['total']} ({order['status']})")

        if pending_orders:
            print(f"\n   Other Orders:")
            for order in pending_orders:
                print(f"      - Order #{order['id']}: £{order['total']} ({order['status']})")

        print()

if __name__ == "__main__":
    main()
