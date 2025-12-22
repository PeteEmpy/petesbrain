#!/usr/bin/env python3
"""
Tree2mydoor Deep Audit HTML Generator

Generates comprehensive HTML reports showing:
- Deep configuration audits
- Root cause analyses
- Best practice violations
- Knowledge base-informed recommendations
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Import from same directory
from report_html_generator import HTMLReportGenerator


class Tree2mydoorDeepHTMLGenerator(HTMLReportGenerator):
    """
    HTML generator for Tree2mydoor deep auditing reports

    Extends base generator with sections for:
    - Deep audit results
    - Root cause analyses
    - Knowledge base insights
    - Specific actionable fixes
    """

    def generate_html_report(
        self,
        analysis: Dict[str, Any],
        client_name: str,
        date_range: Tuple[str, str]
    ) -> str:
        """Generate comprehensive HTML report with deep audit sections"""

        # Generate base sections
        header = self._generate_header(client_name, date_range)
        health_card = self._generate_health_score_card(analysis)

        # Deep audit-specific sections (NEW)
        deep_audits_section = self._generate_deep_audits_section(analysis.get('deep_audits', {}))
        root_cause_section = self._generate_root_cause_section(analysis.get('root_cause_analyses', []))
        kb_insights_section = self._generate_kb_insights_section(analysis.get('kb_insights', {}))

        # Standard sections
        profit_context = self._generate_profit_context_section(analysis.get('profit_context', {}))
        tier_guidance = self._generate_tier_guidance_section(analysis.get('tier_guidance', {}))
        seasonality = self._generate_seasonality_section(analysis.get('seasonality_context', {}))
        campaign_breakdown = self._generate_campaign_breakdown(analysis.get('campaign_analyses', []))
        recommendations = self._generate_recommendations_section(analysis.get('recommendations', []))

        # Assemble HTML
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{client_name} - Deep Audit Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1f2937;
            border-bottom: 3px solid #10B981;
            padding-bottom: 12px;
        }}
        h2 {{
            color: #065f46;
            margin-top: 32px;
            margin-bottom: 16px;
        }}
        h3 {{
            color: #047857;
            margin-top: 20px;
            margin-bottom: 12px;
        }}
        .section {{
            margin: 24px 0;
            padding: 20px;
            background: #f9fafb;
            border-radius: 8px;
        }}
        .health-card {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }}
        .metric-card {{
            background: white;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #10B981;
        }}
        .metric-label {{
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
            margin: 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            background: white;
        }}
        th {{
            background: #f3f4f6;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #d1d5db;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
        }}
        tr:hover {{
            background: #f9fafb;
        }}
        .audit-issue {{
            background: white;
            padding: 16px;
            margin: 12px 0;
            border-left: 4px solid #ef4444;
            border-radius: 4px;
        }}
        .audit-issue.high {{
            border-left-color: #dc2626;
        }}
        .audit-issue.medium {{
            border-left-color: #f59e0b;
        }}
        .audit-issue.low {{
            border-left-color: #3b82f6;
        }}
        .root-cause {{
            background: #fef3c7;
            padding: 20px;
            margin: 16px 0;
            border-radius: 8px;
            border-left: 4px solid #f59e0b;
        }}
        .kb-insight {{
            background: #e0f2fe;
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
            border-left: 4px solid #0284c7;
        }}
        .recommendation {{
            background: white;
            padding: 20px;
            margin: 16px 0;
            border-radius: 8px;
            border-left: 4px solid #10B981;
        }}
        .priority-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
        }}
        .priority-p0 {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .priority-p1 {{
            background: #fed7aa;
            color: #9a3412;
        }}
        .priority-p2 {{
            background: #dbeafe;
            color: #1e40af;
        }}
        .copy-button {{
            background: #10B981;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            margin: 20px 0;
        }}
        .copy-button:hover {{
            background: #059669;
        }}
        .tier-bar {{
            height: 24px;
            background: #d1fae5;
            border-radius: 4px;
            margin: 8px 0;
            position: relative;
            overflow: hidden;
        }}
        .tier-bar-fill {{
            height: 100%;
            background: #10B981;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {header}
        <button class="copy-button" onclick="copyReport()">📋 Copy Report to Clipboard</button>

        {health_card}
        {deep_audits_section}
        {root_cause_section}
        {kb_insights_section}
        {profit_context}
        {tier_guidance}
        {seasonality}
        {campaign_breakdown}
        {recommendations}

        <div style="margin-top: 40px; padding: 20px; background: #f3f4f6; border-radius: 8px; text-align: center; color: #6b7280;">
            <p style="margin: 0;">🤖 Generated with Deep Account Auditor</p>
            <p style="margin: 8px 0 0 0; font-size: 12px;">Tree2mydoor Profit-Focused Analysis • {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </div>
    </div>

    <script>
        function copyReport() {{
            const content = document.querySelector('.container').innerText;
            navigator.clipboard.writeText(content).then(() => {{
                alert('✅ Report copied to clipboard!');
            }});
        }}
    </script>
</body>
</html>
'''

        return html

    def _generate_deep_audits_section(self, audits: Dict[str, Any]) -> str:
        """Generate deep audits section showing all detected issues"""

        if not audits:
            return ''

        sections = []

        # Performance issues
        if audits.get('performance_issues'):
            performance_html = '<h3>⚠️  Performance Issues Detected</h3>'
            for issue in audits['performance_issues']:
                severity_class = issue.get('severity', 'MEDIUM').lower()
                performance_html += f'''
                    <div class="audit-issue {severity_class}">
                        <div style="font-weight: bold; color: #dc2626; margin-bottom: 8px;">
                            {issue.get('severity', 'ISSUE')}: {issue['campaign']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            {issue['issue']}
                        </div>
                        {f'<div style="color: #6b7280; font-size: 14px;">Spend: £{issue["spend"]:.2f} | POAS: {issue["poas"]:.2f}x</div>' if 'spend' in issue else ''}
                    </div>
                '''
            sections.append(performance_html)

        # Budget issues
        if audits.get('budget_issues'):
            budget_html = '<h3>💰 Budget Allocation Issues</h3>'
            for issue in audits['budget_issues']:
                severity_class = issue.get('severity', 'MEDIUM').lower()
                budget_html += f'''
                    <div class="audit-issue {severity_class}">
                        <div style="font-weight: bold; margin-bottom: 8px;">
                            {issue['campaign']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>Issue:</strong> {issue['issue']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>Impact:</strong> {issue.get('impact', 'N/A')}
                        </div>
                        <div style="color: #047857;">
                            <strong>Fix:</strong> {issue.get('fix', 'N/A')}
                        </div>
                        <div style="color: #6b7280; font-size: 14px; margin-top: 8px;">
                            Expected Outcome: {issue.get('expected_outcome', 'N/A')}
                        </div>
                    </div>
                '''
            sections.append(budget_html)

        # Product Hero recommendations
        if audits.get('product_hero_recommendations'):
            hero_html = '<h3>🦸 Product Hero Optimization</h3>'
            for rec in audits['product_hero_recommendations']:
                hero_html += f'''
                    <div class="audit-issue medium">
                        <div style="font-weight: bold; margin-bottom: 8px;">
                            <span class="priority-badge priority-{rec['priority'].lower()}">{rec['priority']}</span>
                            {rec['action']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>Why:</strong> {rec['why']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <strong>How:</strong> {rec['how']}
                        </div>
                        <div style="color: #047857;">
                            <strong>Expected Outcome:</strong> {rec['expected_outcome']}
                        </div>
                    </div>
                '''
            sections.append(hero_html)

        # Seasonal issues
        if audits.get('seasonal_issues'):
            seasonal_html = '<h3>🎄 Seasonal Readiness Issues</h3>'
            for issue in audits['seasonal_issues']:
                severity_class = issue.get('severity', 'MEDIUM').lower()
                seasonal_html += f'''
                    <div class="audit-issue {severity_class}">
                        <div style="font-weight: bold; margin-bottom: 8px;">
                            {issue.get('campaign', 'General')}
                        </div>
                        <div style="margin-bottom: 8px;">
                            {issue['issue']}
                        </div>
                        <div style="color: #047857; margin-bottom: 8px;">
                            <strong>Fix:</strong> {issue['fix']}
                        </div>
                        <div style="color: #6b7280; font-size: 14px;">
                            {issue['impact']}
                        </div>
                    </div>
                '''
            sections.append(seasonal_html)

        if sections:
            return f'''
                <div class="section" style="background: #fef2f2; border-left: 4px solid #dc2626;">
                    <h2 style="color: #991b1b;">🔍 Deep Account Audits</h2>
                    <p style="color: #1f2937; margin-bottom: 20px;">
                        Comprehensive configuration analysis revealing specific issues beyond surface metrics.
                    </p>
                    {''.join(sections)}
                </div>
            '''

        return ''

    def _generate_root_cause_section(self, root_causes: List[Dict[str, Any]]) -> str:
        """Generate root cause analysis section"""

        if not root_causes:
            return ''

        root_cause_html = ''

        for rc in root_causes:
            causes_html = '<ul style="margin: 12px 0;">'
            for cause in rc.get('likely_causes', []):
                causes_html += f'<li style="margin: 8px 0;">{cause}</li>'
            causes_html += '</ul>'

            evidence_html = '<ul style="margin: 12px 0;">'
            for evidence in rc.get('evidence', []):
                evidence_html += f'<li style="margin: 8px 0; color: #6b7280;">{evidence}</li>'
            evidence_html += '</ul>'

            fixes_html = ''
            for i, fix in enumerate(rc.get('recommended_fixes', []), 1):
                fixes_html += f'''
                    <div style="background: white; padding: 12px; margin: 8px 0; border-radius: 4px;">
                        <div style="font-weight: bold; margin-bottom: 4px;">{i}. {fix['action']}</div>
                        <div style="color: #047857; font-size: 14px;">
                            Expected Impact: {fix['expected_impact']}
                        </div>
                    </div>
                '''

            root_cause_html += f'''
                <div class="root-cause">
                    <h3 style="color: #92400e; margin-top: 0;">Campaign: {rc['campaign']}</h3>
                    <div style="background: #fef3c7; padding: 12px; border-radius: 4px; margin-bottom: 16px;">
                        <strong>Problem:</strong> {rc['problem']}
                    </div>

                    <div style="margin: 16px 0;">
                        <strong style="color: #92400e;">Likely Root Causes:</strong>
                        {causes_html}
                    </div>

                    <div style="margin: 16px 0;">
                        <strong style="color: #92400e;">Evidence:</strong>
                        {evidence_html}
                    </div>

                    <div style="margin: 16px 0;">
                        <strong style="color: #92400e;">Recommended Fixes:</strong>
                        {fixes_html}
                    </div>
                </div>
            '''

        return f'''
            <div class="section" style="background: #fffbeb; border-left: 4px solid #f59e0b;">
                <h2 style="color: #92400e;">🎯 Root Cause Analysis</h2>
                <p style="color: #1f2937; margin-bottom: 20px;">
                    Deep dive into WHY campaigns are underperforming, with evidence-based diagnosis and specific fixes.
                </p>
                {root_cause_html}
            </div>
        '''

    def _generate_kb_insights_section(self, kb_insights: Dict[str, Any]) -> str:
        """Generate knowledge base insights section"""

        if not kb_insights or not kb_insights.get('key_recommendations'):
            return ''

        insights_html = ''

        for insight in kb_insights.get('key_recommendations', []):
            insights_html += f'''
                <div class="kb-insight">
                    <h3 style="color: #0c4a6e; margin-top: 0;">📚 {insight['topic']}</h3>
                    <div style="margin: 12px 0; color: #1f2937;">
                        <strong>Insight:</strong> {insight['insight']}
                    </div>
                    <div style="margin: 12px 0; color: #047857;">
                        <strong>Application to Tree2mydoor:</strong> {insight['application']}
                    </div>
                    <div style="font-size: 12px; color: #6b7280;">
                        Source: {insight['source']}
                    </div>
                </div>
            '''

        return f'''
            <div class="section" style="background: #f0f9ff; border-left: 4px solid #0284c7;">
                <h2 style="color: #0c4a6e;">💡 Knowledge Base Insights</h2>
                <p style="color: #1f2937; margin-bottom: 20px;">
                    Strategic recommendations from knowledge base (1,983 articles) applied to your account.
                </p>
                {insights_html}
            </div>
        '''

    def _generate_profit_context_section(self, profit_context: Dict[str, Any]) -> str:
        """Generate profit context section"""

        if not profit_context:
            return ''

        conversions_value_meaning = profit_context.get('conversions_value_meaning', 'PROFIT')
        target_poas = profit_context.get('target_poas', 1.60)
        optimization_focus = profit_context.get('optimization_focus', 'Maximise profit per £1 spent')

        tier_structure = profit_context.get('tier_structure', {})
        tier_html = ''
        for tier, description in tier_structure.items():
            tier_html += f'<li style="margin: 8px 0;"><strong>{tier.replace("_", " ").title()}:</strong> {description}</li>'

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
                </div>
            </div>
        '''

    def _generate_tier_guidance_section(self, tier_guidance: Dict[str, Any]) -> str:
        """Generate tier-based guidance section"""

        if not tier_guidance:
            return ''

        tier_dist = tier_guidance.get('tier_distribution', {})
        total_campaigns = sum(tier_dist.values())

        tier_bars = ''
        for tier, count in tier_dist.items():
            percentage = (count / total_campaigns * 100) if total_campaigns > 0 else 0
            tier_bars += f'''
                <div style="margin: 12px 0;">
                    <div style="margin-bottom: 4px; font-weight: 600;">{tier}: {count} campaign{'s' if count != 1 else ''}</div>
                    <div class="tier-bar">
                        <div class="tier-bar-fill" style="width: {percentage}%;">
                            {percentage:.0f}%
                        </div>
                    </div>
                </div>
            '''

        actions = tier_guidance.get('actions', {})
        actions_html = '<ul style="list-style-type: none; padding-left: 0; margin-top: 16px;">'
        for tier, action in actions.items():
            actions_html += f'<li style="margin: 8px 0;"><strong>{tier.replace("_", " ").title()}:</strong> {action}</li>'
        actions_html += '</ul>'

        return f'''
            <div class="section" style="background: #f0fdf4; border-left: 4px solid #10B981;">
                <h2 style="color: #065f46;">📊 Tier-Based Campaign Assessment</h2>
                {tier_bars}
                <div style="margin-top: 20px;">
                    <h3 style="color: #065f46;">Recommended Actions by Tier:</h3>
                    {actions_html}
                </div>
            </div>
        '''

    def _generate_seasonality_section(self, seasonality: Dict[str, Any]) -> str:
        """Generate seasonality context section"""

        if not seasonality:
            return ''

        season_name = seasonality.get('season_name', 'Standard Season')
        is_peak = seasonality.get('is_peak_season', False)
        guidance = seasonality.get('guidance', '')

        icon = '🎄' if is_peak else '📅'
        bg_color = '#fef3c7' if is_peak else '#f3f4f6'
        border_color = '#f59e0b' if is_peak else '#9ca3af'

        guidance_html = guidance.replace('\n', '<br>')

        return f'''
            <div class="section" style="background: {bg_color}; border-left: 4px solid {border_color};">
                <h2 style="color: #92400e;">{icon} Seasonality Context</h2>
                <div style="color: #1f2937; line-height: 1.8;">
                    <p style="margin-bottom: 16px;">
                        <strong>Current Season:</strong> {season_name} {' (PEAK SEASON)' if is_peak else ''}
                    </p>
                    <div style="background: white; padding: 16px; border-radius: 8px;">
                        {guidance_html}
                    </div>
                </div>
            </div>
        '''


if __name__ == '__main__':
    print("Tree2mydoor Deep HTML Generator")
    print("This is a library module - use run_tree2mydoor_deep_report.py to generate reports")
