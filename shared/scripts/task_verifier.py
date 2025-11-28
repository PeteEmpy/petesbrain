#!/usr/bin/env python3
"""
Task Pre-Verification Module

Automatically verifies "check" and "verify" tasks before daily summary generation.
Pre-verified tasks are presented with actual data so user can quickly approve/close.

Verification Types:
1. Budget checks - Query Google Ads API for current budgets vs expected
2. Campaign status - Check if campaigns are running/paused as intended
3. Performance thresholds - Verify ROAS, CPA, etc. are within targets
4. Structural changes - Confirm settings are as configured

Usage:
    from task_verifier import pre_verify_task

    result = pre_verify_task(task)
    if result['verified']:
        print(f"✅ {result['summary']}")
        print(result['details'])
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Google Ads MCP client (will be imported when needed)
def get_google_ads_client():
    """Get Google Ads client data for all clients"""
    platform_ids_file = PROJECT_ROOT / 'data' / 'state' / 'client-platform-ids.json'

    if not platform_ids_file.exists():
        return None

    try:
        with open(platform_ids_file, 'r') as f:
            data = json.load(f)

        # Convert from array format to dict by client name
        clients_dict = {}
        for client in data.get('clients', []):
            client_name = client.get('name')
            if client_name:
                clients_dict[client_name] = client

        return clients_dict
    except:
        return None


def detect_verification_type(task_title: str, task_notes: str) -> Optional[str]:
    """
    Detect if a task is a verification task and what type.

    Returns:
        - 'budget_check' - Verify budget levels are correct
        - 'campaign_status' - Check if campaign is running/paused
        - 'performance_threshold' - Verify metrics are within range
        - 'setting_verification' - Confirm settings are as configured
        - None - Not a verifiable task
    """
    combined = f"{task_title} {task_notes}".lower()

    # Budget verification patterns
    budget_patterns = [
        r'verify.*budget',
        r'check.*budget',
        r'confirm.*budget',
        r'budget.*holding',
        r'budget.*still.*\d+',
        r'daily.*spend.*correct',
    ]

    for pattern in budget_patterns:
        if re.search(pattern, combined):
            return 'budget_check'

    # Campaign status patterns
    status_patterns = [
        r'verify.*campaign.*(running|paused|enabled|disabled)',
        r'check.*campaign.*(status|active)',
        r'confirm.*campaign.*(on|off)',
        r'is.*campaign.*still.*(running|paused)',
    ]

    for pattern in status_patterns:
        if re.search(pattern, combined):
            return 'campaign_status'

    # Performance threshold patterns
    threshold_patterns = [
        r'verify.*roas.*(above|below|at|within)',
        r'check.*cpa.*(under|over|at)',
        r'confirm.*performance.*target',
        r'is.*(roas|cpa|spend).*still.*\d+',
        # More flexible patterns for general performance checks
        r'check.*(roas|cpa).*performance',
        r'verify.*(roas|cpa)',
        r'review.*(roas|cpa)',
        r'check.*performance.*after.*(change|reduction|increase)',
        r'monitor.*(roas|cpa)',
        r'roas.*check',
        r'cpa.*check',
    ]

    for pattern in threshold_patterns:
        if re.search(pattern, combined):
            return 'performance_threshold'

    # Setting verification patterns
    setting_patterns = [
        r'verify.*setting',
        r'check.*configured',
        r'confirm.*(bid|target|limit)',
        r'is.*setting.*still',
    ]

    for pattern in setting_patterns:
        if re.search(pattern, combined):
            return 'setting_verification'

    return None


def extract_client_name(task_title: str, task_notes: str) -> Optional[str]:
    """Extract client name from task title or notes"""
    combined = f"{task_title} {task_notes}".lower()

    # Common client name patterns
    client_patterns = {
        'superspace': r'\bsuperspace\b',
        'smythson': r'\bsmythson\b',
        'tree2mydoor': r'\b(tree2mydoor|tree 2 my door|t2md)\b',
        'national-design-academy': r'\b(national design academy|nda)\b',
        'devonshire-hotels': r'\b(devonshire|devonshire hotels)\b',
        'accessories-for-the-home': r'\b(accessories for the home|accessories|afh)\b',
        'uno-lighting': r'\b(uno lighting|uno lights|uno)\b',
        'bright-minds': r'\b(bright minds|brightminds)\b',
        'go-glean': r'\b(go glean|goglean)\b',
        'grain-guard': r'\b(grain guard|grainguard)\b',
        'just-bin-bags': r'\b(just bin bags|jbb)\b',
        'crowd-control': r'\b(crowd control|crowdcontrol)\b',
        'clear-prospects': r'\b(clear prospects|clearprospects)\b',
        'godshot': r'\bgodshot\b',
        'positive-bakes': r'\b(positive bakes|positivebakes)\b',
    }

    for client_name, pattern in client_patterns.items():
        if re.search(pattern, combined):
            return client_name

    # Check if it's in [Client Name] format at start
    bracket_match = re.match(r'^\[([^\]]+)\]', task_title)
    if bracket_match:
        client_display = bracket_match.group(1).lower().replace(' ', '-')
        # Try to match to known clients
        for client_name, pattern in client_patterns.items():
            if client_display in client_name or client_name in client_display:
                return client_name

    return None


def verify_budget_check(client_name: str, task_title: str, task_notes: str) -> Dict:
    """
    Verify budget levels for a client.

    Returns dict with:
        - verified: bool
        - status: 'success' | 'warning' | 'error'
        - summary: str (one-line summary)
        - details: str (formatted details)
        - data: dict (raw verification data)
    """
    try:
        # Get client's Google Ads customer ID
        platform_ids = get_google_ads_client()
        if not platform_ids:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Unable to load platform IDs',
                'details': 'client-platform-ids.json not found',
                'data': {}
            }

        client_data = platform_ids.get(client_name, {})
        customer_id = client_data.get('google_ads_customer_id')

        if not customer_id:
            return {
                'verified': False,
                'status': 'error',
                'summary': f'No Google Ads customer ID for {client_name}',
                'details': f'Add google_ads_customer_id to platform IDs file',
                'data': {}
            }

        # Query Google Ads API for budget data
        try:
            # Use subprocess to call Google Ads via MCP-like approach
            # Import the Google Ads library that daily-briefing.py uses
            import subprocess
            import json

            # Create a Python script that queries Google Ads
            query_script = f"""
