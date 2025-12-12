# NDA Enrollment Data Protocol

**Status**: Active
**Last Updated**: 11 December 2025

---

## Source of Truth

**Kelly Rawson's enrollment spreadsheets (received via email) are the definitive source for all NDA enrollment data.**

Each new email from Kelly automatically supersedes all previous data.

---

## How It Works

### 1. Email Reception & Automatic Processing

- **Who sends it**: Kelly Rawson (Student Services Manager) - kelly@nda.ac.uk
  - **Note**: May be forwarded via Paul Riley - still counts as new data from Kelly
- **When**: Weekly, typically Mondays
- **What's included**:
  - `NDA UK Enrolments 25-26.xlsx` - UK student records
  - `NDA International Enrolments 25-26.xlsx` - International student records
  - `NDA Enrolment Report 25-26.xlsx` - Summary/pivot tables
  - `Application Figures - 25-26.xlsx` - Active applications

### 2. Automatic Storage

The **email-sync agent** automatically:
1. Receives Kelly's email
2. Extracts all attachments
3. Stores in: `/clients/national-design-academy/emails/attachments/{DATE}/`
4. Example: `/clients/national-design-academy/emails/attachments/2025-12-08/`

**Do not use files from `/spreadsheets/` folder** - these become outdated and may be duplicates.

### 3. Analysis Updates

When new data arrives:

1. **Check for new folder** in `/emails/attachments/` (sorted by date, newest first)
2. **Extract data** from the latest dated folder
3. **Update analysis JSON**: `/enrolments/NDA-Enrollment-Analysis-Complete-{DATE}.json`
4. **Update comparison charts** with new figures
5. **Archive previous analysis** with superseded tag

---

## Protocol Checklist: When New Data Arrives

**❇️ For Analysts/AI Processing Kelly's New Email:**

- [ ] **Identify** the new folder in `/emails/attachments/{LATEST-DATE}/`
- [ ] **Extract** enrollment data from:
  - `NDA UK Enrolments 25-26.xlsx`
  - `NDA International Enrolments 25-26.xlsx`
- [ ] **Update** `/enrolments/NDA-Enrollment-Analysis-Complete-{NEW-DATE}.json`
- [ ] **Recalculate** monthly breakdowns and revenue totals
- [ ] **Regenerate** charts and comparisons
- [ ] **Update markdown** documents with verified figures
- [ ] **Mark previous analysis** as "Superseded by {NEW-DATE}"
- [ ] **Document** what changed from previous snapshot

---

## Data Elements Extracted

### From International Enrollments File
- **By Country**: Student count and revenue per country
- **By Course**: Course breakdown and per-course revenue
- **Payment Methods**: BACS, Checkout, Overseas transfers
- **Total Revenue**: Calculated from fee column (convert USD → GBP at current rate)
- **Monthly Breakdown**: Enrollments by month (academic year: Aug-Jul)

### From UK Enrollments File
- **By Course**: Student count and revenue per course
- **Payment Methods**: BACS, Checkout, Loan, etc.
- **Total Revenue**: UK fees (GBP)
- **Monthly Breakdown**: Enrollments by month (academic year: Aug-Jul)

### From Application Figures File
- **Application Status**: Auto-approved, Conditional, Awaiting approval, etc.
- **Advertising Source**: Online Search, Instagram, Direct, etc.
- **Current Queue**: Active applications under review

---

## Key Data Points to Always Verify

- ✅ **Total UK enrollments** (should match spreadsheet row count)
- ✅ **Total International enrollments** (should match spreadsheet row count)
- ✅ **Total combined** (UK + International)
- ✅ **Total revenue** (all fees summed)
- ✅ **Geographic breakdown** (countries with enrollment count)
- ✅ **Monthly pattern** (enrollments by month within academic year)
- ✅ **Average fee per enrollment** (total revenue ÷ total students)

---

## File Naming Convention

**Analysis output files should use this naming pattern:**

```
NDA-Enrollment-Analysis-Complete-{YYYY-MM-DD}.json
enrollment-data-{YYYY-MM-DD}.md
nda-enrollment-comparison-{YYYY-MM-DD}.html
```

**Example** (for Dec 8 data):
- `NDA-Enrollment-Analysis-Complete-2025-12-08.json`
- `enrollment-data-2025-12-08.md`
- `nda-enrollment-comparison-2025-12-08.html`

This makes it easy to track which analysis corresponds to which Kelly email.

---

## Supersession Process

When new data arrives:

1. **Previous analysis marked as superseded**
   ```
   Status: ✅ SUPERSEDED by 2025-12-15 data
   ```

2. **New analysis created** with latest date

3. **Archive** previous file (don't delete, keep for reference)

4. **Update** any dashboards/reports to use new analysis

5. **Document** the changes in a changelog entry

---

## Currency Handling

**International fees are stored as USD, must be converted to GBP:**

- **Conversion rate**: 1 USD = 0.79 GBP (current market rate)
- **Document the rate** used in each analysis
- **Update rate** if >2% change occurs

**UK fees** are already in GBP - use as-is.

---

## Monthly Academic Year Pattern (2025-26)

Expected seasonal pattern based on 2024-25 baseline:

| Month | 2024-25 | 2025-26 Est. | Notes |
|-------|---------|--------------|-------|
| August | 33-76 | TBA | Academic year start |
| September | 41-82 | TBA | Peak intake |
| October | 38-50 | TBA | Continued intake |
| November | 20-38 | TBA | Late intake |
| December | 14 | TBA | Holiday period low |
| January | TBD | TBA | Post-holiday recovery |
| Feb-July | TBD | TBA | Spring/summer term |

Use prior year as baseline for comparing new data.

---

## Reporting Guidelines

When reporting to client/stakeholders:

1. **Always cite the source date**: "As of Kelly's {DATE} email"
2. **Show year-over-year** comparison (2024-25 vs 2025-26)
3. **Highlight growth areas** (countries, courses with strong growth)
4. **Flag revenue surprises** (actual vs estimated)
5. **Note incomplete months** (if current month data is partial)

---

## What NOT to Do

❌ **Don't use** spreadsheets from `/spreadsheets/` folder for current analysis
❌ **Don't mix** data from multiple Kelly emails (use latest only)
❌ **Don't** manually calculate totals - extract directly from files
❌ **Don't** assume any dataset is current - always check the folder date
❌ **Don't** overwrite analysis without archiving previous version

---

## Contact

**Data Questions**: Email Kelly Rawson (kelly@nda.ac.uk)
**Analysis Issues**: Reference this protocol and the dated analysis file

---

**Last Updated**: 11 December 2025
**Next Expected Data**: ~18 December 2025 (weekly Monday email)
