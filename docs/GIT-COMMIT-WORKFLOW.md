# Git Commit Workflow

**Problem:** 2,294 uncommitted files accumulated over December 2025.

**Root Cause:** No clear workflow for when/what to commit during rapid development.

---

## 🎯 **Decision Framework: When to Commit**

### ✅ **ALWAYS COMMIT (System Changes)**

**Commit immediately after completing work:**

1. **Code changes** (agents, scripts, tools)
2. **Infrastructure updates** (MCP servers, LaunchAgents, configs)
3. **Documentation** (.claude/*, docs/*)
4. **Deprecated file deletions** (google-tasks-mcp-server, wispr-flow-importer)
5. **Architecture changes** (task system, agent refactors)

**Example commit flow:**
```bash
# Complete Phase 3 Task Manager
git add shared/task-manager/ .claude/skills/task-manager/
git commit -m "feat: Complete Task Manager Phase 3"
git push origin main
```

---

### ⚠️ **REVIEW BEFORE COMMIT (Client Data)**

**Check for sensitive data first:**

1. **Client CONTEXT.md updates** (platform IDs are public references, but review)
2. **tasks-completed.md files** (historical work records - usually safe)
3. **Client scripts** (deployment scripts, analysis tools)

**Review workflow:**
```bash
# Check what changed in CONTEXT.md
git diff clients/smythson/CONTEXT.md

# If only platform IDs/voice aliases changed → safe to commit
# If contains sensitive strategy → DO NOT commit

# Commit batch of client updates
git add clients/*/CONTEXT.md clients/*/tasks-completed.md
git commit -m "docs: Update client context and task archives"
```

---

### ❌ **NEVER COMMIT (Runtime/Temporary Data)**

**Keep these local only:**

1. **Cache files** (`data/cache/*.json`, `clients/data/cache/*`)
2. **State files** (`agents/*/data/trends-state.json`)
3. **Dated deliverables** (`DEPLOY-MONDAY-*.csv`, `weekly-report-2025-12-*.html`)
4. **Meeting notes** (`clients/*/meeting-notes/*` - contain client conversations)
5. **Client reports** (`clients/*/reports/*.html` - one-time deliverables)

**These are already in .gitignore or should be:**
```bash
# Add to .gitignore if needed
echo "clients/*/reports/*.html" >> .gitignore
echo "data/cache/*.json" >> .gitignore
```

---

## 📅 **Commit Frequency Guidelines**

### **Daily Commits** (End of Work Day)
- Architecture changes
- New features completed
- Bug fixes
- Documentation updates

### **Weekly Commits** (Friday)
- Client CONTEXT.md updates (batch)
- tasks-completed.md archives (batch)
- Deprecated file cleanup

### **On-Demand Commits** (Immediately)
- Critical fixes
- System changes affecting other work
- Before major refactors (checkpoint)

---

## 🧹 **Cleanup Strategy for 2,294 Files**

### **Batch 1: Deprecated File Deletions (High Priority)**
```bash
# Commit all deprecated file deletions
git add -u infrastructure/mcp-servers/google-tasks-mcp-server/
git add -u agents/sync-todos-to-google-tasks/
git add -u agents/wispr-flow-importer/
git add -u infrastructure/rollback-snapshots/20251211_*/
git add -u clients/shared/

git commit -m "chore: Remove deprecated systems (Google Tasks, Wispr Flow, old snapshots)"
git push origin main
```

### **Batch 2: Documentation Updates (High Priority)**
```bash
# Commit all doc updates
git add .claude/CLAUDE.md .claude/commands/ .claude/skills/
git add docs/

git commit -m "docs: Update architecture docs and skill definitions"
git push origin main
```

### **Batch 3: Agent & Infrastructure Updates (High Priority)**
```bash
# Commit agent code changes
git add agents/
git add infrastructure/mcp-servers/microsoft-ads-mcp-server/
git add infrastructure/mcp-servers/prestashop-mcp-server/
git add .sync-config

git commit -m "refactor: Update agents and MCP servers"
git push origin main
```

### **Batch 4: Client Archives (Medium Priority)**
```bash
# Review and commit safe client updates
git add clients/*/CONTEXT.md clients/*/tasks-completed.md

git commit -m "docs: Update client context and task completion archives"
git push origin main
```

### **Batch 5: Discard Temporary Files (Cleanup)**
```bash
# Discard cache/state files
git restore data/cache/
git restore agents/tree2mydoor-search-trends/data/trends-state.json
git restore clients/data/cache/

# Delete dated deliverables (not tracked by git)
rm clients/smythson/spreadsheets/DEPLOY-MONDAY-*.csv
```

---

## 🔄 **Going Forward: Daily Workflow**

### **At End of Each Work Session:**

1. **Check status:**
   ```bash
   git status --short | wc -l  # Count uncommitted files
   ```

2. **If < 50 files:** Review and commit relevant changes
3. **If > 50 files:** Run batch commit workflow (see above)

### **Friday Routine:**

```bash
# Weekly cleanup commit
git add clients/*/CONTEXT.md clients/*/tasks-completed.md
git commit -m "docs: Weekly client updates"

# Check for deprecated files
find . -name "*deprecated*" -o -name "*old*"  # Review and delete

# Verify no accumulation
git status --short | wc -l  # Should be < 20
```

---

## 🚨 **Red Flags**

**If uncommitted files exceed 100:**
→ Stop and run batch commit workflow immediately

**If git status shows hundreds of deleted files:**
→ These are tracked deletions - commit them to clean history

**If MCP submodules show "modified content":**
→ Check if these are actual changes or local dev artifacts

---

## 📝 **Commit Message Standards**

```
feat: Add new feature
fix: Bug fix
docs: Documentation only
refactor: Code restructuring
chore: Maintenance (cleanup, deprecation)
test: Testing updates
```

**Examples:**
```bash
git commit -m "feat: Implement Task Manager Phase 3 monitoring system"
git commit -m "fix: Resolve orphaned product-feeds task files"
git commit -m "docs: Update internal task system architecture guide"
git commit -m "chore: Remove deprecated Google Tasks integration"
```

---

## ✅ **Success Criteria**

**Healthy Repository State:**
- ✅ < 50 uncommitted files at any time
- ✅ All system changes committed within 24 hours
- ✅ Client updates batched weekly
- ✅ No cache/temporary files in staging
- ✅ Deprecated files removed promptly

**Monitoring:**
```bash
# Add to ~/.zshrc or ~/.bashrc
alias gitstatus='cd ~/Documents/PetesBrain.nosync && git status --short | wc -l'

# Check daily: if > 100, time to batch commit
```
