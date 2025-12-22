#!/usr/bin/env python3
"""
Task Manager Automated Recovery Script

Detects and fixes common Task Manager issues automatically:
1. Removes stale PID files
2. Kills duplicate processes
3. Fixes configuration drift
4. Creates missing state files
5. Restarts crashed servers

Usage:
    python3 recovery.py [--dry-run] [--auto-restart]

Options:
    --dry-run       Show what would be fixed without making changes
    --auto-restart  Automatically restart servers after fixes
"""

import json
import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

# Load configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'

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

def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print("=" * len(title))

def print_fix(message: str, dry_run: bool = False):
    """Print fix message"""
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{Colors.YELLOW}🔧 {prefix}{message}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_stale_pid_files(config: Dict, dry_run: bool = False) -> int:
    """Remove stale PID files"""
    print_section("Checking for Stale PID Files")

    fixed = 0

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
                print_info(f"{server_name}: PID file valid (process {pid} exists)")
            except ProcessLookupError:
                # Stale PID file - process doesn't exist
                print_fix(f"Removing stale PID file for {server_name} (PID {pid})", dry_run)

                if not dry_run:
                    pid_file.unlink()
                    print_success(f"Removed stale PID file: {pid_file}")

                fixed += 1

        except (ValueError, IOError) as e:
            print_fix(f"Removing corrupt PID file for {server_name}", dry_run)

            if not dry_run:
                pid_file.unlink()
                print_success(f"Removed corrupt PID file: {pid_file}")

            fixed += 1

    if fixed == 0:
        print_success("No stale PID files found")

    return fixed

def check_port_conflicts(config: Dict, dry_run: bool = False) -> int:
    """Detect and resolve port conflicts"""
    print_section("Checking for Port Conflicts")

    fixed = 0

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        port = server_config['port']

        # Get process using the port
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
                    print_fix(f"Multiple processes on port {port}: {', '.join(pids)}", dry_run)

                    # Kill duplicates (keep first one)
                    for pid in pids[1:]:
                        print_fix(f"Killing duplicate process {pid}", dry_run)

                        if not dry_run:
                            try:
                                os.kill(int(pid), 9)
                                print_success(f"Killed duplicate process {pid}")
                                fixed += 1
                            except:
                                pass
                else:
                    print_info(f"Port {port}: Single process {pids[0]} (expected)")
            else:
                print_info(f"Port {port}: Available (no conflicts)")

        except Exception as e:
            print(f"{Colors.RED}❌ Error checking port {port}: {e}{Colors.END}")

    if fixed == 0:
        print_success("No port conflicts found")

    return fixed

def check_missing_state_files(config: Dict, dry_run: bool = False) -> int:
    """Create missing state files"""
    print_section("Checking State Files")

    fixed = 0

    base_dir = expand_path(config['paths']['base_dir'])
    state_file = base_dir / config['paths']['state_file']

    if not state_file.exists():
        print_fix(f"Creating missing state file: {state_file}", dry_run)

        if not dry_run:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(state_file, 'w') as f:
                json.dump([], f, indent=2)

            print_success(f"Created state file: {state_file}")

        fixed += 1
    else:
        # Verify it's valid JSON
        try:
            with open(state_file, 'r') as f:
                json.load(f)
            print_info(f"State file valid: {state_file}")
        except json.JSONDecodeError:
            print_fix(f"Fixing corrupt state file: {state_file}", dry_run)

            if not dry_run:
                # Backup corrupt file
                backup = state_file.with_suffix('.json.corrupt')
                state_file.rename(backup)

                # Create new empty file
                with open(state_file, 'w') as f:
                    json.dump([], f, indent=2)

                print_success(f"Fixed corrupt file (backup: {backup})")

            fixed += 1

    if fixed == 0:
        print_success("All state files valid")

    return fixed

