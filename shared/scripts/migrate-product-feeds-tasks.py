#!/usr/bin/env python3
"""
Migrate Product-Feeds Tasks to Correct Locations

Based on audit results, migrates tasks from product-feeds/tasks*.json
to correct locations (clients/{client}/tasks.json or roksys/tasks.json).

Handles:
- Duplicate detection (skip tasks that already exist in correct location)
- Roksys special case (roksys/tasks.json, not clients/roksys/)
- Backup creation before migration
- Migration report generation
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / 'clients'
ROKSYS_DIR = PROJECT_ROOT / 'roksys'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'state'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_audit_report(audit_file: Path) -> Dict[str, Any]:
    """Load the most recent audit report"""
    if not audit_file.exists():
        # Try to find the most recent audit file
        audit_files = sorted(OUTPUT_DIR.glob('product-feeds-audit-*.json'), reverse=True)
        if audit_files:
            audit_file = audit_files[0]
            print(f"📄 Using audit report: {audit_file.name}")
        else:
            raise FileNotFoundError("No audit report found. Run audit-product-feeds-tasks.py first.")
    
    with open(audit_file, 'r') as f:
        return json.load(f)


def get_correct_task_file(client: str) -> Path:
    """Get the correct location for a client's tasks"""
    if client == 'roksys':
        return ROKSYS_DIR / 'tasks.json'
    else:
        return CLIENTS_DIR / client / 'tasks.json'


def load_tasks_from_file(task_file: Path) -> Dict[str, Any]:
    """Load tasks from a JSON file"""
    if not task_file.exists():
        return {'tasks': [], 'last_updated': datetime.now().isoformat()}
    
    try:
        with open(task_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"⚠️  Error reading {task_file}: {e}")
        return {'tasks': [], 'last_updated': datetime.now().isoformat()}


