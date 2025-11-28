# Tree2mydoor PMAX Asset Optimisation Workflow

**Campaign:** T2MD | P Max | HP&P (15820346778)
**Created:** 2025-11-24
**Status:** Ready for Implementation

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `pmax-asset-replacement-sheet.csv` | Assets to replace (pause old, create new) |
| `pmax-new-assets-sheet.csv` | New assets to add to asset groups |
| `implement-asset-changes.py` | Python script that implements changes via Google Ads API |
| `pmax-text-asset-optimisation-cheat-sheet.md` | Full analysis and recommendations |

---

## 🔄 Workflow Steps

### Step 1: Import CSVs into Google Sheets

1. Go to Google Sheets: https://sheets.google.com
2. Create a new spreadsheet: "Tree2mydoor PMAX Asset Optimisation - Nov 2024"
3. Import `pmax-asset-replacement-sheet.csv` into Sheet 1 (rename to "Assets to Replace")
4. Import `pmax-new-assets-sheet.csv` into Sheet 2 (rename to "New Assets to Add")

### Step 2: Edit the Assets

**In "Assets to Replace" sheet:**
- Column F: "New Text (EDIT THIS)" - Edit these as you like
- Column E: "Action" - Change REPLACE to SKIP if you want to skip that asset
- Column G: Update character count if you edit the text

**In "New Assets to Add" sheet:**
- Column D: "New Text (EDIT THIS)" - Edit these as you like
- Column F: "Priority" - Change HIGH/MEDIUM to SKIP if you want to skip that asset
- Column E: Update character count if you edit the text

**Character limits:**
- Headlines: Max 30 characters
- Descriptions: Max 90 characters

### Step 3: Export Back to CSV

1. Download "Assets to Replace" as CSV
2. Download "New Assets to Add" as CSV
3. Replace the original CSV files in `/Users/administrator/Documents/PetesBrain/clients/tree2mydoor/`

### Step 4: Run the Implementation Script

Tell Claude:

```
Read the Tree2mydoor asset CSVs and implement the changes
```

Or run manually:

```bash
cd /Users/administrator/Documents/PetesBrain/clients/tree2mydoor
python3 implement-asset-changes.py
```

### Step 5: Monitor Performance

- Allow 24-48 hours for the Google Ads algorithm to learn the new assets
- Check asset performance labels in Google Ads UI (Asset report)
- Review after 2 weeks to assess impact

---

## 📊 What the Script Does

### For Assets to Replace (Action = REPLACE):
1. ✅ Queries Google Ads to find the asset by ID
2. ⏸️  Pauses the old asset (sets status to PAUSED)
3. ➕ Creates a new text asset with your edited text
4. 🔗 Links the new asset to the same asset group
5. ✅ Confirms completion

### For New Assets (Priority = HIGH/MEDIUM):
1. ➕ Creates a new text asset with your text
2. 🔗 Links the asset to the specified asset group
3. ✅ Confirms completion

### Assets Marked SKIP:
- These are completely ignored

---

## 🎯 Summary of Changes

### Assets to Replace: 10
- **6 Headlines** in Anniversary Ads asset group
- **4 Descriptions** across Olive Tree Competitors and T2MD | Others & Catchall

### New Assets to Add: 11
- **6 Headlines** across multiple asset groups
- **5 Descriptions** across multiple asset groups

---

## 💡 Tips for Editing

### Headlines (30 char max)
**Good patterns from data:**
- Include brand: "Tree2mydoor..."
- Specific products: "Olive Trees", "Rose Bushes"
- Emotional hooks: "Living", "Ethical", "Memorial"
- Urgency: "Next Day Delivery"

**Avoid:**
- Generic: "Perfect", "Ultimate", "Best"
- Negative: "Scrap the...", "Why X when..."
- Clichés: "Gifts that last"

### Descriptions (90 char max)
**Good patterns from data:**
- Lead with benefit: "Living gifts that last..."
- Address objections: "Perfect for small gardens & patios"
- Include trust signals: "Since 2003", "100+ varieties"
- Call to action: "Take a look", "Explore now"

**Avoid:**
- Pure feature lists without benefits
- Limiting language: "Perfect for patio only"
- Generic packing statements

---

## ⚠️ Important Notes

### DO NOT Edit:
- Asset ID column
- Asset Group ID column
- Asset Group column (name is just for reference)

### You CAN Edit:
- "New Text (EDIT THIS)" columns
- "Action" column (REPLACE → SKIP)
- "Priority" column (HIGH/MEDIUM → SKIP)

### Character Counting:
- The CSV "Char Count" column does NOT auto-update
- If you edit text, manually recount characters
- Headlines: 30 max
- Descriptions: 90 max

---

## 🚨 Troubleshooting

### "Asset not found" error
- The asset may have already been paused manually
- Check Google Ads UI to verify asset status
- If already paused, the script will skip it

### "Permission denied" error
- Ensure google-ads.yaml is properly configured
- Check that CUSTOMER_ID is correct (4941701449)

### "Character limit exceeded" error
- Google Ads will reject assets that exceed character limits
- Recheck your text character counts before running

---

## 📈 Expected Results

### Immediate Impact (Week 1-2):
- £350-400/month budget freed up from paused underperformers
- Algorithm reallocates budget to proven winners

### Medium-term Impact (Week 2-4):
- New assets move from PENDING → LEARNING → GOOD/BEST performance labels
- Improved CTR and conversion rate as better assets get impressions

### Long-term Impact (Month 2-3):
- Campaign ROAS improves 8-12% (target: 140% → 155-160%)
- More consistent performance across asset groups

---

## 🔗 Related Documents

- **Full Analysis:** `pmax-text-asset-optimisation-cheat-sheet.md`
- **Implementation Script:** `implement-asset-changes.py`
- **Replacement Assets:** `pmax-asset-replacement-sheet.csv`
- **New Assets:** `pmax-new-assets-sheet.csv`

---

## ✅ Quick Checklist

Before running implementation:

- [ ] Edited "New Text (EDIT THIS)" columns as needed
- [ ] Verified all headlines are ≤30 characters
- [ ] Verified all descriptions are ≤90 characters
- [ ] Changed any unwanted assets to SKIP
- [ ] Saved edited CSVs back to the tree2mydoor folder
- [ ] Ready to run implementation script

After implementation:

- [ ] Check Google Ads UI to confirm assets are paused/created
- [ ] Set calendar reminder for 2-week performance review
- [ ] Monitor campaign ROAS daily for first week
- [ ] Note any immediate performance changes

---

**Questions?** Ask Claude for help with any step of the process!