import sys
import os
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

config_file = os.path.expanduser('~/google-ads.yaml')
client = GoogleAdsClient.load_from_storage(config_file)
ga_service = client.get_service("GoogleAdsService")

query = '''
SELECT
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_7_DAYS
ORDER BY campaign.name
'''

search_request = client.get_type("SearchGoogleAdsRequest")
search_request.customer_id = '{customer_id}'
search_request.query = query

response = ga_service.search(request=search_request)

results = []
for row in response:
    results.append({{
        'campaign_name': row.campaign.name,
        'budget_micros': row.campaign_budget.amount_micros,
        'cost_micros': row.metrics.cost_micros
    }})

import json
print(json.dumps({{'results': results}}))
"""

            # Write temp script
            temp_script = PROJECT_ROOT / 'shared' / 'tmp_query.py'
            with open(temp_script, 'w') as f:
                f.write(query_script)

            # Run with product-impact-analyzer's venv (has google-ads library installed)
            result = subprocess.run(
                [str(PROJECT_ROOT / 'tools' / 'product-impact-analyzer' / '.venv' / 'bin' / 'python3'), str(temp_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Clean up temp script
            if temp_script.exists():
                temp_script.unlink()

            if result.returncode != 0:
                return {
                    'verified': False,
                    'status': 'error',
                    'summary': 'Google Ads API query failed',
                    'details': f'Error: {result.stderr}',
                    'data': {}
                }

            # Parse results
            result_data = json.loads(result.stdout)

        except Exception as e:
            return {
                'verified': False,
                'status': 'error',
                'summary': f'API query error: {str(e)}',
                'details': f'Failed to query Google Ads API: {str(e)}',
                'data': {}
            }

        result = result_data

        if 'error' in result:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Google Ads API error',
                'details': result['error'],
                'data': {}
            }

        # Aggregate campaign data
        campaigns = result.get('results', [])

        if not campaigns:
            return {
                'verified': True,
                'status': 'warning',
                'summary': 'No enabled campaigns found',
                'details': f'No active campaigns in last 7 days for {client_name}',
                'data': {}
            }

        # Calculate total daily budgets and actual spend
        total_budget_micros = 0
        total_spend_micros = 0
        campaign_count = 0

        campaign_details = []

        # Group by campaign to avoid duplication (GAQL returns one row per day)
        campaigns_by_name = {}
        for row in campaigns:
            campaign_name = row['campaign_name']
            if campaign_name not in campaigns_by_name:
                campaigns_by_name[campaign_name] = {
                    'name': campaign_name,
                    'budget_micros': row['budget_micros'],
                    'spend_micros': 0
                }
            campaigns_by_name[campaign_name]['spend_micros'] += row['cost_micros']

        for campaign_data in campaigns_by_name.values():
            total_budget_micros += int(campaign_data['budget_micros'])
            total_spend_micros += int(campaign_data['spend_micros'])
            campaign_count += 1

            campaign_details.append({
                'name': campaign_data['name'],
                'budget_daily': int(campaign_data['budget_micros']) / 1_000_000,
                'spend_7days': int(campaign_data['spend_micros']) / 1_000_000,
            })

        # Convert to currency
        total_budget_daily = total_budget_micros / 1_000_000
        total_spend_7days = total_spend_micros / 1_000_000
        avg_spend_daily = total_spend_7days / 7

        # Format summary
        summary = f"{client_name.replace('-', ' ').title()}: £{avg_spend_daily:.0f}/day average spend (budget: £{total_budget_daily:.0f}/day)"

        # Format details
        details = f"""**Budget Verification** (Last 7 Days)

