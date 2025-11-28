#!/usr/bin/env python3
"""
Pre-Call Performance Summary
Quick Google Ads performance snapshot for client calls

Shows:
- Last 7 days performance
- Comparison vs previous 7 days (WoW)
- Comparison vs same period last year (YoY)
- Key successes and failures

Usage:
    python tools/pre-call-performance-summary.py [client-slug]
    python tools/pre-call-performance-summary.py accessories-for-the-home
"""

import os
import sys
import json
import re
import csv
import webbrowser
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent

# Try to load dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    # Try loading from project root first
    load_dotenv(PROJECT_ROOT / '.env')
    # Also try loading from MCP server directory
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env')
except ImportError:
    pass

sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'))
sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / 'lib'))

from oauth.google_auth import execute_gaql

# Load client configuration
CLIENTS_FILE = PROJECT_ROOT / 'shared' / 'data' / 'google-ads-clients.json'


def get_client_product_issues(client_name, days=7):
    """Get recent product issues (price changes, disapprovals) for a client"""
    issues = {
        'price_changes': [],
        'disapprovals': []
    }
    
    # Map client display names to product analyzer folder names
    client_folder_map = {
        'Accessories for the Home': 'Accessories for the Home',
        'BrightMinds': 'BrightMinds',
        'Clear Prospects': 'BMPM',  # BMPM is Clear Prospects
        'Crowd Control': 'Crowd Control',
        'Devonshire Group': None,  # Not tracked in product analyzer
        'Go Glean': 'Go Glean UK',
        'Godshot': 'Godshot',
        'Grain Guard': 'Grain Guard',
        'Just Bin Bags': 'Just Bin Bags',
        'National Design Academy (NDA)': None,  # Not tracked
        'Positive Bakes': None,  # Not tracked
        'Smythson UK': 'Smythson UK',
        'Superspace': 'Superspace',
        'Tree2mydoor': 'Tree2mydoor',
        'Uno Lights': 'Uno Lights'
    }
    
    folder_name = client_folder_map.get(client_name)
    if not folder_name:
        return issues
    
    # Get recent product changes
    changes_dir = PROJECT_ROOT / 'tools' / 'product-impact-analyzer' / 'data' / 'product_changes' / folder_name
    if changes_dir.exists():
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get most recent change file
        change_files = sorted(changes_dir.glob('*.json'), reverse=True)
        for change_file in change_files[:3]:  # Check last 3 days
            try:
                file_date_str = change_file.stem.split()[0]  # Get date part
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                
                if file_date >= cutoff_date:
                    with open(change_file, 'r', encoding='utf-8') as f:
                        change_data = json.load(f)
                    
                    # Extract significant price changes
                    price_changes = change_data.get('price_changes', [])
                    for pc in price_changes[:5]:  # Limit to 5 most significant
                        if 'title' in pc and 'changes' in pc and 'price' in pc['changes']:
                            old_price = pc['changes']['price'][0] if len(pc['changes']['price']) > 0 else 'N/A'
                            new_price = pc['changes']['price'][1] if len(pc['changes']['price']) > 1 else 'N/A'
                            
                            # Calculate percentage change
                            try:
                                old_val = float(old_price.split()[0]) if old_price != 'N/A' else 0
                                new_val = float(new_price.split()[0]) if new_price != 'N/A' else 0
                                if old_val > 0:
                                    pct_change = ((new_val - old_val) / old_val) * 100
                                    if abs(pct_change) > 5:  # Only significant changes (>5%)
                                        issues['price_changes'].append({
                                            'date': file_date_str,
                                            'product_id': pc.get('product_id', ''),
                                            'title': pc.get('title', 'Unknown'),
                                            'old_price': old_price,
                                            'new_price': new_price,
                                            'change_pct': round(pct_change, 1)
                                        })
                            except (ValueError, IndexError):
                                pass
            except (json.JSONDecodeError, ValueError, KeyError):
                continue
    
    # Get current disapprovals
    monitor_dir = PROJECT_ROOT / 'tools' / 'product-impact-analyzer' / 'data'
    disapprovals_file = monitor_dir / 'disapprovals_current.json'
    
    if disapprovals_file.exists():
        try:
            with open(disapprovals_file, 'r', encoding='utf-8') as f:
                disapproval_data = json.load(f)
            
            # Find client in disapproval data
            clients_data = disapproval_data.get('clients', {})
            for client_key, products in clients_data.items():
                # Match client name (flexible matching)
                if client_name.lower() in client_key.lower() or client_key.lower() in client_name.lower():
                    for product in products[:10]:  # Limit to 10 most recent
                        if product.get('status') == 'disapproved':
                            issues['disapprovals'].append({
                                'product_id': product.get('product_id', '').split(':')[-1] if ':' in str(product.get('product_id', '')) else str(product.get('product_id', '')),
                                'title': product.get('title', 'Unknown'),
                                'issues': [issue.get('description', 'Unknown issue') for issue in product.get('item_level_issues', [])[:2]]
                            })
                    break
        except (json.JSONDecodeError, KeyError, AttributeError):
            pass
    
    return issues


