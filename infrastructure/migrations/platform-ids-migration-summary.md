# Platform IDs Migration - Actual State Analysis

## Summary

**Initial expectation:** 29 deprecated MCP calls to migrate
**Reality:** Most code already uses direct Python imports, not MCP

## Current State

### 1. **Documentation References (66 instances)**
- Most deprecated references are in `.md` files (documentation, not code)
- Located in: skills, commands, CLAUDE.md, tool docs
- **Action:** Update documentation to reference `mcp__platform-ids__get_client_platform_ids`

### 2. **Direct Python Module Usage (3 instances)**
```python
from shared.platform_ids import get_client_platform_ids
```
- **This is actually BETTER than MCP for most use cases**
- Direct imports are faster (no MCP overhead)
- MCP is better for: Claude Code skills, external tools, cross-language access

### 3. **Existing Centralized MCP Usage (12 instances)**
- Already using `mcp__platform-ids__get_client_platform_ids` - correct pattern

### 4. **MCP Server Code (3 Python files)**
- The deprecated calls are in the MCP servers themselves (documentation/examples)
- Not actual functional code that needs migration

## The Real Opportunity

**NOT** mass-migration of code (it's already mostly correct).

**INSTEAD:**

### A. **Standardize Usage Pattern**

**For Python agents/scripts:**
```python
# PREFERRED (fastest, simplest)
from shared.platform_ids import get_client_platform_ids

ids = get_client_platform_ids('smythson')
```

**For Claude Code skills:**
```python
# PREFERRED (Claude can call MCP directly)
ids = mcp__platform-ids__get_client_platform_ids('smythson')
```

### B. **Update Documentation**

Update these files to reference the centralized approach:
- `.claude/CLAUDE.md` (line 340)
- `.claude/commands/weekly.md`
- `.claude/commands/client.md`
- `.claude/skills/google-ads-weekly-report/skill.md`
- `.claude/skills/smythson-deploy/skill.md`
- Tool documentation files

### C. **Add to Skills That Don't Use It Yet**

**34 MCP calls in skills** but platform IDs should be used in ALL client-specific skills.

Example: `google-ads-weekly-report` skill should start with:
```markdown
## Step 1: Get Client Platform IDs

ids = mcp__platform-ids__get_client_platform_ids('$ARGUMENTS')
```

## Decision Matrix: When to Use What?

| Context | Use | Reason |
|---------|-----|--------|
| **Python agent/script** | `from shared.platform_ids import...` | Faster, simpler, less overhead |
| **Claude Code skill** | `mcp__platform-ids__get_client_platform_ids()` | Claude can call MCP directly |
| **External tool/service** | `mcp__platform-ids__get_client_platform_ids()` | Language-agnostic API access |
| **One-off command** | `mcp__platform-ids__get_client_platform_ids()` | No import needed |

## Revised Action Plan

### ✅ DONE
1. Added platform-ids MCP server to `.mcp.json`
2. Created migration script (useful for future reference)

### 🎯 RECOMMENDED NEXT STEPS

1. **Update documentation** (10 minutes)
   - Update `.claude/CLAUDE.md` line 340
   - Update skill.md files to reference centralized version

2. **Standardize skill patterns** (30 minutes)
   - Add platform IDs fetching to top of all client-specific skills
   - Use consistent pattern across all skills

3. **Create usage guide** (15 minutes)
   - When to use MCP vs direct Python import
   - Add to infrastructure docs

### ❌ NOT NEEDED
- Mass code migration (code is already correct)
- Rollback mechanism (no changes made to functional code)
- Testing 29 changed files (only docs changed)

## Conclusion

**Your codebase is in better shape than expected!**

The "29 deprecated calls" were mostly documentation references, not functional code. The actual code already uses the correct patterns (direct Python imports for agents, MCP for skills).

The migration effort is:
- **90% documentation updates** (low risk)
- **10% standardizing skill patterns** (adding platform IDs where missing)
- **0% risky code changes** (nothing broken that needs fixing)
