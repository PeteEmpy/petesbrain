# iCloud + Shortcuts Setup Guide

**Complete step-by-step implementation guide**  
**Time Required:** 1-2 hours  
**Cost:** Free  
**Difficulty:** Easy

---

## Overview

This guide will help you set up mobile note capture using iCloud Drive and iOS Shortcuts - the fastest, easiest, and most cost-effective solution for capturing inbox notes on your iPhone or iPad.

---

## Part 1: Mac Setup (30 minutes)

### Step 1: Configure iCloud Folder

We have two options. **Option B is recommended** as it's cleaner and more reliable.

#### Option A: Two-Way Sync (Advanced)

```bash
# Create iCloud folder
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox

# This will be monitored by inbox processor alongside main inbox
```

Then update `agents/system/inbox-processor.py`:

```python
# Replace INBOX_DIR = PROJECT_ROOT / '!inbox' with:

INBOX_DIRS = [
    PROJECT_ROOT / '!inbox',
    Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Inbox'
]

# Update process_inbox() function to loop through both directories
def process_inbox():
    """Process all files in inbox directories"""
    
    for inbox_dir in INBOX_DIRS:
        if not inbox_dir.exists():
            print(f"⚠️  {inbox_dir} not found, skipping")
            continue
            
        print(f"📁 Processing: {inbox_dir}")
        
        # Get all markdown files (except README)
        inbox_files = [f for f in inbox_dir.glob('*.md') if f.name != 'README.md']
        
        # ... rest of processing logic
```

#### Option B: Direct iCloud Integration (Recommended)

```bash
# 1. Move inbox to iCloud
mv ~/Documents/PetesBrain/\!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox

# 2. Create symlink so everything still works
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox ~/Documents/PetesBrain/\!inbox

# 3. Verify it works
ls -la ~/Documents/PetesBrain/\!inbox
# Should show symlink arrow → to iCloud location

# 4. Test by creating a file
echo "# Test" > ~/Documents/PetesBrain/\!inbox/test.md
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/test.md
# Should show the file exists in both locations
```

### Step 2: Verify iCloud Sync

1. **Check iCloud Drive is enabled:**
   - System Settings → Apple ID → iCloud
   - Ensure "iCloud Drive" is checked
   - Ensure enough storage available

2. **Test sync:**
   ```bash
   # Create test file on Mac
   echo "Test from Mac $(date)" > ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/mac-test.md
   
   # Wait 10-30 seconds
   # Check on iPhone: Files app → iCloud Drive → PetesBrain-Inbox
   # Should see mac-test.md
   ```

3. **Clean up test:**
   ```bash
   rm ~/Documents/PetesBrain/\!inbox/test.md
   rm ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/mac-test.md
   ```

### Step 3: Update Inbox Processor (if needed)

If you chose Option A, update the processor:

```bash
# Back up current processor
cp ~/Documents/PetesBrain/agents/system/inbox-processor.py ~/Documents/PetesBrain/agents/system/inbox-processor.py.backup

# Edit the file
code ~/Documents/PetesBrain/agents/system/inbox-processor.py
# Or your preferred editor
```

Add at the top after `INBOX_DIR` definition:

```python
ICLOUD_INBOX = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Inbox'
INBOX_DIRS = [INBOX_DIR]
if ICLOUD_INBOX.exists():
    INBOX_DIRS.append(ICLOUD_INBOX)
```

Then modify `process_inbox()` to iterate through `INBOX_DIRS` instead of just `INBOX_DIR`.

### Step 4: Test the System

```bash
# Run processor manually
cd ~/Documents/PetesBrain
python3 agents/system/inbox-processor.py

# Should show both directories being checked
```

---

## Part 2: iPhone Setup (30 minutes)

### Step 1: Verify iCloud Access

1. Open **Files** app on iPhone
2. Tap **Browse** (bottom right)
3. Look for **iCloud Drive** in locations
4. Navigate to `iCloud Drive`
5. You should see `PetesBrain-Inbox` folder
6. If not, wait a few minutes for sync

### Step 2: Create Shortcuts

Open **Shortcuts** app (pre-installed on iOS).

#### Shortcut 1: Quick Capture

