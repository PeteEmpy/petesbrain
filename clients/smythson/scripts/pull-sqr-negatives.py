#!/usr/bin/env python3
"""
Pull Search Query Reports for EUR and ROW accounts to identify negative keyword candidates.
Focus on new campaigns launched this month (November 2025).
"""

import os
import json
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Account IDs
EUR_ACCOUNT = "7679616761"
ROW_ACCOUNT = "5556710725"

# Date range - last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
DATE_RANGE = f"'{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'"

# Initialize client
client = GoogleAdsClient.load_from_storage(os.path.expanduser("~/google-ads.yaml"))

def get_search_terms(customer_id, account_name):
    """Get search terms from Search campaigns with metrics"""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            campaign.id,
            ad_group.name,
            search_term_view.search_term,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM search_term_view
        WHERE segments.date BETWEEN {DATE_RANGE}
        AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 5000
    """

    results = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            cost = row.metrics.cost_micros / 1_000_000
            results.append({
                'account': account_name,
                'campaign': row.campaign.name,
                'campaign_id': row.campaign.id,
                'ad_group': row.ad_group.name,
                'search_term': row.search_term_view.search_term,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'cost': round(cost, 2),
                'conversions': row.metrics.conversions,
                'conv_value': round(row.metrics.conversions_value, 2)
            })
    except GoogleAdsException as ex:
        print(f"Error getting search terms for {account_name}: {ex}")

    return results

def get_pmax_search_insights(customer_id, account_name):
    """Get PMax search term insights (aggregated categories)"""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            campaign_search_term_insight.category_label,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions
        FROM campaign_search_term_insight
        WHERE segments.date BETWEEN {DATE_RANGE}
        AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        ORDER BY metrics.impressions DESC
        LIMIT 500
    """

    results = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            results.append({
                'account': account_name,
                'campaign': row.campaign.name,
                'category': row.campaign_search_term_insight.category_label,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'conversions': row.metrics.conversions
            })
    except GoogleAdsException as ex:
        print(f"Error getting PMax insights for {account_name}: {ex}")

    return results

def identify_negative_candidates(search_terms):
    """Identify search terms that should be negatives"""

    # Criteria for negative candidates:
    # 1. High spend, no conversions
    # 2. Irrelevant terms (competitors, wrong products, etc.)
    # 3. Very low CTR with decent impressions

    negatives = []

    # Known irrelevant patterns
    irrelevant_patterns = [
        'cheap', 'free', 'discount', 'coupon', 'sale', 'outlet',
        'second hand', 'used', 'ebay', 'amazon', 'aliexpress',
        'diy', 'how to make', 'tutorial',
        'job', 'jobs', 'career', 'hiring', 'salary',
        'wiki', 'wikipedia', 'reddit',
        'repair', 'fix', 'broken',
        # Competitors
        'aspinal', 'mulberry', 'louis vuitton', 'gucci', 'prada',
        'montblanc', 'cross', 'parker', 'waterman', 'filofax',
        'moleskine', 'leuchtturm', 'rhodia',
    ]

    for term in search_terms:
        term_lower = term['search_term'].lower()
        reasons = []

        # Check for irrelevant patterns
        for pattern in irrelevant_patterns:
            if pattern in term_lower:
                reasons.append(f"Contains '{pattern}'")
                break

        # High spend no conversions (>£5 spend, 0 conversions)
        if term['cost'] > 5 and term['conversions'] == 0:
            reasons.append(f"£{term['cost']} spent, 0 conversions")

        # Very high spend no conversions (>£20)
        if term['cost'] > 20 and term['conversions'] == 0:
            reasons.append("HIGH PRIORITY - significant wasted spend")

        # Low CTR with impressions (< 1% CTR with 100+ impressions)
        if term['impressions'] >= 100 and term['clicks'] > 0:
            ctr = (term['clicks'] / term['impressions']) * 100
            if ctr < 1 and term['conversions'] == 0:
                reasons.append(f"Low CTR ({ctr:.1f}%) with {term['impressions']} imps")

        if reasons:
            negatives.append({
                **term,
                'reasons': reasons,
                'priority': 'HIGH' if term['cost'] > 20 else 'MEDIUM' if term['cost'] > 5 else 'LOW'
            })

    # Sort by cost descending
    negatives.sort(key=lambda x: x['cost'], reverse=True)

    return negatives

def main():
    all_search_terms = []
    all_pmax_insights = []

    print("="*60)
    print("Pulling Search Query Reports for EUR and ROW")
    print("="*60)

    # EUR Account
    print(f"\nProcessing EUR Account ({EUR_ACCOUNT})...")
    eur_terms = get_search_terms(EUR_ACCOUNT, 'EUR')
    print(f"  Found {len(eur_terms)} search terms")
    all_search_terms.extend(eur_terms)

    print("  Fetching PMax search insights...")
    eur_pmax = get_pmax_search_insights(EUR_ACCOUNT, 'EUR')
    print(f"  Found {len(eur_pmax)} PMax insights")
    all_pmax_insights.extend(eur_pmax)

    # ROW Account
    print(f"\nProcessing ROW Account ({ROW_ACCOUNT})...")
    row_terms = get_search_terms(ROW_ACCOUNT, 'ROW')
    print(f"  Found {len(row_terms)} search terms")
    all_search_terms.extend(row_terms)

    print("  Fetching PMax search insights...")
    row_pmax = get_pmax_search_insights(ROW_ACCOUNT, 'ROW')
    print(f"  Found {len(row_pmax)} PMax insights")
    all_pmax_insights.extend(row_pmax)

    # Identify negative candidates
    print("\nIdentifying negative keyword candidates...")
    negatives = identify_negative_candidates(all_search_terms)
    print(f"Found {len(negatives)} potential negatives")

    # Save results
    output_dir = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents'

    # Save all search terms
    with open(f'{output_dir}/eur-row-search-terms-raw.json', 'w') as f:
        json.dump(all_search_terms, f, indent=2)

    # Save PMax insights
    with open(f'{output_dir}/eur-row-pmax-insights.json', 'w') as f:
        json.dump(all_pmax_insights, f, indent=2)

    # Save negative candidates
    with open(f'{output_dir}/eur-row-negative-candidates.json', 'w') as f:
        json.dump(negatives, f, indent=2)

    # Create HTML report
    create_html_report(negatives, all_pmax_insights, output_dir)

    print(f"\nResults saved to {output_dir}/")
    print("  - eur-row-search-terms-raw.json")
    print("  - eur-row-pmax-insights.json")
    print("  - eur-row-negative-candidates.json")
    print("  - eur-row-negative-recommendations.html")

