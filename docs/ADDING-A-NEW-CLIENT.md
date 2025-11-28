# Adding a New Client - Complete Setup Guide

**Last Updated**: January 27, 2025  
**Purpose**: Comprehensive checklist for adding a new client to all systems, agents, and processes

---

## Overview

This guide documents **every step required** to fully integrate a new client into Pete's Brain. Follow this checklist to ensure the client is included in all automated processes, agent skills, and monitoring systems.

---

## Prerequisites

Before starting, gather this information:

- [ ] **Client name** (official business name)
- [ ] **Client slug** (lowercase-with-dashes format, e.g., `positive-bakes`)
- [ ] **Primary contact name** and email
- [ ] **Google Ads Customer ID** (10-digit number, if available)
- [ ] **Google Ads Manager ID** (if account is managed via MCC)
- [ ] **Website URL** and platform (Shopify, WordPress, WooCommerce, etc.)
- [ ] **Industry** and business type
- [ ] **Services provided** (Google Ads, Meta Ads, etc.)

---

## Step-by-Step Setup Checklist

### Phase 1: Basic Client Folder Structure

#### 1.1 Create Client Folder Structure

```bash
# Create main client directory
mkdir -p clients/[client-slug]/{emails,documents,spreadsheets,presentations,meeting-notes,briefs,reports,product-feeds,scripts}
```

**Required folders:**
- `emails/` - Email correspondence
- `documents/` - Strategy docs, analysis
- `spreadsheets/` - Data files, CSVs
- `presentations/` - Client presentations
- `meeting-notes/` - Meeting transcripts
- `briefs/` - Project briefs, SOWs
- `reports/` - Performance reports (HTML/PDF)
- `product-feeds/` - Product feed files (if e-commerce)
- `scripts/` - Client-specific automation

#### 1.2 Create Core Files

**Create `clients/[client-slug]/README.md`**
- Copy from `clients/_templates/README.md`
- Fill in client details, contacts, services
- Add to Quick Links section

**Create `clients/[client-slug]/CONTEXT.md`**
- Copy from `clients/_templates/CONTEXT.md`
- Fill in account overview, strategic context
- Document business model, goals, KPIs
- Add client preferences and communication style

**Create `clients/[client-slug]/tasks-completed.md`**
- Empty file (auto-populated by Google Tasks sync)

#### 1.3 Update Clients List

**File**: `clients/README.md`

Add client to the "Current Clients" list:
```markdown
## Current Clients
...
13. **Positive Bakes** - `positive-bakes/`
```

---

### Phase 2: Inbox & Email Processing

#### 2.1 Add to Inbox Processors

**File**: `agents/system/ai-inbox-processor.py`

Add to `CLIENTS` list (alphabetical order):
```python
CLIENTS = [
    ...
    'positive-bakes',
    ...
]
```

**File**: `agents/system/inbox-processor.py`

Add to `CLIENTS` list (alphabetical order):
```python
CLIENTS = [
    ...
    'positive-bakes',
    ...
]
```

**Purpose**: Enables automatic routing of inbox notes to client folders

#### 2.2 Configure Email Auto-Labeling

**File**: `shared/email-sync/auto-label-config.yaml`

Add client configuration:
```yaml
  positive-bakes:
    label: "client/positive-bakes"
    domains:
      - "positivebakes.com"
      - "positive-bakes.com"
    emails:
      - "contact@positivebakes.com"  # Add primary contact email
      - "aatin@positivebakes.com"    # Add other contacts
    keywords:
      - "positive bakes"
      - "positivebakes"
    company_names:
      - "Positive Bakes"
      - "PositiveBakes"
```

**Purpose**: Automatically labels emails from/to client with Gmail label

---

### Phase 3: Google Ads Integration

#### 3.1 Add to Google Ads Client Mapping

**File**: `shared/data/google-ads-clients.json`

Add client entry:
```json
{
  "clients": {
    "positive-bakes": {
      "customer_id": "TBD",  // Replace with actual 10-digit customer ID
      "display_name": "Positive Bakes",
      "manager_id": null,  // Set to MCC ID if account is managed
      "folder_path": "clients/positive-bakes",
      "status": "active",
      "note": "Customer ID to be added once Google Ads account is set up"
    }
  }
}
```

