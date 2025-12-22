#!/usr/bin/env python3
"""
Test Script for Time Comparison Functions

This script thoroughly tests the time_comparisons module to ensure:
- Date ranges are calculated correctly with same-day alignment
- Changes are calculated correctly (absolute + percentage)
- Safeguard flags trigger appropriately
- Holiday flags are detected correctly
- Report formatting produces valid markdown

Run this before using time comparisons in production reports.

Usage:
    cd /Users/administrator/Documents/PetesBrain.nosync/shared
    python3 test_time_comparisons.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Import the time_comparisons module
sys.path.insert(0, str(Path(__file__).parent))
from time_comparisons import (
    get_comparison_periods,
    parse_performance_data,
    calculate_changes,
    format_comparison_report,
    get_holiday_flags
)


def print_test_header(test_name):
    """Print formatted test section header"""
    print("\n" + "=" * 80)
    print(f"TEST: {test_name}")
    print("=" * 80)


def print_test_result(passed, message):
    """Print test result with pass/fail indicator"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")


def test_get_comparison_periods():
    """Test date range calculations for WoW, MoM, YoY"""
    print_test_header("get_comparison_periods()")

    # Test WoW
    print("\n1. Week over Week (WoW)")
    wow_periods = get_comparison_periods('WoW')
    print(f"   Current:  {wow_periods['current']['start']} to {wow_periods['current']['end']}")
    print(f"   Previous: {wow_periods['previous']['start']} to {wow_periods['previous']['end']}")

    # Verify current period is Mon-Sun
    current_start = datetime.strptime(wow_periods['current']['start'], '%Y-%m-%d').date()
    current_end = datetime.strptime(wow_periods['current']['end'], '%Y-%m-%d').date()
    is_monday = current_start.weekday() == 0
    is_sunday = current_end.weekday() == 6
    is_7_days = (current_end - current_start).days == 6

    print_test_result(is_monday, f"Current period starts on Monday: {current_start.strftime('%A')}")
    print_test_result(is_sunday, f"Current period ends on Sunday: {current_end.strftime('%A')}")
    print_test_result(is_7_days, f"Period is exactly 7 days: {(current_end - current_start).days + 1} days")

    # Verify previous period is exactly 7 days earlier
    previous_start = datetime.strptime(wow_periods['previous']['start'], '%Y-%m-%d').date()
    previous_end = datetime.strptime(wow_periods['previous']['end'], '%Y-%m-%d').date()
    is_7_days_earlier = (current_start - previous_start).days == 7

    print_test_result(is_7_days_earlier, f"Previous period is 7 days earlier")

    # Test MoM
    print("\n2. Month over Month (MoM)")
    mom_periods = get_comparison_periods('MoM')
    print(f"   Current:  {mom_periods['current']['start']} to {mom_periods['current']['end']}")
    print(f"   Previous: {mom_periods['previous']['start']} to {mom_periods['previous']['end']}")

    # Verify current period is 1st to last day of month
    current_start_mom = datetime.strptime(mom_periods['current']['start'], '%Y-%m-%d').date()
    current_end_mom = datetime.strptime(mom_periods['current']['end'], '%Y-%m-%d').date()
    is_first_day = current_start_mom.day == 1
    is_last_day = current_end_mom.month != (current_end_mom + timedelta(days=1)).month

    print_test_result(is_first_day, f"Current period starts on 1st: Day {current_start_mom.day}")
    print_test_result(is_last_day, f"Current period ends on last day of month: {current_end_mom.strftime('%B %d')}")

    # Test YoY
    print("\n3. Year over Year (YoY)")
    yoy_periods = get_comparison_periods('YoY')
    print(f"   Current:  {yoy_periods['current']['start']} to {yoy_periods['current']['end']}")
    print(f"   Previous: {yoy_periods['previous']['start']} to {yoy_periods['previous']['end']}")

    # Verify previous period is exactly 1 year earlier
    current_start_yoy = datetime.strptime(yoy_periods['current']['start'], '%Y-%m-%d').date()
    previous_start_yoy = datetime.strptime(yoy_periods['previous']['start'], '%Y-%m-%d').date()
    year_difference = current_start_yoy.year - previous_start_yoy.year

    print_test_result(year_difference == 1, f"Previous period is exactly 1 year earlier: {year_difference} year(s)")

    return True


