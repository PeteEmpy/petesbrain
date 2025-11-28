

**Created:** 2025-11-12
**Status:** Planning Phase

---

## 🎯 Objective

Reorganize the PetesBrain project structure for better clarity, maintainability, and discoverability. Key goals:

1. **Self-contained agents** - Each agent in its own folder with metadata
2. **Logical grouping** - Related resources organized together
3. **Clean top level** - Remove clutter, duplicates, and archives
4. **Clear separation** - Distinct folders for agents, skills, tools, and infrastructure

---

## 📊 New Structure Overview

```
PetesBrain/
│
├── agents/                             # Automated background processes (~35 agents)
│   ├── ai-news-monitor/
│   │   ├── agent.md                    # Metadata (name, schedule, status, dependencies)
│   │   ├── ai-news-monitor.py          # Implementation
│   │   ├── config.plist                # LaunchAgent configuration
│   │   └── README.md                   # Documentation
│   └── [other agents...]
│
├── .claude/                            # Claude Code configuration (NO CHANGE)
│   ├── skills/                         # Claude-invocable workflows (~30 skills)
│   ├── settings.json
│   └── settings.local.json
│
├── tools/                              # Standalone applications (NO CHANGE)
│   └── [tool folders...]
│
├── clients/                            # Client work (NO CHANGE)
├── roksys/                             # Internal company (NO CHANGE)
├── personal/                           # Personal content (NO CHANGE)
│
├── infrastructure/                     # NEW: System infrastructure
│   ├── mcp-servers/                    # FROM: shared/mcp-servers/
│   ├── credentials/                    # FROM: shared/credentials/
│   ├── templates/                      # FROM: shared/templates/
│   └── config/                         # FROM: shared/config/
│
├── data/                               # NEW: All data files
│   ├── state/                          # FROM: shared/data/ (state/tracking files)
│   ├── exports/                        # FROM: shared/data/ (export files)
│   └── cache/                          # FROM: shared/data/ (cache files)
│
├── knowledge/                          # NEW: Reference materials
│   ├── specifications/
│   │   ├── facebook/                   # FROM: facebook-specifications/
│   │   ├── google/                     # FROM: google-specifications/
│   │   └── shopify/                    # Future
│   └── documentation/                  # FROM: docs/ (cleaned up)
│
├── output/                             # NEW: Generated outputs
│   ├── briefings/                      # FROM: briefing/ + briefing-archive/
│   │   ├── 2025-11/
│   │   └── archive/
│   └── reports/                        # Future
│
├── inbox/                              # NEW: Processing queue
│   ├── wispr-flow/                     # FROM: todo/ (wispr captures)
│   ├── voice-notes/                    # Future
│   └── screenshots/                    # Future
│
├── .config/                            # NEW: Hidden project config
│   └── venv/                           # FROM: venv/
│
├── CLAUDE.md                           # Keep (clean up duplicates)
├── README.md                           # Keep
├── .mcp.json                           # Keep (update paths)
└── .gitignore                          # Keep (update)
```

---

## 📋 Migration Steps

### Phase 1: Preparation & Backup

#### 1.1 Create Backup
```bash
# Create timestamped backup
tar -czf ~/Desktop/petesbrain-backup-$(date +%Y%m%d-%H%M%S).tar.gz \
  /Users/administrator/Documents/PetesBrain

# Verify backup
tar -tzf ~/Desktop/petesbrain-backup-*.tar.gz | head
```

#### 1.2 Document Current State
- [x] List all agents and their locations
- [x] List all LaunchAgent plist files
- [x] List all MCP server dependencies
- [ ] Create migration checklist

---

### Phase 2: Create New Structure

#### 2.1 Create New Folders
```bash
cd /Users/administrator/Documents/PetesBrain

# Create main folders
mkdir -p infrastructure/{mcp-servers,credentials,templates,config}
mkdir -p data/{state,exports,cache}
mkdir -p knowledge/{specifications/{facebook,google,shopify},documentation}
mkdir -p output/{briefings,reports}
mkdir -p inbox/{wispr-flow,voice-notes,screenshots}
mkdir -p .config
```

#### 2.2 Verify Folder Structure
```bash
tree -L 2 -d
```

---

### Phase 3: Migrate Agents (~35 agents)

#### 3.1 Agent Metadata Template

Create `agent.md` template:

```markdown
---
name: agent-name
category: content-sync|reporting|system|monitoring|tracking
schedule: "Every 6 hours" | "Daily 7:00 AM" | etc.
status: active|inactive|testing
python: /usr/local/bin/python3
dependencies:
  - anthropic
  - requests
last_updated: YYYY-MM-DD
---

# Agent Name

## Purpose
Brief description of what this agent does

## Schedule
When and how often it runs

## Configuration
- LaunchAgent: `config.plist`
- Environment variables: ANTHROPIC_API_KEY, etc.
- Log file: `~/.petesbrain-agent-name.log`

## Dependencies
Python packages and external services required

## Key Features
- Feature 1
- Feature 2

## Troubleshooting
Common issues and solutions
```