**Total Daily Budgets:** £{total_budget_daily:.0f}
**Average Daily Spend:** £{avg_spend_daily:.0f} ({(avg_spend_daily/total_budget_daily*100):.1f}% of budget)
**Total Spend (7 days):** £{total_spend_7days:.0f}

**Campaigns:** {campaign_count} active campaigns
"""

        # Add top campaigns
        campaign_details.sort(key=lambda x: x['budget_daily'], reverse=True)
        if campaign_details:
            details += "\n**Top Campaigns by Budget:**\n"
            for campaign in campaign_details[:5]:
                details += f"- {campaign['name']}: £{campaign['budget_daily']:.0f}/day budget\n"

        return {
            'verified': True,
            'status': 'success',
            'summary': summary,
            'details': details,
            'data': {
                'total_budget_daily': total_budget_daily,
                'avg_spend_daily': avg_spend_daily,
                'total_spend_7days': total_spend_7days,
                'campaign_count': campaign_count,
                'campaigns': campaign_details
            }
        }

    except Exception as e:
        return {
            'verified': False,
            'status': 'error',
            'summary': f'Verification failed: {str(e)}',
            'details': f'Error: {str(e)}',
            'data': {}
        }


def fetch_client_budget_data(client_name: str) -> Dict:
    """
    Fetch budget data for a client once, to be reused for multiple task verifications.

    Args:
        client_name: Client name (e.g., 'superspace')

    Returns:
        Dict with 'results' (list of campaign data) or 'error' (str)
    """
    try:
        # Get client's Google Ads customer ID
        platform_ids = get_google_ads_client()
        if not platform_ids:
            return {'error': 'Unable to load platform IDs'}

        client_data = platform_ids.get(client_name, {})
        customer_id = client_data.get('google_ads_customer_id')

        if not customer_id:
            return {'error': f'No Google Ads customer ID for {client_name}'}

        # Query Google Ads API for budget data
        try:
            import subprocess
            import json

            # Create a Python script that queries Google Ads
            query_script = f"""
import sys
import os
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

config_file = os.path.expanduser('~/google-ads.yaml')
client = GoogleAdsClient.load_from_storage(config_file)
ga_service = client.get_service("GoogleAdsService")

query = '''
SELECT
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_7_DAYS
ORDER BY campaign.name
'''

search_request = client.get_type("SearchGoogleAdsRequest")
search_request.customer_id = '{customer_id}'
search_request.query = query

response = ga_service.search(request=search_request)

results = []
for row in response:
    results.append({{
        'campaign_name': row.campaign.name,
        'budget_micros': row.campaign_budget.amount_micros,
        'cost_micros': row.metrics.cost_micros
    }})

import json
print(json.dumps({{'results': results}}))
"""

            # Write temp script
            temp_script = PROJECT_ROOT / 'shared' / 'tmp_query.py'
            with open(temp_script, 'w') as f:
                f.write(query_script)

            # Run with product-impact-analyzer's venv (has google-ads library installed)
            result = subprocess.run(
                [str(PROJECT_ROOT / 'tools' / 'product-impact-analyzer' / '.venv' / 'bin' / 'python3'), str(temp_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Clean up temp script
            if temp_script.exists():
                temp_script.unlink()

            if result.returncode != 0:
                return {'error': f'Google Ads API query failed: {result.stderr}'}

            # Parse results
            result_data = json.loads(result.stdout)
            return result_data

        except Exception as e:
            return {'error': f'API query error: {str(e)}'}

    except Exception as e:
        return {'error': f'Fetch error: {str(e)}'}


def verify_budget_check_with_cached_data(client_name: str, task_title: str, task_notes: str, cached_data: Dict) -> Dict:
    """
    Verify budget levels using pre-fetched data (no API call).

    Args:
        client_name: Client name
        task_title: Task title
        task_notes: Task notes
        cached_data: Pre-fetched budget data from fetch_client_budget_data()

    Returns:
        Verification result dict (same format as verify_budget_check)
    """
    try:
        if 'error' in cached_data:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Google Ads API error',
                'details': cached_data['error'],
                'data': {}
            }

        # Aggregate campaign data
        campaigns = cached_data.get('results', [])

        if not campaigns:
            return {
                'verified': True,
                'status': 'warning',
                'summary': 'No enabled campaigns found',
                'details': f'No active campaigns in last 7 days for {client_name}',
                'data': {}
            }

        # Calculate total daily budgets and actual spend
        total_budget_micros = 0
        total_spend_micros = 0
        campaign_count = 0

        campaign_details = []

        # Group by campaign to avoid duplication (GAQL returns one row per day)
        campaigns_by_name = {}
        for row in campaigns:
            campaign_name = row['campaign_name']
            if campaign_name not in campaigns_by_name:
                campaigns_by_name[campaign_name] = {
                    'name': campaign_name,
                    'budget_micros': row['budget_micros'],
                    'spend_micros': 0
                }
            campaigns_by_name[campaign_name]['spend_micros'] += row['cost_micros']

        for campaign_data in campaigns_by_name.values():
            total_budget_micros += int(campaign_data['budget_micros'])
            total_spend_micros += int(campaign_data['spend_micros'])
            campaign_count += 1

            campaign_details.append({
                'name': campaign_data['name'],
                'budget_daily': int(campaign_data['budget_micros']) / 1_000_000,
                'spend_7days': int(campaign_data['spend_micros']) / 1_000_000,
            })

        # Convert to currency
        total_budget_daily = total_budget_micros / 1_000_000
        total_spend_7days = total_spend_micros / 1_000_000
        avg_spend_daily = total_spend_7days / 7

        # Format summary
        summary = f"{client_name.replace('-', ' ').title()}: £{avg_spend_daily:.0f}/day average spend (budget: £{total_budget_daily:.0f}/day)"

        # Format details
        details = f"""**Budget Verification** (Last 7 Days)

