#!/usr/bin/env python3
"""
Task Manager System Validation Script

Performs 8 comprehensive safety checks before allowing Task Manager to start:
1. Configuration file loads correctly
2. All scripts exist at expected paths
3. All ports available (not in use)
4. PID files don't indicate running duplicates
5. HTML endpoints match backend configuration
6. Python syntax valid for all scripts
7. LaunchAgents configured correctly
8. State files exist and valid JSON

Exit codes:
0 - All checks passed (safe to start)
1 - Critical failure (blocks startup)
2 - Warning only (can proceed with caution)
"""

import json
import os
import sys
import re
import ast
import socket
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ValidationResult:
    """Store validation check results"""
    def __init__(self, name: str, passed: bool, message: str, critical: bool = True):
        self.name = name
        self.passed = passed
        self.message = message
        self.critical = critical

def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print("=" * len(text))

def print_check(name: str, passed: bool, message: str):
    """Print check result"""
    if passed:
        print(f"{Colors.GREEN}✅ {name}{Colors.END}")
    else:
        print(f"{Colors.RED}❌ {name}{Colors.END}")
    if message:
        print(f"   {message}")

def load_config() -> Dict:
    """Load and validate configuration file"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    if not config_path.exists():
        print(f"{Colors.RED}❌ Configuration file not found: {config_path}{Colors.END}")
        sys.exit(1)

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"{Colors.GREEN}✅ Configuration loaded: {config_path}{Colors.END}")
        print(f"   Version: {config.get('version', 'unknown')}")
        return config
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}❌ Invalid JSON in config file: {e}{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Error loading config: {e}{Colors.END}")
        sys.exit(1)

def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path"""
    return Path(os.path.expanduser(os.path.expandvars(path)))

def check_scripts_exist(config: Dict) -> ValidationResult:
    """Check all required scripts exist"""
    base_dir = expand_path(config['paths']['base_dir'])
    scripts_dir = base_dir / config['paths']['scripts_dir']

    missing_scripts = []
    found_scripts = []

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        script_path = expand_path(server_config['script_path'])
        if script_path.exists():
            found_scripts.append(script_path.name)
        else:
            missing_scripts.append(str(script_path))

    if missing_scripts:
        message = f"Missing scripts: {', '.join(missing_scripts)}"
        return ValidationResult("All scripts exist", False, message, critical=True)
    else:
        message = f"{len(found_scripts)} scripts found: {', '.join(found_scripts)}"
        return ValidationResult("All scripts exist", True, message)

def check_ports_available(config: Dict) -> ValidationResult:
    """Check all required ports are available"""
    busy_ports = []
    available_ports = []

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        port = server_config['port']

        # Try to bind to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.bind(('localhost', port))
            sock.close()
            available_ports.append(port)
        except OSError:
            # Port is in use
            busy_ports.append(port)
            sock.close()

    if busy_ports:
        # Check if it's our own servers using PID files
        our_servers = []
        for port in busy_ports:
            # Find which server uses this port
            for server_name, server_config in config['servers'].items():
                if server_config['port'] == port:
                    pid_file = expand_path(server_config['pid_file'])
                    if pid_file.exists():
                        our_servers.append(f"port {port} (likely our {server_name})")
                    else:
                        our_servers.append(f"port {port} (unknown process)")

        message = f"Ports in use: {', '.join(our_servers)}"
        # Not critical if it's our own servers
        return ValidationResult("All ports available", False, message, critical=False)
    else:
        message = f"Ports {', '.join(map(str, available_ports))} available"
        return ValidationResult("All ports available", True, message)

def check_pid_files(config: Dict) -> ValidationResult:
    """Check PID files don't indicate running duplicates"""
    stale_pids = []
    running_pids = []

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
                running_pids.append(f"{server_name} (PID {pid})")
            except ProcessLookupError:
                stale_pids.append(f"{server_name} (stale PID {pid})")
        except (ValueError, IOError):
            stale_pids.append(f"{server_name} (corrupt PID file)")

    if stale_pids:
        message = f"Stale PID files: {', '.join(stale_pids)}"
        return ValidationResult("No stale PID files", False, message, critical=False)
    elif running_pids:
        message = f"Servers already running: {', '.join(running_pids)}"
        return ValidationResult("No duplicate processes", False, message, critical=False)
    else:
        message = "No PID files found (clean state)"
        return ValidationResult("No duplicate processes", True, message)

def check_html_endpoints_match(config: Dict) -> ValidationResult:
    """Check HTML files reference correct backend endpoints"""
    base_dir = expand_path(config['paths']['base_dir'])
    task_manager_dir = base_dir / config['paths']['task_manager_dir']

    mismatches = []
    matches = []

    for html_file, expected_endpoints in config['expected_html_endpoints'].items():
        html_path = task_manager_dir / html_file

        if not html_path.exists():
            mismatches.append(f"{html_file} not found")
            continue

        with open(html_path, 'r') as f:
            html_content = f.read()

        for endpoint in expected_endpoints:
            if endpoint in html_content:
                matches.append(endpoint)
            else:
                mismatches.append(f"{endpoint} not in {html_file}")

    if mismatches:
        message = f"Mismatches: {', '.join(mismatches)}"
        return ValidationResult("HTML endpoints match backend", False, message, critical=True)
    else:
        message = f"{len(matches)} endpoints verified in HTML"
        return ValidationResult("HTML endpoints match backend", True, message)

