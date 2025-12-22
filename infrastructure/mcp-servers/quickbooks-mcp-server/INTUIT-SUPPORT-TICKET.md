# QuickBooks OAuth Issue - Support Ticket

**Date**: 2025-12-19
**Severity**: High - Blocking MCP Server Integration
**App Name**: Roksys Reporting
**App ID**: 7c5b9497-fe3d-4845-9170-007d99e5bb48
**Developer Email**: [Your email here]

---

## Problem Summary

OAuth 2.0 authentication completes successfully, but **all QuickBooks API calls return 401 "Authorization Failure"** errors, even when using tokens generated via the official OAuth 2.0 Playground.

---

## Error Details

### Error Code
- **HTTP Status**: 401
- **Error Code**: 120 (AuthorizationFault)
- **Message**: "Authorization Failure"

### Full API Response
```json
{
  "Fault": {
    "Error": [{
      "Message": "Authorization Failure",
      "Detail": "AuthorizationFailure: {0}, statusCode: {1}",
      "code": "120"
    }],
    "type": "AuthorizationFault"
  }
}
```

---

## What We've Tried

### ✅ Successfully Completed:

1. **Created QuickBooks Developer App**
   - App Name: "Roksys Reporting"
   - Environment: Production
   - Status: Active
   - Scopes: com.intuit.quickbooks.accounting (enabled)

2. **OAuth 2.0 Playground Testing**
   - ✅ OAuth flow completes successfully
   - ✅ Tokens generated for correct company (Rok Systems, ID: 4038212550)
   - ✅ Access Token and Refresh Token received
   - ✅ Tokens valid (60 minutes remaining)
   - ❌ **API calls with these tokens return 401 errors**

3. **Multiple Authentication Attempts**
   - Tried Development credentials
   - Tried Production credentials
   - Re-authenticated 10+ times
   - Used tokens from OAuth Playground
   - Manually verified Company ID (4038212550)

4. **Configuration Verification**
   - ✅ Redirect URI configured: `http://localhost:8000/callback` (Development)
   - ✅ Accounting scope enabled
   - ✅ Credentials match between app and code
   - ✅ Environment set to "production"

### ❌ Issues Encountered:

#### Issue #1: OAuth Auto-Selects Wrong Company
- When using local OAuth flow (via redirect), it consistently selects **Company ID: 9341455649204247**
- This is NOT the desired company "Rok Systems Ltd" (ID: 4038212550)
- OAuth does not show company selection dropdown during authorization
- Expected behavior: Show dropdown to select which company to authorize

#### Issue #2: Production App Redirect URI Validation
- Production app won't accept `http://localhost:8000/callback` redirect URI
- Error: "Please enter a unique valid redirect URI"
- Development app accepts this URI without issues
- This prevents local OAuth testing with Production credentials

#### Issue #3: 401 Errors with Valid Tokens
- Even tokens generated via OAuth Playground return 401 errors
- Tokens are valid (not expired)
- Tokens are for correct company (Rok Systems - 4038212550)
- Credentials match Production app
- **API calls still fail with Authorization Failure**

---

## Current Configuration

### App Details
- **App Name**: Roksys Reporting
- **App ID**: 7c5b9497-fe3d-4845-9170-007d99e5bb48
- **Workspace**: Rok Systems
- **Environment**: Production

### Production Credentials
- **Client ID**: AB8LdLwfbfrplyk6iuxxnh3XcIgtG9UjzkI3xiQB6VHNTDMpZb
- **Client Secret**: V4Qb6Y0TFDEnlWgNYNhQpkckuBfo7ixPnVRh5LYq
- **Redirect URI**: https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl (Playground)
- **Scope**: com.intuit.quickbooks.accounting

### Token Details (from OAuth Playground)
- **Access Token**: Valid (59 minutes remaining)
- **Refresh Token**: Valid (101 days remaining)
- **Realm ID**: 4038212550 (Rok Systems Ltd)
- **Token Type**: bearer

### API Endpoints Tested
All return 401 errors:

1. **Company Info**
   ```
   GET https://quickbooks.api.intuit.com/v3/company/4038212550/companyinfo/4038212550
   Headers:
     Authorization: Bearer [valid_access_token]
     Accept: application/json
     Content-Type: application/json
   ```

2. **Profit & Loss Report**
   ```
   GET https://quickbooks.api.intuit.com/v3/company/4038212550/reports/ProfitAndLoss
   ```

---

## Questions for Intuit Support

1. **Why do tokens generated via OAuth Playground return 401 errors?**
   - The Playground shows successful authorization
   - Tokens are valid and not expired
   - Realm ID matches target company (4038212550)

2. **Why doesn't OAuth show company selection dropdown?**
   - User has multiple companies in QuickBooks account
   - OAuth auto-selects Company ID 9341455649204247
   - Expected: Dropdown to choose "Rok Systems Ltd" (4038212550)

3. **Why won't Production app accept localhost redirect URI?**
   - Development app accepts `http://localhost:8000/callback`
   - Production app shows validation error for same URI
   - Error: "Please enter a unique valid redirect URI"

4. **Does Production app require additional approval/verification?**
   - Is app status "IN DEVELOPMENT" blocking API access?
   - Does app need to be published or verified?
   - Are there additional permissions required?

5. **Is there a configuration issue with the app or QuickBooks company?**
   - Company settings blocking API access?
   - App missing required permissions?
   - Account-level restrictions?

---

## Expected Behavior

1. OAuth should show company selection dropdown
2. User selects "Rok Systems Ltd" (ID: 4038212550)
3. Tokens generated for selected company
4. API calls with tokens return data (200 OK)

---

## Actual Behavior

1. OAuth auto-selects wrong company (9341455649204247)
2. Manually updating Realm ID to 4038212550
3. API calls return 401 Authorization Failure
4. Even OAuth Playground tokens fail with 401

---

## Technical Environment

- **OAuth Flow**: Authorization Code
- **Token Storage**: File-based (token.json)
- **API Base URL**: https://quickbooks.api.intuit.com/v3
- **Environment**: production (not sandbox)
- **Python Version**: 3.13
- **Libraries**:
  - requests 2.32.3
  - intuitlib 0.4.3

---

## Files Available for Review

We have complete server code ready for review if needed:
- MCP server implementation (`server.py`)
- OAuth module (`oauth/quickbooks_auth.py`)
- Test scripts
- Complete logs

---

## Business Impact

This is blocking integration of QuickBooks financial data into our AI-powered business intelligence system. The MCP server code is complete and tested - only OAuth authorization is preventing deployment.

---

## Request

Please help us resolve the 401 Authorization Failure issue so we can:
1. Successfully make API calls with valid tokens
2. Connect to the correct QuickBooks company (Rok Systems)
3. Deploy the MCP server integration

**Preferred Contact Method**: [Email/Phone]
**Availability**: [Your availability]
**Urgency**: High - Integration project blocked

---

## Additional Notes

- Willing to schedule screen share session to demonstrate issue
- Can provide real-time logs during OAuth flow
- Happy to test any suggested configuration changes
- App is for internal use only (not public marketplace)

---

**Thank you for your assistance!**