**How to get Customer ID:**

**Option 1: Use Utility Script (Recommended)**
```bash
cd shared/mcp-servers/google-ads-mcp-server
.venv/bin/python3 get_client_ids.py "Client Name" --client-slug "client-slug" --update-config
```

This script will:
- Find the Google Ads Customer ID
- Find the Merchant Center ID (if Shopping/PMax campaigns exist)
- Optionally update config files automatically

**Option 2: Use MCP**
```
List all my Google Ads accounts
```
Then search the output for the client name.

**Option 3: Manual**
1. Check Google Ads UI: Settings → Account details
2. Update `customer_id` field (remove "TBD" placeholder)

**Purpose**: Enables natural language audits ("Audit Positive Bakes")

#### 3.2 Add to Google Ads Auditor

**File**: `agents/reporting/google-ads-auditor.py`

Add to `CLIENTS` list:
```python
CLIENTS = [
    ...
    "positive-bakes",
    ...
]
```

**Purpose**: Includes client in weekly automated audits

#### 3.3 Add to Performance Monitoring (When Customer ID Available)

**File**: `agents/performance-monitoring/daily-anomaly-detector.py`

Uncomment and add to `ACTIVE_CLIENTS`:
```python
ACTIVE_CLIENTS = {
    ...
    'Positive Bakes': '1234567890',  # Replace with actual customer ID
}
```

**File**: `agents/performance-monitoring/fetch-weekly-performance.py`

Uncomment and add to `ACTIVE_CLIENTS`:
```python
ACTIVE_CLIENTS = {
    ...
    'Positive Bakes': '1234567890',  # Replace with actual customer ID
}
```

**Note**: Keep commented until Google Ads account is set up and customer ID is known.

**Purpose**: 
- Daily anomaly detection (revenue drops, ROAS issues)
- Weekly performance data collection

---

### Phase 4: Document Management

#### 4.1 Add to Google Docs Creation Script

**File**: `shared/scripts/create-all-client-docs.py`

Add to `CLIENTS` list:
```python
CLIENTS = [
    ...
    "positive-bakes",
    ...
]
```

**Purpose**: Enables automated Google Doc creation for client CONTEXT.md

---

### Phase 5: Product Feed Monitoring (E-commerce Only)

**⚠️ Only required if client has Shopping/Performance Max campaigns with product feeds**

#### 5.1 Create Product Performance Spreadsheet

**Required**: Each client needs a dedicated Google Spreadsheet for product performance tracking.

**Step 1: Create the Spreadsheet**

Use MCP Google Drive to create a new spreadsheet:
```
mcp__google-drive__createGoogleSheet(
  title: "[Client Name] - Product Performance"
)
```

**Or create manually in Google Sheets:**
1. Go to Google Sheets
2. Create new spreadsheet
3. Name it: `[Client Name] - Product Performance`
4. Note the spreadsheet ID from the URL

**Step 2: Create Required Sheets**

The spreadsheet needs **3 sheets** (tabs):

1. **"Daily Performance"** - Daily product performance data
2. **"Impact Analysis"** - Product change impact analysis
3. **"Product Summary"** - Current product status summary

**Step 3: Add Headers**

**Daily Performance sheet (Row 1):**
```
Date | Client | Product ID | Product Title | Impressions | Clicks | Conversions | Revenue (£) | Cost (£) | CTR (%) | Conv Rate (%) | ROAS | Label
```

**Impact Analysis sheet (Row 1):**
```
Analysis Date | Client | Product ID | Product Title | Change Type | Date Changed | Days Since | Before Clicks | After Clicks | Click Change % | Before Revenue | After Revenue | Revenue Change £ | Revenue Change % | Impact Flag | Label
```

**Product Summary sheet (Row 1):**
```
Client | Product ID | Product Title | Current Label | Last 7D Clicks | Last 7D Revenue | Last 30D Clicks | Last 30D Revenue | ROAS | Status
```

**Step 4: Share with Service Account**

**Critical**: The spreadsheet must be shared with the service account for automated writes.

