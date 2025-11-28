# Inbox Processing System

**Created:** November 5, 2025  
**Status:** ✅ Active and Production-Ready  
**Source:** Adapted from Mike Rhodes' 8020Brain inboxy agent

---

## Overview

Quick capture system for ideas, notes, and tasks that intelligently routes them to appropriate locations (client folders, todos, knowledge base) based on content and keywords.

## Features

- 📝 **Quick Capture** - Drop files in `!inbox/` folder instantly
- 🤖 **Smart Routing** - Auto-detects clients and action types
- 🏷️ **Action Keywords** - `client:`, `task:`, `knowledge:`, `email:`
- 📦 **Auto-Archive** - Processed files moved to `!inbox/processed/`
- ⏰ **Daily Processing** - Runs automatically at 8:00 AM
- 🔍 **Content Detection** - Finds client names in text

---

## Quick Start

### 1. Capture an Idea

```bash
# Quick way
echo "client: Smythson
Great performance this week!" > ~/Documents/PetesBrain/\!inbox/idea.md

# Or just create a file
open ~/Documents/PetesBrain/\!inbox/
# Then create your note
```

### 2. Use Action Keywords

**Client Note:**
```markdown
client: Smythson

Shopping campaigns performing well. 
Should discuss budget increase for Q4.
```

**Task:**
```markdown
task: Review budget trackers

Check October actuals for all clients.
Due end of week.
```

**Knowledge:**
```markdown
knowledge: Performance Max Tips

PMax works best with optimized product feeds
and 30+ day history.
```

**Email Draft:**
```markdown
email Devonshire Hotels:

Subject: October Performance Review

Hi team, wanted to share...
```

### 3. Process Manually (Optional)

```bash
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py
```

Or wait until 8:00 AM for automatic processing!

---

## Action Keywords

| Keyword | Usage | Result |
|---------|-------|--------|
| `client: [name]` | Client-related note | Saved to `clients/[name]/documents/` |
| `task: [title]` | Create todo item | Creates `todo/YYYYMMDD-[title].md` |
| `knowledge: [topic]` | Knowledge base entry | Adds to `roksys/knowledge-base/inbox-captures/` |
| `email [client]:` | Email draft | Saved to `clients/[name]/emails/` |

---

## How It Works

### Processing Flow

```
!inbox/note.md
    ↓
Detect Keywords
    ↓
┌─────────────┬─────────────┬──────────────┬─────────────┐
│   client:   │   task:     │  knowledge:  │   email:    │
│     ↓       │     ↓       │      ↓       │     ↓       │
│  Client     │    Todo     │  Knowledge   │   Email     │
│  Folder     │   Folder    │    Base      │   Draft     │
└─────────────┴─────────────┴──────────────┴─────────────┘
    ↓
Archive to !inbox/processed/
```

### Smart Detection

**If no keyword:**
1. Searches content for client names
2. If client found → routes to client folder
3. If no client → creates general todo

**Supported clients:**
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

---

## Routing Examples

### Example 1: Client Note with Keyword

**Input:** `!inbox/smythson-idea.md`
```markdown
client: Smythson

Shopping ads ROAS improved to 4.2x this week.
Should we increase budget?
```

**Output:** `clients/smythson/documents/inbox-capture-20251105.md`
```markdown
# Inbox Capture - 2025-11-05 10:04

**Source:** smythson-idea.md  
**Client:** smythson

---

Shopping ads ROAS improved to 4.2x this week.
Should we increase budget?
```

### Example 2: Task Creation

**Input:** `!inbox/budget-review.md`
```markdown
task: Monthly budget review

Check all client budgets:
- Devonshire (October actuals)
- Smythson (Q4 plan)
```

**Output:** `todo/20251105-monthly-budget-review.md`
```markdown
# monthly budget review

**Created:** 2025-11-05 10:04  
**Source:** budget-review.md

## Details

Check all client budgets:
- Devonshire (October actuals)
- Smythson (Q4 plan)

## Status

- [ ] Todo
```

### Example 3: Auto-Detection

**Input:** `!inbox/note.md`
```markdown
Just had a call with Devonshire Hotels.
They want to increase December budget by 30%.
```

**Output:** Detected "Devonshire Hotels" → `clients/devonshire-hotels/documents/inbox-capture-20251105.md`

---

## Configuration

### Schedule

**File:** `~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist`

**Current:** Daily at 8:00 AM

**Change time:**
```xml
<key>Hour</key>
<integer>8</integer>      <!-- 0-23 -->
<key>Minute</key>
<integer>0</integer>       <!-- 0-59 -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist
```

### Add More Clients

Edit `agents/system/inbox-processor.py`:

```python
CLIENTS = [
    'existing-client',
    'your-new-client',  # Add here
]
```

### Customize Routing

Modify the processing functions in `inbox-processor.py`:
- `process_client_note()` - Client document handling
- `process_task()` - Todo creation
- `process_knowledge()` - Knowledge base entries
- `process_email_draft()` - Email drafts

---

## Managing the Inbox

### View Current Inbox

```bash
ls -la ~/Documents/PetesBrain/\!inbox/
```

### View Processed Archive

