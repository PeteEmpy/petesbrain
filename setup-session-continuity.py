#!/usr/bin/env python3
"""
Setup Session Continuity System for All Clients

Creates session-log.md and open-questions.md for every client folder.
These files enable session continuity across AI conversations.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path("/Users/administrator/Documents/PetesBrain.nosync/clients")

# Session log template
SESSION_LOG_TEMPLATE = """# {client_name} - Session Log

This file tracks significant work sessions to maintain continuity across conversations. Each entry captures what was analysed, decided, and what's still being investigated.

---

## Session: 2025-12-22 (Session Continuity System Implementation)

**Analysed:**
- Current state of session continuity practices
- Gaps in handoff documentation
- Opportunities to systematise context loading

**Decided:**
- Implement session-log.md for all major clients
- Create open-questions.md for tracking unresolved curiosities
- Build "Start With Context" briefing automation

**Still investigating:**
- N/A (initial setup session)

**Next session:**
- Test the new continuity system on next {client_name} optimisation work
- Capture first real session summary following the new template

---

## Template for Future Sessions

```markdown
## Session: YYYY-MM-DD (Brief Topic Description)

**Analysed:**
- What data/campaigns/issues we examined
- What patterns or insights emerged

**Decided:**
- Actions taken (budget changes, bid adjustments, pauses, etc.)
- Strategic decisions made
- Experiments launched

**Still investigating:**
- Open questions that need more data
- Issues requiring follow-up
- Hypotheses to test

**Next session:**
- What to check/review next time
- Expected outcomes to verify
- Follow-up analyses needed
```

---
"""

# Open questions template
OPEN_QUESTIONS_TEMPLATE = """# {client_name} - Open Questions

This file tracks unresolved questions, patterns to investigate, and curiosities that aren't urgent enough for tasks but important to remember.

**Purpose:** Capture insights that emerge during analysis but require more data, time, or context to resolve. This prevents valuable observations from being forgotten.

---

## Template for New Questions

```markdown
**Question:** [Clear, specific question]
**Noticed:** YYYY-MM-DD
**Context:** [What triggered this question? What were you looking at?]
**Hypothesis:** [Your initial theory about why/what's happening]
**Need:** [What data/time/analysis would resolve this?]
**Priority:** [High/Medium/Low - how important is this to understand?]
**Status:** [Open/Investigating/Resolved]
```

---

## Active Questions

*(Add your open questions below as they emerge)*

---

## Resolved Questions

*(Move resolved questions here with the answer and date)*

### Example Resolved Question

**Question:** Why does mobile ROAS differ significantly from desktop?
**Noticed:** 2025-12-22
**Context:** Weekly performance review showed 50% gap
**Hypothesis:** Research behaviour vs conversion behaviour
**Resolution:** Cross-device attribution analysis revealed mobile users research, desktop users convert
**Resolved:** 2025-12-29
**Action taken:** Adjusted mobile bid modifier to account for assist value

---
"""


def get_client_display_name(client_slug):
    """Convert client slug to display name."""
    # Special cases
    special_cases = {
        'accessories-for-the-home': 'Accessories for the Home',
        'bright-minds': 'Bright Minds',
        'clear-prospects': 'Clear Prospects',
        'devonshire-hotels': 'Devonshire Hotels',
        'tree2mydoor': 'Tree2mydoor',
        'uno-lighting': 'Uno Lighting',
        'smythson': 'Smythson',
        'superspace': 'Superspace',
    }

    if client_slug in special_cases:
        return special_cases[client_slug]

    # Default: Title case with hyphens as spaces
    return client_slug.replace('-', ' ').title()


def create_session_continuity_files():
    """Create session-log.md and open-questions.md for all clients."""

    if not BASE_DIR.exists():
        print(f"❌ Client directory not found: {BASE_DIR}")
        return

    # Get all client directories (exclude _template)
    client_dirs = [d for d in BASE_DIR.iterdir()
                   if d.is_dir() and not d.name.startswith('_') and not d.name.startswith('.')]

    print(f"🟢 Found {len(client_dirs)} client directories")
    print()

    created_count = 0
    skipped_count = 0

    for client_dir in sorted(client_dirs):
        client_slug = client_dir.name
        client_name = get_client_display_name(client_slug)

        session_log_path = client_dir / "session-log.md"
        open_questions_path = client_dir / "open-questions.md"

        print(f"📁 {client_name} ({client_slug})")

        # Create session-log.md
        if session_log_path.exists():
            print(f"   ⏭️  session-log.md already exists - skipping")
            skipped_count += 1
        else:
            session_log_content = SESSION_LOG_TEMPLATE.format(client_name=client_name)
            session_log_path.write_text(session_log_content)
            print(f"   ✅ Created session-log.md")
            created_count += 1

        # Create open-questions.md
        if open_questions_path.exists():
            print(f"   ⏭️  open-questions.md already exists - skipping")
            skipped_count += 1
        else:
            open_questions_content = OPEN_QUESTIONS_TEMPLATE.format(client_name=client_name)
            open_questions_path.write_text(open_questions_content)
            print(f"   ✅ Created open-questions.md")
            created_count += 1

        print()

    print("=" * 60)
    print(f"🟢 Session Continuity Setup Complete")
    print(f"   ✅ Files created: {created_count}")
    print(f"   ⏭️  Files skipped (already exist): {skipped_count}")
    print(f"   📁 Clients processed: {len(client_dirs)}")
    print()
    print("Next steps:")
    print("1. Test the system on your next client work session")
    print("2. After each session, update session-log.md")
    print("3. Capture open questions in open-questions.md as they emerge")
    print("4. Start sessions by reading these files for context")


if __name__ == "__main__":
    create_session_continuity_files()
