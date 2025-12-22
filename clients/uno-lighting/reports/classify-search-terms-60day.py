#!/usr/bin/env python3
"""
Classify 60-day search term data using three-tier statistical criteria.
NO product category assumptions - purely statistical analysis.
"""

import json
from decimal import Decimal

# Search term data from 60-day GAQL query (Oct 18 - Dec 17, 2025)
# This is the raw data from the previous query
search_terms_raw = """
Based on the 60-day search term query results, classify terms into three tiers.
"""

def classify_search_terms(terms_data):
    """
    Classify search terms into three statistical tiers.

    Tier 1 - Strong Negative Candidates:
        - 30+ clicks in 60 days
        - 0 conversions (or <0.1 effective conversions)
        - Total spend £20+

    Tier 2 - Monitor Closely:
        - 10-29 clicks in 60 days
        - 0 conversions (or <0.1 effective conversions)

    Tier 3 - Insufficient Data:
        - <10 clicks in 60 days
    """

    tier1 = []  # Strong negative candidates
    tier2 = []  # Monitor closely
    tier3 = []  # Insufficient data
    converting = []  # Has conversions (exclude from analysis)

    for term in terms_data:
        search_term = term['search_term']
        clicks = term['clicks']
        conversions = term['conversions']
        spend_micros = term['cost_micros']
        spend_gbp = spend_micros / 1_000_000
        conv_value_micros = term.get('conversions_value', 0)
        conv_value_gbp = conv_value_micros / 1_000_000

        # Calculate ROAS if there are conversions
        roas = (conv_value_gbp / spend_gbp * 100) if spend_gbp > 0 else 0

        # If has meaningful conversions, exclude from negative analysis
        if conversions >= 0.1:
            converting.append({
                'search_term': search_term,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend_gbp,
                'revenue': conv_value_gbp,
                'roas': roas
            })
            continue

        # Classify zero/near-zero conversion terms
        term_data = {
            'search_term': search_term,
            'clicks': clicks,
            'conversions': conversions,
            'spend': spend_gbp,
            'cpc': spend_gbp / clicks if clicks > 0 else 0
        }

        if clicks >= 30 and spend_gbp >= 20:
            tier1.append(term_data)
        elif clicks >= 10:
            tier2.append(term_data)
        else:
            tier3.append(term_data)

    # Sort each tier by spend (highest first)
    tier1.sort(key=lambda x: x['spend'], reverse=True)
    tier2.sort(key=lambda x: x['spend'], reverse=True)
    tier3.sort(key=lambda x: x['spend'], reverse=True)
    converting.sort(key=lambda x: x['revenue'], reverse=True)

    return {
        'tier1': tier1,
        'tier2': tier2,
        'tier3': tier3,
        'converting': converting
    }

def calculate_statistics(classified_terms):
    """Calculate summary statistics for each tier."""

    stats = {}

    for tier_name in ['tier1', 'tier2', 'tier3']:
        terms = classified_terms[tier_name]

        if not terms:
            stats[tier_name] = {
                'count': 0,
                'total_spend': 0,
                'total_clicks': 0,
                'avg_cpc': 0
            }
            continue

        total_spend = sum(t['spend'] for t in terms)
        total_clicks = sum(t['clicks'] for t in terms)
        avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0

        stats[tier_name] = {
            'count': len(terms),
            'total_spend': total_spend,
            'total_clicks': total_clicks,
            'avg_cpc': avg_cpc
        }

    # Converting terms stats
    converting = classified_terms['converting']
    if converting:
        total_spend = sum(t['spend'] for t in converting)
        total_revenue = sum(t['revenue'] for t in converting)
        total_conversions = sum(t['conversions'] for t in converting)

        stats['converting'] = {
            'count': len(converting),
            'total_spend': total_spend,
            'total_revenue': total_revenue,
            'total_conversions': total_conversions,
            'roas': (total_revenue / total_spend * 100) if total_spend > 0 else 0
        }
    else:
        stats['converting'] = {
            'count': 0,
            'total_spend': 0,
            'total_revenue': 0,
            'total_conversions': 0,
            'roas': 0
        }

    return stats

