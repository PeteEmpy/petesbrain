#!/usr/bin/env python3
"""
Batch generate alternatives for ALL underperforming NDA assets
Processes in batches by asset type to optimize API calls
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from anthropic import Anthropic

# Add paths
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-sheets-mcp-server'))
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

URL = "https://www.nda.ac.uk/"
SPREADSHEET_ID = "1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto"
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = Path(__file__).parent / 'final-alternatives-for-dropdowns.json'
CUSTOMER_ID = "1994728449"


def fetch_website_content(url: str) -> str:
    """Fetch and extract content from NDA website."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    title = soup.find('title')
    title_text = title.get_text() if title else ""

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    meta_text = meta_desc.get('content', '') if meta_desc else ""

    h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')[:8]]
    h2_tags = [h2.get_text().strip() for h2 in soup.find_all('h2')[:15]]
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')[:25] if len(p.get_text().strip()) > 30]

    return f"""URL: {url}
TITLE: {title_text}
META: {meta_text}
H1: {', '.join(h1_tags[:5])}
H2: {', '.join(h2_tags[:10])}
CONTENT: {' '.join(paragraphs[:8])}"""


def get_sheets_service():
    """Build Google Sheets service."""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get('access_token') or token_data.get('token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    return build('sheets', 'v4', credentials=creds)


def get_asset_group_urls(asset_group_ids: list) -> dict:
    """Get final URLs for asset groups from Google Ads API."""
    headers = get_headers_with_auto_token()
    formatted_customer_id = format_customer_id(CUSTOMER_ID)

    # Query asset group URLs
    asset_group_ids_str = ', '.join([f'"{ag_id}"' for ag_id in asset_group_ids])

    query = f'''
        SELECT
            asset_group.id,
            asset_group.name,
            asset_group.final_urls
        FROM asset_group
        WHERE asset_group.id IN ({asset_group_ids_str})
    '''

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/googleAds:search"
    response = requests.post(url, headers=headers, json={"query": query})

    if not response.ok:
        print(f"Error querying asset groups: {response.status_code}")
        return {}

    data = response.json()

    # Map asset_group_id -> final_url
    ag_urls = {}
    for row in data.get('results', []):
        ag = row.get('assetGroup', {})
        ag_id = ag.get('id')
        final_urls = ag.get('finalUrls', [])

        if final_urls:
            # Clean URL (remove UTM parameters)
            clean_url = final_urls[0].split('?')[0]
            ag_urls[ag_id] = clean_url

    return ag_urls


def get_missing_assets():
    """Get all unique asset texts that don't have alternatives, with asset group URLs."""
    service = get_sheets_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A2:O70'  # Get all columns including asset_group_id
    ).execute()

    values = result.get('values', [])

    # Load existing alternatives
    if ALTERNATIVES_FILE.exists():
        with open(ALTERNATIVES_FILE, 'r') as f:
            existing = json.load(f)
        existing_texts = set(data.get('current', '').lower() for data in existing.values())
    else:
        existing_texts = set()

    # Collect missing assets with metadata
    missing_assets = []

    for row in values:
        if len(row) >= 15:  # Ensure we have all columns
            asset_group_name = row[1]
            asset_type = row[2]  # Column C
            asset_text = row[3]  # Column D
            asset_group_id = row[14]  # Column O

            if asset_text.lower() not in existing_texts:
                missing_assets.append({
                    'asset_group_name': asset_group_name,
                    'asset_group_id': asset_group_id,
                    'asset_type': asset_type,
                    'asset_text': asset_text
                })

    return missing_assets


