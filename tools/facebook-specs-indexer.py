#!/usr/bin/env python3
"""
Facebook Specifications Indexer

Generates master index.json for programmatic access to all Facebook/Meta specifications.
Indexes both JSON specification files and Markdown best practice files.

Run after any updates to specifications or best practices.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
SPECS_ROOT = PROJECT_ROOT / "facebook-specifications"
INDEX_FILE = SPECS_ROOT / "index.json"


def extract_json_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract metadata from JSON specification file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        spec = data.get("specification", {})
        
        return {
            "file": str(file_path.relative_to(SPECS_ROOT)),
            "version": spec.get("version", "1.0"),
            "last_updated": spec.get("last_updated", ""),
            "title": spec.get("title", file_path.stem),
            "summary": spec.get("title", ""),
            "sources": [s.get("type", "unknown") for s in spec.get("sources", [])]
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def extract_markdown_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract metadata from Markdown best practice file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract frontmatter
        title = "Untitled"
        date_added = ""
        tags = []
        source_type = ""
        
        # Try to extract from frontmatter
        if content.startswith('---'):
            frontmatter_end = content.find('---', 3)
            if frontmatter_end > 0:
                frontmatter = content[3:frontmatter_end]
                for line in frontmatter.split('\n'):
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith('date_added:'):
                        date_added = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith('tags:'):
                        tags_str = line.split(':', 1)[1].strip()
                        tags = json.loads(tags_str) if tags_str.startswith('[') else []
                    elif line.startswith('source_type:'):
                        source_type = line.split(':', 1)[1].strip().strip('"\'')
        
        # Fallback: extract from first heading
        if title == "Untitled":
            for line in content.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
        
        return {
            "file": str(file_path.relative_to(SPECS_ROOT)),
            "title": title,
            "date_added": date_added,
            "tags": tags,
            "source_type": source_type,
            "word_count": len(content.split())
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def build_index() -> Dict[str, Any]:
    """Build master index of all specifications"""
    print("=" * 60)
    print("  Facebook Specifications Indexer")
    print("=" * 60)
    print()
    
    if not SPECS_ROOT.exists():
        print(f"❌ Specifications directory not found: {SPECS_ROOT}")
        return {}
    
    index = {
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "facebook_ads": {
            "specifications": {},
            "best_practices": {}
        },
        "meta_business_suite": {
            "specifications": {},
            "best_practices": {}
        }
    }
    
    # Index JSON specification files
    print("Indexing JSON specification files...")
    for json_file in SPECS_ROOT.rglob("specifications/**/*.json"):
        if json_file.name == "index.json":
            continue
        
        metadata = extract_json_metadata(json_file)
        if not metadata:
            continue
        
        # Determine category and subcategory from path
        rel_path = json_file.relative_to(SPECS_ROOT)
        parts = rel_path.parts
        
        if len(parts) >= 3:
            category = parts[0]  # facebook-ads or meta-business-suite
            subcategory = parts[2]  # ad-formats, campaign-types, etc.
            filename = json_file.stem
            
            # Map category names
            category_key = category.replace("-", "_")
            
            if category_key not in index:
                index[category_key] = {"specifications": {}, "best_practices": {}}
            
            if subcategory not in index[category_key]["specifications"]:
                index[category_key]["specifications"][subcategory] = {}
            
            index[category_key]["specifications"][subcategory][filename] = metadata
    
    # Index Markdown best practice files
    print("Indexing Markdown best practice files...")
    for md_file in SPECS_ROOT.rglob("best-practices/**/*.md"):
        if md_file.name == "README.md":
            continue
        
        metadata = extract_markdown_metadata(md_file)
        if not metadata:
            continue
        
        # Determine category and subcategory from path
        rel_path = md_file.relative_to(SPECS_ROOT)
        parts = rel_path.parts
        
        if len(parts) >= 3:
            category = parts[0]
            subcategory = parts[2]
            filename = md_file.stem
            
            # Map category names
            category_key = category.replace("-", "_")
            
            if category_key not in index:
                index[category_key] = {"specifications": {}, "best_practices": {}}
            
            if subcategory not in index[category_key]["best_practices"]:
                index[category_key]["best_practices"][subcategory] = []
            
            index[category_key]["best_practices"][subcategory].append(metadata)
    
    # Count totals
    total_specs = 0
    total_best_practices = 0
    
    for category in ["facebook_ads", "meta_business_suite"]:
        if category in index:
            for subcat_specs in index[category]["specifications"].values():
                total_specs += len(subcat_specs)
            for subcat_bp in index[category]["best_practices"].values():
                total_best_practices += len(subcat_bp)
    
    print()
    print("=" * 60)
    print(f"✅ Indexed {total_specs} specifications")
    print(f"✅ Indexed {total_best_practices} best practice files")
    print("=" * 60)
    print()
    
    return index


def save_index(index: Dict[str, Any]):
    """Save index to JSON file"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"💾 Index saved to: {INDEX_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == '__main__':
    try:
        index = build_index()
        if index:
            save_index(index)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

