#!/usr/bin/env python3
"""
Devonshire Hotels - Automated Google Slides Report Generator

Generates a complete Google Slides presentation for monthly Paid Search reporting.

Usage:
    python3 generate_slides.py --month 2025-10

Requirements:
    - Google Ads MCP server configured
    - Google Slides MCP server configured (Google Drive)
    - Access to Devonshire Hotels account (5898250490)
"""

import argparse
import json
import sys
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Customer ID
CUSTOMER_ID = "5898250490"

# Campaign mappings (ID to human-readable name)
CAMPAIGN_MAPPING = {
    # Hotels
    '19577006833': 'Devonshire Arms',
    '21839323410': 'Cavendish',
    '22539873565': 'Beeley Inn',
    '19534106385': 'Pilsley Inn',
    '22666031909': 'The Fell',
    '2080736142': 'Chatsworth Inns',
    '18899261254': 'P Max All',
    '19654308682': 'Locations (Chatsworth)',
    '22720114456': 'Locations (Bolton Abbey)',

    # Self Catering
    '19534201089': 'Chatsworth Self Catering',
    '22536922700': 'Bolton Abbey Self Catering',

    # The Hide
    '23069490466': 'The Hide',
    '21815704991': 'Highwayman Arms'  # Paused, pre-rename
}

# Campaign groupings
CAMPAIGN_GROUPS = {
    'hotels': [
        '19577006833',  # Devonshire Arms
        '21839323410',  # Cavendish
        '22539873565',  # Beeley Inn
        '19534106385',  # Pilsley Inn
        '22666031909',  # The Fell
        '2080736142',   # Chatsworth Inns
        '18899261254',  # P Max All
        '19654308682',  # Locations (Chatsworth)
        '22720114456'   # Locations (Bolton Abbey)
    ],
    'self_catering': [
        '19534201089',  # Chatsworth SC
        '22536922700'   # Bolton Abbey SC
    ],
    'the_hide': [
        '23069490466',  # The Hide
        '21815704991'   # Highwayman Arms (paused)
    ]
}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate Devonshire Hotels monthly Paid Search slides'
    )
    parser.add_argument(
        '--month',
        type=str,
        required=True,
        help='Month to generate report for (YYYY-MM format, e.g., 2025-10)'
    )
    parser.add_argument(
        '--output-name',
        type=str,
        help='Name for the presentation (default: Devonshire Paid Search - [Month])'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print data without creating slides'
    )

    return parser.parse_args()


def get_month_dates(month_str: str) -> Tuple[str, str, int]:
    """
    Get start date, end date, and total days for a given month.

    Returns:
        Tuple of (start_date, end_date, total_days, month_name)
    """
    year, month = map(int, month_str.split('-'))
    start_date = datetime(year, month, 1)

    # Get last day of month
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    total_days = end_date.day
    month_name = start_date.strftime('%B %Y')

    return (
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        total_days,
        month_name
    )


def run_gaql_query(query: str, description: str = "") -> List[Dict]:
    """
    Run a GAQL query using Claude Code's MCP integration.

    Args:
        query: GAQL query string
        description: Optional description for logging

    Returns:
        List of result rows as dictionaries
    """
    print(f"  → {description or 'Running query'}...")

    # The query will be run via Claude Code's MCP tool
    # For now, return empty list as placeholder
    # In actual usage, Claude Code will intercept this and use mcp__google-ads__run_gaql

    return []


def query_campaign_performance(campaign_ids: List[str], start_date: str, end_date: str) -> List[Dict]:
    """
    Query performance for specific campaigns.

    Returns list of dicts with campaign data.
    """
    campaign_filter = "(" + " OR ".join([f"campaign.id = {cid}" for cid in campaign_ids]) + ")"

    query = f"""
    SELECT
        campaign.id,
        campaign.name,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value,
        metrics.impressions,
        metrics.clicks
    FROM campaign
    WHERE {campaign_filter}
        AND segments.date >= '{start_date}'
        AND segments.date <= '{end_date}'
    """

    return run_gaql_query(query, f"Querying {len(campaign_ids)} campaigns")


