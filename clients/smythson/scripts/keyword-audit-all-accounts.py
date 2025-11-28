#!/usr/bin/env python3
"""
Smythson Keyword Audit - All Accounts
Performs comprehensive keyword audit across all 4 Smythson Google Ads accounts.

This script uses the Google Ads MCP server's execute_gaql function directly.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # Go up from scripts/smythson/clients/ to project root
sys.path.insert(0, str(PROJECT_ROOT))

# Change to MCP server directory to ensure proper imports
MCP_SERVER_DIR = PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'
os.chdir(str(MCP_SERVER_DIR))
sys.path.insert(0, str(MCP_SERVER_DIR))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import Google Ads MCP modules (now from correct directory)
try:
    from oauth.google_auth import execute_gaql, format_customer_id
except ImportError as e:
    print(f"Error: Could not import Google Ads MCP server modules: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"MCP server directory: {MCP_SERVER_DIR}")
    print("\nTroubleshooting:")
    print("1. Make sure you're running from project root")
    print("2. Check that GOOGLE_ADS_DEVELOPER_TOKEN is set in environment")
    print("3. Verify GOOGLE_ADS_OAUTH_CONFIG_PATH points to OAuth credentials")
    sys.exit(1)

# Smythson Account IDs
ACCOUNTS = {
    'UK': '8573235780',
    'USA': '7808690871',
    'EUR': '7679616761',
    'ROW': '5556710725'
}

MANAGER_ID = '2569949686'  # Rok Systems MCC

# Date range - last 14 days for keyword analysis
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=14)
DATE_RANGE = f"'{START_DATE.strftime('%Y-%m-%d')}' AND '{END_DATE.strftime('%Y-%m-%d')}'"

def query_keyword_performance(account_id: str, account_name: str) -> List[Dict]:
    """Query keyword performance data"""
    print(f"\n📊 Querying keyword data for {account_name} ({account_id})...")
    
    query = f"""
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value,
        metrics.ctr,
        metrics.average_cpc,
        metrics.search_impression_share,
        metrics.search_rank_lost_impression_share
    FROM keyword_view
    WHERE segments.date BETWEEN {DATE_RANGE}
      AND campaign.status = 'ENABLED'
      AND campaign.advertising_channel_type = 'SEARCH'
      AND ad_group.status = 'ENABLED'
      AND ad_group_criterion.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
    """
    
    try:
        result = execute_gaql(account_id, query, MANAGER_ID)
        keywords = []
        
        for row in result.get('results', []):
            keyword_data = {
                'account': account_name,
                'campaign_id': row.get('campaign', {}).get('id', ''),
                'campaign_name': row.get('campaign', {}).get('name', ''),
                'ad_group_id': row.get('adGroup', {}).get('id', ''),
                'ad_group_name': row.get('adGroup', {}).get('name', ''),
                'keyword': row.get('adGroupCriterion', {}).get('keyword', {}).get('text', ''),
                'match_type': row.get('adGroupCriterion', {}).get('keyword', {}).get('matchType', ''),
                'impressions': row.get('metrics', {}).get('impressions', 0),
                'clicks': row.get('metrics', {}).get('clicks', 0),
                'cost_micros': row.get('metrics', {}).get('costMicros', 0),
                'conversions': row.get('metrics', {}).get('conversions', 0.0),
                'conversions_value': row.get('metrics', {}).get('conversionsValue', 0.0),
                'ctr': row.get('metrics', {}).get('ctr', 0.0),
                'average_cpc_micros': row.get('metrics', {}).get('averageCpc', 0),
                'search_impression_share': row.get('metrics', {}).get('searchImpressionShare', 0.0),
                'search_rank_lost_impression_share': row.get('metrics', {}).get('searchRankLostImpressionShare', 0.0)
            }
            
            # Calculate derived metrics
            cost = keyword_data['cost_micros'] / 1_000_000
            keyword_data['cost'] = cost
            keyword_data['roas'] = keyword_data['conversions_value'] / cost if cost > 0 else 0
            keyword_data['cvr'] = keyword_data['conversions'] / keyword_data['clicks'] if keyword_data['clicks'] > 0 else 0
            keyword_data['cpa'] = cost / keyword_data['conversions'] if keyword_data['conversions'] > 0 else 0
            
            keywords.append(keyword_data)
        
        print(f"  ✅ Found {len(keywords)} keywords")
        return keywords
        
    except Exception as e:
        print(f"  ❌ Error querying keywords: {e}")
        return []


def query_search_terms(account_id: str, account_name: str) -> List[Dict]:
    """Query search term performance data"""
    print(f"\n🔍 Querying search terms for {account_name} ({account_id})...")
    
    query = f"""
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        segments.search_term,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value,
        metrics.ctr
    FROM search_term_view
    WHERE segments.date BETWEEN {DATE_RANGE}
      AND campaign.status = 'ENABLED'
      AND campaign.advertising_channel_type = 'SEARCH'
      AND metrics.clicks > 0
    ORDER BY metrics.cost_micros DESC
    """
    
    try:
        result = execute_gaql(account_id, query, MANAGER_ID)
        search_terms = []
        
        for row in result.get('results', []):
            term_data = {
                'account': account_name,
                'campaign_id': row.get('campaign', {}).get('id', ''),
                'campaign_name': row.get('campaign', {}).get('name', ''),
                'ad_group_id': row.get('adGroup', {}).get('id', ''),
                'ad_group_name': row.get('adGroup', {}).get('name', ''),
                'search_term': row.get('segments', {}).get('searchTerm', ''),
                'impressions': row.get('metrics', {}).get('impressions', 0),
                'clicks': row.get('metrics', {}).get('clicks', 0),
                'cost_micros': row.get('metrics', {}).get('costMicros', 0),
                'conversions': row.get('metrics', {}).get('conversions', 0.0),
                'conversions_value': row.get('metrics', {}).get('conversionsValue', 0.0),
                'ctr': row.get('metrics', {}).get('ctr', 0.0)
            }
            
            cost = term_data['cost_micros'] / 1_000_000
            term_data['cost'] = cost
            term_data['roas'] = term_data['conversions_value'] / cost if cost > 0 else 0
            
            search_terms.append(term_data)
        
        print(f"  ✅ Found {len(search_terms)} search terms")
        return search_terms
        
    except Exception as e:
        print(f"  ❌ Error querying search terms: {e}")
        return []


def calculate_account_averages(keywords: List[Dict]) -> Dict[str, float]:
    """Calculate account average metrics for benchmarking"""
    if not keywords:
        return {'roas': 0, 'ctr': 0, 'cvr': 0}
    
    total_cost = sum(k['cost'] for k in keywords)
    total_revenue = sum(k['conversions_value'] for k in keywords)
    total_clicks = sum(k['clicks'] for k in keywords)
    total_conversions = sum(k['conversions'] for k in keywords)
    total_impressions = sum(k['impressions'] for k in keywords)
    
    avg_roas = total_revenue / total_cost if total_cost > 0 else 0
    avg_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    avg_cvr = total_conversions / total_clicks if total_clicks > 0 else 0
    
    return {
        'roas': avg_roas,
        'ctr': avg_ctr,
        'cvr': avg_cvr,
        'total_cost': total_cost,
        'total_revenue': total_revenue
    }


def analyze_keywords(keywords: List[Dict], account_name: str) -> Dict:
    """Analyze keywords using ROK framework"""
    if not keywords:
        return {
            'wasted_spend': [],
            'growth_opportunities': [],
            'zero_conversion': [],
            'account_averages': {}
        }
    
    # Calculate account averages
    averages = calculate_account_averages(keywords)
    
    # Thresholds
    min_spend = 50  # £50 minimum
    waste_multiplier = 0.7
    opportunity_multiplier = 1.3
    
    wasted_spend = []
    growth_opportunities = []
    zero_conversion = []
    
    for kw in keywords:
        # Skip if below minimum spend
        if kw['cost'] < min_spend:
            continue
        
        # Wasted spend: ROAS < account_avg × 0.7
        if kw['roas'] < (averages['roas'] * waste_multiplier):
            wasted_spend.append(kw)
        
        # Growth opportunities: ≥2 conversions AND ROAS ≥ account_avg × 1.3
        if kw['conversions'] >= 2 and kw['roas'] >= (averages['roas'] * opportunity_multiplier):
            growth_opportunities.append(kw)
        
        # Zero conversion waste: >£100 spend, 0 conversions
        if kw['cost'] > 100 and kw['conversions'] == 0:
            zero_conversion.append(kw)
    
    return {
        'wasted_spend': sorted(wasted_spend, key=lambda x: x['cost'], reverse=True),
        'growth_opportunities': sorted(growth_opportunities, key=lambda x: x['roas'], reverse=True),
        'zero_conversion': sorted(zero_conversion, key=lambda x: x['cost'], reverse=True),
        'account_averages': averages
    }


def analyze_search_terms(search_terms: List[Dict]) -> Dict:
    """Analyze search terms for negative keyword opportunities"""
    negative_candidates = []
    new_keyword_candidates = []
    
    for term in search_terms:
        # High spend, zero conversions = negative keyword candidate
        if term['cost'] > 10 and term['conversions'] == 0:
            negative_candidates.append(term)
        
        # High performing queries not yet keywords = new keyword candidate
        if term['conversions'] >= 2 and term['roas'] > 2.0:
            new_keyword_candidates.append(term)
    
    return {
        'negative_candidates': sorted(negative_candidates, key=lambda x: x['cost'], reverse=True),
        'new_keyword_candidates': sorted(new_keyword_candidates, key=lambda x: x['roas'], reverse=True)
    }


def generate_report(all_data: Dict) -> str:
    """Generate formatted audit report"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    date_range_str = f"{START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}"
    
    report = f"""# Keyword Audit: Smythson (All Accounts)
**Date Range**: {date_range_str}  
**Analysis Date**: {report_date}  
**Accounts Analyzed**: UK, USA, EUR, ROW

## Executive Summary

"""
    
    # Calculate totals
    total_keywords = sum(len(data['keywords']) for data in all_data.values())
    total_wasted_cost = 0
    total_opportunity_revenue = 0
    
    for account_name, data in all_data.items():
        analysis = data['analysis']
        wasted = analysis['wasted_spend']
        opportunities = analysis['growth_opportunities']
        
        total_wasted_cost += sum(kw['cost'] for kw in wasted)
        total_opportunity_revenue += sum(kw['conversions_value'] for kw in opportunities[:10])  # Top 10
    
    report += f"""**Quick Stats**:
- Keywords analyzed: {total_keywords:,}
- Accounts analyzed: 4 (UK, USA, EUR, ROW)
- Potential monthly savings: £{total_wasted_cost * 2:.2f} (14-day period × 2)
- Potential growth opportunity: £{total_opportunity_revenue * 2:.2f}/month

---

"""
    
    # Per-account analysis
    for account_name in ['UK', 'USA', 'EUR', 'ROW']:
        if account_name not in all_data:
            continue
        
        data = all_data[account_name]
        keywords = data['keywords']
        search_terms = data['search_terms']
        analysis = data['analysis']
        averages = analysis['account_averages']
        
        report += f"""## {account_name} Account Analysis

**Account Average Metrics**:
- Average ROAS: {averages['roas']:.2f}
- Average CTR: {averages['ctr']:.2%}
- Average CVR: {averages['cvr']:.2%}
- Total Spend: £{averages['total_cost']:,.2f}
- Total Revenue: £{averages['total_revenue']:,.2f}

### 🔴 Wasted Spend (Immediate Action Required)

"""
        
        # Wasted spend keywords
        wasted = analysis['wasted_spend'][:20]  # Top 20
        if wasted:
            report += """| Keyword | Campaign | Spend | Conversions | ROAS | Recommendation |
|---------|----------|-------|-------------|------|----------------|
"""
            for kw in wasted:
                rec = "Pause or reduce bid by 50%"
                report += f"| {kw['keyword']} | {kw['campaign_name']} | £{kw['cost']:.2f} | {kw['conversions']:.1f} | {kw['roas']:.2f} | {rec} |\n"
            
            wasted_total = sum(kw['cost'] for kw in wasted)
            report += f"\n**Total waste identified**: £{wasted_total:.2f} in last 14 days\n\n"
        else:
            report += "No significant wasted spend identified.\n\n"
        
        # Zero conversion keywords
        zero_conv = analysis['zero_conversion'][:10]
        if zero_conv:
            report += """### Zero-Conversion Keywords (>£100 spend)

| Keyword | Campaign | Spend | Recommendation |
|---------|----------|-------|----------------|
"""
            for kw in zero_conv:
                report += f"| {kw['keyword']} | {kw['campaign_name']} | £{kw['cost']:.2f} | Pause keyword |\n"
            report += "\n"
        
        # Growth opportunities
        opportunities = analysis['growth_opportunities'][:20]
        if opportunities:
            report += """### 🟢 Growth Opportunities

| Keyword | Campaign | Conversions | ROAS | Current IS | Recommendation |
|---------|----------|-------------|------|------------|----------------|
"""
            for kw in opportunities:
                is_pct = kw['search_impression_share'] * 100 if kw['search_impression_share'] else 0
                rec = f"Increase bid (+20%)" if is_pct < 80 else "Maintain bid"
                report += f"| {kw['keyword']} | {kw['campaign_name']} | {kw['conversions']:.1f} | {kw['roas']:.2f} | {is_pct:.1f}% | {rec} |\n"
            
            opp_revenue = sum(kw['conversions_value'] for kw in opportunities[:10])
            report += f"\n**Potential additional revenue**: £{opp_revenue * 2:.2f}/month\n\n"
        else:
            report += "No significant growth opportunities identified.\n\n"
        
        # Search term analysis
        search_analysis = analyze_search_terms(search_terms)
        negatives = search_analysis['negative_candidates'][:20]
        
        if negatives:
            report += """### Zero-Conversion Search Terms (Negative Keyword Candidates)

| Search Term | Campaign | Impressions | Clicks | Spend | Recommendation |
|-------------|----------|-------------|--------|-------|----------------|
"""
            for term in negatives:
                report += f"| {term['search_term']} | {term['campaign_name']} | {term['impressions']} | {term['clicks']} | £{term['cost']:.2f} | Add as negative (broad) |\n"
            
            neg_total = sum(term['cost'] for term in negatives)
            report += f"\n**Action**: Add {len(negatives)} negative keywords - Save ~£{neg_total * 2:.2f}/month\n\n"
        
        report += "---\n\n"
    
    # Prioritized action plan
    report += """## Prioritized Action Plan

### This Week (High Impact)
"""
    
    all_negatives = []
    all_wasted = []
    all_opportunities = []
    
    for account_name, data in all_data.items():
        search_analysis = analyze_search_terms(data['search_terms'])
        all_negatives.extend(search_analysis['negative_candidates'][:10])
        all_wasted.extend(data['analysis']['wasted_spend'][:10])
        all_opportunities.extend(data['analysis']['growth_opportunities'][:10])
    
    if all_negatives:
        neg_savings = sum(t['cost'] for t in all_negatives[:20]) * 2
        report += f"""1. **Add {min(20, len(all_negatives))} negative keywords** - Save ~£{neg_savings:.2f}/month
   - Focus on zero-conversion search terms with >£10 spend
   - Add at campaign level with broad match
"""
    
    if all_wasted:
        wasted_savings = sum(kw['cost'] for kw in all_wasted[:20]) * 2
        report += f"""2. **Pause {min(20, len(all_wasted))} underperforming keywords** - Save £{wasted_savings:.2f}/month
   - Keywords with ROAS < account average × 0.7
"""
    
    if all_opportunities:
        opp_revenue = sum(kw['conversions_value'] for kw in all_opportunities[:20]) * 2
        report += f"""3. **Increase bids on {min(20, len(all_opportunities))} high-performers** - Add ~£{opp_revenue:.2f} revenue/month
   - Keywords with ROAS ≥ account average × 1.3 and ≥2 conversions
"""
    
    report += """
### Next 2 Weeks (Medium Impact)
4. Review match type distribution and optimize
5. Refresh ad copy for declining keywords
6. Review landing pages for low-CVR keywords

### Ongoing (Monitoring)
7. Weekly search term review - Catch new negatives
8. Monitor bid adjustments impact
9. Track Quality Score indicators

---

## Data Quality Notes
- Analysis based on last 14 days of performance data
- Focus on Search campaigns only (Shopping campaigns excluded)
- Minimum spend threshold: £50 for keyword analysis
- Search terms minimum: £10 spend for negative keyword consideration
- All financial metrics converted to GBP for reporting consistency

## Follow-Up Actions
- [ ] Implement negative keywords (use bulk upload sheet)
- [ ] Adjust bids for high-performing keywords
- [ ] Pause waste keywords
- [ ] Schedule follow-up audit in 2 weeks
"""
    
    return report


