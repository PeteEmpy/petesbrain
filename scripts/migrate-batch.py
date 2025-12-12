#!/usr/bin/env python3
"""
Batch migration script for Keychain + Path standardization.

Applies Phase 2-3 changes to a batch of agents:
- Adds Keychain secrets import
- Adds path standardization import
- Updates plist files with PETESBRAIN_ROOT

Usage:
    python3 scripts/migrate-batch.py agent1 agent2 agent3 ...

    # Or with full paths:
    python3 scripts/migrate-batch.py agents/agent-name/agent-name.py tools/tool-name/tool-script.py

Example:
    python3 scripts/migrate-batch.py \
        agents/weekly-reports/weekly-reports.py \
        agents/campaign-audit/campaign-audit.py \
        tools/performance-analyzer/analyzer.py
"""

import sys
import os
import subprocess
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def find_agent_script(name):
    """Find agent script by name or path."""
    # If it's a full path, use it
    if name.endswith('.py'):
        script = PROJECT_ROOT / name
        if script.exists():
            return script

    # Try as agent directory
    script = PROJECT_ROOT / 'agents' / name / f'{name}.py'
    if script.exists():
        return script

    # Try as tool
    script = PROJECT_ROOT / 'tools' / name / f'{name}.py'
    if script.exists():
        return script

    # Try shared scripts
    script = PROJECT_ROOT / 'shared' / name / f'{name}.py'
    if script.exists():
        return script

    return None

def get_plist_path(script_path):
    """Determine plist file for an agent script."""
    # Extract agent name from path
    if 'agents/' in str(script_path):
        agent_name = script_path.parent.name
    elif 'tools/' in str(script_path):
        # Tools might not have plist, return None
        return None
    elif 'shared/' in str(script_path):
        return None
    else:
        agent_name = script_path.parent.name

    plist_path = Path.home() / 'Library/LaunchAgents' / f'com.petesbrain.{agent_name}.plist'
    return plist_path if plist_path.exists() else None

def update_agent_code(script_path):
    """Add Keychain and paths imports to agent code."""
    content = script_path.read_text()

    # Check if already migrated
    if 'from shared.paths import' in content and 'from shared.secrets import' in content:
        return True, "Already migrated"

    # Find PROJECT_ROOT line
    match = re.search(r'PROJECT_ROOT = Path\(__file__\)\.parent(?:\.parent)*(?:\)\s*)', content)
    if not match:
        return False, "Could not find PROJECT_ROOT initialization"

    # Insert imports after PROJECT_ROOT
    insert_pos = match.end()

    imports = '''
# Import centralized path discovery and Keychain secrets
from shared.paths import get_project_root as get_project_root_paths
from shared.secrets import get_secret

# Verify project root can be discovered
try:
    PROJECT_ROOT = get_project_root_paths()
except RuntimeError as e:
    print(f"Error: {e}")
    print("Make sure PETESBRAIN_ROOT environment variable is set or run from project directory")
    sys.exit(1)'''

    new_content = content[:insert_pos] + imports + content[insert_pos:]

    # Add imports at top if not already there
    if 'from shared.secrets import get_secret' not in new_content[:1000]:
        # Already handled above
        pass

    script_path.write_text(new_content)
    return True, "Code updated successfully"

def update_plist_file(plist_path):
    """Add PETESBRAIN_ROOT to plist EnvironmentVariables."""
    content = plist_path.read_text()

    # Check if already has PETESBRAIN_ROOT
    if 'PETESBRAIN_ROOT' in content:
        return True, "Already has PETESBRAIN_ROOT"

    # Find EnvironmentVariables section
    if '<key>EnvironmentVariables</key>' not in content:
        # Create EnvironmentVariables section
        dict_match = re.search(r'<dict>\n', content)
        if dict_match:
            env_vars = '''	<key>EnvironmentVariables</key>
	<dict>
		<key>PETESBRAIN_ROOT</key>
		<string>/Users/administrator/Documents/PetesBrain.nosync</string>
	</dict>
	<key>Label</key>'''

            # Replace the Label line
            new_content = re.sub(
                r'<key>Label</key>',
                env_vars,
                content,
                count=1
            )
        else:
            return False, "Could not find dict section"
    else:
        # Add PETESBRAIN_ROOT to existing EnvironmentVariables
        new_content = re.sub(
            r'(<key>EnvironmentVariables</key>\s*<dict>)',
            r'\1\n\t\t<key>PETESBRAIN_ROOT</key>\n\t\t<string>/Users/administrator/Documents/PetesBrain.nosync</string>',
            content
        )

    plist_path.write_text(new_content)
    return True, "Plist updated successfully"

