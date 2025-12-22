# No External Attribution Policy

**Status:** ACTIVE (December 16, 2025)
**Scope:** ALL production code, documentation, prompts, and client-facing content

---

## Policy Statement

**PetesBrain does NOT include external educator, course, or teaching framework attributions in production code, documentation, or prompts.**

All strategic approaches, frameworks, and methodologies are presented as:
- "Industry best practices"
- "Proven optimization frameworks"
- "Professional campaign structure approaches"
- "Industry-standard methodologies"

---

## Rationale

### Why This Policy Exists

1. **Professional Independence** - Roksys is an independent consultancy with 22+ years of PPC experience
2. **IP Clarity** - Avoids external attribution confusion in proprietary systems
3. **Client Perception** - Clients engage Roksys for expertise, not third-party frameworks
4. **Documentation Simplicity** - Cleaner, more maintainable codebase without external references

### What Changed (December 16, 2025)

**Comprehensive cleanup completed:**
- **30 production files cleaned** (code, documentation, skills, agents, tools, UI)
- **Mike Rhodes / 8020brain references** removed from all production work
- **Historical/archival documents** intentionally preserved for accurate record-keeping

---

## Implementation Rules

### ❌ PROHIBITED in Production

**NEVER include in production code, documentation, or prompts:**

```markdown
# ❌ WRONG - External attribution
"Based on Mike Rhodes' teaching from 8020brain.com"
"Using [Educator Name]'s framework for..."
"[Course Name] approach to campaign structure"
"As taught in [Course]..."
```

### ✅ CORRECT Alternatives

**ALWAYS use generic industry language:**

```markdown
# ✅ CORRECT - Industry best practices
"Based on industry best practices"
"Using proven optimization framework"
"Professional campaign structure approach"
"Industry-standard methodology"
"Established PPC principles"
```

---

## Scope Definitions

### Production Files (NO external attribution)

**Clean of all external references:**
- Python code files (`.py`)
- Documentation (`.md`)
- Skills (`.claude/skills/`)
- Agents (`agents/`)
- Tools (`tools/`)
- UI/HTML files
- Configuration files
- Prompts and templates
- Client-facing content

### Historical/Archival Files (Preserve references)

**External references ALLOWED ONLY in:**
- Documents ABOUT past integrations (e.g., `MIKE-RHODES-INTEGRATION-PLAN.md`)
- Historical meeting notes documenting actual events
- Archive directories (`docs/archive/`, `_backups/`, `_archive/`)
- System logs recording actual email subjects/senders
- Git history (already committed)

**Rationale:** These document actual historical events and should remain accurate.

---

## Cleaning Process (Completed December 16, 2025)

### Files Cleaned

| Category | Files | Method |
|----------|-------|--------|
| Production Documentation | 10 files | Manual + Python script |
| Production Code | 2 files | Manual editing |
| Skills | 4 files | Python batch script |
| Agents | 7 files | Python batch script |
| Client CONTEXT | 2 files | Python batch script |
| Tools | 3 files | Python batch script |
| Miscellaneous | 1 file | Manual |
| HTML/UI | 1 file | Manual |
| **TOTAL** | **30 files** | ✅ Complete |

### Replacement Patterns Used

All cleaning scripts used consistent regex patterns:

```python
replacements = [
    (r'Mike Rhodes[\'"]?\s*', ''),
    (r'8020[Bb]rain\.com', 'industry best practices'),
    (r'8020[Bb]rain', 'industry resources'),
    (r'\s*\(?based on 8020brain\.com\)?', ''),
    (r'Based on Mike Rhodes[\'"]?\s+["\']?([^"\']+)["\']?\s+teaching', r'Based on \1 principles'),
    (r'Mike Rhodes[\'"]?\s+["\']?([^"\']+)["\']?\s+from 8020brain', r'\1'),
    (r'from Mike Rhodes[\'"]?\s+8020brain', 'from industry best practices'),
    (r'Mike Rhodes Integration', 'Updated Framework'),
    (r'Mike Rhodes Approach', 'Updated Approach'),
]
```

