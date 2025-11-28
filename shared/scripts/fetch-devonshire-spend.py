#!/usr/bin/env python3
"""
Fetch Devonshire spend data from Google Ads.
Called by daily-budget-monitor.py to get actual spend data.

Returns JSON with current month spend breakdown.
"""

import json
import sys
from datetime import datetime

def main():
    """
    Fetch current month spend for Devonshire campaigns.

    This is a placeholder that shows the structure.
    In production, this would be called by daily-budget-monitor.py
    which has access to Google Ads MCP tools.
    """

    # Get current month date range
    today = datetime.now()
    year = today.year
    month = today.month
    first_day = f"{year}-{month:02d}-01"
    current_day = today.strftime('%Y-%m-%d')

    # This structure shows what the MCP query should return
    result = {
        'account_id': '5898250490',
        'date_range': {
            'start': first_day,
            'end': current_day
        },
        'main_properties': {
            'spend': 0.0,
            'campaigns': []
        },
        'the_hide': {
            'spend': 0.0
        },
        'total_spend': 0.0,
        'data_as_of': current_day
    }

    print(json.dumps(result, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
