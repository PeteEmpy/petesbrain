# Data Storytelling Report Agent

**Version:** 1.0
**Created:** 2025-11-19
**Status:** Active
**Model:** Sonnet (via Anthropic API)

---

## Purpose

Transform raw performance data into compelling narratives that highlight key insights and drive understanding. Based on expert frameworks from Nancy Duarte, Cole Nussbaumer Knaflic, and Edward Tufte.

## What It Does

Takes Google Ads performance data (ROAS, spend, conversions, etc.) and generates:
- Client-ready reports with narrative structure
- Performance anomaly explanations with context
- Budget recommendation emails with clear reasoning
- Monthly/quarterly reviews with data-driven stories
- Crisis communications with beginning-middle-end structure

## How It Works

**5-Phase Workflow:**

1. **Understand Context & Audience** - Determine who cares, what they care about, and detail level needed
2. **Ingest & Scan Data** - Find trends, anomalies, comparisons, correlations in performance metrics
3. **Identify Key Insight** - Create "Data Point of View" (what happened + why it matters + stakes)
4. **Gather Supporting Details** - Add time context, benchmarks, breakdowns, possible causes
5. **Structure Narrative** - Three-act structure (Setup → Conflict/Insight → Resolution)

## Usage

```bash
# Manual invocation
python3 agents/datastory-report/datastory-report.py \
  --client smythson \
  --data-file clients/smythson/reports/november-performance.json \
  --audience client \
  --goal diagnose_problem

# With specific output format
python3 agents/datastory-report/datastory-report.py \
  --client superspace \
  --data clients/superspace/data/q4-performance.csv \
  --audience executive \
  --goal track_progress \
  --output-format html
```

## Input Data Format

Accepts JSON or CSV with performance metrics:

```json
{
  "client": "smythson",
  "period": "2024-10-01 to 2024-10-31",
  "metrics": {
    "roas_previous": 385,
    "roas_current": 432,
    "spend_previous": 26350,
    "spend_current": 26350,
    "conversions_previous": 101,
    "conversions_current": 114,
    "revenue_previous": 101448,
    "revenue_current": 113832
  },
  "context": {
    "recent_changes": ["Feed optimization implemented Oct 1"],
    "seasonality": "Pre-holiday period",
    "client_goals": ["Maintain ROAS above 400%", "Prepare for Q1 2025"]
  }
}
```

## Output Format

**HTML Report** (default for client communications):
- Roksys branding (green header, logo)
- Three-act narrative structure
- Data visualizations embedded
- Clear sections: Context → Insight → Resolution

**Markdown** (for internal documentation):
- Clean markdown format
- Suitable for saving to client documents folder
- Can be converted to email or PDF later

**Email Draft** (for direct client communication):
- HTML email format
- Verdana 13px typography
- Concise narrative (300-600 words)
- Clear call-to-action

## Example Transformation

**Before (Data Dump):**
> "Smythson October: ROAS increased from 385% to 432% (+12%). Spend stable at £26,350. Conversions up from 101 to 114 (+13%). Revenue increased from £101,448 to £113,832 (+12%)."

**After (Data Story):**
> **The Breakthrough**
>
> For six months, Smythson's luxury goods campaigns held steady around 385% ROAS—solid performance, but plateaued. Then October 2024 brought a turning point: ROAS climbed to 432%, a 12% breakthrough that shifted the trajectory.
>
> **What Changed?**
>
> The catalyst was your feed optimization on October 1st. By surfacing bestsellers and refining product titles weekly, we gave Google's algorithm exactly what it needed to find higher-intent buyers. Spend remained at £26,350 (discipline maintained), but conversions jumped from 101 to 114—pure efficiency gain, not just volume.
>
> **What This Means**
>
> This pattern reveals a clear path: feed quality drives ROAS more than budget increases. At your current spend level, every 10% ROAS improvement means £2,635 additional monthly profit. The next move: replicate this feed quality methodology across your Spring 2025 collection launch.
>
> **Recommended Action:** Continue weekly feed audits. Monitor ROAS daily for 3 weeks to confirm sustainability. If ROAS holds above 420%, consider 15% budget increase for Q1.

