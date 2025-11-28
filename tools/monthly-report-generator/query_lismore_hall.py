from google.ads.googleads.client import GoogleAdsClient
import os

# Initialize the Google Ads client
client = GoogleAdsClient.load_from_storage(os.path.expanduser("~/google-ads.yaml"))
ga_service = client.get_service("GoogleAdsService")

CUSTOMER_ID = "5898250490"  # Devonshire Group

# Query Lismore campaigns
query_lismore = """
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
      AND campaign.name LIKE '%Lismore%'
      AND campaign.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY campaign.name, metrics.cost_micros DESC
"""

# Query The Hall campaigns
query_hall = """
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
      AND campaign.name LIKE '%Hall%'
      AND campaign.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY campaign.name, metrics.cost_micros DESC
"""

print(f"\nQuerying Lismore and The Hall campaigns for customer {CUSTOMER_ID}...")
print("=" * 80)

all_data = []

# Query Lismore
print("\n=== LISMORE ===")
response_lismore = ga_service.search(customer_id=CUSTOMER_ID, query=query_lismore)

total_spend_lismore = 0
total_revenue_lismore = 0
total_conversions_lismore = 0

for row in response_lismore:
    campaign_name = row.campaign.name
    ad_group_name = row.ad_group.name
    impressions = row.metrics.impressions
    clicks = row.metrics.clicks
    ctr = row.metrics.ctr * 100
    spend = row.metrics.cost_micros / 1_000_000
    revenue = row.metrics.conversions_value_by_conversion_date
    conversions = row.metrics.conversions_by_conversion_date
    
    total_spend_lismore += spend
    total_revenue_lismore += revenue
    total_conversions_lismore += conversions
    
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
    
    all_data.append({
        'campaign': 'Lismore',
        'ad_group': ad_group_name,
        'impressions': impressions,
        'clicks': clicks,
        'ctr': ctr,
        'spend': spend,
        'revenue': revenue,
        'conversions': conversions,
        'roas': roas
    })

# Query The Hall
print("\n=== THE HALL ===")
response_hall = ga_service.search(customer_id=CUSTOMER_ID, query=query_hall)

total_spend_hall = 0
total_revenue_hall = 0
total_conversions_hall = 0

for row in response_hall:
    campaign_name = row.campaign.name
    ad_group_name = row.ad_group.name
    impressions = row.metrics.impressions
    clicks = row.metrics.clicks
    ctr = row.metrics.ctr * 100
    spend = row.metrics.cost_micros / 1_000_000
    revenue = row.metrics.conversions_value_by_conversion_date
    conversions = row.metrics.conversions_by_conversion_date
    
    total_spend_hall += spend
    total_revenue_hall += revenue
    total_conversions_hall += conversions
    
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
    
    all_data.append({
        'campaign': 'The Hall',
        'ad_group': ad_group_name,
        'impressions': impressions,
        'clicks': clicks,
        'ctr': ctr,
        'spend': spend,
        'revenue': revenue,
        'conversions': conversions,
        'roas': roas
    })

print("\n" + "=" * 80)
print(f"LISMORE TOTALS:")
print(f"  Total Spend: £{total_spend_lismore:,.2f}")
print(f"  Total Revenue: £{total_revenue_lismore:,.2f}")
print(f"  Total Conversions: {total_conversions_lismore:.2f}")
print(f"  Overall ROAS: {total_revenue_lismore / total_spend_lismore if total_spend_lismore > 0 else 0:.2f}x")

print(f"\nTHE HALL TOTALS:")
print(f"  Total Spend: £{total_spend_hall:,.2f}")
print(f"  Total Revenue: £{total_revenue_hall:,.2f}")
print(f"  Total Conversions: {total_conversions_hall:.2f}")
print(f"  Overall ROAS: {total_revenue_hall / total_spend_hall if total_spend_hall > 0 else 0:.2f}x")

print(f"\nCOMBINED TOTALS:")
print(f"  Total Spend: £{total_spend_lismore + total_spend_hall:,.2f}")
print(f"  Total Revenue: £{total_revenue_lismore + total_revenue_hall:,.2f}")
print(f"  Total Conversions: {total_conversions_lismore + total_conversions_hall:.2f}")
print(f"  Overall ROAS: {(total_revenue_lismore + total_revenue_hall) / (total_spend_lismore + total_spend_hall) if (total_spend_lismore + total_spend_hall) > 0 else 0:.2f}x")
