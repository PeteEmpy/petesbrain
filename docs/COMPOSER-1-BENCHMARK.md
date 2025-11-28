# Composer 1 Performance Benchmark

**Purpose**: Test Composer 1's speed and accuracy on Pete's Brain daily workflows

**Date Created**: 2025-11-07
**Model Being Tested**: Composer 1 (in Claude Code agent mode)
**Baseline Comparison**: Sonnet 4.5

---

## Test Categories

### Category 1: Simple File Operations (Should be VERY fast)

**Expected Time with Composer 1**: <10 seconds each

#### Test 1.1: Read Client CONTEXT
```
Task: "Read Smythson CONTEXT.md and summarize the current strategic priorities"
Measures: File read speed, context extraction
```

#### Test 1.2: Quick CONTEXT Update
```
Task: "Add to Smythson context - Ad Hoc Notes: Benchmark test completed [timestamp]"
Measures: Single-file edit speed
```

#### Test 1.3: Read Experiment Notes
```
Task: "Show me all Smythson experiments from the last 30 days"
Measures: CSV read, filtering, presentation
```

---

### Category 2: Multi-File Operations (Should be notably faster)

**Expected Time with Composer 1**: <30 seconds each

#### Test 2.1: Client Folder Discovery
```
Task: "List all files in the Devonshire Hotels client folder, organized by type"
Measures: Directory traversal, file organization
```

#### Test 2.2: Recent Email Review
```
Task: "Find and summarize the 3 most recent emails for National Design Academy"
Measures: Multi-file read, date sorting, summarization
```

#### Test 2.3: Meeting Notes Search
```
Task: "Find all meeting notes mentioning 'budget' across all clients in the last 60 days"
Measures: Multi-file grep, cross-client search
```

---

### Category 3: Data Processing (Fast but watch accuracy)

**Expected Time with Composer 1**: <45 seconds each

#### Test 3.1: Experiment Logging (with mandatory questions)
```
Task: "Log this experiment: Tree2MyDoor, paused 3 underperforming ad groups to improve efficiency"

CRITICAL: Composer 1 MUST ask the 5 mandatory questions before logging:
- What was driving this change?
- What are you expecting to see?
- When should we check back?
- What would make this a win?
- Any other context?

Pass/Fail: Did it ask ALL 5 questions? ✅/❌
```

#### Test 3.2: Knowledge Base Inbox Processing
```
Setup: Drop a test markdown file in roksys/knowledge-base/_inbox/documents/
Task: "Process the knowledge base inbox"

Measures:
- File read
- Category determination
- Markdown formatting
- File move
- Index update
```

#### Test 3.3: Tasks Completed Review
```
Task: "Show me all completed tasks for Smythson in the last 30 days, include task notes"
Measures: File read, filtering, note extraction
```

---

### Category 4: Simple Analysis (Watch for quality degradation)

**Expected Time with Composer 1**: <60 seconds each

#### Test 4.1: Single-Source Analysis
```
Task: "Based on Smythson CONTEXT.md only, what are the top 3 priorities right now?"
Measures: Single-file reasoning, prioritization
```

#### Test 4.2: Email Draft Generation
```
Task: "Draft a quick update email for Uno Lighting about their Q4 performance"
Measures:
- CONTEXT.md read
- HTML email generation
- British English spelling
- ROAS as percentage format
```

#### Test 4.3: Recent Activity Summary
```
Task: "Summarize all Smythson activity (emails, meetings, tasks) from the last 7 days"
Measures: Multi-file read, chronological sorting, summarization
```

---

### Category 5: Complex Multi-Source Analysis (May need Sonnet 4.5)

**Expected Time with Composer 1**: Unknown - may struggle or skip steps

#### Test 5.1: Performance Investigation
```
Task: "Analyze Tree2MyDoor's performance changes in October. Check:
- CONTEXT.md
- Experiment notes (rok-experiments-client-notes.csv)
- Tasks completed (tasks-completed.md + notes)
- Recent emails
- Meeting notes
Provide root cause analysis with evidence from all sources"

Watch for:
- Does it check ALL sources?
- Does it cite evidence properly?
- Does it avoid speculation without evidence?
- Does it read task NOTES (not just titles)?
```

