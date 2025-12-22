# 🗂️ Smythson Google Ads Deployment - Master Index

**Last Updated**: 15th December 2025
**Purpose**: Central navigation hub for all Smythson deployment documentation
**Critical Deadline**: Tuesday, 24th December 2025 (Christmas Eve) - 30-minute deployment window

---

## 🚀 Quick Start (Christmas Eve Deployment)

**When Alex provides sale copy on Dec 24th, follow this path**:

1. **📖 Start Here**: [DEPLOYMENT-PLAYBOOK-2025.md](./DEPLOYMENT-PLAYBOOK-2025.md)
   - Complete deployment guide for all workflows
   - Decision tree: RSA vs PMax text vs PMax images
   - Step-by-step instructions
   - Pre-flight checklists

2. **🎯 30-Minute Deployment Plan**:
   - Read updates from Alex
   - Identify what's changed (RSA text? PMax text? Images?)
   - Follow appropriate workflow in playbook
   - Deploy via Google Ads Editor (RSA) or API (PMax)

3. **🆘 If Something Goes Wrong**: See "Emergency Procedures" section below

---

## 📚 Core Documentation

### Primary Guides

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[DEPLOYMENT-PLAYBOOK-2025.md](./DEPLOYMENT-PLAYBOOK-2025.md)** | **Master deployment guide** | **ALWAYS start here** |
| **[HOW-TO-SELECT-IMAGES-FOR-ALEX.md](./HOW-TO-SELECT-IMAGES-FOR-ALEX.md)** | Image selection guide for Alex | When Alex needs to choose images |
| **[CONTEXT.md](./CONTEXT.md)** | Client background, platform IDs, strategic context | Reference for client details |

### Historical/Reference Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[RSA-DEPLOYMENT-CHECKLIST-MONDAY-DEC-16.md](./reports/RSA-DEPLOYMENT-CHECKLIST-MONDAY-DEC-16.md)** | RSA deployment checklist (Dec 16 version) | Reference for RSA workflow |
| **[IMAGE-DEPLOYMENT-CHECKLIST-MONDAY-DEC-16.md](./reports/IMAGE-DEPLOYMENT-CHECKLIST-MONDAY-DEC-16.md)** | Image deployment checklist (Dec 16 version) | Reference for image workflow |
| **[pmax-asset-application-workflow.md](./documents/pmax-asset-application-workflow.md)** | PMax asset workflow documentation | Deep dive on PMax API process |

---

## 🎯 Workflow Quick Reference

### Decision Tree: What Am I Deploying?

```
Alex provides updates
    ├─ RSA ad copy changes?
    │  └─ Follow: DEPLOYMENT-PLAYBOOK → "RSA Workflow" section
    │     Files: data/DEPLOY-rsa-[region]-CHANGES-ONLY.csv
    │     Tool: Google Ads Editor (CSV import)
    │
    ├─ PMax text changes?
    │  └─ Follow: DEPLOYMENT-PLAYBOOK → "PMax Text Workflow" section
    │     Scripts: clients/smythson/scripts/apply-pmax-text-assets-v2.py
    │     Tool: Google Ads API
    │
    └─ PMax image changes?
       └─ Follow: DEPLOYMENT-PLAYBOOK → "PMax Image Workflow" section
          Scripts: clients/smythson/scripts/apply-image-assets-from-sheet.py
          Tool: Google Ads API
```

---

## 🗄️ File Locations Reference

### Data Files (Generated CSVs)

**Location**: `/clients/smythson/data/`

