# iOS Inbox App Integration

**Created:** November 5, 2025  
**Status:** 🚧 Planning Phase  
**Goal:** Enable quick note capture from iPhone/iPad that syncs to PetesBrain inbox

---

## Overview

Create a mobile capture system that allows you to quickly create notes on iPhone/iPad that automatically sync to the `!inbox/` folder for processing by the inbox agent.

## Current Inbox System

The existing inbox processor:
- Monitors `!inbox/` folder for `.md` files
- Processes files daily at 8:00 AM (or manually)
- Routes based on keywords: `client:`, `task:`, `knowledge:`, `email:`
- Auto-detects client names in content
- Archives processed files to `!inbox/processed/`
- Creates Google Tasks for task items

**Key requirement:** We just need to get markdown files into the `!inbox/` directory!

---

## Integration Options

### Option 1: iCloud Drive Sync ⭐ RECOMMENDED
**Complexity:** Low  
**Cost:** Free  
**Timeline:** 1-2 hours  

#### How It Works
1. Create `PetesBrain/!inbox/` folder in iCloud Drive
2. Use symlink or modify inbox processor to monitor iCloud location
3. Use native iOS Notes app or any markdown editor with iCloud support
4. Files automatically sync to Mac and get processed

#### Pros
- ✅ No app development needed
- ✅ Works immediately
- ✅ Uses native iOS features
- ✅ Zero cost
- ✅ Works on iPhone, iPad, Mac seamlessly
- ✅ Multiple app options (Notes, Drafts, iA Writer, etc.)

#### Cons
- ⚠️ Requires iCloud Drive setup
- ⚠️ Sync delay (usually seconds, but not instant)
- ⚠️ Depends on Apple ecosystem

#### Implementation Steps
1. Enable iCloud Drive on Mac
2. Create symbolic link:
   ```bash
   ln -s ~/Documents/PetesBrain/!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox
   ```
   OR
3. Move inbox to iCloud and symlink back:
   ```bash
   mv ~/Documents/PetesBrain/!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox
   ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox ~/Documents/PetesBrain/!inbox
   ```
4. On iOS: Use any markdown editor that supports iCloud Drive
5. Create notes in `PetesBrain-Inbox` folder
6. Files sync automatically and get processed at 8 AM

#### Recommended iOS Apps
- **Drafts** ($19.99/year) - Quick capture, templates, automation
- **iA Writer** ($49.99) - Beautiful markdown editor
- **Apple Notes** (Free) - Built-in, simple
- **Bear** ($29.99/year) - Clean interface, markdown support
- **Obsidian Mobile** (Free) - Full markdown vault sync

---

### Option 2: Dropbox/Google Drive Sync
**Complexity:** Low  
**Cost:** Free (with existing accounts)  
**Timeline:** 2-3 hours

#### How It Works
1. Create `PetesBrain/!inbox/` in Dropbox or Google Drive
2. Install desktop sync client on Mac
3. Modify inbox processor to monitor sync folder
4. Use mobile app to create notes

#### Pros
- ✅ Cross-platform (works on Android too)
- ✅ No app development needed
- ✅ Multiple device support
- ✅ Web access available

#### Cons
- ⚠️ Requires third-party account
- ⚠️ Sync client must be running
- ⚠️ Potential sync conflicts

---

### Option 3: Shortcuts + iCloud
**Complexity:** Low-Medium  
**Cost:** Free  
**Timeline:** 2-4 hours

#### How It Works
1. Create iOS Shortcut that:
   - Prompts for note text
   - Adds action keywords (client:, task:, etc.)
   - Saves to iCloud Drive folder
   - Names file with timestamp
2. Add to Home Screen or Siri
3. Files sync to Mac automatically

#### Pros
- ✅ No app development
- ✅ Custom UI and prompts
- ✅ Siri integration ("Hey Siri, create inbox note")
- ✅ Widget support
- ✅ Can add templates for different note types

#### Cons
- ⚠️ Limited UI customization
- ⚠️ Requires learning Shortcuts
- ⚠️ iOS only

