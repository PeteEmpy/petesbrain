#!/usr/bin/env python3
"""
Deploy Tier 1 Negative Keywords - Smythson All Regions
Excludes Aspinal terms per user requirement
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add MCP server to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests

API_VERSION = "v22"
MANAGER_ID = "2569949686"

# Smythson accounts
ACCOUNTS = {
    "UK": "8573235780",
    "USA": "7808690871",
    "EUR": "7679616761",
    "ROW": "5556710725"
}

# UK terms from detailed report (excluding aspinal)
UK_TERMS = [
    "スマイソン",  # Japanese text
    "smythson tote bag",
    "smythson jewellery box",
    "smythson jewelry box",  # US spelling
    "2026 diary",
    "smythson leather",
    "jewellery box",
    "smythson handbags",
    "smythson personalised stationery",
    "smythson bond street store",
    "smythson bag",
    "smyths",  # Toy store confusion
    "smythson travel wallet",
    "smythson tote",
    "smythson near me",
    "smythson passport cover",
    "smythson leather notebook",
    "selfridges",  # Retailer
    "frank smythson"  # Founder name
]

def query_tier1_terms(customer_id, account_name):
    """Query Tier 1 terms for an account"""
    print(f"\n🔍 Querying {account_name} ({customer_id}) for Tier 1 terms...")

    try:
        formatted_customer_id = format_customer_id(customer_id)
        headers = get_headers_with_auto_token()
        headers['login-customer-id'] = format_customer_id(MANAGER_ID)

        # Query using keyword_view instead of search_term_view
        query = """
            SELECT
              campaign.id,
              campaign.name,
              ad_group.id,
              ad_group.name,
              ad_group_criterion.keyword.text,
              metrics.clicks,
              metrics.cost_micros,
              metrics.conversions
            FROM keyword_view
            WHERE
              segments.date BETWEEN '2025-10-18' AND '2025-12-17'
              AND metrics.clicks >= 30
              AND metrics.conversions = 0
              AND metrics.cost_micros >= 20000000
            ORDER BY metrics.cost_micros DESC
        """

        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/googleAds:search"
        payload = {"query": query}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        results = data.get('results', [])

        print(f"   Found {len(results)} keywords meeting Tier 1 criteria")
        return results

    except Exception as e:
        print(f"   ❌ Error querying {account_name}: {e}")
        return []

def filter_aspinal_terms(terms, account_name):
    """Remove Aspinal-related terms"""
    filtered = []
    excluded_count = 0

    for term in terms:
        keyword_text = term.get('adGroupCriterion', {}).get('keyword', {}).get('text', '').lower()
        if 'aspinal' not in keyword_text:
            filtered.append(term)
        else:
            excluded_count += 1
            print(f"   ⊗ Excluded {account_name}: '{keyword_text}' (Aspinal term)")

    if excluded_count > 0:
        print(f"   Excluded {excluded_count} Aspinal terms from {account_name}")

    return filtered

def organize_by_campaign(terms):
    """Group terms by campaign"""
    campaigns = {}

    for term in terms:
        campaign_id = term.get('campaign', {}).get('id')
        campaign_name = term.get('campaign', {}).get('name')
        keyword_text = term.get('adGroupCriterion', {}).get('keyword', {}).get('text')
        clicks = term.get('metrics', {}).get('clicks', 0)
        cost_micros = term.get('metrics', {}).get('costMicros', 0)

        if campaign_id not in campaigns:
            campaigns[campaign_id] = {
                'name': campaign_name,
                'terms': []
            }

        campaigns[campaign_id]['terms'].append({
            'text': keyword_text,
            'clicks': int(clicks) if clicks else 0,
            'cost': int(cost_micros) / 1_000_000 if cost_micros else 0
        })

    return campaigns

def create_backup(account_name, customer_id, campaigns_data):
    """Create backup file before deployment"""
    backup = {
        "backup_created": datetime.now().isoformat(),
        "operation": f"Add Tier 1 negative keywords - {account_name}",
        "client": "smythson",
        "customer_id": customer_id,
        "manager_id": MANAGER_ID,
        "accounts_data": campaigns_data,
        "exclusions": "Aspinal terms excluded per user requirement"
    }

    backup_path = Path(__file__).parent.parent / f"reports/backup-tier1-deployment-{account_name.lower()}-2025-12-17.json"
    backup_path.write_text(json.dumps(backup, indent=2))
    print(f"\n✅ BACKUP created: {backup_path}")
    return str(backup_path)

def add_campaign_negative_keywords(customer_id, campaign_id, keywords):
    """Add negative keywords to a campaign"""
    try:
        formatted_customer_id = format_customer_id(customer_id)
        headers = get_headers_with_auto_token()
        headers['login-customer-id'] = format_customer_id(MANAGER_ID)

        campaign_resource = f"customers/{formatted_customer_id}/campaigns/{campaign_id}"
        operations = []

        for keyword_text in keywords:
            operations.append({
                "create": {
                    "campaign": campaign_resource,
                    "negative": True,
                    "keyword": {
                        "text": keyword_text,
                        "matchType": "EXACT"
                    }
                }
            })

        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/campaignCriteria:mutate"
        payload = {"operations": operations}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return len(result.get('results', []))

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

def main():
    print("🟢 **Smythson Tier 1 Negative Keyword Deployment**")
    print("=" * 70)
    print("Excluding Aspinal terms per user requirement\n")

    all_accounts_data = {}
    total_terms = 0

    # STEP 1: Query all accounts
    print("\n📊 STEP 1: Querying all accounts for Tier 1 terms")
    print("-" * 70)

    for account_name, customer_id in ACCOUNTS.items():
        terms = query_tier1_terms(customer_id, account_name)
        filtered_terms = filter_aspinal_terms(terms, account_name)
        campaigns_data = organize_by_campaign(filtered_terms)

        all_accounts_data[account_name] = {
            'customer_id': customer_id,
            'campaigns': campaigns_data,
            'total_terms': sum(len(c['terms']) for c in campaigns_data.values())
        }

        total_terms += all_accounts_data[account_name]['total_terms']

        if campaigns_data:
            print(f"\n   {account_name}: {all_accounts_data[account_name]['total_terms']} terms across {len(campaigns_data)} campaigns")

    print(f"\n✅ Total terms to deploy: {total_terms} (across {len(ACCOUNTS)} accounts)")

    if total_terms == 0:
        print("\n⚠️  No terms to deploy. Exiting.")
        return

    # STEP 2: Create backups
    print("\n💾 STEP 2: Creating backups")
    print("-" * 70)

    for account_name, data in all_accounts_data.items():
        if data['total_terms'] > 0:
            backup_path = create_backup(account_name, data['customer_id'], data['campaigns'])

    # STEP 3: Show deployment plan
    print("\n📋 STEP 3: Deployment Plan")
    print("-" * 70)

    for account_name, data in all_accounts_data.items():
        if data['total_terms'] > 0:
            print(f"\n{account_name} ({data['customer_id']}):")
            for campaign_id, campaign_data in data['campaigns'].items():
                print(f"   Campaign {campaign_id}: {campaign_data['name']}")
                print(f"   → Add {len(campaign_data['terms'])} negative keywords")
                total_cost = sum(t['cost'] for t in campaign_data['terms'])
                print(f"   → Projected savings: £{total_cost:.2f}/60 days = £{total_cost * 6:.2f}/year")

    # User already confirmed - proceed directly
    print("\n" + "=" * 70)
    print("✅ User confirmed - proceeding with deployment")
    print("=" * 70)

    # STEP 4: Execute deployment
    print("\n🚀 STEP 4: Executing deployment")
    print("-" * 70)

    total_deployed = 0

    for account_name, data in all_accounts_data.items():
        if data['total_terms'] > 0:
            print(f"\n{account_name} ({data['customer_id']}):")

            for campaign_id, campaign_data in data['campaigns'].items():
                keywords = [t['text'] for t in campaign_data['terms']]
                print(f"   Adding {len(keywords)} negatives to campaign {campaign_id}...")

                deployed_count = add_campaign_negative_keywords(
                    data['customer_id'],
                    campaign_id,
                    keywords
                )

                if deployed_count > 0:
                    print(f"   ✅ Added {deployed_count} negative keywords")
                    total_deployed += deployed_count
                else:
                    print(f"   ❌ Failed to add keywords")

    # STEP 5: Summary
    print("\n" + "=" * 70)
    print(f"✅ Deployment Complete: {total_deployed} negative keywords added")
    print("=" * 70)

    if total_deployed > 0:
        print("\n📝 Next Steps:")
        print("1. Monitor campaigns for 24-48 hours")
        print("2. Verify impressions reduced for excluded terms")
        print("3. Check for any unexpected traffic drops")
        print("4. Update tier2_tracker.json to mark terms as deployed")

if __name__ == "__main__":
    main()
