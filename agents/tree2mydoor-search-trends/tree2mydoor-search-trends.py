#!/usr/bin/env python3
"""
Tree2MyDoor PMAX Search Trends Analyzer
Runs every Friday to identify high-quality Search campaign opportunities
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add shared directory to path for MCP client imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = "14ACzJ8TfJd_8wPreCryno_EkWD6M1RBX2jbXNQgdb84"
SHEET_RANGE = "Sheet1!A1:Z100"
CUSTOMER_ID = "4941701449"  # Tree2MyDoor

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

STATE_FILE = DATA_DIR / "trends-state.json"
BRIEFING_DIR = Path(__file__).parent.parent.parent / "briefing"

# Quality filters (HIGH BAR)
MIN_IMPRESSIONS = 100
MIN_GROWTH_PCT = 200  # +200% or higher
MIN_DECLINE_PCT = -60  # -60% or worse
NOVELTY_WEEKS = 4  # Don't re-flag same opportunity within 4 weeks

# High commercial intent keywords
COMMERCIAL_INTENT_KEYWORDS = [
    'gift', 'birthday', 'anniversary', 'memorial', 'sympathy',
    'bereavement', 'remembrance', 'wedding', 'present'
]


def load_state():
    """Load previous state with historical snapshots and flagged opportunities"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_updated": None,
        "flagged_opportunities": [],
        "historical_snapshots": []
    }


def save_state(state):
    """Save state with historical tracking"""
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def fetch_trending_data():
    """Fetch current trending search categories from Google Sheet"""
    try:
        # Use service account credentials for background access
        from google.oauth2 import service_account

        credentials_path = Path(__file__).parent.parent.parent / "infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json"
        creds = service_account.Credentials.from_service_account_file(
            str(credentials_path),
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_RANGE
        ).execute()

        values = result.get('values', [])

        # Parse into structured data
        trends = []
        for row in values[1:]:  # Skip header
            if len(row) < 6:
                continue

            try:
                trends.append({
                    'campaign': row[0],
                    'category': row[1],
                    'impressions_last_7d': int(row[2]) if row[2] else 0,
                    'impressions_prior_7d': int(row[3]) if row[3] else 0,
                    'diff': int(row[4]) if row[4] else 0,
                    'relative_change_pct': float(row[5].replace('%', '')) if row[5] else 0
                })
            except (ValueError, IndexError):
                continue

        return trends

    except Exception as e:
        print(f"Error fetching trending data: {e}")
        return []


def has_commercial_intent(category):
    """Check if search category has high commercial intent"""
    category_lower = category.lower()
    return any(keyword in category_lower for keyword in COMMERCIAL_INTENT_KEYWORDS)


def was_recently_flagged(category, state):
    """Check if category was flagged in last N weeks"""
    cutoff_date = datetime.now() - timedelta(weeks=NOVELTY_WEEKS)

    for opp in state.get('flagged_opportunities', []):
        if opp['category'] == category:
            first_flagged = datetime.fromisoformat(opp.get('first_flagged', '2000-01-01'))
            if first_flagged > cutoff_date:
                return True

    return False


def analyze_trends(trends, state):
    """Apply quality filters to identify truly notable opportunities"""
    opportunities = []

    for trend in trends:
        category = trend['category']
        impressions = trend['impressions_last_7d']
        change_pct = trend['relative_change_pct']

        # Filter 1: Minimum impression threshold
        if impressions < MIN_IMPRESSIONS:
            continue

        # Filter 2: Significant trend change
        is_growth = change_pct >= MIN_GROWTH_PCT
        is_decline = change_pct <= MIN_DECLINE_PCT and trend['impressions_prior_7d'] >= MIN_IMPRESSIONS

        if not (is_growth or is_decline):
            continue

        # Filter 3: Commercial intent
        if not has_commercial_intent(category):
            continue

        # Filter 4: Novelty (not recently flagged)
        if was_recently_flagged(category, state):
            continue

        # Determine why it's notable
        if is_growth:
            why_notable = f"{abs(change_pct):.0f}% growth surge + high commercial intent"
            recommended_action = f"Consider creating dedicated Search ad group for '{category}'"
        else:
            why_notable = f"{abs(change_pct):.0f}% decline on previously high-volume category"
            recommended_action = f"Investigate cause of decline for '{category}' - feed issue? Seasonality?"

        opportunities.append({
            'category': category,
            'campaign': trend['campaign'],
            'impressions_last_7d': impressions,
            'impressions_prior_7d': trend['impressions_prior_7d'],
            'relative_change_pct': change_pct,
            'why_notable': why_notable,
            'recommended_action': recommended_action,
            'first_flagged': datetime.now().isoformat()
        })

    return opportunities


def create_briefing_output(opportunities):
    """Create briefing file if opportunities found"""
    if not opportunities:
        return

    today = datetime.now().strftime('%Y-%m-%d')
    briefing_file = BRIEFING_DIR / f"tree2mydoor-search-opportunity-{today}.md"

    content = f"""# Tree2MyDoor PMAX Search Trends - {today}

**High-Quality Opportunities Identified** ({len(opportunities)} flagged)

---

"""

    for opp in opportunities:
        change_symbol = "📈" if opp['relative_change_pct'] > 0 else "📉"

        content += f"""## {change_symbol} {opp['category']}

**Trend**: {opp['relative_change_pct']:+.0f}% ({opp['impressions_last_7d']} impressions last 7d, was {opp['impressions_prior_7d']})
**Campaign**: {opp['campaign']}
**Why Notable**: {opp['why_notable']}

**Recommended Action**: {opp['recommended_action']}

---

"""

    content += f"""
**Analysis Date**: {today}
**Quality Filters Applied**:
- Minimum 100+ impressions
- Growth +200% OR Decline -60%+
- High commercial intent only
- New opportunities (not flagged in last 4 weeks)

**Next Steps**: Review these opportunities and decide which warrant creating dedicated Search ad groups.
"""

    with open(briefing_file, 'w') as f:
        f.write(content)

    print(f"✅ Created briefing: {briefing_file}")


def main():
    """Main execution"""
    print(f"🔍 Tree2MyDoor PMAX Search Trends Analyzer - {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Load previous state
    state = load_state()

    # Fetch current trending data
    print("📊 Fetching trending search categories...")
    trends = fetch_trending_data()

    if not trends:
        print("❌ No trending data found")
        return

    print(f"✅ Fetched {len(trends)} trending categories")

    # Store snapshot for historical tracking
    snapshot = {
        'date': datetime.now().isoformat(),
        'trends': trends
    }
    state.setdefault('historical_snapshots', []).append(snapshot)

    # Keep only last 12 weeks of history
    state['historical_snapshots'] = state['historical_snapshots'][-12:]

    # Analyze trends with quality filters
    print("🎯 Applying quality filters...")
    opportunities = analyze_trends(trends, state)

    print(f"✅ Found {len(opportunities)} high-quality opportunities")

    if opportunities:
        # Update state with new opportunities
        state['flagged_opportunities'].extend(opportunities)

        # Create briefing output
        create_briefing_output(opportunities)

        # Print summary
        print("\n📈 Notable Opportunities:")
        for opp in opportunities:
            print(f"  - {opp['category']}: {opp['relative_change_pct']:+.0f}% ({opp['impressions_last_7d']} impr)")
    else:
        print("ℹ️  No new opportunities this week (quality filters applied)")

    # Save state
    save_state(state)
    print(f"💾 State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
