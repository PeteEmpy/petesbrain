#!/usr/bin/env python3
"""
Asset Performance Analyser - Identify underperforming PMAX text assets

This script reads the Google Ads Asset performance report CSV and identifies
underperforming text assets based on statistical thresholds.

Author: PetesBrain
Created: 2025-11-25
"""

import csv
import yaml
import sys
from typing import List, Dict, Tuple
from pathlib import Path
from datetime import datetime


class AssetPerformanceAnalyser:
    """Analyses asset performance data and identifies underperformers"""

    def __init__(self, config_path: str):
        """
        Initialise analyser with configuration

        Args:
            config_path: Path to config.yaml file
        """
        self.config = self._load_config(config_path)
        self.assets = []
        self.pmax_text_assets = []
        self.stats = {}

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def load_asset_report(self, csv_path: str):
        """
        Load and parse Asset performance report CSV

        Args:
            csv_path: Path to Asset performance report CSV
        """
        print(f"📂 Loading Asset performance report: {csv_path}")

        with open(csv_path, 'r', encoding='utf-8') as f:
            # Skip first 2 rows (title and date range)
            next(f)
            next(f)

            reader = csv.DictReader(f)
            self.assets = list(reader)

        print(f"✅ Loaded {len(self.assets)} total assets")

    def filter_pmax_text_assets(self):
        """Filter to Performance Max text assets only"""
        campaign_types = self.config['analysis']['campaign_types']
        asset_types = self.config['analysis']['asset_types']
        exclude_google_ai = self.config['analysis']['exclude_google_ai_assets']

        self.pmax_text_assets = []

        for asset in self.assets:
            # Check campaign type (skip if column doesn't exist - assume all PMAX)
            if 'Campaign type' in asset and asset.get('Campaign type') not in campaign_types:
                continue

            # Check asset type
            if asset.get('Asset type') not in asset_types:
                continue

            # Optionally exclude Google AI assets
            if exclude_google_ai and asset.get('Added by') == 'Google AI':
                continue

            self.pmax_text_assets.append(asset)

        print(f"📊 Filtered to {len(self.pmax_text_assets)} Performance Max text assets")
        print(f"   - Excluding Google AI: {exclude_google_ai}")

    def calculate_campaign_averages(self) -> Dict[str, float]:
        """
        Calculate campaign-wide average performance metrics

        Returns:
            Dictionary with average CTR, conv rate, cost per conv
        """
        print("\n📈 Calculating campaign averages...")

        total_impressions = 0
        total_clicks = 0
        total_conversions = 0
        total_cost = 0

        for asset in self.pmax_text_assets:
            # Parse metrics (handle formatting)
            impr = self._parse_number(asset.get('Impr.', '0'))
            clicks_str = asset.get('Clicks', '0')  # Might not be in CSV
            ctr_str = asset.get('CTR', '0%')
            cost = self._parse_number(asset.get('Cost', '0'))
            conv = self._parse_number(asset.get('Conversions', '0'))

            total_impressions += impr

            # Calculate clicks from CTR if not directly available
            if impr > 0 and ctr_str:
                ctr_val = self._parse_percentage(ctr_str)
                clicks = int(impr * (ctr_val / 100))
                total_clicks += clicks

            total_cost += cost
            total_conversions += conv

        # Calculate averages
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_conv_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        avg_cost_per_conv = (total_cost / total_conversions) if total_conversions > 0 else 0

        self.stats = {
            'avg_ctr': avg_ctr,
            'avg_conv_rate': avg_conv_rate,
            'avg_cost_per_conv': avg_cost_per_conv,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_cost': total_cost
        }

        print(f"   Average CTR: {avg_ctr:.2f}%")
        print(f"   Average Conv Rate: {avg_conv_rate:.2f}%")
        print(f"   Average Cost/Conv: £{avg_cost_per_conv:.2f}")

        return self.stats

    def identify_underperformers(self) -> List[Dict]:
        """
        Identify underperforming assets based on thresholds

        Returns:
            List of dictionaries with underperformer details
        """
        print("\n🔍 Identifying underperforming assets...")

        thresholds = self.config['thresholds']
        min_impr = thresholds['min_impressions_for_judgement']
        zero_conv_threshold = thresholds['zero_conv_high_impr_threshold']

        underperformers = []

        for asset in self.pmax_text_assets:
            # Parse asset metrics
            asset_text = asset.get('Asset', '')
            asset_type = asset.get('Asset type', '')
            impr = self._parse_number(asset.get('Impr.', '0'))
            ctr = self._parse_percentage(asset.get('CTR', '0%'))
            conv_rate = self._parse_percentage(asset.get('Conv. rate', '0%'))
            cost_per_conv = self._parse_number(asset.get('Cost / conv.', '0'))
            conversions = self._parse_number(asset.get('Conversions', '0'))
            cost = self._parse_number(asset.get('Cost', '0'))

            # Skip assets with no impressions
            if impr == 0:
                continue

            # Determine if asset is underperforming
            reasons = []
            priority = 'LOW'

            # Check: Zero conversions with high impressions
            if impr >= zero_conv_threshold and conversions == 0:
                reasons.append(f'Zero conversions despite {impr:,} impressions')
                priority = 'HIGH'

            # Check: CTR below threshold
            if impr >= min_impr and ctr < (self.stats['avg_ctr'] * thresholds['ctr_multiplier']):
                reasons.append(f'Low CTR ({ctr:.2f}% vs avg {self.stats["avg_ctr"]:.2f}%)')
                if priority != 'HIGH':
                    priority = 'MEDIUM' if impr >= 100 else 'LOW'

            # Check: Conv rate below threshold
            if impr >= min_impr and conv_rate < (self.stats['avg_conv_rate'] * thresholds['conv_rate_multiplier']):
                reasons.append(f'Low conv rate ({conv_rate:.2f}% vs avg {self.stats["avg_conv_rate"]:.2f}%)')
                if priority != 'HIGH':
                    priority = 'MEDIUM' if impr >= 100 else 'LOW'

            # Check: Cost per conversion above threshold
            if conversions > 0 and cost_per_conv > (self.stats['avg_cost_per_conv'] * thresholds['cost_per_conv_multiplier']):
                reasons.append(f'High cost/conv (£{cost_per_conv:.2f} vs avg £{self.stats["avg_cost_per_conv"]:.2f})')
                if priority != 'HIGH':
                    priority = 'MEDIUM'

            # If any reasons flagged, add to underperformers
            if reasons:
                underperformers.append({
                    'Campaign ID': asset.get('Campaign ID', ''),
                    'Campaign': asset.get('Campaign', ''),
                    'Asset Group ID': asset.get('Asset Group ID', ''),
                    'Asset Group': asset.get('Asset Group', ''),
                    'Asset Group URL': asset.get('Asset Group URL', ''),
                    'Asset': asset_text,
                    'Asset Type': asset_type,
                    'Impressions': int(impr),
                    'CTR': f'{ctr:.2f}%',
                    'Conv Rate': f'{conv_rate:.2f}%',
                    'Cost/Conv': f'£{cost_per_conv:.2f}' if cost_per_conv > 0 else 'N/A',
                    'Conversions': conversions,
                    'Cost': f'£{cost:.2f}',
                    'Flag Reason': '; '.join(reasons),
                    'Priority': priority,
                    'Suggested Action': 'REPLACE'
                })

        # Sort by priority and impressions
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        underperformers.sort(key=lambda x: (priority_order[x['Priority']], -x['Impressions']))

        print(f"\n🎯 Identified {len(underperformers)} underperforming assets:")
        print(f"   - HIGH priority: {sum(1 for u in underperformers if u['Priority'] == 'HIGH')}")
        print(f"   - MEDIUM priority: {sum(1 for u in underperformers if u['Priority'] == 'MEDIUM')}")
        print(f"   - LOW priority: {sum(1 for u in underperformers if u['Priority'] == 'LOW')}")

        return underperformers

    def save_underperformers_csv(self, underperformers: List[Dict], output_path: str):
        """
        Save underperformers to CSV

        Args:
            underperformers: List of underperformer dictionaries
            output_path: Path to output CSV file
        """
        if not underperformers:
            print("\n⚠️  No underperformers to save")
            return

        fieldnames = [
            'Campaign ID', 'Campaign', 'Asset Group ID', 'Asset Group', 'Asset Group URL',
            'Asset', 'Asset Type', 'Impressions', 'CTR', 'Conv Rate',
            'Cost/Conv', 'Conversions', 'Cost', 'Flag Reason',
            'Priority', 'Suggested Action'
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(underperformers)

        print(f"\n✅ Saved underperformers to: {output_path}")

    def print_summary(self, underperformers: List[Dict]):
        """Print analysis summary"""
        print("\n" + "=" * 80)
        print("ANALYSIS SUMMARY")
        print("=" * 80)

        print(f"\nTotal assets analysed: {len(self.pmax_text_assets)}")
        print(f"Underperformers identified: {len(underperformers)}")

        if underperformers:
            print("\nTop 5 underperformers (by priority and impressions):")
            print("-" * 80)
            for i, asset in enumerate(underperformers[:5], 1):
                print(f"\n{i}. [{asset['Priority']}] {asset['Asset'][:60]}...")
                print(f"   Type: {asset['Asset Type']}")
                print(f"   Impressions: {asset['Impressions']:,} | CTR: {asset['CTR']} | Conv Rate: {asset['Conv Rate']}")
                print(f"   Reason: {asset['Flag Reason']}")

        print("\n" + "=" * 80)

    # Helper methods

    def _parse_number(self, value: str) -> float:
        """Parse number from string (handles commas and currency symbols)"""
        if not value or value in ['--', 'N/A', '']:
            return 0.0

        # Remove currency symbols, commas, spaces
        cleaned = value.replace('£', '').replace('$', '').replace(',', '').replace(' ', '').strip()

        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def _parse_percentage(self, value: str) -> float:
        """Parse percentage from string"""
        if not value or value in ['--', 'N/A', '']:
            return 0.0

        # Remove % symbol and spaces
        cleaned = value.replace('%', '').replace(' ', '').strip()

        try:
            return float(cleaned)
        except ValueError:
            return 0.0


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze PMAX asset performance')
    parser.add_argument('--csv', required=True, help='Path to asset performance CSV')
    parser.add_argument('--output', help='Output CSV file path (optional)')
    args = parser.parse_args()

    print("=" * 80)
    print("PMAX ASSET PERFORMANCE ANALYSER")
    print("=" * 80)
    print()

    # Paths
    base_dir = Path(__file__).parent
    config_path = base_dir / 'config.yaml'
    input_csv = Path(args.csv)

    # Determine output path
    if args.output:
        output_csv = Path(args.output)
    else:
        output_csv = base_dir / 'output' / 'underperforming-assets.csv'

    # Check files exist
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)

    if not input_csv.exists():
        print(f"❌ Input CSV not found: {input_csv}")
        print(f"   Please copy Asset performance report.csv to: {input_csv}")
        sys.exit(1)

    # Initialise analyser
    analyser = AssetPerformanceAnalyser(str(config_path))

    # Load and analyse
    analyser.load_asset_report(str(input_csv))
    analyser.filter_pmax_text_assets()
    analyser.calculate_campaign_averages()
    underperformers = analyser.identify_underperformers()

    # Save results
    analyser.save_underperformers_csv(underperformers, str(output_csv))

    # Print summary
    analyser.print_summary(underperformers)

    print(f"\n📁 Next steps:")
    print(f"   1. Review underperformers: {output_csv}")
    print(f"   2. Run text generation: python3 generate_replacement_text.py")
    print(f"   3. Review generated alternatives in Google Sheets")
    print(f"   4. Execute swaps: python3 execute_asset_optimisation.py")


if __name__ == "__main__":
    main()
