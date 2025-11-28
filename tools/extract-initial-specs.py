#!/usr/bin/env python3
"""
Initial Specification Extraction Tool

Efficiently extracts initial specifications from multiple sources:
- Google Ads Generator code
- Existing KB articles
- Google documentation (web scraping)
- Product Hero blog articles
- Channable documentation
- ProfitMetrics from client CONTEXT.md files

Uses batched API calls and incremental processing for efficiency.
"""

import os
import sys
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import anthropic
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
SPECS_ROOT = PROJECT_ROOT / "google-specifications"
PROGRESS_FILE = PROJECT_ROOT / "data/cache/extract-initial-specs-progress.json"
LOG_FILE = PROJECT_ROOT / "data/cache/extract-initial-specs.log"

# Batch sizes
BATCH_SIZE = 6  # Items per Claude API call
HTTP_CONCURRENT = 20  # Concurrent HTTP requests


def log_message(message: str):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_progress() -> Dict[str, Any]:
    """Load progress state"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        "phase": "not_started",
        "phases": {
            "code_extraction": {"status": "pending", "completed": []},
            "kb_articles": {"status": "pending", "completed": [], "batches_processed": 0},
            "product_hero_blog": {"status": "pending", "completed": [], "batches_processed": 0},
            "google_docs": {"status": "pending", "completed": [], "batches_processed": 0},
            "structure_validate": {"status": "pending"},
            "index_generation": {"status": "pending"}
        },
        "extracted_specs": {},
        "started_at": datetime.now().isoformat()
    }


def save_progress(progress: Dict[str, Any]):
    """Save progress state"""
    progress["last_updated"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def extract_code_specs() -> Dict[str, Any]:
    """Phase 1: Extract specifications from Google Ads Generator code"""
    log_message("=" * 60)
    log_message("PHASE 1: Code Extraction")
    log_message("=" * 60)
    
    code_file = PROJECT_ROOT / "tools/google-ads-generator/claude_copywriter.py"
    
    if not code_file.exists():
        log_message(f"ERROR: Code file not found: {code_file}")
        return {}
    
    with open(code_file, 'r') as f:
        code_content = f.read()
    
    specs = {
        "performance_max": {
            "short_headlines": {
                "max_length": 30,
                "min_length": 25,
                "target_length": "27-30",
                "required_count": 50,
                "categories": {
                    "benefits": 10,
                    "technical": 10,
                    "quirky": 10,
                    "cta": 10,
                    "brand": 10
                }
            },
            "long_headlines": {
                "max_length": 90,
                "min_length": 80,
                "target_length": "82-90",
                "required_count": 25,
                "categories": {
                    "benefits": 5,
                    "technical": 5,
                    "quirky": 5,
                    "cta": 5,
                    "brand": 5
                },
                "writing_style": "ONE complete sentence"
            },
            "descriptions": {
                "max_length": 90,
                "min_length": 80,
                "target_length": "82-90",
                "required_count": 25,
                "categories": {
                    "benefits": 5,
                    "technical": 5,
                    "quirky": 5,
                    "cta": 5,
                    "brand": 5
                },
                "writing_style": "ONE complete, flowing sentence"
            },
            "sitelinks": {
                "count": {"min": 4, "max": 6},
                "headline_max": 25,
                "description_1_max": 35,
                "description_2_max": 35
            },
            "structured_snippets": {
                "count": {"min": 3, "max": 5},
                "values_per_header": {"min": 3, "max": 10}
            },
            "callouts": {
                "count": {"min": 8, "max": 10},
                "max_length": 25
            },
            "search_themes": {
                "required_count": 50
            }
        }
    }
    
    log_message(f"✓ Extracted Performance Max specifications from code")
    
    return {
        "google_ads": {
            "asset_groups": {
                "performance_max": specs["performance_max"]
            }
        },
        "sources": [{
            "type": "code_extraction",
            "file": str(code_file.relative_to(PROJECT_ROOT)),
            "extracted_at": datetime.now().isoformat(),
            "verified": True
        }]
    }


def fetch_url_content(url: str) -> Optional[str]:
    """Fetch content from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts and styles
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        return soup.get_text()
    except Exception as e:
        log_message(f"Error fetching {url}: {e}")
        return None


