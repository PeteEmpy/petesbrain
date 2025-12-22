# Google Ads Audit Framework Guide

**Last Updated**: December 16, 2025
**Framework Source**: GOOGLE-ADS-AUDIT-FRAMEWORK.csv (457 items)
**Purpose**: Comprehensive Google Ads account audit and optimisation methodology

---

## Overview

The Google Ads Audit Framework is a **400+ item checklist** organised into 6 workflow sections covering everything from initial setup to ongoing optimisation. This framework represents industry best practices for managing Google Ads accounts at scale.

**Framework File**: `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv`

---

## Framework Structure

### 6 Major Sections

| Section | Focus Area | Item Count | Primary Use |
|---------|-----------|------------|-------------|
| **1 - FOUNDATION** | Tracking, analytics, conversions, site optimisation | ~80 items | New client onboarding |
| **2 - ATTRIBUTION** | Model selection, conversion path analysis | ~10 items | Strategic benchmarking |
| **3 - PLANNING** | Strategy, keyword research, account structure | ~70 items | Pre-build planning |
| **4 - BUILDING** | Campaign creation, ad groups, extensions, PMax | ~160 items | Implementation phase |
| **5 - OPTIMISATION** | Weekly/ongoing performance management | ~140 items | Routine management |
| **6 - SHOPPING** | Merchant feed, shopping campaign management | ~25 items | E-commerce specific |

### Column Structure

Each item in the framework contains:

| Column | Purpose | Values |
|--------|---------|--------|
| **Checkbox** | Completion tracking | TRUE/FALSE |
| **Icon** | Visual indicator | 💡 (insight), 🚨 (warning), ✓ (check) |
| **Action Type** | Task verb | Check, Apply, Review, Enable, Watch |
| **Task/Item** | Specific action description | Detailed task text |
| **Frequency** | Execution cadence | Once, Daily, Weekly, Bi-weekly, Monthly, Quarterly, Ongoing, Automated |
| **Note** | Additional context | 💬 (note), ⌛ (time-sensitive) |
| **Impact** | Priority level | HIGH, MID, LOW |
| **Resources** | Documentation links | DOC 📑, SCRIPT 🛠️, VIDEO ▶️, TOOL 🔗 |

---

## When to Use This Framework

### 1. Comprehensive Client Audits

**Frequency**: Annually for major clients, or when performance issues require deep investigation

**Process**:
1. Create audit document: `clients/{client}/audits/{year}-comprehensive-audit.md`
2. Work through framework sections 1-6
3. Focus on HIGH-impact items first
4. Document findings and recommendations
5. Create P0/P1 tasks for critical issues

**Major Clients for Annual Audits**:
- Smythson
- Tree2mydoor
- Devonshire Hotels
- Superspace
- Clear Prospects

### 2. New Client Onboarding

**Frequency**: Once per new client

**Process**:
1. Use **Section 1 (FOUNDATION)** as primary checklist
2. Verify tracking setup (GA4, GTM, conversion tags)
3. Audit existing account structure
4. Document findings in `clients/{client}/documents/onboarding-audit.md`
5. Create onboarding tasks for critical issues

**See**: `docs/CLIENT-ONBOARDING-AUDIT-CHECKLIST.md` for extracted Foundation items

### 3. Campaign Build Projects

**Frequency**: When building new campaigns or restructuring accounts

**Process**:
1. Use **Section 3 (PLANNING)** for strategic planning
2. Use **Section 4 (BUILDING)** for implementation checklist
3. Reference framework items in build documentation
4. Verify all HIGH-impact items completed before launch

### 4. Performance Troubleshooting

**Frequency**: When performance drops significantly or anomalies detected

**Process**:
1. Start with **Section 5 (OPTIMISATION)** → Strategic Decisions
2. Check recent major changes
3. Review tracking integrity (Section 1)
4. Analyse specific campaign types (PMax, Shopping, Search sections)
5. Document root cause and remediation

### 5. Weekly Report Enhancement

**Frequency**: Ongoing, embedded in weekly report process

**Process**:
1. Map weekly report recommendations to framework sections
2. Reference framework when making strategic recommendations
3. Cite framework items to show best-practice alignment
4. Use framework to identify gaps in current optimisation

**Example Mapping**:
- Budget issues → Section 5 - Budget & KPI
- Search term waste → Section 5 - Keyword & Query
- Poor ROAS → Section 5 - Bidding
- Asset performance → Section 4 - Performance Max Assets

