#!/usr/bin/env python3
"""
Generate ALL Task View HTML Files (Consolidated Script)
- Standard view (by client): tasks-overview.html
- Priority view (by P0/P1/P2/P3): tasks-overview-priority.html
- Task Manager & Reminders: tasks-manager.html

This single script generates ALL THREE views to ensure they're always in sync.
"""
import json
import re
import sys
import os
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
import pickle

# Configure logging
LOG_DIR = Path.home() / '.petesbrain-logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'tasks-overview_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler()  # Also output to console for LaunchAgent logs
    ]
)

logger = logging.getLogger(__name__)

# Add project root to path for centralized imports
sys.path.insert(0, str(Path(__file__).parent))

# Import centralized path discovery
try:
    from shared.paths import get_project_root
    PROJECT_ROOT = get_project_root()
except ImportError:
    # Fallback: use PETESBRAIN_ROOT environment variable or relative path
    project_root_env = os.getenv('PETESBRAIN_ROOT')
    if project_root_env:
        PROJECT_ROOT = Path(project_root_env)
    else:
        PROJECT_ROOT = Path(__file__).parent

def escape_template_strings(text):
    """Escape backticks and ${} to prevent breaking JavaScript template strings"""
    if not text:
        return text
    # Replace backticks with single quotes and escape ${ sequences
    # Backticks break JavaScript template strings, so we replace them
    return text.replace('`', "'").replace('${', '\\${}')


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


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

    logger.debug(f"Deduplicating {len(tasks)} internal tasks (threshold: {threshold})")

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
                logger.debug(f"  ⏭️  Internal duplicate: '{title[:50]}...'")
                logger.debug(f"       Similar to: '{seen_task.get('title', '')[:50]}...'")
                break

            # Very high fuzzy match threshold to avoid false positives
            # Only catches near-identical tasks (e.g., same task imported multiple times)
            if len(normalized) > 10 and len(seen_norm) > 10:
                ratio = difflib.SequenceMatcher(None, normalized, seen_norm).ratio()
                if ratio >= threshold:
                    is_duplicate = True
                    logger.debug(f"  ⏭️  Internal duplicate ({ratio:.0%}): '{title[:50]}...'")
                    logger.debug(f"       Similar to: '{seen_task.get('title', '')[:50]}...'")
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
    logger.info("📥 Fetching Google Tasks...")
    google_tasks = []

    try:
        # Import Google Tasks API service
        logger.debug("Importing Google Tasks service...")
        sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')
        from tasks_service import tasks_service

        logger.debug("Building Google Tasks service...")
        service = tasks_service()

        # Get all task lists
        logger.debug("Fetching task lists from Google Tasks API...")
        task_lists_response = service.tasklists().list().execute()
        task_lists = task_lists_response.get('items', [])

        logger.info(f"Found {len(task_lists)} Google Tasks lists")

        for idx, task_list in enumerate(task_lists, 1):
            list_id = task_list['id']
            list_title = task_list['title']

            logger.debug(f"Processing list {idx}/{len(task_lists)}: {list_title}")

            # Get incomplete tasks only (active tasks)
            tasks_response = service.tasks().list(
                tasklist=list_id,
                showCompleted=False
            ).execute()
            tasks = tasks_response.get('items', [])

            logger.debug(f"  Found {len(tasks)} active tasks in {list_title}")

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

        logger.info(f"✅ Fetched {len(google_tasks)} active tasks from Google Tasks")

    except ImportError as e:
        logger.error("=" * 60)
        logger.error("❌ Google Tasks service import failed")
        logger.error(f"Error: {e}")
        logger.error("Action required: Check Google Tasks MCP server installation")
        logger.error("=" * 60)
    except Exception as e:
        logger.warning("=" * 60)
        logger.warning("⚠️  Could not fetch Google Tasks")
        logger.warning(f"Error: {e}")
        logger.warning("Continuing with internal tasks only")
        logger.warning("=" * 60)
        if "credentials" in str(e).lower() or "auth" in str(e).lower():
            logger.error("Possible cause: OAuth token expired")
            logger.error("Action: Run oauth-refresh skill")

    return google_tasks

def get_client_display_name(client_dir):
    """
    Extract the proper client name from CONTEXT.md.
    Falls back to title-cased folder name if CONTEXT.md doesn't exist.

    Args:
        client_dir: Path object for the client directory

    Returns:
        str: Proper client display name (e.g., "Tree2MyDoor", "Smythson")
    """
    context_file = client_dir / 'CONTEXT.md'

    if context_file.exists():
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                # Extract name from heading: "# ClientName - Context & Strategic Notes"
                if first_line.startswith('#'):
                    # Remove leading '#' and extract name before ' - '
                    name_part = first_line.lstrip('#').strip()
                    if ' - ' in name_part:
                        return name_part.split(' - ')[0].strip()
                    return name_part
        except Exception as e:
            logger.debug(f"Could not read client name from {context_file}: {e}")

    # Fallback: title-case the folder name
    return client_dir.name.replace('-', ' ').title()


