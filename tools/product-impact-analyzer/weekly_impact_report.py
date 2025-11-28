#!/usr/bin/env python3
"""
Weekly Impact Report Generator - Automated weekly product change analysis

Generates comprehensive weekly reports showing:
- All product changes this week
- Impact analysis for changes with sufficient data
- Top performing/underperforming products
- Recommendations for optimization

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json python3 weekly_impact_report.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class WeeklyImpactReport:
    """Generate weekly product impact reports"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.changes_dir = self.base_dir / 'data' / 'product_changes'
        self.reports_dir = self.base_dir / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def get_week_dates(self) -> tuple:
        """Get start and end dates for last week"""
        today = datetime.now()
        # Last Monday
        last_monday = today - timedelta(days=today.weekday() + 7)
        # Last Sunday
        last_sunday = last_monday + timedelta(days=6)

        return (
            last_monday.strftime("%Y-%m-%d"),
            last_sunday.strftime("%Y-%m-%d")
        )

    def load_week_changes(self, client_name: str, start_date: str, end_date: str) -> Dict:
        """
        Load all changes for a client in a week

        Args:
            client_name: Name of the client
            start_date: Week start date (YYYY-MM-DD)
            end_date: Week end date (YYYY-MM-DD)

        Returns:
            Aggregated changes dict
        """
        client_changes_dir = self.changes_dir / client_name

        if not client_changes_dir.exists():
            return {}

        # Aggregate all changes in week
        all_changed_products = {}
        all_new_products = []
        all_removed_products = []

        price_changes_all = []
        availability_changes_all = []
        title_changes_all = []
        description_changes_all = []
        label_changes_all = []

        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        while current_date <= end_dt:
            date_str = current_date.strftime("%Y-%m-%d")
            changes_file = client_changes_dir / f"{date_str}.json"

            if changes_file.exists():
                try:
                    with open(changes_file) as f:
                        day_changes = json.load(f)

                    # Aggregate by product
                    for product in day_changes.get('changed_products', []):
                        product_id = product['product_id']
                        if product_id not in all_changed_products:
                            all_changed_products[product_id] = {
                                'product_id': product_id,
                                'title': product.get('title', ''),
                                'changes_by_date': {}
                            }
                        all_changed_products[product_id]['changes_by_date'][date_str] = product['changes']

                    # Add price changes
                    price_changes_all.extend(day_changes.get('price_changes', []))
                    availability_changes_all.extend(day_changes.get('availability_changes', []))
                    title_changes_all.extend(day_changes.get('title_changes', []))
                    description_changes_all.extend(day_changes.get('description_changes', []))
                    label_changes_all.extend(day_changes.get('label_changes', []))

                    # Add new/removed
                    all_new_products.extend(day_changes.get('new_products', []))
                    all_removed_products.extend(day_changes.get('removed_products', []))

                except Exception as e:
                    self.log(f"  ⚠️  Error reading {changes_file}: {e}")

            current_date += timedelta(days=1)

        return {
            'changed_products': list(all_changed_products.values()),
            'new_products': all_new_products,
            'removed_products': all_removed_products,
            'price_changes': price_changes_all,
            'availability_changes': availability_changes_all,
            'title_changes': title_changes_all,
            'description_changes': description_changes_all,
            'label_changes': label_changes_all
        }

    def format_report_text(self, client_name: str, week_changes: Dict, week_start: str, week_end: str) -> str:
        """
        Format changes as text report

        Args:
            client_name: Name of the client
            week_changes: Aggregated week changes
            week_start: Week start date
            week_end: Week end date

        Returns:
            Formatted report text
        """
        lines = [
            "=" * 80,
            f"WEEKLY PRODUCT IMPACT REPORT - {client_name}",
            f"Week of {week_start} to {week_end}",
            "=" * 80,
            "",
            "## SUMMARY",
            "",
            f"Changed products: {len(week_changes.get('changed_products', []))}",
            f"  Price changes: {len(week_changes.get('price_changes', []))}",
            f"  Availability changes: {len(week_changes.get('availability_changes', []))}",
            f"  Title changes: {len(week_changes.get('title_changes', []))}",
            f"  Description changes: {len(week_changes.get('description_changes', []))}",
            f"  Label changes: {len(week_changes.get('label_changes', []))}",
            "",
            f"New products: {len(week_changes.get('new_products', []))}",
            f"Removed products: {len(week_changes.get('removed_products', []))}",
            "",
            "=" * 80,
            ""
        ]

        # Price changes detail
        if week_changes.get('price_changes'):
            lines.append("## PRICE CHANGES")
            lines.append("")
            for product in week_changes['price_changes'][:20]:  # Top 20
                product_id = product['product_id']
                title = product.get('title', '')
                old_price, new_price = product['changes']['price']
                lines.append(f"  {product_id}: {title}")
                lines.append(f"    {old_price} → {new_price}")
                lines.append("")

        # Availability changes detail
        if week_changes.get('availability_changes'):
            lines.append("=" * 80)
            lines.append("## AVAILABILITY CHANGES")
            lines.append("")
            for product in week_changes['availability_changes'][:20]:
                product_id = product['product_id']
                title = product.get('title', '')
                old_avail, new_avail = product['changes']['availability']
                lines.append(f"  {product_id}: {title}")
                lines.append(f"    {old_avail} → {new_avail}")
                lines.append("")

        # New products
        if week_changes.get('new_products'):
            lines.append("=" * 80)
            lines.append("## NEW PRODUCTS")
            lines.append("")
            for product in week_changes['new_products'][:20]:
                lines.append(f"  {product['product_id']}: {product.get('title', '')}")
                lines.append(f"    Price: {product.get('price', 'N/A')}")
                lines.append(f"    Availability: {product.get('availability', 'N/A')}")
                lines.append("")

        # Removed products
        if week_changes.get('removed_products'):
            lines.append("=" * 80)
            lines.append("## REMOVED PRODUCTS")
            lines.append("")
            for product in week_changes['removed_products'][:20]:
                lines.append(f"  {product['product_id']}: {product.get('title', '')}")
                lines.append(f"    Last price: {product.get('price', 'N/A')}")
                lines.append("")

        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def generate_reports(self) -> Dict[str, str]:
        """
        Generate reports for all clients

        Returns:
            Dict mapping client names to report file paths
        """
        self.log("="*80)
        self.log("WEEKLY IMPACT REPORT GENERATOR")
        self.log("="*80)
        self.log("")

        week_start, week_end = self.get_week_dates()
        self.log(f"Generating reports for week: {week_start} to {week_end}\n")

        reports = {}

        for client in self.config['clients']:
            if not client.get('enabled', True):
                continue

            client_name = client['name']
            self.log(f"Generating report for {client_name}...")

            # Load week changes
            week_changes = self.load_week_changes(client_name, week_start, week_end)

            if not week_changes.get('changed_products') and not week_changes.get('new_products'):
                self.log(f"  ⚠️  No changes this week")
                continue

            # Format report
            report_text = self.format_report_text(client_name, week_changes, week_start, week_end)

            # Save report
            report_filename = f"{client_name}_{week_start}_to_{week_end}.txt".replace(' ', '_')
            report_path = self.reports_dir / report_filename

            try:
                with open(report_path, 'w') as f:
                    f.write(report_text)

                self.log(f"  ✓ Saved report to {report_path}")
                reports[client_name] = str(report_path)

            except Exception as e:
                self.log(f"  ❌ Error saving report: {e}")

            self.log("")

        self.log("="*80)
        self.log("REPORT GENERATION COMPLETE")
        self.log("="*80)
        self.log(f"\nReports generated: {len(reports)}")

        return reports


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    generator = WeeklyImpactReport(config_path)
    reports = generator.generate_reports()

    if reports:
        print("\n📊 Weekly reports generated:")
        for client_name, report_path in reports.items():
            print(f"  {client_name}: {report_path}")


if __name__ == "__main__":
    main()
