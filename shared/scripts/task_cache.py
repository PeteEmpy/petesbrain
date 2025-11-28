#!/usr/bin/env python3
"""
Task System Cache

Phase 4: Performance optimization through caching Google Tasks queries.
Reduces API calls and improves response times.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_FILE = PROJECT_ROOT / "shared" / "data" / "tasks-cache.json"

# Cache TTL (time to live) in seconds
CACHE_TTL = 300  # 5 minutes


def load_cache() -> Dict:
    """Load cache from file."""
    if not CACHE_FILE.exists():
        return {
            "tasks": {},
            "last_updated": None,
            "version": "1.0"
        }
    
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Error loading cache: {e}")
        return {
            "tasks": {},
            "last_updated": None,
            "version": "1.0"
        }


def save_cache(cache: Dict):
    """Save cache to file."""
    cache["last_updated"] = datetime.now().isoformat()
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Warning: Error saving cache: {e}")


def is_cache_valid(cache_entry: Dict, ttl: int = CACHE_TTL) -> bool:
    """Check if cache entry is still valid."""
    if not cache_entry:
        return False
    
    last_updated = cache_entry.get("last_updated")
    if not last_updated:
        return False
    
    try:
        updated_dt = datetime.fromisoformat(last_updated)
        age = (datetime.now() - updated_dt).total_seconds()
        return age < ttl
    except (ValueError, AttributeError):
        return False


def get_cached_tasks(task_list_id: str) -> Optional[List[Dict]]:
    """
    Get cached tasks for a task list.
    
    Args:
        task_list_id: Google Tasks list ID
    
    Returns:
        Cached tasks if valid, None otherwise
    """
    cache = load_cache()
    cache_entry = cache.get("tasks", {}).get(task_list_id)
    
    if cache_entry and is_cache_valid(cache_entry):
        return cache_entry.get("data")
    
    return None


def cache_tasks(task_list_id: str, tasks: List[Dict]):
    """
    Cache tasks for a task list.
    
    Args:
        task_list_id: Google Tasks list ID
        tasks: List of task dictionaries
    """
    cache = load_cache()
    
    if "tasks" not in cache:
        cache["tasks"] = {}
    
    cache["tasks"][task_list_id] = {
        "data": tasks,
        "last_updated": datetime.now().isoformat(),
        "count": len(tasks)
    }
    
    save_cache(cache)


def clear_cache(task_list_id: Optional[str] = None):
    """
    Clear cache for a specific task list or all caches.
    
    Args:
        task_list_id: Optional task list ID to clear, or None to clear all
    """
    cache = load_cache()
    
    if task_list_id:
        if task_list_id in cache.get("tasks", {}):
            del cache["tasks"][task_list_id]
            save_cache(cache)
    else:
        cache["tasks"] = {}
        save_cache(cache)


def get_cache_stats() -> Dict:
    """Get cache statistics."""
    cache = load_cache()
    tasks_cache = cache.get("tasks", {})
    
    total_entries = len(tasks_cache)
    valid_entries = sum(
        1 for entry in tasks_cache.values()
        if is_cache_valid(entry)
    )
    
    total_cached_tasks = sum(
        entry.get("count", 0)
        for entry in tasks_cache.values()
    )
    
    return {
        "total_entries": total_entries,
        "valid_entries": valid_entries,
        "expired_entries": total_entries - valid_entries,
        "total_cached_tasks": total_cached_tasks,
        "cache_file": str(CACHE_FILE)
    }


if __name__ == "__main__":
    print("=" * 80)
    print("TASK SYSTEM CACHE")
    print("=" * 80)
    print()
    
    stats = get_cache_stats()
    print(f"Cache Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Valid entries: {stats['valid_entries']}")
    print(f"  Expired entries: {stats['expired_entries']}")
    print(f"  Total cached tasks: {stats['total_cached_tasks']}")
    print(f"  Cache file: {stats['cache_file']}")
    print()

