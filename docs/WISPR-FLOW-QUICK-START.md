# Wispr Flow as Primary Capture System - Quick Start

**Last Updated:** November 5, 2025

Your primary capture system is now **Wispr Flow** - dictate notes on desktop or mobile, and they automatically flow into PetesBrain.

---

## The Complete Flow

```
┌─────────────────────────────────────────────────────────┐
│  YOU: Dictate in Wispr Flow (Desktop or Mobile)        │
└────────────┬────────────────────────────────────────────┘
             │
             │ Syncs to cloud (automatic)
             ▼
┌─────────────────────────────────────────────────────────┐
│  DESKTOP: Wispr Flow syncs to local database           │
└────────────┬────────────────────────────────────────────┘
             │
             │ Every 5 minutes (automatic)
             ▼
┌─────────────────────────────────────────────────────────┐
│  IMPORTER: Extracts new notes → Saves to !inbox/       │
└────────────┬────────────────────────────────────────────┘
             │
             │ You review and add keywords
             ▼
┌─────────────────────────────────────────────────────────┐
│  PROCESSOR: Routes notes to correct location           │
│  - client: → Client CONTEXT.md                          │
│  - task: → Google Tasks                                 │
│  - knowledge: → Knowledge Base                          │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start: Your First Note

### 1. Dictate in Wispr Flow

**On Desktop or Mobile, speak naturally:**

> "Client Smythson: They want to increase Q4 budget by 30 percent. Need to prepare proposal by Friday."

### 2. Wait 5 Minutes (or Run Manually)

**Automatic:** Importer runs every 5 minutes
**Manual:**
```bash
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

### 3. Check Inbox

```bash
ls -la !inbox/
```

You'll see a file like:
`20251105-143000-wispr-client-smythson-they-want-to.md`

### 4. Add Routing Keyword (Optional)

Open the file and add keyword at the top:

```markdown
client: Smythson

# Client Smythson

They want to increase Q4 budget by 30 percent. Need to prepare proposal by Friday.

---
*Source: Wispr Flow*
*Created: 2025-11-05 14:30:00*
```

### 5. Process (Automatic Daily or Manual)

**Automatic:** Runs daily at 8 AM
**Manual:**
```bash
python3 agents/system/inbox-processor.py
```

**Result:** Saved to `clients/smythson/documents/inbox-capture-20251105.md`

---

## Routing Keywords (Add After Import)

### Client Notes
```markdown
client: [client-name]

[your dictated content]
```
**Goes to:** `clients/[client-name]/documents/inbox-capture-YYYYMMDD.md`

### Tasks
```markdown
task: [task description]

[your dictated content]
```
**Goes to:** Google Tasks

### Knowledge
```markdown
knowledge: [topic]

[your dictated content]
```
**Goes to:** `roksys/knowledge-base/[category]/`

### No Keyword
Notes without keywords stay in `!inbox/processed/` for manual review

---

## Pro Tips for Dictation

### Include Context in Your Dictation

**Good:**
> "Client Smythson: Budget discussion. They want 30 percent increase for Q4."

**Better:**
> "Client Smythson: Had budget meeting today. They're happy with performance and want to increase Q4 budget by 30 percent. Action: Prepare proposal showing projected ROAS and revenue increase by Friday."

### Use Natural Markers

Wispr Flow is smart - use natural language:

- "Client [name]:" - Easy to spot and route
- "Task:" or "To-do:" - Signals an action item
- "Note:" or "Remember:" - General capture
- "Idea:" - For later consideration

### Multiple Notes vs One Long Note

**Separate notes work better:**
- One client, one note
- One task, one note
- One idea, one note

**Why:** Easier to route and process individually

---

## Common Workflows

### Workflow 1: Client Meeting Notes

**During/after meeting, dictate:**
> "Client Devonshire Hotels: Discussed October performance. They're happy with bookings increase. Mentioned competitor running aggressive campaign. Action: Analyze competitor ads and suggest counter-strategy."

**What happens:**
1. Syncs to desktop within seconds
2. Imported to !inbox/ within 5 minutes
3. You add `client: Devonshire Hotels` at top
4. Processed to `clients/devonshire-hotels/documents/`
5. I read it when analyzing that client

### Workflow 2: Quick Task Capture

**While thinking about something:**
> "Task: Review September budgets for all clients. Check if any are overspending."

