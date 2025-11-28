#!/usr/bin/env python3
"""
Get Google Ads conversions_value for a specific date
"""
import sys
import os
from datetime import datetime, timedelta

try:
    from google.ads.googleads.client import GoogleAdsClient
except ImportError:
    print("Error: google-ads library not installed")
    sys.exit(1)

# Google Ads Account ID for Godshot
CUSTOMER_ID = "9922220205"

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime('%Y-%m-%d')

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
    
    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    
    conversions_value = 0
    conversions = 0
    cost_micros = 0
    clicks = 0
    
    for row in response:
        conversions_value += row.metrics.conversions_value
        conversions += row.metrics.conversions
        cost_micros += row.metrics.cost_micros
        clicks += row.metrics.clicks
    
    print(f"{conversions_value:.2f}")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