---

## Integration with PetesBrain Systems

### With google-ads-campaign-audit Skill

**Location**: `.claude/skills/google-ads-campaign-audit/`

**Integration**:
- Audit skill conducts **data analysis** (GAQL queries, metrics)
- Framework provides **strategic structure** (what to check)
- Combined = comprehensive audit output

**Implementation**:
- Audit skill outputs results mapped to framework sections
- HIGH/MID/LOW impact ratings applied to findings
- Framework section headers included in audit reports

### With google-ads-weekly-report Skill

**Location**: `.claude/skills/google-ads-weekly-report/`

**Integration**:
- Weekly reports identify performance issues
- Recommendations mapped to framework sections
- Shows clients: "recommendations based on industry best practices"

**Implementation**:
- Add framework section references to recommendations
- Cite specific framework items when relevant
- Use framework terminology in analysis

### With Knowledge Base

**Relationship**: Complementary, not duplicative

| System | Purpose | Content Type |
|--------|---------|--------------|
| **Knowledge Base** | Strategic insights, examples, case studies | "How to optimise PMax campaigns" |
| **Framework** | Checklist of what to audit/check | "Review asset performance column" |
| **Integration** | KB articles reference framework sections | "See Framework Section 5 - Performance Max for checklist" |

**Do NOT**: Duplicate framework items into KB articles
**Do**: Cross-reference framework sections from KB articles
**Do**: Link KB articles in framework Resources column

---

## Frequency-Based Workflow

The framework uses frequency tags to organise routine work:

### Daily Tasks

**Total**: ~10 items (Section 5 - Optimisation)

**Key Items**:
- Anomaly detection and tracking verification
- Budget monitoring and overspend protection
- Disapproval checks

**PetesBrain Integration**: Automated via `daily-intel-report` agent

### Weekly Tasks

**Total**: ~30 items (Section 5 - Optimisation)

**Key Items**:
- Keyword performance review
- Search term report analysis
- Budget correction
- Ad performance review
- Priority campaign metrics

**PetesBrain Integration**: `google-ads-weekly-report` skill

### Bi-Weekly Tasks

**Total**: ~20 items (Section 5 - Optimisation)

**Key Items**:
- Secondary campaign review
- RSA optimisation
- Audience performance
- Asset group analysis

### Monthly Tasks

**Total**: ~40 items (Section 5 - Optimisation)

**Key Items**:
- Attribution model review
- Ad copy testing results
- Extension performance
- Geographic analysis
- Automated rule review

### Quarterly Tasks

**Total**: ~8 items (Section 2 - Attribution)

**Key Items**:
- Attribution model benchmarking
- Path length analysis
- Top conversion paths
- Strategic model updates

### Once Tasks

**Total**: ~200 items (Sections 1, 3, 4)

**Key Items**:
- Initial account setup (Section 1)
- Campaign build checklist (Section 4)
- Strategic planning (Section 3)

---

## Priority System

### HIGH Impact Items

**Definition**: Critical for account performance, tracking integrity, or compliance

**Examples**:
- ✅ Conversion tracking configured correctly
- ✅ GA4 property linked to Google Ads
- ✅ Auto-applied recommendations disabled
- ✅ Branded keywords negative against non-brand campaigns
- ✅ Budget limited campaigns optimised

**Action**: Complete HIGH items first in any audit

### MID Impact Items

**Definition**: Important for optimisation and efficiency, but not critical

**Examples**:
- ✅ GTM conversion linker installed
- ✅ Remarketing audiences configured
- ✅ Callout extensions applied
- ✅ Audience observations applied

**Action**: Complete after HIGH items, prioritise based on client needs

### LOW Impact Items

**Definition**: Nice-to-have, minor optimisations, edge cases

**Examples**:
- ✅ Spam referrals excluded from Analytics
- ✅ Self-referrals excluded
- ✅ Keyword labels for reporting

**Action**: Complete when time permits or for comprehensive audits

---

## Section-by-Section Guide

### Section 1: FOUNDATION (Lines 3-84)

**Purpose**: Ensure tracking, analytics, and conversion setup is correct