1. Tap **+** to create new shortcut
2. Add these actions:

**Action 1: Ask for Input**
- Search for "Ask for Input"
- Question: "What would you like to capture?"
- Input Type: Text
- Allow Multiple Lines: ON

**Action 2: Get Current Date**
- Search for "Format Date"
- Date: Current Date
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 3: Text**
- Add "Text" action
- Content: (tap to edit)
  ```
  Formatted Date
  -quick-note.md
  ```
- This creates filename like: `20251105-143022-quick-note.md`

**Action 4: Set Variable**
- Search "Set Variable"
- Variable Name: `Filename`
- Input: Previous Text result

**Action 5: Save File**
- Search "Save File"
- File: Provided Input (the text from step 1)
- Destination: Ask Where to Save
- On first run: Navigate to iCloud Drive/PetesBrain-Inbox
- Check "Always use this location"
- File Name: Filename (variable from step 4)

**Action 6: Show Notification**
- Search "Show Notification"
- Text: "Note captured to inbox! ✓"

3. **Name the shortcut:** "Inbox Capture"
4. **Choose icon:** Tap icon, choose color and glyph
5. **Test it:** Tap ▶️ to run

#### Shortcut 2: Client Note

1. Create new shortcut
2. Add actions:

**Action 1: Choose from Menu**
- Question: "Which client?"
- Add menu items (adjust to your clients):
  - Smythson
  - Devonshire Hotels  
  - Superspace
  - National Design Academy
  - Tree2MyDoor
  - Crowd Control
  - Accessories for the Home
  - Clear Prospects
  - Bright Minds
  - (add others as needed)

**Action 2: Set Variable**
- Variable Name: `ClientName`
- Input: Menu Result

**Action 3: Ask for Input**
- Question: "Note about Chosen Menu Item"
- Input Type: Text
- Allow Multiple Lines: ON

**Action 4: Text** (create content)
```
client: ClientName

Provided Input
```

**Action 5: Get Current Date**
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 6: Text** (create filename)
```
Formatted Date
-
ClientName
-note.md
```

**Action 7: Save File**
- File: Text from Action 4 (the content)
- Destination: iCloud Drive/PetesBrain-Inbox (set once)
- File Name: Text from Action 6

**Action 8: Show Notification**
- "Client note saved for ClientName! ✓"

3. **Name:** "Client Note"
4. **Choose icon:** Different color from Quick Capture
5. **Test**

#### Shortcut 3: Quick Task

1. Create new shortcut
2. Add actions:

**Action 1: Ask for Input**
- Question: "Task title:"
- Input Type: Text

**Action 2: Set Variable**
- Variable: `TaskTitle`

**Action 3: Ask for Input**  
- Question: "Task details (optional):"
- Input Type: Text
- Allow Multiple Lines: ON

**Action 4: Set Variable**
- Variable: `TaskDetails`

**Action 5: Ask for Input**
- Question: "Due date?"
- Input Type: Date and Time
- Default: No Default

**Action 6: If** (has due date)
- If `Provided Input` has any value

**Action 7: Format Date** (inside If)
- Date: Provided Input
- Format: Custom  
- Format String: `yyyy-MM-dd`

**Action 8: Set Variable** (inside If)
- Variable: `DueDate`
- Input: Formatted Date

**Action 9: Otherwise**

**Action 10: Set Variable** (in Otherwise)
- Variable: `DueDate`
- Input: (leave empty)

**Action 11: End If**

**Action 12: Text** (create content)
```
task: TaskTitle

TaskDetails

due: DueDate
```

**Action 13: Get Current Date**
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 14: Text** (filename)
```
Formatted Date
-task.md
```

**Action 15: Save File**
- File: Text from Action 12
- Destination: iCloud Drive/PetesBrain-Inbox
- File Name: Text from Action 14

**Action 16: Show Notification**
- "Task created: TaskTitle ✓"

3. **Name:** "Quick Task"
4. **Test**

#### Shortcut 4: Voice Note (Bonus)

1. Create new shortcut
2. Add actions:

**Action 1: Dictate Text**
- Language: English (or your preference)
- Show on screen: ON

**Action 2: Get Current Date**
- Format: Custom
- Format String: `yyyyMMdd-HHmmss`

