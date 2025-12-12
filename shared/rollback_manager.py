"""
Rollback Manager for PetesBrain

Manages system snapshots and restoration for safe incremental migrations.
Allows restoration of agent configurations, MCP settings, and system state
without requiring manual git commands or complex recovery procedures.

Architecture:
- Snapshots stored in: infrastructure/rollback-snapshots/{timestamp}/
- Each snapshot captures: plist files, .mcp.json, shared modules, git state
- Venvs NOT captured directly (too large), but metadata preserved for verification
- All operations are read-only until restore is explicitly called

Safe by design:
- Never deletes anything
- Always creates backups before changes
- Dry-run mode shows what would change
- Full logging and verification
"""

import json
import os
import shutil
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class RollbackSnapshot:
    """Represents a point-in-time system snapshot."""

    def __init__(self, snapshot_dir: Path):
        self.snapshot_dir = Path(snapshot_dir)
        self.manifest_file = self.snapshot_dir / "manifest.json"
        self.plist_dir = self.snapshot_dir / "plist"
        self.config_dir = self.snapshot_dir / "config"
        self.credentials_dir = self.snapshot_dir / "credentials"
        self.venv_state_file = self.snapshot_dir / "venv-state.json"

    def load_manifest(self) -> Dict:
        """Load snapshot manifest."""
        if not self.manifest_file.exists():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_file}")
        with open(self.manifest_file) as f:
            return json.load(f)

    def get_timestamp(self) -> str:
        """Extract timestamp from snapshot directory name."""
        return self.snapshot_dir.name

    def get_created_at(self) -> datetime:
        """Get snapshot creation time."""
        manifest = self.load_manifest()
        return datetime.fromisoformat(manifest['created_at'])

    def get_description(self) -> str:
        """Get snapshot description."""
        manifest = self.load_manifest()
        return manifest.get('description', 'No description')

    def get_category(self) -> str:
        """Get snapshot category (e.g., 'pre-phase-4', 'pre-venv-fix')."""
        manifest = self.load_manifest()
        return manifest.get('category', 'manual')

    def get_plist_files(self) -> List[str]:
        """Get list of plist files in snapshot."""
        manifest = self.load_manifest()
        return manifest.get('plist_files', [])

    def get_config_files(self) -> List[str]:
        """Get list of config files in snapshot."""
        manifest = self.load_manifest()
        return manifest.get('config_files', [])

    def get_credential_files(self) -> List[str]:
        """Get list of credential files in snapshot."""
        manifest = self.load_manifest()
        return manifest.get('credential_files', [])

    def get_git_state(self) -> Dict:
        """Get git state at snapshot time."""
        manifest = self.load_manifest()
        return manifest.get('git_state', {})


