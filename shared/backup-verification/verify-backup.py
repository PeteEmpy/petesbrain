#!/usr/bin/env python3
"""
Backup Verification System
Validates backup integrity and alerts on issues

CRITICAL: Run after every backup to catch corruption early
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import tarfile
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.petesbrain-backup-verification.log')),
        logging.StreamHandler()
    ]
)

# Configuration
MIN_BACKUP_SIZE_KB = 50  # Minimum acceptable backup size
MIN_CLIENT_FILES = 10    # Minimum number of client task files
TASK_COUNT_DROP_THRESHOLD = 0.20  # Alert if tasks drop >20%
BASELINE_FILE = Path(__file__).parent / 'backup-baseline.json'

class BackupVerificationError(Exception):
    """Raised when backup verification fails"""
    pass

class BackupVerifier:
    def __init__(self, backup_path: str):
        self.backup_path = Path(backup_path)
        self.issues = []
        self.warnings = []
        self.stats = {}

    def verify(self) -> bool:
        """Run all verification checks. Returns True if backup is valid."""
        try:
            logging.info(f"Verifying backup: {self.backup_path}")

            # Check 1: File exists
            if not self.backup_path.exists():
                self.issues.append(f"Backup file does not exist: {self.backup_path}")
                return False

            # Check 2: File size
            size_kb = self.backup_path.stat().st_size / 1024
            self.stats['size_kb'] = size_kb
            logging.info(f"Backup size: {size_kb:.2f} KB")

            if size_kb < 1:
                self.issues.append(f"CRITICAL: Backup file is tiny ({size_kb:.2f} KB) - likely corrupt")
                return False
            elif size_kb < MIN_BACKUP_SIZE_KB:
                self.issues.append(f"Backup file is suspiciously small ({size_kb:.2f} KB < {MIN_BACKUP_SIZE_KB} KB minimum)")
                return False

            # Check 3: Extract and verify contents (if tar.gz)
            if self.backup_path.suffix == '.gz' or self.backup_path.name.endswith('.tar.gz'):
                if not self._verify_tarball():
                    return False

            # Check 4: Verify JSON files if direct JSON backup
            elif self.backup_path.suffix == '.json':
                if not self._verify_json_file(self.backup_path):
                    return False

            # Check 5: Compare against baseline
            if not self._verify_against_baseline():
                self.warnings.append("Task count differs significantly from baseline")

            # Summary
            if self.issues:
                logging.error(f"Backup verification FAILED with {len(self.issues)} critical issues")
                return False

            if self.warnings:
                logging.warning(f"Backup verification PASSED with {len(self.warnings)} warnings")
            else:
                logging.info("Backup verification PASSED - all checks successful")

            # Update baseline if backup is valid
            self._update_baseline()

            return True

        except Exception as e:
            self.issues.append(f"Verification exception: {str(e)}")
            logging.exception("Error during backup verification")
            return False

    def _verify_tarball(self) -> bool:
        """Verify tar.gz backup contents"""
        try:
            with tarfile.open(self.backup_path, 'r:gz') as tar:
                members = tar.getmembers()

                # Count task files
                task_files = [m for m in members if m.name.endswith('tasks.json')]
                self.stats['task_files_count'] = len(task_files)

                logging.info(f"Found {len(task_files)} task files in backup")

                if len(task_files) < MIN_CLIENT_FILES:
                    self.issues.append(
                        f"Too few client task files ({len(task_files)} < {MIN_CLIENT_FILES} minimum)"
                    )
                    return False

                # Verify each task file is valid JSON
                total_tasks = 0
                for member in task_files:
                    f = tar.extractfile(member)
                    if f is None:
                        self.warnings.append(f"Could not extract {member.name}")
                        continue

                    content = f.read()
                    if len(content) < 10:  # Suspiciously small
                        self.issues.append(f"Task file {member.name} is too small ({len(content)} bytes)")
                        continue

                    try:
                        # Try UTF-8 first, then fallback to latin-1
                        try:
                            content_str = content.decode('utf-8')
                        except UnicodeDecodeError:
                            content_str = content.decode('latin-1')

                        data = json.loads(content_str)
                        if 'tasks' in data:
                            task_count = len(data['tasks'])
                            total_tasks += task_count
                            logging.debug(f"{member.name}: {task_count} tasks")
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        self.warnings.append(f"Could not parse {member.name}: {e}")

                self.stats['total_tasks'] = total_tasks
                logging.info(f"Total tasks in backup: {total_tasks}")

                if total_tasks == 0:
                    self.warnings.append("Backup contains 0 tasks across all clients")

                return True

        except tarfile.TarError as e:
            self.issues.append(f"Failed to read tar file: {e}")
            return False

    def _verify_json_file(self, json_path: Path) -> bool:
        """Verify a single JSON file"""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)

            if 'tasks' in data:
                task_count = len(data['tasks'])
                self.stats['total_tasks'] = task_count
                logging.info(f"JSON file contains {task_count} tasks")

            return True

        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON: {e}")
            return False

    def _verify_against_baseline(self) -> bool:
        """Compare task count against baseline"""
        if not BASELINE_FILE.exists():
            logging.info("No baseline file exists yet - will create one")
            return True

        try:
            with open(BASELINE_FILE, 'r') as f:
                baseline = json.load(f)

            baseline_tasks = baseline.get('total_tasks', 0)
            current_tasks = self.stats.get('total_tasks', 0)

            if baseline_tasks == 0:
                return True

            # Calculate percentage change
            change_pct = (current_tasks - baseline_tasks) / baseline_tasks

            logging.info(f"Task count comparison: {baseline_tasks} (baseline) -> {current_tasks} (current) = {change_pct:+.1%}")

            # Alert if significant drop
            if change_pct < -TASK_COUNT_DROP_THRESHOLD:
                self.warnings.append(
                    f"Task count dropped {abs(change_pct):.1%} from baseline "
                    f"({baseline_tasks} -> {current_tasks})"
                )
                return False

            return True

        except Exception as e:
            logging.warning(f"Could not compare against baseline: {e}")
            return True

    def _update_baseline(self):
        """Update baseline with current stats"""
        try:
            baseline = {
                'last_update': datetime.now().isoformat(),
                'backup_path': str(self.backup_path),
                'total_tasks': self.stats.get('total_tasks', 0),
                'task_files_count': self.stats.get('task_files_count', 0),
                'size_kb': self.stats.get('size_kb', 0)
            }

            BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(BASELINE_FILE, 'w') as f:
                json.dump(baseline, f, indent=2)

            logging.debug(f"Updated baseline: {baseline}")

        except Exception as e:
            logging.warning(f"Could not update baseline: {e}")

    def send_alert(self):
        """Send alert about backup issues"""
        if not self.issues and not self.warnings:
            return

        alert_msg = f"""
