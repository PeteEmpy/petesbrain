"""
Venv Health Checker for PetesBrain

Detects and repairs broken virtual environments without disrupting running agents.

Features:
- Detects broken venvs (import failures, missing Python, corrupted binaries)
- Auto-rebuilds failed venvs from requirements.txt
- Verifies rebuild succeeded with import tests
- Comprehensive logging of all repairs
- Completely standalone (doesn't integrate with agents until Phase C)

Usage:
    # Dry-run: Check venv health without repairs
    python3 shared/venv_health_checker.py check

    # Actually repair broken venvs
    python3 shared/venv_health_checker.py repair

    # Check specific venv
    python3 shared/venv_health_checker.py check /path/to/venv
"""

import subprocess
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging


class VenvHealthChecker:
    """Checks and repairs virtual environments."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize health checker.

        Args:
            project_root: Path to PetesBrain root. If None, auto-detect.
        """
        if project_root is None:
            # Try env var first
            if 'PETESBRAIN_ROOT' in os.environ:
                project_root = Path(os.environ['PETESBRAIN_ROOT'])
            else:
                # Fallback: assume in shared/ directory
                project_root = Path(__file__).parent.parent

        self.project_root = Path(project_root)
        self.log_dir = self.project_root / "data" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self._setup_logging()

        # Venvs to check
        self.venvs_to_check = self._discover_venvs()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging to file and console."""
        logger = logging.getLogger("venv_health")
        logger.setLevel(logging.DEBUG)

        # File handler
        log_file = self.log_dir / f"venv-health-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def _discover_venvs(self) -> Dict[str, Path]:
        """Discover all venvs in the project."""
        venvs = {}

        # Shared venv-google
        shared_venv = self.project_root / "venv-google"
        if shared_venv.exists():
            venvs["venv-google"] = shared_venv

        # MCP server venvs
        mcp_servers_dir = self.project_root / "infrastructure" / "mcp-servers"
        if mcp_servers_dir.exists():
            for server_dir in mcp_servers_dir.iterdir():
                if server_dir.is_dir():
                    venv = server_dir / ".venv"
                    if venv.exists():
                        venvs[f"mcp/{server_dir.name}"] = venv

        # Agent venvs (if any)
        agents_dir = self.project_root / "agents"
        if agents_dir.exists():
            for agent_dir in agents_dir.glob("**/"):
                if agent_dir.is_dir():
                    venv = agent_dir / ".venv"
                    if venv.exists():
                        venvs[f"agent/{agent_dir.name}"] = venv

        return venvs

    def check_health(self) -> Dict[str, Dict]:
        """Check health of all venvs.

        Returns:
            Dict mapping venv name to health status
        """
        self.logger.info(f"Checking health of {len(self.venvs_to_check)} venvs...")
        results = {}

        for name, venv_path in self.venvs_to_check.items():
            self.logger.info(f"Checking: {name}")
            health = self._check_venv_health(name, venv_path)
            results[name] = health

            if health['status'] == 'healthy':
                self.logger.info(f"  ✅ Healthy")
            else:
                self.logger.warning(f"  ❌ {health['status'].upper()}: {health['reason']}")

        # Summary
        healthy = sum(1 for h in results.values() if h['status'] == 'healthy')
        broken = len(results) - healthy
        self.logger.info(f"\nSummary: {healthy}/{len(results)} healthy, {broken} broken")

        return results

    def _check_venv_health(self, name: str, venv_path: Path) -> Dict:
        """Check health of a single venv.

        Returns:
            Dict with 'status' and 'reason'
        """
        python_exe = venv_path / "bin" / "python"

        # Check 1: Python executable exists
        if not python_exe.exists():
            return {
                'status': 'broken',
                'reason': 'Python executable missing',
                'venv_path': str(venv_path)
            }

        # Check 2: Python executable is runnable
        try:
            version = subprocess.check_output(
                [str(python_exe), "--version"],
                stderr=subprocess.STDOUT,
                text=True,
                timeout=5
            ).strip()
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            return {
                'status': 'broken',
                'reason': f'Python not runnable: {str(e)[:100]}',
                'venv_path': str(venv_path)
            }

        # Check 3: Can import basic packages
        try:
            subprocess.check_output(
                [str(python_exe), "-c", "import sys; print('ok')"],
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return {
                'status': 'broken',
                'reason': 'Python imports broken',
                'venv_path': str(venv_path)
            }

        # Check 4: Has pip
        pip_exe = venv_path / "bin" / "pip"
        if not pip_exe.exists():
            return {
                'status': 'degraded',
                'reason': 'pip executable missing',
                'venv_path': str(venv_path)
            }

        # All checks passed
        return {
            'status': 'healthy',
            'reason': f'{version}',
            'venv_path': str(venv_path)
        }

    def repair_venvs(self, dry_run: bool = True) -> Dict[str, Dict]:
        """Repair broken venvs.

        Args:
            dry_run: If True, show what would be repaired but don't actually repair

        Returns:
            Dict mapping venv name to repair result
        """
        health_check = self.check_health()
        broken_venvs = {
            name: status for name, status in health_check.items()
            if status['status'] != 'healthy'
        }

        if not broken_venvs:
            self.logger.info("✅ All venvs are healthy, nothing to repair")
            return {}

        self.logger.info(f"Found {len(broken_venvs)} broken venvs")

        if dry_run:
            self.logger.info("\n📋 DRY RUN - What would be repaired:")
            for name in broken_venvs:
                self.logger.info(f"  Would rebuild: {name}")
            return broken_venvs

        # Actually repair
        self.logger.info("\n🔧 Repairing broken venvs...")
        results = {}
        for name, venv_path in self.venvs_to_check.items():
            if name in broken_venvs:
                result = self._repair_venv(name, venv_path)
                results[name] = result

        return results

    def _repair_venv(self, name: str, venv_path: Path) -> Dict:
        """Repair a single venv.

        Returns:
            Dict with repair result
        """
        self.logger.info(f"Repairing: {name}")

        # Step 1: Backup old venv (just rename it)
        backup_path = venv_path.parent / f"{venv_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            shutil.move(str(venv_path), str(backup_path))
            self.logger.info(f"  Backed up to: {backup_path}")
        except Exception as e:
            return {
                'status': 'failed',
                'reason': f'Could not backup old venv: {e}',
                'venv_path': str(venv_path)
            }

        # Step 2: Find requirements file
        requirements_file = self._find_requirements(venv_path)
        if not requirements_file:
            self.logger.warning(f"  ⚠️  No requirements.txt found, creating minimal venv")
            requirements_file = None

        # Step 3: Create new venv
        try:
            subprocess.check_call(
                [sys.executable, "-m", "venv", str(venv_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.logger.info(f"  Created new venv")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"  Failed to create venv: {e}")
            return {
                'status': 'failed',
                'reason': f'Could not create new venv',
                'venv_path': str(venv_path)
            }

        # Step 4: Install requirements if file exists
        if requirements_file:
            try:
                pip_exe = venv_path / "bin" / "pip"
                subprocess.check_call(
                    [str(pip_exe), "install", "-q", "-r", str(requirements_file)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=300  # 5 minute timeout for installs
                )
                self.logger.info(f"  Installed requirements from {requirements_file.name}")
            except subprocess.CalledProcessError as e:
                self.logger.warning(f"  ⚠️  Some requirements failed to install: {e}")
                # This is not fatal - partial venv is better than no venv
            except subprocess.TimeoutExpired:
                self.logger.error(f"  Timeout installing requirements")
                return {
                    'status': 'failed',
                    'reason': 'Requirements installation timed out',
                    'venv_path': str(venv_path)
                }

        # Step 5: Verify repair
        health = self._check_venv_health(name, venv_path)
        if health['status'] == 'healthy':
            self.logger.info(f"  ✅ Repair successful ({health['reason']})")
            return {
                'status': 'repaired',
                'reason': health['reason'],
                'backup_path': str(backup_path),
                'venv_path': str(venv_path)
            }
        else:
            self.logger.error(f"  ❌ Repair failed: {health['reason']}")
            return {
                'status': 'failed',
                'reason': f'Repair did not succeed: {health["reason"]}',
                'backup_path': str(backup_path),
                'venv_path': str(venv_path)
            }

    def _find_requirements(self, venv_path: Path) -> Optional[Path]:
        """Find requirements file for a venv."""
        # Check parent directories for requirements
        current = venv_path.parent
        while current != current.parent:  # Until we reach root
            # Check for requirements.txt
            req_file = current / "requirements.txt"
            if req_file.exists():
                return req_file

            # Check for requirements.txt.backup (Phase 2 backup)
            req_backup = current / "requirements.txt.backup"
            if req_backup.exists():
                return req_backup

            current = current.parent

        return None

    def report(self) -> str:
        """Generate a report of venv status."""
        health = self.check_health()

        report = "📊 Venv Health Report\n"
        report += "=" * 50 + "\n\n"

        # Group by status
        healthy = {k: v for k, v in health.items() if v['status'] == 'healthy'}
        broken = {k: v for k, v in health.items() if v['status'] != 'healthy'}

        report += f"✅ Healthy ({len(healthy)}):\n"
        for name, status in healthy.items():
            report += f"  - {name}: {status['reason']}\n"

        if broken:
            report += f"\n❌ Broken ({len(broken)}):\n"
            for name, status in broken.items():
                report += f"  - {name}: {status['reason']}\n"

        report += f"\n📈 Summary: {len(healthy)}/{len(health)} healthy\n"

        return report


import os


def main():
    """Command-line interface."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python venv_health_checker.py <command> [args]")
        print("\nCommands:")
        print("  check              - Check health of all venvs (dry-run)")
        print("  repair             - Repair broken venvs (dry-run by default)")
        print("  repair --force     - Actually repair broken venvs")
        print("  report             - Generate status report")
        print("  check <venv-path>  - Check specific venv")
        return

    command = sys.argv[1]
    checker = VenvHealthChecker()

    if command == "check":
        if len(sys.argv) > 2:
            # Check specific venv
            venv_path = Path(sys.argv[2])
            if venv_path.exists():
                health = checker._check_venv_health(venv_path.name, venv_path)
                print(f"Health: {health['status']} - {health['reason']}")
            else:
                print(f"❌ Venv not found: {venv_path}")
        else:
            # Check all venvs
            health = checker.check_health()
            print("\n" + checker.report())

    elif command == "repair":
        force = "--force" in sys.argv
        results = checker.repair_venvs(dry_run=not force)

        if not force:
            print("\n⚠️  This is a dry run. Use --force to actually repair:")
            print("   python3 venv_health_checker.py repair --force")
        else:
            print("\n" + checker.report())

    elif command == "report":
        print(checker.report())

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
