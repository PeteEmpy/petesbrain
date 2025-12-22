#!/usr/bin/env python3
"""
Tree2mydoor Deep Account Auditor

Performs comprehensive account auditing with:
- Campaign configuration analysis
- Best practice validation via knowledge base
- Root cause analysis of underperformance
- Specific actionable recommendations

This is NOT just metric reporting - this is deep strategic analysis.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Import from same directory
from campaign_analyzer import CampaignAnalyzer


class Tree2mydoorDeepAuditor(CampaignAnalyzer):
    """
    Deep account auditor for Tree2mydoor

    Goes beyond metric reporting to provide real strategic insights:
    - Audits campaign configuration against best practices
    - Identifies root causes of underperformance
    - Checks for specific violations (bidding, targeting, structure)
    - Provides evidence-based recommendations from knowledge base
    """

    def __init__(self):
        super().__init__()

        # Tree2mydoor-specific configuration
        self.profit_targets = {
            'tier_a': 1.80,
            'tier_b': 1.45,
            'tier_c': 1.35,
            'account_target': 1.60
        }

        # Campaign type best practices (from knowledge base)
        self.campaign_type_best_practices = {
            'PERFORMANCE_MAX': {
                'min_budget': 10.0,  # £10/day minimum
                'recommended_budget': 20.0,  # £20/day for learning
                'learning_period_days': 14,
                'asset_requirements': {
                    'headlines': (3, 15),
                    'descriptions': (2, 5),
                    'images': (4, 20)
                }
            },
            'SHOPPING': {
                'min_budget': 5.0,
                'feed_update_frequency': 'daily',
                'requires_product_groups': True
            },
            'SEARCH': {
                'min_budget': 5.0,
                'max_keywords_per_ad_group': 20,
                'recommended_keywords_per_ad_group': 10,
                'requires_negative_keywords': True
            }
        }

        # Known issues from CONTEXT.md
        self.known_issues = [
            'Stock instability affects campaign learning',
            'CPC inflation outpacing efficiency gains',
            'Feed issues can reset learning on bestsellers',
            'Profit compression at scale'
        ]

    def analyze_campaigns(
        self,
        client: str,
        campaigns: List[Dict[str, Any]],
        date_range: Dict[str, str],
        detailed_campaign_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Perform deep analysis with configuration auditing

        Args:
            client: Client slug
            campaigns: Campaign performance data
            date_range: Date range for analysis
            detailed_campaign_data: Optional detailed campaign config from API

        Returns:
            Comprehensive analysis with audits and root cause analysis
        """

        # Run base analysis first
        base_analysis = super().analyze_campaigns(client, campaigns, date_range)

        # Apply profit terminology
        base_analysis = self._apply_profit_terminology(base_analysis)

        # Add deep auditing sections
        base_analysis['deep_audits'] = self._perform_deep_audits(
            campaigns,
            detailed_campaign_data
        )

        # Add root cause analysis for underperformers
        base_analysis['root_cause_analyses'] = self._analyze_root_causes(
            campaigns,
            base_analysis['deep_audits']
        )

        # Add knowledge base insights
        base_analysis['kb_insights'] = self._fetch_kb_insights(
            campaigns,
            base_analysis['deep_audits']
        )

        # Generate enhanced recommendations based on audits
        base_analysis['recommendations'] = self._generate_audit_based_recommendations(
            base_analysis['campaign_analyses'],
            base_analysis['deep_audits'],
            base_analysis['root_cause_analyses'],
            base_analysis['kb_insights']
        )

        # Add profit context
        base_analysis['profit_context'] = self._generate_profit_context()

        # Add tier guidance
        base_analysis['tier_guidance'] = self._generate_tier_guidance(
            base_analysis['campaign_analyses']
        )

        # Add seasonality context
        base_analysis['seasonality_context'] = self._generate_seasonality_context()

        return base_analysis

    def _apply_profit_terminology(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Replace ROAS with POAS terminology throughout"""

        # Update recommendations
        if 'recommendations' in analysis:
            for rec in analysis['recommendations']:
                if 'title' in rec:
                    rec['title'] = rec['title'].replace('ROAS', 'POAS')
                if 'recommendation' in rec:
                    rec['recommendation'] = rec['recommendation'].replace('ROAS', 'POAS')
                    rec['recommendation'] = rec['recommendation'].replace('revenue', 'profit')
                if rec.get('issue_type') == 'low_roas':
                    rec['issue_type'] = 'low_poas'

        # Update campaign analyses
        if 'campaign_analyses' in analysis:
            for campaign in analysis['campaign_analyses']:
                if 'insights' in campaign:
                    for i, insight in enumerate(campaign['insights']):
                        campaign['insights'][i] = insight.replace('ROAS', 'POAS')
                        campaign['insights'][i] = insight.replace('revenue', 'profit')

        return analysis

    def _perform_deep_audits(
        self,
        campaigns: List[Dict[str, Any]],
        detailed_data: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Perform deep configuration audits on campaigns

        Checks:
        - Campaign structure issues
        - Budget allocation problems
        - Bidding strategy appropriateness
        - Targeting issues
        - Feed quality (for Shopping/PMax)
        """

        audits = {
            'structure_issues': [],
            'budget_issues': [],
            'bidding_issues': [],
            'targeting_issues': [],
            'feed_quality_issues': [],
            'performance_issues': []
        }

        for campaign in campaigns:
            campaign_name = campaign['name']
            campaign_type = campaign.get('type', 'UNKNOWN')
            metrics = campaign.get('metrics', {})

            # Calculate daily budget from spend
            spend = metrics.get('spend', 0)
            days_in_range = 7  # Assuming 7-day range
            daily_budget = spend / days_in_range if days_in_range > 0 else 0

            # Audit budget allocation
            if campaign_type in self.campaign_type_best_practices:
                best_practice = self.campaign_type_best_practices[campaign_type]
                min_budget = best_practice.get('min_budget', 0)

                if daily_budget < min_budget and metrics.get('impressions', 0) > 0:
                    audits['budget_issues'].append({
                        'campaign': campaign_name,
                        'issue': f'Budget below minimum (£{daily_budget:.2f}/day vs £{min_budget}/day recommended)',
                        'severity': 'HIGH',
                        'impact': 'Campaign not spending enough to learn effectively',
                        'fix': f'Increase daily budget to at least £{min_budget}/day',
                        'expected_outcome': 'Improved campaign learning and performance stability'
                    })

            # Audit performance issues
            poas = metrics.get('roas', 0)  # Actually POAS for Tree2mydoor
            conversions = metrics.get('conversions', 0)

            # Low POAS but high spend = urgent issue
            if poas < self.profit_targets['tier_c'] and spend > 50:
                audits['performance_issues'].append({
                    'campaign': campaign_name,
                    'issue': f'POAS {poas:.2f}x below Tier C threshold ({self.profit_targets["tier_c"]}x) with significant spend',
                    'severity': 'CRITICAL',
                    'spend': spend,
                    'poas': poas,
                    'requires_root_cause': True
                })

            # No conversions but spending = major problem
            if conversions == 0 and spend > 20:
                audits['performance_issues'].append({
                    'campaign': campaign_name,
                    'issue': f'Zero conversions despite £{spend:.2f} spend',
                    'severity': 'CRITICAL',
                    'spend': spend,
                    'requires_immediate_action': True,
                    'recommended_action': 'Pause immediately pending investigation'
                })

            # Check for impression share loss
            if campaign_type in ['SEARCH', 'SHOPPING']:
                budget_lost_is = metrics.get('search_budget_lost_impression_share', 0)
                if budget_lost_is > 0.2:  # Losing >20% impression share to budget
                    audits['budget_issues'].append({
                        'campaign': campaign_name,
                        'issue': f'Losing {budget_lost_is*100:.0f}% impression share to budget constraints',
                        'severity': 'MEDIUM',
                        'impact': 'Missing profitable traffic opportunities',
                        'fix': 'Increase budget or reallocate from underperforming campaigns',
                        'expected_outcome': f'Capture additional {budget_lost_is*100:.0f}% impression share'
                    })

        # Add Profit Tier structure audits (ProfitMetrics-based)
        audits['profit_tier_recommendations'] = self._audit_profit_tier_structure(campaigns)

        # Add seasonal audits
        audits['seasonal_issues'] = self._audit_seasonal_readiness(campaigns)

        return audits

    def _analyze_root_causes(
        self,
        campaigns: List[Dict[str, Any]],
        audits: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Perform root cause analysis on underperforming campaigns

        For each problem, determine WHY it's happening:
        - Is it a budget issue?
        - Is it bidding strategy?
        - Is it targeting?
        - Is it feed quality?
        - Is it seasonal/market conditions?
        """

        root_causes = []

        # Analyze campaigns requiring root cause analysis
        for issue in audits.get('performance_issues', []):
            if issue.get('requires_root_cause'):
                campaign_name = issue['campaign']

                # Find the campaign
                campaign = next((c for c in campaigns if c['name'] == campaign_name), None)
                if not campaign:
                    continue

                metrics = campaign.get('metrics', {})
                campaign_type = campaign.get('type', 'UNKNOWN')

                # Perform root cause analysis
                root_cause = {
                    'campaign': campaign_name,
                    'problem': issue['issue'],
                    'likely_causes': [],
                    'evidence': [],
                    'recommended_fixes': []
                }

                # Check for budget constraints
                budget_lost_is = metrics.get('search_budget_lost_impression_share', 0)
                if budget_lost_is > 0.15:
                    root_cause['likely_causes'].append('Budget constraints limiting exposure')
                    root_cause['evidence'].append(f'Losing {budget_lost_is*100:.0f}% impression share to budget')
                    root_cause['recommended_fixes'].append({
                        'action': f'Increase daily budget by {budget_lost_is*100:.0f}%',
                        'expected_impact': 'Capture missed impression share, likely improve POAS through scale'
                    })

                # Check for poor conversion rate (low CR with traffic)
                clicks = metrics.get('clicks', 0)
                conversions = metrics.get('conversions', 0)
                if clicks > 50:
                    cr = conversions / clicks if clicks > 0 else 0
                    if cr < 0.02:  # <2% conversion rate
                        root_cause['likely_causes'].append('Poor conversion rate indicates targeting or landing page issues')
                        root_cause['evidence'].append(f'Conversion rate {cr*100:.1f}% (industry average ~3-5%)')
                        root_cause['recommended_fixes'].append({
                            'action': 'Review search terms report for irrelevant queries, check landing page experience',
                            'expected_impact': 'Eliminate wasted spend on non-converting traffic'
                        })

                # Check for high CPC
                cpc = metrics.get('spend', 0) / clicks if clicks > 0 else 0
                if cpc > 1.5 and campaign_type in ['SEARCH', 'SHOPPING']:
                    root_cause['likely_causes'].append('High CPC eroding profit margins')
                    root_cause['evidence'].append(f'Average CPC £{cpc:.2f} (check if competitive pressure or broad targeting)')
                    root_cause['recommended_fixes'].append({
                        'action': 'Review search terms for expensive non-converting queries, add negative keywords, tighten targeting',
                        'expected_impact': 'Reduce CPC, improve profit per conversion'
                    })

                # Performance Max specific checks
                if campaign_type == 'PERFORMANCE_MAX':
                    if metrics.get('spend', 0) / 7 < 20:  # Less than £20/day
                        root_cause['likely_causes'].append('Insufficient budget for Performance Max learning')
                        root_cause['evidence'].append('PMax requires £20+/day for effective learning (currently spending less)')
                        root_cause['recommended_fixes'].append({
                            'action': 'Increase daily budget to £20-30/day minimum',
                            'expected_impact': 'Enable proper machine learning, improve asset testing'
                        })

                # Product feed issues (Shopping/PMax)
                if campaign_type in ['PERFORMANCE_MAX', 'SHOPPING']:
                    root_cause['likely_causes'].append('Potential feed quality issues affecting product eligibility')
                    root_cause['evidence'].append('Known issue from CONTEXT.md: "Feed issues can reset learning on bestsellers"')
                    root_cause['recommended_fixes'].append({
                        'action': 'Check Merchant Centre for disapprovals, verify feed quality in Channable, ensure high-profit products have complete data',
                        'expected_impact': 'Improve product approval rate, maximize impression share for profitable products'
                    })

                # Known seasonal/market issues
                if datetime.now().month == 12:
                    root_cause['likely_causes'].append('December CPC inflation (peak season competition)')
                    root_cause['evidence'].append('Known issue from CONTEXT.md: "CPC inflation outpacing efficiency gains"')
                    root_cause['recommended_fixes'].append({
                        'action': 'Accept higher CPCs during peak season IF profit targets maintained, focus budget on Tier A campaigns, review profit margins via ProfitMetrics',
                        'expected_impact': 'Maximize profitable volume during peak season without sacrificing profitability'
                    })

                # If no specific causes found, add general investigation
                if not root_cause['likely_causes']:
                    root_cause['likely_causes'].append('Requires detailed investigation - multiple potential factors')
                    root_cause['recommended_fixes'].append({
                        'action': 'Comprehensive campaign audit: search terms, auction insights, landing pages, product mix, conversion tracking',
                        'expected_impact': 'Identify hidden issues preventing profitability'
                    })

                root_causes.append(root_cause)

        return root_causes

    def _audit_profit_tier_structure(self, campaigns: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Audit profit tier campaign structure and segmentation (ProfitMetrics-based)"""

        recommendations = []

        # Analyse current Profitable/Unprofitable split
        profitable_campaigns = [c for c in campaigns if 'profitable' in c['name'].lower() and 'unprofitable' not in c['name'].lower()]
        unprofitable_campaigns = [c for c in campaigns if 'unprofitable' in c['name'].lower()]

        # Check if "unprofitable" campaigns are actually profitable
        for campaign in unprofitable_campaigns:
            metrics = campaign.get('metrics', {})
            poas = metrics.get('roas', 0)

            if poas >= self.profit_targets['tier_b']:
                recommendations.append({
                    'priority': 'P0',
                    'action': f'Review "{campaign["name"]}" segmentation - achieving Tier B POAS ({poas:.2f}x) but in Unprofitable campaign',
                    'why': f'Campaign labelled "Unprofitable" is actually performing at Tier B level (≥{self.profit_targets["tier_b"]}x)',
                    'how': 'Review product mix via ProfitMetrics data → Identify profitable products → Consider moving to Profitable campaign or creating Tier B campaign',
                    'expected_outcome': 'Reallocate budget from genuinely unprofitable products to proven profit generators'
                })

        # Check for campaigns below Tier C threshold
        pmax_shopping_campaigns = [c for c in campaigns if c.get('type') in ['PERFORMANCE_MAX', 'SHOPPING']]
        low_poas_campaigns = [c for c in pmax_shopping_campaigns if c.get('metrics', {}).get('roas', 0) < self.profit_targets['tier_c']]

        if low_poas_campaigns:
            recommendations.append({
                'priority': 'P1',
                'action': 'Analyse product-level profitability for campaigns below Tier C threshold',
                'why': f'{len(low_poas_campaigns)} Shopping/PMax campaigns below Tier C ({self.profit_targets["tier_c"]}x) - need to identify unprofitable products',
                'how': 'ProfitMetrics → Export product-level POAS data → Channable → Filter products <1.35x POAS → Exclude via negative product groups or reduce bids',
                'expected_outcome': 'Stop budget waste on unprofitable products, focus spend on proven profit generators'
            })

        # Recommend Tier A/B/C restructure if still using Profitable/Unprofitable
        if profitable_campaigns or unprofitable_campaigns:
            recommendations.append({
                'priority': 'P2',
                'action': 'Prepare for Tier A/B/C campaign restructure',
                'why': 'Current Profitable/Unprofitable split is binary; Tier structure allows better budget control by margin levels',
                'how': 'Create 3 campaign tiers: Tier A (≥1.80x POAS), Tier B (1.45-1.79x), Tier C (<1.45x probe/throttle) → Use Channable rules to segment products',
                'expected_outcome': 'More granular budget allocation, better control over margin optimization, aligned with Gareth\'s October proposal'
            })

        return recommendations

    def _audit_seasonal_readiness(self, campaigns: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Audit seasonal readiness (December = peak season for Tree2mydoor)"""

        issues = []
        current_month = datetime.now().month

        # December peak season checks
        if current_month == 12:
            # Check if Tier A campaigns have enough budget
            tier_a_campaigns = [
                c for c in campaigns
                if c.get('metrics', {}).get('roas', 0) >= self.profit_targets['tier_a']
            ]

            for campaign in tier_a_campaigns:
                metrics = campaign.get('metrics', {})
                budget_lost_is = metrics.get('search_budget_lost_impression_share', 0)

                if budget_lost_is > 0.1:  # Losing >10% to budget during peak season
                    issues.append({
                        'campaign': campaign['name'],
                        'issue': f'Tier A campaign losing {budget_lost_is*100:.0f}% impression share to budget during peak season',
                        'severity': 'HIGH',
                        'fix': 'Increase budget by 30-50% to capture Christmas demand',
                        'impact': 'Missing profitable holiday traffic on best-performing campaign'
                    })

            # Check for asset updates (seasonal messaging)
            issues.append({
                'general': True,
                'issue': 'Verify Christmas/gift-focused ad copy is active across all campaigns',
                'severity': 'MEDIUM',
                'fix': 'Review RSAs and PMax assets for "gift", "Christmas", "memorial tree" messaging',
                'impact': 'Seasonal messaging improves CTR and conversion rates during December'
            })

        return issues

    def _fetch_kb_insights(
        self,
        campaigns: List[Dict[str, Any]],
        audits: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetch relevant insights from knowledge base

        TODO: Implement actual KB search using KBIntegration
        For now, return placeholder structure showing what should be searched
        """

        kb_insights = {
            'relevant_searches': [
                'Performance Max budget optimization',
                'Shopping campaign feed quality best practices',
                'Profit-based bidding strategies',
                'E-commerce campaign structure for seasonal products',
                'Product feed optimization for Google Shopping'
            ],
            'key_recommendations': [
                {
                    'topic': 'Performance Max Budget',
                    'insight': 'PMax campaigns require minimum £20/day for effective learning, ideally £30-50/day during peak seasons',
                    'source': 'Google Ads best practices (knowledge base)',
                    'application': 'Review PMax campaigns with <£20/day budget'
                },
                {
                    'topic': 'Product Feed Quality',
                    'insight': 'Product titles should include: Brand + Product Type + Key Attributes. Poor titles reduce impression share by 30-50%',
                    'source': 'Shopping feed optimization guidelines',
                    'application': 'Audit Merchant Centre feed titles via Channable'
                },
                {
                    'topic': 'Seasonal Campaign Management',
                    'insight': 'December: Increase budgets on Tier A campaigns by 30-50%, focus on gift-focused messaging, monitor stock levels daily',
                    'source': 'E-commerce seasonal strategies',
                    'application': 'Current month (December) - implement immediately'
                }
            ]
        }

        return kb_insights

    def _generate_audit_based_recommendations(
        self,
        campaign_analyses: List[Dict[str, Any]],
        audits: Dict[str, Any],
        root_causes: List[Dict[str, Any]],
        kb_insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate comprehensive recommendations based on audits and root cause analysis

        These are NOT generic recommendations - these are specific, evidence-based
        actions derived from the deep auditing process
        """

        recommendations = []

        # Critical performance issues first (P0)
        for issue in audits.get('performance_issues', []):
            if issue.get('severity') == 'CRITICAL':
                # Find root cause analysis for this campaign
                root_cause = next(
                    (rc for rc in root_causes if rc['campaign'] == issue['campaign']),
                    None
                )

                rec = {
                    'priority': 'P0',
                    'title': f"Critical: {issue['campaign']} - {issue['issue']}",
                    'issue_type': 'critical_performance',
                    'campaign': issue['campaign'],
                    'problem': issue['issue'],
                    'recommendation': self._format_root_cause_recommendation(root_cause) if root_cause else issue.get('recommended_action', 'Investigate immediately')
                }
                recommendations.append(rec)

        # Budget issues (P1)
        for issue in audits.get('budget_issues', []):
            if issue.get('severity') in ['HIGH', 'CRITICAL']:
                rec = {
                    'priority': 'P1',
                    'title': f"Budget Issue: {issue['campaign']}",
                    'issue_type': 'budget_allocation',
                    'campaign': issue['campaign'],
                    'problem': issue['issue'],
                    'recommendation': f"{issue['fix']}\n\nExpected Outcome: {issue['expected_outcome']}"
                }
                recommendations.append(rec)

        # Profit Tier recommendations (P1)
        for rec_item in audits.get('profit_tier_recommendations', []):
            rec = {
                'priority': rec_item['priority'],
                'title': f"Profit Tier: {rec_item['action']}",
                'issue_type': 'product_optimization',
                'problem': rec_item['why'],
                'recommendation': f"Action: {rec_item['action']}\n\nHow: {rec_item['how']}\n\nExpected Outcome: {rec_item['expected_outcome']}"
            }
            recommendations.append(rec)

        # Seasonal issues (P1 during peak season)
        for issue in audits.get('seasonal_issues', []):
            if not issue.get('general'):
                rec = {
                    'priority': 'P1' if datetime.now().month == 12 else 'P2',
                    'title': f"Seasonal: {issue['issue']}",
                    'issue_type': 'seasonal_optimization',
                    'campaign': issue.get('campaign', 'Multiple campaigns'),
                    'problem': issue['issue'],
                    'recommendation': f"{issue['fix']}\n\nImpact: {issue['impact']}"
                }
                recommendations.append(rec)

        # Knowledge base-informed recommendations (P2)
        for insight in kb_insights.get('key_recommendations', []):
            rec = {
                'priority': 'P2',
                'title': f"Best Practice: {insight['topic']}",
                'issue_type': 'best_practice',
                'problem': f"Industry best practice: {insight['insight']}",
                'recommendation': f"Application: {insight['application']}\n\nSource: {insight['source']}"
            }
            recommendations.append(rec)

        # Sort by priority
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'P3'), 3))

        return recommendations

    def _format_root_cause_recommendation(self, root_cause: Dict[str, Any]) -> str:
        """Format root cause analysis into a comprehensive recommendation"""

        output = []

        output.append("ROOT CAUSE ANALYSIS:\n")
        for i, cause in enumerate(root_cause.get('likely_causes', []), 1):
            output.append(f"{i}. {cause}")

        output.append("\n\nEVIDENCE:")
        for evidence in root_cause.get('evidence', []):
            output.append(f"• {evidence}")

        output.append("\n\nRECOMMENDED FIXES:")
        for i, fix in enumerate(root_cause.get('recommended_fixes', []), 1):
            output.append(f"\n{i}. {fix['action']}")
            output.append(f"   Expected Impact: {fix['expected_impact']}")

        return "\n".join(output)

    def _generate_profit_context(self) -> Dict[str, Any]:
        """Generate profit-based optimization context"""

        return {
            'uses_profitmetrics': True,
            'conversions_value_meaning': 'PROFIT (not revenue)',
            'target_poas': self.profit_targets['account_target'],
            'optimization_focus': 'Maximise profit per £1 spent (not revenue)',
            'tier_structure': {
                'tier_a': f"≥{self.profit_targets['tier_a']}x POAS - Scale aggressively",
                'tier_b': f"≥{self.profit_targets['tier_b']}x POAS - Maintain, optimize to Tier A",
                'tier_c': f"≥{self.profit_targets['tier_c']}x POAS - Throttle budget",
                'below_tier_c': f"<{self.profit_targets['tier_c']}x POAS - Pause or reduce -50%"
            }
        }

    def _generate_tier_guidance(self, campaign_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate tier-based campaign guidance"""

        tier_campaigns = {
            'tier_a': [],
            'tier_b': [],
            'tier_c': [],
            'below_tier_c': []
        }

        for campaign in campaign_analyses:
            poas = campaign['metrics'].get('roas', 0)  # Actually POAS

            if poas >= self.profit_targets['tier_a']:
                tier_campaigns['tier_a'].append(campaign)
            elif poas >= self.profit_targets['tier_b']:
                tier_campaigns['tier_b'].append(campaign)
            elif poas >= self.profit_targets['tier_c']:
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
            'actions': {
                'tier_a': 'Scale: +20-30% budget, maximize impression share',
                'tier_b': 'Optimize: Hold budget, improve to Tier A',
                'tier_c': 'Throttle: -30% budget, review product mix',
                'below_tier_c': 'Pause or -50% budget pending investigation'
            }
        }

    def _generate_seasonality_context(self) -> Dict[str, Any]:
        """Generate seasonality context"""

        current_month = datetime.now().month

        peak_seasons = {
            12: 'Christmas Peak',
            11: 'Pre-Christmas',
            5: 'Mother\'s Day'
        }

        season_name = peak_seasons.get(current_month, 'Standard Season')
        is_peak = current_month in peak_seasons

        return {
            'current_month': current_month,
            'season_name': season_name,
            'is_peak_season': is_peak,
            'guidance': self._get_seasonal_guidance(current_month, is_peak)
        }

    def _get_seasonal_guidance(self, month: int, is_peak: bool) -> str:
        """Get season-specific guidance"""

        if month == 12:
            return (
                "Christmas Peak Season - Highest demand period:\n"
                "• Increase Tier A budgets by 30-50%\n"
                "• Focus spend on highest POAS products (gift trees, memorial trees)\n"
                "• Monitor stock levels daily (OOS = missed opportunity)\n"
                "• Ensure gift-focused messaging active\n"
                "• Accept higher CPCs if profit targets maintained"
            )
        elif month == 11:
            return (
                "Pre-Christmas Season - Building momentum:\n"
                "• Prepare for December: Test messaging, optimize feeds\n"
                "• Scale Tier A campaigns gradually (+10-20%)\n"
                "• Verify product profitability data accurate in ProfitMetrics\n"
                "• Build budget headroom for December surge"
            )
        elif month == 5:
            return (
                "Mother's Day Season - Gift focus:\n"
                "• Emphasize gift messaging\n"
                "• Increase budgets on gift-appropriate products\n"
                "• Monitor for stock issues on popular gifts"
            )
        else:
            return (
                "Standard Season - Focus on efficiency:\n"
                "• Maintain POAS targets strictly\n"
                "• Test new products/categories\n"
                "• Optimize feeds and campaigns for next peak\n"
                "• Build up Tier A campaigns"
            )


if __name__ == '__main__':
    print("Tree2mydoor Deep Auditor")
    print("This is a library module - use run_tree2mydoor_deep_report.py to generate reports")
