#!/usr/bin/env python3
"""
PetesBrain Daily Briefing Generator

Creates a comprehensive daily briefing covering:
- Today's calendar events (via Google Calendar API)
- Recent client performance anomalies
- Pending tasks from tasks-completed.json
- Recent client alerts from last 24 hours
- AI inbox processing activity (notes processed, tasks created, etc.)
- AI-generated priority summary

Runs daily at 7:00 AM via LaunchAgent
Output: briefing/YYYY-MM-DD-briefing.md
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Keychain secrets module
from shared.secrets import get_secret

def get_today_str():
    """Get today's date as YYYY-MM-DD"""
    return datetime.now().strftime('%Y-%m-%d')

def get_yesterday_str():
    """Get yesterday's date as YYYY-MM-DD"""
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_briefing_path():
    """Get path for today's briefing"""
    briefing_dir = PROJECT_ROOT / 'briefing'
    briefing_dir.mkdir(exist_ok=True)
    return briefing_dir / f"{get_today_str()}-briefing.md"

def get_calendar_events():
    """
    Get today's calendar events from Google Calendar
    """
    try:
        # Try to use Google Calendar client
        sys.path.insert(0, str(PROJECT_ROOT / 'shared'))
        from google_calendar_client import get_today_events

        events = get_today_events()

        if not events:
            return "### Calendar - Today\n\n**No events scheduled for today**\n"

        output = "### Calendar - Today\n\n"

        for event in events:
            start_time = event['start']
            summary = event['summary']

            # Parse time
            if 'T' in start_time:
                # DateTime event
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                time_str = dt.strftime('%I:%M %p')
                output += f"- **{time_str}** - {summary}\n"
            else:
                # All-day event
                output += f"- **All day** - {summary}\n"

        return output

    except Exception as e:
        return f"### Calendar - Today\n\n*Calendar integration error: {str(e)}*\n"

def get_recent_anomalies():
    """Get recent performance anomalies (2-day lag for data accuracy)"""
    anomaly_file = PROJECT_ROOT / 'data' / 'cache' / 'daily-performance-anomalies.json'

    if not anomaly_file.exists():
        return "**No anomaly data available**\n"

    try:
        with open(anomaly_file, 'r') as f:
            data = json.load(f)

        # Check data freshness - anomalies use 2-day lag for accurate data
        two_days_ago = (datetime.now().date() - timedelta(days=2)).strftime('%Y-%m-%d')
        file_date = data.get('target_date') or data.get('date')

        # Allow data from 2-3 days ago (in case of timing differences)
        three_days_ago = (datetime.now().date() - timedelta(days=3)).strftime('%Y-%m-%d')
        if file_date not in [two_days_ago, three_days_ago]:
            return f"**Anomaly data stale** *(data from {file_date}, expected {two_days_ago})*\n"

        # Anomalies can be a dict (keyed by client) or a list
        anomalies_data = data.get('anomalies', {})

        if isinstance(anomalies_data, dict):
            # New format: dict keyed by client name
            if not anomalies_data:
                return f"**No anomalies detected ✅** *(data from {file_date})*\n"

            output = ""
            for client, client_anomalies in anomalies_data.items():
                for anomaly in client_anomalies:
                    severity = anomaly.get('severity', 'warning')
                    emoji = "🔴" if severity == "critical" else "🟡"
                    message = anomaly.get('message', anomaly.get('issue', ''))
                    output += f"{emoji} **{client}**: {message}\n"

            return output if output else f"**No anomalies detected ✅** *(data from {file_date})*\n"
        else:
            # Old format: list of anomalies
            if not anomalies_data:
                return f"**No anomalies detected ✅** *(data from {file_date})*\n"

            output = ""
            for anomaly in anomalies_data:
                severity = anomaly.get('severity', 'warning')
                emoji = "🔴" if severity == "critical" else "🟡"
                client = anomaly.get('client_name', 'Unknown')
                issue = anomaly.get('issue', anomaly.get('message', ''))
                output += f"{emoji} **{client}**: {issue}\n"

            return output

    except Exception as e:
        return f"*Error reading anomalies: {str(e)}*\n"

def get_task_priority(task):
    """
    Extract priority from task title and notes.
    Returns tuple: (priority_score, priority_label)
    Lower score = higher priority (P0=0, P1=1, etc.)
    """
    title = task.get('title', '').upper()
    notes = task.get('notes', '').upper()
    combined = f"{title} {notes}"

    # Check for explicit priority indicators
    if 'CRITICAL' in combined or 'URGENT' in combined or 'P0' in combined:
        return (0, 'P0')
    elif 'HIGH' in combined or 'P1' in combined or 'THIS WEEK' in combined:
        return (1, 'P1')
    elif 'MEDIUM' in combined or 'P2' in combined:
        return (2, 'P2')
    elif 'LOW' in combined or 'P3' in combined:
        return (3, 'P3')
    else:
        # Default priority based on due date
        return (2, 'P2')  # Default to P2 (Medium)

def get_time_estimate(task):
    """Extract time estimate from task notes (e.g., '30 mins', '1-2 hours')"""
    notes = task.get('notes', '')

    # Look for patterns like "30 mins", "1-2 hours", "10 minutes"
    import re

    # Match patterns like: 30 mins, 1-2 hours, 10 minutes
    patterns = [
        r'(\d+)\s*min',       # "30 mins" or "30 minutes"
        r'(\d+)-(\d+)\s*hour', # "1-2 hours"
        r'(\d+)\s*hour',       # "1 hour"
    ]

    for pattern in patterns:
        match = re.search(pattern, notes.lower())
        if match:
            return match.group(0)

    return None


def extract_source_from_task(task):
    """
    Extract source attribution from task notes.

    Returns:
        String describing where the task came from
    """
    notes = task.get('notes', '')

    # Check for explicit source in notes
    source_match = re.search(r'\*\*Source:\*\*\s*(.+?)(?:\n|$)', notes)
    if source_match:
        return source_match.group(1).strip()

    # Check for client request patterns
    if 'client request' in notes.lower() or 'requested by' in notes.lower():
        # Try to extract client name
        client_match = re.search(r'(?:request from|requested by|client[: ]+)([A-Za-z]+)', notes, re.IGNORECASE)
        if client_match:
            return f"Client request - {client_match.group(1).title()}"
        return "Client request"

    # Check for meeting references
    if 'meeting' in notes.lower():
        meeting_match = re.search(r'(?:meeting|discussed)\s+(?:on\s+)?([A-Za-z]+\s+\d+)', notes, re.IGNORECASE)
        if meeting_match:
            return f"Client meeting ({meeting_match.group(1)})"
        return "Client meeting"

    # Check for committed/promised patterns
    if 'COMMITTED' in notes or 'PROMISED' in notes:
        committed_match = re.search(r'COMMITTED TO ([A-Z]+)', notes)
        if committed_match:
            return f"Committed to {committed_match.group(1).title()}"
        return "Client commitment"

    # Check for proactive monitoring
    if 'proactive' in notes.lower() or 'monitoring' in notes.lower():
        return "Proactive monitoring"

    # Check for task list name in task dict
    tasklist_name = task.get('tasklist_name', '')
    if tasklist_name and tasklist_name != 'Unknown List':
        return f"Google Tasks - {tasklist_name}"

    # Default
    return "Google Tasks"

def format_task_for_email(task, use_upcoming_label=False, today=None):
    """
    Format a task for inclusion in email, handling both pre-verified and standard tasks.

    Args:
        task: Task dict (may include '_verification' key if pre-verified)
        use_upcoming_label: Whether to show due dates
        today: Today's date for date comparison

    Returns:
        Formatted string for email
    """
    if today is None:
        today = datetime.now().date()

    # Extract source
    source = extract_source_from_task(task)

    # Extract time estimate
    notes = task.get('notes', '')
    time_match = re.search(r'\*\*Time Estimate:\*\*\s*(.+?)(?:\n|$)', notes)
    time_estimate = time_match.group(1).strip() if time_match else "Est. time not set"

    # Check if task was pre-verified
    if '_verification' in task:
        # Use CONDENSED pre-verified format
        verification = task['_verification']
        title = task['title']

        status_emoji = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }.get(verification['status'], '📋')

        output = f"**{title}** {status_emoji} PRE-VERIFIED\n"
        output += f"⏱️ {time_estimate} · 📍 {source}\n"

        # Extract client name for completion phrase
        client_match = re.search(r'\[([^\]]+)\]', title)
        client = client_match.group(1).lower() if client_match else "client"

        # CONDENSED: Just the key info
        output += f"{status_emoji} {verification['summary']}\n"
        output += f"→ Reply \"{client} verified - close\" to complete\n\n"
        return output
    else:
        # Use standard format with clear structure
        title = task['title']
        due = task.get('due', '')

        # Add due date prefix if not today
        due_prefix = ""
        if due and use_upcoming_label:
            try:
                due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                if due_date != today:
                    formatted_date = due_date.strftime('%b %d')
                    due_prefix = f"**{formatted_date}** · "
            except:
                pass

        output = f"{due_prefix}**{title}**\n"
        output += f"⏱️ {time_estimate} · 📍 {source}\n"

        # Extract context/reason from notes
        reason_match = re.search(r'\*\*Reason:\*\*\s*(.+?)(?:\n\n|\n\*\*|$)', notes, re.DOTALL)
        if reason_match:
            context = reason_match.group(1).strip()
            # Clean up any extra formatting
            context = re.sub(r'\n+', ' ', context)
            output += f"{context}\n\n"
        else:
            output += "\n"

        return output

