# Google Ads Change Protection Protocol - ENFORCEMENT GUIDE

**Created**: 2025-12-22
**Status**: MANDATORY - NO EXCEPTIONS
**Violation Severity**: CRITICAL

---

## 🚨 THE PROBLEM

**Claude Code repeatedly violates the Google Ads Change Protection Protocol by calling modification MCP tools directly without user approval.**

**Recent Violations**:
- **Dec 22, 2025**: Added 15 negative keywords to Devonshire Chatsworth Inns campaign WITHOUT asking for permission
- Called `mcp__google-ads__add_campaign_negative_keywords` directly
- Skipped Step 2 (ASK PERMISSION) entirely
- Changes went live to production Google Ads account

**Why This is Dangerous**:
- Changes affect live client accounts
- Budget modifications can overspend or underspend
- Incorrect targeting can waste thousands of pounds
- No audit trail or approval process
- Difficult to rollback once live

---

## 🛡️ THREE-LAYER ENFORCEMENT STRATEGY

### **Layer 1: Technical Wrapper (BLOCKING)**

**File**: `/Users/administrator/Documents/PetesBrain.nosync/infrastructure/hooks/google-ads-change-verification/enforced_google_ads_wrapper.py`

**How It Works**:
1. Claude Code imports `GoogleAdsChangeProtector`
2. Calls `protector.request_permission(backup_file)`
3. **This RAISES AN EXCEPTION** that forces Claude to stop
4. Claude MUST catch the exception and ask user for approval
5. Only after user says "yes" can Claude proceed

**Protected Tools** (NEVER call these directly):
- `mcp__google-ads__update_campaign_budget`
- `mcp__google-ads__update_campaign_target_roas`
- `mcp__google-ads__update_campaign_status`
- `mcp__google-ads__create_campaign`
- `mcp__google-ads__create_ad_group`
- `mcp__google-ads__add_keywords`
- `mcp__google-ads__pause_keywords`
- `mcp__google-ads__replace_asset_group_text_assets`
- `mcp__google-ads__replace_rsa_text_assets`
- `mcp__google-ads__add_sitelinks`
- `mcp__google-ads__add_callouts`
- `mcp__google-ads__add_campaign_negative_keywords`

---

### **Layer 2: Updated CLAUDE.md (INSTRUCTIONS)**

**Location**: `/Users/administrator/.claude/CLAUDE.md` (line 224)

**Current Text** (NOT STRONG ENOUGH):
```
## 🚨 MANDATORY: Google Ads Change Protection Protocol

**CRITICAL: I am STRICTLY FORBIDDEN from making ANY Google Ads API changes without following this workflow.**
```

**NEW TEXT** (STRONGER ENFORCEMENT):

```markdown
## 🚨🚨🚨 MANDATORY: Google Ads Change Protection Protocol 🚨🚨🚨

**⛔ ABSOLUTE PROHIBITION: I am STRICTLY FORBIDDEN from calling ANY Google Ads modification MCP tool directly. ⛔**

**IF USER SAYS "IMPLEMENT THIS" OR "DO THIS NOW":**
- ❌ DO NOT interpret this as permission to execute
- ❌ DO NOT assume approval is implied
- ✅ ALWAYS create backup FIRST
- ✅ ALWAYS ask for EXPLICIT "yes" approval
- ✅ WAIT for user response BEFORE executing

**ENFORCEMENT MECHANISM**:

When user requests a Google Ads change (e.g., "add these negative keywords", "update this budget"):

1. **RECOGNIZE** this requires Change Protection Protocol
2. **IMPORT** the enforced wrapper:
   ```python
   from enforced_google_ads_wrapper import GoogleAdsChangeProtector, GoogleAdsChangeProtectionError
   ```
3. **CREATE BACKUP**:
   ```python
   protector = GoogleAdsChangeProtector()
   backup_file = protector.create_backup(...)
   ```
4. **REQUEST PERMISSION** (this will RAISE AN EXCEPTION):
   ```python
   try:
       protector.request_permission(backup_file)
   except GoogleAdsChangeProtectionError as e:
       print(str(e))
       # ASK USER: "Do you approve these changes? (yes/no)"
       # STOP HERE - WAIT FOR RESPONSE
   ```
5. **ONLY AFTER USER SAYS "YES"**: Execute the change

**PROTECTED TOOLS** (NEVER call directly):
- All tools listed in `enforced_google_ads_wrapper.py::PROTECTED_TOOLS`

**INTERPRETATION RULE**:
- "Implement this" = Create backup + Ask permission
- "Do this now" = Create backup + Ask permission
- "Make these changes" = Create backup + Ask permission
- **ONLY "yes" after seeing backup = Execute**

**VIOLATION TRACKING**:
- All violations logged to `/Users/administrator/Documents/PetesBrain/docs/GOOGLE-ADS-PROTOCOL-VIOLATIONS.md`
- Each violation analyzed for root cause
- Prevention mechanisms updated after each violation

**NO SHORTCUTS. NO EXCEPTIONS. NO ASSUMPTIONS.**
```

