#!/usr/bin/env python3
"""
Data Fetcher for Product Impact Analyzer

Fetches data from Google Sheets and Google Ads via MCP servers.
This script bridges the automated analysis with MCP integration.

Usage:
    # Fetch all data
    python3 fetch_data.py

    # Fetch specific client only
    python3 fetch_data.py --client "Tree2mydoor"

    # Test mode (verbose output)
    python3 fetch_data.py --test
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class MCPDataFetcher:
    """Fetches data via MCP servers"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def generate_ads_query(self, days_back: int = 30) -> str:
        """Generate GAQL query for Shopping performance data"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        query = f"""
        SELECT
            segments.product_item_id,
            segments.product_title,
            segments.date,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM shopping_performance_view
        WHERE segments.date >= '{start_date}'
            AND segments.date <= '{end_date}'
        ORDER BY segments.product_item_id, segments.date
        """

        return query.strip()

    def fetch_sheets_data(self) -> bool:
        """Fetch Outliers Report from Google Sheets via MCP

        Returns JSON data structure for use by analyzer.py

        This requires calling the MCP tool:
        mcp__google-sheets__read_cells(
            spreadsheet_id=...,
            range_name="Outliers Report!A1:J5000"
        )
        """
        self.log("Fetching Outliers Report from Google Sheets...")

        spreadsheet_id = self.config['spreadsheet_id']
        sheet_name = self.config['outliers_sheet_name']
        range_name = f"{sheet_name}!A1:J5000"  # Extended to include price columns

        self.log(f"  Spreadsheet ID: {spreadsheet_id}")
        self.log(f"  Range: {range_name}")

        # Note: In actual automation, this would use MCP directly
        # For now, we output instructions for Claude Code

        print("\n" + "="*80)
        print("MCP COMMAND FOR CLAUDE CODE:")
        print("="*80)
        print(f"""
Please run this MCP command:

mcp__google-sheets__read_cells(
    spreadsheet_id="{spreadsheet_id}",
    range_name="{range_name}"
)

Then save the result to:
{self.data_dir / "outliers_report.json"}

Format: Save the 'values' array from the MCP response as JSON
""")
        print("="*80)

        return True

    def fetch_ads_data_for_client(self, client_config: Dict) -> bool:
        """Fetch Google Ads data for a single client

        This requires calling the MCP tool:
        mcp__google-ads__run_gaql(
            customer_id=...,
            query=...
        )
        """
        client_name = client_config['name']
        customer_id = client_config['google_ads_customer_id']

        if customer_id == "UNKNOWN":
            self.log(f"  ⚠ Skipping {client_name} - customer ID unknown")
            return False

        self.log(f"Fetching Google Ads data for {client_name}...")
        self.log(f"  Customer ID: {customer_id}")

        query = self.generate_ads_query(days_back=30)

        # Output instructions for Claude Code
        print("\n" + "="*80)
        print(f"MCP COMMAND FOR CLAUDE CODE ({client_name}):")
        print("="*80)
        print(f"""
Please run this MCP command:

mcp__google-ads__run_gaql(
    customer_id="{customer_id}",
    query='''
{query}
    '''
)

