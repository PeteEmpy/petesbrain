#!/usr/bin/env python3
"""
Product Anomaly Detector - Detect per-product performance anomalies

Compares today's product performance to baselines and alerts on significant deviations.
Uses product labels (hero/sidekick/villain/zombie) to adjust sensitivity.

Alert thresholds (configurable per client):
- Heroes: 30% deviation (most sensitive)
- Sidekicks: 40% deviation
- Villains: 60% deviation
- Zombies: 70% deviation (least sensitive)

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json python3 product_anomaly_detector.py
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ProductAnomalyDetector:
    """Detect per-product performance anomalies"""

    def __init__(self, config_path: Path):
        """Initialize with configuration"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.baselines_dir = self.base_dir / 'data' / 'product_baselines'
        self.changes_dir = self.base_dir / 'data' / 'product_changes'

        # Default thresholds by label
        self.default_thresholds = {
            'hero': 0.30,      # 30% deviation
            'sidekick': 0.40,  # 40% deviation
            'villain': 0.60,   # 60% deviation
            'zombie': 0.70,    # 70% deviation
            'unknown': 0.50    # 50% deviation for unlabeled products
        }

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def load_baselines(self, client_name: str) -> Optional[Dict]:
        """
        Load baselines for a client

        Args:
            client_name: Name of the client

        Returns:
            Baselines dict or None if not found
        """
        baseline_path = self.baselines_dir / f"{client_name}.json"

        if not baseline_path.exists():
            self.log(f"  ⚠️  No baselines found for {client_name}")
            return None

        try:
            with open(baseline_path) as f:
                return json.load(f)
        except Exception as e:
            self.log(f"  ❌ Error loading baselines for {client_name}: {e}")
            return None

    def load_product_changes(self, client_name: str) -> Optional[Dict]:
        """
        Load today's product changes for a client

        Args:
            client_name: Name of the client

        Returns:
            Changes dict or None if not found
        """
        today = datetime.now().strftime("%Y-%m-%d")
        changes_path = self.changes_dir / client_name / f"{today}.json"

        if not changes_path.exists():
            return None

        try:
            with open(changes_path) as f:
                return json.load(f)
        except Exception as e:
            self.log(f"  ⚠️  Error loading changes for {client_name}: {e}")
            return None

    def get_threshold_for_product(self, label: str, client_config: Dict) -> float:
        """
        Get alert threshold for a product based on its label

        Args:
            label: Product label (hero/sidekick/villain/zombie)
            client_config: Client configuration dict

        Returns:
            Threshold percentage (e.g., 0.30 for 30%)
        """
        # Normalize label
        label_lower = label.lower().strip()

        # Check client-specific thresholds
        if 'product_monitoring' in client_config:
            monitoring_config = client_config['product_monitoring']
            threshold_key = f"{label_lower}_threshold_pct"
            if threshold_key in monitoring_config:
                return monitoring_config[threshold_key]

        # Fall back to defaults
        for key in self.default_thresholds:
            if key in label_lower:
                return self.default_thresholds[key]

        return self.default_thresholds['unknown']

    def detect_anomalies(
        self,
        client_name: str,
        today_performance: List[Dict],
        baselines: Dict
    ) -> List[Dict]:
        """
        Detect anomalies by comparing today's performance to baselines

        Args:
            client_name: Name of the client
            today_performance: List of today's product performance dicts
            baselines: Dict of baselines per product

        Returns:
            List of anomaly dicts
        """
        self.log(f"Detecting anomalies for {client_name}...")

        # Get client config
        client_config = next((c for c in self.config['clients'] if c['name'] == client_name), {})

        anomalies = []
        baseline_products = baselines.get('baselines', {})

        for product in today_performance:
            product_id = product['product_id']

            # Check if we have a baseline
            if product_id not in baseline_products:
                continue

            baseline = baseline_products[product_id]

            # Get threshold based on product label
            label = baseline.get('label', 'unknown')
            threshold = self.get_threshold_for_product(label, client_config)

            # Check revenue deviation
            baseline_revenue = baseline['revenue']['mean']
            today_revenue = product.get('revenue', 0)

            if baseline_revenue > 0:
                deviation = (today_revenue - baseline_revenue) / baseline_revenue
                abs_deviation = abs(deviation)

                if abs_deviation >= threshold:
                    # Anomaly detected
                    direction = 'increase' if deviation > 0 else 'decrease'
                    severity = 'critical' if abs_deviation >= threshold * 1.5 else 'warning'

                    anomaly = {
                        'product_id': product_id,
                        'product_title': product.get('product_title', baseline.get('product_title', '')),
                        'label': label,
                        'threshold': threshold,
                        'metric': 'revenue',
                        'baseline_value': baseline_revenue,
                        'today_value': today_revenue,
                        'deviation_pct': deviation * 100,
                        'direction': direction,
                        'severity': severity
                    }

                    anomalies.append(anomaly)

            # Check clicks deviation
            baseline_clicks = baseline['clicks']['mean']
            today_clicks = product.get('clicks', 0)

            if baseline_clicks > 0:
                deviation = (today_clicks - baseline_clicks) / baseline_clicks
                abs_deviation = abs(deviation)

                if abs_deviation >= threshold:
                    direction = 'increase' if deviation > 0 else 'decrease'
                    severity = 'warning'  # Clicks less critical than revenue

                    anomaly = {
                        'product_id': product_id,
                        'product_title': product.get('product_title', baseline.get('product_title', '')),
                        'label': label,
                        'threshold': threshold,
                        'metric': 'clicks',
                        'baseline_value': baseline_clicks,
                        'today_value': today_clicks,
                        'deviation_pct': deviation * 100,
                        'direction': direction,
                        'severity': severity
                    }

                    anomalies.append(anomaly)

        self.log(f"  ✓ Detected {len(anomalies)} anomalies")
        return anomalies

    def format_alert_email(
        self,
        client_name: str,
        anomalies: List[Dict],
        changes: Optional[Dict]
    ) -> Tuple[str, str]:
        """
        Format alert email

        Args:
            client_name: Name of the client
            anomalies: List of anomaly dicts
            changes: Product changes dict (if available)

        Returns:
            Tuple of (subject, body)
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Count by severity
        critical_count = len([a for a in anomalies if a['severity'] == 'critical'])
        warning_count = len([a for a in anomalies if a['severity'] == 'warning'])

        # Subject
        if critical_count > 0:
            subject = f"🚨 {client_name}: {critical_count} Critical Product Anomalies Detected"
        else:
            subject = f"⚠️ {client_name}: {warning_count} Product Anomalies Detected"

        # Body
        body_lines = [
            f"Product Anomaly Alert - {client_name}",
            f"Date: {today}",
            "",
            f"Detected {len(anomalies)} product anomalies:",
            f"  Critical: {critical_count}",
            f"  Warning: {warning_count}",
            "",
            "=" * 80,
            ""
        ]

        # Group anomalies by product
        products_with_anomalies = {}
        for anomaly in anomalies:
            product_id = anomaly['product_id']
            if product_id not in products_with_anomalies:
                products_with_anomalies[product_id] = []
            products_with_anomalies[product_id].append(anomaly)

        # Format each product
        for product_id, product_anomalies in products_with_anomalies.items():
            first_anomaly = product_anomalies[0]

            body_lines.append(f"Product: {first_anomaly['product_title']}")
            body_lines.append(f"  ID: {product_id}")
            body_lines.append(f"  Label: {first_anomaly['label']}")
            body_lines.append("")

            # Check if product has changes today
            if changes:
                changed_products = {p['product_id']: p for p in changes.get('changed_products', [])}
                if product_id in changed_products:
                    product_changes = changed_products[product_id]['changes']
                    body_lines.append("  ⚠️ Product changed today:")
                    for field, (old_val, new_val) in product_changes.items():
                        body_lines.append(f"    {field}: {old_val} → {new_val}")
                    body_lines.append("")

            # Format each anomaly
            for anomaly in product_anomalies:
                icon = "🚨" if anomaly['severity'] == 'critical' else "⚠️"
                metric = anomaly['metric'].capitalize()
                direction = "↑" if anomaly['direction'] == 'increase' else "↓"

                body_lines.append(f"  {icon} {metric} {direction} {abs(anomaly['deviation_pct']):.1f}%")
                body_lines.append(f"    Baseline: {anomaly['baseline_value']:.2f}")
                body_lines.append(f"    Today: {anomaly['today_value']:.2f}")
                body_lines.append(f"    Threshold: {anomaly['threshold']*100:.0f}%")
                body_lines.append("")

            body_lines.append("=" * 80)
            body_lines.append("")

        # Add context if changes detected
        if changes:
            summary = changes.get('summary', {})
            if summary.get('changed_products', 0) > 0:
                body_lines.append("Product Changes Today:")
                body_lines.append(f"  Price changes: {summary.get('price_changes', 0)}")
                body_lines.append(f"  Availability changes: {summary.get('availability_changes', 0)}")
                body_lines.append(f"  Title changes: {summary.get('title_changes', 0)}")
                body_lines.append(f"  New products: {summary.get('new_products', 0)}")
                body_lines.append(f"  Removed products: {summary.get('removed_products', 0)}")
                body_lines.append("")

        body = "\n".join(body_lines)
        return subject, body

    def send_alert_email(self, subject: str, body: str, recipient: str) -> bool:
        """
        Send alert email

        Args:
            subject: Email subject
            body: Email body
            recipient: Recipient email address

        Returns:
            True if successful
        """
        # Get email config
        email_config = self.config.get('email', {})
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config.get('sender_email', '')
        sender_password = email_config.get('sender_password', '')

        if not sender_email or not sender_password:
            self.log("  ⚠️  Email not configured, skipping alert")
            return False

        # Check business hours (9 AM - 6 PM weekdays)
        now = datetime.now()
        if now.weekday() >= 5:  # Weekend
            self.log("  ⚠️  Weekend - skipping email alert")
            return False

        if now.hour < 9 or now.hour >= 18:  # Outside business hours
            self.log("  ⚠️  Outside business hours - skipping email alert")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            self.log(f"  ✓ Alert email sent to {recipient}")
            return True

        except Exception as e:
            self.log(f"  ❌ Error sending email: {e}")
            return False


def main():
    """Main entry point - to be called by monitor.py"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    detector = ProductAnomalyDetector(config_path)

    # This would be called by monitor.py with today's performance data
    print("Product anomaly detector initialized")
    print("Call detect_anomalies() with today's performance data")


if __name__ == "__main__":
    main()