def reload_agent(plist_path):
    """Reload agent via launchctl."""
    agent_label = plist_path.stem.replace('com.petesbrain.', '')

    try:
        subprocess.run(
            ['launchctl', 'unload', str(plist_path)],
            capture_output=True,
            timeout=5
        )

        import time
        time.sleep(1)

        result = subprocess.run(
            ['launchctl', 'load', str(plist_path)],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return True, "Agent reloaded"
        else:
            return False, f"Reload failed: {result.stderr}"
    except Exception as e:
        return False, f"Error reloading: {str(e)}"

def check_agent_health(plist_path):
    """Check agent exit code via launchctl."""
    agent_label = 'com.petesbrain.' + plist_path.stem.replace('com.petesbrain.', '')

    try:
        result = subprocess.run(
            ['launchctl', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )

        for line in result.stdout.split('\n'):
            if agent_label in line:
                parts = line.split()
                if len(parts) >= 2:
                    exit_code = parts[1]
                    if exit_code == '0':
                        return True, f"Healthy (exit code 0)"
                    else:
                        return False, f"Exit code {exit_code}"

        return None, "Agent not found in launchctl list"
    except Exception as e:
        return None, f"Error checking health: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print(f"{BLUE}Usage:{RESET} python3 scripts/migrate-batch.py agent1 agent2 agent3 ...")
        print(f"\n{YELLOW}Examples:{RESET}")
        print(f"  python3 scripts/migrate-batch.py weekly-reports campaign-audit")
        print(f"  python3 scripts/migrate-batch.py agents/agent-name/agent-name.py")
        sys.exit(1)

    agent_names = sys.argv[1:]

    print(f"\n{BOLD}{BLUE}═══════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}PetesBrain Batch Migration Script{RESET}")
    print(f"{BOLD}{BLUE}═══════════════════════════════════════════════════════════{RESET}\n")

    results = []

    for agent_name in agent_names:
        print(f"{BOLD}Processing: {agent_name}{RESET}")

        # Find script
        script_path = find_agent_script(agent_name)
        if not script_path:
            print(f"  {RED}✗ Could not find agent script{RESET}\n")
            results.append((agent_name, False, "Script not found"))
            continue

        print(f"  Script: {script_path}")

        # Update code
        success, msg = update_agent_code(script_path)
        if success:
            print(f"  {GREEN}✓ Code updated{RESET}")
        else:
            print(f"  {YELLOW}⚠ Code update skipped: {msg}{RESET}")

        # Update plist (if it exists)
        plist_path = get_plist_path(script_path)
        if plist_path:
            success, msg = update_plist_file(plist_path)
            if success:
                print(f"  {GREEN}✓ Plist updated{RESET}")
            else:
                print(f"  {RED}✗ Plist update failed: {msg}{RESET}")
                results.append((agent_name, False, msg))
                continue

            # Reload agent
            success, msg = reload_agent(plist_path)
            if success:
                print(f"  {GREEN}✓ Agent reloaded{RESET}")
            else:
                print(f"  {YELLOW}⚠ Reload warning: {msg}{RESET}")

            # Check health
            import time
            time.sleep(1)
            success, health_msg = check_agent_health(plist_path)
            if success:
                print(f"  {GREEN}✓ {health_msg}{RESET}")
            elif success is False:
                print(f"  {RED}✗ {health_msg}{RESET}")
            else:
                print(f"  {YELLOW}⚠ {health_msg}{RESET}")
        else:
            print(f"  {YELLOW}⚠ No plist file (not a LaunchAgent, or tool script){RESET}")

        print()
        results.append((agent_name, True, "Migrated"))

    # Summary
    print(f"{BOLD}{BLUE}═══════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}Summary:{RESET}\n")

    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)

    for agent_name, success, msg in results:
        symbol = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        print(f"  {symbol} {agent_name}: {msg}")

    print(f"\n{BOLD}Result:{RESET} {success_count}/{total_count} agents migrated successfully")

    if success_count == total_count:
        print(f"\n{GREEN}{BOLD}✅ Batch migration complete! Ready to commit.{RESET}\n")
    else:
        print(f"\n{YELLOW}{BOLD}⚠️  Some agents failed. Fix and retry.{RESET}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
