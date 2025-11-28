#!/usr/bin/env python3
"""
Weekly Client Strategy Generator

Generates strategic weekly priorities for ALL clients based on:
1. Last week's performance trends (from weekly-client-performance.json)
2. Client CONTEXT.md (goals, priorities, ongoing work)
3. Recent meeting notes and action items
4. Upcoming deadlines and seasonal factors
5. Strategic opportunities and risks

Unlike the daily generator (tactical focus), this takes a STRATEGIC view:
- What needs to be accomplished THIS WEEK?
- What are the strategic priorities for each client?
- What weekly reviews, reports, or planning sessions are needed?
- What experiments or optimizations should be started?

Runs every Monday morning before weekly summary email.
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import anthropic

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
CLIENTS_DIR = PROJECT_ROOT / "clients"

def get_weekend_plans():
    """Check Google Calendar for weekend plans/holidays"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        # Use same OAuth token as daily briefing
        token_path = PROJECT_ROOT / "infrastructure/mcp-servers/google-tasks-mcp-server/token.json"

        if not token_path.exists():
            return None

        creds = Credentials.from_authorized_user_file(
            str(token_path),
            ['https://www.googleapis.com/auth/calendar.readonly']
        )

        service = build('calendar', 'v3', credentials=creds)

        # Get this Friday through Sunday
        today = datetime.now()
        days_until_friday = (4 - today.weekday()) % 7  # 4 = Friday
        friday = today + timedelta(days=days_until_friday)

        # Get ALL of Friday through Sunday 11:59pm (user may take whole Friday off)
        weekend_start = datetime(friday.year, friday.month, friday.day, 0, 0, 0)
        sunday = friday + timedelta(days=2)
        weekend_end = datetime(sunday.year, sunday.month, sunday.day, 23, 59, 59)

        # Query calendar
        events_result = service.events().list(
            calendarId='primary',
            timeMin=weekend_start.isoformat() + 'Z',
            timeMax=weekend_end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return None

        # Look for holidays, travel, time off
        weekend_plans = []
        keywords = ['holiday', 'vacation', 'away', 'break', 'grasmere', 'lake district', 'travel', 'trip']

        for event in events:
            summary = event.get('summary', '').lower()

            # Check for holiday keywords or all-day events
            if any(keyword in summary for keyword in keywords) or 'date' in event['start']:
                weekend_plans.append({
                    'summary': event.get('summary', 'Untitled'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'all_day': 'date' in event['start']
                })

        if weekend_plans:
            return {
                'has_plans': True,
                'friday_date': friday.strftime('%b %d'),
                'plans': weekend_plans
            }

        return None

    except Exception as e:
        print(f"   ⚠️  Could not check calendar: {e}")
        return None

def get_active_clients():
    """Get list of active clients"""
    clients = []

    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir():
            continue
        if client_dir.name.startswith('_'):
            continue
        if client_dir.name in ['README.md']:
            continue

        clients.append({
            'name': client_dir.name,
            'path': client_dir
        })

    return clients

def read_context_file(client_path):
    """Read client CONTEXT.md"""
    context_file = client_path / "CONTEXT.md"

    if not context_file.exists():
        return None

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def get_client_performance(client_name):
    """Get last week's performance data for client"""
    performance_file = PROJECT_ROOT / "shared/data/weekly-client-performance.json"

    if not performance_file.exists():
        return None

    try:
        with open(performance_file, 'r') as f:
            data = json.load(f)

        # Find this client's data
        for client_data in data.get('clients', []):
            if client_data['name'].lower() == client_name.lower():
                return client_data

        return None
    except:
        return None

def get_recent_meetings(client_path, days=14):
    """Get recent meeting notes (last 2 weeks for strategic context)"""
    meetings_dir = client_path / "meeting-notes"

    if not meetings_dir.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    recent_meetings = []

    for meeting_file in meetings_dir.glob("*.md"):
        try:
            mtime = datetime.fromtimestamp(meeting_file.stat().st_mtime)
            if mtime >= cutoff:
                with open(meeting_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                recent_meetings.append({
                    'file': meeting_file.name,
                    'date': mtime,
                    'content': content[:3000]  # More context for strategic planning
                })
        except Exception as e:
            continue

    return sorted(recent_meetings, key=lambda x: x['date'], reverse=True)

def get_recent_completed_work(client_path):
    """Check what was completed last week"""
    completed_file = client_path / "tasks-completed.md"

    if not completed_file.exists():
        return None

    try:
        with open(completed_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get last 2 weeks of entries
        cutoff = datetime.now() - timedelta(days=14)
        recent_entries = []

        # Parse by date headers
        for line in content.split('\n'):
            if line.startswith('## '):
                try:
                    date_str = line.replace('## ', '').strip()
                    entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                    if entry_date >= cutoff:
                        recent_entries.append(line)
                except:
                    pass

        return '\n'.join(recent_entries[:50])  # Last 50 lines
    except:
        return None

def analyze_weekly_strategy(client_name, context, performance, meetings, completed_work):
    """Use Claude to generate strategic weekly priorities"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return []

    # Build strategic analysis prompt
    performance_summary = ""
    if performance:
        curr = performance.get('current_week', {})
        prev = performance.get('previous_week', {})
        changes = performance.get('changes', {})

        performance_summary = f"""
LAST WEEK PERFORMANCE:
- Revenue: £{int(curr.get('revenue', 0)):,} (vs £{int(prev.get('revenue', 0)):,} prior week)
- ROAS: {int(curr.get('roas', 0))}% (vs {int(prev.get('roas', 0))}% prior week)
- Trend: {changes.get('trend', 'unknown')} ({changes.get('revenue_pct', 0):+.1f}% WoW revenue change)
- Summary: {performance.get('summary', 'No summary available')}
"""

        if performance.get('outliers'):
            performance_summary += "\nNOTABLE DAYS:\n"
            for outlier in performance['outliers']:
                reason = outlier.get('reason', outlier.get('type', 'Unknown'))
                performance_summary += f"- {outlier['date']}: {reason}\n"

    meetings_summary = ""
    if meetings:
        meetings_summary = f"\n\nRECENT MEETINGS (last 2 weeks):\n"
        for meeting in meetings[:2]:  # Last 2 meetings
            meetings_summary += f"\n{meeting['file']} ({meeting['date'].strftime('%Y-%m-%d')}):\n"
            meetings_summary += f"{meeting['content'][:1000]}\n"

    completed_summary = ""
    if completed_work:
        completed_summary = f"\n\nCOMPLETED LAST WEEK:\n{completed_work}"

    prompt = f"""You are a strategic account manager analyzing weekly priorities for client: {client_name}

CLIENT CONTEXT & GOALS:
{context if context else "No context available"}
{performance_summary}
{meetings_summary}
{completed_summary}

Based on this information, identify 2-4 STRATEGIC priorities for THIS WEEK.

Think strategically, not tactically:
- What weekly reviews, reports, or planning sessions are needed?
- What strategic goals should progress this week?
- What experiments should be started or evaluated?
- What optimizations have the highest potential impact?
- What client communications or check-ins are needed?
- What planning for next month/quarter needs to start?

Consider:
- Performance trends (up/down/stable)
- Upcoming deadlines or seasonal factors
- Client meetings and commitments
- Strategic opportunities and risks
- Work completed vs work remaining

CRITICAL - Account Maturity and Cross-Account Comparisons:
- CHECK the CONTEXT for "Related Businesses" or "Sister Company" mentions
- If CONTEXT mentions "NEW ACCOUNT" / "BUILDING PHASE" / "RECENTLY CREATED" → DO NOT compare to established sister companies
- If CONTEXT mentions "NOT comparable" or "Different maturity stages" → RESPECT those constraints
- NEVER suggest comparing new/building accounts to mature accounts for optimization ideas
- Each account should be analyzed on its OWN merits and lifecycle stage

Return ONLY a JSON array of strategic priorities (no other text):
[
  {{
    "priority": "Brief strategic priority (not tactical task)",
    "type": "reporting" | "optimization" | "planning" | "communication" | "review" | "experiment",
    "effort": "low" | "medium" | "high",
    "impact": "low" | "medium" | "high",
    "why": "Why this is strategically important this week"
  }}
]

If client genuinely needs no strategic attention this week, return: []

IMPORTANT: Return ONLY valid JSON, no markdown, no explanations."""

    try:
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=800,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text.strip()

        # Extract JSON
        if response_text.startswith('['):
            priorities = json.loads(response_text)
            return priorities
        else:
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                priorities = json.loads(json_match.group(0))
                return priorities

        return []

    except Exception as e:
        print(f"   ⚠️  Error analyzing strategy: {e}")
        return []

def generate_weekly_strategy():
    """Main function to generate weekly strategic priorities"""

    print("=" * 80)
    print("WEEKLY CLIENT STRATEGY GENERATOR")
    print("=" * 80)
    print()
    print(f"Analyzing strategic priorities for week of {datetime.now().strftime('%B %d, %Y')}")
    print()

    # Check for weekend plans/holidays
    print("📅 Checking calendar for weekend plans...")
    weekend_plans = get_weekend_plans()
    if weekend_plans:
        plans_list = weekend_plans['plans']
        print(f"   🏖️  Weekend plans found: {plans_list[0]['summary']}")
        print(f"   ⚠️  Consider finishing by lunchtime Friday ({weekend_plans['friday_date']})")
    else:
        print(f"   ✓ No weekend plans detected - full week available")
    print()

    # Get all active clients
    clients = get_active_clients()
    print(f"📋 Found {len(clients)} active clients")
    print()

    all_priorities = []
    clients_with_work = 0

    for i, client in enumerate(clients, 1):
        client_name = client['name']
        client_path = client['path']

        print(f"[{i}/{len(clients)}] Analyzing {client_name}...")

        # Gather strategic context
        context = read_context_file(client_path)
        performance = get_client_performance(client_name)
        meetings = get_recent_meetings(client_path)
        completed = get_recent_completed_work(client_path)

        # Analyze weekly strategy
        priorities = analyze_weekly_strategy(client_name, context, performance, meetings, completed)

        if priorities:
            clients_with_work += 1
            print(f"   ✓ {len(priorities)} strategic priorit{'y' if len(priorities) == 1 else 'ies'} identified")
            for priority in priorities:
                priority['client'] = client_name
                all_priorities.append(priority)
        else:
            print(f"   → Minimal strategic attention needed")

        print()

    # Group by type and impact
    by_type = {}
    for priority in all_priorities:
        type_key = priority.get('type', 'other')
        if type_key not in by_type:
            by_type[type_key] = []
        by_type[type_key].append(priority)

    high_impact = [p for p in all_priorities if p.get('impact') == 'high']
    medium_impact = [p for p in all_priorities if p.get('impact') == 'medium']
    low_impact = [p for p in all_priorities if p.get('impact') == 'low']

    # Display summary
    print("=" * 80)
    print("WEEKLY STRATEGY SUMMARY")
    print("=" * 80)
    print()
    print(f"**{clients_with_work}/{len(clients)} clients** need strategic attention this week")
    print(f"**{len(all_priorities)} total priorities** identified")
    print()

    if high_impact:
        print(f"🔴 **HIGH IMPACT**: {len(high_impact)} priorities")
        for priority in high_impact[:10]:
            print(f"   • [{priority['client']}] {priority['priority']}")
        print()

    if medium_impact:
        print(f"🟡 **MEDIUM IMPACT**: {len(medium_impact)} priorities")
        for priority in medium_impact[:5]:
            print(f"   • [{priority['client']}] {priority['priority']}")
        if len(medium_impact) > 5:
            print(f"   ... and {len(medium_impact) - 5} more")
        print()

    if by_type:
        print("📊 **BY TYPE**:")
        for type_name, priorities in sorted(by_type.items(), key=lambda x: -len(x[1])):
            print(f"   {type_name}: {len(priorities)}")
        print()

    # Save to JSON
    output_file = PROJECT_ROOT / "shared/data/weekly-client-strategy.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        'generated_at': datetime.now().isoformat(),
        'week_of': datetime.now().strftime('%Y-%m-%d'),
        'total_clients': len(clients),
        'clients_with_priorities': clients_with_work,
        'total_priorities': len(all_priorities),
        'priorities': all_priorities,
        'by_type': {k: len(v) for k, v in by_type.items()},
        'by_impact': {
            'high': len(high_impact),
            'medium': len(medium_impact),
            'low': len(low_impact)
        }
    }

    # Add weekend plans if detected
    if weekend_plans:
        output_data['weekend_plans'] = {
            'has_plans': True,
            'friday_date': weekend_plans['friday_date'],
            'summary': weekend_plans['plans'][0]['summary'] if weekend_plans['plans'] else 'Weekend plans',
            'all_plans': weekend_plans['plans']
        }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 Strategy saved to: {output_file}")
    print()

    return all_priorities

if __name__ == "__main__":
    try:
        generate_weekly_strategy()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
