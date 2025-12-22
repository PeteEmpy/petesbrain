---
name: smythson-deploy
description: Quick access to Smythson Google Ads deployment workflows, documentation, and common commands. Use when user says "Smythson deploy", "Smythson deployment", "deploy Smythson", or needs to access Smythson deployment tools.
allowed-tools: Read, Bash, Write, mcp__google-ads__run_gaql, mcp__platform-ids__get_client_platform_ids, mcp__google-drive__getGoogleSheetContent
---

# Smythson Deployment Skill

**Purpose**: Rapid access to Smythson deployment system for Christmas Eve (Dec 24th) and ongoing updates.

---

## Instructions

When this skill is invoked:

### 1. Greet and Present Options

Display this menu:

```
🎄 Smythson Google Ads Deployment System

What would you like to do?

📚 DOCUMENTATION:
1. View Master Index (start here)
2. View Deployment Playbook (complete guide)
3. View Image Selection Guide (for Alex)

🚀 DEPLOYMENT ACTIONS:
4. Generate RSA CSVs (all regions)
5. Deploy PMax Text Assets (with dry-run)
6. Deploy PMax Images (with dry-run)
7. Generate Asset Library Browser for Alex

📊 DATA OPERATIONS:
8. Refresh data from Google Sheets
9. View current data files
10. Validate CSV files

🔧 UTILITIES:
11. Show account IDs reference
12. Check deployment status
13. View recent deployment history

Type the number or describe what you need.
```

Wait for user selection.

---

### 2. Execute User Selection

#### Option 1: View Master Index

```bash
Read: /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/MASTER-INDEX.md
```

Display the full content and say:
```
This is your central navigation hub. Key sections:
- Quick Start (Christmas Eve deployment)
- Core Documentation
- Workflow Quick Reference
- File Locations
- Account Reference
- Common Commands
- Emergency Procedures

What would you like to explore next?
```

---

#### Option 2: View Deployment Playbook

```bash
Read: /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/DEPLOYMENT-PLAYBOOK-2025.md
```

Display and highlight:
```
📖 This is the MASTER deployment guide covering:
- RSA Workflow (Google Ads Editor CSV import)
- PMax Text Workflow (API deployment)
- PMax Image Workflow (API with spreadsheet)
- Pre-flight checklists
- Troubleshooting

Ready to deploy? Which workflow do you need (RSA/PMax Text/PMax Images)?
```

---

#### Option 3: View Image Selection Guide

```bash
Read: /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/HOW-TO-SELECT-IMAGES-FOR-ALEX.md
```

Display and say:
```
🖼️ This guide shows Alex how to:
- Use the Asset Library Browser
- Select images by Asset ID
- Meet minimum requirements (1 landscape + 1 square)
- Populate the Google Sheet

Need me to generate an Asset Library Browser? (Option 7)
```

---

#### Option 4: Generate RSA CSVs

**Ask user**:
```
Which region(s)?
1. UK only
2. USA only
3. EUR only
4. All regions with changes
5. Custom selection
```

**For each selected region**, run:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/shared/scripts

# UK
python3 generate-rsa-update-csv.py \
  --input ~/Documents/PetesBrain.nosync/clients/smythson/data/uk_rsa_updates_from_sheet.json \
  --output ~/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-uk-CHANGES-ONLY.csv \
  --account-id 8573235780 \
  --changes-only

# USA
python3 generate-rsa-update-csv.py \
  --input ~/Documents/PetesBrain.nosync/clients/smythson/data/usa_rsa_updates_from_sheet.json \
  --output ~/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-usa-CHANGES-ONLY.csv \
  --account-id 7808690871 \
  --changes-only

# EUR
python3 generate-rsa-update-csv.py \
  --input ~/Documents/PetesBrain.nosync/clients/smythson/data/eur_rsa_updates_from_sheet.json \
  --output ~/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-eur-CHANGES-ONLY.csv \
  --account-id 7679616761 \
  --changes-only
