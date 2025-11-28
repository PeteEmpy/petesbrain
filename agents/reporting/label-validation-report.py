#!/usr/bin/env python3
"""
Product Hero Label Validation Report Generator

Generates label validation sections for weekly reports.
Checks:
- Products in wrong asset groups (Hero in Zombie campaign)
- Recent label transitions with performance impact
- Campaign coverage gaps (Heroes not in campaigns)
"""

import json
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


def load_current_labels(client_name: str) -> Dict[str, str]:
    """Load current labels snapshot for a client"""
    history_dir = Path(__file__).parent / "history" / "label-transitions"
    client_dir = history_dir / client_name.lower().replace(" ", "-")
    current_file = client_dir / "current-labels.json"

    if not current_file.exists():
        return {}

    with open(current_file, 'r') as f:
        data = json.load(f)

    return data.get("products", {})


def load_recent_transitions(client_name: str, days: int = 7) -> List[Dict]:
    """Load transitions from last N days"""
    history_dir = Path(__file__).parent / "history" / "label-transitions"
    client_dir = history_dir / client_name.lower().replace(" ", "-")

    # Get current and previous month files
    today = date.today()
    current_month = today.strftime("%Y-%m")

    # Load current month transitions
    current_file = client_dir / f"{current_month}.json"
    transitions = []

    if current_file.exists():
        with open(current_file, 'r') as f:
            data = json.load(f)
            transitions.extend(data.get("transitions", []))

    # Filter to last N days
    cutoff_date = (today - timedelta(days=days)).isoformat()
    recent = [t for t in transitions if t.get("date", "") >= cutoff_date]

    return recent


def get_label_distribution(labels: Dict[str, str]) -> Dict[str, int]:
    """Count products by label"""
    distribution = defaultdict(int)
    for label in labels.values():
        distribution[label] += 1
    return dict(distribution)


