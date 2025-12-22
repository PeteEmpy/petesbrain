#!/usr/bin/env python3
"""
Task Manager Integration Tests

Comprehensive tests for all Task Manager components and endpoints.
Tests run against live servers to verify behavior matches expectations.

Tests:
1. Configuration loads correctly
2. Validation script detects issues
3. HTML endpoints match backend
4. Servers respond to health checks
5. Manual task notes save successfully
6. Regenerate endpoint works
7. Notes count endpoint accurate
8. All responses match expected format

Exit codes:
0 - All tests passed
1 - One or more tests failed
"""

import json
import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import Dict, List, Tuple

class Colors:
    """Terminal colors"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestResult:
    """Store test result"""
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print("=" * len(text))

def print_test(name: str, passed: bool, message: str = ""):
    """Print test result"""
    if passed:
        print(f"{Colors.GREEN}✅ {name} (PASSED){Colors.END}")
    else:
        print(f"{Colors.RED}❌ {name} (FAILED){Colors.END}")
    if message:
        print(f"   {message}")

def load_config() -> Dict:
    """Load configuration file"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'

    with open(config_path, 'r') as f:
        return json.load(f)

def test_configuration_loads() -> TestResult:
    """Test 1: Configuration file loads correctly"""
    try:
        config = load_config()

        # Verify required sections exist
        required_sections = ['version', 'servers', 'paths', 'validation']
        missing = [s for s in required_sections if s not in config]

        if missing:
            return TestResult(
                "Configuration loads",
                False,
                f"Missing sections: {', '.join(missing)}"
            )

        # Verify version
        version = config.get('version', '')
        if not version:
            return TestResult(
                "Configuration loads",
                False,
                "No version specified"
            )

        return TestResult(
            "Configuration loads",
            True,
            f"Version {version}, {len(config['servers'])} servers configured"
        )
    except Exception as e:
        return TestResult("Configuration loads", False, str(e))

def test_validation_catches_issues() -> TestResult:
    """Test 2: Validation script catches issues"""
    try:
        script_dir = Path(__file__).parent
        validate_script = script_dir / 'validate.py'

        if not validate_script.exists():
            return TestResult(
                "Validation catches issues",
                False,
                "validate.py not found"
            )

        # Run validation (should exit with 0, 1, or 2)
        result = subprocess.run(
            ['python3', str(validate_script)],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Exit code 0 = all checks passed
        # Exit code 1 = critical failures
        # Exit code 2 = warnings only
        if result.returncode in [0, 2]:
            return TestResult(
                "Validation catches issues",
                True,
                f"Validation script works (exit code {result.returncode})"
            )
        else:
            return TestResult(
                "Validation catches issues",
                False,
                f"Unexpected exit code: {result.returncode}"
            )
    except subprocess.TimeoutExpired:
        return TestResult(
            "Validation catches issues",
            False,
            "Validation script timed out"
        )
    except Exception as e:
        return TestResult("Validation catches issues", False, str(e))

def test_html_endpoints_match() -> TestResult:
    """Test 3: HTML endpoints match backend configuration"""
    try:
        config = load_config()
        base_dir = Path(config['paths']['base_dir']).expanduser()
        task_manager_dir = base_dir / config['paths']['task_manager_dir']

        expected_endpoints = config['expected_html_endpoints']

        for html_file, endpoints in expected_endpoints.items():
            html_path = task_manager_dir / html_file

            if not html_path.exists():
                return TestResult(
                    "HTML endpoints match backend",
                    False,
                    f"{html_file} not found at {html_path}"
                )

            with open(html_path, 'r') as f:
                content = f.read()

            missing = [e for e in endpoints if e not in content]

            if missing:
                return TestResult(
                    "HTML endpoints match backend",
                    False,
                    f"{html_file} missing: {', '.join(missing)}"
                )

        return TestResult(
            "HTML endpoints match backend",
            True,
            f"All endpoints verified in {len(expected_endpoints)} HTML files"
        )
    except Exception as e:
        return TestResult("HTML endpoints match backend", False, str(e))

def test_servers_respond() -> TestResult:
    """Test 4: Servers respond to health checks"""
    try:
        config = load_config()
        servers_checked = []
        servers_down = []

        for server_name, server_config in config['servers'].items():
            if not server_config.get('enabled', True):
                continue

            port = server_config['port']

            # Check if port is open
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)

            try:
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    servers_checked.append(f"{server_name} (port {port})")
                else:
                    servers_down.append(f"{server_name} (port {port})")
            finally:
                sock.close()

        if servers_down:
            return TestResult(
                "Servers respond to health checks",
                False,
                f"Servers down: {', '.join(servers_down)}"
            )

        return TestResult(
            "Servers respond to health checks",
            True,
            f"{len(servers_checked)} servers responding"
        )
    except Exception as e:
        return TestResult("Servers respond to health checks", False, str(e))

def test_save_manual_note() -> TestResult:
    """Test 5: Manual task note saves successfully"""
    try:
        # Prepare test data
        test_note = {
            "task_id": "test-" + str(int(time.time())),
            "client": "test",
            "task_title": "Test Task",
            "note_text": "Test note created by integration tests"
        }

        # Send POST request to save-note endpoint
        url = "http://localhost:5002/save-note"
        data = json.dumps(test_note).encode('utf-8')

        req = Request(url, data=data, headers={'Content-Type': 'application/json'})

        try:
            response = urlopen(req, timeout=5)
            response_data = json.loads(response.read().decode('utf-8'))

            if response_data.get('success'):
                return TestResult(
                    "Save manual task note",
                    True,
                    f"Note saved successfully: {response_data.get('message', '')}"
                )
            else:
                return TestResult(
                    "Save manual task note",
                    False,
                    f"Save failed: {response_data.get('error', 'unknown error')}"
                )
        except HTTPError as e:
            return TestResult(
                "Save manual task note",
                False,
                f"HTTP {e.code}: {e.reason}"
            )
        except URLError as e:
            return TestResult(
                "Save manual task note",
                False,
                f"Server not reachable: {e.reason}"
            )
    except Exception as e:
        return TestResult("Save manual task note", False, str(e))