def create_html_report(negatives, pmax_insights, output_dir):
    """Create HTML report of negative recommendations"""

    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Smythson EUR/ROW - Negative Keyword Recommendations</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; font-size: 12px; }
        h1 { font-size: 18px; }
        h2 { font-size: 14px; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; vertical-align: top; }
        th { background: #f0f0f0; }
        .high { background: #f8d7da; }
        .medium { background: #fff3cd; }
        .low { background: #d4edda; }
        .summary { background: #e7f3ff; padding: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Smythson EUR/ROW - Negative Keyword Recommendations</h1>
    <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
    <p>Period: Last 30 days</p>

    <div class="summary">
        <strong>Summary:</strong><br>
        Total negative candidates: """ + str(len(negatives)) + """<br>
        HIGH priority (>£20 wasted): """ + str(len([n for n in negatives if n['priority'] == 'HIGH'])) + """<br>
        MEDIUM priority (>£5 wasted): """ + str(len([n for n in negatives if n['priority'] == 'MEDIUM'])) + """
    </div>
"""

    # High priority negatives
    high_priority = [n for n in negatives if n['priority'] == 'HIGH']
    if high_priority:
        html += """
    <h2>HIGH PRIORITY - Significant Wasted Spend (>£20, 0 conversions)</h2>
    <table>
        <tr>
            <th>Account</th>
            <th>Campaign</th>
            <th>Search Term</th>
            <th>Cost</th>
            <th>Clicks</th>
            <th>Conv</th>
            <th>Reason</th>
        </tr>"""
        for n in high_priority[:50]:
            html += f"""
        <tr class="high">
            <td>{n['account']}</td>
            <td>{n['campaign'][:40]}...</td>
            <td><strong>{n['search_term']}</strong></td>
            <td>£{n['cost']}</td>
            <td>{n['clicks']}</td>
            <td>{n['conversions']}</td>
            <td>{'; '.join(n['reasons'])}</td>
        </tr>"""
        html += "</table>"

    # Medium priority negatives
    medium_priority = [n for n in negatives if n['priority'] == 'MEDIUM']
    if medium_priority:
        html += """
    <h2>MEDIUM PRIORITY - Moderate Wasted Spend (£5-20, 0 conversions)</h2>
    <table>
        <tr>
            <th>Account</th>
            <th>Campaign</th>
            <th>Search Term</th>
            <th>Cost</th>
            <th>Clicks</th>
            <th>Conv</th>
            <th>Reason</th>
        </tr>"""
        for n in medium_priority[:100]:
            html += f"""
        <tr class="medium">
            <td>{n['account']}</td>
            <td>{n['campaign'][:40]}...</td>
            <td><strong>{n['search_term']}</strong></td>
            <td>£{n['cost']}</td>
            <td>{n['clicks']}</td>
            <td>{n['conversions']}</td>
            <td>{'; '.join(n['reasons'])}</td>
        </tr>"""
        html += "</table>"

    # Irrelevant pattern matches
    pattern_matches = [n for n in negatives if any('Contains' in r for r in n['reasons'])]
    if pattern_matches:
        html += """
    <h2>Pattern Matches - Irrelevant Terms (competitors, cheap, etc.)</h2>
    <table>
        <tr>
            <th>Account</th>
            <th>Campaign</th>
            <th>Search Term</th>
            <th>Cost</th>
            <th>Reason</th>
        </tr>"""
        for n in pattern_matches[:100]:
            pattern_reason = [r for r in n['reasons'] if 'Contains' in r][0]
            html += f"""
        <tr>
            <td>{n['account']}</td>
            <td>{n['campaign'][:40]}...</td>
            <td><strong>{n['search_term']}</strong></td>
            <td>£{n['cost']}</td>
            <td>{pattern_reason}</td>
        </tr>"""
        html += "</table>"

    # PMax insights section
    if pmax_insights:
        html += """
    <h2>PMax Search Categories (Aggregated Insights)</h2>
    <p><em>These are category-level insights, not individual search terms. Review for broad themes.</em></p>
    <table>
        <tr>
            <th>Account</th>
            <th>Campaign</th>
            <th>Category</th>
            <th>Impressions</th>
            <th>Clicks</th>
            <th>Conversions</th>
        </tr>"""
        for insight in pmax_insights[:50]:
            html += f"""
        <tr>
            <td>{insight['account']}</td>
            <td>{insight['campaign'][:40]}...</td>
            <td>{insight['category']}</td>
            <td>{insight['impressions']:,}</td>
            <td>{insight['clicks']}</td>
            <td>{insight['conversions']}</td>
        </tr>"""
        html += "</table>"

    html += """
</body>
</html>
"""

    with open(f'{output_dir}/eur-row-negative-recommendations.html', 'w') as f:
        f.write(html)

if __name__ == "__main__":
    main()
