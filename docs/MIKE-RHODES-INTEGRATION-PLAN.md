# Mike Rhodes 8020Brain Integration Plan
**Created:** 2025-11-19
**Updated Template Version:** 2025.11.0 (November 1, 2025)
**Approach:** Learn, enhance, don't replace

---

## 🎯 Philosophy

**Key Principles:**
1. **Learn from Mike's experience** - He has more coding expertise
2. **Enhance, don't replace** - Keep your skills, add Mike's patterns
3. **Interactive learning** - Understand WHY things are built a certain way
4. **Preserve your operational focus** - Mike's is content-focused, yours is client operations

---

## 📊 Phase 1: CSV Analyzer
**Status:** ✅ COMPLETE (2025-11-19)
**Priority:** ⭐ HIGH - Immediate ROI on client reports
**Time Estimate:** 3-4 hours (actual: 3.5 hours)
**Location:** `.claude/skills/csv-analyzer/`

### What You'll Learn

**Mike's Key Innovations:**
1. **Two-script architecture** - General + specialized Google Ads analyzer
2. **Auto-detection** - Identifies Google Ads format automatically (skiprows=2)
3. **Robust file finding** - Handles spaces, fuzzy matching
4. **Data cleaning patterns** - Commas, currency, percentages, '--' handling
5. **No-questions philosophy** - Immediately analyzes without user prompts
6. **Smart visualization** - Only creates charts that make sense for the data

### Implementation Steps

#### Step 1: Study the Code (30-45 minutes)

**Files to review:**
```
/Users/administrator/Documents/brain/.claude/skills/csv-analyzer/
├── skill.md              ← Skill instructions (read first)
├── analyze.py            ← General CSV analyzer
├── analyze_google_ads.py ← Google Ads specific analyzer
├── requirements.txt      ← Dependencies
└── examples/             ← Example data
```

**Learning objectives:**
- [ ] Understand the "no questions" philosophy (lines 21-34 in skill.md)
- [ ] How `detect_google_ads_format()` works (lines 42-63 in analyze.py)
- [ ] How `clean_numeric_columns()` handles messy data (lines 65-83)
- [ ] Google Ads specific cleaning patterns (lines 27-49 in analyze_google_ads.py)
- [ ] Campaign-level aggregation logic (lines 133-149 in analyze_google_ads.py)

**Questions to answer:**
1. Why does Mike skip the first 2 rows for Google Ads exports?
2. How does he handle '--' values in Google Ads data?
3. What's the benefit of creating `column_numeric` duplicates vs replacing?
4. Why separate enabled vs paused ad groups?

#### Step 2: Create Your Implementation (1-2 hours)

**Create:**
```
/Users/administrator/Documents/PetesBrain/.claude/skills/csv-analyzer/
├── skill.md              ← Adapt Mike's instructions
├── analyze.py            ← Port Mike's general analyzer
├── analyze_google_ads.py ← Port Mike's Google Ads analyzer
├── requirements.txt      ← pandas, matplotlib, seaborn
├── examples/             ← Add sample client reports
└── LEARNING-NOTES.md     ← Your observations from Mike's code
```

**Adaptations needed:**
1. **File paths:** Change `/Users/{MAC_USER}/Desktop/` to your working directory
2. **British English:** "Analyse" vs "Analyze" in comments/output
3. **ROAS format:** Change `2.92x` to `292%` in output
4. **Your branding:** Add your report styling if applicable
5. **Integration:** Make it work with your existing report workflows

#### Step 3: Test with Real Data (30 minutes)

**Test cases:**
```bash
# Create test directory
mkdir -p ~/.claude/skills/csv-analyzer/examples

# Test 1: General CSV (not Google Ads)
# - Should create: correlation_heatmap.png, distributions.png, etc.

# Test 2: Google Ads export
# - Should auto-detect skiprows=2
# - Should create: ad_groups_by_spend.png, campaign_performance.png, etc.

# Test 3: CSV with missing data
# - Should report missing values gracefully

# Test 4: CSV with commas and currency symbols
# - Should clean and convert properly
```

