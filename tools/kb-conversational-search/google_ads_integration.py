#!/usr/bin/env python3
"""
Google Ads API Integration for Conversational Search

Direct Google Ads API integration (not via MCP) for Flask web application.
Fetches real-time campaign data to enrich AI strategic recommendations.

Author: PetesBrain
Created: 2025-11-28
"""

import os
import sys
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# Add PetesBrain shared modules to path
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain")
sys.path.insert(0, str(PETESBRAIN_ROOT))

# Import platform IDs helper
try:
    from shared.platform_ids import get_client_ids
    logger.info("✅ Loaded platform_ids helper")
    platform_ids_available = True
except ImportError as e:
    logger.warning(f"⚠️  Could not import platform_ids: {e}")
    platform_ids_available = False
    get_client_ids = None

# Import Google Ads library
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    google_ads_available = True
    logger.info("✅ Loaded Google Ads library")
except ImportError as e:
    logger.error(f"❌ Google Ads library not available: {e}")
    google_ads_available = False
    GoogleAdsClient = None
    GoogleAdsException = Exception


# Google Ads OAuth configuration
GOOGLE_ADS_DEVELOPER_TOKEN = "VrzEP-PTSY01pm1BJidERQ"
GOOGLE_ADS_OAUTH_PATH = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json"
GOOGLE_ADS_TOKEN_PATH = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/google_ads_token.json"


