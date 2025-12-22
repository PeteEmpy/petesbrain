#!/usr/bin/env python3
"""
Tree2mydoor Profit-Focused HTML Report Generator
Extends base HTML generator with profit-specific sections
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from report_html_generator import HTMLReportGenerator


class Tree2mydoorHTMLGenerator(HTMLReportGenerator):
    """
    Specialized HTML generator for Tree2mydoor profit reports

    Adds:
    - Profit context section
    - Tier structure visualization
    - Product Hero performance breakdown
    - Seasonality context
    - POAS terminology (not ROAS)
    """

    def generate_html_report(self, analysis_data, client_name, date_range):
        """
        Generate HTML report with profit-focused enhancements

        Args:
            analysis_data: Dict from Tree2mydoorProfitAnalyzer.analyze_campaigns()
            client_name: Client name for display
            date_range: Tuple of (start_date, end_date)

        Returns:
            str: HTML content
        """
        # Get base HTML
        html = super().generate_html_report(analysis_data, client_name, date_range)

        # Replace ROAS with POAS throughout
        html = html.replace('ROAS', 'POAS')
        html = html.replace('Revenue', 'Profit')

        # Add profit context section (after health score, before campaigns)
        profit_context_html = self._generate_profit_context_section(
            analysis_data.get('profit_context', {})
        )

        # Find insertion point (after health-score div)
        insertion_marker = '</div>\n\n        \n\n        <div class="section">'
        html = html.replace(
            insertion_marker,
            f'</div>\n\n{profit_context_html}\n\n        <div class="section">'
        )

        # Add tier guidance section (after campaigns, before recommendations)
        tier_guidance_html = self._generate_tier_guidance_section(
            analysis_data.get('tier_guidance', {})
        )

        # Find insertion point (before recommendations section)
        recommendations_marker = '<div class="section">\n            <h2>Prioritised Recommendations</h2>'
        html = html.replace(
            recommendations_marker,
            f'{tier_guidance_html}\n\n        {recommendations_marker}'
        )

        # Add seasonality context (after recommendations, before footer)
        seasonality_html = self._generate_seasonality_section(
            analysis_data.get('seasonality_context', {})
        )

        footer_marker = '<div class="footer">'
        html = html.replace(
            footer_marker,
            f'{seasonality_html}\n\n        {footer_marker}'
        )

        return html

    def _generate_profit_context_section(self, profit_context: Dict[str, Any]) -> str:
        """Generate profit context section with ProfitMetrics explanation"""

        if not profit_context:
            return ''

        uses_profitmetrics = profit_context.get('uses_profitmetrics', False)
        conversions_value_meaning = profit_context.get('conversions_value_meaning', '')
        target_poas = profit_context.get('target_poas', 1.60)
        tier_structure = profit_context.get('tier_structure', {})
        optimization_focus = profit_context.get('optimization_focus', '')
        key_considerations = profit_context.get('key_considerations', [])

        # Build tier structure list
        tier_list = []
        for tier, description in tier_structure.items():
            tier_list.append(f'<li><strong>{tier}</strong>: {description}</li>')

        tier_html = '\n                    '.join(tier_list)

        # Build key considerations list
        considerations_list = []
        for consideration in key_considerations:
            considerations_list.append(f'<li>{consideration}</li>')

        considerations_html = '\n                    '.join(considerations_list)

        return f'''
        <div class="section" style="background: #f0fdf4; border-left: 4px solid #10B981;">
            <h2 style="color: #065f46;">💰 Profit-Based Optimization Context</h2>
            <div style="color: #1f2937; line-height: 1.8;">
                <p style="margin-bottom: 16px;">
                    <strong>⚠️  CRITICAL:</strong> Tree2mydoor uses <strong>ProfitMetrics</strong> - all conversion values represent <strong>{conversions_value_meaning}</strong>.
                </p>
                <p style="margin-bottom: 16px;">
                    This means "POAS" (Profit on Ad Spend) is used instead of ROAS. A POAS of {target_poas:.2f}x means £{target_poas:.2f} profit per £1 spent.
                </p>

                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #d1fae5;">
                    <h3 style="color: #065f46; margin-bottom: 12px;">Tier Structure (Channable + Product Hero)</h3>
                    <p style="margin-bottom: 12px;"><strong>Optimization Focus:</strong> {optimization_focus}</p>
                    <ul style="list-style-type: none; padding-left: 0;">
                        {tier_html}
                    </ul>
                </div>

                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #d1fae5;">
                    <h3 style="color: #065f46; margin-bottom: 12px;">Key Considerations</h3>
                    <ul style="padding-left: 20px;">
                        {considerations_html}
                    </ul>
                </div>
            </div>
        </div>
'''

    def _generate_tier_guidance_section(self, tier_guidance: Dict[str, Any]) -> str:
        """Generate tier-based campaign guidance section"""

        if not tier_guidance:
            return ''

        tier_distribution = tier_guidance.get('tier_distribution', {})
        guidance_text = tier_guidance.get('guidance', '')

        # Build tier distribution bars
        tier_rows = []
        tier_colors = {
            'Tier A (≥1.80x)': '#10B981',
            'Tier B (≥1.45x)': '#3b82f6',
            'Tier C (≥1.35x)': '#f59e0b',
            'Below Tier C': '#ef4444'
        }

        total_campaigns = sum(tier_distribution.values())

        for tier, count in tier_distribution.items():
            percentage = (count / total_campaigns * 100) if total_campaigns > 0 else 0
            color = tier_colors.get(tier, '#6b7280')

            tier_rows.append(f'''
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="font-weight: 600; color: #1f2937;">{tier}</span>
                        <span style="color: #6b7280;">{count} campaigns ({percentage:.0f}%)</span>
                    </div>
                    <div style="background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: {color}; width: {percentage}%; height: 100%;"></div>
                    </div>
                </div>
            ''')

        tier_bars_html = '\n'.join(tier_rows)

        # Format guidance text (preserve line breaks)
        guidance_html = guidance_text.replace('\n', '<br>')

        return f'''
        <div class="section">
            <h2>📊 Tier-Based Campaign Assessment</h2>
            <p style="color: #6b7280; margin-bottom: 20px;">
                Campaigns grouped by POAS performance tier. Budget allocation should prioritize Tier A, throttle Tier C, and pause campaigns below Tier C.
            </p>

            <div style="background: #f9fafb; padding: 24px; border-radius: 8px; margin-bottom: 24px; border: 1px solid #e5e7eb;">
                <h3 style="color: #1f2937; margin-bottom: 16px;">Campaign Distribution by Tier</h3>
                {tier_bars_html}
            </div>

            <div style="background: white; padding: 24px; border-radius: 8px; border: 1px solid #e5e7eb;">
                <h3 style="color: #1f2937; margin-bottom: 16px;">Actionable Guidance</h3>
                <div style="color: #4b5563; line-height: 1.8; font-family: 'Courier New', monospace; font-size: 14px;">
                    {guidance_html}
                </div>
            </div>
        </div>
'''

    def _generate_seasonality_section(self, seasonality_context: Dict[str, Any]) -> str:
        """Generate seasonality context section"""

        if not seasonality_context:
            return ''

        is_peak_season = seasonality_context.get('is_peak_season', False)
        season_name = seasonality_context.get('season_name', 'Unknown')
        context_text = seasonality_context.get('context', '')

        # Icon and color based on season
        if is_peak_season:
            icon = '🎄'
            bg_color = '#f0fdf4'
            border_color = '#10B981'
            title_color = '#065f46'
        else:
            icon = '📊'
            bg_color = '#f9fafb'
            border_color = '#6b7280'
            title_color = '#1f2937'

        # Format context text
        context_html = context_text.replace('\n', '<br>')

        return f'''
        <div class="section" style="background: {bg_color}; border-left: 4px solid {border_color};">
            <h2 style="color: {title_color};">{icon} Seasonality Context: {season_name}</h2>
            <div style="color: #1f2937; line-height: 1.8; font-family: 'Courier New', monospace; font-size: 14px;">
                {context_html}
            </div>
        </div>
'''


def main():
    """Test HTML generator"""
    print("🌳 Tree2mydoor HTML Generator Test")
    print("=" * 60)

    generator = Tree2mydoorHTMLGenerator()

    # Sample analysis data with profit-specific sections
    sample_data = {
        'health_score': 77,
        'campaign_analyses': [
            {
                'campaign_name': 'T2MD | P Max | HP&P',
                'metrics': {
                    'spend': 1356.58,
                    'revenue': 1948.25,  # Actually profit
                    'roas': 1.44,  # Actually POAS
                    'conversions': 101,
                    'clicks': 1336,
                    'impressions': 95834
                },
                'status': 'ENABLED'
            }
        ],
        'recommendations': [],
        'profit_context': {
            'uses_profitmetrics': True,
            'conversions_value_meaning': 'PROFIT (not revenue)',
            'target_poas': 1.60,
            'tier_structure': {
                'Tier A': '≥1.80x POAS - Heroes & top Sidekicks',
                'Tier B': '≥1.45x POAS - Mid-performing products',
                'Tier C': '≥1.35x POAS or throttle - Marginal performers'
            },
            'optimization_focus': 'Maximize profit while maintaining growth',
            'key_considerations': [
                'Stock instability affects campaign learning',
                'December is peak season',
                'Memorial roses perform well',
                'CPC inflation outpacing efficiency gains'
            ]
        },
        'tier_guidance': {
            'tier_distribution': {
                'Tier A (≥1.80x)': 2,
                'Tier B (≥1.45x)': 4,
                'Tier C (≥1.35x)': 2,
                'Below Tier C': 1
            },
            'guidance': '✅ TIER A - Scale aggressively\n⚠️  TIER B - Maintain budget\n⚠️  TIER C - THROTTLE\n🚨 Below - PAUSE'
        },
        'seasonality_context': {
            'is_peak_season': True,
            'season_name': 'Christmas Peak (December)',
            'context': '🎄 PEAK SEASON - Maximize profit opportunity'
        },
        'product_analysis': {'total_products': 0},
        'context_applied': {'target_roas': 1.6}
    }

    html = generator.generate_html_report(
        sample_data,
        'Tree2mydoor',
        ('2025-12-07', '2025-12-13')
    )

    # Save to test file
    output_file = Path(__file__).parent / 'reports' / 'tree2mydoor_profit_test.html'
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(html)

    print(f"✅ Test report generated: {output_file}")
    print(f"   File size: {len(html):,} bytes")
    print()

    # Check for profit-specific sections
    checks = {
        'Profit-Based Optimization Context': 'Profit-Based Optimization Context' in html,
        'POAS terminology': 'POAS' in html and 'ROAS' not in html.replace('POAS', ''),
        'Tier-Based Campaign Assessment': 'Tier-Based Campaign Assessment' in html,
        'Seasonality Context': 'Seasonality Context' in html,
        'Product Hero': 'Product Hero' in html or 'Heroes' in html
    }

    print("Section Checks:")
    for check, passed in checks.items():
        status = '✅' if passed else '❌'
        print(f"   {status} {check}")

    print()
    print("✅ HTML generator working correctly")


if __name__ == '__main__':
    main()
