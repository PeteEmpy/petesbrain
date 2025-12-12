#!/usr/bin/env python3
"""
PMAX Asset Optimizer - Master End-to-End Script

Usage:
    python3 optimize_pmax_assets.py --client devonshire-hotels
    python3 optimize_pmax_assets.py --customer-id 5898250490 --client-name devonshire-hotels

What it does:
1. Fetches asset performance from Google Ads API (with landing page URLs)
2. Stores CSV in /clients/{client}/data/pmax/
3. Identifies HIGH priority underperformers only
4. Generates AI-powered replacement text (3 options per asset)
5. Creates review sheet in correct format (1 row per asset, options in columns)
6. Uploads to Google Sheets for client review

Output:
- CSV: /clients/{client}/data/pmax/asset-performance-YYYY-MM-DD.csv
- Review CSV: /clients/{client}/data/pmax/review-sheet-YYYY-MM-DD.csv
- Google Sheet URL for client to review
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
import csv
import json
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))
from paths import get_project_root, get_clients_dir, get_infrastructure_dir

PROJECT_ROOT = get_project_root()
sys.path.insert(0, str(get_infrastructure_dir() / "mcp-servers" / "google-sheets-mcp-server"))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CLIENTS_DIR = get_clients_dir()
TODAY = datetime.now().strftime("%Y-%m-%d")

def get_client_info(client_name=None, customer_id=None):
    """Get client name and customer ID"""
    if customer_id and not client_name:
        # Look up client name from customer ID in CONTEXT.md files
        for client_dir in CLIENTS_DIR.iterdir():
            if client_dir.is_dir():
                context_file = client_dir / "CONTEXT.md"
                if context_file.exists():
                    content = context_file.read_text()
                    if f"Google Ads Customer ID: {customer_id}" in content:
                        return client_dir.name, customer_id

        print(f"❌ Could not find client with customer ID {customer_id}")
        sys.exit(1)

    return client_name, customer_id

def fetch_asset_performance(customer_id, client_name, days=90):
    """Step 1: Fetch asset performance from API"""
    print("\n" + "="*80)
    print("STEP 1: FETCHING ASSET PERFORMANCE FROM API")
    print("="*80)

    output_dir = CLIENTS_DIR / client_name / "data" / "pmax"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"asset-performance-{TODAY}.csv"

    cmd = [
        ".venv/bin/python3",
        "fetch_asset_performance_api.py",
        "--customer-id", customer_id,
        "--days", str(days),
        "--output", str(output_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print(f"❌ API fetch failed:\n{result.stderr}")
        sys.exit(1)

    return output_file

def identify_high_priority_underperformers(csv_file):
    """Step 2: Analyze and filter to HIGH priority only"""
    print("\n" + "="*80)
    print("STEP 2: IDENTIFYING HIGH PRIORITY UNDERPERFORMERS")
    print("="*80)

    # Run analysis
    cmd = [
        ".venv/bin/python3",
        "analyse_asset_performance.py",
        "--csv", str(csv_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    # Filter to HIGH priority
    underperformers_file = Path("output/underperforming-assets.csv")
    if not underperformers_file.exists():
        print("❌ Underperformers file not created")
        sys.exit(1)

    # Read and filter
    with open(underperformers_file, 'r') as f:
        reader = csv.DictReader(f)
        all_assets = list(reader)

    high_priority = [a for a in all_assets if a.get('Priority') == 'HIGH']

    print(f"\n📊 Analysis Results:")
    print(f"   Total underperformers: {len(all_assets)}")
    print(f"   HIGH priority: {len(high_priority)}")
    print(f"   Filtering to HIGH priority only for AI generation")

    # Save HIGH priority only
    high_priority_file = csv_file.parent / f"high-priority-underperformers-{TODAY}.csv"
    with open(high_priority_file, 'w', newline='') as f:
        if high_priority:
            writer = csv.DictWriter(f, fieldnames=high_priority[0].keys())
            writer.writeheader()
            writer.writerows(high_priority)

    return high_priority_file, len(high_priority)

def generate_replacement_text(customer_id, high_priority_csv, client_name):
    """Step 3: Generate AI replacements for HIGH priority only"""
    print("\n" + "="*80)
    print("STEP 3: GENERATING AI REPLACEMENT TEXT (HIGH PRIORITY ONLY)")
    print("="*80)

    output_dir = CLIENTS_DIR / client_name / "data" / "pmax"
    output_file = output_dir / f"replacements-{TODAY}.csv"

    cmd = [
        ".venv/bin/python3",
        "generate_replacement_text.py",
        "--customer-id", customer_id,
        "--csv", str(high_priority_csv),
        "--output", str(output_file)
    ]

    print(f"⏱️  This will take ~3 seconds per asset...")

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print(f"❌ Replacement generation failed:\n{result.stderr}")
        sys.exit(1)

    return output_file

def create_review_sheet(replacements_csv, client_name):
    """Step 4: Transform to horizontal review format"""
    print("\n" + "="*80)
    print("STEP 4: CREATING REVIEW SHEET FORMAT")
    print("="*80)

    # Read vertical format (3 rows per asset with Option_Number 1, 2, 3)
    with open(replacements_csv, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Group by original text
    assets = {}
    for row in rows:
        key = (row['Campaign'], row['Asset_Group'], row['Original_Text'])
        if key not in assets:
            assets[key] = {
                'asset': row,
                'options': []
            }
        assets[key]['options'].append(row['Replacement_Text'])

    # Create horizontal format (1 row per asset, 3 option columns)
    output_rows = []
    for (campaign, asset_group, original_text), data in assets.items():
        asset = data['asset']
        options = data['options']

        # Ensure 3 options
        while len(options) < 3:
            options.append('')

        output_row = {
            'Campaign': campaign,
            'Asset Group': asset_group,
            'Priority': asset['Priority'],
            'Asset Type': asset['Asset_Type'],
            'Current Text': original_text,
            'Impressions': asset['Impressions'],
            'CTR': asset['CTR'],
            'Conv Rate': asset['Conv_Rate'],
            'Issue': asset['Flag_Reason'],
            'Option 1': options[0],
            'Option 2': options[1],
            'Option 3': options[2],
            'Selected Option (1/2/3 or blank to skip)': '',
            'Notes': ''
        }
        output_rows.append(output_row)

    # Save review sheet
    output_dir = CLIENTS_DIR / client_name / "data" / "pmax"
    review_file = output_dir / f"review-sheet-{TODAY}.csv"

    fieldnames = ['Campaign', 'Asset Group', 'Priority', 'Asset Type', 'Current Text',
                  'Impressions', 'CTR', 'Conv Rate', 'Issue', 'Option 1', 'Option 2', 'Option 3',
                  'Selected Option (1/2/3 or blank to skip)', 'Notes']

    with open(review_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"✅ Created review sheet: {review_file}")
    print(f"   Total assets: {len(output_rows)}")

    return review_file

def upload_to_google_sheets(review_csv, client_name):
    """Step 5: Upload to Google Sheets"""
    print("\n" + "="*80)
    print("STEP 5: UPLOADING TO GOOGLE SHEETS")
    print("="*80)

    # Load credentials
    creds = Credentials.from_authorized_user_file(
        '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json'
    )
    service = build('sheets', 'v4', credentials=creds)

    # Read review sheet
    with open(review_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Create spreadsheet
    title = f"{client_name.replace('-', ' ').title()} - PMAX Asset Review ({TODAY})"
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': title},
        'sheets': [{'properties': {'title': 'Asset Review'}}]
    }).execute()

    spreadsheet_id = spreadsheet['spreadsheetId']

    # Upload data
    body = {'values': data}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Asset Review!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    print(f"✅ Uploaded {len(data)} rows to Google Sheets")
    print(f"\n🔗 Sheet URL: {url}")

    return url

def main():
    parser = argparse.ArgumentParser(
        description='End-to-end PMAX asset optimization for any client'
    )
    parser.add_argument('--client', help='Client name (e.g., devonshire-hotels)')
    parser.add_argument('--customer-id', help='Google Ads customer ID')
    parser.add_argument('--days', type=int, default=90, help='Days of data to analyze')

    args = parser.parse_args()

    if not args.client and not args.customer_id:
        print("❌ Must provide either --client or --customer-id")
        sys.exit(1)

    # Get client info
    client_name, customer_id = get_client_info(args.client, args.customer_id)

    print("="*80)
    print("PMAX ASSET OPTIMIZER - END-TO-END WORKFLOW")
    print("="*80)
    print(f"Client: {client_name}")
    print(f"Customer ID: {customer_id}")
    print(f"Date: {TODAY}")
    print(f"Days: {args.days}")
    print("="*80)

    # Step 1: Fetch from API
    csv_file = fetch_asset_performance(customer_id, client_name, args.days)

    # Step 2: Identify HIGH priority
    high_priority_csv, count = identify_high_priority_underperformers(csv_file)

    if count == 0:
        print("\n✅ No HIGH priority underperformers found - nothing to optimize!")
        sys.exit(0)

    # Step 3: Generate replacements (HIGH priority only)
    replacements_csv = generate_replacement_text(customer_id, high_priority_csv, client_name)

    # Step 4: Create review sheet
    review_csv = create_review_sheet(replacements_csv, client_name)

    # Step 5: Upload to Google Sheets
    sheet_url = upload_to_google_sheets(review_csv, client_name)

    print("\n" + "="*80)
    print("✅ WORKFLOW COMPLETE")
    print("="*80)
    print(f"Files saved in: /clients/{client_name}/data/pmax/")
    print(f"Google Sheet: {sheet_url}")
    print("\nNext step: Client reviews and selects options in the Google Sheet")
    print("="*80)

if __name__ == "__main__":
    main()
