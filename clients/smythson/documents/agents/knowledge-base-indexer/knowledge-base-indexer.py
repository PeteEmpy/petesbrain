#!/usr/bin/env python3
"""
Knowledge Base Indexer
Scans all markdown files in the knowledge base and creates a searchable index.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
KB_ROOT = PROJECT_ROOT / "roksys/knowledge-base"
INDEX_FILE = PROJECT_ROOT / "data/cache/kb-index.json"

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown"""
    frontmatter = {}
    if content.startswith('---'):
        try:
            end = content.find('\n---\n', 4)
            if end > 0:
                fm_text = content[4:end]
                for line in fm_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
        except:
            pass
    return frontmatter

def extract_date_from_filename(filename):
    """Extract date from filename like 2025-11-18_title.md"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None

def index_knowledge_base():
    """Scan knowledge base and create index"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Indexing knowledge base...")

    files = []
    total_files = 0

    for md_file in KB_ROOT.rglob("*.md"):
        # Skip README and index files
        if md_file.name in ['README.md', 'INDEX.md', 'QUICKSTART.md']:
            continue

        # Skip _inbox directory
        if '_inbox' in md_file.parts:
            continue

        total_files += 1

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Get file metadata
            stat = md_file.stat()
            modified_timestamp = stat.st_mtime

            # Extract frontmatter
            frontmatter = extract_frontmatter(content)

            # Get date (from frontmatter, filename, or modified time)
            date = frontmatter.get('date') or extract_date_from_filename(md_file.name)
            if not date:
                date = datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d')

            # Get category from path
            relative_path = md_file.relative_to(KB_ROOT)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "uncategorized"

            # Get title (from frontmatter, first heading, or filename)
            title = frontmatter.get('title')
            if not title:
                # Try to find first heading
                heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if heading_match:
                    title = heading_match.group(1).strip()
                else:
                    title = md_file.stem.replace('_', ' ').replace('-', ' ').title()

            # Get content preview (first 500 chars, skip frontmatter)
            content_start = content.find('\n---\n', 4)
            if content_start > 0:
                preview_content = content[content_start + 5:]
            else:
                preview_content = content

            # Remove markdown formatting for preview
            preview = re.sub(r'[#*`\[\]()]', '', preview_content)
            preview = ' '.join(preview.split())[:500]

            file_data = {
                "path": str(relative_path),
                "title": title,
                "category": category,
                "date": date,
                "modified": modified_timestamp,
                "content_preview": preview,
                "file_id": hashlib.md5(str(relative_path).encode()).hexdigest()
            }

            files.append(file_data)

        except Exception as e:
            print(f"Error indexing {md_file}: {e}")

    # Create index
    index = {
        "generated": datetime.now().isoformat(),
        "total_files": len(files),
        "scanned_files": total_files,
        "files": files
    }

    # Save index
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Indexed {len(files)} files")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Index saved to {INDEX_FILE}")

    return index

if __name__ == '__main__':
    index_knowledge_base()