**Validation:**
- [ ] Auto-detects Google Ads format
- [ ] Cleans commas, currency, percentages
- [ ] Handles '--' values (Google Ads)
- [ ] Creates appropriate visualizations
- [ ] No user prompts (immediate analysis)
- [ ] Works with your client report CSVs

#### Step 4: Integrate with Your Workflow (30-45 minutes)

**Where to use:**
1. Client monthly reports (automate CSV analysis)
2. Performance reviews (quick campaign analysis)
3. Ad hoc client questions (instant insights)
4. Your existing report generator tools

**Integration points:**
- `tools/report-generator/` - Add CSV analysis capability
- Client reports - Automate insights from exported data
- Your existing Python scripts - Import Mike's functions

#### Step 5: Document Your Learning (15 minutes)

**Create:** `LEARNING-NOTES.md` with:
- What Mike does differently than you would have
- Why his approach is better (or not)
- Patterns you'll apply to other skills
- Questions for future improvements

---

## 📋 Phase 2: Compare Google Ads Skills

**Status:** ✅ COMPLETE (2025-11-19)
**Priority:** 🟡 MEDIUM - Learning opportunity
**Time Estimate:** 2-3 hours (actual: 2 hours)
**Goal:** Learn from Mike's patterns, enhance yours
**Outcome:** PetesBrain enhanced with Mike's documentation files while retaining Product Impact Analyzer advantage

### What to Compare

**Your existing skills:**
```
/Users/administrator/Documents/PetesBrain/.claude/skills/
├── google-ads-campaign-audit/
├── google-ads-text-generator/
├── gaql-query-builder/
└── google-ads-campaign-builder/
```

**Mike's skills:**
```
/Users/administrator/Documents/brain/.claude/skills/
├── demo-google-ads-campaign-audit/
├── demo-google-ads-keyword-audit/
├── gaql-query-builder/
├── google-ads-account-info/
└── google-ads-campaign-performance/
```

### Comparison Framework

For each skill, document:

**1. Coverage**
- What does Mike's version cover that yours doesn't?
- What does yours cover that Mike's doesn't?
- Are they solving the same problem?

**2. Implementation Quality**
- Code organization and structure
- Error handling patterns
- User experience (prompts, output)
- Documentation quality

**3. Learning Opportunities**
- Patterns you can adopt
- Better ways to structure prompts
- Improved error messages
- Documentation improvements

