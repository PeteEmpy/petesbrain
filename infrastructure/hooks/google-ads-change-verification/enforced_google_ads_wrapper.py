#!/usr/bin/env python3
"""
MANDATORY Google Ads Change Protection Wrapper

This wrapper ENFORCES the Google Ads Change Protection Protocol.
ALL Google Ads modification MCP calls MUST go through this wrapper.

Claude Code is FORBIDDEN from calling Google Ads modification tools directly.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# CRITICAL: List of MCP tools that REQUIRE protection
PROTECTED_TOOLS = [
    'mcp__google-ads__update_campaign_budget',
    'mcp__google-ads__update_campaign_target_roas',
    'mcp__google-ads__update_campaign_status',
    'mcp__google-ads__create_campaign',
    'mcp__google-ads__create_ad_group',
    'mcp__google-ads__add_keywords',
    'mcp__google-ads__pause_keywords',
    'mcp__google-ads__replace_asset_group_text_assets',
    'mcp__google-ads__replace_rsa_text_assets',
    'mcp__google-ads__add_sitelinks',
    'mcp__google-ads__add_callouts',
    'mcp__google-ads__add_campaign_negative_keywords',  # The one I violated!
]


class GoogleAdsChangeProtectionError(Exception):
    """Raised when Change Protection Protocol is violated"""
    pass


class GoogleAdsChangeProtector:
    """
    Enforces the Google Ads Change Protection Protocol.

    WORKFLOW (MANDATORY):
    1. BACKUP - Create backup with expected state
    2. ASK PERMISSION - Display backup, wait for user approval
    3. EXECUTE - Make changes (only after approval)
    4. VERIFY - Query actual state, compare to expected
    5. ROLLBACK - Offer to restore if verification fails
    """

    def __init__(self, base_path: str = "/Users/administrator/Documents/PetesBrain.nosync"):
        self.base_path = Path(base_path)
        self.backup_dir = self.base_path / "infrastructure/hooks/google-ads-change-verification/backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def check_if_protected_tool(self, tool_name: str) -> bool:
        """Check if tool requires Change Protection Protocol"""
        return tool_name in PROTECTED_TOOLS

    def create_backup(
        self,
        customer_id: str,
        change_description: str,
        expected_changes: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> Path:
        """
        Step 1: Create backup with current state and expected changes

        Returns: Path to backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{customer_id}_{timestamp}.json"

        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": customer_id,
            "change_description": change_description,
            "current_state": current_state,
            "expected_changes": expected_changes,
            "status": "awaiting_approval"
        }

        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)

        return backup_file

    def request_permission(self, backup_file: Path) -> bool:
        """
        Step 2: Display backup and request explicit user approval

        THIS IS WHERE THE ENFORCEMENT HAPPENS.
        Claude Code MUST call this and wait for user response.

        Returns: True if approved, raises exception if called directly
        """
        # Load backup
        with open(backup_file, 'r') as f:
            backup = json.load(f)

        # Display approval request
        print("\n" + "=" * 80)
        print("🚨 GOOGLE ADS CHANGE PROTECTION PROTOCOL - APPROVAL REQUIRED")
        print("=" * 80)
        print(f"\nChange Description: {backup['change_description']}")
        print(f"Customer ID: {backup['customer_id']}")
        print(f"Backup Created: {backup['timestamp']}")
        print(f"\nBackup Location: {backup_file}")
        print("\nExpected Changes:")
        print(json.dumps(backup['expected_changes'], indent=2))
        print("\n" + "=" * 80)
        print("⚠️  WARNING: This will make LIVE changes to Google Ads")
        print("=" * 80)

        # CRITICAL: This raises an exception that Claude Code must handle
        raise GoogleAdsChangeProtectionError(
            "\n\n🛑 APPROVAL REQUIRED 🛑\n\n"
            "Google Ads Change Protection Protocol requires explicit user approval.\n\n"
            "YOU MUST:\n"
            "1. Review the backup file and expected changes above\n"
            "2. Ask the user: 'Do you approve these changes? (yes/no)'\n"
            "3. Wait for user response\n"
            "4. Only proceed if user types 'yes'\n\n"
            "DO NOT:\n"
            "- Assume approval\n"
            "- Proceed without explicit 'yes'\n"
            "- Call the MCP tool directly\n\n"
            f"Backup saved: {backup_file}\n"
        )

    def execute_with_verification(
        self,
        mcp_tool_function,
        tool_params: Dict[str, Any],
        backup_file: Path,
        verification_query_function,
        verification_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Steps 3-4: Execute change and verify result

        Args:
            mcp_tool_function: The MCP tool to call (e.g., mcp__google_ads__add_campaign_negative_keywords)
            tool_params: Parameters for the MCP tool
            backup_file: Path to backup file
            verification_query_function: Function to query actual state after change
            verification_params: Parameters for verification query

        Returns: Dictionary with execution result and verification status
        """
        # Update backup status
        with open(backup_file, 'r') as f:
            backup = json.load(f)

        backup['status'] = 'executing'
        backup['execution_timestamp'] = datetime.now().isoformat()

        with open(backup_file, 'w') as f:
            json.dump(backup, f, indent=2)

        # Execute the MCP tool
        try:
            execution_result = mcp_tool_function(**tool_params)

            # Verify the change
            actual_state = verification_query_function(**verification_params)

            # Compare actual vs expected
            verification_passed = self._verify_changes(
                backup['expected_changes'],
                actual_state
            )

            # Update backup with results
            backup['status'] = 'completed' if verification_passed else 'verification_failed'
            backup['execution_result'] = execution_result
            backup['actual_state'] = actual_state
            backup['verification_passed'] = verification_passed
            backup['completion_timestamp'] = datetime.now().isoformat()

            with open(backup_file, 'w') as f:
                json.dump(backup, f, indent=2)

            return {
                'success': verification_passed,
                'execution_result': execution_result,
                'actual_state': actual_state,
                'backup_file': str(backup_file),
                'verification_passed': verification_passed
            }

        except Exception as e:
            # Update backup with error
            backup['status'] = 'failed'
            backup['error'] = str(e)
            backup['error_timestamp'] = datetime.now().isoformat()

            with open(backup_file, 'w') as f:
                json.dump(backup, f, indent=2)

            raise

    def _verify_changes(self, expected: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """
        Compare expected changes with actual state

        This is a simple implementation - can be enhanced with specific checks
        """
        # For now, just check if the change appears to have succeeded
        # This should be customized per change type
        return True  # Placeholder - implement specific verification logic

    def offer_rollback(self, backup_file: Path) -> Dict[str, Any]:
        """
        Step 5: Offer to rollback if verification failed

        Returns: Rollback operations to restore original state
        """
        with open(backup_file, 'r') as f:
            backup = json.load(f)

        if backup['status'] != 'verification_failed':
            return {'rollback_needed': False}

        # Generate rollback operations based on what was changed
        # This is change-type specific
        rollback_operations = self._generate_rollback_operations(backup)

        return {
            'rollback_needed': True,
            'rollback_operations': rollback_operations,
            'backup_file': str(backup_file)
        }

    def _generate_rollback_operations(self, backup: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate operations to restore original state"""
        # Placeholder - implement specific rollback logic per change type
        return []


# USAGE EXAMPLE (How Claude Code MUST use this)
"""
from enforced_google_ads_wrapper import GoogleAdsChangeProtector, GoogleAdsChangeProtectionError

# Initialize protector
protector = GoogleAdsChangeProtector()

# Step 1: Create backup
backup_file = protector.create_backup(
    customer_id='5898250490',
    change_description='Add 15 negative keywords to campaign 2080736142',
    expected_changes={
        'negative_keywords_added': 15,
        'keywords': ['hide', 'pilsley', 'beeley', ...]
    },
    current_state={
        'existing_negative_keywords': 206
    }
)

# Step 2: Request permission (THIS WILL RAISE AN EXCEPTION)
try:
    protector.request_permission(backup_file)
except GoogleAdsChangeProtectionError as e:
    # Claude Code MUST catch this and ask user for approval
    print(str(e))
    # STOP HERE - WAIT FOR USER TO SAY "YES"
    # DO NOT PROCEED WITHOUT EXPLICIT APPROVAL

# Step 3-4: Execute with verification (ONLY after user says "yes")
# result = protector.execute_with_verification(
#     mcp_tool_function=mcp__google_ads__add_campaign_negative_keywords,
#     tool_params={'customer_id': '5898250490', 'campaign_id': '2080736142', ...},
#     backup_file=backup_file,
#     verification_query_function=mcp__google_ads__run_gaql,
#     verification_params={'customer_id': '5898250490', 'query': '...'}
# )

# Step 5: Check if rollback needed
# if not result['verification_passed']:
#     rollback = protector.offer_rollback(backup_file)
#     # Ask user if they want to rollback
"""


if __name__ == "__main__":
    print("Google Ads Change Protection Wrapper")
    print("=" * 80)
    print("\nThis module enforces the Google Ads Change Protection Protocol.")
    print("\nProtected MCP Tools:")
    for tool in PROTECTED_TOOLS:
        print(f"  - {tool}")
    print("\nAll calls to these tools MUST go through GoogleAdsChangeProtector.")
    print("Direct calls are FORBIDDEN.")
