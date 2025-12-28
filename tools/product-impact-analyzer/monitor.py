#!/usr/bin/env python3
"""
Product Impact Analyzer - Real-Time Monitoring & Alerts

Runs daily (or hourly) to detect critical changes and send immediate alerts.

Features:
- Revenue drop alerts (e.g., >£500/day)
- Revenue spike alerts (investigate unexpected gains)
- Product disappearance detection
- Anomaly detection with immediate notification
- Smart alerting (business hours only, no spam)

Usage:
    # Daily check (via LaunchAgent)
    python3 monitor.py

    # Manual check
    python3 monitor.py --test

    # Specific client only
    python3 monitor.py --client "Tree2mydoor"
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))
from analyzer import normalize_product_id
from sheets_writer import SheetsWriter

# Add project root to path for centralized imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.petesbrain_secrets import get_secret


@dataclass
class Alert:
    """Represents a monitoring alert"""
    severity: str  # "critical", "warning", "info"
    alert_type: str  # "revenue_drop", "revenue_spike", "product_missing", "anomaly"
    client: str
    product_id: str
    product_title: str
    message: str
    metric_value: float
    threshold_value: float
    timestamp: str


class ProductMonitor:
    """Real-time monitoring for product changes"""

    def __init__(self, config_path: Path):
        """Initialize monitor with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.monitor_dir = self.base_dir / "monitoring"

        # Create monitoring directory
        self.monitor_dir.mkdir(exist_ok=True)

        # Initialize Sheets writer for historical tracking
        self.sheets_writer = SheetsWriter(config_path)

        # Load monitoring config
        self.monitor_config = self.config.get('monitoring', {
            'enabled': True,
            'check_frequency': 'daily',
            'alert_revenue_drop_threshold': 500,
            'alert_revenue_spike_threshold': 500,
            'alert_click_drop_threshold_percent': 50,
            'alert_product_missing_count': 5,
            'alert_hours_start': 9,
            'alert_hours_end': 18,
            'slack_webhook': None
        })

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

    def get_client_config(self, client_name: str) -> Dict:
        """Get configuration for a specific client"""
        for client in self.config.get('clients', []):
            if client['name'].lower() == client_name.lower():
                return client
        return {}

    def load_previous_snapshot(self, client: str) -> Optional[Dict]:
        """Load the most recent snapshot for comparison"""
        snapshot_files = sorted(self.monitor_dir.glob(f"snapshot_{client.replace(' ', '_').lower()}_*.json"))

        if not snapshot_files:
            return None

        # Get most recent
        latest = snapshot_files[-1]
        with open(latest) as f:
            return json.load(f)

    def save_current_snapshot(self, client: str, data: Dict):
        """Save current snapshot for future comparison"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = self.monitor_dir / f"snapshot_{client.replace(' ', '_').lower()}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_current_ads_data(self, client_name: str) -> Optional[List[Dict]]:
        """Load current Google Ads data"""
        ads_file = self.data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"

        if not ads_file.exists():
            return None

        with open(ads_file) as f:
            return json.load(f)

    def load_product_feed_data(self, client_name: str) -> Dict[str, Dict]:
        """Load latest product feed data (includes availability status)"""
        feed_history_dir = self.base_dir / 'data' / 'product_feed_history' / client_name

        if not feed_history_dir.exists():
            return {}

        # Get most recent snapshot
        snapshot_files = sorted(feed_history_dir.glob('*.json'))
        if not snapshot_files:
            return {}

        latest_snapshot = snapshot_files[-1]

        try:
            with open(latest_snapshot) as f:
                products = json.load(f)

            # Normalize product IDs for matching
            normalized = {}
            for product in products:
                product_id = normalize_product_id(product.get('product_id', ''))
                if product_id:
                    normalized[product_id] = product

            return normalized
        except Exception as e:
            self.log(f"  Warning: Could not load product feed data: {e}")
            return {}

    def aggregate_product_metrics(self, ads_data: List[Dict], client_name: str, days_back: int = 1) -> Dict[str, Dict]:
        """Aggregate metrics by product for recent period, enriched with product feed data (availability)"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        metrics_by_product = {}

        for row in ads_data:
            try:
                product_id = normalize_product_id(row['segments']['productItemId'])
                date = row['segments']['date']

                if not (start_date <= date <= end_date):
                    continue

                if product_id not in metrics_by_product:
                    metrics_by_product[product_id] = {
                        'product_id': product_id,
                        'product_title': row['segments'].get('productTitle', 'Unknown'),
                        'clicks': 0,
                        'impressions': 0,
                        'revenue': 0.0,
                        'cost': 0.0,
                        'availability': 'NOT_SET'  # Will be enriched from product feed
                    }

                metrics = row['metrics']
                product = metrics_by_product[product_id]

                product['clicks'] += int(metrics.get('clicks', 0))
                product['impressions'] += int(metrics.get('impressions', 0))
                product['revenue'] += float(metrics.get('conversionsValue', 0))
                product['cost'] += float(metrics.get('costMicros', 0)) / 1_000_000

            except (KeyError, ValueError) as e:
                continue

        # Enrich with product feed data (availability status)
        product_feed = self.load_product_feed_data(client_name)

        if product_feed:
            self.log(f"  Enriching with product feed data ({len(product_feed)} products with availability status)")
            enriched_count = 0

            for product_id, metrics in metrics_by_product.items():
                if product_id in product_feed:
                    feed_data = product_feed[product_id]
                    metrics['availability'] = feed_data.get('availability', 'NOT_SET')
                    enriched_count += 1

            self.log(f"  Enriched {enriched_count}/{len(metrics_by_product)} products with availability status")
        else:
            self.log(f"  Warning: No product feed data available - availability will be 'NOT_SET'")

        return metrics_by_product

    def detect_alerts(self, client: str, current: Dict[str, Dict], previous: Optional[Dict[str, Dict]]) -> List[Alert]:
        """Detect critical changes requiring alerts"""
        alerts = []

        if not previous:
            self.log(f"  No previous snapshot for {client} - establishing baseline")
            return alerts

        # Get client-specific thresholds or use global defaults
        client_config = self.get_client_config(client)
        thresholds = client_config.get('monitoring_thresholds', {})

        # Client-specific thresholds (fallback to global config if not set)
        revenue_drop_threshold = thresholds.get('revenue_drop',
                                               self.monitor_config.get('alert_revenue_drop_threshold', 500))
        revenue_spike_threshold = thresholds.get('revenue_spike',
                                                 self.monitor_config.get('alert_revenue_spike_threshold', 500))
        click_drop_threshold_pct = thresholds.get('click_drop_percent',
                                                   self.monitor_config.get('alert_click_drop_threshold_percent', 50))

        self.log(f"  Using thresholds for {client}: Rev drop £{revenue_drop_threshold}, Rev spike £{revenue_spike_threshold}, Click drop {click_drop_threshold_pct}%")

        for product_id, current_metrics in current.items():
            if product_id not in previous:
                continue  # New product, not an alert

            prev_metrics = previous[product_id]
            revenue_change = current_metrics['revenue'] - prev_metrics['revenue']

            # Critical revenue drop
            if revenue_change < -revenue_drop_threshold:
                alerts.append(Alert(
                    severity="critical",
                    alert_type="revenue_drop",
                    client=client,
                    product_id=product_id,
                    product_title=current_metrics['product_title'],
                    message=f"Revenue dropped £{abs(revenue_change):.2f} in last 24 hours",
                    metric_value=revenue_change,
                    threshold_value=-revenue_drop_threshold,
                    timestamp=datetime.now().isoformat()
                ))

            # Revenue spike (investigate opportunity)
            if revenue_change > revenue_spike_threshold:
                alerts.append(Alert(
                    severity="info",
                    alert_type="revenue_spike",
                    client=client,
                    product_id=product_id,
                    product_title=current_metrics['product_title'],
                    message=f"Revenue spiked +£{revenue_change:.2f} in last 24 hours - investigate!",
                    metric_value=revenue_change,
                    threshold_value=revenue_spike_threshold,
                    timestamp=datetime.now().isoformat()
                ))

            # Click drop
            if prev_metrics['clicks'] > 0:
                click_change_pct = ((current_metrics['clicks'] - prev_metrics['clicks']) / prev_metrics['clicks'] * 100)

                if click_change_pct < -click_drop_threshold_pct:
                    alerts.append(Alert(
                        severity="warning",
                        alert_type="click_drop",
                        client=client,
                        product_id=product_id,
                        product_title=current_metrics['product_title'],
                        message=f"Clicks dropped {abs(click_change_pct):.1f}% in last 24 hours",
                        metric_value=click_change_pct,
                        threshold_value=-click_drop_threshold_pct,
                        timestamp=datetime.now().isoformat()
                    ))

        # Check for missing products
        missing_products = set(previous.keys()) - set(current.keys())
        missing_threshold = self.monitor_config.get('alert_product_missing_count', 5)

        if len(missing_products) >= missing_threshold:
            product_list = ", ".join(list(missing_products)[:5])
            alerts.append(Alert(
                severity="warning",
                alert_type="products_missing",
                client=client,
                product_id="multiple",
                product_title=f"{len(missing_products)} products",
                message=f"{len(missing_products)} products disappeared from feed. Examples: {product_list}...",
                metric_value=len(missing_products),
                threshold_value=missing_threshold,
                timestamp=datetime.now().isoformat()
            ))

        # Check for out-of-stock products still getting clicks (wasting ad spend)
        out_of_stock_threshold = self.monitor_config.get('alert_out_of_stock_clicks', 10)
        out_of_stock_cost_threshold = self.monitor_config.get('alert_out_of_stock_cost', 10.0)
        out_of_stock_products = []

        for product_id, current_metrics in current.items():
            availability = current_metrics.get('availability', 'NOT_SET')
            clicks = current_metrics.get('clicks', 0)
            cost = current_metrics.get('cost', 0.0)

            # Alert if out of stock AND getting significant clicks
            if availability == 'out of stock' and (clicks >= out_of_stock_threshold or cost >= out_of_stock_cost_threshold):
                out_of_stock_products.append({
                    'id': product_id,
                    'title': current_metrics['product_title'],
                    'clicks': clicks,
                    'cost': cost
                })

        if out_of_stock_products:
            # Sort by cost (most wasted spend first)
            out_of_stock_products.sort(key=lambda x: x['cost'], reverse=True)
            total_wasted = sum(p['cost'] for p in out_of_stock_products)
            total_clicks = sum(p['clicks'] for p in out_of_stock_products)

            # Create summary for first few products
            top_offenders = out_of_stock_products[:3]
            product_list = ", ".join([f"{p['id']} (£{p['cost']:.2f})" for p in top_offenders])

            alerts.append(Alert(
                severity="warning",
                alert_type="out_of_stock",
                client=client,
                product_id="multiple",
                product_title=f"{len(out_of_stock_products)} out-of-stock products",
                message=f"{len(out_of_stock_products)} out-of-stock products still getting clicks - wasting £{total_wasted:.2f}. Top offenders: {product_list}",
                metric_value=total_wasted,
                threshold_value=out_of_stock_cost_threshold,
                timestamp=datetime.now().isoformat()
            ))

        return alerts

    def send_alert_email(self, alerts: List[Alert]):
        """Send email alert for critical changes"""
        if not alerts:
            return

        alert_settings = self.config.get('alert_settings', {})

        if not alert_settings.get('email_enabled'):
            self.log("  Email alerts disabled in config")
            return

        email_to = alert_settings.get('email_to')
        email_from = alert_settings.get('email_from', 'petere@roksys.co.uk')

        if not email_to or email_to == "your-email@example.com":
            self.log("  Email recipient not configured")
            return

        # Generate email content
        html = self._generate_alert_email_html(alerts)

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 Product Impact Alert - {len(alerts)} Critical Change{'s' if len(alerts) > 1 else ''}"
            msg['From'] = email_from
            msg['To'] = email_to

            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

            # Send via Gmail (password from Keychain)
            gmail_password = get_secret('GMAIL_APP_PASSWORD', fallback_env_var='GMAIL_APP_PASSWORD')

            if not gmail_password:
                self.log("  ⚠ GMAIL_APP_PASSWORD not set - cannot send email (check Keychain or environment)")
                return

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(email_from, gmail_password)
                server.send_message(msg)

            self.log(f"  ✓ Alert email sent to {email_to} ({len(alerts)} alerts)")

        except Exception as e:
            self.log(f"  ERROR sending alert email: {e}")

    def _generate_alert_email_html(self, alerts: List[Alert]) -> str:
        """Generate HTML for alert email"""
        critical_alerts = [a for a in alerts if a.severity == "critical"]
        warning_alerts = [a for a in alerts if a.severity == "warning"]
        info_alerts = [a for a in alerts if a.severity == "info"]

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
                h1 {{ color: #d32f2f; border-bottom: 3px solid #d32f2f; padding-bottom: 10px; }}
                .alert {{ padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #ddd; }}
                .alert.critical {{ background: #ffebee; border-left-color: #d32f2f; }}
                .alert.warning {{ background: #fff3e0; border-left-color: #f57c00; }}
                .alert.info {{ background: #e3f2fd; border-left-color: #1976d2; }}
                .alert-title {{ font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }}
                .alert-message {{ color: #555; }}
                .metric {{ font-family: monospace; background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
                .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚨 Product Impact Alert</h1>
                <p><strong>Alert Time:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                <p><strong>Total Alerts:</strong> {len(alerts)} ({len(critical_alerts)} critical, {len(warning_alerts)} warnings, {len(info_alerts)} info)</p>
        """

        # Critical alerts first
        if critical_alerts:
            html += "<h2>🔥 Critical Alerts</h2>"
            for alert in critical_alerts:
                html += f"""
                <div class="alert critical">
                    <div class="alert-title">🔥 {alert.client} - {alert.product_id}: {alert.product_title[:60]}</div>
                    <div class="alert-message">{alert.message}</div>
                    <div style="margin-top: 8px;">
                        <span class="metric">Change: £{alert.metric_value:.2f}</span>
                        <span class="metric">Threshold: £{alert.threshold_value:.2f}</span>
                    </div>
                </div>
                """

        # Warning alerts
        if warning_alerts:
            html += "<h2>⚠️ Warnings</h2>"
            for alert in warning_alerts:
                html += f"""
                <div class="alert warning">
                    <div class="alert-title">⚠️ {alert.client} - {alert.product_id}: {alert.product_title[:60]}</div>
                    <div class="alert-message">{alert.message}</div>
                </div>
                """

        # Info alerts (spikes/opportunities)
        if info_alerts:
            html += "<h2>💡 Opportunities</h2>"
            for alert in info_alerts:
                html += f"""
                <div class="alert info">
                    <div class="alert-title">💡 {alert.client} - {alert.product_id}: {alert.product_title[:60]}</div>
                    <div class="alert-message">{alert.message}</div>
                </div>
                """

        html += """
                <div class="footer">
                    <p>🤖 Real-Time Monitoring - Product Impact Analyzer</p>
                    <p>To adjust alert thresholds, update config.json in tools/product-impact-analyzer/</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def send_slack_alert(self, alerts: List[Alert]):
        """Send alert to Slack (optional)"""
        webhook_url = self.monitor_config.get('slack_webhook')

        if not webhook_url:
            return  # Slack not configured

        try:
            import requests

            critical = [a for a in alerts if a.severity == "critical"]
            warning = [a for a in alerts if a.severity == "warning"]

            text = f"🚨 *Product Impact Alert*\n\n"
            text += f"Total: {len(alerts)} alerts ({len(critical)} critical, {len(warning)} warnings)\n\n"

            for alert in critical[:5]:  # Top 5 critical
                text += f"🔥 *{alert.client}* - {alert.product_id}\n"
                text += f"   {alert.message}\n\n"

            payload = {"text": text}
            requests.post(webhook_url, json=payload)

            self.log(f"  ✓ Slack alert sent")

        except Exception as e:
            self.log(f"  ERROR sending Slack alert: {e}")

    def run(self, client_filter: Optional[str] = None, test: bool = False):
        """Run monitoring check"""
        self.log("="*80)
        self.log("PRODUCT IMPACT ANALYZER - REAL-TIME MONITORING")
        self.log("="*80)

        if not self.monitor_config.get('enabled', True):
            self.log("Monitoring disabled in config")
            return 0

        # Check business hours (unless testing)
        if not test and not self.is_business_hours():
            self.log("Outside business hours - skipping alerts")
            self.log("(Snapshots will still be taken for comparison)")

        all_alerts = []

        # Process each client
        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                continue

            client_name = client_config['name']

            if client_filter and client_name != client_filter:
                continue

            self.log(f"\nChecking {client_name}...")

            # Load current ads data
            current_ads_data = self.load_current_ads_data(client_name)

            if not current_ads_data:
                self.log(f"  No current ads data for {client_name}")
                continue

            # Aggregate current metrics (last 24 hours)
            current_metrics = self.aggregate_product_metrics(current_ads_data, client_name, days_back=1)
            self.log(f"  Found {len(current_metrics)} active products")

            # Load previous snapshot
            previous_metrics = self.load_previous_snapshot(client_name)

            # Detect alerts
            client_alerts = self.detect_alerts(client_name, current_metrics, previous_metrics)

            if client_alerts:
                self.log(f"  ⚠️  {len(client_alerts)} alerts detected")
                all_alerts.extend(client_alerts)
            else:
                self.log(f"  ✓ No alerts")

            # Save current snapshot for next comparison
            self.save_current_snapshot(client_name, current_metrics)

            # Write daily metrics to Google Sheets for historical tracking
            products_list = list(current_metrics.values())
            self.sheets_writer.append_daily_performance(client_name, products_list)

        # Send alerts if any found
        if all_alerts:
            self.log(f"\n{'='*80}")
            self.log(f"TOTAL ALERTS: {len(all_alerts)}")
            self.log(f"{'='*80}")

            if test or self.is_business_hours():
                self.send_alert_email(all_alerts)
                self.send_slack_alert(all_alerts)
            else:
                self.log("Alerts suppressed (outside business hours)")
        else:
            self.log("\n✓ No alerts detected - all systems normal")

        self.log("="*80)
        return 0


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='Monitor product impacts in real-time')
    parser.add_argument('--client', help='Monitor specific client only')
    parser.add_argument('--test', action='store_true', help='Test mode (ignore business hours)')

    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.json"
    monitor = ProductMonitor(config_path)

    return monitor.run(client_filter=args.client, test=args.test)


if __name__ == "__main__":
    sys.exit(main())
