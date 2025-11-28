#!/usr/bin/env python3
"""
Create GoMarble Implementation Project Tasks
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

# Create parent task with all phase children
parent_task = service.create_parent_with_children(
    parent_title="[Roksys] GoMarble Analytics Implementation",
    client="roksys",
    parent_due_date="2026-01-31",
    parent_priority="P1",
    parent_notes="""Complete implementation of GoMarble-inspired analytics automation system.

**Overview:**
Structured analytics prompts for Google Ads, GA4, and cross-channel reporting.
Focus on automated client reporting and proactive optimization detection.

**Documentation:** docs/GOMARBLE-IMPLEMENTATION-PLAN.md

**Test Clients:** Godshot, Go Glean, Bright Minds

**Expected Outcomes:**
- 50% reduction in manual reporting time
- Proactive optimization detection
- Improved client satisfaction with clearer insights
- Data-driven budget increase recommendations""",
    parent_source="Strategic Initiative (Nov 19, 2025)",
    parent_tags=["gomarble", "automation", "analytics", "strategic-project"],
    children_data=[
        # Phase 1: Quick Wins (Week 1-2)
        {
            "title": "[Roksys] Phase 1A: Google Ads Weekly E-commerce Report Skill",
            "due_date": "2025-11-26",
            "priority": "P0",
            "time_estimate_mins": 240,
            "notes": """Create .claude/skills/google-ads-weekly-report/ skill.

**Output:**
- Campaign overview (spend, conversions, ROAS, CPA)
- Product-level performance (top 10 best/worst by ROAS)
- Placement analysis (Shopping, YouTube, Display, Discover)
- Week-over-week changes (>15% flagged)
- 3-5 prioritized recommendations

**Test with:** Godshot (simple), Go Glean, Bright Minds

**Success:** Generate report in <5 minutes, identify 1+ actionable insight per client