**Action 3: Text** (filename)
```
Formatted Date
-voice-note.md
```

**Action 4: Save File**
- File: Dictated Text
- Destination: iCloud Drive/PetesBrain-Inbox
- File Name: Text from previous

**Action 5: Show Notification**
- "Voice note captured! ✓"

3. **Name:** "Voice Note"
4. **Test:** Speak something, should save transcription

### Step 3: Add to Home Screen

For each shortcut:

1. **Long press** the shortcut in the list
2. Tap **"Details"**
3. Tap **"Add to Home Screen"**
4. Customize:
   - Name (shows under icon)
   - Icon (color and symbol)
5. Tap **"Add"**
6. Arrange on Home Screen

**Suggested arrangement:**
Create a folder called "Capture" with all four shortcuts.

### Step 4: Set Up Siri

For each shortcut:

1. In Shortcuts app, tap the shortcut
2. Tap ⓘ (info icon)
3. Tap **"Add to Siri"**
4. Record phrase:
   - "Capture inbox note"
   - "Add client note"
   - "Create task"
   - "Record voice note"
5. Tap **"Done"**

Now you can say: **"Hey Siri, capture inbox note"**

### Step 5: Create Widgets (Optional)

1. **Long press** on Home Screen (empty area)
2. Tap **"+"** (top left)
3. Search **"Shortcuts"**
4. Choose widget size:
   - Small: 1 shortcut
   - Medium: 4 shortcuts
   - Large: 8 shortcuts
5. Tap **"Add Widget"**
6. Long press widget → **"Edit Widget"**
7. Select your shortcuts
8. Position on Home Screen

**Recommended:** Medium widget with:
- Quick Capture
- Client Note
- Quick Task
- Voice Note

---

## Part 3: Testing (15 minutes)

### Test 1: Quick Capture

1. **On iPhone:**
   - Run "Inbox Capture" shortcut
   - Type: "Test note from iPhone"
   - Verify "Note captured!" notification

2. **On Mac:**
   ```bash
   # Wait 10-30 seconds for sync
   ls -la ~/Documents/PetesBrain/\!inbox/
   # Should see: 20251105-XXXXXX-quick-note.md
   
   # View content
   cat ~/Documents/PetesBrain/\!inbox/20251105-*-quick-note.md
   # Should show: "Test note from iPhone"
   ```

### Test 2: Client Note

1. **On iPhone:**
   - Run "Client Note" shortcut
   - Choose "Smythson"
   - Type: "Performance review meeting scheduled for next week"
   - Check notification

2. **On Mac:**
   ```bash
   ls -la ~/Documents/PetesBrain/\!inbox/
   cat ~/Documents/PetesBrain/\!inbox/20251105-*-smythson-note.md
   ```
   
   Should see:
   ```markdown
   client: Smythson
   
   Performance review meeting scheduled for next week
   ```

### Test 3: Task Creation

1. **On iPhone:**
   - Run "Quick Task"
   - Title: "Update budget trackers"
   - Details: "Check October actuals for all clients"
   - Due: Next Friday
   - Check notification

2. **On Mac:**
   ```bash
   cat ~/Documents/PetesBrain/\!inbox/20251105-*-task.md
   ```
   
   Should see:
   ```markdown
   task: Update budget trackers
   
   Check October actuals for all clients
   
   due: 2025-11-08
   ```

### Test 4: End-to-End Processing

1. **Create all three test notes above**

2. **Wait for sync** (30 seconds)

3. **Run inbox processor:**
   ```bash
   cd ~/Documents/PetesBrain
   python3 agents/system/inbox-processor.py
   ```

4. **Check results:**
   ```bash
   # Quick note should become a todo
   ls -la todo/20251105-*test-note*
   
   # Client note should go to Smythson
   ls -la clients/smythson/documents/inbox-capture-*
   cat clients/smythson/documents/inbox-capture-$(date +%Y%m%d).md
   
   # Task should create todo
   ls -la todo/20251105-*update-budget*
   cat todo/20251105-*update-budget*
   ```

5. **Check archive:**
   ```bash
   ls -la !inbox/processed/
   # All three original files should be here
   ```

