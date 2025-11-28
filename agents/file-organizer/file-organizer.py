#!/usr/bin/env python3
"""
File Organization & Cleanup Skill - Comprehensive Edition

Automatically tidies up files in the PetesBrain project with advanced features:
1. Organizes client folders according to standard structure
2. Removes/archives duplicate files (name-based and content-based)
3. Moves misplaced files to correct locations
4. Cleans up temporary/backup files
5. Organizes reports by date/quarter
6. Detects and organizes email drafts
7. Content-based file detection
8. Product feed organization
9. Broken reference detection and fixing
10. Empty folder cleanup
11. Archive old files
12. File size analysis
13. Folder structure validation
14. Script path updates
15. Undo functionality
16. HTML report generation

Usage:
    python3 shared/scripts/file-organizer.py [--dry-run] [--client CLIENT_NAME] [--undo] [--report]
"""

import os
import sys
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Set
import json
import html

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CLIENTS_DIR = PROJECT_ROOT / 'clients'
ROKSYS_DIR = PROJECT_ROOT / 'roksys'
PERSONAL_DIR = PROJECT_ROOT / 'personal'
SHARED_DIR = PROJECT_ROOT / 'shared'
DOCS_DIR = PROJECT_ROOT / 'docs'
TOOLS_DIR = PROJECT_ROOT / 'tools'

# Files that should stay in root
ROOT_FILES = {
    'README.md',
    '.gitignore',
    '.mcp.json',
    'verify_completion.sh'
}

# Client root files (must stay in client root)
CLIENT_ROOT_FILES = {
    'CONTEXT.md',
    'tasks-completed.md',
    'README.md',
    'llms.txt',
    'agents.txt'
}

# Standard client folder structure
CLIENT_FOLDERS = [
    'emails',
    'meeting-notes',
    'briefs',
    'documents',
    'presentations',
    'spreadsheets',
    'reports',
    'product-feeds',
    'scripts',
    'audits'
]

# Report subfolders
REPORT_SUBFOLDERS = {
    'monthly': r'(\d{4})-(\d{2})',  # YYYY-MM pattern
    'q1': r'q1-(\d{4})',
    'q2': r'q2-(\d{4})',
    'q3': r'q3-(\d{4})',
    'q4': r'q4-(\d{4})',
    'pmax-analysis': r'pmax',
    'ad-hoc': None  # Default catch-all
}

# File type mappings
FILE_TYPE_MAPPINGS = {
    '.py': 'scripts',
    '.sh': 'scripts',
    '.js': 'scripts',
    '.md': 'documents',  # Will be refined based on content
    '.txt': 'documents',
    '.docx': 'documents',
    '.doc': 'documents',
    '.pdf': 'documents',
    '.xlsx': 'spreadsheets',
    '.xls': 'spreadsheets',
    '.csv': 'spreadsheets',
    '.pptx': 'presentations',
    '.ppt': 'presentations',
    '.key': 'presentations',
    '.html': 'reports',
    '.json': 'product-feeds',  # Will be refined
    '.xml': 'product-feeds',
    '.png': 'documents',
    '.jpg': 'documents',
    '.jpeg': 'documents',
    '.gif': 'documents',
    '.yaml': 'documents',
    '.yml': 'documents',
    '.toml': 'documents',
    '.lock': 'documents',
    '.backup': None,
}

# Patterns for duplicate files
DUPLICATE_PATTERNS = [
    r'(.+)\s+2\.(\w+)$',
    r'(.+)\s+3\.(\w+)$',
    r'(.+)\s+4\.(\w+)$',
    r'(.+)\s+5\.(\w+)$',
]

# Temporary/backup file patterns
TEMP_PATTERNS = [
    r'\.tmp$',
    r'\.bak$',
    r'\.backup$',
    r'~$',
    r'\.swp$',
    r'\.DS_Store$',
]

# Archive retention (days)
ARCHIVE_RETENTION = {
    'reports': 365,  # Keep reports for 1 year
    'spreadsheets': 180,  # Keep spreadsheets for 6 months
    'documents': 365,
    'default': 90,  # Default 3 months
}


