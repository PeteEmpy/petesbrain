# Google Ads Client Mapping Setup

**Created**: November 5, 2025  
**Status**: ⏳ Needs Population  
**Purpose**: Map client names to Google Ads customer IDs for automated audits

---

## Why This Is Needed

The **Campaign Audit skill** needs to know which Google Ads customer ID corresponds to each client name. This allows you to say:

```
"Audit Accessories for the Home"
```

Instead of:

```
"Audit customer ID 1234567890"
```

---

## Quick Setup (5 Minutes)

### Step 1: List All Accounts

In **Claude Code** (with MCP connected), run:

```
List all my Google Ads accounts
```

This will call `mcp__google-ads__list_accounts` and show something like:

```json
{
  "accounts": [
    {
      "id": "1234567890",
      "name": "Accessories For The Home",
      "access_type": "direct",
      "is_manager": false
    },
    {
      "id": "0987654321",
      "name": "Devonshire Hotels",
      "access_type": "direct",
      "is_manager": false
    },
    ...
  ]
}
```

### Step 2: Update the Mapping File

Edit: `/Users/administrator/Documents/PetesBrain/shared/data/google-ads-clients.json`

For each client, add the `customer_id`:

```json
{
  "clients": {
    "accessories-for-the-home": {
      "customer_id": "1234567890",  // ← Add this
      "display_name": "Accessories For The Home",
      ...
    }
  }
}
```

### Step 3: Test It

Run in Claude Code:

```
Audit Accessories for the Home for last 7 days
```

The skill will now:
1. Look up "accessories-for-the-home" in the mapping file
2. Find customer ID "1234567890"
3. Query Google Ads via MCP
4. Generate comprehensive audit

---

## Alternative: Quick Population Script

If you want to automate this, I can create a Python script:

```python
# populate-google-ads-clients.py
# Calls MCP list_accounts and auto-populates the mapping file
```

Would match account names to client folders and fill in customer IDs automatically.

---

## File Location

**Mapping File**: `/Users/administrator/Documents/PetesBrain/shared/data/google-ads-clients.json`

**Structure**:
```json
{
  "_metadata": {
    "description": "Client name → Google Ads customer ID mapping",
    "last_updated": "YYYY-MM-DD"
  },
  "clients": {
    "client-slug": {
      "customer_id": "10-digit number",
      "display_name": "Client Display Name",
      "manager_id": "Optional MCC ID if managed",
      "folder_path": "clients/client-slug",
      "status": "active"
    }
  }
}
```

---

## How Skills Use This

### Before (Manual)
```
You: "Audit customer 1234567890"
```

### After (Automatic)
```
You: "Audit Accessories for the Home"
     ↓
Skill loads: google-ads-clients.json
     ↓
Finds: customer_id = "1234567890"
     ↓
Queries: mcp__google-ads__run_gaql(customer_id, query)
     ↓
Returns: Full audit with live data
```

---

## Integration Points

The mapping file is used by:

1. **google-ads-campaign-audit skill**
2. **google-ads-keyword-audit skill**
3. **gaql-query-builder skill**
4. **Future automated agents**

---

## Next Steps

### Option 1: Manual (Recommended First Time)
1. Open Claude Code
2. Say: "List all my Google Ads accounts"
3. Copy customer IDs
4. Manually update `google-ads-clients.json`
5. Test: "Audit [client name]"

### Option 2: Automated
1. Ask me to create `populate-google-ads-clients.py`
2. Run it once
3. It auto-fills the mapping file
4. Test: "Audit [client name]"

---

## Troubleshooting

### "No customer ID found for client X"
→ Check client slug matches exactly (use hyphens, lowercase)
→ Verify customer_id is populated in mapping file

### "MCP not connected"
→ Restart Claude Code
→ Check `.mcp.json` configuration
→ Verify Google Ads OAuth credentials

### "Account not accessible"
→ Verify you have access to the account
→ Check if account is managed (needs manager_id)
→ Run "List accounts" to see what's available

---

## Status

- [x] Mapping file created (`google-ads-clients.json`)
- [ ] Customer IDs populated (needs MCP call)
- [ ] Skills updated to use mapping (automatic)
- [ ] Tested with real client audit

---

**Once populated, this enables natural language audits:**

✅ "Audit Accessories for the Home"  
✅ "Show Devonshire's performance last week"  
✅ "Find wasted keywords in Smythson Search campaigns"  
✅ "Build query for Tree2MyDoor impression share"

**Ready to populate? Just say: "List all my Google Ads accounts" in Claude Code!**