**Total Daily Budgets:** £{total_budget_daily:.0f}
**Average Daily Spend:** £{avg_spend_daily:.0f} ({(avg_spend_daily/total_budget_daily*100):.1f}% of budget)
**Total Spend (7 days):** £{total_spend_7days:.0f}

**Campaigns:** {campaign_count} active campaigns
"""

        # Add top campaigns
        campaign_details.sort(key=lambda x: x['budget_daily'], reverse=True)
        if campaign_details:
            details += "\n**Top Campaigns by Budget:**\n"
            for campaign in campaign_details[:5]:
                details += f"- {campaign['name']}: £{campaign['budget_daily']:.0f}/day budget\n"

        return {
            'verified': True,
            'status': 'success',
            'summary': summary,
            'details': details,
            'data': {
                'total_budget_daily': total_budget_daily,
                'avg_spend_daily': avg_spend_daily,
                'total_spend_7days': total_spend_7days,
                'campaign_count': campaign_count,
                'campaigns': campaign_details
            }
        }

    except Exception as e:
        return {
            'verified': False,
            'status': 'error',
            'summary': f'Verification failed: {str(e)}',
            'details': f'Error: {str(e)}',
            'data': {}
        }


def fetch_client_campaign_data(client_name: str) -> Dict:
    """
    Fetch campaign status and settings data for a client.

    Args:
        client_name: Client name (e.g., 'superspace')

    Returns:
        Dict with 'results' (list of campaign data) or 'error' (str)
    """
    try:
        # Get client's Google Ads customer ID
        platform_ids = get_google_ads_client()
        if not platform_ids:
            return {'error': 'Unable to load platform IDs'}

        client_data = platform_ids.get(client_name, {})
        customer_id = client_data.get('google_ads_customer_id')

        if not customer_id:
            return {'error': f'No Google Ads customer ID for {client_name}'}

        # Query Google Ads API for campaign status and settings
        try:
            import subprocess
            import json

            query_script = f"""
import sys
import os
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

config_file = os.path.expanduser('~/google-ads.yaml')
client = GoogleAdsClient.load_from_storage(config_file)
ga_service = client.get_service("GoogleAdsService")

query = '''
SELECT
  campaign.name,
  campaign.status,
  campaign_budget.amount_micros,
  metrics.conversions_value,
  metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
ORDER BY campaign.name
'''

search_request = client.get_type("SearchGoogleAdsRequest")
search_request.customer_id = '{customer_id}'
search_request.query = query

response = ga_service.search(request=search_request)

results = []
for row in response:
    results.append({{
        'campaign_name': row.campaign.name,
        'status': row.campaign.status.name,
        'budget_micros': row.campaign_budget.amount_micros,
        'conversions_value': row.metrics.conversions_value,
        'cost_micros': row.metrics.cost_micros
    }})

