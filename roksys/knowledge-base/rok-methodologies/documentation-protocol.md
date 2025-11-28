---
title: Documentation Protocol - Claude Code Work Sessions
category: ROK Methodologies
date_added: 2025-11-03
tags: [documentation, workflow, best-practices, claude-code]
---

## Overview

Standard protocol for ensuring all work completed in Claude Code sessions is properly documented and saved for future reference.

## Core Principle

**Nothing gets lost.** Every system built, every automation configured, every insight discovered must be documented in the appropriate location before moving on.

## User Triggers - Save Progress Mid-Project

When the user says any of these phrases, **immediately create documentation**:

### Simple Triggers
- "Save this"
- "Document this"
- "Make sure this is saved"
- "Write this down somewhere"
- "Don't lose this work"
- "Create documentation for what we just did"

### Checkpoint Triggers
- "We should save our progress here"
- "Let's document this before moving on"
- "Can you save what we've built so far?"
- "Make sure this process is all saved"

## User Triggers - Complete Documentation

When the user says these phrases, **create comprehensive end-of-project documentation**:

- "Document everything we did today"
- "Save all of this work"
- "Create complete documentation"
- "Write up everything we built"
- "Make sure nothing is lost"

## Proactive Documentation Offers

Claude Code should **automatically offer to document** when:

1. ✅ **Complete system is working** - Tested and deployed successfully
2. ✅ **Multi-step implementation finished** - All stages complete
3. ✅ **LaunchAgents configured** - Automation scheduled and loaded
4. ✅ **New scripts or tools created** - Working and tested
5. ✅ **Major system changes** - Significant updates to existing infrastructure

**Standard offer**: *"This is complete and working. Should I create documentation before we move on?"*

## What to Document

### System Documentation (`/docs/`)
When a new system, tool, or automation is built:

**Required sections**:
- **Overview** - What it does, status (active/prototype/planned)
- **How It Works** - Technical architecture and flow
- **Files** - Scripts, data files, configuration, LaunchAgents
- **Running Manually** - Command examples with full paths
- **Monitoring** - How to check status, view logs, verify operation
- **Troubleshooting** - Common issues and solutions
- **Test Results** - Actual data from deployment testing
- **Implementation History** - Deployment date, what was built

**File naming**:
- `SYSTEM-NAME-COMPLETE.md` - For finished implementations
- `SYSTEM-NAME.md` - For reference documentation
- `TOOL-NAME-GUIDE.md` - For user-facing guides

### Client Context (`/clients/[client]/CONTEXT.md`)

When client-specific insights, strategies, or decisions are discussed:

**What to capture**:
- Strategic decisions or direction changes
- New goals, KPIs, or targets
- Client preferences or sensitivities
- Business changes (products, pricing, stock, website)
- Technical issues or tracking problems
- Performance patterns or anomalies
- Successful or failed experiments
- Important dates or upcoming events
- Client concerns or feedback
- Competitive intelligence

**How to update**:
- Use Edit tool to add to appropriate section
- Keep existing info - only add, don't remove
- Include dates for time-sensitive information
- Cross-reference sources (e.g., "Per Oct 27 email...")
- Update "Last Updated" date
- Add entry to "Document History" table

### Tool Architecture (`/tools/[tool]/TOOL_CLAUDE.md`)

When building or modifying tools:

**Document**:
- Architecture decisions and patterns
- Dependencies and requirements
- API integrations
- Data flows
- Configuration options
- Known limitations
- Future enhancement ideas

### Summary Files

For major projects or multi-part implementations:

**Create overview document** (e.g., `PERFORMANCE-MONITORING-COMPLETE.md`):
- List all components built
- Show how they work together
- Include all file locations
- Provide complete command reference
- Document success criteria met
- Link to detailed docs for each component

## Documentation Locations

