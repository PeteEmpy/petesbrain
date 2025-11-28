#!/usr/bin/env python3
"""
Just Bin Bags Group - ROAS Dashboard Generator

Fetches WooCommerce revenue from JBB and JHD stores, Google Ads cost,
calculates monthly ROAS, and displays an interactive graph in the browser.

Usage:
    python3 generate-roas-dashboard.py [--months 6]
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import subprocess
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# WooCommerce store configurations
STORES = {
    'justbinbags': {
        'name': 'Just Bin Bags',
        'mcp_server': 'woocommerce-justbinbags'
    },
    'justhealthdisposables': {
        'name': 'Just Health Disposables',
        'mcp_server': 'woocommerce-justhealthdisposables'
    }
}

# Google Ads configuration
GOOGLE_ADS_CUSTOMER_ID = '9697059148'


def get_month_range(year, month):
    """Get start and end dates for a given month"""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def fetch_woocommerce_revenue(store_key, start_date, end_date):
    """
    Fetch WooCommerce revenue for a store using the MCP server

    Returns total revenue for the date range
    """
    store = STORES[store_key]
    mcp_server = store['mcp_server']

    # Build the MCP command to fetch orders
    # Note: We'll need to use the claude mcp call command or call the MCP server directly
    # For now, return 0 as placeholder - will implement actual fetching

    print(f"  Fetching {store['name']} revenue from {start_date} to {end_date}...")

    # TODO: Implement actual WooCommerce API call via MCP
    # This will require either:
    # 1. Direct WooCommerce API calls using requests library
    # 2. Calling the MCP server via subprocess
    # 3. Using the WooCommerce Python library

    # Placeholder return
    return 0.0


def fetch_woocommerce_revenue_direct(store_key, start_date, end_date):
    """
    Fetch WooCommerce revenue directly using WooCommerce REST API

    Uses environment variables from MCP server configuration
    """
    import requests
    from requests.auth import HTTPBasicAuth

    store = STORES[store_key]

    # Get credentials from environment or MCP config
    # For now, we'll read from the claude mcp config
    mcp_config = get_mcp_config(store['mcp_server'])

    if not mcp_config:
        print(f"    WARNING: Could not load MCP config for {store['name']}")
        return 0.0

    url = mcp_config.get('WOOCOMMERCE_URL', '')
    consumer_key = mcp_config.get('WOOCOMMERCE_CONSUMER_KEY', '')
    consumer_secret = mcp_config.get('WOOCOMMERCE_CONSUMER_SECRET', '')

    if not all([url, consumer_key, consumer_secret]):
        print(f"    WARNING: Missing credentials for {store['name']}")
        return 0.0

    # Fetch orders
    api_url = f"{url}/wp-json/wc/v3/orders"
    params = {
        'after': f"{start_date}T00:00:00",
        'before': f"{end_date}T23:59:59",
        'status': 'completed',  # Only completed orders
        'per_page': 100
    }

    total_revenue = 0.0
    page = 1

    try:
        while True:
            params['page'] = page
            response = requests.get(
                api_url,
                params=params,
                auth=HTTPBasicAuth(consumer_key, consumer_secret),
                timeout=30
            )

            if response.status_code != 200:
                print(f"    WARNING: API request failed with status {response.status_code}")
                break

            orders = response.json()

            if not orders:
                break

            for order in orders:
                # Add order total to revenue
                total_revenue += float(order.get('total', 0))

            # Check if there are more pages
            if len(orders) < 100:
                break

            page += 1

        print(f"    ✓ Fetched £{total_revenue:.2f} from {len(orders) if orders else 0} completed orders")
        return total_revenue

    except Exception as e:
        print(f"    ERROR: Failed to fetch revenue: {e}")
        return 0.0


def get_mcp_config(server_name):
    """Get MCP server configuration from claude mcp get"""
    try:
        result = subprocess.run(
            ['claude', 'mcp', 'get', server_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return None

        # Parse the output to extract environment variables
        config = {}
        for line in result.stdout.split('\n'):
            line = line.strip()
            if '=' in line and not line.startswith('To remove'):
                # Lines like: WOOCOMMERCE_URL=https://...
                key, value = line.split('=', 1)
                config[key] = value

        return config

    except Exception as e:
        print(f"    ERROR: Failed to get MCP config: {e}")
        return None


def fetch_google_ads_cost(start_date, end_date):
    """
    Fetch Google Ads cost for the date range

    For now, this uses a cache file. To integrate with Google Ads API:
    1. Use mcp__google-ads__run_gaql tool
    2. Or manually update the cache file with monthly costs

    Returns total cost for the date range (in GBP)
    """
    print(f"  Fetching Google Ads cost from {start_date} to {end_date}...")

    # Check cache file first
    cache_file = Path(__file__).parent.parent / 'data' / 'google-ads-cost-cache.json'

    if cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text())
            month_key = f"{start_date[:7]}"  # YYYY-MM format

            if month_key in cache:
                cost = cache[month_key]
                print(f"    ✓ Loaded £{cost:.2f} from cache")
                return cost
        except Exception as e:
            print(f"    WARNING: Failed to load cache: {e}")

    # If not in cache, return 0 and warn
    print(f"    WARNING: No Google Ads cost data found for {start_date[:7]}")
    print(f"    To add cost data, create {cache_file}")
    print(f"    Format: {{'YYYY-MM': cost_in_gbp}}")

    return 0.0


def generate_monthly_data(months=12):
    """
    Generate monthly ROAS data for the specified number of months

    Returns list of monthly data points
    """
    data = []

    # Start from current month and go backwards
    current_date = datetime.now()

    for i in range(months):
        # Calculate month
        month_date = current_date - relativedelta(months=i)
        year = month_date.year
        month = month_date.month

        month_name = month_date.strftime('%B %Y')
        start_date, end_date = get_month_range(year, month)

        print(f"\nProcessing {month_name}...")

        # Fetch revenue from both stores
        jbb_revenue = fetch_woocommerce_revenue_direct('justbinbags', start_date, end_date)
        jhd_revenue = fetch_woocommerce_revenue_direct('justhealthdisposables', start_date, end_date)
        total_revenue = jbb_revenue + jhd_revenue

        # Fetch Google Ads cost
        ads_cost = fetch_google_ads_cost(start_date, end_date)

        # Calculate ROAS
        if ads_cost > 0:
            roas = total_revenue / ads_cost
        else:
            roas = 0.0

        data.append({
            'month': month_name,
            'year': year,
            'month_num': month,
            'jbb_revenue': jbb_revenue,
            'jhd_revenue': jhd_revenue,
            'total_revenue': total_revenue,
            'ads_cost': ads_cost,
            'roas': roas
        })

        print(f"  JBB Revenue: £{jbb_revenue:.2f}")
        print(f"  JHD Revenue: £{jhd_revenue:.2f}")
        print(f"  Total Revenue: £{total_revenue:.2f}")
        print(f"  Google Ads Cost: £{ads_cost:.2f}")
        print(f"  ROAS: {roas:.2f}x")

    # Reverse to show oldest first
    data.reverse()

    return data


def generate_html_dashboard(data, output_path):
    """Generate HTML dashboard with ROAS graph"""

    # Prepare data for Chart.js
    months = [d['month'] for d in data]
    roas_values = [d['roas'] for d in data]
    revenue_values = [d['total_revenue'] for d in data]
    cost_values = [d['ads_cost'] for d in data]

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Just Bin Bags Group - ROAS Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px;
            background: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        h1 {{
            color: #2c3e50;
            margin: 0 0 10px 0;
        }}
        .subtitle {{
            color: #7f8c8d;
            font-size: 16px;
        }}
        .dashboard {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        .stat-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-subvalue {{
            font-size: 14px;
            color: #95a5a6;
            margin-top: 5px;
        }}
        .chart-container {{
            position: relative;
            height: 400px;
            margin-bottom: 20px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .data-table th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .data-table tr:hover {{
            background: #f8f9fa;
        }}
        .positive {{
            color: #27ae60;
        }}
        .negative {{
            color: #e74c3c;
        }}
        .updated {{
            text-align: center;
            color: #95a5a6;
            font-size: 14px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Just Bin Bags Group - ROAS Dashboard</h1>
        <div class="subtitle">Combined performance: Just Bin Bags + Just Health Disposables</div>
    </div>

    <div class="dashboard">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Current Month ROAS</div>
                <div class="stat-value">{data[-1]['roas']:.2f}x</div>
                <div class="stat-subvalue">{data[-1]['month']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Revenue (Current)</div>
                <div class="stat-value">£{data[-1]['total_revenue']:,.0f}</div>
                <div class="stat-subvalue">JBB: £{data[-1]['jbb_revenue']:,.0f} | JHD: £{data[-1]['jhd_revenue']:,.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Google Ads Cost (Current)</div>
                <div class="stat-value">£{data[-1]['ads_cost']:,.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Average ROAS ({len(data)} months)</div>
                <div class="stat-value">{sum(d['roas'] for d in data) / len(data):.2f}x</div>
            </div>
        </div>

        <h2 style="margin-top: 30px;">Monthly ROAS Trend</h2>
        <div class="chart-container">
            <canvas id="roasChart"></canvas>
        </div>

        <h2 style="margin-top: 30px;">Revenue vs Cost</h2>
        <div class="chart-container">
            <canvas id="revenueChart"></canvas>
        </div>

        <h2 style="margin-top: 30px;">Detailed Monthly Data</h2>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Month</th>
                    <th>JBB Revenue</th>
                    <th>JHD Revenue</th>
                    <th>Total Revenue</th>
                    <th>Google Ads Cost</th>
                    <th>ROAS</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f'''
                <tr>
                    <td>{d['month']}</td>
                    <td>£{d['jbb_revenue']:,.2f}</td>
                    <td>£{d['jhd_revenue']:,.2f}</td>
                    <td><strong>£{d['total_revenue']:,.2f}</strong></td>
                    <td>£{d['ads_cost']:,.2f}</td>
                    <td><strong>{d['roas']:.2f}x</strong></td>
                </tr>
                ''' for d in reversed(data))}
            </tbody>
        </table>
    </div>

    <div class="updated">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>

    <script>
        // ROAS Chart
        const roasCtx = document.getElementById('roasChart').getContext('2d');
        const roasChart = new Chart(roasCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(months)},
                datasets: [{{
                    label: 'ROAS',
                    data: {json.dumps(roas_values)},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'ROAS: ' + context.parsed.y.toFixed(2) + 'x';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(2) + 'x';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Revenue vs Cost Chart
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        const revenueChart = new Chart(revenueCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(months)},
                datasets: [
                    {{
                        label: 'Revenue',
                        data: {json.dumps(revenue_values)},
                        backgroundColor: 'rgba(46, 204, 113, 0.7)',
                        borderColor: '#2ecc71',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Cost',
                        data: {json.dumps(cost_values)},
                        backgroundColor: 'rgba(231, 76, 60, 0.7)',
                        borderColor: '#e74c3c',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': £' + context.parsed.y.toLocaleString();
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '£' + value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✓ Dashboard generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate ROAS dashboard for Just Bin Bags group')
    parser.add_argument('--months', type=int, default=12, help='Number of months to analyze (default: 12)')
    args = parser.parse_args()

    print("=" * 60)
    print("Just Bin Bags Group - ROAS Dashboard Generator")
    print("=" * 60)

    # Generate monthly data
    data = generate_monthly_data(months=args.months)

    # Generate HTML dashboard
    output_path = Path(__file__).parent.parent / 'reports' / 'roas-dashboard.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_html_dashboard(data, output_path)

    # Open in browser
    print(f"\nOpening dashboard in browser...")
    subprocess.run(['open', str(output_path)])

    print("\n✓ Done!")


if __name__ == '__main__':
    main()
