#!/usr/bin/env python3
"""
Query all ad groups with activity in October 2025 for Devonshire Hotels
"""

import os
import sys
from google.ads.googleads.client import GoogleAdsClient

# Customer ID
CUSTOMER_ID = "5898250490"  # Devonshire Group

def main():
    # Load Google Ads credentials
    yaml_path = os.path.expanduser("~/google-ads.yaml")

    try:
        client = GoogleAdsClient.load_from_storage(yaml_path)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)

    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          campaign.id,
          campaign.name,
          ad_group.id,
          ad_group.name,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions_value_by_conversion_date,
          metrics.conversions_by_conversion_date
        FROM ad_group
        WHERE segments.date BETWEEN '2025-10-01' AND '2025-10-31'
          AND campaign.status = 'ENABLED'
          AND ad_group.status = 'ENABLED'
          AND metrics.impressions > 0
        ORDER BY campaign.name, metrics.cost_micros DESC
    """

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        current_campaign = None

        for batch in response:
            for row in batch.results:
                campaign_name = row.campaign.name
                ad_group_name = row.ad_group.name
                impressions = row.metrics.impressions
                clicks = row.metrics.clicks
                ctr = row.metrics.ctr * 100
                cost = row.metrics.cost_micros / 1_000_000
                revenue = row.metrics.conversions_value_by_conversion_date
                conversions = row.metrics.conversions_by_conversion_date
                roas = revenue / cost if cost > 0 else 0

                # Print campaign header when it changes
                if campaign_name != current_campaign:
                    print(f"\n{'='*80}")
                    print(f"Campaign: {campaign_name}")
                    print(f"{'='*80}")
                    current_campaign = campaign_name

                print(f"\nAd Group: {ad_group_name}")
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