def check_scripts_syntax(config: Dict) -> ValidationResult:
    """Check Python syntax is valid for all scripts"""
    invalid_scripts = []
    valid_scripts = []

    for server_name, server_config in config['servers'].items():
        if not server_config.get('enabled', True):
            continue

        script_path = expand_path(server_config['script_path'])

        if not script_path.exists():
            continue

        try:
            with open(script_path, 'r') as f:
                source = f.read()
            ast.parse(source)
            valid_scripts.append(script_path.name)
        except SyntaxError as e:
            invalid_scripts.append(f"{script_path.name} (line {e.lineno}: {e.msg})")

    if invalid_scripts:
        message = f"Syntax errors: {', '.join(invalid_scripts)}"
        return ValidationResult("Python syntax valid", False, message, critical=True)
    else:
        message = f"{len(valid_scripts)} scripts have valid syntax"
        return ValidationResult("Python syntax valid", True, message)

def check_launchagents(config: Dict) -> ValidationResult:
    """Check LaunchAgents configured correctly"""
    issues = []
    correct = []

    for agent_name, agent_config in config['launchagents'].items():
        plist_path = expand_path(agent_config['plist_path'])

        if not plist_path.exists():
            issues.append(f"{agent_config['label']} plist not found")
            continue

        with open(plist_path, 'r') as f:
            plist_content = f.read()

        # Check if expected script is referenced
        expected_script = agent_config['expected_script']
        if expected_script not in plist_content:
            issues.append(f"{agent_config['label']} doesn't reference {expected_script}")
        else:
            correct.append(agent_config['label'])

    if issues:
        message = f"LaunchAgent issues: {', '.join(issues)}"
        return ValidationResult("LaunchAgents configured correctly", False, message, critical=False)
    else:
        message = f"{len(correct)} LaunchAgents configured correctly"
        return ValidationResult("LaunchAgents configured correctly", True, message)

def check_state_files(config: Dict) -> ValidationResult:
    """Check state files exist and valid JSON"""
    base_dir = expand_path(config['paths']['base_dir'])
    state_file = base_dir / config['paths']['state_file']

    if not state_file.exists():
        message = f"State file not found: {state_file} (will be created)"
        return ValidationResult("State files valid", False, message, critical=False)

    try:
        with open(state_file, 'r') as f:
            data = json.load(f)

        message = f"State file valid: {len(data) if isinstance(data, list) else 'N/A'} entries"
        return ValidationResult("State files valid", True, message)
    except json.JSONDecodeError as e:
        message = f"Invalid JSON in {state_file}: {e}"
        return ValidationResult("State files valid", False, message, critical=True)

def check_python_modules(config: Dict) -> ValidationResult:
    """Check required Python modules are installed"""
    required_modules = ['json', 'os', 'sys', 'pathlib', 'http', 'datetime']
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        message = f"Missing modules: {', '.join(missing_modules)}"
        return ValidationResult("Required Python modules installed", False, message, critical=True)
    else:
        message = f"All {len(required_modules)} required modules available"
        return ValidationResult("Required Python modules installed", True, message)

def run_all_checks(config: Dict) -> List[ValidationResult]:
    """Run all validation checks"""
    results = []

    print_header("Running Task Manager Validation Checks")

    # Check 1: Scripts exist
    print("\n🔍 Check 1: Scripts Exist")
    result = check_scripts_exist(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 2: Ports available
    print("\n🔍 Check 2: Ports Available")
    result = check_ports_available(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 3: PID files
    print("\n🔍 Check 3: PID Files")
    result = check_pid_files(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 4: HTML endpoints match
    print("\n🔍 Check 4: HTML Endpoints Match Backend")
    result = check_html_endpoints_match(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 5: Python syntax
    print("\n🔍 Check 5: Python Syntax")
    result = check_scripts_syntax(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 6: LaunchAgents
    print("\n🔍 Check 6: LaunchAgents Configuration")
    result = check_launchagents(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 7: State files
    print("\n🔍 Check 7: State Files")
    result = check_state_files(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    # Check 8: Python modules
    print("\n🔍 Check 8: Python Modules")
    result = check_python_modules(config)
    print_check(result.name, result.passed, result.message)
    results.append(result)

    return results

def print_summary(results: List[ValidationResult]):
    """Print validation summary"""
    print_header("Validation Summary")

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    critical_failures = sum(1 for r in results if not r.passed and r.critical)
    warnings = sum(1 for r in results if not r.passed and not r.critical)

    print(f"\n{Colors.BOLD}Total Checks: {len(results)}{Colors.END}")
    print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.END}")

    if critical_failures > 0:
        print(f"{Colors.RED}❌ Critical Failures: {critical_failures}{Colors.END}")

    if warnings > 0:
        print(f"{Colors.YELLOW}⚠️  Warnings: {warnings}{Colors.END}")

    print()

    if critical_failures > 0:
        print(f"{Colors.RED}{Colors.BOLD}❌ VALIDATION FAILED - Task Manager cannot start safely{Colors.END}")
        print(f"{Colors.RED}Fix the critical issues above and try again{Colors.END}")
        return 1
    elif warnings > 0:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  WARNINGS DETECTED - Task Manager can start but may have issues{Colors.END}")
        print(f"{Colors.YELLOW}Consider fixing warnings before proceeding{Colors.END}")
        return 2
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL CHECKS PASSED - Safe to start Task Manager{Colors.END}")
        return 0

def main():
    """Main validation entry point"""
    print(f"\n{Colors.BOLD}Task Manager System Validation{Colors.END}")
    print(f"Date: {os.popen('date').read().strip()}")

    # Load configuration
    config = load_config()

    # Run all checks
    results = run_all_checks(config)

    # Print summary
    exit_code = print_summary(results)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
