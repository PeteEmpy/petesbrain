"""
Campaign Analyzer Core

Analyzes Google Ads campaign performance and generates intelligent recommendations
using client context and Knowledge Base insights.

PHASE 1: Campaign-level performance analysis
- ROAS analysis (vs targets)
- Budget efficiency (Lost IS Budget)
- Spend pattern analysis
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from context_parser import ClientContextParser
from kb_integration import KBIntegration
from product_analyzer import ProductAnalyzer

logger = logging.getLogger(__name__)


class CampaignAnalyzer:
    """Analyzes campaign performance with context-aware recommendations"""

    def __init__(self):
        """Initialize analyzer with context parser, KB integration, and product analyzer"""
        self.context_parser = ClientContextParser()
        self.kb = KBIntegration()
        self.product_analyzer = ProductAnalyzer()

    def analyze_campaigns(
        self,
        client_slug: str,
        campaign_data: List[Dict[str, Any]],
        date_range: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Analyze campaigns for a client

        Args:
            client_slug: Client identifier (e.g., 'smythson', 'tree2mydoor')
            campaign_data: List of campaign performance dicts with metrics
            date_range: Dict with 'start_date' and 'end_date'

        Returns:
            Comprehensive analysis with issues, recommendations, and summary
        """
        logger.info(f"Analyzing {len(campaign_data)} campaigns for {client_slug}")

        # Load client context
        client_context = self.context_parser.load_client_context(client_slug)
        if not client_context:
            logger.warning(f"No context found for {client_slug} - using generic analysis")
            client_context = {'client_slug': client_slug}

        # Analyze each campaign
        campaign_analyses = []
        all_issues = []

        for campaign in campaign_data:
            analysis = self._analyze_single_campaign(campaign, client_context)
            campaign_analyses.append(analysis)
            all_issues.extend(analysis.get('issues', []))

        # Run product analysis for e-commerce clients
        product_analysis = None
        if self._is_ecommerce_client(client_context, campaign_data):
            logger.info(f"Running product analysis for e-commerce client {client_slug}")
            target_roas = client_context.get('performance_targets', {}).get('target_roas', 3.0)

            try:
                product_analysis = self.product_analyzer.analyze_products(
                    client_slug=client_slug,
                    campaign_data=campaign_data,
                    date_range=date_range,
                    target_roas=target_roas
                )

                # Integrate product issues into overall issues list
                if product_analysis and product_analysis.get('product_issues'):
                    all_issues.extend(product_analysis['product_issues'])
                    logger.info(f"Added {len(product_analysis['product_issues'])} product-level issues")
            except Exception as e:
                logger.warning(f"Product analysis failed: {e}")
                product_analysis = {'error': str(e), 'total_products': 0}

        # Generate prioritized recommendations (now includes product issues)
        recommendations = self._generate_recommendations(all_issues, client_context)

        # Calculate account health score (now includes product issues)
        health_score = self._calculate_health_score(campaign_analyses, all_issues)

        # Build result
        result = {
            'client_slug': client_slug,
            'date_range': date_range,
            'health_score': health_score,
            'summary': self._generate_summary(campaign_analyses, health_score, product_analysis),
            'campaign_analyses': campaign_analyses,
            'recommendations': recommendations,
            'context_applied': {
                'target_roas': client_context.get('performance_targets', {}).get('target_roas'),
                'known_issues_count': len(client_context.get('known_issues', [])),
                'uses_product_hero': client_context.get('strategic_approach', {}).get('uses_product_hero', False)
            }
        }

        # Add product analysis if available
        if product_analysis:
            result['product_analysis'] = product_analysis

        return result

    def _is_ecommerce_client(self, client_context: Dict, campaign_data: List[Dict]) -> bool:
        """Determine if client is e-commerce based on context and campaign types"""
        # Check if client has Shopping or Performance Max campaigns
        has_shopping_campaigns = any(
            c.get('advertising_channel_type') in ['SHOPPING', 'PERFORMANCE_MAX']
            for c in campaign_data
        )

        # Check if client context indicates e-commerce
        platform = client_context.get('platform_information', {}).get('platform', '').lower()
        is_ecommerce_platform = platform in ['shopify', 'woocommerce', 'magento', 'bigcommerce']

        return has_shopping_campaigns or is_ecommerce_platform

    def _analyze_single_campaign(
        self,
        campaign: Dict[str, Any],
        client_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a single campaign

        Args:
            campaign: Campaign data with metrics
            client_context: Parsed client context

        Returns:
            Analysis dict with issues and metrics
        """
        campaign_name = campaign.get('name', 'Unknown')
        metrics = campaign.get('metrics', {})

        issues = []

        # Extract metrics (convert from micros if needed)
        spend = metrics.get('cost_micros', 0) / 1_000_000
        revenue = metrics.get('conversions_value_micros', metrics.get('conversions_value', 0))
        if revenue > 1_000_000:  # Likely in micros
            revenue = revenue / 1_000_000
        conversions = metrics.get('conversions', 0)

        # Calculate ROAS
        roas = revenue / spend if spend > 0 else 0

        # Get client-specific target
        target_roas = self.context_parser.get_applicable_threshold(
            client_context,
            'roas'
        )

        # Issue Detection: Low ROAS
        if target_roas and spend > 0:
            roas_gap_pct = ((target_roas - roas) / target_roas) * 100
            if roas < target_roas * 0.8:  # Below 80% of target
                issue = {
                    'type': 'low_roas',
                    'severity': 'P1' if roas < target_roas * 0.6 else 'P2',
                    'campaign': campaign_name,
                    'description': f"ROAS {roas:.2f}x is {roas_gap_pct:.0f}% below target {target_roas}x",
                    'metrics': {
                        'actual_roas': roas,
                        'target_roas': target_roas,
                        'gap_percentage': roas_gap_pct,
                        'spend': spend,
                        'revenue': revenue
                    }
                }

                # Check if this is a known issue
                if not self.context_parser.should_ignore_issue(
                    client_context,
                    f"low ROAS {campaign_name}"
                ):
                    issues.append(issue)
                else:
                    logger.info(f"Ignoring known issue: Low ROAS in {campaign_name}")

        # Issue Detection: Budget Constraints (Lost IS Budget)
        lost_is_budget = metrics.get('search_lost_impression_share_budget', 0)
        if lost_is_budget > 0.10:  # >10% lost impression share
            issue = {
                'type': 'budget_constraint',
                'severity': 'P1' if lost_is_budget > 0.25 else 'P2',
                'campaign': campaign_name,
                'description': f"Losing {lost_is_budget*100:.0f}% of impressions due to budget",
                'metrics': {
                    'lost_is_budget': lost_is_budget,
                    'spend': spend,
                    'roas': roas
                }
            }

            if not self.context_parser.should_ignore_issue(
                client_context,
                f"budget constraint {campaign_name}"
            ):
                issues.append(issue)

        # Issue Detection: High Spend, Low Performance
        if spend > 100 and roas < 1.0:  # Spending >£100 but not breaking even
            issue = {
                'type': 'high_spend_low_performance',
                'severity': 'P0' if spend > 500 else 'P1',
                'campaign': campaign_name,
                'description': f"£{spend:.0f} spend with {roas:.2f}x ROAS (not profitable)",
                'metrics': {
                    'spend': spend,
                    'roas': roas,
                    'revenue': revenue,
                    'loss': spend - revenue
                }
            }

            if not self.context_parser.should_ignore_issue(
                client_context,
                f"unprofitable {campaign_name}"
            ):
                issues.append(issue)

        # Issue Detection: Zero Conversions with Spend
        if spend > 50 and conversions == 0:
            issue = {
                'type': 'zero_conversions',
                'severity': 'P1',
                'campaign': campaign_name,
                'description': f"£{spend:.0f} spend but zero conversions",
                'metrics': {
                    'spend': spend,
                    'conversions': conversions,
                    'clicks': metrics.get('clicks', 0),
                    'impressions': metrics.get('impressions', 0)
                }
            }

            if not self.context_parser.should_ignore_issue(
                client_context,
                f"zero conversions {campaign_name}"
            ):
                issues.append(issue)

        return {
            'campaign_name': campaign_name,
            'campaign_id': campaign.get('id'),
            'campaign_type': campaign.get('advertising_channel_type', 'Unknown'),
            'status': campaign.get('status', 'Unknown'),
            'metrics': {
                'spend': spend,
                'revenue': revenue,
                'roas': roas,
                'conversions': conversions,
                'clicks': metrics.get('clicks', 0),
                'impressions': metrics.get('impressions', 0),
                'lost_is_budget': lost_is_budget
            },
            'issues': issues,
            'target_roas': target_roas
        }

    def _generate_recommendations(
        self,
        issues: List[Dict[str, Any]],
        client_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate prioritized recommendations with KB insights

        Args:
            issues: List of detected issues
            client_context: Client context data

        Returns:
            Prioritized list of recommendations
        """
        recommendations = []

        # Group issues by type
        issues_by_type = {}
        for issue in issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # Generate recommendations for each issue type
        for issue_type, type_issues in issues_by_type.items():
            # Sort by severity
            type_issues.sort(key=lambda x: x['severity'])

            # Get KB insights for this issue type
            kb_articles = self._get_kb_insights_for_issue(issue_type, client_context)

            # Create recommendation
            rec = self._create_recommendation(
                issue_type,
                type_issues,
                kb_articles,
                client_context
            )

            if rec:
                recommendations.append(rec)

        # Sort recommendations by priority
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 99))

        return recommendations

    def _get_kb_insights_for_issue(
        self,
        issue_type: str,
        client_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get relevant KB articles for an issue type"""

        # Map issue types to search queries
        issue_queries = {
            'low_roas': ('Performance Max', 'low ROAS improvement'),
            'budget_constraint': ('Google Ads', 'budget optimization lost impression share'),
            'high_spend_low_performance': ('campaign', 'unprofitable high cost optimization'),
            'zero_conversions': ('conversion tracking', 'setup verification')
        }

        if issue_type not in issue_queries:
            return []

        campaign_type, issue_desc = issue_queries[issue_type]

        # Search KB
        articles = self.kb.search_optimization_insights(
            campaign_type,
            issue_desc,
            limit=3
        )

        return articles

    def _create_recommendation(
        self,
        issue_type: str,
        issues: List[Dict[str, Any]],
        kb_articles: List[Dict[str, Any]],
        client_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a structured recommendation"""

        if not issues:
            return None

        # Get highest priority issue
        highest_priority = issues[0]['severity']

        # Count affected campaigns
        affected_campaigns = len(issues)

        # Calculate total impact
        total_spend = sum(i['metrics'].get('spend', 0) for i in issues)
        avg_roas = sum(i['metrics'].get('roas', 0) for i in issues) / len(issues) if issues else 0

        # Generate recommendation text based on issue type
        rec_text = self._generate_recommendation_text(
            issue_type,
            issues,
            client_context
        )

        # Build recommendation
        recommendation = {
            'priority': highest_priority,
            'issue_type': issue_type,
            'title': self._get_issue_title(issue_type),
            'affected_campaigns': affected_campaigns,
            'campaign_names': [i['campaign'] for i in issues],
            'impact': {
                'total_spend': total_spend,
                'avg_roas': avg_roas
            },
            'recommendation': rec_text,
            'kb_articles': kb_articles,
            'next_steps': self._get_next_steps(issue_type, issues, client_context)
        }

        return recommendation

    def _generate_recommendation_text(
        self,
        issue_type: str,
        issues: List[Dict[str, Any]],
        client_context: Dict[str, Any]
    ) -> str:
        """Generate recommendation text for an issue type"""

        templates = {
            'low_roas': """ROAS Performance Below Target

{count} campaign(s) are performing below the target ROAS of {target}x. This represents £{spend:.0f} in spend generating {roas:.2f}x average return.

Root Cause Analysis:
- Campaign efficiency is {gap:.0f}% below target
- May indicate bidding strategy misalignment, poor product/ad relevance, or targeting issues

Recommendation:
1. Review bidding strategy - consider adjusting Target ROAS or switching to Maximize Conversion Value
2. Analyse Search Terms report for wasted spend on irrelevant queries
3. Review product feed quality (if Shopping/PMax) - ensure titles, descriptions optimised
4. Check audience targeting for efficiency opportunities""",

            'budget_constraint': """Budget Constraints Limiting Performance

{count} campaign(s) are losing impressions due to budget constraints (avg {lost_is:.0f}% Lost IS Budget).

Root Cause Analysis:
- Campaigns are performing well but can't spend more due to daily budget caps
- Potential revenue being left on the table

Recommendation:
1. Assess performance: Campaigns with ROAS >{min_roas:.2f}x should receive budget increases
2. Reallocate budget from lower-performing campaigns
3. Consider increasing overall account budget if all campaigns are constrained
4. Monitor pacing - ensure budgets aren't exhausted early in the day""",

            'high_spend_low_performance': """High Spend, Low Performance Campaigns

{count} campaign(s) with significant spend (£{spend:.0f} total) are underperforming at {roas:.2f}x ROAS.

Root Cause Analysis:
- Campaigns are not profitable - spending more than revenue generated
- This is a critical waste of budget

Recommendation:
1. IMMEDIATE: Pause or reduce budgets for campaigns with ROAS <1.0x
2. Diagnose: Review Search Terms, Placements, Audience targeting for waste
3. Test: If pausing isn't an option, create tightly controlled test with lower budget
4. Consider: If consistently unprofitable, campaign may not be viable for this business""",

            'zero_conversions': """Zero Conversions Despite Spend

{count} campaign(s) have spent £{spend:.0f} but generated zero conversions.

Root Cause Analysis:
- Either conversion tracking is broken, or campaigns aren't driving valuable actions
- Need to diagnose tracking vs performance issue

Recommendation:
1. VERIFY TRACKING: Check Google Ads conversion tracking is firing correctly
2. Review Google Tag Assistant / Preview mode to confirm tracking implementation
3. Check conversion action settings - ensure they're set to "Primary" and "Include in Conversions"
4. If tracking is correct, review campaign targeting and landing page relevance"""
        }

        template = templates.get(issue_type, "Issue detected: {count} campaigns affected")

        # Calculate template variables
        count = len(issues)
        total_spend = sum(i['metrics'].get('spend', 0) for i in issues)
        avg_roas = sum(i['metrics'].get('roas', 0) for i in issues) / count if count > 0 else 0

        target_roas = client_context.get('performance_targets', {}).get('target_roas', 0)
        if target_roas and avg_roas:
            gap = ((target_roas - avg_roas) / target_roas) * 100
        else:
            gap = 0

        lost_is = sum(i['metrics'].get('lost_is_budget', 0) for i in issues) / count if count > 0 else 0

        # Generate campaign breakdown with specific details
        campaign_breakdown = self._generate_campaign_breakdown(issues, issue_type, target_roas)

        base_text = template.format(
            count=count,
            spend=total_spend,
            roas=avg_roas,
            target=target_roas,
            gap=gap,
            lost_is=lost_is * 100,
            min_roas=round(target_roas * 0.8, 2) if target_roas else 1.5
        )

        # Append campaign breakdown
        return f"{base_text}\n\n{campaign_breakdown}"

    def _generate_campaign_breakdown(
        self,
        issues: List[Dict[str, Any]],
        issue_type: str,
        target_roas: float
    ) -> str:
        """Generate detailed campaign breakdown with specific metrics and actions"""

        if not issues:
            return ""

        breakdown = "Affected Campaigns (Worst First):\n"

        # Sort by severity (worst first)
        sorted_issues = sorted(issues, key=lambda x: x['metrics'].get('spend', 0), reverse=True)

        # Limit to top 10 for readability
        top_issues = sorted_issues[:10]

        for i, issue in enumerate(top_issues, 1):
            campaign_name = issue.get('campaign', 'Unknown')
            metrics = issue.get('metrics', {})

            spend = metrics.get('spend', 0)
            revenue = metrics.get('revenue', 0)
            roas = metrics.get('actual_roas', metrics.get('roas', 0))  # Try actual_roas first, fallback to roas
            conversions = metrics.get('conversions', 0)
            lost_is = metrics.get('lost_is_budget', 0)

            # Generate specific action based on issue type and metrics
            action = self._get_campaign_action(issue_type, metrics, target_roas)

            breakdown += f"\n{i}. {campaign_name}\n"
            breakdown += f"   Spend: £{spend:.2f} | Revenue: £{revenue:.2f} | ROAS: {roas:.2f}x | Conv: {conversions:.0f}"

            if issue_type == 'budget_constraint':
                breakdown += f" | Lost IS: {lost_is*100:.0f}%"

            breakdown += f"\n   → ACTION: {action}\n"

        if len(sorted_issues) > 10:
            remaining = len(sorted_issues) - 10
            breakdown += f"\n... and {remaining} more campaigns with similar issues"

        return breakdown

    def _get_campaign_action(self, issue_type: str, metrics: Dict[str, Any], target_roas: float) -> str:
        """Generate specific action for a campaign based on issue type and metrics"""

        spend = metrics.get('spend', 0)
        roas = metrics.get('actual_roas', metrics.get('roas', 0))  # Try actual_roas first, fallback to roas
        conversions = metrics.get('conversions', 0)
        lost_is = metrics.get('lost_is_budget', 0)

        if issue_type == 'low_roas':
            if roas < 1.0:
                return f"PAUSE immediately - losing money (ROAS {roas:.2f}x < 1.0x)"
            elif roas < target_roas * 0.5:
                return f"Reduce budget by 50% and review Search Terms for waste"
            else:
                return f"Adjust Target ROAS to {target_roas * 0.9:.2f}x and monitor for 7 days"

        elif issue_type == 'high_spend_low_performance':
            return f"PAUSE campaign - spending £{spend:.2f} at unprofitable {roas:.2f}x ROAS"

        elif issue_type == 'budget_constraint':
            if roas > target_roas:
                revenue_opportunity = (lost_is * spend) / (1 - lost_is) * roas if lost_is < 1 else 0
                return f"Increase budget by 20% - losing £{revenue_opportunity:.0f}/week in potential revenue"
            else:
                return f"Monitor - constrained but ROAS below target ({roas:.2f}x vs {target_roas:.2f}x)"

        elif issue_type == 'zero_conversions':
            if spend > 50:
                return f"PAUSE - £{spend:.2f} spent with 0 conversions (check tracking first)"
            else:
                return "Review conversion tracking setup before taking action"

        return "Review campaign performance and adjust"

    def _get_issue_title(self, issue_type: str) -> str:
        """Get human-readable title for issue type"""
        titles = {
            'low_roas': 'Low ROAS Performance',
            'budget_constraint': 'Budget Constraints',
            'high_spend_low_performance': 'High Spend, Low Performance',
            'zero_conversions': 'Zero Conversions'
        }
        return titles.get(issue_type, issue_type.replace('_', ' ').title())

    def _get_next_steps(
        self,
        issue_type: str,
        issues: List[Dict[str, Any]],
        client_context: Dict[str, Any]
    ) -> List[str]:
        """Get actionable next steps for an issue"""

        # Calculate metrics for data-driven steps
        total_spend = sum(i['metrics'].get('spend', 0) for i in issues)

        if issue_type == 'low_roas':
            steps = [
                "Review Search Terms report for last 30 days (focus on campaigns listed above)",
                "Check Quality Score for keywords <7 in underperforming campaigns",
                "Analyse landing page relevance and conversion rate for worst performers",
                "Consider bid strategy adjustment (Target ROAS → Maximize Conversion Value test)"
            ]

        elif issue_type == 'budget_constraint':
            # Calculate revenue opportunity
            top_constrained = sorted(issues, key=lambda x: x['metrics'].get('lost_is_budget', 0), reverse=True)[:3]
            total_lost_is = sum(c['metrics'].get('lost_is_budget', 0) for c in top_constrained)
            avg_roas = sum(c['metrics'].get('roas', 0) for c in top_constrained) / len(top_constrained) if top_constrained else 0
            revenue_opp = (total_lost_is / (1 - total_lost_is)) * total_spend * avg_roas if total_lost_is < 1 else 0

            steps = [
                f"Immediate: Increase budgets for top 3 constrained campaigns (potential +£{revenue_opp:.0f}/week revenue)",
                "Identify budget reallocation candidates from low ROAS campaigns",
                "Test 20% budget increase for 7 days, monitor ROAS stability",
                "Set up automated budget alerts to catch constraints earlier"
            ]

        elif issue_type == 'high_spend_low_performance':
            pause_count = len([i for i in issues if i['metrics'].get('roas', 0) < 0.5])
            reduce_count = len([i for i in issues if 0.5 <= i['metrics'].get('roas', 0) < 1.0])

            steps = [
                f"IMMEDIATE: Pause {pause_count} campaign(s) with ROAS <0.5x (see campaign list above)",
                "Export Search Terms report to identify wasted spend on irrelevant queries",
                "Add negative keywords for top wasting search terms",
                f"Reduce budgets by 50% for {reduce_count} campaign(s) with 0.5-1.0x ROAS while diagnosing"
            ]

        elif issue_type == 'zero_conversions':
            steps = [
                "FIRST: Test conversion tracking using Google Tag Assistant (verify it's not a tracking issue)",
                "Verify conversion action is set to 'Primary' and 'Include in Conversions'",
                "Check if conversion window is too short (extend to 90 days for testing)",
                f"If tracking is correct: Pause highest-spending zero-conversion campaigns until diagnosis complete"
            ]

        else:
            steps = ["Review campaign performance in detail", "Take corrective action based on data"]

        return steps

    def _calculate_health_score(
        self,
        campaign_analyses: List[Dict[str, Any]],
        all_issues: List[Dict[str, Any]]
    ) -> int:
        """
        Calculate account health score (0-100)

        Args:
            campaign_analyses: List of campaign analysis results
            all_issues: All detected issues

        Returns:
            Health score 0-100
        """
        if not campaign_analyses:
            return 0

        score = 100

        # Deduct points for issues
        issue_penalties = {
            'P0': 15,  # Critical issues
            'P1': 10,  # High priority
            'P2': 5,   # Medium priority
            'P3': 2    # Low priority
        }

        for issue in all_issues:
            severity = issue.get('severity', 'P3')
            score -= issue_penalties.get(severity, 2)

        # Bonus points for campaigns meeting ROAS targets
        campaigns_with_targets = [
            c for c in campaign_analyses
            if c.get('target_roas') is not None
        ]

        if campaigns_with_targets:
            meeting_target = sum(
                1 for c in campaigns_with_targets
                if c['metrics']['roas'] >= c['target_roas']
            )
            target_rate = meeting_target / len(campaigns_with_targets)
            score += int(target_rate * 10)  # Up to +10 points

        # Ensure score stays within 0-100
        return max(0, min(100, score))

    def _generate_summary(
        self,
        campaign_analyses: List[Dict[str, Any]],
        health_score: int,
        product_analysis: Optional[Dict] = None
    ) -> str:
        """Generate executive summary including product analysis"""

        total_campaigns = len(campaign_analyses)
        total_spend = sum(c['metrics']['spend'] for c in campaign_analyses)
        total_revenue = sum(c['metrics']['revenue'] for c in campaign_analyses)
        blended_roas = total_revenue / total_spend if total_spend > 0 else 0

        total_issues = sum(len(c['issues']) for c in campaign_analyses)

        p0_issues = sum(
            1 for c in campaign_analyses
            for i in c['issues']
            if i['severity'] == 'P0'
        )

        health_label = "Excellent" if health_score >= 90 else \
                      "Good" if health_score >= 75 else \
                      "Fair" if health_score >= 60 else \
                      "Poor" if health_score >= 40 else "Critical"

        summary = f"""Account Health: {health_label} ({health_score}/100)

Analysed {total_campaigns} campaigns with total spend of £{total_spend:,.0f} and blended ROAS of {blended_roas:.2f}x.

Detected {total_issues} issues requiring attention"""

        if p0_issues > 0:
            summary += f" (including {p0_issues} critical P0 issues)"

        summary += "."

        # Add product analysis summary if available
        if product_analysis and not product_analysis.get('error'):
            total_products = product_analysis.get('total_products', 0)
            products_with_issues = product_analysis.get('products_with_issues', 0)
            disapproved = product_analysis.get('disapproved_products', 0)

            summary += f"\n\nProduct Analysis: {total_products} products tracked"
            if products_with_issues > 0:
                summary += f", {products_with_issues} with issues"
            if disapproved > 0:
                summary += f" ({disapproved} disapproved)"
            summary += "."

        return summary
