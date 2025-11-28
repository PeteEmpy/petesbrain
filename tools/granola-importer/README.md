# Granola Meeting Importer

Automatically imports meeting notes and transcripts from Granola AI into your client folders, and generates daily to-do lists from meeting action items.

## Features

### Meeting Import
- **Fully automated**: Background sync daemon runs continuously
- **Dual content**: Saves both AI-enhanced notes and full transcripts
- **Smart client detection**: Auto-matches meetings to client folders by title + content
- **De-duplication**: Tracks imported meetings to avoid duplicates
- **Organized storage**: Files saved to `clients/[client-name]/meeting-notes/`
- **Metadata rich**: Includes date, participants, duration in YAML frontmatter
- **📧 Email summaries**: Weekly reports of all imported meetings (optional)
- **🚨 Real-time alerts**: Notifications for unassigned meetings and errors (optional)

### Daily Task Generation (NEW!)
- **✅ Automatic to-do lists**: Creates Google Tasks from meeting action items
- **📅 Daily sync**: Runs every morning at 8am automatically
- **🏢 Client-organized**: Tasks grouped by client with full meeting context
- **🧠 Smart extraction**: Identifies tasks assigned to you from "Action Items" sections
- **📝 Rich context**: Each task includes meeting title, date, and file location

## Installation

```bash
cd tools/granola-importer

# Create virtual environment
python3 -m venv venv

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

## Setup

The importer reads Granola credentials from your local system:
```
~/Library/Application Support/Granola/supabase.json
```

No additional configuration needed - the tool automatically locates your Granola installation.

## Usage

### Start Background Sync

```bash
python3 sync_daemon.py
```

This will:
1. Check for new Granola meetings every 5 minutes
2. Auto-detect which client each meeting belongs to
3. Save notes to the appropriate `clients/[client-name]/meeting-notes/` folder
4. Log all imports to `.import_history.json`

### Manual Import

To import a specific meeting:

```bash
python3 import_meeting.py --meeting-id "abc123"
```

To import all meetings from the last 7 days:

```bash
python3 import_meeting.py --days 7
```

## File Naming Convention

```
YYYY-MM-DD-meeting-title-[client-slug].md
```

Example:
```
2025-10-28-q4-strategy-review-bright-minds.md
```

## Client Detection

The tool uses **3-tier intelligent detection** (most accurate → least accurate):

### 1. Email Domain Detection (Primary - Most Accurate!) 🎯
Matches attendee email domains to clients:

- **Manual mappings** (highest priority): Define custom domain → client mappings in `domain_mappings.yaml`
  - Example: `collaber.agency` → `tree2mydoor` (contractors/agencies)
- **Automatic matching**: Fuzzy matches email domains to client names
  - `alexclarke@smythson.com` → `clients/smythson/`
  - `mike@accessoriesforthehome.co.uk` → `clients/accessories-for-the-home/`

**Best Practice**: Use Granola's folder feature to organize meetings by client. The attendee emails automatically map to clients!

### 2. Title-Based Detection (Secondary)
Fuzzy string matching against meeting titles:

- "Bright Minds Q4 Review" → `clients/bright-minds/`
- "Uno Lighting Design Discussion" → `clients/uno-lighting/`

### 3. Content-Based Detection (Fallback)
Analyzes meeting content (notes + transcript) for client mentions:

- Counts client name mentions
- Uses phrase matching
- Analyzes first 1000 characters

**Example:**
- Title: "Weekly Strategy Call" (generic)
- Content: "We discussed the Bright Minds campaign..."
- Result: `clients/bright-minds/` via content

### Custom Domain Mappings

If a client uses a different email domain than their company name, add it to `domain_mappings.yaml`:

```yaml
# Format: "email-domain": "client-folder-name"
"collaber.agency": "tree2mydoor"  # Contractors working for Tree2MyDoor
"agency-name.com": "client-slug"  # Another example
```

After editing, restart the daemon:
```bash
launchctl restart com.petesbrain.granola-importer
```

### Unassigned Meetings

If no detection method finds a match, meetings are saved to:
```
clients/_unassigned/meeting-notes/
```

You can then manually move them to the correct client folder.

## Output Format

Each imported meeting creates a Markdown file with:

```markdown
---
granola_id: abc123xyz
date: 2025-10-28
time: 14:30
duration: 45 minutes
participants: ["John Smith", "Jane Doe"]
client: bright-minds
imported_at: 2025-10-28T15:45:00Z
---

