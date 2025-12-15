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
import logging

# Configure logging
LOG_DIR = Path.home() / '.petesbrain-logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'tasks-backup_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler()  # Also output to console for LaunchAgent logs
    ]
)

logger = logging.getLogger(__name__)

# Add shared directory to path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync')

def export_google_tasks():
    """Export all Google Tasks to JSON files

    Returns:
        list: List of exported JSON file paths
    """
    logger.info("📥 Exporting Google Tasks...")
    exported_files = []

    try:
        # Import Google Tasks API service
        logger.debug("Importing Google Tasks service...")
        sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')
        from tasks_service import tasks_service

        logger.debug("Building Google Tasks service...")
        service = tasks_service()

        # Create temp directory for exports
        temp_dir = Path(tempfile.gettempdir()) / 'google-tasks-export'
        temp_dir.mkdir(exist_ok=True)
        logger.debug(f"Export directory: {temp_dir}")

        # Get all task lists
        logger.debug("Fetching task lists from Google Tasks API...")
        task_lists_response = service.tasklists().list().execute()
        task_lists = task_lists_response.get('items', [])

        # Decision point: Were any task lists found?
        if not task_lists:
            logger.warning("No Google Tasks lists found")
            return exported_files

        logger.info(f"Found {len(task_lists)} Google Tasks lists")

        # Export each task list
        for idx, task_list in enumerate(task_lists, 1):
            list_id = task_list['id']
            list_title = task_list['title']
            safe_title = list_title.replace(' ', '-').replace('/', '-').lower()

            logger.debug(f"Processing list {idx}/{len(task_lists)}: {list_title}")

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
            logger.info(f"  ✅ {list_title}: {len(tasks)} tasks")

        total_tasks = sum(len(json.load(open(f))['tasks']) for f in exported_files)
        logger.info(f"✅ Exported {len(task_lists)} Google Tasks lists ({total_tasks} total tasks)")

    except ImportError as e:
        logger.error("=" * 60)
        logger.error("❌ Google Tasks service import failed")
        logger.error(f"Error: {e}")
        logger.error("Action required: Check Google Tasks MCP server installation")
        logger.error("=" * 60)
    except Exception as e:
        logger.warning("=" * 60)
        logger.warning("⚠️  Could not export Google Tasks")
        logger.warning(f"Error: {e}")
        logger.warning("Continuing with local tasks.json files only")
        logger.warning("=" * 60)
        if "credentials" in str(e).lower() or "auth" in str(e).lower():
            logger.error("Possible cause: OAuth token expired")
            logger.error("Action: Run oauth-refresh skill")

    return exported_files

def find_all_task_files():
    """Find all tasks.json files across the codebase"""
    logger.info("🔍 Finding all task files...")
    base_path = Path('/Users/administrator/Documents/PetesBrain.nosync')
    logger.debug(f"Base path: {base_path}")

    task_files = []

    # Find all client tasks.json files
    clients_dir = base_path / 'clients'
    if clients_dir.exists():
        logger.debug(f"Scanning clients directory: {clients_dir}")
        client_count = 0
        for client_dir in clients_dir.iterdir():
            if client_dir.is_dir():
                # Check root location first (primary for all client work)
                tasks_file = client_dir / 'tasks.json'
                if tasks_file.exists():
                    task_files.append(tasks_file)
                    client_count += 1
                    logger.debug(f"  Found: {client_dir.name}/tasks.json")
                # Also check product-feeds location (temporary during migration rollback)
                product_feeds_tasks = client_dir / 'product-feeds' / 'tasks.json'
                if product_feeds_tasks.exists():
                    task_files.append(product_feeds_tasks)
                    client_count += 1
                    logger.debug(f"  Found: {client_dir.name}/product-feeds/tasks.json")

        logger.info(f"  ✅ Found {client_count} client task files")
    else:
        logger.warning(f"Clients directory not found: {clients_dir}")

    # Add main clients queue
    main_queue = clients_dir / 'tasks.json'
    if main_queue.exists():
        task_files.append(main_queue)
        logger.debug("  Found: clients/tasks.json (main queue)")

    # Add roksys tasks.json
    roksys_tasks = base_path / 'roksys' / 'tasks.json'
    if roksys_tasks.exists():
        task_files.append(roksys_tasks)
        logger.debug("  Found: roksys/tasks.json")

    # Add state files for completeness
    state_files = [
        base_path / 'data' / 'state' / 'tasks-state.json',
        base_path / 'data' / 'state' / 'tasks-completed.json',
        base_path / 'data' / 'state' / 'client-tasks.json',
    ]

    state_count = 0
    for state_file in state_files:
        if state_file.exists():
            task_files.append(state_file)
            state_count += 1
            logger.debug(f"  Found: {state_file.relative_to(base_path)}")

    if state_count > 0:
        logger.info(f"  ✅ Found {state_count} state files")

    logger.info(f"✅ Total task files found: {len(task_files)}")

    return task_files

