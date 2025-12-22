#!/usr/bin/env python3
"""
Pete's Brain System Health Check

Monitors all automated workflows to ensure they're running properly.
Checks LaunchAgents, log file freshness, and recent activity.

Usage:
    python3 system-health-check.py [--dry-run] [--verbose] [--restart-unhealthy]

Exit codes:
    0 = All systems healthy
    1 = Some systems unhealthy (restarted if --restart-unhealthy)
    2 = Critical failure

Run this via cron/LaunchAgent every hour to ensure automation stays healthy.
"""

import os
import sys
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# WORKFLOW DEFINITIONS
# ============================================================================

WORKFLOWS = {
    # Core automation (should always be running)
    "granola-importer": {
        "label": "com.petesbrain.granola-google-docs-importer",
        "log": "~/.petesbrain-granola-google-docs.log",
        "type": "interval",  # Runs every 30 minutes
        "interval_hours": 0.5,  # 30 minutes
        "check_activity": lambda log: check_granola_activity(log),
        "critical": True,
        "description": "Granola meeting importer (every 30 min)"
    },
    "knowledge-base": {
        "label": "com.petesbrain.knowledge-base",
        "log": "~/.petesbrain-knowledge-base.log",
        "type": "interval",  # Runs every N hours
        "interval_hours": 6,
        "check_activity": lambda log: check_kb_activity(log),
        "critical": True,
        "description": "Knowledge base processor (every 6 hours)"
    },
    "tasks-monitor": {
        "label": "com.petesbrain.tasks-monitor",
        "log": "~/.petesbrain-tasks-monitor.log",
        "type": "interval",
        "interval_hours": 6,
        "check_activity": lambda log: check_tasks_activity(log),
        "critical": True,
        "description": "Google Tasks sync (every 6 hours)"
    },
    "industry-news": {
        "label": "com.petesbrain.industry-news",
        "log": "~/.petesbrain-industry-news.log",
        "type": "interval",
        "interval_hours": 6,
        "critical": True,
        "description": "Industry news monitor (every 6 hours)"
    },
    "ai-news": {
        "label": "com.petesbrain.ai-news",
        "log": "~/.petesbrain-ai-news.log",
        "type": "interval",
        "interval_hours": 6,
        "critical": True,
        "description": "AI news monitor (every 6 hours)"
    },

    # Weekly summaries (Monday mornings)
    "kb-weekly-summary": {
        "label": "com.petesbrain.kb-weekly-summary",
        "log": "~/.petesbrain-kb-weekly-summary.log",
        "type": "weekly",
        "day_of_week": 0,  # Monday
        "critical": False,
        "description": "Knowledge base weekly summary (Mon 9 AM)"
    },
    "granola-weekly-summary": {
        "label": "com.petesbrain.granola-weekly-summary",
        "log": "~/.petesbrain-granola-weekly-summary.log",
        "type": "weekly",
        "day_of_week": 0,  # Monday
        "critical": False,
        "description": "Meeting weekly review (Mon 9 AM)"
    },

    # Product tracking & analysis
    "product-data-fetcher": {
        "label": "com.petesbrain.product-data-fetcher",
        "log": "~/.petesbrain-product-data-fetcher.log",
        "type": "daily",
        "critical": False,
        "description": "Product data fetcher (daily 6 AM)"
    },
    "label-snapshots": {
        "label": "com.petesbrain.label-snapshots",
        "log": "~/.petesbrain-label-snapshots.log",
        "type": "daily",
        "critical": False,
        "description": "Product label snapshots (daily)"
    },
    "weekly-label-reports": {
        "label": "com.petesbrain.weekly-label-reports",
        "log": "~/.petesbrain-weekly-label-reports.log",
        "type": "weekly",
        "day_of_week": 0,  # Monday
        "critical": False,
        "description": "Weekly product label reports (Mon)"
    },

    # Client-specific automation
    "smythson-dashboard": {
        "label": "com.petesbrain.smythson-dashboard",
        "log": "~/.petesbrain-smythson-dashboard.log",
        "type": "daily",
        "critical": False,
        "description": "Smythson Q4 dashboard (daily)"
    },
}


# ============================================================================
# ACTIVITY CHECKERS (workflow-specific logic)
# ============================================================================

