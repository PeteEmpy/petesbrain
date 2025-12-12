#!/usr/bin/env python3
"""
PetesBrain Credential Validation Script

Checks that all expected credentials exist, are readable, and have reasonable sizes.
Helps detect credential issues before they cause OAuth popups or agent failures.

Usage:
    python3 scripts/validate-credentials.py
    python3 scripts/validate-credentials.py --verbose
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print("=" * 60)
    print("PetesBrain Credential Validation")
    print("=" * 60)
    print()

    project_root = Path.home() / 'Documents/PetesBrain.nosync'
    credentials_to_check = get_expected_credentials()

    total = len(credentials_to_check)
    healthy = 0
    warnings = 0
    errors = 0

    # Check each credential
    for credential_info in credentials_to_check:
        cred_path = credential_info['path']
        cred_name = credential_info['name']

        # Expand path
        if str(cred_path).startswith('~'):
            full_path = Path(cred_path).expanduser()
        else:
            full_path = cred_path

        # Check if file exists
        if not full_path.exists():
            print(f"❌ MISSING: {cred_name}")
            if verbose:
                print(f"   Expected at: {full_path}")
            errors += 1
            continue

        # Check if readable
        if not full_path.is_file():
            print(f"❌ NOT A FILE: {cred_name}")
            if verbose:
                print(f"   Path: {full_path}")
            errors += 1
            continue

        # Check readability
        if not full_path.stat().st_mode & 0o400:
            print(f"⚠️  NOT READABLE: {cred_name}")
            if verbose:
                print(f"   Permissions: {oct(full_path.stat().st_mode)}")
            warnings += 1
            continue

        # Check file size (should not be empty or suspiciously small)
        size = full_path.stat().st_size
        if size == 0:
            print(f"⚠️  EMPTY FILE: {cred_name}")
            warnings += 1
            continue

        if size < 50:
            print(f"⚠️  SUSPICIOUSLY SMALL: {cred_name} ({size} bytes)")
            if verbose:
                print(f"   Credentials should be larger. May be corrupted.")
            warnings += 1
            continue

        # For JSON files, try to parse them
        if full_path.suffix == '.json':
            try:
                with open(full_path, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ INVALID JSON: {cred_name}")
                if verbose:
                    print(f"   Error: {e}")
                errors += 1
                continue
            except Exception as e:
                print(f"⚠️  COULD NOT READ: {cred_name}")
                if verbose:
                    print(f"   Error: {e}")
                warnings += 1
                continue

        # All checks passed
        if verbose:
            print(f"✅ {cred_name} ({size} bytes)")
        healthy += 1

    # Summary
    print()
    print("=" * 60)
    print(f"✅ Healthy:  {healthy}/{total}")
    print(f"⚠️  Warnings: {warnings}/{total}")
    print(f"❌ Errors:   {errors}/{total}")
    print("=" * 60)
    print()

    if errors > 0:
        print("🔴 CRITICAL ISSUES FOUND")
        print("Missing credentials may cause OAuth popups or agent failures.")
        print()
        print("Common fixes:")
        print("1. Re-authenticate MCP servers (delete ~/.config and re-auth)")
        print("2. Restore credentials from latest snapshot:")
        print("   python3 shared/rollback_manager.py list")
        print("   python3 shared/rollback_manager.py restore <snapshot-id> --force")
        return 1

    if warnings > 0:
        print("🟡 WARNINGS FOUND")
        print("Some credentials may have issues. Monitor carefully.")
        return 0

    print("🟢 ALL CREDENTIALS VALIDATED SUCCESSFULLY")
    return 0

def get_expected_credentials() -> List[Dict]:
    """Return list of credentials to validate."""
    project_root = Path.home() / 'Documents/PetesBrain.nosync'

    return [
        # MCP server credentials
        {
            'name': 'Google Sheets MCP credentials',
            'path': project_root / 'infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
        },
        {
            'name': 'Google Ads MCP credentials',
            'path': project_root / 'infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'
        },
        {
            'name': 'Google Drive MCP credentials',
            'path': project_root / 'infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json'
        },
        {
            'name': 'Google Photos MCP credentials',
            'path': project_root / 'infrastructure/mcp-servers/google-photos-mcp-server/credentials.json'
        },
        {
            'name': 'Google Tasks MCP credentials',
            'path': project_root / 'infrastructure/mcp-servers/google-tasks-mcp-server/credentials.json'
        },
        # System credentials
        {
            'name': 'Google Ads configuration',
            'path': '~/.google-ads/google-ads.yaml'
        },
        # OAuth credentials from .mcp.json
        {
            'name': 'Google Analytics OAuth',
            'path': Path.home() / 'Downloads/client_secret_512285153243-p5nnhlj4j62h5052glghlctmetc5bevp.apps.googleusercontent.com.json'
        },
    ]

if __name__ == '__main__':
    sys.exit(main())