def create_backup_archive():
    """Create a timestamped tarball of all task files including Google Tasks"""
    logger.info("📦 Creating backup archive...")
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
    archive_name = f'tasks-backup-{timestamp}.tar.gz'

    # Create in temp directory
    temp_dir = tempfile.gettempdir()
    archive_path = os.path.join(temp_dir, archive_name)
    logger.debug(f"Archive will be created at: {archive_path}")

    # Get local task files
    task_files = find_all_task_files()

    # Export Google Tasks
    google_tasks_files = export_google_tasks()

    # Decision point: Are there any files to backup?
    if not task_files and not google_tasks_files:
        logger.error("=" * 60)
        logger.error("❌ No task files found to backup")
        logger.error("Possible causes:")
        logger.error("  - Clients directory is empty")
        logger.error("  - Google Tasks export failed")
        logger.error("  - File permissions issue")
        logger.error("Action: Check clients directory and Google Tasks access")
        logger.error("=" * 60)
        return None

    logger.info(f"Creating tarball with {len(task_files)} local files + {len(google_tasks_files)} Google Tasks exports...")

    # Create tarball
    try:
        with tarfile.open(archive_path, 'w:gz') as tar:
            # Add local task files
            logger.debug("Adding local task files to archive...")
            for idx, task_file in enumerate(task_files, 1):
                # Add with relative path from PetesBrain root
                arcname = str(task_file.relative_to('/Users/administrator/Documents/PetesBrain.nosync'))
                tar.add(task_file, arcname=arcname)
                logger.debug(f"  [{idx}/{len(task_files)}] Added: {arcname}")

            # Add Google Tasks exports
            if google_tasks_files:
                logger.debug("Adding Google Tasks exports to archive...")
                for idx, google_tasks_file in enumerate(google_tasks_files, 1):
                    # Add with path that identifies them as Google Tasks exports
                    arcname = f'google-tasks/{google_tasks_file.name}'
                    tar.add(google_tasks_file, arcname=arcname)
                    logger.debug(f"  [{idx}/{len(google_tasks_files)}] Added: {arcname}")

        file_size = os.path.getsize(archive_path) / 1024  # KB

        logger.info("✅ Created backup archive successfully")
        logger.info(f"  Archive name: {archive_name}")
        logger.info(f"  Local task files: {len(task_files)}")
        logger.info(f"  Google Tasks exports: {len(google_tasks_files)}")
        logger.info(f"  Total files: {len(task_files) + len(google_tasks_files)}")
        logger.info(f"  Archive size: {file_size:.1f} KB")

        return archive_path, archive_name

    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ Failed to create backup archive")
        logger.error(f"Error: {e}")
        logger.error(f"Archive path: {archive_path}")
        logger.error("=" * 60)
        import traceback
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                logger.error(f"  {line}")
        return None

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
            logger.debug(f"  Found existing folder: {folder_name}")
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
            logger.info(f"📁 Created folder: {folder_name}")

    return parent_id

