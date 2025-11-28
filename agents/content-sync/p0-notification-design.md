# P0 Task Email Notification Design

## Problem

When meetings are automatically imported and analyzed, P0 (urgent) tasks may be created without the user knowing immediately. This defeats the purpose of urgency categorization.

## Solution

Send an email notification immediately when P0 tasks are created from meetings.

## Email Format

**Subject:** `⚠️ URGENT Task Created from Meeting: [Meeting Title]`

**Body:**
```
URGENT TASK ALERT

A high-priority P0 task was created from your meeting:

Meeting: [Meeting Title]
Date: [Meeting Date]
Attendees: [Attendees list]

🔴 URGENT TASK:
[Task Title]

Due: TODAY
Client: [Client Name]
Context: [2-3 sentence context]

---

This task requires immediate attention and has been added to your Google Tasks.

View all tasks in priority order: /tmp/tasks-priority-view-YYYY-MM-DD.html
Or run: "view tasks" in Claude Code
```

## Implementation

### 1. Add Email Notification to Granola Importer

In `granola-google-docs-importer.py`, after creating tasks:

```python
def send_p0_notification(self, p0_tasks: List[Dict], meeting_data: Dict):
    """Send email notification for P0 tasks"""
    if not p0_tasks:
        return

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Email config (use environment variables)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('GMAIL_USER')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    recipient_email = sender_email  # Send to self

    if not sender_email or not sender_password:
        print("  ⚠️  Email credentials not configured - skipping P0 notification")
        return

    # Build email
    subject = f"⚠️ URGENT Task Created from Meeting: {meeting_data['title']}"

    body = f"""URGENT TASK ALERT

A high-priority P0 task was created from your meeting:

Meeting: {meeting_data['title']}
Date: {meeting_data['date']}
Attendees: {', '.join(meeting_data.get('attendees', []))}

"""

    for task in p0_tasks:
        body += f"""
🔴 URGENT TASK:
{task['task']}

Due: TODAY
Client: {task.get('client', 'N/A')}
Context: {task.get('context', 'No context provided')[:200]}...

"""

    body += """
---

These tasks require immediate attention and have been added to your Google Tasks.

View all tasks in priority order by running "view tasks" in Claude Code.
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"  ✅ P0 notification email sent for {len(p0_tasks)} urgent task(s)")
    except Exception as e:
        print(f"  ⚠️  Failed to send P0 notification: {e}")

# In import_google_doc(), after creating tasks:
if created_action_tasks:
    p0_tasks = [t for t in action_items if t.get('priority') == 'P0']
    if p0_tasks:
        self.send_p0_notification(p0_tasks, meeting_data)
```

### 2. Alternative: macOS Notification

For instant visibility without email:

```python
def send_macos_notification(self, p0_tasks: List[Dict], meeting_title: str):
    """Send macOS notification for P0 tasks"""
    import subprocess

    for task in p0_tasks:
        title = "⚠️ URGENT Task from Meeting"
        message = f"{task['task']}\n\nFrom: {meeting_title}"

        # Use macOS osascript to show notification
        script = f'''
        display notification "{message}" with title "{title}" sound name "Basso"
        '''

        try:
            subprocess.run(['osascript', '-e', script])
        except Exception as e:
            print(f"  ⚠️  Failed to send notification: {e}")
```

### 3. Both Options

Ideally, send both:
- **macOS Notification**: Immediate pop-up (if at computer)
- **Email**: Persistent record (if away from computer)

## Configuration

Add to environment variables:
```bash
export GMAIL_USER="petere@roksys.co.uk"
export GMAIL_APP_PASSWORD="your-app-password"  # Already set
```

## Testing

Run with Devonshire meeting:
```bash
ANTHROPIC_API_KEY="..." \
GMAIL_USER="petere@roksys.co.uk" \
GMAIL_APP_PASSWORD="..." \
python3 agents/content-sync/test-devonshire-extraction.py
```

Should send email if P0 tasks detected.

## Benefits

✅ **Immediate awareness** of urgent tasks
✅ **No missed commitments** from meetings
✅ **Persistent record** (email saved in inbox)
✅ **Works remotely** (email reaches you anywhere)

## Future Enhancement

- Send summary at end of day: "You have X urgent P0 tasks outstanding"
- Send reminder if P0 task not completed by end of day
- Integrate with macOS Focus modes (no notifications during meetings)