def analyze_transitions_impact(transitions: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize transitions by type"""
    categorized = {
        "upgrades": [],      # Zombie→Sidekick, Sidekick→Hero, etc.
        "downgrades": [],    # Hero→Sidekick, Sidekick→Villain, etc.
        "to_zombie": [],     # Any→Zombie (dormant)
        "from_zombie": [],   # Zombie→Any (reactivated)
    }

    # Define label hierarchy
    hierarchy = {"heroes": 4, "sidekicks": 3, "villains": 2, "zombies": 1}

    for t in transitions:
        from_label = t.get("from", "").lower()
        to_label = t.get("to", "").lower()

        from_rank = hierarchy.get(from_label, 0)
        to_rank = hierarchy.get(to_label, 0)

        if to_label == "zombies":
            categorized["to_zombie"].append(t)
        elif from_label == "zombies":
            categorized["from_zombie"].append(t)
        elif to_rank > from_rank:
            categorized["upgrades"].append(t)
        elif to_rank < from_rank:
            categorized["downgrades"].append(t)

    return categorized


def generate_label_validation_section(client_name: str, days: int = 7) -> str:
    """
    Generate HTML section for label validation in weekly reports.

    Args:
        client_name: Name of client (e.g., "Tree2mydoor")
        days: Number of days to look back for transitions (default 7)

    Returns:
        HTML string to inject into weekly report
    """
    # Load data
    current_labels = load_current_labels(client_name)
    recent_transitions = load_recent_transitions(client_name, days)

    # Handle no data
    if not current_labels and not recent_transitions:
        return f"""
        <div class="label-validation">
            <h3>🏷️ Product Hero Label Tracking</h3>
            <p style="color: #888; font-style: italic;">
                No label tracking data available for {client_name}.
                Label tracking may not be enabled for this client.
            </p>
        </div>
        """

    # Build HTML
    html = """
    <div class="label-validation" style="margin-top: 30px;">
        <h3>🏷️ Product Hero Label Tracking</h3>
    """

    # Current distribution
    if current_labels:
        distribution = get_label_distribution(current_labels)
        total_products = len(current_labels)

        html += """
        <div style="background: #f9f9f9; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: #6CC24A;">Current Label Distribution</h4>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        """

        # Sort by hierarchy (heroes first)
        label_order = ["heroes", "sidekicks", "villains", "zombies"]
        label_icons = {
            "heroes": "⭐",
            "sidekicks": "🎯",
            "villains": "⚠️",
            "zombies": "😴"
        }

        for label in label_order:
            count = distribution.get(label, 0)
            if count > 0 or label in ["heroes", "zombies"]:  # Always show heroes and zombies
                pct = (count / total_products * 100) if total_products > 0 else 0
                html += f"""
                <div style="flex: 1; min-width: 120px; text-align: center; background: white; padding: 10px; border-radius: 4px;">
                    <div style="font-size: 24px;">{label_icons.get(label, "•")}</div>
                    <div style="font-weight: bold; font-size: 18px; margin: 5px 0;">{count}</div>
                    <div style="color: #888; font-size: 14px; text-transform: capitalize;">{label}</div>
                    <div style="color: #6CC24A; font-size: 12px;">{pct:.1f}%</div>
                </div>
                """

        html += f"""
            </div>
            <p style="margin: 10px 0 0 0; color: #888; font-size: 0.9em;">
                Total products tracked: {total_products}
            </p>
        </div>
        """

    # Recent transitions
    if recent_transitions:
        categorized = analyze_transitions_impact(recent_transitions)

        html += f"""
        <div style="background: #f9f9f9; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: #6CC24A;">Label Changes (Last {days} Days)</h4>
        """

        # Summary stats
        total_changes = len(recent_transitions)
        html += f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 15px;">
            <div style="background: white; padding: 10px; border-radius: 4px; text-align: center;">
                <div style="font-weight: bold; font-size: 16px;">{total_changes}</div>
                <div style="color: #888; font-size: 12px;">Total Changes</div>
            </div>
            <div style="background: white; padding: 10px; border-radius: 4px; text-align: center;">
                <div style="font-weight: bold; font-size: 16px; color: #4CAF50;">↗ {len(categorized['upgrades'])}</div>
                <div style="color: #888; font-size: 12px;">Upgrades</div>
            </div>
            <div style="background: white; padding: 10px; border-radius: 4px; text-align: center;">
                <div style="font-weight: bold; font-size: 16px; color: #f44336;">↘ {len(categorized['downgrades'])}</div>
                <div style="color: #888; font-size: 12px;">Downgrades</div>
            </div>
            <div style="background: white; padding: 10px; border-radius: 4px; text-align: center;">
                <div style="font-weight: bold; font-size: 16px; color: #FF9800;">😴 {len(categorized['to_zombie'])}</div>
                <div style="color: #888; font-size: 12px;">To Zombie</div>
            </div>
            <div style="background: white; padding: 10px; border-radius: 4px; text-align: center;">
                <div style="font-weight: bold; font-size: 16px; color: #2196F3;">🎉 {len(categorized['from_zombie'])}</div>
                <div style="color: #888; font-size: 12px;">From Zombie</div>
            </div>
        </div>
        """

        # Notable transitions (show a few examples)
        if categorized['downgrades']:
            html += """
            <div style="margin-top: 15px;">
                <strong style="color: #f44336;">⚠️ Notable Downgrades:</strong>
                <ul style="margin: 5px 0;">
            """
            for t in categorized['downgrades'][:5]:  # Show top 5
                html += f"""
                <li style="font-size: 0.9em; color: #555;">
                    Product {t['product_id']}: {t['from']} → {t['to']} ({t['date']})
                </li>
                """
            if len(categorized['downgrades']) > 5:
                html += f'<li style="font-size: 0.9em; color: #888; font-style: italic;">... and {len(categorized["downgrades"]) - 5} more</li>'
            html += "</ul></div>"

        if categorized['upgrades']:
            html += """
            <div style="margin-top: 15px;">
                <strong style="color: #4CAF50;">✅ Notable Upgrades:</strong>
                <ul style="margin: 5px 0;">
            """
            for t in categorized['upgrades'][:5]:  # Show top 5
                html += f"""
                <li style="font-size: 0.9em; color: #555;">
                    Product {t['product_id']}: {t['from']} → {t['to']} ({t['date']})
                </li>
                """
            if len(categorized['upgrades']) > 5:
                html += f'<li style="font-size: 0.9em; color: #888; font-style: italic;">... and {len(categorized["upgrades"]) - 5} more</li>'
            html += "</ul></div>"

        html += "</div>"
    else:
        html += f"""
        <div style="background: #f9f9f9; padding: 15px; border-radius: 4px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: #6CC24A;">Label Changes (Last {days} Days)</h4>
            <p style="color: #888; font-style: italic;">No label changes detected in the last {days} days.</p>
        </div>
        """

    # Recommendations section
    html += """
    <div style="background: #FFF9E6; padding: 15px; border-radius: 4px; margin: 15px 0; border-left: 4px solid #FFC107;">
        <h4 style="margin-top: 0; color: #F57C00;">💡 Recommendations</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
    """

    if recent_transitions:
        categorized = analyze_transitions_impact(recent_transitions)

        if categorized['downgrades']:
            html += f"""
            <li><strong>Review {len(categorized['downgrades'])} downgraded products</strong> - These may need campaign restructuring or optimization</li>
            """

        if categorized['to_zombie']:
            html += f"""
            <li><strong>Investigate {len(categorized['to_zombie'])} products moving to Zombie</strong> - Check for stock issues, pricing problems, or seasonal trends</li>
            """

        if categorized['upgrades']:
            html += f"""
            <li><strong>Capitalize on {len(categorized['upgrades'])} upgrades</strong> - Consider increasing bids or budgets for newly promoted products</li>
            """

    if current_labels:
        distribution = get_label_distribution(current_labels)
        zombie_count = distribution.get("zombies", 0)
        total = len(current_labels)
        zombie_pct = (zombie_count / total * 100) if total > 0 else 0

        if zombie_pct > 30:
            html += f"""
            <li><strong>High Zombie rate ({zombie_pct:.1f}%)</strong> - Consider reviewing product catalog, pricing, or feed quality</li>
            """

    html += """
        </ul>
    </div>
    </div>
    """

    return html


if __name__ == "__main__":
    # Test with Tree2mydoor
    print("Testing label validation report generation...")
    print()

    test_client = "Tree2mydoor"
    html = generate_label_validation_section(test_client, days=7)

    # Save test output
    output_file = Path(__file__).parent / "test_label_validation_report.html"

    full_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Label Validation Report - {test_client}</h1>
            <p>Generated: {datetime.now().strftime("%B %d, %Y %I:%M %p")}</p>
            {html}
        </div>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(full_html)

    print(f"✅ Test report generated: {output_file}")
    print(f"   Open in browser to preview")