import json
print(json.dumps({{'results': results}}))
"""

            temp_script = PROJECT_ROOT / 'shared' / 'tmp_query.py'
            with open(temp_script, 'w') as f:
                f.write(query_script)

            # Run with product-impact-analyzer's venv (has google-ads library installed)
            result = subprocess.run(
                [str(PROJECT_ROOT / 'tools' / 'product-impact-analyzer' / '.venv' / 'bin' / 'python3'), str(temp_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Clean up temp script
            if temp_script.exists():
                temp_script.unlink()

            if result.returncode != 0:
                return {'error': f'Google Ads API query failed: {result.stderr}'}

            result_data = json.loads(result.stdout)
            return result_data

        except Exception as e:
            return {'error': f'API query error: {str(e)}'}

    except Exception as e:
        return {'error': f'Fetch error: {str(e)}'}


def verify_campaign_status_with_cached_data(client_name: str, task_title: str, task_notes: str, cached_data: Dict) -> Dict:
    """
    Verify campaign status using pre-fetched data.

    Args:
        client_name: Client name
        task_title: Task title
        task_notes: Task notes
        cached_data: Pre-fetched campaign data

    Returns:
        Verification result dict
    """
    try:
        if 'error' in cached_data:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Google Ads API error',
                'details': cached_data['error'],
                'data': {}
            }

        campaigns = cached_data.get('results', [])

        if not campaigns:
            return {
                'verified': True,
                'status': 'warning',
                'summary': 'No campaigns found',
                'details': f'No campaigns found for {client_name}',
                'data': {}
            }

        # Extract expected campaign name from task title/notes
        # Look for patterns like "Campaign X" or quoted campaign names
        combined = f"{task_title} {task_notes}"
        campaign_name_match = re.search(r'campaign[:\s]+["\']?([^"\']+?)["\']?\s+(?:is|should|still)', combined, re.IGNORECASE)

        if not campaign_name_match:
            # Try alternative pattern
            campaign_name_match = re.search(r'verify.*?["\']([^"\']+)["\'].*?campaign', combined, re.IGNORECASE)

        if campaign_name_match:
            expected_campaign = campaign_name_match.group(1).strip()

            # Find matching campaign (fuzzy match)
            matching_campaign = None
            for camp in campaigns:
                if expected_campaign.lower() in camp['campaign_name'].lower():
                    matching_campaign = camp
                    break

            if matching_campaign:
                status = matching_campaign['status']
                campaign_name = matching_campaign['campaign_name']

                # Determine if status matches expectation
                status_ok = True
                expected_status = None

                if 'paused' in combined.lower() or 'disabled' in combined.lower():
                    expected_status = 'PAUSED'
                    status_ok = (status == 'PAUSED')
                elif 'running' in combined.lower() or 'enabled' in combined.lower() or 'active' in combined.lower():
                    expected_status = 'ENABLED'
                    status_ok = (status == 'ENABLED')

                result_status = 'success' if status_ok else 'warning'
                summary = f"{campaign_name}: {status}" + (" ✓" if status_ok else " (unexpected)")

                details = f"""**Campaign Status Verification**

**Campaign:** {campaign_name}
**Current Status:** {status}
"""
                if expected_status:
                    details += f"**Expected Status:** {expected_status}\n"
                    details += f"**Match:** {'✓ Yes' if status_ok else '✗ No'}\n"

                return {
                    'verified': True,
                    'status': result_status,
                    'summary': summary,
                    'details': details,
                    'data': {
                        'campaign_name': campaign_name,
                        'status': status,
                        'expected_status': expected_status,
                        'status_ok': status_ok
                    }
                }

        # If no specific campaign identified, show all campaign statuses
        summary = f"{client_name.replace('-', ' ').title()}: {len(campaigns)} campaigns"

        details = f"""**Campaign Status Overview**

**Total Campaigns:** {len(campaigns)}

