# QuickBooks 403 Error - Troubleshooting Summary

**Date:** 2025-11-06  
**Error Code:** 003100 - ApplicationAuthorizationFailed  
**Status:** ❌ Blocking Issue

## Problem Summary

OAuth authentication completes successfully, but **all API calls return 403 "ApplicationAuthorizationFailed"** errors, regardless of which company we try to access.

## What We've Tried

### ✅ Successfully Completed:
1. Created QuickBooks Developer App "PetesBrain Financial Reporting"
2. Enabled Accounting scope (com.intuit.quickbooks.accounting)
3. Configured redirect URI (http://localhost:8000/callback)
4. OAuth flow completes successfully (generates tokens)
5. Tokens are valid and not expired
6. Development AND Production keys obtained (they're identical)
7. Multiple re-authentication attempts
8. Tried from incognito/private windows
9. Tried while logged into different companies
10. Manual realmId editing in token file

### ❌ Issues Encountered:

#### Issue #1: OAuth Auto-Selects Wrong Company
- OAuth consistently connects to Company ID: **9341455649204247**
- This is NOT Rok Systems Ltd (which has ID: **4038212550**)
- This is NOT Crowd Control Company either (based on Apps page)
- Likely a sandbox/test company auto-created by Intuit Developer account

#### Issue #2: 403 Errors on ALL Companies
- Company **9341455649204247** → 403 error
- Company **4038212550** (Rok Systems Ltd) → 403 error  
- Error persists with both Development and Production credentials
- Error occurs even for the company OAuth selected

## Error Details

```json
{
  "fault": {
    "error": [{
      "message": "message=ApplicationAuthorizationFailed; errorCode=003100; statusCode=403",
      "code": "3100"
    }]
  }
}
```

**Intuit Error 003100** typically means:
- App doesn't have authorization for the specific company
- App permissions/scopes not properly configured
- App needs additional verification/approval
- Company doesn't allow third-party API access

## Current State

### Credentials:
- **Client ID:** ABMRNKlEsbJdErUnarH3FvpAToMgwir1yWVM7lT3hdNWFGqO3n
- **Client Secret:** XHxB3YeBdQ2Nfg5DQ1Go4XSmBetSuV2ODwl2Fsga
- **App Status:** IN DEVELOPMENT

### Companies:
1. **Crowd Control Company** - No "PetesBrain" app shown in Apps page
2. **Rok Systems Ltd** (ID: 4038212550) - No "PetesBrain" app shown in Apps page
3. **Unknown Company** (ID: 9341455649204247) - OAuth keeps selecting this

### Token Status:
- ✓ OAuth succeeds
- ✓ Tokens generated
- ✓ Tokens valid and not expired
- ❌ API calls return 403

## Possible Root Causes

### Theory #1: Development App Limitations
Development apps might have restrictions that prevent API access even after OAuth. May need to:
- Submit app for review
- Get app approved by Intuit
- Switch to Production mode (requires app verification)

### Theory #2: Sandbox Company Issue
Company ID 9341455649204247 might be a sandbox/test company that:
- Doesn't have real API access
- Is created automatically for developers
- Can't be used for actual data access

### Theory #3: Missing App Configuration
Something in the app configuration might be missing:
- Additional permissions needed
- App needs to be "published" even for personal use
- Specific settings not configured in Developer Portal

### Theory #4: QuickBooks Account Type
The QuickBooks account might need:
- Specific subscription level
- API access enabled by Intuit
- Additional permissions granted

## Recommended Next Steps

### Option 1: Contact Intuit Developer Support
**Most Direct Solution**

1. Go to: https://help.developer.intuit.com/s/
2. Create a support ticket with:
   - App ID: 7c5b9497-fe3d-4845-9170-007d99e5bb48
   - Error Code: 003100
   - Description: OAuth succeeds but all API calls return 403
   - Attach this document

**What to Ask:**
- Why does OAuth always select Company ID 9341455649204247?
- How to authorize app for specific company (Rok Systems Ltd, ID: 4038212550)?
- Do development apps need additional approval for API access?
- Is error 003100 related to app configuration or company settings?

### Option 2: Try OAuth 2.0 Playground
**Test if Issue is with Our App or QuickBooks Account**

1. Go to: https://developer.intuit.com/app/developer/playground
2. Use QuickBooks OAuth 2.0 Playground
3. Try to connect to Rok Systems Ltd
4. If Playground works → Issue is with our app configuration
5. If Playground fails → Issue is with QuickBooks account/permissions

### Option 3: Create New App from Scratch
**Workaround Attempt**

1. Delete current app in Developer Portal
2. Create brand new app with different name
3. Use exact same configuration
4. See if fresh app has different behavior

### Option 4: Use QuickBooks API Explorer
**Verify API Access**

1. Go to: https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account
2. Click "Try it" on any endpoint
3. Select Rok Systems Ltd company
4. See if test API calls work
5. If they work → Get working credentials from there

### Option 5: Check App Compliance/Verification
**May Need App Approval**

1. In Developer Portal, check "Compliance" tab
2. See if app needs verification even for personal use
3. Check if any approval steps are required
4. Complete any pending requirements

## Workarounds (Temporary)

### Manual Data Export
While we debug the API:
1. Export reports manually from QuickBooks
2. Save as CSV/PDF
3. Process locally until API works

### QuickBooks Desktop API
If Online API continues to fail:
1. QuickBooks Desktop has different API
2. May have different authorization process
3. Consider as last resort

## Documentation to Review

1. **Intuit OAuth Guide:** https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0
2. **Error Code Reference:** https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/error-codes
3. **App Configuration:** https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app
4. **Permissions & Scopes:** https://developer.intuit.com/app/developer/qbo/docs/learn/scopes

## Technical Details for Support

### API Endpoint Tested:
```
GET https://quickbooks.api.intuit.com/v3/company/{realmId}/companyinfo/{realmId}
```

### Headers Used:
```
Authorization: Bearer {access_token}
Accept: application/json
Content-Type: application/json
```

### Response:
```json
{
  "fault": {
    "error": [{
      "message": "message=ApplicationAuthorizationFailed; errorCode=003100; statusCode=403",
      "detail": null,
      "code": "3100",
      "element": null
    }],
    "type": "SERVICE"
  }
}
```

### OAuth Flow:
1. Authorization URL generated correctly
2. User redirects to QuickBooks
3. User authorizes app
4. Callback receives authorization code
5. Code exchanged for access token (SUCCESS)
6. Tokens stored with realmId
7. API calls made with Bearer token (403 ERROR)

## Files Ready for Testing

All code is complete and ready:
- `/shared/mcp-servers/quickbooks-mcp-server/server.py` - MCP server
- `/shared/mcp-servers/quickbooks-mcp-server/oauth/quickbooks_auth.py` - OAuth module
- All dependencies installed
- Configuration files ready

**Once the 403 issue is resolved, the integration should work immediately.**

## Contact Information

**Intuit Developer Support:**
- Portal: https://help.developer.intuit.com/s/
- Community: https://help.developer.intuit.com/s/global-search/quickbooks
- Phone: Available through support portal

**App Details for Support Ticket:**
- App Name: PetesBrain Financial Reporting
- App ID: 7c5b9497-fe3d-4845-9170-007d99e5bb48
- Workspace: Sample Workspace (ID: 9341455649210685)
- Scopes: com.intuit.quickbooks.accounting
- Environment: Development (Production keys same as Development)

---

**Status:** Waiting for resolution of 403 error before proceeding with Cursor integration.

**Next Action:** Contact Intuit Developer Support with this information.

