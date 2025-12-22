#!/usr/bin/env python3
"""
Enhanced Tier System Weekly Monitor

Comprehensive weekly monitoring that:
1. Checks existing Tier 2 terms for promotion to Tier 1
2. Runs fresh 7-day search term analysis to find NEW Tier 1/Tier 2 terms
3. Auto-adds new terms to tracker
4. Generates summary for daily briefing email
5. Creates consolidated tasks for bi-weekly Tier 1 deployment and monthly Tier 2 review

Runs every Monday at 9:00 AM via LaunchAgent
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import calendar

# Add MCP server to path
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient

# Add tier2_tracker functions
sys.path.insert(0, str(Path(__file__).parent))
from tier2_tracker import (
    load_tracker_data,
    save_tracker_data,
    check_term_status,
    check_client_terms
)

# Add shared modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from client_tasks_service import ClientTasksService

# Notification file for daily briefing integration
NOTIFICATION_FILE = Path(__file__).parent.parent / 'data' / 'state' / 'tier-alerts.json'
CONFIG_FILE = Path(__file__).parent / 'tier-system-config.json'


def get_7_day_search_terms(customer_id: str, manager_id: str = "2569949686") -> List[Dict]:
    """
    Get all search terms from last 7 days with 10+ clicks.

    Returns list of dicts with: search_term, clicks, conversions, cost, campaign_name
    """
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.name,
            metrics.clicks,
            metrics.conversions,
            metrics.cost_micros
        FROM search_term_view
        WHERE segments.date >= '{start_date.strftime('%Y-%m-%d')}'
          AND segments.date <= '{end_date.strftime('%Y-%m-%d')}'
          AND metrics.clicks >= 10
        ORDER BY metrics.clicks DESC
    """

    try:
        # Use login-customer-id for manager account access
        response = ga_service.search(
            customer_id=customer_id,
            query=query,
            login_customer_id=manager_id if manager_id else None
        )

        results = []
        for row in response:
            results.append({
                'search_term': row.search_term_view.search_term,
                'campaign_name': row.campaign.name,
                'clicks': row.metrics.clicks,
                'conversions': row.metrics.conversions,
                'cost': row.metrics.cost_micros / 1_000_000
            })

        return results

    except Exception as e:
        print(f"⚠️  Error fetching 7-day search terms for {customer_id}: {e}")
        return []