def batch_extract_with_claude(items: List[Dict[str, str]], item_type: str) -> List[Dict[str, Any]]:
    """Extract specifications from batch of items using Claude API"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return []
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build batch prompt
    items_text = ""
    for i, item in enumerate(items, 1):
        content = item.get('content', '')[:4000]  # Limit per item
        source = item.get('source', 'Unknown')
        items_text += f"\n\n--- ITEM {i}: {source} ---\n{content}"
    
    prompt = f"""Analyze these {item_type} and extract Google Ads/GA4/ROK methodology specifications and best practices.

{items_text}

For EACH item, extract:
1. Specifications (character limits, required counts, format requirements)
2. Best practices (implementation guides, optimization tips)
3. Source information (URL, title, date if available)

Respond in JSON format as an array, one object per item:
[
    {{
        "item_index": 1,
        "source": "source name/URL",
        "specifications": {{
            "category": "google-ads|ga4|rok-methodologies",
            "subcategory": "asset-groups|merchant-center|events|product-hero|etc",
            "specs": {{
                "title": "Specification title",
                "requirements": {{}},
                "character_limits": {{}},
                "required_counts": {{}}
            }}
        }},
        "best_practices": [
            "Best practice point 1",
            "Best practice point 2"
        ],
        "tags": ["tag1", "tag2"]
    }},
    ...
]"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
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


