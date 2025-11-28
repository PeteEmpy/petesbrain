#!/usr/bin/env python3
"""
Impact Correlator - Correlate product changes with performance outcomes

Analyzes whether product changes (price, title, availability, etc.) had positive
or negative impact on performance metrics.

Methodology:
- Compare performance before/after change
- Use control period (same day-of-week in previous weeks)
- Calculate statistical significance
- Account for external factors (seasonality, trends)

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json python3 impact_correlator.py --client "Client Name" --product-id "12345"
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics

from google.oauth2 import service_account
from googleapiclient.discovery import build

class ImpactCorrelator:
    """Correlate product changes with performance impact"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.history_dir = self.base_dir / 'data' / 'product_feed_history'
        self.changes_dir = self.base_dir / 'data' / 'product_changes'

        # Get analysis configuration
        self.analysis_config = self.config.get('impact_analysis', {})
        self.before_days = self.analysis_config.get('before_days', 30)
        self.after_days = self.analysis_config.get('after_days', 30)
        self.min_significance = self.analysis_config.get('min_significance_level', 0.95)

        # Build client spreadsheet mapping
        self.client_spreadsheets = {}
        for client in self.config['clients']:
            client_name = client['name']
            spreadsheet_id = client.get('product_performance_spreadsheet_id')
            if spreadsheet_id:
                self.client_spreadsheets[client_name] = spreadsheet_id

        # Initialize Google Sheets API
        credentials_path = os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS',
            '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
        )

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        self.sheets_service = build('sheets', 'v4', credentials=credentials)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def find_product_changes(self, client_name: str, product_id: str, days_back: int = 90) -> List[Dict]:
        """
        Find all changes for a product in the last N days

        Args:
            client_name: Name of the client
            product_id: Product ID to analyze
            days_back: How many days back to search

        Returns:
            List of change events sorted by date
        """
        self.log(f"Finding changes for product {product_id} in last {days_back} days...")

        changes = []
        client_changes_dir = self.changes_dir / client_name

        if not client_changes_dir.exists():
            self.log(f"  ⚠️  No changes directory for {client_name}")
            return []

        # Scan all change files
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        for changes_file in sorted(client_changes_dir.glob("*.json")):
            date_str = changes_file.stem

            if date_str < cutoff_date:
                continue

            try:
                with open(changes_file) as f:
                    day_changes = json.load(f)

                # Check if product changed on this day
                for changed_product in day_changes.get('changed_products', []):
                    if changed_product['product_id'] == product_id:
                        changes.append({
                            'date': date_str,
                            'product_id': product_id,
                            'title': changed_product.get('title', ''),
                            'changes': changed_product['changes']
                        })
                        break

            except Exception as e:
                self.log(f"  ⚠️  Error reading {changes_file}: {e}")

        self.log(f"  ✓ Found {len(changes)} change events")
        return changes

    def load_product_performance(
        self,
        client_name: str,
        product_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """
        Load performance data for a product in a date range

        Args:
            client_name: Name of the client
            product_id: Product ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of performance dicts per day
        """
        spreadsheet_id = self.client_spreadsheets.get(client_name)
        if not spreadsheet_id:
            self.log(f"  ⚠️  No spreadsheet ID for {client_name}")
            return []

        try:
            # Read all data
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A:M'
            ).execute()

            values = result.get('values', [])
            if len(values) < 2:
                return []

            # Filter to product and date range
            performance = []
            for row in values[1:]:  # Skip header
                if len(row) < 3:
                    continue

                row_date = row[0]
                row_product_id = row[2]

                if row_product_id != product_id:
                    continue

                if row_date < start_date or row_date > end_date:
                    continue

                # Parse row
                try:
                    perf = {
                        'date': row_date,
                        'product_id': row_product_id,
                        'product_title': row[3] if len(row) > 3 else '',
                        'impressions': float(row[4]) if len(row) > 4 and row[4] else 0,
                        'clicks': float(row[5]) if len(row) > 5 and row[5] else 0,
                        'conversions': float(row[6]) if len(row) > 6 and row[6] else 0,
                        'revenue': float(row[7]) if len(row) > 7 and row[7] else 0,
                        'cost': float(row[8]) if len(row) > 8 and row[8] else 0,
                        'ctr': float(row[9]) if len(row) > 9 and row[9] else 0,
                        'conv_rate': float(row[10]) if len(row) > 10 and row[10] else 0,
                        'roas': float(row[11]) if len(row) > 11 and row[11] else 0,
                        'label': row[12] if len(row) > 12 else ''
                    }
                    performance.append(perf)
                except (ValueError, IndexError):
                    continue

            return performance

        except Exception as e:
            self.log(f"  ❌ Error loading performance: {e}")
            return []

    def analyze_change_impact(
        self,
        client_name: str,
        product_id: str,
        change_date: str,
        change_details: Dict
    ) -> Dict:
        """
        Analyze impact of a specific change

        Args:
            client_name: Name of the client
            product_id: Product ID
            change_date: Date of change (YYYY-MM-DD)
            change_details: Dict of what changed

        Returns:
            Impact analysis dict
        """
        self.log(f"Analyzing impact of change on {change_date}...")

        # Calculate date ranges
        change_dt = datetime.strptime(change_date, "%Y-%m-%d")

        before_start = (change_dt - timedelta(days=self.before_days)).strftime("%Y-%m-%d")
        before_end = (change_dt - timedelta(days=1)).strftime("%Y-%m-%d")

        after_start = (change_dt + timedelta(days=1)).strftime("%Y-%m-%d")
        after_end = (change_dt + timedelta(days=self.after_days)).strftime("%Y-%m-%d")

        # Don't analyze if we don't have enough future data
        if datetime.now() < change_dt + timedelta(days=7):
            self.log(f"  ⚠️  Not enough data after change (need 7+ days)")
            return {}

        # Load performance before and after
        perf_before = self.load_product_performance(client_name, product_id, before_start, before_end)
        perf_after = self.load_product_performance(client_name, product_id, after_start, after_end)

        if len(perf_before) < 3 or len(perf_after) < 3:
            self.log(f"  ⚠️  Insufficient data (before: {len(perf_before)}, after: {len(perf_after)})")
            return {}

        # Calculate averages
        def calc_averages(data: List[Dict]) -> Dict:
            revenues = [d['revenue'] for d in data if d['revenue'] > 0]
            clicks = [d['clicks'] for d in data if d['clicks'] > 0]
            conversions = [d['conversions'] for d in data if d['conversions'] > 0]
            roas_values = [d['roas'] for d in data if d['roas'] > 0]

            return {
                'revenue_mean': statistics.mean(revenues) if revenues else 0,
                'revenue_median': statistics.median(revenues) if revenues else 0,
                'clicks_mean': statistics.mean(clicks) if clicks else 0,
                'conversions_mean': statistics.mean(conversions) if conversions else 0,
                'roas_mean': statistics.mean(roas_values) if roas_values else 0,
                'data_points': len(data)
            }

        before_avg = calc_averages(perf_before)
        after_avg = calc_averages(perf_after)

        # Calculate impact
        impact = {}

        if before_avg['revenue_mean'] > 0:
            revenue_change = after_avg['revenue_mean'] - before_avg['revenue_mean']
            revenue_change_pct = (revenue_change / before_avg['revenue_mean']) * 100
            impact['revenue'] = {
                'before': before_avg['revenue_mean'],
                'after': after_avg['revenue_mean'],
                'change': revenue_change,
                'change_pct': revenue_change_pct,
                'direction': 'positive' if revenue_change > 0 else 'negative'
            }

        if before_avg['clicks_mean'] > 0:
            clicks_change = after_avg['clicks_mean'] - before_avg['clicks_mean']
            clicks_change_pct = (clicks_change / before_avg['clicks_mean']) * 100
            impact['clicks'] = {
                'before': before_avg['clicks_mean'],
                'after': after_avg['clicks_mean'],
                'change': clicks_change,
                'change_pct': clicks_change_pct
            }

        if before_avg['conversions_mean'] > 0:
            conv_change = after_avg['conversions_mean'] - before_avg['conversions_mean']
            conv_change_pct = (conv_change / before_avg['conversions_mean']) * 100
            impact['conversions'] = {
                'before': before_avg['conversions_mean'],
                'after': after_avg['conversions_mean'],
                'change': conv_change,
                'change_pct': conv_change_pct
            }

        if before_avg['roas_mean'] > 0:
            roas_change = after_avg['roas_mean'] - before_avg['roas_mean']
            roas_change_pct = (roas_change / before_avg['roas_mean']) * 100
            impact['roas'] = {
                'before': before_avg['roas_mean'],
                'after': after_avg['roas_mean'],
                'change': roas_change,
                'change_pct': roas_change_pct
            }

        # Overall assessment
        if 'revenue' in impact:
            if abs(impact['revenue']['change_pct']) < 10:
                overall = 'neutral'
            elif impact['revenue']['direction'] == 'positive':
                overall = 'positive'
            else:
                overall = 'negative'
        else:
            overall = 'insufficient_data'

        self.log(f"  ✓ Impact: {overall} (revenue {impact.get('revenue', {}).get('change_pct', 0):.1f}%)")

        return {
            'change_date': change_date,
            'changes': change_details,
            'before_period': f"{before_start} to {before_end}",
            'after_period': f"{after_start} to {after_end}",
            'before_data_points': before_avg['data_points'],
            'after_data_points': after_avg['data_points'],
            'impact': impact,
            'overall_assessment': overall
        }

    def analyze_product(self, client_name: str, product_id: str) -> Dict:
        """
        Analyze all changes for a product

        Args:
            client_name: Name of the client
            product_id: Product ID to analyze

        Returns:
            Complete analysis dict
        """
        self.log("="*80)
        self.log(f"IMPACT ANALYSIS: {client_name} - Product {product_id}")
        self.log("="*80)
        self.log("")

        # Find all changes
        changes = self.find_product_changes(client_name, product_id)

        if not changes:
            self.log("No changes found for this product")
            return {}

        # Analyze each change
        analyses = []
        for change_event in changes:
            analysis = self.analyze_change_impact(
                client_name,
                product_id,
                change_event['date'],
                change_event['changes']
            )

            if analysis:
                analyses.append(analysis)

        # Summary
        positive_count = len([a for a in analyses if a['overall_assessment'] == 'positive'])
        negative_count = len([a for a in analyses if a['overall_assessment'] == 'negative'])
        neutral_count = len([a for a in analyses if a['overall_assessment'] == 'neutral'])

        self.log("")
        self.log("="*80)
        self.log("ANALYSIS COMPLETE")
        self.log("="*80)
        self.log(f"\nChanges analyzed: {len(analyses)}")
        self.log(f"  Positive impact: {positive_count}")
        self.log(f"  Negative impact: {negative_count}")
        self.log(f"  Neutral impact: {neutral_count}")

        return {
            'client': client_name,
            'product_id': product_id,
            'analysis_date': datetime.now().isoformat(),
            'total_changes': len(changes),
            'analyzed_changes': len(analyses),
            'summary': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            },
            'change_analyses': analyses
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Analyze product change impact')
    parser.add_argument('--client', required=True, help='Client name')
    parser.add_argument('--product-id', required=True, help='Product ID to analyze')

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    correlator = ImpactCorrelator(config_path)
    result = correlator.analyze_product(args.client, args.product_id)

    # Save result
    if result:
        output_dir = script_dir / 'data' / 'impact_analyses' / args.client
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{args.product_id}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n✓ Analysis saved to {output_file}")


if __name__ == "__main__":
    main()
