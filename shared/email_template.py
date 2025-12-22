#!/usr/bin/env python3
"""
Canonical Email Template Module
================================

This module provides the single source of truth for email formatting across
all PetesBrain tools and agents.

Standards:
- Font: Verdana 13px
- Line-height: 1.5
- Copy-to-clipboard button (green styling)
- British English spelling throughout

Usage:
    from shared.email_template import render_email

    html = render_email(
        content="<p>Email body goes here.</p>",
        recipient_name="Barry",
        sender_name="Peter",
        sign_off="Regards"
    )
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict, List


def get_template_path() -> Path:
    """Get path to master email template."""
    # Try to find project root
    current = Path(__file__).resolve()

    # Go up until we find infrastructure/templates
    for parent in [current.parent.parent, Path.cwd()]:
        template_path = parent / "infrastructure" / "templates" / "email-template-master.html"
        if template_path.exists():
            return template_path

    raise FileNotFoundError(
        "Could not find email-template-master.html. "
        "Expected at: infrastructure/templates/email-template-master.html"
    )


def html_to_plain_text(html: str) -> str:
    """
    Convert HTML content to plain text for clipboard.

    Preserves:
    - Paragraph breaks (double newline)
    - Line breaks (single newline)
    - Lists (bullet points)
    - Tables (ASCII format)
    - Headings (with emphasis)
    """
    text = html

    # Remove script and style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert headings to emphasized text
    text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n\n\1\n\n', text, flags=re.DOTALL)

    # Convert paragraphs to double newlines
    text = re.sub(r'</p>\s*<p[^>]*>', '\n\n', text)
    text = re.sub(r'</?p[^>]*>', '', text)

    # Convert line breaks
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Convert lists
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1\n', text, flags=re.DOTALL)
    text = re.sub(r'</?[uo]l[^>]*>', '', text)

    # Convert tables (simple ASCII representation)
    text = re.sub(r'</tr>\s*<tr[^>]*>', '\n', text)
    text = re.sub(r'</t[dh]>\s*<t[dh][^>]*>', ' | ', text)
    text = re.sub(r'</?t(?:able|head|body|r|h|d)[^>]*>', '', text)

    # Convert strong/bold to uppercase (optional - can remove if too aggressive)
    # text = re.sub(r'<strong[^>]*>(.*?)</strong>', lambda m: m.group(1).upper(), text, flags=re.DOTALL)

    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&pound;', '£')

    # Clean up whitespace
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\n ', '\n', text)  # Remove leading spaces on lines
    text = re.sub(r' \n', '\n', text)  # Remove trailing spaces on lines
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines

    return text.strip()


def embed_chart(
    chart_path: str,
    alt_text: str,
    caption: Optional[str] = None,
    max_width: str = "100%"
) -> str:
    """
    Generate HTML for embedding a chart image in email.

    Args:
        chart_path: Path to chart image file (relative to email HTML location)
        alt_text: Alt text for image
        caption: Optional caption below chart
        max_width: Maximum width (default: "100%")

    Returns:
        HTML string for chart embedding

    Example:
        chart_html = embed_chart(
            chart_path="2025-12-16-roas-trend.png",
            alt_text="ROAS Trend - Last 7 Days",
            caption="ROAS trending upward, driven by Performance Max improvements"
        )
    """
    html = f'<div class="chart-container" style="margin: 20px 0;">\n'
    html += f'    <img src="{chart_path}" alt="{alt_text}" '
    html += f'style="max-width: {max_width}; height: auto; border: 1px solid #ddd; border-radius: 4px;">\n'

    if caption:
        html += f'    <p style="margin: 5px 0 0 0; font-size: 12px; color: #6c757d; font-style: italic;">{caption}</p>\n'

    html += '</div>\n'

    return html


def render_email(
    content: str,
    recipient_name: str = "[Name]",
    sender_name: str = "Peter",
    sign_off: str = "Regards",
    contact_details: Optional[str] = None
) -> str:
    """
    Render an email using the canonical template.

    Args:
        content: HTML content of the email body (paragraphs, lists, tables, etc.)
        recipient_name: Name to use in greeting ("Hi {name},")
        sender_name: Name to use in signature
        sign_off: Sign-off phrase (Regards, Best, etc.)
        contact_details: Optional contact info (defaults to Peter's standard details)

    Returns:
        Complete HTML email ready to display in browser with copy button

    Example:
        html = render_email(
            content='''
                <p>Quick update on last week's performance:</p>
                <ul>
                    <li>Revenue: £3,500</li>
                    <li>ROAS: 320%</li>
                </ul>
                <p>All looking good.</p>
            ''',
            recipient_name="Barry",
            sign_off="Best"
        )
    """
    # Load template
    template_path = get_template_path()
    with open(template_path, 'r') as f:
        template = f.read()

    # Default contact details
    if contact_details is None:
        contact_details = (
            "e: petere@roksys.co.uk<br>\n"
            "            t: 07932 454652"
        )

    # Generate plain text version for clipboard
    # Build complete plain text email
    plain_text_parts = [
        f"Hi {recipient_name},",
        "",
        html_to_plain_text(content),
        "",
        f"{sign_off},",
        sender_name,
        "",
        html_to_plain_text(contact_details)
    ]
    plain_text = "\n".join(plain_text_parts)

    # Escape plain text for JavaScript (using JSON encoding for safety)
    plain_text_js = json.dumps(plain_text)

    # Replace placeholders
    html = template.replace('{{RECIPIENT_NAME}}', recipient_name)
    html = html.replace('{{CONTENT}}', content)
    html = html.replace('{{SENDER_NAME}}', sender_name)
    html = html.replace('{{SIGN_OFF}}', sign_off)
    html = html.replace('{{CONTACT_DETAILS}}', contact_details)
    html = html.replace('{{PLAIN_TEXT}}', plain_text_js)

    return html


def save_email_draft(
    html: str,
    filepath: str,
    open_in_browser: bool = True
) -> Path:
    """
    Save email draft to file and optionally open in browser.

    Args:
        html: Rendered HTML from render_email()
        filepath: Path to save the HTML file
        open_in_browser: Whether to automatically open in default browser

    Returns:
        Path object of the saved file
    """
    import subprocess

    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(html)

    if open_in_browser:
        subprocess.run(['open', str(output_path)])

    return output_path


def render_performance_email_with_charts(
    recipient_name: str,
    client: str,
    week_range: str,
    key_metrics: Dict,
    charts: Dict[str, str],
    insights: List[str],
    recommendations: Optional[List[str]] = None,
    sender_name: str = "Peter",
    sign_off: str = "Regards"
) -> str:
    """
    Render performance update email with embedded charts.

    Pre-formatted template for weekly Google Ads performance emails.

    Args:
        recipient_name: Recipient's name
        client: Client name
        week_range: Week date range (e.g., "9-15 December 2025")
        key_metrics: Dict of metrics {'spend': '£2,450', 'roas': '420%', ...}
        charts: Dict of chart filenames {'roas_trend': '2025-12-16-roas-trend.png', ...}
        insights: List of insight strings (bullets)
        recommendations: Optional list of recommendations
        sender_name: Sender name
        sign_off: Sign-off phrase

    Returns:
        Complete HTML email with charts

    Example:
        email = render_performance_email_with_charts(
            recipient_name="Barry",
            client="Bright Minds",
            week_range="9-15 December 2025",
            key_metrics={
                'spend': '£2,450',
                'roas': '420%',
                'conversions': '65',
                'spend_change': '+12%',
                'roas_change': '+30pp'
            },
            charts={
                'roas_trend': '2025-12-16-roas-trend.png',
                'campaigns_spend': '2025-12-16-campaigns-spend.png'
            },
            insights=[
                'ROAS improving steadily, up 30pp week-over-week',
                'Performance Max driving 60% of revenue',
                'Search campaign efficiency improved by 15%'
            ],
            recommendations=[
                'Increase Performance Max budget by £200/week',
                'Test new product headlines in Search ads'
            ]
        )
    """
    # Build content
    content = f'<h2 style="color: #059669;">Weekly Performance Update - {week_range}</h2>\n\n'

    # Key Metrics Table
    content += '<h3 style="color: #047857;">Key Metrics</h3>\n'
    content += '<table style="width: 100%; border-collapse: collapse; margin: 15px 0;">\n'
    content += '  <tr style="background-color: #f8f9fa;">\n'
    content += '    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Metric</th>\n'
    content += '    <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Value</th>\n'
    content += '    <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Change</th>\n'
    content += '  </tr>\n'

    metrics_rows = [
        ('Spend', key_metrics.get('spend', '—'), key_metrics.get('spend_change', '—')),
        ('ROAS', key_metrics.get('roas', '—'), key_metrics.get('roas_change', '—')),
        ('Conversions', key_metrics.get('conversions', '—'), key_metrics.get('conv_change', '—')),
    ]

    for metric, value, change in metrics_rows:
        # Color code change
        change_color = '#10B981' if '+' in change else '#dc3545' if '-' in change else '#6c757d'
        content += f'  <tr>\n'
        content += f'    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{metric}</td>\n'
        content += f'    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;"><strong>{value}</strong></td>\n'
        content += f'    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd; color: {change_color}; font-weight: bold;">{change}</td>\n'
        content += '  </tr>\n'

    content += '</table>\n\n'

    # Charts
    content += '<h3 style="color: #047857;">Performance Charts</h3>\n'

    if 'roas_trend' in charts:
        content += embed_chart(
            chart_path=charts['roas_trend'],
            alt_text="ROAS Trend",
            caption="ROAS performance over the last 7 days"
        )

    if 'campaigns_spend' in charts:
        content += embed_chart(
            chart_path=charts['campaigns_spend'],
            alt_text="Top Campaigns by Spend",
            caption="Budget allocation across top-performing campaigns"
        )

    if 'top_products' in charts:
        content += embed_chart(
            chart_path=charts['top_products'],
            alt_text="Top Products by Revenue",
            caption="Highest revenue-generating products"
        )

    # Insights
    content += '<h3 style="color: #047857;">Key Insights</h3>\n'
    content += '<ul style="line-height: 1.8;">\n'
    for insight in insights:
        content += f'  <li>{insight}</li>\n'
    content += '</ul>\n\n'

    # Recommendations (if provided)
    if recommendations:
        content += '<h3 style="color: #047857;">Recommendations</h3>\n'
        content += '<ol style="line-height: 1.8;">\n'
        for rec in recommendations:
            content += f'  <li>{rec}</li>\n'
        content += '</ol>\n\n'

    content += '<p>Let me know if you have any questions or would like to discuss any of these points.</p>\n'

    # Render using standard template
    return render_email(
        content=content,
        recipient_name=recipient_name,
        sender_name=sender_name,
        sign_off=sign_off
    )


# Example usage
if __name__ == "__main__":
    # Test the module
    test_content = """
        <p>Quick update on last week's performance:</p>

        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Revenue</td>
                <td>£3,500</td>
            </tr>
            <tr>
                <td>ROAS</td>
                <td>320%</td>
            </tr>
        </table>

        <p>All looking good.</p>
    """

    html = render_email(
        content=test_content,
        recipient_name="Barry",
        sign_off="Best"
    )

    # Save and open
    save_email_draft(html, "/tmp/test-email.html")
    print("✓ Test email created and opened in browser")