def get_client_work_for_today():
    """Get client work from aggregated task file"""

    try:
        # Load from aggregated task file
        tasks_file = PROJECT_ROOT / 'data' / 'state' / 'client-tasks.json'

        if not tasks_file.exists():
            return "## 🎯 Client Work for Today\n\n**No tasks file found**\n\n*Run task sync to populate tasks.*\n"

        with open(tasks_file, 'r') as f:
            data = json.load(f)

        all_tasks = data.get('tasks', [])

        # Filter to active tasks (overdue, due today, or due in next 7 days)
        today = datetime.now().date()
        cutoff = today + timedelta(days=7)

        upcoming_tasks = []
        for task in all_tasks:
            if task.get('status') != 'active':
                continue
            due_str = task.get('due_date')
            if not due_str:
                # Include tasks without due dates
                upcoming_tasks.append(task)
                continue
            try:
                due_date = datetime.fromisoformat(due_str).date()
                # Include overdue tasks (due_date < today) and upcoming tasks
                if due_date <= cutoff:
                    upcoming_tasks.append(task)
            except:
                continue

        if not upcoming_tasks:
            return "## 🎯 Client Work for Today\n\n**No tasks due today or in next 7 days**\n\n*All clients are up to date. Check back tomorrow or create new tasks if needed.*\n"

        # Sort by due date then priority
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        upcoming_tasks.sort(key=lambda t: (t.get('due_date') or '9999', priority_order.get(t.get('priority', 'P2'), 2)))

        # Determine if we're showing upcoming tasks or just today
        today_tasks = [t for t in upcoming_tasks if t.get('due_date') == today.isoformat()]
        use_upcoming_label = len(upcoming_tasks) > len(today_tasks)

        # Organize by priority
        p0_tasks = [t for t in upcoming_tasks if t.get('priority') == 'P0']
        p1_tasks = [t for t in upcoming_tasks if t.get('priority') == 'P1']
        p2_tasks = [t for t in upcoming_tasks if t.get('priority') == 'P2']
        p3_tasks = [t for t in upcoming_tasks if t.get('priority') == 'P3']

        # Format output
        if use_upcoming_label:
            output = "## 🎯 Client Work (Upcoming)\n\n"
            output += f"**{len(upcoming_tasks)} task(s)** due in next 7 days\n\n"
        else:
            output = "## 🎯 Client Work for Today\n\n"
            output += f"**{len(upcoming_tasks)} task(s)** due today\n\n"

        def format_task_simple(task):
            title = task.get('title', 'Untitled')
            due = task.get('due_date', '')
            client = task.get('client', '')
            time_est = task.get('time_estimate_mins', 0)
            time_str = f"{time_est} mins" if time_est else ""

            # Format due date
            due_str = ""
            if due:
                try:
                    due_dt = datetime.fromisoformat(due).date()
                    if due_dt == today:
                        due_str = "Today"
                    elif due_dt == today + timedelta(days=1):
                        due_str = "Tomorrow"
                    else:
                        due_str = due_dt.strftime('%a %d %b')
                except:
                    due_str = due

            line = f"- **{title}**"
            if due_str:
                line += f" *(Due: {due_str})*"
            if time_str:
                line += f" [{time_str}]"
            return line + "\n"

        if p0_tasks:
            output += "### 🔴 URGENT (P0)\n\n"
            for task in p0_tasks:
                output += format_task_simple(task)
            output += "\n"

        if p1_tasks:
            output += "### 🟡 HIGH PRIORITY (P1)\n\n"
            for task in p1_tasks:
                output += format_task_simple(task)
            output += "\n"

        if p2_tasks:
            output += "### ⚪ NORMAL (P2)\n\n"
            for task in p2_tasks:
                output += format_task_simple(task)
            output += "\n"

        if p3_tasks:
            output += f"### ℹ️ LOW (P3): {len(p3_tasks)} task(s)\n\n"

        return output

    except Exception as e:
        return f"## 🎯 Client Work for Today\n\n*Error loading client work: {str(e)}*\n"