def save_tasks_to_file(task_file: Path, data: Dict[str, Any]):
    """Save tasks to a JSON file"""
    task_file.parent.mkdir(parents=True, exist_ok=True)
    data['last_updated'] = datetime.now().isoformat()
    
    with open(task_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def create_backup(task_file: Path, backup_dir: Path):
    """Create backup of a task file"""
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"{task_file.name}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(task_file, backup_file)
    return backup_file


def migrate_tasks(dry_run: bool = True) -> Dict[str, Any]:
    """Migrate tasks from product-feeds to correct locations"""
    # Find most recent audit report
    audit_files = sorted(OUTPUT_DIR.glob('product-feeds-audit-*.json'), reverse=True)
    if not audit_files:
        print("❌ No audit report found. Run audit-product-feeds-tasks.py first.")
        sys.exit(1)
    
    audit_report = load_audit_report(audit_files[0])
    
    print(f"\n{'='*80}")
    print(f"MIGRATING PRODUCT-FEEDS TASKS ({'DRY RUN' if dry_run else 'LIVE'})")
    print(f"{'='*80}\n")
    print(f"Found {len(audit_report['product_feeds_files'])} product-feeds task files")
    print(f"Total tasks: {audit_report['summary']['total_tasks_in_pf']}")
    print(f"Duplicates: {audit_report['summary']['total_duplicates']}\n")
    
    migration_results = {
        'timestamp': datetime.now().isoformat(),
        'dry_run': dry_run,
        'files_processed': 0,
        'tasks_migrated': 0,
        'tasks_skipped_duplicates': 0,
        'tasks_skipped_errors': 0,
        'backups_created': [],
        'migrations': []
    }
    
    # Create backup directory
    backup_dir = OUTPUT_DIR / f"product-feeds-migration-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    if not dry_run:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"📦 Backup directory: {backup_dir}\n")
    
    # Process each product-feeds file
    for pf_file_info in audit_report['product_feeds_files']:
        client = pf_file_info['client']
        pf_file_path = Path(pf_file_info['path'])
        pf_analysis = pf_file_info['analysis']
        correct_analysis = pf_file_info['correct_location']
        
        print(f"📁 Processing: {pf_file_info['relative_path']}")
        print(f"   Client: {client}")
        print(f"   Tasks in PF: {pf_analysis.get('total_tasks', 0)}")
        print(f"   Duplicates: {pf_file_info['duplicate_count']}")
        
        # Get correct location
        correct_task_file = get_correct_task_file(client)
        correct_tasks_data = load_tasks_from_file(correct_task_file)
        correct_task_ids = {t.get('id') for t in correct_tasks_data.get('tasks', [])}
        
        # Process tasks from product-feeds
        tasks_to_migrate = []
        skipped_duplicates = []
        skipped_errors = []
        
        for task in pf_analysis.get('tasks', []):
            task_id = task.get('id')
            if not task_id:
                skipped_errors.append({'task': task.get('title', 'Unknown'), 'reason': 'No task ID'})
                continue
            
            if task_id in correct_task_ids:
                skipped_duplicates.append({'task_id': task_id, 'title': task.get('title', '')})
            else:
                tasks_to_migrate.append(task)
        
        print(f"   ✅ To migrate: {len(tasks_to_migrate)}")
        print(f"   ⏭️  Skipped (duplicates): {len(skipped_duplicates)}")
        if skipped_errors:
            print(f"   ❌ Skipped (errors): {len(skipped_errors)}")
        
        # Migrate tasks
        if tasks_to_migrate:
            if not dry_run:
                # Create backup of correct location file
                if correct_task_file.exists():
                    backup_file = create_backup(correct_task_file, backup_dir)
                    migration_results['backups_created'].append(str(backup_file))
                    print(f"   💾 Backup created: {backup_file.name}")
                
                # Add tasks to correct location
                correct_tasks_data['tasks'].extend(tasks_to_migrate)
                save_tasks_to_file(correct_task_file, correct_tasks_data)
                print(f"   ✅ Migrated {len(tasks_to_migrate)} task(s) to {correct_task_file.relative_to(PROJECT_ROOT)}")
            else:
                print(f"   [DRY RUN] Would migrate {len(tasks_to_migrate)} task(s) to {correct_task_file.relative_to(PROJECT_ROOT)}")
        
        migration_results['migrations'].append({
            'client': client,
            'pf_file': pf_file_info['relative_path'],
            'tasks_migrated': len(tasks_to_migrate),
            'tasks_skipped_duplicates': len(skipped_duplicates),
            'tasks_skipped_errors': len(skipped_errors),
            'correct_location': str(correct_task_file.relative_to(PROJECT_ROOT))
        })
        
        migration_results['tasks_migrated'] += len(tasks_to_migrate)
        migration_results['tasks_skipped_duplicates'] += len(skipped_duplicates)
        migration_results['tasks_skipped_errors'] += len(skipped_errors)
        migration_results['files_processed'] += 1
        
        print()
    
    # Save migration report
    report_file = OUTPUT_DIR / f'product-feeds-migration-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    with open(report_file, 'w') as f:
        json.dump(migration_results, f, indent=2, default=str)
    
    print(f"{'='*80}")
    print(f"MIGRATION SUMMARY")
    print(f"{'='*80}\n")
    print(f"Files processed: {migration_results['files_processed']}")
    print(f"Tasks migrated: {migration_results['tasks_migrated']}")
    print(f"Tasks skipped (duplicates): {migration_results['tasks_skipped_duplicates']}")
    print(f"Tasks skipped (errors): {migration_results['tasks_skipped_errors']}")
    print(f"Backups created: {len(migration_results['backups_created'])}")
    print(f"\n📄 Report saved to: {report_file.relative_to(PROJECT_ROOT)}")
    
    if not dry_run:
        print(f"\n📦 Backups in: {backup_dir.relative_to(PROJECT_ROOT)}")
        print(f"\n⚠️  NEXT STEP: Delete product-feeds task files after verifying migration")
        print(f"   Command: find clients -path '*/product-feeds/tasks*.json' ! -path '*/_archived*' -delete")
    
    return migration_results


def main():
    """Main migration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate product-feeds tasks to correct locations')
    parser.add_argument('--live', action='store_true', help='Perform actual migration (default is dry-run)')
    args = parser.parse_args()
    
    dry_run = not args.live
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")
    else:
        print("⚠️  LIVE MODE - Files will be modified\n")
        response = input("Continue with live migration? (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled.")
            sys.exit(0)
    
    try:
        results = migrate_tasks(dry_run=dry_run)
        
        if dry_run:
            print("\n✅ Dry run complete. Run with --live to perform actual migration.")
            return 0
        else:
            print("\n✅ Migration complete!")
            return 0
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())