**Sub-Sections**:
1. **Clarity** - Business rationale and messaging
2. **Tags** - GTM, conversion linker, Analytics code
3. **Google Analytics 4** - Property setup, audiences, enhanced measurement
4. **Conversion** - Macro/micro conversions, attribution
5. **Destination** - Website SSL, speed, SEO
6. **Shopping Specific** - Merchant Centre setup (e-commerce only)
7. **Performance Max** - Enhanced conversions, lead quality

**Use Cases**:
- ✅ New client onboarding
- ✅ Tracking audit after performance anomalies
- ✅ Pre-build verification

**Key Insight**: Get foundation right BEFORE building campaigns

### Section 2: ATTRIBUTION (Lines 85-93)

**Purpose**: Select and benchmark appropriate attribution model

**Sub-Sections**:
1. **Benchmark Your Situation** - Path length, conversion paths, model comparison

**Use Cases**:
- ✅ Quarterly strategic review
- ✅ When conversion volume increases significantly
- ✅ Before major campaign restructuring

**Key Insight**: Attribution model should match customer journey complexity

### Section 3: PLANNING (Lines 94-134)

**Purpose**: Strategic planning before campaign build

**Sub-Sections**:
1. **Find Your Keywords** - Keyword research methodology
2. **Budget** - Budget allocation, target setting
3. **Bidding** - Bid strategy selection

**Use Cases**:
- ✅ New client onboarding
- ✅ Campaign build projects
- ✅ Account restructuring

**Key Insight**: "Do you want ROI or volume? Pick a side"

### Section 4: BUILDING (Lines 135-257)

**Purpose**: Campaign creation and implementation checklist

**Sub-Sections**:
1. **Campaign Hygiene** - Naming conventions, organisation
2. **Brand** - Brand campaign setup
3. **Search** - Search campaign structure
4. **Performance Max** - PMax setup (extensive sub-sections)
   - Structure strategy
   - Ecommerce specific
   - Audience signals
   - Budget & bidding
   - Setup final checks
   - Assets
5. **Account** - Account-level settings
6. **Audiences** - Audience setup and observation

**Use Cases**:
- ✅ New campaign builds
- ✅ Account restructuring
- ✅ PMax migration from Standard Shopping

**Key Insight**: Extensive PMax guidance (60+ items) reflects campaign importance

### Section 5: OPTIMISATION (Lines 258-433)

**Purpose**: Ongoing performance management and improvement

**Sub-Sections**:
1. **Strategic Decisions** - High-level optimisation principles
2. **Account Structure** - When to split campaigns/ad groups
3. **Search Optimisation Routine** - Weekly process
4. **Week 1** - Data gathering phase (first week of management)
5. **Budget & KPI** - Budget management, overspend protection
6. **Keyword & Query** - Keyword decision matrix, search terms
7. **Search Terms** - Query analysis and negative keyword mining
8. **Bidding** - Bid strategy optimisation
9. **Tests** - Testing methodology and ad copy testing
10. **Ad Optimisation** - RSA optimisation, DKI, ad copy creation
11. **Performance Max** - PMax-specific optimisation
12. **Audiences** - Audience performance and adjustments
13. **Ad Extensions** - Extension optimisation
14. **Display** - Display campaign optimisation
15. **Targeting & Data** - Geographic, schedule, attribution
16. **Shared Libraries** - Negative lists, placement exclusions
17. **Automated Routines** - Scripts, rules, alerts
18. **Disapprovals** - Monitoring disapproved items

**Use Cases**:
- ✅ Weekly optimisation routine
- ✅ Performance troubleshooting
- ✅ Monthly reviews

**Key Insight**: Largest section (140+ items) - reflects ongoing nature of optimisation

### Section 6: SHOPPING (Lines 434-456)

**Purpose**: Google Shopping and Merchant Centre optimisation

**Sub-Sections**:
1. **Merchant Feed** - Product feed requirements and optimisation
2. **Shopping Specific** - Shopping campaign structure and bidding

**Use Cases**:
- ✅ E-commerce client audits
- ✅ Product feed troubleshooting
- ✅ Shopping campaign optimisation

**Key Insight**: Cross-references "Product feed optimisation" doc (not in PetesBrain KB yet)

---

## Practical Examples

### Example 1: New Client Onboarding (Tree2mydoor)

**Scenario**: New e-commerce client selling live Christmas trees

**Process**:
1. Work through Section 1 (FOUNDATION)
2. Create document: `clients/tree2mydoor/documents/onboarding-audit.md`
3. Check HIGH-impact items:
   - ✅ GA4 tracking configured?
   - ✅ Conversion actions setup?
   - ✅ Merchant Centre linked?
   - ✅ Ecommerce tracking enabled?
