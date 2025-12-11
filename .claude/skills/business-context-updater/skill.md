---
name: business-context-updater
description: Update business context files dynamically with metrics, strategic priorities, and new insights. Use when user says "update business context", "add to business context", "update metrics", or needs to record strategic changes. Use this to keep business context fresh and decision-ready.
allowed-tools: Read, Write, Bash, Glob
---

# Business Context Updater Skill

---

## Core Workflow

When this skill is triggered, present three update modes and guide the user through their choice.

### Mode 1: Metrics Update
**When to use**: Update quantitative business data (client count, MRR, capacity, current quarter priorities)

**Fields to update** (from `context/business/business-overview.md`):
- Active Clients: [number]
- Monthly Recurring Revenue: £[range]/month
- Client Capacity: [number] clients
- Current Quarter Priorities: [list 3-5 priorities]
- Last updated: [date]

**Workflow**:
1. Read current `context/business/business-overview.md` (Business Metrics section, lines 42-56)
2. Display current values:
   ```
   Current State:
   • Active Clients: 12
   • Monthly Recurring Revenue: £12K-£18K/month
   • Client Capacity: 20 clients
   ```
3. Prompt for updates: "Which fields need updating? (leave blank to keep current)"
4. Validate before saving:
   - Client count must match actual `clients/` folder count
   - MRR should be reasonable based on pricing model (£1-2.5K/month per client)
   - Show diff: "You're changing 12 → [X] clients"
5. Update file with new values
6. Add entry to Document History table at bottom of file
7. Commit changes to git with clear message

**Document History Format**:
```markdown
### Document History

| Date | Change | Updated By |
|------|--------|-----------|
| 2025-12-11 | Updated client count 12→15, MRR £12-18K→£15-22K | Claude Code |
| 2025-12-10 | Added Q4 2025 priorities | Claude Code |
```

---

### Mode 2: Strategic Update
**When to use**: Update goals, strategic focus, quarterly priorities, or change existing strategic content

**Files you can update**:
- `business-overview.md` - Strategic Priorities section (lines 59-78)
- `personal-profile.md` - Current Focus section (lines 151-164)
- `business-philosophy.md` - Operating principles, decision framework
- `key-relationships.md` - Customer segments, partnerships
- `market-position.md` - Market opportunities, competitive landscape

**Workflow**:
1. Ask user which file/section to update
2. Read the relevant section
3. Display current content
4. Prompt: "What should this section say instead?" (allow multi-line input)
5. Show diff before confirming
6. Update file
7. Add entry to Document History
8. Commit to git

**Example**:
```
Current Q4 2025 Strategic Priorities:
• Scale client base to 15-20 clients via automation
• Develop proprietary tool suite
• Expand knowledge base to 2,000 articles

New priorities:
• [User enters new priorities]
```

---

### Mode 3: Context Addition
**When to use**: Add new sections, lessons learned, market insights, or strategic decisions to any file

**How it works**:
1. Ask which file to add to: "Which business context file?"
2. Ask what section: "New section title?" (e.g., "Q4 2025 Learnings", "New Competitive Threat", "Product Launch")
3. Ask for content: "What should this section include?"
4. Show preview before confirming
5. Add section to appropriate file (usually at end, before Document History)
6. Update Document History
7. Commit to git

**Example output**:
```markdown
### Q4 2025 Learnings

- Automation without team: Solo operation scales to 20 clients with 50+ LaunchAgents
- Client retention: Direct owner access + weekly reports → 100% retention
- Knowledge base as moat: 1,983 articles enables rapid client insights
```

---

## Implementation Details

### File Structure

**business-overview.md** sections to update:
- Business Metrics (lines 42-56)
- Strategic Priorities (lines 59-78)
- Operations (lines 81-101)

**personal-profile.md** sections to update:
- Current Focus (lines 151-164)

**business-philosophy.md** sections to update:
- Core values
- Operating principles

**key-relationships.md** sections to update:
- Customer segments
- Strategic partners

**market-position.md** sections to update:
- Market opportunities
- Risks and mitigation

### Validation Rules

**Metrics Mode**:
- Client count: Must match `clients/` folder count ±1
- MRR: Should be within £8K-£30K range (allow exceptions with confirmation)
- Capacity: Should be ≥ current client count
- Dates: Must be valid (use `date` command to verify)

**Strategic Mode**:
- No validation needed, content is qualitative
- Just preserve formatting and structure

**Addition Mode**:
- Ensure new section title is unique in file
- Place before Document History section
- Maintain markdown heading hierarchy

### Document History

Every file must have a Document History table at the bottom:

```markdown
### Document History

| Date | Change | Updated By |
|------|--------|-----------|
| 2025-12-11 | [Summary of change] | Claude Code |
| 2025-12-10 | [Previous change] | Claude Code |
```

Add new entries at the top of the table (most recent first).

---

## User Interaction Flow

