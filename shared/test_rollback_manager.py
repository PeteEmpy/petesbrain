"""
Unit tests for RollbackManager

Tests core functionality:
- Snapshot creation
- Snapshot listing
- Dry-run restore
- Actual restore
- File integrity checking
- Error handling

Run with: python -m pytest shared/test_rollback_manager.py -v
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
import shutil

from rollback_manager import RollbackManager, RollbackSnapshot


class TestRollbackSnapshot(unittest.TestCase):
    """Tests for RollbackSnapshot class."""

    def setUp(self):
        """Set up test snapshot directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.snapshot_dir = Path(self.temp_dir) / "20251211_120000"
        self.snapshot_dir.mkdir()

        # Create manifest
        self.manifest = {
            "created_at": datetime.now().isoformat(),
            "description": "Test snapshot",
            "category": "test",
            "plist_files": [
                {
                    "original": "/path/to/test.plist",
                    "backup": str(self.snapshot_dir / "plist" / "test.plist"),
                    "hash": "abc123"
                }
            ],
            "config_files": [],
            "git_state": {
                "commit": "abc123def456",
                "branch": "main"
            },
            "venv_metadata": {}
        }

        manifest_file = self.snapshot_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(self.manifest, f)

    def tearDown(self):
        """Clean up test directories."""
        shutil.rmtree(self.temp_dir)

    def test_load_manifest(self):
        """Test loading snapshot manifest."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        manifest = snapshot.load_manifest()
        self.assertEqual(manifest["description"], "Test snapshot")
        self.assertEqual(manifest["category"], "test")

    def test_get_timestamp(self):
        """Test extracting timestamp from snapshot."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        self.assertEqual(snapshot.get_timestamp(), "20251211_120000")

    def test_get_created_at(self):
        """Test getting creation time."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        created = snapshot.get_created_at()
        self.assertIsInstance(created, datetime)

    def test_get_description(self):
        """Test getting snapshot description."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        self.assertEqual(snapshot.get_description(), "Test snapshot")

    def test_get_category(self):
        """Test getting snapshot category."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        self.assertEqual(snapshot.get_category(), "test")

    def test_get_plist_files(self):
        """Test getting list of plist files."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        plist_files = snapshot.get_plist_files()
        self.assertEqual(len(plist_files), 1)
        self.assertIn("original", plist_files[0])

    def test_get_git_state(self):
        """Test getting git state."""
        snapshot = RollbackSnapshot(self.snapshot_dir)
        git_state = snapshot.get_git_state()
        self.assertIn("commit", git_state)
        self.assertIn("branch", git_state)


