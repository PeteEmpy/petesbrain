#!/usr/bin/env python3
"""
Complete Email Sync Workflow
1. Auto-label incoming and sent emails
2. Sync labeled emails to folders
3. Copy Google rep emails to knowledge base inbox
"""

import sys
import os
import subprocess
from pathlib import Path

# Get script directory
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.resolve()

# Set working directory explicitly
os.chdir(str(SCRIPT_DIR))

def run_command(cmd, description):
    """Run a command and return exit code."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}\n")
    
    # Ensure environment variables are set
    env = os.environ.copy()
    env['GOOGLE_APPLICATION_CREDENTIALS'] = str(SCRIPT_DIR / 'credentials.json')
    
    result = subprocess.run(
        cmd, 
        cwd=str(SCRIPT_DIR),
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    return result.returncode

def main():
    """Run complete email sync workflow."""
    import argparse

    parser = argparse.ArgumentParser(description='Complete Email Sync Workflow')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    args = parser.parse_args()

    # Build command arguments
    extra_args = ['--dry-run'] if args.dry_run else []

    print("="*60)
    print("Pete's Brain - Complete Email Sync Workflow")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    print("="*60)

    # Step 0: Validate Gmail OAuth scopes (critical - prevents recurring issue)
    exit_code = run_command(
        [str(SCRIPT_DIR / ".venv" / "bin" / "python3"),
         str(SCRIPT_DIR / "validate-scopes-on-startup.py")],
        "Step 0: Validating Gmail OAuth scopes..."
    )

    if exit_code != 0:
        print(f"\n❌ Scope validation failed - STOPPING")
        print("Fix the scope issues before continuing.")
        sys.exit(exit_code)

    # Step 1: Auto-label emails (inbox and sent)
    exit_code = run_command(
        [str(SCRIPT_DIR / ".venv" / "bin" / "python3"), 
         str(SCRIPT_DIR / "auto_label.py")] + extra_args,
        "Step 1: Auto-labeling emails..."
    )
    
    if exit_code != 0:
        print(f"\n❌ Auto-labeling failed with exit code {exit_code}")
        sys.exit(exit_code)
    
    # Step 2: Sync labeled emails
    exit_code = run_command(
        [str(SCRIPT_DIR / ".venv" / "bin" / "python3"), 
         str(SCRIPT_DIR / "sync_emails.py")] + extra_args,
        "Step 2: Syncing labeled emails..."
    )
    
    if exit_code != 0:
        print(f"\n❌ Email sync failed with exit code {exit_code}")
        sys.exit(exit_code)
    
    # Step 3: Copy Google rep emails to KB inbox (optional, don't fail if missing)
    copy_script = PROJECT_ROOT / "shared" / "scripts" / "copy-google-rep-emails-to-kb.py"
    if copy_script.exists():
        exit_code = run_command(
            [str(SCRIPT_DIR / ".venv" / "bin" / "python3"), 
             str(copy_script)],
            "Step 3: Copying Google rep emails to knowledge base..."
        )
        if exit_code != 0:
            print(f"\n⚠️  Google rep email copy failed (non-critical)")
    else:
        print(f"\n⚠️  Google rep email copy script not found (skipping)")
    
    print("\n" + "="*60)
    print("✅ Complete Email Sync Workflow Finished")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Workflow cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)

