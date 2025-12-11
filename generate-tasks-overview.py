#!/usr/bin/env python3
"""
Generate ALL Tasks Overview HTML Files
- Standard view (by client): tasks-overview.html
- Priority view (by P0/P1/P2/P3): tasks-overview-priority.html

This single script generates BOTH views to ensure they're always in sync.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

def escape_template_strings(text):
    """Escape backticks and ${} to prevent breaking JavaScript template strings"""
    if not text:
        return text
    # Replace backticks with single quotes and escape ${ sequences
    # Backticks break JavaScript template strings, so we replace them
    return text.replace('`', "'").replace('${', '\\${}')


def normalize_title_for_dedup(title):
    """
    Normalize task title for duplicate detection.
    Strips prefixes, timestamps, trailing numbers, and common noise.
    """
    import difflib
    # Lowercase and strip
    title = title.lower().strip()
    # Remove common prefixes like [Client], [Personal], [Roksys]
    title = re.sub(r'^\[[^\]]+\]\s*', '', title)
    # Remove timestamps and dates
    title = re.sub(r'\d{8}[-_]?\d{6}', '', title)  # 20251123-090757
    title = re.sub(r'\d{4}-\d{2}-\d{2}', '', title)  # 2025-11-23
    # Remove "wispr quick note" prefix
    title = re.sub(r'wispr\s*(quick\s*)?note\s*', '', title)
    # Remove trailing numbers (like "-1", "-2", etc.)
    title = re.sub(r'[-_]\d+$', '', title)
    # Collapse whitespace
    title = ' '.join(title.split())
    return title.strip()


def deduplicate_internal_tasks(tasks, threshold=0.95):
    """
    Deduplicate tasks within the internal task list.
    Keeps the first occurrence (based on order) and removes similar duplicates.
    Returns (deduplicated_tasks, duplicates_removed_count)

    Note: Uses a high threshold (0.95) to avoid false positives on sequential
    tasks like "Week 1: Review..." vs "Week 2: Remove..." which are intentionally
    different.
    """
    import difflib

    seen_normalized = []  # List of (normalized_title, original_task)
    deduplicated = []
    duplicates_removed = 0

    for task in tasks:
        title = task.get('title', '')
        normalized = normalize_title_for_dedup(title)

        is_duplicate = False
        for seen_norm, seen_task in seen_normalized:
            # Exact match after normalization
            if normalized == seen_norm:
                is_duplicate = True
                print(f"  ⏭️  Internal duplicate: '{title[:50]}...'")
                print(f"       Similar to: '{seen_task.get('title', '')[:50]}...'")
                break

            # Very high fuzzy match threshold to avoid false positives
            # Only catches near-identical tasks (e.g., same task imported multiple times)
            if len(normalized) > 10 and len(seen_norm) > 10:
                ratio = difflib.SequenceMatcher(None, normalized, seen_norm).ratio()
                if ratio >= threshold:
                    is_duplicate = True
                    print(f"  ⏭️  Internal duplicate ({ratio:.0%}): '{title[:50]}...'")
                    print(f"       Similar to: '{seen_task.get('title', '')[:50]}...'")
                    break

        if is_duplicate:
            duplicates_removed += 1
        else:
            seen_normalized.append((normalized, task))
            deduplicated.append(task)

    return deduplicated, duplicates_removed

def parse_completed_tasks_from_markdown(md_file):
    """Parse tasks-completed.md and return list of completed task objects"""
    if not md_file.exists():
        return []

    completed_tasks = []

    with open(md_file, 'r') as f:
        content = f.read()

    # Split by task headers (## Task Title)
    task_sections = re.split(r'\n## ', content)

    for section in task_sections[1:]:  # Skip first split (file header)
        lines = section.split('\n')
        if not lines:
            continue

        # First line is the title
        title = lines[0].strip()

        # Extract metadata and notes
        completed_date = None
        source = None
        notes_lines = []

        # Track when we've passed metadata section
        metadata_section = True

        for line in lines[1:]:
            # Stop at task separator
            if line.strip() == '---':
                break

            # Extract metadata
            if metadata_section:
                if line.startswith('**Completed:**'):
                    # Extract date from "**Completed:** 2025-11-19 14:30"
                    match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                    if match:
                        completed_date = match.group(1)
                    continue
                elif line.startswith('**Source:**'):
                    source = line.replace('**Source:**', '').strip()
                    continue
                elif not line.strip():
                    # Empty line after metadata = start of notes
                    metadata_section = False
                    continue
                elif not line.startswith('**'):
                    # Non-metadata content = notes have started
                    metadata_section = False

            # Collect ALL content after metadata (including blank lines, bullet points, sections)
            if not metadata_section:
                notes_lines.append(line)

        # Create task object matching internal task format
        task = {
            'id': f"completed_{len(completed_tasks)}",
            'title': escape_template_strings(title),
            'status': 'completed',
            'type': 'standalone',
            'completed_at': completed_date or 'Unknown',
            'source': source or 'Manual completion',
            'completion_notes': escape_template_strings('\n'.join(notes_lines).strip())
        }

        completed_tasks.append(task)

    return completed_tasks

def fetch_google_tasks():
    """Fetch all active tasks from Google Tasks and convert to internal format"""
    google_tasks = []

    try:
        # Import Google Tasks API service
        sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')
        from tasks_service import tasks_service

        service = tasks_service()

        # Get all task lists
        task_lists_response = service.tasklists().list().execute()
        task_lists = task_lists_response.get('items', [])

        for task_list in task_lists:
            list_id = task_list['id']
            list_title = task_list['title']

            # Get incomplete tasks only (active tasks)
            tasks_response = service.tasks().list(
                tasklist=list_id,
                showCompleted=False
            ).execute()
            tasks = tasks_response.get('items', [])

            for task in tasks:
                # Convert Google Tasks format to internal task format
                internal_task = {
                    'id': task['id'],
                    'title': escape_template_strings(task.get('title', 'Untitled')),
                    'status': 'active',
                    'client_name': 'google-tasks',
                    'client_display': f'Google Tasks: {list_title}',
                    'type': 'standalone',
                    'source': 'google-tasks',
                    'task_list': list_title,
                    'priority': 'P2'  # Default priority, will be overridden if in title
                }

                # Extract priority from title if present (e.g., "[P0]" or "[P1]")
                title_lower = task.get('title', '').lower()
                if '[p0]' in title_lower:
                    internal_task['priority'] = 'P0'
                elif '[p1]' in title_lower:
                    internal_task['priority'] = 'P1'
                elif '[p3]' in title_lower:
                    internal_task['priority'] = 'P3'

                # Add due date if present
                if 'due' in task:
                    # Google Tasks due format: "2025-11-26T00:00:00.000Z"
                    due_str = task['due'].split('T')[0]  # Extract YYYY-MM-DD
                    internal_task['due_date'] = due_str

                # Add notes if present
                if 'notes' in task and task['notes']:
                    internal_task['notes'] = escape_template_strings(task['notes'])

                google_tasks.append(internal_task)

        print(f"Fetched {len(google_tasks)} active tasks from Google Tasks")

    except Exception as e:
        print(f"⚠️  Could not fetch Google Tasks: {e}")
        print("   Continuing with internal tasks only")

    return google_tasks

# ============================================================================
# PART 1: Generate Standard Overview (by client)
# ============================================================================
print("="*70)
print("GENERATING STANDARD OVERVIEW (by client)")
print("="*70)

clients_dir = Path('/Users/administrator/Documents/PetesBrain.nosync/clients')
client_data = []

for client_dir in sorted(clients_dir.iterdir()):
    if client_dir.is_dir() and not client_dir.name.startswith('_'):
        # Check root location first (primary for all client work)
        task_file = client_dir / 'tasks.json'
        if not task_file.exists():
            # Fallback: check product-feeds (legacy location - should be migrated)
            task_file = client_dir / 'product-feeds' / 'tasks.json'
        completed_md_file = client_dir / 'tasks-completed.md'

        # Skip if client has neither tasks.json nor tasks-completed.md
        if not task_file.exists() and not completed_md_file.exists():
            continue

        # Load active tasks from tasks.json (if exists)
        active_tasks = []
        last_updated = 'Unknown'
        if task_file.exists():
            with open(task_file, 'r') as f:
                data = json.load(f)
            active_tasks = [t for t in data['tasks'] if t.get('status', 'pending') in ['active', 'pending', 'in_progress']]
            last_updated = data.get('last_updated', 'Unknown')

        # Load completed tasks from tasks-completed.md (if exists)
        completed_tasks = parse_completed_tasks_from_markdown(completed_md_file)

        # Add default type if missing and escape template-breaking characters for active tasks only
        # (completed tasks are already escaped by parse_completed_tasks_from_markdown)
        for task in active_tasks:
            if 'type' not in task:
                task['type'] = 'standalone'
            # Escape fields that will be inserted into template strings
            if 'notes' in task and task['notes']:
                task['notes'] = escape_template_strings(task['notes'])
            if 'title' in task:
                task['title'] = escape_template_strings(task['title'])

        # Sort completed tasks by completion date (newest first)
        completed_tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)

        # Separate by type for active tasks
        parent_tasks = [t for t in active_tasks if t.get('type') == 'parent']
        child_tasks = [t for t in active_tasks if t.get('type') == 'child']
        standalone_tasks = [t for t in active_tasks if t.get('type') == 'standalone']

        # Get P0 count
        p0_count = len([t for t in active_tasks if t.get('priority') == 'P0'])

        client_data.append({
            'name': client_dir.name,
            'display': client_dir.name.replace('-', ' ').title(),
            'path': str(client_dir),
            'active_count': len(active_tasks),
            'completed_count': len(completed_tasks),
            'p0_count': p0_count,
            'parent_tasks': parent_tasks,
            'child_tasks': child_tasks,
            'standalone_tasks': standalone_tasks,
            'completed_tasks': completed_tasks,
            'last_updated': last_updated
        })

print(f"Found {len(client_data)} clients")
print(f"Total active: {sum(c['active_count'] for c in client_data)}")
print(f"Total P0: {sum(c['p0_count'] for c in client_data)}")

# Write the standard overview HTML file
output_file = Path('/Users/administrator/Documents/PetesBrain/tasks-overview.html')
template_file = Path('/Users/administrator/Documents/PetesBrain/tasks-overview-template.html')

if template_file.exists():
    with open(template_file, 'r') as f:
        html_template = f.read()

    # Inject client data as JSON
    html_output = html_template.replace(
        'const CLIENT_DATA = [];',
        f'const CLIENT_DATA = {json.dumps(client_data, indent=2, default=str)};'
    )

    with open(output_file, 'w') as f:
        f.write(html_output)

    print("✅ Generated tasks-overview.html")
else:
    print("❌ Error: tasks-overview-template.html not found")

# ============================================================================
# PART 2: Generate Priority Overview (by P0/P1/P2/P3)
# ============================================================================
print("\n" + "="*70)
print("GENERATING PRIORITY OVERVIEW (by P0/P1/P2/P3)")
print("="*70)

# Load all internal tasks for priority view
all_tasks = []

print("Loading internal tasks...")
for client_dir in sorted(clients_dir.iterdir()):
    if client_dir.is_dir() and not client_dir.name.startswith('_'):
        # Check root location first (primary for all client work)
        task_file = client_dir / 'tasks.json'
        if not task_file.exists():
            # Fallback: check product-feeds (legacy location - should be migrated)
            task_file = client_dir / 'product-feeds' / 'tasks.json'
        if task_file.exists():
            with open(task_file, 'r') as f:
                data = json.load(f)

            # Get active tasks and add client context
            for task in data['tasks']:
                if task.get('status', 'pending') in ['active', 'pending', 'in_progress']:
                    task['client_name'] = client_dir.name
                    task['client_display'] = client_dir.name.replace('-', ' ').title()
                    task['source'] = 'internal'  # Mark as internal task
                    # Default type to 'standalone' if missing
                    if 'type' not in task:
                        task['type'] = 'standalone'
                    # Escape fields that will be inserted into template strings
                    if 'notes' in task and task['notes']:
                        task['notes'] = escape_template_strings(task['notes'])
                    if 'title' in task:
                        task['title'] = escape_template_strings(task['title'])
                    all_tasks.append(task)

# Also load roksys tasks
roksys_tasks_file = Path('/Users/administrator/Documents/PetesBrain/roksys/tasks.json')
if roksys_tasks_file.exists():
    with open(roksys_tasks_file, 'r') as f:
        data = json.load(f)
    for task in data.get('tasks', []):
        if task.get('status', 'pending') in ['active', 'pending', 'in_progress']:
            task['client_name'] = 'roksys'
            task['client_display'] = 'Roksys / Personal'
            task['source'] = 'internal'
            if 'type' not in task:
                task['type'] = 'standalone'
            if 'notes' in task and task['notes']:
                task['notes'] = escape_template_strings(task['notes'])
            if 'title' in task:
                task['title'] = escape_template_strings(task['title'])
            all_tasks.append(task)

print(f"Loaded {len(all_tasks)} internal tasks")

# Deduplicate internal tasks first
print("\nDeduplicating internal tasks...")
all_tasks, internal_dups_removed = deduplicate_internal_tasks(all_tasks)
if internal_dups_removed > 0:
    print(f"⚠️  Removed {internal_dups_removed} duplicate internal tasks")
print(f"After deduplication: {len(all_tasks)} internal tasks")

# Build set of internal task titles for Google Tasks deduplication
internal_titles = {task['title'].lower().strip() for task in all_tasks}
print(f"Built index of {len(internal_titles)} internal task titles for Google Tasks deduplication")

# Fetch and merge Google Tasks (with deduplication)
google_tasks = fetch_google_tasks()
duplicates_skipped = 0
for gtask in google_tasks:
    gtask_title = gtask.get('title', '').lower().strip()
    if gtask_title in internal_titles:
        duplicates_skipped += 1
        print(f"  ⏭️  Skipping duplicate: {gtask.get('title', '')[:60]}...")
    else:
        all_tasks.append(gtask)

if duplicates_skipped > 0:
    print(f"⚠️  Skipped {duplicates_skipped} Google Tasks that already exist in internal tasks")

# Group tasks by priority
priority_groups = {
    'P0': [],
    'P1': [],
    'P2': [],
    'P3': []
}

for task in all_tasks:
    priority = task.get('priority', 'P2')
    if priority in priority_groups:
        priority_groups[priority].append(task)
    else:
        # Default to P2 if priority is invalid
        priority_groups['P2'].append(task)

# Sort tasks within each priority: personal tasks first, then by due date
def is_personal_task(task):
    """Check if task is a personal task (should appear first)"""
    # Check client_display
    if task.get('client_display') == 'Roksys / Personal':
        return True
    # Check tags for 'personal'
    tags = task.get('tags', [])
    if 'personal' in tags:
        return True
    # Check title prefix
    if task.get('title', '').startswith('[Personal]'):
        return True
    return False

for priority in priority_groups:
    if priority == 'P0':
        # P0 tasks: Sort strictly by due date (earliest first), then client
        # No special treatment for personal - urgency is what matters
        priority_groups[priority].sort(key=lambda x: (
            x.get('due_date') or '9999-12-31',
            x.get('client_display') or ''
        ))
    else:
        # Other priorities: Personal tasks first, then by due date
        priority_groups[priority].sort(key=lambda x: (
            0 if is_personal_task(x) else 1,  # Personal tasks first
            x.get('due_date') or '9999-12-31',
            x.get('client_display') or ''
        ))

# Separate parent, child, and standalone tasks for each priority
priority_data = {}
for priority, tasks in priority_groups.items():
    parent_tasks = [t for t in tasks if t.get('type') == 'parent']
    child_tasks = [t for t in tasks if t.get('type') == 'child']
    standalone_tasks = [t for t in tasks if t.get('type') == 'standalone']

    # Count only standalone + parent tasks (child tasks are displayed under parents)
    display_count = len(standalone_tasks) + len(parent_tasks)

    priority_data[priority] = {
        'parent_tasks': parent_tasks,
        'child_tasks': child_tasks,
        'standalone_tasks': standalone_tasks,
        'total_count': display_count
    }

# Calculate source breakdown
internal_count = len([t for t in all_tasks if t.get('source') == 'internal'])
google_count = len([t for t in all_tasks if t.get('source') == 'google-tasks'])

print(f"\n{'='*60}")
print(f"Total: {len(all_tasks)} active tasks")
print(f"  Internal tasks: {internal_count}")
print(f"  Google Tasks: {google_count}")
print(f"{'='*60}")
print(f"P0: {priority_data['P0']['total_count']} tasks")
print(f"P1: {priority_data['P1']['total_count']} tasks")
print(f"P2: {priority_data['P2']['total_count']} tasks")
print(f"P3: {priority_data['P3']['total_count']} tasks")
print(f"{'='*60}")

# Write the priority overview HTML file
priority_output_file = Path('/Users/administrator/Documents/PetesBrain/tasks-overview-priority.html')
priority_template_file = Path('/Users/administrator/Documents/PetesBrain/tasks-overview-priority-template.html')

if priority_template_file.exists():
    with open(priority_template_file, 'r') as f:
        html_template = f.read()

    # Inject priority data as JSON
    html_output = html_template.replace(
        'const PRIORITY_DATA = {};',
        f'const PRIORITY_DATA = {json.dumps(priority_data, indent=2, default=str)};'
    )

    with open(priority_output_file, 'w') as f:
        f.write(html_output)

    print("✅ Generated tasks-overview-priority.html")
else:
    print("❌ Error: tasks-overview-priority-template.html not found")

print("\n" + "="*70)
print("✅ BOTH TASK VIEWS GENERATED SUCCESSFULLY")
print("="*70)