#### 3.2 Migration Process for Each Agent

**For agents in `shared/scripts/`:**

1. Create agent folder: `mkdir agents/agent-name/`
2. Move script: `mv shared/scripts/agent-name.py agents/agent-name/`
3. Copy plist: `cp ~/Library/LaunchAgents/com.petesbrain.agent-name.plist agents/agent-name/config.plist`
4. Create metadata: `agents/agent-name/agent.md`
5. Update plist path (see Phase 5)

**For agents already in `agents/category/`:**

1. Create agent folder: `mkdir agents/agent-name/`
2. Move script: `mv agents/category/agent-name.py agents/agent-name/`
3. Copy plist from `agents/launchagents/` or `~/Library/LaunchAgents/`
4. Create metadata: `agents/agent-name/agent.md`
5. Update plist path (see Phase 5)

#### 3.3 Agent List (to migrate)

**Content Sync:**
- ai-news-monitor
- industry-news-monitor
- knowledge-base-processor
- granola-google-docs-importer
- weekly-blog-generator
- facebook-news-monitor
- facebook-specs-monitor
- facebook-specs-processor
- google-specs-monitor
- google-specs-processor
- google-ads-feature-email-processor

**Reporting:**
- daily-intel-report
- kb-weekly-summary
- weekly-meeting-review (in shared/scripts)
- campaign-audit-agent
- google-ads-auditor

**System:**
- ai-inbox-processor
- inbox-processor
- tasks-monitor
- sync-todos-to-google-tasks
- health-check
- agent-dashboard

**Performance Monitoring:**
- daily-anomaly-detector
- fetch-weekly-performance
- baseline-calculator
- nda-enrolments-tracker
- trend-monitor

**Budget Tracking:**
- daily-budget-monitor (in shared/scripts)
- devonshire-budget-tracker

**Product Feeds:**
- product-monitor
- merchant-center-monitor
- label-tracker
- snapshot-product-feed
- product-data-fetcher

