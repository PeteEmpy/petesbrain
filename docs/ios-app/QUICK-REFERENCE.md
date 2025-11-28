# iOS Inbox Capture - Quick Reference Card

**Keep this handy for daily use** 📋

---

## 🚀 Quick Start Commands

### Mac Setup (One Time)
```bash
# Move inbox to iCloud
mv ~/Documents/PetesBrain/\!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox

# Create symlink
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox ~/Documents/PetesBrain/\!inbox

# Test
ls ~/Documents/PetesBrain/\!inbox/
```

### Manual Processing
```bash
# Process inbox now
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# Check logs
cat ~/.petesbrain-inbox-processor.log
```

---

## 📱 iOS Shortcuts

### Quick Capture Shortcut
```
1. Ask for Input → "What do you want to capture?"
2. Format Date → yyyyMMdd-HHmmss
3. Text → [Formatted Date]-quick-note.md
4. Set Variable → Filename
5. Save File → iCloud Drive/PetesBrain-Inbox/[Filename]
6. Show Notification → "Note captured! ✓"
```

### Client Note Shortcut
```
1. Choose from Menu → [Your Clients]
2. Set Variable → ClientName
3. Ask for Input → "Note about [ClientName]"
4. Text → "client: [ClientName]\n\n[Input]"
5. Format Date → yyyyMMdd-HHmmss
6. Text → [Date]-client-note.md
7. Save File → iCloud Drive/PetesBrain-Inbox/
8. Show Notification → "Client note saved!"
```

### Task Shortcut
```
1. Ask for Input → "Task title:"
2. Set Variable → TaskTitle
3. Ask for Input → "Task details:"
4. Set Variable → TaskDetails
5. Ask for Input (Date) → "Due date?"
6. Text → "task: [TaskTitle]\n\n[TaskDetails]\n\ndue: [Date]"
7. Format Date → yyyyMMdd-HHmmss
8. Save File → iCloud Drive/PetesBrain-Inbox/[Date]-task.md
9. Show Notification → "Task created!"
```

### Voice Note Shortcut
```
1. Dictate Text
2. Format Date → yyyyMMdd-HHmmss
3. Text → [Date]-voice-note.md
4. Save File → iCloud Drive/PetesBrain-Inbox/[Filename]
5. Show Notification → "Voice note captured!"
```

---

## 🗣️ Siri Commands

```
"Hey Siri, capture inbox note"
"Hey Siri, add client note"
"Hey Siri, create task"
"Hey Siri, record voice note"
```

---

## 🎹 Keyword Syntax

### Client Note
```markdown
client: Smythson

Your note content here...
```

### Task
```markdown
task: Task title here

Task details...

due: 2025-11-15
```

### Knowledge
```markdown
knowledge: Topic Name

Knowledge content...
```

### Email Draft
```markdown
email Devonshire Hotels:

Subject: Topic

Email content...
```

---

## 📂 File Naming Convention

```
YYYYMMDD-HHMMSS-description.md

Examples:
20251105-143022-quick-note.md
20251105-143100-client-note.md
20251105-143215-task.md
20251105-143500-voice-note.md
```

---

## 🔄 How It Works

```
┌─────────────┐
│   iPhone    │  Create note in Shortcuts
│   Shortcut  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ iCloud Drive│  Auto-sync (10-30 seconds)
│  PetesBrain-│
│    Inbox/   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     Mac     │  Symlink to PetesBrain/!inbox/
│  !inbox/    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   8:00 AM   │  Daily automatic processing
│  Processor  │
└──────┬──────┘
       │
       ├──→ clients/[name]/documents/
       ├──→ todo/[date]-[task].md
       ├──→ roksys/knowledge-base/
       └──→ !inbox/processed/ (archive)
```

---

## 🛠️ Common Commands

### Check Sync Status
```bash
# iCloud sync status
brctl status

# Force sync (if stuck)
killall bird

# Check files
ls -la ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/
```

### View Recent Captures
```bash
# Last 10 inbox files
ls -lt ~/Documents/PetesBrain/\!inbox/*.md | head -10

# Last 20 processed
ls -lt ~/Documents/PetesBrain/\!inbox/processed/*.md | head -20
```

### Manual Processing
```bash
# Run processor
cd ~/Documents/PetesBrain
python3 agents/system/inbox-processor.py

# View logs
cat ~/.petesbrain-inbox-processor.log

# View errors
cat ~/.petesbrain-inbox-processor-error.log
```

---

## 🐛 Troubleshooting Quick Fixes

### Files Not Appearing on Mac
```bash
# Check iCloud folder
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/

# Force sync
killall bird

# Wait 30 seconds, check again
```

### Shortcut Can't Save
**iPhone Settings:**
1. Settings → Shortcuts → iCloud Drive: ON
2. Settings → Privacy → Files and Folders → Shortcuts: ON

### Inbox Not Processing
```bash
# Run manually to see errors
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# Check LaunchAgent
launchctl list | grep inbox-processor

# Restart LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.inbox-processor.plist
```