**What happens:**
1. Imported to !inbox/ within 5 minutes
2. You add `task:` at top (or it's detected automatically)
3. Creates Google Task
4. Tracked in tasks system

### Workflow 3: Knowledge Capture

**After reading an article:**
> "Knowledge: Performance Max works best with stable budgets for at least 30 days. From Google Ads blog."

**What happens:**
1. Imported to !inbox/ within 5 minutes
2. You add `knowledge: Performance Max` at top
3. Added to knowledge base
4. I reference it when advising on PMax campaigns

### Workflow 4: General Thoughts

**Random idea:**
> "Idea: Create dashboard showing all client ROAS trends in one view. Would make weekly reviews faster."

**What happens:**
1. Imported to !inbox/ within 5 minutes
2. No keyword needed - stays in inbox
3. Review daily, decide what to do with it
4. Could become a task, project note, or just archive

---

## Mobile + Desktop Sync

### How Sync Works

1. **Create on mobile** → Syncs to Wispr Flow cloud → Downloads to desktop
2. **Create on desktop** → Already local, processed immediately
3. **Sync time:** Usually seconds to 1-2 minutes

### Best Practice

**For time-sensitive notes:**
- Create on desktop if you're there (faster processing)
- Create on mobile when on the go (syncs within minutes)
- Run importer manually if urgent: `python3 agents/wispr-flow-importer/wispr-flow-importer.py`

---

## Daily Routine

### Morning (Review Inbox)

```bash
# Check what came in overnight
ls -la !inbox/

# Review each note
# Add routing keywords where needed

# Process manually (or wait for 8 AM auto-run)
python3 agents/system/inbox-processor.py
```

### Throughout Day (Capture Freely)

- Dictate client notes during/after meetings
- Capture tasks as they come up
- Note learnings from articles or discussions
- Voice memo ideas and observations

### Evening (Quick Check)

```bash
# See what's queued for tomorrow's processing
ls -la !inbox/
```

---

## Checking Status

### Is Everything Running?

```bash
# Check Wispr Flow importer
launchctl list | grep wispr-flow

# Should show: com.petesbrain.wispr-flow-importer
```

### When Did It Last Run?

```bash
# View log
cat ~/.petesbrain-wispr-flow.log | tail -20
```

### Force Import Now

```bash
# Don't wait 5 minutes
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

---

## Replacing Old System

### Old Way (Manual Files)
❌ Create file in !inbox/ manually
❌ Type or paste content
❌ Add routing keywords
❌ Wait for processing

### New Way (Wispr Flow)
✅ Dictate anywhere (desktop/mobile)
✅ Auto-syncs and imports
✅ Add keywords during review
✅ Same processing

**Advantage:** Capture instantly by voice, anywhere, anytime

---

## Examples with Full Context

### Example 1: Client Budget Discussion

**You dictate in Wispr Flow:**
> "Client Smythson: Called about Q4 strategy. Current performance is strong with 420 percent ROAS. They have full inventory for holiday season and want to scale. Proposing 30 percent budget increase from 150 to 200 pounds daily. Need to check impression share and prepare forecast by Friday."

**After import (file in !inbox/):**

```markdown
# Client Smythson

Called about Q4 strategy. Current performance is strong with 420 percent ROAS. They have full inventory for holiday season and want to scale. Proposing 30 percent budget increase from 150 to 200 pounds daily. Need to check impression share and prepare forecast by Friday.

---
*Source: Wispr Flow*
*Created: 2025-11-05 14:30:00*
```

**You add keyword:**

```markdown
client: Smythson

# Client Smythson

Called about Q4 strategy. Current performance is strong with 420 percent ROAS...
```

**After processing:**
- Saved to `clients/smythson/documents/inbox-capture-20251105.md`
- I read this when you ask about Smythson
- Informs Q4 strategy decisions

### Example 2: Multiple Tasks from Meeting

**You dictate THREE separate notes in Wispr Flow:**

> "Task: Send Devonshire October report by end of day"

> "Task: Update Superspace product feed with new items"

> "Task: Schedule Q4 review calls with top 5 clients"

**After import:**
- Three files in !inbox/
- Add `task:` to each
- Process → Three Google Tasks created

---

## Troubleshooting

### Notes Not Appearing

**Check sync:**
- Open Wispr Flow on desktop
- See your mobile notes there?
- If not, check Wispr Flow sync settings

**Check importer:**
```bash
# Is it running?
launchctl list | grep wispr-flow

# Run manually
python3 agents/wispr-flow-importer/wispr-flow-importer.py

# Check logs
cat ~/.petesbrain-wispr-flow.log
```

### Notes Not Being Routed

**Check you added keywords:**
- Open file in !inbox/
- Add `client:`, `task:`, or `knowledge:` at top

**Run processor:**
```bash
python3 agents/system/inbox-processor.py
```

**Check processed folder:**
```bash
ls -la !inbox/processed/
```

---

## Summary

**Your workflow is now:**

1. **Dictate** in Wispr Flow (anywhere, anytime)
2. **Syncs** automatically (desktop ← → mobile)
3. **Imports** every 5 minutes to !inbox/
4. **Review** daily, add keywords
5. **Processes** daily or on-demand
6. **Routes** to correct location automatically

**No more manual file creation. Just speak and it flows through the system.**

---

## Commands Cheat Sheet

```bash
# Run importer now
python3 agents/wispr-flow-importer/wispr-flow-importer.py

# Check inbox
ls -la !inbox/

# Process inbox
python3 agents/system/inbox-processor.py

# View logs
cat ~/.petesbrain-wispr-flow.log | tail -20

# Check status
launchctl list | grep wispr
```

---

## Next Steps

1. **Test it now**: Dictate a note in Wispr Flow
2. **Wait 5 min** (or run: `python3 agents/wispr-flow-importer/wispr-flow-importer.py`)
3. **Check !inbox/**: `ls -la !inbox/`
4. **Add keyword** to route it
5. **Process**: `python3 agents/system/inbox-processor.py`

**You're ready! Start dictating.** 🎤

---

**Complete Documentation:** `docs/WISPR-FLOW-INTEGRATION.md`