**And ~15 more from shared/scripts/**

---

### Phase 4: Migrate Infrastructure & Data

#### 4.1 Migrate shared/ Folder

```bash
# MCP Servers
mv shared/mcp-servers/* infrastructure/mcp-servers/

# Credentials
mv shared/credentials/* infrastructure/credentials/

# Templates
mv shared/templates/* infrastructure/templates/

# Config
mv shared/config/* infrastructure/config/

# Data - requires categorization
# (Manual sorting into state/, exports/, cache/)
```

#### 4.2 Categorize Data Files

**State files** (→ `data/state/`):
- `*-state.json`
- `*-history.json`
- `*-tracking.json`

**Export files** (→ `data/exports/`):
- `*.csv`
- Export snapshots
- Report data

**Cache files** (→ `data/cache/`):
- Temporary processing files
- Cached API responses

#### 4.3 Migrate Specifications

```bash
mv facebook-specifications/* knowledge/specifications/facebook/
mv google-specifications/* knowledge/specifications/google/
```

#### 4.4 Migrate Documentation

```bash
# Clean up docs/ and move to knowledge/documentation/
# (Manual review needed - many duplicate/outdated files)
```

#### 4.5 Migrate Briefings

```bash
mv briefing/* output/briefings/2025-11/
mv briefing-archive/* output/briefings/archive/
```

#### 4.6 Migrate Wispr Notes

```bash
mv todo/*.md inbox/wispr-flow/
```

#### 4.7 Move Virtual Environment

```bash
mv venv .config/venv
```

---

### Phase 5: Update Configurations

#### 5.1 Update LaunchAgent Plists

For each agent, update plist file:

**OLD:**
```xml
<string>/Users/administrator/Documents/PetesBrain/shared/scripts/agent-name.py</string>
```

**NEW:**
```xml
<string>/Users/administrator/Documents/PetesBrain/agents/agent-name/agent-name.py</string>
```

**Batch update script:**
```bash
cd ~/Library/LaunchAgents

for plist in com.petesbrain.*.plist; do
  # Update shared/scripts paths to agents/
  sed -i '' 's|shared/scripts/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

  # Update agents/category/ paths to agents/
  sed -i '' 's|agents/\(.*\)\.py|agents/\1/\1.py|g' "$plist"
  sed -i '' 's|agents/reporting/\(.*\)\.py|agents/\1/\1.py|g' "$plist"
  sed -i '' 's|agents/system/\(.*\)\.py|agents/\1/\1.py|g' "$plist"
  # ... etc for other categories
done
```

#### 5.2 Update .mcp.json

Update paths in `.mcp.json`:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3",
      "args": [
        "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/server.py"
      ],
      "env": {
        "CLIENT_IDS_PATH": "/Users/administrator/Documents/PetesBrain/data/state/client-platform-ids.json",
        "GOOGLE_ADS_CONFIGURATION_FILE_PATH": "/Users/administrator/google-ads.yaml"
      }
    }
  }
}
```

#### 5.3 Update Python Scripts with Hardcoded Paths

Search for hardcoded paths and update:

```bash
# Find scripts with hardcoded paths
grep -r "shared/scripts" agents/
grep -r "shared/data" agents/
grep -r "shared/mcp-servers" agents/

# Update each file (manual review recommended)
```

Common path updates:
- `shared/data/` → `data/state/` or `data/exports/`
- `shared/scripts/` → `agents/[agent-name]/`
- `shared/mcp-servers/` → `infrastructure/mcp-servers/`
- `shared/credentials/` → `infrastructure/credentials/`

---

### Phase 6: Documentation Updates

#### 6.1 Update CLAUDE.md

- Update agent structure references
- Update MCP server paths
- Update data file locations
- Remove outdated sections
- Add new structure overview

#### 6.2 Update agents/README.md

- Document new self-contained structure
- Update directory tree
- Update troubleshooting paths
- Add metadata file documentation

#### 6.3 Create New READMEs

- `infrastructure/README.md` - MCP servers, credentials, config
- `data/README.md` - Data organization, state vs exports vs cache
- `knowledge/README.md` - Specifications and documentation
- `output/README.md` - Generated outputs
- `inbox/README.md` - Processing queue

#### 6.4 Clean Up Duplicates

Delete duplicate files:
- `CLAUDE 2.md`
- `SESSION_STATUS.md` (outdated)
- `settings 2.json`, `settings 3.json`
- `.email-sync-state 2.json`, etc.
- Archive old documentation

---

### Phase 7: Testing

#### 7.1 Test LaunchAgents

```bash
# Reload all agents
launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist

# Check status
launchctl list | grep petesbrain

# Test each agent manually
launchctl start com.petesbrain.ai-news-monitor
cat ~/.petesbrain-ai-news-monitor.log
```

#### 7.2 Test MCP Servers

```bash
# Test in Claude Code
# Use mcp__ tools to verify connectivity
```

#### 7.3 Test Skills

```bash
# Launch skills via Skill tool
# Verify they can access data files
```

#### 7.4 Test Tools

```bash
cd tools/google-ads-generator
./start.sh
# Verify application launches correctly
```

---

### Phase 8: Cleanup

#### 8.1 Remove Empty Folders

```bash
# After migration, remove old folders if empty
rmdir shared/scripts 2>/dev/null
rmdir shared/data 2>/dev/null
rmdir facebook-specifications 2>/dev/null
rmdir google-specifications 2>/dev/null
rmdir briefing 2>/dev/null
rmdir briefing-archive 2>/dev/null
rmdir todo 2>/dev/null
rmdir venv 2>/dev/null

# Remove old agent category folders
rmdir agents/content-sync 2>/dev/null
rmdir agents/reporting 2>/dev/null
rmdir agents/system 2>/dev/null
# etc.
```

#### 8.2 Update .gitignore

Add new patterns:
```
.config/venv/
data/cache/
infrastructure/credentials/*.json
```

#### 8.3 Remove Archives

```bash
rm -rf _archive/  # After reviewing contents
```

---

## 📊 Migration Tracking

### Agents Migrated: 0/35
### Plists Updated: 0/35
### Data Files Sorted: 0/100+
### Documentation Updated: 0/5

---

## ⚠️ Risks & Mitigation

**Risk:** Breaking LaunchAgents during migration
**Mitigation:** Backup all plists, test one agent before migrating all

**Risk:** Losing data during file moves
**Mitigation:** Full backup before starting, use `mv` not `rm`, verify after each phase

**Risk:** MCP servers can't find new paths
**Mitigation:** Update .mcp.json carefully, test each server after update

**Risk:** Python imports break due to path changes
**Mitigation:** Search for relative imports, test scripts manually before reloading agents

---

## 🎯 Success Criteria

- [ ] All 35+ agents running successfully from new locations
- [ ] All LaunchAgent plists updated and loaded
- [ ] All MCP servers connecting properly
- [ ] All skills working correctly
- [ ] All tools launching successfully
- [ ] Documentation fully updated
- [ ] No duplicate files remaining
- [ ] Clean, logical folder structure
- [ ] All tests passing

---

## 📝 Notes

- Prioritize agents in order of importance (daily/weekly use first)
- Test thoroughly after each phase before proceeding
- Keep backup accessible until migration fully verified (48 hours)
- Document any unexpected issues or path dependencies discovered
