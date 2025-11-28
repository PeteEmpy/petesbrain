#!/usr/bin/env python3
"""
Calculate Google Ads revenue percentage vs total WooCommerce revenue for yesterday
"""
import requests
from datetime import datetime, timedelta
import sys
import os

# Add the shared scripts path to import Google Ads client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared', 'mcp-servers', 'google-ads-mcp-server'))

# WooCommerce API credentials
SITE_URL = "https://mygodshot.com"
CONSUMER_KEY = "ck_d1906a0a64cdc4f9b365d67c6757c0b603335402"
CONSUMER_SECRET = "cs_ebcb7f623c95498adf6138feb81ce79a8c10530a"

# Google Ads Account ID
GOOGLE_ADS_CUSTOMER_ID = "9922220205"

def get_woocommerce_revenue(date_str):
    """Get total revenue from WooCommerce for a specific date"""
    after = f"{date_str}T00:00:00"
    before = f"{date_str}T23:59:59"
    
    url = f"{SITE_URL}/wp-json/wc/v3/orders"
    params = {
        'after': after,
        'before': before,
        'per_page': 100,
        'status': 'any'
    }
    
    response = requests.get(
        url,
        auth=(CONSUMER_KEY, CONSUMER_SECRET),
        params=params
    )
    
    if response.status_code != 200:
        print(f"Error fetching WooCommerce orders: {response.status_code}")
        print(response.text)
        return None
    
    orders = response.json()
    total_revenue = 0
    order_count = len(orders)
    
    # Calculate total revenue from completed/processing orders
    for order in orders:
        status = order.get('status', 'unknown')
        order_total = float(order.get('total', 0))
        
        # Include all order statuses for total revenue
        total_revenue += order_total
    
    return {
        'total_revenue': total_revenue,
        'order_count': order_count,
        'orders': orders
    }

def get_google_ads_revenue(date_str):
    """Get Google Ads conversions_value for a specific date"""
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        print("Error: google-ads library not installed")
        return None
    
    try:
        # Initialize Google Ads client
        client = GoogleAdsClient.load_from_storage()
        ga_service = client.get_service("GoogleAdsService")
        
        # Query for conversions_value on the specific date
        query = f"""
            SELECT
                segments.date,
                metrics.conversions_value,
                metrics.conversions,
                metrics.cost_micros,
                metrics.clicks
            FROM customer
            WHERE segments.date = '{date_str}'
        """
        
        response = ga_service.search(customer_id=GOOGLE_ADS_CUSTOMER_ID, query=query)
        
        conversions_value = 0
        conversions = 0
        cost_micros = 0
        clicks = 0
        
        for row in response:
            conversions_value += row.metrics.conversions_value
            conversions += row.metrics.conversions
            cost_micros += row.metrics.cost_micros
            clicks += row.metrics.clicks
        
        return {
            'revenue': conversions_value,
            'conversions': conversions,
            'cost': cost_micros / 1_000_000,  # Convert micros to currency
            'clicks': clicks
        }
    except Exception as e:
        print(f"Error fetching Google Ads data: {e}")
        return None

def main():
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    
    print("\n" + "="*70)
    print(f"GODSHOT REVENUE ANALYSIS - {date_str}")
    print("="*70 + "\n")
    
    # Get WooCommerce revenue
    print("📦 Fetching WooCommerce orders...")
    wc_data = get_woocommerce_revenue(date_str)
    
    if wc_data is None:
        print("❌ Failed to fetch WooCommerce data")
        return
    
    wc_revenue = wc_data['total_revenue']
    wc_orders = wc_data['order_count']
    
    print(f"✅ WooCommerce Total Revenue: £{wc_revenue:.2f}")
    print(f"   Total Orders: {wc_orders}")
    
    # Get Google Ads revenue
    print("\n📊 Fetching Google Ads conversions...")
    ga_data = get_google_ads_revenue(date_str)
    
    if ga_data is None:
        print("❌ Failed to fetch Google Ads data")
        return
    
    ga_revenue = ga_data['revenue']
    ga_conversions = ga_data['conversions']
    ga_cost = ga_data['cost']
    
    print(f"✅ Google Ads Revenue: £{ga_revenue:.2f}")
    print(f"   Conversions: {ga_conversions:.2f}")
    print(f"   Spend: £{ga_cost:.2f}")
    
    # Calculate percentage
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    if wc_revenue > 0:
        percentage = (ga_revenue / wc_revenue) * 100
        print(f"\n💰 Total WooCommerce Revenue: £{wc_revenue:.2f}")
        print(f"📊 Google Ads Revenue: £{ga_revenue:.2f}")
        print(f"📈 Google Ads % of Total Revenue: {percentage:.2f}%")
        
        if percentage > 100:
            print(f"\n⚠️  Note: Google Ads revenue ({percentage:.2f}%) exceeds total WooCommerce revenue.")
            print("   This could indicate:")
            print("   - Conversion tracking includes offline conversions")
            print("   - Multiple attribution windows")
            print("   - Conversion value discrepancies")
        elif percentage < 0:
            print(f"\n⚠️  Note: Negative percentage indicates data issues.")
    else:
        print(f"\n⚠️  No WooCommerce revenue for {date_str}")
        print(f"   Google Ads reported £{ga_revenue:.2f} in revenue")
    
    print()

if __name__ == "__main__":
    main()

