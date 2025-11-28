#!/usr/bin/env python3
"""
Facebook Specifications Monitor

Automatically checks Facebook/Meta Ads and Meta Business Suite documentation for updates weekly.
Uses batched API calls and content hashing for efficiency.

Runs automatically every Sunday at 2:00 AM via LaunchAgent.
"""

import os
import sys
import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import anthropic
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
SPECS_ROOT = PROJECT_ROOT / "facebook-specifications"
MONITOR_URLS_FILE = SPECS_ROOT / "monitor-urls.json"
CONTENT_HASHES_FILE = PROJECT_ROOT / "data/cache/facebook-specs-content-hashes.json"
CHANGELOG_FILE = PROJECT_ROOT / "data/cache/facebook-specs-changelog.json"
STATE_FILE = PROJECT_ROOT / "data/state/facebook-specs-state.json"
LOG_FILE = PROJECT_ROOT / "data/cache/facebook-specs-monitor.log"

# Batch sizes
BATCH_SIZE = 6  # Pages per Claude API call
HTTP_CONCURRENT = 20  # Concurrent HTTP requests


def log_message(message: str):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_content_hashes() -> Dict[str, str]:
    """Load content hash history"""
    if CONTENT_HASHES_FILE.exists():
        with open(CONTENT_HASHES_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_content_hashes(hashes: Dict[str, str]):
    """Save content hash history"""
    CONTENT_HASHES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTENT_HASHES_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)


def load_changelog() -> List[Dict[str, Any]]:
    """Load change log"""
    if CHANGELOG_FILE.exists():
        with open(CHANGELOG_FILE, 'r') as f:
            return json.load(f)
    return []


def save_changelog(changelog: List[Dict[str, Any]]):
    """Save change log"""
    CHANGELOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHANGELOG_FILE, 'w') as f:
        json.dump(changelog, f, indent=2)


def fetch_url_content(url: str) -> Optional[Dict[str, Any]]:
    """Fetch content from URL and return content + metadata"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts and styles
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        content = soup.get_text()
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        return {
            "url": url,
            "content": content,
            "hash": content_hash,
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        log_message(f"Error fetching {url}: {e}")
        return None


def batch_extract_specs(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract specifications from batch of pages using Claude API"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return []
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build batch prompt
    pages_text = ""
    for i, page in enumerate(pages, 1):
        content = page.get('content', '')[:4000]  # Limit per page
        url = page.get('url', 'Unknown')
        pages_text += f"\n\n--- PAGE {i}: {url} ---\n{content}"
    
    prompt = f"""Analyze these Facebook/Meta Ads and Meta Business Suite documentation pages and extract specifications and requirements.

{pages_text}

For EACH page, extract:
1. Specifications (character limits, required counts, format requirements, technical requirements)
2. Best practices (implementation guides, optimization tips)
3. Any changes or updates from previous versions

Focus on:
- Ad format specifications (Single Image, Video, Carousel, Collection, Stories, Reels)
- Campaign type requirements (Awareness, Traffic, Engagement, Conversions, App Promotion)
- Audience targeting specifications (Custom Audiences, Lookalike Audiences, Detailed Targeting)
- Bidding strategy requirements (Lowest Cost, Cost Cap, Bid Cap, ROAS, Value Optimization)
- Facebook Pixel setup and event tracking specifications
- Conversions API specifications (server-side tracking, event matching, deduplication)
- Creative specifications (image sizes, video lengths, text limits, aspect ratios)
- Account structure requirements (Ad Accounts, Business Manager, Pages, Instagram Accounts)
- Meta Business Suite specifications (Business Manager setup, Page management, permissions, billing)

Respond in JSON format as an array, one object per page:
[
    {{
        "page_index": 1,
        "url": "page URL",
        "specifications": {{
            "category": "facebook-ads|meta-business-suite",
            "subcategory": "ad-formats|campaign-types|audience-targeting|bidding-strategies|pixel-setup|conversions-api|creative-specs|account-structure|etc",
            "specs": {{
                "title": "Specification title",
                "requirements": {{}},
                "character_limits": {{}},
                "required_counts": {{}},
                "format_requirements": {{}}
            }}
        }},
        "best_practices": [
            "Best practice point 1",
            "Best practice point 2"
        ],
        "changes_detected": false,
        "tags": ["tag1", "tag2"]
    }},
    ...
]"""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        
        # Extract JSON array
        if '[' in response_text and ']' in response_text:
            json_start = response_text.index('[')
            json_end = response_text.rindex(']') + 1
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            log_message("Could not parse JSON array from Claude response")
            return []
    
    except Exception as e:
        log_message(f"Error in batch extraction: {e}")
        return []


def update_specification_file(category: str, subcategory: str, filename: str, specs_data: Dict[str, Any], sources: List[Dict[str, Any]]):
    """Update or create specification JSON file"""
    spec_file = SPECS_ROOT / category / "specifications" / subcategory / filename
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing if exists
    existing_spec = {}
    if spec_file.exists():
        with open(spec_file, 'r') as f:
            existing_spec = json.load(f)
    
    # Merge with new data
    spec_data = {
        "specification": {
            "title": specs_data.get("title", existing_spec.get("specification", {}).get("title", "Untitled")),
            "version": str(float(existing_spec.get("specification", {}).get("version", "1.0")) + 0.1),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "sources": existing_spec.get("specification", {}).get("sources", []) + sources,
            "content": {**existing_spec.get("specification", {}).get("content", {}), **specs_data.get("requirements", {})}
        }
    }
    
    with open(spec_file, 'w') as f:
        json.dump(spec_data, f, indent=2)
    
    log_message(f"✓ Updated {spec_file.relative_to(PROJECT_ROOT)}")


def create_best_practice_markdown(category: str, subcategory: str, filename: str, title: str, content: List[str], sources: List[Dict[str, Any]]):
    """Create best practice markdown file"""
    bp_file = SPECS_ROOT / category / "best-practices" / subcategory / filename
    bp_file.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter = f"""---