def generate_batch(landing_page_content: str, landing_page_url: str, asset_texts: list, asset_type: str) -> dict:
    """Generate alternatives for a batch using Claude with landing page context."""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)

    # Build asset list
    assets_list = "\n".join([f"{i+1}. {text}" for i, text in enumerate(asset_texts)])

    # Type-specific instructions
    if asset_type == "HEADLINE":
        type_instructions = """
Generate 15 short headlines (30 chars max) per asset text:
- 5 sections: Benefits, Technical, Quirky, CTA, Brand
- 3 headlines per section
- Character limits: MAX 30, TARGET 25-30, MIN 20
- Sentence case only

JSON structure:
{
  "Asset Text": {
    "current": "Asset Text",
    "section_breakdown": {
      "Benefits": ["h1", "h2", "h3"],
      "Technical": ["h1", "h2", "h3"],
      "Quirky": ["h1", "h2", "h3"],
      "CTA": ["h1", "h2", "h3"],
      "Brand": ["h1", "h2", "h3"]
    }
  }
}"""
    elif asset_type == "LONG_HEADLINE":
        type_instructions = """
Generate 10 long headlines (90 chars max) per asset text:
- 5 sections: Benefits, Technical, Quirky, CTA, Brand
- 2 long headlines per section
- Character limits: MAX 90, TARGET 85-90 (use the FULL 90 chars), MIN 75
- ONE CONTINUOUS SENTENCE - NO periods, NO two sentences
- Must read naturally and scan smoothly as a single flowing sentence
- Use connecting words (with, that, for, from, and) to extend the sentence
- Sentence case only

CRITICAL: Each headline must be ONE sentence only. No periods except at the end.

GOOD EXAMPLES:
✓ "Study accredited interior design diplomas online with flexible learning and 0% finance available" (89 chars)
✓ "Join 35,000+ graduates from the UK's leading provider of online interior design education" (90 chars)

BAD EXAMPLES:
✗ "Study interior design online. Flexible learning with 0% finance." (TWO sentences - rejected)
✗ "Accredited diplomas. Join 35,000+ graduates." (TWO sentences - rejected)

JSON structure:
{
  "Asset Text": {
    "current": "Asset Text",
    "long_headlines": {
      "Benefits": ["h1", "h2"],
      "Technical": ["h1", "h2"],
      "Quirky": ["h1", "h2"],
      "CTA": ["h1", "h2"],
      "Brand": ["h1", "h2"]
    }
  }
}"""
    else:  # DESCRIPTION
        type_instructions = """
Generate 10 descriptions (90 chars max) per asset text:
- 5 sections: Benefits, Technical, Quirky, CTA, Brand
- 2 descriptions per section
- Character limits: MAX 90, TARGET 85-90 (use the FULL 90 chars), MIN 75
- ONE CONTINUOUS SENTENCE - NO periods, NO two sentences
- Must read naturally and scan smoothly as a single flowing sentence
- Use connecting words (with, that, for, from, and) to extend the sentence
- Persuasive, benefit-focused
- Sentence case only

CRITICAL: Each description must be ONE sentence only. No periods except at the end.

GOOD EXAMPLES:
✓ "Start your interior design career with our accredited online diploma and flexible payment plans" (88 chars)
✓ "Transform your passion into a career with UK-accredited interior design courses and expert tutors" (90 chars)

BAD EXAMPLES:
✗ "Start your interior design career. Accredited online diploma with flexible payments." (TWO sentences - rejected)
✗ "Study online. Expert tutors and flexible payment plans available." (TWO sentences - rejected)

JSON structure:
{
  "Asset Text": {
    "current": "Asset Text",
    "descriptions": {
      "Benefits": ["d1", "d2"],
      "Technical": ["d1", "d2"],
      "Quirky": ["d1", "d2"],
      "CTA": ["d1", "d2"],
      "Brand": ["d1", "d2"]
    }
  }
}"""

    prompt = f"""You are an ELITE Google Ads copywriter creating Performance Max alternatives for NDA.

ASSET TEXTS TO REWRITE ({asset_type}):
{assets_list}

{type_instructions}

LANDING PAGE CONTEXT:
These assets will send users to: {landing_page_url}

LANDING PAGE CONTENT:
{landing_page_content[:1500]}

NDA KEY USPs (USE THESE):
- 35+ years teaching interior design (established 1991)
- 35,000+ graduates worldwide in 100+ countries
- UK accredited (AIM Awards, Ofqual regulated, KHDA approved)
- 100% online, flexible study - no term times or semesters
- From short courses to BA (Hons) degrees and Master's
- University partner (de Montfort University)
- Career-focused, practical training
- Personal tutor support included
- 0% finance and payment plans available
- Study from anywhere in the world

CRITICAL REQUIREMENTS:
✓ EXACT character limits enforced
✓ EXACT counts per section (3 for short headlines, 2 for long/descriptions)
✓ Sentence case ONLY (not title case)
✓ Match the landing page messaging and offer (e.g., if page is about Diplomas, emphasize Diplomas)
✓ Use actual USPs from the list above
✓ Professional yet approachable tone
✓ NO generic education phrases - be specific to NDA

Return ONLY valid JSON with the exact structure shown above. No additional text."""

    print(f"  Generating via Claude API ({len(asset_texts)} texts)...", flush=True)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text

    # Extract JSON
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(0)

    return json.loads(response_text)


