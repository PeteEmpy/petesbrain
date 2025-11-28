#!/usr/bin/env python3
"""
Product Impact Analyzer - Phase 2 (Fully Automated)

Runs weekly on Tuesdays:
1. Fetches product changes from Google Sheets
2. Fetches Google Ads performance data
3. Runs impact analysis
4. Generates HTML email report
5. Sends email automatically
6. Stores results for trend tracking

Usage:
    # Automated (via LaunchAgent)
    python3 run_automated_analysis.py

    # Manual test
    python3 run_automated_analysis.py --test

    # Dry run (no email)
    python3 run_automated_analysis.py --dry-run
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from analyzer import (
    parse_product_changes,
    analyze_impact,
    ImpactAnalysis
)
from label_validation_report import generate_label_validation_section
from sheets_writer import SheetsWriter


class AutomatedAnalyzer:
    """Orchestrates automated weekly analysis"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.history_dir = self.base_dir / "history"

        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)

        # Initialize Sheets writer for historical tracking
        self.sheets_writer = SheetsWriter(config_path)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def fetch_sheets_data(self) -> bool:
        """Fetch product changes from Google Sheets via MCP"""
        self.log("Fetching product changes from Google Sheets...")

        try:
            # Use MCP to fetch Outliers Report
            spreadsheet_id = self.config['spreadsheet_id']
            sheet_name = self.config['outliers_sheet_name']

            # This would use the MCP server in production
            # For now, we'll check if data exists from manual run
            outliers_path = self.data_dir / "outliers_report.json"

            if not outliers_path.exists():
                self.log("ERROR: No outliers data found. Please run manual fetch first.")
                self.log("Command: Ask Claude Code to fetch the Outliers Report")
                return False

            self.log(f"  ✓ Outliers Report found: {outliers_path}")
            return True

        except Exception as e:
            self.log(f"ERROR fetching Sheets data: {e}")
            return False

    def fetch_ads_data(self) -> bool:
        """Fetch Google Ads performance data via MCP"""
        self.log("Fetching Google Ads performance data...")

        success_count = 0
        enabled_clients = [c for c in self.config['clients'] if c.get('enabled')]

        for client in enabled_clients:
            client_name = client['name']
            ads_file = self.data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"

            if not ads_file.exists():
                self.log(f"  ⚠ Warning: No ads data for {client_name}")
                self.log(f"    File expected: {ads_file}")
                continue

            self.log(f"  ✓ Ads data found for {client_name}")
            success_count += 1

        if success_count == 0:
            self.log("ERROR: No Google Ads data found for any client")
            return False

        self.log(f"  ✓ Loaded ads data for {success_count}/{len(enabled_clients)} clients")
        return True

    def run_analysis(self) -> Optional[List[ImpactAnalysis]]:
        """Run the impact analysis"""
        self.log("Running impact analysis...")

        try:
            # Load outliers data
            with open(self.data_dir / "outliers_report.json") as f:
                outliers_data = json.load(f)

            product_changes = parse_product_changes(outliers_data)
            self.log(f"  Found {len(product_changes)} product changes")

            # Load Google Ads data by client
            ads_data_by_client = {}

            for client_config in self.config['clients']:
                if not client_config.get('enabled'):
                    continue

                client_name = client_config['name']
                ads_path = self.data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"

                if not ads_path.exists():
                    continue

                with open(ads_path) as f:
                    ads_data_by_client[client_name] = json.load(f)

            # Run analysis
            comparison_days = self.config['analysis_settings']['comparison_window_days']
            analyses = analyze_impact(product_changes, ads_data_by_client, comparison_days)

            self.log(f"  ✓ Analyzed {len(analyses)} product changes")

            # Save JSON output
            json_output = self.output_dir / "impact_analysis.json"
            with open(json_output, 'w') as f:
                json.dump([a.to_dict() for a in analyses], f, indent=2)

            return analyses

        except Exception as e:
            self.log(f"ERROR during analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_to_history(self, analyses: List[ImpactAnalysis]):
        """Save analysis results to history for trend tracking"""
        self.log("Saving to history...")

        timestamp = datetime.now().strftime("%Y-%m-%d")
        history_file = self.history_dir / f"analysis_{timestamp}.json"

        with open(history_file, 'w') as f:
            json.dump([a.to_dict() for a in analyses], f, indent=2)

        self.log(f"  ✓ Saved to {history_file}")

    def generate_html_report(self, analyses: List[ImpactAnalysis]) -> str:
        """Generate HTML email report"""
        self.log("Generating HTML report...")

        # Group by client
        from collections import defaultdict
        by_client = defaultdict(list)
        for analysis in analyses:
            by_client[analysis.client].append(analysis)

        # Build HTML
        html = """
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
                h1 {{ color: #333; border-bottom: 3px solid #6CC24A; padding-bottom: 10px; }}
                h2 {{ color: #6CC24A; margin-top: 30px; }}
                .summary-box {{ background: #f9f9f9; padding: 15px; border-left: 4px solid #6CC24A; margin: 20px 0; }}
                .product {{ background: #fafafa; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #ddd; }}
                .product.positive {{ border-left-color: #4CAF50; }}
                .product.negative {{ border-left-color: #f44336; }}
                .metric {{ display: inline-block; margin-right: 20px; }}
                .metric-label {{ color: #888; font-size: 0.9em; }}
                .metric-value {{ font-weight: bold; font-size: 1.1em; }}
                .positive-value {{ color: #4CAF50; }}
                .negative-value {{ color: #f44336; }}
                .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Weekly Product Impact Analysis</h1>
                <p><strong>Report Date:</strong> {date}</p>

                <div class="summary-box">
                    <h3>Summary</h3>
                    <p><strong>Total Changes Analyzed:</strong> {total_changes}</p>
                    <p><strong>Clients Covered:</strong> {num_clients}</p>
                </div>
        """.format(
            date=datetime.now().strftime("%B %d, %Y"),
            total_changes=len(analyses),
            num_clients=len(by_client)
        )

        # Add client sections
        for client, client_analyses in by_client.items():
            # Filter for significant impacts
            significant = [a for a in client_analyses
                          if a.revenue_change_abs() and abs(a.revenue_change_abs()) > 10]

            if not significant:
                html += f"""
                <h2>{client}</h2>
                <p>No significant impacts detected this week.</p>
                """
                continue

            # Sort by absolute revenue impact
            significant.sort(key=lambda a: abs(a.revenue_change_abs() or 0), reverse=True)

            html += f"<h2>{client}</h2>"

            for analysis in significant[:10]:  # Top 10
                flag = analysis.impact_flag()
                rev_change = analysis.revenue_change_abs() or 0
                rev_pct = analysis.revenue_change_pct() or 0
                clicks_pct = analysis.clicks_change_pct() or 0

                product_class = "positive" if rev_change > 0 else "negative"
                value_class = "positive-value" if rev_change > 0 else "negative-value"

                html += f"""
                <div class="product {product_class}">
                    <div><strong>{flag} {analysis.product_id}: {analysis.product_title[:80]}</strong></div>
                    <div style="margin-top: 10px;">
                        <span class="metric">
                            <span class="metric-label">Change Type:</span>
                            <span class="metric-value">{analysis.change_type}</span>
                        </span>
                        <span class="metric">
                            <span class="metric-label">Date:</span>
                            <span class="metric-value">{analysis.date_changed}</span>
                        </span>
                    </div>
                    <div style="margin-top: 10px;">
                        <span class="metric">
                            <span class="metric-label">Revenue Impact:</span>
                            <span class="metric-value {value_class}">£{rev_change:+.2f} ({rev_pct:+.1f}%)</span>
                        </span>
                """

                if analysis.before and analysis.after:
                    html += f"""
                        <span class="metric">
                            <span class="metric-label">Clicks:</span>
                            <span class="metric-value">{analysis.before.clicks} → {analysis.after.clicks} ({clicks_pct:+.1f}%)</span>
                        </span>
                    """

                html += """
                    </div>
                </div>
                """

            # Add label validation section for this client
            try:
                label_section = generate_label_validation_section(client, days=7)
                html += label_section
            except Exception as e:
                self.log(f"  ⚠️  Could not generate label validation for {client}: {e}")

        html += """
                <div class="footer">
                    <p>🤖 Generated by Pete's Brain - Product Impact Analyzer</p>
                    <p>For detailed analysis, see the Impact Analysis sheet in Google Sheets.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Save HTML report
        html_file = self.output_dir / f"report_{datetime.now().strftime('%Y-%m-%d')}.html"
        with open(html_file, 'w') as f:
            f.write(html)

        self.log(f"  ✓ HTML report saved: {html_file}")
        return html

    def send_email_report(self, html_content: str, dry_run: bool = False):
        """Send email report via Gmail"""
        self.log("Preparing email report...")

        alert_settings = self.config.get('alert_settings', {})

        if not alert_settings.get('email_enabled'):
            self.log("  ⚠ Email disabled in config")
            return

        email_to = alert_settings.get('email_to')
        if not email_to or email_to == "your-email@example.com":
            self.log("  ⚠ Email recipient not configured")
            return

        if dry_run:
            self.log("  ✓ DRY RUN - Email not sent")
            self.log(f"    Would send to: {email_to}")
            return

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Product Impact Analysis - {datetime.now().strftime('%B %d, %Y')}"
            msg['From'] = alert_settings.get('email_from', 'petere@roksys.co.uk')
            msg['To'] = email_to

            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send via Gmail SMTP (requires app password)
            # Note: This requires GMAIL_APP_PASSWORD environment variable
            import os
            gmail_password = os.getenv('GMAIL_APP_PASSWORD')

            if not gmail_password:
                self.log("  ⚠ GMAIL_APP_PASSWORD not set - cannot send email")
                self.log("    Set via: export GMAIL_APP_PASSWORD='your-app-password'")
                return

            email_from = alert_settings.get('email_from', 'petere@roksys.co.uk')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(email_from, gmail_password)
                server.send_message(msg)

            self.log(f"  ✓ Email sent to {email_to}")

        except Exception as e:
            self.log(f"ERROR sending email: {e}")

    def run(self, dry_run: bool = False, test: bool = False):
        """Run full automated analysis"""
        self.log("="*80)
        self.log("PRODUCT IMPACT ANALYZER - AUTOMATED RUN")
        self.log("="*80)

        # Step 1: Fetch data
        if not self.fetch_sheets_data():
            self.log("FAILED: Could not fetch Sheets data")
            return 1

        if not self.fetch_ads_data():
            self.log("FAILED: Could not fetch Ads data")
            return 1

        # Step 2: Run analysis
        analyses = self.run_analysis()
        if not analyses:
            self.log("FAILED: Analysis returned no results")
            return 1

        # Step 3: Save to history
        self.save_to_history(analyses)

        # Step 3.5: Write analysis results to Google Sheets
        self.log("Writing analysis results to Google Sheets...")
        analyses_dicts = [a.to_dict() for a in analyses]

        # Group analyses by client
        from collections import defaultdict
        analyses_by_client = defaultdict(list)
        for analysis_dict in analyses_dicts:
            client = analysis_dict.get('client', 'Unknown')
            analyses_by_client[client].append(analysis_dict)

        # Write each client's analyses separately
        for client, client_analyses in analyses_by_client.items():
            self.sheets_writer.write_impact_analysis(client, client_analyses)

        # Step 4: Generate HTML report
        html_report = self.generate_html_report(analyses)

        # Step 5: Send email
        self.send_email_report(html_report, dry_run=dry_run)

        self.log("="*80)
        self.log("✓ AUTOMATED ANALYSIS COMPLETE")
        self.log("="*80)

        if test:
            self.log("\nTest mode - review outputs in:")
            self.log(f"  - {self.output_dir}")
            self.log(f"  - {self.history_dir}")

        return 0


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='Run automated product impact analysis')
    parser.add_argument('--dry-run', action='store_true', help='Run without sending email')
    parser.add_argument('--test', action='store_true', help='Test mode with verbose output')

    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.json"
    analyzer = AutomatedAnalyzer(config_path)

    return analyzer.run(dry_run=args.dry_run, test=args.test)


if __name__ == "__main__":
    sys.exit(main())