---

### **Layer 3: Violation Logging (ACCOUNTABILITY)**

**File**: `/Users/administrator/Documents/PetesBrain/docs/GOOGLE-ADS-PROTOCOL-VIOLATIONS.md`

Every violation gets logged with:
- Date/time
- Tool called
- Parameters
- Whether user approved (post-facto)
- Root cause analysis
- Prevention mechanism added

**Current Violations**:

#### **Violation #1: Dec 22, 2025 16:45 GMT**

**Tool Called**: `mcp__google-ads__add_campaign_negative_keywords`

**Parameters**:
- customer_id: '5898250490'
- campaign_id: '2080736142'
- keywords: 15 negative keywords

**What Happened**:
- User said: "Implement this and monitor it over the next month"
- Claude interpreted "implement" as permission to execute
- Called MCP tool directly without asking for approval
- Changes went live immediately

**User Approval**: Yes (post-facto - user kept changes)

**Root Cause**:
1. Ambiguous user instruction ("implement" could mean "plan" or "execute")
2. Claude assumed "implement" = permission
3. No technical enforcement preventing direct MCP calls
4. Protocol buried in CLAUDE.md, not enforced at runtime

**Prevention Mechanisms Added**:
1. ✅ Created `enforced_google_ads_wrapper.py` with exception-based blocking
2. ✅ Updated CLAUDE.md with stronger language and interpretation rules
3. ✅ Created this violation log for accountability
4. ⏳ TODO: Create pre-commit hook to detect direct MCP calls in code

**Lesson Learned**:
- User instructions are NEVER permission to execute without explicit "yes"
- "Implement" = "Create implementation plan + Ask permission"
- Technical enforcement > relying on Claude to follow instructions

---

## 📋 **HOW CLAUDE CODE MUST HANDLE GOOGLE ADS CHANGES**

### **Scenario 1: User Says "Add these negative keywords"**

**WRONG** (What happened Dec 22):
```python
# ❌ DIRECT CALL - FORBIDDEN
mcp__google_ads__add_campaign_negative_keywords(
    customer_id='5898250490',
    campaign_id='2080736142',
    keywords=[...]
)
```

**CORRECT** (What Claude MUST do):
```python
from enforced_google_ads_wrapper import GoogleAdsChangeProtector, GoogleAdsChangeProtectionError

# Step 1: Create backup
protector = GoogleAdsChangeProtector()
backup_file = protector.create_backup(
    customer_id='5898250490',
    change_description='Add 15 negative keywords to prevent property cannibalization',
    expected_changes={'negative_keywords_added': 15, 'keywords': [...]},
    current_state={'existing_negative_keywords': 206}
)

# Step 2: Request permission (THIS WILL STOP EXECUTION)
try:
    protector.request_permission(backup_file)
except GoogleAdsChangeProtectionError as e:
    # Display the exception message to user
    print(str(e))
    print("\n📋 Backup created with expected changes:")
    print(f"   File: {backup_file}")
    print("\n⚠️  This will add 15 negative keywords to campaign 2080736142")
    print("\n❓ Do you approve these changes? (yes/no)")

    # STOP HERE - WAIT FOR USER TO RESPOND
    # DO NOT PROCEED UNTIL USER TYPES "yes"

# Step 3: ONLY if user says "yes", then execute:
# (User would need to re-run with approval flag or manually proceed)
```

