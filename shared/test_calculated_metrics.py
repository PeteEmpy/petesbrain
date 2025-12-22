"""
Test Suite for Calculated Metrics Helper

Tests all edge cases, especially:
- Division by zero handling
- Proper aggregation (never average percentages)
- Format display with N/A handling
- Context comparison

Run with:
    cd /Users/administrator/Documents/PetesBrain
    python3 shared/test_calculated_metrics.py

Expected output: All tests pass
"""

import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent))

from calculated_metrics import (
    calculate_roas, calculate_cpa, calculate_ctr, calculate_conversion_rate,
    format_metric, calculate_variance, format_variance,
    aggregate_metrics, add_context, convert_micros_to_currency,
    process_campaign_metrics
)


def test_calculate_roas():
    """Test ROAS calculation with edge cases"""
    print("Testing calculate_roas()...")

    # Normal case
    assert calculate_roas(5400, 1200) == 4.5, "Normal ROAS calculation failed"

    # Division by zero
    assert calculate_roas(5400, 0) is None, "Division by zero should return None"
    assert calculate_roas(0, 0) is None, "Zero revenue, zero cost should return None"

    # None values
    assert calculate_roas(5400, None) is None, "None cost should return None"

    print("✓ calculate_roas() passed all tests")


def test_calculate_cpa():
    """Test CPA calculation with edge cases"""
    print("Testing calculate_cpa()...")

    # Normal case
    assert abs(calculate_cpa(1200, 28) - 42.857142857142854) < 0.01, "Normal CPA calculation failed"

    # Division by zero
    assert calculate_cpa(1200, 0) is None, "Division by zero should return None"
    assert calculate_cpa(0, 0) is None, "Zero cost, zero conversions should return None"

    # None values
    assert calculate_cpa(1200, None) is None, "None conversions should return None"

    print("✓ calculate_cpa() passed all tests")


def test_calculate_ctr():
    """Test CTR calculation"""
    print("Testing calculate_ctr()...")

    # Normal case
    assert calculate_ctr(350, 10000) == 0.035, "Normal CTR calculation failed"

    # Division by zero
    assert calculate_ctr(350, 0) is None, "Zero impressions should return None"

    print("✓ calculate_ctr() passed all tests")


def test_calculate_conversion_rate():
    """Test conversion rate calculation"""
    print("Testing calculate_conversion_rate()...")

    # Normal case
    assert calculate_conversion_rate(28, 350) == 0.08, "Normal conversion rate calculation failed"

    # Division by zero
    assert calculate_conversion_rate(28, 0) is None, "Zero clicks should return None"

    print("✓ calculate_conversion_rate() passed all tests")


def test_format_metric():
    """Test metric formatting with different types"""
    print("Testing format_metric()...")

    # ROAS formatting
    assert format_metric(4.567, 'roas') == '4.57x', "ROAS formatting failed"
    assert format_metric(None, 'roas') == 'N/A', "None ROAS should show N/A"

    # Currency formatting
    assert format_metric(1234.56, 'currency') == '£1,234.56', "Currency formatting failed"
    assert format_metric(1234567.89, 'currency') == '£1,234,567.89', "Large currency formatting failed"

    # Percentage formatting
    assert format_metric(0.0345, 'percentage') == '3.45%', "Percentage formatting failed"

    # Integer formatting
    assert format_metric(1234567, 'integer') == '1,234,567', "Integer formatting failed"

    # N/A vs em dash
    assert format_metric(None, 'roas', show_na=True) == 'N/A', "N/A formatting failed"
    assert format_metric(None, 'roas', show_na=False) == '—', "Em dash formatting failed"

    print("✓ format_metric() passed all tests")