def get_pending_tasks():
    """Get active tasks from Google Tasks for today"""
    try:
        # Try to use Google Tasks MCP to get active tasks
        sys.path.insert(0, str(PROJECT_ROOT / 'shared'))
        from google_tasks_client import get_all_active_tasks

        active_tasks = get_all_active_tasks()

        if not active_tasks:
            return "**No active tasks in Google Tasks**\n"

        # Separate by due date AND priority
        today = datetime.now().date()
        overdue = []
        due_today = []
        upcoming = []
        no_due = []

        # Filter out client tasks (they'll be shown in Client Work section)
        # Client tasks have format: [Client Name] Task description OR mention client names
        
        # Get all client names from client directories (more reliable than JSON)
        client_names = []
        client_folders = PROJECT_ROOT / 'clients'
        if client_folders.exists():
            for client_dir in sorted(client_folders.iterdir()):
                if client_dir.is_dir() and not client_dir.name.startswith('_'):
                    # Add folder name (kebab-case)
                    client_names.append(client_dir.name.lower())
                    # Add display name (Title Case)
                    display_name = client_dir.name.replace('-', ' ').title()
                    client_names.append(display_name.lower())
                    # Add common variations
                    if 'devonshire' in client_dir.name:
                        client_names.extend(['devonshire', 'devonshire hotels', 'devonshire group'])
                    elif 'national-design-academy' in client_dir.name:
                        client_names.extend(['nda', 'national design academy', 'national design'])
                    elif 'accessories-for-the-home' in client_dir.name:
                        client_names.extend(['accessories for the home', 'accessories', 'uno accessories'])
                    elif 'uno-lighting' in client_dir.name:
                        client_names.extend(['uno lighting', 'uno', 'uno lights'])
                    elif 'just-bin-bags' in client_dir.name:
                        client_names.extend(['just bin bags', 'jbb'])
                    elif 'crowd-control' in client_dir.name:
                        client_names.extend(['crowd control', 'crowdcontrol'])
                    elif 'go-glean' in client_dir.name:
                        client_names.extend(['go glean', 'goglean', 'go clean'])
                    elif 'grain-guard' in client_dir.name:
                        client_names.extend(['grain guard', 'grainguard'])
                    elif 'bright-minds' in client_dir.name:
                        client_names.extend(['bright minds', 'brightminds'])
                    elif 'tree2mydoor' in client_dir.name:
                        client_names.extend(['tree2mydoor', 'tree 2 my door', 'tree to my door'])

        # Add standalone clients without dedicated folders (separate clients that share infrastructure)
        client_names.extend([
            'nma', 'national motorsports academy', 'national motorsports'
        ])
        
        # Remove duplicates and empty strings
        client_names = list(set([c for c in client_names if c and len(c) > 2]))
        
        personal_tasks = []
        import re
        for task in active_tasks:
            title = task.get('title', '')
            notes = task.get('notes', '')
            combined = f"{title} {notes}".lower()
            original_title = title  # Keep original for bracket check
            
            # Skip tasks that look like client work
            is_client_task = False
            
            # Check 1: [Client Name] format
            if original_title.startswith('[') and ']' in original_title:
                is_client_task = True
            
            # Check 2: AI-generated task metadata
            if '**Source:** AI Generated' in notes or '**Client:**' in notes:
                is_client_task = True
            
            # Check 3: Any client name mentioned (with word boundaries to avoid false positives)
            for client_name in client_names:
                if not client_name or len(client_name) < 3:
                    continue
                # Use word boundaries to avoid matching "roxys" in "roksys"
                pattern = r'\b' + re.escape(client_name) + r'\b'
                if re.search(pattern, combined, re.IGNORECASE):
                    is_client_task = True
                    break
            
            # Check 4: Multi-client patterns like "Godshot & Crowd Control" or "Client, Client"
            multi_client_patterns = [
                r'\b(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)\s*[&\-]\s*(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)',
                r'\b(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)\s*,\s*(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)',
            ]
            for pattern in multi_client_patterns:
                if re.search(pattern, combined, re.IGNORECASE):
                    is_client_task = True
                    break
            
            # Check 5: Pattern like "Client: Task" or "Client - Task" (colon or dash separator)
            client_colon_pattern = r'\b(?:smythson|godshot|crowd control|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma|accessories|uno)\s*[:\-]\s*'
            if re.search(client_colon_pattern, combined, re.IGNORECASE):
                is_client_task = True
            
            if not is_client_task:
                personal_tasks.append(task)
        
        if not personal_tasks:
            return "**No personal tasks in Google Tasks**\n"
        
        for task in personal_tasks:
            # Add priority info to task
            priority_score, priority_label = get_task_priority(task)
            task['_priority_score'] = priority_score
            task['_priority_label'] = priority_label
            task['_time_estimate'] = get_time_estimate(task)

            due = task.get('due')
            if due:
                try:
                    due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                    if due_date < today:
                        overdue.append(task)
                    elif due_date == today:
                        due_today.append(task)
                    else:
                        upcoming.append(task)
                except:
                    no_due.append(task)
            else:
                no_due.append(task)

        # Sort each category by priority first, then by date
        overdue.sort(key=lambda t: (t.get('_priority_score', 999), t.get('due', '')))
        due_today.sort(key=lambda t: t.get('_priority_score', 999))
        no_due.sort(key=lambda t: t.get('_priority_score', 999))

        output = ""

        if overdue:
            output += "**⚠️ Overdue:**\n\n"
            for task in overdue[:5]:
                title = task.get('title', 'Untitled')
                task_id = task.get('id', '')
                due = task.get('due', '')
                priority = task.get('_priority_label', 'P2')
                time_est = task.get('_time_estimate')

                # Create clickable link to Google Tasks
                task_link = f"https://tasks.google.com/task/{task_id}" if task_id else ""

                # Build priority + time display
                meta = f"**{priority}**"
                if time_est:
                    meta += f" · {time_est}"

                if task_link:
                    if due:
                        due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                        formatted_date = due_date.strftime('%b %d')
                        output += f"- 🔴 **{formatted_date}** · {meta}: [{title}]({task_link})\n\n"
                    else:
                        output += f"- 🔴 {meta}: [{title}]({task_link})\n\n"
                else:
                    # Fallback if no task ID
                    if due:
                        due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                        formatted_date = due_date.strftime('%b %d')
                        output += f"- 🔴 **{formatted_date}** · {meta}: {title}\n\n"
                    else:
                        output += f"- 🔴 {meta}: {title}\n\n"

        if due_today:
            output += "**📅 Due Today:**\n\n"

            # Calculate total time for today
            total_mins = 0
            for task in due_today[:10]:
                time_est = task.get('_time_estimate')
                if time_est:
                    # Extract minutes from time estimate
                    import re
                    mins_match = re.search(r'(\d+)\s*min', time_est)
                    hours_match = re.search(r'(\d+)(?:-(\d+))?\s*hour', time_est)
                    if mins_match:
                        total_mins += int(mins_match.group(1))
                    elif hours_match:
                        # Use average if range, otherwise use single value
                        if hours_match.group(2):
                            avg_hours = (int(hours_match.group(1)) + int(hours_match.group(2))) / 2
                            total_mins += int(avg_hours * 60)
                        else:
                            total_mins += int(hours_match.group(1)) * 60

            if total_mins > 0:
                hours = total_mins // 60
                mins = total_mins % 60
                if hours > 0:
                    output += f"*Total estimated time: {hours}h {mins}m*\n\n"
                else:
                    output += f"*Total estimated time: {mins}m*\n\n"

            for task in due_today[:10]:
                title = task.get('title', 'Untitled')
                task_id = task.get('id', '')
                priority = task.get('_priority_label', 'P2')
                time_est = task.get('_time_estimate')
                notes = task.get('notes', '')

                # Create clickable link to Google Tasks
                task_link = f"https://mail.google.com/tasks/canvas" if task_id else ""

                # Build priority + time display
                meta = f"**{priority}**"
                if time_est:
                    meta += f" · {time_est}"

                # Extract key details from notes (first 3 non-empty lines)
                details = []
                if notes:
                    lines = [line.strip() for line in notes.split('\n') if line.strip()]
                    # Skip markdown headers, metadata, and common noise
                    skip_patterns = ['#', 'Priority:', '<!--', 'Wispr Flow Note', 'Status:', '**Status:**']
                    for line in lines[:8]:  # Look at more lines to find useful content
                        if not any(line.startswith(pattern) for pattern in skip_patterns):
                            details.append(line)
                            if len(details) >= 3:
                                break

                output += f"- {meta}: **{title}**\n"
                for detail in details:
                    # Truncate long lines to 100 chars
                    if len(detail) > 100:
                        detail = detail[:97] + "..."
                    output += f"  • {detail}\n"
                output += "\n"

        if upcoming:
            output += "**📆 Coming Up (Next 7 Days):**\n\n"
            # Filter to next 7 days only and sort by date
            seven_days_from_now = today + timedelta(days=7)
            upcoming_week = []
            for task in upcoming:
                due = task.get('due', '')
                if due:
                    due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                    if due_date <= seven_days_from_now:
                        upcoming_week.append((due_date, task))

            # Sort by date
            upcoming_week.sort(key=lambda x: x[0])

            for due_date, task in upcoming_week[:10]:  # Show up to 10 tasks
                title = task.get('title', 'Untitled')
                task_id = task.get('id', '')
                priority = task.get('_priority_label', 'P2')
                time_est = task.get('_time_estimate')
                notes = task.get('notes', '')
                formatted_date = due_date.strftime('%b %d')

                # Create clickable link to Google Tasks
                task_link = f"https://mail.google.com/tasks/canvas" if task_id else ""

                # Build priority + time display
                meta = f"**{priority}**"
                if time_est:
                    meta += f" · {time_est}"

                # Extract key details from notes (first 3 non-empty lines)
                details = []
                if notes:
                    lines = [line.strip() for line in notes.split('\n') if line.strip()]
                    # Skip markdown headers, metadata, and common noise
                    skip_patterns = ['#', 'Priority:', '<!--', 'Wispr Flow Note', 'Status:', '**Status:**']
                    for line in lines[:8]:  # Look at more lines to find useful content
                        if not any(line.startswith(pattern) for pattern in skip_patterns):
                            details.append(line)
                            if len(details) >= 3:
                                break

                output += f"- **{formatted_date}** · {meta}: **{title}**\n"
                for detail in details:
                    # Truncate long lines to 100 chars
                    if len(detail) > 100:
                        detail = detail[:97] + "..."
                    output += f"  • {detail}\n"
                output += "\n"

        if no_due and not (overdue or due_today or upcoming):
            output += "**No Due Date:**\n"
            for task in no_due[:5]:
                title = task.get('title', 'Untitled')
                output += f"- {title}\n"

        return output if output else "**No active tasks**\n"

    except Exception as e:
        # Fallback to completed tasks if Google Tasks integration fails
        return f"*Unable to fetch active tasks - {str(e)}*\n\n" + get_completed_tasks_fallback()

def get_completed_tasks_fallback():
    """Fallback: Get recently completed tasks from JSON"""
    tasks_file = PROJECT_ROOT / 'data' / 'state' / 'tasks-completed.json'

    if not tasks_file.exists():
        return ""

    try:
        with open(tasks_file, 'r') as f:
            data = json.load(f)

        if isinstance(data, list):
            tasks = data
        else:
            tasks = data.get('tasks', [])

        # Get tasks from last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_tasks = []

        for task in tasks:
            if not isinstance(task, dict):
                continue
            task_date = task.get('completed_at', '')
            if task_date:
                try:
                    task_datetime = datetime.fromisoformat(task_date.replace('Z', '+00:00'))
                    if task_datetime >= seven_days_ago:
                        recent_tasks.append(task)
                except:
                    pass

        if not recent_tasks:
            return ""

        output = "**Recently Completed (last 7 days):**\n"
        for task in recent_tasks[:5]:
            title = task.get('title', 'Untitled')
            output += f"- ✅ {title}\n"

        return output

    except:
        return ""

