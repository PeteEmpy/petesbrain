#!/usr/bin/env python3
"""
Google Ads Campaign Audit Agent

Automated campaign structure and budget audit using hierarchical approach.
Executes Phase 1 (Account Intelligence) → Phase 2 (Core Audit) → Phase 3 (Optional Deep-Dive).

This agent runs audits automatically and generates comprehensive reports focusing on:
- Structural inefficiencies (geographic targeting, network settings, bid strategies)
- Budget misallocations (constrained campaigns, wasted spend)

Runs weekly (Monday 10 AM) or on-demand for specific clients.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    # Try loading from project root
    load_dotenv(PROJECT_ROOT / '.env')
    # Also try loading from MCP server directory
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env')
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env 2')
except ImportError:
    # Fallback: manually load .env file if dotenv not available
    env_files = [
        PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env',
        PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env 2',
        PROJECT_ROOT / '.env'
    ]
    for env_file in env_files:
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            break

# Import MCP server utilities
try:
    sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'))
    from oauth.google_auth import execute_gaql
    GAQL_AVAILABLE = True
except ImportError:
    GAQL_AVAILABLE = False
    print("⚠️  Google Ads API not available - MCP server not configured")


def log(message: str):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_client_config(client_slug: str) -> Optional[Dict[str, Any]]:
    """Load client configuration from google-ads-clients.json"""
    clients_file = PROJECT_ROOT / 'shared' / 'data' / 'google-ads-clients.json'
    
    if not clients_file.exists():
        log(f"❌ Client config file not found: {clients_file}")
        return None
    
    with open(clients_file, 'r') as f:
        config = json.load(f)
    
    clients = config.get('clients', {})
    if client_slug not in clients:
        log(f"❌ Client '{client_slug}' not found in config")
        return None
    
    return clients[client_slug]


def get_currency_symbol(client_config: Dict[str, Any]) -> str:
    """Determine currency symbol from client config or default to £"""
    # Check CONTEXT.md for currency info
    client_dir = PROJECT_ROOT / client_config.get('folder_path', '')
    context_file = client_dir / 'CONTEXT.md'
    
    if context_file.exists():
        with open(context_file, 'r') as f:
            content = f.read()
            if 'GBP' in content or '£' in content:
                return '£'
            elif 'USD' in content or '$' in content:
                return '$'
            elif 'AUD' in content:
                return 'A$'
    
    # Default to £ for UK clients
    return '£'


def read_gaql_query(query_name: str) -> str:
    """Read GAQL query from queries directory"""
    query_file = PROJECT_ROOT / '.claude' / 'skills' / 'google-ads-campaign-audit' / 'queries' / f'{query_name}.gaql'
    
    if not query_file.exists():
        log(f"❌ Query file not found: {query_file}")
        return ""
    
    with open(query_file, 'r') as f:
        return f.read().strip()


def execute_query(customer_id: str, query: str, manager_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Execute GAQL query via MCP"""
    if not GAQL_AVAILABLE:
        log("❌ GAQL execution not available - MCP server not configured")
        return None
    
    try:
        result = execute_gaql(customer_id, query, manager_id or "")
        return result
    except Exception as e:
        log(f"❌ Error executing query: {e}")
        return None


def save_json_data(data: Dict[str, Any], filename: str, output_dir: Path):
    """Save query results to JSON file"""
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    
    # Extract results array if present
    if 'results' in data:
        results = data['results']
    else:
        results = data
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    log(f"✓ Saved {filename} ({len(results)} rows)")
    return filepath


def transform_data(output_dir: Path, currency: str) -> Path:
    """Run transform_data.py to convert JSON to markdown tables"""
    transform_script = PROJECT_ROOT / '.claude' / 'skills' / 'google-ads-campaign-audit' / 'transform_data.py'
    
    if not transform_script.exists():
        log(f"❌ Transform script not found: {transform_script}")
        return None
    
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(transform_script),
                '--currency', currency,
                '--input-dir', str(output_dir),
                '--output', 'transformed-analysis-ready.md'
            ],
            capture_output=True,
            text=True,
            cwd=str(output_dir)
        )
        
        if result.returncode == 0:
            log("✓ Data transformation complete")
            return output_dir / 'transformed-analysis-ready.md'
        else:
            log(f"❌ Transformation failed: {result.stderr}")
            return None
    except Exception as e:
        log(f"❌ Error running transform script: {e}")
        return None


