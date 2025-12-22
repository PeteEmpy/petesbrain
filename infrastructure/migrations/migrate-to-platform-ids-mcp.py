#!/usr/bin/env python3
"""
Platform IDs MCP Migration Script

Migrates all deprecated platform ID calls to the centralized platform-ids MCP server.

Deprecated patterns (29 instances found):
- mcp__google-ads__get_client_platform_ids()
- mcp__google-analytics__get_client_platform_ids()
- mcp__microsoft-ads__get_client_platform_ids()
- mcp__facebook-ads__get_client_platform_ids()

Replacement:
- mcp__platform-ids__get_client_platform_ids()

Safety features:
- Creates backup of all files before modification
- Dry-run mode to preview changes
- Verification report after migration
- Rollback capability if issues detected

Usage:
    # Preview changes (dry-run)
    python migrate-to-platform-ids-mcp.py --dry-run

    # Execute migration
    python migrate-to-platform-ids-mcp.py

    # Execute with backup
    python migrate-to-platform-ids-mcp.py --backup

    # Rollback if needed
    python migrate-to-platform-ids-mcp.py --rollback
"""

import os
import re
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Configuration
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain.nosync")
BACKUP_DIR = PETESBRAIN_ROOT / "infrastructure" / "migrations" / "backups"
LOG_FILE = PETESBRAIN_ROOT / "infrastructure" / "migrations" / "migration-log.json"

# Deprecated patterns to replace
DEPRECATED_PATTERNS = [
    (
        r'mcp__google-ads__get_client_platform_ids\(',
        'mcp__platform-ids__get_client_platform_ids('
    ),
    (
        r'mcp__google-analytics__get_client_platform_ids\(',
        'mcp__platform-ids__get_client_platform_ids('
    ),
    (
        r'mcp__microsoft-ads__get_client_platform_ids\(',
        'mcp__platform-ids__get_client_platform_ids('
    ),
    (
        r'mcp__facebook-ads__get_client_platform_ids\(',
        'mcp__platform-ids__get_client_platform_ids('
    ),
]

# Directories to search
SEARCH_PATHS = [
    PETESBRAIN_ROOT / "clients",
    PETESBRAIN_ROOT / "agents",
    PETESBRAIN_ROOT / "tools",
    PETESBRAIN_ROOT / ".claude" / "skills",
    PETESBRAIN_ROOT / "shared",
]

# File extensions to process
FILE_EXTENSIONS = ['.py', '.md']