### Voice Notes Not Transcribing
**iPhone Settings:**
1. Settings → Privacy → Microphone → Shortcuts: ON
2. Settings → General → Keyboard → Dictation: ON
3. Check internet connection (required)

---

## ⚙️ iPhone Settings Checklist

### Required Permissions
- [ ] iCloud Drive enabled
- [ ] Shortcuts has iCloud Drive access
- [ ] Shortcuts has Files & Folders access
- [ ] Microphone access (for voice notes)
- [ ] Internet connection for sync

### Check Permissions
```
Settings → Shortcuts → iCloud Drive: ✓
Settings → Privacy & Security → Files and Folders → Shortcuts: ✓
Settings → Privacy & Security → Microphone → Shortcuts: ✓
```

---

## 🎯 Daily Workflow

### Morning
```
☀️ 8:00 AM - Inbox processor runs automatically
📧 Check if any notes failed to process
✅ Review processed notes in client folders
📋 See new tasks in todo/ folder
```

### During the Day
```
💡 Idea strikes → Pull out phone
📱 Tap shortcut (or use Siri)
⌨️  Type/speak note
💾 Save (automatic sync)
🎯 Forget it - will be processed tomorrow
```

### Evening
```
📝 Review day's captures
✓  Any that need immediate attention?
🔄 Everything else processes at 8 AM
```

---

## 📊 Performance Expectations

| Action | Expected Time |
|--------|---------------|
| Capture note | 5 seconds |
| Local save | Instant |
| iCloud sync | 10-30 seconds |
| Appear on Mac | 10-30 seconds |
| Daily processing | 8:00 AM daily |
| Total capture → processed | < 24 hours |

---

## 🎨 Customization Ideas

### Additional Shortcuts
- Meeting notes template
- Performance review capture
- Campaign idea structure
- Expense tracking
- Client call summary

### Automation Triggers
- Location-based (at client office)
- Time-based (morning stand-up)
- NFC tag tap (desk, car)
- Back tap (double-tap phone back)
- Focus mode (work hours)

### Widget Configurations
```
Small Widget:  1 shortcut (Quick Capture)
Medium Widget: 4 shortcuts (all types)
Large Widget:  8+ shortcuts (custom variations)
```

---

## 📖 Documentation Links

**Quick Start:** [QUICK-START.md](QUICK-START.md)  
**Complete Setup:** [ICLOUD-SHORTCUTS-SETUP.md](ICLOUD-SHORTCUTS-SETUP.md)  
**All Options:** [IOS-INBOX-APP.md](IOS-INBOX-APP.md)  
**Native App Spec:** [NATIVE-APP-SPEC.md](NATIVE-APP-SPEC.md)  
**Full Index:** [INDEX.md](INDEX.md)

---

## 🔑 Key Principles

1. **Capture fast** - Don't think, just save
2. **Trust the system** - It will route correctly
3. **Process daily** - Morning routine includes review
4. **Use keywords** - More accurate routing
5. **Review weekly** - Optimize your workflow

---

## ⚡ Pro Tips

### Faster Capture
- Use Siri when hands-free
- Set up back tap for instant access
- Add Lock Screen widget
- Create Focus mode widget

### Better Organization
- Always use keywords (client:, task:, etc.)
- One topic per note
- Descriptive content
- Add due dates for tasks

### Maintenance
- Review logs weekly
- Clean processed archive monthly
- Update client list quarterly
- Refine shortcuts based on usage

---

## 🎓 Quick Training (5 minutes)

1. **Open iPhone** → Tap "Inbox Capture"
2. **Type:** "Test note from iPhone"
3. **Wait 30 seconds**
4. **On Mac:** Check `!inbox/` folder
5. **Run:** `python3 agents/system/inbox-processor.py`
6. **Check:** `todo/` folder for new file
7. **Success!** You've completed the full cycle

---

## 📞 Quick Help

**Can't find the file on Mac?**
→ Wait 30 seconds, check iCloud folder directly

**Shortcut not working?**
→ Check permissions in Settings

**Want to add a client?**
→ Edit the "Client Note" shortcut, add to menu

**Need more help?**
→ See full troubleshooting in setup guides

---

## ✅ Status Indicators

### Shortcut Behavior
- **✓ Notification** = Saved successfully
- **⚠️ Error** = Check permissions
- **No response** = Force quit and retry

### Sync Status
- **File in !inbox/** = Synced to Mac
- **File in processed/** = Processed successfully
- **File in todo/** = Task created
- **File in clients/[name]/** = Routed to client

---

## 🎯 Success Checklist

After setup, you should be able to:
- [ ] Capture note on iPhone in < 5 seconds
- [ ] See it on Mac within 30 seconds
- [ ] Run processor manually
- [ ] See it routed to correct folder
- [ ] Use Siri to capture
- [ ] Access from Home Screen widget
- [ ] Work offline (queues for sync)

**All checked? You're ready!** 🎉

---

**Print this page or bookmark it for quick reference!** 

**Status:** Ready to use ✅  
**Version:** 1.0  
**Updated:** November 5, 2025

