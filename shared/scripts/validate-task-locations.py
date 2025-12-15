#!/usr/bin/env python3
"""
Task Location Validator

Permanent guard against product-feeds/tasks.json file recurrence.

This script:
1. Runs on system startup (LaunchAgent)
2. Scans for ANY product-feeds/tasks.json files
3. Alerts immediately if found (indicates regression)
4. Logs findings to audit trail

Why This Exists:
- Product-feeds/tasks.json files were a legacy artifact that kept reappearing
- Multiple "fixes" failed because no guard prevented recreation
- This validation serves as early warning system
- If this script ever finds product-feeds/tasks.json, it indicates:
  a) Someone manually recreated them
  b) A new script started writing to product-feeds
  c) A backup was restored without consolidation
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / 'clients'
AUDIT_LOG = PROJECT_ROOT / 'data' / 'state' / 'tasks-audit.log'


def scan_for_product_feeds_tasks():
    """Scan all client directories for product-feeds/tasks.json files"""
    critical_violations = []
    archived_violations = []

    if not CLIENTS_DIR.exists():
        return critical_violations, archived_violations

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        # CRITICAL: Check for active product-feeds/tasks*.json (all variants)
        pf_dir = client_dir / 'product-feeds'
        if pf_dir.exists() and pf_dir.is_dir():
            for pf_task_file in pf_dir.glob('tasks*.json'):
                # Skip archived files
                if '_archived' in str(pf_task_file):
                    continue
                critical_violations.append({
                    'client': client_dir.name,
                    'path': str(pf_task_file),
                    'file_name': pf_task_file.name,
                    'file_size': pf_task_file.stat().st_size,
                    'modified': datetime.fromtimestamp(pf_task_file.stat().st_mtime).isoformat(),
                    'discovered_at': datetime.now().isoformat(),
                    'severity': 'CRITICAL'
                })

        # WARNING: Check for archived product-feeds tasks (historical, less urgent)
        archived_pf = client_dir / 'product-feeds' / '_archived-tasks' / 'tasks.json'
        if archived_pf.exists():
            archived_violations.append({
                'client': client_dir.name,
                'path': str(archived_pf),
                'file_size': archived_pf.stat().st_size,
                'modified': datetime.fromtimestamp(archived_pf.stat().st_mtime).isoformat(),
                'discovered_at': datetime.now().isoformat(),
                'severity': 'WARNING',
                'note': 'Archived product-feeds location (historical, can be cleaned later)'
            })

    return critical_violations, archived_violations


def log_violations(critical_violations, archived_violations):
    """Log violations to audit trail"""
    if not critical_violations and not archived_violations:
        return

    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()
    log_entry = f"\n{'='*80}\n"

    if critical_violations:
        log_entry += f"🚨 CRITICAL: Active product-feeds task files detected! ({timestamp})\n"
    elif archived_violations:
        log_entry += f"⚠️  WARNING: Archived product-feeds task files found ({timestamp})\n"

    log_entry += f"{'='*80}\n"

    if critical_violations:
        log_entry += f"CRITICAL violations ({len(critical_violations)}):\n\n"
        for i, violation in enumerate(critical_violations, 1):
            log_entry += f"{i}. {violation['client']}\n"
            log_entry += f"   Path: {violation['path']}\n"
            log_entry += f"   Size: {violation['file_size']} bytes\n"
            log_entry += f"   Modified: {violation['modified']}\n"
            log_entry += "\n"

    if archived_violations:
        if critical_violations:
            log_entry += f"\nWARNING violations ({len(archived_violations)}):\n\n"
        else:
            log_entry += f"Found {len(archived_violations)} archived violations:\n\n"
        for i, violation in enumerate(archived_violations, 1):
            log_entry += f"{i}. {violation['client']} (archived)\n"
            log_entry += f"   Path: {violation['path']}\n"
            log_entry += f"   Modified: {violation['modified']}\n"
            log_entry += "\n"

    log_entry += f"ACTION:\n"
    if critical_violations:
        log_entry += f"- CRITICAL: Remove active product-feeds/tasks.json immediately\n"
        log_entry += f"- Check git log to see what recreated them\n"
        log_entry += f"- Check for any new scripts writing to product-feeds\n"
        log_entry += f"- Re-run consolidation if tasks were lost\n"
        log_entry += f"- Verify ClientTasksService guard is preventing writes\n"
    if archived_violations:
        log_entry += f"- Clean archived files: find {CLIENTS_DIR} -path '*/_archived-tasks/tasks.json' -delete\n"
    log_entry += f"- See: docs/ARCHITECTURAL-MIGRATION-DEC10-2025.md\n"
    log_entry += f"\n{'='*80}\n"

    with open(AUDIT_LOG, 'a') as f:
        f.write(log_entry)


def alert_user(critical_violations, archived_violations):
    """Alert user to violations"""
    if not critical_violations and not archived_violations:
        return False

    print("\n" + "="*80)

    if critical_violations:
        print("🚨 CRITICAL ALERT: Active product-feeds task files detected!")
        print("="*80)
        print(f"\nCRITICAL violations ({len(critical_violations)}):")
        print()

        for violation in critical_violations:
            print(f"  ❌ {violation['client']}")
            print(f"     {violation['path']}")
            print(f"     Modified: {violation['modified']}")
            print()

        print("This indicates one of:")
        print("  1. Someone manually recreated product-feeds/tasks.json")
        print("  2. A new script is writing to product-feeds (bug)")
        print("  3. A backup was restored without consolidation")
        print()
        print("IMMEDIATE ACTION REQUIRED:")
        print("  1. Delete files: find clients -path '*/product-feeds/tasks.json' ! -path '*/_archived*' -delete")
        print("  2. Check git log to see what created these files")
        print("  3. Check for any scripts still referencing product-feeds")
        print("  4. Verify ClientTasksService guard is preventing writes")
        print()

    if archived_violations:
        if critical_violations:
            print("="*80)
            print(f"⚠️  WARNING: Archived product-feeds task files found ({len(archived_violations)})")
            print("="*80)
            print("\nThese are in _archived-tasks/ (historical, lower priority)")
        else:
            print("⚠️  WARNING: Archived product-feeds task files found")
            print("="*80)
            print(f"\nFound {len(archived_violations)} archived violation(s):")

        print("\nThese should eventually be cleaned up:")
        print("  find clients -path '*/_archived-tasks/tasks.json' -delete")
        print()

    print("See: docs/ARCHITECTURAL-MIGRATION-DEC10-2025.md")
    print("="*80 + "\n")

    return bool(critical_violations)


def main():
    """Main validation function - FAIL-FAST if violations found"""
    critical_violations, archived_violations = scan_for_product_feeds_tasks()

    if critical_violations or archived_violations:
        # Log to audit trail
        log_violations(critical_violations, archived_violations)

        # Alert user
        is_critical = alert_user(critical_violations, archived_violations)

        # FAIL-FAST: Exit with error code if ANY violations found (critical or archived)
        # This ensures operations that depend on validation will fail
        if is_critical:
            print("\n❌ CRITICAL: Validation failed - operations blocked until fixed")
        else:
            print("\n⚠️  WARNING: Validation found archived violations - review recommended")
        
        return 1  # Always fail if violations found
    else:
        # All clear
        print(f"✅ Task location validation passed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print("   No product-feeds/tasks.json files detected")
        return 0


if __name__ == '__main__':
    sys.exit(main())