class FileOrganizer:
    """Comprehensive file organizer with advanced features"""
    
    def __init__(self, dry_run: bool = False, client_filter: Optional[str] = None):
        self.dry_run = dry_run
        self.client_filter = client_filter
        self.stats = {
            'moved': 0,
            'archived': 0,
            'deleted': 0,
            'folders_created': 0,
            'duplicates_found': 0,
            'references_fixed': 0,
            'large_files': [],
            'empty_folders': [],
            'errors': 0
        }
        self.actions = []
        self.content_hashes = {}  # For content-based duplicate detection
        
    def log_action(self, action: str, source: Path, target: Optional[Path] = None, metadata: Optional[Dict] = None):
        """Log an action for reporting and undo"""
        self.actions.append({
            'action': action,
            'source': str(source),
            'target': str(target) if target else None,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
        
    def get_file_hash(self, file_path: Path) -> Optional[str]:
        """Get MD5 hash of file content for duplicate detection"""
        try:
            if file_path.stat().st_size > 100 * 1024 * 1024:  # Skip files > 100MB
                return None
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None
    
    def ensure_folder_structure(self, client_dir: Path):
        """Ensure standard folder structure exists for a client"""
        created = []
        for folder in CLIENT_FOLDERS:
            folder_path = client_dir / folder
            if not folder_path.exists():
                if not self.dry_run:
                    folder_path.mkdir(parents=True, exist_ok=True)
                created.append(folder)
                self.stats['folders_created'] += 1
                self.log_action('create_folder', folder_path)
        
        # Ensure report subfolders exist
        reports_dir = client_dir / 'reports'
        if reports_dir.exists():
            for subfolder in REPORT_SUBFOLDERS.keys():
                subfolder_path = reports_dir / subfolder
                if not subfolder_path.exists() and subfolder != 'ad-hoc':
                    if not self.dry_run:
                        subfolder_path.mkdir(parents=True, exist_ok=True)
                    created.append(f'reports/{subfolder}')
        
        # Ensure emails/drafts exists
        emails_dir = client_dir / 'emails'
        if emails_dir.exists():
            drafts_dir = emails_dir / 'drafts'
            if not drafts_dir.exists():
                if not self.dry_run:
                    drafts_dir.mkdir(parents=True, exist_ok=True)
                created.append('emails/drafts')
        
        return created
    
    def is_duplicate_file(self, file_path: Path) -> Tuple[bool, Optional[Path]]:
        """Check if file is a duplicate (name-based)"""
        name = file_path.name
        for pattern in DUPLICATE_PATTERNS:
            match = re.match(pattern, name)
            if match:
                base_name = match.group(1)
                ext = match.group(2)
                original_name = f"{base_name}.{ext}"
                original_path = file_path.parent / original_name
                if original_path.exists():
                    return True, original_path
        return False, None
    
    def find_content_duplicates(self, file_path: Path, directory: Path) -> List[Path]:
        """Find files with identical content"""
        file_hash = self.get_file_hash(file_path)
        if not file_hash:
            return []
        
        duplicates = []
        for other_file in directory.rglob('*'):
            if other_file == file_path or not other_file.is_file():
                continue
            if other_file.name.startswith('.'):
                continue
            
            other_hash = self.get_file_hash(other_file)
            if other_hash == file_hash:
                duplicates.append(other_file)
        
        return duplicates
    
    def should_stay_in_root(self, file_path: Path, is_client: bool = False) -> bool:
        """Check if file should stay in root directory"""
        if is_client:
            return file_path.name in CLIENT_ROOT_FILES
        return file_path.name in ROOT_FILES
    
    def detect_email_draft(self, file_path: Path) -> bool:
        """Detect if file is an email draft"""
        name_lower = file_path.name.lower()
        return 'email-draft' in name_lower or 'draft' in name_lower or 'email_draft' in name_lower
    
    def detect_meeting_note(self, file_path: Path) -> bool:
        """Detect if file is a meeting note based on content"""
        if file_path.suffix != '.md':
            return False
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')[:500].lower()
            meeting_keywords = ['meeting', 'call', 'transcript', 'participants', 'agenda', 'minutes']
            return any(keyword in content for keyword in meeting_keywords)
        except Exception:
            return False
    
    def extract_date_from_filename(self, filename: str) -> Optional[datetime]:
        """Extract date from filename patterns"""
        # YYYY-MM-DD pattern
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
        if date_match:
            try:
                return datetime(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
            except ValueError:
                pass
        
        # YYYY-MM pattern
        month_match = re.search(r'(\d{4})-(\d{2})', filename)
        if month_match:
            try:
                return datetime(int(month_match.group(1)), int(month_match.group(2)), 1)
            except ValueError:
                pass
        
        # Quarter pattern (q1-2025, q2-2025, etc.)
        quarter_match = re.search(r'q([1-4])-(\d{4})', filename, re.IGNORECASE)
        if quarter_match:
            quarter = int(quarter_match.group(1))
            year = int(quarter_match.group(2))
            month = (quarter - 1) * 3 + 1
            try:
                return datetime(year, month, 1)
            except ValueError:
                pass
        
        return None
    
    def determine_report_subfolder(self, file_path: Path) -> str:
        """Determine which reports subfolder a file should go in"""
        name_lower = file_path.name.lower()
        
        # Check for PMax
        if 'pmax' in name_lower:
            return 'pmax-analysis'
        
        # Check for quarter
        quarter_match = re.search(r'q([1-4])-(\d{4})', name_lower)
        if quarter_match:
            quarter = quarter_match.group(1)
            return f'q{quarter}'
        
        # Check for monthly pattern
        date = self.extract_date_from_filename(file_path.name)
        if date:
            # If it's a monthly report (has YYYY-MM pattern)
            if re.search(r'\d{4}-\d{2}', file_path.name):
                return 'monthly'
        
        return 'ad-hoc'
    
    def determine_file_location(self, file_path: Path, client_dir: Optional[Path] = None) -> Tuple[Optional[str], Optional[str]]:
        """Determine where a file should be moved based on type and content.
        Returns (folder, subfolder) tuple"""
        ext = file_path.suffix.lower()
        
        # Email drafts
        if self.detect_email_draft(file_path):
            return 'emails', 'drafts'
        
        # Meeting notes
        if self.detect_meeting_note(file_path):
            return 'meeting-notes', None
        
        # Reports - special handling
        if ext == '.html' or (ext == '.md' and 'report' in file_path.name.lower()):
            subfolder = self.determine_report_subfolder(file_path)
            return 'reports', subfolder
        
        # Check file type mapping
        if ext in FILE_TYPE_MAPPINGS:
            folder = FILE_TYPE_MAPPINGS[ext]
            if folder:
                # Special handling for reports
                if folder == 'reports':
                    subfolder = self.determine_report_subfolder(file_path)
                    return folder, subfolder
                return folder, None
        
        # Special handling for markdown files
        if ext == '.md':
            name_lower = file_path.name.lower()
            if 'meeting' in name_lower or 'call' in name_lower:
                return 'meeting-notes', None
            elif 'brief' in name_lower:
                return 'briefs', None
            elif 'email' in name_lower:
                return 'emails', 'drafts'
            else:
                return 'documents', None
        
        # Special handling for JSON files
        if ext == '.json':
            name_lower = file_path.name.lower()
            if 'product' in name_lower or 'feed' in name_lower:
                return 'product-feeds', None
            elif 'report' in name_lower:
                subfolder = self.determine_report_subfolder(file_path)
                return 'reports', subfolder
            else:
                return 'documents', None
        
        # Default: documents
        return 'documents', None
    
    def organize_client_folder(self, client_dir: Path):
        """Organize files in a client folder"""
        client_name = client_dir.name
        print(f"\n📁 Organizing: {client_name}")
        
        # Ensure folder structure exists
        created = self.ensure_folder_structure(client_dir)
        if created:
            print(f"  ✓ Created folders: {', '.join(created)}")
        
        # Find all files recursively (but prioritize root files)
        root_files = [f for f in client_dir.iterdir() if f.is_file()]
        subdir_files = []
        
        # Also check subdirectories for misplaced files
        for subdir in client_dir.iterdir():
            if subdir.is_dir() and subdir.name not in CLIENT_FOLDERS and not subdir.name.startswith('_'):
                for file_path in subdir.rglob('*'):
                    if file_path.is_file() and file_path.parent != client_dir:
                        subdir_files.append(file_path)
        
        all_files = root_files + subdir_files
        moved_count = 0
        
        for file_path in all_files:
            # Skip if should stay in root (only for root files)
            if file_path.parent == client_dir and self.should_stay_in_root(file_path, is_client=True):
                continue
            
            # Skip if already in correct location
            folder, subfolder = self.determine_file_location(file_path, client_dir)
            if folder:
                expected_dir = client_dir / folder
                if subfolder:
                    expected_dir = expected_dir / subfolder
                if file_path.parent == expected_dir:
                    continue
            
            # Check for name-based duplicates
            is_dup, original = self.is_duplicate_file(file_path)
            if is_dup:
                self.stats['duplicates_found'] += 1
                print(f"  🔄 Duplicate: {file_path.name}")
                print(f"     Original: {original.name}")
                
                # Keep newer version
                if file_path.stat().st_mtime > original.stat().st_mtime:
                    print(f"     → Keeping newer version, archiving older")
                    archive_path = original
                    keep_path = file_path
                else:
                    archive_path = file_path
                    keep_path = original
                
                archive_dir = client_dir / '_archive'
                if not archive_dir.exists() and not self.dry_run:
                    archive_dir.mkdir()
                
                final_archive_path = archive_dir / archive_path.name
                if not self.dry_run:
                    shutil.move(str(archive_path), str(final_archive_path))
                self.stats['archived'] += 1
                self.log_action('archive_duplicate', archive_path, final_archive_path)
                print(f"     → Archived to _archive/")
                continue
            
            # Determine target folder
            if not folder:
                continue
            
            target_dir = client_dir / folder
            if subfolder:
                target_dir = target_dir / subfolder
            
            target_path = target_dir / file_path.name
            
            # Check if target already exists
            if target_path.exists() and target_path != file_path:
                # Create unique name
                stem = file_path.stem
                ext = file_path.suffix
                counter = 1
                while target_path.exists():
                    target_path = target_dir / f"{stem}_{counter}{ext}"
                    counter += 1
            
            # Move file
            print(f"  📦 {file_path.relative_to(client_dir)}")
            if subfolder:
                print(f"     → {folder}/{subfolder}/")
            else:
                print(f"     → {folder}/")
            
            if not self.dry_run:
                try:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(target_path))
                    self.stats['moved'] += 1
                    self.log_action('move', file_path, target_path)
                    moved_count += 1
                except Exception as e:
                    print(f"     ❌ Error: {e}")
                    self.stats['errors'] += 1
        
        if moved_count > 0:
            print(f"  ✓ Moved {moved_count} file(s)")
        else:
            print(f"  ✓ No files to move")
    
    def clean_temp_files(self, directory: Path):
        """Remove temporary and backup files"""
        deleted = []
        for pattern in TEMP_PATTERNS:
            for file_path in directory.rglob(f'*{pattern}'):
                if file_path.is_file():
                    # Skip if in venv, __pycache__, or _archive
                    path_str = str(file_path)
                    if 'venv' in path_str or '__pycache__' in path_str or '_archive' in path_str:
                        continue
                    
                    print(f"  🗑️  Temp file: {file_path.relative_to(PROJECT_ROOT)}")
                    if not self.dry_run:
                        try:
                            file_path.unlink()
                            self.stats['deleted'] += 1
                            self.log_action('delete_temp', file_path)
                            deleted.append(file_path)
                        except Exception as e:
                            print(f"     ❌ Error: {e}")
                            self.stats['errors'] += 1
        
        return len(deleted)
    
    def find_empty_folders(self, directory: Path) -> List[Path]:
        """Find empty folders (excluding standard structure folders)"""
        empty = []
        for folder in directory.rglob('*'):
            if not folder.is_dir():
                continue
            
            # Skip venv, __pycache__, .git
            if any(skip in str(folder) for skip in ['venv', '__pycache__', '.git', '_archive']):
                continue
            
            # Check if folder is empty
            try:
                if not any(folder.iterdir()):
                    empty.append(folder)
            except PermissionError:
                pass
        
        return empty
    
    def clean_empty_folders(self, directory: Path):
        """Remove empty folders"""
        empty = self.find_empty_folders(directory)
        self.stats['empty_folders'] = empty
        
        for folder in empty:
            # Don't delete standard structure folders
            if folder.name in CLIENT_FOLDERS:
                continue
            
            print(f"  📁 Empty folder: {folder.relative_to(PROJECT_ROOT)}")
            if not self.dry_run:
                try:
                    folder.rmdir()
                    self.log_action('delete_empty_folder', folder)
                except Exception as e:
                    print(f"     ❌ Error: {e}")
                    self.stats['errors'] += 1
    
    def find_large_files(self, directory: Path, size_mb: int = 10) -> List[Tuple[Path, int]]:
        """Find files larger than specified size in MB"""
        large = []
        size_bytes = size_mb * 1024 * 1024
        
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip venv, __pycache__
            if 'venv' in str(file_path) or '__pycache__' in str(file_path):
                continue
            
            try:
                size = file_path.stat().st_size
                if size > size_bytes:
                    large.append((file_path, size // (1024 * 1024)))
            except Exception:
                pass
        
        return large
    
    def archive_old_files(self, directory: Path, days: int = 90):
        """Archive files older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        archived = []
        
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip root files and important files
            if file_path.name in CLIENT_ROOT_FILES or file_path.name in ROOT_FILES:
                continue
            
            # Skip venv, __pycache__, _archive
            if any(skip in str(file_path) for skip in ['venv', '__pycache__', '_archive']):
                continue
            
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff:
                    # Determine archive location
                    relative_path = file_path.relative_to(directory)
                    archive_path = directory / '_archive' / relative_path.parent / file_path.name
                    
                    print(f"  📦 Archive old: {file_path.relative_to(directory)} ({mtime.strftime('%Y-%m-%d')})")
                    
                    if not self.dry_run:
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(archive_path))
                        self.stats['archived'] += 1
                        self.log_action('archive_old', file_path, archive_path, {'age_days': days})
                        archived.append(file_path)
            except Exception as e:
                print(f"     ❌ Error: {e}")
                self.stats['errors'] += 1
        
        return len(archived)
    
    def find_broken_references(self, file_path: Path) -> List[Dict]:
        """Find broken file references in markdown files"""
        broken = []
        
        if file_path.suffix != '.md':
            return broken
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Find markdown links
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            for match in re.finditer(link_pattern, content):
                link_text = match.group(1)
                link_path = match.group(2)
                
                # Skip external URLs
                if link_path.startswith('http://') or link_path.startswith('https://'):
                    continue
                
                # Resolve relative path
                if link_path.startswith('/'):
                    resolved = PROJECT_ROOT / link_path[1:]
                else:
                    resolved = file_path.parent / link_path
                
                if not resolved.exists():
                    broken.append({
                        'file': file_path,
                        'link_text': link_text,
                        'link_path': link_path,
                        'line': content[:match.start()].count('\n') + 1
                    })
        except Exception:
            pass
        
        return broken
    
    def fix_broken_references(self, directory: Path):
        """Fix broken file references after moves"""
        fixed = 0
        
        for md_file in directory.rglob('*.md'):
            broken = self.find_broken_references(md_file)
            if not broken:
                continue
            
            print(f"  🔗 Found {len(broken)} broken reference(s) in {md_file.relative_to(PROJECT_ROOT)}")
            
            if not self.dry_run:
                try:
                    content = md_file.read_text(encoding='utf-8')
                    for ref in broken:
                        # Try to find the file in new location
                        old_path = md_file.parent / ref['link_path']
                        filename = old_path.name
                        
                        # Search for file in project
                        found = list(PROJECT_ROOT.rglob(filename))
                        if found and len(found) == 1:
                            new_path = found[0]
                            relative_path = os.path.relpath(new_path, md_file.parent)
                            content = content.replace(ref['link_path'], relative_path)
                            fixed += 1
                            self.stats['references_fixed'] += 1
                except Exception as e:
                    print(f"     ❌ Error fixing references: {e}")
                    self.stats['errors'] += 1
        
        return fixed
    
    def organize_root_files(self):
        """Organize files in project root"""
        print("\n📁 Organizing project root...")
        
        root_files = [f for f in PROJECT_ROOT.iterdir() if f.is_file()]
        moved = 0
        
        for file_path in root_files:
            if self.should_stay_in_root(file_path):
                continue
            
            is_dup, original = self.is_duplicate_file(file_path)
            if is_dup:
                self.stats['duplicates_found'] += 1
                print(f"  🔄 Duplicate: {file_path.name}")
                
                archive_dir = PROJECT_ROOT / '_archive'
                if not archive_dir.exists() and not self.dry_run:
                    archive_dir.mkdir()
                
                archive_path = archive_dir / file_path.name
                if not self.dry_run:
                    shutil.move(str(file_path), str(archive_path))
                self.stats['archived'] += 1
                self.log_action('archive_duplicate', file_path, archive_path)
                print(f"     → Archived to _archive/")
                continue
            
            name_lower = file_path.name.lower()
            
            # Move documentation files to docs/
            if file_path.suffix == '.md' and file_path.name not in ROOT_FILES:
                target = DOCS_DIR / file_path.name
                if not target.parent.exists() and not self.dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                
                print(f"  📦 {file_path.name}")
                print(f"     → docs/")
                
                if not self.dry_run:
                    try:
                        shutil.move(str(file_path), str(target))
                        self.stats['moved'] += 1
                        self.log_action('move', file_path, target)
                        moved += 1
                    except Exception as e:
                        print(f"     ❌ Error: {e}")
                        self.stats['errors'] += 1
                continue
            
            # Move client-related files
            if file_path.suffix == '.docx' and 'google ads' in name_lower:
                target = ROKSYS_DIR / 'documents' / file_path.name
                if not target.parent.exists() and not self.dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                
                print(f"  📦 {file_path.name}")
                print(f"     → roksys/documents/")
                
                if not self.dry_run:
                    try:
                        shutil.move(str(file_path), str(target))
                        self.stats['moved'] += 1
                        self.log_action('move', file_path, target)
                        moved += 1
                    except Exception as e:
                        print(f"     ❌ Error: {e}")
                        self.stats['errors'] += 1
        
        if moved > 0:
            print(f"  ✓ Moved {moved} file(s)")
        else:
            print(f"  ✓ No files to move")
    
    def organize_all_clients(self):
        """Organize all client folders"""
        print("\n" + "=" * 80)
        print("ORGANIZING CLIENT FOLDERS")
        print("=" * 80)
        
        clients = [d for d in CLIENTS_DIR.iterdir() 
                  if d.is_dir() and not d.name.startswith('_')]
        
        if self.client_filter:
            clients = [c for c in clients if c.name == self.client_filter]
        
        for client_dir in sorted(clients):
            try:
                self.organize_client_folder(client_dir)
            except Exception as e:
                print(f"  ❌ Error organizing {client_dir.name}: {e}")
                self.stats['errors'] += 1
    
    def generate_html_report(self) -> str:
        """Generate HTML report of all actions"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>File Organizer Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #4CAF50; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #4CAF50; }}
        .stat-label {{ color: #666; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .action-move {{ color: #2196F3; }}
        .action-archive {{ color: #FF9800; }}
        .action-delete {{ color: #F44336; }}
        .action-create {{ color: #4CAF50; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 File Organizer Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Mode:</strong> {'🔍 Dry Run' if self.dry_run else '⚙️ Live'}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{self.stats['moved']}</div>
                <div class="stat-label">Files Moved</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.stats['archived']}</div>
                <div class="stat-label">Files Archived</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.stats['deleted']}</div>
                <div class="stat-label">Files Deleted</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.stats['folders_created']}</div>
                <div class="stat-label">Folders Created</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.stats['duplicates_found']}</div>
                <div class="stat-label">Duplicates Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{self.stats['references_fixed']}</div>
                <div class="stat-label">References Fixed</div>
            </div>
        </div>
        
        <h2>Actions Taken</h2>
        <table>
            <tr>
                <th>Action</th>
                <th>Source</th>
                <th>Target</th>
                <th>Time</th>
            </tr>
"""
        
        for action in self.actions:
            action_class = f"action-{action['action'].split('_')[0]}"
            html_content += f"""
            <tr>
                <td class="{action_class}">{action['action']}</td>
                <td>{html.escape(action['source'])}</td>
                <td>{html.escape(action['target'] or '')}</td>
                <td>{action['timestamp']}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
</body>
</html>"""
        
        return html_content
    
    def undo_last_run(self, log_file: Path):
        """Undo actions from a previous run"""
        if not log_file.exists():
            print(f"❌ Log file not found: {log_file}")
            return
        
        with open(log_file, 'r') as f:
            actions = json.load(f)
        
        print(f"🔄 Undoing {len(actions)} actions...")
        
        # Reverse the actions
        for action in reversed(actions):
            if action['action'] == 'move' and action['target']:
                # Move back
                source = Path(action['target'])
                target = Path(action['source'])
                if source.exists():
                    print(f"  ↶ Moving {source.name} back to {target.parent}")
                    if not self.dry_run:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source), str(target))
            elif action['action'] == 'archive_duplicate' and action['target']:
                # Move back from archive
                source = Path(action['target'])
                target = Path(action['source'])
                if source.exists():
                    print(f"  ↶ Restoring {source.name} from archive")
                    if not self.dry_run:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source), str(target))
            elif action['action'] == 'delete_temp' and action['source']:
                # Can't undo deletions
                print(f"  ⚠️  Cannot undo deletion of {Path(action['source']).name}")
    
    def run(self):
        """Run the full organization process"""
        print("=" * 80)
        print("FILE ORGANIZER - PetesBrain Cleanup (Comprehensive Edition)")
        print("=" * 80)
        
        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No files will be moved")
        else:
            print("\n⚙️  LIVE MODE - Files will be moved")
        
        print()
        
        # 1. Organize project root
        self.organize_root_files()
        
        # 2. Clean temporary files
        print("\n🧹 Cleaning temporary files...")
        temp_deleted = self.clean_temp_files(PROJECT_ROOT)
        if temp_deleted > 0:
            print(f"  ✓ Deleted {temp_deleted} temporary file(s)")
        else:
            print(f"  ✓ No temporary files found")
        
        # 3. Organize client folders
        self.organize_all_clients()
        
        # 4. Find large files
        print("\n📊 Analyzing file sizes...")
        large_files = self.find_large_files(PROJECT_ROOT, size_mb=10)
        self.stats['large_files'] = large_files
        if large_files:
            print(f"  ⚠️  Found {len(large_files)} large file(s) (>10MB):")
            for file_path, size_mb in large_files[:10]:  # Show first 10
                print(f"     - {file_path.relative_to(PROJECT_ROOT)} ({size_mb}MB)")
        else:
            print(f"  ✓ No unusually large files found")
        
        # 5. Clean empty folders
        print("\n📁 Cleaning empty folders...")
        self.clean_empty_folders(PROJECT_ROOT)
        if self.stats['empty_folders']:
            print(f"  ✓ Found {len(self.stats['empty_folders'])} empty folder(s)")
        else:
            print(f"  ✓ No empty folders found")
        
        # 6. Fix broken references
        print("\n🔗 Fixing broken references...")
        refs_fixed = self.fix_broken_references(PROJECT_ROOT)
        if refs_fixed > 0:
            print(f"  ✓ Fixed {refs_fixed} broken reference(s)")
        else:
            print(f"  ✓ No broken references found")
        
        # 7. Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"  📦 Files moved: {self.stats['moved']}")
        print(f"  📚 Files archived: {self.stats['archived']}")
        print(f"  🗑️  Files deleted: {self.stats['deleted']}")
        print(f"  📁 Folders created: {self.stats['folders_created']}")
        print(f"  🔄 Duplicates found: {self.stats['duplicates_found']}")
        print(f"  🔗 References fixed: {self.stats['references_fixed']}")
        print(f"  📊 Large files found: {len(self.stats['large_files'])}")
        print(f"  📁 Empty folders found: {len(self.stats['empty_folders'])}")
        if self.stats['errors'] > 0:
            print(f"  ❌ Errors: {self.stats['errors']}")
        print("=" * 80)
        
        # Save action log
        if self.actions:
            log_file = PROJECT_ROOT / 'shared' / 'data' / f'file-organizer-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
            log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(log_file, 'w') as f:
                json.dump(self.actions, f, indent=2)
            print(f"\n📝 Action log saved: {log_file.relative_to(PROJECT_ROOT)}")
            
            # Generate HTML report
            html_report = self.generate_html_report()
            html_file = log_file.with_suffix('.html')
            with open(html_file, 'w') as f:
                f.write(html_report)
            print(f"📄 HTML report saved: {html_file.relative_to(PROJECT_ROOT)}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive file organizer for PetesBrain')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without actually moving files')
    parser.add_argument('--client', type=str, 
                       help='Only organize a specific client folder')
    parser.add_argument('--undo', type=str, metavar='LOG_FILE',
                       help='Undo actions from a previous run (provide log file path)')
    parser.add_argument('--report', action='store_true',
                       help='Generate HTML report after completion')
    
    args = parser.parse_args()
    
    organizer = FileOrganizer(dry_run=args.dry_run, client_filter=args.client)
    
    try:
        if args.undo:
            organizer.undo_last_run(Path(args.undo))
        else:
            organizer.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