def main():
    """Main execution"""
    print("=" * 80)
    print("SMYTHSON KEYWORD AUDIT - ALL ACCOUNTS")
    print("=" * 80)
    print(f"\nDate Range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"Accounts: UK, USA, EUR, ROW\n")
    
    all_data = {}
    
    # Query all accounts
    for account_name, account_id in ACCOUNTS.items():
        print(f"\n{'=' * 80}")
        print(f"Processing {account_name} Account")
        print(f"{'=' * 80}")
        
        keywords = query_keyword_performance(account_id, account_name)
        search_terms = query_search_terms(account_id, account_name)
        
        if keywords:
            analysis = analyze_keywords(keywords, account_name)
        else:
            analysis = {
                'wasted_spend': [],
                'growth_opportunities': [],
                'zero_conversion': [],
                'account_averages': {}
            }
        
        all_data[account_name] = {
            'keywords': keywords,
            'search_terms': search_terms,
            'analysis': analysis
        }
    
    # Generate report
    print(f"\n{'=' * 80}")
    print("GENERATING AUDIT REPORT")
    print(f"{'=' * 80}\n")
    
    report = generate_report(all_data)
    
    # Save report
    output_dir = PROJECT_ROOT / 'clients' / 'smythson' / 'audits'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    report_file = output_dir / f'keyword-audit-all-accounts-{timestamp}.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Audit report saved: {report_file.relative_to(PROJECT_ROOT)}")
    
    # Also save raw data as JSON for reference
    json_file = output_dir / f'keyword-audit-data-{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print(f"✅ Raw data saved: {json_file.relative_to(PROJECT_ROOT)}")
    
    # Print summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}\n")
    
    for account_name, data in all_data.items():
        analysis = data['analysis']
        print(f"{account_name}:")
        print(f"  Keywords analyzed: {len(data['keywords'])}")
        print(f"  Wasted spend items: {len(analysis['wasted_spend'])}")
        print(f"  Growth opportunities: {len(analysis['growth_opportunities'])}")
        print(f"  Zero-conversion keywords: {len(analysis['zero_conversion'])}")
        print()
    
    print(f"📄 Full report: {report_file.relative_to(PROJECT_ROOT)}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

