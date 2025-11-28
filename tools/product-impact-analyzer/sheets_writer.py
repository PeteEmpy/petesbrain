#!/usr/bin/env python3
"""
Google Sheets Writer for Product Impact Analyzer

Writes analysis results and daily snapshots to Google Sheets for long-term
historical tracking and trend analysis.

Updated to write to per-merchant sheets for better performance and isolation.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time


class SheetsWriter:
    """Writes Product Impact Analyzer data to Google Sheets"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        # Legacy consolidated spreadsheet (for Impact Analysis, Product Summary)
        self.spreadsheet_id = self.config['spreadsheet_id']
        self.base_dir = Path(__file__).parent

        # Build client to merchant mapping and per-client spreadsheet IDs
        self.client_to_merchant = {}
        self.client_spreadsheets = {}
        for client in self.config['clients']:
            merchant_id = client.get('merchant_id')
            client_name = client['name']
            if merchant_id and merchant_id != 'UNKNOWN':
                self.client_to_merchant[client_name] = {
                    'merchant_id': merchant_id,
                    'name': client_name
                }
                # Store per-client spreadsheet ID
                spreadsheet_id = client.get('product_performance_spreadsheet_id')
                if spreadsheet_id:
                    self.client_spreadsheets[client_name] = spreadsheet_id

        # Initialize Google Sheets API
        credentials_path = os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS',
            str(Path.home() / 'Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json')
        )

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.sheets_service = build('sheets', 'v4', credentials=credentials)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def get_client_spreadsheet_id(self, client_name: str) -> Optional[str]:
        """
        Get the spreadsheet ID for a client's per-client spreadsheet

        Returns:
            Spreadsheet ID or None if client not found
        """
        spreadsheet_id = self.client_spreadsheets.get(client_name)
        if not spreadsheet_id:
            self.log(f"⚠️  No spreadsheet ID found for client '{client_name}'")
            return None
        return spreadsheet_id

    def append_daily_performance(self, client_name: str, products: List[Dict]) -> bool:
        """
        Append today's product performance to client's per-client spreadsheet

        Args:
            client_name: Name of the client
            products: List of product dicts with metrics

        Format:
            Date | Client | Product ID | Product Title | Impressions | Clicks |
            Conversions | Revenue | Cost | CTR | Conv Rate | ROAS | Label
        """
        # Get client's dedicated spreadsheet ID
        spreadsheet_id = self.get_client_spreadsheet_id(client_name)
        if not spreadsheet_id:
            return False

        self.log(f"Preparing daily performance data for {client_name}...")

        today = datetime.now().strftime("%Y-%m-%d")
        rows = []

        for product in products:
            # Calculate derived metrics
            impressions = product.get('impressions', 0)
            clicks = product.get('clicks', 0)
            conversions = product.get('conversions', 0.0)
            revenue = product.get('revenue', 0.0)
            cost = product.get('cost', 0.0)

            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
            roas = (revenue / cost) if cost > 0 else 0

            row = [
                today,
                client_name,
                str(product.get('product_id', '')),
                product.get('product_title', ''),
                str(impressions),
                str(clicks),
                f"{conversions:.2f}",
                f"{revenue:.2f}",
                f"{cost:.2f}",
                f"{ctr:.2f}",
                f"{conv_rate:.2f}",
                f"{roas:.2f}",
                product.get('label', '')
            ]
            rows.append(row)

        if not rows:
            self.log("  ⚠️  No products to write")
            return False

        try:
            # Append rows to client's own spreadsheet (Sheet1 = Daily Performance)
            body = {'values': rows}
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range="Sheet1!A2",  # Per-client spreadsheets use "Sheet1" not named sheets
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            self.log(f"  ✓ Wrote {len(rows)} rows to {client_name}'s spreadsheet")
            return True

        except Exception as e:
            self.log(f"  ❌ Error writing to {client_name}'s spreadsheet: {e}")
            return False

    def write_impact_analysis(self, client_name: str, analyses: List[Dict]) -> bool:
        """
        Write weekly impact analysis results to Impact Analysis sheet

        Args:
            client_name: Name of the client
            analyses: List of ImpactAnalysis dicts from analyzer

        Format:
            Analysis Date | Client | Product ID | Product Title | Change Type |
            Date Changed | Days Since | Before Clicks | After Clicks | Click Change % |
            Before Revenue | After Revenue | Revenue Change £ | Revenue Change % |
            Impact Flag | Label
        """
        self.log(f"Preparing impact analysis data for {client_name}...")

        analysis_date = datetime.now().strftime("%Y-%m-%d")
        rows = []

        for analysis in analyses:
            before = analysis.get('before', {})
            after = analysis.get('after', {})

            # Calculate changes
            clicks_change = None
            if before and after and before.get('clicks', 0) > 0:
                clicks_change = ((after.get('clicks', 0) - before.get('clicks', 0)) / before.get('clicks', 1) * 100)

            revenue_change_pct = None
            if before and after and before.get('revenue', 0) > 0:
                revenue_change_pct = ((after.get('revenue', 0) - before.get('revenue', 0)) / before.get('revenue', 1) * 100)

            revenue_change_abs = None
            if before and after:
                revenue_change_abs = after.get('revenue', 0) - before.get('revenue', 0)

            row = [
                analysis_date,
                client_name,
                str(analysis.get('product_id', '')),
                analysis.get('product_title', ''),
                analysis.get('change_type', ''),
                analysis.get('date_changed', ''),
                str(analysis.get('days_since_change', '')),
                str(before.get('clicks', 0)) if before else '',
                str(after.get('clicks', 0)) if after else '',
                f"{clicks_change:.1f}" if clicks_change is not None else '',
                f"{before.get('revenue', 0):.2f}" if before else '',
                f"{after.get('revenue', 0):.2f}" if after else '',
                f"{revenue_change_abs:.2f}" if revenue_change_abs is not None else '',
                f"{revenue_change_pct:.1f}" if revenue_change_pct is not None else '',
                analysis.get('impact_flag', ''),
                analysis.get('label', '')
            ]
            rows.append(row)

        if not rows:
            self.log("  ⚠️  No analyses to write")
            return False

        try:
            # Append to Impact Analysis sheet (still shared across all clients)
            body = {'values': rows}
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="'Impact Analysis'!A2",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            self.log(f"  ✓ Wrote {len(rows)} impact analysis rows")
            return True

        except Exception as e:
            self.log(f"  ❌ Error writing impact analysis: {e}")
            return False

    def write_product_summary(self, client_name: str, products: List[Dict]) -> bool:
        """
        Write current snapshot of products to Product Summary sheet

        Args:
            client_name: Name of the client
            products: List of product dicts

        Format:
            Client | Product ID | Product Title | Current Label |
            Last 7 Days Clicks | Last 7 Days Revenue | Last 30 Days Clicks |
            Last 30 Days Revenue | ROAS | Status
        """
        self.log(f"Preparing product summary for {client_name}...")

        rows = []

        for product in products:
            row = [
                client_name,
                str(product.get('product_id', '')),
                product.get('product_title', ''),
                product.get('label', ''),
                str(product.get('clicks_7d', 0)),
                f"{product.get('revenue_7d', 0):.2f}",
                str(product.get('clicks_30d', 0)),
                f"{product.get('revenue_30d', 0):.2f}",
                f"{product.get('roas', 0):.2f}",
                product.get('status', 'active')
            ]
            rows.append(row)

        if not rows:
            self.log("  ⚠️  No products to write")
            return False

        try:
            # Append to Product Summary sheet (still shared across all clients)
            body = {'values': rows}
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="'Product Summary'!A2",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            self.log(f"  ✓ Wrote {len(rows)} product summary rows")
            return True

        except Exception as e:
            self.log(f"  ❌ Error writing product summary: {e}")
            return False


def main():
    """Test the sheets writer"""
    config_path = Path(__file__).parent / "config.json"
    writer = SheetsWriter(config_path)

    print("\n" + "=" * 80)
    print("GOOGLE SHEETS WRITER - TEST MODE")
    print("=" * 80)

    # Test with sample data
    sample_products = [
        {
            'product_id': 'TEST-001',
            'product_title': 'Test Product 1',
            'impressions': 1000,
            'clicks': 50,
            'conversions': 5.0,
            'revenue': 250.00,
            'cost': 100.00,
            'label': 'hero'
        },
        {
            'product_id': 'TEST-002',
            'product_title': 'Test Product 2',
            'impressions': 500,
            'clicks': 25,
            'conversions': 2.5,
            'revenue': 125.00,
            'cost': 75.00,
            'label': 'sidekick'
        }
    ]

    # Test with Tree2mydoor
    success = writer.append_daily_performance("Tree2mydoor", sample_products)

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    if success:
        print("✓ Test data written successfully")
        print(f"  Check: https://docs.google.com/spreadsheets/d/{writer.spreadsheet_id}/edit")
    else:
        print("✗ Test failed")


if __name__ == "__main__":
    main()
