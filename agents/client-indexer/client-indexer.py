#!/usr/bin/env python3
"""
Client Content Indexer

Creates a searchable index of all client content including CONTEXT.md, meetings,
emails, documents, reports, and tasks-completed.md. Also indexes Roksys content.

Follows the same pattern as knowledge-base-indexer.py but for client folders.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_ROOT = PROJECT_ROOT / "clients"
ROKSYS_ROOT = PROJECT_ROOT / "roksys"
INDEX_FILE = PROJECT_ROOT / "shared" / "data" / "client-index.json"


def extract_metadata(file_path: Path, content: str, client_name: str, content_type: str) -> Dict[str, Any]:
    """Extract metadata from file"""
    metadata = {
        "path": str(file_path.relative_to(PROJECT_ROOT)),
        "filename": file_path.name,
        "client": client_name,
        "content_type": content_type,
        "title": extract_title(content, file_path),
        "date": extract_date(file_path.name, content),
        "word_count": len(content.split()),
        "size_bytes": file_path.stat().st_size,
        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
    }
    
    # Extract first meaningful paragraph as preview
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    for line in lines:
        if not line.startswith('#') and not line.startswith('>') and len(line) > 50:
            metadata["preview"] = line[:200] + "..." if len(line) > 200 else line
            break
    
    return metadata


def extract_title(content: str, file_path: Path) -> str:
    """Extract title from content or filename"""
    lines = content.split('\n')
    
    # Try to find markdown heading
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    
    # Try to find subject line (for emails)
    for line in lines[:10]:
        if line.startswith('Subject:'):
            return line.replace('Subject:', '').strip()
    
    # Use filename without extension and date prefix
    name = file_path.stem
    # Remove date prefix pattern: YYYY-MM-DD-
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    name = name.replace('-', ' ').replace('_', ' ').title()
    
    return name if name else "Untitled"


def extract_date(filename: str, content: str) -> str:
    """Extract date from filename or content"""
    # Try filename pattern: YYYY-MM-DD
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        return date_match.group(1)
    
    # Try content for dates in first 500 chars
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content[:500])
    if date_match:
        return date_match.group(1)
    
    return None


def get_content_type(file_path: Path, client_root: Path) -> str:
    """Determine content type from file path"""
    relative = file_path.relative_to(client_root)
    parts = relative.parts
    
    # Check if it's a main file
    if file_path.name == "CONTEXT.md":
        return "context"
    if file_path.name == "tasks-completed.md":
        return "tasks-completed"
    
    # Determine from folder
    if len(parts) > 1:
        folder = parts[0]
        if folder == "meeting-notes":
            return "meeting"
        elif folder == "emails":
            return "email"
        elif folder == "documents":
            return "document"
        elif folder == "briefs":
            return "brief"
        elif folder == "reports":
            return "report"
        elif folder == "presentations":
            return "presentation"
        elif folder == "knowledge-base":
            # For Roksys knowledge base
            if len(parts) > 2:
                return f"knowledge-base/{parts[1]}"
            return "knowledge-base"
    
    return "other"


def index_client_folder(client_path: Path, client_name: str) -> List[Dict[str, Any]]:
    """Index all content in a client folder"""
    files = []
    
    # Define file patterns to index
    patterns = [
        "CONTEXT.md",
        "tasks-completed.md",
        "meeting-notes/*.md",
        "emails/*.md",
        "documents/*.md",
        "briefs/*.md",
        "reports/*.md",
        "reports/*/*.md",
        "reports/*.html",
        "reports/*/*.html",
    ]
    
    for pattern in patterns:
        for file_path in client_path.glob(pattern):
            if file_path.is_file() and not file_path.name.startswith('.'):
                files.append(file_path)
    
    # Index each file
    indexed_files = []
    for file_path in files:
        try:
            # Read content based on file type
            if file_path.suffix == '.html':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Strip HTML tags for preview (basic)
                content = re.sub(r'<[^>]+>', ' ', content)
                content = re.sub(r'\s+', ' ', content)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            content_type = get_content_type(file_path, client_path)
            metadata = extract_metadata(file_path, content, client_name, content_type)
            
            indexed_files.append({
                **metadata,
                "content_preview": content[:500],  # First 500 chars for search
            })
        
        except Exception as e:
            print(f"  ⚠️  Error indexing {file_path.name}: {e}")
    
    return indexed_files


def index_roksys_special() -> List[Dict[str, Any]]:
    """Index special Roksys content (meetings, documents, methodologies)"""
    files = []
    
    # Patterns for Roksys
    patterns = [
        ("meeting-notes/*.md", "meeting"),
        ("documents/*.md", "document"),
        ("knowledge-base/rok-methodologies/*.md", "methodology"),
    ]
    
    indexed_files = []
    for pattern, content_type in patterns:
        for file_path in ROKSYS_ROOT.glob(pattern):
            if file_path.is_file() and not file_path.name.startswith('.') and file_path.name != "README.md":
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    metadata = extract_metadata(file_path, content, "Roksys", content_type)
                    
                    indexed_files.append({
                        **metadata,
                        "content_preview": content[:500],
                    })
                
                except Exception as e:
                    print(f"  ⚠️  Error indexing {file_path.name}: {e}")
    
    return indexed_files


def index_all_clients() -> Dict[str, Any]:
    """Create searchable index of all client content"""
    print("=" * 60)
    print("  Client Content Indexer")
    print("=" * 60)
    print()
    
    if not CLIENTS_ROOT.exists():
        print(f"❌ Clients folder not found: {CLIENTS_ROOT}")
        return {}
    
    index = {
        "generated": datetime.now().isoformat(),
        "total_files": 0,
        "total_words": 0,
        "clients": {},
        "content_types": {},
        "files": []
    }
    
    # Get all client folders (skip templates and unassigned)
    client_folders = [
        d for d in CLIENTS_ROOT.iterdir()
        if d.is_dir() and not d.name.startswith('_') and not d.name.startswith('.')
    ]
    
    print(f"📁 Found {len(client_folders)} client folders")
    print()
    
    # Index each client
    for client_path in sorted(client_folders):
        client_name = client_path.name.replace('-', ' ').title()
        print(f"  Indexing {client_name}...")
        
        client_files = index_client_folder(client_path, client_name)
        
        if client_files:
            # Add to main index
            index["files"].extend(client_files)
            
            # Track client stats
            index["clients"][client_name] = {
                "count": len(client_files),
                "total_words": sum(f["word_count"] for f in client_files)
            }
            
            # Track content type stats
            for file_data in client_files:
                content_type = file_data["content_type"]
                if content_type not in index["content_types"]:
                    index["content_types"][content_type] = {
                        "count": 0,
                        "total_words": 0
                    }
                index["content_types"][content_type]["count"] += 1
                index["content_types"][content_type]["total_words"] += file_data["word_count"]
            
            print(f"    ✓ {len(client_files)} files indexed")
    
    # Index Roksys content
    print()
    print("  Indexing Roksys content...")
    roksys_files = index_roksys_special()
    
    if roksys_files:
        index["files"].extend(roksys_files)
        
        # Track Roksys stats
        index["clients"]["Roksys"] = {
            "count": len(roksys_files),
            "total_words": sum(f["word_count"] for f in roksys_files)
        }
        
        # Track content types
        for file_data in roksys_files:
            content_type = file_data["content_type"]
            if content_type not in index["content_types"]:
                index["content_types"][content_type] = {
                    "count": 0,
                    "total_words": 0
                }
            index["content_types"][content_type]["count"] += 1
            index["content_types"][content_type]["total_words"] += file_data["word_count"]
        
        print(f"    ✓ {len(roksys_files)} files indexed")
    
    # Update totals
    index["total_files"] = len(index["files"])
    index["total_words"] = sum(f["word_count"] for f in index["files"])
    
    print()
    print("=" * 60)
    print(f"✅ Indexed {index['total_files']} files")
    print(f"📊 Total words: {index['total_words']:,}")
    print(f"👥 Clients: {len(index['clients'])}")
    print(f"📂 Content types: {len(index['content_types'])}")
    print("=" * 60)
    print()
    
    # Show client breakdown
    print("👥 Client Breakdown:")
    print()
    for client, stats in sorted(index["clients"].items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {client:30} {stats['count']:3} files  ({stats['total_words']:,} words)")
    
    print()
    print("📂 Content Type Breakdown:")
    print()
    for content_type, stats in sorted(index["content_types"].items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {content_type:30} {stats['count']:3} files  ({stats['total_words']:,} words)")
    
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
        index = index_all_clients()
        if index:
            save_index(index)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

