#!/usr/bin/env python3
"""
Wedding Venues Year-over-Year Analysis
Compares 2024 vs 2025 search interest
"""

from pytrends.request import TrendReq
import pandas as pd
import json
import time
from datetime import datetime

def analyze_wedding_venues():
    """Analyze wedding venues trends YoY"""

    print("=" * 60)
    print("Wedding Venues: 2024 vs 2025 Analysis")
    print("=" * 60)
    print("\nInitializing Google Trends connection...")

    pytrends = TrendReq(hl='en-GB', tz=0)

    # Get data for last 12 months
    print("Fetching trend data (this may take a moment)...")

    try:
        pytrends.build_payload(['wedding venues'], timeframe='today 12-m', geo='GB')
        df = pytrends.interest_over_time()

        if df.empty or 'wedding venues' not in df.columns:
            print("❌ No data available")
            return

        # Remove 'isPartial' column if present
        if 'isPartial' in df.columns:
            df = df.drop(columns=['isPartial'])

        # Organize data by year and month
        data_by_year = {2024: {}, 2025: {}}

        for date, row in df.iterrows():
            year = date.year
            month = date.strftime('%B')
            value = int(row['wedding venues'])

            if year in data_by_year:
                if month not in data_by_year[year]:
                    data_by_year[year][month] = []
                data_by_year[year][month].append(value)

        # Display comparison table
        print("\n" + "=" * 70)
        print("Monthly Comparison: Wedding Venues Search Interest")
        print("=" * 70)
        print(f"\n{'Month':<12} {'2024 Avg':<15} {'2025 Avg':<15} {'Change':<15}")
        print("-" * 70)

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        comparison_data = []

        for month in months:
            avg_2024 = None
            avg_2025 = None

            if month in data_by_year[2024] and data_by_year[2024][month]:
                avg_2024 = sum(data_by_year[2024][month]) / len(data_by_year[2024][month])

            if month in data_by_year[2025] and data_by_year[2025][month]:
                avg_2025 = sum(data_by_year[2025][month]) / len(data_by_year[2025][month])

            if avg_2024 is not None or avg_2025 is not None:
                str_2024 = f"{avg_2024:.1f}/100" if avg_2024 is not None else "No data"
                str_2025 = f"{avg_2025:.1f}/100" if avg_2025 is not None else "No data"

                if avg_2024 and avg_2025:
                    change_pct = ((avg_2025 - avg_2024) / avg_2024) * 100
                    change_str = f"{change_pct:+.1f}%"
                    arrow = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "→"
                    change_str = f"{arrow} {change_str}"

                    comparison_data.append({
                        'month': month,
                        '2024': avg_2024,
                        '2025': avg_2025,
                        'change': change_pct
                    })
                else:
                    change_str = "N/A"

                print(f"{month:<12} {str_2024:<15} {str_2025:<15} {change_str:<15}")

        # Overall statistics
        print("\n" + "=" * 70)
        print("Overall Statistics")
        print("=" * 70)

        all_2024 = [v for vals in data_by_year[2024].values() for v in vals]
        all_2025 = [v for vals in data_by_year[2025].values() for v in vals]

        if all_2024:
            print(f"\n2024:")
            print(f"  Average: {sum(all_2024)/len(all_2024):.1f}/100")
            print(f"  Peak: {max(all_2024)}/100")
            print(f"  Lowest: {min(all_2024)}/100")

        if all_2025:
            print(f"\n2025:")
            print(f"  Average: {sum(all_2025)/len(all_2025):.1f}/100")
            print(f"  Peak: {max(all_2025)}/100")
            print(f"  Lowest: {min(all_2025)}/100")

        if all_2024 and all_2025:
            yoy_change = ((sum(all_2025)/len(all_2025)) - (sum(all_2024)/len(all_2024))) / (sum(all_2024)/len(all_2024)) * 100
            print(f"\n📊 Overall Year-over-Year Change: {yoy_change:+.1f}%")

        # Key insights
        if comparison_data:
            print("\n" + "=" * 70)
            print("Key Insights")
            print("=" * 70)

            avg_change = sum(c['change'] for c in comparison_data) / len(comparison_data)
            max_gain = max(comparison_data, key=lambda x: x['change'])
            max_loss = min(comparison_data, key=lambda x: x['change'])

            print(f"\n✓ Average monthly change: {avg_change:+.1f}%")
            print(f"✓ Strongest month: {max_gain['month']} ({max_gain['change']:+.1f}%)")
            print(f"✓ Weakest month: {max_loss['month']} ({max_loss['change']:+.1f}%)")

            # Trend direction
            if avg_change > 5:
                trend = "📈 Strong upward trend - Search interest significantly higher in 2025"
            elif avg_change > 0:
                trend = "📈 Slight upward trend - Modest growth in 2025"
            elif avg_change > -5:
                trend = "📉 Slight downward trend - Small decline in 2025"
            else:
                trend = "📉 Strong downward trend - Search interest significantly lower in 2025"

            print(f"\n{trend}")

        # Save data
        output = {
            'keyword': 'wedding venues',
            'geo': 'GB',
            'analysis_date': datetime.now().isoformat(),
            'data_by_year': data_by_year,
            'comparison': comparison_data,
            'overall_stats': {
                '2024': {
                    'average': sum(all_2024)/len(all_2024) if all_2024 else None,
                    'max': max(all_2024) if all_2024 else None,
                    'min': min(all_2024) if all_2024 else None
                },
                '2025': {
                    'average': sum(all_2025)/len(all_2025) if all_2025 else None,
                    'max': max(all_2025) if all_2025 else None,
                    'min': min(all_2025) if all_2025 else None
                }
            }
        }

        output_file = '/tmp/wedding_venues_yoy.json'
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✅ Data saved to: {output_file}")
        print("\n" + "=" * 70)

    except Exception as e:
        if '429' in str(e):
            print("\n⚠️  Rate limit reached. Please wait 60 seconds and try again.")
            print("Google Trends allows ~10 requests per minute.")
        else:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    analyze_wedding_venues()