4. Check Section 6 (SHOPPING) items:
   - ✅ Product feed quality?
   - ✅ Product titles optimised?
   - ✅ Categories correct?
5. Document findings and create P0 tasks for critical issues

**Output**: Comprehensive onboarding audit with prioritised action items

### Example 2: Quarterly Audit (Smythson)

**Scenario**: Annual comprehensive audit for luxury brand client

**Process**:
1. Create document: `clients/smythson/audits/2025-annual-comprehensive-audit.md`
2. Work through all 6 sections systematically
3. Focus on HIGH-impact items in each section
4. Run GAQL queries to verify findings
5. Document recommendations with framework references
6. Create tasks for HIGH-impact issues

**Output**:
- Comprehensive audit report
- Prioritised recommendations
- Tasks for implementation

### Example 3: Performance Troubleshooting (Devonshire Hotels)

**Scenario**: ROAS dropped 25% week-over-week, investigate cause

**Process**:
1. Start with Section 5 - Strategic Decisions:
   - Check: No major changes made recently? ✅
   - Review: Trend and spend from previous periods? ✅
   - Check: Anomaly detected - review tracking first? ⚠️
2. Discover: Conversion tracking dropped off on booking pages
3. Jump to Section 1 - Conversion:
   - Check: Conversion tag firing on all pages? ❌
   - Check: Go through conversion process yourself? ✅
4. Root cause: Website update broke conversion tag
5. Create P0 task: Fix conversion tracking immediately

**Output**: Root cause identified, remediation task created

### Example 4: Weekly Report Enhancement (Superspace)

**Scenario**: Generating weekly report, enhance with framework references

**Process**:
1. Run `google-ads-weekly-report` skill
2. Identify recommendations (e.g., "High search term waste detected")
3. Map to framework: Section 5 - Search Terms
4. Add framework reference to recommendation:
   - "Search term waste detected (Framework 5.7). Recommendation: Apply negative keywords based on keyword decision matrix (Framework 5.6.2)"
5. Shows client: recommendations based on industry best practices

**Output**: Enhanced weekly report with framework alignment

---

## Creating Client-Specific Audit Documents

### Template Structure

```markdown
# [Client Name] - Comprehensive Google Ads Audit

**Date**: [Date]
**Account ID**: [Google Ads Customer ID]
**Auditor**: Peter Empson
**Framework Version**: December 2025 (457 items)

---

## Executive Summary

[Brief overview of audit scope and key findings]

---

## 1 - FOUNDATION

### Tracking & Analytics
- [ ] HIGH: GA4 tracking configured correctly
- [ ] HIGH: Conversion actions setup and firing
- [ ] MID: GTM conversion linker installed

**Findings**:
- [Document specific findings]

**Recommendations**:
- [Prioritised recommendations with P0/P1/P2 labels]

---

## 2 - ATTRIBUTION

### Model Benchmarking
- [ ] HIGH: Attribution model benchmarked quarterly
- [ ] HIGH: Path length analysis reviewed

**Findings**:
- [Document specific findings]

---

[Continue for sections 3-6]

---

## Priority Action Items

### P0 - Critical (Complete Immediately)
1. [Task with framework reference]

### P1 - High Priority (Complete This Week)
1. [Task with framework reference]

### P2 - Important (Complete This Month)
1. [Task with framework reference]

---

## Appendix: Framework Items Checked

Total items reviewed: [X/457]
- Section 1: [X/80]
- Section 2: [X/10]
- Section 3: [X/70]
- Section 4: [X/160]
- Section 5: [X/140]
- Section 6: [X/25]
```

### Saving Location

**Comprehensive Audits**: `clients/{client}/audits/{year}-comprehensive-audit.md`
**Onboarding Audits**: `clients/{client}/documents/onboarding-audit-{date}.md`
**Troubleshooting Audits**: `clients/{client}/documents/troubleshooting-audit-{date}-{issue}.md`

---

## Automation Opportunities

The framework identifies tasks suitable for automation:

### Currently Automated in PetesBrain