def check_granola_activity(log_path: str) -> Tuple[bool, str]:
    """Check if Granola importer is fetching meetings (not stuck at 0)."""
    if not os.path.exists(log_path):
        return True, "No log file to check"

    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()

        # Check last 2 hours of logs
        found_pattern = re.compile(r'Found (\d+) meetings')
        recent_counts = []

        cutoff_time = datetime.now() - timedelta(hours=2)

        for line in reversed(lines[-500:]):
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                try:
                    log_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                    if log_time < cutoff_time:
                        break

                    count_match = found_pattern.search(line)
                    if count_match:
                        recent_counts.append(int(count_match.group(1)))
                except ValueError:
                    continue

        if not recent_counts:
            return True, "No recent fetch attempts found"

        # If ALL recent fetches are 0 and we have many samples, likely stuck
        if all(c == 0 for c in recent_counts) and len(recent_counts) >= 10:
            return False, f"Stuck at 0 meetings for {len(recent_counts)} checks"

        max_count = max(recent_counts)
        return True, f"Fetching OK (max: {max_count} in last 2h)"

    except Exception as e:
        return True, f"Error checking: {e}"


def check_kb_activity(log_path: str) -> Tuple[bool, str]:
    """Check if KB processor is running successfully."""
    if not os.path.exists(log_path):
        return True, "No log file to check"

    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()

        # Look for recent "Processing" or "Completed" messages
        for line in reversed(lines[-100:]):
            if "Processing inbox" in line or "processed successfully" in line:
                return True, "Recent processing activity found"
            if "ERROR" in line or "CRITICAL" in line:
                return False, "Errors found in recent logs"

        return True, "No issues detected"

    except Exception as e:
        return True, f"Error checking: {e}"


def check_tasks_activity(log_path: str) -> Tuple[bool, str]:
    """Check if Tasks monitor is syncing successfully."""
    if not os.path.exists(log_path):
        return True, "No log file to check"

    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()

        # Look for sync activity
        for line in reversed(lines[-100:]):
            if "Synced" in line or "No changes" in line:
                return True, "Recent sync activity found"
            if "ERROR" in line or "Failed" in line:
                return False, "Sync errors found"

        return True, "No issues detected"

    except Exception as e:
        return True, f"Error checking: {e}"


# ============================================================================
# CORE HEALTH CHECK FUNCTIONS
# ============================================================================

def check_process_running(label: str) -> bool:
    """Check if a LaunchAgent is loaded and running."""
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def check_log_freshness(log_path: str, workflow_type: str, interval_hours: int = None) -> Tuple[bool, str]:
    """Check if log file has been updated within expected timeframe."""
    log_path = os.path.expanduser(log_path)

    if not os.path.exists(log_path):
        return True, "No log file (may not have run yet)"

    log_mtime = datetime.fromtimestamp(os.path.getmtime(log_path))
    age_hours = (datetime.now() - log_mtime).total_seconds() / 3600

    # Determine acceptable age based on workflow type
    if workflow_type == "daemon":
        max_age = 0.25  # 15 minutes for continuous daemons
    elif workflow_type == "interval" and interval_hours:
        max_age = interval_hours + 1  # Interval + 1 hour grace period
    elif workflow_type == "daily":
        max_age = 25  # 24 hours + 1 hour grace
    elif workflow_type == "weekly":
        # Only check on expected day (Monday)
        if datetime.now().weekday() == 0:
            max_age = 25  # Should have run today
        else:
            max_age = 168  # Can be up to a week old
    else:
        max_age = 25  # Default: daily

    if age_hours > max_age:
        return False, f"Log {age_hours:.1f}h old (max: {max_age:.1f}h)"

    return True, f"Updated {age_hours:.1f}h ago"


def restart_workflow(label: str) -> bool:
    """Restart a LaunchAgent workflow."""
    try:
        # Stop
        subprocess.run(
            ["launchctl", "stop", label],
            capture_output=True,
            check=True
        )

        # Wait
        import time
        time.sleep(2)

        # Start
        subprocess.run(
            ["launchctl", "start", label],
            capture_output=True,
            check=True
        )

        return True
    except subprocess.CalledProcessError:
        return False


