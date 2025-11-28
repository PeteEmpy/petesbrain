#!/usr/bin/env python3
"""
Weekly Task Review Script

Phase 3: Friday afternoon review of all AI-generated tasks.
- Flags tasks that should be completed but aren't
- Generates summary for weekly client strategy
- Identifies patterns and trends
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
        get_open_tasks_by_client,
        get_client_completion_stats
    )
    from tasks_service import tasks_service
except ImportError as e:
    print(f"Error: Required modules not found: {e}")
    sys.exit(1)


def cluster_tasks_by_type(tasks: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Cluster tasks by type (budget reviews, feed issues, etc.).
    
    Args:
        tasks: List of task dicts
    
    Returns:
        Dict mapping task type to list of tasks
    """
    clusters = defaultdict(list)
    
    # Keywords for task clustering
    type_keywords = {
        "budget": ["budget", "spend", "pacing", "cost", "roas"],
        "feed": ["feed", "merchant center", "product", "shopping"],
        "campaign": ["campaign", "ad group", "keyword", "search"],
        "audit": ["audit", "review", "check", "analyze"],
        "optimization": ["optimize", "improve", "enhance", "tune"],
        "reporting": ["report", "summary", "update", "briefing"],
        "tracking": ["tracking", "conversion", "tag", "pixel"],
        "creative": ["ad copy", "creative", "ad text", "asset"]
    }
    
    for task in tasks:
        title = task.get('task_title', '').lower()
        notes = task.get('notes', '').lower()
        text = f"{title} {notes}"
        
        matched_type = "other"
        for task_type, keywords in type_keywords.items():
            if any(keyword in text for keyword in keywords):
                matched_type = task_type
                break
        
        clusters[matched_type].append(task)
    
    return dict(clusters)


def generate_weekly_review() -> str:
    """
    Generate weekly task review summary.
    
    Returns:
        Markdown formatted review
    """
    state = load_state()
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    # Get all open tasks
    open_tasks = get_open_tasks_by_client()
    
    # Get completion stats by client
    clients = set()
    for task in open_tasks:
        clients.add(task.get('client'))
    
    client_stats = {}
    for client in clients:
        stats = get_client_completion_stats(client, days=7)
        client_stats[client] = stats
    
    # Cluster tasks by type
    clusters = cluster_tasks_by_type(open_tasks)
    
    # Find stale tasks (open for 5+ days)
    stale_tasks = []
    for task in open_tasks:
        created = task.get('created')
        if created:
            try:
                created_dt = datetime.fromisoformat(created)
                days_open = (now - created_dt).days
                if days_open >= 5:
                    stale_tasks.append((task, days_open))
            except:
                pass
    
    stale_tasks.sort(key=lambda x: x[1], reverse=True)
    
    # Build review
    review = f"""# Weekly Task Review - {now.strftime('%Y-%m-%d')}

Generated: {now.strftime('%A, %B %d, %Y at %H:%M')}

---

## 📊 Summary Statistics

- **Total Open Tasks:** {len(open_tasks)}
- **Stale Tasks (5+ days):** {len(stale_tasks)}
- **Clients with Open Tasks:** {len(clients)}

---

## ⚠️ Stale Tasks (Need Attention)

"""
    
    if stale_tasks:
        review += f"**{len(stale_tasks)} task(s) open for 5+ days:**\n\n"
        for task, days_open in stale_tasks[:10]:  # Top 10
            client = task.get('client', 'unknown')
            title = task.get('task_title', 'Untitled')
            priority = task.get('priority', 'P2')
            review += f"- **[{client}]** {title} ({priority}) - **{days_open} days open**\n"
        
        if len(stale_tasks) > 10:
            review += f"\n*... and {len(stale_tasks) - 10} more stale tasks*\n"
    else:
        review += "✅ No stale tasks! All tasks are relatively fresh.\n"
    
    review += "\n---\n\n## 📦 Task Clusters\n\n"
    
    # Show clusters
    for cluster_type, cluster_tasks in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        if cluster_type == "other" and len(cluster_tasks) == 0:
            continue
        
        review += f"### {cluster_type.title()} ({len(cluster_tasks)} tasks)\n\n"
        
        # Group by client
        by_client = defaultdict(list)
        for task in cluster_tasks:
            client = task.get('client', 'unknown')
            by_client[client].append(task)
        
        for client, client_tasks in sorted(by_client.items()):
            review += f"**{client}:** {len(client_tasks)} task(s)\n"
            for task in client_tasks[:3]:  # Show top 3 per client
                priority = task.get('priority', 'P2')
                review += f"  - {task.get('task_title', 'Untitled')} ({priority})\n"
            if len(client_tasks) > 3:
                review += f"  *... and {len(client_tasks) - 3} more*\n"
        
        review += "\n"
    
    review += "---\n\n## 📈 Client Completion Rates\n\n"
    
    # Sort clients by completion rate
    sorted_clients = sorted(
        client_stats.items(),
        key=lambda x: x[1].get('completion_rate', 0.0),
        reverse=True
    )
    
    for client, stats in sorted_clients:
        completion_rate = stats.get('completion_rate', 0.0)
        completions = stats.get('completions_this_week', 0)
        open_count = stats.get('open_tasks', 0)
        
        if completion_rate >= 0.7:
            emoji = "✅"
        elif completion_rate >= 0.4:
            emoji = "🟡"
        else:
            emoji = "🔴"
        
        review += f"{emoji} **{client}:** {completion_rate:.0%} completion rate ({completions} completed, {open_count} open)\n"
    
    review += "\n---\n\n## 💡 Recommendations\n\n"
    
    # Generate recommendations
    recommendations = []
    
    if len(stale_tasks) > 5:
        recommendations.append(f"⚠️ **High number of stale tasks ({len(stale_tasks)})** - Consider bulk completion or task review")
    
    low_completion_clients = [
        (client, stats) for client, stats in client_stats.items()
        if stats.get('completion_rate', 0.0) < 0.3 and stats.get('open_tasks', 0) > 3
    ]
    
    if low_completion_clients:
        recommendations.append(f"🔴 **{len(low_completion_clients)} client(s) with low completion rates** - Consider reducing task generation or reviewing priorities")
    
    high_completion_clients = [
        (client, stats) for client, stats in client_stats.items()
        if stats.get('completion_rate', 0.0) >= 0.7
    ]
    
    if high_completion_clients:
        recommendations.append(f"✅ **{len(high_completion_clients)} client(s) with excellent completion rates** - These clients are on track")
    
    if not recommendations:
        recommendations.append("✅ **All systems operating normally** - No immediate concerns")
    
    for rec in recommendations:
        review += f"- {rec}\n"
    
    review += f"\n---\n\n*Review generated automatically. Next review: Next Friday*\n"
    
    return review


if __name__ == "__main__":
    print("=" * 80)
    print("WEEKLY TASK REVIEW")
    print("=" * 80)
    print()
    
    review = generate_weekly_review()
    
    # Save to file
    output_file = PROJECT_ROOT / "shared" / "data" / f"weekly-task-review-{datetime.now().strftime('%Y-%m-%d')}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(review)
    
    print(review)
    print()
    print(f"✅ Review saved to: {output_file}")