**4. Decision**
- ✅ **Keep yours** (it's better/more comprehensive)
- 🔄 **Enhance yours** (add Mike's patterns)
- 📚 **Learn only** (interesting but not applicable)
- ⚠️ **Replace** (Mike's is significantly better)

### Step-by-Step Process

#### 2.1: Campaign Audit Comparison (45 mins)

**Your version:** `google-ads-campaign-audit/`
**Mike's version:** `demo-google-ads-campaign-audit/`

**Compare:**
```bash
# Read both skill.md files
Read: .claude/skills/google-ads-campaign-audit/skill.md
Read: /Users/administrator/Documents/brain/.claude/skills/demo-google-ads-campaign-audit/skill.md

# Compare file structure
ls -la .claude/skills/google-ads-campaign-audit/
ls -la /Users/administrator/Documents/brain/.claude/skills/demo-google-ads-campaign-audit/
```

**Document:**
- Audit scope differences
- GAQL queries used
- Output format and insights
- Which is more comprehensive?

**Decision:** [Keep yours | Enhance yours | Replace]

#### 2.2: GAQL Query Builder Comparison (30 mins)

**Your version:** `gaql-query-builder/`
**Mike's version:** `gaql-query-builder/`

**Compare:**
- Query templates provided
- Error handling
- Documentation of Google Ads API quirks
- Examples provided

**Decision:** [Merge best of both]

#### 2.3: Skills You Don't Have (30 mins)

**Mike has these that you don't:**
- `google-ads-account-info` - Account structure hierarchy
- `google-ads-campaign-performance` - Performance analysis
- `demo-google-ads-keyword-audit` - Keyword analysis

**Evaluate:**
- Do you need these capabilities?
- Do you have this functionality elsewhere?
- Worth implementing?

#### 2.4: Skills Mike Doesn't Have (15 mins)

**You have these that Mike doesn't:**
- `google-ads-text-generator` - RSA/ad copy generation
- `google-ads-campaign-builder` - Campaign creation workflows

**Reflect:**
- Why doesn't Mike need these?
- What makes your use case different?
- Could Mike benefit from your approach?

### Deliverable

**Create:** `docs/GOOGLE-ADS-SKILLS-COMPARISON.md`

Template:
```markdown
# Google Ads Skills Comparison
## Campaign Audit
- **Your version:** [strengths]
- **Mike's version:** [strengths]
- **Decision:** [Keep/Enhance/Replace]
- **Action items:** [specific improvements]

## [Repeat for each skill]

## Overall Learnings
- Key patterns from Mike to adopt
- Areas where your approach is stronger
- Net new capabilities to implement
```

---

## 🌅 Phase 3: Daily Briefing System

**Status:** ✅ COMPLETE (2025-11-19)
**Priority:** 🟢 HIGH - Daily operational value
**Time Estimate:** 2-3 hours (actual: 2 hours)
**Outcome:** Comprehensive analysis complete - Enhancement roadmap documented

### What You'll Learn

**Mike's approach:**
- Calendar integration (Google Calendar API)
- Todo aggregation from multiple sources
- Recent activity summary
- Output formatting (markdown)

**Your context:**
- You already have: Weekly client performance summaries
- You already have: Daily performance anomaly detection
- You already have: Google Calendar MCP integration
- You need: Morning briefing to start your day

### Implementation Approach

**Don't replace your existing tools - enhance them:**

1. **Study Mike's briefing generator**
```
/Users/administrator/Documents/brain/.claude/skills/briefing-generator/
```

2. **Create new agent** (not replace existing):
```
/Users/administrator/Documents/PetesBrain/agents/daily-briefing/
├── daily-briefing.py
├── agent.md
└── config.plist (LaunchAgent for 7:00 AM)
```

3. **Integrate your existing data sources:**
- `data/cache/daily-performance-anomalies.json` (you already have this)
- `data/state/tasks-state.json` (your tasks)
- Google Calendar via MCP (meetings today)
- Recent client emails (from your email sync)
- Recent knowledge base updates (from your KB processors)

4. **Output to:**
```
/Users/administrator/Documents/PetesBrain/briefing/YYYY-MM-DD-briefing.md
```

### Learning Objectives

- How Mike structures his calendar queries
- His markdown formatting patterns
- How he prioritizes information
- Integration patterns with Google APIs

### Deliverable

A morning briefing that includes:
- **Today's meetings** (from Google Calendar)
- **Priority tasks** (P0/P1 from your task system)
- **Client alerts** (from daily anomaly detection)
- **Recent updates** (KB additions, email highlights)
- **Yesterday's summary** (key completions)

---

## 🧠 Phase 4: Knowledge Base Search

**Status:** Pending
**Priority:** 🟢 HIGH - Makes your 178+ docs searchable
**Time Estimate:** 4-5 hours

### What You'll Learn

**Mike's brain-advisor agent:**
```
/Users/administrator/Documents/brain/.claude/agents/brain-advisor.md
```

**Key concepts:**
- Semantic search vs keyword search
- Context window management
- Query expansion techniques
- Result ranking and relevance

### Your Knowledge Base Structure

```
/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/
├── google-ads/              (50+ docs)
│   ├── performance-max/
│   ├── shopping/
│   ├── search/
│   └── platform-updates/
├── facebook-ads/            (10+ docs)
├── ai-strategy/             (25+ docs)
├── analytics/               (15+ docs)
├── industry-insights/       (30+ docs)
└── rok-methodologies/       (20+ docs)
```

**Total:** 178+ markdown files

### Implementation Approach

**Option A: Simple (2-3 hours)**
- Basic keyword search with grep
- Rank by relevance (number of matches)
- Return top 5 matching files
- Let Claude Code read and synthesize

**Option B: Advanced (4-5 hours)**
- Build search index (file paths + first 500 chars)
- Use Claude API for semantic matching
- Cache results for common queries
- Progressive context disclosure

### Learning Path

1. **Study Mike's approach** (1 hour)
   - Read `brain-advisor.md` thoroughly
   - Understand his search strategy
   - Note any APIs or tools he uses

2. **Prototype simple version** (1-2 hours)
   - Start with keyword search
   - Test with common queries:
     - "PMax bidding strategies"
     - "Google Ads platform updates November 2025"
     - "Facebook campaign structure best practices"

3. **Enhance based on usage** (1-2 hours)
   - Add semantic search if needed
   - Improve ranking algorithm
   - Add caching for speed

4. **Integrate with your workflow** (30 mins)
   - Create command: `/search-kb [query]`
   - Make it accessible in daily briefing
   - Test with real client questions

### Deliverable

**Tool:** `tools/kb-search/` (already exists - enhance it!)
**Agent:** `agents/knowledge-search/` (new)
**Command:** `/search-kb` (add to `.claude/commands/`)

**Test queries:**
- "How do I optimize PMax campaigns for ROAS?"
- "What changed in Google Ads in the last 30 days?"
- "Best practices for Shopping feed optimization"
- "Facebook campaign structure for e-commerce"

---

## 📥 Phase 5: Inbox Processing

**Status:** Pending
**Priority:** 🟢 HIGH - Better task capture
**Time Estimate:** 2-3 hours

### What You'll Learn

**Mike's inboxy agent:**
```
/Users/administrator/Documents/brain/.claude/agents/inboxy.md
```

**Concepts:**
- Action keyword detection ("todo", "write post", "video script")
- Smart routing to appropriate folders
- Context preservation
- Quick capture workflow

### Your Current Workflow

You already have:
- Email sync (labels, automated processing)
- Google Tasks integration
- Meeting notes import (Granola)
- Wispr Flow import (voice notes)

**Gap:** Quick capture for ad-hoc ideas/tasks while working

### Implementation Approach

**1. Create inbox folder:**
```
/Users/administrator/Documents/PetesBrain/!inbox/
```

**2. Create processor agent:**
```
/Users/administrator/Documents/PetesBrain/agents/inbox-processor/
├── inbox-processor.py
├── agent.md
└── config.plist (process every 6 hours)
```

**3. Define action keywords:**
- `[TASK]` → Add to client tasks.json
- `[CLIENT: name]` → Route to client folder
- `[KB]` → Add to knowledge base inbox
- `[IDEA]` → Add to context/ideas/
- `[EXPERIMENT]` → Prompt for 5 questions, add to rok-experiments
- `[NOTE]` → Add to appropriate client notes

**4. Processor workflow:**
```python
1. Scan !inbox/ for .md files
2. Parse action keywords
3. Route to appropriate location
4. Archive processed file to !inbox/processed/
5. Log processing results
```

### Learning Objectives

- Mike's keyword parsing patterns
- How he preserves context during routing
- Error handling (ambiguous instructions)
- User feedback mechanisms

### Deliverable

Quick capture workflow:
1. Drop note in `!inbox/note.md`
2. Processor runs every 6 hours (or on demand)
3. Note routed to appropriate location
4. Confirmation logged

**Test cases:**
```
!inbox/2025-11-19-smythson-roas-idea.md
---
[TASK] [CLIENT: smythson]
Experiment: Increase tROAS from 400% to 450% for 7 days
Expected: Reduced impression share, maintained efficiency
---
```

Should create:
- Task in `clients/smythson/tasks.json`
- Prompt to log experiment
- Archive to `!inbox/processed/`

---

## 🎨 Phase 6: Learn from Remaining Agents

**Status:** Pending
**Priority:** 🟡 MEDIUM - Learning only
**Time Estimate:** 3-4 hours

### Mike's Other Agents

**Content Creation:**
- `posty.md` - Social media posts
- `image-finder.md` - Find relevant images
- `update-doc.md` - Maintain documentation
- `briefly.md` - Summarize content

**Research:**
- `newsletter-idea-extractor.md` - Newsletter summaries
- `youtube-idea-extractor.md` - YouTube summaries

**Development:**
- `githuby.md` - Git operations
- `datastory.md` - Data narratives

### Learning Approach

**For each agent:**
1. **Read the agent definition** (15 mins)
2. **Identify key patterns** (10 mins)
   - How are prompts structured?
   - What's the workflow?
   - Any reusable patterns?
3. **Note applicability** (5 mins)
   - Relevant to your work?
   - Could enhance existing tools?
   - Pure learning exercise?

### Deliverable

**Create:** `docs/MIKE-RHODES-PATTERNS.md`

Document:
- **Prompt Engineering Patterns** (how Mike structures instructions)
- **Workflow Patterns** (multi-step processes)
- **Error Handling Patterns** (graceful failures)
- **Documentation Patterns** (how he documents agents/skills)
- **Naming Conventions** (file naming, folder structure)

Use this as reference when building future skills/agents.

---

## 📈 Success Metrics

### Phase 1 (CSV Analyzer)
- ✅ Can analyze any CSV without user prompts
- ✅ Auto-detects Google Ads exports
- ✅ Handles messy data (commas, currency, '--')
- ✅ Creates appropriate visualizations
- ✅ Saves 30-60 min per client report

### Phase 2 (Skills Comparison)
- ✅ Documented comparison for each skill
- ✅ Identified patterns to adopt
- ✅ Enhanced at least 2 existing skills
- ✅ Clear decision on each skill (keep/enhance/replace)

### Phase 3 (Daily Briefing)
- ✅ Morning briefing generated at 7:00 AM
- ✅ Includes calendar, tasks, alerts, updates
- ✅ Saves 15-20 min each morning
- ✅ Integrated with your existing data sources

### Phase 4 (Knowledge Search)
- ✅ Can search 178+ KB docs in < 5 seconds
- ✅ Returns relevant results for common queries
- ✅ Integrated into daily workflow
- ✅ Used at least once per day

### Phase 5 (Inbox Processing)
- ✅ Quick capture workflow works reliably
- ✅ 95%+ accurate routing
- ✅ Used daily for idea capture
- ✅ Reduces friction for task creation

### Phase 6 (Learning)
- ✅ Patterns document created
- ✅ Applied patterns to 2+ of your own tools
- ✅ Improved your prompt engineering skills
- ✅ Better understanding of Mike's architecture

---

## 🎓 Overall Learning Goals

**By the end of this process, you should understand:**

1. **Architecture patterns** - How to structure skills vs agents vs commands
2. **Prompt engineering** - Mike's approach to clear, directive prompts
3. **Data handling** - Robust parsing, cleaning, error handling
4. **User experience** - When to ask questions vs act decisively
5. **Integration** - How to connect multiple tools into workflows
6. **Documentation** - Clear, comprehensive skill/agent documentation
7. **Testing** - How to validate functionality systematically

**Apply these learnings to:**
- Your existing tools (enhance them)
- Future skills/agents (build better from start)
- Client work (more efficient workflows)
- Your PetesBrain evolution (architectural decisions)

---

## 📅 Timeline Recommendation

**Week 1:**
- Phase 1: CSV Analyzer (3-4 hours)
- Phase 2: Skills comparison (2-3 hours)
- **Total:** 5-7 hours

**Week 2:**
- Phase 3: Daily Briefing (2-3 hours)
- Phase 4: Knowledge Search (4-5 hours)
- **Total:** 6-8 hours

**Week 3:**
- Phase 5: Inbox Processing (2-3 hours)
- Phase 6: Learn from agents (3-4 hours)
- **Total:** 5-7 hours

**Total Investment:** 16-22 hours over 3 weeks
**Expected ROI:** 60-90 min saved per day + improved code quality

---

## 📝 Progress Tracking

**Use TodoWrite to track each phase:**
- Mark phases complete as you finish
- Add sub-tasks for each step
- Document learnings in LEARNING-NOTES.md
- Update this plan with insights gained

**Monthly review:**
- Check Mike's template for updates (`git pull origin main`)
- Review CHANGELOG.md for new features
- Assess if new features are worth integrating
- Update your integration plan accordingly

---

**Ready to start Phase 1?**

Let's implement the CSV Analyzer step by step, learning from Mike's approach as we go!
