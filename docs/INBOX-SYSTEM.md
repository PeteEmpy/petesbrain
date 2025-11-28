# Inbox Processing System

**Status:** ✅ Active  
**Last Updated:** 2025-11-05

## Overview

The Inbox Processing System is your **personal assistant for capturing ideas**. Drop notes quickly into the `!inbox/` folder, and the system automatically routes them to the right place based on keywords and content analysis.

## The Problem It Solves

**Before:**
- 💭 Have an idea about a client → Where do you save it?
- ✅ Think of a task → Create a todo... somewhere?
- 📚 Learn something → Need to remember to document it
- **Result:** Ideas get lost or scattered everywhere

**After:**
- 📥 Drop ANY note in `!inbox/` folder
- 🤖 System reads it and routes automatically
- 📂 Everything ends up in the right place
- ✅ Nothing gets lost!

## How It Works

### 1. Quick Capture

Create a file in `!inbox/` with action keywords:

```markdown
# !inbox/my-idea.md

client: Smythson

Great campaign performance this week! 
ROAS up to 4.5x. Should we propose budget increase?
```

### 2. Automatic Processing

**Runs Daily:** Every morning at 8:00 AM  
**Manual:** Anytime with `python3 agents/system/inbox-processor.py`

### 3. Smart Routing

The system:
- ✅ Reads the file
- ✅ Detects action keyword (`client: Smythson`)
- ✅ Creates organized file in `clients/smythson/documents/`
- ✅ Archives original to `!inbox/processed/`

## Action Keywords

Tell the system where things should go:

| Keyword | Where It Goes | Example |
|---------|---------------|---------|
| `client: [name]` | Client documents folder | `client: Smythson` |
| `task: [title]` | Todo folder + Google Tasks | `task: Review budgets` |
| `knowledge: [topic]` | Knowledge base | `knowledge: PMax tips` |
| `email [client]:` | Client emails folder (draft) | `email Devonshire:` |

**No keyword?** System tries to detect client name in content!

## Examples

### Example 1: Client Note

**Create:** `!inbox/smythson-thought.md`
```markdown
client: Smythson

Their shopping campaigns are crushing it. 
ROAS up to 4.5x. Should we propose budget increase?
```

**Result:**
- ✅ File created: `clients/smythson/documents/inbox-capture-20251105.md`
- ✅ Properly formatted with timestamp
- ✅ Original archived to `!inbox/processed/`

### Example 2: Quick Task

**Create:** `!inbox/reminder.md`
```markdown
task: Update Devonshire budget tracker

Need to check October actuals vs plan.
Due Friday.
```

**Result:**
- ✅ Local todo: `todo/20251105-update-devonshire-budget-tracker.md`
- ✅ Google Task created with due date
- ✅ Original archived

### Example 3: Knowledge Capture

**Create:** `!inbox/pmax-tip.md`
```markdown
knowledge: Performance Max

Just learned PMax needs 30-day history 
minimum to perform well.

Source: Google Ads newsletter
```

**Result:**
- ✅ Saved to: `roksys/knowledge-base/inbox-captures/20251105-performance-max.md`
- ✅ Searchable for future reference
- ✅ Original archived

### Example 4: Email Draft

**Create:** `!inbox/email-idea.md`
```markdown
email Devonshire:

Subject: Q4 Performance Review

Hi team,

I wanted to share some fantastic results from October...
```

**Result:**
- ✅ Draft saved: `clients/devonshire-hotels/emails/draft-20251105.md`
- ✅ Ready to refine and send
- ✅ Original archived

## Manual Processing