6. **Clean up test files:**
   ```bash
   # Remove test todos
   rm todo/20251105-*test-note*
   rm todo/20251105-*update-budget*
   
   # Remove test client note
   rm clients/smythson/documents/inbox-capture-$(date +%Y%m%d).md
   
   # Archive already handled by processor
   ```

### Test 5: Voice Note

1. **On iPhone:**
   - Run "Voice Note" shortcut
   - Speak: "Meeting with Devonshire Hotels went well, they're happy with performance"
   - Check transcription accuracy
   - Tap Done

2. **On Mac:**
   ```bash
   cat ~/Documents/PetesBrain/\!inbox/20251105-*-voice-note.md
   # Should see transcription
   ```

---

## Part 4: Daily Usage

### Quick Capture Workflow

**Throughout the day when ideas strike:**

1. Pull out iPhone
2. Tap "Inbox Capture" icon (or use Siri)
3. Type or dictate note
4. Done! Notification confirms

**Next morning:**
- Inbox processor runs at 8:00 AM automatically
- Notes are routed to appropriate folders
- You see them in client folders or todo list

### Client Meeting Workflow

**During client meeting:**

1. Open "Client Note" shortcut
2. Select client from list
3. Type meeting notes as you go
4. Save
5. Continue meeting

**Alternative: Voice capture**
1. Run "Voice Note" during/after meeting
2. Speak notes naturally
3. Later, add "client: ClientName" manually if needed

**After meeting:**
- Notes automatically route to client folder
- Appear in morning briefing
- Can reference in future

### Task Capture Workflow

**When something needs doing:**

1. Run "Quick Task"
2. Enter title (what needs done)
3. Enter details (context)
4. Set due date
5. Save

**Result:**
- Creates local todo file
- Creates Google Task (if integration enabled)
- Appears in your task list
- Reminder on due date

---

## Part 5: Optimization

### Tips for Faster Capture

1. **Use Siri for truly quick capture:**
   - "Hey Siri, capture inbox note"
   - Dictate the note
   - No screen needed!

2. **Create back tap shortcuts** (iPhone):
   - Settings → Accessibility → Touch → Back Tap
   - Double/Triple Tap → Shortcuts
   - Choose "Inbox Capture"
   - Now: Tap back of phone to capture!

3. **Use Control Center:**
   - Settings → Control Center
   - Add Shortcuts
   - Quick access from any screen

4. **Use Lock Screen widgets** (iOS 16+):
   - Long press Lock Screen
   - Customize → Widgets
   - Add Shortcuts
   - Capture without unlocking!

### Customize Shortcuts

**Add more clients:**
- Edit "Client Note" shortcut
- Add items to "Choose from Menu"

**Add templates:**
Create variations like:
- "Meeting Notes" (pre-formatted structure)
- "Performance Review" (includes metrics prompts)
- "Campaign Idea" (structured idea capture)

**Add automation:**
- Trigger shortcuts by time
- Trigger by location (at client office)
- Trigger by NFC tag (tap tag to capture)

### Advanced: Focus Mode Integration

**Create "Work" Focus:**

1. Settings → Focus → + → Custom
2. Name: "Work" or "Client Work"
3. Customize Lock Screen
4. Add "Inbox Capture" shortcut widget
5. Schedule: Weekdays 9am-5pm

**Now during work hours:**
- Lock screen shows capture widget
- One tap to create notes
- Optimized for work context

---

## Troubleshooting

### Files Not Appearing on Mac

**Check iCloud sync:**
```bash
# See if iCloud folder is being updated
ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/ | head -5

# Check for sync issues
brctl log --wait --shorten
```

**Force sync:**
- On Mac: Close and reopen Files app
- Kill bird process: `killall bird`
- On iPhone: Force quit Files app, reopen

**Check storage:**
- System Settings → Apple ID → iCloud
- Ensure not out of storage

### Shortcut Save Error

**"Couldn't Save File" error:**

1. Check iCloud Drive enabled in Shortcuts:
   - Settings → Shortcuts → iCloud Drive: ON

2. Grant Files & Folders access:
   - Settings → Privacy → Files and Folders → Shortcuts
   - Ensure allowed

