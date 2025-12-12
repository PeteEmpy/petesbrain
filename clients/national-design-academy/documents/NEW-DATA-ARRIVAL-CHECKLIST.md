# NDA Enrollment Data Arrival Checklist

**Use this checklist each time Kelly sends new enrollment data.**

---

## Step 1: Confirm New Data Received ✅

- [ ] Email from Kelly Rawson received (kelly@nda.ac.uk)
  - [ ] Or forwarded via Paul Riley (still counts as Kelly's data)
- [ ] Email contains enrollment spreadsheet attachments
- [ ] Check `/clients/national-design-academy/emails/attachments/` for new dated folder
- [ ] Confirm new folder date (e.g., `2025-12-15/`)

**New data folder**: `_________________`

---

## Step 2: Verify File Contents ✅

In the new folder, confirm presence of:

- [ ] `NDA UK Enrolments 25-26.xlsx` (UK students)
- [ ] `NDA International Enrolments 25-26.xlsx` (International students)
- [ ] `NDA Enrolment Report 25-26.xlsx` (Summary)
- [ ] `Application Figures - 25-26.xlsx` (Applications)

**All files present**: Yes / No

---

## Step 3: Extract & Analyze Data ✅

**UK Enrollment Data:**

- [ ] Extract total UK enrollments: `_______`
- [ ] Calculate UK total revenue: `£_______`
- [ ] Identify top 3 courses by student count
- [ ] Extract monthly breakdown (Aug-present)

**International Enrollment Data:**

- [ ] Extract total international enrollments: `_______`
- [ ] Calculate international total revenue: `£_______`
- [ ] Identify top 3 countries by student count
- [ ] Extract monthly breakdown (Aug-present)
- [ ] Confirm USD→GBP conversion rate used: `_______`

**Combined Totals:**

- [ ] Total enrollments: `_______`
- [ ] Total revenue: `£_______`
- [ ] Average revenue per enrollment: `£_______`

---

## Step 4: Update Analysis Files ✅

Create new analysis with today's date:

- [ ] **JSON Analysis**: Create `NDA-Enrollment-Analysis-Complete-{DATE}.json`
  - [ ] Include UK breakdown
  - [ ] Include International breakdown (by country)
  - [ ] Include combined totals
  - [ ] Include timestamp and source date

- [ ] **Markdown Summary**: Update `enrollment-data-2025-26.md`
  - [ ] Update verified revenue figures
  - [ ] Update monthly breakdown tables
  - [ ] Add new findings/observations
  - [ ] Note date of analysis

---

## Step 5: Compare to Prior Data ✅

- [ ] Compare to previous Kelly email data (folder: `_________`)
- [ ] Identify changes:
  - [ ] Total enrollments change: `_______`
  - [ ] Revenue change: `£_______`
  - [ ] New countries appearing: `_________`
  - [ ] Significant course shifts: `_________`

**Key changes to highlight:**
```
1.
2.
3.
```

---

## Step 6: Update Visualizations ✅

- [ ] **Chart**: Regenerate year-over-year comparison chart
  - [ ] Update file: `enrollment-comparison-chart.html`
  - [ ] Verify data points match analysis JSON
  - [ ] Update chart title with new data date

- [ ] **Dashboard** (if applicable):
  - [ ] Update any client dashboard with new figures

---

## Step 7: Archive Previous Analysis ✅

- [ ] Locate previous analysis file (e.g., `NDA-Enrollment-Analysis-Complete-2025-12-08.json`)
- [ ] Add header: `SUPERSEDED by {NEW-DATE} data`
- [ ] Keep in place for reference/audit trail
- [ ] Do NOT delete

---

## Step 8: Quality Assurance ✅

- [ ] **Verify totals**: Spreadsheet row count = Analysis figure
- [ ] **Cross-check revenue**: Spot-check 5-10 fee calculations
- [ ] **Geographic sense**: International countries look reasonable
- [ ] **Seasonality**: Monthly pattern follows academic calendar (Aug-Jul)
- [ ] **YoY comparison**: Numbers compared to 2024-25 baseline
- [ ] **No negative figures**: All counts and revenue >0

**QA Status**: ✅ Pass / ❌ Fail (if fail, note issue): `_________`

---

## Step 9: Documentation & Handoff ✅

- [ ] **Document the update**:
  - [ ] Note what changed in `Document History` section
  - [ ] Timestamp: `{DATE}`

- [ ] **Notify stakeholders** (if applicable):
  - [ ] Client Peter: "New enrollment data received and analyzed"
  - [ ] Any reports that need updating

---

## Step 10: Archive Old Spreadsheets (Optional) ✅

- [ ] Move outdated files from `/spreadsheets/` to archive subfolder
- [ ] Keep only the latest email attachments as active source
- [ ] Label old files with "SUPERSEDED - See /emails/attachments/{DATE}/"

---

## Checklist Complete ✅

**Analysis completed by**: `_____________`
**Completion date**: `_____________`
**Files created/updated**:
- [ ] `NDA-Enrollment-Analysis-Complete-{DATE}.json`
- [ ] `enrollment-data-2025-26.md`
- [ ] `enrollment-comparison-chart.html`
- [ ] Other: `_____________`

**Status**: Ready for reporting

---

## Next Steps

- [ ] Schedule next Kelly email check: ~7 days from receipt date
- [ ] Note next expected data date: `_____________`
- [ ] Set reminder to review if no email by expected date

---

**Template Version**: 1.0
**Last Updated**: 11 December 2025
