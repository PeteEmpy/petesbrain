#!/usr/bin/env python3
"""
Tasks Backup Agent
Backs up all tasks.json files to Google Drive every 3 hours
Prevents catastrophic data loss from accidental deletions
"""

import os
import sys
import json
import tarfile
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain')

def export_google_tasks():
    """Export all Google Tasks to JSON files

    Returns:
        list: List of exported JSON file paths
    """
    exported_files = []

    try:
        # Import Google Tasks API service
        sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')
        from tasks_service import tasks_service

        service = tasks_service()

        # Create temp directory for exports
        temp_dir = Path(tempfile.gettempdir()) / 'google-tasks-export'
        temp_dir.mkdir(exist_ok=True)

        print("📥 Exporting Google Tasks...")

        # Get all task lists
        task_lists_response = service.tasklists().list().execute()
        task_lists = task_lists_response.get('items', [])

        if not task_lists:
            print("   No Google Tasks lists found")
            return exported_files

        # Export each task list
        for task_list in task_lists:
            list_id = task_list['id']
            list_title = task_list['title']
            safe_title = list_title.replace(' ', '-').replace('/', '-').lower()

            # Get all tasks in this list (including completed)
            tasks_response = service.tasks().list(
                tasklist=list_id,
                showCompleted=True,
                showHidden=True
            ).execute()
            tasks = tasks_response.get('items', [])

            # Create export data
            export_data = {
                'task_list': task_list,
                'tasks': tasks,
                'exported_at': datetime.now().isoformat(),
                'task_count': len(tasks)
            }

            # Save to JSON file
            export_file = temp_dir / f'{safe_title}.json'
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2)

            exported_files.append(export_file)
            print(f"   ✅ {list_title}: {len(tasks)} tasks")

        total_tasks = sum(len(json.load(open(f))['tasks']) for f in exported_files)
        print(f"✅ Exported {len(task_lists)} Google Tasks lists ({total_tasks} total tasks)")

    except Exception as e:
        print(f"⚠️  Could not export Google Tasks: {e}")
        print("   Continuing with local tasks.json files only")

    return exported_files

def find_all_task_files():
    """Find all tasks.json files across the codebase"""
    base_path = Path('/Users/administrator/Documents/PetesBrain')

    task_files = []

    # Find all client tasks.json files
    clients_dir = base_path / 'clients'
    if clients_dir.exists():
        for client_dir in clients_dir.iterdir():
            if client_dir.is_dir():
                # Check root location first (primary for all client work)
                tasks_file = client_dir / 'tasks.json'
                if tasks_file.exists():
                    task_files.append(tasks_file)                pf_tasks_file = None  # Removed: product-feeds location no longer used
                if pf_tasks_file.exists():
                    task_files.append(tasks_file)

    # Add main clients queue
    main_queue = clients_dir / 'tasks.json'
    if main_queue.exists():
        task_files.append(main_queue)

    # Add roksys tasks.json
    roksys_tasks = base_path / 'roksys' / 'tasks.json'
    if roksys_tasks.exists():
        task_files.append(roksys_tasks)

    # Add state files for completeness
    state_files = [
        base_path / 'data' / 'state' / 'tasks-state.json',
        base_path / 'data' / 'state' / 'tasks-completed.json',
        base_path / 'data' / 'state' / 'client-tasks.json',
    ]

    for state_file in state_files:
        if state_file.exists():
            task_files.append(state_file)

    return task_files

def create_backup_archive():
    """Create a timestamped tarball of all task files including Google Tasks"""
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
    archive_name = f'tasks-backup-{timestamp}.tar.gz'

    # Create in temp directory
    temp_dir = tempfile.gettempdir()
    archive_path = os.path.join(temp_dir, archive_name)

    # Get local task files
    task_files = find_all_task_files()

    # Export Google Tasks
    google_tasks_files = export_google_tasks()

    if not task_files and not google_tasks_files:
        print("⚠️  No task files found to backup")
        return None

    # Create tarball
    with tarfile.open(archive_path, 'w:gz') as tar:
        # Add local task files
        for task_file in task_files:
            # Add with relative path from PetesBrain root
            arcname = str(task_file.relative_to('/Users/administrator/Documents/PetesBrain'))
            tar.add(task_file, arcname=arcname)

        # Add Google Tasks exports
        for google_tasks_file in google_tasks_files:
            # Add with path that identifies them as Google Tasks exports
            arcname = f'google-tasks/{google_tasks_file.name}'
            tar.add(google_tasks_file, arcname=arcname)

    file_size = os.path.getsize(archive_path) / 1024  # KB

    print(f"✅ Created backup archive: {archive_name}")
    print(f"   Local task files: {len(task_files)}")
    print(f"   Google Tasks exports: {len(google_tasks_files)}")
    print(f"   Total files: {len(task_files) + len(google_tasks_files)}")
    print(f"   Archive size: {file_size:.1f} KB")

    return archive_path, archive_name