def check_configuration_drift(config: Dict, dry_run: bool = False) -> int:
    """Detect configuration drift"""
    print_section("Checking Configuration Drift")

    issues = []

    # Check LaunchAgents reference correct scripts
    for agent_name, agent_config in config['launchagents'].items():
        plist_path = expand_path(agent_config['plist_path'])

        if not plist_path.exists():
            issues.append(f"LaunchAgent {agent_config['label']} plist not found")
            continue

        with open(plist_path, 'r') as f:
            plist_content = f.read()

        expected_script = agent_config['expected_script']
        if expected_script not in plist_content:
            issues.append(f"LaunchAgent {agent_config['label']} doesn't reference {expected_script}")

    if issues:
        for issue in issues:
            print(f"{Colors.YELLOW}⚠️  {issue}{Colors.END}")
        print_info("Configuration drift detected - manual review recommended")
        return len(issues)
    else:
        print_success("No configuration drift detected")
        return 0

def check_crashed_servers(config: Dict, dry_run: bool = False, auto_restart: bool = False) -> int:
    """Check if servers have crashed"""
    print_section("Checking for Crashed Servers")

    fixed = 0

    # Check LaunchAgent status
    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )

        for agent_name, agent_config in config['launchagents'].items():
            label = agent_config['label']

            if label in result.stdout:
                # Parse status
                for line in result.stdout.split('\n'):
                    if label in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            pid = parts[0]
                            exit_code = parts[1]

                            if exit_code != '0':
                                print_fix(f"Server {label} exited with code {exit_code}", dry_run)

                                if auto_restart and not dry_run:
                                    print_fix(f"Restarting {label}", dry_run)

                                    subprocess.run(
                                        ['launchctl', 'unload', str(expand_path(agent_config['plist_path']))],
                                        capture_output=True
                                    )

                                    subprocess.run(
                                        ['launchctl', 'load', str(expand_path(agent_config['plist_path']))],
                                        capture_output=True
                                    )

                                    print_success(f"Restarted {label}")
                                    fixed += 1
                            else:
                                print_info(f"{label}: Running (PID {pid}, exit code {exit_code})")
            else:
                print(f"{Colors.RED}❌ {label} not loaded{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}❌ Error checking LaunchAgents: {e}{Colors.END}")

    if fixed == 0 and auto_restart:
        print_success("No crashed servers found")
    elif not auto_restart:
        print_info("Use --auto-restart to automatically restart crashed servers")

    return fixed

def run_recovery(dry_run: bool = False, auto_restart: bool = False) -> Tuple[int, int]:
    """Run all recovery checks"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Task Manager Automated Recovery{Colors.END}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}\n")

    if dry_run:
        print(f"{Colors.YELLOW}Running in DRY RUN mode - no changes will be made{Colors.END}\n")

    config = load_config()
    total_issues = 0
    total_fixed = 0

    # Run all checks
    checks = [
        check_stale_pid_files,
        check_port_conflicts,
        check_missing_state_files,
        check_configuration_drift,
        check_crashed_servers
    ]

    for check in checks:
        if check == check_crashed_servers:
            fixed = check(config, dry_run, auto_restart)
        else:
            fixed = check(config, dry_run)

        if fixed > 0:
            total_issues += fixed
            if not dry_run:
                total_fixed += fixed

    # Print summary
    print_section("Recovery Summary")

    if dry_run:
        print(f"\n{Colors.YELLOW}Total issues detected: {total_issues}{Colors.END}")
        print(f"{Colors.YELLOW}Run without --dry-run to fix automatically{Colors.END}\n")
    else:
        if total_fixed > 0:
            print(f"\n{Colors.GREEN}✅ Fixed {total_fixed} issue(s){Colors.END}\n")
        else:
            print(f"\n{Colors.GREEN}✅ No issues found - system healthy{Colors.END}\n")

    return total_issues, total_fixed

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Task Manager Automated Recovery')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--auto-restart', action='store_true', help='Automatically restart crashed servers')
    args = parser.parse_args()

    try:
        total_issues, total_fixed = run_recovery(args.dry_run, args.auto_restart)

        # Exit with appropriate code
        if args.dry_run:
            sys.exit(1 if total_issues > 0 else 0)
        else:
            sys.exit(0)  # Always exit 0 after recovery attempt

    except Exception as e:
        print(f"{Colors.RED}❌ Recovery error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == '__main__':
    main()
