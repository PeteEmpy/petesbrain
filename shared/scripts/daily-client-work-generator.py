#!/usr/bin/env python3
"""
Daily Client Work Generator

Analyzes all active clients and generates a daily work list based on:
1. Client CONTEXT.md (current status, priorities, issues)
2. Recent meeting notes (action items, deadlines)
3. Recent client activity (emails, performance changes)
4. Scheduled audits and reporting deadlines
5. Product feed changes and alerts

This ensures every client gets appropriate attention daily, not just those with
explicit tasks or meetings.
"""

import os
import sys
import json
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import anthropic

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
CACHE_FILE = PROJECT_ROOT / "data/cache/client-analysis-cache.json"
CACHE_MAX_AGE_HOURS = 24  # Force refresh after this many hours
CLIENTS_DIR = PROJECT_ROOT / "clients"

# Add MCP server path for Google Tasks integration
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
SCRIPTS_PATH = PROJECT_ROOT / "shared" / "scripts"
sys.path.insert(0, str(MCP_SERVER_PATH))
sys.path.insert(0, str(SCRIPTS_PATH))

def load_analysis_cache():
    """Load the client analysis cache from disk"""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"   ⚠️  Error loading cache: {e}")
        return {}

def save_analysis_cache(cache):
    """Save the client analysis cache to disk"""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2, default=str)
    except Exception as e:
        print(f"   ⚠️  Error saving cache: {e}")

def hash_content(content):
    """Generate a hash for content to detect changes"""
    if content is None:
        return None
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]

def get_latest_file_mtime(directory, pattern="*.md"):
    """Get the most recent modification time of files in a directory"""
    if not directory.exists():
        return None

    latest = None
    for f in directory.glob(pattern):
        try:
            mtime = f.stat().st_mtime
            if latest is None or mtime > latest:
                latest = mtime
        except:
            continue

    return datetime.fromtimestamp(latest).isoformat() if latest else None

def get_cache_triggers(client_path, context, alerts, audits):
    """Generate cache invalidation triggers for a client"""
    triggers = {
        'context_hash': hash_content(context),
        'context_mtime': None,
        'latest_meeting_mtime': get_latest_file_mtime(client_path / "meeting-notes"),
        'latest_email_mtime': get_latest_file_mtime(client_path / "emails"),
        'alerts_hash': hash_content(json.dumps(alerts, sort_keys=True)) if alerts else None,
        'audits_hash': hash_content(json.dumps(audits, sort_keys=True)) if audits else None,
    }

    # Get CONTEXT.md mtime
    context_file = client_path / "CONTEXT.md"
    if context_file.exists():
        try:
            triggers['context_mtime'] = datetime.fromtimestamp(
                context_file.stat().st_mtime
            ).isoformat()
        except:
            pass

    return triggers

def is_cache_valid(client_name, cache, current_triggers):
    """Check if cached analysis is still valid for this client"""
    if client_name not in cache:
        return False, "No cache entry"

    entry = cache[client_name]
    cached_triggers = entry.get('triggers', {})
    cached_at = entry.get('cached_at')

    # Check cache age
    if cached_at:
        try:
            cached_time = datetime.fromisoformat(cached_at)
            age_hours = (datetime.now() - cached_time).total_seconds() / 3600
            if age_hours > CACHE_MAX_AGE_HOURS:
                return False, f"Cache expired ({age_hours:.1f}h old)"
        except:
            return False, "Invalid cache timestamp"
    else:
        return False, "No cache timestamp"

    # Check CONTEXT.md changed
    if current_triggers.get('context_hash') != cached_triggers.get('context_hash'):
        return False, "CONTEXT.md content changed"

    if current_triggers.get('context_mtime') != cached_triggers.get('context_mtime'):
        return False, "CONTEXT.md modified"

    # Check for new meetings
    cached_meeting = cached_triggers.get('latest_meeting_mtime')
    current_meeting = current_triggers.get('latest_meeting_mtime')
    if current_meeting and (not cached_meeting or current_meeting > cached_meeting):
        return False, "New meeting notes"

    # Check for new emails
    cached_email = cached_triggers.get('latest_email_mtime')
    current_email = current_triggers.get('latest_email_mtime')
    if current_email and (not cached_email or current_email > cached_email):
        return False, "New emails"

    # Check alerts changed
    if current_triggers.get('alerts_hash') != cached_triggers.get('alerts_hash'):
        return False, "Alerts changed"

    # Check audits changed
    if current_triggers.get('audits_hash') != cached_triggers.get('audits_hash'):
        return False, "Audits changed"

    return True, "Cache valid"