**Service Account Email**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`  
**Permission Level**: Editor (Writer)

**How to share:**
1. Open the spreadsheet
2. Click "Share" button
3. Add email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Set permission to "Editor"
5. Click "Send"

**Or use MCP Google Drive:**
```
mcp__google-drive__shareFile(
  fileId: "[SPREADSHEET_ID]",
  email: "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com",
  role: "writer"
)
```

#### 5.2 Add to Product Impact Analyzer Config

**File**: `tools/product-impact-analyzer/config.json`

Add client entry to `clients` array:
```json
{
  "name": "Positive Bakes",
  "merchant_id": "TBD",  // Google Merchant Center ID
  "google_ads_customer_id": "1234567890",
  "enabled": true,
  "product_performance_spreadsheet_id": "TBD",  // ← Add spreadsheet ID here
  "monitoring_thresholds": {
    "revenue_drop": 200,      // Adjust based on typical daily revenue
    "revenue_spike": 300,
    "click_drop_percent": 40,
    "comment": "Brief context about client size/type"
  },
  "label_tracking": {
    "enabled": false,  // Set to true if using custom labels
    "label_field": null
  },
  "notes": "Any important context (multi-brand, tracking issues, etc.)"
}
```

**Important fields:**
- `name`: Must match client folder name (use spaces, e.g., "Positive Bakes")
- `merchant_id`: Google Merchant Center ID (find via Google Ads query)
- `google_ads_customer_id`: 10-digit Google Ads customer ID
- `product_performance_spreadsheet_id`: Spreadsheet ID from Step 1
- `enabled`: Set to `true` to activate monitoring, `false` to configure but not monitor yet

**How to find Merchant ID:**
1. Query Google Ads: `SELECT campaign.shopping_setting.merchant_id FROM campaign WHERE campaign.advertising_channel_type IN ('SHOPPING', 'PERFORMANCE_MAX')`
2. Or check Google Merchant Center UI (shown in top-left corner)

#### 5.3 Grant Service Account Access to Merchant Center

**CRITICAL**: For disapproval tracking and product feed monitoring to work, the service account **must** have access to the client's Merchant Center account.

**Service Account Email**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

**Steps:**
1. Go to the client's Merchant Center: https://merchants.google.com/mc/accounts/[MERCHANT_ID]/users
2. Click "Add User" or "Invite User"
3. Enter email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Select access level: **"Standard"** (read access to products and reports)
5. Click "Send" or "Save"

**Wait 5-10 minutes** for permissions to propagate before testing.

**Verification:**
```bash
cd tools/product-impact-analyzer
source .venv/bin/activate
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  python3 merchant_center_tracker.py --client "[Client Name]" --report
```

**Expected output** (success):
```
Checking [Client Name] (Merchant ID: XXXXXX)...

Product Status Summary:
- Total Products: XXX
- Approved: XXX
- Disapproved: X
- Pending: X
```

**If you see 401 error**: "The caller does not have access to the accounts: [MERCHANT_ID]"
- Wait 5-10 more minutes for permissions to propagate
- Verify you added the correct email address
- Verify you granted "Standard" (or higher) access level

**Purpose**:
- Product feed monitoring
- Daily performance tracking
- **Disapproval tracking** (requires Merchant Center API access)
- Price change monitoring (future)
- Product attribute change monitoring (future)
- Performance alerts
- Weekly impact analysis reports

---

### Phase 6: Verification & Testing

#### 6.1 Verify Folder Structure

```bash
ls -la clients/[client-slug]/
```

Should show all standard folders created.

#### 6.2 Test Email Auto-Labeling

Send a test email from client domain and verify it gets labeled correctly.

#### 6.3 Test Google Ads Integration

Once customer ID is added:
```bash
# Test audit command
python3 agents/reporting/google-ads-auditor.py --client positive-bakes
```

#### 6.4 Verify Inbox Processing

Create a test note in `!inbox/` mentioning client name, verify it routes correctly.

---

## Quick Reference: Files to Update

| File | Purpose | Required? |
|------|---------|-----------|
| `clients/[client-slug]/README.md` | Client overview | ✅ Always |
| `clients/[client-slug]/CONTEXT.md` | Strategic notes | ✅ Always |
| `clients/[client-slug]/tasks-completed.md` | Task log | ✅ Always |
| `clients/README.md` | Client list | ✅ Always |
| `agents/system/ai-inbox-processor.py` | Inbox routing | ✅ Always |
| `agents/system/inbox-processor.py` | Inbox routing | ✅ Always |
| `shared/email-sync/auto-label-config.yaml` | Email labeling | ✅ Always |
| `shared/data/google-ads-clients.json` | Google Ads mapping | ✅ If Google Ads client |
| `agents/reporting/google-ads-auditor.py` | Weekly audits | ✅ If Google Ads client |
| `agents/performance-monitoring/daily-anomaly-detector.py` | Anomaly detection | ✅ If Google Ads client |
| `agents/performance-monitoring/fetch-weekly-performance.py` | Performance data | ✅ If Google Ads client |
| `shared/scripts/create-all-client-docs.py` | Google Docs sync | ✅ Always |
| `tools/product-impact-analyzer/config.json` | Product monitoring | ⚠️ E-commerce only |
| **Google Spreadsheet** | Product performance tracking | ⚠️ E-commerce only (create via MCP) |
| **Merchant Center User Access** | Disapproval tracking | ⚠️ E-commerce only (grant service account "Standard" access) |

---

## Future Extensibility

### Adding New Agent Skills or Processes

When new agent skills or automated processes are added to the system, update this document:

1. **Add new section** under "Phase X" (or create new phase)
2. **Document the file** that needs updating
3. **Show example code** with placeholder `[client-slug]` or `[Client Name]`
4. **Explain purpose** of the integration
5. **Add to Quick Reference table** above
6. **Include any required setup steps** (API keys, permissions, etc.)

### Template for New Integrations

```markdown
#### X.Y Add to [Process Name]

