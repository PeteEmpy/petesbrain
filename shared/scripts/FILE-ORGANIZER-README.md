# File Organizer Skill

Comprehensive file organization and cleanup tool for PetesBrain project.

## Features

✅ **Complete File Organization**
- Organizes client folders according to standard structure
- Moves files to correct locations based on type and content
- Creates missing folder structures automatically

✅ **Duplicate Management**
- Detects name-based duplicates (files with " 2", " 3" suffixes)
- Content-based duplicate detection (MD5 hash)
- Smart duplicate resolution (keeps newer version)

✅ **Report Organization**
- Automatically organizes reports by date/quarter
- Creates subfolders: `monthly/`, `q1-YYYY/`, `q2-YYYY/`, `q3-YYYY/`, `q4-YYYY/`, `pmax-analysis/`, `ad-hoc/`
- Detects dates from filenames and content

✅ **Email Draft Detection**
- Automatically detects email drafts
- Moves to `emails/drafts/` subfolder

✅ **Content-Based Detection**
- Analyzes markdown content to detect meeting notes
- Identifies file types from content, not just extension

✅ **Product Feed Organization**
- Organizes product feed files (CSV, JSON, XML)
- Maintains proper folder structure

✅ **Broken Reference Fixing**
- Scans markdown files for broken file links
- Automatically fixes paths after file moves

✅ **Empty Folder Cleanup**
- Removes empty folders (preserves standard structure)
- Reports empty folders found

✅ **File Size Analysis**
- Identifies unusually large files (>10MB)
- Reports files that might need attention

✅ **Temporary File Cleanup**
- Removes `.tmp`, `.bak`, `.backup`, `~`, `.swp`, `.DS_Store` files
- Skips venv and __pycache__ directories

✅ **Undo Functionality**
- Saves complete action log
- Can undo previous runs with `--undo` flag

✅ **HTML Report Generation**
- Generates beautiful HTML report after each run
- Shows all actions taken with statistics

## Usage

### Ad-Hoc Execution (Skill)

```bash
# Dry run (see what would happen)
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/file-organizer.py --dry-run

# Organize all files
python3 shared/scripts/file-organizer.py

# Organize specific client only
python3 shared/scripts/file-organizer.py --client positive-bakes

# Undo last run
python3 shared/scripts/file-organizer.py --undo shared/data/file-organizer-YYYYMMDD-HHMMSS.json
```

### Using the Skill Wrapper

```bash
# From project root
./shared/scripts/organize-files.sh --dry-run
./shared/scripts/organize-files.sh --client smythson
```

### Weekly Automated Execution

The file organizer runs automatically every Monday at 8:00 AM.

**Setup:**
```bash
cd /Users/administrator/Documents/PetesBrain
./agents/launchagents/setup-file-organizer.sh
```

**Check Status:**
```bash
launchctl list | grep file-organizer
```

**View Logs:**
```bash
cat ~/.petesbrain-file-organizer.log
cat ~/.petesbrain-file-organizer-error.log
```

**Unload/Stop:**
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
```

**Reload:**
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
```

## What Gets Organized

### Client Folders
- Files moved from root to appropriate folders
- Reports organized by date/quarter
- Email drafts moved to `emails/drafts/`
- Scripts moved to `scripts/`
- Product feeds organized in `product-feeds/`

### Project Root
- Documentation files moved to `docs/`
- Client-specific files moved to appropriate client folders
- Duplicate files archived to `_archive/`

### Reports Organization
Reports are automatically organized into:
- `reports/monthly/` - Monthly reports (YYYY-MM pattern)
- `reports/q1-YYYY/`, `q2-YYYY/`, `q3-YYYY/`, `q4-YYYY/` - Quarterly reports
- `reports/pmax-analysis/` - Performance Max analysis reports
- `reports/ad-hoc/` - One-off analysis and investigations

## Action Logs

Each run creates:
1. **JSON Log**: `shared/data/file-organizer-YYYYMMDD-HHMMSS.json`
   - Complete list of all actions taken
   - Can be used for undo operations

2. **HTML Report**: `shared/data/file-organizer-YYYYMMDD-HHMMSS.html`
   - Beautiful visual report
   - Statistics and action summary
   - Open in browser to view

## Undo Functionality

To undo a previous run:
```bash
python3 shared/scripts/file-organizer.py --undo shared/data/file-organizer-YYYYMMDD-HHMMSS.json
```

This will:
- Reverse all file moves
- Restore archived duplicates
- Note: Cannot undo file deletions

## Safety Features

- **Dry Run Mode**: Always test with `--dry-run` first
- **Action Logging**: Every action is logged for undo capability
- **Preserves Important Files**: Never moves `CONTEXT.md`, `tasks-completed.md`, etc.
- **Skips System Files**: Ignores venv, __pycache__, .git directories

## Examples

### Organize Single Client
```bash
python3 shared/scripts/file-organizer.py --client smythson --dry-run
```

### Full Organization
```bash
python3 shared/scripts/file-organizer.py
```

### View Last Report
```bash
# Find latest HTML report
ls -t shared/data/file-organizer-*.html | head -1 | xargs open
```

## Integration

The file organizer integrates with:
- **tasks-monitor**: Updates file references in CONTEXT.md
- **inbox-processor**: Doesn't interfere with files being processed
- **Standard folder structure**: Follows `clients/_templates/FOLDER-STRUCTURE.md`

## Troubleshooting

**Files not being moved:**
- Check if file should stay in root (see `CLIENT_ROOT_FILES`)
- Verify file isn't currently being processed by another script
- Check error log: `~/.petesbrain-file-organizer-error.log`

**Undo not working:**
- Ensure log file path is correct
- Check that target files still exist
- Some actions (like deletions) cannot be undone

**Large files reported:**
- Files >10MB are reported but not moved
- Review manually to determine if they should be archived

## Schedule

Default schedule: **Every Monday at 8:00 AM**

To change schedule, edit the plist file:
```bash
nano ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.file-organizer.plist
```

