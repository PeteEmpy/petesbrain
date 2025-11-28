#!/usr/bin/env python3
"""
Platform IDs Helper - Extract Google Ads, Merchant Centre, and GA4 IDs from client CONTEXT.md files.

This module provides utilities to:
1. Parse Platform IDs from CONTEXT.md files
2. Load client IDs from the central JSON mapping
3. Validate and format IDs for API usage

Usage:
    from shared.platform_ids import get_client_ids, get_all_client_ids

    # Get IDs for a specific client
    ids = get_client_ids('smythson')
    print(ids['google_ads_customer_id'])

    # Get all client IDs
    all_ids = get_all_client_ids()
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Union


# Base path for the project
BASE_PATH = Path(__file__).parent.parent
CLIENTS_PATH = BASE_PATH / "clients"
CLIENT_IDS_JSON = BASE_PATH / "shared" / "data" / "client-platform-ids.json"


def normalize_client_name(name: str) -> str:
    """
    Normalize client name to match folder structure.

    Args:
        name: Client name (can be 'Smythson', 'smythson', 'Smythson UK', etc.)

    Returns:
        Normalized folder name (e.g., 'smythson')
    """
    # Convert to lowercase and replace spaces/special chars with hyphens
    normalized = name.lower().strip()
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    normalized = re.sub(r'[-\s]+', '-', normalized)
    return normalized


def parse_context_md_ids(context_path: Path) -> Dict[str, Union[str, List[str]]]:
    """
    Parse Platform IDs section from a CONTEXT.md file.

    Args:
        context_path: Path to the CONTEXT.md file

    Returns:
        Dictionary with parsed IDs:
        {
            'google_ads_customer_id': '1234567890' or ['123', '456'] for multi-account,
            'google_ads_manager_id': '2569949686' (if applicable),
            'merchant_centre_id': '1234567890' or ['123', '456'] for multi-merchant,
            'ga4_property_id': '421301275' or '[TBD]'
        }
    """
    if not context_path.exists():
        raise FileNotFoundError(f"CONTEXT.md not found: {context_path}")

    content = context_path.read_text()
    ids = {}

    # Find Platform IDs section
    platform_section_match = re.search(
        r'\*\*Platform IDs\*\*:(.*?)(?=\n\n|\n\*\*|\Z)',
        content,
        re.DOTALL
    )

    if not platform_section_match:
        return ids

    platform_section = platform_section_match.group(1)

    # Extract Google Ads Customer ID(s)
    # First check if there's a "Google Ads Customer IDs:" section with sub-bullets
    multi_ads_match = re.search(
        r'\*\*Google Ads Customer IDs?\*\*:(.*?)(?=\n- \*\*|\n\*\*|\Z)',
        platform_section,
        re.DOTALL | re.IGNORECASE
    )

    if multi_ads_match:
        ads_section = multi_ads_match.group(1)
        # Extract all numeric IDs (10 digits)
        numeric_ids = re.findall(r'\b\d{10}\b', ads_section)
        if numeric_ids:
            ids['google_ads_customer_id'] = numeric_ids if len(numeric_ids) > 1 else numeric_ids[0]
        elif '[TBD]' in ads_section or 'Multiple' in ads_section:
            # Look for the actual IDs in the description
            id_in_text = re.search(r'Multiple\s*\(([^)]+)\)', ads_section)
            if id_in_text:
                numeric_ids = re.findall(r'\b\d{10}\b', id_in_text.group(1))
                ids['google_ads_customer_id'] = numeric_ids if len(numeric_ids) > 1 else numeric_ids[0] if numeric_ids else '[TBD]'
            else:
                ids['google_ads_customer_id'] = '[TBD]'
    else:
        # Single-line format
        ads_match = re.search(
            r'\*\*Google Ads Customer ID\*\*:\s*([^\n]+)',
            platform_section,
            re.IGNORECASE
        )
        if ads_match:
            ads_text = ads_match.group(1).strip()
            id_match = re.search(r'\b(\d{10})\b', ads_text)
            ids['google_ads_customer_id'] = id_match.group(1) if id_match else '[TBD]'

    # Extract Google Ads Manager ID (if present)
    manager_match = re.search(
        r'\*\*Google Ads Manager (?:Account )?ID\*\*:\s*(\d{10})',
        platform_section,
        re.IGNORECASE
    )
    if manager_match:
        ids['google_ads_manager_id'] = manager_match.group(1)

    # Extract Merchant Centre ID(s)
    # Check for multi-line format with sub-items
    multi_merchant_match = re.search(
        r'\*\*Google Merchant Centre IDs?\*\*:(.*?)(?=\n- \*\*|\n\*\*|\Z)',
        platform_section,
        re.DOTALL | re.IGNORECASE
    )

    if multi_merchant_match:
        merchant_section = multi_merchant_match.group(1)
        # Check for N/A or lead generation
        if 'N/A' in merchant_section or 'Lead generation' in merchant_section:
            ids['merchant_centre_id'] = 'N/A'
        else:
            # Extract all numeric IDs (6-12 digits)
            numeric_ids = re.findall(r'\b\d{6,12}\b', merchant_section)
            if numeric_ids:
                ids['merchant_centre_id'] = numeric_ids if len(numeric_ids) > 1 else numeric_ids[0]
            elif '[TBD]' in merchant_section:
                ids['merchant_centre_id'] = '[TBD]'
    else:
        # Single-line format
        merchant_match = re.search(
            r'\*\*Google Merchant Centre ID\*\*:\s*([^\n]+)',
            platform_section,
            re.IGNORECASE
        )
        if merchant_match:
            merchant_text = merchant_match.group(1).strip()
            if 'N/A' in merchant_text or 'Lead generation' in merchant_text:
                ids['merchant_centre_id'] = 'N/A'
            else:
                id_match = re.search(r'\b(\d{6,12})\b', merchant_text)
                ids['merchant_centre_id'] = id_match.group(1) if id_match else '[TBD]'

    # Extract GA4 Property ID
    ga4_match = re.search(
        r'\*\*Google Analytics 4 \(GA4\)(?: Property ID)?\*\*:\s*([^\n]+)',
        platform_section,
        re.IGNORECASE
    )
    if ga4_match:
        ga4_text = ga4_match.group(1).strip()
        # Extract property ID (can be in format "Property ID: 123456789" or just "123456789")
        if 'Property ID:' in ga4_text:
            id_match = re.search(r'Property ID:\s*(\d{9}|\[TBD\])', ga4_text)
        else:
            id_match = re.search(r'\b(\d{9}|\[TBD\])\b', ga4_text)
        ids['ga4_property_id'] = id_match.group(1) if id_match else '[TBD]'

    # Extract Microsoft Ads Account ID
    msft_ads_match = re.search(
        r'\*\*Microsoft Ads Account ID\*\*:\s*([^\n]+)',
        platform_section,
        re.IGNORECASE
    )
    if msft_ads_match:
        msft_text = msft_ads_match.group(1).strip()
        id_match = re.search(r'\b(\d{8,12})\b', msft_text)
        ids['microsoft_ads_account_id'] = id_match.group(1) if id_match else '[TBD]'

    # Extract Facebook Ads Account ID
    fb_ads_match = re.search(
        r'\*\*Facebook Ads Account ID\*\*:\s*([^\n]+)',
        platform_section,
        re.IGNORECASE
    )
    if fb_ads_match:
        fb_text = fb_ads_match.group(1).strip()
        id_match = re.search(r'\b(\d{15,16})\b', fb_text)
        ids['facebook_ads_account_id'] = id_match.group(1) if id_match else '[TBD]'

    return ids


def get_client_ids(client_name: str, prefer_json: bool = False) -> Dict[str, Union[str, List[str]]]:
    """
    Get Platform IDs for a specific client.

    Args:
        client_name: Client name (e.g., 'smythson', 'tree2mydoor')
        prefer_json: If True, prefer JSON mapping over parsing CONTEXT.md

    Returns:
        Dictionary with client Platform IDs

    Raises:
        FileNotFoundError: If client folder or CONTEXT.md not found
    """
    normalized_name = normalize_client_name(client_name)

    # Try JSON first if preferred
    if prefer_json and CLIENT_IDS_JSON.exists():
        try:
            with open(CLIENT_IDS_JSON, 'r') as f:
                data = json.load(f)
                for client in data.get('clients', []):
                    if normalize_client_name(client['name']) == normalized_name:
                        return {
                            'google_ads_customer_id': client.get('google_ads_customer_id'),
                            'merchant_centre_id': client.get('merchant_centre_id'),
                            'ga4_property_id': client.get('ga4_property_id'),
                            'notes': client.get('notes', '')
                        }
        except (json.JSONDecodeError, KeyError):
            pass  # Fall back to parsing CONTEXT.md

    # Parse from CONTEXT.md
    context_path = CLIENTS_PATH / normalized_name / "CONTEXT.md"
    return parse_context_md_ids(context_path)


def get_all_client_ids(source: str = 'json') -> Dict[str, Dict[str, Union[str, List[str]]]]:
    """
    Get Platform IDs for all clients.

    Args:
        source: 'json' to load from JSON, 'context' to parse all CONTEXT.md files

    Returns:
        Dictionary mapping client names to their Platform IDs
    """
    if source == 'json' and CLIENT_IDS_JSON.exists():
        with open(CLIENT_IDS_JSON, 'r') as f:
            data = json.load(f)
            return {
                normalize_client_name(client['name']): {
                    'google_ads_customer_id': client.get('google_ads_customer_id'),
                    'merchant_centre_id': client.get('merchant_centre_id'),
                    'ga4_property_id': client.get('ga4_property_id'),
                    'display_name': client.get('display_name'),
                    'notes': client.get('notes', '')
                }
                for client in data.get('clients', [])
            }

    # Parse all CONTEXT.md files
    all_ids = {}
    for client_dir in CLIENTS_PATH.iterdir():
        if client_dir.is_dir() and not client_dir.name.startswith(('_', '.')):
            context_path = client_dir / "CONTEXT.md"
            if context_path.exists():
                try:
                    all_ids[client_dir.name] = parse_context_md_ids(context_path)
                except Exception as e:
                    print(f"Warning: Could not parse {client_dir.name}: {e}")

    return all_ids


def get_google_ads_accounts() -> List[Dict[str, str]]:
    """
    Get list of all Google Ads accounts with customer IDs.

    Returns:
        List of dictionaries with 'client_name' and 'customer_id' keys
    """
    all_ids = get_all_client_ids()
    accounts = []

    for client_name, ids in all_ids.items():
        customer_id = ids.get('google_ads_customer_id')
        if customer_id and customer_id != '[TBD]':
            # Handle multi-account clients
            if isinstance(customer_id, list):
                for idx, cid in enumerate(customer_id):
                    accounts.append({
                        'client_name': f"{client_name}-{idx+1}",
                        'customer_id': cid
                    })
            else:
                accounts.append({
                    'client_name': client_name,
                    'customer_id': customer_id
                })

    return accounts


def get_merchant_centre_accounts() -> List[Dict[str, str]]:
    """
    Get list of all Merchant Centre accounts with merchant IDs.

    Returns:
        List of dictionaries with 'client_name' and 'merchant_id' keys
    """
    all_ids = get_all_client_ids()
    accounts = []

    for client_name, ids in all_ids.items():
        merchant_id = ids.get('merchant_centre_id')
        if merchant_id and merchant_id not in ['[TBD]', 'N/A']:
            # Handle multi-merchant clients
            if isinstance(merchant_id, list):
                for idx, mid in enumerate(merchant_id):
                    accounts.append({
                        'client_name': f"{client_name}-{idx+1}",
                        'merchant_id': mid
                    })
            else:
                accounts.append({
                    'client_name': client_name,
                    'merchant_id': merchant_id
                })

    return accounts


def validate_customer_id(customer_id: str) -> bool:
    """
    Validate a Google Ads customer ID format.

    Args:
        customer_id: Customer ID to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^\d{10}$', str(customer_id)))


def validate_merchant_id(merchant_id: str) -> bool:
    """
    Validate a Google Merchant Centre ID format.

    Args:
        merchant_id: Merchant ID to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^\d{6,12}$', str(merchant_id)))


def validate_ga4_property_id(property_id: str) -> bool:
    """
    Validate a GA4 property ID format.

    Args:
        property_id: Property ID to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^\d{9}$', str(property_id)))


# CLI interface for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 platform_ids.py <client_name>")
        print("       python3 platform_ids.py --all")
        print("       python3 platform_ids.py --google-ads")
        print("       python3 platform_ids.py --merchant-centre")
        sys.exit(1)

    if sys.argv[1] == '--all':
        all_ids = get_all_client_ids()
        print(json.dumps(all_ids, indent=2))
    elif sys.argv[1] == '--google-ads':
        accounts = get_google_ads_accounts()
        print(json.dumps(accounts, indent=2))
    elif sys.argv[1] == '--merchant-centre':
        accounts = get_merchant_centre_accounts()
        print(json.dumps(accounts, indent=2))
    else:
        client_name = sys.argv[1]
        try:
            ids = get_client_ids(client_name)
            print(json.dumps(ids, indent=2))
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