def test_calculate_variance():
    """Test variance calculation"""
    print("Testing calculate_variance()...")

    # Positive variance (above target) - use approximate equality due to floating point
    assert abs(calculate_variance(4.8, 4.0) - 20.0) < 0.01, "Positive variance calculation failed"

    # Negative variance (below target)
    assert abs(calculate_variance(3.2, 4.0) - (-20.0)) < 0.01, "Negative variance calculation failed"

    # Zero variance (at target)
    assert abs(calculate_variance(4.0, 4.0) - 0.0) < 0.01, "Zero variance calculation failed"

    # Division by zero
    assert calculate_variance(4.0, 0) is None, "Zero target should return None"

    # None actual
    assert calculate_variance(None, 4.0) is None, "None actual should return None"

    print("✓ calculate_variance() passed all tests")


def test_format_variance():
    """Test variance formatting with indicators"""
    print("Testing format_variance()...")

    # Significantly above target
    assert '✓' in format_variance(20.5), "Should show ✓ for +20%"
    assert '+20.5%' in format_variance(20.5), "Should show +20.5%"

    # Significantly below target
    assert '⚠️' in format_variance(-15.3), "Should show ⚠️ for -15%"
    assert '-15.3%' in format_variance(-15.3), "Should show -15.3%"

    # Slightly below target
    assert '◆' in format_variance(-5.2), "Should show ◆ for -5%"

    # None handling
    assert format_variance(None) == 'N/A', "None variance should show N/A"

    print("✓ format_variance() passed all tests")


def test_aggregate_metrics():
    """Test proper aggregation (CRITICAL - never average percentages!)"""
    print("Testing aggregate_metrics()...")

    # Example showing proper aggregation:
    # Campaign 1: £100 spend, £500 revenue = 5.0x ROAS
    # Campaign 2: £900 spend, £2,700 revenue = 3.0x ROAS
    # Average ROAS = 4.0x (WRONG)
    # Actual ROAS = 3.2x (CORRECT)

    campaigns = [
        {'cost': 100, 'conversions_value': 500, 'conversions': 10},
        {'cost': 900, 'conversions_value': 2700, 'conversions': 90}
    ]

    result = aggregate_metrics(campaigns)

    assert result['total_cost'] == 1000, "Total cost calculation failed"
    assert result['total_revenue'] == 3200, "Total revenue calculation failed"
    assert result['total_conversions'] == 100, "Total conversions calculation failed"
    assert result['roas'] == 3.2, f"Aggregated ROAS should be 3.2, not {result['roas']} (NOT 4.0!)"
    assert result['cpa'] == 10.0, "Aggregated CPA calculation failed"

    # Verify averaging would give WRONG answer
    campaign_1_roas = calculate_roas(500, 100)  # 5.0
    campaign_2_roas = calculate_roas(2700, 900)  # 3.0
    wrong_average = (campaign_1_roas + campaign_2_roas) / 2  # 4.0
    assert wrong_average == 4.0, "Setup check: averaging should give 4.0"
    assert result['roas'] != wrong_average, "CRITICAL: Should NOT average ROAS!"

    print("✓ aggregate_metrics() passed all tests (proper aggregation verified)")


def test_add_context():
    """Test context addition with multiple comparisons"""
    print("Testing add_context()...")

    context = add_context(
        current_metric=3.8,
        target=4.0,
        previous=4.2,
        account_average=4.5
    )

    assert context['value'] == 3.8, "Value should be stored"
    assert abs(context['vs_target'] - (-5.0)) < 0.01, "vs_target calculation failed"
    assert abs(context['vs_previous'] - (-9.523809523809524)) < 0.01, "vs_previous calculation failed"
    assert abs(context['vs_account'] - (-15.555555555555555)) < 0.01, "vs_account calculation failed"

    # With missing comparisons
    context_partial = add_context(current_metric=3.8, target=4.0)
    assert abs(context_partial['vs_target'] - (-5.0)) < 0.01, "Should calculate available comparisons"
    assert context_partial['vs_previous'] is None, "Should handle missing previous"
    assert context_partial['vs_account'] is None, "Should handle missing account average"

    print("✓ add_context() passed all tests")


