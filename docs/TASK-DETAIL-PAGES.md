# Task Detail Pages - Clickable Rich Context

**Status:** ✅ Implemented and Working  
**Date:** Nov 17, 2025

## Overview

Task detail pages provide rich AI analysis and context for every task, accessible via clickable links from:
1. Google Tasks (click link in notes)
2. Daily briefing email (coming soon)
3. Direct file access

## How It Works

### 1. HTML Detail Pages

**Location:** `data/task-details/{task-id}.html`

**Features:**
- Beautiful gradient header with task title
- Quick info grid (priority, urgency, time, type)
- AI analysis section
- Client context (if applicable)
- Related tasks
- Dependencies/blockers
- Expandable full details
- Action buttons (mark complete, open in Google Tasks, print)

**Example:**
```
file:///Users/administrator/Documents/PetesBrain/data/task-details/f5172de3c52d.html
```

### 2. Google Tasks Integration

When tasks are created, the notes field includes:

```
Follow up with doctor regarding recent blood test results.

Priority: High | Time: 15 min

📊 View full AI analysis:
file:///Users/administrator/Documents/PetesBrain/data/task-details/f5172de3c52d.html

Source: Wispr Flow
Created: 2025-11-16
```

**To view:** Click the `file://` link in Google Tasks

### 3. Your Existing Tasks

✅ **Already updated** (Nov 17, 2025):
- "Ring doctor - Re blood test" → [f5172de3c52d.html]
- "Sort the hose out" → [0d0ffbc17a34.html]

## Usage Examples

### From Google Tasks
1. Open Google Tasks app/web
2. Click on any task
3. Look for "📊 View full AI analysis" link in notes
4. Click to open rich detail page in browser

### Direct Access
```bash
# Open task detail pages directory
open /Users/administrator/Documents/PetesBrain/data/task-details/

# Open specific task
open /Users/administrator/Documents/PetesBrain/data/task-details/f5172de3c52d.html
```

### Programmatic Access
```python
from shared.task_detail_generator import (
    generate_task_detail_html,
    get_task_detail_link,
    format_google_task_notes
)

# Generate HTML page
html_path = generate_task_detail_html(
    task_id="abc123",
    task_title="Example Task",
    task_description="Task description",
    priority="high",
    estimated_time="30 min",
    ai_analysis="AI analysis here..."
)

# Get clickable link
link = get_task_detail_link("abc123")
# Returns: file:///Users/administrator/Documents/PetesBrain/data/task-details/abc123.html

# Format Google Task notes with link
notes = format_google_task_notes(
    task_description="Task description",
    task_id="abc123",
    priority="high",
    estimated_time="30 min",
    source="Wispr Flow"
)
```

## Architecture

```
Wispr Flow Note
      ↓
Inbox (!inbox/)
      ↓
AI Inbox Processor (future)
      ↓
┌─────────────────────┬──────────────────────┐
│ Google Task Created │ HTML Page Generated  │
│ with clickable link │ (data/task-details/) │
└─────────────────────┴──────────────────────┘
      ↓                         ↓
Daily Briefing Email    Click link → Browser
      ↓
Click task → Browser
```

## What's Working Now

✅ **HTML Template System**
- Beautiful gradient design
- Responsive layout
- Collapsible details
- Print-friendly

✅ **Python Generator**
- `shared/task_detail_generator.py`
- Easy to use API
- Automatic ID generation
- Link formatting

✅ **Google Tasks Integration**
- Links in task notes
- Working on your two Wispr tasks
- Ready for all future tasks

✅ **Wispr Flow Integration**
- Timestamp boundary bug fixed
- Importer runs every 30 min
- Notes processed correctly

## What's Next (Optional Enhancements)

### Phase 2: Daily Briefing Email Links
- Update daily briefing to link to HTML pages (instead of Google Tasks)
- Keep email concise, detail on-demand via clicks

### Phase 3: AI Inbox Processor Auto-Generation
- Auto-generate HTML when AI processes inbox
- Include richer context from AI analysis
- Duplicate detection results

### Phase 4: Interactive Features
- Mark complete button (integrates with Google Tasks API)
- Snooze functionality
- Edit task inline
- Add comments/notes

## Files Modified

**New Files:**
- `shared/task_detail_template.html` - HTML template
- `shared/task_detail_generator.py` - Python generator
- `docs/TASK-DETAIL-PAGES.md` - This document

**Modified Files:**
- `agents/wispr-flow-importer/wispr-flow-importer.py` - Fixed timestamp bug (>= instead of >)
- `agents/inbox-processor/inbox-processor.py` - Fixed NoneType error

**Generated Files:**
- `data/task-details/test-task-123.html` - Test file
- `data/task-details/f5172de3c52d.html` - Ring doctor task
- `data/task-details/0d0ffbc17a34.html` - Hose task

## Testing

Test task created and working:
```bash
python3 shared/task_detail_generator.py
open data/task-details/test-task-123.html
```

Your real tasks updated:
- Google Tasks "Ring doctor" and "Sort the hose" now have clickable links
- HTML pages generated and accessible
- Browser opens correctly when clicked

## Key Benefits

1. **Not Overwhelming**: Email stays concise, details on-demand
2. **Rich Context**: All AI analysis available when you need it
3. **Multiple Access Points**: Email, Google Tasks, or direct file
4. **Beautiful Presentation**: Professional gradient design
5. **Offline Access**: HTML files work without internet
6. **Searchable**: All details in one place
7. **Expandable**: Easy to add more features later

## Support

**Questions?** Ask Claude Code:
- "Show me the HTML for task X"
- "Generate detail page for this task"
- "Update Google Task with clickable link"

**Troubleshooting:**
- If links don't work: Check file:// URLs are correct
- If HTML doesn't load: Verify file exists in data/task-details/
- If formatting breaks: Check template file for errors
