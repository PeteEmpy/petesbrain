#!/usr/bin/env python3
"""
HTML Report Generator for Campaign Analysis
Generates beautiful, browser-ready HTML reports from analysis data
"""

from pathlib import Path
from datetime import datetime


class HTMLReportGenerator:
    """Generates HTML reports from campaign analysis data"""

    def __init__(self):
        self.templates_dir = Path(__file__).parent / 'templates'

    def generate_html_report(self, analysis_data, client_name, date_range):
        """
        Generate HTML report from analysis data

        Args:
            analysis_data: Dict from CampaignAnalyzer.analyze_campaigns()
            client_name: Client name for display
            date_range: Tuple of (start_date, end_date)

        Returns:
            str: HTML content
        """
        template_path = self.templates_dir / 'campaign_insights_report.html'
        template = template_path.read_text()

        # Calculate metrics
        campaigns = analysis_data.get('campaign_analyses', [])
        total_spend = sum(c['metrics']['spend'] for c in campaigns)
        total_revenue = sum(c['metrics']['revenue'] for c in campaigns)
        total_conversions = sum(c['metrics']['conversions'] for c in campaigns)
        blended_roas = total_revenue / total_spend if total_spend > 0 else 0

        health_score = analysis_data.get('health_score', 0)
        health_status = self._get_health_status(health_score)

        # Determine ROAS class
        target_roas = analysis_data.get('context_applied', {}).get('target_roas', 1.6)
        if blended_roas >= target_roas:
            roas_class = 'good'
        elif blended_roas >= target_roas * 0.8:
            roas_class = 'warning'
        else:
            roas_class = 'bad'

        # Issues class
        total_issues = len(analysis_data.get('recommendations', []))
        if total_issues == 0:
            issues_class = 'good'
        elif total_issues <= 3:
            issues_class = 'warning'
        else:
            issues_class = 'bad'

        # Generate campaign breakdown section
        campaigns_section = self._generate_campaigns_section(campaigns, target_roas)

        # Generate product section
        product_section = self._generate_product_section(analysis_data.get('product_analysis', {}))

        # Generate recommendations
        recommendations_html = self._generate_recommendations(analysis_data.get('recommendations', []))

        # Replace template placeholders
        html = template.replace('{{client_name}}', client_name.title())
        html = html.replace('{{date_range}}', f"{date_range[0]} to {date_range[1]}")
        html = html.replace('{{health_status}}', health_status)
        html = html.replace('{{health_score}}', str(health_score))
        html = html.replace('{{total_spend}}', f"{total_spend:,.2f}")
        html = html.replace('{{total_revenue}}', f"{total_revenue:,.2f}")
        html = html.replace('{{blended_roas}}', f"{blended_roas:.2f}")
        html = html.replace('{{roas_class}}', roas_class)
        html = html.replace('{{total_conversions}}', f"{total_conversions:.0f}")
        html = html.replace('{{total_issues}}', str(total_issues))
        html = html.replace('{{issues_class}}', issues_class)
        html = html.replace('{{campaigns_section}}', campaigns_section)
        html = html.replace('{{product_section}}', product_section)
        html = html.replace('{{recommendations}}', recommendations_html)
        html = html.replace('{{generated_date}}', datetime.now().strftime('%d %B %Y at %H:%M'))

        return html

    def _generate_campaigns_section(self, campaigns, target_roas):
        """Generate comprehensive campaign breakdown table"""
        if not campaigns:
            return ''

        # Sort campaigns by spend (highest first)
        sorted_campaigns = sorted(campaigns, key=lambda c: c['metrics']['spend'], reverse=True)

        rows = []
        for campaign in sorted_campaigns:
            name = campaign['campaign_name']
            metrics = campaign['metrics']
            spend = metrics['spend']
            revenue = metrics['revenue']
            roas = metrics['roas']
            conversions = metrics['conversions']
            clicks = metrics.get('clicks', 0)
            impressions = metrics.get('impressions', 0)

            # ROAS badge
            if roas >= target_roas:
                roas_badge = 'success'
                roas_symbol = '✓'
            elif roas >= target_roas * 0.8:
                roas_badge = 'warning'
                roas_symbol = '~'
            else:
                roas_badge = 'danger'
                roas_symbol = '✗'

            # Status badge
            status = campaign.get('status', 'UNKNOWN')
            status_class = 'success' if status == 'ENABLED' else 'warning'

            rows.append(f"""
            <tr>
                <td style="max-width: 300px; word-wrap: break-word;">{name}</td>
                <td><span class="badge {status_class}">{status}</span></td>
                <td style="text-align: right;">£{spend:,.2f}</td>
                <td style="text-align: right;">£{revenue:,.2f}</td>
                <td style="text-align: center;"><span class="badge {roas_badge}">{roas_symbol} {roas:.2f}x</span></td>
                <td style="text-align: right;">{conversions:.0f}</td>
                <td style="text-align: right;">{clicks:,}</td>
                <td style="text-align: right;">{impressions:,}</td>
            </tr>
            """)

        campaigns_table = f"""
        <table class="product-table">
            <thead>
                <tr>
                    <th>Campaign</th>
                    <th>Status</th>
                    <th style="text-align: right;">Spend</th>
                    <th style="text-align: right;">Revenue</th>
                    <th style="text-align: center;">ROAS</th>
                    <th style="text-align: right;">Conv</th>
                    <th style="text-align: right;">Clicks</th>
                    <th style="text-align: right;">Impr</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """

        return f"""
        <div class="section">
            <h2>Campaign Performance Breakdown</h2>
            <p style="color: #6b7280; margin-bottom: 20px;">
                Detailed metrics for all {len(campaigns)} campaigns. Target ROAS: {target_roas:.2f}x
            </p>
            {campaigns_table}
        </div>
        """

    def _get_health_status(self, score):
        """Get health status label from score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'

    def _generate_product_section(self, product_analysis):
        """Generate product insights section"""
        if not product_analysis or product_analysis.get('total_products', 0) == 0:
            return ''

        total_products = product_analysis.get('total_products', 0)
        products_with_issues = product_analysis.get('products_with_issues', 0)

        # Get top products
        product_metrics = product_analysis.get('product_metrics', {})
        if not product_metrics:
            return ''

        products = list(product_metrics.values())
        top_products = sorted(products, key=lambda p: p['cost'], reverse=True)[:5]

        rows = []
        for i, product in enumerate(top_products, 1):
            roas = (product['revenue'] / product['cost']) if product['cost'] > 0 else 0
            roas_badge = 'success' if roas >= 1.5 else 'warning' if roas >= 1.0 else 'danger'

            rows.append(f"""
            <tr>
                <td>{i}</td>
                <td>{product['product_title'][:80]}</td>
                <td>£{product['cost']:.2f}</td>
                <td>£{product['revenue']:.2f}</td>
                <td><span class="badge {roas_badge}">{roas:.2f}x</span></td>
                <td>{product['conversions']:.0f}</td>
                <td>{product['clicks']}</td>
            </tr>
            """)

        product_table = f"""
        <table class="product-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Product</th>
                    <th>Spend</th>
                    <th>Revenue</th>
                    <th>ROAS</th>
                    <th>Conv</th>
                    <th>Clicks</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """

        return f"""
        <div class="section">
            <h2>Product-Level Insights</h2>
            <p style="color: #6b7280; margin-bottom: 20px;">
                Tracking {total_products} unique products. {products_with_issues} products have issues requiring attention.
            </p>
            {product_table}
        </div>
        """

    def _generate_recommendations(self, recommendations):
        """Generate recommendations HTML"""
        if not recommendations:
            return '<p style="color: #6b7280;">No recommendations at this time.</p>'

        html_parts = []
        for rec in recommendations:
            priority = rec['priority'].lower()
            priority_class = priority

            # Format recommendation text (full text with line breaks preserved)
            rec_text = rec['recommendation'].replace('\n', '<br>')

            # Impact metrics
            impact = rec['impact']
            impact_html = f"""
            <div class="impact-metrics">
                <div class="impact-metric">
                    <div class="label">Affected Campaigns</div>
                    <div class="value">{rec['affected_campaigns']}</div>
                </div>
                <div class="impact-metric">
                    <div class="label">Total Spend</div>
                    <div class="value">£{impact['total_spend']:.0f}</div>
                </div>
                <div class="impact-metric">
                    <div class="label">Average ROAS</div>
                    <div class="value">{impact['avg_roas']:.2f}x</div>
                </div>
            </div>
            """

            # Next steps
            next_steps_html = ''
            if rec.get('next_steps'):
                steps = '\n'.join(f'<li>{step}</li>' for step in rec['next_steps'][:3])
                next_steps_html = f"""
                <div class="next-steps">
                    <h4>✅ Next Steps</h4>
                    <ul>
                        {steps}
                    </ul>
                </div>
                """

            # KB articles
            kb_html = ''
            if rec.get('kb_articles'):
                articles = '\n'.join(
                    f'<div class="kb-article">📚 {article["title"]}</div>'
                    for article in rec['kb_articles'][:2]
                )
                kb_html = f"""
                <div class="kb-articles">
                    <h4>Related Knowledge Base Articles</h4>
                    {articles}
                </div>
                """

            html_parts.append(f"""
            <div class="recommendation {priority_class}">
                <div class="recommendation-header">
                    <div class="recommendation-title">{rec['title']}</div>
                    <span class="priority-badge {priority_class}">{rec['priority']}</span>
                </div>
                {impact_html}
                <div class="recommendation-content">{rec_text}</div>
                {next_steps_html}
                {kb_html}
            </div>
            """)

        return '\n'.join(html_parts)

    def save_and_open_report(self, html_content, output_path):
        """
        Save HTML report and open in browser

        Args:
            html_content: HTML string
            output_path: Path to save file

        Returns:
            Path: Path to saved file
        """
        import subprocess

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content)

        # Open in browser
        subprocess.run(['open', str(output_path)], check=False)

        return output_path


if __name__ == '__main__':
    # Test with sample data
    generator = HTMLReportGenerator()

    sample_data = {
        'health_score': 75,
        'campaign_analyses': [
            {
                'campaign_name': 'Test Campaign',
                'metrics': {
                    'spend': 500.0,
                    'revenue': 1500.0,
                    'conversions': 30,
                    'roas': 3.0
                }
            }
        ],
        'recommendations': [
            {
                'priority': 'P1',
                'title': 'Test Recommendation',
                'affected_campaigns': 1,
                'campaign_names': ['Test Campaign'],
                'impact': {
                    'total_spend': 500.0,
                    'avg_roas': 3.0
                },
                'recommendation': 'This is a test recommendation.',
                'next_steps': ['Step 1', 'Step 2'],
                'kb_articles': []
            }
        ],
        'product_analysis': {
            'total_products': 0
        },
        'context_applied': {
            'target_roas': 1.6
        }
    }

    html = generator.generate_html_report(
        sample_data,
        'Test Client',
        ('2025-12-01', '2025-12-15')
    )

    print("HTML report generated successfully")