def test_convert_micros_to_currency():
    """Test Google Ads micros conversion"""
    print("Testing convert_micros_to_currency()...")

    assert convert_micros_to_currency(1200000000) == 1200.0, "Standard micros conversion failed"
    assert convert_micros_to_currency(0) == 0.0, "Zero micros should return 0.0"
    assert convert_micros_to_currency(None) == 0.0, "None micros should return 0.0"
    assert convert_micros_to_currency(1000000) == 1.0, "£1 micros conversion failed"

    print("✓ convert_micros_to_currency() passed all tests")


def test_process_campaign_metrics():
    """Test complete workflow with real API-like data"""
    print("Testing process_campaign_metrics()...")

    raw_data = {
        'cost_micros': 1200000000,  # £1,200
        'conversions_value_micros': 5400000000,  # £5,400
        'conversions': 28
    }

    previous_data = {
        'cost_micros': 1100000000,  # £1,100
        'conversions_value_micros': 4400000000,  # £4,400
        'conversions': 25
    }

    result = process_campaign_metrics(raw_data, target_roas=4.0, previous_data=previous_data)

    # Check conversions
    assert result['cost'] == 1200.0, "Cost conversion failed"
    assert result['revenue'] == 5400.0, "Revenue conversion failed"
    assert result['conversions'] == 28, "Conversions should be stored"

    # Check ROAS calculation and context
    assert result['roas']['value'] == 4.5, "ROAS calculation failed"
    assert result['roas']['vs_target'] == 12.5, "ROAS vs_target failed"  # 4.5 vs 4.0 = +12.5%

    # Previous ROAS was 4.0, current is 4.5 = +12.5% improvement
    previous_roas = 4400000000 / 1100000000  # 4.0
    expected_vs_previous = ((4.5 - previous_roas) / previous_roas) * 100
    assert abs(result['roas']['vs_previous'] - expected_vs_previous) < 0.01, "ROAS vs_previous failed"

    # Check CPA
    assert abs(result['cpa']['value'] - 42.857142857142854) < 0.01, "CPA calculation failed"

    print("✓ process_campaign_metrics() passed all tests")


def test_edge_cases():
    """Test edge cases that could break automation"""
    print("Testing edge cases...")

    # All zeros
    assert calculate_roas(0, 0) is None, "Zero revenue, zero cost should be None"
    assert calculate_cpa(0, 0) is None, "Zero cost, zero conversions should be None"

    # Mixed zeros
    assert calculate_roas(100, 0) is None, "Revenue with zero cost should be None"
    assert calculate_roas(0, 100) == 0.0, "Zero revenue with cost should be 0.0"

    # Very small numbers
    small_roas = calculate_roas(0.01, 100)
    assert small_roas == 0.0001, "Very small ROAS calculation failed"

    # Very large numbers
    large_roas = calculate_roas(1000000, 1)
    assert large_roas == 1000000.0, "Very large ROAS calculation failed"

    # Formatting edge cases
    assert format_metric(0, 'roas') == '0.00x', "Zero ROAS formatting failed"
    assert format_metric(0.001, 'percentage', decimal_places=3) == '0.100%', "Small percentage formatting failed"

    print("✓ Edge cases passed all tests")


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "=" * 60)
    print("CALCULATED METRICS TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_calculate_roas()
        test_calculate_cpa()
        test_calculate_ctr()
        test_calculate_conversion_rate()
        test_format_metric()
        test_calculate_variance()
        test_format_variance()
        test_aggregate_metrics()
        test_add_context()
        test_convert_micros_to_currency()
        test_process_campaign_metrics()
        test_edge_cases()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nCalculated metrics module is ready for use in weekly reports.")
        print("Key verified behaviours:")
        print("  - Division by zero returns None (not errors)")
        print("  - Aggregation uses sum-first-calculate-second (not averaging)")
        print("  - Context comparison calculates variance correctly")
        print("  - Formatting handles None gracefully with N/A")
        print("  - Micros conversion works for Google Ads API data")
        return True

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
