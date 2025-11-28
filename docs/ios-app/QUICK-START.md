# iOS Inbox Capture - Quick Start

**Get mobile capture working in under 1 hour!** ⚡

---

## TL;DR

1. Set up iCloud folder (5 min)
2. Create iOS Shortcut (15 min)
3. Test and use! (5 min)

**Total time:** 25 minutes  
**Cost:** $0  
**Result:** Capture notes on iPhone → Auto-process to PetesBrain

---

## Step 1: Mac Setup (5 minutes)

Open Terminal and run:

```bash
# Move inbox to iCloud
mv ~/Documents/PetesBrain/\!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox

# Create symlink back
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox ~/Documents/PetesBrain/\!inbox

# Test it works
echo "# Test" > ~/Documents/PetesBrain/\!inbox/test-sync.md
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/test-sync.md

# Clean up test
rm ~/Documents/PetesBrain/\!inbox/test-sync.md
```

**Done!** Your inbox now syncs via iCloud.

---

## Step 2: iPhone Setup (15 minutes)

### A. Verify iCloud Access

1. Open **Files** app on iPhone
2. Tap **Browse** (bottom right)
3. Look for **iCloud Drive**
4. Navigate inside → you should see `PetesBrain-Inbox` folder
5. It should have your README.md file

### B. Create Quick Capture Shortcut

1. Open **Shortcuts** app
2. Tap **+** (top right)
3. Search and add these actions **in order:**

**Action 1: "Ask for Input"**
- Question: `What do you want to capture?`
- Input Type: Text
- Allow Multiple Lines: ON

**Action 2: "Format Date"**
- Date: Current Date
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 3: "Text"**
```
Formatted Date
-quick-note.md
```

**Action 4: "Set Variable"**
- Variable Name: `Filename`

**Action 5: "Save File"**
- File: Provided Input (from Action 1)
- Ask Where to Save: First time only
  - Navigate to iCloud Drive → PetesBrain-Inbox
  - Check "Always use this location"
- File Name: Filename

**Action 6: "Show Notification"**
- Text: `Note captured! ✓`

4. Tap ⋯ (top right) → Details
5. Name: `Inbox Capture`
6. Icon: Pick a color and symbol
7. **Add to Home Screen** (in details)
8. Done!

---

## Step 3: Test (5 minutes)

### On iPhone

1. Tap your new "Inbox Capture" icon
2. Type: `Test note from iPhone`
3. Verify notification appears

### On Mac

Wait 30 seconds, then:

```bash
# See the file
ls -la ~/Documents/PetesBrain/\!inbox/

# Should show: 20251105-XXXXXX-quick-note.md

# Read it
cat ~/Documents/PetesBrain/\!inbox/*quick-note.md
# Should show: "Test note from iPhone"
```

### Process It

```bash
# Run inbox processor
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# It should create a todo
ls ~/Documents/PetesBrain/todo/*quick-note*

# And archive the original
ls ~/Documents/PetesBrain/\!inbox/processed/*quick-note*
```

**It works!** 🎉

---

## Optional: Add Client Shortcut (10 minutes)

### Create Client Note Shortcut

1. Open Shortcuts app
2. Create new shortcut
3. Add actions:

**Action 1: "Choose from Menu"**
- Question: `Which client?`
- Add your top 5-10 clients:
  - Smythson
  - Devonshire Hotels
  - Superspace
  - National Design Academy
  - Tree2MyDoor
  - (add others)

**Action 2: "Set Variable"**
- Variable Name: `ClientName`

**Action 3: "Ask for Input"**
- Question: `Note about Chosen Menu Item`
- Input Type: Text
- Allow Multiple Lines: ON

**Action 4: "Text"**
```
client: ClientName

Provided Input
```

**Action 5: "Format Date"**
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 6: "Text"**
```
Formatted Date
-
ClientName
-note.md
```
(Replace spaces with hyphens manually)

**Action 7: "Save File"**
- File: Text from Action 4
- Destination: iCloud Drive/PetesBrain-Inbox
- File Name: Text from Action 6

**Action 8: "Show Notification"**
- `Client note saved for ClientName! ✓`

4. Name: `Client Note`
5. Add to Home Screen
6. Done!

### Test Client Note