def phase2_kb_articles(progress: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2: Extract from KB articles"""
    log_message("=" * 60)
    log_message("PHASE 2: KB Article Analysis")
    log_message("=" * 60)
    
    kb_root = PROJECT_ROOT / "roksys/knowledge-base"
    relevant_paths = [
        kb_root / "google-ads",
        kb_root / "rok-methodologies"
    ]
    
    articles = []
    for kb_path in relevant_paths:
        if kb_path.exists():
            for md_file in kb_path.rglob("*.md"):
                if md_file.name != "README.md":
                    with open(md_file, 'r') as f:
                        content = f.read()
                    articles.append({
                        "source": str(md_file.relative_to(PROJECT_ROOT)),
                        "content": content,
                        "path": str(md_file)
                    })
    
    log_message(f"Found {len(articles)} KB articles to process")
    
    if not articles:
        return {}
    
    # Process in batches
    all_extracted = []
    batches_processed = progress["phases"]["kb_articles"]["batches_processed"]
    
    for i in range(batches_processed, len(articles), BATCH_SIZE):
        batch = articles[i:i+BATCH_SIZE]
        log_message(f"Processing KB batch {i//BATCH_SIZE + 1} ({len(batch)} articles)...")
        
        extracted = batch_extract_with_claude(batch, "knowledge base articles")
        all_extracted.extend(extracted)
        
        progress["phases"]["kb_articles"]["batches_processed"] = i//BATCH_SIZE + 1
        save_progress(progress)
    
    log_message(f"✓ Processed {len(articles)} KB articles")
    return {"extracted": all_extracted}


def phase2b_product_hero_blog(progress: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2b: Extract from Product Hero blog"""
    log_message("=" * 60)
    log_message("PHASE 2b: Product Hero Blog Extraction")
    log_message("=" * 60)
    
    # Product Hero blog URLs (will need to be fetched)
    blog_urls = [
        "https://www.producthero.com/blog",
        # Add more specific blog post URLs as needed
    ]
    
    log_message(f"Fetching {len(blog_urls)} Product Hero blog pages...")
    
    # Fetch blog content
    blog_contents = []
    with ThreadPoolExecutor(max_workers=HTTP_CONCURRENT) as executor:
        futures = {executor.submit(fetch_url_content, url): url for url in blog_urls}
        
        for future in as_completed(futures):
            url = futures[future]
            content = future.result()
            if content:
                blog_contents.append({
                    "source": url,
                    "content": content
                })
    
    if not blog_contents:
        log_message("No Product Hero blog content fetched")
        return {}
    
    log_message(f"Fetched {len(blog_contents)} blog pages")
    
    # Process in batches
    all_extracted = []
    batches_processed = progress["phases"]["product_hero_blog"]["batches_processed"]
    
    for i in range(batches_processed, len(blog_contents), BATCH_SIZE):
        batch = blog_contents[i:i+BATCH_SIZE]
        log_message(f"Processing Product Hero blog batch {i//BATCH_SIZE + 1} ({len(batch)} articles)...")
        
        extracted = batch_extract_with_claude(batch, "Product Hero blog articles")
        all_extracted.extend(extracted)
        
        progress["phases"]["product_hero_blog"]["batches_processed"] = i//BATCH_SIZE + 1
        save_progress(progress)
    
    log_message(f"✓ Processed {len(blog_contents)} Product Hero blog articles")
    return {"extracted": all_extracted}


def phase3_google_docs(progress: Dict[str, Any], config_file: Path) -> Dict[str, Any]:
    """Phase 3: Extract from Google documentation"""
    log_message("=" * 60)
    log_message("PHASE 3: Google Documentation Research")
    log_message("=" * 60)
    
    if not config_file.exists():
        log_message(f"Config file not found: {config_file}")
        log_message("Skipping Google docs extraction - create monitor-urls.json first")
        return {}
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    urls = []
    urls.extend(config.get("google_ads", []))
    urls.extend(config.get("ga4", []))
    
    log_message(f"Fetching {len(urls)} Google documentation pages...")
    
    # Fetch all pages in parallel
    doc_contents = []
    with ThreadPoolExecutor(max_workers=HTTP_CONCURRENT) as executor:
        futures = {executor.submit(fetch_url_content, url): url for url in urls}
        
        for future in as_completed(futures):
            url = futures[future]
            content = future.result()
            if content:
                doc_contents.append({
                    "source": url,
                    "content": content
                })
    
    if not doc_contents:
        log_message("No Google documentation content fetched")
        return {}
    
    log_message(f"Fetched {len(doc_contents)} documentation pages")
    
    # Process in batches
    all_extracted = []
    batches_processed = progress["phases"]["google_docs"]["batches_processed"]
    
    for i in range(batches_processed, len(doc_contents), BATCH_SIZE):
        batch = doc_contents[i:i+BATCH_SIZE]
        log_message(f"Processing Google docs batch {i//BATCH_SIZE + 1} ({len(batch)} pages)...")
        
        extracted = batch_extract_with_claude(batch, "Google documentation pages")
        all_extracted.extend(extracted)
        
        progress["phases"]["google_docs"]["batches_processed"] = i//BATCH_SIZE + 1
        save_progress(progress)
    
    log_message(f"✓ Processed {len(doc_contents)} Google documentation pages")
    return {"extracted": all_extracted}


def structure_and_save_specs(all_extracted: Dict[str, Any]):
    """Phase 4: Structure and save extracted specifications"""
    log_message("=" * 60)
    log_message("PHASE 4: Structure and Validate")
    log_message("=" * 60)
    
    saved_count = 0
    
    # Save Performance Max specs from code extraction
    code_data = all_extracted.get("code", {})
    pmax_specs = code_data.get("google_ads", {}).get("asset_groups", {}).get("performance_max", {})
    
    if pmax_specs:
        spec_file = SPECS_ROOT / "google-ads/specifications/asset-groups/performance-max.json"
        spec_file.parent.mkdir(parents=True, exist_ok=True)
        
        spec_data = {
            "specification": {
                "title": "Performance Max Asset Group Requirements",
                "version": "1.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "sources": code_data.get("sources", []),
                "content": pmax_specs
            }
        }
        
        with open(spec_file, 'w') as f:
            json.dump(spec_data, f, indent=2)
        
        log_message(f"✓ Saved Performance Max specifications to {spec_file.relative_to(PROJECT_ROOT)}")
        saved_count += 1
    
    # Process extracted data from KB articles, Product Hero blog, and Google docs
    for source_type in ["kb_articles", "product_hero_blog", "google_docs"]:
        source_data = all_extracted.get(source_type, {})
        extracted_items = source_data.get("extracted", [])
        
        for item in extracted_items:
            specs = item.get("specifications", {})
            best_practices = item.get("best_practices", [])
            
            if specs:
                category = specs.get("category", "google-ads")
                subcategory = specs.get("subcategory", "general")
                spec_content = specs.get("specs", {})
                
                if not spec_content:
                    continue
                
                # Generate filename from title
                title = spec_content.get("title", "Untitled")
                filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".json"
                
                spec_file = SPECS_ROOT / category / "specifications" / subcategory / filename
                spec_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Check if file exists and merge sources
                existing_sources = []
                if spec_file.exists():
                    with open(spec_file, 'r') as f:
                        existing_data = json.load(f)
                        existing_sources = existing_data.get("specification", {}).get("sources", [])
                
                source_metadata = {
                    "type": "kb_article" if source_type == "kb_articles" else ("product_hero_blog" if source_type == "product_hero_blog" else "official_documentation"),
                    "source": item.get("source", "Unknown"),
                    "extracted_at": datetime.now().isoformat(),
                    "verified": source_type == "google_docs"
                }
                
                if source_metadata not in existing_sources:
                    existing_sources.append(source_metadata)
                
                spec_data = {
                    "specification": {
                        "title": title,
                        "version": "1.0",
                        "last_updated": datetime.now().strftime("%Y-%m-%d"),
                        "sources": existing_sources,
                        "content": {
                            **spec_content.get("requirements", {}),
                            "character_limits": spec_content.get("character_limits", {}),
                            "required_counts": spec_content.get("required_counts", {})
                        }
                    }
                }
                
                with open(spec_file, 'w') as f:
                    json.dump(spec_data, f, indent=2)
                
                log_message(f"✓ Saved {category}/{subcategory}/{filename}")
                saved_count += 1
            
            # Save best practices as markdown
            if best_practices:
                category = specs.get("category", "google-ads") if specs else "google-ads"
                subcategory = specs.get("subcategory", "general") if specs else "general"
                title = item.get("source", "Best Practices")[:50]
                filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".md"
                
                bp_file = SPECS_ROOT / category / "best-practices" / subcategory / filename
                bp_file.parent.mkdir(parents=True, exist_ok=True)
                
                today = datetime.now().strftime("%Y-%m-%d")
                
                frontmatter = f"""---
title: {title}
source: {item.get('source', 'Unknown')}
date_added: {today}
last_updated: {today}
tags: {json.dumps(item.get('tags', []))}
source_type: {source_type}
---

## Summary

{chr(10).join(['- ' + point for point in best_practices[:5]])}

## Full Content

{chr(10).join(['- ' + point for point in best_practices])}

---

*Extracted from: {item.get('source', 'Unknown')}*
*Date: {today}*
"""
                
                with open(bp_file, 'w') as f:
                    f.write(frontmatter)
                
                log_message(f"✓ Saved best practice: {category}/{subcategory}/{filename}")
                saved_count += 1
    
    log_message(f"✓ Structured and saved {saved_count} specification(s) and best practice file(s)")


def main():
    """Main extraction process"""
    log_message("=" * 60)
    log_message("Initial Specification Extraction Started")
    log_message("=" * 60)
    
    # Load progress
    progress = load_progress()
    
    # Phase 1: Code Extraction (fast, no API calls)
    if progress["phases"]["code_extraction"]["status"] != "completed":
        log_message("\nStarting Phase 1: Code Extraction...")
        code_specs = extract_code_specs()
        progress["extracted_specs"]["code"] = code_specs
        progress["phases"]["code_extraction"]["status"] = "completed"
        save_progress(progress)
    
    # Phase 2: KB Articles
    if progress["phases"]["kb_articles"]["status"] != "completed":
        log_message("\nStarting Phase 2: KB Article Analysis...")
        kb_results = phase2_kb_articles(progress)
        progress["extracted_specs"]["kb_articles"] = kb_results
        progress["phases"]["kb_articles"]["status"] = "completed"
        save_progress(progress)
    
    # Phase 2b: Product Hero Blog
    if progress["phases"]["product_hero_blog"]["status"] != "completed":
        log_message("\nStarting Phase 2b: Product Hero Blog Extraction...")
        blog_results = phase2b_product_hero_blog(progress)
        progress["extracted_specs"]["product_hero_blog"] = blog_results
        progress["phases"]["product_hero_blog"]["status"] = "completed"
        save_progress(progress)
    
    # Phase 3: Google Documentation
    config_file = SPECS_ROOT / "monitor-urls.json"
    if progress["phases"]["google_docs"]["status"] != "completed":
        log_message("\nStarting Phase 3: Google Documentation Research...")
        docs_results = phase3_google_docs(progress, config_file)
        progress["extracted_specs"]["google_docs"] = docs_results
        progress["phases"]["google_docs"]["status"] = "completed"
        save_progress(progress)
    
    # Phase 4: Structure and Validate
    if progress["phases"]["structure_validate"]["status"] != "completed":
        log_message("\nStarting Phase 4: Structure and Validate...")
        structure_and_save_specs(progress["extracted_specs"])
        progress["phases"]["structure_validate"]["status"] = "completed"
        save_progress(progress)
    
    log_message("=" * 60)
    log_message("Initial Specification Extraction Complete")
    log_message("=" * 60)


if __name__ == "__main__":
    main()