def format_report(classified_terms, stats):
    """Format the classification results as a text report."""

    report = []
    report.append("=" * 80)
    report.append("UNO LIGHTING: 60-DAY SEARCH TERM CLASSIFICATION")
    report.append("Statistical Analysis Only - No Product Assumptions")
    report.append("Period: 18th October - 17th December 2025 (60 days)")
    report.append("=" * 80)
    report.append("")

    # Executive Summary
    report.append("🟢 **EXECUTIVE SUMMARY**")
    report.append("")
    report.append(f"Total unique search terms analysed: {sum(stats[t]['count'] for t in ['tier1', 'tier2', 'tier3', 'converting'])}")
    report.append(f"- Converting terms: {stats['converting']['count']} terms (£{stats['converting']['total_spend']:.2f} spend, {stats['converting']['total_conversions']:.1f} conv, {stats['converting']['roas']:.0f}% ROAS)")
    report.append(f"- Tier 1 (Strong negative candidates): {stats['tier1']['count']} terms (£{stats['tier1']['total_spend']:.2f} wasted spend)")
    report.append(f"- Tier 2 (Monitor closely): {stats['tier2']['count']} terms (£{stats['tier2']['total_spend']:.2f} spend)")
    report.append(f"- Tier 3 (Insufficient data): {stats['tier3']['count']} terms (£{stats['tier3']['total_spend']:.2f} spend)")
    report.append("")

    # Tier 1: Strong Negative Candidates
    report.append("-" * 80)
    report.append("TIER 1: STRONG NEGATIVE CANDIDATES")
    report.append("Criteria: 30+ clicks, 0 conversions, £20+ spend")
    report.append(f"Statistical confidence: HIGH ({stats['tier1']['count']} terms, £{stats['tier1']['total_spend']:.2f} total waste)")
    report.append("-" * 80)
    report.append("")

    if classified_terms['tier1']:
        report.append(f"{'Search Term':<40} {'Clicks':>8} {'Spend':>10} {'CPC':>8}")
        report.append("-" * 80)
        for term in classified_terms['tier1']:
            report.append(f"{term['search_term']:<40} {term['clicks']:>8} £{term['spend']:>9.2f} £{term['cpc']:>7.2f}")
    else:
        report.append("No terms meet Tier 1 criteria.")

    report.append("")
    report.append("")

    # Tier 2: Monitor Closely
    report.append("-" * 80)
    report.append("TIER 2: MONITOR CLOSELY")
    report.append("Criteria: 10-29 clicks, 0 conversions")
    report.append(f"Statistical confidence: MEDIUM ({stats['tier2']['count']} terms, £{stats['tier2']['total_spend']:.2f} total spend)")
    report.append("Action: Watch for next 30 days. Add to Tier 1 if pattern continues.")
    report.append("-" * 80)
    report.append("")

    if classified_terms['tier2']:
        report.append(f"{'Search Term':<40} {'Clicks':>8} {'Spend':>10} {'CPC':>8}")
        report.append("-" * 80)
        for term in classified_terms['tier2'][:20]:  # Show top 20
            report.append(f"{term['search_term']:<40} {term['clicks']:>8} £{term['spend']:>9.2f} £{term['cpc']:>7.2f}")

        if len(classified_terms['tier2']) > 20:
            report.append(f"\n... and {len(classified_terms['tier2']) - 20} more terms")
    else:
        report.append("No terms meet Tier 2 criteria.")

    report.append("")
    report.append("")

    # Tier 3: Insufficient Data
    report.append("-" * 80)
    report.append("TIER 3: INSUFFICIENT DATA")
    report.append("Criteria: <10 clicks in 60 days")
    report.append(f"Statistical confidence: LOW ({stats['tier3']['count']} terms, £{stats['tier3']['total_spend']:.2f} total spend)")
    report.append("Action: Need more data. Continue monitoring.")
    report.append("-" * 80)
    report.append("")
    report.append(f"Total terms in Tier 3: {stats['tier3']['count']}")
    report.append(f"Average clicks per term: {stats['tier3']['total_clicks'] / stats['tier3']['count']:.1f}" if stats['tier3']['count'] > 0 else "N/A")
    report.append("")
    report.append("(Individual terms not listed - insufficient statistical significance)")
    report.append("")
    report.append("")

    # Converting Terms (for context)
    report.append("-" * 80)
    report.append("CONVERTING TERMS (For Context)")
    report.append("These terms are performing well and should NOT be negated")
    report.append("-" * 80)
    report.append("")

    if classified_terms['converting']:
        report.append(f"{'Search Term':<40} {'Clicks':>8} {'Conv':>8} {'Revenue':>10} {'ROAS':>8}")
        report.append("-" * 80)
        for term in classified_terms['converting'][:20]:  # Show top 20
            report.append(f"{term['search_term']:<40} {term['clicks']:>8} {term['conversions']:>8.1f} £{term['revenue']:>9.2f} {term['roas']:>7.0f}%")

        if len(classified_terms['converting']) > 20:
            report.append(f"\n... and {len(classified_terms['converting']) - 20} more converting terms")
    else:
        report.append("No converting terms found.")

    report.append("")
    report.append("")
    report.append("=" * 80)
    report.append("END OF CLASSIFICATION REPORT")
    report.append("=" * 80)

    return "\n".join(report)

if __name__ == "__main__":
    # Note: This script template is ready for the actual search term data
    # The data will be processed from the GAQL query results
    print("Search term classification script ready.")
    print("Awaiting 60-day search term data input...")
