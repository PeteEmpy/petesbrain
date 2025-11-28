#!/usr/bin/env python3
"""
Weekly Experiment Review

Scans the ROK experiments CSV for experiments older than configurable threshold
and prompts user to review and categorize outcomes.

Helps migrate completed experiments from CSV to CONTEXT.md structured tables.

Usage:
    python3 weekly-experiment-review.py           # Interactive mode (requires terminal)
    python3 weekly-experiment-review.py --auto    # Automated mode (generates report, no prompts)
    python3 weekly-experiment-review.py --report  # Just print pending experiments

Runs every Friday at 4:00 PM via LaunchAgent (--auto mode).
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
EXPERIMENTS_CSV = PROJECT_ROOT / "roksys/spreadsheets/rok-experiments-client-notes.csv"
STATE_FILE = PROJECT_ROOT / "data/state/experiment-review-state.json"
LOG_FILE = PROJECT_ROOT / "data/cache/experiment-review.log"

# Configuration
MIN_DAYS_BEFORE_REVIEW = 14  # Review experiments older than 14 days
REVIEW_LOOKBACK_DAYS = 60     # Look at experiments from last 60 days


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    print(log_entry.strip())

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_state():
    """Load previously reviewed experiment IDs"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"reviewed_experiments": [], "last_run": None}


def save_state(state):
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def parse_date(date_str):
    """Parse date from CSV (format: DD/MM/YYYY HH:MM)"""
    try:
        # Try with time first
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    except ValueError:
        try:
            # Try without time
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            return None


