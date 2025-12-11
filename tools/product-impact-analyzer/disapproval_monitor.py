#!/usr/bin/env python3
"""
Merchant Center Disapproval Monitor

Runs daily alongside monitor.py to check for product disapprovals.
Sends immediate alerts when products are disapproved or when disapproval reasons change.

Integrates with Product Impact Analyzer monitoring system.

Usage:
    # Daily check (via LaunchAgent)
    python3 disapproval_monitor.py

    # Test mode (ignore business hours)
    python3 disapproval_monitor.py --test

    # Specific client only
    python3 disapproval_monitor.py --client "Tree2mydoor"
"""

import json
import sys
import os
import argparse
import smtplib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import Merchant Center tracker
sys.path.insert(0, str(Path(__file__).parent))
from merchant_center_tracker import MerchantCenterTracker

# Import Keychain secrets
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.secrets import get_secret


@dataclass
class DisapprovalAlert:
    """Represents a disapproval alert"""
    severity: str  # "critical", "warning", "info"
    client: str
    product_id: str
    product_title: str
    issue_code: str
    issue_description: str
    affected_countries: List[str]
    resolution: str
    is_new: bool  # True if newly disapproved since last check
    timestamp: str


class DisapprovalMonitor:
    """Monitor for product disapprovals in Merchant Center"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize monitor"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.monitor_dir = self.base_dir / "monitoring"
        self.monitor_dir.mkdir(exist_ok=True)

        self.monitor_config = self.config.get('monitoring', {})
        self.tracker = MerchantCenterTracker(config_path)

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def is_business_hours(self) -> bool:
        """Check if current time is within business hours"""
        now = datetime.now()
        start_hour = self.monitor_config.get('alert_hours_start', 9)
        end_hour = self.monitor_config.get('alert_hours_end', 18)

        # Check if weekend
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False

        # Check if within business hours
        return start_hour <= now.hour < end_hour

    def load_previous_snapshot(self) -> Optional[Dict]:
        """Load previous disapproval snapshot"""
        snapshot_file = self.monitor_dir / "disapprovals_previous.json"

        if not snapshot_file.exists():
            return None

        try:
            with open(snapshot_file) as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Error loading previous snapshot: {e}")
            return None

    def save_current_snapshot(self, results: Dict[str, List[Dict]]):
        """Save current disapproval snapshot"""
        snapshot_file = self.monitor_dir / "disapprovals_current.json"

        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'clients': results
        }

        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

        # Copy current to previous
        previous_file = self.monitor_dir / "disapprovals_previous.json"
        with open(previous_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

    def detect_new_disapprovals(self, current: Dict[str, List[Dict]],
                               previous: Optional[Dict]) -> List[DisapprovalAlert]:
        """
        Detect newly disapproved products

        Args:
            current: Current product statuses
            previous: Previous snapshot (or None if first run)

        Returns:
            List of DisapprovalAlert objects for newly disapproved products
        """
        alerts = []

        for client_name, statuses in current.items():
            # Get previous statuses for this client
            prev_statuses = {}
            if previous:
                prev_statuses = {
                    s['product_id']: s
                    for s in previous.get('clients', {}).get(client_name, [])
                }

            # Check each current product
            for status in statuses:
                if status['status'] != 'disapproved':
                    continue

                product_id = status['product_id']
                simple_id = product_id.split(':')[-1]  # Extract just the numeric ID

                # Check if this is newly disapproved
                is_new = False
                if product_id not in prev_statuses:
                    is_new = True  # Product wasn't in previous snapshot
                elif prev_statuses[product_id]['status'] != 'disapproved':
                    is_new = True  # Product status changed to disapproved

                # Create alert for each issue
                for issue in status['item_level_issues']:
                    severity = self._determine_severity(issue)

                    alert = DisapprovalAlert(
                        severity=severity,
                        client=client_name,
                        product_id=simple_id,
                        product_title=status['title'],
                        issue_code=issue['code'],
                        issue_description=issue['description'],
                        affected_countries=issue.get('affected_countries', []),
                        resolution=issue.get('resolution', 'See Merchant Center'),
                        is_new=is_new,
                        timestamp=datetime.now().isoformat()
                    )

                    alerts.append(alert)

        return alerts

    def _determine_severity(self, issue: Dict) -> str:
        """
        Determine alert severity based on issue

        Critical issues require immediate action (policy violations)
        Warning issues may be temporary or less impactful
        """
        servability = issue.get('servability', '').lower()
        code = issue.get('code', '').lower()

        # Critical: Product cannot be shown
        if servability == 'disapproved':
            return 'critical'

        # Critical: Policy violations
        if 'policy' in code or 'prohibited' in code or 'counterfeit' in code:
            return 'critical'

        # Warning: Data quality issues (usually fixable)
        if 'missing' in code or 'invalid' in code or 'incomplete' in code:
            return 'warning'

        # Default to warning
        return 'warning'

    def send_email_alert(self, alerts: List[DisapprovalAlert]):
        """Send email alert for disapprovals"""
        gmail_password = get_secret('GMAIL_APP_PASSWORD', fallback_env_var='GMAIL_APP_PASSWORD')
        if not gmail_password:
            self.log("⚠️  GMAIL_APP_PASSWORD not set - cannot send email (check Keychain or environment)")
            return

        # Group alerts by severity
        critical = [a for a in alerts if a.severity == 'critical']
        warnings = [a for a in alerts if a.severity == 'warning']
        new_alerts = [a for a in alerts if a.is_new]

        # Create email
        subject = f"🚨 Merchant Center Disapprovals - {len(new_alerts)} New Issues"

        body_lines = [
            "=" * 80,
            "MERCHANT CENTER DISAPPROVAL ALERT",
            f"Alert Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total: {len(alerts)} disapprovals ({len(new_alerts)} new)",
            "=" * 80,
            ""
        ]

        if critical:
            body_lines.append("\n🔥 CRITICAL ISSUES (Immediate Action Required)")
            body_lines.append("─" * 80)
            for alert in critical:
                if alert.is_new:
                    body_lines.append(f"🆕 {alert.client} - Product {alert.product_id}")
                else:
                    body_lines.append(f"   {alert.client} - Product {alert.product_id}")

                body_lines.append(f"   Title: {alert.product_title}")
                body_lines.append(f"   Issue: {alert.issue_code}")
                body_lines.append(f"   {alert.issue_description}")

                if alert.affected_countries:
                    countries = ', '.join(alert.affected_countries)
                    body_lines.append(f"   Affected Countries: {countries}")

                if alert.resolution:
                    body_lines.append(f"   Resolution: {alert.resolution}")

                body_lines.append("")

        if warnings:
            body_lines.append("\n⚠️  WARNINGS (Data Quality Issues)")
            body_lines.append("─" * 80)
            for alert in warnings:
                if alert.is_new:
                    body_lines.append(f"🆕 {alert.client} - Product {alert.product_id}")
                else:
                    body_lines.append(f"   {alert.client} - Product {alert.product_id}")

                body_lines.append(f"   Title: {alert.product_title}")
                body_lines.append(f"   Issue: {alert.issue_code}")
                body_lines.append(f"   {alert.issue_description}")

                if alert.resolution:
                    body_lines.append(f"   Resolution: {alert.resolution}")

                body_lines.append("")

        body_lines.append("\n" + "=" * 80)
        body_lines.append("Fix these issues in Google Merchant Center:")
        body_lines.append("https://merchants.google.com/")
        body_lines.append("=" * 80)

        body = '\n'.join(body_lines)

        # Send email
        try:
            msg = MIMEMultipart()
            msg['From'] = 'petere@roksys.co.uk'
            msg['To'] = 'petere@roksys.co.uk'
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login('petere@roksys.co.uk', gmail_password)
                server.send_message(msg)

            self.log(f"✓ Email alert sent to petere@roksys.co.uk")

        except Exception as e:
            self.log(f"❌ Failed to send email: {e}")

    def run_check(self, client_filter: Optional[str] = None, test_mode: bool = False):
        """
        Run disapproval check

        Args:
            client_filter: Only check specific client (or None for all)
            test_mode: If True, ignore business hours and always alert
        """
        self.log("=" * 80)
        self.log("MERCHANT CENTER DISAPPROVAL MONITORING")
        self.log("=" * 80)
        self.log("")

        # Check business hours (unless test mode)
        if not test_mode and not self.is_business_hours():
            self.log("Outside business hours - exiting without alerts")
            return

        # Get current product statuses
        if client_filter:
            # Check specific client
            client_config = next(
                (c for c in self.config['clients'] if c['name'].lower() == client_filter.lower()),
                None
            )

            if not client_config:
                self.log(f"❌ Client '{client_filter}' not found")
                return

            merchant_id = client_config.get('merchant_id')
            if not merchant_id or merchant_id == "UNKNOWN":
                self.log(f"❌ No merchant ID for {client_filter}")
                return

            self.log(f"Checking {client_filter}...")
            statuses = self.tracker.get_all_product_statuses(merchant_id)
            current_results = {client_filter: statuses}
        else:
            # Check all clients
            current_results = self.tracker.check_all_clients()

        # Load previous snapshot
        previous_snapshot = self.load_previous_snapshot()

        # Detect new disapprovals
        alerts = self.detect_new_disapprovals(current_results, previous_snapshot)

        # Save current snapshot
        self.save_current_snapshot(current_results)

        # Report results
        if not alerts:
            self.log("\n✓ No disapprovals detected - all products approved")
        else:
            new_count = len([a for a in alerts if a.is_new])
            total_count = len(alerts)

            self.log(f"\n⚠️  {total_count} disapprovals found ({new_count} new)")

            # Send email if there are new disapprovals
            if new_count > 0:
                self.log(f"Sending email alert for {new_count} new disapprovals...")
                self.send_email_alert(alerts)
            else:
                self.log("No new disapprovals - email not sent")

        self.log("=" * 80)


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Monitor Merchant Center disapprovals')
    parser.add_argument('--client', help='Check specific client only')
    parser.add_argument('--test', action='store_true', help='Test mode (ignore business hours)')

    args = parser.parse_args()

    monitor = DisapprovalMonitor()
    monitor.run_check(client_filter=args.client, test_mode=args.test)


if __name__ == '__main__':
    main()
