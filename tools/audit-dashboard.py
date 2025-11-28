#!/usr/bin/env python3
"""
Google Ads Audit Dashboard

Displays status of all client audits including:
- Which audits have been generated
- Which have been completed (results filled in)
- Which recommendations have been actioned
- Summary statistics
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent
CLIENTS_DIR = PROJECT_ROOT / "clients"


def check_audit_completed(audit_file: Path) -> bool:
    """Check if an audit has been completed (has results)"""
    if not audit_file.exists():
        return False
    
    content = audit_file.read_text()
    
    # Check for indicators that audit was run
    indicators = [
        "## 📊 Audit Results",
        "Campaign Overview",
        "Total Spend:",
        "ROAS:",
        "## Recommendations",
    ]
    
    # If any indicator is found after the prompt section, audit was completed
    prompt_end = content.find("## 📊 Audit Results")
    if prompt_end == -1:
        prompt_end = content.find("<!-- Claude will populate")
    
    if prompt_end == -1:
        return False
    
    content_after_prompt = content[prompt_end:]
    
    for indicator in indicators:
        if indicator in content_after_prompt and "Run the audit prompt" not in content_after_prompt:
            return True
    
    return False


def get_client_audit_status(client_slug: str) -> Dict[str, Any]:
    """Get audit status for a specific client"""
    client_dir = CLIENTS_DIR / client_slug
    audit_dir = client_dir / "audits"
    
    if not audit_dir.exists():
        return {
            "client": client_slug,
            "has_audits": False,
            "total_audits": 0,
            "completed": 0,
            "pending": 0,
        }
    
    audit_files = list(audit_dir.glob("*-audit-template.md"))
    completed_audits = [f for f in audit_files if check_audit_completed(f)]
    
    return {
        "client": client_slug,
        "has_audits": True,
        "total_audits": len(audit_files),
        "completed": len(completed_audits),
        "pending": len(audit_files) - len(completed_audits),
        "last_generated": max((f.stat().st_mtime for f in audit_files), default=0),
    }


def display_dashboard():
    """Display audit dashboard"""
    print("=" * 70)
    print("  GOOGLE ADS AUDIT DASHBOARD")
    print("=" * 70)
    print()
    
    if not CLIENTS_DIR.exists():
        print("❌ Clients directory not found")
        return
    
    # Get all clients
    clients = sorted([d.name for d in CLIENTS_DIR.iterdir() if d.is_dir()])
    
    if not clients:
        print("❌ No clients found")
        return
    
    # Collect audit status for each client
    client_statuses = []
    for client in clients:
        status = get_client_audit_status(client)
        if status["has_audits"]:
            client_statuses.append(status)
    
    if not client_statuses:
        print("📋 No audits generated yet")
        print()
        print("To generate audits:")
        print("  ./audit --all")
        print("  ./audit --client <client-name> --type full")
        return
    
    # Display summary
    total_audits = sum(c["total_audits"] for c in client_statuses)
    total_completed = sum(c["completed"] for c in client_statuses)
    total_pending = sum(c["pending"] for c in client_statuses)
    
    completion_rate = (total_completed / total_audits * 100) if total_audits > 0 else 0
    
    print(f"📊 SUMMARY")
    print()
    print(f"  Clients with audits: {len(client_statuses)}")
    print(f"  Total audit templates: {total_audits}")
    print(f"  Completed: {total_completed} ✅")
    print(f"  Pending: {total_pending} 🟡")
    print(f"  Completion rate: {completion_rate:.1f}%")
    print()
    print("=" * 70)
    print()
    
    # Display per-client status
    print("📋 CLIENT AUDIT STATUS")
    print()
    print(f"{'Client':<25} {'Total':<8} {'Done':<8} {'Pending':<10} {'Last Gen'}")
    print("-" * 70)
    
    for status in sorted(client_statuses, key=lambda x: x["pending"], reverse=True):
        client = status["client"][:24]
        total = status["total_audits"]
        done = status["completed"]
        pending = status["pending"]
        
        if status["last_generated"]:
            last_gen = datetime.fromtimestamp(status["last_generated"])
            days_ago = (datetime.now() - last_gen).days
            if days_ago == 0:
                last_str = "Today"
            elif days_ago == 1:
                last_str = "Yesterday"
            else:
                last_str = f"{days_ago}d ago"
        else:
            last_str = "N/A"
        
        # Status indicator
        if pending == 0:
            status_emoji = "✅"
        elif done > 0:
            status_emoji = "🟡"
        else:
            status_emoji = "⚪"
        
        print(f"{status_emoji} {client:<23} {total:<8} {done:<8} {pending:<10} {last_str}")
    
    print()
    print("=" * 70)
    print()
    
    # Show next steps
    if total_pending > 0:
        print("💡 NEXT STEPS")
        print()
        print(f"  You have {total_pending} audit template(s) waiting to be run:")
        print()
        
        # Show clients with most pending
        top_pending = sorted(client_statuses, key=lambda x: x["pending"], reverse=True)[:3]
        for status in top_pending:
            if status["pending"] > 0:
                client = status["client"]
                pending = status["pending"]
                print(f"  • {client}: {pending} audit(s) pending")
                print(f"    → Open clients/{client}/audits/ in Claude Code")
        
        print()
        print("  Run audits with Claude Code + Google Ads MCP:")
        print("    1. Open audit template file")
        print("    2. Copy audit prompt")
        print("    3. Paste into Claude Code")
        print("    4. Save results back to template")
        print()
    
    print("=" * 70)


def display_client_detail(client_slug: str):
    """Display detailed audit info for specific client"""
    print("=" * 70)
    print(f"  AUDIT DETAIL: {client_slug.upper()}")
    print("=" * 70)
    print()
    
    client_dir = CLIENTS_DIR / client_slug
    audit_dir = client_dir / "audits"
    
    if not audit_dir.exists():
        print(f"❌ No audits found for {client_slug}")
        print()
        print("Generate audits:")
        print(f"  ./audit --client {client_slug} --type full")
        return
    
    audit_files = sorted(audit_dir.glob("*-audit-template.md"), reverse=True)
    
    if not audit_files:
        print(f"❌ No audit templates found for {client_slug}")
        return
    
    print("📋 AUDIT TEMPLATES:\n")
    
    for audit_file in audit_files:
        completed = check_audit_completed(audit_file)
        status_emoji = "✅" if completed else "🟡"
        status_text = "Completed" if completed else "Pending"
        
        # Get file age
        mtime = datetime.fromtimestamp(audit_file.stat().st_mtime)
        days_ago = (datetime.now() - mtime).days
        
        if days_ago == 0:
            age_str = "Today"
        elif days_ago == 1:
            age_str = "Yesterday"
        else:
            age_str = f"{days_ago} days ago"
        
        print(f"{status_emoji} {audit_file.name}")
        print(f"   Status: {status_text}")
        print(f"   Created: {age_str}")
        print(f"   Path: clients/{client_slug}/audits/{audit_file.name}")
        print()
    
    # Show audit index if exists
    index_files = list(audit_dir.glob("*-audit-index.md"))
    if index_files:
        latest_index = max(index_files, key=lambda f: f.stat().st_mtime)
        print(f"📑 Audit Index: {latest_index.name}")
        print(f"   Path: clients/{client_slug}/audits/{latest_index.name}")
        print()
    
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Google Ads Audit Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show dashboard for all clients
  python3 tools/audit-dashboard.py
  
  # Show detail for specific client
  python3 tools/audit-dashboard.py --client smythson
        """
    )
    
    parser.add_argument('--client', help='Show detail for specific client')
    
    args = parser.parse_args()
    
    try:
        if args.client:
            display_client_detail(args.client)
        else:
            display_dashboard()
    
    except KeyboardInterrupt:
        print("\n\nDashboard closed.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

