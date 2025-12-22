"""
Insight Generation Rules for Google Ads Weekly Reports

Systematically converts data + information into insights.
Based on the Data → Information → Insight → Action framework.

CRITICAL: Includes conversion lag detection to prevent false insights from incomplete data.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date


class InsightEngine:
    """
    Generates insights from Google Ads performance data.

    Insight = Information + Meaning
    - What changed (information)
    - Why it happened (diagnosis)
    - What direction to explore (recommendation)
    """

    def __init__(self):
        """Initialize the insight engine"""
        self.rules = {
            'roas_drop': self._analyse_roas_drop,
            'roas_spike': self._analyse_roas_spike,
            'zero_conversions': self._analyse_zero_conversions,
            'spend_increase': self._analyse_spend_increase,
            'below_target': self._analyse_below_target_roas,
        }

    def _check_data_quality(
        self,
        period_end_date: Optional[str],
        period_days: int
    ) -> Dict[str, Any]:
        """
        Calculate data quality based on conversion lag.

        Conversions can be attributed 30-90 days after click, meaning recent data
        is incomplete. Industry standards:
        - 0-2 days after period end: 40-70% complete (too unreliable)
        - 3-6 days: 80-90% complete (usable with caveats)
        - 7+ days: 95%+ complete (reliable)

        Args:
            period_end_date: End date of period (YYYY-MM-DD) or None if unknown
            period_days: Number of days in period (for context)

        Returns:
            Dict with:
            - days_since_end: Days since period ended (int)
            - completeness: Data completeness percentage (float 0-100)
            - recommended_wait_until: Date string to wait until (YYYY-MM-DD)
            - quality_level: 'incomplete' | 'partial' | 'complete'
        """
        # If no period_end_date provided, assume data is complete (backwards compatibility)
        if not period_end_date:
            return {
                'days_since_end': 999,  # Unknown, assume old
                'completeness': 100,
                'recommended_wait_until': 'N/A',
                'quality_level': 'complete'
            }

        try:
            # Parse period end date
            end_date = datetime.strptime(period_end_date, '%Y-%m-%d').date()
            today = date.today()

            # Calculate days since period ended
            days_since_end = (today - end_date).days

            # Calculate recommended wait date (7 days after period ends)
            from datetime import timedelta
            wait_until = end_date + timedelta(days=7)
            recommended_wait_until = wait_until.strftime('%Y-%m-%d')

            # Calculate data completeness based on industry standards
            if days_since_end <= 0:
                # Period hasn't ended yet - data is very incomplete
                completeness = 30
                quality_level = 'incomplete'
            elif days_since_end == 1:
                # 1 day after end - ~40% complete (most conversions still pending)
                completeness = 40
                quality_level = 'incomplete'
            elif days_since_end == 2:
                # 2 days after end - ~48% complete (still too early)
                completeness = 48
                quality_level = 'incomplete'
            elif days_since_end == 3:
                # 3 days - ~80% complete
                completeness = 80
                quality_level = 'partial'
            elif days_since_end == 4:
                # 4 days - ~85% complete
                completeness = 85
                quality_level = 'partial'
            elif days_since_end == 5:
                # 5 days - ~88% complete
                completeness = 88
                quality_level = 'partial'
            elif days_since_end == 6:
                # 6 days - ~90% complete
                completeness = 90
                quality_level = 'partial'
            elif days_since_end >= 7:
                # 7+ days - ~95%+ complete (asymptotic to 100%)
                # After 7 days, most conversions are attributed
                # After 30 days, nearly all conversions are attributed
                if days_since_end >= 30:
                    completeness = 99
                else:
                    # Gradual increase from 95% to 99% over days 7-30
                    completeness = 95 + ((days_since_end - 7) / 23) * 4
                quality_level = 'complete'
            else:
                # Fallback (shouldn't reach here)
                completeness = 50
                quality_level = 'incomplete'

            return {
                'days_since_end': days_since_end,
                'completeness': round(completeness, 1),
                'recommended_wait_until': recommended_wait_until,
                'quality_level': quality_level
            }

        except (ValueError, AttributeError) as e:
            # If date parsing fails, assume data is complete (backwards compatibility)
            return {
                'days_since_end': 999,
                'completeness': 100,
                'recommended_wait_until': 'N/A',
                'quality_level': 'complete',
                'parse_error': str(e)
            }

    def generate_insights(
        self,
        current_metrics: Dict[str, float],
        previous_metrics: Dict[str, float],
        target_roas: Optional[float] = None,
        current_period_end_date: Optional[str] = None,
        current_period_days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Generate insights from performance data with conversion lag awareness.

        Args:
            current_metrics: Current period metrics (spend, revenue, roas, cpc, cvr, aov)
            previous_metrics: Previous period metrics (same structure)
            target_roas: Optional target ROAS for comparison
            current_period_end_date: End date of current period (YYYY-MM-DD) for lag calculation
            current_period_days: Number of days in current period (default 7)

        Returns:
            List of insights with diagnosis and recommendations
        """
        insights = []

        # CRITICAL: Check data quality first (conversion lag detection)
        data_quality = self._check_data_quality(current_period_end_date, current_period_days)

        # If data is too fresh, return warning instead of insights
        if data_quality['completeness'] < 50:
            return [{
                'type': 'data_quality_warning',
                'title': 'Data too recent for reliable insights',
                'diagnosis': 'Conversion lag - data incomplete',
                'priority': 'INFO',
                'what_changed': f"Current period ended {data_quality['days_since_end']} days ago (only {data_quality['completeness']:.0f}% complete)",
                'why_it_happened': 'Conversions can be attributed up to 30 days after click. Data from periods that ended <3 days ago is too incomplete for reliable analysis.',
                'recommended_direction': [
                    f"Wait until {data_quality['recommended_wait_until']} for reliable data (7 days after period ends)",
                    'For immediate analysis, use previous complete week instead',
                    'Or accept that insights may change as more conversions are attributed'
                ],
                'data_quality': data_quality,
                'metrics': {
                    'days_since_period_end': data_quality['days_since_end'],
                    'data_completeness_pct': data_quality['completeness'],
                    'period_days': current_period_days
                }
            }]

        # Calculate changes
        changes = self._calculate_changes(current_metrics, previous_metrics)

        # Apply rules to detect patterns (adjusted thresholds for real-world significance)
        if changes['roas_change_pct'] < -10:  # 10%+ drop is significant
            insights.append(self._analyse_roas_drop(current_metrics, previous_metrics, changes))

        if changes['roas_change_pct'] > 15:  # 15%+ increase is significant
            insights.append(self._analyse_roas_spike(current_metrics, previous_metrics, changes))

        if current_metrics.get('conversions', 0) == 0 and current_metrics.get('spend', 0) > 50:
            insights.append(self._analyse_zero_conversions(current_metrics, previous_metrics, changes))

        if changes['spend_change_pct'] > 15:  # 15%+ spend increase needs analysis
            insights.append(self._analyse_spend_increase(current_metrics, previous_metrics, changes))

        if target_roas and current_metrics.get('roas', 0) < target_roas * 0.90:  # 10%+ below target
            insights.append(self._analyse_below_target_roas(current_metrics, previous_metrics, changes, target_roas))

        # Add data quality metadata to all insights
        for insight in insights:
            insight['data_quality'] = data_quality

            # Downgrade priorities if data is incomplete
            if data_quality['completeness'] < 90:
                original_priority = insight['priority']
                # Downgrade: P0 → P1, P1 → P2, P2 → P2 (floor at P2)
                if original_priority == 'P0':
                    insight['priority'] = 'P1'
                    insight['priority_note'] = 'Downgraded from P0 due to incomplete data'
                elif original_priority == 'P1':
                    insight['priority'] = 'P2'
                    insight['priority_note'] = 'Downgraded from P1 due to incomplete data'

                # Add caveat to all insights
                insight['caveat'] = f"⚠️ Based on {data_quality['completeness']:.0f}% complete data (period ended {data_quality['days_since_end']} days ago). True performance may differ as more conversions are attributed."

        return insights

    def _calculate_changes(
        self,
        current: Dict[str, float],
        previous: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate percentage changes between periods"""
        changes = {}

        for key in ['spend', 'revenue', 'roas', 'conversions', 'cpc', 'cvr', 'aov']:
            curr_val = current.get(key, 0)
            prev_val = previous.get(key, 0.0001)  # Prevent division by zero

            change_pct = ((curr_val - prev_val) / prev_val) * 100 if prev_val > 0 else 0
            changes[f'{key}_change_pct'] = change_pct
            changes[f'{key}_change_abs'] = curr_val - prev_val

        return changes

    def _analyse_roas_drop(
        self,
        current: Dict[str, float],
        previous: Dict[str, float],
        changes: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyse why ROAS dropped.

        Diagnosis logic:
        1. CPC increased >15% + CVR stable → External competitive pressure
        2. CVR dropped >10% + CPC stable → Landing page/conversion issue
        3. AOV dropped >10% → Product mix or pricing issue
        4. All stable but ROAS down → Mixed factors or data anomaly
        """
        roas_drop = changes['roas_change_pct']
        cpc_change = changes['cpc_change_pct']
        cvr_change = changes['cvr_change_pct']
        aov_change = changes['aov_change_pct']

        # Determine diagnosis
        if cpc_change > 15 and abs(cvr_change) < 10:
            diagnosis = "External competitive pressure"
            reason = f"CPC increased {cpc_change:.0f}% while conversion rate remained stable at {current['cvr']:.1f}%. This indicates auction competition increased, not a performance issue with your ads or site."
            recommended_direction = [
                "Test improved ad copy to increase Quality Score and reduce CPC",
                "Add exact match keywords to reduce waste from broad match",
                "Check Auction Insights for new competitors",
                "Consider alternative keyword themes with lower competition"
            ]
            priority = 'P1'

        elif cvr_change < -10 and abs(cpc_change) < 15:
            diagnosis = "Landing page or conversion issue"
            reason = f"Conversion rate dropped {abs(cvr_change):.0f}% (from {previous['cvr']:.1f}% to {current['cvr']:.1f}%) while CPC remained stable. This suggests a problem with the site, checkout flow, or offer appeal."
            recommended_direction = [
                "Check for recent site changes or technical issues",
                "Review landing page performance in GA4",
                "Test alternative landing pages",
                "Check for stock-outs or pricing changes",
                "Review checkout funnel for drop-off points"
            ]
            priority = 'P0'  # Critical - conversion issues need immediate attention

        elif aov_change < -10:
            diagnosis = "Product mix or pricing issue"
            reason = f"Average Order Value dropped {abs(aov_change):.0f}% (from £{previous['aov']:.2f} to £{current['aov']:.2f}). Customers are buying lower-value items or purchasing less per order."
            recommended_direction = [
                "Review product performance to identify high-AOV items",
                "Check for promotions or discounts driving low-value purchases",
                "Test AOV-boosting tactics (bundles, upsells, free shipping thresholds)",
                "Analyse product-level ROAS to shift spend to high-value products"
            ]
            priority = 'P1'

        else:
            diagnosis = "Mixed factors or data anomaly"
            reason = f"ROAS dropped {abs(roas_drop):.0f}% but no single metric shows clear cause. CPC change: {cpc_change:+.0f}%, CVR change: {cvr_change:+.0f}%, AOV change: {aov_change:+.0f}%."
            recommended_direction = [
                "Check for attribution window changes or data delays",
                "Review daily breakdown to identify if drop is consistent or spike-driven",
                "Compare to same period last year for seasonality",
                "Monitor over next 2-3 days to confirm trend"
            ]
            priority = 'P2'

        return {
            'type': 'roas_drop',
            'title': f"ROAS dropped {abs(roas_drop):.0f}% WoW",
            'what_changed': f"ROAS decreased from {previous['roas']:.0f}% to {current['roas']:.0f}% ({roas_drop:+.0f}%)",
            'why_it_happened': reason,
            'diagnosis': diagnosis,
            'recommended_direction': recommended_direction,
            'priority': priority,
            'metrics': {
                'current_roas': current['roas'],
                'previous_roas': previous['roas'],
                'roas_change_pct': roas_drop,
                'cpc_change_pct': cpc_change,
                'cvr_change_pct': cvr_change,
                'aov_change_pct': aov_change
            }
        }

    def _analyse_roas_spike(
        self,
        current: Dict[str, float],
        previous: Dict[str, float],
        changes: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyse why ROAS spiked (good news, but understand why).
        """
        roas_spike = changes['roas_change_pct']
        cvr_change = changes['cvr_change_pct']
        aov_change = changes['aov_change_pct']
        cpc_change = changes['cpc_change_pct']

        if cvr_change > 15:
            diagnosis = "Conversion rate improvement"
            reason = f"Conversion rate improved {cvr_change:.0f}% (from {previous['cvr']:.1f}% to {current['cvr']:.1f}%). This could be due to better traffic quality, site improvements, or seasonal factors."
        elif aov_change > 15:
            diagnosis = "Higher-value purchases"
            reason = f"Average Order Value increased {aov_change:.0f}% (from £{previous['aov']:.2f} to £{current['aov']:.2f}). Customers are buying more expensive items or larger orders."
        elif cpc_change < -15:
            diagnosis = "Cost efficiency improvement"
            reason = f"CPC decreased {abs(cpc_change):.0f}% while maintaining conversion performance. Quality Score improvements or reduced competition."
        else:
            diagnosis = "Overall performance improvement"
            reason = f"ROAS increased {roas_spike:.0f}% across multiple factors (CVR: {cvr_change:+.0f}%, AOV: {aov_change:+.0f}%, CPC: {cpc_change:+.0f}%)."

        return {
            'type': 'roas_spike',
            'title': f"ROAS increased {roas_spike:.0f}% WoW",
            'what_changed': f"ROAS increased from {previous['roas']:.0f}% to {current['roas']:.0f}% ({roas_spike:+.0f}%)",
            'why_it_happened': reason,
            'diagnosis': diagnosis,
            'recommended_direction': [
                "Document what contributed to improvement for future reference",
                "Consider increasing budgets to capitalise on strong performance",
                "Monitor to ensure improvement is sustained, not a one-week spike"
            ],
            'priority': 'P2',  # Good news - monitor rather than urgent action
            'metrics': {
                'current_roas': current['roas'],
                'previous_roas': previous['roas'],
                'roas_change_pct': roas_spike
            }
        }

    def _analyse_zero_conversions(
        self,
        current: Dict[str, float],
        previous: Dict[str, float],
        changes: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyse campaigns with zero conversions but significant spend.
        """
        weekly_spend = current.get('spend', 0)
        monthly_waste = weekly_spend * 4.33  # Approximate monthly

        diagnosis = "Zero conversion campaign"
        reason = f"Campaign spent £{weekly_spend:.2f} this week with zero conversions. This represents approximately £{monthly_waste:.2f}/month in wasted spend if trend continues."

        return {
            'type': 'zero_conversions',
            'title': f"Zero conversions with £{weekly_spend:.0f} spend",
            'what_changed': f"Campaign generated {current.get('clicks', 0)} clicks but zero conversions",
            'why_it_happened': reason,
            'diagnosis': diagnosis,
            'recommended_direction': [
                "Check conversion tracking is working correctly",
                "Review search terms for irrelevant traffic",
                "Evaluate landing page relevance and quality",
                "Consider pausing if consistently underperforming",
                "Test alternative targeting or ad copy"
            ],
            'priority': 'P0',  # Critical waste
            'metrics': {
                'weekly_spend': weekly_spend,
                'monthly_waste': monthly_waste,
                'clicks': current.get('clicks', 0),
                'conversions': 0
            }
        }

    def _analyse_spend_increase(
        self,
        current: Dict[str, float],
        previous: Dict[str, float],
        changes: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyse significant spend increases.
        """
        spend_change = changes['spend_change_pct']
        roas_change = changes['roas_change_pct']

        if roas_change > 0:
            diagnosis = "Profitable scale"
            reason = f"Spend increased {spend_change:.0f}% while ROAS improved {roas_change:+.0f}%. This is efficient scaling."
            priority = 'P2'
            recommended_direction = [
                "Monitor closely to ensure ROAS remains above target",
                "Consider further budget increases if headroom exists"
            ]
        elif abs(roas_change) < 10:
            diagnosis = "Neutral scale"
            reason = f"Spend increased {spend_change:.0f}% while ROAS remained relatively stable ({roas_change:+.0f}%). Scaling efficiently."
            priority = 'P2'
            recommended_direction = [
                "Continue monitoring - stable ROAS during scale is good",
                "Watch for diminishing returns if further increases planned"
            ]
        else:
            diagnosis = "Inefficient scale"
            reason = f"Spend increased {spend_change:.0f}% but ROAS declined {abs(roas_change):.0f}%. Hitting diminishing returns."
            priority = 'P1'
            recommended_direction = [
                "Consider reducing budgets back to previous level",
                "Analyse what additional traffic/products drove increased spend",
                "Test incremental increases rather than large jumps"
            ]

        return {
            'type': 'spend_increase',
            'title': f"Spend increased {spend_change:.0f}% WoW",
            'what_changed': f"Spend rose from £{previous['spend']:.2f} to £{current['spend']:.2f}",
            'why_it_happened': reason,
            'diagnosis': diagnosis,
            'recommended_direction': recommended_direction,
            'priority': priority,
            'metrics': {
                'current_spend': current['spend'],
                'previous_spend': previous['spend'],
                'spend_change_pct': spend_change,
                'roas_change_pct': roas_change
            }
        }

    def _analyse_below_target_roas(
        self,
        current: Dict[str, float],
        previous: Dict[str, float],
        changes: Dict[str, float],
        target_roas: float
    ) -> Dict[str, Any]:
        """
        Analyse campaigns performing below target ROAS.
        """
        current_roas = current.get('roas', 0)
        gap_pct = ((current_roas - target_roas) / target_roas) * 100

        diagnosis = "Below target ROAS"
        reason = f"Current ROAS of {current_roas:.0f}% is {abs(gap_pct):.0f}% below target of {target_roas:.0f}%."

        return {
            'type': 'below_target',
            'title': f"ROAS {abs(gap_pct):.0f}% below target",
            'what_changed': f"ROAS at {current_roas:.0f}% vs {target_roas:.0f}% target",
            'why_it_happened': reason,
            'diagnosis': diagnosis,
            'recommended_direction': [
                "Review if target is still realistic for current market conditions",
                "Analyse top-performing campaigns for optimisation patterns",
                "Consider reducing spend if consistently below target",
                "Test campaign structure changes or new targeting approaches"
            ],
            'priority': 'P1',
            'metrics': {
                'current_roas': current_roas,
                'target_roas': target_roas,
                'gap_pct': gap_pct
            }
        }


# Quick test
if __name__ == "__main__":
    print("Testing Insight Engine...\n")

    engine = InsightEngine()

    # Test scenario: ROAS drop due to CPC increase
    current = {
        'spend': 2450,
        'revenue': 8820,
        'roas': 360,
        'conversions': 48,
        'cpc': 2.20,
        'cvr': 4.2,
        'aov': 185
    }

    previous = {
        'spend': 2100,
        'revenue': 8820,
        'roas': 420,
        'conversions': 46,
        'cpc': 1.80,
        'cvr': 4.2,
        'aov': 185
    }

    insights = engine.generate_insights(current, previous, target_roas=400)

    for insight in insights:
        print(f"🔍 {insight['title']}")
        print(f"   Diagnosis: {insight['diagnosis']}")
        print(f"   Why: {insight['why_it_happened']}")
        print(f"   Priority: {insight['priority']}")
        print(f"   Next steps:")
        for step in insight['recommended_direction']:
            print(f"   - {step}")
        print()