def find_or_create_folder_structure(service, folder_names):
    """Find or create nested folder structure in Google Drive

    Args:
        service: Google Drive API service instance
        folder_names: List of folder names (e.g., ['PetesBrain-Backups', 'Tasks'])

    Returns:
        str: ID of the final folder in the structure
    """
    parent_id = 'root'

    for folder_name in folder_names:
        # Search for folder with this name under parent
        query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"

        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        folders = results.get('files', [])

        if folders:
            # Folder exists, use it
            parent_id = folders[0]['id']
        else:
            # Create folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }

            folder = service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            parent_id = folder['id']
            print(f"📁 Created folder: {folder_name}")

    return parent_id

def upload_to_google_drive(archive_path, archive_name):
    """Upload backup archive to Google Drive using Google Drive API"""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials

        # Load OAuth tokens from MCP server's token file
        token_path = os.path.expanduser('~/.config/google-drive-mcp/tokens.json')

        if not os.path.exists(token_path):
            print(f"⚠️  Google Drive tokens not found at {token_path}")
            print("   Run: npx @piotr-agier/google-drive-mcp auth")
            return False

        with open(token_path, 'r') as f:
            token_data = json.load(f)

        # Create credentials from token
        creds = Credentials(
            token=token_data['token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret')
        )

        # Build Google Drive service
        service = build('drive', 'v3', credentials=creds)

        print(f"📤 Uploading to Google Drive: {archive_name}")
        print(f"   Size: {os.path.getsize(archive_path) / 1024:.1f} KB")

        # Find or create backup folder structure
        folder_id = find_or_create_folder_structure(service, ['PetesBrain-Backups', 'Tasks'])

        # Upload file
        file_metadata = {
            'name': archive_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(
            archive_path,
            mimetype='application/gzip',
            resumable=True
        )

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()

        print(f"✅ Uploaded to Google Drive successfully")
        print(f"   File ID: {file['id']}")
        print(f"   Location: PetesBrain-Backups/Tasks/{archive_name}")

        # Update tokens if refreshed
        with open(token_path, 'w') as f:
            token_data['token'] = creds.token
            if creds.expiry:
                token_data['expiry'] = creds.expiry.isoformat()
            json.dump(token_data, f, indent=2)

        # Also save local backup as fallback
        import shutil
        backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')
        backup_dir.mkdir(parents=True, exist_ok=True)
        local_backup = backup_dir / archive_name
        shutil.copy2(archive_path, local_backup)

        print(f"✅ Local backup saved: {local_backup}")

        return True

    except Exception as e:
        print(f"❌ Error uploading to Google Drive: {e}")
        print(f"   Falling back to local backup only")

        # Still save local backup as fallback
        try:
            import shutil
            backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')
            backup_dir.mkdir(parents=True, exist_ok=True)
            local_backup = backup_dir / archive_name
            shutil.copy2(archive_path, local_backup)
            print(f"✅ Local backup saved: {local_backup}")
            return True
        except Exception as fallback_error:
            print(f"❌ Local backup also failed: {fallback_error}")
            return False

def cleanup_old_backups():
    """Remove backups older than 30 days"""
    backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')

    if not backup_dir.exists():
        return

    cutoff_date = datetime.now() - timedelta(days=30)
    removed_count = 0

    for backup_file in backup_dir.glob('tasks-backup-*.tar.gz'):
        # Extract date from filename: tasks-backup-YYYY-MM-DD-HHMM.tar.gz
        try:
            date_str = backup_file.stem.replace('tasks-backup-', '')[:10]  # YYYY-MM-DD
            file_date = datetime.strptime(date_str, '%Y-%m-%d')

            if file_date < cutoff_date:
                backup_file.unlink()
                removed_count += 1
                print(f"🗑️  Removed old backup: {backup_file.name}")
        except Exception as e:
            print(f"⚠️  Could not parse date from {backup_file.name}: {e}")

    if removed_count > 0:
        print(f"✅ Cleaned up {removed_count} old backup(s)")

def main():
    """Main backup routine"""
    print("=" * 60)
    print("Tasks Backup Agent")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Create backup archive
    result = create_backup_archive()

    if result is None:
        print("❌ Backup failed: No files to backup")
        return 1

    archive_path, archive_name = result

    # Upload to Google Drive
    success = upload_to_google_drive(archive_path, archive_name)

    # Clean up temp archive
    try:
        os.remove(archive_path)
    except Exception as e:
        print(f"⚠️  Could not remove temp archive: {e}")

    # Clean up old backups
    cleanup_old_backups()

    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
