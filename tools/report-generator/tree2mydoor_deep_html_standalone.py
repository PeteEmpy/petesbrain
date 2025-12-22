#!/usr/bin/env python3
"""
Standalone HTML generator for Tree2mydoor deep audits

Generates complete HTML without inheritance dependencies
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime


def generate_deep_audit_html(
    analysis: Dict[str, Any],
    client_name: str,
    date_range: Tuple[str, str]
) -> str:
    """Generate complete HTML report for deep audit"""

    start_date, end_date = date_range

    # Calculate totals
    campaigns = analysis.get('campaign_analyses', [])
    total_spend = sum(c['metrics']['spend'] for c in campaigns)
    total_profit = sum(c['metrics']['revenue'] for c in campaigns)
    total_conversions = sum(c['metrics']['conversions'] for c in campaigns)
    account_poas = total_profit / total_spend if total_spend > 0 else 0

    health_score = analysis.get('health_score', 0)

    # Generate HTML sections
    header_html = _generate_header(client_name, start_date, end_date)
    health_card_html = _generate_health_card(
        health_score, total_spend, total_profit, account_poas, total_conversions
    )
    deep_audits_html = _generate_deep_audits_section(analysis.get('deep_audits', {}))
    root_cause_html = _generate_root_cause_section(analysis.get('root_cause_analyses', []))
    kb_insights_html = _generate_kb_insights_section(analysis.get('kb_insights', {}))
    recommendations_html = _generate_recommendations_section(analysis.get('recommendations', []))

    # Assemble full HTML
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
    </style>
</head>
<body>
    <div class="container">
        {header_html}
        <button class="copy-button" onclick="copyReport()">📋 Copy Report to Clipboard</button>
        {health_card_html}
        {deep_audits_html}
        {root_cause_html}
        {kb_insights_html}
        {recommendations_html}

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


def _generate_header(client_name: str, start_date: str, end_date: str) -> str:
    """Generate report header"""
    return f'''
        <h1>🌳 {client_name} Deep Account Audit</h1>
        <div style="color: #6b7280; margin: 12px 0 24px 0;">
            <strong>Period:</strong> {start_date} to {end_date} (3-day conversion lag applied)<br>
            <strong>Type:</strong> Comprehensive Configuration & Performance Audit<br>
            <strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </div>
    '''


def _generate_health_card(
    health_score: int,
    total_spend: float,
    total_profit: float,
    account_poas: float,
    total_conversions: float
) -> str:
    """Generate health score card"""
    return f'''
        <div class="health-card">
            <div class="metric-card">
                <div class="metric-label">Health Score</div>
                <div class="metric-value">{health_score}/100</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Spend</div>
                <div class="metric-value">£{total_spend:,.2f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Profit</div>
                <div class="metric-value">£{total_profit:,.2f}</div>
                <div style="font-size: 11px; color: #6b7280;">conversions_value = PROFIT</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Account POAS</div>
                <div class="metric-value">{account_poas:.2f}x</div>
                <div style="font-size: 11px; color: #6b7280;">Target: 1.60x</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Conversions</div>
                <div class="metric-value">{total_conversions:.0f}</div>
            </div>
        </div>
    '''


def _generate_deep_audits_section(audits: Dict[str, Any]) -> str:
    """Generate deep audits section"""

    if not audits:
        return ''

    sections = []

    # Performance issues
    perf_issues = audits.get('performance_issues', [])
    if perf_issues:
        perf_html = '<h3>⚠️  Performance Issues Detected</h3>'
        for issue in perf_issues:
            severity_class = issue.get('severity', 'MEDIUM').lower()
            perf_html += f'''
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
        sections.append(perf_html)

    # Budget issues
    budget_issues = audits.get('budget_issues', [])
    if budget_issues:
        budget_html = '<h3>💰 Budget Allocation Issues</h3>'
        for issue in budget_issues:
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

    # Profit Tier recommendations (ProfitMetrics-based)
    tier_recs = audits.get('profit_tier_recommendations', [])
    if tier_recs:
        tier_html = '<h3>📊 Profit Tier Optimization</h3>'
        for rec in tier_recs:
            tier_html += f'''
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
        sections.append(tier_html)

    # Seasonal issues
    seasonal_issues = audits.get('seasonal_issues', [])
    if seasonal_issues:
        seasonal_html = '<h3>🎄 Seasonal Readiness Issues</h3>'
        for issue in seasonal_issues:
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


def _generate_root_cause_section(root_causes: List[Dict[str, Any]]) -> str:
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
                <div style="background: white; padding: 12px; border-radius: 4px; margin-bottom: 16px;">
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


def _generate_kb_insights_section(kb_insights: Dict[str, Any]) -> str:
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


def _generate_recommendations_section(recommendations: List[Dict[str, Any]]) -> str:
    """Generate recommendations section"""

    if not recommendations:
        return ''

    recs_html = ''

    for rec in recommendations:
        priority = rec.get('priority', 'P2')
        title = rec.get('title', 'Recommendation')
        problem = rec.get('problem', '')
        recommendation = rec.get('recommendation', '')

        recs_html += f'''
            <div class="recommendation">
                <div style="margin-bottom: 12px;">
                    <span class="priority-badge priority-{priority.lower()}">{priority}</span>
                    <strong style="font-size: 18px;">{title}</strong>
                </div>
                {f'<div style="margin-bottom: 12px; color: #6b7280;">{problem}</div>' if problem else ''}
                <div style="line-height: 1.8; white-space: pre-wrap;">{recommendation}</div>
            </div>
        '''

    return f'''
        <div class="section" style="background: #f0fdf4; border-left: 4px solid #10B981;">
            <h2 style="color: #065f46;">🎯 Prioritised Recommendations</h2>
            {recs_html}
        </div>
    '''


if __name__ == '__main__':
    print("Tree2mydoor Deep HTML Standalone Generator")
    print("This is a library module")
