# Analysis Folder

## Purpose

This folder contains documented investigations and analyses performed on the Uno Lighting account. These are NOT changes made to the account (those go in the experiment log), but rather audit trails of analytical work.

## What Goes Here

**✅ Include:**
- Performance investigations (why did X happen?)
- Data quality checks (conversion lag analysis, attribution checks)
- Opportunity assessments (should we do X? Analysis says...)
- Root cause analyses (revenue dropped - why?)
- Strategic decision documentation (decided NOT to do X because...)
- Methodology findings (discovered account behaves like Y)

**❌ Don't Include:**
- Actual account changes (those go in rok-experiments-client-notes.csv)
- Client emails (those go in emails/)
- Meeting notes (those go in meeting-notes/)
- Strategy documents (those go in documents/)
- Reports (those go in reports/)

## File Naming

Format: `YYYY-MM-DD-brief-description.md`

Examples:
- `2025-11-13-conversion-lag-investigation.md`
- `2025-11-15-impression-share-decline-root-cause.md`
- `2025-11-20-black-friday-budget-opportunity-assessment.md`

## When to Create Analysis Documents

**Create when:**
1. You perform a non-trivial investigation (>15 mins analysis)
2. The findings inform a strategic decision
3. The methodology/learnings would be valuable to reference later
4. You discover something unexpected about account behavior
5. You need to document why you did/didn't take an action

**Don't create for:**
- Routine checks (quick glance at yesterday's performance)
- Simple questions answered in seconds
- Standard reporting (monthly reports go in reports/)

## Structure

Each analysis document should include:
1. **Trigger**: What prompted this analysis?
2. **Question**: What were we trying to answer?
3. **Data/Method**: What did we look at and how?
4. **Findings**: What did we discover?
5. **Conclusion**: What does this mean?
6. **Actions Taken**: What decisions/changes resulted?

## Integration with Other Systems

- **CONTEXT.md**: Strategic learnings from analysis get added to CONTEXT.md
- **Experiment Log**: If analysis leads to account change, log the change (not the analysis)
- **Tasks**: If analysis identifies work needed, create task in Google Tasks
- **Reports**: If analysis becomes client-facing, move to reports/

Think of this folder as your **analytical audit trail** - it shows the work you did to understand the account and make informed decisions.