# Meeting Title

## AI-Enhanced Notes

[Granola's AI-generated summary and notes]

---

## Full Transcript

**[14:30:00] John Smith:**
Let's start with the Q4 review...

**[14:31:15] Jane Doe:**
Great, I have the numbers ready...

```

## Troubleshooting

### Credentials Not Found

If the tool can't find your Granola credentials:
```bash
ls -la ~/Library/Application\ Support/Granola/
```

Ensure `supabase.json` exists. If not, log into Granola desktop app first.

### Client Not Detected

Check client folder names:
```bash
ls clients/
```

Client names must match the lowercase-with-dashes format (e.g., `bright-minds`, not `Bright Minds`).

## Running as a Service (macOS)

To run the sync daemon on startup:

```bash
./install_service.sh
```

This creates a LaunchAgent that starts the daemon when you log in.

To stop the service:
```bash
launchctl stop com.petesbrain.granola-importer
```

## Email Notifications (Optional)

Get weekly summaries and real-time alerts delivered to your inbox!

### Quick Setup

```bash
# 1. Copy config template
cp config.example.yaml config.yaml

# 2. Edit config.yaml with your email settings
# (See EMAIL_SETUP.md for detailed instructions)

# 3. Test email
source venv/bin/activate
python3 send_weekly_summary.py

# 4. Schedule weekly emails (every Monday at 9 AM)
./setup_weekly_email.sh
```

**Features:**
- 📊 **Weekly Summary**: Every Monday, get a report of all meetings imported
- 🚨 **Unassigned Alerts**: Instant notification when a meeting can't be auto-assigned
- ⚠️ **Error Alerts**: Get notified if the sync daemon fails

**See [EMAIL_SETUP.md](EMAIL_SETUP.md) for complete email configuration guide.**

## Logs

View daemon activity:
```bash
tail -f ~/.petesbrain-granola-importer.log
```

View weekly email logs:
```bash
tail -f ~/.petesbrain-granola-weekly-email.log
```

Check import history:
```bash
cat .import_history.json
```

## Daily Task Generator

The Daily Task Generator automatically creates to-do lists in Google Tasks from meeting action items.

### Features

- Scans meetings from the last 7 days
- Extracts action items assigned to "Peter:" or general team tasks
- Creates organized tasks in Google Tasks by client
- Includes meeting context (title, date, file path) in task notes
- Runs automatically every morning at 8:00 AM

### Setup

**See [DAILY_TASKS_SETUP.md](DAILY_TASKS_SETUP.md) for complete setup instructions.**

Quick start:

```bash
# 1. Restart Claude Code to load Google Tasks MCP server

# 2. Install the LaunchAgent for automatic daily execution
cp com.petesbrain.dailytasks.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist

# 3. Test manual run
source venv/bin/activate
python3 generate_daily_tasks.py
```

### How It Works

1. **Scans meetings**: Finds all meetings from the last 7 days
2. **Extracts action items**: Looks for "Action Items", "Next Steps", "Action Points" sections
3. **Filters for you**: Identifies tasks with "Peter:" prefix or general team tasks
4. **Creates Google Tasks**: Organizes tasks by client with full meeting context

### Example Output

```
================================================================================
DAILY TASK GENERATOR - Scanning recent meetings for action items
================================================================================

📅 Scanning meetings from the last 7 days...
   ✓ Found 3 recent meetings

🔍 Extracting action items for Peter...
   • smythson: Paid Search catch up (2025-10-28)
      Found 4 action item(s)
   • tree2mydoor: Gareth & Peter PPC Channel Meet (2025-10-27)
      Found 2 action item(s)

   ✓ Total action items found: 6

================================================================================
CREATING TASKS IN GOOGLE TASKS
================================================================================

✓ Successfully created 6 tasks
```

### Configuration

**Change scan period** (default: 7 days):

Edit `generate_daily_tasks.py`:
```python
meetings = get_recent_meeting_notes(days=14)  # Scan last 14 days
```

**Change schedule** (default: 8:00 AM):

Edit `com.petesbrain.dailytasks.plist`:
```xml
<key>Hour</key>
<integer>9</integer>  <!-- Change to 9 AM -->
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.dailytasks.plist
```

### Logs

View daily task generator logs:
```bash
tail -f daily-tasks.log
tail -f daily-tasks-error.log
```

Check backup JSON file:
```bash
cat daily-tasks.json
```