def save_audit_issues(client_slug: str, issues: List[Dict[str, Any]], audit_date: str):
    """Save audit issues to weekly issues file"""
    issues_file = PROJECT_ROOT / 'shared' / 'data' / 'weekly-audit-issues.json'
    
    # Load existing issues or create new structure
    if issues_file.exists():
        with open(issues_file, 'r') as f:
            all_issues = json.load(f)
    else:
        all_issues = {
            'generated_at': datetime.now().isoformat(),
            'clients': {}
        }
    
    # Update issues for this client
    if issues:
        all_issues['clients'][client_slug] = {
            'audit_date': audit_date,
            'issues': issues,
            'critical_count': sum(1 for i in issues if i['priority'] == 'CRITICAL'),
            'high_count': sum(1 for i in issues if i['priority'] == 'HIGH'),
            'total_count': len(issues)
        }
    else:
        # Remove client if no issues
        all_issues['clients'].pop(client_slug, None)
    
    # Update generated timestamp
    all_issues['generated_at'] = datetime.now().isoformat()
    
    # Save
    issues_file.parent.mkdir(parents=True, exist_ok=True)
    with open(issues_file, 'w') as f:
        json.dump(all_issues, f, indent=2)
    
    if issues:
        log(f"📋 Saved {len(issues)} issues ({sum(1 for i in issues if i['priority'] == 'CRITICAL')} critical) to {issues_file}")


def detect_serious_issues(client_slug: str, output_dir: Path) -> List[Dict[str, Any]]:
    """
    Analyze audit data to detect serious issues that need review.
    
    Returns list of serious issues with priority, description, and impact.
    """
    issues = []
    
    # Load campaign performance data
    perf_file = output_dir / '03-campaign-performance.json'
    settings_file = output_dir / '05-campaign-settings.json'
    budget_file = output_dir / '04-budget-constraints.json'
    
    if not perf_file.exists():
        return issues
    
    try:
        with open(perf_file, 'r') as f:
            perf_data = json.load(f)
        
        with open(settings_file, 'r') as f:
            settings_data = json.load(f)
        
        with open(budget_file, 'r') as f:
            budget_data = json.load(f)
        
        # Check for zero-conversion campaigns with significant spend
        for campaign in perf_data:
            name = campaign['campaign'].get('name', 'Unknown')
            cost_micros = int(campaign['metrics'].get('costMicros', 0))
            conversions = campaign['metrics'].get('conversions', 0)
            conv_value = campaign['metrics'].get('conversionsValue', 0)
            
            cost = cost_micros / 1_000_000
            
            # CRITICAL: Zero conversions with >£100 spend
            if conversions == 0 and cost > 100:
                issues.append({
                    'priority': 'CRITICAL',
                    'type': 'zero_conversions',
                    'campaign': name,
                    'description': f'Campaign spending £{cost:.2f}/month with zero conversions',
                    'impact': f'Wasting £{cost:.2f}/month',
                    'action': 'Investigate and fix or pause campaign'
                })
            
            # CRITICAL: Negative ROAS (spending more than revenue)
            if cost > 0 and conv_value > 0:
                roas = conv_value / cost
                if roas < 0.5 and cost > 200:  # Less than 0.5x ROAS with >£200 spend
                    issues.append({
                        'priority': 'CRITICAL',
                        'type': 'low_roas',
                        'campaign': name,
                        'description': f'Campaign has {roas:.2f}x ROAS (spending £{cost:.2f}/month)',
                        'impact': f'Losing money - {roas:.2f}x ROAS',
                        'action': 'Review campaign targeting, bids, or pause'
                    })
        
        # Check for geographic targeting waste (PRESENCE_OR_INTEREST)
        for campaign in settings_data:
            name = campaign['campaign'].get('name', 'Unknown')
            geo_setting = campaign['campaign'].get('geoTargetTypeSetting', {})
            positive_geo = geo_setting.get('positiveGeoTargetType', '')
            
            if positive_geo == 'PRESENCE_OR_INTEREST':
                # Find spend for this campaign
                campaign_spend = 0
                for perf_campaign in perf_data:
                    if perf_campaign['campaign'].get('name') == name:
                        campaign_spend = int(perf_campaign['metrics'].get('costMicros', 0)) / 1_000_000
                        break
                
                if campaign_spend > 50:  # Only flag if spending >£50/month
                    issues.append({
                        'priority': 'CRITICAL',
                        'type': 'geographic_targeting_waste',
                        'campaign': name,
                        'description': f'Using PRESENCE_OR_INTEREST targeting (waste)',
                        'impact': f'Wasting 10-15% of £{campaign_spend:.2f}/month spend',
                        'action': 'Change to PRESENCE only'
                    })
        
        # Check for budget constraints
        for campaign in budget_data:
            name = campaign['campaign'].get('name', 'Unknown')
            lost_is_budget = campaign['metrics'].get('searchBudgetLostImpressionShare', 0)
            conversions = campaign['metrics'].get('conversions', 0)
            
            # HIGH: Losing >10% impression share to budget with conversions
            if lost_is_budget > 0.1 and conversions > 0:
                issues.append({
                    'priority': 'HIGH',
                    'type': 'budget_constraint',
                    'campaign': name,
                    'description': f'Losing {lost_is_budget*100:.1f}% impression share to budget',
                    'impact': f'Missing opportunities - campaign is converting but budget-limited',
                    'action': 'Increase budget or reallocate from underperforming campaigns'
                })
        
    except Exception as e:
        log(f"⚠️  Error detecting issues for {client_slug}: {e}")
    
    return issues


