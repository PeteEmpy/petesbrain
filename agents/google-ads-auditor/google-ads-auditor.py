#!/usr/bin/env python3
"""
Google Ads Account Auditor

Automated weekly audit of Google Ads accounts using ROK's systematic analysis framework.
Generates comprehensive audit reports covering:
- Campaign structure and performance
- Product/keyword performance
- Impression share opportunities
- Budget efficiency
- Actionable recommendations

Runs weekly (Monday 10 AM) or on-demand for specific clients.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Client configuration
CLIENTS = [
    "smythson",
    "devonshire-hotels",
    "tree2mydoor",
    "uno-lighting",
    "superspace",
    "positive-bakes",
    # Add more active clients
]

AUDIT_TYPES = {
    "weekly": "Comprehensive weekly performance review",
    "impression_share": "Auction insights and impression share analysis",
    "keyword": "Keyword and search query optimization",
    "structure": "Account segmentation and restructuring analysis",
}


def log(message: str):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


class GoogleAdsAuditor:
    """Automated Google Ads account auditor"""
    
    def __init__(self, client_slug: str):
        self.client_slug = client_slug
        self.client_dir = PROJECT_ROOT / "clients" / client_slug
        self.audits_dir = self.client_dir / "audits"
        self.audits_dir.mkdir(parents=True, exist_ok=True)
        
        # Load client context if available
        self.context = self._load_context()
    
    def _load_context(self) -> Dict[str, Any]:
        """Load client CONTEXT.md for business intelligence"""
        context_file = self.client_dir / "CONTEXT.md"
        if context_file.exists():
            with open(context_file, 'r') as f:
                return {"raw": f.read()}
        return {}
    
    def run_weekly_audit(self, days: int = 7) -> str:
        """
        Run comprehensive weekly audit (Prompt 1 from ROK framework)
        
        Analyzes:
        - Campaign overview (impressions, clicks, spend, ROAS)
        - Product-level performance
        - Placement analysis
        - Audience & asset insights
        - Budget efficiency
        - Root cause diagnostics
        - Prioritized recommendations
        """
        log(f"Running weekly audit for {self.client_slug}...")
        
        audit_prompt = f"""You are a senior Google Ads analyst specializing in e-commerce Google Ads.

Client: {self.client_slug}
Date Range: Last {days} days

Please perform the following analyses:

1. Campaign Overview
Summarize total impressions, clicks, spend, conversions, conversion value, ROAS, CTR, CVR, and CPA.

2. Product-Level Performance
Break down performance metrics (impressions, clicks, spend, conversions, ROAS) by product or product group.

Identify the top 10 best-performing and bottom 10 worst-performing products by ROAS and conversion volume.

Flag products with week-over-week changes in ROAS or conversions exceeding ±15%.

3. Placement Analysis
Analyze spend and conversion performance across key placements (Shopping, YouTube, Display, Discover, Gmail).

Highlight which placements drive the highest ROAS and which are underperforming.

4. Audience & Asset Insights
Review the audience segments contributing most to conversions and revenue.

Identify any underperforming asset groups or creatives causing wasted spend or low CTR.

5. Spend & Budget Efficiency
Check for pacing issues, budget caps, or inefficient spend allocation within campaigns.

6. Root Cause Diagnostics
For flagged products or placements, diagnose potential issues such as feed data quality, auction competition, or creative fatigue.

7. Recommendations
Prioritize 3–5 actionable recommendations for bidding, budget allocation, feed improvements, or creative refreshes.

8. Output Format
Provide a structured Markdown report with:
→ An executive summary highlighting key metrics and notable changes.
→ Tables for product-level and placement performance (limit to 20 rows).
→ Bullet-pointed insights and prioritized next steps.

Use human-friendly metrics (e.g., dollars, percentages) and clear headings.
"""
        
        # Save audit prompt for manual execution if needed
        audit_config = {
            "type": "weekly",
            "client": self.client_slug,
            "date_range_days": days,
            "prompt": audit_prompt,
            "generated": datetime.now().isoformat(),
        }
        
        config_file = self.audits_dir / f"audit-config-{datetime.now().strftime('%Y%m%d')}.json"
        with open(config_file, 'w') as f:
            json.dump(audit_config, f, indent=2)
        
        log(f"✓ Audit configuration saved: {config_file.name}")
        
        return self._save_audit_template("weekly", audit_prompt)
    
    def run_impression_share_audit(self) -> str:
        """
        Run impression share audit (Prompt 2 from ROK framework)
        
        Analyzes:
        - Impression share metrics
        - Lost IS due to budget vs rank
        - Competitive pressure detection
        - Growth opportunities
        - Recovery recommendations
        """
        log(f"Running impression share audit for {self.client_slug}...")
        
        audit_prompt = f"""You are a senior Google Ads analyst with expertise in Shopping campaigns.