def fetch_calendar_events():
    """Fetch calendar events for today from Google Calendar"""
    logger.info("📅 Fetching today's calendar events...")
    events = []

    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        # Load OAuth token from shared directory
        token_path = PROJECT_ROOT / 'shared' / 'calendar_token.json'

        if not token_path.exists():
            logger.warning(f"Calendar OAuth token not found at {token_path}")
            return []

        # Load credentials from JSON token file
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
            creds = Credentials.from_authorized_user_info(token_data)

        # Build Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        # Get today's date range (start of day to end of day)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today + timedelta(days=1)

        # Calendar ID for "Peter - Work" calendar
        work_calendar_id = 'c_03826f839a86edf1e8e9ac0f4e0719a1759f8b4589a3da52ea10f2be01b18482@group.calendar.google.com'

        # Fetch events for today from work calendar
        events_result = service.events().list(
            calendarId=work_calendar_id,
            timeMin=today.isoformat() + 'Z',
            timeMax=today_end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        calendar_events = events_result.get('items', [])
        logger.info(f"Found {len(calendar_events)} calendar events for today")

        # Get current time for filtering
        now = datetime.now()

        for event in calendar_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            # Parse time
            if 'T' in start:  # Has time component
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

                # Skip events that have already ended
                if end_dt.replace(tzinfo=None) < now:
                    logger.debug(f"Skipping past event: {event.get('summary')} (ended at {end_dt.strftime('%H:%M')})")
                    continue

                time_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
            else:  # All-day event
                time_str = "All day"

            events.append({
                'title': escape_html(event.get('summary', 'Untitled Event')),
                'time': time_str,
                'start': start,
                'location': escape_html(event.get('location', '')),
                'description': escape_html(event.get('description', ''))
            })

        logger.info(f"Showing {len(events)} upcoming/current events (filtered out past events)")

    except FileNotFoundError:
        logger.warning("Calendar OAuth token file not found")
    except ImportError:
        logger.error("Google Calendar API library not available")
    except Exception as e:
        logger.error(f"Error fetching calendar events: {e}")

    return events

def load_all_tasks():
    """Load all tasks from client task.json files and roksys/tasks.json"""
    tasks_by_client = {}
    all_tasks = []
    all_reminders = []
    seen_task_ids = set()

    clients_dir = PROJECT_ROOT / 'clients'

    # Load client tasks (excluding clients/roksys/)
    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        # SPECIAL CASE: Skip clients/roksys/ folder
        # Roksys uses roksys/tasks.json (root-level), NOT clients/roksys/tasks.json
        # The clients/roksys/ folder exists for company documentation but is not a "client"
        if client_dir.name == 'roksys':
            continue

        # Check root location ONLY (product-feeds is legacy and no longer used)
        task_file = client_dir / 'tasks.json'

        # READ-SIDE GUARD: Refuse to read from product-feeds
        pf_task_file = client_dir / 'product-feeds' / 'tasks.json'
        if pf_task_file.exists():
            print(f"⚠️  WARNING: {client_dir.name} has product-feeds/tasks.json (legacy - ignoring)")
            print(f"   Only reading from: {task_file}")

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

            # Add client context for priority view
            task['client_name'] = client_dir.name
            task['client_display'] = get_client_display_name(client_dir)
            task['source'] = 'internal'

            # Add task ID tracking
            task_id = task.get('id')
            if task_id and task_id not in seen_task_ids:
                seen_task_ids.add(task_id)
                all_tasks.append(task)

                # Create reminder entry if has due_date (for Task Manager view)
                if task.get('due_date'):
                    reminder = {
                        'id': task_id,
                        'title': task['title'],
                        'due_date': task['due_date'],
                        'client': client_dir.name,
                        'task_data': task
                    }
                    all_reminders.append(reminder)

        # Sort completed tasks by completion date (newest first)
        completed_tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)

        # Separate by type for active tasks
        parent_tasks = [t for t in active_tasks if t.get('type') == 'parent']
        child_tasks = [t for t in active_tasks if t.get('type') == 'child']
        standalone_tasks = [t for t in active_tasks if t.get('type') == 'standalone']

        # Get P0 count
        p0_count = len([t for t in active_tasks if t.get('priority') == 'P0'])

        # For client view (tasks-overview.html)
        tasks_by_client[client_dir.name] = {
            'name': client_dir.name,
            'display': get_client_display_name(client_dir),
            'path': str(client_dir),
            'active_count': len(active_tasks),
            'completed_count': len(completed_tasks),
            'p0_count': p0_count,
            'parent_tasks': parent_tasks,
            'child_tasks': child_tasks,
            'standalone_tasks': standalone_tasks,
            'completed_tasks': completed_tasks,
            'last_updated': last_updated,
            'all_active_tasks': active_tasks  # For Task Manager view
        }

    # Load roksys tasks from root-level roksys/ directory (SPECIAL CASE)
    # Note: Roksys is personal/business work and uses roksys/tasks.json
    # NOT clients/roksys/tasks.json (which is forbidden per TASK-SYSTEM-ARCHITECTURE.md)
    # See: docs/TASK-SYSTEM-ARCHITECTURE.md for complete rationale
    roksys_tasks_file = PROJECT_ROOT / 'roksys' / 'tasks.json'
    if roksys_tasks_file.exists():
        roksys_personal_tasks = []
        with open(roksys_tasks_file, 'r') as f:
            data = json.load(f)
        for task in data.get('tasks', []):
            if task.get('status', 'pending') in ['active', 'pending', 'in_progress']:
                # Rename to 'roksys-personal' in UI to distinguish from client work
                task['client_name'] = 'roksys-personal'
                task['client_display'] = 'Roksys (Personal/Business)'
                task['source'] = 'internal'
                if 'type' not in task:
                    task['type'] = 'standalone'
                if 'notes' in task and task['notes']:
                    task['notes'] = escape_template_strings(task['notes'])
                if 'title' in task:
                    task['title'] = escape_template_strings(task['title'])

                task_id = task.get('id')
                if task_id and task_id not in seen_task_ids:
                    seen_task_ids.add(task_id)
                    all_tasks.append(task)
                    roksys_personal_tasks.append(task)

                    # Create reminder entry if has due_date (for Task Manager view)
                    if task.get('due_date'):
                        reminder = {
                            'id': task_id,
                            'title': task['title'],
                            'due_date': task['due_date'],
                            'client': 'roksys-personal',  # Match client_name above
                            'task_data': task
                        }
                        all_reminders.append(reminder)

        # Add roksys-personal to tasks_by_client so it appears in the client list
        if roksys_personal_tasks:
            p0_count = len([t for t in roksys_personal_tasks if t.get('priority') == 'P0'])
            parent_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'parent']
            child_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'child']
            standalone_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'standalone']

            tasks_by_client['roksys-personal'] = {
                'name': 'roksys-personal',
                'display': 'Roksys (Personal/Business)',
                'path': str(PROJECT_ROOT / 'roksys'),
                'active_count': len(roksys_personal_tasks),
                'completed_count': 0,  # Not tracking completed for root roksys
                'p0_count': p0_count,
                'parent_tasks': parent_tasks,
                'child_tasks': child_tasks,
                'standalone_tasks': standalone_tasks,
                'completed_tasks': [],
                'last_updated': datetime.now().isoformat(),
                'all_active_tasks': roksys_personal_tasks
            }

    return tasks_by_client, all_tasks, all_reminders


