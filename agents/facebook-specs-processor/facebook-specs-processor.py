#!/usr/bin/env python3
"""
Facebook Specifications Processor

Processes manual additions from Meta rep emails/meetings.
Uses batched API calls for efficiency.

Runs automatically every 2 hours via LaunchAgent.
"""

import os
import sys
import json
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import anthropic

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
SPECS_ROOT = PROJECT_ROOT / "facebook-specifications"
INBOX_ROOT = SPECS_ROOT / "_inbox"
PROCESSED_ROOT = INBOX_ROOT / "processed"
LOG_FILE = PROJECT_ROOT / "data/cache/facebook-specs-processor.log"

# Batch sizes
BATCH_SIZE = 6  # Files per Claude API call


def log_message(message: str):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def read_file_content(file_path: Path) -> Optional[str]:
    """Read content from various file types"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"[Binary file: {file_path.name}. Manual processing may be required.]"
    except Exception as e:
        log_message(f"Error reading {file_path}: {e}")
        return None


def batch_process_files(file_contents: Dict[str, str]) -> List[Dict[str, Any]]:
    """Process batch of files using Claude API"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return []
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build batch prompt
    files_text = ""
    for i, (filename, content) in enumerate(file_contents.items(), 1):
        files_text += f"\n\n--- FILE {i}: {filename} ---\n{content[:4000]}"
    
    prompt = f"""Analyze these Meta rep recommendations, meeting notes, or manual additions and extract specifications and best practices.

{files_text}

For EACH file, extract:
1. Specifications mentioned (character limits, requirements, setup procedures)
2. Best practices recommended
3. Source information (rep name, meeting title, email subject, date)
4. Category (facebook-ads or meta-business-suite)
5. Subcategory (ad-formats, campaign-types, audience-targeting, bidding-strategies, pixel-setup, conversions-api, creative-specs, account-structure, etc.)

Respond in JSON format as an array, one object per file:
[
    {{
        "filename": "filename1.md",
        "source_type": "meta_rep_recommendation|manual_addition",
        "source_name": "Rep name or meeting title",
        "date": "YYYY-MM-DD",
        "context": "Meeting/email context",
        "category": "facebook-ads|meta-business-suite",
        "subcategory": "ad-formats|campaign-types|audience-targeting|bidding-strategies|pixel-setup|conversions-api|creative-specs|account-structure|etc",
        "specifications": {{
            "title": "Specification title",
            "requirements": {{}},
            "character_limits": {{}},
            "required_counts": {{}}
        }},
        "best_practices": [
            "Best practice point 1",
            "Best practice point 2"
        ],
        "tags": ["tag1", "tag2"],
        "verified": false
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
        log_message(f"Error in batch processing: {e}")
        return []


def update_specification_file(category: str, subcategory: str, filename: str, specs_data: Dict[str, Any], source_info: Dict[str, Any]):
    """Update or create specification JSON file"""
    spec_file = SPECS_ROOT / category / "specifications" / subcategory / filename
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing if exists
    existing_spec = {}
    if spec_file.exists():
        with open(spec_file, 'r') as f:
            existing_spec = json.load(f)
    
    # Create source metadata
    source_metadata = {
        "type": source_info.get("source_type", "manual_addition"),
        "source": source_info.get("source_name", "Unknown"),
        "date": source_info.get("date", datetime.now().strftime("%Y-%m-%d")),
        "context": source_info.get("context", ""),
        "file": source_info.get("filename", ""),
        "verified": source_info.get("verified", False)
    }
    
    # Merge with existing
    existing_sources = existing_spec.get("specification", {}).get("sources", [])
    if source_metadata not in existing_sources:
        existing_sources.append(source_metadata)
    
    spec_data = {
        "specification": {
            "title": specs_data.get("title", existing_spec.get("specification", {}).get("title", "Untitled")),
            "version": str(float(existing_spec.get("specification", {}).get("version", "1.0")) + 0.1),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "sources": existing_sources,
            "content": {**existing_spec.get("specification", {}).get("content", {}), **specs_data.get("requirements", {})}
        }
    }
    
    with open(spec_file, 'w') as f:
        json.dump(spec_data, f, indent=2)
    
    log_message(f"✓ Updated {spec_file.relative_to(PROJECT_ROOT)}")


def create_best_practice_markdown(category: str, subcategory: str, filename: str, title: str, content: List[str], source_info: Dict[str, Any]):
    """Create best practice markdown file"""
    bp_file = SPECS_ROOT / category / "best-practices" / subcategory / filename
    bp_file.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    source_metadata = {
        "type": source_info.get("source_type", "manual_addition"),
        "source": source_info.get("source_name", "Unknown"),
        "date": source_info.get("date", today),
        "context": source_info.get("context", ""),
        "file": source_info.get("filename", ""),
        "verified": source_info.get("verified", False)
    }
    
    frontmatter = f"""---
