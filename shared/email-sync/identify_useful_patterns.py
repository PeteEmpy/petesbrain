#!/usr/bin/env python3
"""
Identify useful self-sent email patterns for client analysis
"""

import json
from pathlib import Path
from collections import defaultdict
import re

results_file = Path('/Users/administrator/Documents/PetesBrain/data/cache/personal-email-scan-results.json')

with open(results_file) as f:
    findings = json.load(f)

# Categorize emails by subject pattern
patterns = defaultdict(list)

for finding in findings:
    subject = finding['subject']

    # Extract pattern (remove dates, client names, numbers)
    pattern = subject
    pattern = re.sub(r'\d{4}-\d{2}-\d{2}', 'YYYY-MM-DD', pattern)
    pattern = re.sub(r'\d+', 'N', pattern)
    pattern = re.sub(r'(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)', 'DAY', pattern)
    pattern = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)', 'MONTH', pattern)

    patterns[pattern].append({
        'subject': subject,
        'date': finding['date'],
        'clients': finding.get('clients', []),
        'has_sheets': len(finding.get('sheets_links', [])) > 0
    })

# Sort by frequency
sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)

print("=" * 100)
print("USEFUL EMAIL PATTERNS FOR CLIENT ANALYSIS")
print("=" * 100)
print()

# Analyze each pattern for usefulness
useful_patterns = []
operational_patterns = []

for pattern, emails in sorted_patterns:
    count = len(emails)
    has_client = any(e.get('clients') for e in emails)
    has_sheets = any(e.get('has_sheets') for e in emails)

    # Determine usefulness based on pattern
    pattern_lower = pattern.lower()

    # High value patterns - historical record of actions/changes
    if any(keyword in pattern_lower for keyword in [
        'negatives added',
        'best sellers not eligible',
        'disapproved',
        'budget',
        'roas',
        'change history',
        'performance report',
        'alert',
        'q4 dashboard',
        'q4 strategy',
        'optimization'
    ]):
        category = "HIGH VALUE"
        useful_patterns.append((pattern, emails, category))

    # Medium value patterns - useful context
    elif any(keyword in pattern_lower for keyword in [
        'briefing',
        'summary',
        'week ahead',
        'meeting',
        'update'
    ]):
        category = "MEDIUM VALUE"
        useful_patterns.append((pattern, emails, category))

    # Operational patterns - not archival
    else:
        category = "OPERATIONAL"
        operational_patterns.append((pattern, emails, category))

print("🔥 HIGH VALUE PATTERNS - Archive to Client Folders")
print("=" * 100)
print("(Historical record of changes, issues, optimizations)")
print()

for pattern, emails, category in [p for p in useful_patterns if p[2] == "HIGH VALUE"]:
    count = len(emails)
    clients = set()
    for e in emails:
        clients.update(e.get('clients', []))

    has_sheets = any(e.get('has_sheets') for e in emails)

    print(f"📧 Pattern: {pattern}")
    print(f"   Count: {count} emails")
    if clients:
        print(f"   Clients: {', '.join(sorted(clients)[:10])}{'...' if len(clients) > 10 else ''}")
    if has_sheets:
        print(f"   ✓ Contains Google Sheets links")

    # Show sample
    sample = emails[0]
    print(f"   Example: {sample['subject']}")

    # Explain why useful
    pattern_lower = pattern.lower()
    if 'negatives added' in pattern_lower:
        print(f"   📊 Value: Track negative keyword exclusions over time (explains traffic drops)")
    elif 'best sellers not eligible' in pattern_lower:
        print(f"   📊 Value: Product feed issues that explain performance drops")
    elif 'disapproved' in pattern_lower:
        print(f"   📊 Value: Ad disapprovals - critical for explaining lost impressions")
    elif 'budget' in pattern_lower or 'roas' in pattern_lower:
        print(f"   📊 Value: Strategic budget/bid changes - shows decision timeline")
    elif 'change history' in pattern_lower:
        print(f"   📊 Value: Complete account change log")
    elif 'performance report' in pattern_lower:
        print(f"   📊 Value: Performance snapshots for trend analysis")
    elif 'q4' in pattern_lower:
        print(f"   📊 Value: Strategic campaign tracking and status")
    elif 'alert' in pattern_lower:
        print(f"   📊 Value: Performance anomalies and issues requiring attention")

    print()

print()
print("📊 MEDIUM VALUE PATTERNS - Consider Archiving")
print("=" * 100)
print("(Summaries and context - useful but not critical)")
print()

for pattern, emails, category in [p for p in useful_patterns if p[2] == "MEDIUM VALUE"]:
    count = len(emails)
    clients = set()
    for e in emails:
        clients.update(e.get('clients', []))

    print(f"📧 Pattern: {pattern}")
    print(f"   Count: {count} emails")
    if clients:
        print(f"   Clients: {', '.join(sorted(clients)[:10])}{'...' if len(clients) > 10 else ''}")
    sample = emails[0]
    print(f"   Example: {sample['subject']}")
    print()

print()
print("🤖 OPERATIONAL PATTERNS - Don't Archive")
print("=" * 100)
print("(Daily reports that regenerate - not historical value)")
print()

for pattern, emails, category in operational_patterns[:10]:  # Top 10
    count = len(emails)
    sample = emails[0]
    print(f"📧 {pattern} ({count} emails)")
    print(f"   Example: {sample['subject']}")

print()
print()
print("=" * 100)
print("RECOMMENDED AUTO-LABELING RULES")
print("=" * 100)
print()
print("Add these patterns to auto-label-config.yaml to automatically save to client folders:")
print()

# Generate specific patterns for auto-labeling
auto_label_patterns = [
    {
        'pattern': 'Negatives added for {client}',
        'label': 'client/{client}',
        'reason': 'Historical negative keyword log'
    },
    {
        'pattern': '[MCC Script Alert] Best sellers not eligible for Shopping - {client}',
        'label': 'client/{client}',
        'reason': 'Product feed issue alerts'
    },
    {
        'pattern': '[Script Alert] Best sellers not eligible for Shopping - {client}',
        'label': 'client/{client}',
        'reason': 'Product feed issue alerts'
    },
    {
        'pattern': '{client} Q4 Dashboard',
        'label': 'client/{client}',
        'reason': 'Strategic tracking dashboard'
    },
    {
        'pattern': '{client} Google Ads Performance Report',
        'label': 'client/{client}',
        'reason': 'Performance snapshots'
    },
    {
        'pattern': '{client} Google Ads Change History',
        'label': 'client/{client}',
        'reason': 'Account change log'
    },
    {
        'pattern': '{client} Budget Optimization',
        'label': 'client/{client}',
        'reason': 'Budget strategy recommendations'
    },
    {
        'pattern': 'Performance Alerts',
        'label': 'roksys',
        'reason': 'Cross-client performance monitoring (contains multiple clients)'
    },
    {
        'pattern': '[MCC Alert] Disapproved Ads and Extensions Report',
        'label': 'roksys',
        'reason': 'Cross-client ad disapproval tracking'
    }
]

for rule in auto_label_patterns:
    print(f"Pattern: {rule['pattern']}")
    print(f"Label:   {rule['label']}")
    print(f"Reason:  {rule['reason']}")
    print()

print()
print("=" * 100)
print("NEXT STEPS")
print("=" * 100)
print()
print("1. Review HIGH VALUE patterns above")
print("2. Update shared/email-sync/auto-label-config.yaml with new patterns")
print("3. Run email sync to retroactively label and save these emails")
print("4. These emails will then be automatically saved to client folders")
print()
