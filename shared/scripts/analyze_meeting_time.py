#!/usr/bin/env python3
"""
Meeting Time Analyzer

Extracts meeting durations from Granola imports to calculate time spent per client.
Uses heuristic estimation when exact duration not available.
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / "clients"


def parse_meeting_frontmatter(file_path):
    """Extract frontmatter from meeting note."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]

            # Parse YAML-like frontmatter
            metadata = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip("'\"")

            return metadata, parts[2]  # metadata and content

    return {}, content


def estimate_meeting_duration(file_path, metadata, content):
    """
    Estimate meeting duration in hours.

    Strategies:
    1. Look for duration in metadata or content
    2. Use word count as proxy (150 words/min average speaking rate)
    3. Default to 30 minutes if no data
    """

    # Strategy 1: Check frontmatter metadata for explicit duration
    # NOTE: Do NOT search content - speakers mention durations all the time
    # (e.g., "get back to you in 12-24 hours" transcribed as "1224 hours")
    if 'duration' in metadata and metadata['duration'] and metadata['duration'] != 'null':
        try:
            # Parse duration from metadata (e.g., "45 minutes", "1.5 hours")
            duration_str = metadata['duration'].lower()
            if 'hour' in duration_str or 'hr' in duration_str:
                match = re.search(r'(\d+\.?\d*)', duration_str)
                if match:
                    return float(match.group(1))
            elif 'min' in duration_str:
                match = re.search(r'(\d+\.?\d*)', duration_str)
                if match:
                    return float(match.group(1)) / 60.0
        except:
            pass  # Fall through to word count

    # Strategy 2: Word count-based bucketing
    # Granola transcripts are detailed, so we use conservative buckets
    word_count = len(content.split())

    if word_count > 5000:
        # Very long transcript - probably 1.5-2 hour meeting
        return 2.0
    elif word_count > 3000:
        # Long transcript - probably 1-1.5 hour meeting
        return 1.5
    elif word_count > 1500:
        # Medium transcript - probably 45-60 min meeting
        return 1.0
    elif word_count > 800:
        # Short transcript - probably 30-45 min meeting
        return 0.75
    elif word_count > 300:
        # Very short transcript - probably 15-30 min meeting
        return 0.5
    else:
        # Minimal content - default to 30 minutes
        return 0.5


def analyze_meeting_time(days_back=30):
    """
    Analyze meeting time by client over the last N days.

    Returns:
        dict: {client_name: {'meetings': count, 'hours': float}}
    """
    cutoff_date = datetime.now() - timedelta(days=days_back)

    client_data = defaultdict(lambda: {'meetings': 0, 'hours': 0.0})

    # Iterate through all client meeting folders
    for client_dir in CLIENTS_DIR.iterdir():
        if not client_dir.is_dir() or client_dir.name.startswith('.'):
            continue

        meeting_notes_dir = client_dir / "meeting-notes"
        if not meeting_notes_dir.exists():
            continue

        client_name = client_dir.name

        # Process each meeting note
        for meeting_file in meeting_notes_dir.glob("*.md"):
            try:
                # Extract date from filename: YYYY-MM-DD-title.md
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})', meeting_file.name)
                if not date_match:
                    continue

                meeting_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')

                # Skip meetings outside date range
                if meeting_date < cutoff_date:
                    continue

                # Parse meeting metadata and content
                metadata, content = parse_meeting_frontmatter(meeting_file)

                # Estimate duration
                duration_hours = estimate_meeting_duration(meeting_file, metadata, content)

                client_data[client_name]['meetings'] += 1
                client_data[client_name]['hours'] += duration_hours

            except Exception as e:
                print(f"Warning: Could not process {meeting_file}: {e}")
                continue

    return dict(client_data)


def main():
    """Run analysis and print results."""
    print("Analyzing meeting time by client (last 30 days)...")
    print()

    results = analyze_meeting_time(days_back=30)

    if not results:
        print("No meetings found in the last 30 days.")
        return

    # Sort by hours descending
    sorted_results = sorted(results.items(), key=lambda x: x[1]['hours'], reverse=True)

    total_meetings = sum(data['meetings'] for data in results.values())
    total_hours = sum(data['hours'] for data in results.values())

    print(f"Total: {total_meetings} meetings, {total_hours:.1f} hours")
    print()
    print(f"{'Client':<30} {'Meetings':<12} {'Hours':<10}")
    print("-" * 55)

    for client, data in sorted_results:
        print(f"{client:<30} {data['meetings']:<12} {data['hours']:<10.1f}")

    return results


if __name__ == "__main__":
    main()
