#!/usr/bin/env python3
"""
Fetch search terms from source spreadsheet and organize by country.
Uses Google Sheets API directly to handle large datasets.
"""

import sys
sys.path.insert(0, "/Users/administrator/Documents/PetesBrain")

# Since MCP calls have token limits, we'll read the spreadsheet using direct API access
# through the existing Google Sheets credentials

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SOURCE_SPREADSHEET_ID = '15hAiWAEuaqUCucTm1egzoHPhQpckTy-jRuR6MUqpXIE'
RANGE_NAME = 'Search terms report - Superspace!A:F'

def get_country(campaign_name):
    """Extract country code from campaign name."""
    if "SUP | US |" in campaign_name:
        return "US"
    elif "SUP | UK |" in campaign_name:
        return "UK"
    elif "SUP | AU |" in campaign_name:
        return "AUS"
    return None

def get_campaign_type(match_type, campaign_name):
    """Determine campaign type from match type and campaign name."""
    if match_type == "Performance Max":
        return "Performance Max"
    elif "Shopping" in campaign_name:
        return "Shopping"
    elif "P Max" in campaign_name:
        return "Performance Max"
    elif "Search" in campaign_name:
        return "Search"
    return "Unknown"

def is_data_row(row):
    """Check if row is actual data (not header or total)."""
    if len(row) < 4:
        return False
    search_term = row[0]
    # Skip header rows and total rows
    if search_term in ["Search term", "Total: Filtered search terms", "Total: Account",
                       "Total: Search", "Total: Demand Gen", "Total: Shopping",
                       "Total: Performance Max", "Search terms report - Superspace", ""]:
        return False
    if search_term.startswith("Total:") or search_term.startswith("1 January"):
        return False
    return True

def main():
    # Authenticate
    creds = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Read data
    print("Fetching data from Google Sheets...")
    result = sheet.values().get(
        spreadsheetId=SOURCE_SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    values = result.get('values', [])
    print(f"Retrieved {len(values)} rows")

    # Organize by country
    us_data = [["Search Term", "Campaign Name", "Campaign Type", "Clicks"]]
    uk_data = [["Search Term", "Campaign Name", "Campaign Type", "Clicks"]]
    aus_data = [["Search Term", "Campaign Name", "Campaign Type", "Clicks"]]

    for row in values:
        if not is_data_row(row):
            continue

        # Extract fields
        search_term = row[0] if len(row) > 0 else ""
        match_type = row[1] if len(row) > 1 else ""
        campaign_name = row[3] if len(row) > 3 else ""
        clicks = row[5] if len(row) > 5 else "0"

        # Determine country and campaign type
        country = get_country(campaign_name)
        campaign_type = get_campaign_type(match_type, campaign_name)

        if country is None:
            continue

        # Add to appropriate list
        new_row = [search_term, campaign_name, campaign_type, clicks]

        if country == "US":
            us_data.append(new_row)
        elif country == "UK":
            uk_data.append(new_row)
        elif country == "AUS":
            aus_data.append(new_row)

    print(f"US: {len(us_data)-1} rows")
    print(f"UK: {len(uk_data)-1} rows")
    print(f"AUS: {len(aus_data)-1} rows")

    # Save to CSV files
    import csv

    with open('us-data-new.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(us_data)

    with open('uk-data-new.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(uk_data)

    with open('aus-data-new.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(aus_data)

    print("\nFiles created:")
    print("  - us-data-new.csv")
    print("  - uk-data-new.csv")
    print("  - aus-data-new.csv")

    # Also return the data for loading to destination spreadsheet
    return us_data, uk_data, aus_data

if __name__ == "__main__":
    main()
