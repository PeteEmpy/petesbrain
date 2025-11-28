#!/usr/bin/env python3
"""
Meta (Facebook) Ads MCP Server

A FastMCP-powered Model Context Protocol server for Meta Marketing API integration
with OAuth 2.0 authentication, following PetesBrain patterns.
"""

from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import logging
import requests
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import OAuth modules
from oauth.meta_auth import get_headers_with_auto_token, format_account_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('meta_ads_server')

# Constants
META_API_VERSION = "v22.0"
META_GRAPH_URL = f"https://graph.facebook.com/{META_API_VERSION}"

# Create FastMCP server
mcp = FastMCP("Meta Ads Tools")

# Server startup
logger.info("Starting Meta Ads MCP Server...")


def make_api_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET"
) -> Dict[str, Any]:
    """
    Make a request to Meta Marketing API with automatic authentication.
    
    Args:
        endpoint: API endpoint (e.g., '/me/adaccounts')
        params: Query parameters
        method: HTTP method (GET or POST)
    
    Returns:
        Dict with API response
    """
    headers, access_token = get_headers_with_auto_token()
    
    # Add access token to params
    if params is None:
        params = {}
    params['access_token'] = access_token
    
    # Build full URL
    if endpoint.startswith('http'):
        url = endpoint
    else:
        endpoint = endpoint.lstrip('/')
        url = f"{META_GRAPH_URL}/{endpoint}"
    
    # Make request
    if method.upper() == "GET":
        response = requests.get(url, params=params, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(url, params=params, headers=headers, json={})
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    if not response.ok:
        error_msg = f"API request failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    return response.json()


def paginate_results(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Fetch all pages of results from a paginated endpoint.
    
    Args:
        endpoint: API endpoint
        params: Query parameters
        limit: Maximum number of results to return
    
    Returns:
        List of all results
    """
    all_results = []
    
    result = make_api_request(endpoint, params)
    
    if 'data' in result:
        all_results.extend(result['data'])
    
    # Follow pagination
    while 'paging' in result and 'next' in result['paging']:
        if limit and len(all_results) >= limit:
            break
        
        result = make_api_request(result['paging']['next'])
        if 'data' in result:
            all_results.extend(result['data'])
    
    # Trim to limit if specified
    if limit and len(all_results) > limit:
        all_results = all_results[:limit]
    
    return all_results


@mcp.tool
def list_ad_accounts(ctx: Context = None) -> Dict[str, Any]:
    """
    List all ad accounts accessible to the authenticated user.
    
    Returns:
        Dict with list of ad accounts and their basic information
    """
    if ctx:
        ctx.info("Fetching accessible ad accounts...")
    
    try:
        # Get user's ad accounts
        params = {
            'fields': ','.join([
                'account_id',
                'name',
                'account_status',
                'currency',
                'business_name',
                'timezone_name',
                'amount_spent',
                'balance',
                'age'
            ])
        }
        
        accounts = paginate_results('me/adaccounts', params)
        
        if ctx:
            ctx.info(f"Found {len(accounts)} ad accounts")
        
        return {
            'accounts': accounts,
            'total_accounts': len(accounts)
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error listing ad accounts: {str(e)}")
        raise


@mcp.tool
def get_account_details(
    account_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific ad account.
    
    Args:
        account_id: Ad account ID (with or without 'act_' prefix)
    
    Returns:
        Dict with account details
    """
    account_id = format_account_id(account_id)
    
    if ctx:
        ctx.info(f"Fetching details for account {account_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'account_id',
                'name',
                'account_status',
                'currency',
                'business_name',
                'business',
                'timezone_name',
                'amount_spent',
                'balance',
                'spend_cap',
                'age',
                'created_time',
                'min_campaign_group_spend_cap',
                'min_daily_budget'
            ])
        }
        
        result = make_api_request(account_id, params)
        
        if ctx:
            ctx.info(f"Retrieved account details for {result.get('name', account_id)}")
        
        return result
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching account details: {str(e)}")
        raise


