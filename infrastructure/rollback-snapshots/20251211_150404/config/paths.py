#!/usr/bin/env python3
"""
Centralized path discovery for PetesBrain agents and tools.

This module provides a single source of truth for all file paths, supporting:
- Environment variable-based discovery (PETESBRAIN_ROOT for portability)
- Fallback to relative path discovery for development
- Convenient helper functions for common directories

Usage:
    from shared.paths import get_project_root, get_client_dir, get_briefing_dir

    # Get project root
    root = get_project_root()

    # Get specific directories
    clients_dir = get_clients_dir()
    briefing_dir = get_briefing_dir()

    # Get per-client directories
    smythson_dir = get_client_dir('smythson')
    smythson_tasks = get_client_tasks_file('smythson')
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Get the PetesBrain project root directory.

    Attempts discovery in this order:
    1. PETESBRAIN_ROOT environment variable (set by plist files)
    2. Relative path from current script location
    3. Relative path from __file__ location

    Returns:
        Path object pointing to project root (/Users/administrator/Documents/PetesBrain.nosync)

    Raises:
        RuntimeError: If project root cannot be determined
    """

    # Try environment variable first (set by LaunchAgent plist)
    petesbrain_root = os.getenv('PETESBRAIN_ROOT')
    if petesbrain_root:
        root = Path(petesbrain_root).resolve()
        if root.exists() and (root / 'shared').exists():
            return root

    # Fallback 1: Try from this file's location
    # shared/paths.py -> shared -> project root
    try:
        root = Path(__file__).parent.parent.resolve()
        if root.exists() and (root / 'shared').exists():
            return root
    except Exception:
        pass

    # Fallback 2: Try from current working directory
    cwd = Path.cwd().resolve()
    if cwd.exists() and (cwd / 'shared').exists():
        return cwd

    # Fallback 3: Try from sys.path entries
    for path_entry in sys.path:
        if path_entry:
            candidate = Path(path_entry).parent.resolve()
            if candidate.exists() and (candidate / 'shared').exists():
                return candidate

    # If all else fails, raise an error
    raise RuntimeError(
        "Could not determine PetesBrain project root. "
        "Set PETESBRAIN_ROOT environment variable or ensure paths.py is in project."
    )


def get_clients_dir() -> Path:
    """Get the clients directory."""
    return get_project_root() / 'clients'


def get_client_dir(client_slug: str) -> Path:
    """
    Get the directory for a specific client.

    Args:
        client_slug: Client slug (e.g., 'smythson', 'superspace')

    Returns:
        Path to client directory
    """
    return get_clients_dir() / client_slug


def get_client_tasks_file(client_slug: str) -> Path:
    """Get the tasks.json file for a specific client."""
    return get_client_dir(client_slug) / 'tasks.json'


def get_client_tasks_completed_file(client_slug: str) -> Path:
    """Get the tasks-completed.md file for a specific client."""
    return get_client_dir(client_slug) / 'tasks-completed.md'


def get_client_context_file(client_slug: str) -> Path:
    """Get the CONTEXT.md file for a specific client."""
    return get_client_dir(client_slug) / 'CONTEXT.md'


def get_briefing_dir() -> Path:
    """Get the briefing directory for daily reports."""
    return get_project_root() / 'briefing'


def get_data_dir() -> Path:
    """Get the data directory for cache/state files."""
    return get_project_root() / 'data'


def get_data_cache_dir() -> Path:
    """Get the data/cache directory for temporary cache files."""
    return get_data_dir() / 'cache'


def get_tools_dir() -> Path:
    """Get the tools directory."""
    return get_project_root() / 'tools'


def get_tool_dir(tool_name: str) -> Path:
    """Get the directory for a specific tool."""
    return get_tools_dir() / tool_name


def get_agents_dir() -> Path:
    """Get the agents directory."""
    return get_project_root() / 'agents'


def get_shared_dir() -> Path:
    """Get the shared directory."""
    return get_project_root() / 'shared'


def get_shared_scripts_dir() -> Path:
    """Get the shared/scripts directory."""
    return get_shared_dir() / 'scripts'


def get_shared_email_sync_dir() -> Path:
    """Get the shared/email-sync directory."""
    return get_shared_dir() / 'email-sync'


def get_infrastructure_dir() -> Path:
    """Get the infrastructure directory."""
    return get_project_root() / 'infrastructure'


def get_infrastructure_mcp_servers_dir() -> Path:
    """Get the infrastructure/mcp-servers directory."""
    return get_infrastructure_dir() / 'mcp-servers'


def get_mcp_server_dir(server_name: str) -> Path:
    """Get the directory for a specific MCP server."""
    return get_infrastructure_mcp_servers_dir() / server_name


def get_docs_dir() -> Path:
    """Get the docs directory."""
    return get_project_root() / 'docs'


def verify_paths() -> bool:
    """
    Verify that critical directories exist.

    Returns:
        True if all critical directories exist, False otherwise
    """
    critical_dirs = [
        get_project_root(),
        get_clients_dir(),
        get_briefing_dir(),
        get_shared_dir(),
        get_agents_dir(),
    ]

    for dir_path in critical_dirs:
        if not dir_path.exists():
            print(f"❌ Missing critical directory: {dir_path}")
            return False

    return True


if __name__ == '__main__':
    # Test script
    print("PetesBrain Path Discovery Test")
    print("=" * 60)

    try:
        root = get_project_root()
        print(f"✅ Project root: {root}")

        print(f"\nKey directories:")
        print(f"  Clients:        {get_clients_dir()}")
        print(f"  Briefing:       {get_briefing_dir()}")
        print(f"  Tools:          {get_tools_dir()}")
        print(f"  Agents:         {get_agents_dir()}")
        print(f"  Shared:         {get_shared_dir()}")
        print(f"  Infrastructure: {get_infrastructure_dir()}")
        print(f"  Docs:           {get_docs_dir()}")

        print(f"\nVerifying directories...")
        if verify_paths():
            print("✅ All critical directories exist")
        else:
            print("❌ Some critical directories missing")

    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