def get_recent_meeting_notes():
    """Get meetings from yesterday and today (accounting for processing delays)"""
    clients_dir = PROJECT_ROOT / 'clients'
    yesterday = get_yesterday_str()
    today = get_today_str()

    meetings = []

    # Scan all client meeting-notes folders
    for client_dir in clients_dir.iterdir():
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        meeting_notes_dir = client_dir / 'meeting-notes'
        if not meeting_notes_dir.exists():
            continue

        for meeting_file in meeting_notes_dir.glob('*.md'):
            filename = meeting_file.stem
            # Skip Granola "enhanced-notes" files
            if '--enhanced-notes--' in filename:
                continue
            # Skip shared/unassigned folder meetings
            if client_dir.name in ['shared', '_unassigned']:
                continue
            # Check if filename contains yesterday or today's date
            if yesterday in filename or today in filename:
                meetings.append({
                    'client': client_dir.name,
                    'file': meeting_file.name,
                    'path': meeting_file
                })

    if not meetings:
        return "**No meetings in last 2 days**\n"

    output = ""
    for meeting in meetings:
        # Try to extract actual meeting date from filename
        filename_lower = meeting['file'].lower()
        if yesterday in filename_lower:
            date_label = " *(Yesterday)*"
        elif today in filename_lower:
            date_label = " *(Today)*"
        else:
            date_label = ""

        output += f"- **{meeting['client']}**{date_label}: {meeting['file']}\n"

    return output

def get_weekly_performance_summary():
    """Get high-level performance summary from weekly data"""
    weekly_file = PROJECT_ROOT / 'data' / 'cache' / 'weekly-client-performance.json'
    
    if not weekly_file.exists():
        return "*Weekly performance data not available*\n"
    
    try:
        with open(weekly_file, 'r') as f:
            data = json.load(f)
        
        clients = data.get('clients', [])
        if not clients:
            return "*No client data available*\n"
        
        # Summarize trends - trend is nested in 'changes' object
        up_count = sum(1 for c in clients if c.get('changes', {}).get('trend', '').lower() == 'up')
        down_count = sum(1 for c in clients if c.get('changes', {}).get('trend', '').lower() == 'down')
        stable_count = sum(1 for c in clients if c.get('changes', {}).get('trend', '').lower() == 'stable')

        output = f"**Week Trends:** {up_count} Up ↗️  |  {stable_count} Stable →  |  {down_count} Down ↘️\n\n"

        # Show any notable changes - revenue_pct is also in 'changes' object
        notable = [c for c in clients if abs(c.get('changes', {}).get('revenue_pct', 0)) > 20]
        if notable:
            output += "**Notable Changes:**\n"
            for client in notable[:3]:  # Top 3
                name = client.get('name', 'Unknown')
                change = client.get('changes', {}).get('revenue_pct', 0)
                direction = "↗️" if change > 0 else "↘️"
                output += f"- {name}: {abs(change):.1f}% {direction}\n"
        
        return output
        
    except Exception as e:
        return f"*Error reading weekly performance: {str(e)}*\n"

def generate_ai_summary(briefing_content):
    """
    Generate AI summary using Claude
    
    Note: Requires ANTHROPIC_API_KEY environment variable
    """
    try:
        import anthropic

        api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
        if not api_key:
            return "*AI summary unavailable - ANTHROPIC_API_KEY not set*"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"""You are Pete's AI assistant for a digital marketing agency (Roksys). 

Based on this daily briefing, provide a 2-3 sentence executive summary highlighting the most important things to focus on today. Be direct and actionable.

Briefing content:
{briefing_content}

Provide only the summary, no preamble."""
            }]
        )
        
        return message.content[0].text.strip()
        
    except ImportError:
        return "*AI summary unavailable - anthropic package not installed*"
    except Exception as e:
        return f"*AI summary unavailable - {str(e)}*"