def upload_to_google_drive(archive_path, archive_name):
    """Upload backup archive to Google Drive using Google Drive API"""
    logger.info("📤 Uploading to Google Drive...")

    try:
        # Import Google Drive dependencies
        logger.debug("Importing Google Drive API dependencies...")
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials

        # Load OAuth tokens from MCP server's token file
        token_path = os.path.expanduser('~/.config/google-drive-mcp/tokens.json')
        logger.debug(f"Looking for OAuth tokens at: {token_path}")

        # Decision point: Do OAuth tokens exist?
        if not os.path.exists(token_path):
            logger.error("=" * 60)
            logger.error("❌ Google Drive tokens not found")
            logger.error(f"Expected location: {token_path}")
            logger.error("Action required: Run authentication command")
            logger.error("Command: npx @piotr-agier/google-drive-mcp auth")
            logger.error("=" * 60)
            return False

        logger.debug("Loading OAuth tokens...")
        with open(token_path, 'r') as f:
            token_data = json.load(f)

        # Create credentials from token
        logger.debug("Creating credentials from OAuth tokens...")
        creds = Credentials(
            token=token_data['token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret')
        )

        # Build Google Drive service
        logger.debug("Building Google Drive service...")
        service = build('drive', 'v3', credentials=creds)

        file_size_kb = os.path.getsize(archive_path) / 1024
        logger.info(f"  Archive name: {archive_name}")
        logger.info(f"  Archive size: {file_size_kb:.1f} KB")

        # Find or create backup folder structure
        logger.debug("Finding/creating backup folder structure...")
        folder_id = find_or_create_folder_structure(service, ['PetesBrain-Backups', 'Tasks'])
        logger.debug(f"Target folder ID: {folder_id}")

        # Upload file
        logger.info("Uploading file to Google Drive...")
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

        logger.info("✅ Uploaded to Google Drive successfully")
        logger.info(f"  File ID: {file['id']}")
        logger.info(f"  Location: PetesBrain-Backups/Tasks/{archive_name}")

        # Update tokens if refreshed
        logger.debug("Updating OAuth tokens...")
        with open(token_path, 'w') as f:
            token_data['token'] = creds.token
            if creds.expiry:
                token_data['expiry'] = creds.expiry.isoformat()
            json.dump(token_data, f, indent=2)

        # Also save local backup as fallback
        logger.info("Saving local backup copy...")
        import shutil
        backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')
        backup_dir.mkdir(parents=True, exist_ok=True)
        local_backup = backup_dir / archive_name
        shutil.copy2(archive_path, local_backup)

        logger.info(f"✅ Local backup saved: {local_backup}")

        return True

    except ImportError as e:
        logger.error("=" * 60)
        logger.error("❌ Google Drive API dependencies missing")
        logger.error(f"Error: {e}")
        logger.error("Action required: pip install google-api-python-client google-auth")
        logger.error("=" * 60)
        return False

    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ Error uploading to Google Drive")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e}")

        # Check for common error types
        if "credentials" in str(e).lower() or "auth" in str(e).lower():
            logger.error("Possible cause: OAuth token expired or invalid")
            logger.error("Action: Re-run authentication or run oauth-refresh skill")
        elif "quota" in str(e).lower():
            logger.error("Possible cause: Google Drive API quota exceeded")
            logger.error("Action: Wait 24 hours or increase quota")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            logger.error("Possible cause: Network connectivity issue")
            logger.error("Action: Check internet connection")
        else:
            logger.error("Action: Review error message above")

        logger.error("Falling back to local backup only...")
        logger.error("=" * 60)

        # Still save local backup as fallback
        try:
            logger.info("Attempting local backup fallback...")
            import shutil
            backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')
            backup_dir.mkdir(parents=True, exist_ok=True)
            local_backup = backup_dir / archive_name
            shutil.copy2(archive_path, local_backup)
            logger.info(f"✅ Local backup saved: {local_backup}")
            return True
        except Exception as fallback_error:
            logger.error("=" * 60)
            logger.error("❌ Local backup also failed")
            logger.error(f"Error: {fallback_error}")
            logger.error("=" * 60)
            import traceback
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    logger.error(f"  {line}")
            return False

def cleanup_old_backups():
    """Remove backups older than 30 days"""
    logger.info("🗑️  Cleaning up old backups...")
    backup_dir = Path('/Users/administrator/Documents/PetesBrain/_backups/tasks')

    # Decision point: Does backup directory exist?
    if not backup_dir.exists():
        logger.debug(f"Backup directory does not exist: {backup_dir}")
        logger.info("No cleanup needed (backup directory does not exist)")
        return

    logger.debug(f"Scanning backup directory: {backup_dir}")
    cutoff_date = datetime.now() - timedelta(days=30)
    logger.debug(f"Removing backups older than: {cutoff_date.strftime('%Y-%m-%d')}")

    removed_count = 0
    error_count = 0

    for backup_file in backup_dir.glob('tasks-backup-*.tar.gz'):
        # Extract date from filename: tasks-backup-YYYY-MM-DD-HHMM.tar.gz
        try:
            date_str = backup_file.stem.replace('tasks-backup-', '')[:10]  # YYYY-MM-DD
            file_date = datetime.strptime(date_str, '%Y-%m-%d')

            # Decision point: Is this backup older than cutoff?
            if file_date < cutoff_date:
                backup_file.unlink()
                removed_count += 1
                logger.debug(f"  🗑️  Removed old backup: {backup_file.name} (from {file_date.strftime('%Y-%m-%d')})")
            else:
                logger.debug(f"  ✓ Keeping backup: {backup_file.name} (from {file_date.strftime('%Y-%m-%d')})")

        except Exception as e:
            error_count += 1
            logger.warning(f"⚠️  Could not parse date from {backup_file.name}: {e}")

    # Summary
    if removed_count > 0:
        logger.info(f"✅ Cleaned up {removed_count} old backup(s)")
    else:
        logger.info("No old backups to remove")

    if error_count > 0:
        logger.warning(f"⚠️  {error_count} file(s) could not be processed")

