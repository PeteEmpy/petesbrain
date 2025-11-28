#!/usr/bin/env python3
"""
Daily Full Backup Agent
Backs up entire PetesBrain project to local + iCloud
Runs at system boot
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def main():
    """Main backup routine"""
    print("=" * 60)
    print("Daily Full Backup Agent")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Configuration
    project_dir = Path("/Users/administrator/Documents/PetesBrain")
    local_backup_dir = Path("/Users/administrator/Documents")
    icloud_backup_dir = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups"

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_name = f"PetesBrain-backup-{timestamp}.tar.gz"

    max_local = 5
    max_icloud = 10

    # Ensure iCloud directory exists
    icloud_backup_dir.mkdir(parents=True, exist_ok=True)

    # Change to backup directory
    os.chdir(local_backup_dir)

    print(f"📦 Creating backup archive: {backup_name}")
    print(f"   Source: {project_dir}")
    print(f"   Size: {get_dir_size(project_dir):.1f} GB")

    # Build tar command with exclusions
    tar_cmd = [
        'tar', '-czf', backup_name,
        '--exclude=PetesBrain/*/venv',
        '--exclude=PetesBrain/*/node_modules',
        '--exclude=PetesBrain/*/.venv',
        '--exclude=PetesBrain/*/__pycache__',
        '--exclude=PetesBrain/.git',
        'PetesBrain'
    ]

    # Execute tar backup
    try:
        result = subprocess.run(
            tar_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            print("⚠️  tar completed with warnings:")
            if result.stderr:
                # Show first 5 lines of errors
                error_lines = result.stderr.strip().split('\n')[:5]
                for line in error_lines:
                    print(f"   {line}")
        else:
            print("✅ Archive created successfully")

    except subprocess.TimeoutExpired:
        print("❌ Backup timed out after 10 minutes")
        return 1
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return 1

    # Check backup file was created
    backup_path = local_backup_dir / backup_name
    if not backup_path.exists():
        print("❌ Backup file was not created")
        return 1

    backup_size = backup_path.stat().st_size / (1024 * 1024)  # MB
    print(f"✅ Local backup created: {backup_size:.1f} MB")

    # Copy to iCloud
    try:
        icloud_path = icloud_backup_dir / backup_name
        shutil.copy2(backup_path, icloud_path)
        print(f"✅ Copied to iCloud: {icloud_path}")
    except Exception as e:
        print(f"⚠️  Could not copy to iCloud: {e}")

    # Cleanup old local backups
    cleanup_old_backups(local_backup_dir, "PetesBrain-backup-*.tar.gz", max_local)

    # Cleanup old iCloud backups
    cleanup_old_backups(icloud_backup_dir, "PetesBrain-backup-*.tar.gz", max_icloud)

    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backup location: {backup_path}")
    print(f"Backup size: {backup_size:.1f} MB")
    print("=" * 60)

    return 0

def get_dir_size(path):
    """Get directory size in GB"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total / (1024 ** 3)  # GB

def cleanup_old_backups(directory, pattern, keep_count):
    """Remove old backups, keeping only the most recent N"""
    try:
        # Find all matching backup files
        backups = sorted(
            directory.glob(pattern),
            key=lambda x: x.stat().st_mtime,
            reverse=True  # Newest first
        )

        # Remove old backups beyond keep_count
        removed = 0
        for old_backup in backups[keep_count:]:
            old_backup.unlink()
            removed += 1
            print(f"🗑️  Removed old backup: {old_backup.name}")

        if removed > 0:
            print(f"✅ Cleaned up {removed} old backup(s) from {directory.name}")

    except Exception as e:
        print(f"⚠️  Error during cleanup in {directory}: {e}")

if __name__ == '__main__':
    sys.exit(main())
