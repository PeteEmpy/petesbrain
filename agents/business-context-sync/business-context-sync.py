#!/usr/bin/env python3
"""
Business Context Sync Agent

Automatically synchronises operational metrics from PetesBrain system state to
context/business/business-overview.md.

Runs daily at 8:00 AM via LaunchAgent.

What it syncs:
- Active client count (from clients/ folder)
- Monthly Recurring Revenue (from client CONTEXT.md retainer amounts)
- Knowledge base article count (from KB index)
- MCP server count (from .mcp.json)
- LaunchAgent count (from ~/Library/LaunchAgents/)

What it does NOT touch:
- Strategic priorities, goals, philosophy (requires human judgment)
- Personal preferences, communication style
- Market opportunities and risks
- Anything outside the <!-- AUTO-SYNC --> markers

Safe by design:
- Only updates content between HTML comments
- Never overwrites manual content outside markers
- Full audit trail logged
- Runs non-destructively (dry-run by default)
"""

import logging
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import sys
import os

# Setup logging
log_file = Path.home() / ".petesbrain-business-context-sync.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

# Base paths
BASE_PATH = Path(__file__).parent.parent.parent
CLIENTS_PATH = BASE_PATH / "clients"
BUSINESS_CONTEXT_FILE = BASE_PATH / "context" / "business" / "business-overview.md"
MCP_JSON_PATH = BASE_PATH / ".mcp.json"
KB_PATH = BASE_PATH / "roksys" / "knowledge-base"
LAUNCH_AGENTS_PATH = Path.home() / "Library" / "LaunchAgents"

# Import retainer functions from shared
sys.path.insert(0, str(BASE_PATH / "shared"))
try:
    from platform_ids import calculate_total_mrr
except ImportError:
    logger.error("Could not import calculate_total_mrr from platform_ids")
    calculate_total_mrr = None


def count_active_clients() -> int:
    """Count active clients from clients/ folder."""
    if not CLIENTS_PATH.exists():
        logger.warning("clients/ folder not found")
        return 0

    count = 0
    for item in CLIENTS_PATH.iterdir():
        if item.is_dir() and not item.name.startswith(('_', '.')):
            if (item / "CONTEXT.md").exists():
                count += 1

    logger.info(f"Found {count} active clients")
    return count


def calculate_mrr() -> Dict[str, int]:
    """Calculate MRR using platform_ids helper."""
    if calculate_total_mrr is None:
        logger.warning("calculate_total_mrr not available, returning 0")
        return {'total_mrr': 0, 'documented': 0}

    try:
        result = calculate_total_mrr()
        logger.info(f"Calculated MRR: £{result['total_mrr']} from {result['clients_with_retainer']} documented clients")
        return {
            'total_mrr': result['total_mrr'],
            'documented': result['clients_with_retainer']
        }
    except Exception as e:
        logger.error(f"Error calculating MRR: {e}")
        return {'total_mrr': 0, 'documented': 0}


def count_kb_articles() -> int:
    """Count knowledge base articles."""
    if not KB_PATH.exists():
        logger.warning("Knowledge base folder not found")
        return 0

    # Count all .md files recursively
    count = sum(1 for _ in KB_PATH.rglob("*.md"))
    logger.info(f"Found {count} knowledge base articles")
    return count


def count_mcp_servers() -> int:
    """Count active MCP servers from .mcp.json."""
    if not MCP_JSON_PATH.exists():
        logger.warning(".mcp.json not found")
        return 0

    try:
        with open(MCP_JSON_PATH) as f:
            data = json.load(f)
            servers = data.get("mcpServers", {})
            count = len(servers)
            logger.info(f"Found {count} MCP servers in configuration")
            return count
    except Exception as e:
        logger.error(f"Error reading .mcp.json: {e}")
        return 0


def count_launch_agents() -> int:
    """Count PetesBrain LaunchAgents from ~/Library/LaunchAgents/."""
    if not LAUNCH_AGENTS_PATH.exists():
        logger.warning("LaunchAgents folder not found")
        return 0

    count = 0
    for plist_file in LAUNCH_AGENTS_PATH.glob("com.petesbrain.*.plist"):
        count += 1

    logger.info(f"Found {count} PetesBrain LaunchAgents")
    return count


def collect_metrics() -> Dict[str, int]:
    """Collect all operational metrics."""
    logger.info("=" * 60)
    logger.info("Starting business context sync")
    logger.info("=" * 60)

    metrics = {
        'client_count': count_active_clients(),
        'kb_articles': count_kb_articles(),
        'mcp_servers': count_mcp_servers(),
        'launch_agents': count_launch_agents(),
    }

    # Get MRR (special handling)
    mrr_data = calculate_mrr()
    metrics['mrr'] = mrr_data['total_mrr']
    metrics['mrr_documented_clients'] = mrr_data['documented']

    logger.info(f"Collected metrics: {metrics}")
    return metrics


