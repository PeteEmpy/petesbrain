#!/usr/bin/env python3
"""
Knowledge Base Inbox Processor

Automatically processes files in the knowledge base inbox:
1. Reads files from roksys/knowledge-base/_inbox/
2. Analyzes content using Claude API
3. Categorizes and moves to appropriate knowledge base folder
4. Updates knowledge base index
5. Logs processing activity

Runs automatically every 6 hours via LaunchAgent
"""

import os
import sys
import json
import shutil
import re
from datetime import datetime
from pathlib import Path
import anthropic
from youtube_transcript_api import YouTubeTranscriptApi

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
INBOX_ROOT = PROJECT_ROOT / "roksys/knowledge-base/_inbox"
KB_ROOT = PROJECT_ROOT / "roksys/knowledge-base"
LOG_FILE = PROJECT_ROOT / "data/cache/kb-processing.log"

# Knowledge base categories
CATEGORIES = {
    "google-ads/performance-max": "Performance Max campaigns, optimization, strategies",
    "google-ads/shopping": "Shopping campaigns, product feeds, merchant center",
    "google-ads/search": "Search campaigns, keywords, ad copy",
    "google-ads/platform-updates": "Google Ads platform updates and announcements",
    "google-ads/bidding-automation": "Smart Bidding, tROAS, automated bidding strategies",
    "ai-strategy": "AI in marketing, automation, machine learning",
    "analytics": "Google Analytics, attribution, tracking, measurement",
    "industry-insights": "Market trends, competitive intelligence, research",
    "rok-methodologies": "ROK frameworks, processes, best practices"
}


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    print(log_entry.strip())

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def read_file_content(file_path):
    """Read content from various file types"""
    try:
        # Try reading as text
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        # If binary file (PDF, etc.), return a note
        return f"[Binary file: {file_path.name}. Manual processing may be required.]"
    except Exception as e:
        log_message(f"Error reading {file_path}: {e}")
        return None


def extract_youtube_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_youtube_transcript(video_id):
    """Fetch transcript for a YouTube video"""
    try:
        # Create API instance and fetch transcript
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)

        # Combine all transcript segments into full text
        full_transcript = ' '.join([entry.text for entry in transcript_list])

        return full_transcript
    except Exception as e:
        log_message(f"Error fetching transcript for video {video_id}: {e}")
        return None


def detect_and_process_youtube_urls(content):
    """Detect YouTube URLs in content and fetch their transcripts"""
    # Find all YouTube URLs in the content
    youtube_url_pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    urls = re.findall(youtube_url_pattern, content)

    if not urls:
        return None

    log_message(f"Found {len(urls)} YouTube URL(s)")

    # Process each URL
    all_transcripts = []
    for url_match in re.finditer(youtube_url_pattern, content):
        full_url = url_match.group(0)
        video_id = extract_youtube_video_id(full_url)

        if video_id:
            log_message(f"Fetching transcript for video: {video_id}")
            transcript = fetch_youtube_transcript(video_id)

            if transcript:
                all_transcripts.append({
                    'url': full_url,
                    'video_id': video_id,
                    'transcript': transcript
                })
                log_message(f"✓ Successfully fetched transcript ({len(transcript)} chars)")
            else:
                log_message(f"✗ Failed to fetch transcript for {video_id}")

    if not all_transcripts:
        return None

    # Combine all transcripts into formatted content
    formatted_content = ""
    for item in all_transcripts:
        formatted_content += f"\n\n## Video: {item['url']}\n\n"
        formatted_content += f"**Video ID**: {item['video_id']}\n\n"
        formatted_content += f"### Transcript\n\n{item['transcript']}\n\n"

    return formatted_content


def analyze_content(content, filename):
    """Use Claude API to analyze content and determine category"""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set. Cannot analyze content.")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analyze this knowledge base content and help me organize it.

Filename: {filename}

Content:
{content[:8000]}  # Limit to avoid token issues

Please provide:
1. A clear, descriptive title for this document
2. The best category from this list:
   - google-ads/performance-max
   - google-ads/shopping
   - google-ads/search
   - google-ads/platform-updates
   - google-ads/bidding-automation
   - ai-strategy
   - analytics
   - industry-insights
   - rok-methodologies

3. A brief summary (3-5 bullet points) of key takeaways
4. 3-5 relevant tags
5. Key insights and actionable recommendations