#### Example Shortcut Flow
```
1. Show Menu: "What type of note?"
   - Client Note
   - Task
   - Knowledge
   - General Note

2. If "Client Note":
   - Ask for client name
   - Ask for note content
   - Create file: "client: {name}\n\n{content}"
   
3. If "Task":
   - Ask for task title
   - Ask for details
   - Ask for due date (optional)
   - Create file: "task: {title}\n\n{details}\n\ndue: {date}"

4. Save to iCloud Drive/PetesBrain-Inbox/{timestamp}-{type}.md

5. Show notification: "Note captured!"
```

---

### Option 4: Native iOS App (SwiftUI)
**Complexity:** High  
**Cost:** Free (development time)  
**Timeline:** 2-4 weeks

#### How It Works
1. Build native iOS app in SwiftUI
2. Use CloudKit or iCloud Drive API for sync
3. Custom UI optimized for quick capture
4. Background sync when possible

#### Pros
- ✅ Full control over UI/UX
- ✅ Native iOS experience
- ✅ Offline support with queue
- ✅ Custom features (voice notes, photos, etc.)
- ✅ App Store distribution (if desired)

#### Cons
- ❌ Requires Swift/iOS development knowledge
- ❌ Significant time investment
- ❌ Maintenance required
- ❌ Apple Developer account needed ($99/year for distribution)

#### Tech Stack
- **Frontend:** SwiftUI
- **Data:** Core Data + CloudKit
- **Sync:** iCloud Drive API or CloudKit
- **Text:** Markdown rendering
- **UI:** Native iOS components

#### Core Features
- Quick capture with templates
- Client/task type selection
- Voice-to-text notes
- Due date picker
- Offline queue
- Background sync
- Widget support
- Siri Shortcuts integration

---

### Option 5: Progressive Web App (PWA)
**Complexity:** Medium-High  
**Cost:** Free + hosting (optional)  
**Timeline:** 1-2 weeks

#### How It Works
1. Build web app that works on iPhone
2. Use Web Share API or file download
3. Options for sync:
   - Email notes to processing email
   - API endpoint that saves to inbox
   - Download files to iCloud Drive folder

#### Pros
- ✅ Works on any device (iPhone, Android, etc.)
- ✅ No App Store approval
- ✅ Web technologies (HTML/CSS/JS)
- ✅ Can be added to Home Screen
- ✅ Easier updates

#### Cons
- ⚠️ Not fully native experience
- ⚠️ Sync requires backend or email
- ⚠️ Limited offline capabilities
- ⚠️ Less integrated with iOS

---

### Option 6: Email-to-Inbox Integration
**Complexity:** Medium  
**Cost:** Free  
**Timeline:** 4-6 hours

#### How It Works
1. Set up email processing script
2. Create dedicated email address (e.g., inbox@your-domain.com)
3. Python script monitors email via IMAP
4. Extracts content and creates inbox files
5. Send notes from iPhone Mail or any email app

#### Pros
- ✅ Works from any device with email
- ✅ No special app needed
- ✅ Can forward existing emails
- ✅ Subject line = filename
- ✅ Body = content

#### Cons
- ⚠️ Email account setup
- ⚠️ Script must run continuously
- ⚠️ Less immediate than file sync
- ⚠️ Email formatting issues

#### Implementation
```python
# agents/system/email-to-inbox.py
import imaplib
import email
from pathlib import Path

def process_inbox_emails():
    # Connect to email
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('inbox@yourdomain.com', 'password')
    mail.select('INBOX')
    
    # Get unread messages
    _, messages = mail.search(None, 'UNSEEN')
    
    for msg_num in messages[0].split():
        _, msg_data = mail.fetch(msg_num, '(RFC822)')
        email_body = email.message_from_bytes(msg_data[0][1])
        
        subject = email_body['subject']
        body = get_body(email_body)
        
        # Create inbox file
        filename = f"{timestamp()}-{slugify(subject)}.md"
        save_to_inbox(filename, body)
        
        # Mark as read
        mail.store(msg_num, '+FLAGS', '\\Seen')
```

---

### Option 7: Telegram Bot Integration
**Complexity:** Medium  
**Cost:** Free  
**Timeline:** 4-8 hours

#### How It Works
1. Create Telegram bot
2. Send messages to bot
3. Bot saves to inbox folder
4. Use special commands for routing

