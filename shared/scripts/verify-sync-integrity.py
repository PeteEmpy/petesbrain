#!/usr/bin/env python3

"""
PetesBrain Sync Integrity Verification System

Calculates and verifies SHA-256 checksums for critical files to prevent
silent data corruption during sync operations.

Usage:
    python3 verify-sync-integrity.py pre-sync    # Calculate baseline checksums
    python3 verify-sync-integrity.py post-sync   # Verify checksums match
    python3 verify-sync-integrity.py update      # Update checksum database

Exit codes:
    0 - Verification passed
    1 - Verification failed (corruption detected)
    2 - Checksum database missing (first run)
"""

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
CHECKSUM_FILE = PROJECT_ROOT / ".sync-checksums.json"
CHECKSUM_BACKUP = PROJECT_ROOT / ".sync-checksums.json.backup"

# Critical files to track (relative to PROJECT_ROOT)
CRITICAL_PATTERNS = [
    "clients/*/tasks.json",
    "clients/*/CONTEXT.md",
    "clients/*/tasks-completed.md",
    "data/state/*.json",
    ".mcp.json",
    "roksys/tasks.json",
    "roksys/tasks-completed.md",
]

# Files to exclude from checksum verification
EXCLUDE_PATTERNS = [
    "*.pyc",
    "__pycache__/*",
    ".git/*",
    "venv/*",
    ".venv/*",
    "*.log",
    ".DS_Store",
    ".sync-checksums.json",
    ".sync-snapshot/*",
    "data/cache/*",
    "data/alerts/*",
]


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def should_exclude(file_path: Path) -> bool:
    """Check if file matches any exclude pattern."""
    relative_path = file_path.relative_to(PROJECT_ROOT)
    path_str = str(relative_path)

    for pattern in EXCLUDE_PATTERNS:
        # Simple wildcard matching
        if "*" in pattern:
            pattern_parts = pattern.split("*")
            if all(part in path_str for part in pattern_parts if part):
                return True
        elif path_str == pattern or path_str.endswith(pattern):
            return True

    return False


def find_critical_files() -> List[Path]:
    """Find all critical files matching patterns."""
    files = []

    for pattern in CRITICAL_PATTERNS:
        # Convert glob pattern to pathlib
        for file_path in PROJECT_ROOT.glob(pattern):
            if file_path.is_file() and not should_exclude(file_path):
                files.append(file_path)

    return sorted(files)


def calculate_checksums() -> Dict[str, Dict]:
    """Calculate checksums for all critical files."""
    print(f"Calculating checksums for critical files...")

    critical_files = find_critical_files()
    checksums = {}

    for file_path in critical_files:
        try:
            relative_path = str(file_path.relative_to(PROJECT_ROOT))
            checksum = calculate_sha256(file_path)
            file_size = file_path.stat().st_size

            checksums[relative_path] = {
                "sha256": checksum,
                "size": file_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }

            print(f"  ✓ {relative_path}: {checksum[:16]}...")

        except Exception as e:
            print(f"  ✗ Error calculating checksum for {file_path}: {e}", file=sys.stderr)
            continue

    print(f"\nCalculated checksums for {len(checksums)} files")
    return checksums