Respond in JSON format:
{{
    "title": "Document Title",
    "category": "category/subcategory",
    "summary": ["point 1", "point 2", "point 3"],
    "tags": ["tag1", "tag2", "tag3"],
    "key_insights": ["insight 1", "insight 2"],
    "source_type": "email|article|video|document",
    "recommended_filename": "descriptive-filename.md"
}}"""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        response_text = response.content[0].text

        # Try to find JSON in the response
        if '{' in response_text and '}' in response_text:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_str = response_text[json_start:json_end]
            analysis = json.loads(json_str)
            return analysis
        else:
            log_message(f"Could not parse JSON from Claude response for {filename}")
            return None

    except Exception as e:
        log_message(f"Error analyzing content with Claude: {e}")
        return None


def create_formatted_document(analysis, original_content, source_file):
    """Create formatted markdown document"""

    today = datetime.now().strftime("%Y-%m-%d")

    # Build frontmatter
    frontmatter = f"""---
title: {analysis['title']}
source: {source_file.name}
date_added: {today}
last_updated: {today}
tags: [{', '.join(analysis['tags'])}]
source_type: {analysis.get('source_type', 'document')}
---

## Summary

{chr(10).join(['- ' + point for point in analysis['summary']])}

## Key Insights

{chr(10).join(['- ' + insight for insight in analysis['key_insights']])}

## Full Content

{original_content}

---

*Processed from inbox on {today}*
*Original file: {source_file.name}*
"""

    return frontmatter


def process_inbox_file(file_path):
    """Process a single file from the inbox"""

    log_message(f"Processing: {file_path.name}")

    # Read content
    content = read_file_content(file_path)
    if not content:
        log_message(f"Skipping {file_path.name}: Could not read content")
        return False

    # Check if content contains YouTube URLs
    youtube_content = detect_and_process_youtube_urls(content)
    if youtube_content:
        log_message("YouTube URLs detected - using fetched transcripts")
        content = youtube_content

    # Analyze with Claude
    analysis = analyze_content(content, file_path.name)
    if not analysis:
        log_message(f"Skipping {file_path.name}: Could not analyze content")
        return False

    # Create formatted document
    formatted_doc = create_formatted_document(analysis, content, file_path)

    # Determine destination
    category = analysis['category']
    filename = analysis['recommended_filename']

    dest_dir = KB_ROOT / category
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_file = dest_dir / filename

    # Write formatted document
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(formatted_doc)

    log_message(f"✓ Filed: {category}/{filename}")

    # Remove original from inbox
    file_path.unlink()

    return True


def update_knowledge_base_index():
    """Update the main knowledge base README with current inventory"""

    log_message("Updating knowledge base index...")

    # Count documents in each category
    category_counts = {}
    total_docs = 0

    for category in CATEGORIES.keys():
        category_path = KB_ROOT / category
        if category_path.exists():
            md_files = list(category_path.glob("*.md"))
            category_counts[category] = len(md_files)
            total_docs += len(md_files)

    # Count inbox items
    inbox_count = 0
    for subdir in ['emails', 'documents', 'videos']:
        inbox_subdir = INBOX_ROOT / subdir
        if inbox_subdir.exists():
            inbox_count += len(list(inbox_subdir.glob("*")))

    # Read current README
    readme_path = KB_ROOT / "README.md"
    with open(readme_path, 'r') as f:
        readme_content = f.read()

    # Update last updated date
    readme_content = readme_content.replace(
        f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}",
        f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}"
    )

    # Update totals (simple replacement)
    readme_lines = readme_content.split('\n')
    for i, line in enumerate(readme_lines):
        if line.startswith('**Total Documents**:'):
            readme_lines[i] = f"**Total Documents**: {total_docs}"
        elif line.startswith('**Inbox Items Pending**:'):
            readme_lines[i] = f"**Inbox Items Pending**: {inbox_count}"

    # Write back
    with open(readme_path, 'w') as f:
        f.write('\n'.join(readme_lines))

    log_message(f"✓ Index updated: {total_docs} total documents, {inbox_count} inbox items pending")


def process_inbox():
    """Main function to process all inbox files"""

    log_message("=" * 60)
    log_message("Knowledge Base Inbox Processing Started")
    log_message("=" * 60)

    processed_count = 0
    error_count = 0

    # Check all inbox subdirectories
    for subdir in ['emails', 'documents', 'videos']:
        inbox_subdir = INBOX_ROOT / subdir

        if not inbox_subdir.exists():
            continue

        # Process each file
        for file_path in inbox_subdir.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.') and file_path.name != 'README.md':
                try:
                    if process_inbox_file(file_path):
                        processed_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    log_message(f"ERROR processing {file_path.name}: {e}")
                    error_count += 1

    # Update index
    if processed_count > 0:
        update_knowledge_base_index()

    log_message("=" * 60)
    log_message(f"Processing Complete: {processed_count} processed, {error_count} errors")
    log_message("=" * 60)


if __name__ == "__main__":
    process_inbox()