| Framework Item | Automation | Status |
|----------------|------------|--------|
| Daily anomaly detection | `daily-intel-report` agent | ✅ Active |
| Budget monitoring | `budget-monitor` agent | ✅ Active |
| Disapproval monitoring | `disapproval-monitor` agent | ✅ Active |
| Weekly performance review | `google-ads-weekly-report` skill | ✅ Active |

### Automation Candidates

| Framework Item | Potential Automation | Priority |
|----------------|---------------------|----------|
| Negative keyword list builder | Script (referenced in framework) | HIGH |
| Link checker | Script (referenced in framework) | MID |
| Low quality score alert | Script (referenced in framework) | MID |
| 404 error alerts | GA4 alert | HIGH |
| Duplicate keyword remover | Script (referenced in framework) | MID |
| Query cannibalisation detection | Script (referenced in framework) | MID |

**Next Steps**: Evaluate scripts referenced in framework for PetesBrain integration

---

## Best Practices

### When Conducting Audits

1. **Start with HIGH-impact items** - Complete these before moving to MID/LOW
2. **Document as you go** - Don't wait until end to write findings
3. **Run GAQL queries for verification** - Don't rely on UI alone
4. **Create tasks immediately** - Don't defer P0 issues
5. **Reference framework items** - Shows systematic approach

### When Using for Weekly Work

1. **Don't check every item weekly** - Use frequency tags as guide
2. **Focus on Section 5 (OPTIMISATION)** - This is the weekly section
3. **Map findings to framework** - Enhances professionalism
4. **Track recurring issues** - If same item fails repeatedly, investigate root cause

### When Onboarding Clients

1. **Section 1 is non-negotiable** - Foundation must be solid
2. **Document "not applicable" items** - Explain why (e.g., no e-commerce = skip Section 6)
3. **Create onboarding checklist** - Extract relevant items into client-specific doc
4. **Verify before launch** - Don't launch campaigns with HIGH-impact items incomplete

---

## Updating the Framework

### When to Update

- **Annually**: Review framework against Google Ads product updates
- **After major changes**: When Google releases new campaign types or features
- **Based on experience**: Add client-specific best practices

### Update Process

1. Review original framework source (external)
2. Document changes in `docs/AUDIT-FRAMEWORK-CHANGELOG.md`
3. Update `GOOGLE-ADS-AUDIT-FRAMEWORK.csv`
4. Update this guide with new sections/items
5. Communicate changes to weekly report and audit processes

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv` | Master framework (457 items) |
| `docs/CLIENT-ONBOARDING-AUDIT-CHECKLIST.md` | Extracted Section 1 items |
| `docs/GOOGLE-ADS-PROTOCOL.md` | Change management protocol |
| `docs/DATA-VERIFICATION-PROTOCOL.md` | Data accuracy protocol |
| `.claude/skills/google-ads-campaign-audit/` | Automated audit skill |
| `.claude/skills/google-ads-weekly-report/` | Weekly report skill |

---

## Quick Reference

### Most Important HIGH-Impact Items (Top 10)

1. ✅ **Conversion tracking configured correctly** (Foundation)
2. ✅ **GA4 linked to Google Ads** (Foundation)
3. ✅ **Auto-applied recommendations disabled** (Building)
4. ✅ **Branded keywords negative against non-brand campaigns** (Building)
5. ✅ **Attribution model appropriate for business** (Attribution)
6. ✅ **Budget limited campaigns optimised** (Optimisation)
7. ✅ **Search term report reviewed weekly** (Optimisation)
8. ✅ **Anomaly detection and tracking verification daily** (Optimisation)
9. ✅ **Micro conversions configured** (Foundation)
10. ✅ **Merchant Centre diagnostics clean** (Shopping - e-commerce only)

### Framework Stats

- **Total Items**: 457
- **HIGH Impact**: ~120 items (26%)
- **MID Impact**: ~180 items (39%)
- **LOW Impact**: ~40 items (9%)
- **Unrated**: ~117 items (26% - typically sub-headers or guidance)

### Section Weights

| Section | Items | % of Total |
|---------|-------|-----------|
| Section 1: Foundation | 80 | 18% |
| Section 2: Attribution | 10 | 2% |
| Section 3: Planning | 70 | 15% |
| Section 4: Building | 160 | 35% |
| Section 5: Optimisation | 140 | 31% |
| Section 6: Shopping | 25 | 5% |

---

**This framework is your strategic foundation for comprehensive Google Ads management. Use it systematically, reference it consistently, and adapt it to each client's unique needs.**
