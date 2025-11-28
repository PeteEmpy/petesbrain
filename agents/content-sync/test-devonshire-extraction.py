#!/usr/bin/env python3
"""
Test comprehensive action item extraction with Devonshire meeting.

This script simulates the extraction process without creating actual Google Tasks.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
import anthropic

# Setup
MEETING_FILE = Path("/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/meeting-notes/2025-11-13-devonshire-meeting-with-helen-and-gary.md")
API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not API_KEY:
    print("❌ ANTHROPIC_API_KEY not set")
    exit(1)

# Read meeting file
print(f"📄 Reading: {MEETING_FILE.name}\n")

with open(MEETING_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse frontmatter and content
if content.startswith('---'):
    parts = content.split('---', 2)
    if len(parts) >= 3:
        transcript = parts[2].strip()
    else:
        transcript = content
else:
    transcript = content

# Prepare extraction request
meeting_data = {
    'title': '2025-11-13 Devonshire meeting with Helen and Gary',
    'date': '2025-11-13',
    'attendees': ['Peter', 'Helen', 'Gary']
}

system_prompt = """You are an expert task extraction assistant for a Google Ads consultant.
Analyze meeting transcripts to extract ALL action items and commitments.

CRITICAL: These are important client meetings. Do not miss ANY commitments,
whether explicit or implicit.

Extract 3 types of items:

1. **ACTIONS** (for Pete): Tasks Pete committed to do
   - Explicit: "Pete to...", "Pete: [action]", "I'll...", "I will..."
   - Implicit: "We need to...", "Should...", "Let's..." (when Pete will do it)
   - Verbs: analyze, review, email, update, implement, fix, optimize, check, send, create

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
- **task**: Clear, actionable task text (start with verb for actions)
- **priority**:
  - P0: Urgent/ASAP/today (words: urgent, ASAP, immediately, today, now)
  - P1: This week (words: this week, soon, shortly, by [day this week])
  - P2: This month (words: this month, by [date this month])
  - P3: Future/tracking (words: next month, eventually, when, after)
- **due_date**: YYYY-MM-DD or "TBD"
- **context**: 2-3 sentences explaining what/why/background
- **type**: "action", "external", or "strategic"

Output ONLY valid JSON array with no markdown formatting or code blocks. Start with [ and end with ]."""

user_prompt = f"""Meeting Title: {meeting_data['title']}
Meeting Date: {meeting_data['date']}
Attendees: {', '.join(meeting_data['attendees'])}

Transcript:
{transcript[:15000]}

Extract ALL action items, external dependencies, and strategic notes from this meeting."""

print("🤖 Analyzing with Claude API...\n")

# Call Claude API
client = anthropic.Anthropic(api_key=API_KEY)

response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=2000,
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": user_prompt
    }]
)

# Parse response
response_text = response.content[0].text.strip()

# Remove markdown code blocks if present
if response_text.startswith('```'):
    response_text = re.sub(r'^```(?:json)?\n', '', response_text)
    response_text = re.sub(r'\n```$', '', response_text)

try:
    extracted_items = json.loads(response_text)
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse response as JSON: {e}")
    print(f"\nResponse was:\n{response_text[:500]}...")
    exit(1)

# Display results
print(f"✅ Extracted {len(extracted_items)} items\n")
print("=" * 80)

actions = []
external = []
strategic = []

for item in extracted_items:
    if item.get('type') == 'action':
        actions.append(item)
    elif item.get('type') == 'external':
        external.append(item)
    elif item.get('type') == 'strategic':
        strategic.append(item)

# Display actions (will become tasks)
if actions:
    print(f"\n📋 ACTIONS FOR PETE ({len(actions)} tasks would be created):\n")
    for i, item in enumerate(actions, 1):
        priority = item.get('priority', 'P2')
        task = item.get('task', '')
        due = item.get('due_date', 'TBD')
        context = item.get('context', '')

        print(f"{i}. [{priority}] {task}")
        print(f"   Due: {due}")
        print(f"   Context: {context[:100]}...")
        print()

# Display external dependencies
if external:
    print(f"\n📌 EXTERNAL DEPENDENCIES ({len(external)} items logged):\n")
    for i, item in enumerate(external, 1):
        print(f"{i}. {item.get('task', '')}")
        print(f"   Context: {item.get('context', '')[:100]}...")
        print()

# Display strategic notes
if strategic:
    print(f"\n💡 STRATEGIC NOTES ({len(strategic)} items for CONTEXT.md):\n")
    for i, item in enumerate(strategic, 1):
        print(f"{i}. {item.get('task', '')}")
        print()

print("=" * 80)
print("\n✅ Test complete!")
print("\n📝 Note: This was a DRY RUN - no actual tasks were created in Google Tasks")
print("   To create real tasks, the importer will run automatically when new meetings arrive")
