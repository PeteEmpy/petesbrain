#!/usr/bin/env python3
"""
Granola Importer Health Check Script

Monitors the Granola importer daemon to ensure it's:
1. Running (process exists)
2. Making progress (log file is being updated)
3. Actually fetching meetings from the API (not stuck at "Found 0 meetings")

If unhealthy, automatically restarts the daemon.

Usage:
    python3 health_check.py [--dry-run]

Exit codes:
    0 = Healthy
    1 = Unhealthy and restarted
    2 = Error during health check
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
LOG_FILE = os.path.expanduser("~/.petesbrain-granola-importer.log")
IMPORT_HISTORY = "/Users/administrator/Documents/PetesBrain/tools/granola-importer/.import_history.json"
LAUNCHAGENT_LABEL = "com.petesbrain.granola-importer"
ALERT_EMAIL = "petere@roksys.co.uk"

# Health check thresholds
MAX_LOG_AGE_MINUTES = 10  # Log should update every 5 min (sync cycle)
MAX_ZERO_MEETINGS_HOURS = 2  # If "Found 0 meetings" for 2+ hours, likely stuck
MIN_IMPORT_CHECK_HOURS = 24  # Check if any imports in last 24 hours (weekdays only)


def check_process_running():
    """Check if the Granola importer process is running."""
    try:
        result = subprocess.run(
            ["launchctl", "list", LAUNCHAGENT_LABEL],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error checking process: {e}")
        return False


def check_log_freshness():
    """Check if the log file has been updated recently."""
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return False

    log_mtime = datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
    age_minutes = (datetime.now() - log_mtime).total_seconds() / 60

    if age_minutes > MAX_LOG_AGE_MINUTES:
        print(f"❌ Log file not updated in {age_minutes:.1f} minutes (threshold: {MAX_LOG_AGE_MINUTES})")
        return False

    print(f"✓ Log file updated {age_minutes:.1f} minutes ago")
    return True


def check_meeting_fetching():
    """Check if the daemon is successfully fetching meetings from the API."""
    if not os.path.exists(LOG_FILE):
        return True  # Can't check, assume OK

    # Read last 2 hours of logs
    cutoff_time = datetime.now() - timedelta(hours=MAX_ZERO_MEETINGS_HOURS)

    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        # Look for "Found X meetings" entries in recent logs
        found_pattern = re.compile(r'Found (\d+) meetings')
        recent_counts = []

        for line in reversed(lines[-500:]):  # Check last 500 lines
            # Extract timestamp from log line (format: 2025-11-04 14:18:06,046)
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                try:
                    log_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                    if log_time < cutoff_time:
                        break  # Stop looking at older logs

                    # Check if this line reports meeting count
                    count_match = found_pattern.search(line)
                    if count_match:
                        count = int(count_match.group(1))
                        recent_counts.append(count)
                except ValueError:
                    continue

        if not recent_counts:
            print(f"⚠️  No meeting fetch attempts found in last {MAX_ZERO_MEETINGS_HOURS} hours")
            return True  # Can't determine, assume OK

        # If ALL recent fetches returned 0 meetings, daemon might be stuck
        if all(count == 0 for count in recent_counts) and len(recent_counts) >= 10:
            print(f"❌ Daemon reporting 0 meetings for {len(recent_counts)} consecutive checks")
            print(f"   (Checked last {MAX_ZERO_MEETINGS_HOURS} hours of logs)")
            return False

        # If we're seeing non-zero counts, daemon is working
        max_count = max(recent_counts)
        print(f"✓ Daemon fetching meetings successfully (max: {max_count} in last {MAX_ZERO_MEETINGS_HOURS}h)")
        return True

    except Exception as e:
        print(f"⚠️  Error checking meeting fetching: {e}")
        return True  # Can't check, assume OK


def check_recent_imports():
    """Check if any meetings have been imported recently (optional check)."""
    if not os.path.exists(IMPORT_HISTORY):
        print("⚠️  No import history found")
        return True  # Can't check, assume OK

    try:
        with open(IMPORT_HISTORY, 'r') as f:
            history = json.load(f)

        if not history.get('imported'):
            print("⚠️  No imports in history")
            return True

        # Find most recent import
        latest_import = None
        latest_time = None

        for meeting_id, data in history['imported'].items():
            imported_at = datetime.fromisoformat(data['imported_at'])
            if latest_time is None or imported_at > latest_time:
                latest_time = imported_at
                latest_import = data

        if latest_time:
            hours_ago = (datetime.now() - latest_time).total_seconds() / 3600
            print(f"ℹ️  Last import: {hours_ago:.1f} hours ago")

            # Only warn if it's a weekday and no imports for 24+ hours
            if datetime.now().weekday() < 5:  # Monday=0, Friday=4
                if hours_ago > MIN_IMPORT_CHECK_HOURS:
                    print(f"⚠️  No imports in {hours_ago:.1f} hours (weekday)")
                    # This is a warning, not a failure (maybe no meetings scheduled)

        return True

    except Exception as e:
        print(f"⚠️  Error checking import history: {e}")
        return True


def restart_daemon():
    """Restart the Granola importer daemon."""
    print("\n🔄 Restarting daemon...")

    try:
        # Stop the daemon
        subprocess.run(
            ["launchctl", "stop", LAUNCHAGENT_LABEL],
            capture_output=True,
            check=True
        )
        print("✓ Stopped daemon")

        # Give it a moment
        import time
        time.sleep(2)

        # Start the daemon
        subprocess.run(
            ["launchctl", "start", LAUNCHAGENT_LABEL],
            capture_output=True,
            check=True
        )
        print("✓ Started daemon")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error restarting daemon: {e}")
        return False


def send_alert(message):
    """Send email alert about health check failure."""
    try:
        # Log to file
        alert_log = os.path.expanduser("~/.petesbrain-granola-health.log")
        with open(alert_log, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now().isoformat()}]\n")
            f.write(message)
            f.write(f"\n{'='*60}\n")

        # Could add email sending here if needed
        print(f"ℹ️  Alert logged to {alert_log}")

    except Exception as e:
        print(f"⚠️  Error logging alert: {e}")


def main():
    dry_run = "--dry-run" in sys.argv

    print("="*60)
    print("Granola Importer Health Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()

    # Run health checks
    checks = {
        "Process running": check_process_running(),
        "Log freshness": check_log_freshness(),
        "Meeting fetching": check_meeting_fetching(),
        "Recent imports": check_recent_imports()
    }

    print()
    print("-"*60)

    # Determine health status (critical checks only)
    critical_checks = ["Process running", "Log freshness", "Meeting fetching"]
    is_healthy = all(checks[check] for check in critical_checks)

    if is_healthy:
        print("✅ HEALTHY - All checks passed")
        return 0
    else:
        print("❌ UNHEALTHY - Critical checks failed:")
        for check in critical_checks:
            if not checks[check]:
                print(f"   • {check}")

        if dry_run:
            print("\n🔍 DRY RUN - Would restart daemon")
            return 1

        # Attempt recovery
        alert_msg = f"Granola importer unhealthy. Failed checks: {[c for c in critical_checks if not checks[c]]}"
        send_alert(alert_msg)

        if restart_daemon():
            print("✅ Daemon restarted successfully")
            send_alert("Granola importer restarted successfully")
            return 1  # Was unhealthy but recovered
        else:
            print("❌ Failed to restart daemon - manual intervention required")
            send_alert("CRITICAL: Failed to restart Granola importer - manual intervention required")
            return 2


if __name__ == "__main__":
    sys.exit(main())
