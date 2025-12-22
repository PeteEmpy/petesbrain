#!/usr/bin/env python3
"""
Task Manager Alert System

Monitors Task Manager health and sends macOS notifications when issues detected.
Designed to run periodically via LaunchAgent or manually.

Alert Levels:
- CRITICAL: Server down, port conflicts, crashed processes
- WARNING: Configuration drift, stale PIDs, integration test failures
- INFO: Normal operations, health checks passed

Usage:
    python3 alerts.py [--check-interval SECONDS] [--log-file PATH]

Options:
    --check-interval    Seconds between health checks (default: 300)
    --log-file          Alert log file path (default: ~/.petesbrain-task-manager-alerts.log)
"""

import json
import os
import sys
import time
import socket
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError

# Load configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'

class AlertLevel:
    CRITICAL = 'CRITICAL'
    WARNING = 'WARNING'
    INFO = 'INFO'

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def load_config() -> Dict:
    """Load configuration file"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path"""
    return Path(os.path.expanduser(os.path.expandvars(path)))

def send_notification(title: str, message: str, level: AlertLevel = AlertLevel.INFO):
    """Send macOS notification"""
    try:
        # Use osascript to send notification
        sound = 'Basso' if level == AlertLevel.CRITICAL else 'default'

        script = f'''
        display notification "{message}" with title "{title}" sound name "{sound}"
        '''

        subprocess.run(['osascript', '-e', script], check=True)
    except Exception as e:
        print(f"{Colors.RED}Failed to send notification: {e}{Colors.END}")