def get_recent_kb_updates():
    """
    Get recent knowledge base updates from last 7 days across:
    - Platform updates (roksys/knowledge-base/_inbox/documents/)
    - Client documents (clients/*/documents/)
    - Experiment log (rok-experiments-client-notes.csv)

    Returns formatted markdown section or empty string if no updates
    """
    try:
        seven_days_ago = datetime.now() - timedelta(days=7)

        updates = {
            'platform': [],
            'clients': [],
            'experiments': []
        }

        # Scan platform updates inbox
        platform_inbox = PROJECT_ROOT / 'roksys' / 'knowledge-base' / '_inbox' / 'documents'
        if platform_inbox.exists():
            for doc in platform_inbox.glob('*.md'):
                try:
                    mtime = datetime.fromtimestamp(doc.stat().st_mtime)
                    if mtime >= seven_days_ago:
                        # Extract title from filename (format: YYYY-MM-DD_category_title.md)
                        filename_parts = doc.stem.split('_', 2)
                        if len(filename_parts) >= 3:
                            date_str, category, title = filename_parts[0], filename_parts[1], filename_parts[2]
                            title_clean = title.replace('-', ' ').title()
                            updates['platform'].append({
                                'date': date_str,
                                'category': category.upper(),
                                'title': title_clean,
                                'path': str(doc.relative_to(PROJECT_ROOT))
                            })
                except Exception:
                    continue

        # Scan client documents
        clients_dir = PROJECT_ROOT / 'clients'
        if clients_dir.exists():
            for client_dir in clients_dir.iterdir():
                if not client_dir.is_dir() or client_dir.name.startswith('_'):
                    continue

                docs_dir = client_dir / 'documents'
                if docs_dir.exists():
                    for doc in docs_dir.glob('*.{md,html}'):
                        try:
                            mtime = datetime.fromtimestamp(doc.stat().st_mtime)
                            if mtime >= seven_days_ago:
                                # Extract meaningful title from filename
                                title = doc.stem
                                if title.startswith('email-draft-'):
                                    title = title.replace('email-draft-', 'Email: ')
                                elif title.startswith('whatsapp-draft-'):
                                    title = title.replace('whatsapp-draft-', 'WhatsApp: ')

                                title = title.replace('-', ' ').title()

                                updates['clients'].append({
                                    'date': mtime.strftime('%Y-%m-%d'),
                                    'client': client_dir.name.replace('-', ' ').title(),
                                    'title': title,
                                    'path': str(doc.relative_to(PROJECT_ROOT))
                                })
                        except Exception:
                            continue

        # Scan experiment log
        exp_log = PROJECT_ROOT / 'roksys' / 'spreadsheets' / 'rok-experiments-client-notes.csv'
        if exp_log.exists():
            try:
                import csv
                with open(exp_log, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        log_date = row.get('Date', '')
                        if log_date:
                            try:
                                log_datetime = datetime.strptime(log_date, '%Y-%m-%d')
                                if log_datetime >= seven_days_ago:
                                    updates['experiments'].append({
                                        'date': log_date,
                                        'client': row.get('Client', 'Unknown'),
                                        'change': row.get('Change', '')[:100]  # Truncate long changes
                                    })
                            except:
                                pass
            except Exception:
                pass

        # Format output
        if not any(updates.values()):
            return ""

        output = "## 📚 Recent Knowledge Base Updates (Last 7 Days)\n\n"

        if updates['platform']:
            output += f"#### Platform Updates ({len(updates['platform'])} new)\n"
            for item in sorted(updates['platform'], key=lambda x: x['date'], reverse=True)[:5]:
                output += f"- **{item['date']}** - {item['category']}: [{item['title']}]({item['path']})\n"
            output += "\n"

        if updates['clients']:
            output += f"#### Client Developments ({len(updates['clients'])} new)\n"
            for item in sorted(updates['clients'], key=lambda x: x['date'], reverse=True)[:5]:
                output += f"- **{item['date']}** - {item['client']}: [{item['title']}]({item['path']})\n"
            output += "\n"

        if updates['experiments']:
            output += f"#### Experiments Logged ({len(updates['experiments'])} new)\n"
            for item in sorted(updates['experiments'], key=lambda x: x['date'], reverse=True)[:5]:
                output += f"- **{item['date']}** - {item['client']}: {item['change']}\n"
            output += "\n"

        return output

    except Exception as e:
        return f"*Error getting KB updates: {str(e)}*\n"

def get_impression_share_diagnostic():
    """Get impression share diagnostic findings if today is Nov 12"""
    today = datetime.now().date()
    target_date = datetime(2025, 11, 12).date()
    
    if today != target_date:
        return ""
    
    diagnostic_file = PROJECT_ROOT / 'clients' / 'accessories-for-the-home' / 'audits' / '2025-11-09-pmax-search-is-diagnostic.md'
    friday_pattern_file = PROJECT_ROOT / 'clients' / 'accessories-for-the-home' / 'audits' / '20251109-friday-is-pattern-analysis.json'
    
    if not diagnostic_file.exists():
        return ""
    
    try:
        # Read diagnostic file
        with open(diagnostic_file, 'r') as f:
            content = f.read()
        
        # Check if we have Friday pattern analysis
        friday_dip_found = False
        if friday_pattern_file.exists():
            with open(friday_pattern_file, 'r') as f:
                pattern_data = json.load(f)
                if pattern_data.get('friday_dips_detected', 0) > 0:
                    friday_dip_found = True
        
        output = "## 🔍 Impression Share Diagnostic - Accessories for the Home\n\n"
        output += "**P-Max H&S Unbeast Campaign - Search Impression Share Analysis**\n\n"
        
        if friday_dip_found:
            output += "⚠️ **Key Finding**: Cross-account analysis revealed Friday impression share dips are systematic (11.8pp lower for AFH), suggesting **data reporting delays** rather than actual performance issues.\n\n"
            output += "**Action Required**:\n"
            output += "- Re-check impression share data today (Nov 12) - data should now be fully populated\n"
            output += "- Compare Nov 12 data with Nov 7-9 to confirm if drop was real or reporting delay\n"
            output += "- If IS recovered above 30%: Likely was data delay, continue monitoring\n"
            output += "- If IS still below 30%: Investigate quality score and bid strategy issues\n\n"
        else:
            output += "**Status**: Diagnostic analysis completed. Review findings in audit report.\n\n"
        
        output += f"📄 Full diagnostic: `{diagnostic_file.relative_to(PROJECT_ROOT)}`\n\n"
        
        return output
        
    except Exception as e:
        return f"*Error reading diagnostic: {str(e)}*\n"

def get_recent_audit_status():
    """Check for recent Google Ads audits that need attention"""
    clients_dir = PROJECT_ROOT / 'clients'
    
    if not clients_dir.exists():
        return ""
    
    recent_audits = []
    today = datetime.now().date()
    
    # Check each client folder for recent audit files
    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir():
            continue
        
        audit_dir = client_dir / 'audits'
        if not audit_dir.exists():
            continue
        
        # Look for recent audit index files
        for audit_file in audit_dir.glob('*-audit-index.md'):
            # Check file modification time
            mtime = datetime.fromtimestamp(audit_file.stat().st_mtime).date()
            days_old = (today - mtime).days
            
            if days_old <= 7:  # Last week
                recent_audits.append({
                    'client': client_dir.name,
                    'file': audit_file.name,
                    'days_old': days_old
                })
    
    if not recent_audits:
        return ""
    
    output = "### 🔍 Recent Google Ads Audits\n\n"
    
    if len(recent_audits) == 0:
        return ""
    
    output += f"**{len(recent_audits)} audit(s) generated in last 7 days:**\n\n"
    
    for audit in sorted(recent_audits, key=lambda x: x['days_old'])[:5]:
        age = f"({audit['days_old']} days ago)" if audit['days_old'] > 0 else "(today)"
        output += f"- **{audit['client']}** {age} - [View audits](../clients/{audit['client']}/audits/{audit['file']})\n"
    
    output += "\n💡 *Run audit prompts with Claude Code + Google Ads MCP*\n\n"
    
    return output

def get_agent_status_summary():
    """Get summary of all LaunchAgent statuses"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'scripts'))
        from launchagent_discovery import get_all_agents_with_status
        
        agents = get_all_agents_with_status()
        
        if not agents:
            return ""
        
        # Separate by health status
        healthy = [a for a in agents if a.get('is_healthy', False)]
        unhealthy = [a for a in agents if not a.get('is_healthy', False)]
        critical_unhealthy = [a for a in unhealthy if a.get('critical', False)]
        
        output = "## 🤖 Agent Status\n\n"
        output += f"**{len(healthy)}/{len(agents)} agents healthy**\n\n"
        
        if critical_unhealthy:
            output += f"**⚠️ {len(critical_unhealthy)} critical agent(s) need attention:**\n\n"
            for agent in critical_unhealthy[:5]:  # Show top 5
                output += f"- 🔴 **{agent['name']}**: {agent.get('description', 'N/A')}\n"
            output += "\n"
        
        if unhealthy and len(unhealthy) > len(critical_unhealthy):
            non_critical_unhealthy = [a for a in unhealthy if not a.get('critical', False)]
            if non_critical_unhealthy:
                output += f"**⚪ {len(non_critical_unhealthy)} non-critical agent(s) with issues:**\n\n"
                for agent in non_critical_unhealthy[:3]:  # Show top 3
                    output += f"- ⚪ **{agent['name']}**: {agent.get('description', 'N/A')}\n"
                output += "\n"
        
        if not unhealthy:
            output += "✅ **All agents running correctly**\n\n"
        
        return output
        
    except Exception as e:
        return f"*Agent status unavailable: {str(e)}*\n"

def get_ai_inbox_activity():
    """Get AI inbox processing activity from yesterday"""
    ai_enhanced_dir = PROJECT_ROOT / '!inbox' / 'ai-enhanced'
    processed_dir = PROJECT_ROOT / '!inbox' / 'processed'
    clients_dir = PROJECT_ROOT / 'clients'
    
    if not ai_enhanced_dir.exists():
        return ""
    
    yesterday = get_yesterday_str()
    yesterday_date = datetime.strptime(yesterday, '%Y-%m-%d').date()
    
    # Count enhanced notes processed yesterday
    enhanced_files = list(ai_enhanced_dir.glob('enhanced-*.md'))
    notes_processed = 0
    tasks_created = 0
    duplicates_detected = 0
    completions_routed = 0
    email_drafts_generated = 0
    
    # Check enhanced notes from yesterday
    for file_path in enhanced_files:
        try:
            # Check file modification time
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime).date()
            
            # Include files from yesterday (within 24 hours)
            if file_time == yesterday_date or (datetime.now().date() - file_time).days == 0:
                notes_processed += 1
                
                # Read file to analyze content
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                    # Check for task creation
                    if re.search(r'^task:\s*', content, re.MULTILINE | re.IGNORECASE):
                        tasks_created += 1
                    
                    # Check for duplicate detection
                    if 'DUPLICATE DETECTED' in content or 'is_duplicate' in content.lower():
                        duplicates_detected += 1
                    
                    # Check for completion routing
                    if 'Type:** completion' in content or '**COMPLETION NOTE**' in content:
                        completions_routed += 1
        except Exception as e:
            continue
    
    # Check for email drafts generated yesterday
    for client_dir in clients_dir.iterdir():
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue
        
        drafts_dir = client_dir / 'emails' / 'drafts'
        if drafts_dir.exists():
            for draft_file in drafts_dir.glob('*.md'):
                try:
                    file_time = datetime.fromtimestamp(draft_file.stat().st_mtime).date()
                    if file_time == yesterday_date:
                        email_drafts_generated += 1
                except:
                    continue
    
    # Only show section if there was activity
    if notes_processed == 0:
        return ""
    
    output = "## 📝 AI Inbox Processing (Yesterday)\n\n"
    output += f"**{notes_processed} note(s) processed**\n\n"
    
    if tasks_created > 0:
        output += f"- ✅ **{tasks_created} task(s) created**\n"
    
    if email_drafts_generated > 0:
        output += f"- 📧 **{email_drafts_generated} email draft(s) generated**\n"
    
    if duplicates_detected > 0:
        output += f"- 🔄 **{duplicates_detected} duplicate(s) detected**\n"
    
    if completions_routed > 0:
        output += f"- ✅ **{completions_routed} completion(s) routed** (to documents, not tasks)\n"
    
    if tasks_created == 0 and email_drafts_generated == 0 and duplicates_detected == 0 and completions_routed == 0:
        output += "- *Articles added to knowledge base (no task generation needed)*\n"
    
    output += "\n"
    
    return output

def get_weekly_reports_section():
    """Get weekly Google Ads reports generated in last 7 days with clickable links"""
    state_file = PROJECT_ROOT / 'data' / 'state' / 'weekly-reports-generated.json'

    if not state_file.exists():
        return ""

    try:
        with open(state_file, 'r') as f:
            state = json.load(f)

        # Get reports from last 7 days
        cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
        recent_reports = [
            r for r in state.get('reports', [])
            if r.get('generated_at', '') > cutoff_date
        ]

        if not recent_reports:
            return ""

        # Sort by client name
        recent_reports.sort(key=lambda x: x.get('client', ''))

        # Count total tasks
        total_tasks = sum(r.get('tasks_created', 0) for r in recent_reports)

        # Group by has tasks vs no tasks
        with_tasks = [r for r in recent_reports if r.get('tasks_created', 0) > 0]
        without_tasks = [r for r in recent_reports if r.get('tasks_created', 0) == 0]

        output = f"### 📊 Weekly Google Ads Reports\n\n"
        output += f"**{len(recent_reports)} report(s) generated in last 7 days**\n\n"

        if total_tasks > 0:
            output += f"**{total_tasks} critical task(s) created** from P0 recommendations\n\n"

        # Reports with critical issues
        if with_tasks:
            output += "**🚨 Critical Issues Detected:**\n\n"
            for report in with_tasks:
                html_path_absolute = PROJECT_ROOT / report['html_path']
                file_url = f"file://{html_path_absolute}"
                tasks_str = f"({report['tasks_created']} tasks)" if report['tasks_created'] > 0 else ""
                output += f"- [{report['client']}]({file_url}) {tasks_str} - {report['period']}\n"
            output += "\n"

        # Clean reports
        if without_tasks:
            output += "**✅ No Critical Issues:**\n\n"
            for report in without_tasks:
                html_path_absolute = PROJECT_ROOT / report['html_path']
                file_url = f"file://{html_path_absolute}"
                output += f"- [{report['client']}]({file_url}) - {report['period']}\n"
            output += "\n"

        output += "*💡 Click client name to open full HTML report*\n\n"

        return output

    except Exception as e:
        return f"*Weekly reports unavailable: {str(e)}*\n"

def send_email_briefing(briefing_content, briefing_path):
    """
    Send briefing via Gmail SMTP

    Requires environment variables:
    - GMAIL_USER: Your Gmail address
    - GMAIL_APP_PASSWORD: Gmail app password
    """
    try:
        # Get credentials from Keychain with fallback to environment
        gmail_user = get_secret('GMAIL_USER', fallback_env_var='GMAIL_USER')
        gmail_password = get_secret('GMAIL_APP_PASSWORD', fallback_env_var='GMAIL_APP_PASSWORD')

        if not gmail_user or not gmail_password:
            print("⚠️  Email credentials not configured")
            print("   Set GMAIL_USER and GMAIL_APP_PASSWORD in macOS Keychain or environment variables")
            return False

        # Convert markdown to HTML
        try:
            import markdown
            html_content = markdown.markdown(
                briefing_content,
                extensions=['tables', 'fenced_code']
            )
            # Add basic styling
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                           line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                    h1 {{ color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }}
                    h2 {{ color: #1e40af; margin-top: 30px; }}
                    h3 {{ color: #1e3a8a; }}
                    code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 3px; }}
                    pre {{ background: #f3f4f6; padding: 12px; border-radius: 6px; overflow-x: auto; }}
                    a {{ color: #2563eb; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                    ul {{ padding-left: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #e5e7eb; padding: 8px; text-align: left; }}
                    th {{ background: #f3f4f6; font-weight: 600; }}
                    hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 30px 0; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
        except ImportError:
            styled_html = f"<pre>{briefing_content}</pre>"

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Daily Briefing - {datetime.now().strftime('%A, %B %d, %Y')}"
        msg['From'] = gmail_user
        msg['To'] = gmail_user  # Send to self

        # Attach both plain text and HTML versions
        text_part = MIMEText(briefing_content, 'plain')
        html_part = MIMEText(styled_html, 'html')
        msg.attach(text_part)
        msg.attach(html_part)

        # Send via Gmail SMTP
        print("📧 Sending email via Gmail...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        print(f"✅ Email sent to {gmail_user}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def generate_full_client_work_html():
    """
    Generate full client work section with ALL tasks (no truncation)
    Uses INTERNAL task system (client-tasks.json), not Google Tasks
    Returns HTML string with all P0, P1, P2 tasks expanded
    """
    try:
        # Import task verifier for pre-verification (batched)
        sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'scripts'))
        from task_verifier import batch_pre_verify_tasks, format_verification_for_email

        # Import internal task system
        sys.path.insert(0, str(PROJECT_ROOT / 'shared'))
        from client_tasks_service import ClientTasksService

        # Initialize task service
        task_service = ClientTasksService()

        # Get upcoming tasks (next 7 days) from INTERNAL system
        upcoming_tasks = task_service.get_upcoming_tasks(days=7)

        if not upcoming_tasks:
            return "<p><strong>No tasks due today or in next 7 days</strong></p>"

        # Convert internal tasks to task_dict format for pre-verification
        task_dicts = []
        for task in upcoming_tasks:
            task_dicts.append({
                'title': task.get('title', 'Untitled'),
                'notes': task.get('notes', ''),
                'due': task.get('due_date', ''),  # ISO format YYYY-MM-DD
                'id': task.get('id', '')
            })

        # Batch pre-verify all tasks
        task_dicts = batch_pre_verify_tasks(task_dicts)

        # Extract priority and organize into buckets
        p0_tasks = []
        p1_tasks = []
        p2_tasks = []

        # Map back to original tasks to get priority
        task_id_map = {t['id']: t for t in upcoming_tasks}

        for task_dict in task_dicts:
            task_id = task_dict.get('id', '')
            original_task = task_id_map.get(task_id, {})
            priority = original_task.get('priority', 'P2')

            if priority == 'P0':
                p0_tasks.append(task_dict)
            elif priority == 'P1':
                p1_tasks.append(task_dict)
            else:
                p2_tasks.append(task_dict)

        # Format output as HTML
        html_output = ""
        today = datetime.now().date()

        # Add summary
        total_tasks = len(p0_tasks) + len(p1_tasks) + len(p2_tasks)
        html_output += f"<p><strong>{total_tasks} task(s)</strong> due in next 7 days</p>\n"

        if p0_tasks:
            html_output += "<h3 id='p0-tasks' style='color: #dc2626;'>🔴 URGENT (P0)</h3>\n<ul>\n"
            for task in p0_tasks:
                title = task['title']
                due = task.get('due', '')
                notes = task['notes']

                # Format due date
                due_str = ""
                if due:
                    try:
                        due_date = datetime.fromisoformat(due).date()
                        if due_date != today:
                            due_str = f" <span style='color: #dc2626;'>({due_date.strftime('%b %d')})</span>"
                    except:
                        pass

                html_output += f"<li><strong>{title}</strong>{due_str}"

                # Extract time and reason
                time_match = re.search(r'\*\*Time Estimate:\*\* (.+)', notes)
                reason_match = re.search(r'\*\*Reason:\*\* (.+?)(?:\n|$)', notes)
                if time_match or reason_match:
                    details = []
                    if time_match:
                        details.append(time_match.group(1))
                    if reason_match:
                        details.append(reason_match.group(1))
                    html_output += "<ul style='margin-top: 5px;'>\n"
                    for detail in details:
                        html_output += f"<li>{detail}</li>\n"
                    html_output += "</ul>\n"

                html_output += "</li>\n"
            html_output += "</ul>\n"

        if p1_tasks:
            html_output += "<h3 id='p1-tasks' style='color: #f59e0b;'>🟡 HIGH PRIORITY (P1)</h3>\n<ul>\n"
            for task in p1_tasks:
                title = task['title']
                due = task.get('due', '')
                notes = task['notes']

                # Format due date
                due_str = ""
                if due:
                    try:
                        due_date = datetime.fromisoformat(due).date()
                        if due_date != today:
                            due_str = f" <span style='color: #6b7280;'>({due_date.strftime('%b %d')})</span>"
                    except:
                        pass

                html_output += f"<li><strong>{title}</strong>{due_str}"

                # Extract time and reason
                time_match = re.search(r'\*\*Time Estimate:\*\* (.+)', notes)
                reason_match = re.search(r'\*\*Reason:\*\* (.+?)(?:\n|$)', notes)
                if time_match or reason_match:
                    details = []
                    if time_match:
                        details.append(time_match.group(1))
                    if reason_match:
                        details.append(reason_match.group(1))
                    html_output += "<ul style='margin-top: 5px;'>\n"
                    for detail in details:
                        html_output += f"<li>{detail}</li>\n"
                    html_output += "</ul>\n"

                html_output += "</li>\n"
            html_output += "</ul>\n"

        if p2_tasks:
            html_output += "<h3 id='p2-tasks' style='color: #9ca3af;'>⚪ NORMAL PRIORITY (P2)</h3>\n<ul>\n"
            for task in p2_tasks:
                title = task['title']
                due = task.get('due', '')
                notes = task['notes']

                # Format due date
                due_str = ""
                if due:
                    try:
                        due_date = datetime.fromisoformat(due).date()
                        if due_date != today:
                            due_str = f" <span style='color: #6b7280;'>({due_date.strftime('%b %d')})</span>"
                    except:
                        pass

                html_output += f"<li><strong>{title}</strong>{due_str}"

                # Extract time and reason (but don't expand as much for P2)
                time_match = re.search(r'\*\*Time Estimate:\*\* (.+)', notes)
                if time_match:
                    html_output += f" <span style='color: #6b7280; font-size: 0.9em;'>· {time_match.group(1)}</span>"

                html_output += "</li>\n"
            html_output += "</ul>\n"

        return html_output

    except Exception as e:
        return f"<p><em>Error loading client work: {str(e)}</em></p>"

def generate_full_html_briefing(day_name, calendar_section, client_work_section,
                                  anomalies_section, performance_section, meetings_section,
                                  ai_inbox_section, agent_status_section, audit_section,
                                  is_diagnostic_section, kb_updates_section,
                                  weekly_reports_section):
    """
    Generate a full HTML version of the briefing with ALL tasks expanded (no truncation)
    """
    # Get ALL tasks without truncation
    try:
        sys.path.insert(0, str(PROJECT_ROOT / 'shared'))
        from google_tasks_client import get_all_active_tasks

        active_tasks = get_all_active_tasks()

        if not active_tasks:
            full_tasks_html = "<p><strong>No active tasks in Google Tasks</strong></p>"
        else:
            # Load client names for filtering (same as markdown version)
            client_names = []
            client_folders = PROJECT_ROOT / 'clients'
            if client_folders.exists():
                for client_dir in sorted(client_folders.iterdir()):
                    if client_dir.is_dir() and not client_dir.name.startswith('_'):
                        client_names.append(client_dir.name.lower())
                        display_name = client_dir.name.replace('-', ' ').title()
                        client_names.append(display_name.lower())
                        if 'devonshire' in client_dir.name:
                            client_names.extend(['devonshire', 'devonshire hotels', 'devonshire group'])
                        elif 'national-design-academy' in client_dir.name:
                            client_names.extend(['nda', 'national design academy', 'national design'])
                        elif 'accessories-for-the-home' in client_dir.name:
                            client_names.extend(['accessories for the home', 'accessories', 'uno accessories'])
                        elif 'uno-lighting' in client_dir.name:
                            client_names.extend(['uno lighting', 'uno', 'uno lights'])
                        elif 'just-bin-bags' in client_dir.name:
                            client_names.extend(['just bin bags', 'jbb'])
                        elif 'crowd-control' in client_dir.name:
                            client_names.extend(['crowd control', 'crowdcontrol'])
                        elif 'go-glean' in client_dir.name:
                            client_names.extend(['go glean', 'goglean', 'go clean'])
                        elif 'grain-guard' in client_dir.name:
                            client_names.extend(['grain guard', 'grainguard'])
                        elif 'bright-minds' in client_dir.name:
                            client_names.extend(['bright minds', 'brightminds'])
                        elif 'tree2mydoor' in client_dir.name:
                            client_names.extend(['tree2mydoor', 'tree 2 my door', 'tree to my door'])

            # Add standalone clients
            client_names.extend([
                'nma', 'national motorsports academy', 'national motorsports'
            ])

            # Remove duplicates
            client_names = list(set([c for c in client_names if c and len(c) > 2]))

            # Filter out client tasks (same logic as markdown version)
            personal_only_tasks = []
            for task in active_tasks:
                title = task.get('title', '')
                notes = task.get('notes', '')
                combined = f"{title} {notes}".lower()
                original_title = title

                is_client_task = False

                # Check 1: [Client Name] format
                if original_title.startswith('[') and ']' in original_title:
                    is_client_task = True

                # Check 2: AI-generated task metadata
                if '**Source:** AI Generated' in notes or '**Client:**' in notes:
                    is_client_task = True

                # Check 3: Any client name mentioned
                for client_name in client_names:
                    if not client_name or len(client_name) < 3:
                        continue
                    pattern = r'\b' + re.escape(client_name) + r'\b'
                    if re.search(pattern, combined, re.IGNORECASE):
                        is_client_task = True
                        break

                # Check 4: Multi-client patterns
                multi_client_patterns = [
                    r'\b(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)\s*[&\-]\s*(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)',
                    r'\b(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)\s*,\s*(godshot|crowd control|smythson|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma)',
                ]
                for pattern in multi_client_patterns:
                    if re.search(pattern, combined, re.IGNORECASE):
                        is_client_task = True
                        break

                # Check 5: Colon/dash separator pattern
                client_colon_pattern = r'\b(?:smythson|godshot|crowd control|superspace|tree2mydoor|devonshire|uno lighting|bright minds|go glean|go clean|grain guard|just bin bags|national design academy|national motorsports academy|clear prospects|positive bakes|accessories for the home|nda|nma|accessories|uno)\s*[:\-]\s*'
                if re.search(client_colon_pattern, combined, re.IGNORECASE):
                    is_client_task = True

                if not is_client_task:
                    personal_only_tasks.append(task)

            # Process and categorize personal tasks only
            today = datetime.now().date()
            overdue = []
            due_today = []
            upcoming = []
            no_due = []

            for task in personal_only_tasks:
                priority_score, priority_label = get_task_priority(task)
                task['_priority_score'] = priority_score
                task['_priority_label'] = priority_label
                task['_time_estimate'] = get_time_estimate(task)

                due = task.get('due')
                if due:
                    try:
                        due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                        if due_date < today:
                            overdue.append(task)
                        elif due_date == today:
                            due_today.append(task)
                        else:
                            upcoming.append(task)
                    except:
                        no_due.append(task)
                else:
                    no_due.append(task)

            # Sort by priority
            overdue.sort(key=lambda t: (t.get('_priority_score', 999), t.get('due', '')))
            due_today.sort(key=lambda t: t.get('_priority_score', 999))
            no_due.sort(key=lambda t: t.get('_priority_score', 999))

            full_tasks_html = ""

            if overdue:
                full_tasks_html += "<h3 style='color: #dc2626;'>⚠️ Overdue</h3>\n<ul>\n"
                for task in overdue:
                    title = task.get('title', 'Untitled')
                    priority = task.get('_priority_label', 'P2')
                    time_est = task.get('_time_estimate', '')
                    notes = task.get('notes', '')
                    due = task.get('due', '')

                    meta = f"<strong>{priority}</strong>"
                    if time_est:
                        meta += f" · {time_est}"

                    due_str = ""
                    if due:
                        due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                        due_str = f" <span style='color: #dc2626;'>{due_date.strftime('%b %d')}</span>"

                    full_tasks_html += f"<li>{meta}{due_str}: <strong>{title}</strong>"
                    if notes:
                        lines = [line.strip() for line in notes.split('\n') if line.strip()]
                        skip_patterns = ['#', 'Priority:', '<!--', 'Wispr Flow Note', 'Status:', '**Status:**']
                        details = [line for line in lines if not any(line.startswith(pattern) for pattern in skip_patterns)]
                        if details:
                            full_tasks_html += "<ul style='margin-top: 5px;'>\n"
                            for detail in details[:10]:  # Show up to 10 details
                                full_tasks_html += f"<li>{detail}</li>\n"
                            full_tasks_html += "</ul>\n"
                    full_tasks_html += "</li>\n"
                full_tasks_html += "</ul>\n"

            if due_today:
                full_tasks_html += "<h3 style='color: #2563eb;'>📅 Due Today</h3>\n<ul>\n"
                for task in due_today:
                    title = task.get('title', 'Untitled')
                    priority = task.get('_priority_label', 'P2')
                    time_est = task.get('_time_estimate', '')
                    notes = task.get('notes', '')

                    meta = f"<strong>{priority}</strong>"
                    if time_est:
                        meta += f" · {time_est}"

                    full_tasks_html += f"<li>{meta}: <strong>{title}</strong>"
                    if notes:
                        lines = [line.strip() for line in notes.split('\n') if line.strip()]
                        skip_patterns = ['#', 'Priority:', '<!--', 'Wispr Flow Note', 'Status:', '**Status:**']
                        details = [line for line in lines if not any(line.startswith(pattern) for pattern in skip_patterns)]
                        if details:
                            full_tasks_html += "<ul style='margin-top: 5px;'>\n"
                            for detail in details[:10]:
                                full_tasks_html += f"<li>{detail}</li>\n"
                            full_tasks_html += "</ul>\n"
                    full_tasks_html += "</li>\n"
                full_tasks_html += "</ul>\n"

            if upcoming:
                # Filter to next 7 days
                seven_days_from_now = today + timedelta(days=7)
                upcoming_week = []
                for task in upcoming:
                    due = task.get('due', '')
                    if due:
                        due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                        if due_date <= seven_days_from_now:
                            upcoming_week.append((due_date, task))

                upcoming_week.sort(key=lambda x: x[0])

                if upcoming_week:
                    full_tasks_html += "<h3 style='color: #059669;'>📆 Coming Up (Next 7 Days)</h3>\n<ul>\n"
                    for due_date, task in upcoming_week:
                        title = task.get('title', 'Untitled')
                        priority = task.get('_priority_label', 'P2')
                        time_est = task.get('_time_estimate', '')
                        notes = task.get('notes', '')
                        formatted_date = due_date.strftime('%b %d')

                        meta = f"<strong>{priority}</strong>"
                        if time_est:
                            meta += f" · {time_est}"

                        full_tasks_html += f"<li><strong>{formatted_date}</strong> · {meta}: <strong>{title}</strong>"
                        if notes:
                            lines = [line.strip() for line in notes.split('\n') if line.strip()]
                            skip_patterns = ['#', 'Priority:', '<!--', 'Wispr Flow Note', 'Status:', '**Status:**']
                            details = [line for line in lines if not any(line.startswith(pattern) for pattern in skip_patterns)]
                            if details:
                                full_tasks_html += "<ul style='margin-top: 5px;'>\n"
                                for detail in details[:10]:
                                    full_tasks_html += f"<li>{detail}</li>\n"
                                full_tasks_html += "</ul>\n"
                        full_tasks_html += "</li>\n"
                    full_tasks_html += "</ul>\n"

    except Exception as e:
        full_tasks_html = f"<p><em>Error loading tasks: {str(e)}</em></p>"

    # Generate full client work section (untruncated)
    full_client_work_html = generate_full_client_work_html()

    # Convert markdown sections to HTML (basic conversion)
    import markdown
    calendar_html = markdown.markdown(calendar_section)
    client_work_html = markdown.markdown(client_work_section) if client_work_section else ""
    anomalies_html = markdown.markdown(anomalies_section)
    performance_html = markdown.markdown(performance_section)
    meetings_html = markdown.markdown(meetings_section)
    ai_inbox_html = markdown.markdown(ai_inbox_section) if ai_inbox_section else ""
    agent_status_html = markdown.markdown(agent_status_section) if agent_status_section else ""
    audit_html = markdown.markdown(audit_section) if audit_section else ""
    is_diagnostic_html = markdown.markdown(is_diagnostic_section) if is_diagnostic_section else ""
    kb_updates_html = markdown.markdown(kb_updates_section) if kb_updates_section else ""
    weekly_reports_html = markdown.markdown(weekly_reports_section) if weekly_reports_section else ""

    # Build full HTML document
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Daily Briefing - {day_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        h1 {{
            color: #2563eb;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #1e40af;
            margin-top: 40px;
            border-left: 4px solid #2563eb;
            padding-left: 15px;
        }}
        h3 {{
            color: #1e3a8a;
            margin-top: 25px;
        }}
        ul {{
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 12px;
        }}
        strong {{
            font-weight: 600;
            color: #1a1a1a;
        }}
        hr {{
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 30px 0;
        }}
        .meta {{
            background: #f3f4f6;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .timestamp {{
            color: #6b7280;
            font-style: italic;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>📋 Daily Briefing - {day_name}</h1>
    <p class="timestamp">Full Expanded Version - All Tasks Shown</p>

    <hr>

    {calendar_html}

    <hr>

    <h2>📋 Personal Tasks - DO THESE FIRST</h2>
    {full_tasks_html}

    <hr>

    <h2 id="client-work">🎯 Client Work</h2>
    {full_client_work_html}

    <hr>

    <h2>⚠️ Client Alerts (2-Day Lag)</h2>
    {anomalies_html}

    <hr>

    <h2>📊 Performance Overview</h2>
    {performance_html}

    <hr>

    {kb_updates_html}

    <hr>

    <h2>👥 Recent Meetings</h2>
    {meetings_html}

    <hr>

    {ai_inbox_html}
    {agent_status_html}
    {weekly_reports_html}
    {audit_html}
    {is_diagnostic_html}

    <hr>

    <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p class="timestamp">Next briefing: Tomorrow at 7:00 AM</p>
</body>
</html>
"""

    return html_content

def generate_briefing():
    """Generate the daily briefing"""

    print("Generating Daily Briefing...")
    print()

    # Run client work generator FIRST to ensure fresh data
    print("🎯 Generating client work for today...")
    try:
        import subprocess
        result = subprocess.run(
            ['/usr/local/bin/python3', str(PROJECT_ROOT / 'shared/scripts/daily-client-work-generator.py')],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        if result.returncode != 0:
            print(f"   ⚠️  Client work generator had issues: {result.stderr}")
        else:
            print("   ✓ Client work generated successfully")
    except Exception as e:
        print(f"   ⚠️  Error running client work generator: {e}")

    # Phase 3: Check for and escalate stale tasks
    print("⚡ Checking for priority escalations...")
    try:
        sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'scripts'))
        from task_escalation import escalate_tasks
        
        escalated = escalate_tasks()
        if escalated:
            print(f"   ✓ Escalated {len(escalated)} task(s)")
        else:
            print("   ✓ No tasks need escalation")
    except Exception as e:
        print(f"   ⚠️  Error checking escalations: {e}")

    # Get all sections
    print("📅 Fetching calendar...")
    calendar_section = get_calendar_events()

    print("⚠️  Checking anomalies...")
    anomalies_section = get_recent_anomalies()

    print("🎯 Loading client work...")
    client_work_section = get_client_work_for_today()

    print("📝 Loading tasks...")
    tasks_section = get_pending_tasks()

    print("👥 Checking meetings...")
    meetings_section = get_recent_meeting_notes()

    print("📊 Loading performance data...")
    performance_section = get_weekly_performance_summary()

    print("🔍 Checking for recent audits...")
    audit_section = get_recent_audit_status()

    print("🔍 Checking impression share diagnostic...")
    is_diagnostic_section = get_impression_share_diagnostic()

    print("📝 Checking AI inbox activity...")
    ai_inbox_section = get_ai_inbox_activity()

    print("🤖 Checking agent status...")
    agent_status_section = get_agent_status_summary()

    print("📚 Checking KB updates...")
    kb_updates_section = get_recent_kb_updates()

    print("📊 Checking weekly reports...")
    weekly_reports_section = get_weekly_reports_section()

    # Build briefing content
    today = datetime.now()
    day_name = today.strftime('%A, %B %d, %Y')

    # Generate full HTML version path (for expanded view)
    briefing_html_path = get_briefing_path().with_suffix('.html')
    html_link = f"file://{briefing_html_path}"

    briefing_content = f"""# Daily Briefing - {day_name}

📄 **[View Full Expanded Briefing]({html_link})** (all tasks, no truncation)

---

{calendar_section}

---

## 📋 Personal Tasks - DO THESE FIRST

{tasks_section}

---

{client_work_section}

---

## ⚠️ Client Alerts (2-Day Lag)

{anomalies_section}

---

## 📊 Performance Overview

{performance_section}

---

{kb_updates_section}

---

## 👥 Recent Meetings

{meetings_section}

---

{ai_inbox_section}

{agent_status_section}

{weekly_reports_section}

{audit_section}

{is_diagnostic_section}

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Next briefing: Tomorrow at 7:00 AM*
"""
    
    # Write markdown briefing
    briefing_path = get_briefing_path()
    with open(briefing_path, 'w') as f:
        f.write(briefing_content)

    file_size = briefing_path.stat().st_size / 1024  # KB

    print()
    print("✅ Briefing generated!")
    print(f"📄 File: {briefing_path}")
    print(f"📏 Size: {file_size:.2f} KB")

    # Generate FULL expanded HTML version (no truncation)
    print("📄 Generating full expanded HTML version...")
    full_html_content = generate_full_html_briefing(
        day_name, calendar_section, client_work_section,
        anomalies_section, performance_section, meetings_section,
        ai_inbox_section, agent_status_section, audit_section,
        is_diagnostic_section, kb_updates_section,
        weekly_reports_section
    )

    with open(briefing_html_path, 'w') as f:
        f.write(full_html_content)

    html_size = briefing_html_path.stat().st_size / 1024
    print(f"📄 Full HTML: {briefing_html_path}")
    print(f"📏 Size: {html_size:.2f} KB")
    print()

    # Send email
    email_sent = send_email_briefing(briefing_content, briefing_path)

    if not email_sent:
        print(f"View briefing:")
        print(f"  open {briefing_path}")
        print(f"  open {briefing_html_path}")

    return briefing_path

def should_run_report():
    """
    Determine if the report should run.
    Returns True if:
    - Current time is after 7 AM
    - Today's report hasn't been generated yet (or was generated before 7 AM)
    """
    now = datetime.now()

    # Check if it's after 7 AM
    if now.hour < 7:
        print("⏰ Before 7 AM - skipping report")
        return False

    # Check if today's report already exists
    briefing_path = get_briefing_path()
    if briefing_path.exists():
        # Check when it was last modified
        mtime = datetime.fromtimestamp(briefing_path.stat().st_mtime)

        # If modified today after 7 AM, report already run
        if mtime.date() == now.date() and mtime.hour >= 7:
            print(f"✓ Report already generated today at {mtime.strftime('%H:%M')}")
            return False

    return True

if __name__ == '__main__':
    try:
        if should_run_report():
            generate_briefing()
        else:
            sys.exit(0)  # Exit silently if shouldn't run
    except Exception as e:
        print(f"❌ Error generating briefing: {str(e)}", file=sys.stderr)
        sys.exit(1)

