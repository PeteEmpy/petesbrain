#!/usr/bin/env python3
"""
Test script for GoogleAdsChangeProtector wrapper

This script tests the exception-based enforcement mechanism to verify it works as expected.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from enforced_google_ads_wrapper import GoogleAdsChangeProtector, GoogleAdsChangeProtectionError

def test_wrapper_enforcement():
    """
    Test that the wrapper raises GoogleAdsChangeProtectionError when permission is requested.

    This simulates what Claude Code should do:
    1. Create backup
    2. Request permission (which raises exception)
    3. Catch exception and ask user for approval
    """

    print("=" * 80)
    print("Testing GoogleAdsChangeProtector Exception Enforcement")
    print("=" * 80)
    print()

    # Initialize protector
    protector = GoogleAdsChangeProtector()

    # Step 1: Create backup (simulating Chatsworth Inns negative keywords scenario)
    print("Step 1: Creating backup...")
    backup_file = protector.create_backup(
        customer_id='5898250490',
        change_description='Test: Add 15 negative keywords to campaign 2080736142',
        expected_changes={
            'negative_keywords_added': 15,
            'keywords': [
                {'text': 'hide', 'match_type': 'EXACT'},
                {'text': 'hide', 'match_type': 'PHRASE'},
                {'text': 'pilsley', 'match_type': 'EXACT'},
                # ... (abbreviated for test)
            ]
        },
        current_state={
            'existing_negative_keywords': 206,
            'campaign_status': 'ENABLED'
        }
    )

    print(f"✅ Backup created: {backup_file}")
    print()

    # Step 2: Request permission (THIS SHOULD RAISE EXCEPTION)
    print("Step 2: Requesting permission (should raise exception)...")
    print()

    try:
        protector.request_permission(backup_file)

        # If we get here, the enforcement FAILED (no exception was raised)
        print("❌ TEST FAILED: No exception was raised!")
        print("The wrapper did not enforce the protocol correctly.")
        return False

    except GoogleAdsChangeProtectionError as e:
        # This is the CORRECT behavior - exception was raised
        print("✅ TEST PASSED: GoogleAdsChangeProtectionError was raised!")
        print()
        print("Exception message:")
        print("-" * 80)
        print(str(e))
        print("-" * 80)
        print()
        print("✅ Claude Code would now stop and ask user for approval")
        print("✅ Only after user says 'yes' would execution proceed")
        print()
        return True

    except Exception as e:
        # Unexpected exception type
        print(f"❌ TEST FAILED: Unexpected exception type: {type(e).__name__}")
        print(f"Exception: {e}")
        return False

def test_check_protected_tool():
    """Test that protected tools are correctly identified."""

    print("=" * 80)
    print("Testing Protected Tool Detection")
    print("=" * 80)
    print()

    protector = GoogleAdsChangeProtector()

    test_cases = [
        ('mcp__google-ads__add_campaign_negative_keywords', True),
        ('mcp__google-ads__update_campaign_budget', True),
        ('mcp__google-ads__run_gaql', False),  # Read-only, not protected
        ('mcp__google-ads__list_accounts', False),  # Read-only, not protected
    ]

    all_passed = True

    for tool_name, should_be_protected in test_cases:
        is_protected = protector.check_if_protected_tool(tool_name)

        if is_protected == should_be_protected:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False

        expected = "protected" if should_be_protected else "not protected"
        actual = "protected" if is_protected else "not protected"

        print(f"{status}: {tool_name}")
        print(f"  Expected: {expected}, Actual: {actual}")
        print()

    return all_passed

if __name__ == "__main__":
    print()
    print("🧪 Google Ads Change Protection Wrapper - Test Suite")
    print()

    # Run tests
    test1_passed = test_check_protected_tool()
    test2_passed = test_wrapper_enforcement()

    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Protected Tool Detection: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Exception Enforcement: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print()

    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED")
        print()
        print("The GoogleAdsChangeProtector wrapper is working correctly.")
        print("Claude Code will be forced to stop and ask for approval before making changes.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("The wrapper needs fixes before it can enforce the protocol.")
        sys.exit(1)
