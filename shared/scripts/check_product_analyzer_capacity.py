#!/usr/bin/env python3
"""
Check Product Impact Analyzer capacity for weekly summary
Returns HTML-formatted capacity status
"""

import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_capacity_html():
    """Get capacity status as HTML for email"""
    try:
        # Load config
        config_path = Path("/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/config.json")
        with open(config_path) as f:
            config = json.load(f)

        spreadsheet_id = config['spreadsheet_id']

        # Get credentials
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path:
            creds_path = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json"

        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        service = build('sheets', 'v4', credentials=credentials)

        # Get total capacity
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            includeGridData=False
        ).execute()

        total_cells = 0
        for sheet in spreadsheet.get('sheets', []):
            props = sheet['properties']
            grid_props = props.get('gridProperties', {})
            rows = grid_props.get('rowCount', 0)
            cols = grid_props.get('columnCount', 0)
            total_cells += rows * cols

        capacity_pct = total_cells / 10_000_000 * 100

        # Calculate days until full (estimate)
        daily_row_accumulation = 10500  # 15 clients × 700 products
        daily_perf_cols = 13
        cells_per_day = daily_row_accumulation * daily_perf_cols
        available_cells = 10_000_000 - total_cells
        days_remaining = available_cells / cells_per_day if cells_per_day > 0 else 999

        # Determine status and action
        if capacity_pct >= 85:
            status_emoji = "🚨"
            status_color = "#dc3545"  # Red
            status_text = "URGENT - Archive Required"
            action_html = f'''
            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-top: 10px;">
                <h4 style="color: #856404; margin-top: 0;">⚠️ Action Required Within 1 Week</h4>
                <p style="margin: 10px 0;">Run the archive script to free up space:</p>
                <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;">cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \\
  .venv/bin/python3 shrink_sheet.py</pre>
                <p style="margin: 10px 0; font-size: 0.9em; color: #666;">This will resize the sheet to actual data size plus growth buffer.</p>
            </div>
            '''
        elif capacity_pct >= 70:
            status_emoji = "ℹ️"
            status_color = "#0dcaf0"  # Info blue
            status_text = "Plan Archive Soon"
            action_html = f'''
            <div style="background-color: #d1ecf1; border-left: 4px solid #0dcaf0; padding: 15px; margin-top: 10px;">
                <h4 style="color: #0c5460; margin-top: 0;">ℹ️ Plan Ahead</h4>
                <p style="margin: 10px 0;">Capacity approaching 70%. Plan to run archive in the next 2-4 weeks.</p>
                <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;">cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json \\
  .venv/bin/python3 shrink_sheet.py</pre>
            </div>
            '''
        else:
            status_emoji = "✅"
            status_color = "#28a745"  # Green
            status_text = "Healthy"
            action_html = ""

        # Build HTML
        html = f'''
        <div style="border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin: 20px 0; background-color: #ffffff;">
            <h3 style="margin-top: 0; color: #333;">
                {status_emoji} Product Impact Analyzer - Capacity Status
            </h3>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                <div>
                    <p style="margin: 5px 0; color: #666; font-size: 0.9em;">Total Capacity</p>
                    <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: {status_color};">
                        {capacity_pct:.1f}%
                    </p>
                </div>
                <div>
                    <p style="margin: 5px 0; color: #666; font-size: 0.9em;">Days Until Full</p>
                    <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #333;">
                        ~{int(days_remaining)} days
                    </p>
                </div>
            </div>

            <div style="background-color: #f8f9fa; border-radius: 4px; padding: 10px; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold;">Status:</span>
                    <span style="color: {status_color}; font-weight: bold;">{status_text}</span>
                </div>
                <div style="margin-top: 8px;">
                    <div style="background-color: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: {status_color}; height: 100%; width: {capacity_pct}%; transition: width 0.3s;"></div>
                    </div>
                </div>
            </div>

            <p style="margin: 10px 0; font-size: 0.9em; color: #666;">
                {total_cells:,} / 10,000,000 cells used
            </p>

            {action_html}

            <p style="margin: 15px 0 0 0; font-size: 0.85em; color: #999;">
                View spreadsheet: <a href="https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit" style="color: #007bff;">Open in Google Sheets</a>
            </p>
        </div>
        '''

        return html

    except Exception as e:
        return f'''
        <div style="border: 1px solid #dc3545; border-radius: 8px; padding: 20px; margin: 20px 0; background-color: #f8d7da;">
            <h3 style="margin-top: 0; color: #721c24;">
                ⚠️ Product Impact Analyzer - Capacity Check Failed
            </h3>
            <p>Error: {str(e)}</p>
        </div>
        '''


if __name__ == "__main__":
    print(get_capacity_html())