BACKUP VERIFICATION ALERT
========================
Backup: {self.backup_path}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

        if self.issues:
            alert_msg += f"CRITICAL ISSUES ({len(self.issues)}):\n"
            for issue in self.issues:
                alert_msg += f"  - {issue}\n"
            alert_msg += "\n"

        if self.warnings:
            alert_msg += f"WARNINGS ({len(self.warnings)}):\n"
            for warning in self.warnings:
                alert_msg += f"  - {warning}\n"
            alert_msg += "\n"

        if self.stats:
            alert_msg += "Stats:\n"
            for key, value in self.stats.items():
                alert_msg += f"  {key}: {value}\n"

        # Log alert
        logging.error(alert_msg)

        # Write to alert file
        alert_file = Path.home() / '.petesbrain-backup-alerts.log'
        with open(alert_file, 'a') as f:
            f.write(alert_msg + "\n" + "="*50 + "\n\n")

        print(alert_msg)

def verify_backup(backup_path: str) -> bool:
    """Main verification function"""
    verifier = BackupVerifier(backup_path)
    is_valid = verifier.verify()

    if not is_valid or verifier.warnings:
        verifier.send_alert()

    return is_valid

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: verify-backup.py <backup-file-path>")
        print("\nExample:")
        print("  verify-backup.py /path/to/tasks-backup-2025-12-19.tar.gz")
        sys.exit(1)

    backup_path = sys.argv[1]

    is_valid = verify_backup(backup_path)

    if is_valid:
        print("✅ Backup verification PASSED")
        sys.exit(0)
    else:
        print("❌ Backup verification FAILED")
        sys.exit(1)