### Project Structure
```
/docs/                          # System-level documentation
  ├── SYSTEM-NAME.md           # Individual system docs
  ├── AUTOMATION.md            # Automation workflow reference
  └── TROUBLESHOOTING.md       # Cross-system troubleshooting

/clients/[client]/
  └── CONTEXT.md               # Client knowledge base (CRITICAL)

/tools/[tool]/
  ├── TOOL_CLAUDE.md           # Architecture for Claude Code
  ├── README.md                # User-facing guide
  └── QUICKSTART.md            # Setup instructions

/roksys/knowledge-base/
  └── rok-methodologies/       # ROK internal processes
```

## Quality Standards

### Every Documentation File Must Include:

1. **Clear purpose** - What problem does this solve?
2. **Status indicator** - Active/Prototype/Planned
3. **File locations** - Exact paths to all relevant files
4. **Commands** - Copy-paste ready with full paths and env vars
5. **Test results** - Proof it works with actual data
6. **Deployment date** - When was this implemented?
7. **Monitoring** - How to verify it's running
8. **Troubleshooting** - What to check when it breaks

### CONTEXT.md Updates Must Include:

1. **Timestamp** - When was this added?
2. **Source** - Where did this info come from? (email, meeting, analysis)
3. **Context** - Why is this important?
4. **Action items** - What needs to happen because of this?
5. **Updated metadata** - "Last Updated" date and Document History entry

## Anti-Patterns to Avoid

❌ **Don't**:
- Create code without documentation
- Assume the user will remember how something works
- Skip documentation because "it's simple"
- Document in chat only (user can't search conversations easily)
- Create files without explaining what was saved and where

✅ **Do**:
- Document while building, not after
- Ask "Should I document this?" when unsure
- Create comprehensive reference docs for complex systems
- Confirm what was saved and where
- Update CONTEXT.md files whenever client insights emerge

## Example Session Flow

### Good Session
```
User: "Build a daily alert system for performance anomalies"
Claude: [builds system, tests it]
Claude: "This is complete and working. Should I create documentation?"
User: "Yes"
Claude: [creates comprehensive docs in /docs/, confirms locations]
```

### Better Session (Proactive)
```
User: "Build a daily alert system for performance anomalies"
Claude: [builds system, tests it]
Claude: "✅ System complete and tested. Creating documentation now..."
Claude: [creates docs, confirms what was saved]
User: [doesn't have to remember to ask]
```

## Special Case: Client CONTEXT.md

The client CONTEXT.md file is the **institutional memory** for each account. Treat it as sacred.

**When to update**:
- After processing client emails (if strategic info)
- After reviewing meeting notes (ALWAYS - meetings are high-value)
- After client communications reveal new information
- After discovering insights during analysis
- When campaign structure or strategy changes

**Never skip this step** - client context is often more valuable than the technical implementation itself.

## Verification Checklist

Before ending a session where significant work was done, verify:

- [ ] System documentation created in `/docs/`
- [ ] Client insights added to relevant `CONTEXT.md` files
- [ ] Tool architecture documented in `TOOL_CLAUDE.md` (if applicable)
- [ ] File locations explicitly stated
- [ ] Commands tested and included
- [ ] LaunchAgent configs documented
- [ ] Troubleshooting section included
- [ ] Test results recorded
- [ ] User confirmed what was saved

## Why This Matters

**Without documentation**:
- Work gets lost between sessions
- User has to remember how things work
- Troubleshooting takes longer
- Systems can't be maintained
- Knowledge isn't transferable

**With documentation**:
- ✅ Work persists across sessions
- ✅ User can reference and verify independently
- ✅ Systems are maintainable
- ✅ Knowledge compounds over time
- ✅ Nothing is ever lost

## This Is ROK Strategy

Documentation is not optional. It's part of the work, not something that comes after. Every insight, every system, every decision must be captured in the right place at the right time.

**The goal**: Peter should never have to say "I thought that was saved" or "where did we put that?"