def run_audit(client_slug: str) -> bool:
    """Run complete campaign audit for a client"""
    log(f"🔍 Starting campaign audit for {client_slug}")
    
    # Load client config
    client_config = load_client_config(client_slug)
    if not client_config:
        return False
    
    customer_id = client_config.get('customer_id')
    manager_id = client_config.get('manager_id')
    currency = get_currency_symbol(client_config)
    
    log(f"   Customer ID: {customer_id}")
    log(f"   Manager ID: {manager_id or 'None'}")
    log(f"   Currency: {currency}")
    
    # Create output directory
    client_dir = PROJECT_ROOT / client_config.get('folder_path', '')
    audits_dir = client_dir / 'audits'
    audit_date = datetime.now().strftime('%Y%m%d')
    output_dir = audits_dir / f'{audit_date}-campaign-audit-data'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Phase 1: Account Intelligence
    log("\n📊 Phase 1: Account Intelligence")
    
    query1 = read_gaql_query('account-scale')
    if query1:
        result1 = execute_query(customer_id, query1, manager_id)
        if result1:
            save_json_data(result1, '01-account-scale.json', output_dir)
    
    query2 = read_gaql_query('spend-concentration')
    if query2:
        result2 = execute_query(customer_id, query2, manager_id)
        if result2:
            save_json_data(result2, '02-spend-concentration.json', output_dir)
    
    # Phase 2: Core Structural Audit
    log("\n📊 Phase 2: Core Structural Audit")
    
    query3 = read_gaql_query('campaign-performance')
    if query3:
        result3 = execute_query(customer_id, query3, manager_id)
        if result3:
            save_json_data(result3, '03-campaign-performance.json', output_dir)
    
    query4 = read_gaql_query('budget-constraints')
    if query4:
        result4 = execute_query(customer_id, query4, manager_id)
        if result4:
            save_json_data(result4, '04-budget-constraints.json', output_dir)
    
    query5 = read_gaql_query('campaign-settings')
    if query5:
        result5 = execute_query(customer_id, query5, manager_id)
        if result5:
            save_json_data(result5, '05-campaign-settings.json', output_dir)
    
    # Transform data
    log("\n🔄 Transforming data to markdown tables...")
    transformed_file = transform_data(output_dir, currency)
    
    # Detect serious issues
    log("\n🔍 Detecting serious issues...")
    issues = detect_serious_issues(client_slug, output_dir)
    
    if issues:
        log(f"⚠️  Found {len(issues)} serious issue(s):")
        for issue in issues:
            log(f"   [{issue['priority']}] {issue['campaign']}: {issue['description']}")
        save_audit_issues(client_slug, issues, audit_date)
    else:
        log("✅ No serious issues detected")
        # Still save empty issues to clear previous issues
        save_audit_issues(client_slug, [], audit_date)
    
    if transformed_file:
        log(f"✓ Transformed data saved to: {transformed_file}")
        log("\n💡 Next steps:")
        log("   1. Review transformed-analysis-ready.md")
        log("   2. Use Claude Code with the campaign audit skill to analyze")
        log("   3. Generate comprehensive audit report")
        return True
    else:
        log("❌ Data transformation failed")
        return False


def run_audits_all_clients():
    """Run audits for all active clients"""
    clients_file = PROJECT_ROOT / 'shared' / 'data' / 'google-ads-clients.json'
    
    if not clients_file.exists():
        log(f"❌ Client config file not found: {clients_file}")
        return
    
    with open(clients_file, 'r') as f:
        config = json.load(f)
    
    clients = config.get('clients', {})
    active_clients = [slug for slug, data in clients.items() if data.get('status') == 'active']
    
    log(f"📋 Running audits for {len(active_clients)} active clients")
    
    for client_slug in active_clients:
        try:
            run_audit(client_slug)
            log("")
        except Exception as e:
            log(f"❌ Error auditing {client_slug}: {e}")
            log("")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Google Ads Campaign Audit Agent")
    parser.add_argument('--client', help='Client slug to audit (e.g., smythson)')
    parser.add_argument('--all', action='store_true', help='Run audits for all active clients')
    
    args = parser.parse_args()
    
    if args.all:
        run_audits_all_clients()
    elif args.client:
        success = run_audit(args.client)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

