#!/usr/bin/env python3
"""
Generate HTML dashboard showing all client tasks across PetesBrain.

Creates:
1. Main dashboard: shared/tasks-dashboard.html (all clients overview)
2. Individual client pages: clients/[client]/tasks-view.html

Run: python3 shared/scripts/generate-tasks-dashboard.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add shared directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from client_tasks_service import ClientTasksService


def get_client_stats():
    """Get statistics for all clients with tasks."""
    service = ClientTasksService()
    base_path = Path(__file__).parent.parent.parent / 'clients'

    client_stats = []

    # Find all clients with tasks.json files
    for client_dir in sorted(base_path.iterdir()):
        if not client_dir.is_dir():
            continue
        if client_dir.name.startswith('_'):  # Skip _templates, _archived, etc.
            continue

        tasks_file = client_dir / 'tasks.json'
        if not tasks_file.exists():
            continue

        # Skip directories without CONTEXT.md (orphaned task directories)
        context_file = client_dir / 'CONTEXT.md'
        if not context_file.exists():
            continue

        # Read tasks for this client
        with open(tasks_file) as f:
            data = json.load(f)

        tasks = data.get('tasks', [])
        if not tasks:
            continue

        # Calculate stats
        total_tasks = len(tasks)
        active_tasks = [t for t in tasks if t['status'] == 'active']
        completed_tasks = [t for t in tasks if t['status'] == 'completed']

        # Count parent/child/standalone
        parent_tasks = [t for t in active_tasks if t['type'] == 'parent']
        child_tasks = [t for t in active_tasks if t['type'] == 'child']
        standalone_tasks = [t for t in active_tasks if t['type'] == 'standalone']

        # Priority breakdown
        priority_counts = defaultdict(int)
        for task in active_tasks:
            priority_counts[task.get('priority', 'P2')] += 1

        # Time estimates (handle None values)
        total_time = sum(t.get('time_estimate_mins') or 0 for t in active_tasks)

        # Overdue tasks
        today = datetime.now().date()
        overdue = []
        for task in active_tasks:
            if task.get('due_date'):
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                if due_date < today:
                    overdue.append(task)

        # Get display name from CONTEXT.md if available
        context_file = client_dir / 'CONTEXT.md'
        display_name = client_dir.name.replace('-', ' ').title()
        if context_file.exists():
            with open(context_file) as f:
                first_line = f.readline().strip()
                if first_line.startswith('# '):
                    display_name = first_line[2:].strip()
                    # Remove common suffixes
                    display_name = display_name.replace(' - Context & Strategic Notes', '')
                    display_name = display_name.replace(' - Context and Strategic Notes', '')

        client_stats.append({
            'slug': client_dir.name,
            'name': display_name,
            'total_tasks': total_tasks,
            'active_count': len(active_tasks),
            'completed_count': len(completed_tasks),
            'parent_count': len(parent_tasks),
            'child_count': len(child_tasks),
            'standalone_count': len(standalone_tasks),
            'p0_count': priority_counts['P0'],
            'p1_count': priority_counts['P1'],
            'p2_count': priority_counts['P2'],
            'p3_count': priority_counts['P3'],
            'total_hours': round(total_time / 60, 1),
            'overdue_count': len(overdue),
            'has_parents': len(parent_tasks) > 0
        })

    return sorted(client_stats, key=lambda x: x['active_count'], reverse=True)


def generate_dashboard_html(client_stats):
    """Generate main dashboard HTML."""

    total_active = sum(c['active_count'] for c in client_stats)
    total_completed = sum(c['completed_count'] for c in client_stats)
    total_hours = sum(c['total_hours'] for c in client_stats)
    total_overdue = sum(c['overdue_count'] for c in client_stats)
    clients_with_tasks = len(client_stats)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PetesBrain - Client Tasks Dashboard</title>
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

        .global-stats {{
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

        .clients-table {{
            margin-top: 20px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #e0e0e0;
        }}

        .table-header {{
            background: linear-gradient(135deg, #6CC24A 0%, #5aa838 100%);
            color: white;
            padding: 15px 20px;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 2fr 1fr;
            gap: 15px;
            font-size: 12px;
            font-weight: bold;
        }}

        .client-row {{
            padding: 15px 20px;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 2fr 1fr;
            gap: 15px;
            align-items: center;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .client-row:hover {{
            background: #f9f9f9;
            border-left: 4px solid #6CC24A;
            padding-left: 16px;
        }}

        .client-row:last-child {{
            border-bottom: none;
        }}

        .client-name {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
        }}

        .client-name:hover {{
            color: #6CC24A;
        }}

        .client-structure {{
            font-size: 12px;
            color: #666;
        }}

        .client-hours {{
            font-size: 12px;
            color: #666;
        }}

        .priority-badges {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }}

        .priority-badge {{
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            color: white;
            min-width: 40px;
            text-align: center;
        }}

        .priority-badge.p0 {{ background: #ff4444; }}
        .priority-badge.p1 {{ background: #ff9800; }}
        .priority-badge.p2 {{ background: #2196F3; }}
        .priority-badge.p3 {{ background: #9E9E9E; }}

        .overdue-badge {{
            background: #ffc107;
            color: #856404;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
        }}

        .no-clients {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}

        .last-updated {{
            text-align: center;
            color: #999;
            font-size: 11px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img src="shared/assets/branding/roksys-logo-200x50.png" alt="Rok Systems" class="logo">

        <h1>PetesBrain - Client Tasks Dashboard</h1>
        <p class="subtitle">Click any row to view client's detailed tasks</p>

        <div class="global-stats">
            <div class="stat-box">
                <div class="stat-label">Clients with Tasks</div>
                <div class="stat-value">{clients_with_tasks}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Active Tasks</div>
                <div class="stat-value">{total_active}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Completed Tasks</div>
                <div class="stat-value">{total_completed}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Hours</div>
                <div class="stat-value">{total_hours}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Overdue Tasks</div>
                <div class="stat-value">{total_overdue}</div>
            </div>
        </div>
"""

    if not client_stats:
        html += """
        <div class="no-clients">
            <h2>No client tasks found</h2>
            <p style="margin-top: 10px;">Create tasks using ClientTasksService or add tasks.json files to client directories.</p>
        </div>
"""
    else:
        html += """
        <div class="clients-table">
            <div class="table-header">
                <div>Client</div>
                <div>Active / Total</div>
                <div>Hours</div>
                <div>Priorities</div>
                <div>Status</div>
            </div>
"""
        for client in client_stats:
            # Task structure info
            structure_parts = []
            if client['parent_count'] > 0:
                structure_parts.append(f"{client['parent_count']}P")
            if client['child_count'] > 0:
                structure_parts.append(f"{client['child_count']}C")
            if client['standalone_count'] > 0:
                structure_parts.append(f"{client['standalone_count']}S")
            structure = " / ".join(structure_parts) if structure_parts else "—"

            # Priority badges
            priority_html = ""
            if any([client['p0_count'], client['p1_count'], client['p2_count'], client['p3_count']]):
                badges = []
                if client['p0_count'] > 0:
                    badges.append(f'<span class="priority-badge p0">P0: {client["p0_count"]}</span>')
                if client['p1_count'] > 0:
                    badges.append(f'<span class="priority-badge p1">P1: {client["p1_count"]}</span>')
                if client['p2_count'] > 0:
                    badges.append(f'<span class="priority-badge p2">P2: {client["p2_count"]}</span>')
                if client['p3_count'] > 0:
                    badges.append(f'<span class="priority-badge p3">P3: {client["p3_count"]}</span>')
                priority_html = "\n".join(badges)

            # Status column
            status_html = ""
            if client['overdue_count'] > 0:
                status_html = f'<span class="overdue-badge">⚠️ {client["overdue_count"]} overdue</span>'
            else:
                status_html = '<span style="color: #6CC24A;">✓ On track</span>'

            html += f"""
            <div class="client-row" onclick="window.location.href='../clients/{client['slug']}/tasks-view.html'">
                <div>
                    <div class="client-name">{client['name']}</div>
                    <div class="client-structure" style="margin-top: 4px; font-size: 11px; color: #999;">
                        {structure}
                    </div>
                </div>
                <div class="client-structure">{client['active_count']} / {client['total_tasks']}</div>
                <div class="client-hours">{client['total_hours']} hrs</div>
                <div class="priority-badges">
                    {priority_html}
                </div>
                <div>
                    {status_html}
                </div>
            </div>
"""

        html += """
        </div>
"""

    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    html += f"""
        <div class="last-updated">
            Last updated: {now}<br>
            Legend: P = Parent tasks, C = Child tasks, S = Standalone tasks
        </div>
    </div>
</body>
</html>
"""

    return html


def main():
    """Generate tasks dashboard."""
    print("Generating tasks dashboard...")

    # Get all client stats
    client_stats = get_client_stats()

    print(f"Found {len(client_stats)} clients with tasks")

    # Generate main dashboard
    dashboard_html = generate_dashboard_html(client_stats)

    # Write to shared/tasks-dashboard.html
    output_path = Path(__file__).parent.parent / 'tasks-dashboard.html'
    with open(output_path, 'w') as f:
        f.write(dashboard_html)

    print(f"✅ Dashboard created: {output_path}")
    print(f"\nTo view: open {output_path}")

    # Note about individual client pages
    print(f"\n💡 Individual client pages need to be generated separately")
    print(f"   Example: clients/national-motorsports-academy/tasks-view.html already exists")


if __name__ == '__main__':
    main()