#### Pros
- ✅ Works on any platform
- ✅ Telegram's great mobile app
- ✅ Can include photos/files
- ✅ Commands for different note types

#### Cons
- ⚠️ Requires Telegram account
- ⚠️ Bot hosting needed
- ⚠️ Not as private as local solution

#### Bot Commands
```
/client Smythson - Performance review notes
/task Update budget trackers - Check October spend
/note General idea about campaigns
/knowledge PMax works best with optimized feeds
```

---

## Recommended Implementation Path

### Phase 1: Immediate Solution (TODAY)
**Use Option 1: iCloud Drive + Shortcuts**

1. **Set up iCloud Sync (15 minutes)**
   ```bash
   # Move inbox to iCloud
   mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain
   cp -r ~/Documents/PetesBrain/!inbox ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain/inbox
   
   # Update inbox processor to check both locations
   # OR create symlink (test first!)
   ```

2. **Create iOS Shortcut (30 minutes)**
   - Quick capture with templates
   - Add to Home Screen
   - Configure Siri trigger

3. **Test with mobile markdown app (15 minutes)**
   - Install Drafts or iA Writer
   - Point to iCloud folder
   - Create test note
   - Verify sync to Mac
   - Check inbox processing

**Result:** Working mobile capture within 1 hour!

### Phase 2: Enhanced Shortcuts (WEEK 1)
**Improve Option 3 with better workflows**

1. **Create multiple shortcuts:**
   - Quick Client Note (with client picker)
   - Quick Task (with due date)
   - Voice Note to Inbox (transcription)
   - Meeting Notes Capture

2. **Add Home Screen widgets**
   - One-tap note capture
   - Different colors for different types

3. **Siri commands:**
   - "Create client note for Smythson"
   - "Add task to inbox"
   - "Capture meeting notes"

### Phase 3: Native App (MONTH 1-2) - Optional
**Only if you want premium experience**

Build native iOS app with:
- Beautiful, fast UI
- Offline support
- Voice notes with transcription
- Photo capture with OCR
- Client quick-select
- Template system
- Background sync
- Widget support

---

## Technical Specifications

### File Format Requirements

All methods must create files with:
- **Format:** Markdown (`.md`)
- **Naming:** `YYYYMMDD-HHMMSS-description.md` or any name
- **Location:** `!inbox/` folder (or synced location)
- **Content:** Plain text with optional keywords

### Keyword Syntax

```markdown
client: Smythson
Note content here...

task: Task title
Task details here...
due: 2025-11-15

knowledge: Topic Name
Knowledge content...

email Devonshire Hotels:
Email draft content...
```

### Sync Requirements

- **Frequency:** Real-time to 5 minutes acceptable
- **Reliability:** Must handle offline scenarios
- **Conflicts:** Latest-write-wins acceptable
- **Security:** Files contain client data - encryption preferred

---

## Cost Analysis

| Option | Development Cost | Ongoing Cost | Total Year 1 |
|--------|-----------------|--------------|--------------|
| **iCloud + Shortcuts** | $0 (2 hours) | $0 | **$0** ⭐ |
| **iCloud + Drafts app** | $0 (2 hours) | $19.99/year | **$20** |
| **Email Integration** | $0 (6 hours) | $0 | **$0** |
| **Telegram Bot** | $0 (8 hours) | $5/mo hosting | **$60** |
| **PWA** | $0 (40 hours) | $5/mo hosting | **$60** |
| **Native iOS App** | $0 (80 hours) | $99/year Apple | **$99** |

---

## Security Considerations

### Data Privacy
- **Client data:** Notes contain sensitive client information
- **Encryption:** iCloud uses end-to-end encryption
- **Access:** Only your devices have access
- **Sync:** Data never leaves Apple ecosystem (iCloud option)

### Best Practices
1. Use iCloud option (most secure)
2. Enable two-factor authentication
3. Don't share shortcuts publicly
4. Review archived notes periodically
5. Consider client data policies

---

## Implementation Guide: iCloud + Shortcuts

### Step 1: Set Up iCloud Folder