## Audience Types

**Client** (default):
- Focus on business outcomes
- Explain technical terms
- Emphasise ROI and profit
- Action-oriented recommendations

**Technical**:
- Include implementation details
- Reference Google Ads settings
- Explain algorithmic behaviour
- More granular breakdowns

**Executive**:
- High-level summary only
- Focus on strategic implications
- Business metrics over technical metrics
- Clear ROI statements

## Goal Types

**diagnose_problem**:
- Find root causes of performance changes
- Analyse multiple potential factors
- Recommend corrective actions
- Focus on "what went wrong and why"

**track_progress**:
- Compare to previous periods
- Assess against goals/targets
- Highlight wins and improvements
- Focus on "are we on track"

**find_opportunities**:
- Identify growth potential
- Spot underutilised channels
- Recommend optimisations
- Focus on "where should we invest"

## Dependencies

- Python 3.9+
- anthropic>=0.18.0 (for Claude API)
- pandas (for data processing)
- json, csv (built-in)

## Configuration

Environment variables:
- `ANTHROPIC_API_KEY` - Required for narrative generation

## Output Location

Reports saved to:
- HTML: `clients/{client}/reports/datastory-YYYY-MM-DD-{topic}.html`
- Markdown: `clients/{client}/documents/datastory-YYYY-MM-DD-{topic}.md`
- Email: `clients/{client}/documents/email-draft-YYYY-MM-DD-{topic}.html`

## Expert Frameworks

**Nancy Duarte (DataStory):**
- Find the human angle in data
- Frame insights as narratives with heroes and adversaries
- Create a "Data Point of View" (one-sentence story)

**Cole Nussbaumer Knaflic (Storytelling with Data):**
- Understand audience and context first
- Focus on a clear message
- Choose right chart for the data
- Eliminate clutter for clarity

**Edward Tufte (Visual Display):**
- "Complex ideas communicated with clarity, precision, efficiency"
- Maximize data-ink ratio
- Minimize chartjunk
- Maintain graphical integrity

## When to Use

Use this agent when you need to:
- ✅ Create monthly client reports (narrative instead of data dump)
- ✅ Explain performance anomalies (drops or spikes)
- ✅ Recommend budget changes (with compelling reasoning)
- ✅ Present quarterly reviews (comprehensive storytelling)
- ✅ Handle crisis communications (context → problem → resolution)
- ✅ Generate client emails about performance (engaging and clear)

Don't use when:
- ❌ Raw data export needed (use GAQL directly)
- ❌ Internal quick checks (too formal for quick analysis)
- ❌ Real-time monitoring (designed for retrospective analysis)

## Success Criteria

A successful data story:
- Main insight is crystal clear
- Context makes the insight meaningful
- Recommendations are actionable
- Tone is engaging yet professional
- Story has clear beginning, middle, end
- Numbers are accurate and substantiated
- Audience can make a decision based on the narrative

## Testing

Test with real client data:
```bash
# Test with Smythson October data
python3 agents/datastory-report/datastory-report.py \
  --test-mode \
  --client smythson \
  --data tests/fixtures/smythson-october-2024.json

# Expected output: HTML report with narrative structure
# Verify: Clear story arc, accurate metrics, actionable recommendations
```

## Maintenance

- Update narrative templates as client preferences evolve
- Add new audience types as needed
- Refine "Data Point of View" generation based on feedback
- Build library of successful story patterns per client

## Related Documentation

- Phase 6 Analysis: `.claude/skills/csv-analyzer/phase-6-analysis.md`
- Mike Rhodes Datastory Agent: `/Users/administrator/Documents/brain/.claude/agents/datastory.md`
- Client Reporting Standards: `docs/CLIENT-REPORTING-STANDARDS.md` (if exists)

---

**Last Updated:** 2025-11-19
**Maintainer:** Peter Empson / Claude Code
**Priority:** High (Priority 1 implementation from Phase 6)
