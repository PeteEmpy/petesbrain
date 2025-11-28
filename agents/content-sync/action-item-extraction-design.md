# Comprehensive Action Item Extraction Design

## Overview

Replace the basic regex-based `extract_action_items()` method with a multi-pass Claude API analysis that catches ALL action items - explicit, implicit, and strategic notes.

## Method Signature

```python
def extract_action_items_comprehensive(self, meeting_data: Dict) -> List[Dict]:
    """
    Extract action items using Claude API multi-pass analysis.

    Returns list of action items with:
    - task: Task text
    - priority: P0 (urgent/today), P1 (this week), P2 (this month), P3 (tracking)
    - due_date: Calculated due date string
    - context: 2-3 sentences of context
    - type: 'action' (for Pete), 'external' (waiting on others), 'strategic' (CONTEXT.md note)
    - meeting_title: Meeting title
    - meeting_date: Meeting date
    """
```

## Claude API Prompt Design

### System Prompt

```
You are an expert task extraction assistant for a Google Ads consultant.
Analyze meeting transcripts to extract ALL action items and commitments.

CRITICAL: These are important client meetings. Do not miss ANY commitments,
whether explicit or implicit.

Extract 3 types of items:

1. **ACTIONS** (for Pete): Tasks Pete committed to do
   - Explicit: "Pete to...", "Pete: [action]", "I'll..."
   - Implicit: "We need to...", "Should...", "Let's..." (when Pete will do it)
   - Verbs: analyze, review, email, update, implement, fix, optimize, check

2. **EXTERNAL** (waiting on others): Tasks assigned to others or dependencies
   - Explicit: "[Name] to...", "[Name]: [action]"
   - Dependencies: "Once [X] happens, then..."
   - Follow-ups: "After [person] sends..."

3. **STRATEGIC** (for CONTEXT.md): Important business context, not tasks
   - Strategic decisions or direction changes
   - Key insights about client business
   - Performance patterns or anomalies
   - Important dates or deadlines

For each item, provide:
- **task**: Clear, actionable task text (start with verb)
- **priority**:
  - P0: Urgent/ASAP/today (words: urgent, ASAP, immediately, today, now)
  - P1: This week (words: this week, soon, shortly, by [day this week])
  - P2: This month (words: this month, by [date this month])
  - P3: Future/tracking (words: next month, eventually, when, after)
- **due_date**: YYYY-MM-DD or "TBD"
- **context**: 2-3 sentences explaining what/why/background
- **type**: "action", "external", or "strategic"

Output as JSON array.
```

### User Prompt Template

```
Meeting Title: {meeting_title}
Meeting Date: {meeting_date}
Attendees: {attendees}

Transcript:
{transcript}

Extract ALL action items, external dependencies, and strategic notes from this meeting.
```

## Implementation Structure

```python
def extract_action_items_comprehensive(self, meeting_data: Dict) -> List[Dict]:
    """Extract action items using Claude API multi-pass analysis."""

    # Get meeting details
    transcript = meeting_data.get('transcript', '') + '\n' + meeting_data.get('full_content', '')
    meeting_title = meeting_data.get('title', 'Untitled Meeting')
    meeting_date = meeting_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    attendees = meeting_data.get('attendees', [])

    # Prepare Claude API request
    system_prompt = """[System prompt text above]"""

    user_prompt = f"""
Meeting Title: {meeting_title}
Meeting Date: {meeting_date}
Attendees: {', '.join(attendees)}

Transcript:
{transcript[:15000]}  # Limit to ~15k chars for haiku context window

Extract ALL action items, external dependencies, and strategic notes from this meeting.
"""

    try:
        # Call Claude API
        response = self.anthropic_client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        # Parse JSON response
        response_text = response.content[0].text
        extracted_items = json.loads(response_text)

        # Filter and format for Google Tasks
        action_items = []
        for item in extracted_items:
            # Only create tasks for Pete's actions (type='action')
            if item.get('type') == 'action':
                action_items.append({
                    'task': item['task'],
                    'priority': item['priority'],
                    'due_date': item.get('due_date', 'TBD'),
                    'context': item.get('context', ''),
                    'meeting_title': meeting_title,
                    'meeting_date': meeting_date
                })

            # Log external dependencies (don't create tasks, just track)
            elif item.get('type') == 'external':
                print(f"  📌 External dependency: {item['task']}")

            # Log strategic notes (add to meeting frontmatter or CONTEXT.md)
            elif item.get('type') == 'strategic':
                print(f"  💡 Strategic note: {item['task']}")

        return action_items

    except Exception as e:
        print(f"⚠️  Claude API extraction failed: {e}")
        print(f"  Falling back to basic regex extraction...")
        # Fall back to original regex method
        return self.extract_action_items_basic(meeting_data)

def extract_action_items_basic(self, meeting_data: Dict) -> List[Dict]:
    """Fallback: Basic regex extraction (renamed from old extract_action_items)."""
    # Original regex-based method as safety fallback
    # ... (existing code from lines 472-527)
```

## Integration Points

1. **Replace call in import_google_doc()** (around line 905):
   ```python
   # OLD:
   # action_items = self.extract_action_items(meeting_data)

   # NEW:
   action_items = self.extract_action_items_comprehensive(meeting_data)
   ```

