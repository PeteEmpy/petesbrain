#!/usr/bin/env python3
"""
MCP Integration Module for Conversational Search

Provides access to campaign data from Google Ads, Microsoft Ads, and Google Analytics
through MCP servers to enrich strategic recommendations with real-time data.

Author: PetesBrain
Created: 2025-11-28
"""

import os
import sys
import logging
import subprocess
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# Add PetesBrain shared modules to path
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain")
sys.path.insert(0, str(PETESBRAIN_ROOT))

# Import platform IDs helper - using correct function name
try:
    from shared.platform_ids import get_client_ids
    logger.info("✅ Loaded platform_ids helper")
    platform_ids_available = True
except ImportError as e:
    logger.warning(f"⚠️  Could not import platform_ids: {e}")
    platform_ids_available = False
    get_client_ids = None


class MCPCampaignDataClient:
    """
    Client for fetching campaign data via MCP servers

    Uses mcp__google-ads__, mcp__microsoft-ads__, and mcp__google-analytics__
    tool functions to fetch real-time campaign data for strategic analysis.
    """

    def __init__(self):
        self.cache = {}  # Simple in-memory cache for session

    def get_client_platform_ids(self, client_slug: str) -> Optional[Dict[str, str]]:
        """
        Get platform IDs for a client from CONTEXT.md

        Args:
            client_slug: Client folder name (e.g., 'smythson', 'tree2mydoor')

        Returns:
            Dict with google_ads_customer_id, ga4_property_id, microsoft_ads_account_id
        """
        if not platform_ids_available or not get_client_ids:
            logger.error("platform_ids module not available")
            return None

        try:
            # Use correct function name: get_client_ids
            ids = get_client_ids(client_slug)
            logger.info(f"Retrieved platform IDs for {client_slug}")
            return ids
        except Exception as e:
            logger.error(f"Error getting platform IDs for {client_slug}: {e}")
            return None

    def get_google_ads_summary(
        self,
        client_slug: str,
        days: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Get Google Ads performance summary for a client

        Args:
            client_slug: Client folder name
            days: Number of days of data to fetch

        Returns:
            Dict with spend, revenue, ROAS, conversions, etc.
        """
        # Get platform IDs
        ids = self.get_client_platform_ids(client_slug)
        if not ids or not ids.get('google_ads_customer_id'):
            logger.warning(f"No Google Ads customer ID for {client_slug}")
            return None

        customer_id = ids['google_ads_customer_id']
        manager_id = ids.get('google_ads_manager_id', '')

        # Calculate date range
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        # Build GAQL query (customer-level for accuracy)
        query = f'''
            SELECT
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.clicks,
                metrics.impressions
            FROM customer
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        '''

        try:
            # Call MCP function via subprocess (since we're in Flask, not Claude Code)
            # This is a fallback - ideally we'd use MCP SDK directly
            result = self._call_mcp_tool(
                'google-ads',
                'run_gaql',
                {
                    'customer_id': customer_id,
                    'manager_id': manager_id,
                    'query': query
                }
            )

            if result and 'results' in result:
                rows = result['results']
                if rows:
                    metrics = rows[0].get('metrics', {})

                    cost_micros = float(metrics.get('costMicros', 0))
                    conversions_value = float(metrics.get('conversionsValue', 0))
                    conversions = float(metrics.get('conversions', 0))
                    clicks = int(metrics.get('clicks', 0))
                    impressions = int(metrics.get('impressions', 0))

                    spend = cost_micros / 1_000_000
                    revenue = conversions_value
                    roas = (revenue / spend) if spend > 0 else 0

                    return {
                        'client': client_slug,
                        'platform': 'Google Ads',
                        'date_range': f'{start_date} to {end_date}',
                        'spend': round(spend, 2),
                        'revenue': round(revenue, 2),
                        'roas': round(roas, 2),
                        'conversions': round(conversions, 1),
                        'clicks': clicks,
                        'impressions': impressions,
                        'ctr': round((clicks / impressions * 100) if impressions > 0 else 0, 2),
                        'cpc': round((spend / clicks) if clicks > 0 else 0, 2),
                        'cpa': round((spend / conversions) if conversions > 0 else 0, 2)
                    }

            return None

        except Exception as e:
            logger.error(f"Error fetching Google Ads data for {client_slug}: {e}")
            return None

    def get_campaign_performance(
        self,
        client_slug: str,
        days: int = 7
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get per-campaign performance data

        Args:
            client_slug: Client folder name
            days: Number of days of data

        Returns:
            List of campaign performance dicts
        """
        ids = self.get_client_platform_ids(client_slug)
        if not ids or not ids.get('google_ads_customer_id'):
            return None

        customer_id = ids['google_ads_customer_id']
        manager_id = ids.get('google_ads_manager_id', '')

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        query = f'''
            SELECT
                campaign.name,
                campaign.advertising_channel_type,
                campaign.status,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.clicks,
                metrics.impressions
            FROM campaign
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
                AND campaign.status = 'ENABLED'
            ORDER BY metrics.cost_micros DESC
        '''

        try:
            result = self._call_mcp_tool(
                'google-ads',
                'run_gaql',
                {
                    'customer_id': customer_id,
                    'manager_id': manager_id,
                    'query': query
                }
            )

            if result and 'results' in result:
                campaigns = []
                for row in result['results'][:10]:  # Top 10 campaigns by spend
                    campaign = row.get('campaign', {})
                    metrics = row.get('metrics', {})

                    cost_micros = float(metrics.get('costMicros', 0))
                    conversions_value = float(metrics.get('conversionsValue', 0))
                    conversions = float(metrics.get('conversions', 0))

                    spend = cost_micros / 1_000_000
                    revenue = conversions_value
                    roas = (revenue / spend) if spend > 0 else 0

                    campaigns.append({
                        'name': campaign.get('name', 'Unknown'),
                        'type': campaign.get('advertisingChannelType', 'UNKNOWN'),
                        'spend': round(spend, 2),
                        'revenue': round(revenue, 2),
                        'roas': round(roas, 2),
                        'conversions': round(conversions, 1),
                        'clicks': int(metrics.get('clicks', 0)),
                        'impressions': int(metrics.get('impressions', 0))
                    })

                return campaigns

            return None

        except Exception as e:
            logger.error(f"Error fetching campaign performance for {client_slug}: {e}")
            return None

    def get_ga4_summary(
        self,
        client_slug: str,
        days: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Get Google Analytics 4 summary data

        Args:
            client_slug: Client folder name
            days: Number of days of data

        Returns:
            Dict with sessions, users, conversion metrics
        """
        ids = self.get_client_platform_ids(client_slug)
        if not ids or not ids.get('ga4_property_id'):
            logger.warning(f"No GA4 property ID for {client_slug}")
            return None

        property_id = ids['ga4_property_id']
        if property_id == '[TBD]':
            return None

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        try:
            result = self._call_mcp_tool(
                'google-analytics',
                'run_report',
                {
                    'property_id': property_id,
                    'start_date': start_date,
                    'end_date': end_date,
                    'metrics': ['sessions', 'totalUsers', 'screenPageViews', 'conversions', 'totalRevenue']
                }
            )

            if result and 'rows' in result:
                rows = result['rows']
                if rows:
                    row = rows[0]
                    metric_values = row.get('metricValues', [])

                    if len(metric_values) >= 5:
                        return {
                            'client': client_slug,
                            'platform': 'Google Analytics 4',
                            'date_range': f'{start_date} to {end_date}',
                            'sessions': int(metric_values[0].get('value', 0)),
                            'users': int(metric_values[1].get('value', 0)),
                            'pageviews': int(metric_values[2].get('value', 0)),
                            'conversions': float(metric_values[3].get('value', 0)),
                            'revenue': float(metric_values[4].get('value', 0))
                        }

            return None

        except Exception as e:
            logger.error(f"Error fetching GA4 data for {client_slug}: {e}")
            return None

    def _call_mcp_tool(
        self,
        server_name: str,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Call an MCP tool via subprocess

        This is a workaround for Flask environment. In Claude Code context,
        MCP tools are available directly as functions.

        Args:
            server_name: MCP server name (e.g., 'google-ads')
            tool_name: Tool function name (e.g., 'run_gaql')
            params: Tool parameters

        Returns:
            Tool result as dict
        """
        # Cache key
        cache_key = f"{server_name}:{tool_name}:{json.dumps(params, sort_keys=True)}"
        if cache_key in self.cache:
            logger.info(f"Using cached result for {server_name}.{tool_name}")
            return self.cache[cache_key]

        try:
            # Build MCP call command
            # This uses Claude Code's MCP infrastructure
            cmd = [
                'claude',
                'mcp',
                'call',
                server_name,
                tool_name,
                json.dumps(params)
            ]

            logger.info(f"Calling MCP tool: {server_name}.{tool_name}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Parse JSON response
                output = result.stdout.strip()
                data = json.loads(output)

                # Cache result
                self.cache[cache_key] = data

                logger.info(f"✅ MCP call successful: {server_name}.{tool_name}")
                return data
            else:
                logger.error(f"MCP call failed: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"MCP call timed out: {server_name}.{tool_name}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MCP response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error calling MCP tool: {e}")
            return None

    def get_complete_client_data(
        self,
        client_slug: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get comprehensive campaign data for a client

        Fetches Google Ads summary, campaign performance, and GA4 data

        Args:
            client_slug: Client folder name
            days: Number of days of data

        Returns:
            Dict with all available campaign data
        """
        logger.info(f"Fetching complete campaign data for {client_slug}")

        data = {
            'client': client_slug,
            'timestamp': datetime.now().isoformat(),
            'google_ads_summary': None,
            'campaign_performance': None,
            'ga4_summary': None
        }

        # Fetch Google Ads summary
        google_ads = self.get_google_ads_summary(client_slug, days)
        if google_ads:
            data['google_ads_summary'] = google_ads
            logger.info(f"✅ Got Google Ads data: £{google_ads['spend']} spend, {google_ads['roas']} ROAS")

        # Fetch campaign performance
        campaigns = self.get_campaign_performance(client_slug, days=7)
        if campaigns:
            data['campaign_performance'] = campaigns
            logger.info(f"✅ Got {len(campaigns)} campaigns")

        # Fetch GA4 data
        ga4 = self.get_ga4_summary(client_slug, days)
        if ga4:
            data['ga4_summary'] = ga4
            logger.info(f"✅ Got GA4 data: {ga4['sessions']} sessions")

        return data


def format_campaign_data_for_prompt(campaign_data: Dict[str, Any]) -> str:
    """
    Format campaign data into a readable string for AI prompt

    Args:
        campaign_data: Dict from get_complete_client_data()

    Returns:
        Formatted string for inclusion in AI prompt
    """
    parts = []

    # Header
    parts.append(f"## Real-Time Campaign Data for {campaign_data['client']}")
    parts.append(f"Data retrieved: {campaign_data['timestamp']}\n")

    # Google Ads Summary
    google_ads = campaign_data.get('google_ads_summary')
    if google_ads:
        parts.append("### Google Ads Performance")
        parts.append(f"**Period**: {google_ads['date_range']}")
        parts.append(f"**Spend**: £{google_ads['spend']:,.2f}")
        parts.append(f"**Revenue**: £{google_ads['revenue']:,.2f}")
        parts.append(f"**ROAS**: {google_ads['roas']:.2f}")
        parts.append(f"**Conversions**: {google_ads['conversions']}")
        parts.append(f"**Clicks**: {google_ads['clicks']:,}")
        parts.append(f"**Impressions**: {google_ads['impressions']:,}")
        parts.append(f"**CTR**: {google_ads['ctr']}%")
        parts.append(f"**CPC**: £{google_ads['cpc']:.2f}")
        parts.append(f"**CPA**: £{google_ads['cpa']:.2f}\n")

    # Campaign Performance
    campaigns = campaign_data.get('campaign_performance')
    if campaigns:
        parts.append("### Top Campaigns (Last 7 Days)")
        for i, campaign in enumerate(campaigns[:5], 1):
            parts.append(f"{i}. **{campaign['name']}** ({campaign['type']})")
            parts.append(f"   - Spend: £{campaign['spend']:,.2f} | Revenue: £{campaign['revenue']:,.2f} | ROAS: {campaign['roas']:.2f}")
            parts.append(f"   - Conversions: {campaign['conversions']} | Clicks: {campaign['clicks']:,}")
        parts.append("")

    # GA4 Data
    ga4 = campaign_data.get('ga4_summary')
    if ga4:
        parts.append("### Google Analytics 4")
        parts.append(f"**Period**: {ga4['date_range']}")
        parts.append(f"**Sessions**: {ga4['sessions']:,}")
        parts.append(f"**Users**: {ga4['users']:,}")
        parts.append(f"**Pageviews**: {ga4['pageviews']:,}")
        parts.append(f"**Conversions**: {ga4['conversions']}")
        parts.append(f"**Revenue**: £{ga4['revenue']:,.2f}\n")

    # Data availability note
    if not google_ads and not campaigns and not ga4:
        parts.append("*No campaign data available. Ensure platform IDs are configured in client CONTEXT.md.*")

    return "\n".join(parts)


# Initialize client
mcp_client = MCPCampaignDataClient()