```
User: "Update business context"
↓
Skill: "Which update mode?
1. Metrics (client count, MRR, capacity)
2. Strategic (goals, focus, priorities)
3. Add new context (new sections, learnings)"

User: "Metrics"
↓
Skill: "Current state:
• Active Clients: 12
• MRR: £12K-£18K/month
• Capacity: 20 clients

What's changed?"

User: "12→15 clients, MRR now £15-22K"
↓
Skill: "Validating...
✓ Client count: 15 matches folder count (15 client folders found)
✓ MRR: £15-22K is reasonable for 15 clients
✓ Ready to save?

Confirm: Y/N"

User: "Y"
↓
Skill: ✅ Updated context/business/business-overview.md
     ✅ Added Document History entry
     ✅ Committed to git

Done! Your business context is now updated.
Date: 2025-12-11
File: context/business/business-overview.md
Changes:
- Active Clients: 12 → 15
- Monthly Recurring Revenue: £12K-£18K → £15-22K
```

---

## Quality Checks

Before saving, verify:
- [ ] File exists and is readable
- [ ] Markdown structure preserved (no broken headers)
- [ ] Date is current and correct format
- [ ] Document History entry is clear and concise
- [ ] Git commit message is descriptive
- [ ] No unintended changes to other sections

---

## Git Integration

After each update:
1. Add the modified file to staging: `git add context/business/[file]`
2. Commit with descriptive message:
   ```
   git commit -m "Update business context: [summary of changes]"
   ```
3. Example messages:
   - "Update business context: 12→15 active clients, Q4 metrics refresh"
   - "Add Q4 2025 strategic learnings to business-philosophy.md"
   - "Update market position: Add AI adoption trend analysis"

---

## Error Handling

**File not found**:
- Confirm file location with user
- Check if file is in `context/business/`

**Validation failed**:
- Show what failed and why
- Offer to override with confirmation
- Log reason for override

**Git commit failed**:
- Check git status
- Offer to save without committing (then manual commit later)
- Show git error message

---

## Success Criteria

A successful update should:
1. ✅ Display current values clearly
2. ✅ Accept user input without errors
3. ✅ Validate data where applicable
4. ✅ Show diff before confirming
5. ✅ Preserve markdown formatting
6. ✅ Add Document History entry
7. ✅ Commit to git with clear message
8. ✅ Confirm completion to user

---

## Integration with Other Components

**Works with**:
- `context/business/` files (all 6 markdown files)
- `clients/*/CONTEXT.md` (for client count validation)
- Git repository (for change tracking)
- Document History tables (for audit trail)

**Feeds into**:
- business-context-sync agent (reads updated values)
- CLAUDE.md automatic reference (uses latest context)
- Client decision-making (references current business state)

---

## Tips & Tricks

**Quick metrics update** (under 2 minutes):
1. Choose Metrics mode
2. Update only changed fields
3. Confirm and done

**Batch strategic updates**:
1. Multiple strategic changes? Do them separately
2. Each update gets its own Document History entry
3. Better audit trail and git history

**Adding learnings**:
- Do this regularly (monthly or quarterly)
- Add to business-philosophy.md or market-position.md
- Capture patterns you're noticing
- Helps future decision-making

**Validation tips**:
- Run sync agent right after to verify metrics
- Check actual client folders: `ls clients/ | grep -v _template | wc -l`
- Validate MRR: client count × average retainer = approximate MRR

---

## Limitations

This skill:
- **Updates markdown files directly** (not a database)
- **Requires manual content input** (not auto-calculated except for counts)
- **Preserves formatting** (structured markdown only)
- **Commits to git** (requires git repo to be clean)
- **Doesn't sync with Google Sheets** (one-way write to markdown)

For auto-calculation of metrics, see `business-context-sync` agent.

---

## Example Scenarios

### Scenario 1: Quarterly Metrics Refresh

```
User: "Update Q4 business metrics"
Skill: Shows current Q4 values
User: Provides updated client count (14 instead of 12)
User: Updates MRR (£14-20K instead of £12-18K)
Result: metrics updated, Document History recorded, git committed
```

### Scenario 2: New Strategic Learning

```
User: "I want to add a new learning about client retention"
Skill: "Which file? (business-philosophy, market-position, etc.)"
User: "business-philosophy"
Skill: "Section title?"
User: "Client Retention Strategy"
Skill: "Content?"
User: "[Multi-line content about retention approach]"
Result: New section added, Document History updated, committed
```

### Scenario 3: Quarterly Priorities Update

```
User: "Update our Q1 2026 priorities"
Skill: "Showing current Q4 priorities..."
User: "These are outdated, here's what we're focusing on in Q1..."
Result: Strategic Priorities section updated, history recorded
```

---

## Testing

Test all three modes:
1. **Metrics**: Update client count, verify validation
2. **Strategic**: Update a goal, verify formatting
3. **Addition**: Add new section, verify placement and history

Verify:
- Document History entries appear correctly
- Git commits have descriptive messages
- Markdown structure is preserved
- All files are readable after update
