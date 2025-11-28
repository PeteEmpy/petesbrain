#!/usr/bin/env python3
"""
Product Baseline Calculator - Calculate per-product performance baselines

Reads historical product performance data from per-client spreadsheets and calculates
rolling baselines for each product. These baselines are used for anomaly detection.

Metrics calculated:
- 7-day average revenue, clicks, conversions, impressions
- 30-day average revenue, clicks, conversions, impressions
- Standard deviation for each metric
- Product label (hero/sidekick/villain/zombie) for sensitivity adjustment

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json python3 product_baseline_calculator.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import statistics

from google.oauth2 import service_account
from googleapiclient.discovery import build

class ProductBaselineCalculator:
    """Calculate per-product performance baselines"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.baselines_dir = self.base_dir / 'data' / 'product_baselines'
        self.baselines_dir.mkdir(parents=True, exist_ok=True)

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

    def load_historical_data(self, client_name: str, days: int = 30) -> List[Dict]:
        """
        Load historical product performance data from client's spreadsheet

        Args:
            client_name: Name of the client
            days: Number of days of history to load

        Returns:
            List of row dicts with parsed values
        """
        spreadsheet_id = self.client_spreadsheets.get(client_name)
        if not spreadsheet_id:
            self.log(f"  ⚠️  No spreadsheet ID for {client_name}")
            return []

        self.log(f"Loading {days} days of data for {client_name}...")

        try:
            # Read all data from Sheet1
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A:M'
            ).execute()

            values = result.get('values', [])

            if len(values) < 2:
                self.log(f"  ⚠️  No data in spreadsheet")
                return []

            # Parse header and data rows
            header = values[0]
            data_rows = values[1:]

            # Filter to last N days
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            filtered_rows = []
            for row in data_rows:
                if len(row) < 1:
                    continue

                date = row[0]
                if date >= cutoff_date:
                    # Parse row into dict
                    try:
                        row_dict = {
                            'date': row[0] if len(row) > 0 else '',
                            'client': row[1] if len(row) > 1 else '',
                            'product_id': row[2] if len(row) > 2 else '',
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
                        filtered_rows.append(row_dict)
                    except (ValueError, IndexError) as e:
                        # Skip malformed rows
                        continue

            self.log(f"  ✓ Loaded {len(filtered_rows)} rows from last {days} days")
            return filtered_rows

        except Exception as e:
            self.log(f"  ❌ Error loading data for {client_name}: {e}")
            return []

    def calculate_baselines(self, client_name: str, data: List[Dict]) -> Dict[str, Dict]:
        """
        Calculate per-product baselines from historical data

        Args:
            client_name: Name of the client
            data: List of historical data rows

        Returns:
            Dict mapping product_id to baseline metrics
        """
        self.log(f"Calculating baselines for {client_name}...")

        # Group data by product_id
        product_data = defaultdict(list)
        for row in data:
            product_id = row['product_id']
            product_data[product_id].append(row)

        # Calculate baselines for each product
        baselines = {}

        for product_id, rows in product_data.items():
            if len(rows) < 3:  # Need at least 3 data points
                continue

            # Get most recent label
            latest_row = max(rows, key=lambda r: r['date'])
            label = latest_row['label']

            # Calculate averages and standard deviations
            revenues = [r['revenue'] for r in rows if r['revenue'] > 0]
            clicks = [r['clicks'] for r in rows if r['clicks'] > 0]
            conversions = [r['conversions'] for r in rows if r['conversions'] > 0]
            impressions = [r['impressions'] for r in rows if r['impressions'] > 0]
            costs = [r['cost'] for r in rows if r['cost'] > 0]
            roas_values = [r['roas'] for r in rows if r['roas'] > 0]

            baseline = {
                'product_id': product_id,
                'product_title': latest_row['product_title'],
                'label': label,
                'data_points': len(rows),
                'date_range': f"{min(r['date'] for r in rows)} to {max(r['date'] for r in rows)}",
                'revenue': {
                    'mean': statistics.mean(revenues) if revenues else 0,
                    'median': statistics.median(revenues) if revenues else 0,
                    'stdev': statistics.stdev(revenues) if len(revenues) > 1 else 0,
                    'min': min(revenues) if revenues else 0,
                    'max': max(revenues) if revenues else 0
                },
                'clicks': {
                    'mean': statistics.mean(clicks) if clicks else 0,
                    'median': statistics.median(clicks) if clicks else 0,
                    'stdev': statistics.stdev(clicks) if len(clicks) > 1 else 0
                },
                'conversions': {
                    'mean': statistics.mean(conversions) if conversions else 0,
                    'median': statistics.median(conversions) if conversions else 0,
                    'stdev': statistics.stdev(conversions) if len(conversions) > 1 else 0
                },
                'impressions': {
                    'mean': statistics.mean(impressions) if impressions else 0,
                    'median': statistics.median(impressions) if impressions else 0,
                    'stdev': statistics.stdev(impressions) if len(impressions) > 1 else 0
                },
                'cost': {
                    'mean': statistics.mean(costs) if costs else 0,
                    'median': statistics.median(costs) if costs else 0,
                    'stdev': statistics.stdev(costs) if len(costs) > 1 else 0
                },
                'roas': {
                    'mean': statistics.mean(roas_values) if roas_values else 0,
                    'median': statistics.median(roas_values) if roas_values else 0,
                    'stdev': statistics.stdev(roas_values) if len(roas_values) > 1 else 0
                }
            }

            baselines[product_id] = baseline

        self.log(f"  ✓ Calculated baselines for {len(baselines)} products")
        return baselines

    def save_baselines(self, client_name: str, baselines: Dict[str, Dict]) -> bool:
        """
        Save baselines to disk

        Args:
            client_name: Name of the client
            baselines: Dict of baselines per product

        Returns:
            True if successful
        """
        if not baselines:
            self.log(f"  ⚠️  No baselines to save for {client_name}")
            return False

        baseline_path = self.baselines_dir / f"{client_name}.json"

        try:
            baseline_data = {
                'client': client_name,
                'updated': datetime.now().isoformat(),
                'product_count': len(baselines),
                'baselines': baselines
            }

            with open(baseline_path, 'w') as f:
                json.dump(baseline_data, f, indent=2)

            self.log(f"  ✓ Saved baselines to {baseline_path}")
            return True

        except Exception as e:
            self.log(f"  ❌ Error saving baselines for {client_name}: {e}")
            return False

    def calculate_all_clients(self, days: int = 30) -> Dict[str, int]:
        """
        Calculate baselines for all enabled clients

        Args:
            days: Number of days of historical data to use

        Returns:
            Dict mapping client names to product counts
        """
        self.log("="*80)
        self.log("PRODUCT BASELINE CALCULATOR")
        self.log("="*80)
        self.log(f"\nUsing {days} days of historical data\n")

        results = {}

        for client in self.config['clients']:
            if not client.get('enabled', True):
                continue

            client_name = client['name']

            # Load historical data
            data = self.load_historical_data(client_name, days)

            if not data:
                self.log(f"⚠️  No data for {client_name}, skipping\n")
                continue

            # Calculate baselines
            baselines = self.calculate_baselines(client_name, data)

            # Save baselines
            if baselines:
                success = self.save_baselines(client_name, baselines)
                if success:
                    results[client_name] = len(baselines)

            self.log("")

        self.log("="*80)
        self.log("BASELINE CALCULATION COMPLETE")
        self.log("="*80)
        self.log(f"\nClients processed: {len(results)}")
        for client_name, count in results.items():
            self.log(f"  {client_name}: {count} products")

        return results


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    calculator = ProductBaselineCalculator(config_path)
    calculator.calculate_all_clients(days=30)


if __name__ == "__main__":
    main()
