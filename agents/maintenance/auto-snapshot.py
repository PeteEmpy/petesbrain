#!/usr/bin/env python3
"""
Automated daily snapshot creation for PetesBrain.
Runs at 2 AM daily via LaunchAgent.
Creates safety snapshot and cleans up snapshots older than 7 days.
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path.home() / 'Documents/PetesBrain.nosync'))

def main():
    """Create daily snapshot and cleanup old ones."""
    try:
        # Import rollback manager
        from shared.rollback_manager import RollbackManager

        # Create snapshot
        manager = RollbackManager()
        timestamp = datetime.now().strftime('%Y-%m-%d')

        print(f"[{datetime.now().isoformat()}] Creating auto-snapshot for {timestamp}...", flush=True)

        manager.create_snapshot(
            description=f"Auto-snapshot {timestamp}",
            category="auto-daily"
        )

        print(f"[{datetime.now().isoformat()}] ✅ Snapshot created successfully", flush=True)

        # Cleanup old auto-snapshots (keep last 7 days)
        cleanup_old_snapshots()

        print(f"[{datetime.now().isoformat()}] ✅ Auto-snapshot completed successfully", flush=True)

    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ❌ ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

def cleanup_old_snapshots():
    """Remove auto-snapshots older than 7 days."""
    snapshot_dir = Path.home() / 'Documents/PetesBrain.nosync/infrastructure/rollback-snapshots'

    if not snapshot_dir.exists():
        return

    cutoff = datetime.now() - timedelta(days=7)
    deleted_count = 0

    for snapshot in snapshot_dir.glob('*/'):
        try:
            manifest = snapshot / 'manifest.json'
            if manifest.exists():
                data = json.loads(manifest.read_text())
                if data.get('category') == 'auto-daily':
                    # Parse ISO format timestamp
                    created_str = data.get('created_at', '')
                    if created_str:
                        # Handle both ISO format with and without microseconds
                        try:
                            created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                        except:
                            created = datetime.fromisoformat(created_str.split('.')[0])

                        if created < cutoff:
                            print(f"[{datetime.now().isoformat()}] Removing old snapshot: {snapshot.name}", flush=True)
                            shutil.rmtree(snapshot)
                            deleted_count += 1
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Warning: Could not process {snapshot.name}: {e}", flush=True)

    if deleted_count > 0:
        print(f"[{datetime.now().isoformat()}] Cleaned up {deleted_count} old auto-snapshots", flush=True)

if __name__ == '__main__':
    main()