@mcp.tool
def get_campaigns(
    account_id: str,
    status_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get campaigns for an ad account.
    
    Args:
        account_id: Ad account ID (with or without 'act_' prefix)
        status_filter: Optional list of statuses to filter by (ACTIVE, PAUSED, DELETED, ARCHIVED)
        limit: Maximum number of campaigns to return
    
    Returns:
        Dict with list of campaigns
    """
    account_id = format_account_id(account_id)
    
    if ctx:
        ctx.info(f"Fetching campaigns for account {account_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'id',
                'name',
                'status',
                'objective',
                'created_time',
                'start_time',
                'stop_time',
                'updated_time',
                'daily_budget',
                'lifetime_budget',
                'budget_remaining',
                'buying_type'
            ])
        }
        
        # Add status filter if provided
        if status_filter:
            params['filtering'] = json.dumps([{
                'field': 'status',
                'operator': 'IN',
                'value': status_filter
            }])
        
        if limit:
            params['limit'] = limit
        
        campaigns = paginate_results(f'{account_id}/campaigns', params, limit)
        
        if ctx:
            ctx.info(f"Found {len(campaigns)} campaigns")
        
        return {
            'campaigns': campaigns,
            'total_campaigns': len(campaigns),
            'account_id': account_id
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching campaigns: {str(e)}")
        raise


@mcp.tool
def get_campaign_insights(
    campaign_id: str,
    date_preset: str = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    breakdowns: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get performance insights for a specific campaign.
    
    Args:
        campaign_id: Campaign ID
        date_preset: Date preset (today, yesterday, last_7d, last_30d, etc.)
        time_range: Custom time range as dict with 'since' and 'until' (YYYY-MM-DD format)
        breakdowns: Optional breakdowns (e.g., ['age', 'gender', 'device_platform'])
    
    Returns:
        Dict with campaign insights
    """
    if ctx:
        ctx.info(f"Fetching insights for campaign {campaign_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'impressions',
                'clicks',
                'spend',
                'reach',
                'frequency',
                'cpc',
                'cpm',
                'cpp',
                'ctr',
                'actions',
                'action_values',
                'conversions',
                'conversion_values',
                'cost_per_action_type',
                'cost_per_conversion'
            ]),
            'level': 'campaign'
        }
        
        # Add time parameters
        if time_range:
            params['time_range'] = json.dumps(time_range)
        else:
            params['date_preset'] = date_preset
        
        # Add breakdowns if provided
        if breakdowns:
            params['breakdowns'] = ','.join(breakdowns)
        
        insights = paginate_results(f'{campaign_id}/insights', params)
        
        if ctx:
            ctx.info(f"Retrieved {len(insights)} insight records")
        
        return {
            'insights': insights,
            'campaign_id': campaign_id,
            'date_preset': date_preset if not time_range else None,
            'time_range': time_range
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching campaign insights: {str(e)}")
        raise


@mcp.tool
def get_adsets(
    campaign_id: str,
    status_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get ad sets for a specific campaign.
    
    Args:
        campaign_id: Campaign ID
        status_filter: Optional list of statuses to filter by (ACTIVE, PAUSED, DELETED, ARCHIVED)
        limit: Maximum number of ad sets to return
    
    Returns:
        Dict with list of ad sets
    """
    if ctx:
        ctx.info(f"Fetching ad sets for campaign {campaign_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'id',
                'name',
                'status',
                'created_time',
                'start_time',
                'end_time',
                'updated_time',
                'daily_budget',
                'lifetime_budget',
                'budget_remaining',
                'optimization_goal',
                'billing_event',
                'bid_amount',
                'targeting'
            ])
        }
        
        # Add status filter if provided
        if status_filter:
            params['filtering'] = json.dumps([{
                'field': 'status',
                'operator': 'IN',
                'value': status_filter
            }])
        
        if limit:
            params['limit'] = limit
        
        adsets = paginate_results(f'{campaign_id}/adsets', params, limit)
        
        if ctx:
            ctx.info(f"Found {len(adsets)} ad sets")
        
        return {
            'adsets': adsets,
            'total_adsets': len(adsets),
            'campaign_id': campaign_id
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching ad sets: {str(e)}")
        raise


@mcp.tool
def get_adset_insights(
    adset_id: str,
    date_preset: str = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    breakdowns: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get performance insights for a specific ad set.
    
    Args:
        adset_id: Ad set ID
        date_preset: Date preset (today, yesterday, last_7d, last_30d, etc.)
        time_range: Custom time range as dict with 'since' and 'until' (YYYY-MM-DD format)
        breakdowns: Optional breakdowns (e.g., ['age', 'gender', 'device_platform'])
    
    Returns:
        Dict with ad set insights
    """
    if ctx:
        ctx.info(f"Fetching insights for ad set {adset_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'impressions',
                'clicks',
                'spend',
                'reach',
                'frequency',
                'cpc',
                'cpm',
                'cpp',
                'ctr',
                'actions',
                'action_values',
                'conversions',
                'conversion_values',
                'cost_per_action_type',
                'cost_per_conversion'
            ]),
            'level': 'adset'
        }
        
        # Add time parameters
        if time_range:
            params['time_range'] = json.dumps(time_range)
        else:
            params['date_preset'] = date_preset
        
        # Add breakdowns if provided
        if breakdowns:
            params['breakdowns'] = ','.join(breakdowns)
        
        insights = paginate_results(f'{adset_id}/insights', params)
        
        if ctx:
            ctx.info(f"Retrieved {len(insights)} insight records")
        
        return {
            'insights': insights,
            'adset_id': adset_id,
            'date_preset': date_preset if not time_range else None,
            'time_range': time_range
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching ad set insights: {str(e)}")
        raise


@mcp.tool
def get_ads(
    adset_id: str,
    status_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get ads for a specific ad set.
    
    Args:
        adset_id: Ad set ID
        status_filter: Optional list of statuses to filter by (ACTIVE, PAUSED, DELETED, ARCHIVED)
        limit: Maximum number of ads to return
    
    Returns:
        Dict with list of ads
    """
    if ctx:
        ctx.info(f"Fetching ads for ad set {adset_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'id',
                'name',
                'status',
                'created_time',
                'updated_time',
                'creative',
                'effective_status',
                'last_updated_by_app_id'
            ])
        }
        
        # Add status filter if provided
        if status_filter:
            params['filtering'] = json.dumps([{
                'field': 'status',
                'operator': 'IN',
                'value': status_filter
            }])
        
        if limit:
            params['limit'] = limit
        
        ads = paginate_results(f'{adset_id}/ads', params, limit)
        
        if ctx:
            ctx.info(f"Found {len(ads)} ads")
        
        return {
            'ads': ads,
            'total_ads': len(ads),
            'adset_id': adset_id
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching ads: {str(e)}")
        raise


@mcp.tool
def get_ad_insights(
    ad_id: str,
    date_preset: str = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    breakdowns: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get performance insights for a specific ad.
    
    Args:
        ad_id: Ad ID
        date_preset: Date preset (today, yesterday, last_7d, last_30d, etc.)
        time_range: Custom time range as dict with 'since' and 'until' (YYYY-MM-DD format)
        breakdowns: Optional breakdowns (e.g., ['age', 'gender', 'device_platform'])
    
    Returns:
        Dict with ad insights
    """
    if ctx:
        ctx.info(f"Fetching insights for ad {ad_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'impressions',
                'clicks',
                'spend',
                'reach',
                'frequency',
                'cpc',
                'cpm',
                'cpp',
                'ctr',
                'actions',
                'action_values',
                'conversions',
                'conversion_values',
                'cost_per_action_type',
                'cost_per_conversion',
                'video_thruplay_watched_actions',
                'video_p100_watched_actions'
            ]),
            'level': 'ad'
        }
        
        # Add time parameters
        if time_range:
            params['time_range'] = json.dumps(time_range)
        else:
            params['date_preset'] = date_preset
        
        # Add breakdowns if provided
        if breakdowns:
            params['breakdowns'] = ','.join(breakdowns)
        
        insights = paginate_results(f'{ad_id}/insights', params)
        
        if ctx:
            ctx.info(f"Retrieved {len(insights)} insight records")
        
        return {
            'insights': insights,
            'ad_id': ad_id,
            'date_preset': date_preset if not time_range else None,
            'time_range': time_range
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching ad insights: {str(e)}")
        raise


@mcp.tool
def get_account_insights(
    account_id: str,
    date_preset: str = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    level: str = "account",
    breakdowns: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get performance insights for an ad account.
    
    Args:
        account_id: Ad account ID (with or without 'act_' prefix)
        date_preset: Date preset (today, yesterday, last_7d, last_30d, etc.)
        time_range: Custom time range as dict with 'since' and 'until' (YYYY-MM-DD format)
        level: Aggregation level (account, campaign, adset, ad)
        breakdowns: Optional breakdowns (e.g., ['age', 'gender', 'device_platform'])
    
    Returns:
        Dict with account insights
    """
    account_id = format_account_id(account_id)
    
    if ctx:
        ctx.info(f"Fetching insights for account {account_id}...")
    
    try:
        params = {
            'fields': ','.join([
                'impressions',
                'clicks',
                'spend',
                'reach',
                'frequency',
                'cpc',
                'cpm',
                'cpp',
                'ctr',
                'actions',
                'action_values',
                'conversions',
                'conversion_values',
                'cost_per_action_type',
                'cost_per_conversion',
                'campaign_name',
                'adset_name',
                'ad_name'
            ]),
            'level': level
        }
        
        # Add time parameters
        if time_range:
            params['time_range'] = json.dumps(time_range)
        else:
            params['date_preset'] = date_preset
        
        # Add breakdowns if provided
        if breakdowns:
            params['breakdowns'] = ','.join(breakdowns)
        
        insights = paginate_results(f'{account_id}/insights', params)
        
        if ctx:
            ctx.info(f"Retrieved {len(insights)} insight records")
        
        return {
            'insights': insights,
            'account_id': account_id,
            'date_preset': date_preset if not time_range else None,
            'time_range': time_range,
            'level': level
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching account insights: {str(e)}")
        raise


@mcp.tool
def run_custom_insights_query(
    object_id: str,
    fields: List[str],
    date_preset: str = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    level: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    filtering: Optional[List[Dict]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Run a custom insights query with full control over parameters.
    
    Args:
        object_id: ID of object to query (account, campaign, adset, or ad)
        fields: List of fields to retrieve (e.g., ['impressions', 'clicks', 'spend'])
        date_preset: Date preset (today, yesterday, last_7d, last_30d, etc.)
        time_range: Custom time range as dict with 'since' and 'until' (YYYY-MM-DD format)
        level: Optional aggregation level (account, campaign, adset, ad)
        breakdowns: Optional breakdowns (e.g., ['age', 'gender', 'device_platform'])
        filtering: Optional filtering conditions
    
    Returns:
        Dict with query results
    """
    if ctx:
        ctx.info(f"Running custom insights query for {object_id}...")
    
    try:
        params = {
            'fields': ','.join(fields)
        }
        
        # Add time parameters
        if time_range:
            params['time_range'] = json.dumps(time_range)
        else:
            params['date_preset'] = date_preset
        
        # Add optional parameters
        if level:
            params['level'] = level
        if breakdowns:
            params['breakdowns'] = ','.join(breakdowns)
        if filtering:
            params['filtering'] = json.dumps(filtering)
        
        insights = paginate_results(f'{object_id}/insights', params)
        
        if ctx:
            ctx.info(f"Retrieved {len(insights)} insight records")
        
        return {
            'insights': insights,
            'object_id': object_id,
            'query_params': params
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error running custom insights query: {str(e)}")
        raise


@mcp.tool
def get_audience_insights(
    account_id: str,
    targeting_spec: Dict[str, Any],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get audience insights for a specific targeting specification.
    
    Args:
        account_id: Ad account ID (with or without 'act_' prefix)
        targeting_spec: Targeting specification (e.g., interests, demographics)
    
    Returns:
        Dict with audience insights
    """
    account_id = format_account_id(account_id)
    
    if ctx:
        ctx.info(f"Fetching audience insights for account {account_id}...")
    
    try:
        endpoint = f'{account_id}/delivery_estimate'
        params = {
            'targeting_spec': json.dumps(targeting_spec),
            'optimization_goal': 'REACH'
        }
        
        result = make_api_request(endpoint, params, method="GET")
        
        if ctx:
            ctx.info("Successfully retrieved audience insights")
        
        return {
            'delivery_estimate': result,
            'account_id': account_id,
            'targeting_spec': targeting_spec
        }
    
    except Exception as e:
        if ctx:
            ctx.error(f"Error fetching audience insights: {str(e)}")
        raise


@mcp.resource("meta-ads://reference")
def meta_ads_reference() -> str:
    """Meta Marketing API reference documentation."""
    return """
    # Meta (Facebook) Ads API Reference
    
    ## Common Date Presets
    - today
    - yesterday
    - last_7d (last 7 days)
    - last_14d
    - last_30d
    - last_90d
    - this_month
    - last_month
    - this_quarter
    - last_quarter
    - maximum (lifetime)
    
    ## Custom Time Ranges
    Use time_range parameter with format:
    {
        "since": "YYYY-MM-DD",
        "until": "YYYY-MM-DD"
    }
    
    ## Common Insight Fields
    ### Performance Metrics
    - impressions: Number of times ads were shown
    - clicks: Number of clicks on ads
    - spend: Amount spent (in account currency)
    - reach: Number of unique people reached
    - frequency: Average times each person saw the ad
    
    ### Cost Metrics
    - cpc: Cost per click
    - cpm: Cost per 1000 impressions
    - cpp: Cost per 1000 people reached
    - ctr: Click-through rate
    
    ### Conversion Metrics
    - actions: Array of actions taken (likes, shares, conversions, etc.)
    - action_values: Values associated with actions
    - conversions: Total conversions
    - conversion_values: Revenue from conversions
    - cost_per_action_type: Cost per action type
    - cost_per_conversion: Cost per conversion
    
    ### Video Metrics (for video ads)
    - video_thruplay_watched_actions: Videos played to 15s or completion
    - video_p100_watched_actions: Videos played to 100% completion
    
    ## Common Breakdowns
    ### Demographics
    - age: Age range
    - gender: Gender
    
    ### Platform
    - device_platform: Platform (mobile, desktop, etc.)
    - publisher_platform: Facebook, Instagram, Audience Network, Messenger
    - platform_position: Placement within platform (feed, story, etc.)
    
    ### Time
    - hourly_stats_aggregated_by_advertiser_time_zone
    - hourly_stats_aggregated_by_audience_time_zone
    
    ## Status Values
    - ACTIVE: Currently running
    - PAUSED: Paused by user
    - DELETED: Deleted
    - ARCHIVED: Archived
    
    ## Aggregation Levels
    - account: Account level aggregation
    - campaign: Campaign level
    - adset: Ad set level
    - ad: Individual ad level
    
    ## Common Targeting Specifications
    {
        "geo_locations": {
            "countries": ["US"],
            "cities": [{"key": "2490299", "radius": 10, "distance_unit": "mile"}]
        },
        "age_min": 18,
        "age_max": 65,
        "genders": [1, 2],  # 1=male, 2=female
        "interests": [{"id": "6003139266461", "name": "Example Interest"}],
        "behaviors": [{"id": "6002714895372", "name": "Example Behavior"}]
    }
    
    ## Example Queries
    
    ### Get Campaign Performance
    ```
    get_campaign_insights(
        campaign_id="123456789",
        date_preset="last_30d"
    )
    ```
    
    ### Get Account Insights by Campaign
    ```
    get_account_insights(
        account_id="act_123456789",
        date_preset="last_30d",
        level="campaign"
    )
    ```
    
    ### Get Ad Performance with Demographics
    ```
    get_ad_insights(
        ad_id="123456789",
        date_preset="last_7d",
        breakdowns=["age", "gender"]
    )
    ```
    
    ### Custom Query with Filtering
    ```
    run_custom_insights_query(
        object_id="act_123456789",
        fields=["impressions", "clicks", "spend", "campaign_name"],
        date_preset="last_30d",
        level="campaign",
        filtering=[{
            "field": "campaign.delivery_info",
            "operator": "IN",
            "value": ["active"]
        }]
    )
    ```
    """


if __name__ == "__main__":
    import sys
    
    # Check command line arguments for transport mode
    if "--http" in sys.argv:
        logger.info("Starting with HTTP transport on http://127.0.0.1:8001/mcp")
        mcp.run(transport="streamable-http", host="127.0.0.1", port=8001, path="/mcp")
    else:
        # Default to STDIO for Claude Desktop compatibility
        logger.info("Starting with STDIO transport for Claude Desktop")
        mcp.run(transport="stdio")