```bash
ls -lt ~/Documents/PetesBrain/\!inbox/processed/ | head -20
```

### Clean Old Archives

```bash
# Remove processed files older than 30 days
find ~/Documents/PetesBrain/\!inbox/processed/ -name "*.md" -mtime +30 -delete
```

### Manual Processing

```bash
# Process inbox now
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# Check what would be processed (dry run)
ls -la ~/Documents/PetesBrain/\!inbox/*.md | grep -v README
```

---

## Troubleshooting

### Files Not Processing

**Check LaunchAgent:**
```bash
launchctl list | grep inbox-processor
```

**Check logs:**
```bash
cat ~/.petesbrain-inbox-processor.log
cat ~/.petesbrain-inbox-processor-error.log
```

**Run manually to see errors:**
```bash
cd ~/Documents/PetesBrain
python3 agents/system/inbox-processor.py
```

### Wrong Client Detected

Add explicit keyword:
```markdown
client: correct-client-name

Your note here...
```

Or use exact client folder name from `clients/` directory.

### Files Not Archived

Check permissions on `!inbox/processed/` folder:
```bash
ls -la ~/Documents/PetesBrain/\!inbox/
mkdir -p ~/Documents/PetesBrain/\!inbox/processed
```

---

## Integration with Other Systems

### Works With

- **Daily Briefing** - Shows recent meetings (which could come from inbox)
- **Task System** - Creates todos that appear in task lists
- **Client Folders** - Integrates seamlessly with client structure
- **Knowledge Base** - Adds to your growing knowledge repository

### Quick Capture Methods

**From iPhone/iPad:** ⭐ NEW!
See [iOS Inbox Capture](ios-app/README.md) for mobile capture:
- iCloud Drive + iOS Shortcuts (25 min setup)
- Capture notes anywhere, anytime
- Auto-sync to Mac within 30 seconds
- Voice notes with transcription
- Siri integration: "Hey Siri, capture inbox note"

**From Terminal:**
```bash
# Quick alias in ~/.zshrc
alias inbox='cd ~/Documents/PetesBrain/!inbox && code .'
```

**From Keyboard Maestro:**
Create macro to:
1. Create timestamped file in `!inbox/`
2. Open in editor
3. Save and close

**From Voice Notes:**
1. Record voice note
2. Transcribe to text
3. Save to `!inbox/[note].md`
4. Auto-processes at 8 AM

---

## Best Practices

1. **Capture Fast** - Don't overthink, just dump ideas
2. **Use Keywords** - More accurate routing
3. **One Topic Per File** - Easier to process
4. **Review Before 8 AM** - Check inbox daily
5. **Descriptive Filenames** - Helps later if needed
6. **Clean Archives Monthly** - Keep system tidy

---

## Files Reference

### Scripts
- `agents/system/inbox-processor.py` - Main processor

### LaunchAgents
- `~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist`

### Logs
- `~/.petesbrain-inbox-processor.log`
- `~/.petesbrain-inbox-processor-error.log`

### Folders
- `!inbox/` - Capture location
- `!inbox/processed/` - Archive
- `clients/*/documents/` - Client notes destination
- `clients/*/emails/` - Email drafts destination
- `todo/` - Task destination
- `roksys/knowledge-base/inbox-captures/` - Knowledge destination

---

## Comparison with Mike's System

### What We Adopted ✅

- Quick capture concept
- Action keyword system
- Smart routing logic
- Archive after processing

### What We Changed 🔄

- **Python vs Node.js** - Matches your ecosystem
- **Client-focused** - Routes to your 16 client folders
- **Simpler keywords** - 4 main actions vs many
- **Agency workflow** - Designed for client management
- **No content creation** - Focus on capture & route

### What We Added 🎯

- **Auto client detection** - Finds client names in content
- **Email draft routing** - Saves to client email folders
- **Daily automation** - LaunchAgent scheduling
- **Archive system** - Keeps inbox clean

---

## Future Enhancements

### Recently Added ✅

- [x] **Mobile app** - iOS Inbox Capture via iCloud + Shortcuts ([documentation](ios-app/README.md))

### Planned

- [ ] Email integration (forward emails to create notes)
- [ ] Slack message capture
- [ ] Priority detection
- [ ] Deadline extraction
- [ ] Auto-tagging

### Nice to Have

- [ ] AI-powered routing
- [ ] Sentiment analysis
- [ ] Related item suggestions
- [ ] Dashboard view
- [ ] Native iOS app (spec complete, see [docs/ios-app/NATIVE-APP-SPEC.md](ios-app/NATIVE-APP-SPEC.md))

---

## Related Documentation

- [8020Brain Analysis Report](8020BRAIN-ANALYSIS-REPORT.md) - Full analysis
- [Daily Briefing System](DAILY-BRIEFING-SYSTEM.md) - Morning summaries
- [Agents Overview](../agents/README.md) - All automation
- [Client Folder Structure](../clients/_templates/FOLDER-STRUCTURE.md)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-05 | 1.0 | Initial inbox processing system, adapted from Mike Rhodes' inboxy agent |

---

**Success!** Your inbox processing system is active. Drop notes in `!inbox/` and let it organize everything for you! 📥

