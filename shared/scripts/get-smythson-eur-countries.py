#!/usr/bin/env python3
"""Get list of countries targeted in Smythson EUR Google Ads account"""

import sys
from pathlib import Path
import json

# Add MCP server path
PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-ads-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

from google_ads_query import query_google_ads

CUSTOMER_ID = "7679616761"
MANAGER_ID = "2569949686"

# Step 1: Get all unique location geo target constants
print("Fetching location targeting from Smythson EUR account...")
query1 = """
SELECT campaign_criterion.location.geo_target_constant
FROM campaign_criterion
WHERE campaign_criterion.type = 'LOCATION'
  AND campaign.status != 'REMOVED'
"""

results = query_google_ads(CUSTOMER_ID, query1, MANAGER_ID)
unique_constants = set()
for row in results:
    constant = row['campaignCriterion']['location']['geoTargetConstant']
    unique_constants.add(constant)

print(f"Found {len(unique_constants)} unique location targets")

# Step 2: Get country names for these constants
print("Fetching country names...")

# Build IN clause (batch in groups of 100 to avoid query limits)
constants_list = list(unique_constants)
all_countries = {}

for i in range(0, len(constants_list), 100):
    batch = constants_list[i:i+100]
    in_clause = ", ".join([f"'{c}'" for c in batch])

    query2 = f"""
    SELECT
      geo_target_constant.resource_name,
      geo_target_constant.canonical_name,
      geo_target_constant.country_code,
      geo_target_constant.target_type
    FROM geo_target_constant
    WHERE geo_target_constant.resource_name IN ({in_clause})
      AND geo_target_constant.target_type = 'Country'
    """

    results2 = query_google_ads(CUSTOMER_ID, query2, MANAGER_ID)

    for row in results2:
        name = row['geoTargetConstant']['canonicalName']
        code = row['geoTargetConstant']['countryCode']
        all_countries[name] = code

# Step 3: Filter out UK, France, Italy, Germany
exclude = {'United Kingdom', 'France', 'Italy', 'Germany'}
filtered_countries = {name: code for name, code in all_countries.items() if name not in exclude}

# Step 4: Sort and output
sorted_countries = sorted(filtered_countries.keys())

print("\n" + "=" * 60)
print(f"European countries in Smythson EUR account ({len(sorted_countries)} countries)")
print("Excluding: UK, France, Italy, Germany")
print("=" * 60)
print()

for country in sorted_countries:
    print(country)

print()
print(f"Total: {len(sorted_countries)} countries")
