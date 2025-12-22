#!/usr/bin/env python3
"""
Promote Phase 2 Tier 1 Findings to Tracker

Updates tracker to mark the Phase 2 manually-identified Tier 1 terms
with promoted_tier1 status so they appear in interactive deployment script.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from tier2_tracker import load_tracker_data, save_tracker_data

# Phase 2 Tier 1 findings from reports
PHASE2_TIER1_TERMS = {
    'tree2mydoor': [
        {'search_term': 'olive trees', 'clicks': 50, 'cost': 32.47},
        {'search_term': 'tree gifts uk', 'clicks': 32, 'cost': 23.60}
    ],
    # Smythson terms would be added here if we have the full list
    # For now, let's just do tree2mydoor as a test
}

def promote_phase2_findings():
    """Mark Phase 2 findings as promoted_tier1 in tracker"""
    tracker_data = load_tracker_data()

    promoted_count = 0

    for client_slug, terms in PHASE2_TIER1_TERMS.items():
        if client_slug not in tracker_data.get('clients', {}):
            print(f"⚠️  Client {client_slug} not in tracker")
            continue

        client_data = tracker_data['clients'][client_slug]

        for phase2_term in terms:
            # Find matching term in tracker
            for tracker_term in client_data.get('terms', []):
                if tracker_term['search_term'] == phase2_term['search_term']:
                    # Update to promoted_tier1 status
                    tracker_term['status'] = 'promoted_tier1'
                    tracker_term['promoted_date'] = datetime.now().isoformat()
                    tracker_term['clicks'] = phase2_term['clicks']
                    tracker_term['cost'] = phase2_term['cost']
                    tracker_term['deployed'] = False

                    print(f"✅ Promoted: {client_slug} - {phase2_term['search_term']}")
                    promoted_count += 1
                    break
            else:
                # Term not in tracker - add it
                new_term = {
                    'search_term': phase2_term['search_term'],
                    'clicks': phase2_term['clicks'],
                    'cost': phase2_term['cost'],
                    'conversions': 0,
                    'campaign_name': 'Unknown',
                    'match_type': 'Unknown',
                    'added_date': datetime.now().isoformat(),
                    'next_review_date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'promoted_tier1',
                    'promoted_date': datetime.now().isoformat(),
                    'deployed': False,
                    'last_checked': datetime.now().isoformat()
                }
                client_data['terms'].append(new_term)
                print(f"✅ Added: {client_slug} - {phase2_term['search_term']}")
                promoted_count += 1

    # Save updated tracker
    save_tracker_data(tracker_data)

    print(f"\n✅ Promoted {promoted_count} terms to Tier 1 status")
    print("📄 Tracker updated - ready for interactive deployment")

if __name__ == '__main__':
    promote_phase2_findings()