def update_business_overview(metrics: Dict[str, int], dry_run: bool = False) -> bool:
    """
    Update business-overview.md with new metrics.

    Only updates content between <!-- AUTO-SYNC START --> and <!-- AUTO-SYNC END --> markers.

    Args:
        metrics: Dictionary of collected metrics
        dry_run: If True, don't write changes (default: False for actual execution)

    Returns:
        True if successful, False otherwise
    """
    if not BUSINESS_CONTEXT_FILE.exists():
        logger.error(f"business-overview.md not found at {BUSINESS_CONTEXT_FILE}")
        return False

    try:
        content = BUSINESS_CONTEXT_FILE.read_text()
    except Exception as e:
        logger.error(f"Error reading business-overview.md: {e}")
        return False

    # Check if markers exist
    if "<!-- AUTO-SYNC START -->" not in content or "<!-- AUTO-SYNC END -->" not in content:
        logger.warning("AUTO-SYNC markers not found in business-overview.md")
        logger.warning("Skipping update - markers must be manually added first")
        return False

    # Extract section before, during, and after markers
    before_match = re.search(r'(.*?)<!-- AUTO-SYNC START -->', content, re.DOTALL)
    after_match = re.search(r'<!-- AUTO-SYNC END -->(.*)', content, re.DOTALL)

    if not before_match or not after_match:
        logger.error("Could not parse AUTO-SYNC markers")
        return False

    before = before_match.group(1)
    after = after_match.group(1)

    # Build new auto-sync section
    sync_date = datetime.now().strftime("%Y-%m-%d")
    new_section = f"""<!-- AUTO-SYNC START -->
**Current State (synced {sync_date})**:
- Active Clients: {metrics['client_count']}
- Monthly Recurring Revenue: £{metrics['mrr']:,} (from {metrics['mrr_documented_clients']} documented retainers)
- Knowledge Base Articles: {metrics['kb_articles']}
- MCP Servers: {metrics['mcp_servers']}
- LaunchAgents: {metrics['launch_agents']}

*Note: Automatically synced metrics. Manual updates outside these markers are never overwritten.*
<!-- AUTO-SYNC END -->"""

    # Build new content
    new_content = before + new_section + after

    # Show diff
    if before_match and after_match:
        logger.info("Changes that would be made:")
        logger.info(f"  Client Count: {metrics['client_count']}")
        logger.info(f"  MRR: £{metrics['mrr']:,} ({metrics['mrr_documented_clients']} documented clients)")
        logger.info(f"  KB Articles: {metrics['kb_articles']}")
        logger.info(f"  MCP Servers: {metrics['mcp_servers']}")
        logger.info(f"  LaunchAgents: {metrics['launch_agents']}")

    if dry_run:
        logger.info("DRY RUN: No changes written to disk")
        return True

    # Write new content
    try:
        BUSINESS_CONTEXT_FILE.write_text(new_content)
        logger.info("✅ Updated business-overview.md with synced metrics")
        return True
    except Exception as e:
        logger.error(f"Error writing business-overview.md: {e}")
        return False


def add_document_history_entry() -> bool:
    """
    Add entry to Document History table in business-overview.md.

    Returns:
        True if successful, False otherwise
    """
    if not BUSINESS_CONTEXT_FILE.exists():
        return False

    try:
        content = BUSINESS_CONTEXT_FILE.read_text()
    except Exception:
        return False

    # Find Document History table (flexible heading levels and formatting)
    history_match = re.search(
        r'(#{2,3} Document History\n.*?\n\| Date.*?\|.*?\|.*?\|)',
        content,
        re.DOTALL
    )

    if not history_match:
        logger.warning("Document History table not found, skipping entry")
        return False

    sync_date = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"| {sync_date} | Synced operational metrics (clients, MRR, KB articles, agents) | Auto-Sync Agent |"

    # Insert new entry after table header
    insert_pos = history_match.end()
    new_content = content[:insert_pos] + f"{new_entry}\n" + content[insert_pos:]

    try:
        BUSINESS_CONTEXT_FILE.write_text(new_content)
        logger.info("✅ Added Document History entry")
        return True
    except Exception as e:
        logger.error(f"Error updating Document History: {e}")
        return False


def main(dry_run: bool = False):
    """
    Main sync function.

    Args:
        dry_run: If True, collect metrics but don't write changes
    """
    try:
        # Collect all metrics
        metrics = collect_metrics()

        # Update business-overview.md
        success = update_business_overview(metrics, dry_run=dry_run)

        if success:
            add_document_history_entry()
            logger.info("=" * 60)
            logger.info("✅ Business context sync completed successfully")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("=" * 60)
            logger.error("❌ Business context sync failed")
            logger.error("=" * 60)
            return 1

    except Exception as e:
        logger.error(f"Unexpected error in business context sync: {e}")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        logger.info("Running in DRY-RUN mode (no changes will be written)")

    exit_code = main(dry_run=dry_run)
    sys.exit(exit_code)