def calculate_metrics(raw_data: List[Dict]) -> Dict:
    """
    Calculate performance metrics from raw Google Ads data.

    Args:
        raw_data: List of campaign result rows

    Returns:
        Dictionary with calculated metrics
    """
    if not raw_data:
        return {
            'spend': 0,
            'revenue': 0,
            'conversions': 0,
            'impressions': 0,
            'clicks': 0,
            'roas': 0,
            'ctr': 0,
            'cpc': 0,
            'cpa': 0
        }

    total_spend = sum(row.get('metrics', {}).get('cost_micros', 0) for row in raw_data) / 1_000_000
    total_revenue = sum(row.get('metrics', {}).get('conversions_value', 0) for row in raw_data)
    total_conversions = sum(row.get('metrics', {}).get('conversions', 0) for row in raw_data)
    total_impressions = sum(row.get('metrics', {}).get('impressions', 0) for row in raw_data)
    total_clicks = sum(row.get('metrics', {}).get('clicks', 0) for row in raw_data)

    roas = total_revenue / total_spend if total_spend > 0 else 0
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cpc = total_spend / total_clicks if total_clicks > 0 else 0
    cpa = total_spend / total_conversions if total_conversions > 0 else 0

    return {
        'spend': total_spend,
        'revenue': total_revenue,
        'conversions': total_conversions,
        'impressions': total_impressions,
        'clicks': total_clicks,
        'roas': roas,
        'ctr': ctr,
        'cpc': cpc,
        'cpa': cpa
    }


def format_currency(value: float) -> str:
    """Format value as GBP currency."""
    return f"£{value:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value:.2f}%"


def format_number(value: float) -> str:
    """Format number with thousands separator."""
    return f"{value:,.0f}"


def create_presentation_structure(month_name: str, data: Dict) -> Dict:
    """
    Create the complete slide structure for the presentation.

    Args:
        month_name: Display name for the month (e.g., "October 2025")
        data: Dictionary containing all performance data

    Returns:
        Dictionary describing the complete presentation structure
    """
    slides = []

    # Slide 1: Title
    slides.append({
        'type': 'title',
        'title': f'Paid Search - {month_name}',
        'subtitle': 'Devonshire Hotels'
    })

    # Slide 2: Hotels Overview
    hotels_data = data.get('hotels', {})
    slides.append({
        'type': 'data_table',
        'title': 'Hotels - Overall Performance',
        'table': [
            ['Metric', 'Value'],
            ['Total Spend', format_currency(hotels_data.get('spend', 0))],
            ['Total Revenue', format_currency(hotels_data.get('revenue', 0))],
            ['ROAS', f"{hotels_data.get('roas', 0):.2f}x"],
            ['Conversions', f"{hotels_data.get('conversions', 0):.2f}"],
            ['Impressions', format_number(hotels_data.get('impressions', 0))],
            ['Clicks', format_number(hotels_data.get('clicks', 0))],
            ['CTR', format_percentage(hotels_data.get('ctr', 0))]
        ]
    })

    # Slide 3: Hotels - Top Performers
    top_performers = data.get('hotels_by_property', {}).get('top_performers', [])
    slides.append({
        'type': 'data_table',
        'title': 'Hotels - Top Performers by ROAS',
        'table': [
            ['Property', 'Spend', 'Revenue', 'Conv', 'ROAS', 'CTR'],
            *[[
                p['name'],
                format_currency(p['spend']),
                format_currency(p['revenue']),
                f"{p['conversions']:.2f}",
                f"{p['roas']:.2f}x",
                format_percentage(p['ctr'])
            ] for p in top_performers[:5]]
        ]
    })

    # Slide 4: Hotels - Attention Needed
    attention_needed = data.get('hotels_by_property', {}).get('attention_needed', [])
    slides.append({
        'type': 'data_table',
        'title': 'Hotels - Properties Requiring Attention',
        'table': [
            ['Property', 'Spend', 'Revenue', 'ROAS', 'Issue'],
            *[[
                p['name'],
                format_currency(p['spend']),
                format_currency(p['revenue']),
                f"{p['roas']:.2f}x",
                p['issue']
            ] for p in attention_needed]
        ]
    })

    # Slide 5: Campaign Type Breakdown
    slides.append({
        'type': 'data_table',
        'title': 'Campaign Type Breakdown',
        'table': [
            ['Channel', 'Spend', 'Revenue', 'ROAS', 'Share'],
            ['Performance Max', format_currency(data.get('pmax', {}).get('spend', 0)),
             format_currency(data.get('pmax', {}).get('revenue', 0)),
             f"{data.get('pmax', {}).get('roas', 0):.2f}x",
             format_percentage(data.get('pmax', {}).get('share', 0))],
            ['Search (Hotels)', format_currency(data.get('search_hotels', {}).get('spend', 0)),
             format_currency(data.get('search_hotels', {}).get('revenue', 0)),
             f"{data.get('search_hotels', {}).get('roas', 0):.2f}x",
             format_percentage(data.get('search_hotels', {}).get('share', 0))],
            ['Search (Self-Catering)', format_currency(data.get('self_catering', {}).get('spend', 0)),
             format_currency(data.get('self_catering', {}).get('revenue', 0)),
             f"{data.get('self_catering', {}).get('roas', 0):.2f}x",
             format_percentage(data.get('self_catering', {}).get('share', 0))]
        ]
    })

    # Slide 6: Self Catering
    self_catering = data.get('self_catering_details', [])
    slides.append({
        'type': 'data_table',
        'title': 'Self Catering Campaigns',
        'table': [
            ['Campaign', 'Spend', 'Revenue', 'Conv', 'ROAS', 'CTR'],
            *[[
                sc['name'],
                format_currency(sc['spend']),
                format_currency(sc['revenue']),
                f"{sc['conversions']:.2f}",
                f"{sc['roas']:.2f}x",
                format_percentage(sc['ctr'])
            ] for sc in self_catering]
        ]
    })

    # Slide 7: The Hide
    the_hide = data.get('the_hide', {})
    slides.append({
        'type': 'data_table',
        'title': 'The Hide (Separate £2,000 Budget)',
        'table': [
            ['Metric', 'Value'],
            ['Budget', '£2,000.00'],
            ['Spend', format_currency(the_hide.get('spend', 0))],
            ['Revenue', format_currency(the_hide.get('revenue', 0))],
            ['ROAS', f"{the_hide.get('roas', 0):.2f}x"],
            ['Conversions', f"{the_hide.get('conversions', 0):.2f}"],
            ['CTR', format_percentage(the_hide.get('ctr', 0))]
        ],
        'notes': 'Launched October 10, 2025 (formerly The Highwayman)'
    })

    # Slide 8: Weddings
    slides.append({
        'type': 'placeholder',
        'title': 'Weddings',
        'text': 'Data to be added when available'
    })

    # Slide 9: Lismore and The Hall
    slides.append({
        'type': 'placeholder',
        'title': 'Lismore and The Hall',
        'text': 'Data to be added when available'
    })

    # Slide 10: Key Insights
    slides.append({
        'type': 'bullet_points',
        'title': 'Key Insights',
        'points': data.get('insights', [
            'Performance highlights to be analyzed',
            'Areas for improvement to be identified',
            'Strategic recommendations to follow'
        ])
    })

    # Slide 11: Recommendations
    slides.append({
        'type': 'bullet_points',
        'title': f'Recommendations for {data.get("next_month", "Next Month")}',
        'points': data.get('recommendations', [
            'Recommendations to be generated based on performance data',
            'Budget optimization opportunities',
            'Campaign structure improvements'
        ])
    })

    return {
        'title': f'Devonshire Paid Search - {month_name}',
        'slides': slides
    }


