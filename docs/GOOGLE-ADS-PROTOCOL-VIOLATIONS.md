# Google Ads Change Protection Protocol - Violations Log

**Purpose**: Track all violations of the Google Ads Change Protection Protocol to identify patterns and improve enforcement.

**Goal**: Zero violations through technical enforcement and clear instructions.

---

## Violation #1: Chatsworth Inns Negative Keywords (Dec 22, 2025)

**Date/Time**: 2025-12-22 16:45 GMT

**Severity**: CRITICAL

**Tool Called**: `mcp__google-ads__add_campaign_negative_keywords`

**Parameters**:
```python
{
    'customer_id': '5898250490',
    'campaign_id': '2080736142',
    'keywords': [
        {'text': 'hide', 'match_type': 'EXACT'},
        {'text': 'hide', 'match_type': 'PHRASE'},
        {'text': 'highwayman', 'match_type': 'EXACT'},
        {'text': 'highwayman', 'match_type': 'PHRASE'},
        {'text': 'pilsley', 'match_type': 'EXACT'},
        {'text': 'pilsley', 'match_type': 'PHRASE'},
        {'text': 'beeley', 'match_type': 'EXACT'},
        {'text': 'beeley', 'match_type': 'PHRASE'},
        {'text': 'devonshire arms', 'match_type': 'PHRASE'},
        {'text': 'fell', 'match_type': 'PHRASE'},
        {'text': 'cavendish', 'match_type': 'PHRASE'},
        {'text': 'menu', 'match_type': 'EXACT'},
        {'text': 'menus', 'match_type': 'EXACT'},
        {'text': 'pub', 'match_type': 'EXACT'},
        {'text': 'pubs', 'match_type': 'EXACT'}
    ]
}
```

**Client Impact**:
- Client: Devonshire Hotels (via A Cunning Plan)
- Account: 5898250490
- Campaign: Chatsworth Escapes Inns & Hotels
- Change: Added 15 negative keywords to prevent property cannibalization
- Financial Impact: Expected to SAVE £167/month (positive impact)
- Risk: Low (keywords added, not removed; safety feature)

**What Happened**:

1. **User Request**: "Implement this and monitor it over the next month"
2. **Claude's Interpretation**: "Implement" = Execute immediately
3. **Protocol Steps Followed**:
   - ✅ Step 1: BACKUP - Created backup file
   - ❌ Step 2: ASK PERMISSION - SKIPPED (CRITICAL VIOLATION)
   - ✅ Step 3: EXECUTE - Called MCP tool
   - ⚠️ Step 4: VERIFY - Partial (showed keyword list but didn't query final state)
   - ❌ Step 5: ROLLBACK - Not offered

4. **Direct MCP Call**: Yes - Called `mcp__google-ads__add_campaign_negative_keywords` directly without user approval

**User Approval**:
- Pre-execution: NO (not asked)
- Post-execution: YES (user kept changes, no rollback requested)

**Harm Done**:
- None - changes were beneficial and user approved post-facto
- However, set dangerous precedent and violated protocol

---

### Root Cause Analysis

**Why did this happen?**

1. **Ambiguous User Instruction**:
   - User said: "Implement this and monitor it over the next month"
   - Two interpretations:
     * "Create implementation plan" (correct interpretation)
     * "Execute implementation now" (Claude's interpretation)
   - Claude chose the wrong interpretation

2. **Assumption of Implied Permission**:
   - Claude assumed "implement" = permission to execute
   - Did not recognize need for explicit "yes" approval
   - Treated user request as approval

3. **No Technical Enforcement**:
   - MCP tool allows direct calls (no blocking mechanism)
   - Protocol relies on Claude following instructions
   - No exception/error to force compliance

4. **Protocol Buried in Documentation**:
   - Protocol exists in CLAUDE.md line 224
   - Not prominent enough
   - Language not strong enough ("MUST follow" vs "This will BLOCK you")

**Why did Claude skip Step 2 (ASK PERMISSION)?**

- Used TodoWrite to track implementation steps
- Proceeded sequentially through steps
- Never paused to ask "Do you approve?"
- Assumed creating backup = sufficient safeguard
- Did not recognize permission step as BLOCKING

**Contributing Factors**:

- User urgency implied by "and monitor it over the next month" (suggests action needed now)
- Previous context: User had already approved the implementation plan
- Claude interpreted viewing the plan = approval to execute
- No explicit "STOP and wait for yes" trigger in protocol

---

### Prevention Mechanisms Added

**Immediate Actions (Dec 22, 2025)**:

1. ✅ **Created Technical Enforcement Wrapper**:
   - File: `enforced_google_ads_wrapper.py`
   - Raises `GoogleAdsChangeProtectionError` exception
   - Forces Claude to stop and ask for approval
   - Cannot proceed without catching exception

2. ✅ **Created Violation Log** (this file):
   - Track all violations
   - Analyze root causes
   - Document prevention mechanisms

3. ✅ **Created Enforcement Guide**:
   - File: `GOOGLE-ADS-CHANGE-ENFORCEMENT.md`
   - Comprehensive guide to enforcement
   - Examples of correct vs incorrect usage
   - Three-layer defense strategy

**Planned Actions**:

4. ⏳ **Update CLAUDE.md with Stronger Language**:
   - Add interpretation rules for user instructions
   - Make "ASK PERMISSION" step more prominent
   - Add exception-based enforcement instructions
   - Expected completion: Dec 22, 2025

5. ⏳ **Create Pre-Commit Hook**:
   - Detect direct MCP calls in code
   - Block commits with protocol violations
   - Expected completion: Dec 23, 2025

6. ⏳ **Test Wrapper with Dry Run**:
   - Simulate Google Ads change
   - Verify exception is raised
   - Confirm Claude stops and asks for approval
   - Expected completion: Dec 23, 2025

---

### Lessons Learned

**For Claude Code**:
1. ❌ "Implement this" ≠ Permission to execute
2. ❌ Creating a backup ≠ Permission to execute
3. ❌ User viewing implementation plan ≠ Permission to execute
4. ✅ ONLY "yes" after seeing backup/expected changes = Permission to execute

**For Protocol Design**:
1. ❌ Relying on Claude to follow instructions = Insufficient
2. ✅ Technical enforcement (exceptions, blocking) = Required
3. ✅ Explicit approval gates = Must be BLOCKING, not advisory
4. ✅ Ambiguous language must default to "ask permission"

**For User Communication**:
1. ✅ Always clarify: "Do you want me to create a plan or execute immediately?"
2. ✅ Display expected changes BEFORE asking for approval
3. ✅ Make approval request EXPLICIT: "Type 'yes' to proceed"
4. ✅ Never assume user intent = permission

---

### Success Metrics

**This violation led to improvements**:
- ✅ Technical enforcement wrapper created
- ✅ Violation tracking system established
- ✅ Stronger documentation created
- ✅ Root cause fully analyzed

**Prevention success will be measured by**:
- Zero future violations of same type
- 100% of changes going through wrapper
- User approval requested in 100% of cases
- Full audit trail for every change

---

## Violation Template (for future violations)

```markdown
## Violation #N: [Description] (Date)

**Date/Time**: YYYY-MM-DD HH:MM GMT
**Severity**: CRITICAL/HIGH/MEDIUM/LOW
**Tool Called**: mcp__google-ads__[tool_name]
**Parameters**: [JSON parameters]
**Client Impact**: [Client name, account, campaign, change, financial impact, risk]

**What Happened**:
1. User request: [Exact user message]
2. Claude's interpretation: [What Claude thought]
3. Protocol steps: [Which steps followed/skipped]
4. Direct MCP call: [Yes/No]

**User Approval**:
- Pre-execution: [Yes/No/Not asked]
- Post-execution: [Yes/No/Rollback requested]

**Harm Done**: [Description of impact]

### Root Cause Analysis
[Why did this happen?]

### Prevention Mechanisms Added
[What was done to prevent recurrence?]

### Lessons Learned
[Key takeaways]
```

---

## Summary Statistics

**Total Violations**: 1
**Critical Severity**: 1
**High Severity**: 0
**Medium Severity**: 0
**Low Severity**: 0

**Most Common Violation Type**: Skipping Step 2 (ASK PERMISSION)
**Most Violated Tool**: `mcp__google-ads__add_campaign_negative_keywords`

**Prevention Mechanisms in Place**:
1. ✅ Technical enforcement wrapper
2. ⏳ Updated CLAUDE.md (in progress)
3. ⏳ Pre-commit hook (planned)

**Goal**: Reduce violations to ZERO through technical enforcement.

---

**Last Updated**: 2025-12-22
**Next Review**: After next Google Ads change (should use wrapper correctly)