def load_experiments():
    """Load experiments from CSV"""
    if not EXPERIMENTS_CSV.exists():
        log_message(f"❌ Experiments CSV not found: {EXPERIMENTS_CSV}")
        return []

    experiments = []

    with open(EXPERIMENTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = row.get('Timestamp', '')
            client = row.get('Client', '') or ''
            note = row.get('Note', '') or ''
            tags = row.get('Tags (optional)', '') or ''

            client = client.strip()
            note = note.strip()
            tags = tags.strip()

            if not timestamp or not client or not note:
                continue

            date = parse_date(timestamp)
            if not date:
                continue

            # Create unique ID for experiment
            exp_id = f"{timestamp}_{client}_{note[:50]}"

            experiments.append({
                'id': exp_id,
                'timestamp': timestamp,
                'date': date,
                'client': client,
                'note': note,
                'tags': tags,
                'age_days': (datetime.now() - date).days
            })

    return experiments


def filter_experiments_for_review(experiments, state):
    """Filter experiments that need review"""
    reviewed_ids = set(state.get('reviewed_experiments', []))
    cutoff_date = datetime.now() - timedelta(days=REVIEW_LOOKBACK_DAYS)
    min_age_date = datetime.now() - timedelta(days=MIN_DAYS_BEFORE_REVIEW)

    needs_review = []

    for exp in experiments:
        # Skip if already reviewed
        if exp['id'] in reviewed_ids:
            continue

        # Skip if too old (outside lookback window)
        if exp['date'] < cutoff_date:
            continue

        # Skip if too recent (less than min age)
        if exp['date'] > min_age_date:
            continue

        needs_review.append(exp)

    return needs_review


def group_by_client(experiments):
    """Group experiments by client"""
    by_client = defaultdict(list)
    for exp in experiments:
        by_client[exp['client']].append(exp)
    return dict(by_client)


def prompt_for_outcome(exp):
    """Prompt user for experiment outcome"""
    print("\n" + "=" * 80)
    print(f"CLIENT: {exp['client']}")
    print(f"DATE: {exp['timestamp']} ({exp['age_days']} days ago)")
    print(f"EXPERIMENT:")
    print(f"  {exp['note']}")
    if exp['tags']:
        print(f"TAGS: {exp['tags']}")
    print("=" * 80)
    print()
    print("What happened with this experiment?")
    print()
    print("  1. Still monitoring (check again next week)")
    print("  2. Successful (add to CONTEXT.md Successful Tests)")
    print("  3. Failed (add to CONTEXT.md Failed Tests)")
    print("  4. Inconclusive (archive, note in CONTEXT.md)")
    print("  5. Skip (mark as reviewed, don't add to CONTEXT.md)")
    print()

    while True:
        choice = input("Enter choice (1-5) or 'q' to quit: ").strip().lower()

        if choice == 'q':
            return 'quit'

        if choice in ['1', '2', '3', '4', '5']:
            return choice

        print("Invalid choice. Please enter 1-5 or 'q'.")


def get_outcome_details(exp, choice):
    """Get additional details for outcome"""
    if choice == '1':
        # Still monitoring
        return {
            'status': 'monitoring',
            'action': 'Check again next week'
        }

    elif choice == '2':
        # Successful
        print("\nWhat was the RESULT? (e.g., '+22% revenue', 'Improved CTR by 15%')")
        result = input("> ").strip()

        print("\nWhat ACTION was taken? (e.g., 'Monitoring for optimization', 'Rolled out to other campaigns')")
        action = input("> ").strip()

        return {
            'status': 'successful',
            'result': result,
            'action': action
        }

    elif choice == '3':
        # Failed
        print("\nWhy did it FAIL? (e.g., 'No impact on conversions', 'CPA increased by 25%')")
        why_failed = input("> ").strip()

        print("\nWhat did we LEARN? (e.g., 'Need more data before changing targets', 'Product pages need optimization first')")
        lesson = input("> ").strip()

        return {
            'status': 'failed',
            'why_failed': why_failed,
            'lesson': lesson
        }

    elif choice == '4':
        # Inconclusive
        print("\nWhy was it INCONCLUSIVE? (e.g., 'External factors interfered', 'Not enough data')")
        reason = input("> ").strip()

        return {
            'status': 'inconclusive',
            'reason': reason
        }

    elif choice == '5':
        # Skip
        return {
            'status': 'skipped'
        }


def update_context_file(client, exp, outcome):
    """Update client CONTEXT.md with experiment outcome"""
    # Find client folder (handle case-insensitive matching)
    clients_dir = PROJECT_ROOT / "clients"
    client_folder = None

    for folder in clients_dir.iterdir():
        if folder.is_dir() and folder.name.lower() == client.lower().replace(' ', '-'):
            client_folder = folder
            break

    if not client_folder:
        # Try exact match
        client_folder = clients_dir / client.lower().replace(' ', '-')
        if not client_folder.exists():
            log_message(f"⚠️  Could not find client folder for: {client}")
            return False

    context_file = client_folder / "CONTEXT.md"

    if not context_file.exists():
        log_message(f"⚠️  CONTEXT.md not found for {client}")
        return False

    # Read existing content
    with open(context_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Format date
    date_obj = parse_date(exp['timestamp'])
    formatted_date = date_obj.strftime('%b %d, %Y') if date_obj else exp['timestamp']

    # Prepare table row
    if outcome['status'] == 'successful':
        # Find Successful Tests table
        table_marker = "### Successful Tests & Experiments"
        if table_marker not in content:
            log_message(f"⚠️  Successful Tests table not found in {client} CONTEXT.md")
            return False

        # Create row
        row = f"| {formatted_date} | {exp['note'][:100]} | {outcome['result']} | {outcome['action']} |"

        # Insert after header row
        lines = content.split('\n')
        insert_index = None
        for i, line in enumerate(lines):
            if table_marker in line:
                # Find the header separator line (|------|)
                for j in range(i, min(i + 5, len(lines))):
                    if '|---' in lines[j]:
                        insert_index = j + 1
                        break
                break

        if insert_index:
            lines.insert(insert_index, row)
            content = '\n'.join(lines)
            log_message(f"✅ Added successful experiment to {client} CONTEXT.md")

    elif outcome['status'] == 'failed':
        # Find Failed Tests table
        table_marker = "### Failed Tests (Learn From)"
        if table_marker not in content:
            log_message(f"⚠️  Failed Tests table not found in {client} CONTEXT.md")
            return False

        # Create row
        row = f"| {formatted_date} | {exp['note'][:100]} | {outcome['why_failed']} | {outcome['lesson']} |"

        # Insert after header row
        lines = content.split('\n')
        insert_index = None
        for i, line in enumerate(lines):
            if table_marker in line:
                # Find the header separator line (|------|)
                for j in range(i, min(i + 5, len(lines))):
                    if '|---' in lines[j]:
                        insert_index = j + 1
                        break
                break

        if insert_index:
            lines.insert(insert_index, row)
            content = '\n'.join(lines)
            log_message(f"✅ Added failed experiment to {client} CONTEXT.md")

    elif outcome['status'] == 'inconclusive':
        # Add note to Recent Actions section if it exists
        section_marker = "## Recent Actions & Updates"
        if section_marker in content:
            # Find current month section
            month_str = datetime.now().strftime('%B %Y')
            month_marker = f"### {month_str}"

            note_line = f"- **{formatted_date}**: Experiment inconclusive - {exp['note'][:100]}. Reason: {outcome['reason']}"

            # Try to insert in current month section
            lines = content.split('\n')
            insert_index = None

            for i, line in enumerate(lines):
                if month_marker in line:
                    insert_index = i + 1
                    break

            if insert_index:
                lines.insert(insert_index, note_line)
                content = '\n'.join(lines)
                log_message(f"✅ Added inconclusive experiment note to {client} CONTEXT.md")

    # Write updated content
    with open(context_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def generate_report(needs_review, by_client):
    """Generate a text report of experiments needing review"""
    lines = []
    lines.append("=" * 80)
    lines.append("EXPERIMENT REVIEW REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Total experiments needing review: {len(needs_review)}")
    lines.append(f"Clients: {', '.join(sorted(by_client.keys()))}")
    lines.append("")

    for client, client_exps in sorted(by_client.items()):
        lines.append("-" * 60)
        lines.append(f"CLIENT: {client} ({len(client_exps)} experiment(s))")
        lines.append("-" * 60)

        for exp in sorted(client_exps, key=lambda x: x['date']):
            lines.append(f"  [{exp['age_days']} days ago] {exp['timestamp']}")
            lines.append(f"    {exp['note']}")
            if exp['tags']:
                lines.append(f"    Tags: {exp['tags']}")
            lines.append("")

    return "\n".join(lines)


def run_auto_mode():
    """
    Automated mode for LaunchAgent execution.

    - No interactive prompts
    - Generates report of pending experiments
    - Logs status and creates notification if experiments are pending
    """
    log_message("🤖 Running in AUTO mode")

    # Load data
    state = load_state()
    experiments = load_experiments()

    if not experiments:
        log_message("No experiments found in CSV")
        return 0

    log_message(f"📋 Loaded {len(experiments)} total experiments from CSV")

    # Filter for review
    needs_review = filter_experiments_for_review(experiments, state)

    if not needs_review:
        log_message("✅ No experiments need review at this time")
        return 0

    # Group by client
    by_client = group_by_client(needs_review)

    log_message(f"🔍 Found {len(needs_review)} experiment(s) ready for review across {len(by_client)} client(s)")

    # Generate report
    report = generate_report(needs_review, by_client)

    # Save report to file
    report_file = PROJECT_ROOT / "data/cache/experiment-review-pending.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(report)

    log_message(f"📄 Report saved to: {report_file}")

    # Print summary
    print(report)

    # Create a task reminder if experiments are pending (optional integration)
    # This could create a Google Task or send notification
    summary = f"{len(needs_review)} experiment(s) ready for review: {', '.join(sorted(by_client.keys()))}"
    log_message(f"📊 Summary: {summary}")

    # Update last run time
    state['last_run'] = datetime.now().isoformat()
    save_state(state)

    return len(needs_review)


def run_report_mode():
    """
    Report-only mode - just print what needs review without any state changes.
    """
    state = load_state()
    experiments = load_experiments()

    if not experiments:
        print("No experiments found in CSV")
        return 0

    needs_review = filter_experiments_for_review(experiments, state)

    if not needs_review:
        print("✅ No experiments need review at this time")
        return 0

    by_client = group_by_client(needs_review)
    report = generate_report(needs_review, by_client)
    print(report)

    return len(needs_review)


def run_review():
    """Main interactive review function"""
    print("=" * 80)
    print("WEEKLY EXPERIMENT REVIEW")
    print("=" * 80)
    print()
    print(f"Scanning experiments from last {REVIEW_LOOKBACK_DAYS} days...")
    print(f"Reviewing experiments older than {MIN_DAYS_BEFORE_REVIEW} days...")
    print()

    # Load data
    state = load_state()
    experiments = load_experiments()

    if not experiments:
        log_message("No experiments found in CSV")
        return

    log_message(f"📋 Loaded {len(experiments)} total experiments from CSV")

    # Filter for review
    needs_review = filter_experiments_for_review(experiments, state)

    if not needs_review:
        log_message("✅ No experiments need review at this time")
        print()
        print("All caught up! No experiments to review.")
        return

    log_message(f"🔍 Found {len(needs_review)} experiment(s) ready for review")
    print()
    print(f"📊 {len(needs_review)} experiment(s) ready for review")
    print()

    # Group by client
    by_client = group_by_client(needs_review)

    print(f"Clients with experiments to review: {', '.join(by_client.keys())}")
    print()
    input("Press Enter to start review...")

    # Review each experiment
    reviewed_count = 0
    updated_count = 0

    for client, client_exps in sorted(by_client.items()):
        print(f"\n\n{'=' * 80}")
        print(f"CLIENT: {client} ({len(client_exps)} experiment(s))")
        print('=' * 80)

        for exp in client_exps:
            choice = prompt_for_outcome(exp)

            if choice == 'quit':
                log_message(f"Review interrupted by user. Reviewed {reviewed_count} experiment(s).")
                save_state(state)
                return

            # Get outcome details
            outcome = get_outcome_details(exp, choice)

            # Update CONTEXT.md if needed
            if outcome['status'] in ['successful', 'failed', 'inconclusive']:
                if update_context_file(client, exp, outcome):
                    updated_count += 1

            # Mark as reviewed (except if still monitoring)
            if outcome['status'] != 'monitoring':
                state['reviewed_experiments'].append(exp['id'])
                reviewed_count += 1

            # Save state after each experiment
            state['last_run'] = datetime.now().isoformat()
            save_state(state)

    print()
    print("=" * 80)
    print("REVIEW COMPLETE")
    print("=" * 80)
    print()
    log_message(f"✅ Review complete: {reviewed_count} experiment(s) reviewed, {updated_count} CONTEXT.md file(s) updated")
    print(f"📝 Reviewed: {reviewed_count} experiment(s)")
    print(f"✏️  Updated: {updated_count} CONTEXT.md file(s)")
    print()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Weekly Experiment Review - Review and migrate completed experiments'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Run in automated mode (no prompts, generates report only)'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Just print pending experiments without state changes'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        if args.auto:
            # Automated mode for LaunchAgent
            pending_count = run_auto_mode()
            sys.exit(0 if pending_count == 0 else 0)  # Always exit 0 for LaunchAgent
        elif args.report:
            # Report-only mode
            run_report_mode()
            sys.exit(0)
        else:
            # Interactive mode
            run_review()
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nReview interrupted by user.")
        sys.exit(0)
    except Exception as e:
        log_message(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