```bash
# On your Mac

# Option A: Symlink from PetesBrain to iCloud
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox
ln -s ~/Documents/PetesBrain/!inbox/* ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/

# Option B: Update inbox processor to monitor iCloud folder
# Edit agents/system/inbox-processor.py
INBOX_DIRS = [
    PROJECT_ROOT / '!inbox',
    Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Inbox'
]

# Test sync
touch ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Inbox/test-from-mac.md
# Check if it appears on iPhone Files app
```

### Step 2: Create iOS Shortcuts

**Shortcut 1: Quick Inbox Capture**
```
Actions:
1. Ask for Input "What do you want to capture?"
2. Get Current Date (format: YYYYMMdd-HHmmss)
3. Text = "{date}-quick-note.md"
4. Save File to: iCloud Drive/PetesBrain-Inbox/{filename}
   Content: User input
5. Show Notification "Note captured!"
```

**Shortcut 2: Client Note**
```
Actions:
1. Choose from Menu "Which client?"
   - Smythson
   - Devonshire Hotels
   - Superspace
   - [other clients]
   
2. Ask for Input "Note about {chosen client}"

3. Text Content:
   client: {chosen client}
   
   {input}
   
4. Get Current Date (format: YYYYMMdd-HHmmss)
5. Filename = "{date}-{client}-note.md"
6. Save to iCloud Drive/PetesBrain-Inbox/{filename}
7. Show Notification "Client note saved!"
```

**Shortcut 3: Quick Task**
```
Actions:
1. Ask for Input "Task title:"
2. Store as {title}

3. Ask for Input "Task details (optional):"
4. Store as {details}

5. Ask "Due date?" (Date picker)
6. Store as {due_date}

7. Text Content:
   task: {title}
   
   {details}
   
   due: {due_date formatted}
   
8. Get Current Date (format: YYYYMMdd-HHmmss)
9. Filename = "{date}-task.md"
10. Save to iCloud Drive/PetesBrain-Inbox/{filename}
11. Show Notification "Task created!"
```

**Shortcut 4: Voice Note to Inbox**
```
Actions:
1. Dictate Text
2. Store as {transcription}

3. Get Current Date (format: YYYYMMdd-HHmmss)
4. Filename = "{date}-voice-note.md"

5. Save File:
   Location: iCloud Drive/PetesBrain-Inbox/{filename}
   Content: {transcription}
   
6. Show Notification "Voice note captured!"
```

### Step 3: iOS Setup

1. **Install Shortcuts app** (pre-installed on iOS)

2. **Create shortcuts:**
   - Open Shortcuts app
   - Tap "+" to create
   - Follow action list above
   - Name and save each

3. **Add to Home Screen:**
   - Long press shortcut
   - "Add to Home Screen"
   - Choose icon and name

4. **Set up Siri:**
   - Shortcut settings
   - "Add to Siri"
   - Record phrase: "Capture inbox note"

5. **Create widgets:**
   - Long press Home Screen
   - Add Shortcuts widget
   - Choose your inbox shortcuts

### Step 4: Install Markdown App (Optional)

**Recommended: Drafts**
1. Download from App Store
2. Open Drafts
3. Settings → Storage → iCloud Drive
4. Point to `PetesBrain-Inbox` folder
5. Create templates for different note types

**Alternative: iA Writer**
1. Download from App Store  
2. Add Location → iCloud Drive
3. Navigate to `PetesBrain-Inbox`
4. Create notes directly

### Step 5: Test the System

```bash
# On Mac: Watch for new files
watch -n 5 ls -la ~/Documents/PetesBrain/\!inbox/

# On iPhone:
1. Open Shortcuts
2. Run "Quick Inbox Capture"
3. Type test message
4. Check Mac - file should appear within seconds

# Test processing:
python3 ~/Documents/PetesBrain/agents/system/inbox-processor.py
```

---

## Alternative: Markdown App Recommendations

### Best for Quick Capture: Drafts ($19.99/year)
- **Pros:** Opens instantly, customizable actions, keyboard shortcuts
- **Cons:** Subscription required
- **Best for:** Speed and automation

### Best for Writing: iA Writer ($49.99 one-time)
- **Pros:** Beautiful, distraction-free, powerful preview
- **Cons:** Higher upfront cost
- **Best for:** Longer notes and documentation