"""

        status_counts = {}
        for camp in campaigns:
            status = camp['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        for status, count in sorted(status_counts.items()):
            details += f"- {status}: {count} campaigns\n"

        return {
            'verified': True,
            'status': 'success',
            'summary': summary,
            'details': details,
            'data': {
                'total_campaigns': len(campaigns),
                'status_counts': status_counts
            }
        }

    except Exception as e:
        return {
            'verified': False,
            'status': 'error',
            'summary': f'Verification failed: {str(e)}',
            'details': f'Error: {str(e)}',
            'data': {}
        }


def verify_performance_threshold_with_cached_data(client_name: str, task_title: str, task_notes: str, cached_data: Dict) -> Dict:
    """
    Verify performance thresholds (ROAS, CPA) using pre-fetched data.

    Args:
        client_name: Client name
        task_title: Task title
        task_notes: Task notes
        cached_data: Pre-fetched campaign data

    Returns:
        Verification result dict
    """
    try:
        if 'error' in cached_data:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Google Ads API error',
                'details': cached_data['error'],
                'data': {}
            }

        campaigns = cached_data.get('results', [])

        if not campaigns:
            return {
                'verified': True,
                'status': 'warning',
                'summary': 'No campaigns found',
                'details': f'No campaigns found for {client_name}',
                'data': {}
            }

        # Aggregate performance across all campaigns
        campaigns_by_name = {}
        for row in campaigns:
            campaign_name = row['campaign_name']
            if campaign_name not in campaigns_by_name:
                campaigns_by_name[campaign_name] = {
                    'name': campaign_name,
                    'status': row['status'],
                    'conversions_value': 0,
                    'cost': 0
                }
            campaigns_by_name[campaign_name]['conversions_value'] += row.get('conversions_value', 0)
            campaigns_by_name[campaign_name]['cost'] += row.get('cost_micros', 0)

        # Calculate ROAS for each campaign
        campaign_performance = []
        total_cost = 0
        total_conv_value = 0

        for camp_data in campaigns_by_name.values():
            cost = camp_data['cost'] / 1_000_000
            conv_value = camp_data['conversions_value']
            roas = (conv_value / cost * 100) if cost > 0 else 0

            campaign_performance.append({
                'name': camp_data['name'],
                'status': camp_data['status'],
                'cost': cost,
                'conv_value': conv_value,
                'roas': roas
            })

            total_cost += cost
            total_conv_value += conv_value

        overall_roas = (total_conv_value / total_cost * 100) if total_cost > 0 else 0

        # Extract threshold from task
        combined = f"{task_title} {task_notes}"
        threshold_match = re.search(r'(\d+(?:\.\d+)?)\s*%', combined)

        threshold = None
        threshold_met = None
        if threshold_match:
            threshold = float(threshold_match.group(1))

            # Determine if "above" or "below"
            if 'above' in combined.lower() or 'over' in combined.lower():
                threshold_met = overall_roas >= threshold
            elif 'below' in combined.lower() or 'under' in combined.lower():
                threshold_met = overall_roas <= threshold
            else:
                # Default: assume "at least"
                threshold_met = overall_roas >= threshold

        result_status = 'success' if (threshold_met is None or threshold_met) else 'warning'
        summary = f"{client_name.replace('-', ' ').title()}: {overall_roas:.0f}% ROAS (last 7 days)"
        if threshold and threshold_met is not None:
            summary += " ✓" if threshold_met else f" (below {threshold}%)"

        details = f"""**Performance Threshold Verification** (Last 7 Days)

**Overall ROAS:** {overall_roas:.0f}%
**Total Spend:** £{total_cost:.2f}
**Total Conv Value:** £{total_conv_value:.2f}
"""

        if threshold:
            details += f"\n**Threshold:** {threshold}% ROAS\n"
            details += f"**Met:** {'✓ Yes' if threshold_met else '✗ No'}\n"

        # Add top campaigns
        campaign_performance.sort(key=lambda x: x['roas'], reverse=True)
        details += "\n**Top Campaigns by ROAS:**\n"
        for camp in campaign_performance[:5]:
            if camp['status'] == 'ENABLED':
                details += f"- {camp['name']}: {camp['roas']:.0f}% ROAS\n"

        return {
            'verified': True,
            'status': result_status,
            'summary': summary,
            'details': details,
            'data': {
                'overall_roas': overall_roas,
                'total_cost': total_cost,
                'total_conv_value': total_conv_value,
                'threshold': threshold,
                'threshold_met': threshold_met,
                'campaigns': campaign_performance
            }
        }

    except Exception as e:
        return {
            'verified': False,
            'status': 'error',
            'summary': f'Verification failed: {str(e)}',
            'details': f'Error: {str(e)}',
            'data': {}
        }


def verify_setting_with_cached_data(client_name: str, task_title: str, task_notes: str, cached_data: Dict) -> Dict:
    """
    Verify campaign settings (target ROAS, target CPA) using pre-fetched data.

    Args:
        client_name: Client name
        task_title: Task title
        task_notes: Task notes
        cached_data: Pre-fetched campaign data

    Returns:
        Verification result dict
    """
    try:
        if 'error' in cached_data:
            return {
                'verified': False,
                'status': 'error',
                'summary': 'Google Ads API error',
                'details': cached_data['error'],
                'data': {}
            }

        campaigns = cached_data.get('results', [])

        if not campaigns:
            return {
                'verified': True,
                'status': 'warning',
                'summary': 'No campaigns found',
                'details': f'No campaigns found for {client_name}',
                'data': {}
            }

        # Group campaigns to get unique campaign settings
        campaigns_by_name = {}
        for row in campaigns:
            campaign_name = row['campaign_name']
            if campaign_name not in campaigns_by_name:
                campaigns_by_name[campaign_name] = {
                    'name': campaign_name,
                    'status': row['status'],
                    'target_roas': row.get('target_roas'),
                    'target_cpa_micros': row.get('target_cpa_micros')
                }

        # Extract expected setting from task
        combined = f"{task_title} {task_notes}"

        # Check for target ROAS
        roas_match = re.search(r'(?:target\s+)?roas.*?(\d+(?:\.\d+)?)\s*%?', combined, re.IGNORECASE)
        cpa_match = re.search(r'(?:target\s+)?cpa.*?£?(\d+(?:\.\d+)?)', combined, re.IGNORECASE)

        if roas_match:
            expected_roas = float(roas_match.group(1))

            # Find campaigns with target ROAS
            roas_campaigns = []
            for camp_data in campaigns_by_name.values():
                if camp_data['target_roas']:
                    roas_campaigns.append({
                        'name': camp_data['name'],
                        'target_roas': camp_data['target_roas'],
                        'matches': abs(camp_data['target_roas'] - expected_roas) < 0.1
                    })

            matches = sum(1 for c in roas_campaigns if c['matches'])
            result_status = 'success' if matches == len(roas_campaigns) else 'warning'
            summary = f"{len(roas_campaigns)} campaigns with target ROAS: {matches}/{len(roas_campaigns)} match {expected_roas}%"

            details = f"""**Settings Verification - Target ROAS**

