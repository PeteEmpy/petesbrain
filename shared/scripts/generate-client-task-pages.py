#!/usr/bin/env python3
"""
Generate individual task view HTML pages for all clients.

Creates: clients/[client]/tasks-view.html for each client with tasks

Run: python3 shared/scripts/generate-client-task-pages.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def generate_client_task_page(client_dir, tasks_data):
    """Generate task view HTML for a single client."""

    client_slug = client_dir.name
    tasks = tasks_data.get('tasks', [])

    # Get client display name from CONTEXT.md
    context_file = client_dir / 'CONTEXT.md'
    display_name = client_slug.replace('-', ' ').title()
    if context_file.exists():
        with open(context_file) as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                display_name = first_line[2:].strip()

    # Calculate stats
    active_tasks = [t for t in tasks if t['status'] == 'active']
    completed_tasks = [t for t in tasks if t['status'] == 'completed']

    parent_tasks = [t for t in active_tasks if t['type'] == 'parent']
    child_tasks = [t for t in active_tasks if t['type'] == 'child']
    standalone_tasks = [t for t in active_tasks if t['type'] == 'standalone']

    total_time = sum(t.get('time_estimate_mins') or 0 for t in active_tasks)

    # Group tasks by parent
    tasks_by_parent = defaultdict(list)
    standalone_task_list = []

    for task in active_tasks:
        if task['type'] == 'parent':
            tasks_by_parent[task['id']] = {
                'parent': task,
                'children': []
            }
        elif task['type'] == 'standalone':
            standalone_task_list.append(task)

    # Add children to their parents
    for task in active_tasks:
        if task['type'] == 'child' and task.get('parent_id'):
            parent_id = task['parent_id']
            if parent_id in tasks_by_parent:
                tasks_by_parent[parent_id]['children'].append(task)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{display_name} - Tasks</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Verdana, Geneva, sans-serif;
            font-size: 13px;
            line-height: 1.5;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
        }}

        .logo {{
            position: absolute;
            top: 30px;
            right: 30px;
            width: 120px;
            height: auto;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #6CC24A;
            text-decoration: none;
            font-size: 12px;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        h1 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 5px;
            padding-right: 140px;
        }}

        .subtitle {{
            color: #666;
            font-size: 14px;
            margin-bottom: 25px;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }}

        .stat-box {{
            padding: 15px;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #6CC24A;
        }}

        .stat-label {{
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}

        .stat-value {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }}

        .parent-section {{
            margin-bottom: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .parent-task {{
            background: linear-gradient(135deg, #6CC24A 0%, #5aa838 100%);
            color: white;
            padding: 25px;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
        }}

        .parent-task:hover {{
            background: linear-gradient(135deg, #7dd45b 0%, #6CC24A 100%);
        }}

        .parent-task.expanded {{
            background: linear-gradient(135deg, #5aa838 0%, #4d9630 100%);
        }}

        .expand-icon {{
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 24px;
            transition: transform 0.3s;
        }}

        .parent-task.expanded .expand-icon {{
            transform: translateY(-50%) rotate(180deg);
        }}

        .parent-task h2 {{
            font-size: 18px;
            margin-bottom: 10px;
            padding-right: 40px;
        }}

        .parent-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
            font-size: 12px;
        }}

        .parent-badge {{
            background: rgba(255,255,255,0.3);
            padding: 5px 12px;
            border-radius: 3px;
            font-weight: bold;
        }}

        .parent-notes {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.3);
            font-size: 12px;
            line-height: 1.7;
            white-space: pre-line;
        }}

        .children-container {{
            background: white;
            padding: 20px;
            display: none;
            animation: slideDown 0.3s ease-out;
        }}

        .children-container.expanded {{
            display: block;
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                max-height: 0;
            }}
            to {{
                opacity: 1;
                max-height: 5000px;
            }}
        }}

        .child-task {{
            background: #f9f9f9;
            border-left: 3px solid #ccc;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 3px;
            transition: all 0.2s;
        }}

        .child-task:hover {{
            background: #f0f0f0;
            border-left-color: #6CC24A;
        }}

        .child-task.completed {{
            opacity: 0.6;
            border-left: 3px solid #6CC24A;
            padding: 15px 20px;
            cursor: pointer;
        }}

        .child-task.completed:hover {{
            opacity: 0.8;
        }}

        .child-task.completed .task-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .child-task.completed .task-expand-icon {{
            font-size: 14px;
            color: #6CC24A;
            transition: transform 0.3s;
        }}

        .child-task.completed.expanded-task .task-expand-icon {{
            transform: rotate(180deg);
        }}

        .child-task.completed h4 {{
            text-decoration: line-through;
            color: #6CC24A;
            flex: 1;
        }}

        .child-task.completed .task-details {{
            display: none;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #e0e0e0;
        }}

        .child-task.completed.expanded-task .task-details {{
            display: block;
        }}

        .child-task h4 {{
            font-size: 15px;
            color: #333;
            margin-bottom: 12px;
        }}

        .task-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }}

        .badge {{
            background: #e0e0e0;
            padding: 4px 10px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            color: #555;
        }}

        .badge.priority-p0 {{ background: #ff4444; color: white; }}
        .badge.priority-p1 {{ background: #ff9800; color: white; }}
        .badge.priority-p2 {{ background: #2196F3; color: white; }}
        .badge.priority-p3 {{ background: #9E9E9E; color: white; }}

        .completed-badge {{
            background: #6CC24A;
            color: white;
            padding: 4px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}

        .task-notes {{
            color: #555;
            font-size: 12px;
            line-height: 1.8;
            padding: 15px;
            background: white;
            border-radius: 3px;
            white-space: pre-line;
        }}

        .progress-section {{
            background: white;
            padding: 15px;
            margin-bottom: 20px;
        }}

        .progress-bar {{
            background: #e0e0e0;
            height: 20px;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            background: #6CC24A;
            height: 100%;
            transition: width 0.3s;
        }}

        .standalone-section {{
            margin-top: 30px;
        }}

        .standalone-section h2 {{
            color: #5aa838;
            font-size: 18px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #6CC24A;
        }}

        .no-tasks {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img src="../../shared/assets/branding/roksys-logo-200x50.png" alt="Rok Systems" class="logo">

        <a href="../../shared/tasks-dashboard.html" class="back-link">← Back to Dashboard</a>

        <h1>{display_name} - Tasks</h1>
        <p class="subtitle">Click parent tasks to expand/collapse • Click completed tasks to view details</p>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Total Tasks</div>
                <div class="stat-value">{len(tasks)}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Active</div>
                <div class="stat-value">{len(active_tasks)}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Completed</div>
                <div class="stat-value">{len(completed_tasks)}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Parent Tasks</div>
                <div class="stat-value">{len(parent_tasks)}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Hours</div>
                <div class="stat-value">{round(total_time/60, 1)}</div>
            </div>
        </div>
"""

    if not tasks:
        html += """
        <div class="no-tasks">
            <h2>No tasks found</h2>
            <p style="margin-top: 10px;">Create tasks using ClientTasksService.</p>
        </div>
"""
    else:
        # Render parent tasks with children
        for parent_id, data in sorted(tasks_by_parent.items(), key=lambda x: x[1]['parent'].get('created_at', '')):
            parent = data['parent']
            children = sorted(data['children'], key=lambda t: t.get('due_date') or '9999')

            # Calculate parent progress
            completed_children = [c for c in children if c['status'] == 'completed']
            progress_pct = (len(completed_children) / len(children) * 100) if children else 0

            parent_time = sum(c.get('time_estimate_mins') or 0 for c in children)

            html += f"""
        <div class="parent-section">
            <div class="parent-task" onclick="toggleSection('parent-{parent_id}')">
                <div class="expand-icon">▼</div>
                <h2>{parent['title']}</h2>
                <div class="parent-meta">
                    <span class="parent-badge">{parent.get('priority', 'P2')} Priority</span>
                    <span class="parent-badge">Due: {parent.get('due_date', 'No date')}</span>
                    <span class="parent-badge">{len(children)} child tasks</span>
                    <span class="parent-badge">{round(parent_time/60, 1)} hours total</span>
                    <span class="parent-badge">{len(completed_children)} completed ({progress_pct:.1f}%)</span>
                </div>
"""
            if parent.get('notes'):
                html += f"""
                <div class="parent-notes">{parent['notes']}</div>
"""
            html += """
            </div>

            <div id="parent-{}" class="children-container">
""".format(parent_id)

            if children:
                html += f"""
                <div class="progress-section">
                    <div style="font-size: 12px; color: #666; margin-bottom: 5px;">Project Progress: {len(completed_children)} of {len(children)} child tasks completed</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress_pct:.1f}%;"></div>
                    </div>
                </div>
"""

                # Render children
                child_counter = 0
                for child in children:
                    child_counter += 1
                    is_completed = child['status'] == 'completed'

                    completed_class = " completed" if is_completed else ""
                    checkmark = "✅ " if is_completed else ""

                    if is_completed:
                        completed_time = child.get('completed_at', 'Unknown')
                        if completed_time and completed_time != 'Unknown':
                            try:
                                dt = datetime.fromisoformat(completed_time)
                                completed_time = dt.strftime('%b %d, %Y %H:%M')
                            except:
                                pass

                        html += f"""
                <div class="child-task completed" onclick="toggleCompletedTask(event, 'completed-{parent_id}-{child_counter}')">
                    <div class="task-header">
                        <h4>{checkmark}{child['title']}</h4>
                        <span class="task-expand-icon">▼</span>
                    </div>
                    <div class="task-details" id="completed-{parent_id}-{child_counter}">
                        <div class="task-meta">
                            <span class="completed-badge">COMPLETED</span>
                            <span class="badge priority-{child.get('priority', 'P2').lower()}">{child.get('priority', 'P2')}</span>
                            <span class="badge">Due: {child.get('due_date', 'No date')}</span>
                            <span class="badge">Time: {child.get('time_estimate_mins', 0)} mins</span>
                            <span class="badge">Completed: {completed_time}</span>
                        </div>
"""
                        if child.get('notes'):
                            html += f"""
                        <div class="task-notes">{child['notes']}</div>
"""
                        html += """
                    </div>
                </div>
"""
                    else:
                        html += f"""
                <div class="child-task">
                    <h4>{child['title']}</h4>
                    <div class="task-meta">
                        <span class="badge priority-{child.get('priority', 'P2').lower()}">{child.get('priority', 'P2')}</span>
                        <span class="badge">Due: {child.get('due_date', 'No date')}</span>
                        <span class="badge">Time: {child.get('time_estimate_mins', 0)} mins</span>
                    </div>
"""
                        if child.get('notes'):
                            html += f"""
                    <div class="task-notes">{child['notes']}</div>
"""
                        html += """
                </div>
"""

            html += """
            </div>
        </div>
"""

        # Render standalone tasks
        if standalone_task_list:
            html += """
        <div class="standalone-section">
            <h2>Standalone Tasks</h2>
"""
            for task in sorted(standalone_task_list, key=lambda t: t.get('due_date') or '9999'):
                html += f"""
            <div class="child-task">
                <h4>{task['title']}</h4>
                <div class="task-meta">
                    <span class="badge priority-{task.get('priority', 'P2').lower()}">{task.get('priority', 'P2')}</span>
                    <span class="badge">Due: {task.get('due_date', 'No date')}</span>
                    <span class="badge">Time: {task.get('time_estimate_mins', 0)} mins</span>
                </div>
"""
                if task.get('notes'):
                    html += f"""
                <div class="task-notes">{task['notes']}</div>
"""
                html += """
            </div>
"""
            html += """
        </div>
"""

    html += """
    </div>

    <script>
        function toggleSection(sectionId) {
            const section = document.getElementById(sectionId);
            const parentTask = section.previousElementSibling;

            if (section.classList.contains('expanded')) {
                section.classList.remove('expanded');
                parentTask.classList.remove('expanded');
            } else {
                section.classList.add('expanded');
                parentTask.classList.add('expanded');
            }
        }

        function toggleCompletedTask(event, taskId) {
            event.stopPropagation();
            const taskElement = event.currentTarget;

            if (taskElement.classList.contains('expanded-task')) {
                taskElement.classList.remove('expanded-task');
            } else {
                taskElement.classList.add('expanded-task');
            }
        }
    </script>
</body>
</html>
"""

    return html


def main():
    """Generate task view pages for all clients."""
    print("Generating client task pages...")

    base_path = Path(__file__).parent.parent.parent / 'clients'
    generated_count = 0

    for client_dir in sorted(base_path.iterdir()):
        if not client_dir.is_dir():
            continue
        if client_dir.name.startswith('_'):
            continue

        tasks_file = client_dir / 'tasks.json'
        if not tasks_file.exists():
            continue

        # Read tasks
        with open(tasks_file) as f:
            tasks_data = json.load(f)

        if not tasks_data.get('tasks'):
            continue

        # Generate HTML
        html = generate_client_task_page(client_dir, tasks_data)

        # Write to client directory
        output_path = client_dir / 'tasks-view.html'
        with open(output_path, 'w') as f:
            f.write(html)

        print(f"✅ Generated: {output_path}")
        generated_count += 1

    print(f"\n✅ Generated {generated_count} client task pages")
    print(f"\nTo view dashboard: open shared/tasks-dashboard.html")


if __name__ == '__main__':
    main()
