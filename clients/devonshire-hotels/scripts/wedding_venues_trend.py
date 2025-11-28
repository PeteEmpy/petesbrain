#!/usr/bin/env python3
"""
Fetch Google Trends data for 'wedding venues' comparing 2024 vs 2025
"""
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-trends-mcp-server/.venv/lib/python3.13/site-packages')

from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time

# Initialize pytrends
pytrends = TrendReq(hl='en-GB', tz=0, retries=3, backoff_factor=2)

# Fetch 2024 data
print("Fetching 2024 data...")
time.sleep(2)
pytrends.build_payload(['wedding venues'], cat=0, timeframe='2024-01-01 2024-11-06', geo='GB')
df_2024 = pytrends.interest_over_time()

# Fetch 2025 data
print("Fetching 2025 data...")
time.sleep(5)  # Wait 5 seconds between requests
pytrends.build_payload(['wedding venues'], cat=0, timeframe='2025-01-01 2025-11-06', geo='GB')
df_2025 = pytrends.interest_over_time()

# Prepare data for visualization
data_2024 = []
data_2025 = []

if not df_2024.empty:
    df_2024 = df_2024.drop('isPartial', axis=1, errors='ignore')
    for date, row in df_2024.iterrows():
        data_2024.append({
            'date': date.strftime('%Y-%m-%d'),
            'value': int(row['wedding venues'])
        })

if not df_2025.empty:
    df_2025 = df_2025.drop('isPartial', axis=1, errors='ignore')
    for date, row in df_2025.iterrows():
        data_2025.append({
            'date': date.strftime('%Y-%m-%d'),
            'value': int(row['wedding venues'])
        })

# Output as JSON
result = {
    '2024': data_2024,
    '2025': data_2025
}

print(json.dumps(result, indent=2))