**Expected Target ROAS:** {expected_roas}%
**Campaigns Found:** {len(roas_campaigns)}
**Matching:** {matches}/{len(roas_campaigns)}

"""
            if roas_campaigns:
                details += "**Campaign Settings:**\n"
                for camp in roas_campaigns[:10]:
                    match_icon = "✓" if camp['matches'] else "✗"
                    details += f"- {match_icon} {camp['name']}: {camp['target_roas']}%\n"

            return {
                'verified': True,
                'status': result_status,
                'summary': summary,
                'details': details,
                'data': {
                    'expected_roas': expected_roas,
                    'campaigns': roas_campaigns,
                    'matches': matches
                }
            }

        elif cpa_match:
            expected_cpa = float(cpa_match.group(1))

            # Find campaigns with target CPA
            cpa_campaigns = []
            for camp_data in campaigns_by_name.values():
                if camp_data['target_cpa_micros']:
                    target_cpa = camp_data['target_cpa_micros'] / 1_000_000
                    cpa_campaigns.append({
                        'name': camp_data['name'],
                        'target_cpa': target_cpa,
                        'matches': abs(target_cpa - expected_cpa) < 0.01
                    })

            matches = sum(1 for c in cpa_campaigns if c['matches'])
            result_status = 'success' if matches == len(cpa_campaigns) else 'warning'
            summary = f"{len(cpa_campaigns)} campaigns with target CPA: {matches}/{len(cpa_campaigns)} match £{expected_cpa}"

            details = f"""**Settings Verification - Target CPA**

**Expected Target CPA:** £{expected_cpa}
**Campaigns Found:** {len(cpa_campaigns)}
**Matching:** {matches}/{len(cpa_campaigns)}

"""
            if cpa_campaigns:
                details += "**Campaign Settings:**\n"
                for camp in cpa_campaigns[:10]:
                    match_icon = "✓" if camp['matches'] else "✗"
                    details += f"- {match_icon} {camp['name']}: £{camp['target_cpa']:.2f}\n"

            return {
                'verified': True,
                'status': result_status,
                'summary': summary,
                'details': details,
                'data': {
                    'expected_cpa': expected_cpa,
                    'campaigns': cpa_campaigns,
                    'matches': matches
                }
            }

        # Default: show all campaign settings
        summary = f"{client_name.replace('-', ' ').title()}: Campaign settings overview"

        details = f"""**Campaign Settings Overview**

**Total Campaigns:** {len(campaigns_by_name)}

