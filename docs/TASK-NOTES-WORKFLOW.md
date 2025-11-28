# Task Notes Workflow - Quick Reference

**Last Updated:** 2025-11-18

## Setup (One-Time)

**Start the task notes server:**
```bash
python3 ~/Documents/PetesBrain/shared/scripts/save-task-notes.py
```

Leave it running in the background. It saves notes to a fixed location within PetesBrain.

**Optional:** Add to startup (so it runs automatically):
- macOS: Create LaunchAgent
- Or just start it when needed

---

## The 3-Step Workflow

### 1️⃣ Add Notes in Browser
Open `tasks-overview.html` and click "Add Note" on any task.

**Example notes:**
- *"Done. AI/MAX campaign set up with brand inclusions. Review in 7 days."*
- *"Called client, budget increase approved. Implementing tomorrow."*
- *"Started but waiting on data from Google rep."*

### 2️⃣ Click "Process All Notes"
- Saves directly to `/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`
- No downloads, no file management!
- Copies "Process my task notes" to your clipboard

**If server not running:** Falls back to browser download with helpful error message.

### 3️⃣ Paste to Claude
Just paste (Cmd+V) the clipboard message to Claude.

---

## What Happens Next

Claude intelligently processes each note:

✅ **Completes tasks** when you say "done", "completed", "finished"

🔄 **Creates parent/child hierarchy** when you mention follow-ups:
- Standalone → Parent + completed child + follow-up child
- Child → New sibling child for follow-up
- Parent → New child added

📝 **Expands notes** with context from your updates

📅 **Extracts timing** from phrases like "review in 7 days", "check next Monday"

⏸️ **Keeps active** if you mention "waiting", "blocked", "started"

---

## Example Transformation

**Your note:** *"Implemented AI/MAX for brand campaign. Campaign ID 20276730131. Review next Monday."*

**Claude creates:**
```
[AFH] AI Max Brand Campaign - Implementation & Review (PARENT)
  ├─ Implement AI Max campaign (COMPLETED Nov 18)
  │   Notes: Campaign ID 20276730131. Brand targeting enabled.
  │          Settings: [details]. Live as of Nov 18, 2025.
  │
  └─ Review AI Max brand campaign performance (ACTIVE, Due Nov 25)
      Notes: Review after 1 week of data. Check: impressions,
             CTR, conv rate, ROAS vs main PMax.
```

---

## Tips for Best Results

✅ **Be specific:** *"Done. Budget increased to £500/day. Monitor daily for 3 days."*

❌ **Avoid vague:** *"Working on it"*

✅ **Mention follow-ups:** *"Completed. Review in 2 weeks."*

✅ **Include details:** Campaign IDs, settings, who you contacted

✅ **Note blockers:** *"Waiting on client approval before proceeding."*

---

## That's It!

No manual task creation. No thinking about hierarchy. No tracking review dates. Just write what you did naturally, and the system handles the rest.

**Open:** `open tasks-overview.html`
