#!/bin/bash

# PetesBrain Overnight Migration Script
# Created: 2025-11-12
#
# This script performs the physical file migration for the restructuring
# Run after testing with 1-2 agents to ensure the process works correctly
#
# Usage: ./migrate-overnight.sh [--test-mode]
#   --test-mode: Only migrate 2 agents as a test (recommended first run)

set -e  # Exit on error
set -u  # Exit on undefined variable

PROJECT_DIR="/Users/administrator/Documents/PetesBrain"
LOG_FILE="$PROJECT_DIR/migration-$(date +%Y%m%d-%H%M%S).log"
TEST_MODE=false

# Check for test mode flag
if [[ "${1:-}" == "--test-mode" ]]; then
    TEST_MODE=true
    echo "Running in TEST MODE - will only migrate 2 agents"
fi

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

log "========================================="
log "PetesBrain Migration Script Started"
log "Test Mode: $TEST_MODE"
log "========================================="

cd "$PROJECT_DIR" || error_exit "Cannot cd to project directory"

# ============================================
# PHASE 1: Create New Folder Structure
# ============================================
log "Phase 1: Creating new folder structure..."

mkdir -p infrastructure/{mcp-servers,credentials,templates,config}
mkdir -p data/{state,exports,cache}
mkdir -p knowledge/{specifications/{facebook,google,shopify},documentation}
mkdir -p output/{briefings,reports}
mkdir -p inbox/{wispr-flow,voice-notes,screenshots}
mkdir -p .config

log "✓ New folders created"

# ============================================
# PHASE 2: Migrate Simple Folders First
# ============================================
log "Phase 2: Migrating specifications and briefings..."

# Specifications
if [ -d "facebook-specifications" ]; then
    log "Moving facebook-specifications..."
    mv facebook-specifications/* knowledge/specifications/facebook/ 2>/dev/null || true
    rmdir facebook-specifications 2>/dev/null || log "  (keeping folder, has remaining files)"
fi

if [ -d "google-specifications" ]; then
    log "Moving google-specifications..."
    mv google-specifications/* knowledge/specifications/google/ 2>/dev/null || true
    rmdir google-specifications 2>/dev/null || log "  (keeping folder, has remaining files)"
fi

# Briefings
if [ -d "briefing" ]; then
    log "Moving briefings..."
    mkdir -p output/briefings/2025-11
    mv briefing/*.md output/briefings/2025-11/ 2>/dev/null || true
    mv briefing/*.html output/briefings/2025-11/ 2>/dev/null || true
    rmdir briefing 2>/dev/null || log "  (keeping folder, has remaining files)"
fi

if [ -d "briefing-archive" ]; then
    log "Moving briefing archives..."
    mkdir -p output/briefings/archive
    mv briefing-archive/* output/briefings/archive/ 2>/dev/null || true
    rmdir briefing-archive 2>/dev/null || log "  (keeping folder, has remaining files)"
fi

# Wispr notes
if [ -d "todo" ]; then
    log "Moving wispr-flow notes..."
    mv todo/*.md inbox/wispr-flow/ 2>/dev/null || true
    rmdir todo 2>/dev/null || log "  (keeping folder, has remaining files)"
fi

# Virtual environment
if [ -d "venv" ]; then
    log "Moving virtual environment..."
    mv venv .config/venv
fi

log "✓ Simple migrations complete"

# ============================================
# PHASE 3: Migrate Infrastructure (shared/)
# ============================================
log "Phase 3: Migrating infrastructure from shared/..."

# MCP Servers
if [ -d "shared/mcp-servers" ]; then
    log "Moving MCP servers..."
    for server_dir in shared/mcp-servers/*/; do
        if [ -d "$server_dir" ]; then
            server_name=$(basename "$server_dir")
            log "  - $server_name"
            mv "$server_dir" infrastructure/mcp-servers/
        fi
    done
fi