"""

        roas_count = sum(1 for c in campaigns_by_name.values() if c['target_roas'])
        cpa_count = sum(1 for c in campaigns_by_name.values() if c['target_cpa_micros'])

        details += f"**Target ROAS campaigns:** {roas_count}\n"
        details += f"**Target CPA campaigns:** {cpa_count}\n"

        return {
            'verified': True,
            'status': 'success',
            'summary': summary,
            'details': details,
            'data': {
                'total_campaigns': len(campaigns_by_name),
                'roas_count': roas_count,
                'cpa_count': cpa_count
            }
        }

    except Exception as e:
        return {
            'verified': False,
            'status': 'error',
            'summary': f'Verification failed: {str(e)}',
            'details': f'Error: {str(e)}',
            'data': {}
        }


def batch_pre_verify_tasks(tasks: List[Dict]) -> List[Dict]:
    """
    Pre-verify multiple tasks efficiently by batching API calls per client.

    This is the preferred method when verifying multiple tasks, as it:
    - Groups tasks by client
    - Makes only ONE API call per client
    - Reuses cached data for all tasks from the same client

    Args:
        tasks: List of task dicts with 'title' and 'notes' keys

    Returns:
        List of tasks with '_verification' key added to verifiable tasks
    """
    from collections import defaultdict

    # Group tasks by client and verification type
    tasks_by_client = defaultdict(list)
    task_metadata = {}  # Store verification type and client for each task

    for i, task in enumerate(tasks):
        title = task.get('title', '')
        notes = task.get('notes', '')

        # Detect verification type
        verification_type = detect_verification_type(title, notes)
        if not verification_type:
            continue

        # Extract client name
        client_name = extract_client_name(title, notes)
        if not client_name:
            continue

        # Store metadata for this task
        task_metadata[i] = {
            'verification_type': verification_type,
            'client_name': client_name
        }

        # Group by client
        tasks_by_client[client_name].append(i)

    # Determine which data types to fetch per client
    client_data_needs = defaultdict(set)
    for metadata in task_metadata.values():
        client_name = metadata['client_name']
        verification_type = metadata['verification_type']

        if verification_type == 'budget_check':
            client_data_needs[client_name].add('budget')
        elif verification_type in ['campaign_status', 'performance_threshold', 'setting_verification']:
            client_data_needs[client_name].add('campaign')

    # Fetch data once per client (budget or campaign data)
    client_budget_cache = {}
    client_campaign_cache = {}
    api_call_count = 0

    for client_name, data_types in client_data_needs.items():
        print(f"    Fetching data for {client_name}...")

        if 'budget' in data_types:
            client_budget_cache[client_name] = fetch_client_budget_data(client_name)
            api_call_count += 1

        if 'campaign' in data_types:
            client_campaign_cache[client_name] = fetch_client_campaign_data(client_name)
            api_call_count += 1

    # Verify all tasks using cached data
    verified_count = 0
    for task_idx, metadata in task_metadata.items():
        client_name = metadata['client_name']
        verification_type = metadata['verification_type']
        task = tasks[task_idx]

        # Use appropriate cached data for verification
        verification = None

        if verification_type == 'budget_check':
            verification = verify_budget_check_with_cached_data(
                client_name,
                task.get('title', ''),
                task.get('notes', ''),
                client_budget_cache.get(client_name, {})
            )
        elif verification_type == 'campaign_status':
            verification = verify_campaign_status_with_cached_data(
                client_name,
                task.get('title', ''),
                task.get('notes', ''),
                client_campaign_cache.get(client_name, {})
            )
        elif verification_type == 'performance_threshold':
            verification = verify_performance_threshold_with_cached_data(
                client_name,
                task.get('title', ''),
                task.get('notes', ''),
                client_campaign_cache.get(client_name, {})
            )
        elif verification_type == 'setting_verification':
            verification = verify_setting_with_cached_data(
                client_name,
                task.get('title', ''),
                task.get('notes', ''),
                client_campaign_cache.get(client_name, {})
            )

        if verification:
            task['_verification'] = verification
            verified_count += 1

    print(f"    ✓ Pre-verified {verified_count} tasks with {api_call_count} API calls (instead of {verified_count})")

    return tasks


def pre_verify_task(task: Dict) -> Optional[Dict]:
    """
    Pre-verify a single task if it's a verifiable type.

    NOTE: For multiple tasks, use batch_pre_verify_tasks() instead for better performance.

    Args:
        task: Task dict with 'title' and 'notes' keys

    Returns:
        Verification result dict if task is verifiable, None otherwise
    """
    title = task.get('title', '')
    notes = task.get('notes', '')

    # Detect verification type
    verification_type = detect_verification_type(title, notes)

    if not verification_type:
        return None

    # Extract client name
    client_name = extract_client_name(title, notes)

    if not client_name:
        return None

    # Run appropriate verification
    if verification_type == 'budget_check':
        return verify_budget_check(client_name, title, notes)

    # TODO: Add other verification types
    # elif verification_type == 'campaign_status':
    #     return verify_campaign_status(client_name, title, notes)

    return None


def format_verification_for_email(task: Dict, verification: Dict) -> str:
    """
    Format a pre-verified task for inclusion in daily summary email.

    Args:
        task: Original task dict
        verification: Verification result dict

    Returns:
        Formatted string for email
    """
    title = task.get('title', 'Untitled')
    status_emoji = {
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }.get(verification['status'], '📋')

    output = f"""### {status_emoji} {title} [PRE-VERIFIED]

**Status:** {verification['summary']}

{verification['details']}

→ **Action**: Reply with client name + "verified - close" to complete this task
"""

    return output


if __name__ == '__main__':
    # Test with Superspace budget verification
    test_task = {
        'title': '[Superspace] Check current stock levels and verify budget reduction implementation',
        'notes': 'Stock shortage identified in October with budgets reduced 50%, need to confirm proper budget controls are in place to prevent overspending during inventory constraints'
    }

    print("Testing task pre-verification...")
    print(f"Task: {test_task['title']}")
    print()

    result = pre_verify_task(test_task)

    if result:
        print("✅ Verification completed!")
        print()
        print(format_verification_for_email(test_task, result))
    else:
        print("❌ Task is not verifiable")
