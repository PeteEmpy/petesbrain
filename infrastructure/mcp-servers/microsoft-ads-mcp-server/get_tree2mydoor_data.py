#!/usr/bin/env python3
"""
Fetch Tree2MyDoor Microsoft Ads performance data
Account ID: 1658737
Date Range: 2025-11-21 to 2025-12-20
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
from bingads.v13.reporting import ReportingServiceManager, ReportingDownloadParameters

# Get credentials
CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")

ACCOUNT_ID = "2001778"  # From URL aid parameter
CUSTOMER_ID = "536777922"  # Manager account
START_DATE = "2025-11-21"
END_DATE = "2025-12-20"

print(f"🌳 Tree2MyDoor Microsoft Ads Performance Report")
print(f"Account ID: {ACCOUNT_ID}")
print(f"Customer ID: {CUSTOMER_ID}")
print(f"Date Range: {START_DATE} to {END_DATE}\n")

# Set up OAuth
oauth = OAuthDesktopMobileAuthCodeGrant(client_id=CLIENT_ID)
oauth.client_secret = CLIENT_SECRET
oauth.refresh_token = REFRESH_TOKEN
oauth.request_oauth_tokens_by_refresh_token(REFRESH_TOKEN)

# Create authorization data
authorization_data = AuthorizationData(
    account_id=ACCOUNT_ID,
    customer_id=CUSTOMER_ID,
    developer_token=DEVELOPER_TOKEN,
    authentication=oauth,
)

print("📋 Step 1: Fetching campaigns...")
try:
    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
    )

    campaigns_response = campaign_service.GetCampaignsByAccountId(
        AccountId=ACCOUNT_ID,
        CampaignType='Search Shopping DynamicSearchAds'
    )

    campaigns = []
    if campaigns_response and hasattr(campaigns_response, 'Campaign'):
        for campaign in campaigns_response.Campaign:
            campaigns.append({
                'id': campaign.Id,
                'name': campaign.Name,
                'status': campaign.Status,
                'budget': campaign.DailyBudget if hasattr(campaign, 'DailyBudget') else None
            })

        print(f"✅ Found {len(campaigns)} campaign(s):\n")
        for camp in campaigns:
            print(f"   • {camp['name']} (ID: {camp['id']}, Status: {camp['status']})")
        print()
    else:
        print("⚠️  No campaigns found\n")

except Exception as e:
    print(f"❌ Error fetching campaigns: {e}\n")
    campaigns = []

print("📊 Step 2: Fetching campaign performance report...")
try:
    # Parse dates
    start_dt = datetime.strptime(START_DATE, '%Y-%m-%d')
    end_dt = datetime.strptime(END_DATE, '%Y-%m-%d')

    # Create Reporting Service Manager
    reporting_service_manager = ReportingServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=5000,
        environment='production',
    )

    # Create ServiceClient for building report request
    report_service = ServiceClient(
        service='ReportingService',
        version=13,
        authorization_data=authorization_data,
    )

    # Build Campaign Performance Report Request
    report_request = report_service.factory.create('CampaignPerformanceReportRequest')
    report_request.Format = 'Csv'
    report_request.ReportName = 'Tree2MyDoor Campaign Performance Report'
    report_request.ReturnOnlyCompleteData = False
    report_request.Aggregation = 'Daily'

    # Set up date range
    report_time = report_service.factory.create('ReportTime')
    custom_start = report_service.factory.create('Date')
    custom_start.Day = start_dt.day
    custom_start.Month = start_dt.month
    custom_start.Year = start_dt.year

    custom_end = report_service.factory.create('Date')
    custom_end.Day = end_dt.day
    custom_end.Month = end_dt.month
    custom_end.Year = end_dt.year

    report_time.CustomDateRangeStart = custom_start
    report_time.CustomDateRangeEnd = custom_end
    report_request.Time = report_time

    # Set scope
    scope = report_service.factory.create('AccountThroughCampaignReportScope')
    # Try direct assignment without factory
    scope.AccountIds = {'long': [int(ACCOUNT_ID)]}
    report_request.Scope = scope

    # Set columns
    columns = report_service.factory.create('ArrayOfCampaignPerformanceReportColumn')
    columns.CampaignPerformanceReportColumn.append([
        'TimePeriod',
        'AccountId',
        'CampaignName',
        'CampaignId',
        'CampaignStatus',
        'Impressions',
        'Clicks',
        'Ctr',
        'AverageCpc',
        'Spend',
        'Conversions',
        'Revenue',
        'ReturnOnAdSpend',
        'CostPerConversion',
        'ConversionRate',
    ])
    report_request.Columns = columns

    print("   Submitting report request...")

    # Download the report
    reporting_download_parameters = ReportingDownloadParameters(
        report_request=report_request,
        result_file_directory='/tmp',
        result_file_name=f'tree2mydoor_campaign_performance.csv',
        overwrite_result_file=True,
        timeout_in_milliseconds=3600000
    )

    result_file_path = reporting_service_manager.download_file(reporting_download_parameters)

    print(f"✅ Report downloaded to: {result_file_path}\n")
    print(f"📄 Parsing performance data...")

    # Parse the CSV results
    import csv
    performance_data = []

    with open(result_file_path, 'r', encoding='utf-8-sig') as csvfile:
        lines = csvfile.readlines()

        # Find the header row
        header_index = 0
        for i, line in enumerate(lines):
            if line.startswith('TimePeriod') or line.startswith('"TimePeriod"'):
                header_index = i
                break

        # Parse from header onwards
        csv_reader = csv.DictReader(lines[header_index:])

        for row in csv_reader:
            # Skip summary rows
            if row.get('TimePeriod') and row['TimePeriod'].lower() != 'total':
                # Helper function to parse values with % symbols
                def parse_float(value):
                    if not value or value == '--':
                        return 0.0
                    # Remove % sign and convert
                    value = str(value).replace('%', '').replace(',', '').strip()
                    try:
                        return float(value)
                    except:
                        return 0.0

                def parse_int(value):
                    if not value or value == '--':
                        return 0
                    value = str(value).replace(',', '').strip()
                    try:
                        return int(value)
                    except:
                        return 0

                performance_data.append({
                    'date': row.get('TimePeriod', ''),
                    'campaign_name': row.get('CampaignName', ''),
                    'campaign_id': row.get('CampaignId', ''),
                    'campaign_status': row.get('CampaignStatus', ''),
                    'impressions': parse_int(row.get('Impressions', 0)),
                    'clicks': parse_int(row.get('Clicks', 0)),
                    'ctr': parse_float(row.get('Ctr', 0)),
                    'average_cpc': parse_float(row.get('AverageCpc', 0)),
                    'spend': parse_float(row.get('Spend', 0)),
                    'conversions': parse_int(row.get('Conversions', 0)),
                    'revenue': parse_float(row.get('Revenue', 0)),
                    'roas': parse_float(row.get('ReturnOnAdSpend', 0)),
                    'cost_per_conversion': parse_float(row.get('CostPerConversion', 0)),
                    'conversion_rate': parse_float(row.get('ConversionRate', 0)),
                })

    # Calculate summary
    total_impressions = sum(row['impressions'] for row in performance_data)
    total_clicks = sum(row['clicks'] for row in performance_data)
    total_spend = sum(row['spend'] for row in performance_data)
    total_conversions = sum(row['conversions'] for row in performance_data)
    total_revenue = sum(row['revenue'] for row in performance_data)

    print(f"✅ Parsed {len(performance_data)} days of data\n")

    print("=" * 60)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"Date Range: {START_DATE} to {END_DATE}")
    print(f"Total Days: {len(set(row['date'] for row in performance_data))}")
    print()
    print(f"Impressions: {total_impressions:,}")
    print(f"Clicks: {total_clicks:,}")
    print(f"CTR: {(total_clicks / total_impressions * 100) if total_impressions > 0 else 0:.2f}%")
    print(f"Avg CPC: £{total_spend / total_clicks if total_clicks > 0 else 0:.2f}")
    print()
    print(f"Spend: £{total_spend:,.2f}")
    print(f"Conversions: {total_conversions}")
    print(f"Revenue: £{total_revenue:,.2f}")
    print(f"ROAS: {total_revenue / total_spend if total_spend > 0 else 0:.2f}x")
    print(f"Cost per Conversion: £{total_spend / total_conversions if total_conversions > 0 else 0:.2f}")
    print(f"Conversion Rate: {(total_conversions / total_clicks * 100) if total_clicks > 0 else 0:.2f}%")
    print("=" * 60)

    # Save summary to JSON
    import json
    summary_data = {
        'account_id': ACCOUNT_ID,
        'date_range': {'start': START_DATE, 'end': END_DATE},
        'campaigns': campaigns,
        'summary': {
            'impressions': total_impressions,
            'clicks': total_clicks,
            'spend': round(total_spend, 2),
            'conversions': total_conversions,
            'revenue': round(total_revenue, 2),
            'ctr': round((total_clicks / total_impressions * 100) if total_impressions > 0 else 0, 2),
            'average_cpc': round(total_spend / total_clicks if total_clicks > 0 else 0, 2),
            'roas': round(total_revenue / total_spend if total_spend > 0 else 0, 2),
            'cost_per_conversion': round(total_spend / total_conversions if total_conversions > 0 else 0, 2),
            'conversion_rate': round((total_conversions / total_clicks * 100) if total_clicks > 0 else 0, 2),
        },
        'daily_performance': performance_data
    }

    json_file = '/tmp/tree2mydoor_microsoft_ads_summary.json'
    with open(json_file, 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n💾 Summary saved to: {json_file}")

except Exception as e:
    print(f"❌ Error fetching performance: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Data collection complete!")
