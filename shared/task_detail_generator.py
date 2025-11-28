#!/usr/bin/env python3
"""
Task Detail HTML Generator

Generates beautiful HTML detail pages for tasks that can be:
- Linked from daily briefing emails
- Linked from Google Task notes
- Opened directly in browser

Usage:
    from shared.task_detail_generator import generate_task_detail_html

    html_path = generate_task_detail_html(
        task_id="abc123",
        task_title="Ring doctor about blood test",
        task_description="Follow up on recent blood test results",
        priority="high",
        urgency="normal",
        estimated_time="15 min",
        task_type="Personal",
        source="Wispr Flow",
        created_date="Nov 17, 2025",
        ai_analysis="This is a follow-up task...",
        original_content="Ring doctor. Re blood test.",
        google_task_id="xyz789",
        wispr_note_id="note-123"
    )
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = PROJECT_ROOT / 'shared' / 'task_detail_template.html'
TASK_DETAILS_DIR = PROJECT_ROOT / 'data' / 'task-details'

def generate_task_detail_html(
    task_id: str,
    task_title: str,
    task_description: str = None,
    priority: str = "medium",
    urgency: str = "normal",
    estimated_time: str = "Unknown",
    task_type: str = "General",
    source: str = "Unknown",
    created_date: str = None,
    created_datetime: str = None,
    ai_analysis: str = None,
    original_content: str = None,
    google_task_id: str = None,
    wispr_note_id: str = None,
    client: str = None,
    client_context: str = None,
    related_tasks: List[str] = None,
    dependencies: List[str] = None,
    processing_history: str = None
) -> Path:
    """
    Generate HTML detail page for a task.

    Returns:
        Path to generated HTML file
    """
    # Ensure task details directory exists
    TASK_DETAILS_DIR.mkdir(parents=True, exist_ok=True)

    # Load template
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")

    with open(TEMPLATE_PATH, 'r') as f:
        template = f.read()

    # Set defaults
    if not created_date:
        created_date = datetime.now().strftime('%b %d, %Y')
    if not created_datetime:
        created_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
    if not ai_analysis:
        ai_analysis = task_description or "No AI analysis available."
    if not original_content:
        original_content = task_description or task_title

    # Priority badge class
    priority_lower = priority.lower()
    priority_class = priority_lower if priority_lower in ['high', 'medium', 'low'] else 'medium'

    # Urgency badge
    if urgency and urgency.lower() in ['urgent', 'time-sensitive']:
        urgency_badge = '<span class="badge badge-urgent">⚡ URGENT</span>'
    else:
        urgency_badge = '<span class="badge badge-low">Normal</span>'

    # Client context section
    client_context_section = ""
    if client and client_context:
        client_context_section = f"""
            <div class="section">
                <div class="section-title">🏢 CLIENT CONTEXT</div>
                <div class="context-box">
                    <strong>Client:</strong> {client}<br><br>
                    {client_context}
                </div>
            </div>
        """

    # Related tasks section
    related_tasks_section = ""
    if related_tasks and len(related_tasks) > 0:
        tasks_html = "\n".join([f'<li>{task}</li>' for task in related_tasks])
        related_tasks_section = f"""
            <div class="section">
                <div class="section-title">🔗 RELATED TASKS</div>
                <ul class="list">
                    {tasks_html}
                </ul>
            </div>
        """

    # Dependencies section
    dependencies_section = ""
    if dependencies and len(dependencies) > 0:
        deps_html = "\n".join([f'<li>{dep}</li>' for dep in dependencies])
        dependencies_section = f"""
            <div class="section">
                <div class="section-title">⚠️ DEPENDENCIES / BLOCKERS</div>
                <ul class="list">
                    {deps_html}
                </ul>
            </div>
        """

    # Google Task ID line
    google_task_id_line = ""
    google_tasks_link = "https://tasks.google.com"
    if google_task_id:
        google_task_id_line = f"<strong>Google Task ID:</strong> {google_task_id}<br>"
        google_tasks_link = f"https://tasks.google.com/task/{google_task_id}"

    # Wispr Note ID line
    wispr_note_id_line = ""
    if wispr_note_id:
        wispr_note_id_line = f"<strong>Wispr Note ID:</strong> {wispr_note_id}<br>"

    # Processing history section
    processing_history_section = ""
    if processing_history:
        processing_history_section = f"""
            <div class="section">
                <div class="section-title">🔄 PROCESSING HISTORY</div>
                <div class="analysis-text">
                    {processing_history}
                </div>
            </div>
        """

    # Replace template variables
    html = template.format(
        task_id=task_id,
        task_title=task_title,
        created_date=created_date,
        source=source,
        priority=priority.capitalize(),
        priority_class=priority_class,
        urgency_badge=urgency_badge,
        estimated_time=estimated_time,
        task_type=task_type,
        ai_analysis=ai_analysis,
        client_context_section=client_context_section,
        related_tasks_section=related_tasks_section,
        dependencies_section=dependencies_section,
        created_datetime=created_datetime,
        google_task_id_line=google_task_id_line,
        wispr_note_id_line=wispr_note_id_line,
        google_tasks_link=google_tasks_link,
        original_content=original_content,
        processing_history_section=processing_history_section
    )

    # Save HTML file
    html_filename = f"{task_id}.html"
    html_path = TASK_DETAILS_DIR / html_filename

    with open(html_path, 'w') as f:
        f.write(html)

    return html_path

def get_task_detail_link(task_id: str) -> str:
    """
    Get file:// URL for task detail page.

    Returns:
        file:// URL that can be used in emails and Google Tasks
    """
    html_path = TASK_DETAILS_DIR / f"{task_id}.html"
    return f"file://{html_path}"

def format_google_task_notes(
    task_description: str,
    task_id: str,
    priority: str = "medium",
    estimated_time: str = "Unknown",
    source: str = "Unknown",
    created_date: str = None
) -> str:
    """
    Format Google Task notes with clickable link to detail page.

    Returns:
        Formatted notes string for Google Task
    """
    if not created_date:
        created_date = datetime.now().strftime('%Y-%m-%d')

    detail_link = get_task_detail_link(task_id)

    notes = f"""{task_description}

Priority: {priority.capitalize()} | Time: {estimated_time}

📊 View full AI analysis:
{detail_link}

Source: {source}
Created: {created_date}"""

    return notes

if __name__ == '__main__':
    # Test the generator
    print("Testing task detail HTML generator...")

    test_path = generate_task_detail_html(
        task_id="test-task-123",
        task_title="Test Task - Ring Doctor",
        task_description="This is a test task to verify the HTML generator works correctly.",
        priority="high",
        urgency="urgent",
        estimated_time="15 min",
        task_type="Personal",
        source="Wispr Flow",
        ai_analysis="This is a high priority task that requires immediate attention. The user needs to contact their doctor regarding recent blood test results.",
        original_content="Ring doctor. Re blood test.",
        related_tasks=["Schedule follow-up appointment", "Review test results"],
        dependencies=["Wait for doctor's office to open"]
    )

    print(f"✓ Generated HTML: {test_path}")
    print(f"✓ File URL: {get_task_detail_link('test-task-123')}")
    print(f"\nOpen in browser:")
    print(f"  open {test_path}")
