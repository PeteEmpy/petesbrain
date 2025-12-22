# Session Continuity - Quick Start Guide

**3-Minute Guide to Using the Session Continuity System**

---

## What Is This?

A system that makes AI remember what you discussed, decided, and are investigating across sessions - transforming AI from amnesiac assistant to genuine partner.

**Problem it solves:** "Wait, what did we decide about X last week?"

**How it works:** Three practices you'll do every session (takes 3 minutes total)

---

## The 3-Minute Workflow

### Start of Session (60 seconds)

**Run this command:**
```
/client <client-name>
```

**Example:**
```
/client smythson
```

**What you get:**
```
🟢 Smythson - Context Briefing
==========================================

## ✓ Strategic Context
- Target ROAS: 400%
- Current focus: Profit-first optimisation
- Monthly budget: £8,500 total

## ✓ Last Session Summary
**Date:** 2025-12-20 (Shopping campaign optimisation)
**Decided:** Paused low-margin products, created leather goods campaign
**Still investigating:** Travel category ROAS drop

## ✓ Open Questions (1)
- Why did Travel category ROAS drop 170 points? (High priority)

## ✓ Active Tasks (3)
- [Smythson] Review new leather goods campaign performance (P1)

**Ready to work on Smythson. What would you like to do?**
```

**Read this briefing** (takes 60 seconds) - now you have full context.

---

### During Session (0 seconds)

**Work normally.**

**If you notice something interesting but non-urgent:**

Add to open-questions.md:
```markdown
**Question:** Why is mobile ROAS 50% lower than desktop?
**Noticed:** 2025-12-22
**Hypothesis:** Mobile users researching, desktop users converting?
**Priority:** Medium
**Status:** Open
```

**That's it.** Keep working.

---

### End of Session (2 minutes)

**Open `clients/<client-name>/session-log.md`**

**Add this entry:**
```markdown
## Session: 2025-12-22 (Brief topic description)

**Analysed:**
- What you examined (bullet points)

**Decided:**
- Actions you took (budget changes, pauses, etc.)
- Experiments you launched

**Still investigating:**
- Open questions that need more data

**Next session:**
- What to check next time
```

**Example:**
```markdown
## Session: 2025-12-22 (Shopping Campaign Optimisation)

**Analysed:**
- Shopping campaign structure (5 campaigns, 3 product groups)
- Product performance by margin tier

**Decided:**
- Paused low-margin products in "All Products" campaign
- Created dedicated campaign for high-margin leather goods
- Increased bids 20% on Panama collection

**Still investigating:**
- Why Travel category ROAS dropped from 450% to 280%

**Next session:**
- Check Travel category performance after 7 days
- Review new campaign structure results
```

**Time:** 2 minutes

---

## Total Time Investment

- **Start of session:** 60 seconds (load context)
- **During session:** 0 seconds (work normally)
- **End of session:** 2 minutes (update log)

**Total: 3 minutes per session**

**Value: Infinite** (never lose context, decisions compound over time)

---

## The Files (You Already Have Them)

Every client folder now has:

1. **`session-log.md`** - Session summaries
   - What you analysed
   - What you decided
   - What you're still investigating
   - What to check next time

2. **`open-questions.md`** - Unresolved questions
   - Interesting patterns to investigate
   - Hypotheses to test
   - Curiosities that aren't urgent tasks

3. **`CONTEXT.md`** - Strategic context (already existed)
   - Target ROAS, budgets, goals
   - Account structure
   - Current focus

4. **`tasks-completed.md`** - Historical decisions (already existed)
   - Archive of completed tasks
   - Searchable history

---

## Real Examples

### Example 1: Starting Your Next Session

**You:** `/client smythson`

**Claude:** [Shows briefing with last session summary]

**You (reading):** "Oh right, we paused low-margin products last week. Let me check if that improved ROAS."

**Without continuity:** "Hmm, what was I working on last time? Let me try to remember... was it budgets? Or products? Or..."

---

### Example 2: Avoiding Repeated Mistakes

**You:** "Should we increase bids on Panama collection?"

**Claude (checking session-log.md):**

