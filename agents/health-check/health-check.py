#!/usr/bin/env python3
"""
Enhanced System Health Check with Comprehensive Monitoring

Automatically discovers all PetesBrain LaunchAgents and monitors their health.
Includes immediate alerts, failure tracking, escalation, and system monitoring.

Usage:
    python3 agents/health-check/health-check.py [--dry-run] [--verbose] [--restart-unhealthy] [--no-alerts]

Exit codes:
    0 = All systems healthy
    1 = Some systems unhealthy (restarted if --restart-unhealthy)
    2 = Critical failure
"""

import os
import sys
import json
import subprocess
import re
import smtplib
import shutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
import socket
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request
import urllib.error

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import discovery system
try:
    from shared.scripts.launchagent_discovery import (
        discover_launch_agents,
        get_agent_status,
        get_all_agents_with_status
    )
    DISCOVERY_AVAILABLE = True
except ImportError:
    print("⚠️  LaunchAgent discovery not available - using manual config")
    DISCOVERY_AVAILABLE = False

# Configuration file
CONFIG_FILE = Path(__file__).parent / "health-check-config.json"
FAILURE_HISTORY_FILE = Path.home() / ".petesbrain-failure-history.json"
ALERT_STATE_FILE = Path.home() / ".petesbrain-alert-state.json"
HEALTH_CHECK_STATE_FILE = Path.home() / ".petesbrain-health-check-state.json"

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

