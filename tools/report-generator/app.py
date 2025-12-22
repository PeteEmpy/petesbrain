"""
Report Generator Flask Web Application

Interactive web interface for generating, viewing, and managing reports.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from report_generator import ReportGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize report generator
generator = ReportGenerator()

# Store latest generated report data in memory (for single-user desktop app)
latest_report = None


@app.route('/')
def index():
    """Home page with report generation options"""
    clients = generator.list_clients()
    return render_template('index.html', clients=clients)


@app.route('/api/clients')
def api_clients():
    """API endpoint to get list of clients"""
    clients = generator.list_clients()
    return jsonify({'clients': clients})


@app.route('/api/client/<client_name>/accounts')
def api_client_accounts(client_name):
    """API endpoint to get client account information"""
    accounts = generator.get_client_accounts(client_name)
    return jsonify(accounts)


@app.route('/generate', methods=['POST'])
def generate_report():
    """Generate a report based on form input"""
    global latest_report

    try:
        # Get form data
        report_type = request.form.get('report_type')
        client_name = request.form.get('client_name')
        date_range_type = request.form.get('date_range_type')
        custom_start = request.form.get('custom_start')
        custom_end = request.form.get('custom_end')
        save_to_client = request.form.get('save_to_client') == 'true'

        # Calculate date range
        start_date, end_date = generator.calculate_date_range(
            date_range_type, custom_start, custom_end
        )

        # Fetch data based on report type
        if report_type == 'q4_strategy':
            data = fetch_q4_strategy_data(client_name, start_date, end_date)
        elif report_type == 'weekly_performance':
            data = fetch_weekly_performance_data(client_name, start_date, end_date)
        elif report_type == 'monthly_summary':
            data = fetch_monthly_summary_data(client_name, start_date, end_date)
        elif report_type == 'campaign_analysis':
            data = fetch_campaign_analysis_data(client_name, start_date, end_date)
        else:
            return jsonify({'error': 'Invalid report type'}), 400

        # Generate report
        report = generator.generate_report(
            report_type=report_type,
            client_name=client_name,
            date_range=(start_date, end_date),
            data=data
        )

        # Store in global variable for viewing
        latest_report = report

        # Save to file system
        report_path = generator.save_report(report, save_to_client_folder=save_to_client)

        return jsonify({
            'success': True,
            'report_path': report_path,
            'redirect': url_for('view_report')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/view')
def view_report():
    """View the latest generated report"""
    if latest_report is None:
        return redirect(url_for('index'))

    report_type = latest_report['type']
    report_data = latest_report['data']

    # Render appropriate template based on report type
    template = f'reports/{report_type}.html'

    return render_template(template, report=report_data)


@app.route('/reports')
def list_reports():
    """List all saved reports"""
    client_filter = request.args.get('client')
    reports = generator.list_saved_reports(client_name=client_filter)

    return render_template('reports/list.html', reports=reports, client_filter=client_filter)


@app.route('/reports/<filename>')
def load_report(filename):
    """Load a saved report"""
    global latest_report

    try:
        report_path = generator.reports_path / filename
        with open(report_path, 'r') as f:
            latest_report = json.load(f)

        return redirect(url_for('view_report'))

    except Exception as e:
        return f"Error loading report: {e}", 404


@app.route('/export/<format>')
def export_report(format):
    """Export latest report to specified format"""
    if latest_report is None:
        return "No report to export", 400

    if format == 'html':
        return export_html()
    elif format == 'pdf':
        return export_pdf()
    elif format == 'json':
        return export_json()
    else:
        return "Invalid export format", 400


def export_html():
    """Export report as standalone HTML file"""
    if latest_report is None:
        return "No report to export", 400

    # Render template to string
    report_type = latest_report['type']
    report_data = latest_report['data']
    template = f'reports/{report_type}.html'

    html_content = render_template(template, report=report_data, standalone=True)

    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{latest_report['client']}_{report_type}_{timestamp}.html"
    export_path = generator.reports_path / 'exports' / filename

    export_path.parent.mkdir(exist_ok=True)

    with open(export_path, 'w') as f:
        f.write(html_content)

    return send_file(export_path, as_attachment=True, download_name=filename)


def export_pdf():
    """Export report as PDF (requires weasyprint)"""
    # TODO: Implement PDF export using weasyprint
    return "PDF export coming soon", 501


def export_json():
    """Export report as JSON"""
    if latest_report is None:
        return "No report to export", 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{latest_report['client']}_{latest_report['type']}_{timestamp}.json"

    # Create temporary file
    export_path = generator.reports_path / 'exports' / filename
    export_path.parent.mkdir(exist_ok=True)

    with open(export_path, 'w') as f:
        json.dump(latest_report, f, indent=2)

    return send_file(export_path, as_attachment=True, download_name=filename)


# Data fetching functions (integrate with MCP)

def fetch_q4_strategy_data(client_name: str, start_date: str, end_date: str) -> dict:
    """Fetch data for Q4 strategy report

    This function would call MCP tools to fetch real data.
    For now, returns structured data based on client.
    """

    # Get client accounts
    account_info = generator.get_client_accounts(client_name)

    # For Smythson, we have real structure to work with
    if client_name.lower() == 'smythson':
        # This would call MCP Google Ads tools
        # For now, return structure that matches what we need

        return {
            'regions': [
                {
                    'name': 'UK',
                    'code': 'GB',
                    'account_id': '8573235780',
                    'budget': 160752,
                    'revenue_target': 300000,
                    'roas_target': 3.0,
                    'current_spend': 37752,
                    'current_revenue': 156639,
                    'current_roas': 4.15,
                    'conversions': 1086
                },
                {
                    'name': 'USA',
                    'code': 'US',
                    'account_id': '7808690871',
                    'budget': 133960,
                    'revenue_target': 250000,
                    'roas_target': 1.5,
                    'current_spend': 37097,
                    'current_revenue': 123791,
                    'current_roas': 3.34,
                    'conversions': 470
                },
                {
                    'name': 'EUR',
                    'code': 'EU',
                    'account_id': '7679616761',
                    'budget': 51382,
                    'revenue_target': 150000,
                    'roas_target': 1.5,
                    'current_spend': 14511,
                    'current_revenue': 53086,
                    'current_roas': 3.66,
                    'conversions': 404
                },
                {
                    'name': 'ROW',
                    'code': 'WORLD',
                    'account_id': '5556710725',
                    'budget': 20920,
                    'revenue_target': 80691,
                    'roas_target': 1.0,
                    'current_spend': 6729,
                    'current_revenue': 17714,
                    'current_roas': 2.63,
                    'conversions': 135
                }
            ],
            'strategy': {
                'overview': 'Multi-regional Christmas strategy for Q4 2025',
                'total_budget': 367014,
                'total_revenue_target': 780691
            },
            'timeline': [
                {'date': 'Oct 29', 'milestone': 'UK & EUR Launch', 'description': 'Primary markets go live'},
                {'date': 'Nov 1', 'milestone': 'USA Launch', 'description': 'US market activation'},
                {'date': 'Nov 15', 'milestone': 'ROW Launch + Review', 'description': 'Rest of World launch and first review'},
                {'date': 'Nov 25', 'milestone': 'Thanksgiving Boost', 'description': '+15% USA budget increase'},
                {'date': 'Dec 1', 'milestone': 'Peak Season Adjustments', 'description': 'Optimization for peak period'},
                {'date': 'Dec 15', 'milestone': 'Mid-December Assessment', 'description': 'Final push optimization'},
                {'date': 'Dec 31', 'milestone': 'End-of-Quarter Review', 'description': 'Q4 analysis and Q1 planning'}
            ],
            'recommendations': [
                'All regions performing above targets - consider aggressive budget utilization',
                'ROW showing 163% above target - consider earlier launch or increased budget',
                'USA at 3.34 ROAS provides headroom for Thanksgiving competition',
                'Strong baseline performance suggests accelerated asset group rollout'
            ]
        }

    # Default structure for other clients
    # Generate placeholder data based on account info
    regions = []

    if account_info.get('accounts'):
        # Use actual account structure if available
        for account in account_info['accounts']:
            regions.append({
                'name': account.get('region', account.get('name', 'Main')),
                'code': account.get('region', 'UK')[:2],
                'account_id': account['id'],
                'budget': 50000,  # Placeholder
                'revenue_target': 150000,  # Placeholder
                'roas_target': 3.0,
                'current_spend': 15000,  # Placeholder
                'current_revenue': 45000,  # Placeholder
                'current_roas': 3.0,
                'conversions': 150  # Placeholder
            })
    else:
        # Single region placeholder
        regions = [{
            'name': 'UK',
            'code': 'GB',
            'account_id': 'N/A',
            'budget': 50000,
            'revenue_target': 150000,
            'roas_target': 3.0,
            'current_spend': 15000,
            'current_revenue': 45000,
            'current_roas': 3.0,
            'conversions': 150
        }]

    total_budget = sum(r['budget'] for r in regions)
    total_revenue = sum(r['revenue_target'] for r in regions)

    return {
        'regions': regions,
        'strategy': {
            'overview': f'Q4 2025 strategy for {client_name.replace("-", " ").title()}',
            'total_budget': total_budget,
            'total_revenue_target': total_revenue
        },
        'timeline': [
            {'date': 'Oct 29', 'milestone': 'Q4 Launch', 'description': 'Campaign activation for holiday season'},
            {'date': 'Nov 15', 'milestone': 'Mid-Quarter Review', 'description': 'Performance assessment and optimization'},
            {'date': 'Nov 25', 'milestone': 'Black Friday', 'description': 'Peak season preparation'},
            {'date': 'Dec 1', 'milestone': 'December Push', 'description': 'Final month optimization'},
            {'date': 'Dec 15', 'milestone': 'End-of-Year Review', 'description': 'Q4 wrap-up and Q1 planning'}
        ],
        'recommendations': [
            'Monitor performance daily during peak season',
            'Adjust bids based on ROAS trends',
            'Test new ad copy variations',
            'Review budget allocation by campaign'
        ]
    }


def fetch_weekly_performance_data(client_name: str, start_date: str, end_date: str) -> dict:
    """Fetch data for weekly performance report"""
    # TODO: Implement MCP integration
    return {
        'performance': {
            'spend': 0,
            'revenue': 0,
            'roas': 0,
            'conversions': 0,
            'clicks': 0,
            'impressions': 0
        },
        'campaigns': [],
        'trends': {},
        'alerts': []
    }


def fetch_monthly_summary_data(client_name: str, start_date: str, end_date: str) -> dict:
    """Fetch data for monthly summary report"""
    # TODO: Implement MCP integration
    return {
        'summary': {},
        'top_campaigns': [],
        'insights': []
    }


def fetch_campaign_analysis_data(client_name: str, start_date: str, end_date: str) -> dict:
    """Fetch data for campaign analysis report

    NOTE: For now, this returns placeholder data. In production, Claude Code would
    call MCP tools to fetch real Google Ads data and pass it to this route.

    See test_real_data.py for example of how to integrate with real MCP data.
    """
    # TODO: Implement MCP integration via Claude Code
    # For now, return sample campaign data structure
    # When MCP is integrated, this would be replaced with actual GAQL query results

    return {
        'campaigns': [
            {
                'id': 'sample_12345',
                'name': f'{client_name} | Sample Campaign 1',
                'status': 'ENABLED',
                'advertising_channel_type': 'PERFORMANCE_MAX',
                'metrics': {
                    'cost_micros': 500000000,  # £500
                    'conversions_value': 1500.00,  # £1500
                    'conversions': 30,
                    'clicks': 1000,
                    'impressions': 25000,
                    'search_lost_impression_share_budget': 0.12
                }
            },
            {
                'id': 'sample_67890',
                'name': f'{client_name} | Sample Campaign 2',
                'status': 'ENABLED',
                'advertising_channel_type': 'SHOPPING',
                'metrics': {
                    'cost_micros': 300000000,  # £300
                    'conversions_value': 600.00,  # £600
                    'conversions': 15,
                    'clicks': 600,
                    'impressions': 15000,
                    'search_lost_impression_share_budget': 0.05
                }
            }
        ]
    }


if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, port=5002, host='127.0.0.1')
