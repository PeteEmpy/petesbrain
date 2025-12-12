#!/usr/bin/env python3
"""
GA4 Landing Page Analysis for NDA Interior Design Diploma
Compares pre-launch and post-launch performance using GA4 data
"""

import sys
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, FilterExpression, Filter
from google.api_core.exceptions import GoogleAPIError
from pathlib import Path

# Constants
PROPERTY_ID = "354570005"
LANDING_PAGE_PATH = "/study/courses/diploma-interior-design"

# Date ranges
PRE_LAUNCH_START = "2025-11-04"
PRE_LAUNCH_END = "2025-11-21"
POST_LAUNCH_START = "2025-11-22"
POST_LAUNCH_END = "2025-12-09"

def run_ga4_query(property_id, start_date, end_date, dimensions, metrics, filter_expr=None):
    """Execute a GA4 report query"""

    client = BetaAnalyticsDataClient()

    # Build dimension list
    dim_list = [Dimension(name=d) for d in dimensions]

    # Build metric list
    metric_list = [Metric(name=m) for m in metrics]

    # Build request
    request = {
        "property": f"properties/{property_id}",
        "date_ranges": [DateRange(start_date=start_date, end_date=end_date)],
        "dimensions": dim_list,
        "metrics": metric_list,
    }

    # Add filter if specified
    if filter_expr:
        request["dimension_filter"] = filter_expr

    try:
        response = client.run_report(request)
        return response
    except GoogleAPIError as e:
        print(f"❌ GA4 API Error: {e}", file=sys.stderr)
        return None


def parse_response(response):
    """Convert GA4 response to readable format"""
    if not response or not response.rows:
        return []

    results = []
    for row in response.rows:
        row_data = {}

        # Add dimensions
        for i, dim_value in enumerate(row.dimension_values):
            dim_name = response.dimension_headers[i].name
            row_data[dim_name] = dim_value.value

        # Add metrics
        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            try:
                row_data[metric_name] = float(metric_value.value)
            except ValueError:
                row_data[metric_name] = metric_value.value

        results.append(row_data)

    return results


def main():
    print("🔍 GA4 Landing Page Analysis - NDA Interior Design Diploma")
    print("=" * 70)

    # Query 1: Daily performance comparison (page path)
    print("\n📊 Query 1: Daily Page Performance (by date)")
    print("-" * 70)

    try:
        # Pre-launch daily data
        print(f"\n📈 PRE-LAUNCH ({PRE_LAUNCH_START} to {PRE_LAUNCH_END})")
        pre_response = run_ga4_query(
            PROPERTY_ID,
            PRE_LAUNCH_START,
            PRE_LAUNCH_END,
            dimensions=["date", "pagePath"],
            metrics=["screenPageViews", "bounceRate", "averageSessionDuration", "totalUsers"]
        )

        if pre_response:
            pre_data = parse_response(pre_response)
            print(f"✅ Retrieved {len(pre_data)} rows of pre-launch data")

            # Filter for landing page
            landing_page_data = [r for r in pre_data if LANDING_PAGE_PATH in r.get('pagePath', '')]
            print(f"   Landing page rows: {len(landing_page_data)}")

            if landing_page_data:
                total_views = sum(r.get('screenPageViews', 0) for r in landing_page_data)
                avg_bounce = sum(r.get('bounceRate', 0) for r in landing_page_data) / len(landing_page_data) if landing_page_data else 0
                print(f"   Total views: {total_views}")
                print(f"   Avg bounce rate: {avg_bounce:.1f}%")

        # Post-launch daily data
        print(f"\n📉 POST-LAUNCH ({POST_LAUNCH_START} to {POST_LAUNCH_END})")
        post_response = run_ga4_query(
            PROPERTY_ID,
            POST_LAUNCH_START,
            POST_LAUNCH_END,
            dimensions=["date", "pagePath"],
            metrics=["screenPageViews", "bounceRate", "averageSessionDuration", "totalUsers"]
        )

        if post_response:
            post_data = parse_response(post_response)
            print(f"✅ Retrieved {len(post_data)} rows of post-launch data")

            # Filter for landing page
            landing_page_data = [r for r in post_data if LANDING_PAGE_PATH in r.get('pagePath', '')]
            print(f"   Landing page rows: {len(landing_page_data)}")

            if landing_page_data:
                total_views = sum(r.get('screenPageViews', 0) for r in landing_page_data)
                avg_bounce = sum(r.get('bounceRate', 0) for r in landing_page_data) / len(landing_page_data) if landing_page_data else 0
                print(f"   Total views: {total_views}")
                print(f"   Avg bounce rate: {avg_bounce:.1f}%")

        # Query 2: Traffic source comparison
        print("\n\n📊 Query 2: Traffic Source Comparison")
        print("-" * 70)

        print(f"\n🔗 PRE-LAUNCH Traffic Sources")
        pre_source = run_ga4_query(
            PROPERTY_ID,
            PRE_LAUNCH_START,
            PRE_LAUNCH_END,
            dimensions=["source", "medium"],
            metrics=["sessions", "users", "screenPageViews", "bounceRate"]
        )

        if pre_source:
            source_data = parse_response(pre_source)
            print(f"✅ Retrieved {len(source_data)} traffic sources")
            # Show top 5
            sorted_data = sorted(source_data, key=lambda x: x.get('sessions', 0), reverse=True)[:5]
            for row in sorted_data:
                print(f"   {row.get('source')} / {row.get('medium')}: {row.get('sessions')} sessions")

        print(f"\n🔗 POST-LAUNCH Traffic Sources")
        post_source = run_ga4_query(
            PROPERTY_ID,
            POST_LAUNCH_START,
            POST_LAUNCH_END,
            dimensions=["source", "medium"],
            metrics=["sessions", "users", "screenPageViews", "bounceRate"]
        )

        if post_source:
            source_data = parse_response(post_source)
            print(f"✅ Retrieved {len(source_data)} traffic sources")
            # Show top 5
            sorted_data = sorted(source_data, key=lambda x: x.get('sessions', 0), reverse=True)[:5]
            for row in sorted_data:
                print(f"   {row.get('source')} / {row.get('medium')}: {row.get('sessions')} sessions")

        print("\n" + "=" * 70)
        print("✅ GA4 Analysis Complete")

    except Exception as e:
        print(f"\n❌ Error during analysis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
