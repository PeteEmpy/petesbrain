#!/usr/bin/env python3
"""
Weekly Backup Audit
Tests backup restoration and verifies task counts

Run every Monday to ensure backups are recoverable
"""

import json
import sys
import os
import tarfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.petesbrain-weekly-audit.log')),
        logging.StreamHandler()
    ]
)

BASE_DIR = Path("/Users/administrator/Documents/PetesBrain.nosync")
LOCAL_BACKUP_DIR = BASE_DIR / "_backups" / "tasks"
PRODUCTION_DIR = BASE_DIR / "clients"

def get_latest_backup():
    """Find the most recent backup file"""
    backups = list(LOCAL_BACKUP_DIR.glob("tasks-backup-*.tar.gz"))
    if not backups:
        return None
    return max(backups, key=lambda p: p.stat().st_mtime)

def count_production_tasks():
    """Count tasks in production"""
    total = 0
    for client_dir in PRODUCTION_DIR.iterdir():
        if not client_dir.is_dir():
            continue

        tasks_file = client_dir / "tasks.json"
        if not tasks_file.exists():
            continue

        try:
            with open(tasks_file, 'r') as f:
                data = json.load(f)
                if 'tasks' in data:
                    total += len(data['tasks'])
        except Exception as e:
            logging.warning(f"Could not read {tasks_file}: {e}")

    return total

def count_backup_tasks(backup_path):
    """Count tasks in backup tarball"""
    total = 0
    with tarfile.open(backup_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if not member.name.endswith('tasks.json'):
                continue

            try:
                f = tar.extractfile(member)
                if f is None:
                    continue

                content = f.read()
                try:
                    content_str = content.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = content.decode('latin-1')

                data = json.loads(content_str)
                if 'tasks' in data:
                    total += len(data['tasks'])
            except Exception as e:
                logging.warning(f"Could not parse {member.name}: {e}")

    return total

def test_restoration(backup_path):
    """Test restoring backup to temp directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        logging.info(f"Testing restoration to: {tmpdir}")

        try:
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.extractall(tmpdir)

            # Count files extracted
            task_files = list(Path(tmpdir).rglob("tasks.json"))
            logging.info(f"Extracted {len(task_files)} task files")

            # Verify each file is valid JSON
            for task_file in task_files:
                try:
                    with open(task_file, 'r') as f:
                        json.load(f)
                except Exception as e:
                    logging.error(f"Invalid JSON in extracted {task_file}: {e}")
                    return False

            logging.info("✅ All extracted files are valid JSON")
            return True

        except Exception as e:
            logging.error(f"Restoration test failed: {e}")
            return False

def run_weekly_audit():
    """Run the weekly backup audit"""
    logging.info("="*60)
    logging.info("WEEKLY BACKUP AUDIT")
    logging.info("="*60)

    # 1. Find latest backup
    latest_backup = get_latest_backup()
    if not latest_backup:
        logging.error("❌ No backups found in backup directory")
        return False

    logging.info(f"Latest backup: {latest_backup.name}")
    backup_age = (datetime.now() - datetime.fromtimestamp(latest_backup.stat().st_mtime))
    logging.info(f"Backup age: {backup_age}")

    if backup_age.total_seconds() > 86400:  # More than 24 hours old
        logging.warning(f"⚠️ Backup is more than 24 hours old")

    # 2. Count production tasks
    prod_tasks = count_production_tasks()
    logging.info(f"Production tasks: {prod_tasks}")

    # 3. Count backup tasks
    backup_tasks = count_backup_tasks(latest_backup)
    logging.info(f"Backup tasks: {backup_tasks}")

    # 4. Compare counts
    if prod_tasks == 0:
        logging.error("❌ Production has 0 tasks - possible data loss")
        return False

    if backup_tasks == 0:
        logging.error("❌ Backup has 0 tasks - backup is corrupt")
        return False

    diff = abs(prod_tasks - backup_tasks)
    diff_pct = (diff / prod_tasks) * 100 if prod_tasks > 0 else 0

    if diff_pct > 20:
        logging.warning(f"⚠️ Task count differs by {diff_pct:.1f}% ({prod_tasks} prod vs {backup_tasks} backup)")
    else:
        logging.info(f"✅ Task counts are similar (±{diff_pct:.1f}%)")

    # 5. Test restoration
    logging.info("Testing backup restoration...")
    if not test_restoration(latest_backup):
        logging.error("❌ Restoration test failed")
        return False

    logging.info("✅ Restoration test passed")

    # 6. Summary
    logging.info("="*60)
    logging.info("AUDIT SUMMARY")
    logging.info("="*60)
    logging.info(f"  Backup file: {latest_backup.name}")
    logging.info(f"  Backup age: {backup_age}")
    logging.info(f"  Production tasks: {prod_tasks}")
    logging.info(f"  Backup tasks: {backup_tasks}")
    logging.info(f"  Difference: {diff} tasks ({diff_pct:.1f}%)")
    logging.info("  Restoration: PASSED ✅")
    logging.info("="*60)
    logging.info("✅ WEEKLY AUDIT PASSED")

    return True

if __name__ == '__main__':
    success = run_weekly_audit()
    sys.exit(0 if success else 1)