def parse_due_date(date_str):
    """Parse due date string handling both YYYY-MM-DD and ISO timestamp formats"""
    # Remove timezone suffix if present
    if date_str.endswith('Z'):
        date_str = date_str[:-1]
    # Try parsing with timestamp first, then fall back to date-only
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').date()
    except ValueError:
        return datetime.strptime(date_str, '%Y-%m-%d').date()


def categorize_reminders(all_reminders):
    """Split reminders into today/overdue and upcoming"""
    today = datetime.now().date()

    today_reminders = []
    upcoming_reminders = []

    for reminder in all_reminders:
        try:
            due_date = parse_due_date(reminder['due_date'])
            if due_date <= today:
                today_reminders.append(reminder)
            else:
                upcoming_reminders.append(reminder)
        except ValueError:
            # If all parsing fails, add to upcoming as fallback
            upcoming_reminders.append(reminder)

    # Sort by due_date first (chronological), then by priority (P0, P1, P2, P3)
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}

    def sort_key(reminder):
        priority = reminder.get('task_data', {}).get('priority', 'P2')
        priority_num = priority_order.get(priority, 2)
        return (reminder['due_date'], priority_num)

    today_reminders.sort(key=sort_key)
    upcoming_reminders.sort(key=sort_key)

    return today_reminders, upcoming_reminders


def count_priorities(tasks):
    """Count tasks by priority"""
    counts = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
    for task in tasks:
        priority = task.get('priority', 'P2')
        if priority in counts:
            counts[priority] += 1
    return counts


