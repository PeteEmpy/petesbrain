#!/usr/bin/env python3
"""
Search Session History

Search across all client session logs and open questions for patterns,
decisions, or recurring themes.

Usage:
    python3 search-session-history.py "keyword"
    python3 search-session-history.py "keyword" --client smythson
    python3 search-session-history.py "budget" --type decisions
    python3 search-session-history.py "ROAS" --type questions
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/Users/administrator/Documents/PetesBrain.nosync/clients")


def get_client_display_name(client_slug):
    """Convert client slug to display name."""
    special_cases = {
        'accessories-for-the-home': 'Accessories for the Home',
        'bright-minds': 'Bright Minds',
        'clear-prospects': 'Clear Prospects',
        'devonshire-hotels': 'Devonshire Hotels',
        'tree2mydoor': 'Tree2mydoor',
        'uno-lighting': 'Uno Lighting',
        'smythson': 'Smythson',
        'superspace': 'Superspace',
    }

    if client_slug in special_cases:
        return special_cases[client_slug]

    return client_slug.replace('-', ' ').title()


def search_session_logs(keyword, client_filter=None):
    """Search session-log.md files for keyword."""
    results = []

    # Get all client directories
    client_dirs = [d for d in BASE_DIR.iterdir()
                   if d.is_dir() and not d.name.startswith('_') and not d.name.startswith('.')]

    for client_dir in sorted(client_dirs):
        client_slug = client_dir.name

        # Apply client filter if specified
        if client_filter and client_slug != client_filter:
            continue

        session_log_path = client_dir / "session-log.md"

        if not session_log_path.exists():
            continue

        content = session_log_path.read_text()

        # Search for keyword (case-insensitive)
        if keyword.lower() in content.lower():
            client_name = get_client_display_name(client_slug)

            # Extract session entries that contain the keyword
            sessions = re.findall(
                r'## Session: (\d{4}-\d{2}-\d{2}) \((.*?)\)(.*?)(?=## Session:|$)',
                content,
                re.DOTALL | re.IGNORECASE
            )

            for date, topic, session_content in sessions:
                if keyword.lower() in session_content.lower():
                    results.append({
                        'client': client_name,
                        'client_slug': client_slug,
                        'date': date,
                        'topic': topic,
                        'content': session_content.strip(),
                        'type': 'session'
                    })

    return results


def search_open_questions(keyword, client_filter=None):
    """Search open-questions.md files for keyword."""
    results = []

    # Get all client directories
    client_dirs = [d for d in BASE_DIR.iterdir()
                   if d.is_dir() and not d.name.startswith('_') and not d.name.startswith('.')]

    for client_dir in sorted(client_dirs):
        client_slug = client_dir.name

        # Apply client filter if specified
        if client_filter and client_slug != client_filter:
            continue

        open_questions_path = client_dir / "open-questions.md"

        if not open_questions_path.exists():
            continue

        content = open_questions_path.read_text()

        # Search for keyword (case-insensitive)
        if keyword.lower() in content.lower():
            client_name = get_client_display_name(client_slug)

            # Extract question blocks
            questions = re.findall(
                r'\*\*Question:\*\* (.*?)\n\*\*Noticed:\*\* (.*?)\n(.*?)(?=\*\*Question:|$)',
                content,
                re.DOTALL | re.IGNORECASE
            )

            for question, noticed, details in questions:
                if keyword.lower() in (question + details).lower():
                    results.append({
                        'client': client_name,
                        'client_slug': client_slug,
                        'question': question.strip(),
                        'noticed': noticed.strip(),
                        'details': details.strip(),
                        'type': 'question'
                    })

    return results


def extract_decisions(session_content):
    """Extract the 'Decided' section from a session."""
    decided_match = re.search(r'\*\*Decided:\*\*(.*?)(?=\*\*Still investigating:|$)',
                              session_content, re.DOTALL | re.IGNORECASE)
    if decided_match:
        return decided_match.group(1).strip()
    return None


def print_results(results, search_type='all'):
    """Print search results in formatted output."""
    if not results:
        print("❌ No results found")
        return

    print(f"\n🟢 Found {len(results)} results\n")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        if result['type'] == 'session':
            print(f"\n{i}. 📁 {result['client']} - {result['date']} ({result['topic']})")
            print(f"   Path: clients/{result['client_slug']}/session-log.md")

            if search_type == 'decisions':
                decisions = extract_decisions(result['content'])
                if decisions:
                    print(f"\n   **Decided:**")
                    print(f"   {decisions[:300]}..." if len(decisions) > 300 else f"   {decisions}")
            else:
                # Show a snippet of the content
                snippet = result['content'][:300].replace('\n', '\n   ')
                print(f"\n   {snippet}...")

        elif result['type'] == 'question':
            print(f"\n{i}. ❓ {result['client']} - {result['noticed']}")
            print(f"   Path: clients/{result['client_slug']}/open-questions.md")
            print(f"\n   **Question:** {result['question']}")
            details_snippet = result['details'][:200].replace('\n', '\n   ')
            print(f"   {details_snippet}..." if len(result['details']) > 200 else f"   {details_snippet}")

        print()

    print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Search session history and open questions')
    parser.add_argument('keyword', help='Keyword to search for')
    parser.add_argument('--client', help='Filter by specific client (slug format)')
    parser.add_argument('--type', choices=['all', 'sessions', 'questions', 'decisions'],
                        default='all', help='Type of content to search')

    args = parser.parse_args()

    print(f"\n🔍 Searching for: '{args.keyword}'")
    if args.client:
        print(f"   Client filter: {args.client}")
    if args.type != 'all':
        print(f"   Type filter: {args.type}")

    results = []

    # Search session logs
    if args.type in ['all', 'sessions', 'decisions']:
        session_results = search_session_logs(args.keyword, args.client)
        results.extend(session_results)

    # Search open questions
    if args.type in ['all', 'questions']:
        question_results = search_open_questions(args.keyword, args.client)
        results.extend(question_results)

    # Sort results by date (most recent first)
    results.sort(key=lambda x: x.get('date', x.get('noticed', '0000-00-00')), reverse=True)

    print_results(results, args.type)

    # Summary by client
    if len(results) > 1:
        clients = {}
        for r in results:
            client = r['client']
            clients[client] = clients.get(client, 0) + 1

        print("\n📊 Results by client:")
        for client, count in sorted(clients.items(), key=lambda x: x[1], reverse=True):
            print(f"   {client}: {count}")


if __name__ == "__main__":
    main()
