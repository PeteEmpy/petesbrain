#!/usr/bin/env python3
"""
Gmail Scope Validator - Run BEFORE any Gmail operations

Validates that all Gmail OAuth scripts have ONLY gmail.modify scope.
gmail.modify includes all read permissions, so gmail.readonly is redundant and causes token conflicts.

This script prevents the recurring scope issue by:
1. Checking all Python files for incorrect SCOPES declarations
2. Validating token.json has correct scope
3. Failing fast with clear error message if misconfigured

Run this at the start of email-sync-workflow or LaunchAgent startup.
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Tuple

# Directory containing email sync scripts
SCRIPT_DIR = Path(__file__).parent

# Expected scope (ONLY this - no gmail.readonly)
REQUIRED_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
FORBIDDEN_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

def check_python_files() -> List[Tuple[Path, str]]:
    """Check all Python files for incorrect SCOPES declarations."""
    errors = []

    py_files = [
        SCRIPT_DIR / 'sync_emails.py',
        SCRIPT_DIR / 'auto_label.py',
        SCRIPT_DIR / 'scan_personal_emails.py'
    ]

    for file_path in py_files:
        if not file_path.exists():
            continue

        content = file_path.read_text()

        # Check if file has SCOPES declaration
        if 'SCOPES' not in content:
            continue

        # Check for forbidden scope
        if FORBIDDEN_SCOPE in content:
            errors.append((file_path, f"Contains forbidden scope: {FORBIDDEN_SCOPE}"))

        # Check for required scope
        if REQUIRED_SCOPE not in content:
            errors.append((file_path, f"Missing required scope: {REQUIRED_SCOPE}"))

    return errors

def check_token_file() -> str | None:
    """Check token.json has correct scope."""
    token_file = SCRIPT_DIR / 'token.json'

    if not token_file.exists():
        return None  # No token yet - will be created on first auth

    try:
        with open(token_file, 'r') as f:
            token_data = json.load(f)

        scopes = token_data.get('scopes', [])

        # Check if has forbidden scope
        if FORBIDDEN_SCOPE in scopes:
            return f"Token has forbidden scope: {FORBIDDEN_SCOPE}"

        # Check if has required scope
        if REQUIRED_SCOPE not in scopes:
            return f"Token missing required scope: {REQUIRED_SCOPE}"

        return None  # All good

    except Exception as e:
        return f"Error reading token.json: {e}"

def main():
    """Validate Gmail OAuth configuration."""
    print("=" * 60)
    print("Gmail OAuth Scope Validator")
    print("=" * 60)

    all_errors = []

    # Check Python files
    print("\n1. Checking Python scripts for correct SCOPES...")
    py_errors = check_python_files()
    if py_errors:
        print("   ❌ FAILED - Found scope issues:")
        for file_path, error in py_errors:
            print(f"      {file_path.name}: {error}")
            all_errors.append(f"{file_path.name}: {error}")
    else:
        print("   ✅ PASSED - All scripts have correct SCOPES")

    # Check token file
    print("\n2. Checking token.json scope...")
    token_error = check_token_file()
    if token_error:
        print(f"   ❌ FAILED - {token_error}")
        all_errors.append(f"token.json: {token_error}")
    elif (SCRIPT_DIR / 'token.json').exists():
        print("   ✅ PASSED - Token has correct scope")
    else:
        print("   ⚠️  SKIP - No token.json found (will be created on first auth)")

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print("❌ VALIDATION FAILED")
        print("=" * 60)
        print("\nErrors found:")
        for error in all_errors:
            print(f"  - {error}")
        print("\n🔧 FIX:")
        print("  1. Update Python files to use ONLY gmail.modify scope")
        print("  2. Delete token.json and re-authenticate:")
        print("     cd ~/Documents/PetesBrain/shared/email-sync")
        print("     rm token.json")
        print("     .venv/bin/python3 sync_emails.py")
        print("")
        sys.exit(1)
    else:
        print("✅ ALL VALIDATIONS PASSED")
        print("=" * 60)
        print("\nGmail OAuth configuration is correct.")
        print("Safe to proceed with email sync operations.")
        print("")
        sys.exit(0)

if __name__ == '__main__':
    main()
