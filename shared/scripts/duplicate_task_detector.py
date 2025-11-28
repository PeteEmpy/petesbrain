#!/usr/bin/env python3
"""
Duplicate Task Detection Module

Implements multi-level duplicate detection for AI-generated tasks:
- Level 1: Exact task match (last 7 days)
- Level 2: Semantic similarity (last 3 days, 80% threshold)
- Level 3: Context awareness (completed tasks, open tasks with same priority)
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
import sys
from pathlib import Path

# Add MCP server path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
except ImportError:
    print("Warning: tasks_service module not found. Duplicate detection will be limited.")


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between two strings (0.0 to 1.0).
    
    Uses rapidfuzz if available (better accuracy), falls back to SequenceMatcher.
    
    Args:
        str1: First string
        str2: Second string
    
    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Try rapidfuzz first (better performance and accuracy)
    try:
        from rapidfuzz import fuzz
        # Use token_sort_ratio for better semantic matching
        # This handles word order differences better
        return fuzz.token_sort_ratio(str1.lower().strip(), str2.lower().strip()) / 100.0
    except ImportError:
        # Fallback to SequenceMatcher (built-in, always available)
        return SequenceMatcher(None, str1.lower().strip(), str2.lower().strip()).ratio()


def is_same_client(task: Dict, client_name: str) -> bool:
    """
    Check if task belongs to specified client.
    
    Looks for client identifier in task notes or title.
    
    Args:
        task: Task dict from Google Tasks
        client_name: Client folder name (e.g., "smythson")
    
    Returns:
        True if task belongs to client, False otherwise
    """
    # Check notes for client metadata
    notes = task.get('notes', '')
    if f'**Client:** {client_name}' in notes:
        return True
    
    # Check title for client prefix (e.g., "[Smythson] Task description")
    title = task.get('title', '')
    # Extract client name from title prefix
    title_match = re.match(r'^\[(.+?)\]\s*', title)
    if title_match:
        title_client = title_match.group(1).lower().replace(' ', '-')
        if title_client == client_name.lower():
            return True
    
    return False


def get_recent_tasks(task_list_id: str, lookback_days: int = 7, use_cache: bool = True) -> List[Dict]:
    """
    Get recent tasks from Google Tasks for duplicate detection.
    
    Phase 4: Uses cache to reduce API calls.
    
    Args:
        task_list_id: Google Tasks list ID
        lookback_days: Number of days to look back
        use_cache: Whether to use cache (default: True)
    
    Returns:
        List of task dictionaries with metadata
    """
    # Phase 4: Check cache first
    if use_cache:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from task_cache import get_cached_tasks
            
            cached_tasks = get_cached_tasks(task_list_id)
            if cached_tasks:
                # Filter by lookback_days
                cutoff_date = datetime.now() - timedelta(days=lookback_days)
                filtered = []
                
                for task in cached_tasks:
                    created_str = task.get('created', task.get('updated', ''))
                    if created_str:
                        try:
                            created_dt = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                            if created_dt >= cutoff_date:
                                filtered.append(task)
                        except (ValueError, AttributeError):
                            filtered.append(task)
                
                if filtered:
                    return filtered
        except ImportError:
            # Cache module not available, continue with API call
            pass
        except Exception as e:
            # Cache error, continue with API call
            print(f"Warning: Cache error: {e}")
    
    try:
        service = tasks_service()
        
        # Get all tasks (including completed ones for grace period check)
        results = service.tasks().list(
            tasklist=task_list_id,
            showCompleted=True,
            maxResults=100
        ).execute()
        
        items = results.get('items', [])
        
        # Phase 4: Cache the results
        if use_cache:
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from task_cache import cache_tasks
                
                # Convert to our format for caching
                cached_format = []
                for item in items:
                    cached_format.append({
                        'id': item.get('id'),
                        'title': item.get('title', ''),
                        'status': item.get('status', 'needsAction'),
                        'notes': item.get('notes', ''),
                        'created': item.get('updated', item.get('created', '')),
                        'updated': item.get('updated', ''),
                        'completed': item.get('updated', '') if item.get('status') == 'completed' else None,
                        'due': item.get('due', '')
                    })
                
                cache_tasks(task_list_id, cached_format)
            except Exception:
                # Cache save failed, but continue
                pass
        
        # Filter by creation date
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        recent_tasks = []
        
        for item in items:
            # Get creation date (updated date if created date not available)
            created_str = item.get('updated', item.get('created', ''))
            if created_str:
                try:
                    # Parse RFC 3339 format
                    created_dt = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                    if created_dt >= cutoff_date:
                        task = {
                            'id': item.get('id'),
                            'title': item.get('title', ''),
                            'status': item.get('status', 'needsAction'),
                            'notes': item.get('notes', ''),
                            'created': created_str,
                            'updated': item.get('updated', ''),
                        }
                        
                        # Add completed date if completed
                        if item.get('status') == 'completed':
                            task['completed'] = item.get('updated', created_str)
                        
                        # Add due date if present
                        if 'due' in item:
                            task['due'] = item['due']
                        
                        recent_tasks.append(task)
                except (ValueError, AttributeError):
                    # If date parsing fails, include task anyway (better safe than sorry)
                    task = {
                        'id': item.get('id'),
                        'title': item.get('title', ''),
                        'status': item.get('status', 'needsAction'),
                        'notes': item.get('notes', ''),
                        'created': item.get('updated', ''),
                        'updated': item.get('updated', ''),
                    }
                    if item.get('status') == 'completed':
                        task['completed'] = item.get('updated', '')
                    recent_tasks.append(task)
        
        return recent_tasks
    
    except Exception as e:
        print(f"Warning: Error fetching recent tasks: {e}")
        return []


def is_duplicate_task(
    new_task: Dict,
    existing_tasks: List[Dict],
    config: Optional[Dict] = None
) -> Tuple[bool, Optional[Dict]]:
    """
    Check if new task is duplicate of existing task.
    
    Implements multi-level duplicate detection:
    1. Exact match (same client + same title)
    2. Fuzzy match (same client + >80% similarity)
    3. Context awareness (completed within grace period, open with same priority)
    4. Phase 2: State file check (prevents regeneration of open/completed tasks)
    
    Args:
        new_task: New task dict with keys: 'client', 'task', 'priority', 'reason'
        existing_tasks: List of existing tasks from Google Tasks
        config: Configuration dict with duplicate detection settings
    
    Returns:
        Tuple of (is_duplicate: bool, matching_task: Optional[Dict])
    """
    if config is None:
        config = {
            'similarity_threshold': 0.80,
            'lookback_days': 7,
            'completed_grace_period_days': 3
        }
    
    client = new_task.get('client', '')
    task_title = new_task.get('task', '')
    
    if not client or not task_title:
        return (False, None)
    
    # Phase 2: Check state file first (more efficient)
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from ai_tasks_state import check_should_regenerate
        
        should_regen, reason = check_should_regenerate(
            client,
            task_title,
            new_task.get('priority', 'P2'),
            config
        )
        
        if not should_regen:
            # State file indicates this shouldn't be regenerated
            # Return a mock matching task to indicate duplicate
            return (True, {
                'title': task_title,
                'status': 'open',  # Could be completed, but we're treating as duplicate
                'notes': f'State file check: {reason}',
                'id': None
            })
    except ImportError:
        # State file module not available, continue with normal detection
        pass
    except Exception as e:
        # If state check fails, continue with normal detection
        print(f"Warning: State file check failed: {e}")
    
    similarity_threshold = config.get('similarity_threshold', 0.80)
    completed_grace_period = config.get('completed_grace_period_days', 3)
    
    # Filter tasks by client
    client_tasks = [t for t in existing_tasks if is_same_client(t, client)]
    
    if not client_tasks:
        return (False, None)
    
    # Normalize task titles for better comparison
    def normalize_title(title: str) -> str:
        """Normalize title for comparison."""
        # Remove client prefix if present
        title = re.sub(r'^\[.+?\]\s*', '', title).strip()
        # Lowercase and normalize whitespace
        return ' '.join(title.lower().split())
    
    task_title_clean = normalize_title(task_title)
    
    for existing in client_tasks:
        existing_title = existing.get('title', '')
        existing_title_clean = normalize_title(existing_title)
        
        # Level 1: Exact match (after normalization)
        if task_title_clean == existing_title_clean:
            # Check if task is still open
            if existing.get('status') != 'completed':
                return (True, existing)
            
            # Check if recently completed (within grace period)
            completed_date = existing.get('completed')
            if completed_date:
                try:
                    completed_dt = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                    days_ago = (datetime.now() - completed_dt.replace(tzinfo=None)).days
                    if days_ago <= completed_grace_period:
                        return (True, existing)
                except (ValueError, AttributeError):
                    # If date parsing fails, treat as duplicate to be safe
                    return (True, existing)
        
        # Level 2: Fuzzy match (semantic similarity)
        similarity = calculate_similarity(task_title_clean, existing_title_clean)
        
        if similarity >= similarity_threshold:
            # Check if task is still open
            if existing.get('status') != 'completed':
                return (True, existing)
            
            # Check if recently completed (within grace period)
            completed_date = existing.get('completed')
            if completed_date:
                try:
                    completed_dt = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                    days_ago = (datetime.now() - completed_dt.replace(tzinfo=None)).days
                    if days_ago <= completed_grace_period:
                        return (True, existing)
                except (ValueError, AttributeError):
                    # If date parsing fails, treat as duplicate to be safe
                    return (True, existing)
    
    return (False, None)


if __name__ == "__main__":
    # Test duplicate detection
    print("Testing duplicate detection...")
    
    # Mock tasks
    new_task = {
        'client': 'smythson',
        'task': 'Review budget pacing',
        'priority': 'P1',
        'reason': 'Check budget pacing for November'
    }
    
    existing_tasks = [
        {
            'id': '123',
            'title': '[Smythson] Review budget pacing',
            'status': 'needsAction',
            'notes': '**Client:** smythson',
            'created': datetime.now().isoformat()
        }
    ]
    
    is_dup, matching = is_duplicate_task(new_task, existing_tasks)
    print(f"Duplicate detected: {is_dup}")
    if matching:
        print(f"Matching task: {matching['title']}")

