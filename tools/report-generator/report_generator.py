"""
Report Generator Core Engine

Handles report generation, data fetching, and export functionality.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional, Any


class ReportGenerator:
    """Core report generation engine"""

    def __init__(self, base_path: str = None):
        """Initialize the report generator

        Args:
            base_path: Base path for Pete's Brain (defaults to discovering it)
        """
        if base_path is None:
            # Auto-discover Pete's Brain path
            current = Path(__file__).resolve()
            while current.parent != current:
                if (current / 'clients').exists() and (current / 'tools').exists():
                    base_path = str(current)
                    break
                current = current.parent

        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.clients_path = self.base_path / 'clients'
        self.reports_path = Path(__file__).parent / 'reports'
        self.reports_path.mkdir(exist_ok=True)

    def list_clients(self) -> List[Dict[str, str]]:
        """List all available clients

        Returns:
            List of client dictionaries with name and path
        """
        clients = []
        if not self.clients_path.exists():
            return clients

        for client_dir in self.clients_path.iterdir():
            if client_dir.is_dir() and not client_dir.name.startswith('_'):
                clients.append({
                    'name': client_dir.name,
                    'path': str(client_dir),
                    'display_name': client_dir.name.replace('-', ' ').title()
                })

        return sorted(clients, key=lambda x: x['display_name'])

    def get_client_accounts(self, client_name: str) -> Dict[str, Any]:
        """Get Google Ads account information for a client

        Args:
            client_name: Name of the client

        Returns:
            Dictionary with account information
        """
        # This would integrate with MCP Google Ads server
        # For now, return hardcoded mappings for known clients
        account_mapping = {
            'smythson': {
                'accounts': [
                    {'id': '8573235780', 'name': 'Smythson UK', 'region': 'UK'},
                    {'id': '7808690871', 'name': 'Smythson USA', 'region': 'USA'},
                    {'id': '7679616761', 'name': 'Smythson EUR', 'region': 'EUR'},
                    {'id': '5556710725', 'name': 'Smythson ROW', 'region': 'ROW'}
                ],
                'manager_id': '2569949686'
            }
        }

        return account_mapping.get(client_name.lower(), {'accounts': [], 'manager_id': None})

    def calculate_date_range(self, range_type: str, custom_start: str = None, custom_end: str = None) -> tuple:
        """Calculate date range based on type

        Args:
            range_type: Type of range (last_7_days, last_30_days, this_month, last_month, q4_2025, custom)
            custom_start: Custom start date (YYYY-MM-DD)
            custom_end: Custom end date (YYYY-MM-DD)

        Returns:
            Tuple of (start_date, end_date) as strings
        """
        today = datetime.now()

        if range_type == 'last_7_days':
            start = today - timedelta(days=7)
            end = today - timedelta(days=1)
        elif range_type == 'last_30_days':
            start = today - timedelta(days=30)
            end = today - timedelta(days=1)
        elif range_type == 'this_month':
            start = today.replace(day=1)
            end = today
        elif range_type == 'last_month':
            last_month = today.replace(day=1) - timedelta(days=1)
            start = last_month.replace(day=1)
            end = last_month
        elif range_type == 'q4_2025':
            start = datetime(2025, 10, 1)
            end = datetime(2025, 12, 31)
        elif range_type == 'custom':
            start = datetime.strptime(custom_start, '%Y-%m-%d')
            end = datetime.strptime(custom_end, '%Y-%m-%d')
        else:
            # Default to last 7 days
            start = today - timedelta(days=7)
            end = today - timedelta(days=1)

        return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

    def fetch_google_ads_data(self, account_ids: List[str], manager_id: str,
                             start_date: str, end_date: str) -> Dict[str, Any]:
        """Fetch data from Google Ads MCP

        This is a placeholder - actual implementation would use MCP tools

        Args:
            account_ids: List of Google Ads account IDs
            manager_id: Manager account ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Dictionary with performance data
        """
        # NOTE: This would be called from app.py which has access to MCP tools
        # The app.py will pass the fetched data to generate_report()
        return {}

    def generate_report(self, report_type: str, client_name: str,
                       date_range: tuple, data: Dict[str, Any],
                       options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a report

        Args:
            report_type: Type of report to generate
            client_name: Name of the client
            date_range: Tuple of (start_date, end_date)
            data: Report data (fetched from various sources)
            options: Additional report options

        Returns:
            Dictionary with report metadata and content path
        """
        options = options or {}

        # Generate report based on type
        if report_type == 'q4_strategy':
            return self._generate_q4_strategy_report(client_name, date_range, data, options)
        elif report_type == 'weekly_performance':
            return self._generate_weekly_performance_report(client_name, date_range, data, options)
        elif report_type == 'monthly_summary':
            return self._generate_monthly_summary_report(client_name, date_range, data, options)
        elif report_type == 'campaign_analysis':
            return self._generate_campaign_analysis_report(client_name, date_range, data, options)
        else:
            raise ValueError(f"Unknown report type: {report_type}")

    def _generate_q4_strategy_report(self, client_name: str, date_range: tuple,
                                    data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Q4 strategy report"""
        # Extract data
        regions_data = data.get('regions', [])
        strategy = data.get('strategy', {})

        # Calculate metrics
        total_budget = sum(r.get('budget', 0) for r in regions_data)
        total_revenue_target = sum(r.get('revenue_target', 0) for r in regions_data)
        overall_roas_target = total_revenue_target / total_budget if total_budget > 0 else 0

        # Format data for template
        report_data = {
            'client_name': client_name,
            'client_display': client_name.replace('-', ' ').title(),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'date_range': date_range,
            'total_budget': total_budget,
            'total_revenue_target': total_revenue_target,
            'overall_roas_target': overall_roas_target,
            'regions': regions_data,
            'strategy': strategy,
            'timeline': data.get('timeline', []),
            'recommendations': data.get('recommendations', [])
        }

        return {
            'type': 'q4_strategy',
            'client': client_name,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        }

    def _generate_weekly_performance_report(self, client_name: str, date_range: tuple,
                                           data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weekly performance report"""
        report_data = {
            'client_name': client_name,
            'client_display': client_name.replace('-', ' ').title(),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'date_range': date_range,
            'performance': data.get('performance', {}),
            'campaigns': data.get('campaigns', []),
            'trends': data.get('trends', {}),
            'alerts': data.get('alerts', [])
        }

        return {
            'type': 'weekly_performance',
            'client': client_name,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        }

    def _generate_monthly_summary_report(self, client_name: str, date_range: tuple,
                                        data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate monthly summary report"""
        report_data = {
            'client_name': client_name,
            'client_display': client_name.replace('-', ' ').title(),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'date_range': date_range,
            'summary': data.get('summary', {}),
            'top_campaigns': data.get('top_campaigns', []),
            'insights': data.get('insights', [])
        }

        return {
            'type': 'monthly_summary',
            'client': client_name,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        }

    def _generate_campaign_analysis_report(self, client_name: str, date_range: tuple,
                                          data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate campaign analysis report"""
        report_data = {
            'client_name': client_name,
            'client_display': client_name.replace('-', ' ').title(),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'date_range': date_range,
            'campaigns': data.get('campaigns', []),
            'analysis': data.get('analysis', {}),
            'optimizations': data.get('optimizations', [])
        }

        return {
            'type': 'campaign_analysis',
            'client': client_name,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        }

    def save_report(self, report_data: Dict[str, Any], save_to_client_folder: bool = True) -> str:
        """Save report to file system

        Args:
            report_data: Report data dictionary
            save_to_client_folder: Whether to also save to client folder

        Returns:
            Path to saved report file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_data['client']}_{report_data['type']}_{timestamp}.json"

        # Save to reports directory
        report_path = self.reports_path / filename
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        # Optionally save to client folder
        if save_to_client_folder:
            client_path = self.clients_path / report_data['client'] / 'reports'
            client_path.mkdir(exist_ok=True)
            client_report_path = client_path / filename
            with open(client_report_path, 'w') as f:
                json.dump(report_data, f, indent=2)

        return str(report_path)

    def list_saved_reports(self, client_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """List saved reports

        Args:
            client_name: Optional client name to filter by

        Returns:
            List of report metadata dictionaries
        """
        reports = []

        for report_file in self.reports_path.glob('*.json'):
            try:
                with open(report_file, 'r') as f:
                    report_data = json.load(f)

                if client_name is None or report_data.get('client') == client_name:
                    reports.append({
                        'filename': report_file.name,
                        'path': str(report_file),
                        'client': report_data.get('client'),
                        'type': report_data.get('type'),
                        'generated_at': report_data.get('generated_at'),
                        'size': report_file.stat().st_size
                    })
            except Exception as e:
                print(f"Error reading report {report_file}: {e}")
                continue

        # Sort by generated_at descending
        reports.sort(key=lambda x: x.get('generated_at', ''), reverse=True)
        return reports
