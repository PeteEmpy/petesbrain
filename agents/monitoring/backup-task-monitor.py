#!/usr/bin/env python3
"""
Backup Task Monitor

Monitors task backups for significant drops in task counts that could indicate data loss.
Runs daily to compare current task counts against the most recent backup.

Alerts if:
- Any client loses >50% of tasks
- Any client goes from N tasks to 0 tasks
- Total task count drops >30% across all clients

Part of PetesBrain backup monitoring system.
"""

import json
import tarfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / 'clients'
BACKUPS_DIR = PROJECT_ROOT / '_backups' / 'tasks'
ALERT_LOG = PROJECT_ROOT / 'data' / 'state' / 'backup-alerts.log'

# Ensure alert log directory exists
ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)


def get_current_task_counts() -> Dict[str, int]:
    """Get current task counts for all clients"""
    counts = {}

    if not CLIENTS_DIR.exists():
        return counts

    for client_dir in CLIENTS_DIR.iterdir():
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        tasks_file = client_dir / 'tasks.json'
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r') as f:
                    data = json.load(f)
                    counts[client_dir.name] = len(data.get('tasks', []))
            except (json.JSONDecodeError, FileNotFoundError):
                counts[client_dir.name] = 0

    return counts


def get_backup_task_counts(backup_path: Path) -> Dict[str, int]:
    """Extract task counts from a backup tarball"""
    counts = {}

    # Extract to temp directory
    temp_dir = tempfile.mkdtemp()

    try:
        with tarfile.open(backup_path, 'r:gz') as tar:
            tar.extractall(temp_dir)

        # Count tasks in extracted backup
        clients_dir = Path(temp_dir) / 'clients'
        if clients_dir.exists():
            for client_dir in clients_dir.iterdir():
                if not client_dir.is_dir() or client_dir.name.startswith('_'):
                    continue

                tasks_file = client_dir / 'tasks.json'
                if tasks_file.exists():
                    try:
                        with open(tasks_file, 'r') as f:
                            data = json.load(f)
                            counts[client_dir.name] = len(data.get('tasks', []))
                    except (json.JSONDecodeError, FileNotFoundError):
                        counts[client_dir.name] = 0

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

    return counts


def find_latest_backup() -> Path:
    """Find the most recent backup file"""
    if not BACKUPS_DIR.exists():
        raise FileNotFoundError(f"Backups directory not found: {BACKUPS_DIR}")

    backups = sorted(BACKUPS_DIR.glob('tasks-backup-*.tar.gz'), reverse=True)
    if not backups:
        raise FileNotFoundError("No backup files found")

    return backups[0]


def log_alert(message: str):
    """Log alert message to file and print"""
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp} | {message}\n"

    print(f"🚨 {message}")

    with open(ALERT_LOG, 'a') as f:
        f.write(log_entry)


def compare_counts(current: Dict[str, int], backup: Dict[str, int]) -> List[str]:
    """Compare current and backup counts, return list of alerts"""
    alerts = []

    # Check each client in backup
    for client, backup_count in backup.items():
        current_count = current.get(client, 0)

        # Alert: Client lost all tasks
        if backup_count > 0 and current_count == 0:
            alerts.append(f"CRITICAL: {client} lost ALL {backup_count} tasks")

        # Alert: Client lost >50% of tasks
        elif backup_count > 5 and current_count < backup_count * 0.5:
            percent_lost = int((1 - current_count / backup_count) * 100)
            alerts.append(
                f"WARNING: {client} lost {percent_lost}% of tasks "
                f"({backup_count} → {current_count})"
            )

    # Check total task count across all clients
    total_backup = sum(backup.values())
    total_current = sum(current.values())

    if total_backup > 20 and total_current < total_backup * 0.7:
        percent_lost = int((1 - total_current / total_backup) * 100)
        alerts.append(
            f"CRITICAL: Total task count dropped {percent_lost}% "
            f"({total_backup} → {total_current})"
        )

    return alerts


def main():
    """Main monitoring function"""
    print("=" * 80)
    print("BACKUP TASK MONITOR")
    print("=" * 80)
    print()

    try:
        # Get current task counts
        current_counts = get_current_task_counts()
        total_current = sum(current_counts.values())
        print(f"Current tasks: {total_current} across {len(current_counts)} clients")

        # Get latest backup
        latest_backup = find_latest_backup()
        backup_time = latest_backup.stem.replace('tasks-backup-', '')
        print(f"Latest backup: {backup_time}")

        # Get backup task counts
        backup_counts = get_backup_task_counts(latest_backup)
        total_backup = sum(backup_counts.values())
        print(f"Backup tasks:  {total_backup} across {len(backup_counts)} clients")
        print()

        # Compare and check for alerts
        alerts = compare_counts(current_counts, backup_counts)

        if alerts:
            print("=" * 80)
            print("⚠️  ALERTS DETECTED")
            print("=" * 80)
            print()
            for alert in alerts:
                log_alert(alert)
            print()
            print("Check data/state/backup-alerts.log for full history")
            return 1  # Exit with error code
        else:
            print("✅ No significant task count changes detected")
            print()
            return 0

    except Exception as e:
        error_msg = f"Error during backup monitoring: {e}"
        log_alert(error_msg)
        print(f"\n❌ {error_msg}")
        return 1


if __name__ == '__main__':
    exit(main())
