# Git Operations Agent (githuby)

**Version:** 1.0
**Created:** 2025-11-19
**Status:** Active
**Based on:** Mike Rhodes githuby.md pattern

---

## Purpose

Handle all git operations with mandatory fetch-first protocol and automatic automation commit recognition. Prevents merge conflicts, handles divergences intelligently, and auto-merges LaunchAgent automation commits without user prompting.

## What It Does

- **Mandatory Fetch-First**: ALWAYS runs `git fetch --all` before ANY operation (Step 0 is non-negotiable)
- **Automation Pattern Recognition**: Auto-recognizes PetesBrain's LaunchAgent commits and merges without prompting
- **Divergence Handling**: Detects when local/remote have diverged, auto-handles automation commits
- **Conflict Resolution**: Intelligently resolves common conflicts (timestamps, version updates)
- **Branch Management**: Handles Claude-created branches from mobile sessions

## Mandatory Protocol

**Step 0 is NON-NEGOTIABLE:**

```bash
git fetch --all
git status
git branch -a
```

This MUST run before processing ANY request, regardless of what the user asked for. Even if user says "commit and push", you MUST fetch first.

## Automation Commit Patterns (PetesBrain-Specific)

These commit patterns are automatically recognized and merged without prompting:

```python
AUTOMATION_PATTERNS = [
    "Automated: Email sync results",
    "Automated: KB update from",
    "Automated: Weekly blog post",
    "Automated: Meeting notes imported",
    "Automated: Task completion logged",
    "Automated: Daily intel report",
    "Automated: Google Docs import",
    "Automated: Weekly summary generated",
    "Automated: Granola meeting import",
    "Automated: Facebook specs update",
    "Automated: Google specs update"
]
```

When these are detected in remote commits, the agent AUTOMATICALLY runs:
```bash
git pull --rebase origin main
```

**No user prompt required** - these are safe automated commits.

## Usage

### Basic Operations

```bash
# Sync with remote (auto-handles divergences)
python3 agents/githuby/githuby.py --sync

# Commit all changes with message
python3 agents/githuby/githuby.py --commit "Your commit message"

# Commit and push in one operation
python3 agents/githuby/githuby.py --commit-and-push "Your commit message"

# Handle divergence (checks for automation commits)
python3 agents/githuby/githuby.py --handle-divergence

# Check status (always fetches first)
python3 agents/githuby/githuby.py --status
```

### Advanced Operations

```bash
# Resolve conflicts in specific files
python3 agents/githuby/githuby.py --resolve-conflicts file1.py file2.md

# Clean up merged branches
python3 agents/githuby/githuby.py --cleanup-branches

# Handle Claude mobile branch
python3 agents/githuby/githuby.py --merge-claude-branch <branch-name>
```

## How It Works

### Workflow for ANY Operation

1. **Step 0 (MANDATORY):** `git fetch --all`, `git status`, `git branch -a`
2. **Check divergence:** Compare local vs remote
3. **Auto-handle automation:** If remote has automation commits, auto-merge
4. **Proceed with requested operation:** Only after Steps 1-3

### Example: Commit and Push

```
User: "Commit my changes and push"

Agent workflow:
1. git fetch --all              ← MANDATORY Step 0
2. git status                   ← Check current state
3. git branch -a                ← See all branches
4. Check divergence:
   - origin/main is 1 ahead: "Automated: Task completion logged"
   - Pattern recognized! Auto-merge.
5. git pull --rebase origin main
6. git add .
7. git commit -m "User's message"
8. git push origin main
9. Done!
```

### Example: Handle Divergence

```
User: "Sync with remote"

Agent workflow:
1. git fetch --all              ← MANDATORY Step 0
2. git status                   ← Local: 2 commits ahead
3. git log origin/main..HEAD    ← What's local only
4. git log HEAD..origin/main    ← What's remote only
5. Check remote commits:
   - "Automated: Weekly blog post" ← Auto-merge pattern!
   - "Automated: Meeting notes imported" ← Auto-merge pattern!
6. git pull --rebase origin main (NO PROMPT)
7. git push origin main
8. Report: "Rebased 2 local commits on top of 2 remote automation commits"
```

## Safety Features

**Pre-flight checks:**
- Verify correct branch (usually main)
- Check for uncommitted changes (stash if needed)
- Verify no sensitive data (.env, tokens, credentials)
- Ensure commit messages are descriptive