# Credentials
if [ -d "shared/credentials" ]; then
    log "Moving credentials..."
    mv shared/credentials/* infrastructure/credentials/ 2>/dev/null || true
fi

# Templates
if [ -d "shared/templates" ]; then
    log "Moving templates..."
    mv shared/templates/* infrastructure/templates/ 2>/dev/null || true
fi

# Config
if [ -d "shared/config" ]; then
    log "Moving config..."
    mv shared/config/* infrastructure/config/ 2>/dev/null || true
fi

log "✓ Infrastructure migration complete"

# ============================================
# PHASE 4: Categorize and Migrate Data Files
# ============================================
log "Phase 4: Migrating data files from shared/data/..."

if [ -d "shared/data" ]; then
    # State files
    log "Categorizing state files..."
    mv shared/data/*-state.json data/state/ 2>/dev/null || true
    mv shared/data/*-history.json data/state/ 2>/dev/null || true
    mv shared/data/*-tracking.json data/state/ 2>/dev/null || true
    mv shared/data/client-*.json data/state/ 2>/dev/null || true
    mv shared/data/tasks-*.json data/state/ 2>/dev/null || true
    mv shared/data/wispr-*.json data/state/ 2>/dev/null || true
    mv shared/data/granola-*.json data/state/ 2>/dev/null || true

    # Export files
    log "Categorizing export files..."
    mv shared/data/*.csv data/exports/ 2>/dev/null || true

    # Cache files (if any remain)
    log "Moving remaining files to cache..."
    mv shared/data/* data/cache/ 2>/dev/null || true
fi

log "✓ Data migration complete"

# ============================================
# PHASE 5: Migrate Agents (The Big One!)
# ============================================
log "Phase 5: Migrating agents to self-contained folders..."

# Define agents to migrate
declare -a AGENTS_FROM_SCRIPTS=(
    "ai-news-monitor"
    "industry-news-monitor"
    "knowledge-base-processor"
    "weekly-meeting-review"
    "daily-budget-monitor"
    "shopify-news-monitor"
    "weekly-client-strategy-generator"
    "weekly-experiment-review"
    "weekly-news-digest"
    "devonshire-weekly-budget-optimizer"
    "file-organizer"
    "tasks-monitor"
)

declare -a AGENTS_FROM_CONTENT_SYNC=(
    "granola-google-docs-importer"
    "weekly-blog-generator"
    "facebook-news-monitor"
    "facebook-specs-monitor"
    "facebook-specs-processor"
    "google-specs-monitor"
    "google-specs-processor"
    "google-ads-feature-email-processor"
    "client-indexer"
    "knowledge-base-indexer"
)

declare -a AGENTS_FROM_REPORTING=(
    "daily-intel-report"
    "kb-weekly-summary"
    "campaign-audit-agent"
    "google-ads-auditor"
)

declare -a AGENTS_FROM_SYSTEM=(
    "ai-inbox-processor"
    "inbox-processor"
    "sync-todos-to-google-tasks"
    "health-check"
    "agent-dashboard"
    "ai-google-chat-processor"
    "google-chat-processor"
    "whatsapp-processor"
)

# Function to migrate an agent
migrate_agent() {
    local agent_name=$1
    local source_path=$2

    if [ ! -f "$source_path" ]; then
        log "  ⚠️  Skipping $agent_name (not found at $source_path)"
        return
    fi

    log "  Migrating: $agent_name"

    # Create agent folder
    mkdir -p "agents/$agent_name"

    # Move the Python script
    mv "$source_path" "agents/$agent_name/$agent_name.py"

    # Copy LaunchAgent plist if it exists
    local plist_name="com.petesbrain.$agent_name.plist"

    # Check in ~/Library/LaunchAgents first
    if [ -f ~/Library/LaunchAgents/"$plist_name" ]; then
        cp ~/Library/LaunchAgents/"$plist_name" "agents/$agent_name/config.plist"
    # Check in agents/launchagents
    elif [ -f "agents/launchagents/$plist_name" ]; then
        cp "agents/launchagents/$plist_name" "agents/$agent_name/config.plist"
    fi

    # Create basic agent.md metadata file
    cat > "agents/$agent_name/agent.md" << EOF
---
name: $agent_name
status: active
last_migrated: $(date +%Y-%m-%d)
---

# $agent_name

## Purpose
[To be documented]

## Schedule
[Check config.plist]

## Configuration
- Script: \`$agent_name.py\`
- LaunchAgent: \`config.plist\`
- Log: \`~/.petesbrain-$agent_name.log\`

## Migration Notes
Migrated on $(date +%Y-%m-%d) during project restructuring.
EOF

    log "    ✓ Created agents/$agent_name/"
}

# Migrate agents from shared/scripts
log "Migrating agents from shared/scripts/..."
if $TEST_MODE; then
    # Test mode: only migrate first 2 agents
    for agent in "${AGENTS_FROM_SCRIPTS[@]:0:2}"; do
        migrate_agent "$agent" "shared/scripts/$agent.py"
    done
    log "TEST MODE: Stopped after 2 agents"
else
    for agent in "${AGENTS_FROM_SCRIPTS[@]}"; do
        migrate_agent "$agent" "shared/scripts/$agent.py"
    done
fi

# Migrate agents from agents/content-sync
if ! $TEST_MODE; then
    log "Migrating agents from agents/content-sync/..."
    for agent in "${AGENTS_FROM_CONTENT_SYNC[@]}"; do
        migrate_agent "$agent" "agents/content-sync/$agent.py"
    done

    # Migrate agents from agents/reporting
    log "Migrating agents from agents/reporting/..."
    for agent in "${AGENTS_FROM_REPORTING[@]}"; do
        migrate_agent "$agent" "agents/reporting/$agent.py"
    done

    # Migrate agents from agents/system
    log "Migrating agents from agents/system/..."
    for agent in "${AGENTS_FROM_SYSTEM[@]}"; do
        migrate_agent "$agent" "agents/system/$agent.py"
    done
fi

log "✓ Agent migration complete"

# ============================================
# PHASE 5B: Generate agents/README.md
# ============================================
log "Phase 5B: Generating agents/README.md with agent index..."

cat > agents/README.md << 'EOFREADME'
# PetesBrain Agents

**Last Updated:** $(date +%Y-%m-%d)
**Total Agents:** $(ls -1 agents/ | grep -v README | grep -v launchagents | grep -v "^_" | wc -l | tr -d ' ')

---

## Overview

This directory contains all automated background agents (LaunchAgents) that power PetesBrain's self-improving agency infrastructure. Each agent runs on a schedule to monitor, analyze, sync, and report without manual intervention.

**Structure:** Each agent is self-contained in its own folder:
```
agents/
├── agent-name/
│   ├── agent.md              # Metadata (schedule, status, dependencies)
│   ├── agent-name.py         # Implementation
│   ├── config.plist          # LaunchAgent configuration
│   └── README.md             # Documentation (optional)
```

---

## Quick Reference

### List All Agents
```bash
ls -1 agents/ | grep -v README | grep -v launchagents
```

### Search Agent Purposes
```bash
grep -h "## Purpose" agents/*/agent.md
```

### List by Status
```bash
grep -h "status:" agents/*/agent.md | sort | uniq -c
```

### Check Running Agents
```bash
launchctl list | grep petesbrain
```

### View Agent Logs
```bash
cat ~/.petesbrain-AGENT-NAME.log
```

---

## Agent Categories

### Content Sync
Sync meetings, emails, knowledge base, and news content

- **ai-news-monitor** - Monitor AI industry RSS feeds
- **industry-news-monitor** - Monitor Google Ads industry RSS feeds
- **knowledge-base-processor** - Process and organize knowledge base content
- **granola-google-docs-importer** - Import meeting transcripts from Granola
- **weekly-blog-generator** - Generate weekly blog articles
- **facebook-news-monitor** - Monitor Facebook Ads news
- **facebook-specs-monitor** - Monitor Facebook platform specs
- **google-specs-monitor** - Monitor Google Ads platform specs
- **google-ads-feature-email-processor** - Process Google feature announcement emails

### Reporting
Generate and send automated reports and summaries

- **daily-intel-report** - Daily intelligence briefing with pre-verified tasks
- **kb-weekly-summary** - Knowledge base weekly summary email
- **weekly-meeting-review** - Weekly meeting summary email
- **campaign-audit-agent** - Weekly campaign audits (Mike Rhodes approach)
- **google-ads-auditor** - Google Ads audit templates

### System
System maintenance, inbox processing, task tracking

- **ai-inbox-processor** - AI-enhance Wispr Flow notes before routing
- **inbox-processor** - Process and route inbox captures
- **tasks-monitor** - Sync Google Tasks to CONTEXT.md
- **sync-todos-to-google-tasks** - Sync local todos to Google Tasks
- **health-check** - Monitor system health and agent status
- **agent-dashboard** - View status of all agents

### Performance Monitoring
Monitor client performance, detect anomalies

- **daily-anomaly-detector** - Detect critical performance drops
- **fetch-weekly-performance** - Fetch performance data for all clients
- **baseline-calculator** - Calculate performance baselines
- **nda-enrolments-tracker** - Track National Design Academy enrolments
- **trend-monitor** - Track Google Trends for all clients

### Budget Tracking
Monitor budgets and spending

- **daily-budget-monitor** - Monitor daily budget pacing
- **devonshire-budget-tracker** - Specialized Devonshire budget tracking

### Product Feeds
Monitor product feeds and merchant center

- **product-monitor** - Monitor product feed health
- **merchant-center-monitor** - Check Merchant Center status
- **label-tracker** - Track product label changes
- **snapshot-product-feed** - Daily product feed snapshots
- **product-data-fetcher** - Fetch product data from Google Ads

---

## Managing Agents

### Start an Agent
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Stop an Agent
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Run Agent Manually (Once)
```bash
launchctl start com.petesbrain.AGENT-NAME
# or
python3 agents/AGENT-NAME/AGENT-NAME.py
```

### Reload All Agents
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist
```

---

## Adding a New Agent

1. **Create agent folder:**
   ```bash
   mkdir agents/new-agent-name
   ```

2. **Create the script:**
   ```bash
   touch agents/new-agent-name/new-agent-name.py
   chmod +x agents/new-agent-name/new-agent-name.py
   ```

3. **Create agent.md metadata:**
   ```markdown
   ---
   name: new-agent-name
   category: content-sync|reporting|system|monitoring|tracking
   schedule: "Every 6 hours"
   status: active
   dependencies:
     - package1
     - package2
   ---

   # Agent Name

   ## Purpose
   Brief description

   ## Configuration
   - LaunchAgent: config.plist
   - Log: ~/.petesbrain-agent-name.log
   ```

4. **Create LaunchAgent plist:**
   ```bash
   # Copy template from another agent
   cp agents/ai-news-monitor/config.plist agents/new-agent-name/config.plist
   # Edit paths and schedule
   ```

5. **Install and test:**
   ```bash
   cp agents/new-agent-name/config.plist ~/Library/LaunchAgents/com.petesbrain.new-agent-name.plist
   launchctl load ~/Library/LaunchAgents/com.petesbrain.new-agent-name.plist
   launchctl start com.petesbrain.new-agent-name
   tail -f ~/.petesbrain-new-agent-name.log
   ```

6. **Update this README** with new agent in appropriate category

---

## Troubleshooting

### Agent Not Running
```bash
# Check if loaded
launchctl list | grep AGENT-NAME

# Check logs
cat ~/.petesbrain-AGENT-NAME.log
cat ~/.petesbrain-AGENT-NAME-error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Script Errors
```bash
# Run directly to see errors
cd /Users/administrator/Documents/PetesBrain
python3 agents/AGENT-NAME/AGENT-NAME.py
```

### Permission Issues
```bash
# Make executable
chmod +x agents/AGENT-NAME/AGENT-NAME.py

# Check plist
plutil -lint ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

---

## Migration Notes

**Restructured:** 2025-11-13

Previous structure had agents organized in category folders (content-sync/, reporting/, etc.).
New structure has each agent in its own self-contained folder for better organization and portability.

**Benefits:**
- Each agent is complete and portable
- Easy to add/remove agents
- Clear ownership of all files
- Better scalability (35+ agents, growing)

---

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Main project documentation
- [Automation Overview](../docs/AUTOMATION.md) - All automated workflows
- [Troubleshooting](../docs/TROUBLESHOOTING.md) - Common issues and fixes
- [Migration Plan](../RESTRUCTURE-MIGRATION-PLAN.md) - Details of 2025-11-13 restructuring

---

EOFREADME

log "✓ Generated agents/README.md"

# ============================================
# PHASE 6: Update .mcp.json
# ============================================
log "Phase 6: Creating updated .mcp.json..."

# Backup original
cp .mcp.json .mcp.json.backup-$(date +%Y%m%d-%H%M%S)

# Update paths using sed
sed -i '' 's|shared/mcp-servers/|infrastructure/mcp-servers/|g' .mcp.json
sed -i '' 's|shared/data/|data/state/|g' .mcp.json
sed -i '' 's|shared/credentials/|infrastructure/credentials/|g' .mcp.json

log "✓ .mcp.json updated (backup created)"

# ============================================
# PHASE 7: Generate plist update script
# ============================================
log "Phase 7: Generating plist update script..."

cat > update-plists.sh << 'EOF'
#!/bin/bash

# Update all LaunchAgent plists with new agent paths
# Run this manually after verifying migration worked

cd ~/Library/LaunchAgents

for plist in com.petesbrain.*.plist; do
    echo "Updating: $plist"

    # Update shared/scripts paths
    sed -i '' 's|shared/scripts/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/content-sync paths
    sed -i '' 's|agents/content-sync/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/reporting paths
    sed -i '' 's|agents/reporting/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/system paths
    sed -i '' 's|agents/system/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/performance-monitoring paths
    sed -i '' 's|agents/performance-monitoring/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/budget-tracking paths
    sed -i '' 's|agents/budget-tracking/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/product-feeds paths
    sed -i '' 's|agents/product-feeds/\(.*\)\.py|agents/\1/\1.py|g' "$plist"
done

echo "✓ Plist files updated"
echo "Run: launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist"
echo "Then: launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist"
EOF

chmod +x update-plists.sh

log "✓ Generated update-plists.sh (run manually after testing)"

# ============================================
# SUMMARY
# ============================================
log "========================================="
log "Migration Complete!"
log "========================================="
log ""
log "Next steps:"
log "1. Review migration log: $LOG_FILE"
log "2. Test 1-2 agents manually"
log "3. Run ./update-plists.sh to update LaunchAgent configs"
log "4. Reload agents: launchctl unload/load"
log "5. Test all agents"
log ""
log "Backup available at: ~/Desktop/petesbrain-backup-*.tar.gz"
log ""

if $TEST_MODE; then
    log "TEST MODE: Only 2 agents migrated"
    log "Re-run without --test-mode to migrate all agents"
fi

echo ""
echo "Migration log saved to: $LOG_FILE"
