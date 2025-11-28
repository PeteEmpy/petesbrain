#!/usr/bin/env python3
"""
Git Operations Agent (githuby)

Handles all git operations with mandatory fetch-first protocol and automatic
automation commit recognition. Based on Mike Rhodes' githuby pattern.

Usage:
    python3 githuby.py --sync
    python3 githuby.py --commit "Your message"
    python3 githuby.py --commit-and-push "Your message"

Version: 1.0
Created: 2025-11-19
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from datetime import datetime

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Pete's Brain specific automation commit patterns
AUTOMATION_PATTERNS = [
    "Automated: Email sync results",
    "Automated: KB update from",
    "Automated: Weekly blog post",
    "Automated: Meeting notes imported",
    "Automated: Task completion logged",
    "Automated: Daily intel report",
    "Automated: Google Docs import",
    "Automated: Weekly summary generated",
    "Automated: Granola meeting import",
    "Automated: Facebook specs update",
    "Automated: Google specs update",
    "Automated: Wispr Flow import",
    "Automated: Industry news monitor",
    "Automated: AI news monitor"
]


class GitOpsAgent:
    """Git operations with mandatory fetch-first protocol"""

    def __init__(self, cwd: Path = PROJECT_ROOT):
        self.cwd = cwd
        self.branch = "main"  # Default branch

    def run(self, command: str) -> Tuple[int, str, str]:
        """Run git command and return (returncode, stdout, stderr)"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out after 30 seconds"
        except Exception as e:
            return 1, "", str(e)

    def step0_mandatory_fetch(self) -> bool:
        """
        STEP 0: MANDATORY - Execute BEFORE any operation

        This is NON-NEGOTIABLE. Always runs:
        1. git fetch --all
        2. git status
        3. git branch -a

        Returns True if successful
        """
        print("=" * 70)
        print("  STEP 0: MANDATORY FETCH-FIRST PROTOCOL")
        print("=" * 70)
        print()

        # 1. Fetch all
        print("📥 Fetching from all remotes...")
        code, out, err = self.run("git fetch --all")
        if code != 0:
            print(f"   ❌ Fetch failed: {err}")
            return False
        print(f"   ✓ Fetch complete")
        if out.strip():
            print(f"   {out.strip()}")

        # 2. Git status
        print("\n📊 Current status...")
        code, out, err = self.run("git status")
        if code != 0:
            print(f"   ❌ Status check failed: {err}")
            return False

        # Parse status output
        if "Your branch is up to date" in out:
            print("   ✓ Local and remote are in sync")
        elif "Your branch is ahead" in out:
            ahead_match = re.search(r'ahead of .* by (\d+) commit', out)
            if ahead_match:
                print(f"   📤 Local is {ahead_match.group(1)} commit(s) ahead of remote")
        elif "Your branch is behind" in out:
            behind_match = re.search(r'behind .* by (\d+) commit', out)
            if behind_match:
                print(f"   📥 Remote is {behind_match.group(1)} commit(s) ahead of local")
        elif "have diverged" in out:
            print("   🔀 Local and remote have DIVERGED (will handle below)")

        if "nothing to commit" not in out:
            print("   📝 You have uncommitted changes")

        # 3. List branches
        print("\n🌿 Available branches...")
        code, out, err = self.run("git branch -a")
        if code != 0:
            print(f"   ❌ Branch listing failed: {err}")
            return False

        # Show current branch
        for line in out.split('\n'):
            if line.startswith('*'):
                current_branch = line.replace('*', '').strip()
                print(f"   ✓ Current branch: {current_branch}")
                self.branch = current_branch
                break

        print("\n✅ Step 0 complete - safe to proceed")
        print()

        return True

    def is_automation_commit(self, message: str) -> bool:
        """Check if commit message matches automation pattern"""
        return any(message.strip().startswith(pattern) for pattern in AUTOMATION_PATTERNS)

    def get_remote_commits(self) -> List[Dict[str, str]]:
        """Get commits that are in remote but not local"""
        code, out, err = self.run(f"git log HEAD..origin/{self.branch} --pretty=format:'%h|%an|%ar|%s'")
        if code != 0 or not out.strip():
            return []

        commits = []
        for line in out.strip().split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    })
        return commits

    def get_local_commits(self) -> List[Dict[str, str]]:
        """Get commits that are in local but not remote"""
        code, out, err = self.run(f"git log origin/{self.branch}..HEAD --pretty=format:'%h|%an|%ar|%s'")
        if code != 0 or not out.strip():
            return []

        commits = []
        for line in out.strip().split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    })
        return commits

    def handle_divergence(self) -> bool:
        """
        Handle divergence between local and remote.

        Auto-merges if remote commits are all automation patterns.
        Otherwise, presents choices to user.
        """
        print("=" * 70)
        print("  HANDLING DIVERGENCE")
        print("=" * 70)
        print()

        remote_commits = self.get_remote_commits()
        local_commits = self.get_local_commits()

        if not remote_commits:
            print("✓ No remote commits to merge (you're ahead)")
            return True

        if not local_commits:
            print("✓ No local commits (you're behind, can fast-forward)")
            return self.pull_rebase()

        # Both have commits - true divergence
        print(f"🔀 Divergence detected:")
        print(f"   Remote: {len(remote_commits)} commit(s)")
        print(f"   Local: {len(local_commits)} commit(s)")
        print()

        # Check if all remote commits are automation
        all_automation = all(self.is_automation_commit(c['message']) for c in remote_commits)

        if all_automation:
            print("✅ Remote commits are ALL automation patterns:")
            for commit in remote_commits:
                print(f"   • {commit['message'][:60]}")
            print()
            print("🤖 Auto-merging automation commits (no user prompt needed)...")
            return self.pull_rebase()
        else:
            # Has user commits - need to review
            print("⚠️  Remote has NON-automation commits:")
            for commit in remote_commits:
                is_auto = self.is_automation_commit(commit['message'])
                marker = "🤖" if is_auto else "👤"
                print(f"   {marker} {commit['message'][:60]} (by {commit['author']})")
            print()
            print("📋 Your local commits:")
            for commit in local_commits:
                print(f"   • {commit['message'][:60]}")
            print()
            print("❓ What would you like to do?")
            print("   1. Rebase local on top of remote (recommended)")
            print("   2. Merge remote into local")
            print("   3. Cancel (manual resolution)")

            choice = input("\nChoice (1/2/3): ").strip()

            if choice == "1":
                return self.pull_rebase()
            elif choice == "2":
                return self.pull_merge()
            else:
                print("⏸️  Cancelled - please resolve manually")
                return False

    def pull_rebase(self) -> bool:
        """Pull with rebase (keeps history clean)"""
        print(f"\n🔄 Rebasing local commits on top of origin/{self.branch}...")
        code, out, err = self.run(f"git pull --rebase origin {self.branch}")

        if code != 0:
            if "conflict" in err.lower() or "conflict" in out.lower():
                print("   ⚠️  Rebase conflict detected!")
                print(f"   {err if err else out}")
                print("\n   Run: git status")
                print("   Then: git rebase --continue (after resolving)")
                return False
            else:
                print(f"   ❌ Rebase failed: {err}")
                return False

        print(f"   ✅ Rebase successful")
        if out.strip():
            print(f"   {out.strip()}")
        return True

    def pull_merge(self) -> bool:
        """Pull with merge"""
        print(f"\n🔄 Merging origin/{self.branch} into local...")
        code, out, err = self.run(f"git pull origin {self.branch}")

        if code != 0:
            if "conflict" in err.lower() or "conflict" in out.lower():
                print("   ⚠️  Merge conflict detected!")
                print(f"   {err if err else out}")
                return False
            else:
                print(f"   ❌ Merge failed: {err}")
                return False

        print(f"   ✅ Merge successful")
        if out.strip():
            print(f"   {out.strip()}")
        return True

    def commit(self, message: str) -> bool:
        """Commit all changes with given message"""
        print("\n=" * 70)
        print("  COMMITTING CHANGES")
        print("=" * 70)
        print()

        # Check for changes
        code, out, err = self.run("git status --short")
        if not out.strip():
            print("ℹ️  No changes to commit")
            return True

        # Show what will be committed
        print("📝 Changes to commit:")
        for line in out.strip().split('\n'):
            print(f"   {line}")
        print()

        # Stage all changes
        print("➕ Staging all changes...")
        code, out, err = self.run("git add .")
        if code != 0:
            print(f"   ❌ Staging failed: {err}")
            return False
        print("   ✓ Staged")

        # Commit
        print(f"\n💾 Committing: {message}")
        # Escape single quotes in message
        safe_message = message.replace("'", "'\\''")
        code, out, err = self.run(f"git commit -m '{safe_message}'")
        if code != 0:
            print(f"   ❌ Commit failed: {err}")
            return False

        print("   ✅ Committed successfully")
        if out.strip():
            print(f"   {out.strip()}")

        return True

    def push(self) -> bool:
        """Push to remote"""
        print("\n=" * 70)
        print("  PUSHING TO REMOTE")
        print("=" * 70)
        print()

        print(f"📤 Pushing to origin/{self.branch}...")
        code, out, err = self.run(f"git push origin {self.branch}")

        if code != 0:
            print(f"   ❌ Push failed: {err}")
            if "rejected" in err:
                print("\n   Tip: Remote has new commits. Run --sync first.")
            return False

        print("   ✅ Pushed successfully")
        if out.strip():
            print(f"   {out.strip()}")

        return True

    def sync(self) -> bool:
        """Sync with remote (fetch + handle divergence + push if needed)"""
        # Step 0 already done in main()

        # Check status
        code, out, err = self.run("git status")
        if "up to date" in out and "nothing to commit" in out:
            print("✅ Already in sync with remote, nothing to do")
            return True

        # Handle divergence if exists
        if "have diverged" in out or "behind" in out:
            if not self.handle_divergence():
                return False

        # Push if we're ahead
        if "ahead" in out:
            print("\n📤 Local is ahead, pushing...")
            return self.push()

        return True

    def status(self) -> bool:
        """Show detailed git status (Step 0 already executed)"""
        print("=" * 70)
        print("  DETAILED STATUS")
        print("=" * 70)
        print()

        # Full status
        code, out, err = self.run("git status")
        print(out)

        # Check divergence
        remote_commits = self.get_remote_commits()
        local_commits = self.get_local_commits()

        if remote_commits:
            print("\n📥 Remote commits not yet merged:")
            for commit in remote_commits[:5]:
                is_auto = self.is_automation_commit(commit['message'])
                marker = "🤖" if is_auto else "👤"
                print(f"   {marker} {commit['hash']} - {commit['message'][:50]}")

        if local_commits:
            print("\n📤 Local commits not yet pushed:")
            for commit in local_commits[:5]:
                print(f"   • {commit['hash']} - {commit['message'][:50]}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Git Operations Agent - Mandatory fetch-first protocol',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync with remote (auto-handles automation commits)
  githuby --sync

  # Commit all changes
  githuby --commit "Update client contexts"

  # Commit and push in one operation
  githuby --commit-and-push "Add new feature"

  # Show detailed status (fetches first)
  githuby --status

  # Handle divergence manually
  githuby --handle-divergence

Note: Step 0 (fetch-first) ALWAYS runs before any operation.
        """
    )

    parser.add_argument('--sync', action='store_true',
                       help='Sync with remote (fetch + merge + push if needed)')
    parser.add_argument('--commit', metavar='MESSAGE',
                       help='Commit all changes with message')
    parser.add_argument('--commit-and-push', metavar='MESSAGE',
                       help='Commit all changes and push to remote')
    parser.add_argument('--push', action='store_true',
                       help='Push to remote')
    parser.add_argument('--handle-divergence', action='store_true',
                       help='Handle divergence between local and remote')
    parser.add_argument('--status', action='store_true',
                       help='Show detailed git status')

    args = parser.parse_args()

    # Require at least one operation
    if not any([args.sync, args.commit, args.commit_and_push, args.push,
                args.handle_divergence, args.status]):
        parser.print_help()
        return

    print("🚀 Git Operations Agent")
    print(f"   Working directory: {PROJECT_ROOT}")
    print()

    agent = GitOpsAgent()

    # === STEP 0: MANDATORY - ALWAYS RUNS FIRST ===
    if not agent.step0_mandatory_fetch():
        print("\n❌ Step 0 failed - cannot proceed safely")
        sys.exit(1)

    # Execute requested operation
    success = True

    try:
        if args.sync:
            success = agent.sync()

        elif args.commit_and_push:
            success = agent.commit(args.commit_and_push) and agent.push()

        elif args.commit:
            success = agent.commit(args.commit)

        elif args.push:
            success = agent.push()

        elif args.handle_divergence:
            success = agent.handle_divergence()

        elif args.status:
            success = agent.status()

        if success:
            print("\n" + "=" * 70)
            print("✅ OPERATION COMPLETE")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("⚠️  OPERATION INCOMPLETE")
            print("=" * 70)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏸️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
