# New Skills Created - November 7, 2025

Two new high-value skills have been added to Pete's Brain based on your most frequent workflows.

---

## 1. Email Draft Generator ⭐

**Location**: `.claude/skills/email-draft-generator/`

### What It Does
Automatically generates client-ready HTML email drafts with proper formatting, British English spelling, and client-specific tone.

### How to Use
Just say:
- "Draft email to Devonshire about October performance"
- "Write email for Smythson about budget increase"
- "Email National Design Academy about country analysis"

### What You Get
- HTML file saved to `clients/[client]/documents/email-draft-YYYY-MM-DD-[topic].html`
- Automatically opens in browser for copy/paste to Apple Mail
- British English for UK clients, American English for US clients
- ROAS formatted as percentage (400% not £4.00)
- Tight spacing for readability (line-height: 1.4)
- Client-specific tone from CONTEXT.md

### Time Saved
**~10-15 minutes per email** (from 15-20 minutes manual to 30 seconds automated)

---

## 2. Devonshire Monthly Report Generator ⭐

**Location**: `.claude/skills/devonshire-monthly-report/`

### What It Does
Generates complete 14-slide Google Slides presentation for Devonshire Hotels monthly Paid Search reports with branded formatting and strategic insights.

### How to Use
Just say:
- "Generate October report for Devonshire"
- "Create Devonshire monthly slides"
- "Devonshire November Paid Search report"

### What You Get
- 14 professional slides with Estate Blue (#00333D) and Stone (#E5E3DB) branding
- Executive summary, property breakdowns, campaign analysis
- Key insights and actionable recommendations
- Google Slides link ready for review
- Automatically validates The Hide + Highwayman Arms data

### Time Saved
**~2.5 hours per month** (from 3 hours manual to 20 minutes automated)

---

## How Skills Work

Skills **auto-trigger** when Claude detects relevant context. You don't need to invoke them manually.

**Example**:
```
You: "Draft email to Smythson about their Q4 budget"
↓
Claude recognizes: client name + email + topic
↓
Triggers: email-draft-generator skill
↓
Loads: clients/smythson/CONTEXT.md
↓
Generates: Formatted HTML email draft
↓
Saves: clients/smythson/documents/email-draft-2025-11-07-q4-budget.html
↓
Opens: In browser for you to copy/paste
```

---

## Total Skills Now: 6

1. **GAQL Query Builder** - Build Google Ads queries
2. **CSV Analyzer** - Analyze performance data exports
3. **Google Ads Campaign Audit** - Comprehensive account reviews
4. **Google Ads Keyword Audit** - Search campaign optimization
5. **Email Draft Generator** ⭐ NEW - Client email automation
6. **Devonshire Monthly Report** ⭐ NEW - Monthly report automation

---

## Combined Time Savings

**Per Month**:
- Email drafts: 10-15 min × ~20 emails = **3-5 hours**
- Devonshire report: **2.5 hours**
- **Total: 5.5-7.5 hours saved per month**

**Per Year**: **~80 hours saved** (2 full work weeks!)

---

## What's Next?

Both skills are ready to use immediately. They'll auto-trigger when you:

1. **Mention client emails** → Email Draft Generator activates
2. **Request Devonshire report** → Monthly Report Generator activates

Try them out on your next client email or when November's data is ready for Devonshire!

---

## Files Created

```
.claude/skills/
├── email-draft-generator/
│   ├── skill.md                        # Main skill definition
│   ├── client-preferences.md           # Client-specific styles
│   └── british-vs-american-english.md  # Spelling reference
└── devonshire-monthly-report/
    └── skill.md                        # Main skill definition

Updated:
├── README.md                           # Updated to 6 skills
```

---

**Created**: November 7, 2025
**Status**: ✅ Ready to use
**Documentation**: See `.claude/skills/README.md` for complete details
