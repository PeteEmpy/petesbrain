#!/usr/bin/env python3
"""
Check what conversion actions existed in 2024
"""

import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("Error: Google Ads API client not found")
    sys.exit(1)

CUSTOMER_ID = "8573235780"
MANAGER_ID = "2569949686"

def main():
    try:
        client = GoogleAdsClient.load_from_storage("/Users/administrator/google-ads.yaml")
    except Exception as e:
        print(f"Error loading client: {e}")
        sys.exit(1)

    client.login_customer_id = MANAGER_ID

    # Query to see what conversion actions had data in 2024
    query = """
        SELECT
            segments.conversion_action_name,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE
            campaign.advertising_channel_type = 'SEARCH'
            AND segments.date BETWEEN '2024-10-14' AND '2024-11-12'
    """

    ga_service = client.get_service("GoogleAdsService")

    print("Conversion actions with data in Oct-Nov 2024:")
    print("="*80)

    conversion_actions = {}

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        for batch in response:
            for row in batch.results:
                action_name = row.segments.conversion_action_name
                conversions = float(row.metrics.conversions)
                value = float(row.metrics.conversions_value)

                if action_name not in conversion_actions:
                    conversion_actions[action_name] = {'conversions': 0, 'value': 0}

                conversion_actions[action_name]['conversions'] += conversions
                conversion_actions[action_name]['value'] += value

        # Print summary
        for action, data in sorted(conversion_actions.items(), key=lambda x: x[1]['conversions'], reverse=True):
            print(f"\n{action}")
            print(f"  Conversions: {data['conversions']:.0f}")
            print(f"  Value: £{data['value']:,.2f}")

    except GoogleAdsException as ex:
        print(f"Error: {ex.error.code().name}")
        for error in ex.failure.errors:
            print(f'  {error.message}')

if __name__ == '__main__':
    main()