def get_client_experiments(client_name, days=30):
    """Get recent experiments for a specific client"""
    experiments_file = PROJECT_ROOT / "roksys/spreadsheets/rok-experiments-client-notes.csv"
    
    if not experiments_file.exists():
        return []
    
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        client_experiments = []
        
        with open(experiments_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if this experiment is for the client
                row_client = row.get('Client', '')
                if not row_client or not isinstance(row_client, str):
                    continue
                row_client = row_client.strip()
                if not row_client or row_client.lower() != client_name.lower():
                    continue
                
                timestamp_str = row.get('Timestamp', '').strip()
                if not timestamp_str:
                    continue
                
                # Parse date
                try:
                    if '/' in timestamp_str:
                        date_part = timestamp_str.split()[0]
                        exp_date = datetime.strptime(date_part, '%d/%m/%Y')
                    else:
                        date_part = timestamp_str.split()[0]
                        exp_date = datetime.strptime(date_part, '%Y-%m-%d')
                    
                    # Include experiments from the last N days
                    if exp_date >= cutoff_date:
                        note = row.get('Note', '').strip()
                        tags = row.get('Tags (optional)', '').strip()
                        
                        # Extract review date from note if present
                        review_date = None
                        if 'REVIEW:' in note or 'WHEN:' in note:
                            import re as regex_module
                            review_match = regex_module.search(r'(?:REVIEW|WHEN):\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{4})', note)
                            if review_match:
                                review_date_str = review_match.group(1)
                                try:
                                    # Try parsing different date formats
                                    for fmt in ['%B %d, %Y', '%b %d, %Y', '%d/%m/%Y', '%d-%m-%Y']:
                                        try:
                                            review_date = datetime.strptime(review_date_str, fmt)
                                            break
                                        except ValueError:
                                            continue
                                except:
                                    pass
                        
                        client_experiments.append({
                            'date': exp_date,
                            'date_str': timestamp_str,
                            'note': note,
                            'tags': tags,
                            'review_date': review_date
                        })
                except ValueError:
                    continue
        
        # Sort by date (most recent first)
        client_experiments.sort(key=lambda x: x['date'], reverse=True)
        return client_experiments[:5]  # Limit to 5 most recent
        
    except Exception as e:
        print(f"Warning: Could not read experiments: {e}", file=sys.stderr)
        return []


def format_currency(value):
    """Format currency value"""
    return f"£{value:,.2f}"


def format_percent(value):
    """Format percentage"""
    return f"{value:.1f}%"


def format_change(current, previous):
    """Format change percentage with emoji"""
    if previous == 0:
        return "N/A"
    change_pct = ((current - previous) / previous) * 100
    emoji = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "→"
    return f"{emoji} {abs(change_pct):.1f}%"


def fetch_performance(customer_id, start_date, end_date, manager_id=None):
    """Fetch account-level performance data"""
    query = f"""
    SELECT
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM customer
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """
    
    try:
        result = execute_gaql(customer_id, query, manager_id or "")
        
        if not result.get('results'):
            return {'error': 'No data available'}
        
        totals = {
            'impressions': 0,
            'clicks': 0,
            'cost_micros': 0,
            'conversions': 0,
            'conversions_value': 0
        }
        
        for row in result.get('results', []):
            metrics = row.get('metrics', {})
            totals['impressions'] += int(metrics.get('impressions', 0))
            totals['clicks'] += int(metrics.get('clicks', 0))
            totals['cost_micros'] += int(metrics.get('costMicros', 0))
            totals['conversions'] += float(metrics.get('conversions', 0))
            totals['conversions_value'] += float(metrics.get('conversionsValue', 0))
        
        # Check if we have any meaningful data
        if totals['cost_micros'] == 0:
            return {'error': 'No spend data'}
        
        cost = totals['cost_micros'] / 1_000_000
        revenue = totals['conversions_value']
        roas = (revenue / cost * 100) if cost > 0 else 0
        ctr = (totals['clicks'] / totals['impressions'] * 100) if totals['impressions'] > 0 else 0
        cpc = (cost / totals['clicks']) if totals['clicks'] > 0 else 0
        cpa = (cost / totals['conversions']) if totals['conversions'] > 0 else 0
        cvr = (totals['conversions'] / totals['clicks'] * 100) if totals['clicks'] > 0 else 0
        
        return {
            'impressions': totals['impressions'],
            'clicks': totals['clicks'],
            'cost': round(cost, 2),
            'conversions': round(totals['conversions'], 1),
            'revenue': round(revenue, 2),
            'roas': round(roas, 1),
            'ctr': round(ctr, 2),
            'cpc': round(cpc, 2),
            'cpa': round(cpa, 2),
            'cvr': round(cvr, 2)
        }
    except Exception as e:
        return {'error': str(e)}


def analyze_changes(current, previous, period_name):
    """Analyze changes and identify successes/failures"""
    if 'error' in current or 'error' in previous:
        return []
    
    insights = []
    
    # Revenue changes
    rev_change = ((current['revenue'] - previous['revenue']) / previous['revenue'] * 100) if previous['revenue'] > 0 else 0
    if abs(rev_change) > 10:
        insights.append({
            'type': 'success' if rev_change > 0 else 'failure',
            'metric': 'Revenue',
            'change': f"{'+' if rev_change > 0 else ''}{rev_change:.1f}%",
            'current': format_currency(current['revenue']),
            'previous': format_currency(previous['revenue']),
            'period': period_name
        })
    
    # ROAS changes
    roas_change = current['roas'] - previous['roas']
    if abs(roas_change) > 10:
        insights.append({
            'type': 'success' if roas_change > 0 else 'failure',
            'metric': 'ROAS',
            'change': f"{'+' if roas_change > 0 else ''}{roas_change:.1f}pp",
            'current': f"{current['roas']:.1f}%",
            'previous': f"{previous['roas']:.1f}%",
            'period': period_name
        })
    
    # Conversion changes
    conv_change = ((current['conversions'] - previous['conversions']) / previous['conversions'] * 100) if previous['conversions'] > 0 else 0
    if abs(conv_change) > 15:
        insights.append({
            'type': 'success' if conv_change > 0 else 'failure',
            'metric': 'Conversions',
            'change': f"{'+' if conv_change > 0 else ''}{conv_change:.1f}%",
            'current': f"{current['conversions']:.1f}",
            'previous': f"{previous['conversions']:.1f}",
            'period': period_name
        })
    
    # Cost efficiency (CPA)
    cpa_change = ((current['cpa'] - previous['cpa']) / previous['cpa'] * 100) if previous['cpa'] > 0 else 0
    if abs(cpa_change) > 15:
        insights.append({
            'type': 'success' if cpa_change < 0 else 'failure',  # Lower CPA is better
            'metric': 'CPA',
            'change': f"{'+' if cpa_change > 0 else ''}{cpa_change:.1f}%",
            'current': format_currency(current['cpa']),
            'previous': format_currency(previous['cpa']),
            'period': period_name
        })
    
    return insights


def generate_html_report(client_name, current, prev_week, prev_year, experiments=None, product_issues=None):
    """Generate HTML report"""
    # Account for Google Ads reporting delays - use 2 days ago as end date
    end_date = datetime.now() - timedelta(days=2)
    start_date = end_date - timedelta(days=6)  # 7 days total (including end_date)
    
    # Calculate changes
    all_insights = []
    if 'error' not in prev_week and prev_week.get('cost', 0) > 0:
        all_insights.extend(analyze_changes(current, prev_week, "WoW"))
    if 'error' not in prev_year and prev_year.get('cost', 0) > 0:
        all_insights.extend(analyze_changes(current, prev_year, "YoY"))
    
    successes = [i for i in all_insights if i['type'] == 'success']
    failures = [i for i in all_insights if i['type'] == 'failure']
    
    # Get experiments for this client if not provided
    if experiments is None:
        experiments = get_client_experiments(client_name, days=30)
    
    # Get product issues if not provided
    if product_issues is None:
        product_issues = get_client_product_issues(client_name, days=7)
    
    # Generate change HTML
    def format_change_html(current_val, prev_val, metric_name):
        if prev_val == 0:
            return '<span class="change-na">N/A</span>'
        change_pct = ((current_val - prev_val) / prev_val) * 100
        emoji = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "→"
        color_class = "change-up" if change_pct > 0 else "change-down" if change_pct < 0 else "change-neutral"
        return f'<span class="{color_class}">{emoji} {abs(change_pct):.1f}%</span>'
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pre-Call Summary: {client_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .date {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
        }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        .comparison-table th {{
            text-align: left;
            padding: 12px;
            background: #ecf0f1;
            font-weight: 600;
            color: #2c3e50;
            font-size: 13px;
        }}
        .comparison-table td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .comparison-table tr:hover {{
            background: #f8f9fa;
        }}
        .change-up {{
            color: #27ae60;
            font-weight: 600;
        }}
        .change-down {{
            color: #e74c3c;
            font-weight: 600;
        }}
        .change-neutral {{
            color: #7f8c8d;
        }}
        .change-na {{
            color: #bdc3c7;
            font-style: italic;
        }}
        .insights {{
            display: grid;
            gap: 15px;
        }}
        .insight-card {{
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        .insight-success {{
            background: #d5f4e6;
            border-color: #27ae60;
        }}
        .insight-failure {{
            background: #fde8e8;
            border-color: #e74c3c;
        }}
        .insight-metric {{
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 5px;
        }}
        .insight-details {{
            font-size: 14px;
            color: #555;
        }}
        .no-data {{
            color: #95a5a6;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
        .stable {{
            background: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: #3498db;
        }}
        .experiment-card {{
            background: #fff9e6;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f39c12;
            margin-bottom: 15px;
        }}
        .experiment-date {{
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 8px;
        }}
        .experiment-note {{
            font-size: 14px;
            color: #2c3e50;
            line-height: 1.5;
        }}
        .experiment-review {{
            margin-top: 8px;
            font-size: 12px;
            color: #e67e22;
            font-weight: 600;
        }}
        .product-issue-card {{
            background: #fff5f5;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            margin-bottom: 15px;
        }}
        .product-issue-title {{
            font-weight: 600;
            font-size: 14px;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .product-issue-details {{
            font-size: 13px;
            color: #555;
            margin-top: 5px;
        }}
        .price-change {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 12px;
        }}
        .price-up {{
            background: #fee;
            color: #c0392b;
        }}
        .price-down {{
            background: #efe;
            color: #27ae60;
        }}
        .footer {{
            background: #ecf0f1;
            padding: 20px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📞 Pre-Call Performance Summary</h1>
            <div class="date">{client_name} • {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}</div>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">📊 Last 7 Days Performance</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Revenue</div>
                        <div class="metric-value">{format_currency(current['revenue'])}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Spend</div>
                        <div class="metric-value">{format_currency(current['cost'])}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">ROAS</div>
                        <div class="metric-value">{current['roas']:.1f}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Conversions</div>
                        <div class="metric-value">{current['conversions']:.1f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CPA</div>
                        <div class="metric-value">{format_currency(current['cpa'])}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CVR</div>
                        <div class="metric-value">{current['cvr']:.1f}%</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">📈 Week-over-Week Comparison</div>
"""
    
    if 'error' not in prev_week and prev_week.get('cost', 0) > 0:
        html += f"""
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Current</th>
                            <th>Previous</th>
                            <th>Change</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Revenue</td>
                            <td>{format_currency(current['revenue'])}</td>
                            <td>{format_currency(prev_week['revenue'])}</td>
                            <td>{format_change_html(current['revenue'], prev_week['revenue'], 'Revenue')}</td>
                        </tr>
                        <tr>
                            <td>ROAS</td>
                            <td>{current['roas']:.1f}%</td>
                            <td>{prev_week['roas']:.1f}%</td>
                            <td>{format_change_html(current['roas'], prev_week['roas'], 'ROAS')}</td>
                        </tr>
                        <tr>
                            <td>Conversions</td>
                            <td>{current['conversions']:.1f}</td>
                            <td>{prev_week['conversions']:.1f}</td>
                            <td>{format_change_html(current['conversions'], prev_week['conversions'], 'Conversions')}</td>
                        </tr>
                        <tr>
                            <td>CPA</td>
                            <td>{format_currency(current['cpa'])}</td>
                            <td>{format_currency(prev_week['cpa'])}</td>
                            <td>{format_change_html(current['cpa'], prev_week['cpa'], 'CPA')}</td>
                        </tr>
                    </tbody>
                </table>
"""
    else:
        html += '<div class="no-data">No data available for previous 7 days</div>'
    
    html += """
            </div>
            
            <div class="section">
                <div class="section-title">📅 Year-over-Year Comparison</div>
"""
    
    if 'error' not in prev_year and prev_year.get('cost', 0) > 0:
        html += f"""
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Current</th>
                            <th>Last Year</th>
                            <th>Change</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Revenue</td>
                            <td>{format_currency(current['revenue'])}</td>
                            <td>{format_currency(prev_year['revenue'])}</td>
                            <td>{format_change_html(current['revenue'], prev_year['revenue'], 'Revenue')}</td>
                        </tr>
                        <tr>
                            <td>ROAS</td>
                            <td>{current['roas']:.1f}%</td>
                            <td>{prev_year['roas']:.1f}%</td>
                            <td>{format_change_html(current['roas'], prev_year['roas'], 'ROAS')}</td>
                        </tr>
                        <tr>
                            <td>Conversions</td>
                            <td>{current['conversions']:.1f}</td>
                            <td>{prev_year['conversions']:.1f}</td>
                            <td>{format_change_html(current['conversions'], prev_year['conversions'], 'Conversions')}</td>
                        </tr>
                        <tr>
                            <td>CPA</td>
                            <td>{format_currency(current['cpa'])}</td>
                            <td>{format_currency(prev_year['cpa'])}</td>
                            <td>{format_change_html(current['cpa'], prev_year['cpa'], 'CPA')}</td>
                        </tr>
                    </tbody>
                </table>
"""
    else:
        html += '<div class="no-data">No data available for same period last year</div>'
    
    html += """
            </div>
            
            <div class="section">
                <div class="section-title">🔍 Key Insights</div>
"""
    
    if all_insights:
        if successes:
            html += '<div class="insights">'
            for insight in successes[:3]:
                html += f"""
                    <div class="insight-card insight-success">
                        <div class="insight-metric">✅ {insight['metric']} {insight['change']} ({insight['period']})</div>
                        <div class="insight-details">{insight['current']} vs {insight['previous']}</div>
                    </div>
"""
            html += '</div>'
        
        if failures:
            html += '<div class="insights">'
            for insight in failures[:3]:
                html += f"""
                    <div class="insight-card insight-failure">
                        <div class="insight-metric">⚠️ {insight['metric']} {insight['change']} ({insight['period']})</div>
                        <div class="insight-details">{insight['current']} vs {insight['previous']}</div>
                    </div>
"""
            html += '</div>'
    else:
        html += '<div class="stable">ℹ️ Performance stable - no significant changes detected</div>'
    
    html += """
            </div>
            
            <div class="section">
                <div class="section-title">🧪 Recent Experiments & Tests</div>
"""
    
    if experiments:
        html += '<div class="insights">'
        for exp in experiments[:5]:  # Show up to 5 most recent
            # Format note - extract key parts
            note = exp['note']
            review_info = ""
            if exp.get('review_date'):
                days_until = (exp['review_date'] - datetime.now()).days
                if days_until >= 0:
                    review_info = f'<div class="experiment-review">📅 Review due in {days_until} days ({exp["review_date"].strftime("%b %d")})</div>'
                else:
                    review_info = f'<div class="experiment-review">⚠️ Review overdue ({abs(days_until)} days past due)</div>'
            
            # Truncate long notes
            display_note = note
            if len(display_note) > 300:
                display_note = display_note[:300] + "..."
            
            html += f"""
                    <div class="experiment-card">
                        <div class="experiment-date">{exp['date_str']}</div>
                        <div class="experiment-note">{display_note.replace(chr(10), '<br>')}</div>
                        {review_info}
                    </div>
"""
        html += '</div>'
    else:
        html += '<div class="no-data">No recent experiments logged</div>'
    
    html += """
            </div>
            
            <div class="section">
                <div class="section-title">📦 Product Issues & Changes</div>
"""
    
    has_product_issues = False
    
    # Price changes
    if product_issues and product_issues.get('price_changes'):
        has_product_issues = True
        html += '<h3 style="font-size: 16px; margin: 20px 0 10px 0; color: #2c3e50;">💰 Significant Price Changes (Last 7 Days)</h3>'
        html += '<div class="insights">'
        for pc in product_issues['price_changes'][:5]:
            change_class = "price-up" if pc['change_pct'] > 0 else "price-down"
            change_emoji = "↑" if pc['change_pct'] > 0 else "↓"
            html += f"""
                    <div class="product-issue-card">
                        <div class="product-issue-title">{pc['title']}</div>
                        <div class="product-issue-details">
                            <span class="price-change {change_class}">{change_emoji} {abs(pc['change_pct']):.1f}%</span>
                            &nbsp;{pc['old_price']} → {pc['new_price']} ({pc['date']})
                        </div>
                    </div>
"""
        html += '</div>'
    
    # Disapprovals
    if product_issues and product_issues.get('disapprovals'):
        has_product_issues = True
        html += '<h3 style="font-size: 16px; margin: 20px 0 10px 0; color: #e74c3c;">🚫 Product Disapprovals</h3>'
        html += '<div class="insights">'
        for disp in product_issues['disapprovals'][:5]:
            issues_list = ', '.join(disp['issues']) if disp['issues'] else 'Disapproved'
            html += f"""
                    <div class="product-issue-card">
                        <div class="product-issue-title">{disp['title']}</div>
                        <div class="product-issue-details">
                            Issue: {issues_list}
                            {f" (ID: {disp['product_id']})" if disp.get('product_id') else ""}
                        </div>
                    </div>
"""
        html += '</div>'
    
    if not has_product_issues:
        html += '<div class="no-data">No significant product issues detected</div>'
    
    html += f"""
            </div>
        </div>
        
        <div class="footer">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Pre-Call Performance Summary Tool
        </div>
    </div>
</body>
</html>
"""
    
    return html


def print_summary(client_name, current, prev_week, prev_year):
    """Print formatted summary to console"""
    print(f"\n{'='*70}")
    print(f"📞 PRE-CALL PERFORMANCE SUMMARY: {client_name}")
    print(f"{'='*70}\n")
    
    # Current period - account for Google Ads reporting delays (use 2 days ago as end date)
    end_date = datetime.now() - timedelta(days=2)
    start_date = end_date - timedelta(days=6)  # 7 days total (including end_date)
    print(f"📊 LAST 7 DAYS ({start_date.strftime('%b %d')} - {end_date.strftime('%b %d')})")
    print(f"   Revenue:  {format_currency(current['revenue'])}")
    print(f"   Spend:    {format_currency(current['cost'])}")
    print(f"   ROAS:     {current['roas']:.1f}%")
    print(f"   Conv:     {current['conversions']:.1f}")
    print(f"   CPA:      {format_currency(current['cpa'])}")
    print(f"   CVR:      {current['cvr']:.1f}%")
    print()
    
    # Week-over-week comparison
    if 'error' not in prev_week and prev_week.get('cost', 0) > 0:
        print(f"📈 VS PREVIOUS 7 DAYS (Week-over-Week)")
        print(f"   Revenue:  {format_change(current['revenue'], prev_week['revenue'])}")
        print(f"   ROAS:     {format_change(current['roas'], prev_week['roas'])}")
        print(f"   Conv:     {format_change(current['conversions'], prev_week['conversions'])}")
        print(f"   CPA:      {format_change(current['cpa'], prev_week['cpa'])}")
        print()
    elif 'error' in prev_week:
        print(f"📈 VS PREVIOUS 7 DAYS: No data available\n")
    
    # Year-over-year comparison
    if 'error' not in prev_year and prev_year.get('cost', 0) > 0:
        print(f"📅 VS SAME PERIOD LAST YEAR (Year-over-Year)")
        print(f"   Revenue:  {format_change(current['revenue'], prev_year['revenue'])}")
        print(f"   ROAS:     {format_change(current['roas'], prev_year['roas'])}")
        print(f"   Conv:     {format_change(current['conversions'], prev_year['conversions'])}")
        print(f"   CPA:      {format_change(current['cpa'], prev_year['cpa'])}")
        print()
    elif 'error' in prev_year:
        print(f"📅 VS SAME PERIOD LAST YEAR: No data available\n")
    
    # Key insights
    all_insights = []
    if 'error' not in prev_week and prev_week.get('cost', 0) > 0:
        all_insights.extend(analyze_changes(current, prev_week, "WoW"))
    if 'error' not in prev_year and prev_year.get('cost', 0) > 0:
        all_insights.extend(analyze_changes(current, prev_year, "YoY"))
    
    if all_insights:
        successes = [i for i in all_insights if i['type'] == 'success']
        failures = [i for i in all_insights if i['type'] == 'failure']
        
        if successes:
            print(f"✅ KEY SUCCESSES")
            for insight in successes[:3]:
                print(f"   • {insight['metric']} {insight['change']} ({insight['period']}): "
                      f"{insight['current']} vs {insight['previous']}")
            print()
        
        if failures:
            print(f"⚠️  KEY CONCERNS")
            for insight in failures[:3]:
                print(f"   • {insight['metric']} {insight['change']} ({insight['period']}): "
                      f"{insight['current']} vs {insight['previous']}")
            print()
    else:
        print("ℹ️  Performance stable - no significant changes detected\n")
    
    print(f"{'='*70}\n")


def main():
    """Main function"""
    # Load clients
    if not CLIENTS_FILE.exists():
        print(f"❌ Error: Clients file not found: {CLIENTS_FILE}")
        sys.exit(1)
    
    with open(CLIENTS_FILE, 'r') as f:
        clients_data = json.load(f)
    
    clients = clients_data.get('clients', {})
    
    # Get client slug from args or show all
    if len(sys.argv) > 1:
        client_slug = sys.argv[1]
        if client_slug not in clients:
            print(f"❌ Error: Client '{client_slug}' not found")
            print(f"Available clients: {', '.join(clients.keys())}")
            sys.exit(1)
        selected_clients = {client_slug: clients[client_slug]}
    else:
        # Show all active clients
        selected_clients = {k: v for k, v in clients.items() if v.get('status') == 'active'}
    
    # Calculate date ranges - account for Google Ads reporting delays (use 2 days ago as end date)
    today = datetime.now()
    current_end = today - timedelta(days=2)  # End 2 days ago to account for reporting delays
    current_start = current_end - timedelta(days=6)  # 7 days total (including end_date)
    
    current_start_str = current_start.strftime('%Y-%m-%d')
    current_end_str = current_end.strftime('%Y-%m-%d')
    
    # Previous week - same 7-day period, 1 week earlier
    prev_week_end = current_end - timedelta(days=7)
    prev_week_start = prev_week_end - timedelta(days=6)
    
    prev_week_start_str = prev_week_start.strftime('%Y-%m-%d')
    prev_week_end_str = prev_week_end.strftime('%Y-%m-%d')
    
    # Previous year - same date range, 1 year earlier
    prev_year_end = current_end - timedelta(days=365)
    prev_year_start = prev_year_end - timedelta(days=6)
    
    prev_year_start_str = prev_year_start.strftime('%Y-%m-%d')
    prev_year_end_str = prev_year_end.strftime('%Y-%m-%d')
    
    # Fetch and display for each client
    html_reports = []
    
    for slug, client_info in selected_clients.items():
        customer_id = client_info['customer_id']
        display_name = client_info['display_name']
        
        print(f"⏳ Fetching data for {display_name}...", end=' ', flush=True)
        
        # Get manager_id if available
        manager_id = client_info.get('manager_id')
        
        # Fetch all three periods
        current = fetch_performance(customer_id, current_start_str, current_end_str, manager_id)
        prev_week = fetch_performance(customer_id, prev_week_start_str, prev_week_end_str, manager_id)
        prev_year = fetch_performance(customer_id, prev_year_start_str, prev_year_end_str, manager_id)
        
        if 'error' in current:
            print(f"❌ Error: {current['error']}\n")
            continue
        
        print("✅")
        
        # Print summary to console
        print_summary(display_name, current, prev_week, prev_year)
        
        # Get experiments and product issues
        experiments = get_client_experiments(display_name, days=30)
        product_issues = get_client_product_issues(display_name, days=7)
        
        # Generate HTML report
        html_content = generate_html_report(display_name, current, prev_week, prev_year, experiments, product_issues)
        html_reports.append((display_name, html_content))
    
    # Save HTML file and open in browser
    if html_reports:
        # Create output directory
        output_dir = PROJECT_ROOT / 'tools' / 'pre-call-reports'
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        if len(html_reports) == 1:
            client_slug = list(selected_clients.keys())[0]
            filename = f"pre-call-{client_slug}-{timestamp}.html"
        else:
            filename = f"pre-call-all-clients-{timestamp}.html"
        
        output_file = output_dir / filename
        
        # Combine multiple reports if needed
        if len(html_reports) == 1:
            html_final = html_reports[0][1]
        else:
            # Combine multiple reports
            html_final = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pre-Call Summary: All Clients</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .report-section { background: white; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }
    </style>
</head>
<body>
    <div class="container">
"""
            for display_name, html_content in html_reports:
                # Extract body content from each report
                body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
                if body_match:
                    html_final += f'<div class="report-section">{body_match.group(1)}</div>'
            html_final += """
    </div>
</body>
</html>
"""
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_final)
        
        print(f"\n✅ HTML report generated: {output_file}")
        print("🌐 Opening in browser...")
        
        # Open in browser
        try:
            webbrowser.open(f'file://{output_file.absolute()}')
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please open manually: {output_file}")


if __name__ == '__main__':
    main()