**File**: `path/to/file.py` or `path/to/config.json`

**Prerequisites**:
- [ ] Requirement 1
- [ ] Requirement 2

**Setup Steps**:
1. Step 1
2. Step 2

Add client to configuration:
```python
# Example code here
```

**Purpose**: [What this integration enables]

**When Required**: [Always / Only if condition X / Optional]

**Verification**:
- [ ] Test checklist item 1
- [ ] Test checklist item 2
```

---

## Common Issues & Troubleshooting

### Client Not Appearing in Audits

- ✅ Check `google-ads-clients.json` has correct `customer_id` (not "TBD")
- ✅ Verify customer ID is 10 digits
- ✅ Check `status` is set to `"active"`

### Emails Not Auto-Labeling

- ✅ Verify domain/email patterns in `auto-label-config.yaml`
- ✅ Check Gmail label exists: `client/[client-slug]`
- ✅ Test with actual email from client domain

### Inbox Notes Not Routing

- ✅ Verify client name in `CLIENTS` list matches folder name exactly
- ✅ Check for typos (case-sensitive, hyphenation)
- ✅ Ensure client name appears in note content

### Performance Monitoring Not Working

- ✅ Uncomment client entry in `ACTIVE_CLIENTS` dictionaries
- ✅ Verify customer ID is correct (not placeholder)
- ✅ Check account has recent activity/data

---

## Example: Positive Bakes Setup

**Completed**: January 27, 2025

**Steps Completed:**
- ✅ Created folder structure
- ✅ Created README.md, CONTEXT.md, tasks-completed.md
- ✅ Added to clients/README.md
- ✅ Added to inbox processors
- ✅ Added to email auto-labeling
- ✅ Added to Google Ads mapping (customer_id: TBD)
- ✅ Added to Google Ads auditor
- ✅ Added to performance monitoring (commented, pending customer ID)
- ✅ Added to document management script

**Pending:**
- ⏳ Google Ads customer ID (waiting for account setup)
- ⏳ Aatin Anadkat email address (to add to auto-label-config.yaml)
- ⏳ Merchant ID (if e-commerce product feeds needed)
- ⏳ Product Performance Spreadsheet (if e-commerce - create via MCP, add ID to config.json)

---

## Maintenance Notes

**Last Review**: [Date]  
**Next Review**: [Date + 3 months]

**Changes Since Last Review:**
- [List any new agent skills or processes added]

---

**Questions or Issues?**  
Refer to individual documentation files:
- `docs/SETUP-GOOGLE-ADS-CLIENT-MAPPING.md` - Google Ads setup
- `tools/product-impact-analyzer/ADDING-CLIENTS.md` - Product feed setup
- `docs/CLIENT-WORKFLOWS.md` - Client analysis workflows