title: {title}
date_added: {today}
last_updated: {today}
sources: {json.dumps(sources, indent=2)}
---

## Summary

{chr(10).join(['- ' + point for point in content[:5]])}

## Full Content

{chr(10).join(['- ' + point for point in content])}

---

*Last updated: {today}*
"""
    
    with open(bp_file, 'w') as f:
        f.write(frontmatter)
    
    log_message(f"✓ Created best practice: {bp_file.relative_to(PROJECT_ROOT)}")


def main():
    """Main monitoring process"""
    log_message("=" * 60)
    log_message("Facebook Specifications Monitor Started")
    log_message("=" * 60)
    
    # Load URLs to monitor
    if not MONITOR_URLS_FILE.exists():
        log_message(f"ERROR: Monitor URLs file not found: {MONITOR_URLS_FILE}")
        log_message("Create monitor-urls.json with Facebook Ads and Meta Business Suite URLs")
        return
    
    with open(MONITOR_URLS_FILE, 'r') as f:
        url_config = json.load(f)
    
    # Collect all URLs
    all_urls = []
    all_urls.extend(url_config.get("facebook_ads", []))
    all_urls.extend(url_config.get("meta_business_suite", []))
    
    log_message(f"Monitoring {len(all_urls)} documentation pages")
    
    # Load content hash history
    content_hashes = load_content_hashes()
    changelog = load_changelog()
    
    # Fetch all pages in parallel
    log_message(f"Fetching {len(all_urls)} pages (up to {HTTP_CONCURRENT} concurrent)...")
    fetched_pages = []
    
    with ThreadPoolExecutor(max_workers=HTTP_CONCURRENT) as executor:
        futures = {executor.submit(fetch_url_content, url): url for url in all_urls}
        
        for future in as_completed(futures):
            url = futures[future]
            result = future.result()
            if result:
                fetched_pages.append(result)
    
    log_message(f"✓ Fetched {len(fetched_pages)} pages")
    
    # Detect changes by comparing hashes
    changed_pages = []
    for page in fetched_pages:
        url = page["url"]
        current_hash = page["hash"]
        previous_hash = content_hashes.get(url)
        
        if previous_hash != current_hash:
            changed_pages.append(page)
            if previous_hash:
                log_message(f"📝 Change detected: {url}")
            else:
                log_message(f"🆕 New page: {url}")
    
    if not changed_pages:
        log_message("✓ No changes detected - all pages up to date")
        # Update hashes anyway (in case of first run)
        for page in fetched_pages:
            content_hashes[page["url"]] = page["hash"]
        save_content_hashes(content_hashes)
        return
    
    log_message(f"Processing {len(changed_pages)} changed pages in batches of {BATCH_SIZE}...")
    
    # Process changed pages in batches
    all_extracted = []
    for i in range(0, len(changed_pages), BATCH_SIZE):
        batch = changed_pages[i:i+BATCH_SIZE]
        log_message(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch)} pages)...")
        
        extracted = batch_extract_specs(batch)
        all_extracted.extend(extracted)
    
    log_message(f"✓ Extracted specifications from {len(changed_pages)} pages")
    
    # Update specification files
    for extracted in all_extracted:
        url = extracted.get("url", "")
        specs = extracted.get("specifications", {})
        best_practices = extracted.get("best_practices", [])
        
        if specs:
            category = specs.get("category", "facebook-ads")
            subcategory = specs.get("subcategory", "general")
            spec_content = specs.get("specs", {})
            
            # Generate filename from title or URL
            title = spec_content.get("title", "Untitled")
            filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".json"
            
            sources = [{
                "type": "official_documentation",
                "url": url,
                "last_checked": datetime.now().strftime("%Y-%m-%d"),
                "verified": True,
                "content_hash": next((p["hash"] for p in changed_pages if p["url"] == url), "")
            }]
            
            update_specification_file(category, subcategory, filename, spec_content, sources)
            
            # Log change
            changelog.append({
                "date": datetime.now().isoformat(),
                "url": url,
                "action": "updated" if content_hashes.get(url) else "added",
                "specification": f"{category}/{subcategory}/{filename}"
            })
        
        if best_practices:
            category = specs.get("category", "facebook-ads") if specs else "facebook-ads"
            subcategory = specs.get("subcategory", "general") if specs else "general"
            title = spec_content.get("title", "Best Practices") if specs else "Best Practices"
            filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".md"
            
            sources = [{
                "type": "official_documentation",
                "url": url,
                "last_checked": datetime.now().strftime("%Y-%m-%d"),
                "verified": True
            }]
            
            create_best_practice_markdown(category, subcategory, filename, title, best_practices, sources)
    
    # Update content hashes
    for page in fetched_pages:
        content_hashes[page["url"]] = page["hash"]
    
    save_content_hashes(content_hashes)
    save_changelog(changelog)
    
    log_message("=" * 60)
    log_message(f"Monitor Complete: {len(changed_pages)} pages updated")
    log_message("=" * 60)


if __name__ == "__main__":
    main()

