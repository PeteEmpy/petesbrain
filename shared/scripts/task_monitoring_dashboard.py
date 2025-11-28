#!/usr/bin/env python3
"""
Task System Monitoring Dashboard

Phase 4: Tracks and displays metrics for the AI task integration system:
- AI task creation rate
- Duplicate detection rate
- Completion rate by client
- Escalation statistics
- Performance metrics
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "shared" / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"))

try:
    from ai_tasks_state import (
        load_state,
        get_client_completion_stats,
        get_open_tasks_by_client
    )
    from tasks_service import tasks_service
except ImportError as e:
    print(f"Error: Required modules not found: {e}")
    sys.exit(1)


METRICS_FILE = PROJECT_ROOT / "shared" / "data" / "task-metrics.json"


def load_metrics() -> Dict:
    """Load historical metrics."""
    if not METRICS_FILE.exists():
        return {
            "daily_stats": [],
            "last_updated": None,
            "version": "1.0"
        }
    
    try:
        with open(METRICS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Error loading metrics: {e}")
        return {
            "daily_stats": [],
            "last_updated": None,
            "version": "1.0"
        }


def save_metrics(metrics: Dict):
    """Save metrics to file."""
    metrics["last_updated"] = datetime.now().isoformat()
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)
    except Exception as e:
        print(f"Warning: Error saving metrics: {e}")


def record_daily_stats(
    tasks_created: int,
    duplicates_skipped: int,
    skipped_by_state: int,
    errors: int
):
    """Record daily statistics."""
    metrics = load_metrics()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if today's stats already exist
    daily_stats = metrics.get("daily_stats", [])
    today_stats = None
    for stat in daily_stats:
        if stat.get("date") == today:
            today_stats = stat
            break
    
    if not today_stats:
        today_stats = {
            "date": today,
            "tasks_created": 0,
            "duplicates_skipped": 0,
            "skipped_by_state": 0,
            "errors": 0,
            "completions": 0,
            "escalations": 0
        }
        daily_stats.append(today_stats)
    
    # Update stats
    today_stats["tasks_created"] += tasks_created
    today_stats["duplicates_skipped"] += duplicates_skipped
    today_stats["skipped_by_state"] += skipped_by_state
    today_stats["errors"] += errors
    
    # Keep only last 30 days
    cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    metrics["daily_stats"] = [
        stat for stat in daily_stats
        if stat.get("date", "") >= cutoff_date
    ]
    
    save_metrics(metrics)


def get_current_metrics() -> Dict:
    """Get current system metrics."""
    state = load_state()
    now = datetime.now()
    
    # Count tasks by status
    total_tasks = len(state.get("tasks", {}))
    open_tasks = sum(
        1 for task_data in state.get("tasks", {}).values()
        if task_data.get("status") == "open"
    )
    completed_tasks = sum(
        1 for task_data in state.get("tasks", {}).values()
        if task_data.get("status") == "completed"
    )
    
    # Count by priority
    priority_counts = defaultdict(int)
    for task_data in state.get("tasks", {}).values():
        if task_data.get("status") == "open":
            priority = task_data.get("priority", "P2")
            priority_counts[priority] += 1
    
    # Count escalations
    escalations_count = sum(
        1 for task_data in state.get("tasks", {}).values()
        if task_data.get("last_escalated")
    )
    
    # Get client stats
    clients = set()
    for task_data in state.get("tasks", {}).values():
        clients.add(task_data.get("client"))
    
    client_completion_rates = {}
    for client in clients:
        stats = get_client_completion_stats(client, days=7)
        client_completion_rates[client] = stats.get("completion_rate", 0.0)
    
    # Calculate completion rate
    completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
    
    # Get recent stats (last 7 days)
    metrics = load_metrics()
    recent_stats = [
        stat for stat in metrics.get("daily_stats", [])
        if stat.get("date", "") >= (now - timedelta(days=7)).strftime('%Y-%m-%d')
    ]
    
    recent_created = sum(stat.get("tasks_created", 0) for stat in recent_stats)
    recent_duplicates = sum(stat.get("duplicates_skipped", 0) for stat in recent_stats)
    recent_skipped = sum(stat.get("skipped_by_state", 0) for stat in recent_stats)
    recent_errors = sum(stat.get("errors", 0) for stat in recent_stats)
    
    # Calculate duplicate detection rate
    total_attempted = recent_created + recent_duplicates + recent_skipped
    duplicate_rate = recent_duplicates / total_attempted if total_attempted > 0 else 0.0
    
    return {
        "total_tasks": total_tasks,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "priority_distribution": dict(priority_counts),
        "escalations": escalations_count,
        "clients": len(clients),
        "client_completion_rates": client_completion_rates,
        "recent_7_days": {
            "tasks_created": recent_created,
            "duplicates_skipped": recent_duplicates,
            "skipped_by_state": recent_skipped,
            "errors": recent_errors,
            "duplicate_detection_rate": duplicate_rate
        }
    }


def generate_dashboard() -> str:
    """Generate monitoring dashboard."""
    metrics = get_current_metrics()
    
    dashboard = f"""# Task System Monitoring Dashboard

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 System Overview