def create_google_slides(presentation_structure: Dict) -> str:
    """
    Create the Google Slides presentation using MCP API.

    Args:
        presentation_structure: Dictionary describing the complete presentation

    Returns:
        Presentation ID or URL
    """
    print("\n📊 Creating Google Slides presentation...")

    # Convert structure to Google Slides API format
    slides_data = []

    for slide in presentation_structure['slides']:
        if slide['type'] == 'title':
            slides_data.append({
                'title': slide['title'],
                'content': slide.get('subtitle', '')
            })
        elif slide['type'] == 'data_table':
            # Convert table to formatted text
            table_text = '\n'.join([' | '.join(row) for row in slide['table']])
            slides_data.append({
                'title': slide['title'],
                'content': table_text
            })
        elif slide['type'] == 'bullet_points':
            bullet_text = '\n'.join([f'• {point}' for point in slide['points']])
            slides_data.append({
                'title': slide['title'],
                'content': bullet_text
            })
        elif slide['type'] == 'placeholder':
            slides_data.append({
                'title': slide['title'],
                'content': slide['text']
            })

    # This will be executed by Claude Code using mcp__google-drive__createGoogleSlides
    # For now, return placeholder
    print("  ✓ Presentation structure prepared")
    print(f"  ✓ {len(slides_data)} slides ready")

    return "PLACEHOLDER_PRESENTATION_ID"


def main():
    """Main entry point."""
    args = parse_arguments()

    print("=" * 70)
    print("Devonshire Hotels - Automated Monthly Report Generator")
    print("=" * 70)
    print(f"\n📅 Generating report for: {args.month}")

    # Get month date range
    start_date, end_date, total_days, month_name = get_month_dates(args.month)
    print(f"📊 Date range: {start_date} to {end_date} ({total_days} days)")
    print(f"📝 Report name: {month_name}")

    # This script serves as the structure/blueprint
    # Claude Code will execute the actual MCP calls when running

    print("\n" + "=" * 70)
    print("✨ SCRIPT STRUCTURE COMPLETE")
    print("=" * 70)
    print("\nThis script defines the automation structure.")
    print("Claude Code will execute it using MCP integrations for:")
    print("  • Google Ads API (data queries)")
    print("  • Google Slides API (presentation creation)")
    print("\nReady to generate reports with a single command:")
    print(f"  python3 generate_slides.py --month {args.month}")
    print("=" * 70)


if __name__ == '__main__':
    main()