**Time:** 4 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-1", "google-ads"]
        },
        {
            "title": "[Roksys] Phase 1B: Google Ads Auction Insights Analysis Skill",
            "due_date": "2025-12-03",
            "priority": "P1",
            "time_estimate_mins": 360,
            "notes": """Create .claude/skills/google-ads-auction-insights/ skill.

**Purpose:**
- Identify lost impression share (budget vs rank)
- Quantify revenue opportunity from budget increases
- Guide client budget increase requests

**Output:**
- Impression share summary table
- Lost IS breakdown (budget vs rank)
- Revenue opportunity estimates
- Prioritized action recommendations

**Use Cases:**
- Devonshire Hotels (budget constraints)
- Accessories for the Home (recent budget increase)
- National Motorsports Academy (high CPA context)

**Time:** 6 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-1", "google-ads"]
        },
        {
            "title": "[Roksys] Phase 1C: GA4 Traffic Source Performance Skill",
            "due_date": "2025-12-10",
            "priority": "P1",
            "time_estimate_mins": 300,
            "notes": """Create .claude/skills/ga4-channel-performance/ skill.

**Purpose:**
- Compare attribution models (last-click vs data-driven)
- Identify profitable yet undervalued channels
- Explain discrepancies between GA4 and Google Ads

**Output:**
- Channel performance table
- Attribution comparison
- Underperforming high-spend channels
- Undervalued assisted conversion channels

**Use Cases:**
- Smythson (multi-channel strategy)
- Superspace (organic vs paid understanding)
- Tree2MyDoor (seasonal traffic patterns)

**Time:** 5 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-1", "ga4"]
        },
        # Phase 2: Client-Facing Automation (Week 3-4)
        {
            "title": "[Roksys] Phase 2A: Monthly Client Dashboard Generator Agent",
            "due_date": "2025-12-17",
            "priority": "P1",
            "time_estimate_mins": 720,
            "notes": """Create agents/monthly-client-dashboard/ automated reporting agent.

**Workflow:**
1. Runs 1st of each month automatically
2. Pulls Google Ads + GA4 data (previous month vs 2 months prior)
3. Generates visual HTML dashboard using GoMarble "chapters" format
4. Saves to clients/[client]/reports/monthly/
5. Creates draft email

**Chapters:**
1. The Bottom Line - Revenue, ROAS, headline metrics
2. Campaign Performance - Which campaigns drove results
3. Product Winners - Top 10 products (e-commerce only)
4. What Changed - Week-over-week trends
5. Looking Ahead - Next month goals

**Test with:** Top 5 clients by revenue

**Expected Savings:** 10+ hours/month

**Time:** 12 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-2", "automation"]
        },
        {
            "title": "[Roksys] Phase 2B: Weekly Client Email Digest Agent",
            "due_date": "2025-12-24",
            "priority": "P2",
            "time_estimate_mins": 480,
            "notes": """Create agents/weekly-client-digest/ automated email summaries.

**Schedule:** Every Monday 6am (review Sunday performance)

**Format:**
- Last Week at a Glance (revenue, ROAS, conversions)
- What's Working (top 3 wins)
- Watching Closely (concerns)
- This Week's Focus (planned actions)

**Trigger:** Can also run on-demand

**Expected Savings:** 5+ hours/week

**Time:** 8 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-2", "automation"]
        },
        # Phase 3: Optimization Automation (Week 5-6)
        {
            "title": "[Roksys] Phase 3A: Google Ads Budget Opportunity Detector Agent",
            "due_date": "2026-01-07",
            "priority": "P2",
            "time_estimate_mins": 600,
            "notes": """Create agents/budget-opportunity-detector/ proactive optimization.

**Logic:**
- Identify campaigns hitting budget caps with strong ROAS
- Lost impression share (budget) > 10%
- ROAS > target × 1.2
- Opportunity > £500/day

**Output:**
- Creates P1 tasks for manual review
- Quantifies revenue opportunity
- Recommends budget increase amount

**Schedule:** Daily 9am check

**Time:** 10 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-3", "optimization"]
        },
        {
            "title": "[Roksys] Phase 3B: Keyword Waste Detector Agent",
            "due_date": "2026-01-14",
            "priority": "P2",
            "time_estimate_mins": 720,
            "notes": """Create agents/keyword-waste-detector/ proactive optimization.

**Detection Criteria:**
1. Wasted Spend: Spend ≥£50, ROAS < avg × 0.7
2. Growth Opportunities: ≥2 conv, ROAS ≥ avg × 1.3, Lost IS (rank) > 10%
3. Zero-Conversion Waste: Spend ≥£20, 0 conversions

**Output:**
- CSV file with keyword recommendations
- Creates tasks for review
- Logs changes to experiment tracker

**Schedule:** Weekly Sunday 8pm

**Time:** 12 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-3", "optimization"]
        },
        # Phase 4: Cross-Channel Integration (Week 7-8)
        {
            "title": "[Roksys] Phase 4A: Blended Metrics Calculator Utility",
            "due_date": "2026-01-21",
            "priority": "P2",
            "time_estimate_mins": 480,
            "notes": """Create shared/blended_metrics.py utility.

**Functions:**
- calculate_mer() - Marketing Efficiency Ratio (GA4 revenue / Google Ads spend)
- calculate_attribution_discrepancy() - Google Ads vs GA4 comparison
- generate_cross_platform_report() - Unified metrics

**Use Case:**
When client says "Google Ads reports 420% ROAS but I don't see that revenue" - this explains the gap.

**Time:** 8 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-4", "cross-channel"]
        },
        {
            "title": "[Roksys] Phase 4B: Analyst Pack Generator Skill",
            "due_date": "2026-01-28",
            "priority": "P2",
            "time_estimate_mins": 600,
            "notes": """Create .claude/skills/analyst-pack/ unified reporting skill.

**Format:** 14 days vs prior 14 days across Google Ads + GA4

**Sections:**
1. Executive Summary (Google Ads, GA4, Blended MER)
2. Campaign Performance Table (top 12 by spend)
3. Traffic Source Insights (GA4 channels)
4. One-Slide Brief (what changed, top 3 drivers, biggest risk)

**When to Use:**
- Monthly client reports
- Performance investigations
- Budget allocation discussions

**Time:** 10 hours""",
            "source": "GoMarble Implementation Plan",
            "tags": ["gomarble", "phase-4", "cross-channel"]
        }
    ]
)

print(f"✅ Created GoMarble implementation project")
print(f"   Parent Task ID: {parent_task['id']}")
print(f"   Children: {len(parent_task['children'])} tasks")
print(f"   Timeline: Nov 26, 2025 - Jan 31, 2026")
print(f"\nPhase breakdown:")
print(f"   Phase 1 (Quick Wins): 3 tasks - Nov 26 to Dec 10")
print(f"   Phase 2 (Automation): 2 tasks - Dec 17 to Dec 24")
print(f"   Phase 3 (Optimization): 2 tasks - Jan 7 to Jan 14")
print(f"   Phase 4 (Cross-Channel): 2 tasks - Jan 21 to Jan 28")
print(f"\n📋 View in Task Manager to see full project structure")