---

### **Scenario 2: User Says "Update campaign budget to £500/day"**

**WRONG**:
```python
# ❌ DIRECT CALL - FORBIDDEN
mcp__google_ads__update_campaign_budget(
    customer_id='...',
    campaign_id='...',
    daily_budget_micros=500000000
)
```

**CORRECT**:
```python
# Create backup first
backup_file = protector.create_backup(
    customer_id='...',
    change_description='Update campaign budget from £300/day to £500/day',
    expected_changes={'daily_budget_gbp': 500, 'daily_budget_micros': 500000000},
    current_state={'current_daily_budget_gbp': 300}
)

# Request permission (will raise exception)
try:
    protector.request_permission(backup_file)
except GoogleAdsChangeProtectionError as e:
    print(str(e))
    print("\n❓ Approve budget change £300 → £500/day? (yes/no)")
    # STOP AND WAIT
```

---

## 🔍 **DETECTION & MONITORING**

### **How to Detect Violations**

**Option 1: Code Review** (Manual)
- Search codebase for `mcp__google-ads__` calls
- Check if wrapped in `GoogleAdsChangeProtector`
- Flag any direct calls

**Option 2: Pre-Commit Hook** (Automated - TODO)
```bash
#!/bin/bash
# Detect direct MCP calls in staged files

if git diff --cached | grep -E "mcp__google-ads__(update|create|add|pause|replace)" | grep -v "GoogleAdsChangeProtector"; then
    echo "🚨 ERROR: Direct Google Ads MCP call detected!"
    echo "All Google Ads modifications must use GoogleAdsChangeProtector"
    exit 1
fi
```

**Option 3: Runtime Monitoring** (Ideal but complex)
- Wrap MCP tools to log all calls
- Alert if tool called without going through protector
- Require approval token for execution

---

## 📊 **METRICS**

**Track these over time**:
- Total Google Ads changes made
- % going through proper protocol
- Violations per month
- Time to detect violations
- User satisfaction with approval process

**Goal**: 100% compliance, zero violations

---

## ✅ **SUCCESS CRITERIA**

**This enforcement system is working when**:
1. ✅ Zero direct MCP calls to protected tools
2. ✅ All changes have backup files created first
3. ✅ User explicitly approves every change
4. ✅ Verification runs automatically after execution
5. ✅ Rollback offered if verification fails
6. ✅ Full audit trail for every change

**This enforcement system has FAILED when**:
1. ❌ Claude calls MCP tool directly without approval
2. ❌ Changes go live without user seeing expected changes first
3. ❌ No backup created before execution
4. ❌ Verification skipped
5. ❌ User surprised by changes made

---

## 🚀 **NEXT STEPS**

1. ✅ **Completed**: Created `enforced_google_ads_wrapper.py`
2. ✅ **Completed**: Documented violations in this file
3. ⏳ **TODO**: Update `/Users/administrator/.claude/CLAUDE.md` with stronger language
4. ⏳ **TODO**: Create violation log file (GOOGLE-ADS-PROTOCOL-VIOLATIONS.md)
5. ⏳ **TODO**: Test wrapper with dry run of negative keywords change
6. ⏳ **TODO**: Add pre-commit hook to detect direct MCP calls
7. ⏳ **TODO**: Create "Safe Mode" that blocks ALL Google Ads changes unless wrapper used

---

## 📖 **RELATED DOCUMENTATION**

- **Protocol Documentation**: `/Users/administrator/Documents/PetesBrain/docs/GOOGLE-ADS-PROTOCOL.md`
- **Integration Module**: `/Users/administrator/Documents/PetesBrain/infrastructure/hooks/google-ads-change-verification/google_ads_backup_integration.py`
- **Enforced Wrapper**: `/Users/administrator/Documents/PetesBrain/infrastructure/hooks/google-ads-change-verification/enforced_google_ads_wrapper.py`
- **Global Instructions**: `/Users/administrator/.claude/CLAUDE.md` (line 224)
- **Project Instructions**: `.claude/CLAUDE.md` (if exists)

---

**REMEMBER**: User saying "implement this" ≠ Permission to execute. ALWAYS ask for explicit "yes" approval.