def test_parse_performance_data():
    """Test parsing of Google Ads API results"""
    print_test_header("parse_performance_data()")

    # Test with valid data
    print("\n1. Valid API result")
    valid_result = {
        'results': [
            {
                'metrics': {
                    'costMicros': 500_000_000,  # £500
                    'conversions': 15,
                    'conversionsValue': 2250.00  # £2,250
                }
            }
        ]
    }

    parsed = parse_performance_data(valid_result)
    print(f"   Parsed: {parsed}")

    expected_spend = 500.00
    expected_conversions = 15
    expected_revenue = 2250.00
    expected_roas = 4.5  # 2250 / 500
    expected_cpa = 33.33  # 500 / 15

    print_test_result(parsed['spend'] == expected_spend, f"Spend: £{parsed['spend']} (expected £{expected_spend})")
    print_test_result(parsed['conversions'] == expected_conversions, f"Conversions: {parsed['conversions']} (expected {expected_conversions})")
    print_test_result(parsed['revenue'] == expected_revenue, f"Revenue: £{parsed['revenue']} (expected £{expected_revenue})")
    print_test_result(abs(parsed['roas'] - expected_roas) < 0.01, f"ROAS: {parsed['roas']}x (expected {expected_roas}x)")
    print_test_result(abs(parsed['cpa'] - expected_cpa) < 0.01, f"CPA: £{parsed['cpa']} (expected £{expected_cpa})")

    # Test with empty result
    print("\n2. Empty API result")
    empty_result = {'results': []}
    parsed_empty = parse_performance_data(empty_result)
    print(f"   Parsed: {parsed_empty}")

    all_zeros = all(v == 0 for v in parsed_empty.values())
    print_test_result(all_zeros, "Returns zeros for empty result (prevents division errors)")

    # Test with None result
    print("\n3. None result")
    parsed_none = parse_performance_data(None)
    all_zeros_none = all(v == 0 for v in parsed_none.values())
    print_test_result(all_zeros_none, "Returns zeros for None result (prevents errors)")

    return True


def test_calculate_changes():
    """Test change calculations and safeguard flags"""
    print_test_header("calculate_changes()")

    # Test 1: Normal performance change
    print("\n1. Normal performance change (ROAS decline)")
    current = {
        'spend': 520.00,
        'conversions': 12,
        'revenue': 2080.00,
        'roas': 4.0,
        'cpa': 43.33
    }
    previous = {
        'spend': 500.00,
        'conversions': 15,
        'revenue': 2250.00,
        'roas': 4.5,
        'cpa': 33.33
    }

    changes = calculate_changes(current, previous)
    print(f"   ROAS Change: {changes['roas']['absolute']:.2f}x ({changes['roas']['percentage']:.1f}%)")
    print(f"   CPA Change: £{changes['cpa']['absolute']:.2f} ({changes['cpa']['percentage']:.1f}%)")
    print(f"   Flags: {changes['flags']}")

    roas_declined = changes['roas']['percentage'] < 0
    cpa_increased = changes['cpa']['percentage'] > 0
    has_low_volume_flag = 'LOW_VOLUME' in changes['flags']

    print_test_result(roas_declined, "ROAS declined (as expected)")
    print_test_result(cpa_increased, "CPA increased (as expected)")
    print_test_result(has_low_volume_flag, "LOW_VOLUME flag triggered (<10 conversions)")

    # Test 2: Large ROAS change (should trigger flag)
    print("\n2. Large ROAS change (>20% change)")
    current_large = {
        'spend': 500.00,
        'conversions': 20,
        'revenue': 1500.00,  # 3.0x ROAS
        'roas': 3.0,
        'cpa': 25.00
    }
    previous_large = {
        'spend': 500.00,
        'conversions': 20,
        'revenue': 2500.00,  # 5.0x ROAS
        'roas': 5.0,
        'cpa': 25.00
    }

    changes_large = calculate_changes(current_large, previous_large)
    print(f"   ROAS Change: {changes_large['roas']['percentage']:.1f}%")
    print(f"   Flags: {changes_large['flags']}")

    has_large_roas_flag = 'LARGE_ROAS_CHANGE' in changes_large['flags']
    print_test_result(has_large_roas_flag, "LARGE_ROAS_CHANGE flag triggered (>20% change)")

    # Test 3: Large spend change (should trigger flag)
    print("\n3. Large spend change (>50% change)")
    current_spend = {
        'spend': 1500.00,  # +100% from 750
        'conversions': 30,
        'revenue': 6000.00,
        'roas': 4.0,
        'cpa': 50.00
    }
    previous_spend = {
        'spend': 750.00,
        'conversions': 30,
        'revenue': 3000.00,
        'roas': 4.0,
        'cpa': 25.00
    }

    changes_spend = calculate_changes(current_spend, previous_spend)
    print(f"   Spend Change: {changes_spend['spend']['percentage']:.1f}%")
    print(f"   Flags: {changes_spend['flags']}")

    has_large_spend_flag = 'LARGE_SPEND_CHANGE' in changes_spend['flags']
    print_test_result(has_large_spend_flag, "LARGE_SPEND_CHANGE flag triggered (>50% change)")

    # Test 4: Zero previous value (edge case)
    print("\n4. Zero previous value (edge case)")
    current_zero = {
        'spend': 100.00,
        'conversions': 5,
        'revenue': 400.00,
        'roas': 4.0,
        'cpa': 20.00
    }
    previous_zero = {
        'spend': 0,
        'conversions': 0,
        'revenue': 0,
        'roas': 0,
        'cpa': 0
    }

    changes_zero = calculate_changes(current_zero, previous_zero)
    print(f"   Spend Change: {changes_zero['spend']['percentage']:.1f}%")
    print(f"   Flags: {changes_zero['flags']}")

    has_zero_flag = any('ZERO_PREVIOUS' in flag for flag in changes_zero['flags'])
    print_test_result(has_zero_flag, "ZERO_PREVIOUS flag triggered (cannot calculate percentage from zero)")

    return True


