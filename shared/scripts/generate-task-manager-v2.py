#!/usr/bin/env python3
"""
⚠️ DEPRECATED/UNUSED: This file appears to be unused (no references found)

This script is not referenced by any LaunchAgents, other scripts, or documentation.
The active task manager generator is: shared/scripts/generate-task-manager.py

Status checked: December 19, 2025
Consider moving to archive or deleting if confirmed unused.

Original purpose:
Task Manager Generator - Enhanced with client tasks by due date
Generates an HTML task manager with:
- Left column: Clients with expandable task lists
- Right column: Both reminders AND client tasks organized by due date with completion buttons
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Add parent directory to path to import shared modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_all_tasks():
    """Load all tasks from client directories"""
    tasks_by_client = {}
    all_reminders = []
    seen_task_ids = set()

    # Load client tasks (including clients/roksys/)
    clients_dir = PROJECT_ROOT / 'clients'
    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        tasks_file = client_dir / 'tasks.json'
        if not tasks_file.exists():
            continue

        try:
            with open(tasks_file, 'r') as f:
                data = json.load(f)

            client_tasks = []

            for task in data.get('tasks', []):
                task_id = task.get('id', '')

                # Skip if we've already seen this task ID
                if task_id and task_id in seen_task_ids:
                    continue

                if task_id:
                    seen_task_ids.add(task_id)

                # Skip completed tasks
                if task.get('status') == 'completed':
                    continue

                # Add client name to task
                task['client'] = client_dir.name
                client_tasks.append(task)

                # Create reminder entry if has due_date
                if task.get('due_date'):
                    reminder = {
                        'id': task_id,
                        'title': task['title'],
                        'due_date': task['due_date'],
                        'client': client_dir.name,
                        'task_data': task
                    }
                    all_reminders.append(reminder)

            if client_tasks:
                # Sort tasks by priority first, then by due_date
                priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
                client_tasks.sort(key=lambda t: (
                    priority_order.get(t.get('priority', 'P2'), 2),
                    t.get('due_date') or '9999-12-31'  # Tasks without due date go to end
                ))
                tasks_by_client[client_dir.name] = client_tasks

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"  ⚠️ Error loading tasks from {client_dir.name}: {e}")
            continue

    return tasks_by_client, all_reminders


def categorize_reminders(all_reminders):
    """Split reminders into today/overdue and upcoming"""
    today = datetime.now().date()
    today_reminders = []
    upcoming_reminders = []

    for reminder in all_reminders:
        try:
            due_date = datetime.strptime(reminder['due_date'], '%Y-%m-%d').date()
            if due_date <= today:
                today_reminders.append(reminder)
            else:
                upcoming_reminders.append(reminder)
        except ValueError:
            upcoming_reminders.append(reminder)

    # Sort by priority first (P0, P1, P2, P3), then by due_date
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}

    def sort_key(reminder):
        priority = reminder.get('task_data', {}).get('priority', 'P2')
        priority_num = priority_order.get(priority, 2)
        return (priority_num, reminder['due_date'])

    today_reminders.sort(key=sort_key)
    upcoming_reminders.sort(key=sort_key)

    return today_reminders, upcoming_reminders


def count_priorities(tasks):
    """Count tasks by priority"""
    counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    for task in tasks:
        priority = task.get('priority', 'P2')
        if priority in counts:
            counts[priority] += 1
    return counts


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def generate_html(tasks_by_client, today_reminders, upcoming_reminders):
    """Generate the Task Manager HTML file with enhanced right panel"""

    # Collect all tasks with due dates for the right panel
    all_tasks_for_dates = []

    # Build client sections HTML
    client_sections = ""
    for client_name in sorted(tasks_by_client.keys()):
        tasks = tasks_by_client[client_name]
        priorities = count_priorities(tasks)
        total = len(tasks)

        client_sections += f'''        <div class="client-section">
            <div class="client-header" onclick="toggleClient('{client_name}')">
                <div class="client-name">{escape_html(client_name)}</div>
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

        # Add tasks for this client
        for task in tasks:
            priority = task.get('priority', 'P2')
            due_date = task.get('due_date') or 'No due date'
            title = escape_html(task.get('title', 'Untitled'))
            task_id = task.get('id')

            # Add task to left panel
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

            # Collect tasks with dates for right panel
            if task.get('due_date') and due_date != 'No due date':
                all_tasks_for_dates.append({
                    'task': task,
                    'client_name': client_name,
                    'task_id': task_id
                })

        client_sections += '''            </div>
        </div>
'''

    # Sort tasks by due date for right panel
    all_tasks_for_dates.sort(key=lambda x: x['task'].get('due_date', '9999-12-31'))
    today_str = datetime.now().strftime('%Y-%m-%d')
    week_from_now = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # Split tasks into categories
    overdue_tasks = []
    today_tasks = []
    this_week_tasks = []
    later_tasks = []

    for task_info in all_tasks_for_dates:
        due_date = task_info['task'].get('due_date', '')
        if due_date < today_str:
            overdue_tasks.append(task_info)
        elif due_date == today_str:
            today_tasks.append(task_info)
        elif due_date <= week_from_now:
            this_week_tasks.append(task_info)
        else:
            later_tasks.append(task_info)

    # Build client tasks by date HTML
    client_tasks_html = ""

    if overdue_tasks:
        client_tasks_html += '''                <div class="date-section">
                    <div class="date-section-title overdue">⚠️ Overdue</div>
'''
        for task_info in overdue_tasks:
            task = task_info['task']
            client = escape_html(task_info['client_name'])
            title = escape_html(task.get('title', 'Untitled'))
            priority = task.get('priority', 'P2')
            due_date = task.get('due_date')
            task_id = task_info['task_id']

            client_tasks_html += f'''                    <div class="date-task priority-{priority}">
                        <div class="date-task-content" onclick="openTaskModal('{task_id}')">
                            <div class="date-task-title">{title}</div>
                            <div class="date-task-meta">
                                <span class="task-priority-badge">{priority}</span>
                                <span>{due_date} • {client}</span>
                            </div>
                        </div>
                        <button class="date-task-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓</button>
                    </div>
'''
        client_tasks_html += '''                </div>
'''

    if today_tasks:
        client_tasks_html += '''                <div class="date-section">
                    <div class="date-section-title today">📅 Due Today</div>
'''
        for task_info in today_tasks:
            task = task_info['task']
            client = escape_html(task_info['client_name'])
            title = escape_html(task.get('title', 'Untitled'))
            priority = task.get('priority', 'P2')
            due_date = task.get('due_date')
            task_id = task_info['task_id']

            client_tasks_html += f'''                    <div class="date-task priority-{priority}">
                        <div class="date-task-content" onclick="openTaskModal('{task_id}')">
                            <div class="date-task-title">{title}</div>
                            <div class="date-task-meta">
                                <span class="task-priority-badge">{priority}</span>
                                <span>{client}</span>
                            </div>
                        </div>
                        <button class="date-task-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓</button>
                    </div>
'''
        client_tasks_html += '''                </div>
'''

    if this_week_tasks:
        client_tasks_html += '''                <div class="date-section">
                    <div class="date-section-title">📆 This Week</div>
'''
        for task_info in this_week_tasks[:15]:  # Limit to 15 to avoid overflow
            task = task_info['task']
            client = escape_html(task_info['client_name'])
            title = escape_html(task.get('title', 'Untitled'))
            priority = task.get('priority', 'P2')
            due_date = task.get('due_date')
            task_id = task_info['task_id']

            client_tasks_html += f'''                    <div class="date-task priority-{priority}">
                        <div class="date-task-content" onclick="openTaskModal('{task_id}')">
                            <div class="date-task-title">{title}</div>
                            <div class="date-task-meta">
                                <span class="task-priority-badge">{priority}</span>
                                <span>{due_date} • {client}</span>
                            </div>
                        </div>
                        <button class="date-task-complete" onclick="event.stopPropagation(); quickCompleteTask(event, '{task_id}')">✓</button>
                    </div>
'''
        client_tasks_html += '''                </div>
'''

    if not (overdue_tasks or today_tasks or this_week_tasks):
        client_tasks_html = '''                <div class="no-reminders">No tasks with due dates</div>
'''

    # Build today reminders HTML (legacy format)
    today_html = ""
    if today_reminders:
        for reminder in today_reminders:
            title = escape_html(reminder['title'])
            due_date = reminder['due_date']
            client = escape_html(reminder['client'])
            task_id = reminder['id']
            status = "OVERDUE" if datetime.strptime(due_date, '%Y-%m-%d').date() < datetime.now().date() else "DUE TODAY"

            today_html += f'''            <div class="reminder-item reminder-{status.lower().replace(' ', '-')}" onclick="jumpToTask('{task_id}', '{escape_html(reminder['client'])}')">
                <div class="reminder-status">{status}</div>
                <div class="reminder-title">{title}</div>
                <div class="reminder-meta">{due_date} • {client}</div>
            </div>
'''
    else:
        today_html = '            <div class="no-reminders">No overdue or due today</div>\n'

    # Build upcoming reminders HTML (legacy format)
    upcoming_html = ""
    if upcoming_reminders:
        for reminder in upcoming_reminders[:20]:  # Limit to 20 upcoming
            title = escape_html(reminder['title'])
            due_date = reminder['due_date']
            client = escape_html(reminder['client'])
            task_id = reminder['id']

            upcoming_html += f'''            <div class="reminder-item reminder-upcoming" onclick="jumpToTask('{task_id}', '{escape_html(reminder['client'])}')">
                <div class="reminder-title">{title}</div>
                <div class="reminder-meta">{due_date} • {client}</div>
            </div>
'''
    else:
        upcoming_html = '            <div class="no-reminders">No upcoming reminders</div>\n'

    # Build task data JSON for modal - all tasks by ID
    all_tasks_by_id = {}
    for client_tasks in tasks_by_client.values():
        for task in client_tasks:
            task_id = task.get('id')
            if task_id:
                all_tasks_by_id[task_id] = task

    task_data_json = json.dumps(all_tasks_by_id, indent=4)
    # Combine reminders back together for JavaScript
    all_reminders = today_reminders + upcoming_reminders
    reminder_data_json = json.dumps(all_reminders, indent=4)

    # Generate the complete HTML
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetesBrain - Task Manager & Reminders</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 12px;
        }}
        .nav-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .nav-btn {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 13px;
        }}
        .nav-btn:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }}
        #process-notes-btn {{
            display: none;
            background: #28a745;
            border-color: #28a745;
        }}
        #process-notes-btn:hover {{
            background: #218838;
        }}
        .content-wrapper {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .clients-column {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-height: 700px;
            overflow-y: auto;
        }}
        .client-section {{
            margin-bottom: 12px;
        }}
        .client-header {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }}
        .client-header:hover {{
            background: #e9ecef;
        }}
        .client-name {{
            font-weight: 600;
            color: #495057;
            font-size: 14px;
        }}
        .client-stats {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
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
            background: #fafafa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            max-height: 700px;
            overflow-y: auto;
            position: sticky;
            top: 20px;
        }}
        .reminders-title {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #6c757d;
        }}
        .client-tasks-section {{
            background: white;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 15px;
        }}
        .client-tasks-title {{
            font-size: 13px;
            font-weight: 700;
            color: #495057;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #dee2e6;
        }}
        .date-section {{
            margin-bottom: 15px;
        }}
        .date-section-title {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 8px;
        }}
        .date-section-title.overdue {{
            color: #dc3545;
        }}
        .date-section-title.today {{
            color: #ffc107;
        }}
        .date-task {{
            background: white;
            padding: 8px;
            margin-bottom: 6px;
            border-radius: 4px;
            border-left: 3px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }}
        .date-task:hover {{
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            transform: translateX(2px);
        }}
        .date-task.priority-P0 {{
            border-left-color: #dc3545;
        }}
        .date-task.priority-P1 {{
            border-left-color: #ffc107;
        }}
        .date-task.priority-P2 {{
            border-left-color: #28a745;
        }}
        .date-task.priority-P3 {{
            border-left-color: #6c757d;
        }}
        .date-task-content {{
            flex: 1;
            cursor: pointer;
        }}
        .date-task-title {{
            font-weight: 600;
            color: #333;
            font-size: 12px;
            margin-bottom: 3px;
        }}
        .date-task-meta {{
            font-size: 10px;
            color: #666;
            display: flex;
            gap: 6px;
        }}
        .task-priority-badge {{
            background: #f0f0f0;
            padding: 1px 4px;
            border-radius: 2px;
            font-weight: 600;
        }}
        .date-task-complete {{
            background: #28a745;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
            opacity: 0;
        }}
        .date-task:hover .date-task-complete {{
            opacity: 1;
        }}
        .date-task-complete:hover {{
            background: #218838;
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
            cursor: pointer;
            transition: all 0.2s;
        }}
        .reminder-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transform: translateX(2px);
            background: #f9f9f9;
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
            justify-content: center;
            align-items: center;
        }}
        .modal-content {{
            background: white;
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        .modal-header {{
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 18px;
            font-weight: 600;
        }}
        .modal-body {{
            padding: 20px;
            flex: 1;
            overflow-y: auto;
        }}
        .note-section {{
            padding: 15px 20px;
            border-top: 1px solid #e0e0e0;
            background: #f8f9fa;
        }}
        .note-label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #495057;
            font-size: 13px;
        }}
        .note-textarea {{
            width: 100%;
            min-height: 80px;
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
            resize: vertical;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .note-textarea:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        .modal-buttons {{
            padding: 15px 20px;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }}
        .modal-btn {{
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .modal-btn-cancel {{
            background: #e9ecef;
            color: #495057;
        }}
        .modal-btn-cancel:hover {{
            background: #dee2e6;
        }}
        .modal-btn-complete {{
            background: #28a745;
            color: white;
        }}
        .modal-btn-complete:hover {{
            background: #218838;
        }}
        .modal-btn-save {{
            background: #667eea;
            color: white;
        }}
        .modal-btn-save:hover {{
            background: #5969d8;
        }}
        .task-detail-label {{
            font-weight: 600;
            color: #6c757d;
            font-size: 12px;
            text-transform: uppercase;
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
            <div class="nav-buttons">
                <button class="nav-btn" onclick="window.open('tasks-overview-priority.html', '_blank')">🎯 Priority View</button>
                <button class="nav-btn" onclick="window.open('tasks-overview.html', '_blank')">👥 Client View</button>
                <button class="nav-btn" onclick="toggleAllClients()">⚡ Toggle All</button>
                <button class="nav-btn" onclick="hardRefresh()">🔄 Hard Refresh</button>
                <button class="nav-btn" onclick="refreshTaskManager()">♻️ Regenerate</button>
                <button class="nav-btn" id="process-notes-btn" onclick="processAllNotes()">📋 Process Notes</button>
            </div>
        </div>

        <div class="content-wrapper">
            <div class="clients-column">
{client_sections}
            </div>

            <div class="reminders-column">
                <div class="reminders-title">📌 Client Tasks & Reminders</div>

                <div class="client-tasks-section">
                    <div class="client-tasks-title">📋 Client Tasks by Due Date</div>
{client_tasks_html}
                </div>

                <div class="reminders-section">
                    <div class="reminders-section-title">Today & Overdue</div>
{today_html}
                </div>

                <div class="reminders-section">
                    <div class="reminders-section-title">Upcoming</div>
{upcoming_html}
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
const TASK_DATA = {task_data_json};
const REMINDER_DATA = {reminder_data_json};

function toggleClient(clientName) {{
    console.log('Toggling client:', clientName);
    const elementId = 'client-' + clientName;
    console.log('Looking for element:', elementId);
    const content = document.getElementById(elementId);
    if (content) {{
        console.log('Found element, toggling expanded class');
        content.classList.toggle('expanded');
    }} else {{
        console.log('Element not found!');
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

function hardRefresh() {{
    location.reload(true);
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

    // Scroll to the client section
    const clientSection = document.querySelector('div.client-header');
    if (clientSection) {{
        clientSection.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
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
        client: task.client || 'unknown',
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
        client: task.client || 'unknown',
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
        client: task.client || 'unknown',
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
            const taskElement = event.target.closest('.task, .date-task');
            if (taskElement) {{
                taskElement.style.opacity = '0.5';
                taskElement.style.backgroundColor = '#e8f5e9';
            }}
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
        const response = await fetch('http://localhost:5002/regenerate');
        const data = await response.json();

        if (data.status === 'success') {{
            // Wait a moment then reload the page
            setTimeout(() => {{
                location.reload();
            }}, 500);
        }} else {{
            alert('Error refreshing task manager: ' + data.message);
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

    return html_content


def main():
    """Main execution"""
    print("Regenerating Task Manager (Enhanced Version)...")

    tasks_by_client, all_reminders = load_all_tasks()
    today_reminders, upcoming_reminders = categorize_reminders(all_reminders)
    html = generate_html(tasks_by_client, today_reminders, upcoming_reminders)

    # Write to file
    output_file = PROJECT_ROOT / 'tasks-manager-v2.html'
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"\n✅ Generated tasks-manager-v2.html")
    print(f"   Total clients: {len(tasks_by_client)}")
    print(f"   Total tasks: {sum(len(tasks) for tasks in tasks_by_client.values())}")
    print(f"   Total reminders: {len(all_reminders)}")
    print(f"   - Today/Overdue: {len(today_reminders)}")
    print(f"   - Upcoming: {len(upcoming_reminders)}")
    print(f"   Output: {output_file}")


if __name__ == '__main__':
    main()