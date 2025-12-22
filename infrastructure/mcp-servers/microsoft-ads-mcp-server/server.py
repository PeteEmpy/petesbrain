#!/usr/bin/env python3
"""
Microsoft Ads MCP Server
Using official Bing Ads Python SDK for SOAP-based API access
"""

from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import os
import sys
import logging
import json

# Bing Ads SDK imports
from bingads.service_client import ServiceClient
from bingads.authorization import OAuthDesktopMobileAuthCodeGrant, AuthorizationData
from bingads.v13.reporting import ReportingServiceManager, ReportingDownloadParameters

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get credentials from environment
MICROSOFT_ADS_CLIENT_ID = os.environ.get("MICROSOFT_ADS_CLIENT_ID")
MICROSOFT_ADS_CLIENT_SECRET = os.environ.get("MICROSOFT_ADS_CLIENT_SECRET")
MICROSOFT_ADS_DEVELOPER_TOKEN = os.environ.get("MICROSOFT_ADS_DEVELOPER_TOKEN")
MICROSOFT_ADS_REFRESH_TOKEN = os.environ.get("MICROSOFT_ADS_REFRESH_TOKEN")
MICROSOFT_ADS_CUSTOMER_ID = os.environ.get("MICROSOFT_ADS_CUSTOMER_ID", "")
PLATFORM_IDS_HELPER = os.environ.get("PLATFORM_IDS_HELPER")
CLIENT_IDS_PATH = os.environ.get("CLIENT_IDS_PATH")

