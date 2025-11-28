"""
Query monthly performance for The Hide and Highwayman Arms from Jan-Oct 2025
"""

import os
import sys
from google.ads.googleads.client import GoogleAdsClient

CUSTOMER_ID = "5898250490"  # Devonshire Group

def main():
    yaml_path = os.path.expanduser("~/google-ads.yaml")
    
    try:
        client = GoogleAdsClient.load_from_storage(yaml_path)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)
    
    ga_service = client.get_service("GoogleAdsService")
    
    # Store data by month
    monthly_data = {}
    
    # Query 1: The Hide
    query_hide = """
        SELECT
          segments.month,
          campaign.name,
          metrics.clicks,
          metrics.impressions,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions_value_by_conversion_date,
          metrics.conversions_by_conversion_date
        FROM campaign
        WHERE segments.date BETWEEN '2025-01-01' AND '2025-10-31'
          AND campaign.name LIKE '%Hide%'
        ORDER BY segments.month
    """
    
    # Query 2: Highwayman
    query_highwayman = """
        SELECT
          segments.month,
          campaign.name,
          metrics.clicks,
          metrics.impressions,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions_value_by_conversion_date,
          metrics.conversions_by_conversion_date
        FROM campaign
        WHERE segments.date BETWEEN '2025-01-01' AND '2025-10-31'
          AND campaign.name LIKE '%Highwayman%'
        ORDER BY segments.month
    """
    
    print("=== THE HIDE & HIGHWAYMAN MONTHLY PERFORMANCE (JAN-OCT 2025) ===\n")
    
    try:
        # Process both queries
        for query in [query_hide, query_highwayman]:
            response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
            
            for row in response:
                month = row.segments.month
                clicks = row.metrics.clicks
                impressions = row.metrics.impressions
                cost = row.metrics.cost_micros / 1_000_000
                revenue = row.metrics.conversions_value_by_conversion_date
                conversions = row.metrics.conversions_by_conversion_date
                
                if month not in monthly_data:
                    monthly_data[month] = {
                        'clicks': 0,
                        'impressions': 0,
                        'cost': 0,
                        'revenue': 0,
                        'conversions': 0
                    }
                
                monthly_data[month]['clicks'] += clicks
                monthly_data[month]['impressions'] += impressions
                monthly_data[month]['cost'] += cost
                monthly_data[month]['revenue'] += revenue
                monthly_data[month]['conversions'] += conversions
        
        # Print consolidated monthly data
        for month in sorted(monthly_data.keys()):
            data = monthly_data[month]
            ctr = (data['clicks'] / data['impressions'] * 100) if data['impressions'] > 0 else 0
            roas = data['revenue'] / data['cost'] if data['cost'] > 0 else 0
            conv_rate = (data['conversions'] / data['clicks'] * 100) if data['clicks'] > 0 else 0
            
            print(f"Month: {month}")
            print(f"  Clicks: {data['clicks']:,}")
            print(f"  Impressions: {data['impressions']:,}")
            print(f"  CTR: {ctr:.2f}%")
            print(f"  Spend: £{data['cost']:,.2f}")
            print(f"  Revenue: £{data['revenue']:,.2f}")
            print(f"  ROAS: {roas:.2f}x")
            print(f"  Conversions: {data['conversions']:.2f}")
            print(f"  Conversion Rate: {conv_rate:.2f}%")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
