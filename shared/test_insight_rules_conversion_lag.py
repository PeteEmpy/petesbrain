"""
Test InsightEngine conversion lag detection.

This test verifies that the InsightEngine correctly handles incomplete data
and prevents false insights from conversion lag.
"""

from datetime import date, timedelta
from insight_rules import InsightEngine

def test_conversion_lag_detection():
    """Test conversion lag detection across different scenarios"""

    engine = InsightEngine()

    # Test data - ROAS appears to drop from 420% to 360%
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

    print("=" * 70)
    print("CONVERSION LAG DETECTION TEST")
    print("=" * 70)
    print()

    # Scenario 1: Data ended 0 days ago (today) - TOO FRESH
    print("📊 Scenario 1: Period ended TODAY (0 days ago)")
    print("-" * 70)
    today = date.today().strftime('%Y-%m-%d')
    insights = engine.generate_insights(
        current, previous,
        target_roas=400,
        current_period_end_date=today,
        current_period_days=7
    )

    if insights and insights[0]['type'] == 'data_quality_warning':
        print(f"✅ CORRECTLY BLOCKED insights - data only {insights[0]['data_quality']['completeness']:.0f}% complete")
        print(f"   Wait until: {insights[0]['data_quality']['recommended_wait_until']}")
    else:
        print(f"❌ FAILED - should have blocked insights (data too fresh)")
    print()

    # Scenario 2: Data ended 2 days ago - STILL TOO FRESH
    print("📊 Scenario 2: Period ended 2 days ago")
    print("-" * 70)
    two_days_ago = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    insights = engine.generate_insights(
        current, previous,
        target_roas=400,
        current_period_end_date=two_days_ago,
        current_period_days=7
    )

    if insights and insights[0]['type'] == 'data_quality_warning':
        print(f"✅ CORRECTLY BLOCKED insights - data only {insights[0]['data_quality']['completeness']:.0f}% complete")
    else:
        print(f"❌ FAILED - should have blocked insights (data <50% complete)")
    print()

    # Scenario 3: Data ended 4 days ago - PARTIAL (should generate with caveats)
    print("📊 Scenario 3: Period ended 4 days ago")
    print("-" * 70)
    four_days_ago = (date.today() - timedelta(days=4)).strftime('%Y-%m-%d')
    insights = engine.generate_insights(
        current, previous,
        target_roas=400,
        current_period_end_date=four_days_ago,
        current_period_days=7
    )

    if insights and insights[0]['type'] != 'data_quality_warning':
        completeness = insights[0]['data_quality']['completeness']
        print(f"✅ Generated insights with {completeness:.0f}% complete data")

        # Check if priorities were downgraded
        for insight in insights:
            if 'priority_note' in insight:
                print(f"   ✅ Priority downgraded: {insight['priority_note']}")
            if 'caveat' in insight:
                print(f"   ✅ Caveat added: {insight['caveat'][:80]}...")
    else:
        print(f"❌ FAILED - should have generated insights with caveats (data 50-90% complete)")
    print()

    # Scenario 4: Data ended 7 days ago - COMPLETE
    print("📊 Scenario 4: Period ended 7 days ago")
    print("-" * 70)
    seven_days_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    insights = engine.generate_insights(
        current, previous,
        target_roas=400,
        current_period_end_date=seven_days_ago,
        current_period_days=7
    )

    if insights and insights[0]['type'] != 'data_quality_warning':
        completeness = insights[0]['data_quality']['completeness']
        print(f"✅ Generated insights with {completeness:.0f}% complete data")

        # Should NOT have priority downgrades or caveats
        has_downgrades = any('priority_note' in i for i in insights)
        has_caveats = any('caveat' in i for i in insights)

        if not has_downgrades and not has_caveats:
            print(f"   ✅ NO priority downgrades or caveats (data reliable)")
        else:
            print(f"   ⚠️  Unexpected downgrades/caveats for {completeness:.0f}% complete data")

        # Show the insights
        print(f"   Generated {len(insights)} insights:")
        for insight in insights:
            print(f"   - [{insight['priority']}] {insight['title']}")
    else:
        print(f"❌ FAILED - should have generated normal insights (data >90% complete)")
    print()

    # Scenario 5: No period_end_date provided (backwards compatibility)
    print("📊 Scenario 5: No period_end_date provided (legacy mode)")
    print("-" * 70)
    insights = engine.generate_insights(
        current, previous,
        target_roas=400
        # No current_period_end_date parameter
    )

    if insights and insights[0]['type'] != 'data_quality_warning':
        print(f"✅ Generated insights (backwards compatible)")
        print(f"   Data quality: {insights[0]['data_quality']['quality_level']}")
        print(f"   Completeness: {insights[0]['data_quality']['completeness']:.0f}%")
    else:
        print(f"❌ FAILED - should work without period_end_date (backwards compatibility)")
    print()

    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_conversion_lag_detection()
