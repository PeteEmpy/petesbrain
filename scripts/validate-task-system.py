#!/usr/bin/env python3
"""
Task System Validation Script

Validates the PetesBrain task system structure and flags issues.
Run regularly to ensure consistency and catch problems early.

Usage:
    python3 scripts/validate-task-system.py

Exit codes:
    0 = All checks passed
    1 = Issues found (see output)
"""
import json
from pathlib import Path
from datetime import datetime

def validate_task_system():
    """Run all validation checks on the task system"""
    issues = []
    warnings = []
    clients_dir = Path('/Users/administrator/Documents/PetesBrain/clients')

    if not clients_dir.exists():
        print("❌ FATAL: clients/ directory not found")
        return 1

    print("="*70)
    print("TASK SYSTEM VALIDATION")
    print("="*70)
    print(f"Checking: {clients_dir}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    total_clients = 0
    clients_with_tasks = 0
    total_tasks = 0

    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        total_clients += 1
        client = client_dir.name

        # Check 1: Tasks in wrong location? (Critical)
        pf_tasks = client_dir / 'product-feeds' / 'tasks.json'
        if pf_tasks.exists():
            issues.append(f"❌ {client}: Has product-feeds/tasks.json (should be in root)")

        # Check 2: Has root tasks.json?
        root_tasks = client_dir / 'tasks.json'
        if root_tasks.exists():
            clients_with_tasks += 1

            # Check 3: Valid JSON?
            try:
                with open(root_tasks) as f:
                    data = json.load(f)

                # Check 4: Correct structure?
                if 'tasks' not in data:
                    issues.append(f"❌ {client}: tasks.json missing 'tasks' array")
                    continue

                if 'last_updated' not in data:
                    warnings.append(f"⚠️  {client}: tasks.json missing 'last_updated' field")

                tasks = data.get('tasks', [])
                total_tasks += len(tasks)

                # Check 5: Individual task structure
                for i, task in enumerate(tasks):
                    task_ref = f"Task {i+1}"

                    # Required fields
                    if 'id' not in task:
                        issues.append(f"❌ {client}: {task_ref} missing 'id'")

                    if 'title' not in task:
                        issues.append(f"❌ {client}: {task_ref} missing 'title'")

                    if 'status' not in task:
                        issues.append(f"❌ {client}: {task_ref} missing 'status'")
                    else:
                        # Check for completed tasks still in file
                        if task.get('status') == 'completed':
                            title = task.get('title', 'Unknown')[:50]
                            warnings.append(f"⚠️  {client}: Completed task still in tasks.json: {title}")

                    # Type validation
                    if 'type' in task:
                        task_type = task['type']
                        if task_type not in ['standalone', 'parent', 'child']:
                            issues.append(f"❌ {client}: {task_ref} has invalid type: {task_type}")

                        # Parent tasks should have children
                        if task_type == 'parent' and not task.get('children'):
                            warnings.append(f"⚠️  {client}: Parent task has no children: {task.get('title', 'Unknown')[:50]}")

                        # Child tasks should have parent_id
                        if task_type == 'child' and not task.get('parent_id'):
                            issues.append(f"❌ {client}: Child task missing parent_id: {task.get('title', 'Unknown')[:50]}")
                    else:
                        warnings.append(f"⚠️  {client}: {task_ref} missing 'type' field")

                    # Priority validation
                    if 'priority' in task:
                        priority = task['priority']
                        if priority not in ['P0', 'P1', 'P2', 'P3']:
                            issues.append(f"❌ {client}: {task_ref} has invalid priority: {priority}")
                    else:
                        warnings.append(f"⚠️  {client}: {task_ref} missing 'priority' field")

            except json.JSONDecodeError as e:
                issues.append(f"❌ {client}: Invalid JSON in tasks.json: {e}")
            except Exception as e:
                issues.append(f"❌ {client}: Error reading tasks.json: {e}")

        # Check 6: Has tasks-completed.md?
        completed_md = client_dir / 'tasks-completed.md'
        if not completed_md.exists():
            warnings.append(f"⚠️  {client}: Missing tasks-completed.md (create it)")

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Clients checked: {total_clients}")
    print(f"Clients with tasks: {clients_with_tasks}")
    print(f"Total tasks: {total_tasks}")
    print()

    # Print issues
    if issues:
        print("❌ CRITICAL ISSUES:")
        for issue in issues:
            print(f"   {issue}")
        print()

    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        print()

    # Final verdict
    if not issues and not warnings:
        print("✅ VALIDATION PASSED")
        print("   No issues or warnings found")
        print("   Task system is healthy")
        return 0
    elif issues:
        print(f"❌ VALIDATION FAILED")
        print(f"   Found {len(issues)} critical issue(s)")
        print(f"   Found {len(warnings)} warning(s)")
        print()
        print("ACTION REQUIRED: Fix critical issues immediately")
        print("See: /docs/TASK-SYSTEM-COMPLETE-GUIDE.md for troubleshooting")
        return 1
    else:
        print(f"⚠️  VALIDATION PASSED WITH WARNINGS")
        print(f"   Found {len(warnings)} warning(s)")
        print(f"   No critical issues")
        print()
        print("RECOMMENDED: Review warnings and fix when convenient")
        return 0

if __name__ == "__main__":
    try:
        exit_code = validate_task_system()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Validation interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