def load_checksums() -> Dict:
    """Load checksums from database file."""
    if not CHECKSUM_FILE.exists():
        return None

    try:
        with open(CHECKSUM_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading checksums: {e}", file=sys.stderr)
        return None


def save_checksums(checksums: Dict[str, Dict], metadata: Dict = None):
    """Save checksums to database file."""
    # Backup existing checksums
    if CHECKSUM_FILE.exists():
        CHECKSUM_FILE.rename(CHECKSUM_BACKUP)

    data = {
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "hostname": os.uname().nodename,
        "metadata": metadata or {},
        "checksums": checksums,
    }

    try:
        with open(CHECKSUM_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Checksums saved to {CHECKSUM_FILE}")
    except Exception as e:
        print(f"✗ Error saving checksums: {e}", file=sys.stderr)
        # Restore backup
        if CHECKSUM_BACKUP.exists():
            CHECKSUM_BACKUP.rename(CHECKSUM_FILE)
        sys.exit(1)


def verify_checksums(baseline: Dict) -> bool:
    """Verify current checksums against baseline."""
    print(f"Verifying data integrity against baseline...")

    current_checksums = calculate_checksums()
    baseline_checksums = baseline.get("checksums", {})

    # Check for missing files
    baseline_files = set(baseline_checksums.keys())
    current_files = set(current_checksums.keys())

    missing_files = baseline_files - current_files
    new_files = current_files - baseline_files

    corruption_detected = False

    if missing_files:
        print(f"\n🚨 WARNING: {len(missing_files)} file(s) MISSING:", file=sys.stderr)
        for file in sorted(missing_files):
            print(f"  ✗ {file}", file=sys.stderr)
        corruption_detected = True

    if new_files:
        print(f"\n✓ {len(new_files)} new file(s) added:")
        for file in sorted(new_files):
            print(f"  + {file}")

    # Verify checksums for existing files
    mismatches = []
    for file_path, current_data in current_checksums.items():
        if file_path not in baseline_checksums:
            continue

        baseline_data = baseline_checksums[file_path]

        if current_data["sha256"] != baseline_data["sha256"]:
            mismatches.append({
                "file": file_path,
                "baseline": baseline_data["sha256"],
                "current": current_data["sha256"],
                "baseline_size": baseline_data["size"],
                "current_size": current_data["size"],
            })

    if mismatches:
        print(f"\n🚨 CORRUPTION DETECTED: {len(mismatches)} file(s) modified:", file=sys.stderr)
        for mismatch in mismatches:
            print(f"\n  ✗ {mismatch['file']}", file=sys.stderr)
            print(f"    Baseline: {mismatch['baseline'][:16]}... (size: {mismatch['baseline_size']})", file=sys.stderr)
            print(f"    Current:  {mismatch['current'][:16]}... (size: {mismatch['current_size']})", file=sys.stderr)
        corruption_detected = True
    else:
        verified_count = len(set(current_checksums.keys()) & set(baseline_checksums.keys()))
        print(f"\n✓ All {verified_count} existing file(s) verified successfully")

    return not corruption_detected


def pre_sync_check():
    """Pre-sync integrity check: Calculate baseline checksums."""
    print("=== PRE-SYNC INTEGRITY CHECK ===\n")

    checksums = calculate_checksums()

    metadata = {
        "phase": "pre-sync",
        "operation": "baseline",
    }

    save_checksums(checksums, metadata)

    print("\n✓ Pre-sync baseline checksums calculated")
    print(f"  Total files tracked: {len(checksums)}")
    return 0


def post_sync_check():
    """Post-sync integrity check: Verify checksums match baseline."""
    print("=== POST-SYNC INTEGRITY CHECK ===\n")

    baseline = load_checksums()

    if baseline is None:
        print("⚠ No baseline checksums found", file=sys.stderr)
        print("This is normal for first run. Run 'pre-sync' first.", file=sys.stderr)
        return 2

    baseline_timestamp = baseline.get("timestamp", "unknown")
    baseline_hostname = baseline.get("hostname", "unknown")

    print(f"Baseline from: {baseline_timestamp}")
    print(f"Baseline machine: {baseline_hostname}")
    print(f"Current machine: {os.uname().nodename}\n")

    if verify_checksums(baseline):
        print("\n✅ POST-SYNC VERIFICATION PASSED")
        print("All critical files verified - no corruption detected")

        # Update checksums with post-sync state
        current_checksums = calculate_checksums()
        metadata = {
            "phase": "post-sync",
            "operation": "verified",
            "baseline_timestamp": baseline_timestamp,
        }
        save_checksums(current_checksums, metadata)

        return 0
    else:
        print("\n❌ POST-SYNC VERIFICATION FAILED", file=sys.stderr)
        print("Data corruption detected - sync should be rolled back", file=sys.stderr)
        return 1


def update_checksums():
    """Manually update checksum database (for intentional changes)."""
    print("=== UPDATING CHECKSUM DATABASE ===\n")

    print("⚠ This will update the baseline checksums to current state")
    print("Only use this if you've intentionally modified critical files\n")

    response = input("Continue? (yes/no): ")
    if response.lower() != "yes":
        print("Update cancelled")
        return 0

    checksums = calculate_checksums()

    metadata = {
        "phase": "manual-update",
        "operation": "baseline",
        "note": "Manually updated checksums",
    }

    save_checksums(checksums, metadata)

    print("\n✓ Checksum database updated")
    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: verify-sync-integrity.py {pre-sync|post-sync|update}", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "pre-sync":
            exit_code = pre_sync_check()
        elif command == "post-sync":
            exit_code = post_sync_check()
        elif command == "update":
            exit_code = update_checksums()
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            print("Valid commands: pre-sync, post-sync, update", file=sys.stderr)
            exit_code = 1

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n\n🚨 FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