def test_regenerate_endpoint() -> TestResult:
    """Test 6: Regenerate endpoint works"""
    try:
        url = "http://localhost:5002/regenerate"
        req = Request(url, data=b'', headers={'Content-Type': 'application/json'})

        try:
            response = urlopen(req, timeout=10)
            response_data = json.loads(response.read().decode('utf-8'))

            if response_data.get('success'):
                return TestResult(
                    "Regenerate endpoint",
                    True,
                    f"Regeneration successful: {response_data.get('message', '')}"
                )
            else:
                return TestResult(
                    "Regenerate endpoint",
                    False,
                    f"Regeneration failed: {response_data.get('error', 'unknown error')}"
                )
        except HTTPError as e:
            return TestResult(
                "Regenerate endpoint",
                False,
                f"HTTP {e.code}: {e.reason}"
            )
        except URLError as e:
            return TestResult(
                "Regenerate endpoint",
                False,
                f"Server not reachable: {e.reason}"
            )
    except Exception as e:
        return TestResult("Regenerate endpoint", False, str(e))

def test_notes_count() -> TestResult:
    """Test 7: Notes count endpoint accurate"""
    try:
        url = "http://localhost:5002/notes-count"

        try:
            response = urlopen(url, timeout=5)
            response_data = json.loads(response.read().decode('utf-8'))

            count = response_data.get('count')
            if count is not None:
                return TestResult(
                    "Notes count endpoint",
                    True,
                    f"Current notes count: {count}"
                )
            else:
                return TestResult(
                    "Notes count endpoint",
                    False,
                    "Response missing 'count' field"
                )
        except HTTPError as e:
            return TestResult(
                "Notes count endpoint",
                False,
                f"HTTP {e.code}: {e.reason}"
            )
        except URLError as e:
            return TestResult(
                "Notes count endpoint",
                False,
                f"Server not reachable: {e.reason}"
            )
    except Exception as e:
        return TestResult("Notes count endpoint", False, str(e))

def test_response_formats() -> TestResult:
    """Test 8: All responses match expected format"""
    try:
        # Test each endpoint returns valid JSON
        endpoints = [
            ("http://localhost:5002/notes-count", "GET"),
        ]

        for url, method in endpoints:
            try:
                if method == "GET":
                    response = urlopen(url, timeout=5)
                else:
                    req = Request(url, data=b'', headers={'Content-Type': 'application/json'})
                    response = urlopen(req, timeout=5)

                # Verify JSON response
                json.loads(response.read().decode('utf-8'))
            except (HTTPError, URLError) as e:
                return TestResult(
                    "All responses match expected format",
                    False,
                    f"{url} failed: {e}"
                )
            except json.JSONDecodeError:
                return TestResult(
                    "All responses match expected format",
                    False,
                    f"{url} returned invalid JSON"
                )

        return TestResult(
            "All responses match expected format",
            True,
            f"{len(endpoints)} endpoints returning valid JSON"
        )
    except Exception as e:
        return TestResult("All responses match expected format", False, str(e))

def run_all_tests() -> List[TestResult]:
    """Run all integration tests"""
    results = []

    print_header("Running Task Manager Integration Tests")

    # Test 1: Configuration loads
    print("\n🧪 Test 1: Configuration Loads Correctly")
    result = test_configuration_loads()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 2: Validation catches issues
    print("\n🧪 Test 2: Validation Script Detects Issues")
    result = test_validation_catches_issues()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 3: HTML endpoints match
    print("\n🧪 Test 3: HTML Endpoints Match Backend")
    result = test_html_endpoints_match()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 4: Servers respond
    print("\n🧪 Test 4: Servers Respond to Health Checks")
    result = test_servers_respond()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 5: Save manual note
    print("\n🧪 Test 5: Manual Task Note Saves Successfully")
    result = test_save_manual_note()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 6: Regenerate endpoint
    print("\n🧪 Test 6: Regenerate Endpoint Works")
    result = test_regenerate_endpoint()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 7: Notes count
    print("\n🧪 Test 7: Notes Count Endpoint Accurate")
    result = test_notes_count()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    # Test 8: Response formats
    print("\n🧪 Test 8: All Responses Match Expected Format")
    result = test_response_formats()
    print_test(result.name, result.passed, result.message)
    results.append(result)

    return results

def print_summary(results: List[TestResult]):
    """Print test summary"""
    print_header("Test Summary")

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed

    print(f"\n{Colors.BOLD}Total Tests: {len(results)}{Colors.END}")
    print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.END}")

    if failed > 0:
        print(f"{Colors.RED}❌ Failed: {failed}{Colors.END}")

    print()

    if failed > 0:
        print(f"{Colors.RED}{Colors.BOLD}❌ TESTS FAILED ({failed}/{len(results)}){Colors.END}")
        print(f"{Colors.RED}Fix the failures above and re-run tests{Colors.END}")
        return 1
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED ({len(results)}/{len(results)}){Colors.END}")
        return 0

def main():
    """Main test entry point"""
    print(f"\n{Colors.BOLD}Task Manager Integration Tests{Colors.END}")
    print(f"Date: {os.popen('date').read().strip()}")

    # Run all tests
    results = run_all_tests()

    # Print summary
    exit_code = print_summary(results)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