Process inbox anytime (don't wait for 8 AM):

```bash
cd /Users/administrator/Documents/PetesBrain
shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3 \
  agents/system/inbox-processor.py
```

Or use system Python (if Google API libraries installed globally):
```bash
python3 agents/system/inbox-processor.py
```

## Automatic Processing

**Schedule:** Daily at 8:00 AM  
**Agent:** LaunchAgent `com.petesbrain.inbox-processor`  
**Location:** `~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist`

**Check Status:**
```bash
launchctl list | grep petesbrain.inbox
```

**View Logs:**
```bash
tail -f ~/.petesbrain-inbox-processor.log
```

## Google Tasks Integration

When you use `task:` keyword, the system:

1. ✅ Creates local todo file (markdown)
2. ✅ Creates Google Task (mobile accessible!)
3. ✅ Parses due dates automatically
4. ✅ Links them with Google Task ID

**See:** [Google Tasks Integration](./GOOGLE-TASKS-INTEGRATION.md) for full details.

## Supported Clients

The system recognizes these clients automatically:

- accessories-for-the-home
- bright-minds
- clear-prospects
- crowd-control
- devonshire-hotels
- go-glean
- godshot
- grain-guard
- just-bin-bags
- national-design-academy
- otc
- print-my-pdf
- smythson
- superspace
- tree2mydoor
- uno-lighting

**Note:** Client detection works with variations (spaces, hyphens, etc.)

## File Organization

```
PetesBrain/
├── !inbox/                    # Drop files here
│   ├── my-idea.md            # Your quick captures
│   └── processed/            # Auto-archived after processing
│       └── 20251105-*.md
│
├── todo/                      # Tasks go here
│   └── 20251105-*.md
│
├── clients/
│   └── [client-name]/
│       ├── documents/         # Client notes
│       └── emails/            # Email drafts
│
└── roksys/
    └── knowledge-base/
        └── inbox-captures/    # Knowledge items
```

## Processing Logic

1. **Read file** from `!inbox/`
2. **Detect keyword** (client:, task:, knowledge:, email)
3. **Route accordingly:**
   - **client:** → `clients/[name]/documents/`
   - **task:** → `todo/` + Google Tasks
   - **knowledge:** → `roksys/knowledge-base/inbox-captures/`
   - **email:** → `clients/[name]/emails/`
4. **No keyword?** Try to detect client in content
5. **Still nothing?** Create general todo
6. **Archive original** to `!inbox/processed/`

## Due Date Parsing (for Tasks)

The system understands natural language:

| You Write | Interprets As |
|-----------|---------------|
| `Due: tomorrow` | Next day |
| `Due: Thursday` | Next Thursday |
| `Due: end of week` | This Friday |
| `Due: 2025-11-07` | Exact date |

## Benefits

### 1. Zero Friction Capture
- No thinking "where should this go?"
- Just dump it in `!inbox/`
- System handles the rest

### 2. Always Organized
- Wake up to sorted notes
- Everything in its place
- Nothing gets lost

### 3. Mobile Integration
- Tasks sync to Google Tasks
- Access on phone
- Complete from anywhere

### 4. Searchable
- All files properly formatted
- Timestamped and sourced
- Easy to find later

## Tips & Best Practices

### Be Explicit with Keywords
```markdown
✅ Good:
task: Review Q4 budgets
client: Devonshire

❌ Ambiguous:
Check budgets for Devonshire
```

### Use Due Dates for Tasks
```markdown
✅ Good:
task: Send proposal
Due: Friday

❌ Missing:
task: Send proposal
(No due date = harder to prioritize)
```

### Add Context
```markdown
✅ Good:
client: Smythson

Shopping ROAS jumped to 4.5x this week.
Previous benchmark was 3.2x.
Should we increase budget?

❌ Too Brief:
client: Smythson
Good performance
```

### Batch Similar Items
Drop multiple items at once, process together:
```
!inbox/
├── smythson-note.md
├── devonshire-task.md
├── pmax-tip.md
└── budget-review.md
```

Run processor once, all get routed!

## Troubleshooting

### Files Not Processing

**Check:**
1. Is file in `!inbox/` folder?
2. Does it have `.md` extension?
3. Is it not named `README.md`? (excluded)

### Wrong Client Detected

**Fix:** Use explicit keyword:
```markdown
client: exact-client-name

[content]
```

### Task Not in Google Tasks

**Check:**
1. Did you use `task:` keyword?
2. Check Google Tasks web: https://tasks.google.com
3. Look in "PetesBrain" list

**Debug:**
```bash
# Check logs
tail -f ~/.petesbrain-inbox-processor.log
```

### Duplicate Processing

**Issue:** File processed multiple times

**Cause:** Running processor before previous run archived file

**Prevention:** Check `!inbox/` is clear before running again

## Statistics

**Since Launch (2025-11-05):**
- ✅ Processor: Active
- ✅ LaunchAgent: Loaded
- ✅ Google Tasks: Integrated
- ✅ Files Processed: 4+
- ✅ Todos Created: 3+

## Related Documentation

- [Google Tasks Integration](./GOOGLE-TASKS-INTEGRATION.md) - Full task management details
- [Daily Briefing System](./DAILY-BRIEFING-SYSTEM.md) - Morning summaries
- [Agents Overview](../agents/README.md) - All automated agents
- [Automation Guide](./AUTOMATION.md) - Complete automation reference

---

**Quick Start:**

1. Create file in `!inbox/` with keyword
2. Wait for 8 AM or run manually
3. Find it organized automatically
4. Repeat! 🚀