def classify_search_terms(terms: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Classify search terms into Tier 1 (30+) and Tier 2 (10-29).
    Only include terms with 0 conversions.

    Returns: (tier1_terms, tier2_terms)
    """
    tier1 = []
    tier2 = []

    for term in terms:
        if term['conversions'] > 0:
            continue  # Skip converting terms

        if term['clicks'] >= 30:
            tier1.append(term)
        elif term['clicks'] >= 10:
            tier2.append(term)

    return tier1, tier2


def find_new_terms(all_terms: List[Dict], existing_tracker: Dict, client_slug: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Identify terms that are NOT already in tracker.

    Returns: (new_tier1_terms, new_tier2_terms)
    """
    # Get existing terms for this client
    existing_terms = set()
    if client_slug in existing_tracker.get('clients', {}):
        for term_data in existing_tracker['clients'][client_slug].get('terms', []):
            existing_terms.add(term_data['search_term'])

    # Classify and filter
    tier1_all, tier2_all = classify_search_terms(all_terms)

    new_tier1 = [t for t in tier1_all if t['search_term'] not in existing_terms]
    new_tier2 = [t for t in tier2_all if t['search_term'] not in existing_terms]

    return new_tier1, new_tier2


def add_new_terms_to_tracker(
    new_tier1: List[Dict],
    new_tier2: List[Dict],
    tracker_data: Dict,
    client_slug: str,
    customer_id: str
) -> int:
    """
    Add newly discovered terms to tracker.

    Tier 1 terms: Mark as 'promoted_tier1' immediately
    Tier 2 terms: Add to monitoring with 7-day review date

    Returns: Count of terms added
    """
    if client_slug not in tracker_data['clients']:
        tracker_data['clients'][client_slug] = {
            'customer_id': customer_id,
            'terms': []
        }

    client_data = tracker_data['clients'][client_slug]
    added_count = 0

    # Add Tier 1 terms (already high confidence)
    for term in new_tier1:
        new_term = {
            'search_term': term['search_term'],
            'clicks': term['clicks'],
            'cost': term['cost'],
            'conversions': 0,
            'campaign_name': term['campaign_name'],
            'match_type': 'Unknown',
            'added_date': datetime.now().isoformat(),
            'next_review_date': datetime.now().strftime('%Y-%m-%d'),  # Immediate review
            'status': 'promoted_tier1',  # Already meets criteria
            'last_checked': datetime.now().isoformat(),
            'promoted_date': datetime.now().isoformat()
        }
        client_data['terms'].append(new_term)
        added_count += 1

    # Add Tier 2 terms (need monitoring)
    for term in new_tier2:
        new_term = {
            'search_term': term['search_term'],
            'clicks': term['clicks'],
            'cost': term['cost'],
            'conversions': 0,
            'campaign_name': term['campaign_name'],
            'match_type': 'Unknown',
            'added_date': datetime.now().isoformat(),
            'next_review_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'status': 'monitoring',
            'last_checked': datetime.now().isoformat()
        }
        client_data['terms'].append(new_term)
        added_count += 1

    return added_count


def generate_alert_summary(
    client_slug: str,
    tier2_promoted: List,
    new_tier1: List[Dict],
    new_tier2: List[Dict]
) -> Dict:
    """Generate summary for daily briefing integration"""
    return {
        'client': client_slug,
        'tier2_promoted_count': len(tier2_promoted),
        'new_tier1_count': len(new_tier1),
        'new_tier2_count': len(new_tier2),
        'tier2_promoted_terms': [t['search_term'] for t in tier2_promoted],
        'new_tier1_terms': [t['search_term'] for t in new_tier1],
        'total_waste_projection': sum(t['cost'] for t in tier2_promoted + new_tier1) * 6  # Annualize
    }


def load_config() -> Dict:
    """Load tier system configuration"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading config: {e}")
        # Return defaults
        return {
            'tier1_deployment_frequency': 'bi-weekly',
            'tier2_review_frequency': 'monthly',
            'always_p0': True,
            'deployment_schedule': {
                'tier1_deployment_weeks': [1, 3],
                'tier2_review_week': 1
            }
        }


def get_week_of_month() -> int:
    """Get current week number of the month (1-5)"""
    today = datetime.now()
    first_day = today.replace(day=1)
    # Calculate which week this Monday falls in
    day_of_month = today.day
    week_num = ((day_of_month - 1) // 7) + 1
    return week_num


def is_deployment_week(config: Dict) -> bool:
    """Check if this week is a deployment week based on config"""
    frequency = config.get('tier1_deployment_frequency', 'bi-weekly')

    if frequency == 'weekly':
        return True
    elif frequency == 'bi-weekly':
        week_of_month = get_week_of_month()
        deployment_weeks = config.get('deployment_schedule', {}).get('tier1_deployment_weeks', [1, 3])
        return week_of_month in deployment_weeks
    elif frequency == 'monthly':
        week_of_month = get_week_of_month()
        deployment_week = config.get('deployment_schedule', {}).get('tier1_deployment_week', 1)
        return week_of_month == deployment_week

    return False


def is_tier2_review_week(config: Dict) -> bool:
    """Check if this is the monthly Tier 2 review week"""
    frequency = config.get('tier2_review_frequency', 'monthly')

    if frequency == 'weekly':
        return True
    elif frequency == 'monthly':
        week_of_month = get_week_of_month()
        review_week = config.get('deployment_schedule', {}).get('tier2_review_week', 1)
        return week_of_month == review_week

    return False


def create_tier1_deployment_task(all_alerts: List[Dict], config: Dict):
    """Create consolidated Tier 1 deployment task"""
    # Count total terms and waste across all clients
    total_tier1_terms = sum(a['tier2_promoted_count'] + a['new_tier1_count'] for a in all_alerts)
    total_waste = sum(a['total_waste_projection'] for a in all_alerts)

    if total_tier1_terms == 0:
        print("   ℹ️  No Tier 1 terms to deploy - skipping task creation")
        return

    # Build task description
    client_summary = []
    for alert in all_alerts:
        tier1_count = alert['tier2_promoted_count'] + alert['new_tier1_count']
        if tier1_count > 0:
            client_summary.append(f"  - {alert['client']}: {tier1_count} terms")

    task_title = config.get('notification_settings', {}).get('task_titles', {}).get(
        'tier1',
        'Deploy Tier 1 Negative Keywords Across Clients'
    )

    task_notes = f"""Weekly tier system scan identified {total_tier1_terms} Tier 1 negative keywords requiring deployment.

Projected annual waste: £{total_waste:,.0f}/year

Clients affected:
{chr(10).join(client_summary)}

Deploy via Google Ads UI or scripts as [exact match] negative keywords to appropriate campaigns.

Details in: shared/data/state/tier-alerts.json
Reports in: clients/{{client}}/reports/"""

    # Determine priority
    priority = 'P0' if config.get('always_p0', True) else ('P0' if total_waste > 5000 else 'P1')

    # Create task via ClientTasksService
    try:
        service = ClientTasksService()
        service.create_task(
            title=task_title,
            client='roksys',  # Roksys internal task (not client-specific)
            priority=priority,
            notes=task_notes
        )
        print(f"   ✅ Created {priority} task: {task_title}")
        print(f"      Total: {total_tier1_terms} terms, £{total_waste:,.0f}/year waste")
    except Exception as e:
        print(f"   ❌ Error creating task: {e}")


def create_tier2_review_task(all_alerts: List[Dict], config: Dict):
    """Create monthly Tier 2 review task"""
    # Count total Tier 2 terms across all clients
    total_tier2_terms = sum(a['new_tier2_count'] for a in all_alerts)

    if total_tier2_terms == 0:
        print("   ℹ️  No Tier 2 terms detected this month - skipping task creation")
        return

    # Build task description
    client_summary = []
    for alert in all_alerts:
        if alert['new_tier2_count'] > 0:
            client_summary.append(f"  - {alert['client']}: {alert['new_tier2_count']} terms")

    task_title = config.get('notification_settings', {}).get('task_titles', {}).get(
        'tier2',
        'Review Tier 2 Negative Keywords for Promotion'
    )

    task_notes = f"""Monthly tier system scan detected {total_tier2_terms} NEW Tier 2 terms now in monitoring.

These terms have 10-29 clicks and 0 conversions (60-day period).
They'll be automatically promoted to Tier 1 if they reach 30+ clicks.

Clients affected:
{chr(10).join(client_summary)}

Action: Review tracker to ensure no false positives
See: shared/data/tier2_tracker.json

Most terms will auto-promote - this is just a sanity check."""

    # Always P2 for Tier 2 review (informational)
    try:
        service = ClientTasksService()
        service.create_task(
            title=task_title,
            client='roksys',
            priority='P2',
            notes=task_notes
        )
        print(f"   ✅ Created P2 task: {task_title}")
        print(f"      Total: {total_tier2_terms} terms in monitoring")
    except Exception as e:
        print(f"   ❌ Error creating task: {e}")


def run_weekly_monitor():
    """Main monitoring workflow"""
    print("\n" + "="*80)
    print("TIER SYSTEM WEEKLY MONITOR")
    print("="*80)
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load configuration
    config = load_config()
    week_of_month = get_week_of_month()
    print(f"Configuration: {config.get('tier1_deployment_frequency', 'bi-weekly')} deployment")
    print(f"Current week: Week {week_of_month} of month\n")

    tracker_data = load_tracker_data()

    if not tracker_data.get('clients'):
        print("❌ No clients in tracker")
        return

    all_alerts = []

    for client_slug, client_data in tracker_data['clients'].items():
        print(f"\n{'='*80}")
        print(f"CLIENT: {client_slug}")
        print(f"{'='*80}")

        customer_id = client_data['customer_id']

        # STEP 1: Check existing Tier 2 terms for promotion
        print("\n📊 Step 1: Checking existing Tier 2 terms for promotion...")

        # Capture promoted terms before check
        before_promoted = [t for t in client_data['terms'] if t.get('status') == 'promoted_tier1']

        # Run existing Tier 2 check (from tier2_tracker.py)
        check_client_terms(client_slug, force_check=False)

        # Reload to get updated data
        tracker_data = load_tracker_data()
        client_data = tracker_data['clients'][client_slug]

        after_promoted = [t for t in client_data['terms'] if t.get('status') == 'promoted_tier1']
        newly_promoted = [t for t in after_promoted if t not in before_promoted]

        print(f"   ✅ {len(newly_promoted)} terms promoted from Tier 2 to Tier 1")

        # STEP 2: Find NEW Tier 1 and Tier 2 terms
        print("\n🔍 Step 2: Scanning last 7 days for NEW terms...")

        seven_day_terms = get_7_day_search_terms(customer_id)
        print(f"   Found {len(seven_day_terms)} terms with 10+ clicks in last 7 days")

        new_tier1, new_tier2 = find_new_terms(seven_day_terms, tracker_data, client_slug)

        print(f"   🔴 NEW Tier 1 terms: {len(new_tier1)}")
        print(f"   🟡 NEW Tier 2 terms: {len(new_tier2)}")

        # STEP 3: Add new terms to tracker
        if new_tier1 or new_tier2:
            print("\n➕ Step 3: Adding new terms to tracker...")
            added = add_new_terms_to_tracker(new_tier1, new_tier2, tracker_data, client_slug, customer_id)
            print(f"   ✅ Added {added} new terms to tracker")
            save_tracker_data(tracker_data)

        # STEP 4: Generate alert summary
        if newly_promoted or new_tier1 or new_tier2:
            alert = generate_alert_summary(client_slug, newly_promoted, new_tier1, new_tier2)
            all_alerts.append(alert)

            print(f"\n🔔 Alert generated for {client_slug}:")
            if newly_promoted:
                print(f"   📈 {len(newly_promoted)} Tier 2 → Tier 1 promotions")
            if new_tier1:
                print(f"   🆕 {len(new_tier1)} NEW Tier 1 terms detected")
            if new_tier2:
                print(f"   🆕 {len(new_tier2)} NEW Tier 2 terms detected")

    # Save alerts for daily briefing integration
    if all_alerts:
        NOTIFICATION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTIFICATION_FILE, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'alerts': all_alerts
            }, f, indent=2)

        print(f"\n✅ Alerts saved to: {NOTIFICATION_FILE}")
        print(f"   Total clients with alerts: {len(all_alerts)}")

        # Create tasks if configured
        print("\n" + "="*80)
        print("TASK CREATION")
        print("="*80)

        # Check if we should create Tier 1 deployment task
        if is_deployment_week(config):
            print(f"✅ Week {week_of_month} is a deployment week - creating Tier 1 task...")
            create_tier1_deployment_task(all_alerts, config)
        else:
            print(f"ℹ️  Week {week_of_month} is not a deployment week - skipping Tier 1 task")

        # Check if we should create Tier 2 review task
        if is_tier2_review_week(config):
            print(f"✅ Week {week_of_month} is Tier 2 review week - creating review task...")
            create_tier2_review_task(all_alerts, config)
        else:
            print(f"ℹ️  Week {week_of_month} is not Tier 2 review week - skipping review task")

    else:
        print("\n✅ No alerts to report this week")

    print("\n" + "="*80)
    print("WEEKLY MONITOR COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_weekly_monitor()