def main():
    """Main backup routine"""
    # LOG 1/5: START - Entry log with timestamp
    logger.info("=" * 60)
    logger.info("🚀 Starting Tasks Backup Agent")
    logger.info(f"📅 Execution time: {datetime.now():%Y-%m-%d %H:%M:%S}")
    logger.info("=" * 60)

    try:
        # LOG 2/5: DATA COLLECTION - Create backup archive
        logger.info("")
        logger.info("📋 Creating backup archive...")
        result = create_backup_archive()

        if result is None:
            logger.error("")
            logger.error("=" * 60)
            logger.error("❌ Backup failed: No files to backup")
            logger.error("=" * 60)
            return 1

        archive_path, archive_name = result

        # LOG 3/5: PROCESSING - Upload to Google Drive
        logger.info("")
        logger.info("⚙️  Processing backup upload...")
        success = upload_to_google_drive(archive_path, archive_name)

        # Clean up temp archive
        logger.debug("")
        logger.debug("Cleaning up temporary archive...")
        try:
            os.remove(archive_path)
            logger.debug(f"✅ Removed temp archive: {archive_path}")
        except Exception as e:
            logger.warning(f"⚠️  Could not remove temp archive: {e}")

        # LOG 4/5: OUTPUT - Clean up old backups
        logger.info("")
        logger.info("🧹 Performing cleanup...")
        cleanup_old_backups()

        # LOG 5/5: END - Success summary
        logger.info("")
        logger.info("=" * 60)
        if success:
            logger.info("✅ Tasks Backup Completed Successfully")
            logger.info(f"  Archive: {archive_name}")
            logger.info(f"  Location: PetesBrain-Backups/Tasks/ (Google Drive)")
            logger.info(f"  Local: _backups/tasks/ (fallback)")
        else:
            logger.warning("⚠️  Tasks Backup Completed with Warnings")
            logger.warning("  Google Drive upload may have failed")
            logger.warning("  Check logs above for details")
        logger.info("=" * 60)

        return 0 if success else 1

    except KeyboardInterrupt:
        logger.warning("")
        logger.warning("⚠️  Tasks Backup Interrupted by User")
        return 130

    except Exception as e:
        # Full debugging package
        logger.error("")
        logger.error("=" * 60)
        logger.error("❌ Tasks Backup Failed - Unexpected Error")
        logger.error("=" * 60)

        logger.error("1. Operation Context:")
        logger.error(f"   - Function: main()")
        logger.error(f"   - Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S}")
        logger.error(f"   - Working directory: {os.getcwd()}")

        logger.error("2. Error Details:")
        logger.error(f"   - Type: {type(e).__name__}")
        logger.error(f"   - Message: {str(e)}")

        logger.error("3. Possible Causes:")
        if "permission" in str(e).lower() or "denied" in str(e).lower():
            logger.error("   - File permissions issue")
            logger.error("   - Action: Check read/write permissions on backup directories")
        elif "oauth" in str(e).lower() or "credentials" in str(e).lower():
            logger.error("   - OAuth authentication issue")
            logger.error("   - Action: Run oauth-refresh skill")
        elif "quota" in str(e).lower():
            logger.error("   - Google API quota exceeded")
            logger.error("   - Action: Wait 24 hours or increase quota")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            logger.error("   - Network connectivity issue")
            logger.error("   - Action: Check internet connection")
        elif "disk" in str(e).lower() or "space" in str(e).lower():
            logger.error("   - Insufficient disk space")
            logger.error("   - Action: Free up disk space")
        else:
            logger.error("   - Unexpected error")
            logger.error("   - Action: Review error message and stack trace below")

        logger.error("4. Stack Trace:")
        import traceback
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                logger.error(f"   {line}")

        logger.error("=" * 60)

        return 1

if __name__ == '__main__':
    sys.exit(main())