**Conflict resolution strategy:**
- Timestamps/dates: Choose newer version
- Version numbers: Choose higher version
- File renames: Keep new name
- Auto-generated files: Accept incoming changes

**Never auto-merge:**
- User-created commits (only automation commits)
- Breaking changes or refactors
- Conflicts in critical files

## Automation Pattern Detection

```python
def is_automation_commit(message: str) -> bool:
    """Check if commit message matches automation pattern"""
    return any(message.startswith(pattern) for pattern in AUTOMATION_PATTERNS)

def handle_divergence():
    """Handle divergence between local and remote"""
    # Get remote commits
    remote_commits = get_commits("origin/main", "main")

    # Check if all remote commits are automation
    if all(is_automation_commit(c.message) for c in remote_commits):
        # Safe to auto-merge
        run("git pull --rebase origin main")
        print("✅ Auto-merged automation commits (no conflicts)")
        return True
    else:
        # Has user commits, need to review
        present_divergence(remote_commits)
        return False
```

## Integration with PetesBrain

This agent is specifically tuned for PetesBrain's automation patterns:

- **LaunchAgents**: 35+ agents that commit automatically on schedule
- **Email sync**: Commits sync results every 6 hours
- **KB updates**: Commits from news monitors and specs processors
- **Meeting imports**: Granola and Wispr Flow imports commit automatically
- **Task logging**: Task completion logs commit automatically

All these patterns are recognized and auto-merged.

## Example Scenarios

### Scenario 1: Morning Sync

```
You start work in the morning. Overnight, LaunchAgents ran:
- Daily intel report (committed at 6am)
- KB update from news monitor (committed at 8am)
- Weekly blog post generation (committed at 7am)

You run: python3 agents/githuby/githuby.py --sync

Agent:
1. Fetches all
2. Detects 3 remote automation commits
3. AUTO-MERGES without prompting
4. Reports: "Synced 3 automation commits from overnight runs"
5. Done in 5 seconds!
```

### Scenario 2: Commit After Work

```
You've made changes to client CONTEXT.md files all day.
You run: python3 agents/githuby/githuby.py --commit-and-push "Update client contexts"

Agent:
1. Fetches all (mandatory)
2. Detects remote has "Automated: Email sync results" (2pm sync)
3. AUTO-MERGES automation commit
4. Stages your changes
5. Commits with your message
6. Pushes everything
7. Reports: "Merged 1 automation commit + pushed your changes"
```

### Scenario 3: Conflict Resolution

```
You and an automation agent both modified the same file.

Agent:
1. Fetches all
2. Attempts rebase
3. Conflict detected in data/state/tasks-state.json
4. Recognizes this is a state file (accepts incoming/newer)
5. Resolves automatically
6. Continues rebase
7. Pushes successfully
8. Reports: "Resolved 1 conflict (state file: accepted incoming)"
```

## When to Use

Use this agent when you need to:
- ✅ Sync with remote before starting work
- ✅ Commit and push changes without merge conflicts
- ✅ Handle divergences from overnight automation
- ✅ Resolve conflicts intelligently
- ✅ Clean up after merged branches

Don't use when:
- ❌ Just checking git status (use `git status` directly - it's faster)
- ❌ Making complex git workflows (use git commands directly)

## Configuration

Environment variables:
- None required (uses system git)

Dependencies:
- Git 2.x+
- Python 3.9+

## Output Location

Logs saved to:
- Console output (real-time)
- Git commit history (permanent record)

## Related Documentation

- Phase 6 Analysis: `.claude/skills/csv-analyzer/phase-6-analysis.md`
- Mike Rhodes githuby agent: `/Users/administrator/Documents/brain/.claude/agents/githuby.md`
- Git workflow: `docs/GIT-WORKFLOW.md` (if exists)

## Success Criteria

A successful git operation:
- Step 0 executed first (fetch + status + branches)
- Automation commits auto-merged without prompting
- User changes committed with descriptive messages
- Remote synced successfully
- No merge conflicts
- Clear status report to user

## Maintenance

- Update AUTOMATION_PATTERNS as new LaunchAgents are added
- Refine conflict resolution strategies based on common conflicts
- Add new automation sources as they're created

---

**Last Updated:** 2025-11-19
**Maintainer:** Peter Empson / Claude Code
**Priority:** Medium (Priority 3 implementation from Phase 6)