### Best for Free Option: Apple Notes (Free)
- **Pros:** Built-in, syncs perfectly, simple
- **Cons:** Not true markdown, less features
- **Best for:** Basic capture

### Best for Power Users: Obsidian Mobile (Free)
- **Pros:** Full vault sync, plugins, linking
- **Cons:** Heavier app, more complex
- **Best for:** Connected note-taking

---

## Future Enhancements

### Phase 4: Advanced Features
- [ ] Photo capture with OCR
- [ ] PDF attachment support
- [ ] Location tagging
- [ ] Contact integration (client picker from Contacts)
- [ ] Calendar integration (meeting notes auto-tagged)
- [ ] Dictation with AI enhancement
- [ ] Templates for common scenarios
- [ ] Quick client performance capture
- [ ] Expense tracking notes

### Phase 5: Intelligence
- [ ] Auto-detect client from GPS (at client office?)
- [ ] Suggested keywords based on content
- [ ] Voice command routing
- [ ] Smart templates based on time/location
- [ ] Integration with calendar for meeting notes

---

## Troubleshooting

### Files Not Syncing
1. Check iCloud Drive enabled on both devices
2. Verify iCloud storage not full
3. Check internet connection
4. Force quit and reopen Files app
5. Check file permissions

### Shortcut Not Saving Files
1. Verify iCloud Drive permission in Shortcuts
2. Check folder path is correct
3. Test with simple text file first
4. Review Shortcut error messages

### Inbox Not Processing Files
1. Run processor manually to see errors
2. Check file format (must be .md)
3. Verify file permissions
4. Check LaunchAgent is running
5. Review processor logs

---

## Next Steps

1. **Choose your approach:**
   - Start with iCloud + Shortcuts (recommended)
   - Or pick another option from list

2. **Set up infrastructure:**
   - Configure iCloud folder
   - Update inbox processor if needed
   - Test sync

3. **Create shortcuts:**
   - Quick capture
   - Client note
   - Task creation
   - Voice note

4. **Test end-to-end:**
   - Create note on iPhone
   - Verify sync to Mac
   - Run inbox processor
   - Check file routing

5. **Refine and expand:**
   - Add more shortcuts
   - Create templates
   - Configure Siri commands
   - Add widgets

---

## Questions to Consider

1. **How often do you need mobile capture?**
   - Daily? → Use shortcuts
   - Occasionally? → Just use Files app
   - Frequently? → Consider native app

2. **What types of notes most common?**
   - Client notes → Focus on client shortcuts
   - Tasks → Optimize task creation flow
   - Mixed → Create versatile general capture

3. **Do you need offline support?**
   - Yes → Native app or local-first solution
   - No → Any cloud-based option works

4. **Budget for development?**
   - $0 → iCloud + Shortcuts
   - Small → Add paid markdown app
   - Large → Native app development

---

## Recommended Action: Start Simple

**Today: iCloud + Shortcuts (1 hour)**
- Set up iCloud folder
- Create one simple shortcut
- Test on iPhone
- Refine based on usage

**This Week: Expand Shortcuts (2-3 hours)**
- Add client note shortcut
- Add task creation shortcut
- Set up Siri commands
- Add Home Screen widgets

**This Month: Evaluate**
- Is it working well?
- What's missing?
- Need native app?
- Or is current solution sufficient?

**Future: Build Native App (Optional)**
- Only if shortcuts aren't enough
- Requires significant time investment
- But offers best experience

---

## Resources

### iOS Shortcuts
- [Apple Shortcuts User Guide](https://support.apple.com/guide/shortcuts/welcome/ios)
- [Shortcuts Gallery](https://support.apple.com/en-us/HT208309)

### Markdown Apps
- [Drafts](https://getdrafts.com)
- [iA Writer](https://ia.net/writer)
- [Obsidian](https://obsidian.md)
- [Bear](https://bear.app)

### iOS Development (if going native)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [CloudKit Documentation](https://developer.apple.com/icloud/cloudkit/)
- [iCloud Drive API](https://developer.apple.com/documentation/foundation/file_system/icloud)

---

**Ready to start?** Let me know which approach you'd like to implement! 📱✨

