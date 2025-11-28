# Anthropic API Usage Analysis
**Generated:** 2025-11-20

## Overview
Your PetesBrain system has **35+ automated agents** making direct Anthropic API calls. These are **separate from your Claude Pro/Max plan** and generate API charges.

---

## Current API Usage by Agent

### HIGH FREQUENCY (Running Constantly)

#### 1. **ai-inbox-processor** 🔴 HIGH COST
- **Model:** Claude 3.5 Sonnet (expensive) + Haiku fallback
- **Schedule:** Every 10 minutes (144x per day)
- **Purpose:** Process voice notes from !inbox/
- **Est. Monthly Cost:** $15-30
- **Status:** Currently running

### DAILY AGENTS (Running Once Per Day)

#### 2. **daily-intel-report**
- **Model:** Claude 3.5 Haiku (cheap)
- **Schedule:** Daily at 7:00 AM
- **Purpose:** Morning briefing with AI summary (2-3 sentences)
- **Est. Monthly Cost:** $0.50-1.00
- **Status:** Currently running

#### 3. **granola-google-docs-importer**
- **Model:** Claude 3.5 Haiku (cheap)
- **Schedule:** Every 30 minutes
- **Purpose:** Import meeting notes from Granola
- **Est. Monthly Cost:** $2-4
- **Status:** Not currently running

#### 4. **ai-google-chat-processor**
- **Model:** Claude 3.5 Haiku (cheap)
- **Schedule:** Every 10 minutes (when active)
- **Purpose:** Process Google Chat messages
- **Est. Monthly Cost:** $3-6
- **Status:** Not currently running

### WEEKLY AGENTS (High-Cost Sonnet 4.5)

#### 5. **weekly-blog-generator** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Weekly (Mondays 7:30 AM)
- **Purpose:** Generate blog posts for roksys.co.uk
- **Est. Monthly Cost:** $5-10 per run
- **Status:** Not currently running

#### 6. **kb-weekly-summary** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Weekly (Sundays)
- **Purpose:** Knowledge base weekly summary
- **Est. Monthly Cost:** $5-10 per run
- **Status:** Not currently running

#### 7. **weekly-news-digest** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Weekly
- **Purpose:** Compile industry news digest
- **Est. Monthly Cost:** $3-6 per run
- **Status:** Not currently running

### MONITORING AGENTS (Sonnet 4.5)

#### 8. **google-specs-monitor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Monitor Google Ads specifications
- **Est. Monthly Cost:** $10-20
- **Status:** Currently running

#### 9. **google-specs-processor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Process Google Ads spec changes
- **Est. Monthly Cost:** $5-10
- **Status:** Currently running

#### 10. **facebook-specs-monitor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Monitor Facebook Ads specifications
- **Est. Monthly Cost:** $5-10
- **Status:** Not currently running

#### 11. **facebook-specs-processor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Process Facebook spec changes
- **Est. Monthly Cost:** $5-10
- **Status:** Not currently running

#### 12. **shopify-news-monitor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Monitor Shopify platform news
- **Est. Monthly Cost:** $3-6
- **Status:** Not currently running

#### 13. **ai-news-monitor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Monitor AI industry news
- **Est. Monthly Cost:** $3-6
- **Status:** Not currently running

#### 14. **industry-news-monitor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Monitor digital marketing news
- **Est. Monthly Cost:** $3-6
- **Status:** Not currently running

#### 15. **knowledge-base-processor** 🔴 HIGH COST
- **Model:** Claude Sonnet 4.5 (MOST EXPENSIVE)
- **Schedule:** Daily
- **Purpose:** Process knowledge base updates
- **Est. Monthly Cost:** $5-10
- **Status:** Not currently running

### INTERACTIVE TOOLS (On-Demand)

#### 16. **kb-search.py**
- **Model:** Claude Sonnet 4.5
- **Usage:** When you manually search knowledge base
- **Est. Cost:** $0.10-0.50 per search

#### 17. **client-search.py**
- **Model:** Claude Sonnet 4.5
- **Usage:** When you manually search client data
- **Est. Cost:** $0.10-0.50 per search