def load_config() -> Dict:
    """Load configuration from JSON file."""
    default_config = {
        "alerts": {
            "email": {
                "enabled": True,
                "to": None,
                "from": None,
                "critical_only": False,
                "throttle_hours": 1
            },
            "slack": {
                "enabled": False,
                "webhook_url": None
            },
            "sms": {
                "enabled": False,
                "provider": "twilio",
                "api_key": None,
                "api_secret": None,
                "from_number": None,
                "to_number": None
            }
        },
        "monitoring": {
            "check_disk_space": True,
            "disk_space_threshold_gb": 10,
            "check_memory": True,
            "memory_threshold_percent": 90,
            "check_internet": True,
            "check_apis": True
        },
        "failure_tracking": {
            "escalation_threshold": 3,
            "escalation_window_hours": 24,
            "alert_on_new_failures_only": True
        },
        "self_monitoring": {
            "enabled": True,
            "alert_if_not_run_hours": 1
        }
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                def merge_dict(base, update):
                    for key, value in update.items():
                        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                            merge_dict(base[key], value)
                        else:
                            base[key] = value
                merge_dict(default_config, user_config)
        except Exception as e:
            print(f"⚠️  Error loading config: {e}, using defaults")
    
    # Override with environment variables if set
    if os.getenv('GMAIL_USER'):
        default_config['alerts']['email']['from'] = os.getenv('GMAIL_USER')
    if os.getenv('GMAIL_APP_PASSWORD'):
        # Store in config for email sending
        default_config['alerts']['email']['_password'] = os.getenv('GMAIL_APP_PASSWORD')
    
    return default_config

CONFIG = load_config()

# ============================================================================
# FAILURE TRACKING
# ============================================================================

def load_failure_history() -> Dict:
    """Load failure history from file."""
    if FAILURE_HISTORY_FILE.exists():
        try:
            with open(FAILURE_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"failures": {}, "last_check": None}

def save_failure_history(history: Dict):
    """Save failure history to file."""
    try:
        with open(FAILURE_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving failure history: {e}")

def record_failure(agent_name: str, is_critical: bool):
    """Record a failure for an agent."""
    history = load_failure_history()
    
    if agent_name not in history['failures']:
        history['failures'][agent_name] = []
    
    failure_record = {
        "timestamp": datetime.now().isoformat(),
        "critical": is_critical
    }
    
    history['failures'][agent_name].append(failure_record)
    
    # Keep only last 100 failures per agent
    history['failures'][agent_name] = history['failures'][agent_name][-100:]
    
    history['last_check'] = datetime.now().isoformat()
    save_failure_history(history)

def get_failure_count(agent_name: str, window_hours: int = 24) -> int:
    """Get failure count for an agent within time window."""
    history = load_failure_history()
    
    if agent_name not in history['failures']:
        return 0
    
    cutoff = datetime.now() - timedelta(hours=window_hours)
    failures = [
        f for f in history['failures'][agent_name]
        if datetime.fromisoformat(f['timestamp']) > cutoff
    ]
    
    return len(failures)

def check_escalation(agent_name: str) -> bool:
    """Check if agent should be escalated."""
    threshold = CONFIG['failure_tracking']['escalation_threshold']
    window = CONFIG['failure_tracking']['escalation_window_hours']
    return get_failure_count(agent_name, window) >= threshold

# ============================================================================
# ALERT STATE TRACKING (for throttling)
# ============================================================================

def load_alert_state() -> Dict:
    """Load alert state for throttling."""
    if ALERT_STATE_FILE.exists():
        try:
            with open(ALERT_STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_alerts": {}}

def save_alert_state(state: Dict):
    """Save alert state."""
    try:
        with open(ALERT_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving alert state: {e}")

def should_alert(agent_name: str, alert_type: str = "failure") -> bool:
    """Check if we should send an alert (throttling)."""
    state = load_alert_state()
    throttle_hours = CONFIG['alerts']['email']['throttle_hours']
    
    key = f"{agent_name}:{alert_type}"
    last_alert = state['last_alerts'].get(key)
    
    if not last_alert:
        return True
    
    last_alert_time = datetime.fromisoformat(last_alert)
    time_since = (datetime.now() - last_alert_time).total_seconds() / 3600
    
    return time_since >= throttle_hours

def record_alert(agent_name: str, alert_type: str = "failure"):
    """Record that an alert was sent."""
    state = load_alert_state()
    key = f"{agent_name}:{alert_type}"
    state['last_alerts'][key] = datetime.now().isoformat()
    save_alert_state(state)

# ============================================================================
# NEW FAILURE DETECTION
# ============================================================================

def load_previous_state() -> Dict:
    """Load previous health check state."""
    if HEALTH_CHECK_STATE_FILE.exists():
        try:
            with open(HEALTH_CHECK_STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"unhealthy_agents": [], "timestamp": None}

def save_current_state(unhealthy_agents: List[str]):
    """Save current health check state."""
    state = {
        "unhealthy_agents": unhealthy_agents,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open(HEALTH_CHECK_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving state: {e}")

def get_new_failures(current_unhealthy: List[str]) -> List[str]:
    """Get agents that are newly unhealthy."""
    if not CONFIG['failure_tracking']['alert_on_new_failures_only']:
        return current_unhealthy
    
    previous_state = load_previous_state()
    previous_unhealthy = set(previous_state.get('unhealthy_agents', []))
    current_unhealthy_set = set(current_unhealthy)
    
    return list(current_unhealthy_set - previous_unhealthy)

# ============================================================================
# SYSTEM RESOURCE MONITORING
# ============================================================================

def check_disk_space() -> Tuple[bool, str]:
    """Check available disk space."""
    if not CONFIG['monitoring']['check_disk_space']:
        return True, "Disk check disabled"
    
    try:
        threshold_gb = CONFIG['monitoring']['disk_space_threshold_gb']
        stat = shutil.disk_usage('/')
        free_gb = stat.free / (1024**3)
        
        if free_gb < threshold_gb:
            return False, f"Only {free_gb:.1f}GB free (threshold: {threshold_gb}GB)"
        return True, f"{free_gb:.1f}GB free"
    except Exception as e:
        return True, f"Error checking disk: {e}"

def check_memory() -> Tuple[bool, str]:
    """Check memory usage."""
    if not CONFIG['monitoring']['check_memory']:
        return True, "Memory check disabled"
    
    if not PSUTIL_AVAILABLE:
        return True, "Memory check unavailable (psutil not installed)"
    
    try:
        threshold_percent = CONFIG['monitoring']['memory_threshold_percent']
        memory = psutil.virtual_memory()
        usage_percent = memory.percent
        
        if usage_percent > threshold_percent:
            return False, f"Memory usage {usage_percent:.1f}% (threshold: {threshold_percent}%)"
        return True, f"Memory usage {usage_percent:.1f}%"
    except Exception as e:
        return True, f"Error checking memory: {e}"

def check_internet() -> Tuple[bool, str]:
    """Check internet connectivity."""
    if not CONFIG['monitoring']['check_internet']:
        return True, "Internet check disabled"
    
    try:
        # Try to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True, "Internet connected"
    except OSError:
        return False, "No internet connectivity"

# ============================================================================
# DEPENDENCY HEALTH CHECKS
# ============================================================================

def check_gmail_api() -> Tuple[bool, str]:
    """Check Gmail API connectivity."""
    if not CONFIG['monitoring']['check_apis']:
        return True, "API check disabled"
    
    try:
        # Try to import and check credentials
        sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'email-sync'))
        token_file = PROJECT_ROOT / 'shared' / 'email-sync' / 'token.json'
        
        if not token_file.exists():
            return False, "Gmail API token not found"
        
        # Check if token is recent (not expired)
        token_mtime = datetime.fromtimestamp(token_file.stat().st_mtime)
        age_days = (datetime.now() - token_mtime).days
        
        if age_days > 7:
            return False, f"Gmail token may be expired (last updated {age_days} days ago)"
        
        return True, "Gmail API token exists"
    except Exception as e:
        return True, f"Error checking Gmail API: {e}"

def check_google_ads_api() -> Tuple[bool, str]:
    """Check Google Ads API connectivity."""
    if not CONFIG['monitoring']['check_apis']:
        return True, "API check disabled"
    
    try:
        # Check for credentials file
        creds_file = PROJECT_ROOT / 'shared' / 'google-ads' / 'credentials.json'
        if not creds_file.exists():
            return False, "Google Ads credentials not found"
        return True, "Google Ads credentials exist"
    except Exception as e:
        return True, f"Error checking Google Ads API: {e}"

# ============================================================================
# HEALTH CHECK SELF-MONITORING
# ============================================================================

def check_health_check_itself() -> Tuple[bool, str]:
    """Check if health check is running regularly."""
    if not CONFIG['self_monitoring']['enabled']:
        return True, "Self-monitoring disabled"
    
    try:
        alert_hours = CONFIG['self_monitoring']['alert_if_not_run_hours']
        
        # Check health check log file
        log_file = Path.home() / ".petesbrain-health-check.log"
        if not log_file.exists():
            return False, "Health check log file not found"
        
        log_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age_hours = (datetime.now() - log_mtime).total_seconds() / 3600
        
        if age_hours > alert_hours:
            return False, f"Health check hasn't run in {age_hours:.1f} hours"
        
        return True, f"Health check ran {age_hours:.1f}h ago"
    except Exception as e:
        return True, f"Error checking health check: {e}"

# ============================================================================
# NOTIFICATION FUNCTIONS
# ============================================================================

def send_email_alert(subject: str, body_html: str, body_text: str = None, critical: bool = False):
    """Send email alert."""
    if not CONFIG['alerts']['email']['enabled']:
        return False
    
    email_config = CONFIG['alerts']['email']
    
    # Check if we should send (critical only setting)
    if email_config.get('critical_only') and not critical:
        return False
    
    email_to = email_config.get('to') or email_config.get('from') or os.getenv('GMAIL_USER')
    email_from = email_config.get('from') or os.getenv('GMAIL_USER')
    email_password = email_config.get('_password') or os.getenv('GMAIL_APP_PASSWORD')
    
    if not email_to or not email_from or not email_password:
        print("⚠️  Email alert not configured (missing GMAIL_USER or GMAIL_APP_PASSWORD)")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        
        if body_text:
            text_part = MIMEText(body_text, 'plain')
            msg.attach(text_part)
        
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_from, email_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"⚠️  Error sending email alert: {e}")
        return False

def send_macos_notification(title: str, subtitle: str, message: str,
                           critical: bool = False, action_command: str = None) -> bool:
    """
    Send macOS notification using terminal-notifier or osascript fallback.

    Args:
        title: Notification title
        subtitle: Notification subtitle
        message: Notification message body
        critical: If True, uses critical sound (Funk), else Basso
        action_command: Shell command to run when notification clicked

    Returns:
        True if notification sent successfully
    """
    # Check if terminal-notifier is installed
    terminal_notifier = shutil.which('terminal-notifier')

    if terminal_notifier:
        # Use terminal-notifier (preferred)
        sound = "Funk" if critical else "Basso"
        icon_path = PROJECT_ROOT / 'agents' / 'health-check' / 'brain-icon.icns'
        cmd = [
            terminal_notifier,
            '-title', title,
            '-subtitle', subtitle,
            '-message', message,
            '-sound', sound,
            '-group', 'health-check',  # Group all health-check notifications
            '-appIcon', str(icon_path),  # Brain emoji icon
        ]

        # Add click action if provided
        if action_command:
            cmd.extend(['-execute', action_command])

        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=5)
            return True
        except Exception as e:
            print(f"Failed to send terminal-notifier notification: {e}")
            return False
    else:
        # Fallback to osascript
        sound_name = "Funk" if critical else "Basso"

        # Build AppleScript command
        # Note: osascript can't handle click actions as easily, so we skip action_command
        script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound_name}"'

        try:
            subprocess.run(['osascript', '-e', script], capture_output=True, check=True, timeout=5)
            return True
        except Exception as e:
            print(f"Failed to send osascript notification: {e}")
            return False

def build_notification_summary(critical_failures: List[str],
                              new_failures: List[str],
                              escalated: List[str],
                              restart_failed: List[str],
                              unloaded_critical: List[Dict],
                              system_issues: List[str]) -> Tuple[str, str, str, bool]:
    """
    Build concise notification summary.

    Returns:
        (title, subtitle, message, is_critical)
    """
    total_failures = len(critical_failures) + len(new_failures) + len(escalated) + \
                    len(restart_failed) + len(unloaded_critical)

    # Determine severity
    is_critical = bool(critical_failures or unloaded_critical)

    # Build title
    if unloaded_critical:
        title = f"🧠 Pete's Brain Is Hurting: {len(unloaded_critical)} Agents NOT LOADED"
    elif critical_failures:
        title = f"🧠 Pete's Brain Is Hurting: {len(critical_failures)} Critical Failures"
    elif new_failures:
        title = f"🧠 Pete's Brain Is Hurting: {len(new_failures)} New Failures"
    else:
        title = "🧠 Pete's Brain Is Hurting"

    # Build subtitle
    subtitle = f"{total_failures} total issue(s) detected"

    # Build message - list agent names (max 5, then "and X more")
    all_failed_agents = []

    if unloaded_critical:
        all_failed_agents.extend([a['name'] for a in unloaded_critical])
    all_failed_agents.extend(critical_failures)
    all_failed_agents.extend(new_failures)
    all_failed_agents.extend(escalated)
    all_failed_agents.extend(restart_failed)

    if len(all_failed_agents) <= 5:
        message = ", ".join(all_failed_agents)
    else:
        message = ", ".join(all_failed_agents[:5]) + f" and {len(all_failed_agents) - 5} more"

    if system_issues:
        message += f" | {len(system_issues)} system issue(s)"

    return (title, subtitle, message, is_critical)

def send_slack_alert(message: str):
    """Send Slack alert."""
    if not CONFIG['alerts']['slack']['enabled']:
        return False
    
    webhook_url = CONFIG['alerts']['slack'].get('webhook_url')
    if not webhook_url:
        return False
    
    try:
        payload = {"text": message}
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception as e:
        print(f"⚠️  Error sending Slack alert: {e}")
        return False

def send_sms_alert(message: str):
    """Send SMS alert via Twilio."""
    if not CONFIG['alerts']['sms']['enabled']:
        return False
    
    sms_config = CONFIG['alerts']['sms']
    # SMS implementation would go here if Twilio is configured
    # For now, just log
    print(f"⚠️  SMS alerts not yet implemented")
    return False

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

def check_inbox_activity(log_path: str) -> Tuple[bool, str]:
    """Check if inbox processor is working."""
    if not os.path.exists(log_path):
        return True, "No log file to check"

    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()

        # Look for processing activity
        for line in reversed(lines[-100:]):
            if "Processing" in line or "processed" in line or "Enhanced" in line:
                return True, "Recent processing activity found"
            if "ERROR" in line or "Failed" in line:
                return False, "Errors found in recent logs"

        return True, "No issues detected"

    except Exception as e:
        return True, f"Error checking: {e}"

def check_email_sync_activity(log_path: str) -> Tuple[bool, str]:
    """Check if email sync is working."""
    if not os.path.exists(log_path):
        return True, "No log file to check"

    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()

        # Look for sync activity
        for line in reversed(lines[-100:]):
            if "Synced" in line or "Labeled" in line or "Complete" in line:
                return True, "Recent sync activity found"
            if "ERROR" in line or "Failed" in line:
                return False, "Sync errors found"

        return True, "No issues detected"

    except Exception as e:
        return True, f"Error checking: {e}"

def check_disapproval_monitor_activity(log_path: str) -> Tuple[bool, str]:
    """
    Verify disapproval monitor is actually checking products, not just exiting early.

    Returns:
        (is_active, message)
    """
    if not os.path.exists(log_path):
        return False, "Log file not found"

    try:
        with open(log_path, 'r', errors='ignore') as f:
            # Read last 500 lines to check recent runs
            lines = f.readlines()[-500:]
            log_content = ''.join(lines)

        # Count how many times we see "Outside business hours" vs actual monitoring
        outside_hours_count = log_content.count('Outside business hours')
        monitoring_patterns = [
            'Detecting changes for',
            'clients analyzed',
            'Checked',
            'No new disapprovals',
            'Found',
            'products'
        ]

        monitoring_activity_count = sum(1 for pattern in monitoring_patterns if pattern in log_content)

        # If we only see "Outside business hours" and no actual monitoring, flag it
        if outside_hours_count > 5 and monitoring_activity_count == 0:
            return (False, f"Only seeing '{outside_hours_count}' early exits, no actual monitoring")

        # Check for recent successful monitoring run
        if monitoring_activity_count > 0:
            return (True, f"Active monitoring detected ({monitoring_activity_count} activities)")

        # If no monitoring pattern and not many early exits, might be too soon to tell
        return (True, "No recent monitoring activity (may be outside business hours)")

    except Exception as e:
        return (False, f"Error checking activity: {e}")

# Map agent names to activity checkers
ACTIVITY_CHECKERS = {
    'granola-importer': check_granola_activity,
    'granola-google-docs-importer': check_granola_activity,
    'knowledge-base': check_kb_activity,
    'tasks-monitor': check_tasks_activity,
    'inbox-processor': check_inbox_activity,
    'ai-inbox-processor': check_inbox_activity,
    'email-sync': check_email_sync_activity,
    'email-auto-label': check_email_sync_activity,
    'disapproval-monitor': check_disapproval_monitor_activity,
}

# ============================================================================
# CORE HEALTH CHECK FUNCTIONS
# ============================================================================

def check_process_running(label: str) -> bool:
    """Check if a LaunchAgent is loaded and running."""
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def check_log_freshness(log_path: str, workflow_type: str, interval_seconds: Optional[int] = None) -> Tuple[bool, str]:
    """Check if log file has been updated within expected timeframe."""
    log_path = os.path.expanduser(log_path)

    if not os.path.exists(log_path):
        return True, "No log file (may not have run yet)"

    log_mtime = datetime.fromtimestamp(os.path.getmtime(log_path))
    age_hours = (datetime.now() - log_mtime).total_seconds() / 3600

    # Determine acceptable age based on workflow type
    if workflow_type == "daemon":
        max_age = 0.25  # 15 minutes for continuous daemons
    elif workflow_type == "interval" and interval_seconds:
        max_age = (interval_seconds / 3600) + 1  # Interval + 1 hour grace period
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

def check_error_log(log_path: str, workflow_type: str, interval_seconds: Optional[int] = None) -> Tuple[bool, str]:
    """
    Parse error log for recent failure patterns.

    Returns:
        (is_healthy, message)
    """
    # Get stderr log path by replacing .log with -error.log
    if not log_path:
        return (True, "No log path provided")

    error_log_path_str = log_path.replace('.log', '-error.log')
    error_log_path = Path(error_log_path_str).expanduser()

    if not error_log_path.exists():
        return (True, "No error log found")

    try:
        # Determine max age based on workflow type
        if workflow_type == "on_demand" or workflow_type == "interval":
            interval = interval_seconds or 3600
            max_age = (interval / 3600) + 1  # Interval + 1 hour grace period
        elif workflow_type == "daily":
            max_age = 25  # 24 hours + 1 hour grace
        elif workflow_type == "weekly":
            max_age = 168  # One week
        else:
            max_age = 25  # Default: daily

        # Check if error log was updated recently
        mtime = error_log_path.stat().st_mtime
        age_hours = (time.time() - mtime) / 3600

        if age_hours > max_age:
            # Error log hasn't been updated recently - likely no errors
            return (True, "No recent error log activity")

        # Parse recent error log entries for failure patterns
        with open(error_log_path, 'r', errors='ignore') as f:
            # Read last 100 lines
            lines = f.readlines()[-100:]
            recent_errors = ''.join(lines)

        # Error patterns that indicate failures
        error_patterns = [
            'FileNotFoundError',
            'ImportError',
            'ModuleNotFoundError',
            'ConnectionError',
            'PermissionError',
            'KeyError',
            'AttributeError',
            'Traceback (most recent call last)',
            'Fatal Python error',
            'OSError',
            'RuntimeError'
        ]

        found_errors = []
        for pattern in error_patterns:
            if pattern in recent_errors:
                found_errors.append(pattern)

        if found_errors:
            return (False, f"Error patterns detected: {', '.join(found_errors)}")

        return (True, "Error log clean")

    except Exception as e:
        return (True, f"Could not parse error log: {e}")

def check_exit_status(label: str) -> Tuple[bool, str]:
    """
    Check LaunchAgent's last exit status.

    Returns:
        (is_healthy, message)
    """
    if not label:
        return (True, "No label to check")

    try:
        # Query launchctl for agent status
        result = subprocess.run(
            ['launchctl', 'print', f'gui/{os.getuid()}/{label}'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return (True, "Agent not running or not accessible")

        output = result.stdout

        # Parse for "last exit code = X"
        exit_match = re.search(r'last exit code = (\d+)', output)

        if exit_match:
            exit_code = int(exit_match.group(1))
            if exit_code != 0:
                return (False, f"Last exit code: {exit_code} (agent crashed)")

        return (True, "Exit code healthy")

    except Exception as e:
        return (True, f"Could not check exit status: {e}")

def validate_environment(plist_path: str) -> Tuple[bool, str]:
    """
    Validate that required environment variables and files exist.

    Parses plist file to extract EnvironmentVariables and validates
    that any file paths referenced exist.

    Returns:
        (is_valid, message)
    """
    if not plist_path or not Path(plist_path).exists():
        return (True, "No plist file to validate")

    try:
        import plistlib
        with open(plist_path, 'rb') as f:
            plist_data = plistlib.load(f)

        env_vars = plist_data.get('EnvironmentVariables', {})
        if not env_vars:
            return (True, "No environment variables defined")

        missing_files = []

        # Check each environment variable that looks like a file path
        for key, value in env_vars.items():
            # Check if value looks like a file path
            if isinstance(value, str) and ('/' in value or value.startswith('~')):
                # Expand ~ if present
                expanded_path = Path(value).expanduser()

                # Check if file exists
                if not expanded_path.exists():
                    missing_files.append(f"{key}={value}")

        if missing_files:
            return (False, f"Missing files: {', '.join(missing_files)}")

        return (True, "All environment files exist")

    except Exception as e:
        return (True, f"Could not validate environment: {e}")

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
    log_file = Path.home() / ".petesbrain-health-check.log"
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

def check_agent_health(agent: Dict, verbose: bool = False) -> Dict:
    """
    Check health of a single agent.
    
    Returns:
        Dict with health status and details
    """
    name = agent['name']
    label = agent['label']
    log_path = agent.get('log_path', '')
    workflow_type = agent.get('workflow_type', 'on_demand')
    interval_seconds = agent.get('interval_seconds')
    critical = agent.get('critical', False)
    
    checks = {}
    
    # 1. Check if process is running
    is_running = check_process_running(label)
    checks['running'] = is_running
    
    if verbose or not is_running:
        status = "✓" if is_running else "✗"
        print(f"  {status} Process: {'Running' if is_running else 'NOT RUNNING'}")

    # 1.5 Validate environment (pre-flight check)
    plist_path_obj = Path.home() / "Library/LaunchAgents" / f"{label}.plist"
    if plist_path_obj.exists():
        env_valid, env_msg = validate_environment(str(plist_path_obj))
        checks['environment'] = env_valid

        if verbose or not env_valid:
            status = "✓" if env_valid else "✗"
            print(f"  {status} Environment: {env_msg}")

    # 1.7 Check exit code (detect crashes)
    exit_healthy, exit_msg = check_exit_status(label)
    checks['exit_code'] = exit_healthy

    if verbose or not exit_healthy:
        status = "✓" if exit_healthy else "✗"
        print(f"  {status} Exit code: {exit_msg}")

    # 2. Check log freshness
    if log_path:
        is_fresh, msg = check_log_freshness(log_path, workflow_type, interval_seconds)
        checks['log_fresh'] = is_fresh

        if verbose or not is_fresh:
            status = "✓" if is_fresh else "✗"
            print(f"  {status} Log freshness: {msg}")

    # 2.5 Check error log for failure patterns
    if log_path:
        error_healthy, error_msg = check_error_log(log_path, workflow_type, interval_seconds)
        checks['error_log'] = error_healthy

        if verbose or not error_healthy:
            status = "✓" if error_healthy else "✗"
            print(f"  {status} Error log: {error_msg}")

    # 3. Check if plist was modified after agent started (needs reload)
    plist_path = Path.home() / "Library/LaunchAgents" / f"{label}.plist"
    if plist_path.exists():
        try:
            plist_mtime = plist_path.stat().st_mtime
            # Get agent start time from launchctl
            result = subprocess.run(
                ['launchctl', 'print', f'gui/{os.getuid()}/{label}'],
                capture_output=True, text=True
            )
            # Check if plist is newer than last successful run in log
            if log_path and Path(os.path.expanduser(log_path)).exists():
                log_mtime = Path(os.path.expanduser(log_path)).stat().st_mtime
                plist_is_stale = plist_mtime > log_mtime
                checks['plist_current'] = not plist_is_stale
                if plist_is_stale:
                    print(f"  ⚠️  Plist modified after last run - AUTO-RELOADING...")
                    try:
                        # Unload and reload the agent
                        subprocess.run(
                            ['launchctl', 'unload', str(plist_path)],
                            capture_output=True, text=True
                        )
                        subprocess.run(
                            ['launchctl', 'load', str(plist_path)],
                            capture_output=True, text=True
                        )
                        print(f"  ✓ Agent reloaded successfully")
                        checks['plist_current'] = True  # Now current after reload
                    except Exception as reload_err:
                        print(f"  ✗ Auto-reload failed: {reload_err}")
                elif verbose:
                    print(f"  ✓ Plist current (no reload needed)")
        except Exception as e:
            if verbose:
                print(f"  ? Could not check plist staleness: {e}")

    # 4. Check workflow-specific activity
    if name in ACTIVITY_CHECKERS and log_path:
        log_path_expanded = os.path.expanduser(log_path)
        is_active, msg = ACTIVITY_CHECKERS[name](log_path_expanded)
        checks['activity'] = is_active
        
        if verbose or not is_active:
            status = "✓" if is_active else "✗"
            print(f"  {status} Activity: {msg}")
    
    # Determine overall health
    critical_checks = ['running']
    if log_path:
        critical_checks.append('log_fresh')
    
    is_healthy = all(checks.get(c, True) for c in critical_checks)
    
    return {
        'name': name,
        'label': label,
        'healthy': is_healthy,
        'checks': checks,
        'critical': critical,
        'description': agent.get('description', name)
    }

def generate_alert_email(critical_failures: List[str], new_failures: List[str],
                         escalated: List[str], system_issues: List[str],
                         results: Dict, restart_failed: List[str] = None,
                         unloaded_critical: List[Dict] = None) -> Tuple[str, str]:
    """Generate HTML and text email for alerts."""
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                   line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #dc2626; border-bottom: 3px solid #dc2626; padding-bottom: 10px; }}
            h2 {{ color: #ea580c; margin-top: 30px; }}
            .critical {{ background: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 10px 0; }}
            .warning {{ background: #fffbeb; border-left: 4px solid #f59e0b; padding: 15px; margin: 10px 0; }}
            .info {{ background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 15px; margin: 10px 0; }}
            ul {{ padding-left: 20px; }}
            li {{ margin: 5px 0; }}
            code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
            .timestamp {{ color: #6b7280; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>🚨 Pete's Brain Health Check Alert</h1>
        <p class="timestamp">Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    
    text = f"🚨 Pete's Brain Health Check Alert\n"
    text += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if critical_failures:
        html += f"""
        <div class="critical">
            <h2>❌ Critical Failures ({len(critical_failures)})</h2>
            <ul>
        """
        text += f"❌ CRITICAL FAILURES ({len(critical_failures)}):\n"
        for name in critical_failures:
            desc = results[name]['description']
            failure_count = get_failure_count(name)
            html += f"<li><strong>{name}</strong> - {desc} (Failed {failure_count} times in last 24h)</li>"
            text += f"  • {name} - {desc} (Failed {failure_count} times in last 24h)\n"
        html += "</ul></div>"
        text += "\n"
    
    if escalated:
        html += f"""
        <div class="critical">
            <h2>⚠️ Escalated Agents ({len(escalated)})</h2>
            <p>These agents have failed multiple times and require immediate attention:</p>
            <ul>
        """
        text += f"⚠️ ESCALATED AGENTS ({len(escalated)}):\n"
        for name in escalated:
            desc = results[name]['description']
            failure_count = get_failure_count(name)
            html += f"<li><strong>{name}</strong> - {desc} ({failure_count} failures)</li>"
            text += f"  • {name} - {desc} ({failure_count} failures)\n"
        html += "</ul></div>"
        text += "\n"

    if unloaded_critical:
        html += f"""
        <div class="critical">
            <h2>🔴 Unloaded Critical Agents ({len(unloaded_critical)})</h2>
            <p>These critical agents are NOT LOADED and need immediate attention:</p>
            <ul>
        """
        text += f"🔴 UNLOADED CRITICAL AGENTS ({len(unloaded_critical)}):\n"
        for agent in unloaded_critical:
            html += f"<li><strong>{agent['name']}</strong> - {agent['description']}<br>"
            html += f"<code>launchctl load ~/Library/LaunchAgents/{agent['label']}.plist</code></li>"
            text += f"  • {agent['name']} - {agent['description']}\n"
            text += f"    → launchctl load ~/Library/LaunchAgents/{agent['label']}.plist\n"
        html += "</ul></div>"
        text += "\n"

    if new_failures:
        html += f"""
        <div class="warning">
            <h2>🆕 New Failures ({len(new_failures)})</h2>
            <ul>
        """
        text += f"🆕 NEW FAILURES ({len(new_failures)}):\n"
        for name in new_failures:
            desc = results[name]['description']
            html += f"<li><strong>{name}</strong> - {desc}</li>"
            text += f"  • {name} - {desc}\n"
        html += "</ul></div>"
        text += "\n"
    
    if restart_failed:
        html += f"""
        <div class="critical">
            <h2>🔄 Restart Failed ({len(restart_failed)})</h2>
            <p>These agents could not be automatically restarted:</p>
            <ul>
        """
        text += f"🔄 RESTART FAILED ({len(restart_failed)}):\n"
        for name in restart_failed:
            desc = results[name]['description']
            html += f"<li><strong>{name}</strong> - {desc}</li>"
            text += f"  • {name} - {desc}\n"
        html += "</ul></div>"
        text += "\n"
    
    if system_issues:
        html += f"""
        <div class="warning">
            <h2>💻 System Issues ({len(system_issues)})</h2>
            <ul>
        """
        text += f"💻 SYSTEM ISSUES ({len(system_issues)}):\n"
        for issue in system_issues:
            html += f"<li>{issue}</li>"
            text += f"  • {issue}\n"
        html += "</ul></div>"
        text += "\n"
    
    html += """
        <hr>
        <p style="color: #6b7280; font-size: 12px;">
        This is an automated alert from Pete's Brain Health Check System.<br>
        Check logs: <code>tail -f ~/.petesbrain-health-check.log</code><br>
        View dashboard: <code>python3 agents/agent-dashboard/agent-dashboard.py</code>
        </p>
    </body>
    </html>
    """
    
    return html, text

def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    auto_restart = "--restart-unhealthy" in sys.argv
    no_alerts = "--no-alerts" in sys.argv

    print("="*80)
    print("Pete's Brain System Health Check (Enhanced)")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %A')}")
    print("="*80)
    print()

    # Check health check itself
    hc_healthy, hc_msg = check_health_check_itself()
    if not hc_healthy:
        print(f"⚠️  Health check self-monitoring: {hc_msg}")
        if not no_alerts:
            send_email_alert(
                "⚠️ Health Check Not Running",
                f"<p>The health check system hasn't run in a while:</p><p>{hc_msg}</p>",
                f"Health check issue: {hc_msg}",
                critical=True
            )

            # Send macOS notification for health-check self-monitoring
            send_macos_notification(
                title="⚠️ Health Check Not Running",
                subtitle="Health check system hasn't run recently",
                message=hc_msg,
                critical=True,
                action_command=f"python3 {PROJECT_ROOT}/agents/agent-dashboard/agent-dashboard.py"
            )

    if not DISCOVERY_AVAILABLE:
        print("❌ LaunchAgent discovery not available")
        print("   Install required dependencies or use manual configuration")
        return 2

    # Discover all agents WITH STATUS (loaded/unloaded)
    print("🔍 Discovering LaunchAgents...")
    agents = get_all_agents_with_status()
    print(f"   Found {len(agents)} agent(s)\n")

    if not agents:
        print("⚠️  No PetesBrain agents found")
        return 1

    # Check for unloaded agents (especially critical ones)
    unloaded_agents = [a for a in agents if not a['status']['loaded']]
    unloaded_critical = [a for a in unloaded_agents if a['critical']]

    if unloaded_agents:
        print(f"⚠️  {len(unloaded_agents)} agent(s) NOT LOADED:")
        for agent in unloaded_agents:
            critical_marker = "🔴 CRITICAL" if agent['critical'] else "⚪"
            print(f"   {critical_marker} {agent['name']} - {agent['description']}")
        print()

    # Check system resources
    print("💻 Checking system resources...")
    system_issues = []
    
    disk_ok, disk_msg = check_disk_space()
    if not disk_ok:
        system_issues.append(f"Disk space: {disk_msg}")
        print(f"  ✗ {disk_msg}")
    elif verbose:
        print(f"  ✓ {disk_msg}")
    
    memory_ok, memory_msg = check_memory()
    if not memory_ok:
        system_issues.append(f"Memory: {memory_msg}")
        print(f"  ✗ {memory_msg}")
    elif verbose:
        print(f"  ✓ {memory_msg}")
    
    internet_ok, internet_msg = check_internet()
    if not internet_ok:
        system_issues.append(f"Internet: {internet_msg}")
        print(f"  ✗ {internet_msg}")
    elif verbose:
        print(f"  ✓ {internet_msg}")
    
    print()

    # Check dependencies
    if verbose:
        print("🔗 Checking dependencies...")
        gmail_ok, gmail_msg = check_gmail_api()
        print(f"  {'✓' if gmail_ok else '✗'} Gmail API: {gmail_msg}")
        
        ads_ok, ads_msg = check_google_ads_api()
        print(f"  {'✓' if ads_ok else '✗'} Google Ads API: {ads_msg}")
        print()

    # Check health of each agent
    results = {}
    unhealthy_workflows = []
    critical_failures = []

    # First, mark unloaded agents as unhealthy (BEFORE checking running agents)
    for agent in unloaded_agents:
        name = agent['name']
        results[name] = {
            'name': name,
            'label': agent['label'],
            'healthy': False,
            'checks': {'loaded': False},
            'critical': agent['critical'],
            'description': agent['description']
        }
        unhealthy_workflows.append(name)
        if agent['critical']:
            critical_failures.append(name)
            # Record failure for unloaded critical agents
            record_failure(name, True)

    # Then check health of loaded agents
    loaded_agents = [a for a in agents if a['status']['loaded']]
    for agent in loaded_agents:
        name = agent['name']

        if verbose:
            print(f"\n{'─'*80}")
            print(f"Checking: {name}")
            print(f"Description: {agent.get('description', 'N/A')}")

        result = check_agent_health(agent, verbose)
        results[name] = result

        if not result['healthy']:
            unhealthy_workflows.append(name)
            if result['critical']:
                critical_failures.append(name)
            # Record failure
            record_failure(name, result['critical'])

    # Get new failures
    new_failures = get_new_failures(unhealthy_workflows)
    
    # Check for escalated agents
    escalated = [name for name in critical_failures if check_escalation(name)]

    # Print summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)

    healthy_count = sum(1 for r in results.values() if r['healthy'])
    total_count = len(results)
    critical_count = sum(1 for r in results.values() if r['critical'])

    print(f"\nHealthy: {healthy_count}/{total_count} workflows")
    print(f"Critical agents: {critical_count}")

    if unloaded_critical:
        print(f"\n🔴 UNLOADED CRITICAL AGENTS ({len(unloaded_critical)}):")
        for agent in unloaded_critical:
            print(f"   • {agent['name']} - {agent['description']}")
            print(f"     → NOT LOADED - needs: launchctl load ~/Library/LaunchAgents/{agent['label']}.plist")

    if critical_failures:
        print(f"\n❌ CRITICAL FAILURES ({len(critical_failures)}):")
        for name in critical_failures:
            desc = results[name]['description']
            failure_count = get_failure_count(name)
            print(f"   • {name} - {desc} (Failed {failure_count}x in 24h)")

    if escalated:
        print(f"\n⚠️  ESCALATED ({len(escalated)}):")
        for name in escalated:
            desc = results[name]['description']
            failure_count = get_failure_count(name)
            print(f"   • {name} - {desc} ({failure_count} failures)")

    if new_failures:
        print(f"\n🆕 NEW FAILURES ({len(new_failures)}):")
        for name in new_failures:
            desc = results[name]['description']
            print(f"   • {name} - {desc}")

    if unhealthy_workflows and not critical_failures:
        print(f"\n⚠️  NON-CRITICAL ISSUES ({len(unhealthy_workflows)}):")
        for name in unhealthy_workflows:
            if name not in critical_failures:
                desc = results[name]['description']
                print(f"   • {name} - {desc}")

    if system_issues:
        print(f"\n💻 SYSTEM ISSUES ({len(system_issues)}):")
        for issue in system_issues:
            print(f"   • {issue}")

    if not unhealthy_workflows and not system_issues:
        print("\n✅ ALL SYSTEMS HEALTHY")
        save_current_state([])
        return 0

    # Handle unhealthy workflows
    restart_failed = []
    if auto_restart and not dry_run:
        print(f"\n🔄 Attempting to restart {len(unhealthy_workflows)} unhealthy workflow(s)...")

        for name in unhealthy_workflows:
            label = results[name]['label']
            print(f"\n   Restarting {name}...")

            if restart_workflow(label):
                print(f"   ✓ Restarted {name}")
                log_alert(f"Auto-restarted unhealthy workflow: {name}")
            else:
                print(f"   ✗ Failed to restart {name}")
                restart_failed.append(name)
                log_alert(f"FAILED to restart workflow: {name}")

    elif auto_restart and dry_run:
        print(f"\n🔍 DRY RUN - Would restart {len(unhealthy_workflows)} workflow(s)")

    # Save current state
    save_current_state(unhealthy_workflows)

    # Send alerts
    if not no_alerts and (critical_failures or new_failures or escalated or restart_failed or system_issues):
        # Determine what to alert on
        agents_to_alert = []
        
        # Always alert on critical failures
        for name in critical_failures:
            if should_alert(name, "critical"):
                agents_to_alert.append(name)
                record_alert(name, "critical")
        
        # Alert on new failures
        for name in new_failures:
            if should_alert(name, "new_failure"):
                agents_to_alert.append(name)
                record_alert(name, "new_failure")
        
        # Alert on escalated
        for name in escalated:
            if should_alert(name, "escalated"):
                agents_to_alert.append(name)
                record_alert(name, "escalated")
        
        if agents_to_alert or restart_failed or system_issues or unloaded_critical:
            # Generate alert email
            html, text = generate_alert_email(
                critical_failures=[n for n in critical_failures if n in agents_to_alert],
                new_failures=[n for n in new_failures if n in agents_to_alert],
                escalated=[n for n in escalated if n in agents_to_alert],
                system_issues=system_issues,
                results=results,
                restart_failed=restart_failed,
                unloaded_critical=unloaded_critical
            )
            
            # Send email
            subject = "🚨 Pete's Brain Health Check Alert"
            if unloaded_critical:
                subject = f"🔴 CRITICAL: {len(unloaded_critical)} Agent(s) NOT LOADED"
            elif critical_failures:
                subject = f"🚨 CRITICAL: {len(critical_failures)} Agent(s) Failed"
            elif new_failures:
                subject = f"⚠️ {len(new_failures)} New Agent Failure(s)"
            
            send_email_alert(subject, html, text, critical=bool(critical_failures))

            # Send macOS notification (only for NEW failures)
            if new_failures or unloaded_critical:
                notif_title, notif_subtitle, notif_message, is_critical = build_notification_summary(
                    critical_failures=critical_failures if unloaded_critical else [],
                    new_failures=new_failures,
                    escalated=[],  # Don't include escalated in notifications (already known failures)
                    restart_failed=restart_failed,
                    unloaded_critical=unloaded_critical,
                    system_issues=system_issues if system_issues else []
                )

                # Command to open agent dashboard in browser when notification clicked
                dashboard_cmd = f"python3 {PROJECT_ROOT}/agents/agent-dashboard/agent-dashboard.py"

                send_macos_notification(
                    title=notif_title,
                    subtitle=notif_subtitle,
                    message=notif_message,
                    critical=is_critical,
                    action_command=dashboard_cmd
                )

            # Send Slack if configured
            if agents_to_alert or restart_failed:
                slack_msg = f"🚨 Pete's Brain Alert: {len(agents_to_alert)} agent(s) need attention"
                if critical_failures:
                    slack_msg += f"\nCRITICAL: {', '.join(critical_failures[:3])}"
                send_slack_alert(slack_msg)

    # Log critical failures
    if critical_failures:
        log_alert(f"CRITICAL: {len(critical_failures)} critical workflows unhealthy: {critical_failures}")
        return 2
    elif unhealthy_workflows:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
