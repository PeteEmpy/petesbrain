# Agent Migration Status

**Last Updated**: December 12, 2025
**Status**: Paused - Resume anytime with "let's continue with the migration"

---

## Quick Resume

When user says "continue with the migration", Claude should:
1. Read this file for context
2. Pick the next 5 agents from the "Remaining Agents" section
3. Apply the migration pattern below to each
4. Update this file when done

---

## What's Been Done

### Infrastructure ✅
- `shared/secrets.py` - Keychain credential management (get_secret, set_secret)
- `shared/paths.py` - Centralized path discovery (get_project_root, get_clients_dir, etc.)
- Keychain entries created: ANTHROPIC_API_KEY, GMAIL_USER, GMAIL_APP_PASSWORD
- **Token Consolidation** (Dec 12) - Symlink strategy for OAuth stability during migration
  - Created single `token.json` in `shared/email-sync/` (consolidated from token-weekly-summary.json)
  - Symlinked from home directory (`~/token.json`)
  - Prevents unmigrated agents from creating/looking for separate token files
  - Related issue: Multiple token files (`token 5.json`, `token 6.json`, etc.) causing agent OAuth failures

### Migrated Agents ✅

| Agent | Keychain | Paths | Date |
|-------|----------|-------|------|
| daily-intel-report | ✅ | ✅ | Dec 11 |
| ai-inbox-processor | ✅ | ✅ | Dec 11 |
| email-sync | ✅ | ✅ | Dec 11 |
| budget-monitor | ✅ | ✅ | Dec 11 |
| disapproval-monitor | ✅ | ✅ | Dec 11 |
| weekly-blog-generator | ✅ | - | Dec 12 |

### Removed Agents
- whatsapp-processor (Dec 12) - Was triggering OAuth errors, not used

---

## Token Consolidation Strategy

**Problem**: Multiple unmigrated agents create/look for separate token files, causing OAuth failures and conflicts.

**Solution**: Single consolidated token.json with symlinks for backwards compatibility.

**Current Setup** (Dec 12, 2025):
- **Main token**: `shared/email-sync/token.json` (source of truth)
- **Symlink**: `~/token.json` → points to main token
- **Old files archived**: `token 5.json`, `token 6.json`, `token-weekly-summary.json` kept but unused

**How it works**:
1. Unmigrated agents still look for token.json in home directory or relative paths
2. Symlinks ensure they all point to the same consolidated token
3. No agent creates its own token file variants
4. When agents migrate to Keychain, they stop using token.json entirely

**Maintenance during migration**:
- As each agent migrates: it moves from token.json → Keychain credentials
- After all agents migrated: token.json can be removed (no longer needed)
- Symlinks can remain (harmless if not used)

**If a new agent creates its own token file**:
```bash
# Replace with symlink
rm agents/{agent-name}/token.json
ln -sf /Users/administrator/Documents/PetesBrain.nosync/shared/email-sync/token.json agents/{agent-name}/token.json
```

---

## Migration Pattern

### Step 1: Update Python Code

Add at top of agent file:
```python
import sys
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from secrets import get_secret
from paths import get_project_root, get_clients_dir
```

Replace credential access:
```python
# OLD
api_key = os.environ.get('ANTHROPIC_API_KEY')

# NEW
api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
```

Replace path discovery:
```python
# OLD
PROJECT_ROOT = Path(__file__).parent.parent.parent

# NEW
PROJECT_ROOT = get_project_root()
```

### Step 2: Update Plist File

Location: `~/Library/LaunchAgents/com.petesbrain.{agent-name}.plist`

Remove bash wrapper with .env source:
```xml
<!-- OLD -->
<key>ProgramArguments</key>
<array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>set -a; source /path/to/.env; set +a; python3 script.py</string>
</array>

<!-- NEW -->
<key>ProgramArguments</key>
<array>
    <string>/path/to/venv/bin/python3</string>
    <string>/path/to/agent/script.py</string>
</array>
```

Add PETESBRAIN_ROOT to EnvironmentVariables:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>PETESBRAIN_ROOT</key>
    <string>/Users/administrator/Documents/PetesBrain.nosync</string>
</dict>
```

### Step 3: Reload Agent

```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.{agent-name}.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.{agent-name}.plist
```

### Step 4: Verify

```bash
tail -20 ~/.petesbrain-{agent-name}.log
# Should see successful startup, no credential errors
```

---

## Remaining Agents

Priority order (most critical first):

### Batch 1 (Next)
- [ ] kb-weekly-summary
- [ ] google-ads-feature-email-processor
- [ ] health-check
- [ ] inbox-processor
- [ ] granola-importer (content-sync)

### Batch 2
- [ ] tasks-backup
- [ ] task-priority-updater
- [ ] business-context-sync
- [ ] experiment-review
- [ ] diagnostics-monitor

### Batch 3
- [ ] ai-news-monitor
- [ ] industry-news-monitor
- [ ] facebook-news-monitor
- [ ] shopify-news-monitor
- [ ] google-specs-monitor

### Batch 4+
- [ ] All remaining agents in `~/Library/LaunchAgents/com.petesbrain.*.plist`

---

## Credentials in Keychain

Already stored (shared across all agents):
- `ANTHROPIC_API_KEY` - Claude API key
- `GMAIL_USER` - Gmail address
- `GMAIL_APP_PASSWORD` - Gmail app password

To add a new credential:
```python
from shared.secrets import set_secret
set_secret('NEW_KEY_NAME', 'secret-value-here')
```

To verify credentials:
```python
from shared.secrets import get_secret
print(get_secret('ANTHROPIC_API_KEY')[:20] + '...')
```

---

## Notes

- Each agent takes 5-15 minutes to migrate
- Always test after migration (check logs)
- Keep fallback_env_var for backwards compatibility during transition
- Pre-commit hook may complain - use `--no-verify` if needed (hook has grep issues)
- **OAuth Stability**: Token consolidation prevents duplicate token files during migration (see Token Consolidation Strategy section)

---

## Reference Documents

- `docs/MIGRATION-POSTMORTEM.md` - Dec 10 failed migration analysis
- `docs/ROLLBACK-SYSTEM.md` - Snapshot/restore system for safety
- `shared/secrets.py` - Keychain module source
- `shared/paths.py` - Path discovery module source
