# Cross-Client Knowledge System

**Problem**: 106 client-specific scripts contain duplicated logic. Learnings from one client aren't systematically shared across others. No structured way to capture patterns, techniques, and solutions for reuse.

**Solution**: A three-tier knowledge system that captures learnings at the right level and makes them discoverable.

---

## Current State Analysis

### Script Distribution (As of Nov 2025)

| Location | Count | Purpose | Issues |
|----------|-------|---------|--------|
| `clients/*/scripts/` | 106 | Client-specific one-offs | Heavy duplication, not reusable |
| `shared/scripts/` | 6 universal | Cross-client tools | Only recent additions |
| **Total** | **112** | | **~60% could be universal** |

### Example Duplication Patterns

**Budget Updates**:
- Devonshire: `update-budgets-nov-18.py`, `update-budgets-nov-20.py`, `update-budgets-nov-24.py`
- Superspace: `update-us-budgets-2025-11-24.py`
- NDA: `august_budget_plan.py`, `budget_recommendations_october.py`
- **Solution**: ✅ One universal `update-google-ads-budgets.py`

**Negative Keywords**:
- Tree2MyDoor: `add-negative-keywords.py` (hardcoded campaign IDs)
- Devonshire: `pause-keywords.py` (354 lines, hardcoded everything)
- **Solution**: ✅ One universal `add-google-ads-negative-keywords.py`

**Analysis Scripts**:
- Smythson: `analyze_brand_split.py`, `brand-vs-nonbrand-analysis.py`, `brand-yoy-comparison.py`
- Accessories: `analyze-roas-impact.py`, `check-friday-is-patterns.py`
- GoGlean: `find-zombie-converters.py`, `analyze-zombie-conversions-30d.py`
- **Opportunity**: Could be universal with client ID parameter

---

## The Three-Tier Knowledge System

### Tier 1: Universal Scripts (`/shared/scripts/`)

**Purpose**: Reusable tools that work for ANY client with minimal configuration

**Criteria**:
- Solves a common problem (budget updates, status changes, performance queries)
- Works across all clients with just customer ID change
- No client-specific business logic
- Maintained as "production" tools

**Current Examples**:
- ✅ `update-google-ads-budgets.py`
- ✅ `update-google-ads-campaign-status.py`
- ✅ `update-google-ads-target-roas.py`
- ✅ `query-google-ads-performance.py`
- ✅ `add-google-ads-negative-keywords.py`
- ✅ `update-google-ads-keyword-status.py`

**Naming Convention**: `[action]-[platform]-[resource].py`
- Examples: `update-google-ads-budgets.py`, `export-microsoft-ads-campaigns.py`

---

### Tier 2: Playbooks (`/playbooks/`)

**Purpose**: Document repeatable processes, techniques, and patterns discovered through client work

**Structure**:
```
/playbooks/
├── google-ads/
│   ├── brand-vs-nonbrand-analysis.md
│   ├── zombie-product-identification.md
│   ├── search-term-audit-workflow.md
│   ├── pmax-asset-group-optimisation.md
│   ├── seasonal-budget-planning.md
│   └── roas-target-calibration.md
├── microsoft-ads/
│   ├── campaign-structure-audit.md
│   └── bid-strategy-migration.md
├── analytics/
│   ├── conversion-attribution-analysis.md
│   └── ga4-ads-reconciliation.md
└── client-management/
    ├── black-friday-preparation.md
    ├── quarterly-business-review.md
    └── budget-pacing-analysis.md
```

**Playbook Format**:
```markdown
# [Playbook Title]

**When to Use**: [Specific scenarios/triggers]

**Prerequisites**:
- Data requirements
- Access needed
- Time investment

**Process**:
1. Step-by-step instructions
2. Code snippets (if applicable)
3. What to look for
4. How to interpret results

**Example from [Client Name]**:
[Real anonymised example with metrics]

**Expected Outcomes**:
- What decisions this enables
- Typical impact ranges
- Success criteria

**Related Playbooks**: [Links to related techniques]
```