def log_alert(message: str, level: AlertLevel, log_file: Path):
    """Log alert to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"{Colors.RED}Failed to write log: {e}{Colors.END}")

def alert(title: str, message: str, level: AlertLevel, log_file: Path, silent: bool = False):
    """Send alert and log it"""
    # Color code terminal output
    if level == AlertLevel.CRITICAL:
        color = Colors.RED
        icon = '🚨'
    elif level == AlertLevel.WARNING:
        color = Colors.YELLOW
        icon = '⚠️'
    else:
        color = Colors.GREEN
        icon = 'ℹ️'

    if not silent:
        print(f"{color}{icon} [{level}] {title}: {message}{Colors.END}")

    # Send macOS notification for non-INFO alerts
    if level != AlertLevel.INFO:
        send_notification(title, message, level)

    # Log to file
    log_alert(f"{title}: {message}", level, log_file)

def check_server_health(config: Dict, log_file: Path) -> Tuple[int, int]:
    """Check if servers are responding to health checks"""
    critical_issues = 0
    warnings = 0

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        port = server_config['port']

        try:
            # Check if port is open
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            sock.close()

            if result != 0:
                alert(
                    "Server Down",
                    f"{server_name} not responding on port {port}",
                    AlertLevel.CRITICAL,
                    log_file
                )
                critical_issues += 1
                continue

            # Check health endpoint
            try:
                response = urlopen(f'http://localhost:{port}/health', timeout=5)
                data = json.loads(response.read().decode('utf-8'))

                if data.get('status') != 'healthy':
                    alert(
                        "Server Unhealthy",
                        f"{server_name} reporting unhealthy status",
                        AlertLevel.WARNING,
                        log_file
                    )
                    warnings += 1
            except URLError:
                alert(
                    "Health Check Failed",
                    f"{server_name} health endpoint not responding",
                    AlertLevel.WARNING,
                    log_file
                )
                warnings += 1

        except Exception as e:
            alert(
                "Health Check Error",
                f"{server_name}: {str(e)}",
                AlertLevel.WARNING,
                log_file
            )
            warnings += 1

    return critical_issues, warnings

def check_port_conflicts(config: Dict, log_file: Path) -> int:
    """Check for multiple processes on same port"""
    warnings = 0

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        port = server_config['port']

        try:
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')

                if len(pids) > 1:
                    alert(
                        "Port Conflict",
                        f"Multiple processes ({len(pids)}) on port {port}: {', '.join(pids)}",
                        AlertLevel.WARNING,
                        log_file
                    )
                    warnings += 1

        except Exception as e:
            alert(
                "Port Check Error",
                f"Failed to check port {port}: {str(e)}",
                AlertLevel.WARNING,
                log_file
            )
            warnings += 1

    return warnings

def check_stale_pid_files(config: Dict, log_file: Path) -> int:
    """Check for stale PID files"""
    warnings = 0

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        pid_file = expand_path(server_config['pid_file'])

        if not pid_file.exists():
            continue

        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())

            # Check if process exists
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                # Stale PID file
                alert(
                    "Stale PID File",
                    f"{server_name} has stale PID file (process {pid} not running)",
                    AlertLevel.WARNING,
                    log_file
                )
                warnings += 1

        except (ValueError, IOError):
            alert(
                "Corrupt PID File",
                f"{server_name} has corrupt PID file",
                AlertLevel.WARNING,
                log_file
            )
            warnings += 1

    return warnings

def check_launchagent_status(config: Dict, log_file: Path) -> Tuple[int, int]:
    """Check LaunchAgent health"""
    critical_issues = 0
    warnings = 0

    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )

        for agent_name, agent_config in config['launchagents'].items():
            label = agent_config['label']

            if label not in result.stdout:
                alert(
                    "LaunchAgent Not Loaded",
                    f"{label} is not loaded in launchctl",
                    AlertLevel.CRITICAL,
                    log_file
                )
                critical_issues += 1
                continue

            # Parse status
            for line in result.stdout.split('\n'):
                if label in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        exit_code = parts[1]

                        if exit_code != '0' and exit_code != '-':
                            alert(
                                "LaunchAgent Crashed",
                                f"{label} exited with code {exit_code}",
                                AlertLevel.CRITICAL,
                                log_file
                            )
                            critical_issues += 1

    except Exception as e:
        alert(
            "LaunchAgent Check Error",
            f"Failed to check LaunchAgent status: {str(e)}",
            AlertLevel.WARNING,
            log_file
        )
        warnings += 1

    return critical_issues, warnings

def check_state_files(config: Dict, log_file: Path) -> int:
    """Check state files exist and valid"""
    warnings = 0

    base_dir = expand_path(config['paths']['base_dir'])
    state_file = base_dir / config['paths']['state_file']

    if not state_file.exists():
        alert(
            "Missing State File",
            f"State file not found: {state_file}",
            AlertLevel.WARNING,
            log_file
        )
        warnings += 1
    else:
        # Verify valid JSON
        try:
            with open(state_file, 'r') as f:
                json.load(f)
        except json.JSONDecodeError:
            alert(
                "Corrupt State File",
                f"State file contains invalid JSON: {state_file}",
                AlertLevel.WARNING,
                log_file
            )
            warnings += 1

    return warnings

def run_health_checks(config: Dict, log_file: Path) -> Dict[str, int]:
    """Run all health checks"""
    results = {
        'critical': 0,
        'warnings': 0,
        'checks_run': 0
    }

    # Check 1: Server health
    critical, warnings = check_server_health(config, log_file)
    results['critical'] += critical
    results['warnings'] += warnings
    results['checks_run'] += 1

    # Check 2: Port conflicts
    warnings = check_port_conflicts(config, log_file)
    results['warnings'] += warnings
    results['checks_run'] += 1

    # Check 3: Stale PID files
    warnings = check_stale_pid_files(config, log_file)
    results['warnings'] += warnings
    results['checks_run'] += 1

    # Check 4: LaunchAgent status
    critical, warnings = check_launchagent_status(config, log_file)
    results['critical'] += critical
    results['warnings'] += warnings
    results['checks_run'] += 1

    # Check 5: State files
    warnings = check_state_files(config, log_file)
    results['warnings'] += warnings
    results['checks_run'] += 1

    return results

def monitor_loop(check_interval: int, log_file: Path):
    """Continuous monitoring loop"""
    config = load_config()

    print(f"{Colors.BOLD}{Colors.BLUE}Task Manager Alert System Started{Colors.END}")
    print(f"{Colors.BLUE}Check interval: {check_interval} seconds{Colors.END}")
    print(f"{Colors.BLUE}Log file: {log_file}{Colors.END}\n")

    while True:
        try:
            results = run_health_checks(config, log_file)

            # Summary
            if results['critical'] == 0 and results['warnings'] == 0:
                alert(
                    "Health Check Complete",
                    f"{results['checks_run']} checks passed - all systems healthy",
                    AlertLevel.INFO,
                    log_file,
                    silent=True  # Don't spam terminal for healthy checks
                )
            else:
                summary = f"{results['critical']} critical, {results['warnings']} warnings"
                level = AlertLevel.CRITICAL if results['critical'] > 0 else AlertLevel.WARNING

                alert(
                    "Health Check Issues",
                    summary,
                    level,
                    log_file
                )

            # Wait for next check
            time.sleep(check_interval)

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Monitoring stopped by user{Colors.END}")
            break
        except Exception as e:
            alert(
                "Monitor Error",
                f"Unexpected error: {str(e)}",
                AlertLevel.WARNING,
                log_file
            )
            time.sleep(check_interval)

def run_once(log_file: Path) -> int:
    """Run checks once and exit"""
    config = load_config()

    print(f"{Colors.BOLD}{Colors.BLUE}Task Manager Health Check{Colors.END}\n")

    results = run_health_checks(config, log_file)

    # Print summary
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Checks run: {results['checks_run']}")
    print(f"  {Colors.RED}Critical issues: {results['critical']}{Colors.END}")
    print(f"  {Colors.YELLOW}Warnings: {results['warnings']}{Colors.END}")

    if results['critical'] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ CRITICAL ISSUES DETECTED{Colors.END}")
        return 1
    elif results['warnings'] > 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ WARNINGS DETECTED{Colors.END}")
        return 2
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL CHECKS PASSED{Colors.END}")
        return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Task Manager Alert System')
    parser.add_argument('--check-interval', type=int, default=300, help='Seconds between checks (default: 300)')
    parser.add_argument('--log-file', type=str, default='~/.petesbrain-task-manager-alerts.log', help='Alert log file path')
    parser.add_argument('--continuous', action='store_true', help='Run continuously (default: run once)')
    args = parser.parse_args()

    log_file = expand_path(args.log_file)

    try:
        if args.continuous:
            monitor_loop(args.check_interval, log_file)
        else:
            exit_code = run_once(log_file)
            sys.exit(exit_code)
    except Exception as e:
        print(f"{Colors.RED}❌ Alert system error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()