#### 18. **google-ads-generator** (Tools)
- **Model:** Claude models (various)
- **Usage:** When you generate ad copy
- **Est. Cost:** $0.50-2.00 per generation

#### 19. **google-ads-campaign-builder** (Tools)
- **Model:** Claude models (various)
- **Usage:** When you build campaigns
- **Est. Cost:** $1-5 per campaign build

---

## Cost Breakdown Summary

### Currently Running (Estimated Monthly Cost)
- **ai-inbox-processor:** $15-30 (HIGH - Sonnet 3.5, 144x/day)
- **daily-intel-report:** $0.50-1 (Haiku, 1x/day)
- **google-specs-monitor:** $10-20 (Sonnet 4.5, daily)
- **google-specs-processor:** $5-10 (Sonnet 4.5, daily)

**Total Currently Running: $30.50-61/month**

### Currently Disabled (Would Add)
- **Weekly agents:** $13-26/month
- **News monitors:** $14-28/month
- **Facebook specs:** $10-20/month
- **Other monitoring:** $8-16/month

**Total If All Enabled: $75.50-151/month**

---

## Model Pricing (Nov 2025)

### Haiku (Cheapest)
- Input: $0.25 per million tokens
- Output: $1.25 per million tokens
- **Used by:** daily-intel-report, granola-importer

### Sonnet 3.5 (Mid-tier)
- Input: $3 per million tokens
- Output: $15 per million tokens
- **Used by:** ai-inbox-processor (complex tasks)

### Sonnet 4.5 (Most Expensive)
- Input: $3 per million tokens
- Output: $15 per million tokens
- **Used by:** Most monitoring agents, news processors, KB tools

---

## Biggest Cost Drivers

### 1. **ai-inbox-processor** (Runs every 10 minutes)
- Uses expensive Sonnet 3.5 for complex processing
- Runs 144 times per day
- **Action:** Consider reducing frequency or switching to Haiku

### 2. **google-specs-monitor + processor** (Daily, Sonnet 4.5)
- Currently running
- Processing Google Ads specification changes
- **Action:** Evaluate if daily monitoring is necessary

### 3. **Weekly content generators** (Currently disabled)
- blog-generator, kb-summary, news-digest
- All use expensive Sonnet 4.5
- **Action:** Keep disabled unless actively needed

---

## Recommendations

### Immediate Cost Reduction (Save ~60-80%)

1. **Reduce ai-inbox-processor frequency:**
   ```bash
   # Change from 10 minutes to 30 minutes
   # Edit: agents/launchagents/com.petesbrain.ai-inbox-processor.plist
   # Change: <integer>600</integer> → <integer>1800</integer>
   ```
   **Saves: $10-20/month**

2. **Switch ai-inbox-processor to Haiku for simple tasks:**
   - Edit agent to use Haiku by default
   - Only use Sonnet for truly complex notes
   **Saves: $5-15/month**

3. **Disable google-specs monitoring (if not critical):**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.petesbrain.google-specs-monitor.plist
   launchctl unload ~/Library/LaunchAgents/com.petesbrain.google-specs-processor.plist
   ```
   **Saves: $15-30/month**

### Long-term Optimization

1. **Batch processing:** Run AI agents less frequently
2. **Model downgrading:** Use Haiku where possible
3. **Caching:** Cache AI responses for repeated queries
4. **Selective processing:** Only process changed/new content

---

## How to Check Your Actual Costs

1. Go to: https://console.anthropic.com/settings/billing
2. Click "Usage" tab
3. Look for:
   - Total spend this month
   - Usage by model (Haiku vs Sonnet)
   - Usage by API key (your key: sk-ant-api03-Nkj...)

---

## Next Steps

**Choose your approach:**

### Option A: Keep Current Setup
- Current estimated cost: $30-60/month
- You get 35+ automated agents
- Consider if value justifies cost

### Option B: Optimize (Recommended)
- Reduce ai-inbox frequency
- Switch to Haiku where possible
- Estimated cost: $10-20/month

### Option C: Disable All AI Agents
- Stop all automated agents
- Only use Claude Code (covered by Pro/Max)
- Estimated cost: $0/month (only manual API tools)

**What would you like to do?**
