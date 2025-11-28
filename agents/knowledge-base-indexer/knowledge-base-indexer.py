#!/usr/bin/env python3
"""
Knowledge Base Indexer

Creates a searchable index of all knowledge base files for fast AI-powered search.
Indexes title, content, category, and metadata for semantic search.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
KB_ROOT = PROJECT_ROOT / "roksys" / "knowledge-base"
INDEX_FILE = PROJECT_ROOT / "shared" / "data" / "kb-index.json"


def extract_metadata(file_path: Path, content: str) -> Dict[str, Any]:
    """Extract metadata from markdown file"""
    metadata = {
        "path": str(file_path.relative_to(KB_ROOT)),
        "filename": file_path.name,
        "category": get_category(file_path),
        "title": extract_title(content),
        "date": extract_date(file_path.name, content),
        "word_count": len(content.split()),
        "size_bytes": file_path.stat().st_size,
        "modified": file_path.stat().st_mtime,
    }
    
    # Extract first paragraph as preview
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    for line in lines:
        if not line.startswith('#') and len(line) > 50:
            metadata["preview"] = line[:200] + "..." if len(line) > 200 else line
            break
    
    return metadata


def get_category(file_path: Path) -> str:
    """Determine category from file path"""
    parts = file_path.relative_to(KB_ROOT).parts
    if len(parts) > 1:
        # Get the main category
        category = parts[0]
        if category.startswith('_'):
            return "uncategorized"
        # Add subcategory if it exists
        if len(parts) > 2:
            return f"{category}/{parts[1]}"
        return category
    return "root"


def extract_title(content: str) -> str:
    """Extract title from markdown content"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    # Fallback to first line
    if lines:
        return lines[0].strip()[:100]
    return "Untitled"


def extract_date(filename: str, content: str) -> str:
    """Extract date from filename or content"""
    # Try filename pattern: YYYY-MM-DD
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    
    # Try content for dates
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content[:500])
    if date_match:
        return date_match.group(1)
    
    return None


def index_knowledge_base() -> Dict[str, Any]:
    """Create searchable index of all knowledge base files"""
    print("=" * 60)
    print("  Knowledge Base Indexer")
    print("=" * 60)
    print()
    
    if not KB_ROOT.exists():
        print(f"❌ Knowledge base not found: {KB_ROOT}")
        return {}
    
    index = {
        "generated": datetime.now().isoformat(),
        "total_files": 0,
        "total_words": 0,
        "categories": {},
        "files": []
    }
    
    # Find all markdown files (except READMEs)
    md_files = []
    for file_path in KB_ROOT.rglob("*.md"):
        if file_path.name != "README.md" and not file_path.name.startswith('.'):
            md_files.append(file_path)
    
    print(f"📚 Found {len(md_files)} knowledge files")
    print()
    
    # Index each file
    for i, file_path in enumerate(sorted(md_files), 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = extract_metadata(file_path, content)
            
            # Add to index
            index["files"].append({
                **metadata,
                "content_preview": content[:500],  # First 500 chars for search
            })
            
            # Update category counts
            category = metadata["category"]
            if category not in index["categories"]:
                index["categories"][category] = {
                    "count": 0,
                    "total_words": 0
                }
            index["categories"][category]["count"] += 1
            index["categories"][category]["total_words"] += metadata["word_count"]
            
            # Update totals
            index["total_files"] += 1
            index["total_words"] += metadata["word_count"]
            
            if i % 20 == 0:
                print(f"  Indexed {i}/{len(md_files)} files...")
        
        except Exception as e:
            print(f"  ⚠️  Error indexing {file_path.name}: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ Indexed {index['total_files']} files")
    print(f"📊 Total words: {index['total_words']:,}")
    print(f"📁 Categories: {len(index['categories'])}")
    print("=" * 60)
    print()
    
    # Show category breakdown
    print("📂 Category Breakdown:")
    print()
    for category, stats in sorted(index["categories"].items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {category:30} {stats['count']:3} files  ({stats['total_words']:,} words)")
    
    return index


def save_index(index: Dict[str, Any]):
    """Save index to JSON file"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    print()
    print(f"💾 Index saved to: {INDEX_FILE}")


if __name__ == '__main__':
    try:
        index = index_knowledge_base()
        if index:
            save_index(index)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