1. Run shortcut
2. Select "Smythson"
3. Type: `Great performance this week`
4. On Mac: Check that it created a properly formatted file
5. Run inbox processor
6. Check: `clients/smythson/documents/inbox-capture-*.md`

---

## Optional: Add Siri (5 minutes)

For each shortcut:

1. Open Shortcuts app
2. Long press the shortcut
3. Tap ⓘ (details)
4. **"Add to Siri"**
5. Record phrase:
   - "Capture inbox note"
   - "Add client note"
6. Done!

Now say: **"Hey Siri, capture inbox note"**

---

## Daily Usage

### When You Have an Idea

1. Pull out iPhone
2. Tap "Inbox Capture" (or use Siri)
3. Type note
4. Done! (syncs automatically)

### After Client Meeting

1. Tap "Client Note"
2. Select client
3. Type meeting notes
4. Done!

### Every Morning

- Inbox processor runs at 8:00 AM automatically
- Notes are routed to correct folders
- You see them in:
  - Client folders: `clients/[client]/documents/`
  - Todo list: `todo/`
  - Knowledge base: `roksys/knowledge-base/`

---

## Troubleshooting

### "Can't save file"

**Fix:** Grant iCloud permission
- Settings → Shortcuts → iCloud Drive: ON
- Settings → Privacy → Files and Folders → Shortcuts: ON

### File not appearing on Mac

**Fix:** Force sync
```bash
# Kill and restart iCloud sync
killall bird

# Or check status
brctl status
```

### Inbox not processing

**Fix:** Run manually
```bash
cd ~/Documents/PetesBrain
python3 agents/system/inbox-processor.py
```

---

## What's Next?

### Working Well?
- Use it daily for a week
- Note what's awkward
- Refine shortcuts as needed

### Want More?
- **Read:** [ICLOUD-SHORTCUTS-SETUP.md](ICLOUD-SHORTCUTS-SETUP.md) - Complete guide
- **Create:** Voice note shortcut, task shortcut, more variants
- **Add:** Widgets, automation, Focus modes

### Not Enough?
- **Read:** [NATIVE-APP-SPEC.md](NATIVE-APP-SPEC.md) - Build native iOS app
- **Consider:** Hiring developer ($6k-24k)
- **Or:** Wait for Shortcuts to mature

---

## Pro Tips

### Faster Capture

**Back Tap:**
- Settings → Accessibility → Touch → Back Tap
- Double Tap: Inbox Capture shortcut
- Now: Tap back of phone to capture!

**Lock Screen Widget:**
- Long press Lock Screen → Customize
- Add Shortcuts widget
- Select Inbox Capture
- Now: Capture without unlocking!

### Better Organization

**Use Keywords:**
```markdown
client: Smythson
[your note]

task: Update budgets
[task details]

knowledge: PMax Tips
[knowledge content]
```

**Result:** Inbox processor knows exactly where to route!

### Voice Capture

Create voice note shortcut:
1. Action 1: "Dictate Text"
2. Action 2-6: Same as Quick Capture
3. Name: "Voice Note"
4. Add to Siri: "Record voice note"

Now: **"Hey Siri, record voice note"** → speak → done!

---

## Summary

✅ **Done in 25 minutes:**
- Mobile capture working
- Auto-sync to Mac
- Daily processing at 8 AM
- Free solution using Apple's tools

✅ **You can now:**
- Capture ideas anywhere
- Create client notes on the go
- Add tasks immediately
- Never lose a thought

✅ **It automatically:**
- Syncs to Mac (30 seconds)
- Routes to correct folders
- Creates todos and Google Tasks
- Archives processed files

---

## Need Help?

**Full Documentation:**
- [IOS-INBOX-APP.md](IOS-INBOX-APP.md) - All options and possibilities
- [ICLOUD-SHORTCUTS-SETUP.md](ICLOUD-SHORTCUTS-SETUP.md) - Complete setup guide
- [NATIVE-APP-SPEC.md](NATIVE-APP-SPEC.md) - Native app specification

**Check System:**
```bash
# Test inbox sync
ls -la ~/Documents/PetesBrain/\!inbox/

# Test iCloud sync
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/

# Run processor
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# Check logs
cat ~/.petesbrain-inbox-processor.log
```

---

**You're ready! Start capturing! 📱 → 💻 → 🎯**