### Cleaning Scripts (Available for Future Use)

Reusable Python scripts saved in `/tmp/`:
1. `/tmp/clean-mike-rhodes-refs.py` - Documentation files
2. `/tmp/clean-skills-refs.py` - Skills files
3. `/tmp/clean-agents-refs.py` - Agent files
4. `/tmp/clean-context-refs.py` - CONTEXT files
5. `/tmp/clean-tools-refs.py` - Tools files

**Usage:** Modify file paths and patterns as needed for future cleanups.

---

## Verification Protocol

### Before Committing New Code/Documentation

**Checklist:**
1. ✅ Search for educator/trainer names
2. ✅ Search for course names or frameworks
3. ✅ Search for educational resource URLs
4. ✅ Check code comments for attributions
5. ✅ Verify prompts use generic language

**Quick grep check:**
```bash
grep -r "Mike Rhodes\|8020brain\|[Educator Name]" /path/to/new/files
```

### If External Attribution Found

**Immediate action required:**
1. Stop work immediately
2. Replace with neutral "industry best practices" language
3. Verify no other references in the file
4. Document the change in commit message
5. Run full verification grep

---

## Examples: Before & After

### Code Comments

```python
# ❌ BEFORE (External attribution)
# Based on Mike Rhodes' "Calculated Metrics" teaching from 8020brain.com
# This module implements proper metric aggregation

# ✅ AFTER (Industry best practices)
# Based on industry-standard metric aggregation principles
# This module implements proper metric aggregation
```

### Documentation

```markdown
❌ BEFORE (External attribution)
## Mike Rhodes Integration Complete

This framework implements Mike Rhodes' approach to campaign audits
from 8020brain.com...

✅ AFTER (Industry best practices)
## Updated Analysis Framework

This framework implements proven campaign audit methodologies
using industry best practices...
```

### UI/HTML

```html
<!-- ❌ BEFORE (External attribution) -->
<p>Mike Rhodes-style strategic recommendations</p>

<!-- ✅ AFTER (Industry best practices) -->
<p>In-depth strategic recommendations</p>
```

---

## Enforcement

### Claude Code Instructions

**Added to global `.claude/CLAUDE.md`:**
```markdown
## 🚨 MANDATORY: No External Attribution Policy

**CRITICAL: NEVER include external educator or course attributions
in production code, documentation, or prompts.**
```

### Code Review

**Before merging new code:**
1. Automated grep check for common patterns
2. Manual review of comments and documentation
3. Verify prompts use generic language

### Future Development

**New developers/agents must:**
1. Read this policy document
2. Understand the rationale
3. Follow the checklist before committing
4. Use provided cleaning scripts if needed

---

## Historical Context

### Why Mike Rhodes Specifically?

**Background:**
- October-November 2025: Integrated Mike Rhodes' 8020brain teaching frameworks
- Used in campaign audit system, calculated metrics, inbox processing
- 30+ production files contained attributions

**December 16, 2025 Decision:**
- Decided to remove all external educator attributions
- Preserve content and methodology, remove attribution
- Maintain professional independence

**Result:**
- 30 production files cleaned
- 12 historical/archival files preserved
- No loss of functionality or content
- Cleaner, more maintainable codebase

---

## Related Documentation

- `/Users/administrator/.claude/CLAUDE.md` - Global Claude Code instructions (policy enforcement)
- `docs/INCIDENTS.md` - Historical incident record
- `/tmp/clean-*-refs.py` - Cleaning scripts (reference)

---

## Contact & Questions

**Policy Owner:** Peter Empson (Roksys)
**Last Updated:** December 16, 2025
**Status:** ACTIVE - Enforced in all new development

**Questions?** Review this document and global CLAUDE.md instructions.

---

## Audit Trail

| Date | Action | Files Affected |
|------|--------|----------------|
| 2025-12-16 | Initial policy implementation | 30 production files cleaned |
| 2025-12-16 | Global CLAUDE.md updated | Added mandatory policy section |
| 2025-12-16 | Documentation created | This file created |

**Next Review:** Annual (December 2026) or as needed for new external frameworks