| File Pattern | What It Contains | Used For |
|-------------|------------------|----------|
| `DEPLOY-rsa-uk-CHANGES-ONLY.csv` | UK RSA updates (only ads with changes) | Google Ads Editor import |
| `DEPLOY-rsa-usa-CHANGES-ONLY.csv` | USA RSA updates | Google Ads Editor import |
| `DEPLOY-rsa-eur-CHANGES-ONLY.csv` | EUR RSA updates | Google Ads Editor import |
| `uk_rsa_updates_from_sheet.json` | UK RSA update definitions (all ads) | Script input |
| `usa_rsa_updates_from_sheet.json` | USA RSA update definitions | Script input |
| `eur_rsa_updates_from_sheet.json` | EUR RSA update definitions | Script input |
| `row_rsa_updates_from_sheet.json` | ROW RSA update definitions | Script input |

**⚠️ Important**: CSVs in `data/` folder are the source of truth for deployment.

---

### Scripts

**Location**: `/clients/smythson/scripts/`

| Script | Purpose | Usage |
|--------|---------|-------|
| `rebuild_rsa_updates_from_spreadsheet.py` | Fetch latest RSA copy from Google Sheet → JSON | When Alex updates RSA sheet |
| `apply-pmax-text-assets-v2.py` | Deploy PMax text assets via API | PMax text deployment |
| `apply-image-assets-from-sheet.py` | Deploy PMax images via API | PMax image deployment |
| `export-image-catalog-to-sheet.py` | Create image asset browser for Alex | When Alex needs to select images |
| `verify-rsa-csvs.py` | Validate CSV meets minimum requirements | Pre-deployment check |

**Full script documentation**: See DEPLOYMENT-PLAYBOOK-2025.md sections.

---

### Google Sheets

