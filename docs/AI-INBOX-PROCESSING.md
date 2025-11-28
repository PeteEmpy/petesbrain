# AI-Enhanced Inbox Processing System

**Status:** ✅ Active (Enhanced Version)
**Last Updated:** 2025-11-08

## Overview

The AI-Enhanced Inbox Processing system adds intelligence to Wispr Flow notes BEFORE they're organized, making your voice notes more actionable and contextually aware.

## The Complete Workflow

```
1. Wispr Flow (Voice Note)
   "Crowd Control - look at hoses budget, refer to Jeremy's email"
   ↓
2. Wispr Flow Importer (Every 5 min)
   Saves to: !inbox/20251106-145604-wispr-crowd-control.md
   ↓
3. AI Inbox Processor (Every 10 min) ⭐ NEW
   - Analyzes note with Claude
   - Reads client CONTEXT.md if relevant
   - Expands into actionable tasks
   - Creates enhanced version
   Saves to: !inbox/ai-enhanced/enhanced-20251106-145604.md
   ↓
4. Regular Inbox Processor (Daily 8 AM or manual)
   - Processes enhanced notes
   - Creates Google Tasks with full details
   - Routes to client folders
   - Archives everything
   ↓
5. Tasks Monitor (Every 6 hours)
   - Syncs Google Tasks to CONTEXT.md
   - Tracks completions
```

## What the AI Does

### 1. Understands Intent
**Your voice note:**
> "Crowd Control - look at hoses budget"

**AI understands:**
- This is a TASK (not just a note)
- It's for the client "Crowd Control"
- It requires budget analysis
- It references an email from Jeremy

### 2. Reads Relevant Context (Smart Section Extraction)
For client notes, AI intelligently extracts relevant sections:
- Uses AI to identify which CONTEXT.md sections are most relevant
- Reads "Planned Work", "Current Issues", "Active Campaigns" sections
- Understands client's business, campaigns, current issues
- No more arbitrary truncation - gets the right context every time

### 3. Expands Into Action
**AI transforms:**
```
Original: "look at hoses budget"

Enhanced:
task: Review Water Hoses for Crowd Control Equipment
due: within 1 week
client: crowd-control

1. Check email from Jeremy about water hoses
2. Browse Amazon for suitable water hoses
3. Compare prices and specifications
4. Prepare summary of top 3-5 options
5. Discuss findings with Jeremy

Context Summary: Investigating potential equipment additions
for crowd control product line.
```

### 4. Creates Proper Routing
AI adds the right keywords so the regular inbox processor knows where to send it:
- `task: [title]` → Creates Google Task
- `client: [name]` → Routes to client folder (in task notes)
- `knowledge: [topic]` → Routes to knowledge base
- `due: [date]` → Sets task due date

## AI Capabilities

### Note Analysis
- **Client Detection**: Recognizes client names in any format
- **Intent Recognition**: Task vs note vs knowledge vs completion
- **Completion Detection**: Detects "done", "completed", "already did" - routes to documents, not tasks
- **Priority Assessment**: High/medium/low based on content
- **Urgency Detection**: Separates urgency (time-sensitive) from priority (importance)
- **Due Date Inference**: Suggests dates from "tomorrow", "next week", etc.
- **Time Estimation**: Estimates task duration ("30 min", "2 hours", etc.)
- **Follow-up Detection**: Identifies follow-ups and links to original items
- **Dependency Detection**: Finds blockers and dependencies mentioned in notes

### Context Integration
- Reads client CONTEXT.md automatically
- Understands current campaigns and issues
- References recent work and known problems
- Provides relevant background in summaries

### Content Enhancement
- Fixes voice transcription errors
- Expands vague notes into specific actions
- Breaks down tasks into steps
- Adds relevant context and reasoning

### Smart Routing
- Determines best destination automatically
- Handles multi-purpose notes (client task = both)
- Creates proper metadata for downstream processing
- **Duplicate Detection**: Checks Google Tasks + recent notes for similar tasks (>70% similarity)
- **Related Task Linking**: Finds related tasks in CONTEXT.md and Google Tasks
- **Batch Processing**: Processes multiple notes together to identify patterns

## Configuration