title: {title}
source: {source_info.get('source_name', 'Unknown')}
date_added: {today}
last_updated: {today}
tags: {json.dumps(source_info.get('tags', []))}
source_type: {source_info.get('source_type', 'manual_addition')}
---

## Summary

{chr(10).join(['- ' + point for point in content[:5]])}

## Key Insights

{chr(10).join(['- ' + point for point in content])}

## Source Information

- **Source Type**: {source_metadata['type']}
- **Source**: {source_metadata['source']}
- **Date**: {source_metadata['date']}
- **Context**: {source_metadata['context']}
- **Verified**: {source_metadata['verified']}

---

*Processed from inbox on {today}*
*Original file: {source_info.get('filename', 'Unknown')}*
"""
    
    with open(bp_file, 'w') as f:
        f.write(frontmatter)
    
    log_message(f"✓ Created best practice: {bp_file.relative_to(PROJECT_ROOT)}")


def process_inbox():
    """Main processing function"""
    log_message("=" * 60)
    log_message("Facebook Specifications Processor Started")
    log_message("=" * 60)
    
    # Collect files from inbox subdirectories
    inbox_subdirs = ["meta-rep-emails", "meeting-notes", "manual-additions"]
    all_files = []
    
    for subdir in inbox_subdirs:
        inbox_subdir = INBOX_ROOT / subdir
        if inbox_subdir.exists():
            for file_path in inbox_subdir.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.') and file_path.name != 'README.md':
                    # Skip processed folder
                    if 'processed' in file_path.parts:
                        continue
                    all_files.append(file_path)
    
    log_message(f"Found {len(all_files)} files to process")
    
    if not all_files:
        log_message("No files to process")
        return
    
    # Process in batches
    processed_count = 0
    error_count = 0
    
    for i in range(0, len(all_files), BATCH_SIZE):
        batch_files = all_files[i:i+BATCH_SIZE]
        log_message(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch_files)} files)...")
        
        # Read file contents
        file_contents = {}
        file_objects = {}
        
        for file_path in batch_files:
            content = read_file_content(file_path)
            if content:
                file_contents[file_path.name] = content
                file_objects[file_path.name] = file_path
        
        if not file_contents:
            error_count += len(batch_files)
            continue
        
        # Process batch with Claude
        extracted = batch_process_files(file_contents)
        
        # Process each extracted item
        for item in extracted:
            filename = item.get("filename", "")
            if filename not in file_objects:
                error_count += 1
                continue
            
            file_path = file_objects[filename]
            category = item.get("category", "facebook-ads")
            subcategory = item.get("subcategory", "general")
            specs = item.get("specifications", {})
            best_practices = item.get("best_practices", [])
            
            try:
                # Update specification file if specs found
                if specs:
                    spec_content = specs.get("specs", {})
                    title = spec_content.get("title", "Untitled")
                    spec_filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".json"
                    
                    update_specification_file(category, subcategory, spec_filename, spec_content, item)
                
                # Create best practice markdown if best practices found
                if best_practices:
                    title = item.get("source_name", "Best Practices") + " - " + datetime.now().strftime("%Y-%m-%d")
                    bp_filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".md"
                    
                    create_best_practice_markdown(category, subcategory, bp_filename, title, best_practices, item)
                
                # Move to processed
                PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
                processed_path = PROCESSED_ROOT / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{file_path.name}"
                shutil.move(str(file_path), str(processed_path))
                
                processed_count += 1
                log_message(f"✓ Processed: {file_path.name}")
            
            except Exception as e:
                log_message(f"ERROR processing {filename}: {e}")
                error_count += 1
    
    log_message("=" * 60)
    log_message(f"Processing Complete: {processed_count} processed, {error_count} errors")
    log_message("=" * 60)


if __name__ == "__main__":
    process_inbox()

