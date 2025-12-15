#!/usr/bin/env python3
"""
Comprehensive Audit of Product-Feeds Task Files

Scans for ALL product-feeds/tasks*.json files and analyzes:
- File locations and metadata
- Task contents and counts
- Duplicate detection (tasks that exist in both locations)
- Code references to product-feeds
- Last modified dates

Output: JSON report + human-readable summary
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / 'clients'
ROKSYS_DIR = PROJECT_ROOT / 'roksys'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'state'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_all_product_feeds_task_files() -> List[Dict[str, Any]]:
    """Find all product-feeds/tasks*.json files"""
    files_found = []
    
    # Scan clients directory
    if CLIENTS_DIR.exists():
        for client_dir in CLIENTS_DIR.iterdir():
            if not client_dir.is_dir() or client_dir.name.startswith('_'):
                continue
            
            # Check for product-feeds/tasks*.json
            pf_dir = client_dir / 'product-feeds'
            if pf_dir.exists() and pf_dir.is_dir():
                for task_file in pf_dir.glob('tasks*.json'):
                    files_found.append({
                        'client': client_dir.name,
                        'path': str(task_file),
                        'relative_path': str(task_file.relative_to(PROJECT_ROOT)),
                        'file_name': task_file.name,
                        'size_bytes': task_file.stat().st_size,
                        'modified': datetime.fromtimestamp(task_file.stat().st_mtime).isoformat(),
                        'exists': True
                    })
    
    # Scan roksys directory (if it has product-feeds)
    if ROKSYS_DIR.exists():
        pf_dir = ROKSYS_DIR / 'product-feeds'
        if pf_dir.exists() and pf_dir.is_dir():
            for task_file in pf_dir.glob('tasks*.json'):
                files_found.append({
                    'client': 'roksys',
                    'path': str(task_file),
                    'relative_path': str(task_file.relative_to(PROJECT_ROOT)),
                    'file_name': task_file.name,
                    'size_bytes': task_file.stat().st_size,
                    'modified': datetime.fromtimestamp(task_file.stat().st_mtime).isoformat(),
                    'exists': True
                })
    
    return files_found


def analyze_task_file(file_path: Path) -> Dict[str, Any]:
    """Analyze contents of a task file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        tasks = data.get('tasks', [])
        active_tasks = [t for t in tasks if t.get('status') == 'active']
        completed_tasks = [t for t in tasks if t.get('status') == 'completed']
        
        return {
            'total_tasks': len(tasks),
            'active_tasks': len(active_tasks),
            'completed_tasks': len(completed_tasks),
            'task_ids': [t.get('id') for t in tasks],
            'task_titles': [t.get('title', '') for t in tasks],
            'has_valid_structure': 'tasks' in data,
            'last_updated': data.get('last_updated'),
            'tasks': tasks  # Full task data for duplicate detection
        }
    except json.JSONDecodeError as e:
        return {
            'error': f'JSON decode error: {e}',
            'total_tasks': 0,
            'tasks': []
        }
    except Exception as e:
        return {
            'error': f'Error reading file: {e}',
            'total_tasks': 0,
            'tasks': []
        }


def find_correct_location_tasks(client: str) -> Dict[str, Any]:
    """Find tasks in the correct location for comparison"""
    if client == 'roksys':
        correct_file = ROKSYS_DIR / 'tasks.json'
    else:
        correct_file = CLIENTS_DIR / client / 'tasks.json'
    
    if not correct_file.exists():
        return {
            'exists': False,
            'tasks': [],
            'task_ids': []
        }
    
    return analyze_task_file(correct_file)


def detect_duplicates(pf_tasks: List[Dict], correct_tasks: Dict) -> List[Dict[str, Any]]:
    """Detect tasks that exist in both product-feeds and correct location"""
    duplicates = []
    correct_task_ids = set(correct_tasks.get('task_ids', []))
    
    for task in pf_tasks.get('tasks', []):
        task_id = task.get('id')
        if task_id and task_id in correct_task_ids:
            duplicates.append({
                'task_id': task_id,
                'title': task.get('title', ''),
                'location': 'Both product-feeds and correct location'
            })
    
    return duplicates


def find_code_references() -> List[Dict[str, Any]]:
    """Find all code references to product-feeds/tasks"""
    references = []
    
    # Search Python files
    for py_file in PROJECT_ROOT.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        try:
            content = py_file.read_text()
            
            # Check for product-feeds references
            if 'product-feeds' in content.lower() and 'tasks' in content.lower():
                lines = content.split('\n')
                matching_lines = []
                for i, line in enumerate(lines, 1):
                    if 'product-feeds' in line.lower() and 'tasks' in line.lower():
                        matching_lines.append({
                            'line_number': i,
                            'content': line.strip()
                        })
                
                if matching_lines:
                    references.append({
                        'file': str(py_file.relative_to(PROJECT_ROOT)),
                        'absolute_path': str(py_file),
                        'matches': matching_lines,
                        'match_count': len(matching_lines)
                    })
        except Exception:
            pass  # Skip files we can't read
    
    return references