For {self.client_slug}, analyze auction insights and impression share data for the active Shopping campaigns.

Please perform the following:

1. For each campaign, ad group, and product group, report:
→ Impression Share (IS)
→ Lost Impression Share due to Budget (IS Lost Budget %)
→ Lost Impression Share due to Rank (IS Lost Rank %)
→ Average Position or Top of Page Rate, if available

2. Identify where impression share loss is most significant (>10%) and determine whether it is primarily due to budget constraints or rank issues.

3. Detect any notable week-over-week changes in impression share metrics that may indicate competitive pressure or new entrants in auctions.

4. Provide insights on which campaigns or product groups have the highest opportunity for growth if the budget is increased or bids are improved.

5. Recommend prioritized actions, such as:
→ Increasing budgets to recover lost impression share due to budget caps
→ Raising bids or improving quality signals for segments losing impression share due to rank
→ Restructuring campaigns or product groups to better compete in auctions

Output: A clear, concise Markdown report including:
→ Tables summarizing key impression share metrics at the campaign, ad group, and product group levels
→ A bullet-point summary of major findings and root causes
→ A prioritized action plan based on potential revenue impact

Present all data using clear visualizations with minimal technical jargon, focusing on business impact rather than ad metrics.
"""
        
        return self._save_audit_template("impression_share", audit_prompt)
    
    def run_keyword_audit(self) -> str:
        """
        Run keyword optimization audit (Prompt 3 from ROK framework)
        
        Analyzes:
        - Underperforming keywords (wasted spend)
        - High-potential keywords (growth opportunities)
        - Declining keywords (ad/LP optimization needed)
        - Zero-conversion queries (negative keyword candidates)
        """
        log(f"Running keyword audit for {self.client_slug}...")
        
        audit_prompt = f"""You are a senior Google Ads analyst focused on ecommerce Search campaigns.

Client: {self.client_slug}

Analyze all active Search campaigns and provide only actionable insights by:

1. Reporting on keywords and search queries that meet these criteria:
→ Keywords or queries with spend ≥ $50 and ROAS below account average × 0.7 (potential waste)
→ Keywords or queries with ≥ 2 conversions and ROAS ≥ account average × 1.3 (growth opportunities)
→ Keywords or queries with week-over-week CTR or CVR declines > 15% (need ad or landing page optimization)
→ Queries generating spend with zero conversions (negative keyword candidates)

2. For all items above, recommend specific optimizations, such as:
→ Bid increases or decreases
→ Adding new exact or phrase match keywords
→ Adding negative keywords
→ Ad copy or landing page improvements

3. Skip any keywords or queries that show stable or good performance and require no action.

4. Provide a concise Markdown report including:
→ Summary tables limited to actionable items only
→ Bullet-pointed, prioritized recommendations
→ Clear section headers and human-readable metrics

Focus solely on what can be improved or optimized.
"""
        
        return self._save_audit_template("keyword", audit_prompt)
    
    def run_structure_audit(self) -> str:
        """
        Run account structure audit (Prompt 4 from ROK framework)
        
        Analyzes:
        - Campaign architecture
        - Product group segmentation
        - Bid control opportunities
        - Reporting clarity issues
        - Restructuring recommendations
        """
        log(f"Running structure audit for {self.client_slug}...")
        
        audit_prompt = f"""You are a senior Google Ads expert analyzing {self.client_slug}.

Please follow these steps:

1. Identify overly broad product groups that may be masking performance details.

2. Evaluate the granularity and logic of the current segmentation.

3. Suggest restructuring approaches to improve bid control and reporting clarity.

Return a Markdown report with segmentation insights and actionable restructuring advice.
"""
        
        return self._save_audit_template("structure", audit_prompt)
    
    def _save_audit_template(self, audit_type: str, prompt: str) -> str:
        """Save audit template for manual execution"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date_str}-{audit_type}-audit-template.md"
        filepath = self.audits_dir / filename
        
        template_content = f"""# {audit_type.replace('_', ' ').title()} Audit - {self.client_slug}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Type:** {AUDIT_TYPES.get(audit_type, 'Custom audit')}  
**Status:** 🟡 Template Ready - Run with Claude + MCP

---

## 🎯 Audit Objective

{AUDIT_TYPES.get(audit_type, 'Custom audit analysis')}

---

## 📋 Execution Instructions

### Option 1: Claude Code + MCP (Recommended)

1. Open Claude Code (Cursor)
2. Ensure Google Ads MCP server is connected
3. Copy the prompt below
4. Paste into Claude Code
5. Claude will fetch data and generate the report
6. Save output to this file

### Option 2: Manual Analysis

1. Export data from Google Ads UI
2. Use the prompt as a framework
3. Manually analyze and document findings

---

## 🤖 Audit Prompt

```
{prompt}
```

---

## 📊 Audit Results

<!-- Claude will populate this section when run -->

*Run the audit prompt above to generate results here*

---

## 📝 Action Items

- [ ] Review audit findings
- [ ] Prioritize recommendations by impact
- [ ] Create Google Tasks for each action
- [ ] Update client CONTEXT.md with key learnings
- [ ] Schedule follow-up audit

---

## 🔗 Related Files

- [Client Context](../CONTEXT.md)
- [ROK Analysis Prompts](../../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)
- [Previous Audits](./)

"""
        
        with open(filepath, 'w') as f:
            f.write(template_content)
        
        log(f"✓ Audit template saved: {filepath.name}")
        return str(filepath)
    
    def run_full_audit_suite(self) -> List[str]:
        """Run complete audit suite for comprehensive analysis"""
        log(f"Running full audit suite for {self.client_slug}...")
        
        audit_files = []
        audit_files.append(self.run_weekly_audit())
        audit_files.append(self.run_impression_share_audit())
        audit_files.append(self.run_keyword_audit())
        audit_files.append(self.run_structure_audit())
        
        # Create index file
        self._create_audit_index(audit_files)
        
        return audit_files


    def _create_audit_index(self, audit_files: List[str]):
        """Create index of all audits"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        index_file = self.audits_dir / f"{date_str}-audit-index.md"
        
        content = f"""# Audit Suite - {self.client_slug}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Status:** 🟡 Templates Ready