# Import platform_ids helper if available
platform_ids = None
if PLATFORM_IDS_HELPER and os.path.exists(PLATFORM_IDS_HELPER):
    try:
        helper_dir = os.path.dirname(os.path.dirname(PLATFORM_IDS_HELPER))
        if helper_dir not in sys.path:
            sys.path.insert(0, helper_dir)
        from shared import platform_ids
    except ImportError as e:
        logging.warning(f"Could not import platform_ids helper: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('microsoft_ads_server')

mcp = FastMCP("Microsoft Ads / Bing Ads Tools")

logger.info("Starting Microsoft Ads / Bing Ads MCP Server with official SDK...")


def get_authorization_data(customer_id: Optional[str] = None, account_id: Optional[str] = None) -> AuthorizationData:
    """
    Create and return authorized AuthorizationData object for Bing Ads API.

    Args:
        customer_id: Optional customer ID (defaults to env variable)
        account_id: Optional account ID

    Returns:
        AuthorizationData: Authenticated authorization object
    """
    if not MICROSOFT_ADS_CLIENT_ID or not MICROSOFT_ADS_CLIENT_SECRET:
        raise ValueError("Microsoft Ads Client ID and Client Secret must be set in environment variables.")

    if not MICROSOFT_ADS_REFRESH_TOKEN:
        raise ValueError("Microsoft Ads Refresh Token must be set. Run OAuth flow first.")

    if not MICROSOFT_ADS_DEVELOPER_TOKEN:
        raise ValueError("Microsoft Ads Developer Token must be set in environment variables.")

    # Use provided IDs or defaults from environment
    cust_id = customer_id or MICROSOFT_ADS_CUSTOMER_ID
    acc_id = account_id

    # Create authorization data
    authorization_data = AuthorizationData(
        account_id=acc_id,
        customer_id=cust_id,
        developer_token=MICROSOFT_ADS_DEVELOPER_TOKEN,
        authentication=None,
    )

    # Set up OAuth
    oauth = OAuthDesktopMobileAuthCodeGrant(client_id=MICROSOFT_ADS_CLIENT_ID)
    oauth.client_secret = MICROSOFT_ADS_CLIENT_SECRET
    oauth.refresh_token = MICROSOFT_ADS_REFRESH_TOKEN

    # Request access token
    oauth.request_oauth_tokens_by_refresh_token(MICROSOFT_ADS_REFRESH_TOKEN)

    # Attach authentication to authorization data
    authorization_data.authentication = oauth

    return authorization_data


@mcp.tool
def list_accounts(ctx: Context = None) -> Dict[str, Any]:
    """
    List all accessible Microsoft Ads accounts.

    NOTE: Due to API permissions, this method requires accounts to be provided manually.
    Users can find their Account ID in the Microsoft Ads UI URL: ?aid=XXXXXXX

    Returns:
        Dict with message about how to find Account IDs
    """
    if ctx:
        ctx.info("Listing Microsoft Ads accounts...")

    return {
        "message": "To find your Account ID, go to Microsoft Ads UI and check the URL",
        "example": "https://ui.ads.microsoft.com/...?aid=1673847",
        "instruction": "The 'aid' parameter is your Account ID",
        "note": "Due to API permissions, automatic account enumeration is not available",
        "default_customer_id": MICROSOFT_ADS_CUSTOMER_ID or "Not set",
        "help": "Set MICROSOFT_ADS_CUSTOMER_ID in .env file for your manager customer ID"
    }


@mcp.tool
def get_campaigns(customer_id: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Get all campaigns for a customer account.

    Args:
        customer_id: Microsoft Ads customer ID (account ID from URL ?aid=XXXXX)

    Returns:
        Dict with campaign list and metadata
    """
    if ctx:
        ctx.info(f"Fetching campaigns for customer {customer_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Get campaigns
        campaigns_response = campaign_service.GetCampaignsByAccountId(
            AccountId=customer_id,
            CampaignType='Search Shopping DynamicSearchAds'
        )

        # Parse response
        campaigns_data = []
        if campaigns_response and hasattr(campaigns_response, 'Campaign'):
            for campaign in campaigns_response.Campaign:
                campaigns_data.append({
                    'id': campaign.Id,
                    'name': campaign.Name,
                    'status': campaign.Status,
                    'budget_type': campaign.BudgetType if hasattr(campaign, 'BudgetType') else None,
                    'daily_budget': campaign.DailyBudget if hasattr(campaign, 'DailyBudget') else None,
                })

        return {
            'customer_id': customer_id,
            'campaign_count': len(campaigns_data),
            'campaigns': campaigns_data
        }

    except Exception as e:
        logger.error(f"Failed to get campaigns: {e}")
        return {
            'error': str(e),
            'customer_id': customer_id
        }


@mcp.tool
def get_campaign_performance(
    customer_id: str,
    campaign_ids: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get campaign performance metrics.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_ids: Optional list of campaign IDs to filter
        start_date: Start date in YYYY-MM-DD format (default: last 30 days)
        end_date: End date in YYYY-MM-DD format (default: today)

    Returns:
        Dict with performance metrics
    """
    if ctx:
        ctx.info(f"Fetching campaign performance for customer {customer_id}...")

    try:
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Parse dates
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

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
        report_request.ReportName = 'Campaign Performance Report'
        report_request.ReturnOnlyCompleteData = False
        report_request.Aggregation = 'Daily'

        # Set up date range
        report_time = report_service.factory.create('ReportTime')

        # Use custom date range
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

        # Set scope (account and campaigns)
        scope = report_service.factory.create('AccountThroughCampaignReportScope')
        scope.AccountIds = report_service.factory.create('ns4:ArrayOflong')
        scope.AccountIds.long = [customer_id]

        if campaign_ids:
            scope.Campaigns = report_service.factory.create('ArrayOfCampaignReportScope')
            for campaign_id in campaign_ids:
                campaign_scope = report_service.factory.create('CampaignReportScope')
                campaign_scope.AccountId = customer_id
                campaign_scope.CampaignId = campaign_id
                scope.Campaigns.CampaignReportScope.append(campaign_scope)

        report_request.Scope = scope

        # Set columns to retrieve
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

        # Download the report
        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory='/tmp',
            result_file_name=f'campaign_performance_{customer_id}.csv',
            overwrite_result_file=True,
            timeout_in_milliseconds=3600000
        )

        if ctx:
            ctx.info("Submitting report request and waiting for download...")

        result_file_path = reporting_service_manager.download_file(
            reporting_download_parameters=reporting_download_parameters
        )

        # Parse the CSV results
        import csv
        performance_data = []

        with open(result_file_path, 'r', encoding='utf-8-sig') as csvfile:
            # Skip metadata rows (first ~10 rows are typically metadata in Bing Ads reports)
            lines = csvfile.readlines()

            # Find the header row (starts with "TimePeriod" or similar)
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
                    performance_data.append({
                        'date': row.get('TimePeriod', ''),
                        'account_id': row.get('AccountId', ''),
                        'campaign_name': row.get('CampaignName', ''),
                        'campaign_id': row.get('CampaignId', ''),
                        'campaign_status': row.get('CampaignStatus', ''),
                        'impressions': int(row.get('Impressions', 0)) if row.get('Impressions') else 0,
                        'clicks': int(row.get('Clicks', 0)) if row.get('Clicks') else 0,
                        'ctr': float(row.get('Ctr', 0)) if row.get('Ctr') else 0.0,
                        'average_cpc': float(row.get('AverageCpc', 0)) if row.get('AverageCpc') else 0.0,
                        'spend': float(row.get('Spend', 0)) if row.get('Spend') else 0.0,
                        'conversions': int(row.get('Conversions', 0)) if row.get('Conversions') else 0,
                        'revenue': float(row.get('Revenue', 0)) if row.get('Revenue') else 0.0,
                        'roas': float(row.get('ReturnOnAdSpend', 0)) if row.get('ReturnOnAdSpend') else 0.0,
                        'cost_per_conversion': float(row.get('CostPerConversion', 0)) if row.get('CostPerConversion') else 0.0,
                        'conversion_rate': float(row.get('ConversionRate', 0)) if row.get('ConversionRate') else 0.0,
                    })

        # Calculate summary metrics
        total_impressions = sum(row['impressions'] for row in performance_data)
        total_clicks = sum(row['clicks'] for row in performance_data)
        total_spend = sum(row['spend'] for row in performance_data)
        total_conversions = sum(row['conversions'] for row in performance_data)
        total_revenue = sum(row['revenue'] for row in performance_data)

        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0
        cost_per_conv = total_spend / total_conversions if total_conversions > 0 else 0
        conv_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

        return {
            'customer_id': customer_id,
            'start_date': start_date,
            'end_date': end_date,
            'summary': {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'spend': round(total_spend, 2),
                'conversions': total_conversions,
                'revenue': round(total_revenue, 2),
                'ctr': round(avg_ctr, 2),
                'average_cpc': round(avg_cpc, 2),
                'roas': round(overall_roas, 2),
                'cost_per_conversion': round(cost_per_conv, 2),
                'conversion_rate': round(conv_rate, 2),
            },
            'daily_performance': performance_data,
            'result_file': result_file_path
        }

    except Exception as e:
        logger.error(f"Failed to get campaign performance: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def get_keywords(
    customer_id: str,
    campaign_id: Optional[str] = None,
    ad_group_id: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get keywords for a campaign or ad group.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_id: Optional campaign ID to filter keywords
        ad_group_id: Optional ad group ID to filter keywords

    Returns:
        Dict with keywords list
    """
    if ctx:
        ctx.info(f"Fetching keywords for customer {customer_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Get ad groups first if filtering by campaign
        ad_group_ids = []
        if campaign_id:
            ad_groups_response = campaign_service.GetAdGroupsByCampaignId(
                CampaignId=campaign_id
            )
            if ad_groups_response and hasattr(ad_groups_response, 'AdGroup'):
                ad_group_ids = [ag.Id for ag in ad_groups_response.AdGroup]
        elif ad_group_id:
            ad_group_ids = [ad_group_id]

        # Get keywords
        keywords_data = []

        if ad_group_ids:
            for ag_id in ad_group_ids:
                try:
                    keywords_response = campaign_service.GetKeywordsByAdGroupId(
                        AdGroupId=ag_id
                    )

                    if keywords_response and hasattr(keywords_response, 'Keyword'):
                        for keyword in keywords_response.Keyword:
                            keywords_data.append({
                                'id': keyword.Id,
                                'ad_group_id': ag_id,
                                'text': keyword.Text,
                                'match_type': keyword.MatchType,
                                'status': keyword.Status,
                                'bid': keyword.Bid.Amount if hasattr(keyword, 'Bid') and keyword.Bid else None,
                                'final_urls': keyword.FinalUrls.string if hasattr(keyword, 'FinalUrls') else []
                            })
                except Exception as e:
                    logger.warning(f"Failed to get keywords for ad group {ag_id}: {e}")
                    continue

        return {
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'ad_group_id': ad_group_id,
            'keyword_count': len(keywords_data),
            'keywords': keywords_data
        }

    except Exception as e:
        logger.error(f"Failed to get keywords: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def get_ad_groups(
    customer_id: str,
    campaign_id: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get ad groups for a customer account or specific campaign.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_id: Optional campaign ID to filter ad groups

    Returns:
        Dict with ad groups list
    """
    if ctx:
        ctx.info(f"Fetching ad groups for customer {customer_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        ad_groups_data = []

        if campaign_id:
            # Get ad groups for specific campaign
            ad_groups_response = campaign_service.GetAdGroupsByCampaignId(
                CampaignId=campaign_id
            )

            if ad_groups_response and hasattr(ad_groups_response, 'AdGroup'):
                for ad_group in ad_groups_response.AdGroup:
                    ad_groups_data.append({
                        'id': ad_group.Id,
                        'campaign_id': campaign_id,
                        'name': ad_group.Name,
                        'status': ad_group.Status,
                        'start_date': str(ad_group.StartDate) if hasattr(ad_group, 'StartDate') else None,
                        'end_date': str(ad_group.EndDate) if hasattr(ad_group, 'EndDate') else None,
                        'network': ad_group.Network if hasattr(ad_group, 'Network') else None,
                        'pricing_model': ad_group.PricingModel if hasattr(ad_group, 'PricingModel') else None,
                        'search_bid': ad_group.SearchBid.Amount if hasattr(ad_group, 'SearchBid') and ad_group.SearchBid else None
                    })
        else:
            # Get all campaigns first, then get ad groups for each
            campaigns_response = campaign_service.GetCampaignsByAccountId(
                AccountId=customer_id,
                CampaignType='Search Shopping DynamicSearchAds'
            )

            if campaigns_response and hasattr(campaigns_response, 'Campaign'):
                for campaign in campaigns_response.Campaign:
                    try:
                        ad_groups_response = campaign_service.GetAdGroupsByCampaignId(
                            CampaignId=campaign.Id
                        )

                        if ad_groups_response and hasattr(ad_groups_response, 'AdGroup'):
                            for ad_group in ad_groups_response.AdGroup:
                                ad_groups_data.append({
                                    'id': ad_group.Id,
                                    'campaign_id': campaign.Id,
                                    'campaign_name': campaign.Name,
                                    'name': ad_group.Name,
                                    'status': ad_group.Status,
                                    'start_date': str(ad_group.StartDate) if hasattr(ad_group, 'StartDate') else None,
                                    'end_date': str(ad_group.EndDate) if hasattr(ad_group, 'EndDate') else None,
                                    'network': ad_group.Network if hasattr(ad_group, 'Network') else None,
                                    'pricing_model': ad_group.PricingModel if hasattr(ad_group, 'PricingModel') else None,
                                    'search_bid': ad_group.SearchBid.Amount if hasattr(ad_group, 'SearchBid') and ad_group.SearchBid else None
                                })
                    except Exception as e:
                        logger.warning(f"Failed to get ad groups for campaign {campaign.Id}: {e}")
                        continue

        return {
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'ad_group_count': len(ad_groups_data),
            'ad_groups': ad_groups_data
        }

    except Exception as e:
        logger.error(f"Failed to get ad groups: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def create_campaign(
    customer_id: str,
    campaign_name: str,
    daily_budget: float,
    campaign_type: str = 'Search',
    status: str = 'Paused',
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create a new Microsoft Ads campaign.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_name: Name for the new campaign
        daily_budget: Daily budget amount
        campaign_type: Campaign type (Search, Shopping, DynamicSearchAds)
        status: Campaign status (Active, Paused)

    Returns:
        Dict with created campaign details
    """
    if ctx:
        ctx.info(f"Creating campaign '{campaign_name}' for customer {customer_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Create campaign object
        campaign = campaign_service.factory.create('Campaign')
        campaign.Name = campaign_name
        campaign.Description = f"Created via MCP on {datetime.now().strftime('%Y-%m-%d')}"
        campaign.BudgetType = 'DailyBudgetStandard'
        campaign.DailyBudget = daily_budget
        campaign.TimeZone = 'GMT'
        campaign.Status = status

        # Set campaign type
        if campaign_type == 'Search':
            campaign.CampaignType = 'Search'
        elif campaign_type == 'Shopping':
            campaign.CampaignType = 'Shopping'
        elif campaign_type == 'DynamicSearchAds':
            campaign.CampaignType = 'DynamicSearchAds'

        # Create campaigns array
        campaigns = campaign_service.factory.create('ArrayOfCampaign')
        campaigns.Campaign.append(campaign)

        # Add campaign
        response = campaign_service.AddCampaigns(
            AccountId=customer_id,
            Campaigns=campaigns
        )

        return {
            'customer_id': customer_id,
            'campaign_id': response.CampaignIds.long[0] if response.CampaignIds else None,
            'campaign_name': campaign_name,
            'daily_budget': daily_budget,
            'status': status,
            'message': 'Campaign created successfully'
        }

    except Exception as e:
        logger.error(f"Failed to create campaign: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def update_campaign_budget(
    customer_id: str,
    campaign_id: str,
    daily_budget: float,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Update the daily budget for a Microsoft Ads campaign.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_id: Campaign ID to update
        daily_budget: New daily budget amount

    Returns:
        Dict with update confirmation
    """
    if ctx:
        ctx.info(f"Updating budget for campaign {campaign_id} to {daily_budget}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Get existing campaign
        get_campaigns = campaign_service.factory.create('ArrayOflong')
        get_campaigns.long.append(campaign_id)

        campaigns_response = campaign_service.GetCampaignsByIds(
            AccountId=customer_id,
            CampaignIds=get_campaigns,
            CampaignType='Search Shopping DynamicSearchAds'
        )

        if not campaigns_response or not hasattr(campaigns_response, 'Campaign'):
            return {'error': 'Campaign not found'}

        campaign = campaigns_response.Campaign[0]

        # Update budget
        campaign.DailyBudget = daily_budget

        # Update campaign
        campaigns_to_update = campaign_service.factory.create('ArrayOfCampaign')
        campaigns_to_update.Campaign.append(campaign)

        campaign_service.UpdateCampaigns(
            AccountId=customer_id,
            Campaigns=campaigns_to_update
        )

        return {
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'campaign_name': campaign.Name,
            'new_daily_budget': daily_budget,
            'message': 'Budget updated successfully'
        }

    except Exception as e:
        logger.error(f"Failed to update campaign budget: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def update_campaign_status(
    customer_id: str,
    campaign_id: str,
    status: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Update the status of a Microsoft Ads campaign.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        campaign_id: Campaign ID to update
        status: New status (Active, Paused, Deleted)

    Returns:
        Dict with update confirmation
    """
    if ctx:
        ctx.info(f"Updating status for campaign {campaign_id} to {status}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Get existing campaign
        get_campaigns = campaign_service.factory.create('ArrayOflong')
        get_campaigns.long.append(campaign_id)

        campaigns_response = campaign_service.GetCampaignsByIds(
            AccountId=customer_id,
            CampaignIds=get_campaigns,
            CampaignType='Search Shopping DynamicSearchAds'
        )

        if not campaigns_response or not hasattr(campaigns_response, 'Campaign'):
            return {'error': 'Campaign not found'}

        campaign = campaigns_response.Campaign[0]

        # Update status
        campaign.Status = status

        # Update campaign
        campaigns_to_update = campaign_service.factory.create('ArrayOfCampaign')
        campaigns_to_update.Campaign.append(campaign)

        campaign_service.UpdateCampaigns(
            AccountId=customer_id,
            Campaigns=campaigns_to_update
        )

        return {
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'campaign_name': campaign.Name,
            'new_status': status,
            'message': 'Status updated successfully'
        }

    except Exception as e:
        logger.error(f"Failed to update campaign status: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'campaign_id': campaign_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def add_keywords(
    customer_id: str,
    ad_group_id: str,
    keywords: List[Dict[str, str]],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Add keywords to a Microsoft Ads ad group.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        ad_group_id: Ad group ID to add keywords to
        keywords: List of keyword dicts with 'text', 'match_type', 'bid' (optional)
                  Match types: Exact, Phrase, Broad

    Returns:
        Dict with added keywords confirmation
    """
    if ctx:
        ctx.info(f"Adding {len(keywords)} keywords to ad group {ad_group_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Create keywords array
        keywords_to_add = campaign_service.factory.create('ArrayOfKeyword')

        for kw_data in keywords:
            keyword = campaign_service.factory.create('Keyword')
            keyword.Text = kw_data['text']
            keyword.MatchType = kw_data.get('match_type', 'Exact')
            keyword.Status = 'Active'

            # Set bid if provided
            if 'bid' in kw_data:
                bid = campaign_service.factory.create('Bid')
                bid.Amount = float(kw_data['bid'])
                keyword.Bid = bid

            keywords_to_add.Keyword.append(keyword)

        # Add keywords
        response = campaign_service.AddKeywords(
            AdGroupId=ad_group_id,
            Keywords=keywords_to_add
        )

        keyword_ids = []
        if response.KeywordIds:
            keyword_ids = response.KeywordIds.long if hasattr(response.KeywordIds, 'long') else []

        return {
            'customer_id': customer_id,
            'ad_group_id': ad_group_id,
            'keywords_added': len(keyword_ids),
            'keyword_ids': keyword_ids,
            'message': f'Successfully added {len(keyword_ids)} keywords'
        }

    except Exception as e:
        logger.error(f"Failed to add keywords: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'ad_group_id': ad_group_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def pause_keywords(
    customer_id: str,
    ad_group_id: str,
    keyword_ids: List[str],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Pause keywords in a Microsoft Ads ad group.

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        ad_group_id: Ad group ID containing the keywords
        keyword_ids: List of keyword IDs to pause

    Returns:
        Dict with pause confirmation
    """
    if ctx:
        ctx.info(f"Pausing {len(keyword_ids)} keywords in ad group {ad_group_id}...")

    try:
        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

        # Create Campaign Management service
        campaign_service = ServiceClient(
            service='CampaignManagementService',
            version=13,
            authorization_data=authorization_data,
        )

        # Get existing keywords
        get_keyword_ids = campaign_service.factory.create('ArrayOflong')
        for kw_id in keyword_ids:
            get_keyword_ids.long.append(kw_id)

        keywords_response = campaign_service.GetKeywordsByIds(
            AdGroupId=ad_group_id,
            KeywordIds=get_keyword_ids
        )

        if not keywords_response or not hasattr(keywords_response, 'Keyword'):
            return {'error': 'Keywords not found'}

        # Update status to Paused
        keywords_to_update = campaign_service.factory.create('ArrayOfKeyword')
        for keyword in keywords_response.Keyword:
            keyword.Status = 'Paused'
            keywords_to_update.Keyword.append(keyword)

        # Update keywords
        campaign_service.UpdateKeywords(
            AdGroupId=ad_group_id,
            Keywords=keywords_to_update
        )

        return {
            'customer_id': customer_id,
            'ad_group_id': ad_group_id,
            'keywords_paused': len(keyword_ids),
            'keyword_ids': keyword_ids,
            'message': f'Successfully paused {len(keyword_ids)} keywords'
        }

    except Exception as e:
        logger.error(f"Failed to pause keywords: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'ad_group_id': ad_group_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def get_search_terms(
    customer_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    campaign_ids: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get search term performance report (search queries that triggered ads).

    Args:
        customer_id: Microsoft Ads customer ID (account ID)
        start_date: Start date in YYYY-MM-DD format (default: last 30 days)
        end_date: End date in YYYY-MM-DD format (default: today)
        campaign_ids: Optional list of campaign IDs to filter

    Returns:
        Dict with search term performance data
    """
    if ctx:
        ctx.info(f"Fetching search terms for customer {customer_id}...")

    try:
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Parse dates
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        # Get authorization
        authorization_data = get_authorization_data(account_id=customer_id)

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

        # Build Search Query Performance Report Request
        report_request = report_service.factory.create('SearchQueryPerformanceReportRequest')
        report_request.Format = 'Csv'
        report_request.ReportName = 'Search Query Performance Report'
        report_request.ReturnOnlyCompleteData = False
        report_request.Aggregation = 'Summary'

        # Set up date range
        report_time = report_service.factory.create('ReportTime')

        # Use custom date range
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
        scope = report_service.factory.create('AccountThroughAdGroupReportScope')
        scope.AccountIds = report_service.factory.create('ns4:ArrayOflong')
        scope.AccountIds.long = [customer_id]

        if campaign_ids:
            scope.Campaigns = report_service.factory.create('ArrayOfCampaignReportScope')
            for campaign_id in campaign_ids:
                campaign_scope = report_service.factory.create('CampaignReportScope')
                campaign_scope.AccountId = customer_id
                campaign_scope.CampaignId = campaign_id
                scope.Campaigns.CampaignReportScope.append(campaign_scope)

        report_request.Scope = scope

        # Set columns
        columns = report_service.factory.create('ArrayOfSearchQueryPerformanceReportColumn')
        columns.SearchQueryPerformanceReportColumn.append([
            'AccountId',
            'CampaignName',
            'CampaignId',
            'AdGroupName',
            'AdGroupId',
            'SearchQuery',
            'Keyword',
            'MatchType',
            'Impressions',
            'Clicks',
            'Ctr',
            'AverageCpc',
            'Spend',
            'Conversions',
            'Revenue',
            'ReturnOnAdSpend',
        ])
        report_request.Columns = columns

        # Download the report
        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory='/tmp',
            result_file_name=f'search_terms_{customer_id}.csv',
            overwrite_result_file=True,
            timeout_in_milliseconds=3600000
        )

        if ctx:
            ctx.info("Submitting search terms report request...")

        result_file_path = reporting_service_manager.download_file(
            reporting_download_parameters=reporting_download_parameters
        )

        # Parse the CSV results
        import csv
        search_terms_data = []

        with open(result_file_path, 'r', encoding='utf-8-sig') as csvfile:
            lines = csvfile.readlines()

            # Find the header row
            header_index = 0
            for i, line in enumerate(lines):
                if line.startswith('AccountId') or line.startswith('"AccountId"'):
                    header_index = i
                    break

            # Parse from header onwards
            csv_reader = csv.DictReader(lines[header_index:])

            for row in csv_reader:
                # Skip summary rows
                if row.get('SearchQuery'):
                    search_terms_data.append({
                        'account_id': row.get('AccountId', ''),
                        'campaign_name': row.get('CampaignName', ''),
                        'campaign_id': row.get('CampaignId', ''),
                        'ad_group_name': row.get('AdGroupName', ''),
                        'ad_group_id': row.get('AdGroupId', ''),
                        'search_query': row.get('SearchQuery', ''),
                        'keyword': row.get('Keyword', ''),
                        'match_type': row.get('MatchType', ''),
                        'impressions': int(row.get('Impressions', 0)) if row.get('Impressions') else 0,
                        'clicks': int(row.get('Clicks', 0)) if row.get('Clicks') else 0,
                        'ctr': float(row.get('Ctr', 0)) if row.get('Ctr') else 0.0,
                        'average_cpc': float(row.get('AverageCpc', 0)) if row.get('AverageCpc') else 0.0,
                        'spend': float(row.get('Spend', 0)) if row.get('Spend') else 0.0,
                        'conversions': int(row.get('Conversions', 0)) if row.get('Conversions') else 0,
                        'revenue': float(row.get('Revenue', 0)) if row.get('Revenue') else 0.0,
                        'roas': float(row.get('ReturnOnAdSpend', 0)) if row.get('ReturnOnAdSpend') else 0.0,
                    })

        # Calculate summary
        total_impressions = sum(row['impressions'] for row in search_terms_data)
        total_clicks = sum(row['clicks'] for row in search_terms_data)
        total_spend = sum(row['spend'] for row in search_terms_data)
        total_conversions = sum(row['conversions'] for row in search_terms_data)
        total_revenue = sum(row['revenue'] for row in search_terms_data)

        return {
            'customer_id': customer_id,
            'start_date': start_date,
            'end_date': end_date,
            'search_term_count': len(search_terms_data),
            'summary': {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'spend': round(total_spend, 2),
                'conversions': total_conversions,
                'revenue': round(total_revenue, 2),
                'ctr': round((total_clicks / total_impressions * 100) if total_impressions > 0 else 0, 2),
                'average_cpc': round(total_spend / total_clicks if total_clicks > 0 else 0, 2),
                'roas': round(total_revenue / total_spend if total_spend > 0 else 0, 2),
            },
            'search_terms': search_terms_data,
            'result_file': result_file_path
        }

    except Exception as e:
        logger.error(f"Failed to get search terms: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            'error': str(e),
            'customer_id': customer_id,
            'traceback': traceback.format_exc()
        }


@mcp.tool
def get_client_platform_ids(client_name: str, ctx: Context = None) -> Dict[str, Any]:
    """
    Get platform IDs for a specific client from their CONTEXT.md file.

    Args:
        client_name: Client name (e.g., 'smythson', 'tree2mydoor')

    Returns:
        Dictionary with platform IDs including Microsoft Ads account ID
    """
    if ctx:
        ctx.info(f"Getting platform IDs for client: {client_name}")

    if platform_ids:
        try:
            result = platform_ids.get_client_platform_ids(client_name)
            return result
        except Exception as e:
            logger.error(f"Failed to get platform IDs: {e}")
            return {'error': str(e)}
    else:
        return {
            'error': 'Platform IDs helper not available',
            'note': 'PLATFORM_IDS_HELPER path not configured in .env'
        }


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