class TestRollbackManager(unittest.TestCase):
    """Tests for RollbackManager class."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)

        # Create necessary directories
        (self.project_root / "infrastructure").mkdir()
        (self.project_root / "shared").mkdir()
        (self.project_root / "infrastructure" / "mcp-servers").mkdir()

        # Create LaunchAgents directory
        self.plist_dir = Path(self.temp_dir) / "LaunchAgents"
        self.plist_dir.mkdir()

        # Create test plist files (must match petesbrain pattern)
        self.test_plist = self.plist_dir / "com.petesbrain.test.plist"
        self.test_plist.write_text("<?xml version='1.0'?><plist></plist>")

        self.manager = RollbackManager(self.project_root)
        self.manager.plist_dir = self.plist_dir

    def tearDown(self):
        """Clean up test directories."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test manager initialization."""
        self.assertTrue(self.manager.snapshots_dir.exists())
        self.assertEqual(self.manager.project_root, self.project_root)

    def test_create_snapshot(self):
        """Test creating a snapshot."""
        snapshot_id = self.manager.create_snapshot("Test snapshot", "test")
        self.assertIsNotNone(snapshot_id)

        # Verify snapshot directory was created
        snapshot_dir = self.manager.snapshots_dir / snapshot_id
        self.assertTrue(snapshot_dir.exists())

        # Verify manifest was created
        manifest_file = snapshot_dir / "manifest.json"
        self.assertTrue(manifest_file.exists())

        # Verify manifest contents
        with open(manifest_file) as f:
            manifest = json.load(f)
        self.assertEqual(manifest["description"], "Test snapshot")
        self.assertEqual(manifest["category"], "test")

    def test_list_snapshots(self):
        """Test listing snapshots."""
        # Create some test snapshots
        self.manager.create_snapshot("Snapshot 1", "test")
        self.manager.create_snapshot("Snapshot 2", "test")

        snapshots = self.manager.list_snapshots()
        self.assertEqual(len(snapshots), 2)

        # Verify they're sorted by date (most recent first)
        first = snapshots[0]
        second = snapshots[1]
        self.assertGreater(
            first.get_created_at(),
            second.get_created_at()
        )

    def test_get_latest_snapshot(self):
        """Test getting the latest snapshot."""
        # No snapshots initially
        self.assertIsNone(self.manager.get_latest_snapshot())

        # Create a snapshot
        self.manager.create_snapshot("Test", "test")
        latest = self.manager.get_latest_snapshot()
        self.assertIsNotNone(latest)
        self.assertEqual(latest.get_description(), "Test")

    def test_file_hash(self):
        """Test file hashing for integrity checking."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("test content")

        # Hash should be deterministic
        hash1 = self.manager._file_hash(test_file)
        hash2 = self.manager._file_hash(test_file)
        self.assertEqual(hash1, hash2)

        # Different content should have different hash
        test_file.write_text("different content")
        hash3 = self.manager._file_hash(test_file)
        self.assertNotEqual(hash1, hash3)

    def test_dry_run_restore_unchanged(self):
        """Test dry-run restore when nothing has changed."""
        # Create a snapshot
        snapshot_id = self.manager.create_snapshot("Test", "test")

        # Dry-run restore (nothing changed, so all files should be marked 'Unchanged')
        success, message = self.manager.restore_snapshot(snapshot_id, dry_run=True)
        self.assertTrue(success)
        self.assertIn("DRY RUN", message)
        self.assertIn("Unchanged", message)

    def test_dry_run_restore_modified(self):
        """Test dry-run restore when a file has been modified."""
        # Create initial snapshot
        snapshot_id = self.manager.create_snapshot("Test", "test")

        # Modify a plist file
        self.test_plist.write_text("<?xml version='1.0'?><modified></modified>")

        # Dry-run restore should show file as modified
        success, message = self.manager.restore_snapshot(snapshot_id, dry_run=True)
        self.assertTrue(success)
        self.assertIn("Would restore (modified)", message)

    def test_restore_snapshot_creates_backup(self):
        """Test that restore creates a backup before restoring."""
        # Create initial snapshot
        snapshot_id = self.manager.create_snapshot("Test", "test")

        # Modify the plist
        self.test_plist.write_text("<?xml version='1.0'?><modified></modified>")

        # Perform restore (this should create an auto-backup)
        success, message = self.manager.restore_snapshot(snapshot_id, dry_run=False)

        # Verify auto-backup was created
        snapshots = self.manager.list_snapshots()
        self.assertEqual(len(snapshots), 2)  # Original + auto-backup

        # Verify auto-backup has "auto-backup" category
        auto_backup = snapshots[0]  # Most recent
        self.assertEqual(auto_backup.get_category(), "auto-backup")

    def test_restore_nonexistent_snapshot(self):
        """Test restore with nonexistent snapshot ID."""
        success, message = self.manager.restore_snapshot("nonexistent", dry_run=True)
        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_snapshot_with_multiple_plist_files(self):
        """Test snapshot creation with multiple plist files."""
        # Create multiple test plist files (must match petesbrain pattern)
        for i in range(3):
            plist = self.plist_dir / f"com.petesbrain.test{i}.plist"
            plist.write_text("<?xml version='1.0'?><plist></plist>")

        # Create snapshot
        snapshot_id = self.manager.create_snapshot("Multiple plists", "test")

        # Load manifest and verify all files are backed up
        snapshot_dir = self.manager.snapshots_dir / snapshot_id
        snapshot = RollbackSnapshot(snapshot_dir)
        plist_files = snapshot.get_plist_files()

        self.assertEqual(len(plist_files), 3)

    def test_snapshot_manifest_structure(self):
        """Test snapshot manifest has required fields."""
        snapshot_id = self.manager.create_snapshot("Test", "test")
        snapshot_dir = self.manager.snapshots_dir / snapshot_id
        snapshot = RollbackSnapshot(snapshot_dir)
        manifest = snapshot.load_manifest()

        required_fields = [
            "created_at",
            "description",
            "category",
            "plist_files",
            "config_files",
            "git_state",
            "venv_metadata"
        ]

        for field in required_fields:
            self.assertIn(field, manifest, f"Missing field: {field}")

    def test_snapshot_timestamp_format(self):
        """Test snapshot timestamp format."""
        snapshot_id = self.manager.create_snapshot("Test", "test")
        # Timestamp should be YYYYMMDD_HHMMSS
        self.assertRegex(snapshot_id, r"^\d{8}_\d{6}$")


class TestRollbackIntegration(unittest.TestCase):
    """Integration tests for complete rollback workflow."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)

        # Create directory structure
        (self.project_root / "infrastructure").mkdir()
        (self.project_root / "shared").mkdir()
        (self.project_root / "infrastructure" / "mcp-servers").mkdir()

        self.plist_dir = Path(self.temp_dir) / "LaunchAgents"
        self.plist_dir.mkdir()

        # Create test plist (must match petesbrain pattern)
        self.test_plist = self.plist_dir / "com.petesbrain.test.plist"
        self.test_plist.write_text("<?xml version='1.0'?><version1></version1>")

        self.manager = RollbackManager(self.project_root)
        self.manager.plist_dir = self.plist_dir

    def tearDown(self):
        """Clean up test directories."""
        shutil.rmtree(self.temp_dir)

    def test_complete_snapshot_and_restore_workflow(self):
        """Test complete workflow: create snapshot, modify, restore."""
        # Step 1: Create initial snapshot
        snapshot_id = self.manager.create_snapshot("Baseline", "test")
        self.assertIsNotNone(snapshot_id)

        # Step 2: Verify file content at snapshot time
        original_content = self.test_plist.read_text()
        self.assertIn("version1", original_content)

        # Step 3: Modify the file
        modified_content = "<?xml version='1.0'?><version2></version2>"
        self.test_plist.write_text(modified_content)
        self.assertIn("version2", self.test_plist.read_text())

        # Step 4: Restore from snapshot
        success, message = self.manager.restore_snapshot(snapshot_id, dry_run=False)
        self.assertTrue(success)

        # Step 5: Verify file was restored to original state
        restored_content = self.test_plist.read_text()
        self.assertEqual(restored_content, original_content)
        self.assertIn("version1", restored_content)
        self.assertNotIn("version2", restored_content)

    def test_multiple_snapshots_and_selective_restore(self):
        """Test creating multiple snapshots and restoring to a specific one."""
        # Create first snapshot
        snap1 = self.manager.create_snapshot("Snapshot 1", "test")
        self.test_plist.write_text("<?xml version='1.0'?><version2></version2>")

        # Create second snapshot
        snap2 = self.manager.create_snapshot("Snapshot 2", "test")
        self.test_plist.write_text("<?xml version='1.0'?><version3></version3>")

        # Restore to first snapshot (should get version2)
        success, message = self.manager.restore_snapshot(snap1, dry_run=False)
        self.assertTrue(success)
        self.assertIn("version2", self.test_plist.read_text())

        # Verify 3 snapshots exist (original, snap1, snap2, plus auto-backups)
        snapshots = self.manager.list_snapshots()
        self.assertGreaterEqual(len(snapshots), 3)


if __name__ == "__main__":
    unittest.main()