### Location
- Agent: `agents/system/ai-inbox-processor.py`
- LaunchAgent: `~/Library/LaunchAgents/com.petesbrain.ai-inbox-processor.plist`

### Schedule
- Runs every **10 minutes** (600 seconds)
- Processes files in `!inbox/` (not subdirectories)
- Saves enhanced versions to `!inbox/ai-enhanced/`

### API Usage
- **Adaptive Model Selection**:
  - Simple notes (<50 words): `claude-3-5-haiku-20241022` (fast & cheap)
  - Complex notes (>100 words): `claude-3-5-sonnet-20241022` (better quality)
- Cost: ~$0.01-0.10 per note (depends on complexity)
- Timeout: 60 seconds per note
- Max tokens: 1000-2000 per response (depends on complexity)

### Environment
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...  # Set in LaunchAgent plist
```

## File Flow

### Input Files
- `!inbox/*.md` - Raw Wispr Flow notes
- `!inbox/*.txt` - Text notes

### Processing
1. AI reads note + relevant CONTEXT.md
2. Analyzes with Claude API
3. Creates enhanced version
4. Moves original to `!inbox/processed/`
5. Saves enhanced to `!inbox/ai-enhanced/`

### Output Structure
```markdown
# AI-Enhanced Note
**Original:** original-filename.md
**Type:** task|client|knowledge|general|completion
**Client:** crowd-control
**Priority:** medium
**Urgency:** urgent|normal
**Estimated Time:** 30 min|2 hours|half day
**Model Used:** haiku|sonnet
**Processed:** 2025-11-08 17:31

⚠️ **DUPLICATE DETECTED**: merge|create_new|review
**Similar to:** Existing Task Name (85.2% similar)

**Dependencies/Blockers:**
- Waiting for client approval
- After Q4 report is complete

**Related Tasks:**
- Review Budget for Q4
- Update Campaign Structure

---

task: Clear Task Title
due: specific date
time: 30 min
urgent: true
client: client-name

[Expanded actionable content with numbered steps]

---

**Context Summary:** [1-2 sentence summary for CONTEXT.md]

---

**Original Note:**
[Original Wispr Flow content preserved]
```

## Agent Management

### Check Status
```bash
launchctl list | grep ai-inbox
# 20990  0  com.petesbrain.ai-inbox-processor
```

### View Logs
```bash
tail -f ~/.petesbrain-ai-inbox.log        # Success log
tail -f ~/.petesbrain-ai-inbox-error.log  # Error log
```

### Manual Run
```bash
ANTHROPIC_API_KEY="your-key" python3 agents/system/ai-inbox-processor.py
```

### Reload Agent
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.ai-inbox-processor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.ai-inbox-processor.plist
```

## Integration with Existing System

### Inbox Processor Changes
Updated to check `!inbox/ai-enhanced/` BEFORE `!inbox/`:
- Processes AI-enhanced notes first (have better routing)
- Falls back to regular inbox for any non-AI-processed notes
- Backward compatible (works with or without AI processing)

### Tasks Monitor (Unchanged)
Still syncs Google Tasks to CONTEXT.md every 6 hours

### Wispr Flow Importer (Unchanged)
Still imports notes every 5 minutes

## Example Transformations

### Client Task
**Voice:**
> "Smythson - check Q4 performance against targets"

**AI Output:**
```
task: Review Smythson Q4 Performance vs Targets
client: smythson
due: this week
priority: high

1. Pull Q4 campaign data (Oct 29 - present)
2. Compare actual revenue vs £780,691 target
3. Check spend vs £367,014 budget
4. Analyze regional performance (UK/USA/EUR/ROW)
5. Prepare summary for client meeting

Context: Q4 strategy milestones at Phase 3, Thanksgiving
boost recently implemented
```

### Personal Task
**Voice:**
> "Order magnesium and zinc tablets tomorrow"

**AI Output:**
```
task: Order Magnesium and Zinc Supplements
due: tomorrow
priority: low

1. Check current stock levels
2. Compare prices on Amazon/Holland & Barrett
3. Order preferred brands
4. Set up Subscribe & Save if available
```

### Knowledge Capture
**Voice:**
> "Google just announced new PMax asset group guidelines"

**AI Output:**
```
knowledge: Google Ads PMax

Google announced new asset group guidelines for Performance Max:
- [Expanded from voice transcription]
- [Key points extracted]
- [Relevant to current campaigns]

Reference: Check official Google Ads blog for full details
```

## Troubleshooting

### AI Not Processing Notes
1. Check API key is set:
   ```bash
   launchctl list | grep ai-inbox
   cat ~/.petesbrain-ai-inbox-error.log
   ```

2. Verify agent is running:
   ```bash
   launchctl start com.petesbrain.ai-inbox-processor
   ```

3. Check for errors in log:
   ```bash
   tail -20 ~/.petesbrain-ai-inbox-error.log
   ```

### Notes Not Enhanced Properly
- Check if anthropic package is installed
- Verify API key has credit
- Review AI response in logs for parsing errors

### Enhanced Notes Not Being Processed
- Inbox processor runs daily at 8 AM
- Run manually: `python3 agents/system/inbox-processor.py`
- Check `!inbox/ai-enhanced/` has files

## Cost & Performance

### Typical Usage
- 10-20 notes per day
- ~200-500 notes per month
- Cost: $2-$10/month

### Performance
- Processing time: 2-5 seconds per note
- Total delay: 10-15 minutes (5 min import + 10 min AI + processing)
- Still faster than manual organization!

### Optimization
- Adaptive model selection (Haiku for simple, Sonnet for complex)
- Smart CONTEXT.md section extraction (relevant parts only)
- Batch processing for multiple notes
- Duplicate detection prevents redundant tasks
- Caches nothing (each request independent)
- Max 1000-2000 tokens per response (depends on complexity)

## New Features (November 2025)

### ✅ Duplicate Detection
- Checks Google Tasks API for similar tasks
- Checks recent processed notes (last 7 days)
- Uses fuzzy string matching (70%+ similarity threshold)
- Suggests merge vs create_new vs review

### ✅ Smart CONTEXT.md Reading
- AI extracts relevant sections instead of truncating
- Focuses on "Planned Work", "Current Issues", "Active Campaigns"
- Better context understanding for each note

### ✅ Completion Detection
- Detects "done", "completed", "already did" language
- Routes completions to documents folder (not tasks)
- Prevents creating tasks for completed work

### ✅ Related Task Linking
- Searches CONTEXT.md "Planned Work" section
- Finds related Google Tasks for same client
- Links related items in enhanced notes

### ✅ Batch Processing
- Processes multiple notes together
- Identifies patterns across notes
- Better prioritization when multiple notes arrive

### ✅ Email Draft Generation
- Automatically generates email drafts for client notes
- Saves to `clients/[client]/emails/drafts/`
- Uses professional tone, references context
- Ready to review and send

### ✅ Time Estimation
- Estimates task duration
- Helps with daily planning
- Included in task metadata

### ✅ Follow-up Detection
- Detects follow-up language ("follow up", "check on")
- Links to original items when possible
- Better context for follow-up tasks

### ✅ Adaptive Model Selection
- Simple notes → Haiku (fast, cheap)
- Complex notes → Sonnet (better quality)
- Balances cost vs quality automatically

### ✅ Dependency Detection
- Finds blockers and dependencies
- Lists dependencies in enhanced notes
- Helps identify task relationships

### ✅ Urgency vs Priority
- Separates urgency (time-sensitive) from priority (importance)
- "URGENT" tag for time-sensitive items
- Better task prioritization

## Future Enhancements

Possible improvements:
- [ ] Calendar awareness for due date suggestions
- [ ] Learn from past routing decisions
- [ ] Multi-note summary and prioritization
- [ ] Voice feedback loop (confirm understanding)
- [ ] Auto-update CONTEXT.md with completions

## Related Documentation

- [INBOX-SYSTEM.md](INBOX-SYSTEM.md) - Regular inbox processor
- [AUTOMATION.md](AUTOMATION.md) - All automated agents
- [CLIENT-WORKFLOWS.md](CLIENT-WORKFLOWS.md) - Client context system

---

**Key Insight:** The AI enhancement step transforms quick voice notes into actionable, context-aware tasks WITHOUT requiring you to think about formatting or details while capturing ideas.
