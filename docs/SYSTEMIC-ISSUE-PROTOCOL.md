# Systemic Issue Protocol

**When a structural or configuration issue is discovered in ONE location, always check if it's SYSTEMIC across all similar locations.**

---

## The Problem

**What happened (Nov 27, 2025):**
- Tasks discovered in `smythson/product-feeds/tasks.json` (wrong location)
- Fixed Smythson only on Nov 26
- **Missed the systemic check** - 15 other clients had the same issue
- Next day: discovered 16+ clients affected, 72 tasks in wrong locations

**Impact:** Task management system couldn't see tasks for most clients because they were in the wrong directory structure.

---

## The Protocol

### 1️⃣ DISCOVER: Issue Found in One Location

When you discover a structural/configuration issue in a single client or location:

```bash
# Example: Found tasks.json in wrong location for Smythson
/clients/smythson/product-feeds/tasks.json  # ❌ Wrong!
/clients/smythson/tasks.json                # ✅ Should be here
```

### 2️⃣ QUESTION: Is This Systemic?

**IMMEDIATELY ask:**
> "If this is wrong here, could it be wrong elsewhere?"

**Common systemic issues:**
- File/folder structure violations
- Configuration inconsistencies
- Missing required files
- Incorrect naming patterns
- Broken symbolic links
- Permission issues

### 3️⃣ AUDIT: Check ALL Similar Locations

**Run a system-wide audit BEFORE fixing:**

```bash
# Example: Check ALL clients for tasks.json location
find /Users/administrator/Documents/PetesBrain/clients -name "tasks.json" -type f

# Or use Python for structured analysis
python3 << 'EOF'
from pathlib import Path

clients_dir = Path("/Users/administrator/Documents/PetesBrain/clients")
issues = []

for client_dir in clients_dir.iterdir():
    if not client_dir.is_dir():
        continue

    # Check for issue pattern
    wrong_location = client_dir / "product-feeds" / "tasks.json"
    if wrong_location.exists():
        issues.append(client_dir.name)

print(f"Found {len(issues)} clients with issue:")
for client in issues:
    print(f"  - {client}")
EOF
```

### 4️⃣ DOCUMENT: Record the Scope

**Before fixing, document:**
- Total number of affected locations
- List of all affected clients/items
- Severity of each case

**Example output:**
```
SYSTEMIC AUDIT RESULTS
======================
Issue: tasks.json in wrong location (product-feeds/ instead of root)
Affected: 16 clients
Total tasks affected: 72

Clients:
- accessories-for-the-home (10 tasks)
- bright-minds (1 tasks)
- clear-prospects (4 tasks)
...
```

### 5️⃣ FIX: Migrate ALL at Once

**Create a comprehensive migration script:**

```python
#!/usr/bin/env python3
"""
Comprehensive fix for [ISSUE_NAME]
Migrates ALL affected clients/locations
"""

# 1. Create backups
# 2. Iterate through ALL affected locations
# 3. Apply fix with verification
# 4. Log results
# 5. Verify nothing was missed
```

**Key principles:**
- ✅ Backup EVERYTHING first
- ✅ Fix ALL instances in one operation
- ✅ Verify each fix individually
- ✅ Log all changes
- ✅ Final verification scan

### 6️⃣ VERIFY: Confirm Complete Resolution

**Run the audit again to ensure ZERO remaining issues:**

```bash
# Re-run the same audit command
# Should return: "0 issues found"
```

### 7️⃣ PREVENT: Update Documentation

**Add to relevant system docs:**
- Correct structure/pattern
- How to verify compliance
- Link to this protocol

---

## Real-World Example: Tasks.json Migration

### Step-by-step execution:

1. **Discover:** Found Smythson tasks in `product-feeds/tasks.json`

2. **Question:** "Are other clients affected?"

3. **Audit:**
   ```bash
   find /clients -name "tasks.json" -type f
   # Result: 16 clients affected!
   ```

4. **Document:**
   ```
   SYSTEMIC ISSUE IDENTIFIED
   - 16 clients with tasks.json in wrong location
   - 72 total tasks affected
   - Task manager cannot read these files
   ```

5. **Fix:** Created `migrate_all_client_tasks.py`
   - Backed up all 16 clients
   - Migrated 72 tasks
   - Deleted incorrect locations
   - Verified each client

6. **Verify:**
   ```bash
   find /clients -path "*/product-feeds/tasks.json"
   # Result: 0 files found ✅
   ```

7. **Prevent:** Created this protocol + updated TASK-SYSTEM docs

---

## Common Systemic Issue Patterns

### File Structure Issues
```bash
# Example patterns to check
find /clients -name "[filename].json" -type f
find /clients -type d -name "[dirname]"
ls -la /clients/*/[expected-file]
```

### Configuration Inconsistencies
```bash
# Check all client CONTEXT.md files for required fields
for client in /clients/*/CONTEXT.md; do
    grep -q "Voice Transcription Aliases" "$client" || echo "Missing: $client"
done
```

### Permission Issues
```bash
# Check file permissions across all clients
find /clients -name "tasks.json" ! -perm 644
```

### Missing Required Files
```bash
# Verify all clients have required files
for client in /clients/*/; do
    [ ! -f "$client/CONTEXT.md" ] && echo "Missing CONTEXT.md: $client"
    [ ! -f "$client/tasks-completed.md" ] && echo "Missing tasks-completed.md: $client"
done
```

---

## Checklist for Any Structural Fix

- [ ] Issue discovered in one location
- [ ] System-wide audit performed
- [ ] Total scope documented (X clients/files affected)
- [ ] Comprehensive migration script created
- [ ] Full backups created before changes
- [ ] All instances fixed in single operation
- [ ] Each fix individually verified
- [ ] Final audit confirms zero remaining issues
- [ ] Documentation updated
- [ ] This protocol followed ✅

---

## Key Principle

**"Fix one, check all, migrate everything."**

If a structural issue exists in one place, it's likely systemic. Always assume the worst-case scenario (affecting everything) and prove otherwise through auditing.

---

## Related Documentation

- `/docs/TASK-SYSTEM-COMPLETE-GUIDE.md` - Task system architecture
- `/docs/TROUBLESHOOTING.md` - General troubleshooting guide
- `/docs/BACKUP-SYSTEM.md` - Backup procedures

---

**Last Updated:** 2025-11-27
**Protocol Version:** 1.0
**Applies To:** All structural, configuration, and file system issues across PetesBrain