class RollbackManager:
    """Manages system snapshots and restoration."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize rollback manager.

        Args:
            project_root: Path to PetesBrain root. If None, will auto-detect.
        """
        if project_root is None:
            # Try to auto-detect from env var
            if 'PETESBRAIN_ROOT' in os.environ:
                project_root = Path(os.environ['PETESBRAIN_ROOT'])
            else:
                # Fallback: assume this file is in shared/ directory
                project_root = Path(__file__).parent.parent

        self.project_root = Path(project_root)
        self.snapshots_dir = self.project_root / "infrastructure" / "rollback-snapshots"
        self.plist_dir = Path.home() / "Library" / "LaunchAgents"
        self.mcp_json = self.project_root / ".mcp.json"

        # Create snapshots directory if it doesn't exist
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def _discover_credentials(self) -> Dict[str, Path]:
        """Discover all credential files in the system.

        Returns:
            Dict mapping credential name to file path
        """
        credentials = {}

        # MCP server credentials
        mcp_servers_dir = self.project_root / "infrastructure" / "mcp-servers"
        if mcp_servers_dir.exists():
            # Standard credentials.json files
            for server_dir in mcp_servers_dir.iterdir():
                if server_dir.is_dir():
                    cred_file = server_dir / "credentials.json"
                    if cred_file.exists():
                        credentials[f"mcp/{server_dir.name}/credentials.json"] = cred_file

                    # Also check for gcp-oauth.keys.json
                    oauth_file = server_dir / "gcp-oauth.keys.json"
                    if oauth_file.exists():
                        credentials[f"mcp/{server_dir.name}/gcp-oauth.keys.json"] = oauth_file

        # Google Ads configuration
        google_ads_config = Path.home() / ".google-ads" / "google-ads.yaml"
        if google_ads_config.exists():
            credentials["~/.google-ads/google-ads.yaml"] = google_ads_config

        # Google Analytics OAuth (referenced in .mcp.json env)
        if self.mcp_json.exists():
            try:
                with open(self.mcp_json) as f:
                    mcp_config = json.load(f)
                    # Check for GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH
                    for server_name, server_config in mcp_config.get('mcpServers', {}).items():
                        env = server_config.get('env', {})
                        for env_var, env_path in env.items():
                            if 'OAUTH' in env_var and env_path:
                                if isinstance(env_path, str) and env_path.startswith('/'):
                                    oauth_path = Path(env_path)
                                    if oauth_path.exists():
                                        credentials[f"oauth/{oauth_path.name}"] = oauth_path
            except Exception as e:
                print(f"⚠️  Failed to check .mcp.json for OAuth paths: {e}")

        # Google Drive MCP OAuth (in ~/.config/)
        google_drive_oauth = Path.home() / ".config" / "google-drive-mcp" / "credentials.json"
        if google_drive_oauth.exists():
            credentials["~/.config/google-drive-mcp/credentials.json"] = google_drive_oauth

        return credentials

    def _backup_credentials(self, credentials: Dict[str, Path], backup_dir: Path) -> List[Dict]:
        """Back up all discovered credentials.

        Args:
            credentials: Dict of credential name to file path
            backup_dir: Directory to store credential backups

        Returns:
            List of dicts with backup info
        """
        backup_dir.mkdir(parents=True, exist_ok=True)
        backed_up = []

        for cred_name, cred_path in credentials.items():
            if not cred_path.exists():
                continue

            try:
                # Create subdirectory structure for organization
                relative_path = cred_name.replace('/', '_').replace('~', 'home')
                backup_path = backup_dir / relative_path

                # Ensure parent directory exists
                backup_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy the credential file
                shutil.copy2(cred_path, backup_path)

                backed_up.append({
                    "name": cred_name,
                    "original": str(cred_path),
                    "backup": str(backup_path),
                    "hash": self._file_hash(cred_path),
                    "size_bytes": cred_path.stat().st_size
                })
            except Exception as e:
                print(f"⚠️  Failed to backup credential {cred_name}: {e}")

        return backed_up

    def create_snapshot(self, description: str, category: str = "manual") -> str:
        """Create a snapshot of current system state.

        Args:
            description: Human-readable description (e.g., "Before Phase 4 migration")
            category: Category label (e.g., "pre-phase-4", "pre-venv-fix")

        Returns:
            Snapshot timestamp/ID

        Note: This is a READ-ONLY operation. No changes are made to the system.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_dir = self.snapshots_dir / timestamp
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        plist_backup_dir = snapshot_dir / "plist"
        config_backup_dir = snapshot_dir / "config"
        credentials_backup_dir = snapshot_dir / "credentials"
        plist_backup_dir.mkdir(exist_ok=True)
        config_backup_dir.mkdir(exist_ok=True)
        credentials_backup_dir.mkdir(exist_ok=True)

        manifest = {
            "created_at": datetime.now().isoformat(),
            "description": description,
            "category": category,
            "plist_files": [],
            "config_files": [],
            "credential_files": [],
            "git_state": self._get_git_state(),
            "venv_metadata": self._get_venv_metadata(),
        }

        # Backup all petesbrain plist files
        plist_files = list(self.plist_dir.glob("*petesbrain*.plist"))
        for plist in plist_files:
            try:
                backup_path = plist_backup_dir / plist.name
                shutil.copy2(plist, backup_path)
                manifest["plist_files"].append({
                    "original": str(plist),
                    "backup": str(backup_path),
                    "hash": self._file_hash(plist)
                })
            except Exception as e:
                print(f"⚠️  Failed to backup plist {plist.name}: {e}")

        # Backup .mcp.json if it exists
        if self.mcp_json.exists():
            try:
                backup_path = config_backup_dir / "mcp.json"
                shutil.copy2(self.mcp_json, backup_path)
                manifest["config_files"].append({
                    "original": str(self.mcp_json),
                    "backup": str(backup_path),
                    "hash": self._file_hash(self.mcp_json)
                })
            except Exception as e:
                print(f"⚠️  Failed to backup .mcp.json: {e}")

        # Backup critical shared modules
        for module in ["secrets.py", "paths.py"]:
            module_path = self.project_root / "shared" / module
            if module_path.exists():
                try:
                    backup_path = config_backup_dir / module
                    shutil.copy2(module_path, backup_path)
                    manifest["config_files"].append({
                        "original": str(module_path),
                        "backup": str(backup_path),
                        "hash": self._file_hash(module_path)
                    })
                except Exception as e:
                    print(f"⚠️  Failed to backup {module}: {e}")

        # Backup all credentials
        print("\n🔐 Backing up credentials...")
        discovered_credentials = self._discover_credentials()
        if discovered_credentials:
            backed_up_credentials = self._backup_credentials(
                discovered_credentials, credentials_backup_dir
            )
            manifest["credential_files"] = backed_up_credentials
            print(f"   ✅ Backed up {len(backed_up_credentials)} credential files")
        else:
            print(f"   ⚠️  No credentials found to backup")

        # Write manifest
        manifest_file = snapshot_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Create a Credential Manifest for transparency
        if manifest["credential_files"]:
            cred_manifest = snapshot_dir / "CREDENTIAL-MANIFEST.md"
            with open(cred_manifest, 'w') as f:
                f.write("# Credential Files Backed Up\n\n")
                f.write(f"Snapshot: {timestamp}\n")
                f.write(f"Created: {datetime.now().isoformat()}\n\n")
                f.write("## Backed Up Credentials\n\n")
                for cred in manifest["credential_files"]:
                    f.write(f"- **{cred['name']}**\n")
                    f.write(f"  - Original: `{cred['original']}`\n")
                    f.write(f"  - Size: {cred['size_bytes']} bytes\n")
                    f.write(f"  - Hash: `{cred['hash'][:16]}...`\n\n")

        print(f"\n✅ Snapshot created: {timestamp}")
        print(f"   Description: {description}")
        print(f"   Category: {category}")
        print(f"   Location: {snapshot_dir}")
        print(f"   Files backed up: {len(manifest['plist_files']) + len(manifest['config_files']) + len(manifest['credential_files'])}")

        return timestamp

    def list_snapshots(self) -> List[RollbackSnapshot]:
        """List all available snapshots, most recent first."""
        snapshots = []
        for snapshot_dir in sorted(self.snapshots_dir.iterdir(), reverse=True):
            if snapshot_dir.is_dir() and (snapshot_dir / "manifest.json").exists():
                snapshots.append(RollbackSnapshot(snapshot_dir))
        return snapshots

    def get_latest_snapshot(self) -> Optional[RollbackSnapshot]:
        """Get most recent snapshot."""
        snapshots = self.list_snapshots()
        return snapshots[0] if snapshots else None

    def show_snapshots(self, limit: int = 10):
        """Display available snapshots in human-readable format."""
        snapshots = self.list_snapshots()[:limit]

        if not snapshots:
            print("❌ No snapshots found")
            return

        print(f"\n📦 Available Snapshots (showing {len(snapshots)}):\n")
        for i, snapshot in enumerate(snapshots, 1):
            manifest = snapshot.load_manifest()
            created = snapshot.get_created_at()
            age = datetime.now() - created

            # Format age in human-readable way
            if age.total_seconds() < 60:
                age_str = f"{int(age.total_seconds())}s ago"
            elif age.total_seconds() < 3600:
                age_str = f"{int(age.total_seconds() / 60)}m ago"
            elif age.total_seconds() < 86400:
                age_str = f"{int(age.total_seconds() / 3600)}h ago"
            else:
                age_str = f"{int(age.total_seconds() / 86400)}d ago"

            print(f"{i}. [{snapshot.get_timestamp()}]")
            print(f"   Description: {snapshot.get_description()}")
            print(f"   Category: {snapshot.get_category()}")
            print(f"   Created: {age_str}")
            cred_count = len(manifest.get('credential_files', []))
            if cred_count > 0:
                print(f"   Files: {len(manifest['plist_files'])} plist, {len(manifest['config_files'])} config, 🔐 {cred_count} credentials")
            else:
                print(f"   Files: {len(manifest['plist_files'])} plist, {len(manifest['config_files'])} config")
            print()

    def restore_snapshot(self, snapshot_id: str, dry_run: bool = True) -> Tuple[bool, str]:
        """Restore system from a snapshot.

        Args:
            snapshot_id: Snapshot timestamp to restore
            dry_run: If True, show what would change but don't restore

        Returns:
            Tuple of (success: bool, message: str)

        Note: Always creates a backup before restoring, so no data is lost.
        """
        snapshot_dir = self.snapshots_dir / snapshot_id
        if not snapshot_dir.exists():
            return False, f"Snapshot not found: {snapshot_id}"

        snapshot = RollbackSnapshot(snapshot_dir)
        manifest = snapshot.load_manifest()

        if dry_run:
            return self._dry_run_restore(snapshot, manifest)
        else:
            return self._execute_restore(snapshot, manifest)

    def _dry_run_restore(self, snapshot: RollbackSnapshot, manifest: Dict) -> Tuple[bool, str]:
        """Show what would be restored without making changes."""
        changes = []

        # Check plist files that would be restored
        for plist_info in manifest.get('plist_files', []):
            original = Path(plist_info['original'])
            backup = Path(plist_info['backup'])

            if not backup.exists():
                changes.append(f"⚠️  Missing backup: {plist_info['original']}")
                continue

            if not original.exists():
                changes.append(f"✓ Would restore (new): {original.name}")
            else:
                current_hash = self._file_hash(original)
                original_hash = plist_info['hash']
                if current_hash != original_hash:
                    changes.append(f"✓ Would restore (modified): {original.name}")
                else:
                    changes.append(f"- Unchanged: {original.name}")

        # Check config files that would be restored
        for config_info in manifest.get('config_files', []):
            original = Path(config_info['original'])
            backup = Path(config_info['backup'])

            if not backup.exists():
                changes.append(f"⚠️  Missing backup: {config_info['original']}")
                continue

            if not original.exists():
                changes.append(f"✓ Would restore (new): {original.name}")
            else:
                current_hash = self._file_hash(original)
                original_hash = config_info['hash']
                if current_hash != original_hash:
                    changes.append(f"✓ Would restore (modified): {original.name}")
                else:
                    changes.append(f"- Unchanged: {original.name}")

        # Check credential files that would be restored
        if manifest.get('credential_files'):
            changes.append("")
            changes.append("🔐 CREDENTIALS:")
            for cred_info in manifest.get('credential_files', []):
                original = Path(cred_info['original'])
                backup = Path(cred_info['backup'])

                if not backup.exists():
                    changes.append(f"⚠️  Missing backup: {cred_info['original']}")
                    continue

                if not original.exists():
                    changes.append(f"✓ Would restore (new): {cred_info['name']}")
                else:
                    current_hash = self._file_hash(original)
                    original_hash = cred_info['hash']
                    if current_hash != original_hash:
                        changes.append(f"✓ Would restore (modified): {cred_info['name']}")
                    else:
                        changes.append(f"- Unchanged: {cred_info['name']}")

        message = f"DRY RUN: Snapshot {snapshot.get_timestamp()}\n"
        message += f"Description: {snapshot.get_description()}\n"
        message += f"Changes:\n" + "\n".join(changes)

        return True, message

    def _execute_restore(self, snapshot: RollbackSnapshot, manifest: Dict) -> Tuple[bool, str]:
        """Actually restore from snapshot."""
        # First, create a backup of current state
        current_snapshot = self.create_snapshot(
            f"Auto-backup before restoring {snapshot.get_timestamp()}",
            "auto-backup"
        )

        restored_count = 0
        failed_count = 0

        # Restore plist files
        for plist_info in manifest.get('plist_files', []):
            original = Path(plist_info['original'])
            backup = Path(plist_info['backup'])

            if not backup.exists():
                print(f"⚠️  Missing backup: {plist_info['original']}")
                failed_count += 1
                continue

            try:
                shutil.copy2(backup, original)
                restored_count += 1
                print(f"✓ Restored: {original.name}")
            except Exception as e:
                print(f"❌ Failed to restore {original.name}: {e}")
                failed_count += 1

        # Restore config files
        for config_info in manifest.get('config_files', []):
            original = Path(config_info['original'])
            backup = Path(config_info['backup'])

            if not backup.exists():
                print(f"⚠️  Missing backup: {config_info['original']}")
                failed_count += 1
                continue

            try:
                shutil.copy2(backup, original)
                restored_count += 1
                print(f"✓ Restored: {original.name}")
            except Exception as e:
                print(f"❌ Failed to restore {original.name}: {e}")
                failed_count += 1

        # Restore credential files
        if manifest.get('credential_files'):
            print("\n🔐 Restoring credentials...")
            for cred_info in manifest.get('credential_files', []):
                original = Path(cred_info['original'])
                backup = Path(cred_info['backup'])

                if not backup.exists():
                    print(f"⚠️  Missing backup: {cred_info['original']}")
                    failed_count += 1
                    continue

                try:
                    # Ensure parent directory exists for credential file
                    original.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup, original)
                    restored_count += 1
                    print(f"✓ Restored credential: {cred_info['name']}")
                except Exception as e:
                    print(f"❌ Failed to restore credential {cred_info['name']}: {e}")
                    failed_count += 1

        message = f"Restored {restored_count} files"
        if failed_count > 0:
            message += f", {failed_count} failed"
        message += f"\nAuto-backup created: {current_snapshot}"

        success = failed_count == 0
        return success, message

    def _file_hash(self, filepath: Path, algorithm: str = "sha256") -> str:
        """Calculate file hash for integrity checking."""
        hasher = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _get_git_state(self) -> Dict:
        """Capture current git state."""
        try:
            # Get current commit
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                text=True
            ).strip()

            # Get current branch
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_root,
                text=True
            ).strip()

            return {
                "commit": commit,
                "branch": branch,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_venv_metadata(self) -> Dict:
        """Capture venv metadata (for reference, venvs aren't backed up)."""
        metadata = {}

        # Check shared venv
        shared_venv = self.project_root / "venv-google"
        if shared_venv.exists():
            metadata["venv-google"] = {
                "exists": True,
                "python_version": self._get_venv_python_version(shared_venv)
            }

        # Check MCP server venvs
        mcp_servers_dir = self.project_root / "infrastructure" / "mcp-servers"
        if mcp_servers_dir.exists():
            for server_dir in mcp_servers_dir.iterdir():
                if server_dir.is_dir():
                    venv = server_dir / ".venv"
                    if venv.exists():
                        metadata[f"mcp/{server_dir.name}"] = {
                            "exists": True,
                            "python_version": self._get_venv_python_version(venv)
                        }

        return metadata

    def _get_venv_python_version(self, venv_dir: Path) -> Optional[str]:
        """Get Python version from venv."""
        try:
            python_exe = venv_dir / "bin" / "python"
            if python_exe.exists():
                version = subprocess.check_output(
                    [str(python_exe), "--version"],
                    text=True
                ).strip()
                return version
        except Exception:
            pass
        return None


def main():
    """Command-line interface for rollback manager."""
    import sys

    manager = RollbackManager()

    if len(sys.argv) < 2:
        print("Usage: python rollback_manager.py <command> [args]")
        print("\nCommands:")
        print("  create <description> [category]  - Create a snapshot")
        print("  list                            - List available snapshots")
        print("  restore <snapshot_id> [--force] - Restore from snapshot (dry-run by default)")
        print("  latest                          - Show latest snapshot")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("❌ Usage: create <description> [category]")
            return
        description = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "manual"
        manager.create_snapshot(description, category)

    elif command == "list":
        manager.show_snapshots()

    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Usage: restore <snapshot_id> [--force]")
            return
        snapshot_id = sys.argv[2]
        force = "--force" in sys.argv

        if not force:
            success, message = manager.restore_snapshot(snapshot_id, dry_run=True)
            print(message)
            print("\n⚠️  This is a dry run. Use --force to actually restore:")
            print(f"   python rollback_manager.py restore {snapshot_id} --force")
        else:
            success, message = manager.restore_snapshot(snapshot_id, dry_run=False)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")

    elif command == "latest":
        snapshot = manager.get_latest_snapshot()
        if snapshot:
            manifest = snapshot.load_manifest()
            print(f"Latest snapshot: {snapshot.get_timestamp()}")
            print(f"Description: {snapshot.get_description()}")
            print(f"Category: {snapshot.get_category()}")
            print(f"Created: {snapshot.get_created_at()}")
            print(f"Files: {len(manifest['plist_files'])} plist, {len(manifest['config_files'])} config")
        else:
            print("❌ No snapshots found")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