| Sheet | Purpose | Link |
|-------|---------|------|
| **RSA Master Sheet** | RSA ad copy for all regions | [View Sheet](https://docs.google.com/spreadsheets/d/189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo/edit) |
| **PMax Master Sheet** | PMax text + image assets | [View Sheet](https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit) |

**Tabs per region**:
- RSA Sheet: UK, US, EUR, ROW (separate tabs)
- PMax Sheet: UK PMax Assets, US PMax Assets, EUR PMax Assets, ROW PMax Assets

---

## 🔑 Account Reference

### Platform IDs

| Region | Customer ID | Account Name |
|--------|-------------|--------------|
| **UK** | 8573235780 | Smythson UK |
| **USA** | 7808690871 | Smythson USA |
| **EUR** | 7679616761 | Smythson EUR |
| **ROW** | 5556710725 | Smythson ROW |

**Manager ID**: 2569949686 (always required for API calls)

**Full context**: See [CONTEXT.md](./CONTEXT.md)

---

## ⚙️ Common Commands Reference

### RSA Workflow

**Regenerate JSON from Google Sheet**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 rebuild_rsa_updates_from_spreadsheet.py
```

**Generate CSV from JSON** (all regions):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/shared/scripts
python3 generate-rsa-update-csv.py \
  --input ~/Documents/PetesBrain.nosync/clients/smythson/data/uk_rsa_updates_from_sheet.json \
  --output ~/Documents/PetesBrain.nosync/clients/smythson/data/DEPLOY-rsa-uk-CHANGES-ONLY.csv \
  --account-id 8573235780 \
  --changes-only

# Repeat for USA (7808690871), EUR (7679616761), ROW (5556710725)
```

**Validate CSV before import**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 verify-rsa-csvs.py ../data/DEPLOY-rsa-uk-CHANGES-ONLY.csv
```

---

### PMax Text Workflow

**Deploy text assets** (dry-run first):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 apply-pmax-text-assets-v2.py --region uk --dry-run
python3 apply-pmax-text-assets-v2.py --region uk  # Live deployment
```

---

### PMax Image Workflow

**Generate Asset Library Browser for Alex**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 export-image-catalog-to-sheet.py --region uk
```

**Deploy image assets** (dry-run first):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 apply-image-assets-from-sheet.py --region uk --dry-run
python3 apply-image-assets-from-sheet.py --region uk  # Live deployment
```

---

## 🆘 Emergency Procedures

### Deployment Failed - What Now?

**1. Check Error Message**

| Error Type | Likely Cause | Quick Fix |
|------------|--------------|-----------|
| "Asset group not found" | Campaign/asset group name mismatch | Verify exact names in Google Ads UI |
| "VALIDATION FAILED: Missing required types" | Missing 1 landscape or 1 square image | Add missing image types to spreadsheet |
| "Google Ads OAuth token expired" | Token expired (exit code 78) | Run: `~/Documents/PetesBrain.nosync/shared/scripts/setup-oauth-once.sh` |
| "DUPLICATE_RESOURCE" | Image already linked | Regenerate with latest API state |
| CSV import shows "Add" not "Edit" | Missing #Original columns or pinning issue | Use CHANGES-ONLY CSV or check pinning |

**2. Rollback Procedures**

**If RSA deployment went wrong**:
1. Open Google Ads Editor
2. Go to "Tools" → "Undo recent changes"
3. Select the import you just did
4. Click "Undo"
5. Publish changes

**If PMax deployment went wrong**:
1. Revert to backup JSON:
   ```bash
   cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data
   ls -lt *backup*.json  # Find latest backup
   ```
2. Re-run script with old data

**3. Contact User**

If stuck, message:
```
"Deployment failed with error: [paste error message].
Need help troubleshooting. Details: [what you were deploying, which region, what step]."
```

---

### Pre-Deployment Checklist (Dec 24th)

**☑️ Day Before (Dec 23rd)**:
- [ ] Confirm Alex will provide updates by 9am Dec 24th
- [ ] Verify all scripts are executable (`chmod +x *.py`)
- [ ] Test OAuth tokens are valid (run a dry-run for each region)
- [ ] Backup current state (JSON files in `data/`)
- [ ] Review DEPLOYMENT-PLAYBOOK-2025.md

**☑️ Morning of Dec 24th (before Alex sends updates)**:
- [ ] Generate fresh Asset Library Browser (if images will change)
- [ ] Pull latest from Google Sheets to verify structure unchanged
- [ ] Test internet connection / API access

**☑️ After Alex sends updates**:
- [ ] Read Alex's message carefully
- [ ] Identify what changed (RSA? PMax text? Images?)
- [ ] Follow appropriate workflow in DEPLOYMENT-PLAYBOOK
- [ ] ALWAYS dry-run first
- [ ] Only deploy live after dry-run succeeds

**☑️ Post-Deployment**:
- [ ] Verify changes in Google Ads UI
- [ ] Confirm asset group status = "Eligible" (not "Learning" with errors)
- [ ] Message Alex: "Deployment complete. Changes live in [regions]."
- [ ] Archive deployment files with date

---

## 📖 Learning Resources

### Understanding the Workflows

**New to this system?** Read in this order:

1. **[CONTEXT.md](./CONTEXT.md)** - Client background, why we're doing this
2. **[HOW-TO-SELECT-IMAGES-FOR-ALEX.md](./HOW-TO-SELECT-IMAGES-FOR-ALEX.md)** - How images work
3. **[DEPLOYMENT-PLAYBOOK-2025.md](./DEPLOYMENT-PLAYBOOK-2025.md)** - Complete technical guide
4. **Historical checklists** (see "Historical/Reference Documentation" above) - Original workflows

### Key Concepts

**RSA (Responsive Search Ads)**:
- Text-only ads with 3-15 headlines, 2-4 descriptions
- Deployed via Google Ads Editor (CSV import)
- Google auto-tests combinations to find best performers

**PMax (Performance Max)**:
- Multi-asset campaigns (text + images + videos)
- Text assets: Headlines (30 chars), long headlines (90 chars), descriptions (90 chars)
- Image assets: Landscape (1.91:1), square (1:1), portrait (4:5), logo (1:1)
- Deployed via Google Ads API (Python scripts)

**Asset Groups**:
- Container for PMax assets
- Each campaign can have multiple asset groups (e.g., "Diaries - Leather", "Notebooks - Seasonal")
- Minimum requirements: 1 landscape + 1 square image

---

## 🔄 Maintenance Schedule

### Regular Updates

| Frequency | Task | Who |
|-----------|------|-----|
| **Ad-hoc** (when Alex requests) | Deploy new ad copy/images | Peter |
| **Weekly** | Review performance, identify opportunities | Peter + Alex |
| **Monthly** | Refresh seasonal imagery | Alex selects, Peter deploys |
| **Quarterly** | Full campaign audit | Peter |

### File Hygiene

**Every deployment**:
- [ ] Archive old CSV/JSON files with date: `DEPLOY-rsa-uk-20251216-ARCHIVED.csv`
- [ ] Keep last 3 deployments in `data/`, move older to `data/archive/`
- [ ] Update this MASTER-INDEX.md if workflows change

**Every month**:
- [ ] Regenerate Asset Library Browser (images may have been added/removed)
- [ ] Verify Google Sheets structure unchanged
- [ ] Test all scripts with dry-run

---

## 📞 Support & Contacts

### Primary Contact

**Peter** (PetesBrain operator)
- For: All deployment questions, technical issues, script errors
- Response time: Within 2 hours during business hours

### Alex (Smythson Marketing)

- For: Creative direction, image selection, ad copy updates
- Provides: Updated copy/images when campaigns need refreshing

### Escalation

If Peter is unavailable and deployment is urgent:
1. Check "Emergency Procedures" section above
2. Review DEPLOYMENT-PLAYBOOK-2025.md troubleshooting sections
3. Check error logs: `~/.petesbrain-*.log`

---

## 🎓 Appendix

### Glossary

| Term | Definition |
|------|------------|
| **Asset Group** | Container for PMax text/image/video assets |
| **Asset ID** | Numeric ID for images in Google Ads (e.g., `1234567890`) |
| **Asset Library** | Google Ads repository of uploaded images/videos |
| **CSV** | Comma-separated values file for Google Ads Editor import |
| **Dry Run** | Test mode - shows what would happen without making changes |
| **Field Type** | Image classification: MARKETING_IMAGE, SQUARE_MARKETING_IMAGE, etc. |
| **GAQL** | Google Ads Query Language (SQL-like syntax for API) |
| **MCP** | Model Context Protocol (API integration framework) |
| **OAuth** | Authentication system for Google APIs |
| **PMax** | Performance Max campaigns (multi-asset, AI-optimized) |
| **RSA** | Responsive Search Ads (text-only, Google auto-tests combinations) |

---

### Version History

| Date | Changes | Author |
|------|---------|--------|
| 2025-12-15 | Initial master index created | Claude (PetesBrain) |
| 2025-12-15 | Added deployment playbook, image guide, emergency procedures | Claude (PetesBrain) |

---

### Related Documentation

**Global PetesBrain Docs** (outside Smythson folder):
- `/docs/GOOGLE-ADS-PROTOCOL.md` - Google Ads change protection protocol
- `/docs/DATA-VERIFICATION-PROTOCOL.md` - Data accuracy requirements
- `/infrastructure/mcp-servers/google-ads-mcp-server/README.md` - Google Ads API setup

**Client-Specific**:
- All documentation in `/clients/smythson/documents/`
- All meeting notes in `/clients/smythson/meeting-notes/`
- Historical reports in `/clients/smythson/reports/`

---

## 🚀 Quick Access Commands

**Jump to Smythson directory**:
```bash
cd ~/Documents/PetesBrain.nosync/clients/smythson
```

**Open this index in browser**:
```bash
open ~/Documents/PetesBrain.nosync/clients/smythson/MASTER-INDEX.md
```

**View all Smythson documentation**:
```bash
ls -lh ~/Documents/PetesBrain.nosync/clients/smythson/*.md
```

---

**Last Updated**: 15th December 2025
**Next Review**: After Christmas Eve deployment (Dec 24th)
**Owner**: Peter / PetesBrain

**🎄 Ready for Christmas Eve deployment!** 🚀