class GoogleAdsCampaignDataClient:
    """
    Client for fetching campaign data directly from Google Ads API

    Uses OAuth credentials from MCP server directory for authentication.
    Reads platform IDs from client CONTEXT.md files.
    """

    def __init__(self):
        self.cache = {}  # In-memory cache for session
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Google Ads API client with OAuth credentials"""
        if not google_ads_available:
            logger.error("Google Ads library not available")
            return

        try:
            # Build credentials dict for GoogleAdsClient
            credentials = {
                "developer_token": GOOGLE_ADS_DEVELOPER_TOKEN,
                "use_proto_plus": True,
                "client_id": None,  # Will be loaded from credentials.json
                "client_secret": None,
                "refresh_token": None,
            }

            # Load OAuth credentials
            if os.path.exists(GOOGLE_ADS_OAUTH_PATH):
                with open(GOOGLE_ADS_OAUTH_PATH, 'r') as f:
                    oauth_creds = json.load(f)
                    if 'installed' in oauth_creds:
                        credentials['client_id'] = oauth_creds['installed']['client_id']
                        credentials['client_secret'] = oauth_creds['installed']['client_secret']

            # Load refresh token
            if os.path.exists(GOOGLE_ADS_TOKEN_PATH):
                with open(GOOGLE_ADS_TOKEN_PATH, 'r') as f:
                    token_data = json.load(f)
                    credentials['refresh_token'] = token_data.get('refresh_token')

            # Create client
            self.client = GoogleAdsClient.load_from_dict(credentials)
            logger.info("✅ Google Ads API client initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Google Ads client: {e}")
            self.client = None

    def get_client_platform_ids(self, client_slug: str) -> Optional[Dict[str, str]]:
        """
        Get platform IDs by parsing client CONTEXT.md directly

        This reads the CONTEXT.md file and extracts Google Ads customer IDs
        from the "ALWAYS query all X accounts" section.
        """
        try:
            context_path = PETESBRAIN_ROOT / "clients" / client_slug / "CONTEXT.md"
            if not context_path.exists():
                logger.error(f"CONTEXT.md not found for {client_slug}")
                return None

            with open(context_path, 'r') as f:
                content = f.read()

            # Parse Google Ads customer IDs
            # Look for patterns like "UK: 8573235780" or "- 8573235780"
            import re
            customer_ids = []

            # Match "UK: 8573235780" or similar patterns
            for match in re.finditer(r'(?:UK|USA|EUR|ROW|Customer ID):\s*(\d{10})', content):
                customer_ids.append(match.group(1))

            # Also match standalone 10-digit IDs in list format
            for match in re.finditer(r'^\s*-\s*(\d{10})\s*$', content, re.MULTILINE):
                if match.group(1) not in customer_ids:
                    customer_ids.append(match.group(1))

            # Look for manager ID
            manager_id = None
            manager_match = re.search(r'Manager(?:\s+Account)?\s+ID:?\s*`?(\d{10})`?', content)
            if manager_match:
                manager_id = manager_match.group(1)

            if not customer_ids:
                logger.warning(f"No Google Ads customer IDs found in {client_slug} CONTEXT.md")
                return None

            result = {
                'google_ads_customer_id': customer_ids if len(customer_ids) > 1 else customer_ids[0],
                'google_ads_manager_id': manager_id
            }

            logger.info(f"✅ Parsed {len(customer_ids)} customer IDs for {client_slug}")
            return result

        except Exception as e:
            logger.error(f"Error parsing CONTEXT.md for {client_slug}: {e}")
            return None

    def _run_gaql_query(
        self,
        customer_id: str,
        query: str,
        login_customer_id: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Execute GAQL query against Google Ads API

        Args:
            customer_id: Google Ads customer ID (10 digits)
            query: GAQL query string
            login_customer_id: Manager account ID for managed accounts

        Returns:
            List of result rows as dicts
        """
        if not self.client:
            logger.error("Google Ads client not initialized")
            return None

        # Check cache
        cache_key = f"{customer_id}:{query}"
        if cache_key in self.cache:
            logger.info(f"Using cached result for {customer_id}")
            return self.cache[cache_key]

        try:
            # Create a client with login_customer_id if provided
            if login_customer_id:
                # Build credentials with login_customer_id
                credentials = {
                    "developer_token": GOOGLE_ADS_DEVELOPER_TOKEN,
                    "use_proto_plus": True,
                    "login_customer_id": login_customer_id,
                    "client_id": None,
                    "client_secret": None,
                    "refresh_token": None,
                }

                # Load OAuth credentials
                if os.path.exists(GOOGLE_ADS_OAUTH_PATH):
                    with open(GOOGLE_ADS_OAUTH_PATH, 'r') as f:
                        oauth_creds = json.load(f)
                        if 'installed' in oauth_creds:
                            credentials['client_id'] = oauth_creds['installed']['client_id']
                            credentials['client_secret'] = oauth_creds['installed']['client_secret']

                # Load refresh token
                if os.path.exists(GOOGLE_ADS_TOKEN_PATH):
                    with open(GOOGLE_ADS_TOKEN_PATH, 'r') as f:
                        token_data = json.load(f)
                        credentials['refresh_token'] = token_data.get('refresh_token')

                # Create client with login_customer_id
                client = GoogleAdsClient.load_from_dict(credentials)
                ga_service = client.get_service("GoogleAdsService")
            else:
                ga_service = self.client.get_service("GoogleAdsService")

            # Execute query
            logger.info(f"Executing GAQL query for {customer_id} (login: {login_customer_id})")
            response = ga_service.search(
                customer_id=customer_id,
                query=query
            )

            # Parse results
            results = []
            for row in response:
                # Convert protobuf row to dict
                row_dict = {}

                # Extract metrics
                if hasattr(row, 'metrics'):
                    metrics = row.metrics
                    row_dict['metrics'] = {
                        'cost_micros': metrics.cost_micros,
                        'conversions': metrics.conversions,
                        'conversions_value': metrics.conversions_value,
                        'clicks': metrics.clicks,
                        'impressions': metrics.impressions,
                    }

                # Extract campaign info if present
                if hasattr(row, 'campaign'):
                    campaign = row.campaign
                    row_dict['campaign'] = {
                        'name': campaign.name,
                        'status': campaign.status.name if hasattr(campaign.status, 'name') else str(campaign.status),
                    }

                results.append(row_dict)

            # Cache results
            self.cache[cache_key] = results

            logger.info(f"✅ Retrieved {len(results)} rows from Google Ads")
            return results

        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            for error in ex.failure.errors:
                logger.error(f"  Error: {error.message}")
            return None
        except Exception as e:
            logger.error(f"Error executing GAQL query: {e}")
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

        # Handle multiple accounts (e.g., Smythson has 4 regional accounts)
        if isinstance(customer_id, list):
            customer_ids = customer_id
        else:
            customer_ids = [customer_id]

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

        # Get manager ID
        manager_id = ids.get('google_ads_manager_id')

        # Query all accounts and sum totals
        total_cost_micros = 0
        total_conversions = 0
        total_conversions_value = 0
        total_clicks = 0
        total_impressions = 0

        for cust_id in customer_ids:
            results = self._run_gaql_query(cust_id, query, login_customer_id=manager_id)
            if results and len(results) > 0:
                metrics = results[0].get('metrics', {})
                total_cost_micros += metrics.get('cost_micros', 0)
                total_conversions += metrics.get('conversions', 0)
                total_conversions_value += metrics.get('conversions_value', 0)
                total_clicks += metrics.get('clicks', 0)
                total_impressions += metrics.get('impressions', 0)

        # Convert to readable format
        spend = total_cost_micros / 1_000_000
        revenue = total_conversions_value
        roas = (revenue / spend) if spend > 0 else 0

        return {
            'client': client_slug,
            'platform': 'Google Ads',
            'date_range': f'{start_date} to {end_date}',
            'spend': round(spend, 2),
            'revenue': round(revenue, 2),
            'roas': round(roas, 2),
            'conversions': round(total_conversions, 1),
            'clicks': int(total_clicks),
            'impressions': int(total_impressions),
            'ctr': round((total_clicks / total_impressions * 100) if total_impressions > 0 else 0, 2),
            'cpc': round((spend / total_clicks) if total_clicks > 0 else 0, 2),
            'cpa': round((spend / total_conversions) if total_conversions > 0 else 0, 2)
        }

    def get_campaign_performance(
        self,
        client_slug: str,
        days: int = 7
    ) -> Optional[List[Dict[str, Any]]]:
        """Get per-campaign performance data"""
        ids = self.get_client_platform_ids(client_slug)
        if not ids or not ids.get('google_ads_customer_id'):
            return None

        customer_id = ids['google_ads_customer_id']
        if isinstance(customer_id, list):
            customer_id = customer_id[0]  # Use primary account

        manager_id = ids.get('google_ads_manager_id')

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        query = f'''
            SELECT
                campaign.name,
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
            LIMIT 10
        '''

        results = self._run_gaql_query(customer_id, query, login_customer_id=manager_id)
        if not results:
            return None

        campaigns = []
        for row in results:
            campaign_info = row.get('campaign', {})
            metrics = row.get('metrics', {})

            cost_micros = metrics.get('cost_micros', 0)
            conversions_value = metrics.get('conversions_value', 0)
            conversions = metrics.get('conversions', 0)

            spend = cost_micros / 1_000_000
            revenue = conversions_value
            roas = (revenue / spend) if spend > 0 else 0

            campaigns.append({
                'name': campaign_info.get('name', 'Unknown'),
                'status': campaign_info.get('status', 'UNKNOWN'),
                'spend': round(spend, 2),
                'revenue': round(revenue, 2),
                'roas': round(roas, 2),
                'conversions': round(conversions, 1),
                'clicks': int(metrics.get('clicks', 0)),
                'impressions': int(metrics.get('impressions', 0))
            })

        return campaigns

    def get_complete_client_data(
        self,
        client_slug: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get comprehensive campaign data for a client

        Fetches Google Ads summary and campaign performance

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

        return data


def format_campaign_data_for_prompt(campaign_data: Dict[str, Any]) -> str:
    """
    Format campaign data into readable string for AI prompt

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
            parts.append(f"{i}. **{campaign['name']}**")
            parts.append(f"   - Spend: £{campaign['spend']:,.2f} | Revenue: £{campaign['revenue']:,.2f} | ROAS: {campaign['roas']:.2f}")
            parts.append(f"   - Conversions: {campaign['conversions']} | Clicks: {campaign['clicks']:,}")
        parts.append("")

    # Data availability note
    if not google_ads and not campaigns:
        parts.append("*No campaign data available. Platform IDs may not be configured in client CONTEXT.md.*")

    return "\n".join(parts)


# Initialize client
google_ads_client = GoogleAdsCampaignDataClient()
