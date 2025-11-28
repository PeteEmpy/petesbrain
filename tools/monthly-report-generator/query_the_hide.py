#!/usr/bin/env python3
"""
Query The Hide campaigns for October 2025
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

    # Query for Hide first
    query_hide = """
        SELECT
          campaign.id,
          campaign.name,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions_value_by_conversion_date,
          metrics.conversions_by_conversion_date
        FROM campaign
        WHERE segments.date BETWEEN '2025-10-01' AND '2025-10-31'
          AND campaign.name LIKE '%Hide%'
        ORDER BY metrics.cost_micros DESC
    """

    print("=== THE HIDE CAMPAIGNS ===")

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_hide)
        for batch in response:
            for row in batch.results:
                campaign_name = row.campaign.name
                campaign_id = row.campaign.id
                impressions = row.metrics.impressions
                clicks = row.metrics.clicks
                ctr = row.metrics.ctr * 100
                cost = row.metrics.cost_micros / 1_000_000
                revenue = row.metrics.conversions_value_by_conversion_date
                conversions = row.metrics.conversions_by_conversion_date
                roas = revenue / cost if cost > 0 else 0

                print(f"\nCampaign: {campaign_name}")
                print(f"  ID: {campaign_id}")
                print(f"  Impressions: {impressions:,}")
                print(f"  Clicks: {clicks:,}")
                print(f"  CTR: {ctr:.2f}%")
                print(f"  Spend: £{cost:.2f}")
                print(f"  Revenue: £{revenue:.2f}")
                print(f"  ROAS: {roas:.2f}x")
                print(f"  Conversions: {conversions:.2f}")
    except Exception as e:
        print(f"Error: {e}")

    # Query for Highwayman
    query_highwayman = """
        SELECT
          campaign.id,
          campaign.name,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions_value_by_conversion_date,
          metrics.conversions_by_conversion_date
        FROM campaign
        WHERE segments.date BETWEEN '2025-10-01' AND '2025-10-31'
          AND campaign.name LIKE '%Highwayman%'
        ORDER BY metrics.cost_micros DESC
    """

    print("\n\n=== HIGHWAYMAN CAMPAIGNS ===")

    query = query_highwayman

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        for batch in response:
            for row in batch.results:
                campaign_name = row.campaign.name
                campaign_id = row.campaign.id
                impressions = row.metrics.impressions
                clicks = row.metrics.clicks
                ctr = row.metrics.ctr * 100
                cost = row.metrics.cost_micros / 1_000_000
                revenue = row.metrics.conversions_value_by_conversion_date
                conversions = row.metrics.conversions_by_conversion_date
                roas = revenue / cost if cost > 0 else 0

                print(f"\nCampaign: {campaign_name}")
                print(f"  ID: {campaign_id}")
                print(f"  Impressions: {impressions:,}")
                print(f"  Clicks: {clicks:,}")
                print(f"  CTR: {ctr:.2f}%")
                print(f"  Spend: £{cost:.2f}")
                print(f"  Revenue: £{revenue:.2f}")
                print(f"  ROAS: {roas:.2f}x")
                print(f"  Conversions: {conversions:.2f}")

    except Exception as e:
        print(f"Error querying Google Ads: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