def get_active_clients():
    """Get list of active clients (exclude templates and special folders)"""
    clients = []

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir():
            continue
        if client_dir.name.startswith('_'):
            continue
        if client_dir.name in ['README.md']:
            continue

        clients.append({
            'name': client_dir.name,
            'path': client_dir
        })

    return clients

def read_context_file(client_path):
    """Read and parse client CONTEXT.md file"""
    context_file = client_path / "CONTEXT.md"

    if not context_file.exists():
        return None

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"   ⚠️  Error reading context: {e}")
        return None

def get_recent_meetings(client_path, days=7):
    """Get recent meeting notes for client"""
    meetings_dir = client_path / "meeting-notes"

    if not meetings_dir.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    recent_meetings = []

    for meeting_file in meetings_dir.glob("*.md"):
        try:
            mtime = datetime.fromtimestamp(meeting_file.stat().st_mtime)
            if mtime >= cutoff:
                with open(meeting_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if tasks already generated (frontmatter flag)
                if 'tasks_generated: true' in content or 'tasks_generated: True' in content:
                    print(f"   ⏭️  Skipping {meeting_file.name} - tasks already generated")
                    continue

                recent_meetings.append({
                    'file': meeting_file.name,
                    'date': mtime,
                    'content': content[:2000]  # First 2000 chars
                })
        except Exception as e:
            continue

    return sorted(recent_meetings, key=lambda x: x['date'], reverse=True)

def get_recent_alerts(client_name):
    """Check for recent performance alerts or anomalies"""
    alerts_file = PROJECT_ROOT / "data/cache/daily-performance-anomalies.json"

    if not alerts_file.exists():
        return []

    try:
        with open(alerts_file, 'r') as f:
            data = json.load(f)

        # Check last 3 days of anomalies
        client_alerts = []
        anomalies = data.get('anomalies', [])

        for anomaly in anomalies:
            if anomaly.get('client_name', '').lower() == client_name.lower():
                client_alerts.append(anomaly)

        return client_alerts
    except:
        return []

def get_pending_audits(client_path):
    """Check if client has recent audits that need action"""
    audits_dir = client_path / "audits"

    if not audits_dir.exists():
        return []

    recent_audits = []
    cutoff = datetime.now() - timedelta(days=7)

    for audit_file in audits_dir.glob("*-audit-index.md"):
        try:
            mtime = datetime.fromtimestamp(audit_file.stat().st_mtime)
            if mtime >= cutoff:
                recent_audits.append({
                    'file': audit_file.name,
                    'days_ago': (datetime.now() - mtime).days
                })
        except:
            continue

    return recent_audits

def filter_completed_tasks(context):
    """Remove completed task sections from context to prevent regeneration"""
    if not context:
        return context

    # Split context into lines
    lines = context.split('\n')
    filtered_lines = []
    skip_section = False
    section_start = -1

    for i, line in enumerate(lines):
        # Check if this is a task heading
        if line.startswith('### [') and ']' in line:
            # Look ahead for status line
            status_found = False
            is_complete = False

            # Check next 5 lines for status
            for j in range(1, min(6, len(lines) - i)):
                next_line = lines[i + j]
                if '**Status:**' in next_line:
                    status_found = True
                    # Check if completed
                    if '✅ Complete' in next_line or 'Complete' in next_line:
                        is_complete = True
                        skip_section = True
                        section_start = i
                    break

            if not is_complete:
                skip_section = False

        # Check if we're exiting a completed section (next heading or separator)
        if skip_section and (line.startswith('###') or line.startswith('---')) and i > section_start:
            skip_section = False
            # Don't add this line if it's just a separator after completed section
            if not line.startswith('---'):
                filtered_lines.append(line)
            continue

        # Add line if not in skip section
        if not skip_section:
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)

