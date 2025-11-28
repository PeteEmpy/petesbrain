#!/usr/bin/env python3
"""
Google Trends Monitor Agent
Tracks search interest trends for all clients and correlates with performance

Runs weekly to:
- Fetch search trends for client products/services
- Identify significant trend changes (>20% movement)
- Correlate trends with campaign performance
- Add insights to client CONTEXT.md
- Alert on declining search interest
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def log(message):
    """Log with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}", flush=True)


def get_client_keywords():
    """
    Get keywords to track for each client
    Returns dict: {client_name: [keywords]}
    """
    # Define primary keywords for each client
    # These should be product/service categories, not brand names
    keywords = {
        "smythson": ["luxury stationery", "leather notebooks", "personalised diaries"],
        "tree2mydoor": ["artificial christmas trees", "christmas trees", "christmas decorations"],
        "national-design-academy": ["interior design courses", "online design courses", "interior design diploma"],
        "devonshire-hotels": ["luxury hotels derbyshire", "peak district hotels", "country house hotels"],
        "superspace": ["office furniture", "standing desks", "ergonomic chairs"],
        "uno-lighting": ["led strip lights", "kitchen lighting", "led lights"],
        "bright-minds": ["educational toys", "stem toys", "learning resources"],
        "accessories-for-the-home": ["home accessories", "home decor", "decorative accessories"],
        "crowd-control": ["crowd control barriers", "event barriers", "queue barriers"],
        "godshot": ["coffee subscription", "speciality coffee", "coffee beans uk"],
    }
    return keywords


def fetch_trends_for_client(client, keywords):
    """
    Fetch Google Trends data for a client's keywords
    Returns dict with trend data
    """
    log(f"Fetching trends for {client}: {', '.join(keywords)}")

    # This would use the MCP server in production
    # For now, return placeholder structure
    return {
        "client": client,
        "keywords": keywords,
        "timeframe": "today 3-m",
        "geo": "GB",
        "summary": {
            kw: {
                "average": 50.0,
                "max": 75,
                "min": 25,
                "current": 55,
                "trend": "rising"
            }
            for kw in keywords
        }
    }


def analyze_trend_changes(current_trends, previous_trends=None):
    """
    Analyze trend changes vs previous period
    Returns list of significant changes
    """
    changes = []

    for keyword, data in current_trends.get("summary", {}).items():
        # Check for significant trend movement
        if data["trend"] == "rising" and data["current"] > data["average"] * 1.2:
            changes.append({
                "keyword": keyword,
                "type": "significant_increase",
                "current": data["current"],
                "average": data["average"],
                "change_pct": ((data["current"] - data["average"]) / data["average"]) * 100
            })
        elif data["trend"] == "falling" and data["current"] < data["average"] * 0.8:
            changes.append({
                "keyword": keyword,
                "type": "significant_decrease",
                "current": data["current"],
                "average": data["average"],
                "change_pct": ((data["current"] - data["average"]) / data["average"]) * 100
            })

    return changes


def update_client_context(client, trends, changes):
    """
    Update client CONTEXT.md with trend insights
    """
    context_file = PROJECT_ROOT / "clients" / client / "CONTEXT.md"

    if not context_file.exists():
        log(f"Warning: CONTEXT.md not found for {client}")
        return

    # Create trend insight section
    insight_date = datetime.now().strftime("%Y-%m-%d")
    insight_text = f"\n### Search Trend Analysis ({insight_date})\n\n"

    if changes:
        insight_text += "**Significant Changes:**\n\n"
        for change in changes:
            direction = "↑" if change["type"] == "significant_increase" else "↓"
            insight_text += f"- **{change['keyword']}** {direction} {abs(change['change_pct']):.1f}% "
            insight_text += f"(current: {change['current']}, avg: {change['average']:.1f})\n"
    else:
        insight_text += "No significant trend changes detected.\n"

    insight_text += "\n**Current Trends:**\n\n"
    for keyword, data in trends.get("summary", {}).items():
        trend_emoji = "📈" if data["trend"] == "rising" else "📉"
        insight_text += f"- {keyword}: {data['current']}/100 {trend_emoji} ({data['trend']})\n"

    log(f"Would update CONTEXT.md for {client} with trend insights")
    # In production, append to CONTEXT.md or update specific section


def send_alert_email(client, changes):
    """
    Send email alert for significant trend changes
    """
    if not changes:
        return

    alert_text = f"Google Trends Alert: {client}\n\n"
    for change in changes:
        alert_text += f"- {change['keyword']}: {change['change_pct']:.1f}% change\n"

    log(f"Would send alert for {client}:")
    log(alert_text)


def save_trend_history(client, trends):
    """
    Save trend data to history file for comparison
    """
    history_dir = PROJECT_ROOT / "shared" / "data" / "trend-history"
    history_dir.mkdir(parents=True, exist_ok=True)

    history_file = history_dir / f"{client}-{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(history_file, 'w') as f:
        json.dump(trends, f, indent=2)

    log(f"Saved trend history: {history_file}")


def main():
    """Main execution"""
    log("Starting Google Trends Monitor Agent")

    client_keywords = get_client_keywords()
    log(f"Monitoring trends for {len(client_keywords)} clients")

    for client, keywords in client_keywords.items():
        try:
            # Fetch current trends
            trends = fetch_trends_for_client(client, keywords)

            # Analyze changes
            changes = analyze_trend_changes(trends)

            # Save to history
            save_trend_history(client, trends)

            # Update context if significant changes
            if changes:
                update_client_context(client, trends, changes)
                send_alert_email(client, changes)

            log(f"✓ {client}: {len(changes)} significant changes detected")

        except Exception as e:
            log(f"✗ Error processing {client}: {str(e)}")
            continue

    log("Trend monitoring complete")


if __name__ == "__main__":
    main()
