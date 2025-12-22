# Fuzzy Date Parsing Enhancement

**Date:** 2025-12-16
**Status:** ✅ Complete
**Agents Updated:** ai-inbox-processor, inbox-processor

---

## Problem

User created a Huel reminder via iPhone shortcut (Inbox Capture system) this morning with natural language date "Within next week". The reminder appeared in tasks with the literal text "Within next week" instead of a proper YYYY-MM-DD date, causing it not to display correctly in the Reminders section.

**User expectation:** Natural language date expressions should automatically convert to proper dates.

---

## Solution

Implemented comprehensive fuzzy date parsing in both inbox processor agents:

### 1. Created `parse_fuzzy_date()` Function

**Location:**
- `/agents/ai-inbox-processor/ai-inbox-processor.py` (lines 154-229)
- `/agents/inbox-processor/inbox-processor.py` (lines 516-591)

**Handles:**
- Simple expressions: "tomorrow", "today", "yesterday"
- Week-based: "next week", "within next week", "in a week", "in the next week"
- Time deltas: "in 3 days", "in 2 weeks", "in 1 month"
- Day of week: "next Monday", "next Tuesday", etc.
- Abbreviations: "tmrw", "mon", "tue", "wed", etc.

**Returns:** YYYY-MM-DD formatted date string, or None if cannot parse

### 2. Integrated Parser into Workflow

**ai-inbox-processor.py:**
- Updated `create_quick_task()` function (lines 654-668)
- Replaced simple date parsing with fuzzy parser
- Removes date expressions from task titles automatically

**inbox-processor.py:**
- Enhanced `extract_due_date()` function (lines 593-629)
- Parses fuzzy dates when reading from AI-enhanced notes
- Logs parsed dates for debugging: "📅 Parsed fuzzy date: 'within next week' → 2025-12-23"

---

## Examples

### Before Enhancement
```json
{
  "title": "Purchase Fuel",
  "due_date": "Within next week"  // ❌ Invalid format
}
```

### After Enhancement
```json
{
  "title": "Order Huel",
  "due_date": "2025-12-23"  // ✅ Properly parsed
}
```

---

## Supported Date Expressions

| Expression | Example | Result (from 2025-12-16) |
|------------|---------|-------------------------|
| **Simple** | tomorrow, today, yesterday | 2025-12-17, 2025-12-16, 2025-12-15 |
| **Week-based** | next week, within next week, in a week | 2025-12-23 |
| **Time deltas** | in 3 days, in 2 weeks, in 1 month | 2025-12-19, 2025-12-30, 2026-01-15 |
| **Day of week** | next Monday, next Friday | 2025-12-22, 2025-12-19 |
| **Abbreviations** | tmrw, mon, tue, wed | (same as full names) |

---

## Testing

Tested with multiple expressions:
```
Within next week     → 2025-12-23 ✅
tomorrow             → 2025-12-17 ✅
in 3 days            → 2025-12-19 ✅
in 2 weeks           → 2025-12-30 ✅
next Monday          → 2025-12-22 ✅
today                → 2025-12-16 ✅
```

---

## Files Modified

1. `/agents/ai-inbox-processor/ai-inbox-processor.py`
   - Added `parse_fuzzy_date()` function (lines 154-229)
   - Updated `create_quick_task()` to use fuzzy parser (lines 654-668)

2. `/agents/inbox-processor/inbox-processor.py`
   - Added `timedelta` import (line 19)
   - Added `parse_fuzzy_date()` function (lines 516-591)
   - Enhanced `extract_due_date()` to parse fuzzy dates (lines 593-629)

---

## How to Use

**For users (via iPhone shortcut):**
Just speak naturally:
- "Remind me to order Huel within next week"
- "Quick task review budget tomorrow"
- "Follow up with client in 3 days"

The system will automatically parse and convert to proper dates.

**For developers:**
```python
from datetime import datetime, timedelta
import re

# Use parse_fuzzy_date() function
date_text = "within next week"
parsed_date = parse_fuzzy_date(date_text)
# Returns: "2025-12-23"
```

---

## Edge Cases

**Already YYYY-MM-DD format:** Returns as-is without parsing
**Unknown format:** Returns None (logged as warning for manual review)
**Month approximation:** Uses 30 days per month (not exact)

---

## Future Enhancements

Potential additions:
- Specific dates: "December 25th", "Jan 1st"
- Relative expressions: "end of month", "start of next quarter"
- Time expressions: "9am tomorrow", "2pm Friday"
- Natural variations: "a couple days", "few weeks"

---

## Related Documentation

- `docs/TASK-SYSTEM-DECISION-GUIDE.md` - Task system overview
- `.claude/CLAUDE.md` - Developer guide
- `docs/INCIDENTS.md` - Historical incident log