class PlatformIDsMigration:
    """Handles migration from deprecated platform ID calls to centralized MCP server."""

    def __init__(self, dry_run: bool = False, create_backup: bool = True):
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.changes: List[Dict] = []
        self.timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    def find_files_to_migrate(self) -> List[Path]:
        """Find all files containing deprecated platform ID calls."""
        files_to_migrate = []

        for search_path in SEARCH_PATHS:
            if not search_path.exists():
                continue

            for ext in FILE_EXTENSIONS:
                pattern = f"**/*{ext}"
                for file_path in search_path.glob(pattern):
                    if self._file_contains_deprecated_calls(file_path):
                        files_to_migrate.append(file_path)

        return files_to_migrate

    def _file_contains_deprecated_calls(self, file_path: Path) -> bool:
        """Check if file contains any deprecated platform ID calls."""
        try:
            content = file_path.read_text()
            for pattern, _ in DEPRECATED_PATTERNS:
                if re.search(pattern, content):
                    return True
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")

        return False

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a file and return details of changes needed."""
        content = file_path.read_text()
        changes_in_file = []

        for old_pattern, new_pattern in DEPRECATED_PATTERNS:
            matches = re.finditer(old_pattern, content)
            for match in matches:
                # Get context (line number)
                line_num = content[:match.start()].count('\n') + 1
                line_content = content.split('\n')[line_num - 1].strip()

                changes_in_file.append({
                    'line': line_num,
                    'old_pattern': old_pattern,
                    'new_pattern': new_pattern,
                    'context': line_content
                })

        return {
            'file': str(file_path),
            'relative_path': str(file_path.relative_to(PETESBRAIN_ROOT)),
            'changes': changes_in_file,
            'change_count': len(changes_in_file)
        }

    def migrate_file(self, file_path: Path) -> bool:
        """Migrate a single file to use centralized platform-ids MCP server."""
        try:
            # Read original content
            content = file_path.read_text()
            original_content = content

            # Apply all replacements
            for old_pattern, new_pattern in DEPRECATED_PATTERNS:
                content = re.sub(old_pattern, new_pattern, content)

            # Check if any changes were made
            if content == original_content:
                return False

            if not self.dry_run:
                # Backup original file
                if self.create_backup:
                    self._backup_file(file_path)

                # Write updated content
                file_path.write_text(content)
                print(f"✅ Migrated: {file_path.relative_to(PETESBRAIN_ROOT)}")
            else:
                print(f"🔍 Would migrate: {file_path.relative_to(PETESBRAIN_ROOT)}")

            return True

        except Exception as e:
            print(f"❌ Error migrating {file_path}: {e}")
            return False

    def _backup_file(self, file_path: Path):
        """Create backup of file before modification."""
        backup_path = BACKUP_DIR / self.timestamp / file_path.relative_to(PETESBRAIN_ROOT)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)

    def run_migration(self) -> Dict:
        """Execute the full migration process."""
        print("\n" + "="*60)
        print("🚀 Platform IDs MCP Migration")
        print("="*60 + "\n")

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files will be modified\n")

        # Find files to migrate
        print("📁 Scanning for files with deprecated platform ID calls...")
        files_to_migrate = self.find_files_to_migrate()

        if not files_to_migrate:
            print("✅ No files found with deprecated calls. Migration not needed!\n")
            return {'status': 'no_changes_needed', 'files_migrated': 0}

        print(f"📋 Found {len(files_to_migrate)} files to migrate:\n")

        # Analyze all files
        analysis_results = []
        total_changes = 0

        for file_path in files_to_migrate:
            analysis = self.analyze_file(file_path)
            analysis_results.append(analysis)
            total_changes += analysis['change_count']

            print(f"  📄 {analysis['relative_path']}")
            print(f"     {analysis['change_count']} deprecated call(s) found")
            for change in analysis['changes'][:3]:  # Show first 3 changes
                print(f"       Line {change['line']}: {change['context'][:60]}...")
            if analysis['change_count'] > 3:
                print(f"       ... and {analysis['change_count'] - 3} more")
            print()

        print(f"\n📊 Summary:")
        print(f"   Files to migrate: {len(files_to_migrate)}")
        print(f"   Total deprecated calls: {total_changes}\n")

        if self.dry_run:
            print("💡 Run without --dry-run to execute migration\n")
            return {
                'status': 'dry_run',
                'files_found': len(files_to_migrate),
                'total_changes': total_changes,
                'analysis': analysis_results
            }

        # Confirm migration
        print("⚠️  This will modify the files listed above.")
        if self.create_backup:
            print(f"✅ Backups will be saved to: {BACKUP_DIR / self.timestamp}")

        response = input("\nProceed with migration? (yes/no): ").lower()
        if response != 'yes':
            print("\n❌ Migration cancelled by user\n")
            return {'status': 'cancelled'}

        # Execute migration
        print("\n🔄 Migrating files...")
        migrated_count = 0

        for file_path in files_to_migrate:
            if self.migrate_file(file_path):
                migrated_count += 1

        # Save migration log
        self._save_migration_log({
            'timestamp': self.timestamp,
            'files_migrated': migrated_count,
            'total_changes': total_changes,
            'analysis': analysis_results
        })

        print(f"\n✅ Migration complete!")
        print(f"   Files migrated: {migrated_count}")
        print(f"   Deprecated calls replaced: {total_changes}")
        if self.create_backup:
            print(f"   Backups saved to: {BACKUP_DIR / self.timestamp}\n")

        return {
            'status': 'success',
            'files_migrated': migrated_count,
            'total_changes': total_changes
        }

    def _save_migration_log(self, log_data: Dict):
        """Save migration log for audit trail."""
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Load existing logs
        logs = []
        if LOG_FILE.exists():
            logs = json.loads(LOG_FILE.read_text())

        # Append new log
        logs.append(log_data)

        # Save
        LOG_FILE.write_text(json.dumps(logs, indent=2))

    def rollback(self, backup_timestamp: str = None):
        """Rollback migration to previous state."""
        if backup_timestamp is None:
            # Use most recent backup
            backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()])
            if not backups:
                print("❌ No backups found for rollback\n")
                return
            backup_timestamp = backups[-1].name

        backup_path = BACKUP_DIR / backup_timestamp
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_timestamp}\n")
            return

        print(f"\n🔄 Rolling back to backup: {backup_timestamp}")
        print(f"   Backup location: {backup_path}\n")

        response = input("Proceed with rollback? (yes/no): ").lower()
        if response != 'yes':
            print("\n❌ Rollback cancelled\n")
            return

        # Restore all files from backup
        restored_count = 0
        for backup_file in backup_path.rglob('*'):
            if backup_file.is_file():
                relative_path = backup_file.relative_to(backup_path)
                original_path = PETESBRAIN_ROOT / relative_path

                # Restore file
                shutil.copy2(backup_file, original_path)
                restored_count += 1
                print(f"✅ Restored: {relative_path}")

        print(f"\n✅ Rollback complete! Restored {restored_count} files\n")


def verify_platform_ids_server() -> bool:
    """Verify that platform-ids MCP server is configured and working."""
    mcp_config = PETESBRAIN_ROOT / ".mcp.json"

    if not mcp_config.exists():
        print("❌ .mcp.json not found")
        return False

    config = json.loads(mcp_config.read_text())

    if 'platform-ids' not in config.get('mcpServers', {}):
        print("⚠️  platform-ids server not configured in .mcp.json")
        print("\nTo add it, edit .mcp.json and add:\n")
        print('''
"platform-ids": {
  "command": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/platform-ids-mcp-server/.venv/bin/python",
  "args": [
    "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/platform-ids-mcp-server/server.py"
  ],
  "env": {
    "CLIENT_IDS_PATH": "/Users/administrator/Documents/PetesBrain.nosync/data/state/client-platform-ids.json"
  }
}
        ''')
        return False

    print("✅ platform-ids MCP server is configured\n")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate to centralized platform-ids MCP server")
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backups (not recommended)')
    parser.add_argument('--rollback', type=str, nargs='?', const='latest', help='Rollback to backup (optionally specify timestamp)')
    parser.add_argument('--verify', action='store_true', help='Verify platform-ids server configuration')

    args = parser.parse_args()

    # Verify MCP server configuration
    if args.verify or not args.rollback:
        if not verify_platform_ids_server():
            print("\n❌ Please configure platform-ids MCP server before running migration\n")
            exit(1)

    # Handle rollback
    if args.rollback:
        migration = PlatformIDsMigration()
        if args.rollback == 'latest':
            migration.rollback()
        else:
            migration.rollback(args.rollback)
        exit(0)

    # Run migration
    migration = PlatformIDsMigration(
        dry_run=args.dry_run,
        create_backup=not args.no_backup
    )

    result = migration.run_migration()

    if result['status'] == 'success':
        print("\n📋 Next steps:")
        print("   1. Test MCP server: mcp__platform-ids__get_client_platform_ids('smythson')")
        print("   2. Run affected scripts/agents to verify they work")
        print("   3. If issues occur, rollback with: python migrate-to-platform-ids-mcp.py --rollback\n")