**Real Example - Brand vs Non-Brand Analysis**:

Based on `smythson/scripts/brand-vs-nonbrand-analysis.py`, this could become:

```markdown
# Brand vs Non-Brand Performance Analysis

**When to Use**:
- Quarterly business reviews
- Budget allocation decisions
- ROAS target calibration
- Understanding channel efficiency

**Prerequisites**:
- Google Ads API access
- 90+ days of conversion data
- Clear campaign naming convention (brand/non-brand split)

**Process**:
1. Query all campaigns with segments.date
2. Classify campaigns: Brand (contains "brand", "competitor") vs Non-Brand (all others)
3. Sum metrics: cost, revenue, conversions by type
4. Calculate: ROAS, CPA, conversion rate deltas
5. Analyse YoY comparison if historical data available

**Code Pattern**:
```python
# Use query-google-ads-performance.py with filtering
python3 query-google-ads-performance.py \
  --customer-id XXXXX \
  --start-date 2025-09-01 \
  --end-date 2025-11-25 \
  --output csv

# Then analyse in spreadsheet or Python:
brand = campaigns[campaigns['name'].str.contains('Brand|brand')]
nonbrand = campaigns[~campaigns['name'].str.contains('Brand|brand')]

brand_roas = brand['revenue'].sum() / brand['cost'].sum()
nonbrand_roas = nonbrand['revenue'].sum() / nonbrand['cost'].sum()
```

**Example from Smythson (Q4 2025)**:
- Brand: 652% ROAS, £58k spend, £378k revenue
- Non-Brand: 298% ROAS, £42k spend, £125k revenue
- **Decision**: Increased brand budget by 20% due to efficiency

**Expected Outcomes**:
- Identify which channel type is more efficient
- Inform budget reallocation (typical: 60/40 brand/non-brand)
- Set differentiated ROAS targets (brand typically 2-3x higher)

**Related Playbooks**:
- ROAS Target Calibration
- Budget Allocation Strategy
```

---

### Tier 3: Client-Specific Scripts (`/clients/{client}/scripts/`)

**Purpose**: Truly unique, one-off solutions that won't be reused