def analyze_client_work_needed(client_name, context, recent_meetings, alerts, audits):
    """Use Claude to analyze what work is needed for this client today"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None

    # Filter out completed tasks from context BEFORE sending to AI
    context = filter_completed_tasks(context)

    # Build analysis prompt
    meetings_summary = ""
    if recent_meetings:
        meetings_summary = f"\n\nRECENT MEETINGS (last 7 days):\n"
        for meeting in recent_meetings[:3]:
            meetings_summary += f"\n{meeting['file']} ({meeting['date'].strftime('%Y-%m-%d')}):\n{meeting['content'][:500]}\n"

    alerts_summary = ""
    if alerts:
        alerts_summary = f"\n\nRECENT ALERTS:\n"
        for alert in alerts:
            alerts_summary += f"- {alert.get('issue', 'Unknown issue')}\n"

    audits_summary = ""
    if audits:
        audits_summary = f"\n\nRECENT AUDITS:\n"
        for audit in audits:
            audits_summary += f"- {audit['file']} ({audit['days_ago']} days ago)\n"

    prompt = f"""You are analyzing the daily work requirements for a Google Ads client: {client_name}

CLIENT CONTEXT:
{context if context else "No context available"}
{meetings_summary}
{alerts_summary}
{audits_summary}

Based on this information, identify 1-3 specific, actionable tasks that should be done TODAY for this client.

Focus on:
- Urgent issues or alerts that need immediate attention
- Follow-up actions from recent meetings
- Regular monitoring and optimization tasks
- Audit findings that need implementation
- Proactive checks (budget pacing, performance trends, feed issues)

CRITICAL FILTERING RULES:
- IGNORE any task sections marked with "Status:** ✅ Complete" or "**Completed:**" - these are already done
- IGNORE any task sections marked with "[x]" - these are checked off
- ONLY create tasks for work that is genuinely outstanding and needs action TODAY
- Do NOT recreate tasks that have been marked complete, even if the underlying issue seems ongoing

Return ONLY a JSON array of tasks (no other text):
[
  {{
    "task": "Brief, actionable task description",
    "priority": "P0" | "P1" | "P2",
    "time_estimate": "10 mins" | "30 mins" | "1 hour" | "2 hours",
    "reason": "Why this task is needed today"
  }}
]

If there's genuinely nothing urgent for this client today, return an empty array: []