```

Report:
```
✅ Generated RSA CSV files:
- UK: [X] ads with changes
- USA: [Y] ads with changes
- EUR: [Z] ads with changes

Files saved to: clients/smythson/data/

Next steps:
1. Import these CSVs in Google Ads Editor
2. Review changes before publishing
3. See DEPLOYMENT-PLAYBOOK section 3.2 for full instructions
```

---

#### Option 5: Deploy PMax Text Assets

**Ask user**:
```
Which region? (uk/us/eur/row/all)
Dry-run first? (yes/no - default: yes)
```

**Run**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Dry-run
python3 apply-pmax-text-assets-v2.py --region [REGION] --dry-run

# If dry-run successful and user confirms, run live:
python3 apply-pmax-text-assets-v2.py --region [REGION]
```

Report results and any errors.

---

#### Option 6: Deploy PMax Images

**Ask user**:
```
⚠️ IMPORTANT: Has Alex updated the image Asset IDs in the Google Sheet?
Region? (uk/us/eur/row/all)
Dry-run first? (yes/no - default: yes)
```

**Run**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

# Dry-run
python3 apply-image-assets-from-sheet.py --region [REGION] --dry-run

# If validation passes and user confirms, run live:
python3 apply-image-assets-from-sheet.py --region [REGION]
```

Report:
```
Validation checks:
✅ All asset groups have 1+ landscape image
✅ All asset groups have 1+ square image
✅ Total images ≤ 20 per asset group

Deployment status: [SUCCESS/FAILED]
[Include any error messages or warnings]
```

---

#### Option 7: Generate Asset Library Browser

**Ask user**:
```
Which region? (uk/us/eur/row)
```

**Run**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 export-image-catalog-to-sheet.py --region [REGION]
```

Report:
```
✅ Asset Library Browser created!

Spreadsheet: [URL from script output]
Contains:
- [X] image assets
- Clickable image previews
- Asset IDs for copy/paste
- Current usage information

Share this with Alex so they can select images.
See HOW-TO-SELECT-IMAGES-FOR-ALEX.md for their instructions.
```

---

#### Option 8: Refresh Data from Google Sheets

**Run**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 rebuild_rsa_updates_from_spreadsheet.py
```

Report:
```
✅ Refreshed RSA data from Google Sheets

Updated files:
- uk_rsa_updates_from_sheet.json
- usa_rsa_updates_from_sheet.json
- eur_rsa_updates_from_sheet.json
- row_rsa_updates_from_sheet.json

Summary:
- UK: [X] ads total, [Y] with changes
- USA: [X] ads total, [Y] with changes
- EUR: [X] ads total, [Y] with changes
- ROW: [X] ads total, [Y] with changes