Then save the result to:
{self.data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"}

Format: Save the 'results' array from the MCP response as JSON
(Just the results array, not the full response wrapper)
""")
        print("="*80)

        return True

    def fetch_all_ads_data(self) -> int:
        """Fetch Google Ads data for all enabled clients"""
        self.log("Fetching Google Ads data for all clients...")

        count = 0
        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                self.log(f"  ⚠ Skipping {client_config['name']} - disabled in config")
                continue

            if self.fetch_ads_data_for_client(client_config):
                count += 1

        self.log(f"\n✓ Generated MCP commands for {count} clients")
        return count

    def verify_data_exists(self) -> Dict[str, bool]:
        """Check which data files exist"""
        self.log("Verifying existing data files...")

        status = {}

        # Check Outliers Report
        outliers_path = self.data_dir / "outliers_report.json"
        status['outliers'] = outliers_path.exists()
        self.log(f"  Outliers Report: {'✓' if status['outliers'] else '✗'} {outliers_path}")

        # Check Google Ads data for each client
        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                continue

            client_name = client_config['name']
            ads_path = self.data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"
            exists = ads_path.exists()
            status[client_name] = exists
            self.log(f"  {client_name}: {'✓' if exists else '✗'} {ads_path}")

        return status

    def print_automation_instructions(self):
        """Print instructions for setting up full automation"""
        print("\n" + "="*80)
        print("AUTOMATION SETUP INSTRUCTIONS")
        print("="*80)
        print("""
To fully automate this process:

1. **MCP Integration Approach A - Python Script with MCP Client**:

   Create a wrapper script that imports the MCP client libraries:
   ```python
   from shared.mcp_client import google_sheets, google_ads

   # Fetch Sheets data
   data = google_sheets.read_cells(spreadsheet_id, range_name)
   save_to_file(data)

   # Fetch Ads data
   for client in clients:
       data = google_ads.run_gaql(customer_id, query)
       save_to_file(data)

   # Run analysis
   subprocess.run(['python3', 'run_automated_analysis.py'])
   ```

2. **MCP Integration Approach B - Claude Code CLI**:

   If Claude Code supports CLI mode with MCP:
   ```bash
   claude-code --prompt "Fetch product impact analyzer data and run analysis"
   ```

3. **LaunchAgent Setup**:

   Once data fetching is automated, set up weekly run:
   ```bash
   cd tools/product-impact-analyzer
   ./setup_weekly_automation.sh
   ```

4. **Required Environment Variables**:
   - ANTHROPIC_API_KEY (for Claude)
   - GOOGLE_APPLICATION_CREDENTIALS (for MCP servers)
   - GMAIL_APP_PASSWORD (for email sending)

For now, this script generates the MCP commands that Claude Code should run.
""")
        print("="*80)

    def run(self, client_filter: Optional[str] = None, test: bool = False):
        """Run data fetch process"""
        self.log("="*80)
        self.log("PRODUCT IMPACT ANALYZER - DATA FETCHER")
        self.log("="*80)

        if test:
            self.log("Running in TEST mode - checking existing data...")
            status = self.verify_data_exists()

            all_present = all(status.values())
            if all_present:
                self.log("\n✓ All data files present - ready to run analysis")
                return 0
            else:
                self.log("\n⚠ Some data files missing - fetch required")

        # Fetch Outliers Report
        if not client_filter:
            self.fetch_sheets_data()

        # Fetch Google Ads data
        if client_filter:
            # Fetch specific client only
            client_config = next(
                (c for c in self.config['clients'] if c['name'] == client_filter),
                None
            )
            if client_config:
                self.fetch_ads_data_for_client(client_config)
            else:
                self.log(f"ERROR: Client '{client_filter}' not found in config")
                return 1
        else:
            # Fetch all clients
            self.fetch_all_ads_data()

        # Print automation instructions
        self.print_automation_instructions()

        self.log("\n" + "="*80)
        self.log("NEXT STEPS:")
        self.log("="*80)
        self.log("1. Run the MCP commands above (via Claude Code)")
        self.log("2. Verify data files exist: python3 fetch_data.py --test")
        self.log("3. Run analysis: python3 run_automated_analysis.py --dry-run")
        self.log("="*80)

        return 0


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='Fetch data for product impact analysis')
    parser.add_argument('--client', help='Fetch specific client only')
    parser.add_argument('--test', action='store_true', help='Test mode - verify existing data')

    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.json"
    fetcher = MCPDataFetcher(config_path)

    return fetcher.run(client_filter=args.client, test=args.test)


if __name__ == "__main__":
    sys.exit(main())
