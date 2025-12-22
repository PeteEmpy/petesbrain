from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import sys
import logging
import requests
import json
from datetime import datetime, timedelta

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# OAuth module will be imported lazily inside tool functions to prevent
# startup popups when tokens are expired

# Import platform_ids helper if available
PLATFORM_IDS_HELPER = os.environ.get("PLATFORM_IDS_HELPER")
CLIENT_IDS_PATH = os.environ.get("CLIENT_IDS_PATH")

platform_ids = None
if PLATFORM_IDS_HELPER and os.path.exists(PLATFORM_IDS_HELPER):
    try:
        # Add parent directory to sys.path to enable import
        helper_dir = os.path.dirname(os.path.dirname(PLATFORM_IDS_HELPER))
        if helper_dir not in sys.path:
            sys.path.insert(0, helper_dir)
        from shared import platform_ids
    except ImportError as e:
        print(f"Warning: Could not import platform_ids helper: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('google_search_console_server')

mcp = FastMCP("Google Search Console Tools")

# Server startup
logger.info("Starting Google Search Console MCP Server...")

@mcp.tool
def list_sites(ctx: Context = None) -> Dict[str, Any]:
    """List all verified sites/properties in Google Search Console.

    Returns:
        Dictionary with list of verified sites and their permission levels
    """
    if ctx:
        ctx.info("Listing all verified Search Console properties...")

    try:
        # Import OAuth module lazily (only when tool is actually called)
        from oauth.google_auth import get_headers_with_auto_token

        # This will automatically trigger OAuth flow if needed
        headers = get_headers_with_auto_token()

        url = "https://www.googleapis.com/webmasters/v3/sites"

        response = requests.get(url, headers=headers)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to list sites: {response.status_code} {response.reason}")
            raise Exception(f"Search Console API error: {response.status_code} {response.reason} - {response.text}")

        data = response.json()
        sites = data.get('siteEntry', [])

        if ctx:
            ctx.info(f"Found {len(sites)} verified sites")

        return {
            "sites": sites,
            "count": len(sites)
        }

    except Exception as e:
        logger.error(f"Error listing sites: {str(e)}")
        raise

@mcp.tool
def get_performance_data(
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None,
    row_limit: int = 1000,
    start_row: int = 0,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get Search Analytics performance data from Google Search Console.

    Args:
        site_url: Site URL (e.g., 'https://example.com/' or 'sc-domain:example.com')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        dimensions: List of dimensions (query, page, country, device, searchAppearance, date)
        metrics: List of metrics (clicks, impressions, ctr, position) - currently not used by API
        row_limit: Maximum number of rows to return (default 1000, max 25000)
        start_row: Zero-based index of first row (for pagination)

    Returns:
        Performance data with clicks, impressions, CTR, and average position
    """
    if ctx:
        ctx.info(f"Getting Search Console performance data for {site_url} from {start_date} to {end_date}")

    # Set default dimensions if none provided
    if dimensions is None:
        dimensions = ["query"]

    try:
        # Import OAuth module lazily
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        url = f"https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(site_url, safe='')}/searchAnalytics/query"

        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit,
            "startRow": start_row
        }

        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to get performance data: {response.status_code} {response.reason}")
            raise Exception(f"Search Console API error: {response.status_code} {response.reason} - {response.text}")

        data = response.json()
        rows = data.get('rows', [])

        if ctx:
            ctx.info(f"Retrieved {len(rows)} rows of performance data")

        return {
            "rows": rows,
            "responseAggregationType": data.get('responseAggregationType'),
            "rowCount": len(rows)
        }

    except Exception as e:
        logger.error(f"Error getting performance data: {str(e)}")
        raise

@mcp.tool
def inspect_url(
    site_url: str,
    inspection_url: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Inspect a specific URL for indexing status and issues.

    Args:
        site_url: Site URL (e.g., 'https://example.com/' or 'sc-domain:example.com')
        inspection_url: The specific URL to inspect (must be under site_url)

    Returns:
        URL inspection data including index status, crawl info, and any issues
    """
    if ctx:
        ctx.info(f"Inspecting URL {inspection_url} in site {site_url}")

    try:
        # Import OAuth module lazily
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        url = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

        payload = {
            "inspectionUrl": inspection_url,
            "siteUrl": site_url
        }

        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to inspect URL: {response.status_code} {response.reason}")
            raise Exception(f"URL Inspection API error: {response.status_code} {response.reason} - {response.text}")

        data = response.json()

        if ctx:
            ctx.info(f"URL inspection completed")

        return data

    except Exception as e:
        logger.error(f"Error inspecting URL: {str(e)}")
        raise

@mcp.tool
def list_sitemaps(
    site_url: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """List all sitemaps for a site.

    Args:
        site_url: Site URL (e.g., 'https://example.com/' or 'sc-domain:example.com')

    Returns:
        List of sitemaps with their status and metadata
    """
    if ctx:
        ctx.info(f"Listing sitemaps for {site_url}")

    try:
        # Import OAuth module lazily
        from oauth.google_auth import get_headers_with_auto_token

        headers = get_headers_with_auto_token()

        url = f"https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(site_url, safe='')}/sitemaps"

        response = requests.get(url, headers=headers)

        if not response.ok:
            if ctx:
                ctx.error(f"Failed to list sitemaps: {response.status_code} {response.reason}")
            raise Exception(f"Search Console API error: {response.status_code} {response.reason} - {response.text}")

        data = response.json()
        sitemaps = data.get('sitemap', [])

        if ctx:
            ctx.info(f"Found {len(sitemaps)} sitemaps")

        return {
            "sitemaps": sitemaps,
            "count": len(sitemaps)
        }

    except Exception as e:
        logger.error(f"Error listing sitemaps: {str(e)}")
        raise

@mcp.tool
def get_client_platform_ids(
    client_name: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """⚠️ DEPRECATED: Use mcp__platform-ids__get_client_platform_ids() instead.

    This tool is deprecated in favour of the centralised platform-ids MCP server.
    It will be removed in a future version.

    **Recommended Usage:**
    ```python
    # OLD (deprecated):
    mcp__google-search-console__get_client_platform_ids('smythson')

    # NEW (preferred):
    mcp__platform-ids__get_client_platform_ids('smythson')
    ```

    Get Google Search Console URL and other platform IDs for a specific client.

    This tool looks up platform IDs from the client's CONTEXT.md file, providing
    quick access to Search Console property URLs and other platform identifiers.

    Args:
        client_name: Client name (e.g., 'smythson', 'tree2mydoor', 'uno-lighting')

    Returns:
        Dictionary with platform IDs including:
        - search_console_url: Google Search Console property URL
        - google_ads_customer_id: Customer ID(s) for Google Ads API
        - ga4_property_id: Google Analytics 4 property ID
        - merchant_centre_id: Merchant Centre feed ID(s)
    """
    if ctx:
        ctx.warning("⚠️ This tool is deprecated. Use mcp__platform-ids__get_client_platform_ids() instead.")
        ctx.info(f"Looking up platform IDs for {client_name}...")

    try:
        if platform_ids is None:
            raise Exception("Platform IDs helper not available. Please check PLATFORM_IDS_HELPER environment variable.")

        ids = platform_ids.get_client_platform_ids(client_name)

        if ctx:
            ctx.info(f"Retrieved platform IDs for {client_name}")

        return ids

    except Exception as e:
        logger.error(f"Error getting client platform IDs: {str(e)}")
        raise

if __name__ == "__main__":
    mcp.run()
