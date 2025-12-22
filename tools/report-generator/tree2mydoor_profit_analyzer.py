#!/usr/bin/env python3
"""
Tree2mydoor Profit-Focused Campaign Analyzer
Specialized analyzer for ProfitMetrics accounts with Product Hero integration
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from campaign_analyzer import CampaignAnalyzer


class Tree2mydoorProfitAnalyzer(CampaignAnalyzer):
    """
    Specialized analyzer for Tree2mydoor's profit-based optimization

    Key Differences from Generic Analyzer:
    - Treats conversions_value as PROFIT (not revenue)
    - Uses POAS (Profit on Ad Spend) terminology
    - Understands Product Hero labels (Heroes/Sidekicks/Villains/Zombies)
    - Respects Tier A/B/C campaign structure
    - Provides seasonality-aware insights (December = peak season)
    - Generates comprehensive reports suitable for Gareth (ADHD consideration)
    """

    def __init__(self):
        super().__init__()

        # Tree2mydoor-specific targets
        self.tier_targets = {
            'tier_a': 1.80,  # ≥1.80x POAS
            'tier_b': 1.45,  # ≥1.45x POAS
            'tier_c': 1.35,  # ≥1.35x POAS or throttle
            'account_target': 1.60  # 1.60x account-level blended target
        }

        # Product Hero label hierarchy
        self.product_hero_labels = ['Heroes', 'Sidekicks', 'Villains', 'Zombies']

        # Seasonality context
        self.peak_months = [11, 12, 5]  # November, December (Christmas/memorial), May (Mother's Day)
        self.current_month = datetime.now().month

    def analyze_campaigns(
        self,
        client_slug: str,
        campaign_data: List[Dict[str, Any]],
        date_range: Dict[str, str],
        product_data: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhanced campaign analysis with profit-focused insights

        Args:
            client_slug: Client identifier (should be 'tree2mydoor')
            campaign_data: Campaign performance data from Google Ads API
            date_range: Date range for analysis
            product_data: Product-level data (optional, from Product Hero)

        Returns:
            Comprehensive analysis dict with profit-focused recommendations
        """
        # Validate this is Tree2mydoor
        if client_slug != 'tree2mydoor':
            print(f"⚠️  WARNING: This analyzer is specialized for Tree2mydoor")
            print(f"   Using for '{client_slug}' may produce inaccurate recommendations")

        # Run base analysis (this handles campaign-level metrics)
        analysis = super().analyze_campaigns(client_slug, campaign_data, date_range)

        # Override terminology: ROAS → POAS throughout
        analysis = self._apply_profit_terminology(analysis)

        # Add profit-specific context
        analysis['profit_context'] = self._generate_profit_context()

        # Enhance recommendations with profit insights
        analysis['recommendations'] = self._enhance_recommendations_with_profit_insights(
            analysis.get('recommendations', []),
            analysis.get('campaign_analyses', [])
        )

        # Add Product Hero analysis if product data provided
        if product_data:
            analysis['product_hero_analysis'] = self._analyze_product_hero_performance(product_data)

        # Add tier structure guidance
        analysis['tier_guidance'] = self._generate_tier_guidance(
            analysis.get('campaign_analyses', [])
        )

        # Add seasonality context
        analysis['seasonality_context'] = self._generate_seasonality_context(date_range)

        return analysis

    def _apply_profit_terminology(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Replace all 'ROAS' references with 'POAS' for clarity"""

        # Update recommendations
        if 'recommendations' in analysis:
            for rec in analysis['recommendations']:
                # Update title
                if 'ROAS' in rec.get('title', ''):
                    rec['title'] = rec['title'].replace('ROAS', 'POAS')

                # Update recommendation text
                if 'recommendation' in rec:
                    rec['recommendation'] = rec['recommendation'].replace('ROAS', 'POAS')
                    rec['recommendation'] = rec['recommendation'].replace('revenue', 'profit')

                # Update issue type
                if rec.get('issue_type') == 'low_roas':
                    rec['issue_type'] = 'low_poas'

        # Update summary
        if 'summary' in analysis:
            analysis['summary'] = analysis['summary'].replace('ROAS', 'POAS')

        return analysis

    def _generate_profit_context(self) -> Dict[str, Any]:
        """Generate profit-specific context for the report"""
        return {
            'uses_profitmetrics': True,
            'conversions_value_meaning': 'PROFIT (not revenue)',
            'target_poas': self.tier_targets['account_target'],
            'tier_structure': {
                'Tier A': f"≥{self.tier_targets['tier_a']:.2f}x POAS - Heroes & top Sidekicks",
                'Tier B': f"≥{self.tier_targets['tier_b']:.2f}x POAS - Mid-performing products",
                'Tier C': f"≥{self.tier_targets['tier_c']:.2f}x POAS or throttle - Marginal performers"
            },
            'optimization_focus': 'Maximize profit while maintaining growth',
            'key_considerations': [
                'Stock instability affects campaign learning',
                'December is peak season for gift trees',
                'Memorial/anniversary roses perform well year-round',
                'CPC inflation outpacing efficiency gains'
            ]
        }

    def _enhance_recommendations_with_profit_insights(
        self,
        recommendations: List[Dict[str, Any]],
        campaign_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Add profit-specific insights to recommendations"""

        enhanced_recommendations = []

        for rec in recommendations:
            # Add profit-aware actions
            if rec.get('issue_type') == 'low_poas' or rec.get('issue_type') == 'low_roas':
                rec = self._add_profit_optimization_actions(rec, campaign_analyses)

            # Add tier-based guidance
            rec = self._add_tier_based_guidance(rec)

            # Add Product Hero recommendations
            rec = self._add_product_hero_recommendations(rec)

            enhanced_recommendations.append(rec)

        # Add new profit-specific recommendations
        profit_recs = self._generate_profit_specific_recommendations(campaign_analyses)
        enhanced_recommendations.extend(profit_recs)

        return enhanced_recommendations

    def _add_profit_optimization_actions(
        self,
        recommendation: Dict[str, Any],
        campaign_analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Add profit-focused optimization actions"""

        affected_campaigns = recommendation.get('campaign_names', [])

        # Find campaigns with issues
        issue_campaigns = [
            c for c in campaign_analyses
            if c.get('campaign_name') in affected_campaigns
        ]

        if not issue_campaigns:
            return recommendation

        # Generate profit-specific actions
        profit_actions = [
            "\n\n🎯 **PROFIT-FOCUSED ACTIONS:**",
            ""
        ]

        for campaign in issue_campaigns:
            metrics = campaign.get('metrics', {})
            poas = metrics.get('roas', 0)  # This is actually POAS (profit/spend)
            spend = metrics.get('spend', 0)
            profit = metrics.get('revenue', 0)  # This is actually profit

            campaign_name = campaign.get('campaign_name', 'Unknown')

            # Determine which tier this campaign should be in
            if poas >= self.tier_targets['tier_a']:
                tier = 'Tier A'
                action = f"**{campaign_name}** ({poas:.2f}x POAS)\n   ✅ PERFORMING WELL - Tier A standard achieved\n   → Consider increasing budget by 15-20% to scale profit"
            elif poas >= self.tier_targets['tier_b']:
                tier = 'Tier B'
                action = f"**{campaign_name}** ({poas:.2f}x POAS)\n   ⚠️  TIER B - Below Tier A threshold\n   → Review Product Hero labels - shift budget to Heroes/Sidekicks\n   → Target POAS: {self.tier_targets['tier_a']:.2f}x"
            elif poas >= self.tier_targets['tier_c']:
                tier = 'Tier C'
                action = f"**{campaign_name}** ({poas:.2f}x POAS)\n   ⚠️  TIER C - Marginal profitability\n   → THROTTLE budget (reduce by 30%)\n   → Review for Villains/Zombies draining budget\n   → Minimum POAS: {self.tier_targets['tier_c']:.2f}x"
            else:
                tier = 'Below Tier C'
                action = f"**{campaign_name}** ({poas:.2f}x POAS)\n   🚨 UNPROFITABLE - Below minimum threshold\n   → PAUSE or reduce budget by 50%\n   → Check for feed issues, stock problems\n   → Review Product Hero labels for Zombies"

            profit_actions.append(action)
            profit_actions.append("")

        # Add to recommendation text
        recommendation['recommendation'] += '\n'.join(profit_actions)

        return recommendation

    def _add_tier_based_guidance(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Add tier structure guidance to recommendations"""

        # Add tier context to next steps
        if 'next_steps' not in recommendation:
            recommendation['next_steps'] = []

        tier_steps = [
            f"Review Tier structure: A (≥{self.tier_targets['tier_a']:.2f}x), B (≥{self.tier_targets['tier_b']:.2f}x), C (≥{self.tier_targets['tier_c']:.2f}x)",
            "Check Product Hero labels via Channable - shift budget to Heroes/Sidekicks",
            "Verify ProfitMetrics data accuracy - ensure optimizing to profit values"
        ]

        # Prepend tier steps (unless already present)
        for step in reversed(tier_steps):
            if step not in recommendation['next_steps']:
                recommendation['next_steps'].insert(0, step)

        return recommendation

    def _add_product_hero_recommendations(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Add Product Hero-specific recommendations"""

        product_hero_context = """

📊 **PRODUCT HERO OPTIMIZATION:**

Product Hero automatically classifies products into performance tiers:
- **Heroes**: Top revenue generators - maximize visibility
- **Sidekicks**: Good converters needing more impressions - scale carefully
- **Villains**: Underperforming but salvageable - review/optimize
- **Zombies**: No conversions/poor performance - exclude or throttle heavily

**Actions via Channable:**
1. Check product label distribution in feed
2. Verify campaigns are properly segmented by labels
3. Ensure Zombies aren't draining budget from Heroes
4. Consider separate asset groups for Heroes vs Sidekicks
"""

        # Add to recommendation if not already present
        if 'Product Hero' not in recommendation.get('recommendation', ''):
            recommendation['recommendation'] += product_hero_context

        return recommendation

    def _generate_profit_specific_recommendations(
        self,
        campaign_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate additional profit-focused recommendations"""

        recommendations = []

        # Calculate account-level POAS
        total_spend = sum(c['metrics']['spend'] for c in campaign_analyses)
        total_profit = sum(c['metrics']['revenue'] for c in campaign_analyses)  # Actually profit
        account_poas = total_profit / total_spend if total_spend > 0 else 0

        # Recommendation 1: Account-level POAS assessment
        if account_poas < self.tier_targets['account_target']:
            poas_gap = self.tier_targets['account_target'] - account_poas
            poas_gap_pct = (poas_gap / self.tier_targets['account_target']) * 100

            recommendations.append({
                'priority': 'P0' if account_poas < 1.0 else 'P1',
                'issue_type': 'account_poas_below_target',
                'title': 'Account-Level POAS Below Target',
                'affected_campaigns': len(campaign_analyses),
                'campaign_names': [c['campaign_name'] for c in campaign_analyses],
                'impact': {
                    'total_spend': total_spend,
                    'total_profit': total_profit,
                    'avg_roas': account_poas  # Keep this key name for compatibility
                },
                'recommendation': f"""🎯 **ACCOUNT-LEVEL PROFIT OPTIMIZATION REQUIRED**

Current Account POAS: {account_poas:.2f}x
Target Account POAS: {self.tier_targets['account_target']:.2f}x
Gap: {poas_gap:.2f}x ({poas_gap_pct:.1f}% below target)

**ROOT CAUSE ANALYSIS:**

This account uses ProfitMetrics - conversions_value = PROFIT (not revenue).
Account-level POAS below {self.tier_targets['account_target']:.2f}x target indicates:

1. **Too much budget on low-margin products** (Villains/Zombies)
2. **CPC inflation outpacing profit gains** (noted in context)
3. **Stock instability** disrupting campaign learning
4. **Insufficient budget on Heroes/Sidekicks**

**IMMEDIATE ACTIONS:**

**Budget Reallocation (Channable + Google Ads):**
1. Tier A campaigns (≥{self.tier_targets['tier_a']:.2f}x): +20% budget
2. Tier B campaigns ({self.tier_targets['tier_b']:.2f}x-{self.tier_targets['tier_a']:.2f}x): Hold steady
3. Tier C campaigns ({self.tier_targets['tier_c']:.2f}x-{self.tier_targets['tier_b']:.2f}x): -30% budget
4. Below Tier C (<{self.tier_targets['tier_c']:.2f}x): Pause or -50% budget

**Product Hero Review:**
1. Export product labels from Channable
2. Calculate POAS by label (Heroes vs Sidekicks vs Villains vs Zombies)
3. Ensure Zombies are excluded from campaigns
4. Shift impressions to Heroes through bidding/budgets

**Feed Quality Check:**
1. Review stock stability - OOS events reset learning
2. Check for SKU/variant handling issues
3. Verify pricing consistency across feed

**Expected Impact:**
- Account POAS increase: +0.15-0.25x within 14 days
- Profit increase: £{poas_gap * total_spend:.0f}-£{(poas_gap + 0.10) * total_spend:.0f} over 30 days
- Campaign learning improvement from stable feed
""",
                'next_steps': [
                    f"Pull Channable product labels export - calculate POAS by Hero/Sidekick/Villain/Zombie",
                    f"Identify campaigns with POAS <{self.tier_targets['tier_c']:.2f}x - reduce budget by 30-50%",
                    "Review top 20 spend products - verify they're Heroes/Sidekicks, not Villains",
                    "Check for recent stock instability events in Shopify/feed logs",
                    f"Set up weekly POAS monitoring alerts for campaigns dropping below {self.tier_targets['account_target']:.2f}x"
                ],
                'kb_articles': []  # Will be populated by KB search if enabled
            })

        # Recommendation 2: Seasonality optimization (if in peak season)
        if self.current_month in self.peak_months:
            peak_month_name = ['', '', '', '', '', 'May', '', '', '', '', '', 'November', 'December'][self.current_month]

            recommendations.append({
                'priority': 'P1',
                'issue_type': 'seasonality_optimization',
                'title': f'{peak_month_name} Peak Season Optimization',
                'affected_campaigns': len(campaign_analyses),
                'campaign_names': [c['campaign_name'] for c in campaign_analyses],
                'impact': {
                    'total_spend': total_spend,
                    'total_profit': total_profit,
                    'avg_roas': account_poas
                },
                'recommendation': f"""🎄 **{peak_month_name.upper()} PEAK SEASON - MAXIMIZE PROFIT OPPORTUNITY**

{peak_month_name} is a PEAK SEASON for Tree2mydoor:
- December: Christmas gifts, memorial trees
- November: Pre-Christmas, memorial occasions
- May: Mother's Day (prime gifting season)

**Current Performance:**
- Account POAS: {account_poas:.2f}x
- Total Profit: £{total_profit:,.0f}
- Campaigns Analyzed: {len(campaign_analyses)}

**PEAK SEASON ACTIONS:**

**1. Budget Scaling (Immediate):**
   - Tier A campaigns (≥{self.tier_targets['tier_a']:.2f}x): Increase budget by 30-50%
   - Focus on Heroes - maximum impression share during peak demand
   - Monitor daily - scale aggressively if POAS holds

**2. Product Focus:**
   - **Memorial/Sympathy Roses** (At Peace series) - year-round demand, peak in Dec
   - **Anniversary Roses** (Diamond 60th, Ruby 40th) - gift-focused
   - **Olive Trees** (peace symbolism) - popular Christmas gifts
   - **Citrus Trees** (Lemon/Orange) - unique gifts

**3. Feed Quality Critical:**
   - Stock instability during peak = massive missed opportunity
   - Ensure all Heroes have stable stock through {peak_month_name}
   - Monitor feed daily for out-of-stock events
   - Have backup products ready if Heroes go OOS

**4. Asset Optimization:**
   - Update ad copy to emphasize gift-giving themes
   - Highlight delivery deadlines for Christmas
   - Emphasize MyTree™ care service (peace of mind for gift-givers)
   - Use seasonal imagery in Performance Max assets

**Expected Impact:**
- Profit increase: +25-40% vs non-peak months
- Volume increase: +30-50% conversions
- Maintain POAS: ≥{self.tier_targets['account_target']:.2f}x despite scale

**Risk Management:**
- Watch for CPC inflation (competition increases in peak)
- Don't sacrifice POAS for volume - minimum {self.tier_targets['tier_c']:.2f}x
- Have budget ceiling ready in case POAS drops below breakeven
""",
                'next_steps': [
                    f"Review last year's {peak_month_name} performance - benchmark expectations",
                    "Export top 20 Heroes - verify stock levels sufficient for peak demand",
                    f"Set up daily POAS monitoring for {peak_month_name} - catch issues fast",
                    "Prepare asset refresh with seasonal messaging",
                    f"Calculate budget headroom - how much can we spend at {self.tier_targets['account_target']:.2f}x POAS?"
                ],
                'kb_articles': []
            })

        return recommendations

    def _analyze_product_hero_performance(
        self,
        product_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze performance by Product Hero labels"""

        # Group products by label
        label_performance = {}

        for product in product_data:
            label = product.get('product_hero_label', 'Unknown')

            if label not in label_performance:
                label_performance[label] = {
                    'products': [],
                    'total_spend': 0,
                    'total_profit': 0,
                    'total_conversions': 0,
                    'total_clicks': 0
                }

            label_performance[label]['products'].append(product)
            label_performance[label]['total_spend'] += product.get('cost', 0)
            label_performance[label]['total_profit'] += product.get('revenue', 0)
            label_performance[label]['total_conversions'] += product.get('conversions', 0)
            label_performance[label]['total_clicks'] += product.get('clicks', 0)

        # Calculate POAS by label
        for label, data in label_performance.items():
            if data['total_spend'] > 0:
                data['poas'] = data['total_profit'] / data['total_spend']
            else:
                data['poas'] = 0

        return label_performance

    def _generate_tier_guidance(
        self,
        campaign_analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate tier-based campaign guidance"""

        tier_campaigns = {
            'tier_a': [],
            'tier_b': [],
            'tier_c': [],
            'below_tier_c': []
        }

        for campaign in campaign_analyses:
            poas = campaign['metrics'].get('roas', 0)  # Actually POAS
            campaign_name = campaign.get('campaign_name', 'Unknown')

            if poas >= self.tier_targets['tier_a']:
                tier_campaigns['tier_a'].append(campaign)
            elif poas >= self.tier_targets['tier_b']:
                tier_campaigns['tier_b'].append(campaign)
            elif poas >= self.tier_targets['tier_c']:
                tier_campaigns['tier_c'].append(campaign)
            else:
                tier_campaigns['below_tier_c'].append(campaign)

        return {
            'tier_distribution': {
                'Tier A (≥1.80x)': len(tier_campaigns['tier_a']),
                'Tier B (≥1.45x)': len(tier_campaigns['tier_b']),
                'Tier C (≥1.35x)': len(tier_campaigns['tier_c']),
                'Below Tier C': len(tier_campaigns['below_tier_c'])
            },
            'tier_campaigns': tier_campaigns,
            'guidance': self._generate_tier_guidance_text(tier_campaigns)
        }

    def _generate_tier_guidance_text(
        self,
        tier_campaigns: Dict[str, List[Dict[str, Any]]]
    ) -> str:
        """Generate actionable tier-based guidance"""

        guidance = []

        # Tier A guidance
        if tier_campaigns['tier_a']:
            guidance.append(f"✅ **TIER A ({len(tier_campaigns['tier_a'])} campaigns)** - Excellent performance")
            guidance.append("   → Scale these aggressively (increase budget by 20-30%)")
            guidance.append("   → Focus Product Hero Heroes/Sidekicks here")
            guidance.append("")

        # Tier B guidance
        if tier_campaigns['tier_b']:
            guidance.append(f"⚠️  **TIER B ({len(tier_campaigns['tier_b'])} campaigns)** - Good but improvable")
            guidance.append("   → Maintain current budget")
            guidance.append(f"   → Optimize to reach Tier A threshold ({self.tier_targets['tier_a']:.2f}x)")
            guidance.append("   → Review for Villains draining budget")
            guidance.append("")

        # Tier C guidance
        if tier_campaigns['tier_c']:
            guidance.append(f"⚠️  **TIER C ({len(tier_campaigns['tier_c'])} campaigns)** - Marginal profitability")
            guidance.append("   → THROTTLE these (reduce budget by 30%)")
            guidance.append(f"   → Must improve to ≥{self.tier_targets['tier_b']:.2f}x or consider pausing")
            guidance.append("   → Check for Zombies eating budget")
            guidance.append("")

        # Below Tier C guidance
        if tier_campaigns['below_tier_c']:
            guidance.append(f"🚨 **BELOW TIER C ({len(tier_campaigns['below_tier_c'])} campaigns)** - Unprofitable")
            guidance.append("   → PAUSE or reduce budget by 50%")
            guidance.append("   → Review for feed/tracking issues")
            guidance.append("   → Check Product Hero labels - likely heavy Villain/Zombie presence")
            guidance.append("")

        return '\n'.join(guidance)

    def _generate_seasonality_context(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Generate seasonality context for the reporting period"""

        is_peak_season = self.current_month in self.peak_months

        if is_peak_season:
            season_name = {
                5: "Mother's Day (May)",
                11: "Pre-Christmas (November)",
                12: "Christmas Peak (December)"
            }.get(self.current_month, "Peak Season")
        else:
            season_name = "Non-peak season"

        return {
            'is_peak_season': is_peak_season,
            'season_name': season_name,
            'current_month': self.current_month,
            'context': self._get_seasonality_guidance(is_peak_season)
        }

    def _get_seasonality_guidance(self, is_peak: bool) -> str:
        """Get seasonality-specific guidance"""

        if is_peak:
            return """
🎄 **PEAK SEASON ACTIVE**

This is a HIGH-DEMAND period for Tree2mydoor:
- Gift purchases increase significantly
- Memorial/sympathy orders elevated
- Competition intensifies (watch CPCs)

**Strategy:**
- Maximize impression share on top performers
- Ensure stock stability (OOS = missed opportunity)
- Scale budget on Tier A campaigns
- Monitor POAS daily - catch issues fast
- Prepare for post-season decline (Jan/Feb)
"""
        else:
            return """
📊 **NON-PEAK SEASON**

Normal demand period - focus on efficiency:
- Maintain POAS targets strictly
- Build up high-performing campaigns for next peak
- Test new products/categories
- Optimize feed quality for next seasonal surge
- Review and improve asset quality

**Opportunity:**
- Lower CPCs (less competition)
- Good time to test Villains (cheap clicks)
- Build up Product Hero data for peak season decisions
"""


def main():
    """Test the profit analyzer with sample data"""

    print("🌳 Tree2mydoor Profit-Focused Analyzer")
    print("=" * 60)
    print()

    analyzer = Tree2mydoorProfitAnalyzer()

    # Sample campaign data (matching Tree2mydoor structure)
    sample_campaigns = [
        {
            'name': 'T2MD | P Max | HP&P 150 5/9 140 23/10',
            'id': '15820346778',
            'status': 'ENABLED',
            'type': 'PERFORMANCE_MAX',
            'metrics': {
                'cost_micros': 1356584153,  # £1,356.58
                'conversions_value': 1948249866,  # £1,948.25 PROFIT
                'conversions': 101.571985,
                'clicks': 1336,
                'impressions': 95834,
                'search_impression_share': 0,
                'search_budget_lost_impression_share': 0
            }
        },
        {
            'name': 'T2MD | Shopping | Catch All 170 150 20/10 140 23/10',
            'id': '22986754502',
            'status': 'ENABLED',
            'type': 'SHOPPING',
            'metrics': {
                'cost_micros': 319690000,  # £319.69
                'conversions_value': 498127686,  # £498.13 PROFIT
                'conversions': 29.743024,
                'clicks': 404,
                'impressions': 42166,
                'search_impression_share': 0,
                'search_budget_lost_impression_share': 0
            }
        }
    ]

    date_range = {
        'start_date': '2025-12-07',
        'end_date': '2025-12-13'
    }

    analysis = analyzer.analyze_campaigns(
        'tree2mydoor',
        sample_campaigns,
        date_range
    )

    print(f"✅ Analysis Complete")
    print(f"   Health Score: {analysis['health_score']}/100")
    print(f"   Account POAS: {analysis.get('blended_roas', 0):.2f}x")
    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
    print()

    # Print profit context
    print("💰 Profit Context:")
    profit_ctx = analysis.get('profit_context', {})
    print(f"   Uses ProfitMetrics: {profit_ctx.get('uses_profitmetrics')}")
    print(f"   Target POAS: {profit_ctx.get('target_poas'):.2f}x")
    print()

    # Print tier guidance
    print("📊 Tier Structure:")
    tier_guidance = analysis.get('tier_guidance', {})
    tier_dist = tier_guidance.get('tier_distribution', {})
    for tier, count in tier_dist.items():
        print(f"   {tier}: {count} campaigns")
    print()

    print("✅ Profit analyzer working correctly")


if __name__ == '__main__':
    main()