def validate_and_clean(data: dict, asset_type: str) -> dict:
    """Validate character limits and remove invalid entries."""

    sections = ["Benefits", "Technical", "Quirky", "CTA", "Brand"]

    if asset_type == "HEADLINE":
        key = "section_breakdown"
        max_chars = 30
        min_chars = 20
        required_per_section = 3
        check_single_sentence = False
    elif asset_type == "LONG_HEADLINE":
        key = "long_headlines"
        max_chars = 90
        min_chars = 75  # Increased from 60 to encourage using full 90 chars
        required_per_section = 2
        check_single_sentence = True
    else:  # DESCRIPTION
        key = "descriptions"
        max_chars = 90
        min_chars = 75  # Increased from 60 to encourage using full 90 chars
        required_per_section = 2
        check_single_sentence = True

    for asset_text, asset_data in data.items():
        if key in asset_data:
            for section in sections:
                if section in asset_data[key]:
                    valid = []
                    for item in asset_data[key][section]:
                        char_count = len(item)

                        # Check character limits
                        if not (min_chars <= char_count <= max_chars):
                            continue

                        # Check for single sentence (no periods in the middle)
                        if check_single_sentence:
                            # Count periods (excluding the final period)
                            text_without_final = item.rstrip('.')
                            if '.' in text_without_final:
                                # Has period in the middle - reject
                                continue

                        valid.append(item)

                    asset_data[key][section] = valid

    return data


def main():
    print("\n" + "="*70)
    print("NDA PMAX - BATCH GENERATE ALL MISSING ALTERNATIVES")
    print("="*70)

    # Get missing assets
    print("\nStep 1: Identifying missing assets from Google Sheet...")
    missing_assets = get_missing_assets()

    if not missing_assets:
        print("✅ No missing assets - all have alternatives!")
        return

    print(f"✅ Found {len(missing_assets)} assets without alternatives")

    # Get asset group URLs
    print("\nStep 2: Fetching asset group landing pages...")
    asset_group_ids = list(set(a['asset_group_id'] for a in missing_assets))
    ag_urls = get_asset_group_urls(asset_group_ids)
    print(f"✅ Retrieved {len(ag_urls)} asset group URLs")

    # Group assets by (landing_page_url, asset_type)
    groups = {}
    for asset in missing_assets:
        ag_id = asset['asset_group_id']
        landing_url = ag_urls.get(ag_id, URL)  # Fallback to homepage if URL not found
        asset_type = asset['asset_type']
        key = (landing_url, asset_type)

        if key not in groups:
            groups[key] = []
        groups[key].append(asset['asset_text'])

    print(f"✅ Grouped into {len(groups)} batches by landing page + type")

    # Load existing alternatives
    if ALTERNATIVES_FILE.exists():
        with open(ALTERNATIVES_FILE, 'r') as f:
            all_alternatives = json.load(f)
        print(f"\n✅ Loaded {len(all_alternatives)} existing alternatives")
    else:
        all_alternatives = {}
        print("\n⚠️  No existing alternatives found - creating new file")

    # Generate for each group
    print("\n" + "="*70)
    print("Step 3: Generating alternatives (grouped by landing page)...")
    print("="*70)

    generated_count = 0
    batch_num = 1

    for (landing_url, asset_type), asset_texts in groups.items():
        print(f"\nBatch {batch_num}/{len(groups)}:")
        print(f"  Landing Page: {landing_url}")
        print(f"  Type: {asset_type}")
        print(f"  Assets: {len(asset_texts)}")

        try:
            # Fetch landing page content
            landing_content = fetch_website_content(landing_url)

            # Generate alternatives
            result = generate_batch(landing_content, landing_url, asset_texts, asset_type)
            result = validate_and_clean(result, asset_type)

            # Merge into all_alternatives
            import hashlib
            for asset_text, asset_data in result.items():
                # Find or create asset ID
                asset_id = None
                for aid, adata in all_alternatives.items():
                    if adata.get('current', '').lower() == asset_text.lower():
                        asset_id = aid
                        break

                if not asset_id:
                    # Generate synthetic ID from hash
                    asset_id = str(int(hashlib.md5(asset_text.encode()).hexdigest()[:10], 16))

                # Merge data
                if asset_id in all_alternatives:
                    # Update existing entry
                    all_alternatives[asset_id].update(asset_data)
                else:
                    # Create new entry
                    all_alternatives[asset_id] = asset_data

            print(f"    ✅ Generated {len(result)} alternatives")
            generated_count += len(result)

            # Rate limiting
            if batch_num < len(groups):
                print(f"    ⏱️  Waiting 2 seconds (rate limiting)...")
                time.sleep(2)

        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            continue

        batch_num += 1

    # Save merged alternatives
    print("\n" + "="*70)
    print("Step 4: Saving merged alternatives...")
    print("="*70)

    with open(ALTERNATIVES_FILE, 'w') as f:
        json.dump(all_alternatives, f, indent=2)

    print(f"\n✅ Saved to {ALTERNATIVES_FILE}")
    print(f"  • Total asset IDs: {len(all_alternatives)}")
    print(f"  • New alternatives generated: {generated_count}")

    # Summary
    print("\n" + "="*70)
    print("BATCH GENERATION COMPLETE")
    print("="*70)
    print(f"\nNext step: Run populate script to add dropdowns to sheet:")
    print(f"  venv/bin/python3 clients/national-design-academy/scripts/populate-by-asset-type.py")
    print()


if __name__ == "__main__":
    main()