def log_alert(message: str):
    """Log alert to health check log file."""
    log_file = os.path.expanduser("~/.petesbrain-health-check.log")
    try:
        with open(log_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now().isoformat()}]\n")
            f.write(message)
            f.write(f"\n{'='*60}\n")
    except Exception as e:
        print(f"⚠️  Error logging alert: {e}")


# ============================================================================
# MAIN HEALTH CHECK
# ============================================================================

def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    auto_restart = "--restart-unhealthy" in sys.argv

    print("="*80)
    print("Pete's Brain System Health Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %A')}")
    print("="*80)
    print()

    results = {}
    unhealthy_workflows = []
    critical_failures = []

    # Check each workflow
    for name, config in WORKFLOWS.items():
        if verbose:
            print(f"\n{'─'*80}")
            print(f"Checking: {name}")
            print(f"Description: {config['description']}")

        checks = {}

        # 1. Check if process is running
        is_running = check_process_running(config['label'])
        checks['running'] = is_running

        if verbose or not is_running:
            status = "✓" if is_running else "✗"
            print(f"  {status} Process: {'Running' if is_running else 'NOT RUNNING'}")

        # 2. Check log freshness
        if 'log' in config:
            is_fresh, msg = check_log_freshness(
                config['log'],
                config['type'],
                config.get('interval_hours')
            )
            checks['log_fresh'] = is_fresh

            if verbose or not is_fresh:
                status = "✓" if is_fresh else "✗"
                print(f"  {status} Log freshness: {msg}")

        # 3. Check workflow-specific activity
        if 'check_activity' in config and 'log' in config:
            log_path = os.path.expanduser(config['log'])
            is_active, msg = config['check_activity'](log_path)
            checks['activity'] = is_active

            if verbose or not is_active:
                status = "✓" if is_active else "✗"
                print(f"  {status} Activity: {msg}")

        # Determine overall health
        # For periodic tasks (interval/daily/weekly), only check log freshness
        # For daemon tasks, also require running process
        if config['type'] == 'daemon':
            critical_checks = ['running', 'log_fresh']
        else:
            critical_checks = ['log_fresh']

        is_healthy = all(checks.get(c, True) for c in critical_checks)

        results[name] = {
            'healthy': is_healthy,
            'checks': checks,
            'critical': config.get('critical', False)
        }

        if not is_healthy:
            unhealthy_workflows.append(name)
            if config.get('critical', False):
                critical_failures.append(name)

    # Print summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)

    healthy_count = sum(1 for r in results.values() if r['healthy'])
    total_count = len(results)

    print(f"\nHealthy: {healthy_count}/{total_count} workflows")

    if critical_failures:
        print(f"\n❌ CRITICAL FAILURES ({len(critical_failures)}):")
        for name in critical_failures:
            print(f"   • {name} - {WORKFLOWS[name]['description']}")

    if unhealthy_workflows and not critical_failures:
        print(f"\n⚠️  NON-CRITICAL ISSUES ({len(unhealthy_workflows)}):")
        for name in unhealthy_workflows:
            if name not in critical_failures:
                print(f"   • {name} - {WORKFLOWS[name]['description']}")

    if not unhealthy_workflows:
        print("\n✅ ALL SYSTEMS HEALTHY")
        return 0

    # Handle unhealthy workflows
    if auto_restart and not dry_run:
        print(f"\n🔄 Attempting to restart {len(unhealthy_workflows)} unhealthy workflow(s)...")

        for name in unhealthy_workflows:
            label = WORKFLOWS[name]['label']
            print(f"\n   Restarting {name}...")

            if restart_workflow(label):
                print(f"   ✓ Restarted {name}")
                log_alert(f"Auto-restarted unhealthy workflow: {name}")
            else:
                print(f"   ✗ Failed to restart {name}")
                log_alert(f"FAILED to restart workflow: {name}")

    elif auto_restart and dry_run:
        print(f"\n🔍 DRY RUN - Would restart {len(unhealthy_workflows)} workflow(s)")

    # Exit with appropriate code
    if critical_failures:
        log_alert(f"CRITICAL: {len(critical_failures)} critical workflows unhealthy: {critical_failures}")
        return 2
    elif unhealthy_workflows:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
