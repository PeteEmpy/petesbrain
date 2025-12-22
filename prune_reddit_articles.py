#!/usr/bin/env python3
"""
KB Reddit Article Pruning Script

Removes low-value Reddit articles from knowledge base inbox as part of
KB Content Strategy Upgrade (Dec 2025).

Why: Reddit posts have variable quality and cap at 2.0 authority score.
New MIN_RELEVANCE_SCORE = 8.0, so Reddit content will no longer be imported.

This script:
1. Identifies all articles with "source: Reddit" in YAML frontmatter
2. Extracts relevance scores and topics
3. Creates archive directory
4. Moves articles to archive with organized structure
5. Generates pruning report
"""

import os
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

# Paths
KB_ROOT = Path("/Users/administrator/Documents/PetesBrain.nosync/roksys/knowledge-base")
INBOX_DIR = KB_ROOT / "_inbox/documents"
ARCHIVE_DIR = KB_ROOT / "_archived/reddit-2025-12"
REPORT_FILE = KB_ROOT / "_archived/reddit-pruning-report-2025-12-16.md"


def extract_frontmatter(filepath):
    """Extract YAML frontmatter from markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = match.group(1)

    # Parse key fields
    data = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    return data


def find_reddit_articles():
    """Find all Reddit articles in inbox"""
    reddit_articles = []

    for filepath in INBOX_DIR.glob("*.md"):
        frontmatter = extract_frontmatter(filepath)

        if frontmatter.get('source', '').startswith('Reddit'):
            reddit_articles.append({
                'filepath': filepath,
                'filename': filepath.name,
                'source': frontmatter.get('source', 'Unknown'),
                'relevance_score': frontmatter.get('relevance_score', 'N/A'),
                'primary_topic': frontmatter.get('primary_topic', 'Unknown'),
                'published': frontmatter.get('published', 'N/A'),
                'url': frontmatter.get('url', 'N/A')
            })

    return reddit_articles


def archive_articles(articles, dry_run=True):
    """Archive Reddit articles to organized structure"""

    if not dry_run:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archived_count = 0

    for article in articles:
        if dry_run:
            print(f"  [DRY RUN] Would archive: {article['filename']}")
        else:
            dest_path = ARCHIVE_DIR / article['filename']
            shutil.move(str(article['filepath']), str(dest_path))
            archived_count += 1
            print(f"  ✓ Archived: {article['filename']}")

    return archived_count


def generate_report(articles):
    """Generate pruning report"""

    report = f"""# Reddit Articles Pruning Report

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Reason:** KB Content Strategy Upgrade - Remove low-value Reddit content
**Policy:** New MIN_RELEVANCE_SCORE = 8.0, Reddit posts capped at 2.0 authority

---

## Summary

- **Total Reddit articles found:** {len(articles)}
- **Archive location:** `_archived/reddit-2025-12/`
- **Status:** Moved to archive (can be restored if needed)

---

## Archived Articles

| Filename | Relevance Score | Topic | Published |
|----------|----------------|-------|-----------|
"""

    # Sort by relevance score (descending)
    try:
        sorted_articles = sorted(
            articles,
            key=lambda x: float(x['relevance_score']) if x['relevance_score'] != 'N/A' else 0,
            reverse=True
        )
    except:
        sorted_articles = articles

    for article in sorted_articles:
        filename = article['filename'][:50] + '...' if len(article['filename']) > 50 else article['filename']
        topic = article['primary_topic'][:40] + '...' if len(article['primary_topic']) > 40 else article['primary_topic']
        published = article['published'][:10] if len(article['published']) > 10 else article['published']

        report += f"| `{filename}` | {article['relevance_score']} | {topic} | {published} |\n"

    report += f"""
---

## Relevance Score Distribution

"""

    # Count by score ranges
    high = sum(1 for a in articles if a['relevance_score'] != 'N/A' and float(a['relevance_score']) >= 8)
    medium = sum(1 for a in articles if a['relevance_score'] != 'N/A' and 6 <= float(a['relevance_score']) < 8)
    low = sum(1 for a in articles if a['relevance_score'] != 'N/A' and float(a['relevance_score']) < 6)

    report += f"""- **High (≥8.0):** {high} articles
- **Medium (6.0-7.9):** {medium} articles
- **Low (<6.0):** {low} articles

**Note:** Under new rubric, Reddit posts would cap at ~4.0 composite score due to 2.0 authority cap.

---

## Next Steps

1. ✅ Reddit articles archived
2. ✅ Future Reddit imports blocked (removed from monitors)
3. [ ] Monitor Brad Geddes (Adalysis) articles for quality
4. [ ] Monitor Common Thread Collective for DTC insights
5. [ ] Verify new scoring rubric is working correctly

---

## Restoration Instructions

If any article needs to be restored:

```bash
# Move specific article back to inbox
mv _archived/reddit-2025-12/FILENAME.md _inbox/documents/

# Restore all articles (NOT RECOMMENDED)
mv _archived/reddit-2025-12/*.md _inbox/documents/
```

---

**Document Status:** Archive complete
**Related:** `docs/KB-CONTENT-STRATEGY-UPGRADE.md`, `docs/KB-CONTENT-UPGRADE-IMPLEMENTATION-SUMMARY.md`
"""

    return report


def main():
    # Check for --yes flag
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv

    print("=" * 70)
    print("KB REDDIT ARTICLES PRUNING SCRIPT")
    print("=" * 70)
    print()

    print(f"Searching for Reddit articles in: {INBOX_DIR}")
    print()

    # Find Reddit articles
    articles = find_reddit_articles()

    if not articles:
        print("✓ No Reddit articles found. KB is clean.")
        return

    print(f"Found {len(articles)} Reddit articles")
    print()

    # Show sample
    print("Sample articles:")
    for article in articles[:5]:
        print(f"  - {article['filename']}")
        print(f"    Score: {article['relevance_score']} | Topic: {article['primary_topic'][:50]}")

    if len(articles) > 5:
        print(f"  ... and {len(articles) - 5} more")
    print()

    # Dry run first
    print("=" * 70)
    print("DRY RUN - No files will be moved")
    print("=" * 70)
    print()

    archive_articles(articles, dry_run=True)
    print()

    # Ask for confirmation (or auto-confirm)
    print("=" * 70)
    if auto_confirm:
        print("Auto-confirming (--yes flag provided)")
        response = 'yes'
    else:
        response = input("Proceed with archiving? (yes/no): ")

    if response.lower() != 'yes':
        print("Cancelled. No files were moved.")
        return

    print()
    print("=" * 70)
    print("ARCHIVING ARTICLES")
    print("=" * 70)
    print()

    # Archive articles
    archived_count = archive_articles(articles, dry_run=False)

    print()
    print(f"✓ Archived {archived_count} articles to: {ARCHIVE_DIR}")
    print()

    # Generate report
    print("Generating pruning report...")
    report = generate_report(articles)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Report saved to: {REPORT_FILE}")
    print()

    print("=" * 70)
    print("PRUNING COMPLETE")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - {len(articles)} Reddit articles archived")
    print(f"  - Archive location: {ARCHIVE_DIR}")
    print(f"  - Report: {REPORT_FILE}")
    print()
    print("Next steps:")
    print("  1. Verify inbox is clean")
    print("  2. Monitor new imports (should be ≥8.0 score only)")
    print("  3. Check Brad Geddes articles are being imported")
    print()


if __name__ == "__main__":
    main()