# ============================================================================
# PRE-FLIGHT: Validate task locations before generating
# ============================================================================
print("="*70)
print("VALIDATING TASK LOCATIONS")
print("="*70)
validation_script = PROJECT_ROOT / 'shared' / 'scripts' / 'validate-task-locations.py'
if validation_script.exists():
    result = subprocess.run([sys.executable, str(validation_script)],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ VALIDATION FAILED - Task location violations detected!")
        print(result.stdout)
        print(result.stderr)
        print("\n⚠️  Cannot generate task overview with violations present.")
        print("   Please fix product-feeds task files before continuing.")
        sys.exit(1)
    else:
        print("✅ Validation passed - proceeding with generation")
else:
    print("⚠️  Validation script not found - skipping validation")

# ============================================================================
# LOAD ALL TASKS (ONCE)
# ============================================================================
print("\n" + "="*70)
print("LOADING ALL TASKS")
print("="*70)

tasks_by_client, all_tasks, all_reminders = load_all_tasks()

print(f"Loaded {len(tasks_by_client)} clients")
print(f"Total active tasks: {len(all_tasks)}")
print(f"Total reminders: {len(all_reminders)}")

# Deduplicate internal tasks
print("\nDeduplicating internal tasks...")
all_tasks, internal_dups_removed = deduplicate_internal_tasks(all_tasks)
if internal_dups_removed > 0:
    print(f"⚠️  Removed {internal_dups_removed} duplicate internal tasks")
print(f"After deduplication: {len(all_tasks)} internal tasks")

# Build set of internal task titles for Google Tasks deduplication
internal_titles = {task['title'].lower().strip() for task in all_tasks}
print(f"Built index of {len(internal_titles)} internal task titles for Google Tasks deduplication")

# Fetch calendar events for today
calendar_events = fetch_calendar_events()

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

# ============================================================================
# PART 1: Generate Standard Overview (by client)
# ============================================================================
print("\n" + "="*70)
print("GENERATING STANDARD OVERVIEW (by client)")
print("="*70)

client_data = list(tasks_by_client.values())

print(f"Total active: {sum(c['active_count'] for c in client_data)}")
print(f"Total P0: {sum(c['p0_count'] for c in client_data)}")

# Write the standard overview HTML file
output_file = PROJECT_ROOT / 'tasks-overview.html'
template_file = PROJECT_ROOT / 'tasks-overview-template.html'

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
priority_output_file = PROJECT_ROOT / 'tasks-overview-priority.html'
priority_template_file = PROJECT_ROOT / 'tasks-overview-priority-template.html'

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

# ============================================================================
# PART 3: Generate Task Manager & Reminders View
# ============================================================================
print("\n" + "="*70)
print("GENERATING TASK MANAGER & REMINDERS VIEW")
print("="*70)

# Categorize reminders for Task Manager view
today_reminders, upcoming_reminders = categorize_reminders(all_reminders)

print(f"Today/Overdue reminders: {len(today_reminders)}")
print(f"Upcoming reminders: {len(upcoming_reminders)}")

# Build client sections HTML
client_sections = ""
for client_name in sorted(tasks_by_client.keys()):
    client_info = tasks_by_client[client_name]
    tasks = client_info['all_active_tasks']
    priorities = count_priorities(tasks)
    total = len(tasks)

    client_sections += f'''        <div class="client-section">
            <div class="client-header" onclick="toggleClient('{client_name}')">
                <div class="client-name">{escape_html(client_info['display'])}</div>
                <div class="client-stats">
                    <span class="client-stat">{total} tasks</span>
                    <span class="client-stat priority-p0">{priorities["P0"]} P0</span>
                    <span class="client-stat priority-p1">{priorities["P1"]} P1</span>
                    <span class="client-stat priority-p2">{priorities["P2"]} P2</span>
                    <span class="client-stat priority-p3">{priorities["P3"]} P3</span>
                </div>
            </div>
            <div class="client-content" id="client-{client_name}">
'''

    # Sort tasks by priority first, then by due_date
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
    tasks_sorted = sorted(tasks, key=lambda t: (
        priority_order.get(t.get('priority', 'P2'), 2),
        t.get('due_date') or '9999-12-31'
    ))

    # Add tasks for this client
    for task in tasks_sorted:
        priority = task.get('priority', 'P2')
        due_date = task.get('due_date') or 'No due date'
        title = escape_html(task.get('title', 'Untitled'))
        task_id = task.get('id')

        client_sections += f'''                <div class="task priority-{priority}" onclick="openTaskModal('{task_id}')">
                    <div class="task-content">
                        <div class="task-title">{title}</div>
                        <div class="task-meta">
                            <span class="task-priority">{priority}</span>
                            <span class="task-due">{due_date}</span>
                        </div>
                    </div>
                    <button class="task-quick-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓ Complete</button>
                </div>
'''

    client_sections += '''            </div>
        </div>
'''

# Build today reminders HTML
today_html = ""
if today_reminders:
    for reminder in today_reminders:
        title = escape_html(reminder['title'])
        due_date = reminder['due_date']
        client = escape_html(reminder['client'])
        task_id = reminder['id']
        status = "OVERDUE" if parse_due_date(due_date) < datetime.now().date() else "DUE TODAY"

        today_html += f'''            <div class="reminder-item reminder-{status.lower().replace(' ', '-')}" onclick="jumpToTask('{task_id}', '{escape_html(reminder['client'])}')">
                <div class="reminder-status">{status}</div>
                <div class="reminder-title">{title}</div>
                <div class="reminder-meta">{due_date} • {client}</div>
            </div>
'''
else:
    today_html = '            <div class="no-reminders">No overdue or due today</div>\n'

# Separate personal reminders from client work tasks
personal_reminders = []
client_tasks = []
today = datetime.now().date()

all_reminders_sorted = today_reminders + upcoming_reminders

for reminder in all_reminders_sorted:
    title = reminder['title']
    # Personal reminders: tasks from 'personal' OR 'roksys-personal' that DON'T start with [Roksys] or [System]
    is_personal = (
        (reminder.get('client') == 'personal' or reminder.get('client') == 'roksys-personal') and
        not title.startswith('[Roksys]') and
        not title.startswith('[System]') and
        not title.startswith('[roksys]')
    )

    if is_personal:
        personal_reminders.append(reminder)
    else:
        client_tasks.append(reminder)

# Build calendar events HTML
calendar_events_html = ""
if calendar_events:
    for event in calendar_events:
        title = event['title']
        time = event['time']
        location = event.get('location', '')

        location_html = f'<div class="event-location">📍 {location}</div>' if location else ''

        calendar_events_html += f'''            <div class="calendar-event">
                <div class="event-time">{time}</div>
                <div class="event-details">
                    <div class="event-title">{title}</div>
                    {location_html}
                </div>
            </div>
'''
else:
    calendar_events_html = '            <div class="no-events">No events today</div>\n'

# Build personal reminders HTML
personal_reminders_html = ""
if personal_reminders:
    for reminder in personal_reminders:
        title = escape_html(reminder['title'])
        due_date = reminder['due_date']
        task_id = reminder['id']
        client = reminder.get('client', 'personal')  # Get actual client name

        # Determine status
        try:
            parsed_date = parse_due_date(due_date)
            if parsed_date < today:
                status_class = "overdue"
                status_label = "OVERDUE"
            elif parsed_date == today:
                status_class = "due-today"
                status_label = "TODAY"
            else:
                status_class = "upcoming"
                status_label = ""
        except ValueError:
            status_class = "upcoming"
            status_label = ""

        status_html = f'<div class="reminder-status">{status_label}</div>' if status_label else ''

        personal_reminders_html += f'''            <div class="reminder-item reminder-{status_class}">
                <div class="reminder-content" onclick="jumpToTask('{task_id}', '{client}')">
                    {status_html}
                    <div class="reminder-title">{title}</div>
                    <div class="reminder-meta">{due_date}</div>
                </div>
                <button class="reminder-quick-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓ Complete</button>
            </div>
'''
else:
    personal_reminders_html = '            <div class="no-reminders">No personal reminders</div>\n'

# Build client tasks HTML (all work tasks in chronological order)
client_tasks_html = ""
if client_tasks:
    for reminder in client_tasks:
        title = escape_html(reminder['title'])
        due_date = reminder['due_date']
        client_slug = reminder['client']
        client_display = tasks_by_client.get(client_slug, {}).get('display', client_slug)
        task_id = reminder['id']
        priority = reminder.get('task_data', {}).get('priority', 'P2')

        # Determine status class
        try:
            parsed_date = parse_due_date(due_date)
            if parsed_date < today:
                status_class = "overdue"
                status_label = "OVERDUE"
            elif parsed_date == today:
                status_class = "due-today"
                status_label = "TODAY"
            else:
                status_class = "upcoming"
                status_label = ""
        except ValueError:
            status_class = "upcoming"
            status_label = ""

        status_html = f'<div class="task-status-label">{status_label}</div>' if status_label else ''

        client_tasks_html += f'''            <div class="task-date-item task-{status_class}">
                <div class="task-date-content" onclick="jumpToTask('{task_id}', '{escape_html(client_slug)}')">
                    {status_html}
                    <div class="task-date-title">{title}</div>
                    <div class="task-date-meta">
                        <span class="task-priority-badge priority-{priority}">{priority}</span>
                        <span class="task-due-date">{due_date}</span>
                        <span class="task-client-name">{escape_html(client_display)}</span>
                    </div>
                </div>
                <button class="task-date-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓</button>
            </div>
'''
else:
    client_tasks_html = '            <div class="no-reminders">No client tasks with due dates</div>\n'

# Build task data JSON for modal - all tasks by ID
all_tasks_by_id = {}
for client_info in tasks_by_client.values():
    for task in client_info['all_active_tasks']:
        all_tasks_by_id[task['id']] = task

task_data = json.dumps(all_tasks_by_id, indent=2, default=str)

# Build reminder data JSON for reference
reminder_data = json.dumps(
    {r['id']: r for r in today_reminders + upcoming_reminders},
    indent=2,
    default=str
)

# Generate Task Manager HTML (inline, as in generate-task-manager.py)
task_manager_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PetesBrain - Task Manager & Reminders</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%234a7c3a'/><text x='50' y='70' font-size='60' text-anchor='middle' fill='white' font-family='Arial, sans-serif' font-weight='bold'>T</text></svg>">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: Verdana, Geneva, sans-serif;
            font-size: 13px;
            line-height: 1.5;
            background-color: #f5f5f5;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }}
        h1 {{ color: #333; margin: 0; font-size: 32px; }}
        .nav-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .nav-link, .action-btn {{
            padding: 10px 20px;
            background: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 13px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .nav-link:hover, .action-btn:hover {{
            background: #5a6268;
        }}
        .action-btn {{
            background: #17a2b8;
        }}
        .action-btn:hover {{
            background: #138496;
        }}
        .nav-separator {{
            margin: 0 10px;
            color: #6c757d;
        }}
        .content-wrapper {{
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
        }}
        .clients-column {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .client-section {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            background: white;
        }}
        .client-header {{
            background: #e8e8e8;
            color: #333;
            padding: 10px 12px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }}
        .client-header:hover {{
            background: #ddd;
        }}
        .client-name {{
            font-size: 14px;
            font-weight: bold;
        }}
        .client-stats {{
            display: flex;
            gap: 5px;
            font-size: 10px;
        }}
        .client-stat {{
            background: rgba(0,0,0,0.1);
            padding: 3px 6px;
            border-radius: 3px;
            color: #333;
        }}
        .client-stat.priority-p0 {{
            background: #dc3545;
            color: white;
        }}
        .client-stat.priority-p1 {{
            background: #ffc107;
            color: #333;
        }}
        .client-stat.priority-p2 {{
            background: #28a745;
            color: white;
        }}
        .client-stat.priority-p3 {{
            background: #6c757d;
            color: white;
        }}
        .client-content {{
            padding: 15px;
            background: #fafafa;
            display: none;
            max-height: 500px;
            overflow-y: auto;
        }}
        .client-content.expanded {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .task {{
            background: white;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .task:hover {{
            border-color: #999;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        .task-content {{
            flex: 1;
        }}
        .task-quick-complete {{
            background: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s;
            opacity: 0;
            margin-left: 10px;
        }}
        .task:hover .task-quick-complete {{
            opacity: 1;
        }}
        .task-quick-complete:hover {{
            background: #218838;
        }}
        .task.priority-P0 {{
            border-left-color: #dc3545;
        }}
        .task.priority-P1 {{
            border-left-color: #ffc107;
        }}
        .task.priority-P2 {{
            border-left-color: #28a745;
        }}
        .task.priority-P3 {{
            border-left-color: #6c757d;
        }}
        .task-title {{
            font-weight: 600;
            color: #333;
            font-size: 13px;
            margin-bottom: 4px;
        }}
        .task-meta {{
            font-size: 11px;
            color: #666;
            display: flex;
            gap: 8px;
        }}
        .task-priority {{
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 2px;
            font-weight: 600;
        }}
        .reminders-column {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .reminders-title {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #6c757d;
        }}
        .reminders-section {{
            margin-bottom: 15px;
        }}
        .reminders-section-title {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 8px;
        }}
        .reminder-item {{
            background: white;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 4px solid #e0e0e0;
            font-size: 12px;
            transition: all 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .reminder-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transform: translateX(2px);
            background: #f9f9f9;
        }}
        .reminder-content {{
            flex: 1;
            cursor: pointer;
        }}
        .reminder-quick-complete {{
            background: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s;
            opacity: 0;
            margin-left: 10px;
        }}
        .reminder-item:hover .reminder-quick-complete {{
            opacity: 1;
        }}
        .reminder-quick-complete:hover {{
            background: #218838;
        }}
        .reminder-overdue {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        .reminder-overdue:hover {{
            border-left-color: #c82333;
            background: #ffe5e5;
        }}
        .reminder-due-today {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        .reminder-due-today:hover {{
            border-left-color: #e0a800;
            background: #fff9e6;
        }}
        .reminder-upcoming {{
            border-left-color: #6c757d;
        }}
        .reminder-upcoming:hover {{
            border-left-color: #5a6268;
            background: #f5f5f5;
        }}
        .reminder-status {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 3px;
        }}
        .reminder-title {{
            font-weight: 600;
            color: #333;
            margin-bottom: 3px;
        }}
        .reminder-meta {{
            font-size: 11px;
            color: #666;
        }}
        .no-reminders {{
            color: #999;
            font-style: italic;
            text-align: center;
            padding: 10px;
        }}
        .reminders-box {{
            background: #fafafa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .reminders-list {{
            max-height: 300px;
            overflow-y: auto;
        }}
        .calendar-box {{
            background: #f0f8ff;
            border: 2px solid #4a7c3a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .calendar-list {{
            max-height: 300px;
            overflow-y: auto;
        }}
        .calendar-event {{
            background: white;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid #4a7c3a;
            display: flex;
            gap: 12px;
            transition: all 0.2s;
        }}
        .calendar-event:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transform: translateX(2px);
        }}
        .event-time {{
            font-weight: 700;
            color: #4a7c3a;
            font-size: 12px;
            min-width: 90px;
            padding-top: 2px;
        }}
        .event-details {{
            flex: 1;
        }}
        .event-title {{
            font-weight: 600;
            color: #333;
            font-size: 13px;
            margin-bottom: 4px;
        }}
        .event-location {{
            font-size: 11px;
            color: #666;
            margin-top: 4px;
        }}
        .no-events {{
            color: #999;
            font-style: italic;
            text-align: center;
            padding: 10px;
        }}
        .all-tasks-box {{
            background: #fafafa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
        }}
        .all-tasks-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        .task-date-item {{
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 4px solid #e0e0e0;
            font-size: 12px;
            transition: all 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .task-date-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transform: translateX(2px);
            background: #f9f9f9;
        }}
        .task-date-content {{
            flex: 1;
            cursor: pointer;
        }}
        .task-date-complete {{
            background: #28a745;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
            opacity: 0;
            margin-left: 10px;
        }}
        .task-date-item:hover .task-date-complete {{
            opacity: 1;
        }}
        .task-date-complete:hover {{
            background: #218838;
        }}
        .task-overdue {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        .task-due-today {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        .task-upcoming {{
            border-left-color: #28a745;
        }}
        .task-status-label {{
            font-size: 9px;
            font-weight: 700;
            color: #dc3545;
            margin-bottom: 4px;
            text-transform: uppercase;
        }}
        .task-date-title {{
            font-weight: 500;
            color: #333;
            margin-bottom: 6px;
        }}
        .task-date-meta {{
            display: flex;
            gap: 10px;
            font-size: 11px;
            color: #666;
            flex-wrap: wrap;
        }}
        .task-priority-badge {{
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 600;
            font-size: 10px;
        }}
        .priority-P0 {{
            background: #fff5f5;
            color: #333;
        }}
        .priority-P1 {{
            background: #fffbf0;
            color: #333;
        }}
        .priority-P2 {{
            background: #f0f9fa;
            color: #333;
        }}
        .priority-P3 {{
            background: #f5f5f5;
            color: #333;
        }}
        .task-due-date {{
            color: #666;
        }}
        .task-client-name {{
            color: #888;
        }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }}
        .modal.open {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .modal-content {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .modal-header {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }}
        .modal-body {{
            margin-bottom: 20px;
        }}
        .task-detail {{
            margin-bottom: 15px;
        }}
        .task-detail-label {{
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .task-detail-value {{
            color: #333;
            padding: 8px 12px;
            background: #f5f5f5;
            border-radius: 4px;
        }}
        .note-section {{
            margin: 20px 0;
        }}
        .note-label {{
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            display: block;
        }}
        .note-textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 4px;
            font-family: Arial, sans-serif;
            font-size: 13px;
            min-height: 120px;
            resize: vertical;
            box-sizing: border-box;
        }}
        .note-textarea:focus {{
            outline: none;
            border-color: #6c757d;
            box-shadow: 0 0 0 3px rgba(108,117,125,0.1);
        }}
        .modal-buttons {{
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            padding-top: 15px;
            border-top: 2px solid #e0e0e0;
        }}
        .modal-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .modal-btn-cancel {{
            background: #e0e0e0;
            color: #333;
        }}
        .modal-btn-cancel:hover {{
            background: #d0d0d0;
        }}
        .modal-btn-save {{
            background: #6c757d;
            color: white;
        }}
        .modal-btn-save:hover {{
            background: #5a6268;
        }}
        .modal-btn-complete {{
            background: #28a745;
            color: white;
        }}
        .modal-btn-complete:hover {{
            background: #218838;
        }}
        @media (max-width: 1200px) {{
            .content-wrapper {{
                grid-template-columns: 1fr;
            }}
            .reminders-column {{
                position: relative;
                top: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>PetesBrain - Task Manager & Reminders</h1>
        </div>

        <div class="nav-buttons">
            <a href="tasks-overview-priority.html" class="nav-link">📊 By Priority</a>
            <a href="tasks-overview.html" class="nav-link">👥 By Client</a>
            <span class="nav-separator">|</span>
            <button class="action-btn" onclick="toggleAllClients()">Expand All Clients</button>
            <button class="action-btn" onclick="refreshTaskManager()" style="background: #17a2b8;">🔄 Refresh</button>
            <button class="action-btn" onclick="processAllNotes()" style="background: #28a745; display: none;" id="process-notes-btn">📋 Process Notes</button>
        </div>

        <div class="content-wrapper">
            <div class="clients-column">
{client_sections}
            </div>

            <div class="reminders-column">
                <div class="calendar-box">
                    <div class="reminders-title">📅 Today's Calendar</div>
                    <div class="calendar-list">
{calendar_events_html}
                    </div>
                </div>

                <div class="reminders-box">
                    <div class="reminders-title">📌 Personal Reminders</div>
                    <div class="reminders-list">
{personal_reminders_html}
                    </div>
                </div>

                <div class="all-tasks-box">
                    <div class="reminders-title">📋 Client Tasks (by due date)</div>
                    <div class="all-tasks-list">
{client_tasks_html}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Task Detail Modal -->
    <div id="taskModal" class="modal">
        <div class="modal-content">
            <div class="modal-header" id="modalTitle">Task Details</div>
            <div class="modal-body" id="modalBody">
            </div>
            <div class="note-section">
                <label class="note-label">Add a Note:</label>
                <textarea class="note-textarea" id="noteText" placeholder="Type your note here..."></textarea>
            </div>
            <div class="modal-buttons">
                <button class="modal-btn modal-btn-cancel" onclick="closeTaskModal()">Cancel</button>
                <button class="modal-btn modal-btn-complete" onclick="completeTask()">✓ Complete</button>
                <button class="modal-btn modal-btn-save" onclick="saveNote()">Save to Manual Tasks</button>
            </div>
        </div>
    </div>

    <!-- Process Notes Modal -->
    <div id="processNotesModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">Process All Task Notes</div>
            <div class="modal-body">
                <p>You have <strong><span id="notes-count">0</span> task note(s)</strong> ready to process.</p>
                <p style="margin-top: 15px;">The following command has been copied to your clipboard:</p>
                <div style="margin-top: 15px; padding: 15px; background: #f5f5f5; border-radius: 4px; font-family: monospace; font-size: 14px;">
                    Process my task notes
                </div>
                <p style="margin-top: 15px; font-size: 13px; color: #666;">
                    Just paste (Cmd+V) into Claude Code to begin processing.
                </p>
            </div>
            <div class="modal-buttons">
                <button class="modal-btn modal-btn-cancel" onclick="closeProcessModal()">Close</button>
            </div>
        </div>
    </div>

    <script>
const TASK_DATA = {task_data};
const REMINDER_DATA = {reminder_data};

function toggleClient(clientName) {{
    const elementId = 'client-' + clientName;
    const content = document.getElementById(elementId);
    if (content) {{
        content.classList.toggle('expanded');
    }}
}}

function toggleAllClients() {{
    const contents = document.querySelectorAll('.client-content');
    const allExpanded = Array.from(contents).every(c => c.classList.contains('expanded'));

    contents.forEach(content => {{
        if (allExpanded) {{
            content.classList.remove('expanded');
        }} else {{
            content.classList.add('expanded');
        }}
    }});
}}

function processAllNotes() {{
    // This would trigger the process-task-notes skill
    console.log('Process notes functionality would be implemented here');
}}

function jumpToTask(taskId, clientName) {{
    // Expand the client section if collapsed
    const clientContent = document.getElementById('client-' + clientName);
    if (clientContent && !clientContent.classList.contains('expanded')) {{
        clientContent.classList.add('expanded');
    }}

    // Wait for expansion animation, then find and highlight the task
    setTimeout(() => {{
        // Find the specific task element
        const taskElement = document.querySelector(`[onclick*="openTaskModal('${{taskId}}')"]`);

        if (taskElement) {{
            // Scroll to the task
            taskElement.scrollIntoView({{ behavior: 'smooth', block: 'center' }});

            // Highlight the task temporarily
            taskElement.style.backgroundColor = '#fff3cd';
            taskElement.style.transition = 'background-color 0.3s ease';

            // Remove highlight after 2 seconds
            setTimeout(() => {{
                taskElement.style.backgroundColor = '';
            }}, 2000);
        }}
    }}, 100);
}}

function openTaskModal(taskId) {{
    const task = TASK_DATA[taskId];
    if (!task) {{
        console.error('Task not found:', taskId);
        return;
    }}

    // Populate modal header
    document.getElementById('modalTitle').textContent = task.title || 'Task Details';

    // Populate modal body with task details
    const modalBody = document.getElementById('modalBody');
    const statusBadge = task.status ? task.status.charAt(0).toUpperCase() + task.status.slice(1) : 'Unknown';

    const priorityBadge = task.priority || 'P2';
    const priorityColor = {{
        'P0': '#dc3545',
        'P1': '#ffc107',
        'P2': '#28a745',
        'P3': '#6c757d'
    }}[priorityBadge] || '#999';

    const priorityTextColor = priorityBadge === 'P1' ? '#333' : 'white';

    let html = '<div style="display: grid; grid-template-columns: auto 1fr auto 1fr auto 1fr; gap: 20px; margin-bottom: 20px; align-items: center;">';
    html += '<div class="task-detail-label">Priority</div>';
    html += '<div><span style="background: ' + priorityColor + '; color: ' + priorityTextColor + '; padding: 4px 8px; border-radius: 3px; font-weight: 600;">' + priorityBadge + '</span></div>';
    html += '<div class="task-detail-label">Status</div>';
    html += '<div>' + statusBadge + '</div>';
    html += '<div class="task-detail-label">Due Date</div>';
    html += '<div>' + (task.due_date || 'No due date') + '</div>';
    html += '</div>';

    if (task.notes) {{
        html += '<div style="margin-top: 20px; padding: 12px; background: #f5f5f5; border-radius: 4px; border-left: 4px solid #999;">';
        html += '<div class="task-detail-label" style="margin-bottom: 8px;">Current Notes</div>';
        html += '<div style="color: #333; white-space: pre-wrap; word-wrap: break-word;">' + task.notes.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</div>';
        html += '</div>';
    }}
    modalBody.innerHTML = html;

    // Clear note textarea
    document.getElementById('noteText').value = '';

    // Store current task ID for saving
    window.currentTaskId = taskId;
    window.currentTask = task;

    // Open modal
    const modal = document.getElementById('taskModal');
    modal.classList.add('open');
}}

function closeTaskModal() {{
    const modal = document.getElementById('taskModal');
    modal.classList.remove('open');
    window.currentTaskId = null;
    window.currentTask = null;
}}

function saveNote() {{
    const noteText = document.getElementById('noteText').value.trim();
    if (!noteText) {{
        alert('Please enter a note before saving.');
        return;
    }}

    const task = window.currentTask;
    if (!task) {{
        alert('Error: Task not found');
        return;
    }}

    // Create manual task note object
    const manualNote = {{
        task_id: task.id,
        task_title: task.title,
        client: task.client || task.client_name || 'unknown',
        priority: task.priority || 'P2',
        due_date: task.due_date,
        note_text: noteText
    }};

    // Send to backend API
    fetch('http://localhost:5002/save-note', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify(manualNote)
    }})
    .then(response => response.json())
    .then(data => {{
        if (data.status === 'success') {{
            closeTaskModal();
            checkForNotes();
            // Note saved silently - no popup needed
        }} else {{
            alert('Error saving note: ' + data.message);
        }}
    }})
    .catch(error => {{
        console.error('Error:', error);
        alert('Error saving note: Could not connect to backend server.\\n\\nMake sure task-notes-api.py is running on port 5002.\\n\\nError: ' + error.message);
    }});
}}

function completeTask() {{
    const task = window.currentTask;
    if (!task) {{
        alert('Error: Task not found');
        return;
    }}

    // Create manual task note object with "Done" as the note
    const manualNote = {{
        task_id: task.id,
        task_title: task.title,
        client: task.client || task.client_name || 'unknown',
        priority: task.priority || 'P2',
        due_date: task.due_date,
        note_text: 'Done'
    }};

    // Send to backend API
    fetch('http://localhost:5002/save-note', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify(manualNote)
    }})
    .then(response => response.json())
    .then(data => {{
        if (data.status === 'success') {{
            closeTaskModal();
            checkForNotes();
            // Task marked complete silently - no popup needed
        }} else {{
            alert('Error completing task: ' + data.message);
        }}
    }})
    .catch(error => {{
        console.error('Error:', error);
        alert('Error completing task: Could not connect to backend server.\\n\\nMake sure task-notes-api.py is running on port 5002.\\n\\nError: ' + error.message);
    }});
}}

function quickCompleteTask(event, taskId) {{
    // Find the task in our data
    const task = TASK_DATA[taskId];

    if (!task) {{
        alert('Error: Task not found');
        return;
    }}

    // Create manual task note object with "Done" as the note
    const manualNote = {{
        task_id: task.id,
        task_title: task.title,
        client: task.client || task.client_name || 'unknown',
        priority: task.priority || 'P2',
        due_date: task.due_date,
        note_text: 'Done'
    }};

    // Send to backend API
    fetch('http://localhost:5002/save-note', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify(manualNote)
    }})
    .then(response => response.json())
    .then(data => {{
        if (data.status === 'success') {{
            // Update the note count
            checkForNotes();
            // Show visual feedback - fade out the task
            const taskElement = event.target.closest('.task');
            if (taskElement) {{
                taskElement.style.opacity = '0.5';
                taskElement.style.backgroundColor = '#e8f5e9';
            }}
            // Task marked complete silently - no popup needed
        }} else {{
            alert('Error completing task: ' + data.message);
        }}
    }})
    .catch(error => {{
        console.error('Error:', error);
        alert('Error completing task: Could not connect to backend server.\\n\\nMake sure task-notes-api.py is running on port 5002.\\n\\nError: ' + error.message);
    }});
}}

// Close modal when clicking outside of it
window.onclick = function(event) {{
    const modal = document.getElementById('taskModal');
    if (event.target === modal) {{
        closeTaskModal();
    }}
}}

// Refresh Task Manager Function
async function refreshTaskManager() {{
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '⏳ Refreshing...';
    btn.disabled = true;

    try {{
        const response = await fetch('http://localhost:5002/regenerate', {{
            method: 'POST'
        }});
        const data = await response.json();

        if (data.success && data.status === 'success') {{
            // Wait a moment then reload the page
            setTimeout(() => {{
                location.reload();
            }}, 500);
        }} else {{
            alert('Error refreshing task manager: ' + (data.message || data.error || 'Unknown error'));
            btn.textContent = originalText;
            btn.disabled = false;
        }}
    }} catch (error) {{
        alert('Could not connect to refresh API.\\n\\nError: ' + error.message);
        btn.textContent = originalText;
        btn.disabled = false;
    }}
}}

// Process Notes Modal Functions
async function checkForNotes() {{
    try {{
        const response = await fetch('http://localhost:5002/notes-count');
        const data = await response.json();
        const processBtn = document.getElementById('process-notes-btn');

        if (data.count > 0) {{
            processBtn.style.display = 'inline-block';
            processBtn.textContent = `📋 Process ${{data.count}} Note${{data.count > 1 ? 's' : ''}}`;
        }} else {{
            processBtn.style.display = 'none';
        }}
    }} catch (error) {{
        console.log('Could not check notes:', error);
        document.getElementById('process-notes-btn').style.display = 'none';
    }}
}}

async function processAllNotes() {{
    try {{
        const response = await fetch('http://localhost:5002/notes-count');
        const data = await response.json();

        document.getElementById('notes-count').textContent = data.count;

        // Copy to clipboard
        const message = 'Process my task notes';
        navigator.clipboard.writeText(message).then(() => {{
            // Show modal
            document.getElementById('processNotesModal').classList.add('open');
        }}).catch((error) => {{
            alert('❌ Could not copy to clipboard.\\n\\nManually copy: "Process my task notes"');
        }});
    }} catch (error) {{
        alert('Error loading notes: ' + error.message);
    }}
}}

function closeProcessModal() {{
    document.getElementById('processNotesModal').classList.remove('open');
}}

// Check for notes on page load
window.addEventListener('DOMContentLoaded', checkForNotes);
    </script>
</body>
</html>
'''

# Write Task Manager HTML
task_manager_output = PROJECT_ROOT / 'tasks-manager.html'
with open(task_manager_output, 'w') as f:
    f.write(task_manager_html)

print(f"✅ Generated tasks-manager.html")
print(f"   Total clients: {len(tasks_by_client)}")
print(f"   Total reminders: {len(all_reminders)}")
print(f"   - Today/Overdue: {len(today_reminders)}")
print(f"   - Upcoming: {len(upcoming_reminders)}")

# Start task notes API server if not already running
def is_server_running():
    """Check if task-notes-api.py is already running on port 5002"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5002))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_task_notes_server():
    """Start the task notes API server in the background"""
    api_script = PROJECT_ROOT / 'shared' / 'scripts' / 'task-notes-api.py'
    if not api_script.exists():
        print(f"⚠️  Warning: Task notes API script not found at {api_script}")
        return False

    try:
        # Start the server in the background
        subprocess.Popen(
            [sys.executable, str(api_script)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # Detach from parent process
        )
        print("✅ Started task-notes-api.py server on port 5002")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not start task notes server: {e}")
        return False

# Check and start server if needed
if not is_server_running():
    start_task_notes_server()
else:
    print("✅ Task notes API server already running on port 5002")

print("\n" + "="*70)
print("✅ ALL THREE TASK VIEWS GENERATED SUCCESSFULLY")
print("="*70)
print(f"Generated: tasks-overview.html (by client)")
print(f"Generated: tasks-overview-priority.html (by priority)")
print(f"Generated: tasks-manager.html (Task Manager & Reminders)")
print("="*70)