def generate_report() -> Dict[str, Any]:
    """Generate comprehensive audit report"""
    print("🔍 Scanning for product-feeds task files...")
    pf_files = find_all_product_feeds_task_files()
    
    print(f"📊 Found {len(pf_files)} product-feeds task file(s)")
    
    print("📖 Analyzing task file contents...")
    analysis_results = []
    all_duplicates = []
    
    for pf_file_info in pf_files:
        file_path = Path(pf_file_info['path'])
        client = pf_file_info['client']
        
        print(f"   Analyzing: {pf_file_info['relative_path']}")
        
        pf_analysis = analyze_task_file(file_path)
        correct_analysis = find_correct_location_tasks(client)
        
        duplicates = detect_duplicates(pf_analysis, correct_analysis)
        
        analysis_results.append({
            **pf_file_info,
            'analysis': pf_analysis,
            'correct_location': correct_analysis,
            'duplicates': duplicates,
            'duplicate_count': len(duplicates)
        })
        
        all_duplicates.extend(duplicates)
    
    print("🔎 Searching for code references...")
    code_refs = find_code_references()
    
    print(f"📝 Found {len(code_refs)} file(s) with product-feeds/tasks references")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_pf_files': len(pf_files),
            'total_tasks_in_pf': sum(a['analysis'].get('total_tasks', 0) for a in analysis_results),
            'total_duplicates': len(all_duplicates),
            'code_references': len(code_refs)
        },
        'product_feeds_files': analysis_results,
        'duplicates': all_duplicates,
        'code_references': code_refs
    }
    
    return report


def print_summary(report: Dict[str, Any]):
    """Print human-readable summary"""
    print("\n" + "="*80)
    print("PRODUCT-FEEDS TASK FILES AUDIT REPORT")
    print("="*80)
    print(f"\nGenerated: {report['timestamp']}")
    
    summary = report['summary']
    print(f"\n📊 SUMMARY:")
    print(f"   Product-feeds task files found: {summary['total_pf_files']}")
    print(f"   Total tasks in product-feeds: {summary['total_tasks_in_pf']}")
    print(f"   Duplicate tasks (exist in both locations): {summary['total_duplicates']}")
    print(f"   Code files referencing product-feeds/tasks: {summary['code_references']}")
    
    if report['product_feeds_files']:
        print(f"\n📁 PRODUCT-FEEDS FILES:")
        for pf_file in report['product_feeds_files']:
            print(f"\n   Client: {pf_file['client']}")
            print(f"   File: {pf_file['relative_path']}")
            print(f"   Size: {pf_file['size_bytes']} bytes")
            print(f"   Modified: {pf_file['modified']}")
            analysis = pf_file['analysis']
            print(f"   Tasks: {analysis.get('total_tasks', 0)} total ({analysis.get('active_tasks', 0)} active, {analysis.get('completed_tasks', 0)} completed)")
            if pf_file['duplicate_count'] > 0:
                print(f"   ⚠️  {pf_file['duplicate_count']} duplicate(s) found in correct location")
            if 'error' in analysis:
                print(f"   ❌ Error: {analysis['error']}")
    
    if report['duplicates']:
        print(f"\n🔄 DUPLICATE TASKS:")
        for dup in report['duplicates']:
            print(f"   - {dup['title'][:60]}... (ID: {dup['task_id']})")
    
    if report['code_references']:
        print(f"\n💻 CODE REFERENCES:")
        for ref in report['code_references']:
            print(f"\n   File: {ref['file']}")
            print(f"   Matches: {ref['match_count']}")
            for match in ref['matches'][:3]:  # Show first 3 matches
                print(f"      Line {match['line_number']}: {match['content'][:70]}...")
            if ref['match_count'] > 3:
                print(f"      ... and {ref['match_count'] - 3} more")
    
    print("\n" + "="*80)


def main():
    """Main audit function"""
    report = generate_report()
    
    # Save JSON report
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    json_file = OUTPUT_DIR / f'product-feeds-audit-{timestamp}.json'
    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Report saved to: {json_file.relative_to(PROJECT_ROOT)}")
    
    # Print summary
    print_summary(report)
    
    # Return exit code
    if report['summary']['total_pf_files'] > 0:
        print("\n⚠️  WARNING: Product-feeds task files found!")
        return 1
    else:
        print("\n✅ No product-feeds task files found")
        return 0


if __name__ == '__main__':
    sys.exit(main())