---

## 📋 Audit Templates Generated

{chr(10).join(f"- [{Path(f).name}](./{Path(f).name})" for f in audit_files)}

---

## 🎯 Recommended Execution Order

1. **Weekly Audit** - Run first for overall health check
2. **Impression Share** or **Keyword Audit** - Based on weekly findings
3. **Structure Audit** - Run quarterly or when major issues found

---

## 💡 Tips

- Use Claude Code + Google Ads MCP for automated data fetching
- Cross-reference findings with client CONTEXT.md
- Create Google Tasks for each action item
- Save completed audits for historical reference
- Update CONTEXT.md with key learnings

"""
        
        with open(index_file, 'w') as f:
            f.write(content)
        
        log(f"✓ Audit index created: {index_file.name}")


def run_weekly_audits_all_clients():
    """Run weekly audits for all active clients"""
    log("=" * 60)
    log("Weekly Google Ads Audit - All Clients")
    log("=" * 60)
    log("")
    
    total_audits = 0
    
    for client_slug in CLIENTS:
        client_dir = PROJECT_ROOT / "clients" / client_slug
        
        if not client_dir.exists():
            log(f"⚠️  Client folder not found: {client_slug}")
            continue
        
        try:
            auditor = GoogleAdsAuditor(client_slug)
            audit_files = auditor.run_full_audit_suite()
            total_audits += len(audit_files)
            log(f"✅ {client_slug}: {len(audit_files)} audit templates created")
            log("")
        
        except Exception as e:
            log(f"❌ Error auditing {client_slug}: {e}")
            log("")
    
    log("=" * 60)
    log(f"✅ Complete: {total_audits} audit templates generated")
    log("=" * 60)


def run_audit_for_client(client_slug: str, audit_type: str = "weekly"):
    """Run specific audit for a single client"""
    log(f"Running {audit_type} audit for {client_slug}...")
    
    auditor = GoogleAdsAuditor(client_slug)
    
    if audit_type == "weekly":
        audit_file = auditor.run_weekly_audit()
    elif audit_type == "impression_share":
        audit_file = auditor.run_impression_share_audit()
    elif audit_type == "keyword":
        audit_file = auditor.run_keyword_audit()
    elif audit_type == "structure":
        audit_file = auditor.run_structure_audit()
    elif audit_type == "full":
        audit_files = auditor.run_full_audit_suite()
        log(f"✅ Full audit suite created: {len(audit_files)} templates")
        return
    else:
        log(f"❌ Unknown audit type: {audit_type}")
        return
    
    log(f"✅ Audit template created: {audit_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Google Ads Account Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run weekly audits for all clients
  python3 google-ads-auditor.py --all
  
  # Run specific audit for one client
  python3 google-ads-auditor.py --client smythson --type weekly
  
  # Run full audit suite for one client
  python3 google-ads-auditor.py --client smythson --type full
  
Audit Types:
  weekly          - Comprehensive weekly performance review
  impression_share - Auction insights and impression share
  keyword         - Keyword and search query optimization
  structure       - Account segmentation analysis
  full            - All audit types
        """
    )
    
    parser.add_argument('--all', action='store_true', help='Run audits for all active clients')
    parser.add_argument('--client', help='Specific client slug')
    parser.add_argument('--type', default='weekly', help='Audit type (default: weekly)')
    
    args = parser.parse_args()
    
    try:
        if args.all:
            run_weekly_audits_all_clients()
        elif args.client:
            run_audit_for_client(args.client, args.type)
        else:
            parser.print_help()
    
    except Exception as e:
        log(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