#### Test 5.2: Strategic Recommendation with KB
```
Task: "Should Devonshire Hotels increase Performance Max budgets in November?
Check:
- Client CONTEXT.md (goals, preferences, history)
- Knowledge Base (roksys/knowledge-base/google-ads/performance-max/)
- Recent experiments (rok-experiments-client-notes.csv)
- Completed tasks and notes (tasks-completed.md)
Provide recommendation with KB citations"

Watch for:
- Does it check Knowledge Base?
- Does it properly cite KB sources?
- Does it integrate client context?
- Does it reference completed tasks AND their notes?
```

#### Test 5.3: Client Onboarding Prep
```
Task: "I have a new client meeting for 'Positive Bakes'. Create:
1. clients/positive-bakes/CONTEXT.md (from template)
2. clients/positive-bakes/README.md (basic structure)
3. Standard folder structure (emails/, meeting-notes/, documents/, etc.)
4. Add entry to roksys/spreadsheets/rok-experiments-client-list.csv"

Measures:
- Multi-file creation
- Template usage
- Folder structure adherence
- CSV update
```

---

## Category 6: Automation Script Tasks (Good test of code understanding)

**Expected Time with Composer 1**: <45 seconds each

#### Test 6.1: LaunchAgent Status Check
```
Task: "Check if all petesbrain LaunchAgents are running. Show status and recent log entries."
Measures: Bash commands, log file reading
```

#### Test 6.2: Script Modification
```
Task: "In shared/scripts/knowledge-base-processor.py, change the relevance threshold from 6 to 7"
Measures: Code comprehension, precise edit
```

#### Test 6.3: MCP Server Verification
```
Task: "Check .mcp.json and verify all paths are absolute and credentials exist"
Measures: JSON parsing, file path validation
```

---

## Scoring System

For each test, record:

| Test | Time (seconds) | Quality (1-5) | Issues | Pass/Fail |
|------|---------------|---------------|--------|-----------|
| 1.1  |               |               |        | ✅/❌      |
| 1.2  |               |               |        | ✅/❌      |
| ...  |               |               |        | ✅/❌      |

**Quality Scale**:
- 5 = Perfect, no issues
- 4 = Minor formatting issues
- 3 = Missing some details but correct approach
- 2 = Significant gaps or errors
- 1 = Completely wrong or unusable

**Pass Criteria**:
- Categories 1-3: Must pass ALL tests (speed is key)
- Category 4: Must pass 2/3 tests (quality matters)
- Category 5: Passing 1/3 is acceptable (these are complex)
- Category 6: Must pass 2/3 tests (automation is critical)

---

## When to Switch Back to Sonnet 4.5

Switch if Composer 1:
- ❌ Skips mandatory experiment logging questions (Test 3.1)
- ❌ Fails to check multiple sources in performance analysis (Test 5.1)
- ❌ Doesn't cite Knowledge Base sources (Test 5.2)
- ❌ Misses task notes when reviewing completed work (Test 4.3, 5.1)
- ❌ Quality scores consistently <3 in Category 4-5

---

## Recommended Daily Model Usage (After Testing)

Based on benchmark results, use:

**Composer 1** for:
- ✅ Quick CONTEXT.md updates
- ✅ Experiment logging (if passes Test 3.1)
- ✅ Email drafts (single-source)
- ✅ File operations and searches
- ✅ Script modifications
- ✅ KB inbox processing

**Sonnet 4.5** for:
- ✅ Complex performance investigations (multi-source)
- ✅ Strategic recommendations requiring KB consultation
- ✅ Client onboarding and major setup
- ✅ Root cause analysis with evidence synthesis
- ✅ Anything requiring task note review

**Opus/GPT-5** for:
- ✅ Novel system design
- ✅ High-stakes client deliverables
- ✅ Complex architectural decisions

---

## Results Log

**Test Date**: _____________

**Overall Findings**:
- Speed improvement over Sonnet 4.5: ____%
- Quality maintenance: _____ (Excellent/Good/Fair/Poor)
- Recommended for daily use: _____ (Yes/No/Conditional)

**Specific Strengths**:
-

**Specific Weaknesses**:
-

**Final Recommendation**:
-

---

## Next Steps

After completing benchmark:
1. Update `.claude/settings.json` with model selection strategy
2. Document any workflow adjustments needed
3. Create quick reference for when to use each model
4. Share findings with any other Roksys team members using Claude Code