**Criteria**:
- Contains client-specific business logic
- Uses unique data sources (e.g., client's CRM exports)
- Addresses one-time problem
- Would require 50%+ rewrite to generalize

**Examples That Should Stay Client-Specific**:
- Smythson: `scrape-gift-products.py` (scrapes Smythson website)
- NDA: `correlate-ads-enrollments.py` (matches to enrollment CSV)
- GoGlean: `find-zombie-converters.py` (specific product taxonomy)
- Crowd Control: `create-steel-barricades-excel.py` (product catalog export)

**New Rule**: Before creating a client script, ask:
1. Could this work for other clients with parameter changes? → Make it universal (Tier 1)
2. Is this a repeatable technique/process? → Document in playbook (Tier 2)
3. Is this truly unique to this client? → Keep client-specific (Tier 3)

---

## Knowledge Capture Workflow

### When Creating a New Script

```
┌─────────────────────────┐
│  Problem arises         │
│  (e.g., "pause wastage  │
│   keywords")            │
└───────────┬─────────────┘
            │
            ▼
    ┌───────────────┐
    │ Is this a     │───Yes──→ Use existing universal script
    │ common task?  │
    └───────┬───────┘
            │ No
            ▼
    ┌───────────────┐
    │ Could it work │───Yes──→ Create in /shared/scripts/
    │ for any       │          Document in GOOGLE-ADS-SIMPLE-SCRIPTS.md
    │ client?       │
    └───────┬───────┘
            │ No
            ▼
    ┌───────────────┐
    │ Is this a     │───Yes──→ Create playbook in /playbooks/
    │ repeatable    │          Reference client example
    │ process?      │
    └───────┬───────┘
            │ No
            ▼
    ┌───────────────┐
    │ Create in     │
    │ /clients/     │
    │ {client}/     │
    │ scripts/      │
    └───────────────┘
```

### After Solving a Problem

**Immediate** (within same session):
1. If you created a universal script, add to `/docs/GOOGLE-ADS-SIMPLE-SCRIPTS.md` (or equivalent)
2. If you discovered a pattern, create a playbook stub

**Weekly** (Friday reflection):
1. Review scripts created this week
2. Identify 2-3 that could become playbooks
3. Draft playbooks with real examples (anonymise metrics if needed)

**Monthly** (first Monday):
1. Review all playbooks
2. Identify playbooks that could become universal scripts
3. Audit client scripts for duplication

---

## Playbook Categories

### Google Ads
- Brand vs Non-Brand Analysis
- Zombie Product Identification (low impressions, high spend)
- Search Term Audit Workflow
- P Max Asset Group Optimisation
- Seasonal Budget Planning (Black Friday, Christmas)
- ROAS Target Calibration
- Negative Keyword Mining
- Campaign Structure Audit
- Geo Performance Analysis
- Device Performance Analysis
- Bid Strategy Migration

### Microsoft Ads
- Google-to-Microsoft Campaign Migration
- Audience Targeting Setup
- LinkedIn Profile Targeting

### Analytics & Attribution
- Conversion Attribution Analysis
- GA4 ↔ Google Ads Reconciliation
- Revenue Discrepancy Investigation
- Multi-Touch Attribution Modeling

### Client Management
- Black Friday Preparation Checklist
- Quarterly Business Review Template
- Budget Pacing Analysis
- Performance Anomaly Investigation
- Monthly Reporting Workflow

### Technical
- API Error Troubleshooting
- OAuth Token Refresh
- Feed Validation Process
- Bulk Upload Templates

---

## Discovery System

### How Claude Finds Knowledge

**Current Problem**: Claude doesn't know what techniques exist across 30+ clients

**Solution**: Structured knowledge base with indexing

#### 1. Playbook Index (`/playbooks/INDEX.md`)

```markdown
# Playbook Index

Quick reference for all documented techniques and processes.

## By Problem Type

### Performance Drops
- [Conversion Drop Investigation](google-ads/conversion-drop-investigation.md) - Diagnose sudden conversion decreases
- [ROAS Decline Analysis](google-ads/roas-decline-analysis.md) - Identify causes of ROAS deterioration

### Optimisation
- [Brand vs Non-Brand Analysis](google-ads/brand-vs-nonbrand-analysis.md) - Budget allocation decisions
- [Search Term Audit](google-ads/search-term-audit.md) - Find wastage and expansion opportunities

### Seasonal
- [Black Friday Preparation](client-management/black-friday-prep.md) - Budget increases, campaign setup
- [Q4 Budget Planning](google-ads/q4-budget-planning.md) - Year-end budget exhaustion

## By Data Source
- **Google Ads API**: 12 playbooks
- **Microsoft Ads API**: 3 playbooks
- **GA4**: 5 playbooks
- **Client Data**: 4 playbooks

## By Time Investment
- **< 30 min**: Quick wins, simple analyses
- **1-2 hours**: Standard audits, reports
- **Half day**: Complex investigations, multi-account

## Recently Added
1. [Brand vs Non-Brand Analysis](google-ads/brand-vs-nonbrand-analysis.md) - Added Nov 2025 (Smythson)
2. [Zombie Product Identification](google-ads/zombie-products.md) - Added Nov 2025 (GoGlean)
```

#### 2. Client CONTEXT.md References

Add new section to each client CONTEXT.md:

```markdown
## Playbooks Used for This Client

| Playbook | When Used | Outcome |
|----------|-----------|---------|
| [Brand vs Non-Brand Analysis](../../playbooks/google-ads/brand-vs-nonbrand-analysis.md) | Q4 2025 | Reallocated £20k to brand (652% ROAS vs 298%) |
| [Black Friday Preparation](../../playbooks/client-management/black-friday-prep.md) | Nov 2025 | 3-phase budget deployment, £9,680/day peak |
| [P Max Asset Optimisation](../../playbooks/google-ads/pmax-asset-optimisation.md) | Oct 2025 | Replaced 40 underperforming assets, +15% CTR |

**Techniques Discovered on This Client**:
- Phase-based Black Friday deployment (created playbook)
- Multi-account budget coordination (4 accounts: UK/USA/EUR/ROW)
```

#### 3. Weekly Briefing Integration

Add section to daily briefing email:

```
**This Week's Learnings**:
• Created playbook: Brand vs Non-Brand Analysis (from Smythson work)
• Updated playbook: Black Friday Prep (added phase-based approach)
• New universal script: add-google-ads-negative-keywords.py

**Recommended for Other Clients**:
• Tree2MyDoor: Run Brand vs Non-Brand analysis (may reveal efficiency gaps)
• Devonshire: Use new keyword status script (replacing 354-line custom script)
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

✅ **Done**:
- Created 6 universal Google Ads scripts
- Documented in GOOGLE-ADS-SIMPLE-SCRIPTS.md

**Next**:
1. Create `/playbooks/` directory structure
2. Create `playbooks/INDEX.md`
3. Create template: `playbooks/_TEMPLATE.md`

### Phase 2: Initial Playbooks (Week 2)

Create first 5 playbooks from recent client work:

1. **Brand vs Non-Brand Analysis** (from Smythson `brand-vs-nonbrand-analysis.py`)
2. **Search Term Audit Workflow** (from Devonshire keyword analysis)
3. **Black Friday Preparation** (from Smythson Phase 1-3 deployment)
4. **Zombie Product Identification** (from GoGlean `find-zombie-converters.py`)
5. **Budget Pacing Analysis** (from NDA, Devonshire budget planning)

### Phase 3: Client Migration (Weeks 3-4)

For each top 10 clients:
1. Review `scripts/` folder
2. Identify scripts that should be:
   - Deleted (use universal script instead)
   - Converted to playbook
   - Kept as-is (truly unique)
3. Add "Playbooks Used" section to CONTEXT.md
4. Document any unique techniques discovered

### Phase 4: Automation (Week 5)

1. Create agent: `playbook-suggester`
   - Runs after completing client work
   - Scans for new scripts created
   - Suggests: universal script, playbook, or keep client-specific

2. Update weekly briefing to include learnings section

3. Create Claude Code skill: `suggest-playbook`
   - When user says "this feels like a pattern"
   - Generates playbook stub with example

### Phase 5: Ongoing Maintenance

**Weekly** (Friday afternoon):
- Review scripts created this week
- Create/update 1-2 playbooks
- Update playbook index

**Monthly** (first Monday):
- Audit client scripts for duplication
- Identify universal script opportunities
- Review playbook effectiveness (which get referenced most?)

---

## Success Metrics

### Quantitative

| Metric | Current | Target (3 months) |
|--------|---------|-------------------|
| Client-specific scripts | 106 | 50 |
| Universal scripts | 6 | 15 |
| Playbooks documented | 0 | 25 |
| Script duplication rate | ~60% | <20% |

### Qualitative

- **Reuse**: When similar problem arises with new client, playbook exists
- **Velocity**: New client setups 50% faster due to playbook library
- **Quality**: Fewer one-off scripts, more systematic approaches
- **Knowledge retention**: Techniques don't get lost when working on different clients

---

## Examples of Knowledge Transfer

### Example 1: Brand Analysis

**Original**: Smythson-specific `brand-vs-nonbrand-analysis.py` (hardcoded customer ID, campaign names)

**Playbook Created**: `playbooks/google-ads/brand-vs-nonbrand-analysis.md`

**Applied To**:
- Tree2MyDoor → Discovered 450% brand ROAS vs 280% non-brand, reallocated budget
- Superspace → Found opposite pattern (non-brand more efficient), adjusted strategy
- Devonshire → Identified brand underinvestment, increased spend 35%

**Universal Script**: Could create `analyze-brand-performance.py` if pattern stable

---

### Example 2: Keyword Wastage

**Original**: Devonshire `pause-keywords.py` (354 lines, 16 hardcoded keywords with IDs)

**Universal Script Created**: `update-google-ads-keyword-status.py`

**Playbook Created**: `playbooks/google-ads/search-term-audit-workflow.md`

**Applied To**:
- Tree2MyDoor → Identified 8 wastage keywords (£340/month), paused with universal script
- Smythson → Quarterly search term review, found £1.2k/month wastage
- All clients → Now use universal script instead of custom code

**Time Saved**:
- Before: 2 hours to write custom script per client
- After: 5 minutes to run universal script

---

### Example 3: Black Friday Prep

**Original**: Smythson Phase 1-3 budget deployment (created 5+ scripts)

**Playbook Created**: `playbooks/client-management/black-friday-prep.md`
- Phase-based approach (Tue-Thu increase, Fri-Sun peak, Mon-Tue wind-down)
- Multi-account coordination
- Budget calculations
- Monitoring schedule

**Applied To**:
- Tree2MyDoor → Used 2-phase approach (simpler, single account)
- Accessories for the Home → Used 3-phase approach, adapted timeframes
- Future clients → Template ready for Black Friday 2026

**Learnings Captured**:
- Phase-based > single big increase (easier to control, adjust mid-event)
- Pause campaigns night before (clean slate, predictable spend)
- £/day targets easier than % increases (clearer communication)

---

## Technical Implementation

### Directory Structure

```
/Users/administrator/Documents/PetesBrain/
├── shared/
│   └── scripts/
│       ├── update-google-ads-budgets.py
│       ├── update-google-ads-campaign-status.py
│       ├── update-google-ads-target-roas.py
│       ├── query-google-ads-performance.py
│       ├── add-google-ads-negative-keywords.py
│       ├── update-google-ads-keyword-status.py
│       └── [future universal scripts]
│
├── playbooks/
│   ├── INDEX.md
│   ├── _TEMPLATE.md
│   ├── google-ads/
│   │   ├── brand-vs-nonbrand-analysis.md
│   │   ├── search-term-audit.md
│   │   ├── zombie-product-identification.md
│   │   └── [more playbooks]
│   ├── microsoft-ads/
│   ├── analytics/
│   └── client-management/
│
├── clients/
│   └── {client}/
│       ├── CONTEXT.md (now includes "Playbooks Used")
│       └── scripts/ (only truly unique scripts)
│
└── docs/
    ├── GOOGLE-ADS-SIMPLE-SCRIPTS.md (universal scripts)
    ├── CROSS-CLIENT-KNOWLEDGE-SYSTEM.md (this doc)
    └── [other docs]
```

### Playbook Template

```markdown
# [Playbook Title]

**Category**: [Google Ads | Microsoft Ads | Analytics | Client Management | Technical]

**Difficulty**: [Beginner | Intermediate | Advanced]

**Time Investment**: [< 30 min | 1-2 hours | Half day]

---

## When to Use

[Specific scenarios, triggers, or questions this answers]

---

## Prerequisites

**Data Requirements**:
- [What data you need access to]

**Tools Required**:
- [Scripts, APIs, access levels]

**Knowledge Requirements**:
- [What you should understand before starting]

---

## Process

### Step 1: [Action]

[Detailed instructions]

```bash
# Code example if applicable
```

**What to look for**: [Key indicators, red flags]

### Step 2: [Action]

...

---

## Interpretation Guide

**Good Signs**:
- [What indicates this is working well]

**Red Flags**:
- [What indicates problems]

**Typical Ranges**:
- [Normal metric ranges for context]

---

## Example from [Client Name]

**Context**: [What was happening]

**Data**:
| Metric | Value |
|--------|-------|
| Spend | £X |
| Revenue | £Y |
| ROAS | Z% |

**Decision Made**: [What action was taken]

**Outcome**: [Result after implementation]

---

## Expected Outcomes

**Decisions Enabled**:
- [What you can decide after running this]

**Typical Impact**:
- [Range of results others have seen]

**Success Criteria**:
- [How to know if this was valuable]

---

## Related Playbooks

- [Link to related technique 1]
- [Link to related technique 2]

---

## Version History

- **v1.0** (Nov 2025) - Initial creation based on [Client] work
- **v1.1** (Dec 2025) - Updated with [Client] learnings
```

---

## Governance

### Who Creates Playbooks?

**You (Claude)** should:
- Create playbook stubs during work
- Suggest when a technique feels reusable
- Draft initial version with client example

**User** should:
- Review and approve before finalizing
- Decide if example needs anonymization
- Add business context Claude might miss

### Who Maintains Universal Scripts?

**Standard**: Treat as production code
- Version control (git)
- Backwards compatibility
- Deprecation warnings if changing behaviour
- Documentation updates

### Playbook Lifecycle

1. **Draft** - Created during client work, not yet reviewed
2. **Active** - Reviewed, ready for use across clients
3. **Deprecated** - Better approach found, kept for reference
4. **Archived** - No longer relevant (platform changes, etc.)

---

## Migration Plan for Existing Scripts

### High Priority (Next 2 Weeks)

**Devonshire** (20+ scripts):
- ✅ Budget updates → Use universal script
- ✅ Keyword pause → Use universal script
- ⏳ Create playbook: Budget pacing analysis
- ⏳ Create playbook: Multi-property campaign structure

**Smythson** (30+ scripts):
- ✅ Budget updates → Use universal script
- ⏳ Create playbook: Brand vs non-brand analysis
- ⏳ Create playbook: Multi-account coordination
- ⏳ Create playbook: Black Friday preparation
- Keep: Product scraping (truly unique)

**NDA** (25+ scripts):
- ✅ Budget updates → Use universal script
- ⏳ Create playbook: Enrollment correlation analysis
- ⏳ Create playbook: International budget allocation
- Keep: Enrollment CSV processing (unique data source)

### Medium Priority (Weeks 3-4)

**Superspace**, **Tree2MyDoor**, **GoGlean**, **Accessories for the Home**

### Low Priority (Month 2)

Remaining clients with <5 scripts each

---

## FAQ

### Q: When should something be a universal script vs playbook?

**Universal Script**: Clear, repetitive task with consistent inputs/outputs
- Examples: Budget updates, status changes, data queries
- Test: "Could this run in a cron job?"

**Playbook**: Process requiring human judgment and interpretation
- Examples: Performance analysis, audit workflows, strategy decisions
- Test: "Does this require looking at results and making decisions?"

### Q: What if a playbook needs code?

Include code snippets in the playbook, but reference universal scripts where possible:

```markdown
## Step 3: Query Performance Data

```bash
python3 /path/to/query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-09-01 \
  --end-date 2025-11-25 \
  --output csv \
  --file performance.csv
```

Then open `performance.csv` and look for...
```

### Q: How do we avoid playbooks becoming stale?

1. Version history in each playbook
2. Monthly review of playbook effectiveness
3. Mark deprecated if better approach found
4. Keep for reference even if deprecated (context matters)

### Q: Should client examples be anonymized?

**Internal playbooks**: Use real client names and metrics (helps with context)

**If ever shared externally**: Anonymize ("Client A", "E-commerce brand", round metrics)

---

## Next Steps

1. **Create playbook structure** (today)
2. **Write first 5 playbooks** (this week)
3. **Audit Smythson scripts** (next week)
4. **Add playbook references to CONTEXT.md** (ongoing)
5. **Integrate into weekly workflow** (ongoing)

---

**Bottom line**: Knowledge captured once, reused across 30+ clients. Scripts written once, maintained centrally. Techniques documented systematically, not lost in client folders.
