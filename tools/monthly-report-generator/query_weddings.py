from google.ads.googleads.client import GoogleAdsClient
import os

# Initialize the Google Ads client
client = GoogleAdsClient.load_from_storage(os.path.expanduser("~/google-ads.yaml"))
ga_service = client.get_service("GoogleAdsService")

CUSTOMER_ID = "5898250490"  # Devonshire Group

# Query Weddings campaigns
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
      AND campaign.name LIKE '%Wedding%'
      AND campaign.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY campaign.name, metrics.cost_micros DESC
"""

print(f"\nQuerying Weddings campaigns for customer {CUSTOMER_ID}...")
print("=" * 80)

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

total_spend = 0
total_revenue = 0
total_conversions = 0

for row in response:
    campaign_name = row.campaign.name
    ad_group_name = row.ad_group.name
    impressions = row.metrics.impressions
    clicks = row.metrics.clicks
    ctr = row.metrics.ctr * 100
    spend = row.metrics.cost_micros / 1_000_000
    revenue = row.metrics.conversions_value_by_conversion_date
    conversions = row.metrics.conversions_by_conversion_date
    
    total_spend += spend
    total_revenue += revenue
    total_conversions += conversions
    
    roas = revenue / spend if spend > 0 else 0
    
    print(f"\nCampaign: {campaign_name}")
    print(f"Ad Group: {ad_group_name}")
    print(f"  Impressions: {impressions:,}")
    print(f"  Clicks: {clicks:,}")
    print(f"  CTR: {ctr:.2f}%")
    print(f"  Spend: £{spend:,.2f}")
    print(f"  Revenue: £{revenue:,.2f}")
    print(f"  Conversions: {conversions:.2f}")
    print(f"  ROAS: {roas:.2f}x")

print("\n" + "=" * 80)
print(f"TOTALS:")
print(f"  Total Spend: £{total_spend:,.2f}")
print(f"  Total Revenue: £{total_revenue:,.2f}")
print(f"  Total Conversions: {total_conversions:.2f}")
print(f"  Overall ROAS: {total_revenue / total_spend if total_spend > 0 else 0:.2f}x")