Next: Generate CSVs? (Option 4)
```

---

#### Option 9: View Current Data Files

**Run**:

```bash
ls -lh /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/*.csv
ls -lh /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/*.json
```

Display list with:
- File names
- Modification dates
- File sizes

Highlight:
```
📂 CSV files = Ready for Google Ads Editor import
📂 JSON files = Source data from Google Sheets

Latest modifications show when data was last refreshed.
```

---

#### Option 10: Validate CSV Files

**Run**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts

python3 verify-rsa-csvs.py ../data/DEPLOY-rsa-uk-CHANGES-ONLY.csv
python3 verify-rsa-csvs.py ../data/DEPLOY-rsa-usa-CHANGES-ONLY.csv
python3 verify-rsa-csvs.py ../data/DEPLOY-rsa-eur-CHANGES-ONLY.csv
```

Report:
```
Validation Results:

UK: ✅ [X] ads, all meet minimum requirements (3+ headlines, 2+ descriptions)
USA: ✅ [Y] ads, all valid
EUR: ✅ [Z] ads, all valid

All CSVs ready for import.
```

---

#### Option 11: Show Account IDs Reference

Display:

```
🔑 Smythson Google Ads Account IDs

UK Account:
  Customer ID: 8573235780
  Account Name: Smythson UK

USA Account:
  Customer ID: 7808690871
  Account Name: Smythson USA

EUR Account:
  Customer ID: 7679616761
  Account Name: Smythson EUR

ROW Account:
  Customer ID: 5556710725
  Account Name: Smythson ROW

Manager Account:
  Manager ID: 2569949686
  (Always required for API calls)

📊 Google Sheets:
  RSA Sheet: https://docs.google.com/spreadsheets/d/189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo/edit
  PMax Sheet: https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit
```

---

#### Option 12: Check Deployment Status

**Query Google Ads API** to check current asset group status:

```python
# For each region, check PMax campaign status
mcp__google_ads__run_gaql(
    customer_id='8573235780',  # UK
    manager_id='2569949686',
    query='''
        SELECT
            campaign.name,
            campaign.status,
            asset_group.name,
            asset_group.status
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        AND campaign.status != 'REMOVED'
        ORDER BY campaign.name
    '''
)
```

Report:
```
📊 Current Deployment Status

UK:
  Campaign: [Name] - Status: [ENABLED/PAUSED]
    Asset Group: [Name] - Status: [ELIGIBLE/LEARNING/LIMITED]
  ...

USA:
  ...

EUR:
  ...

ROW:
  ...

⚠️ Issues detected:
[List any asset groups with status != ELIGIBLE]

All asset groups should show "ELIGIBLE" status after successful deployment.
"LEARNING" = Normal for first 7-14 days after changes.
"LIMITED" = Review asset group for missing assets or policy violations.
```

---

#### Option 13: View Recent Deployment History

**Read deployment logs**:

```bash
ls -lt /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/*.csv | head -10
ls -lt /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/*.json | head -10
```

Report:
```
📜 Recent Deployment History

Last 5 CSV generations:
1. [Date/Time] - DEPLOY-rsa-uk-CHANGES-ONLY.csv
2. [Date/Time] - DEPLOY-rsa-usa-CHANGES-ONLY.csv
...

Last 5 JSON updates:
1. [Date/Time] - uk_rsa_updates_from_sheet.json
...

Most recent activity: [X] hours ago
```

---

### 3. After Action Complete

**Always ask**:
```
Action complete. Would you like to:
- Return to main menu
- Take another action
- Exit
```

---

## Emergency Quick Commands

### Pre-Christmas Eve Checklist (Dec 23rd)

Run full system check:

```bash
# 1. Verify OAuth tokens
cd ~/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 apply-pmax-text-assets-v2.py --region uk --dry-run  # Should succeed

# 2. Backup current state
cd ~/Documents/PetesBrain.nosync/clients/smythson/data
cp *.json backup/

# 3. Test CSV generation
cd ~/Documents/PetesBrain.nosync/shared/scripts
python3 generate-rsa-update-csv.py --help  # Verify script works

# 4. Verify Google Sheets access
# (Check mcp__google-drive__getGoogleSheetContent works)
```

Report checklist status:
```
☑️ Pre-Christmas Eve Checklist

✅ OAuth tokens valid
✅ Scripts executable
✅ Backup created
✅ Google Sheets accessible
✅ Documentation reviewed

System ready for Dec 24th deployment.
```

---

### Christmas Eve Fast Track (Dec 24th)

When Alex provides updates:

1. **Identify what changed** (ask user):
   - RSA copy? → Option 4 + 10
   - PMax text? → Option 5
   - PMax images? → Option 6

2. **30-minute deployment path**:
   - Refresh data (Option 8)
   - Generate/deploy (Options 4/5/6)
   - Validate (Option 10 or 12)
   - Confirm with user

3. **If errors occur**:
   - Read DEPLOYMENT-PLAYBOOK troubleshooting section
   - Check emergency procedures in MASTER-INDEX
   - Present rollback options

---

## Context-Aware Shortcuts

If user says specific phrases, skip menu and go direct:

| User Says | Execute |
|-----------|---------|
| "show docs", "documentation" | Option 1 (Master Index) |
| "playbook", "guide" | Option 2 (Deployment Playbook) |
| "generate CSV", "RSA CSV" | Option 4 (Generate RSA CSVs) |
| "deploy PMax", "PMax text" | Option 5 (Deploy PMax Text) |
| "deploy images", "image deployment" | Option 6 (Deploy PMax Images) |
| "asset library", "image browser" | Option 7 (Asset Library Browser) |
| "account IDs", "customer IDs" | Option 11 (Account Reference) |
| "status check", "deployment status" | Option 12 (Check Status) |
| "emergency", "rollback", "help" | Read emergency procedures from MASTER-INDEX |

---

## Key File Paths Reference

**Documentation**:
- Master Index: `clients/smythson/MASTER-INDEX.md`
- Deployment Playbook: `clients/smythson/DEPLOYMENT-PLAYBOOK-2025.md`
- Image Guide: `clients/smythson/HOW-TO-SELECT-IMAGES-FOR-ALEX.md`
- Context: `clients/smythson/CONTEXT.md`

**Data Files**:
- JSON source data: `clients/smythson/data/*.json`
- CSV deployment files: `clients/smythson/data/DEPLOY-*.csv`

**Scripts**:
- RSA rebuild: `clients/smythson/scripts/rebuild_rsa_updates_from_spreadsheet.py`
- CSV generation: `shared/scripts/generate-rsa-update-csv.py`
- PMax text: `clients/smythson/scripts/apply-pmax-text-assets-v2.py`
- PMax images: `clients/smythson/scripts/apply-image-assets-from-sheet.py`
- Asset browser: `clients/smythson/scripts/export-image-catalog-to-sheet.py`

**Google Sheets**:
- RSA Sheet: `189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo`
- PMax Sheet: `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g`

---

## Examples

### Example 1: User wants to deploy Christmas sale copy

**User**: "Smythson deploy - Alex just sent Christmas sale copy"

**Response**:
```
🎄 Christmas Sale Deployment

Got it! Alex has provided updates. Let me help you deploy.

First, what did Alex update?
1. RSA ad copy (text-only ads)
2. PMax text assets (headlines/descriptions)
3. PMax images
4. Multiple of the above

[After user responds, execute appropriate workflow with dry-run first]
```

---

### Example 2: User needs to help Alex select images

**User**: "Smythson deploy - Alex needs to pick images for new campaign"

**Response**:
```
🖼️ Image Selection for Alex

I'll generate the Asset Library Browser so Alex can easily browse and select images.

Which region is this for?
1. UK
2. USA
3. EUR
4. ROW
5. All regions

[After selection, run Option 7 and provide Alex the spreadsheet link + guide]

Once Alex has updated the image Asset IDs in the PMax sheet, let me know and I'll deploy them (Option 6).
```

---

### Example 3: User wants emergency help

**User**: "Smythson deploy - something went wrong"

**Response**:
```
🆘 Emergency Support

Let's troubleshoot. What happened?

1. Deployment failed with error
2. Wrong ads deployed
3. Images not showing correctly
4. Need to rollback changes
5. Other issue

[Read MASTER-INDEX emergency procedures section and guide user through rollback/fix]
```

---

## Success Criteria

After using this skill, user should be able to:
- ✅ Navigate Smythson documentation quickly
- ✅ Deploy updates in <30 minutes
- ✅ Generate Asset Library Browser for Alex
- ✅ Validate deployments before going live
- ✅ Handle emergencies with rollback procedures
- ✅ Access account IDs and Google Sheets instantly

**🎄 System ready for Christmas Eve deployment!** 🚀