IMPORTANT: Return ONLY valid JSON, no markdown, no explanations."""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text.strip()

        # Extract JSON from response
        if response_text.startswith('['):
            tasks = json.loads(response_text)
            return tasks
        else:
            # Try to find JSON array in response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                tasks = json.loads(json_match.group(0))
                return tasks

        return []

    except Exception as e:
        print(f"   ⚠️  Error analyzing work: {e}")
        return []

def generate_daily_work():
    """Main function to generate daily work for all clients"""

    print("=" * 80)
    print("DAILY CLIENT WORK GENERATOR")
    print("=" * 80)
    print()
    print(f"Analyzing work needed for {datetime.now().strftime('%A, %B %d, %Y')}")
    print()

    # Get all active clients
    clients = get_active_clients()
    print(f"📋 Found {len(clients)} active clients")
    print()

    # Load analysis cache
    analysis_cache = load_analysis_cache()
    cache_hits = 0
    cache_misses = 0

    all_tasks = []
    clients_with_work = 0

    # Phase 3: Load completion stats for adaptive generation
    completion_stats = {}
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "shared" / "scripts"))
        from ai_tasks_state import get_client_completion_stats

        for client in clients:
            client_name = client['name']
            stats = get_client_completion_stats(client_name, days=7)
            completion_stats[client_name] = stats
    except Exception as e:
        print(f"Warning: Could not load completion stats: {e}")

    for i, client in enumerate(clients, 1):
        client_name = client['name']
        client_path = client['path']

        print(f"[{i}/{len(clients)}] Analyzing {client_name}...")

        # Phase 3: Check completion rate for adaptive generation
        stats = completion_stats.get(client_name, {})
        completion_rate = stats.get('completion_rate', 0.0)
        completions_this_week = stats.get('completions_this_week', 0)
        open_tasks = stats.get('open_tasks', 0)

        # Adaptive generation logic
        if completions_this_week >= 3:
            print(f"   ℹ️  High completion rate ({completions_this_week} completions this week) - reducing generation")
        elif completions_this_week == 0 and open_tasks == 0:
            print(f"   ℹ️  No recent activity - maintaining normal generation")
        elif completion_rate < 0.3 and open_tasks > 5:
            print(f"   ⚠️  Low completion rate ({completion_rate:.0%}) with {open_tasks} open tasks - reducing generation")

        # Gather client information
        context = read_context_file(client_path)
        meetings = get_recent_meetings(client_path)
        alerts = get_recent_alerts(client_name)
        audits = get_pending_audits(client_path)

        # Check if we can use cached analysis
        current_triggers = get_cache_triggers(client_path, context, alerts, audits)
        cache_valid, cache_reason = is_cache_valid(client_name, analysis_cache, current_triggers)

        if cache_valid:
            # Use cached analysis
            tasks = analysis_cache[client_name].get('analysis', [])
            cache_hits += 1
            print(f"   💾 Using cached analysis ({cache_reason})")
        else:
            # Analyze what work is needed (API call)
            cache_misses += 1
            print(f"   🔄 Fresh analysis ({cache_reason})")
            tasks = analyze_client_work_needed(client_name, context, meetings, alerts, audits)

            # Update cache with new analysis
            analysis_cache[client_name] = {
                'analysis': tasks,
                'cached_at': datetime.now().isoformat(),
                'triggers': current_triggers
            }
        
        # Phase 3: Apply adaptive filtering based on completion rate
        if tasks:
            original_count = len(tasks)
            
            # If high completion rate (3+ this week), reduce task count
            if completions_this_week >= 3:
                # Keep only P0 and P1 tasks, filter out P2
                tasks = [t for t in tasks if t.get('priority') in ['P0', 'P1']]
                if len(tasks) < original_count:
                    print(f"   → Filtered to {len(tasks)} high-priority task(s) (adaptive generation)")
            
            # If low completion rate with many open tasks, reduce generation
            elif completion_rate < 0.3 and open_tasks > 5:
                # Keep only P0 tasks
                tasks = [t for t in tasks if t.get('priority') == 'P0']
                if len(tasks) < original_count:
                    print(f"   → Filtered to {len(tasks)} urgent task(s) (low completion rate)")

        if tasks:
            clients_with_work += 1
            print(f"   ✓ {len(tasks)} task(s) identified")
            for task in tasks:
                task['client'] = client_name
                all_tasks.append(task)
        else:
            print(f"   → No urgent work needed today")

        print()

    # Sort all tasks by priority
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
    all_tasks.sort(key=lambda t: priority_order.get(t.get('priority', 'P2'), 2))

    # Save updated cache
    save_analysis_cache(analysis_cache)

    # Display summary
    print("=" * 80)
    print("DAILY WORK SUMMARY")
    print("=" * 80)
    print()
    print(f"**{clients_with_work}/{len(clients)} clients** need attention today")
    print(f"**{len(all_tasks)} total tasks** identified")
    print()
    print(f"💾 **Cache stats**: {cache_hits} cached / {cache_misses} fresh analysis")
    if cache_hits > 0:
        savings_pct = (cache_hits / (cache_hits + cache_misses)) * 100
        print(f"   → {savings_pct:.0f}% API calls saved by caching")
    print()

    if all_tasks:
        # Group by priority
        p0_tasks = [t for t in all_tasks if t.get('priority') == 'P0']
        p1_tasks = [t for t in all_tasks if t.get('priority') == 'P1']
        p2_tasks = [t for t in all_tasks if t.get('priority') == 'P2']

        if p0_tasks:
            print(f"🔴 **URGENT (P0)**: {len(p0_tasks)} tasks")
            for task in p0_tasks:
                print(f"   • [{task['client']}] {task['task']}")
                print(f"     {task.get('time_estimate', 'Unknown time')} - {task.get('reason', '')}")
            print()

        if p1_tasks:
            print(f"🟡 **HIGH PRIORITY (P1)**: {len(p1_tasks)} tasks")
            for task in p1_tasks[:5]:  # Show top 5
                print(f"   • [{task['client']}] {task['task']}")
            if len(p1_tasks) > 5:
                print(f"   ... and {len(p1_tasks) - 5} more P1 tasks")
            print()

        if p2_tasks:
            print(f"⚪ **NORMAL (P2)**: {len(p2_tasks)} tasks")
            for task in p2_tasks[:3]:  # Show top 3
                print(f"   • [{task['client']}] {task['task']}")
            if len(p2_tasks) > 3:
                print(f"   ... and {len(p2_tasks) - 3} more P2 tasks")

    # Phase 4: JSON output deprecated - tasks now stored in Google Tasks only
    # Historical note: JSON output was removed in Phase 4 to eliminate duplicate storage
    # All task data is now stored in Google Tasks as the single source of truth
    print()

    # Create Google Tasks (Phase 1 integration)
    CREATE_GOOGLE_TASKS = True  # Set to False to disable Google Tasks creation
    
    if CREATE_GOOGLE_TASKS and all_tasks:
        print()
        print("=" * 80)
        print("CREATING GOOGLE TASKS")
        print("=" * 80)
        print()
        
        try:
            # Import modules
            from tasks_service import tasks_service
            from duplicate_task_detector import is_duplicate_task, get_recent_tasks
            from ai_task_creator import create_ai_generated_task
            from ai_tasks_state import (
                check_should_regenerate,
                register_ai_task,
                get_ai_task_id
            )
            
            # Load config
            config_file = PROJECT_ROOT / "shared" / "config" / "ai-tasks-config.json"
            if not config_file.exists():
                print("⚠️  Config file not found. Run setup_ai_task_list.py first.")
                print("   Skipping Google Tasks creation.")
                return all_tasks
            
            with open(config_file, 'r') as f:
                ai_config = json.load(f)
            
            task_list_id = ai_config.get('task_list_id')
            
            if not task_list_id or task_list_id == "PLACEHOLDER_WILL_BE_SET_ON_FIRST_RUN":
                print("⚠️  Task list ID not configured. Run setup_ai_task_list.py first.")
                print("   Skipping Google Tasks creation.")
                return all_tasks
            
            # Connect to Google Tasks
            tasks_client = tasks_service()
            
            # Get recent tasks for duplicate detection
            duplicate_config = ai_config.get('duplicate_detection', {})
            if duplicate_config.get('enabled', True):
                lookback_days = duplicate_config.get('lookback_days', 7)
                existing_tasks = get_recent_tasks(task_list_id, lookback_days)
                print(f"📋 Found {len(existing_tasks)} recent tasks for duplicate detection")
                print()
            else:
                existing_tasks = []
            
            # Create tasks
            tasks_created = 0
            duplicates_skipped = 0
            skipped_by_state = 0
            errors = 0
            
            for task in all_tasks:
                client_name = task.get('client', '')
                task_title = task.get('task', '')
                
                # Phase 2: Check state file for context-aware regeneration
                should_regen, reason = check_should_regenerate(
                    client_name,
                    task_title,
                    task.get('priority', 'P2'),
                    duplicate_config
                )
                
                if not should_regen:
                    skipped_by_state += 1
                    print(f"   ⏭  Skipped (state check): [{client_name}] {task_title}")
                    if reason:
                        print(f"      Reason: {reason}")
                    continue
                
                # Check for duplicates (existing logic)
                if duplicate_config.get('enabled', True) and existing_tasks:
                    is_dup, matching_task = is_duplicate_task(task, existing_tasks, duplicate_config)
                    
                    if is_dup:
                        duplicates_skipped += 1
                        match_title = matching_task.get('title', 'Unknown') if matching_task else 'Unknown'
                        match_reason = matching_task.get('notes', '') if matching_task else ''
                        print(f"   ⏭  Skipped duplicate: [{client_name}] {task_title}")
                        print(f"      Matches: {match_title}")
                        if match_reason and 'State file check' in match_reason:
                            print(f"      Reason: {match_reason}")
                        continue
                
                # Create task
                try:
                    created_task = create_ai_generated_task(
                        task, 
                        task_list_id, 
                        tasks_client,
                        ai_config
                    )
                    
                    if not created_task or not created_task.get('id'):
                        errors += 1
                        print(f"   ✗ Failed to create task: [{client_name}] {task_title}")
                        continue
                    
                    # Phase 2: Register task in state file (atomic operation)
                    ai_task_id = created_task.get('ai_task_id')
                    google_task_id = created_task.get('id')
                    
                    if ai_task_id and google_task_id:
                        try:
                            register_ai_task(
                                ai_task_id,
                                google_task_id,
                                client_name,
                                task_title,
                                task.get('priority', 'P2'),
                                created_task.get('due', '')
                            )
                        except Exception as reg_error:
                            # If state registration fails, log but don't fail the task creation
                            print(f"   ⚠  Warning: Failed to register task in state file: {reg_error}")
                            print(f"      Task created but may be regenerated: Google Task ID {google_task_id}")
                    
                    tasks_created += 1
                    due_date = created_task.get('due', 'N/A')
                    # Format due date for display
                    if due_date != 'N/A' and 'T' in due_date:
                        try:
                            due_dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                            due_date = due_dt.strftime('%Y-%m-%d')
                        except:
                            pass
                    print(f"   ✓ Created: [{task['client']}] {task['task']} (Due: {due_date})")
                except Exception as e:
                    errors += 1
                    print(f"   ⚠️  Error creating task [{task['client']}] {task['task']}: {e}")
            
            print()
            print(f"✅ {tasks_created} task(s) created in Google Tasks")
            if duplicates_skipped > 0:
                print(f"⏭  {duplicates_skipped} duplicate(s) skipped")
            if skipped_by_state > 0:
                print(f"⏭  {skipped_by_state} task(s) skipped (context-aware)")
            if errors > 0:
                print(f"⚠️  {errors} error(s) encountered")
            print()
            
            # Phase 4: Record metrics
            try:
                sys.path.insert(0, str(PROJECT_ROOT / "shared" / "scripts"))
                from task_monitoring_dashboard import record_daily_stats
                record_daily_stats(tasks_created, duplicates_skipped, skipped_by_state, errors)
            except Exception as e:
                # Graceful fallback if metrics recording fails
                pass
            
        except ImportError as e:
            print(f"⚠️  Import error: {e}")
            print("   Skipping Google Tasks creation. Ensure modules are available.")
            print()
        except Exception as e:
            print(f"❌ Error creating Google Tasks: {e}")
            print("   Falling back to JSON-only mode")
            import traceback
            traceback.print_exc()
            print()

    return all_tasks

if __name__ == "__main__":
    try:
        generate_daily_work()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