- **Total Tasks:** {metrics['total_tasks']}
- **Open Tasks:** {metrics['open_tasks']}
- **Completed Tasks:** {metrics['completed_tasks']}
- **Completion Rate:** {metrics['completion_rate']:.1%}
- **Escalations:** {metrics['escalations']}
- **Active Clients:** {metrics['clients']}

---

## 📈 Recent Activity (Last 7 Days)

- **Tasks Created:** {metrics['recent_7_days']['tasks_created']}
- **Duplicates Skipped:** {metrics['recent_7_days']['duplicates_skipped']}
- **Skipped (State Check):** {metrics['recent_7_days']['skipped_by_state']}
- **Errors:** {metrics['recent_7_days']['errors']}
- **Duplicate Detection Rate:** {metrics['recent_7_days']['duplicate_detection_rate']:.1%}

---

## 🎯 Priority Distribution

"""
    
    priority_counts = metrics['priority_distribution']
    for priority in ['P0', 'P1', 'P2', 'P3']:
        count = priority_counts.get(priority, 0)
        if count > 0:
            dashboard += f"- **{priority}:** {count} tasks\n"
    
    dashboard += "\n---\n\n## 📊 Client Completion Rates\n\n"
    
    # Sort by completion rate
    sorted_clients = sorted(
        metrics['client_completion_rates'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for client, rate in sorted_clients:
        if rate >= 0.7:
            emoji = "✅"
        elif rate >= 0.4:
            emoji = "🟡"
        else:
            emoji = "🔴"
        
        dashboard += f"{emoji} **{client}:** {rate:.0%}\n"
    
    dashboard += "\n---\n\n## 💡 Insights\n\n"
    
    # Generate insights
    insights = []
    
    if metrics['completion_rate'] >= 0.7:
        insights.append("✅ **High overall completion rate** - System is performing well")
    elif metrics['completion_rate'] < 0.3:
        insights.append("⚠️ **Low completion rate** - Consider reviewing task priorities")
    
    if metrics['recent_7_days']['duplicate_detection_rate'] > 0.3:
        insights.append(f"🔍 **High duplicate detection rate ({metrics['recent_7_days']['duplicate_detection_rate']:.0%})** - Duplicate detection is working effectively")
    
    if metrics['recent_7_days']['errors'] > 0:
        insights.append(f"⚠️ **{metrics['recent_7_days']['errors']} error(s) in last 7 days** - Review error logs")
    
    low_completion_clients = [
        client for client, rate in metrics['client_completion_rates'].items()
        if rate < 0.3
    ]
    
    if low_completion_clients:
        insights.append(f"🔴 **{len(low_completion_clients)} client(s) with low completion rates** - Adaptive generation is reducing task load")
    
    if not insights:
        insights.append("✅ **All systems operating normally**")
    
    for insight in insights:
        dashboard += f"- {insight}\n"
    
    dashboard += f"\n---\n\n*Dashboard updated automatically. Metrics stored in: {METRICS_FILE.name}*\n"
    
    return dashboard


if __name__ == "__main__":
    print("=" * 80)
    print("TASK SYSTEM MONITORING DASHBOARD")
    print("=" * 80)
    print()
    
    dashboard = generate_dashboard()
    
    # Save to file
    output_file = PROJECT_ROOT / "shared" / "data" / "task-dashboard.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(dashboard)
    
    print(dashboard)
    print()
    print(f"✅ Dashboard saved to: {output_file}")

