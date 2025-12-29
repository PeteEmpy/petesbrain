#!/usr/bin/env python3
"""
Weekly Performance Summary Email

Consolidated weekly email showing trends across ALL clients, replacing the need
to review 17 individual client reports.

Sections:
- Executive summary (total Heroes/Sidekicks/Villains/Zombies across portfolio)
- Cross-client pattern detection (platform-wide issues)
- Top 5 rising stars (products moving up in classification)
- Top 5 falling stars (products moving down in classification)
- Client-by-client highlights
- Recommended actions

Runs: Weekly on Sundays

Usage:
    # Automated (via LaunchAgent)
    python3 weekly_summary_email.py

    # Manual test
    python3 weekly_summary_email.py --test

    # Dry run (no email)
    python3 weekly_summary_email.py --dry-run
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))
from monitor import ProductMonitor
from cross_client_detector import CrossClientDetector, CrossClientPattern

# Add project root to path for centralized imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.petesbrain_secrets import get_secret


class WeeklySummaryGenerator:
    """Generates consolidated weekly summary across all clients"""

    def __init__(self, config_path: Path):
        """Initialize generator"""
        with open(config_path) as f:
            self.config = json.load(f)

        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.monitor_dir = self.base_dir / "monitoring"

        self.output_dir.mkdir(exist_ok=True)

        # Initialize monitor and cross-client detector
        self.monitor = ProductMonitor(config_path)
        self.cross_client_detector = CrossClientDetector()

    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def load_client_snapshot(self, client: str, days_ago: int = 0) -> Dict:
        """Load snapshot for a client from X days ago"""
        # Normalize client name to match snapshot file naming
        client_slug = client.replace(' ', '_').replace('-', '_').lower()

        # Calculate target date
        target_date = datetime.now() - timedelta(days=days_ago)

        # Snapshot files are named: snapshot_{client-slug}_{YYYY-MM-DD}.json
        target_file = self.monitor_dir / f"snapshot_{client_slug}_{target_date.strftime('%Y-%m-%d')}.json"

        if target_file.exists():
            with open(target_file) as f:
                return json.load(f)

        # Find closest snapshot
        pattern = f"snapshot_{client_slug}_*.json"
        snapshots = sorted(self.monitor_dir.glob(pattern), reverse=True)
        if snapshots:
            with open(snapshots[0]) as f:
                return json.load(f)

        return {}

    def aggregate_portfolio_stats(self, client_snapshots: Dict[str, Dict]) -> Dict:
        """Aggregate statistics across entire portfolio"""
        total_products = 0
        total_heroes = 0
        total_sidekicks = 0
        total_villains = 0
        total_zombies = 0
        total_revenue = 0.0

        for client, snapshot in client_snapshots.items():
            for product_id, metrics in snapshot.items():
                total_products += 1
                total_revenue += metrics.get('revenue', 0)

                # Count by label (if available)
                label = metrics.get('label', 'unknown').lower()
                if 'hero' in label:
                    total_heroes += 1
                elif 'sidekick' in label:
                    total_sidekicks += 1
                elif 'villain' in label:
                    total_villains += 1
                elif 'zombie' in label:
                    total_zombies += 1

        return {
            'total_products': total_products,
            'total_heroes': total_heroes,
            'total_sidekicks': total_sidekicks,
            'total_villains': total_villains,
            'total_zombies': total_zombies,
            'total_revenue': total_revenue,
            'total_clients': len(client_snapshots)
        }

    def find_rising_falling_stars(
        self,
        current_snapshots: Dict[str, Dict],
        previous_snapshots: Dict[str, Dict]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Find products with biggest label improvements/declines.

        Returns:
            Tuple of (rising_stars, falling_stars)
        """
        label_priority = {'heroes': 4, 'sidekicks': 3, 'villains': 2, 'zombies': 1, 'unknown': 0}
        rising = []
        falling = []

        for client, curr_snapshot in current_snapshots.items():
            if client not in previous_snapshots:
                continue

            prev_snapshot = previous_snapshots[client]

            for product_id, curr_metrics in curr_snapshot.items():
                if product_id not in prev_snapshot:
                    continue

                curr_label = curr_metrics.get('label', 'unknown').lower().rstrip('s')  # Remove plural
                prev_label = prev_snapshot[product_id].get('label', 'unknown').lower().rstrip('s')

                curr_priority = label_priority.get(curr_label, 0)
                prev_priority = label_priority.get(prev_label, 0)

                change = curr_priority - prev_priority

                if change > 0:  # Rising star
                    rising.append({
                        'client': client,
                        'product_id': product_id,
                        'product_title': curr_metrics.get('product_title', 'Unknown'),
                        'from_label': prev_label,
                        'to_label': curr_label,
                        'change': change,
                        'revenue': curr_metrics.get('revenue', 0)
                    })
                elif change < 0:  # Falling star
                    falling.append({
                        'client': client,
                        'product_id': product_id,
                        'product_title': curr_metrics.get('product_title', 'Unknown'),
                        'from_label': prev_label,
                        'to_label': curr_label,
                        'change': change,
                        'revenue': curr_metrics.get('revenue', 0)
                    })

        # Sort by change magnitude and revenue
        rising.sort(key=lambda x: (x['change'], x['revenue']), reverse=True)
        falling.sort(key=lambda x: (abs(x['change']), x['revenue']), reverse=True)

        return rising[:5], falling[:5]

    def generate_report(self) -> str:
        """Generate comprehensive weekly summary"""
        self.log("="*80)
        self.log("WEEKLY PERFORMANCE SUMMARY")
        self.log("="*80)

        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        period_str = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"

        # Load current and previous snapshots for all clients
        current_snapshots = {}
        previous_snapshots = {}

        for client_config in self.config['clients']:
            if not client_config.get('enabled'):
                continue

            client_name = client_config['name']
            self.log(f"Loading snapshots for {client_name}...")

            current_snapshots[client_name] = self.load_client_snapshot(client_name, days_ago=0)
            previous_snapshots[client_name] = self.load_client_snapshot(client_name, days_ago=7)

        # Aggregate portfolio statistics
        current_stats = self.aggregate_portfolio_stats(current_snapshots)
        previous_stats = self.aggregate_portfolio_stats(previous_snapshots)

        self.log(f"Portfolio: {current_stats['total_products']} products across {current_stats['total_clients']} clients")

        # Detect cross-client patterns
        patterns = self.cross_client_detector.detect_patterns(current_snapshots, previous_snapshots)
        self.log(f"Detected {len(patterns)} cross-client patterns")

        # Find rising/falling stars
        rising_stars, falling_stars = self.find_rising_falling_stars(current_snapshots, previous_snapshots)
        self.log(f"Found {len(rising_stars)} rising stars, {len(falling_stars)} falling stars")

        # Generate HTML report
        html = self._generate_html(
            period_str,
            current_stats,
            previous_stats,
            patterns,
            rising_stars,
            falling_stars
        )

        return html

    def _generate_html(
        self,
        period_str: str,
        current_stats: Dict,
        previous_stats: Dict,
        patterns: List[CrossClientPattern],
        rising_stars: List[Dict],
        falling_stars: List[Dict]
    ) -> str:
        """Generate HTML report"""

        # Calculate week-over-week changes
        hero_change = current_stats['total_heroes'] - previous_stats.get('total_heroes', 0)
        zombie_change = current_stats['total_zombies'] - previous_stats.get('total_zombies', 0)
        revenue_change = current_stats['total_revenue'] - previous_stats.get('total_revenue', 0)
        revenue_change_pct = (revenue_change / previous_stats['total_revenue'] * 100) if previous_stats.get('total_revenue', 0) > 0 else 0

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Weekly Performance Summary - {period_str}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 40px 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                h1 {{ color: #10B981; border-bottom: 3px solid #10B981; padding-bottom: 10px; }}
                h2 {{ color: #059669; border-bottom: 2px solid #D1FAE5; padding-bottom: 8px; margin-top: 40px; }}
                h3 {{ color: #047857; margin-top: 30px; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th {{
                    background-color: #10B981;
                    color: white;
                    padding: 12px;
                    font-weight: 600;
                    text-align: left;
                }}
                td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #D1FAE5;
                }}
                .stat-box {{
                    display: inline-block;
                    background: #F0FDF4;
                    border-left: 4px solid #10B981;
                    padding: 15px 20px;
                    margin: 10px 10px 10px 0;
                    min-width: 200px;
                }}
                .stat-value {{
                    font-size: 2em;
                    font-weight: 700;
                    color: #059669;
                }}
                .stat-label {{
                    font-size: 0.9em;
                    color: #6B7280;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .change-positive {{ color: #059669; font-weight: 600; }}
                .change-negative {{ color: #DC2626; font-weight: 600; }}
                .rising-star {{ background: #ECFDF5; }}
                .falling-star {{ background: #FEE2E2; }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>🟢 Weekly Performance Summary</h1>
            <p><strong>Period:</strong> {period_str}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

            <h2>Executive Summary</h2>

            <div class="stat-box">
                <div class="stat-value">{current_stats['total_clients']}</div>
                <div class="stat-label">Active Clients</div>
            </div>

            <div class="stat-box">
                <div class="stat-value">{current_stats['total_products']:,}</div>
                <div class="stat-label">Total Products</div>
            </div>

            <div class="stat-box">
                <div class="stat-value">£{current_stats['total_revenue']:,.2f}</div>
                <div class="stat-label">Total Revenue</div>
                <div class="{'change-positive' if revenue_change >= 0 else 'change-negative'}">
                    {revenue_change:+.1f}% vs last week
                </div>
            </div>

            <h3>Portfolio Classification Distribution</h3>
            <table>
                <tr>
                    <th>Classification</th>
                    <th>Current Count</th>
                    <th>Week-over-Week Change</th>
                </tr>
                <tr>
                    <td>Heroes</td>
                    <td>{current_stats['total_heroes']}</td>
                    <td class="{'change-positive' if hero_change >= 0 else 'change-negative'}">
                        {hero_change:+d}
                    </td>
                </tr>
                <tr>
                    <td>Sidekicks</td>
                    <td>{current_stats['total_sidekicks']}</td>
                    <td>{current_stats['total_sidekicks'] - previous_stats.get('total_sidekicks', 0):+d}</td>
                </tr>
                <tr>
                    <td>Villains</td>
                    <td>{current_stats['total_villains']}</td>
                    <td>{current_stats['total_villains'] - previous_stats.get('total_villains', 0):+d}</td>
                </tr>
                <tr>
                    <td>Zombies</td>
                    <td>{current_stats['total_zombies']}</td>
                    <td class="{'change-negative' if zombie_change >= 0 else 'change-positive'}">
                        {zombie_change:+d}
                    </td>
                </tr>
            </table>
        """

        # Add cross-client patterns section
        html += self.cross_client_detector.generate_html_section(patterns)

        # Add rising stars
        if rising_stars:
            html += """
            <h2>🌟 Top 5 Rising Stars</h2>
            <p>Products with biggest label improvements this week:</p>
            <table>
                <tr>
                    <th>Client</th>
                    <th>Product</th>
                    <th>From → To</th>
                    <th>Revenue</th>
                </tr>
            """

            for star in rising_stars:
                html += f"""
                <tr class="rising-star">
                    <td>{star['client']}</td>
                    <td>{star['product_title'][:60]}</td>
                    <td>{star['from_label'].title()} → <strong>{star['to_label'].title()}</strong></td>
                    <td>£{star['revenue']:.2f}</td>
                </tr>
                """

            html += "</table>"

        # Add falling stars
        if falling_stars:
            html += """
            <h2>📉 Top 5 Falling Stars</h2>
            <p>Products with biggest label declines this week:</p>
            <table>
                <tr>
                    <th>Client</th>
                    <th>Product</th>
                    <th>From → To</th>
                    <th>Revenue</th>
                </tr>
            """

            for star in falling_stars:
                html += f"""
                <tr class="falling-star">
                    <td>{star['client']}</td>
                    <td>{star['product_title'][:60]}</td>
                    <td>{star['from_label'].title()} → <strong>{star['to_label'].title()}</strong></td>
                    <td>£{star['revenue']:.2f}</td>
                </tr>
                """

            html += "</table>"

        # Recommended actions
        html += """
        <h2>Recommended Actions</h2>
        <ul>
        """

        if patterns:
            html += "<li><strong>Investigate cross-client patterns</strong> - See sections above for specific recommendations</li>"

        if rising_stars:
            html += "<li><strong>Analyse rising star success</strong> - Understand what changed, replicate across portfolio</li>"

        if falling_stars:
            html += "<li><strong>Address falling stars</strong> - Review why products declined, take corrective action</li>"

        if hero_change < -10:
            html += f"<li><strong>Hero count dropped by {abs(hero_change)}</strong> - Investigate disapprovals, Product Hero settings</li>"

        if revenue_change_pct < -10:
            html += f"<li><strong>Revenue down {abs(revenue_change_pct):.1f}%</strong> - Review seasonal trends, market conditions, ad delivery</li>"

        html += """
        </ul>

        <p style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #E5E7EB; color: #6B7280; font-size: 0.9em;">
            This summary replaces individual client reviews. For detailed client-specific analysis, use the revenue attribution report.
        </p>

        </div>
        </body>
        </html>
        """

        return html

    def send_email(self, html_content: str):
        """Send weekly summary via email"""
        try:
            from_email = get_secret("GMAIL_USERNAME")
            to_email = get_secret("GMAIL_USERNAME")  # Send to self
            password = get_secret("GMAIL_PASSWORD")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Weekly Performance Summary - {datetime.now().strftime('%b %d, %Y')}"
            msg['From'] = from_email
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_email, password)
                server.send_message(msg)

            self.log("✅ Email sent successfully")

        except Exception as e:
            self.log(f"ERROR sending email: {e}")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='Generate weekly performance summary')
    parser.add_argument('--test', action='store_true', help='Test mode')
    parser.add_argument('--dry-run', action='store_true', help='Generate report but don\'t send email')
    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.json"
    generator = WeeklySummaryGenerator(config_path)

    # Generate report
    html = generator.generate_report()

    # Save to file
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = generator.output_dir / f"weekly-summary-{timestamp}.html"

    with open(output_file, 'w') as f:
        f.write(html)

    generator.log(f"\n✅ Report saved: {output_file}")

    # Open in browser for review
    import subprocess
    subprocess.run(['open', str(output_file)])

    # Send email (unless dry-run or test mode)
    if not args.dry_run and not args.test:
        generator.send_email(html)

    generator.log("="*80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