3. Re-select save location:
   - Edit shortcut
   - Change "Save File" action
   - Re-choose destination folder

### Inbox Not Processing

**Files stay in inbox:**

```bash
# Check processor errors
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py

# Check LaunchAgent status
launchctl list | grep inbox-processor

# View logs
cat ~/.petesbrain-inbox-processor.log
cat ~/.petesbrain-inbox-processor-error.log
```

**Common issues:**
- File permissions: `chmod 644 !inbox/*.md`
- Python path wrong in LaunchAgent
- Inbox folder moved without updating paths

### Voice Note Not Transcribing

**"Couldn't Transcribe" error:**

1. Check microphone permission:
   - Settings → Privacy → Microphone → Shortcuts: ON

2. Check network (requires connection):
   - Dictation uses Apple's servers

3. Change dictation language:
   - Settings → General → Keyboard → Dictation
   - Ensure correct language selected

### Sync Taking Too Long

**Files take minutes to appear:**

1. Check WiFi/cellular connection
2. Try toggling Airplane mode
3. Restart both devices
4. Check Apple System Status (icloud.com)

**Reduce sync time:**
- Keep files small (text only, no attachments)
- Ensure good connection when capturing
- Files typically sync in 10-30 seconds

---

## Maintenance

### Weekly

**Review captured notes:**
```bash
# See what was captured this week
find ~/Documents/PetesBrain/\!inbox/processed/ -name "*.md" -mtime -7 -type f | sort

# Review any that weren't processed correctly
```

### Monthly

**Clean archive:**
```bash
# Archive older than 30 days can be removed
find ~/Documents/PetesBrain/\!inbox/processed/ -name "*.md" -mtime +30 -delete

# Or compress for long-term storage
cd ~/Documents/PetesBrain/\!inbox/processed/
tar -czf archive-$(date +%Y%m).tar.gz *.md
# Then delete originals
```

**Update client list in shortcuts:**
- Review clients list
- Add new clients to "Client Note" shortcut
- Remove old clients

### Quarterly

**Review and optimize:**
- Which shortcuts are you using most?
- Create variations of popular ones
- Remove unused ones
- Update templates

---

## Advanced Tips

### Multiple Team Members

**Each person can:**
1. Have their own iCloud account
2. Share PetesBrain-Inbox folder
3. Files sync to main Mac
4. Processor handles all notes

**Setup:**
```bash
# On Mac with shared access:
# Use shared iCloud folder or Dropbox Business
```

### Offline Capture

**Shortcuts work offline:**
- Create note without internet
- Files queue for sync
- Sync when connection returns

**Best practice:**
- Capture immediately
- Don't worry about sync
- Processor runs daily regardless

### Integration with Other Tools

**Capture from other apps:**

1. **Safari:** Share → Shortcuts → "Inbox Capture"
2. **Notes:** Copy text → Run shortcut → Paste
3. **Messages:** Long press → Share → Shortcuts
4. **Mail:** Forward email → Process inbox

---

## Next Steps

### You're Done! 🎉

You now have:
- ✅ Mobile inbox capture
- ✅ Multiple capture methods
- ✅ Siri voice commands
- ✅ Home screen shortcuts
- ✅ Automatic sync
- ✅ Daily processing

### Expand Your System

**Week 1:**
- Use it daily
- Note what works/doesn't
- Adjust shortcuts

**Week 2:**
- Add custom shortcuts for your workflow
- Set up automation
- Configure Focus modes

**Month 1:**
- Review efficiency gains
- Consider native app if needed
- Share system with team

---

## Support

### Need Help?

**Check logs:**
```bash
# Inbox processor logs
cat ~/.petesbrain-inbox-processor.log

# LaunchAgent logs  
cat ~/.petesbrain-inbox-processor-error.log
```

**Test manually:**
```bash
cd ~/Documents/PetesBrain
python3 agents/system/inbox-processor.py
```

**Common commands:**
```bash
# See recent captures
ls -lt ~/Documents/PetesBrain/\!inbox/ | head -10

# See processed archive
ls -lt ~/Documents/PetesBrain/\!inbox/processed/ | head -20

# Check iCloud sync status
brctl status
```

---

**System Active! Start capturing! 📱 → 💻 → 🎯**