"⚠️ We tested this in October 2025:
- Increased bids 25%
- ROAS dropped 60 points
- Reversed after 10 days

Recommendation: Don't repeat the same experiment."

**Without continuity:** *Makes the same mistake again, wastes another 10 days*

---

### Example 3: Building Knowledge Over Time

**Month 1:** Fixed budget issue on one campaign
**Month 2:** Noticed same pattern on another campaign, created framework
**Month 3:** Systematised the solution, automated the checks

**Each month builds on the last** - knowledge compounds.

**Without continuity:** Fix the same issue repeatedly, never systemise.

---

## What Not to Do

❌ **Don't skip the briefing** - defeats the purpose
❌ **Don't forget to update session-log.md** - future you needs this
❌ **Don't write essays** - bullet points only (2 minutes max)
❌ **Don't create tasks for every curiosity** - use open-questions.md

---

## Templates (Copy These)

### Session Log Entry
```markdown
## Session: YYYY-MM-DD (Brief topic)

**Analysed:**
- [What you examined]

**Decided:**
- [Actions taken]

**Still investigating:**
- [Open questions]

**Next session:**
- [What to check]
```

### Open Question
```markdown
**Question:** [Clear question]
**Noticed:** YYYY-MM-DD
**Hypothesis:** [Your theory]
**Priority:** [High/Medium/Low]
**Status:** Open
```

---

## Cheat Sheet

| When | Do This | Time |
|------|---------|------|
| **Start session** | `/client <name>` → Read briefing | 60s |
| **During work** | Notice something? → Add to open-questions.md | 30s |
| **End session** | Update session-log.md with summary | 2min |

**Total: 3 minutes per session**

---

## First Time Using This?

**Test it now:**

1. Pick a client you worked on recently
2. Run `/client <client-name>`
3. Read the briefing (currently just the setup entry)
4. Open `clients/<client-name>/session-log.md`
5. Add an entry about your LAST session (from memory)
6. See how this would have helped if it existed last time

**Next time you work on that client:**
- Run `/client <client-name>` first
- You'll see your last session summary
- You'll pick up exactly where you left off

**That's when you'll feel the value.**

---

## Questions?

**"What if I forget to update session-log.md?"**
- Update it later from memory
- Mark as `[Retroactive: Added YYYY-MM-DD]`
- Better late than never

**"What if I don't have 2 minutes at the end?"**
- Quick version: Just fill "Decided" section
- Add the rest later

**"How detailed should summaries be?"**
- Enough that future-you understands context
- Brief enough to scan in 30 seconds
- Bullet points, not paragraphs

**"What if nothing changes?"**
- Don't create an entry for every tiny thing
- Only significant sessions (30+ minutes of work)
- Weekly reviews always get an entry

**"Where's the full documentation?"**
- `/Users/administrator/Documents/PetesBrain/docs/SESSION-CONTINUITY-SYSTEM.md`
- 400+ lines with examples, best practices, troubleshooting

---

## The Bigger Picture

**This is Phase 4 of Mike Rhodes' Ads to AI Skill Map:**

- Phase 1-3: Automated reporting & analysis ✅ (You have this)
- **Phase 4: Business Context** ✅ (This system)
- Phase 5: Business Brain (Knowledge compounds over time)
- Phase 6: Autonomous Agents

**Session continuity is how you get to Phase 5** - an AI system that gets smarter every week because it remembers everything it learned.

**Without continuity:**
- Knowledge plateaus
- Decisions get forgotten
- Mistakes get repeated

**With continuity:**
- Knowledge compounds
- Decisions build on history
- AI becomes a genuine partner

---

## Start Using It Right Now

**Step 1:** Pick your most active client

**Step 2:** Run `/client <client-name>`

**Step 3:** Start your work session with full context

**Step 4:** At the end, spend 2 minutes updating session-log.md

**That's it.**

**After 3-4 sessions, you'll never want to work without it.**

---

**The goal:** Never start a conversation from zero again.

**The practice:** 3 minutes per session (60s load + 2min update)

**The result:** AI that remembers, knowledge that compounds, decisions that build on history.