2. **Update create_google_tasks()** to handle new fields (priority, due_date, context):
   ```python
   def create_google_tasks(self, action_items: List[Dict], client_slug: Optional[str]) -> List[Dict]:
       """Create Google Tasks from action items with priority and due dates."""

       for item in action_items:
           # Build task title with priority
           priority_label = {
               'P0': '[URGENT]',
               'P1': '[HIGH]',
               'P2': '',
               'P3': '[TRACKING]'
           }.get(item.get('priority', 'P2'), '')

           if client_slug:
               title = f"{priority_label} [{client_slug}] {item['task']}"
           else:
               title = f"{priority_label} [Unassigned] {item['task']}"

           # Build notes with context
           notes = f"From: {item['meeting_title']}\n"
           notes += f"Date: {item['meeting_date']}\n"
           if item.get('context'):
               notes += f"\nContext:\n{item['context']}"

           # Calculate due date
           due_date = None
           if item.get('due_date') and item['due_date'] != 'TBD':
               due_date = item['due_date']
           elif item.get('priority') == 'P0':
               # Urgent: due today
               due_date = datetime.now().strftime('%Y-%m-%d')
           elif item.get('priority') == 'P1':
               # High: due end of week (Friday)
               today = datetime.now()
               days_until_friday = (4 - today.weekday()) % 7
               friday = today + timedelta(days=days_until_friday)
               due_date = friday.strftime('%Y-%m-%d')

           # Create task with due date
           task = self.tasks_client.create_task(
               tasklist_id=tasklist_id,
               title=title.strip(),
               notes=notes,
               due=due_date
           )
   ```

3. **Add frontmatter flag** to prevent duplicate generation:
   ```python
   # In save_meeting_file(), add to frontmatter:
   frontmatter['tasks_generated'] = True
   frontmatter['tasks_generated_date'] = datetime.now().isoformat()
   frontmatter['tasks_created_count'] = len(created_tasks)
   ```

4. **Update daily-intel-report.py** to skip flagged meetings:
   ```python
   # Check frontmatter before generating tasks
   if meeting_metadata.get('tasks_generated'):
       print(f"  ⏭️  Skipping {meeting_file} - tasks already generated")
       continue
   ```

## Duplicate Detection Strategy

Before creating each task, check if it already exists in Google Tasks:

```python
def task_already_exists(self, task_title: str, tasklist_id: str) -> bool:
    """Check if task with similar title already exists."""
    existing_tasks = self.tasks_client.list_tasks(tasklist_id, show_completed=False)

    for existing_task in existing_tasks:
        # Normalize titles for comparison
        existing_normalized = existing_task['title'].lower().strip()
        new_normalized = task_title.lower().strip()

        # Check for exact match or high similarity
        if existing_normalized == new_normalized:
            return True

        # Check for substring match (covers "[HIGH]" prefix variations)
        if new_normalized in existing_normalized or existing_normalized in new_normalized:
            return True

    return False

# In create_google_tasks():
if self.task_already_exists(title, tasklist_id):
    print(f"  ⏭️  Skipping duplicate: {title}")
    continue
```

## Safety Mechanisms

1. **Fallback Mode**: If Claude API fails, fall back to basic regex extraction
2. **Confirmation Log**: Print all extracted items before creating tasks
3. **Manual Review Flag**: If >10 items extracted, prompt for review
4. **Duplicate Prevention**: Check Google Tasks before creating
5. **Frontmatter Flag**: Prevent next-day duplicate generation

## Testing Checklist

- [ ] Test with Devonshire meeting (2025-11-13)
- [ ] Verify all 6 explicit action items extracted
- [ ] Verify implicit commitments extracted (if any)
- [ ] Verify urgency detection (ASAP → P0)
- [ ] Verify due date calculation
- [ ] Verify no duplicates created in Google Tasks
- [ ] Verify frontmatter flag added
- [ ] Verify fallback mode works if API fails
- [ ] Test with meeting that has no action items
- [ ] Test with meeting that has >10 action items

## Example Output

For Devonshire meeting, should extract:

```json
[
  {
    "task": "Email Google weekly re: Beeley/Pillsley PMAX integration",
    "priority": "P1",
    "due_date": "2025-11-15",
    "context": "Following up on ongoing Beeley and Pillsley PMAX integration issues. Need to maintain weekly communication with Google support team.",
    "type": "action",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  },
  {
    "task": "Analyze Bolton Abbey location campaign performance (this month)",
    "priority": "P2",
    "due_date": "2025-11-30",
    "context": "Review performance of Bolton Abbey specific location targeting campaigns. Part of monthly location-based performance analysis.",
    "type": "action",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  },
  {
    "task": "Integrate Hide reporting with main campaigns (next month)",
    "priority": "P3",
    "due_date": "2025-12-31",
    "context": "Consolidate Hide property reporting into main Devonshire campaign reporting structure. Scheduled for next month.",
    "type": "action",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  },
  {
    "task": "Provide exact date Hide conversion tracking went live",
    "priority": "P2",
    "due_date": "TBD",
    "context": "Gary to provide the specific date when Hide property's conversion tracking was implemented. Needed for performance analysis baseline.",
    "type": "external",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  },
  {
    "task": "Review budget recommendations email",
    "priority": "P2",
    "due_date": "TBD",
    "context": "Helen to review the budget recommendations email sent by Pete. Client review required before implementation.",
    "type": "external",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  },
  {
    "task": "Analyze Devonshire Fell vs The Fell search volume trends",
    "priority": "P2",
    "due_date": "TBD",
    "context": "CMG team to analyze search volume trends between 'Devonshire Fell' and 'The Fell' brand name variations. Informs keyword strategy.",
    "type": "external",
    "meeting_title": "Devonshire meeting with Helen and Gary",
    "meeting_date": "2025-11-13"
  }
]
```

## File Location

Implementation will modify:
- `/Users/administrator/Documents/PetesBrain/agents/content-sync/granola-google-docs-importer.py`

Design document:
- `/Users/administrator/Documents/PetesBrain/agents/content-sync/action-item-extraction-design.md`