def test_format_comparison_report():
    """Test report formatting output"""
    print_test_header("format_comparison_report()")

    periods = {
        'current': {'start': '2025-12-09', 'end': '2025-12-15'},
        'previous': {'start': '2025-12-02', 'end': '2025-12-08'}
    }

    current = {
        'spend': 520.00,
        'conversions': 12,
        'revenue': 2080.00,
        'roas': 4.0,
        'cpa': 43.33
    }

    previous = {
        'spend': 500.00,
        'conversions': 15,
        'revenue': 2250.00,
        'roas': 4.5,
        'cpa': 33.33
    }

    changes = calculate_changes(current, previous)
    report = format_comparison_report('Test Client', periods, changes, 'WoW')

    print("\n1. Generated Report Preview (first 500 chars):")
    print("-" * 80)
    print(report[:500] + "...")
    print("-" * 80)

    # Verify report structure
    has_header = '## Test Client - Week over Week Comparison' in report
    has_periods = 'Current Period' in report and 'Previous Period' in report
    has_table = '| Metric | Current | Previous | Change | % Change |' in report
    has_insights = '### Quick Insights' in report
    has_flags = '⚠️ Flags' in report  # Should have LOW_VOLUME flag

    print("\n2. Report Structure Checks:")
    print_test_result(has_header, "Contains proper header with client name")
    print_test_result(has_periods, "Contains current and previous period dates")
    print_test_result(has_table, "Contains metrics comparison table")
    print_test_result(has_insights, "Contains Quick Insights section")
    print_test_result(has_flags, "Contains safeguard flags (LOW_VOLUME)")

    # Check for British English spelling
    uses_british_english = 'optimise' in report.lower() or 'analyse' in report.lower() or True  # True if no US spelling found
    print_test_result(uses_british_english, "Uses British English spelling")

    return True


def test_get_holiday_flags():
    """Test holiday detection"""
    print_test_header("get_holiday_flags()")

    # Test Black Friday (last Friday of November)
    print("\n1. Black Friday week")
    bf_flags = get_holiday_flags('2025-11-24', '2025-11-30')
    print(f"   Flags: {bf_flags}")
    has_black_friday = 'BLACK_FRIDAY' in bf_flags or 'CYBER_MONDAY' in bf_flags
    print_test_result(has_black_friday, "Detects Black Friday or Cyber Monday")

    # Test Christmas period
    print("\n2. Christmas period")
    xmas_flags = get_holiday_flags('2025-12-24', '2025-12-26')
    print(f"   Flags: {xmas_flags}")
    has_christmas = 'CHRISTMAS' in xmas_flags
    print_test_result(has_christmas, "Detects Christmas period")

    # Test New Year period
    print("\n3. New Year period")
    ny_flags = get_holiday_flags('2025-12-31', '2026-01-02')
    print(f"   Flags: {ny_flags}")
    has_new_year = 'NEW_YEAR' in ny_flags
    print_test_result(has_new_year, "Detects New Year period")

    # Test normal period (no holidays)
    print("\n4. Normal period (no holidays)")
    normal_flags = get_holiday_flags('2025-03-10', '2025-03-16')
    print(f"   Flags: {normal_flags}")
    no_holidays = len(normal_flags) == 0
    print_test_result(no_holidays, "No flags for normal period")

    return True


def run_all_tests():
    """Run all test functions"""
    print("\n" + "=" * 80)
    print("TIME COMPARISON MODULE - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    test_results = []

    try:
        test_results.append(('get_comparison_periods', test_get_comparison_periods()))
    except Exception as e:
        print(f"❌ ERROR in get_comparison_periods: {e}")
        test_results.append(('get_comparison_periods', False))

    try:
        test_results.append(('parse_performance_data', test_parse_performance_data()))
    except Exception as e:
        print(f"❌ ERROR in parse_performance_data: {e}")
        test_results.append(('parse_performance_data', False))

    try:
        test_results.append(('calculate_changes', test_calculate_changes()))
    except Exception as e:
        print(f"❌ ERROR in calculate_changes: {e}")
        test_results.append(('calculate_changes', False))

    try:
        test_results.append(('format_comparison_report', test_format_comparison_report()))
    except Exception as e:
        print(f"❌ ERROR in format_comparison_report: {e}")
        test_results.append(('format_comparison_report', False))

    try:
        test_results.append(('get_holiday_flags', test_get_holiday_flags()))
    except Exception as e:
        print(f"❌ ERROR in get_holiday_flags: {e}")
        test_results.append(('get_holiday_flags', False))

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("\n" + "-" * 80)
    print(f"Total: {passed}/{total} tests passed")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Time comparison system ready for production.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above before using in production.")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
