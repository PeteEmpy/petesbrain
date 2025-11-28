# Gmail OAuth Scopes - Permanent Solution

**Date:** 2025-11-28
**Issue:** Gmail API authentication scope problems causing email sync failures

---

## Problem

The email sync system kept failing with `HttpError 403 "Request had insufficient authentication scopes"` errors. This was a recurring problem that required re-authentication multiple times.

### Root Causes Identified

1. **Token created with insufficient scopes** - The `token.json` file was created with only `gmail.readonly` scope, but the scripts need both `gmail.readonly` AND `gmail.modify`
2. **Email confidence scoring too low** - Email address matches only scored 40 points, but minimum confidence threshold was 70%, causing valid emails to be rejected
3. **No documentation** - No clear guidance on which scopes are required

---

## Solution Implemented

### 1. Gmail API Scopes Required

**All Gmail-related scripts MUST use these scopes:**

```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Read emails
    'https://www.googleapis.com/auth/gmail.modify'     # Add/remove labels
]
```

**Files that use Gmail OAuth:**
- `shared/email-sync/auto_label.py` ✓ (lines 28-31)
- `shared/email-sync/sync_emails.py` ✓ (lines 30-33)
- `shared/email-sync/scan_personal_emails.py` ✓ (lines 27-30)

**DO NOT use:**
- `gmail.readonly` alone - insufficient for labeling
- `gmail.send` alone - insufficient for reading/labeling
- Any custom/reduced scope combinations

### 2. Re-authentication Process

When scope errors occur:

```bash
cd ~/Documents/PetesBrain/shared/email-sync
rm token.json  # Delete old token with wrong scopes
.venv/bin/python3 sync_emails.py  # Re-authenticate with correct scopes
```

This will open a browser OAuth flow. The new token will have both required scopes.

### 3. Email Confidence Scoring Fix **[THIS WAS THE REAL PROBLEM]**

**Changed:** Email address match confidence from 40 to 70 points

**File:** `shared/email-sync/auto_label.py` (line 155)

**Before:**
```python
confidence += 40  # Email match
```

**After:**
```python
confidence += 70  # Email match (highly reliable - increased from 40 to 70)
```

**Rationale:** Exact email matches are highly reliable and should meet the 70% confidence threshold on their own.

**Why this is permanent:**
- This is a code change in the Python file
- The file is version-controlled and won't revert unless someone explicitly changes it
- This fix addresses the ROOT CAUSE: emails from configured addresses now automatically meet the confidence threshold

### 4. Automatic Scope Verification

**Added:** Pre-flight check that runs BEFORE every email sync

**File:** `shared/email-sync/check-gmail-scopes.sh` (new file)
**Integration:** `shared/scripts/sync-emails.sh` (lines 10-13)

This check runs automatically and will FAIL the sync if scopes are wrong, forcing re-authentication with correct scopes.

### 4. Verification

Check token has correct scopes:

```bash
cd ~/Documents/PetesBrain/shared/email-sync
cat token.json | python3 -c "import json, sys; data=json.load(sys.stdin); print('Scopes:', data.get('scopes', []))"
```

Expected output:
```
Scopes: ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
```

---

## Prevent Recurrence

### For Future Development

1. **Never change Gmail scopes** - Always use both `gmail.readonly` and `gmail.modify`
2. **Document in code** - Add comment explaining why both scopes are needed
3. **Test after OAuth changes** - Always verify token has correct scopes after re-authentication
4. **Check scope mismatches** - The scripts already detect scope mismatches and warn, but delete token.json and re-auth when this happens

### Scope Documentation in Code

All Gmail OAuth scripts should include this comment:

```python
# Gmail API scopes - BOTH are required:
# - gmail.readonly: Read emails, list messages
# - gmail.modify: Add/remove labels (required for auto-labeling)
# DO NOT reduce scopes - will cause 403 errors
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]
```

---

## Testing Checklist

After any Gmail OAuth changes:

- [ ] Delete `shared/email-sync/token.json`
- [ ] Run `shared/scripts/sync-emails.sh`
- [ ] Complete OAuth browser flow
- [ ] Verify token has both scopes (see verification command above)
- [ ] Test auto-labeling works (check for 403 errors in output)
- [ ] Test email syncing works (new emails appear in client folders)

---

## Related Issues

- **Nov 28, 2025:** Paul Reilly's Gmail address not being labeled/synced
  - **Cause:** Token had wrong scopes + email confidence too low
  - **Fix:** Re-authenticated with correct scopes + increased email match confidence to 70
  - **Result:** Email successfully labeled and synced to `clients/national-design-academy/emails/`

---

## Files Modified

1. `shared/email-sync/auto_label.py` - Increased email match confidence from 40 to 70
2. `shared/email-sync/auto-label-config.yaml` - Added `paullifeofriley@gmail.com` to NDA emails
3. `shared/email-sync/token.json` - Re-created with correct scopes

---

**This solution is permanent.** As long as the scopes in the Python files remain `gmail.readonly` + `gmail.modify`, and the token is created with these scopes, the authentication will work correctly.
