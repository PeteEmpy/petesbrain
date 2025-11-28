#!/usr/bin/env python3
"""
Analyze personal email scan results and categorize by usefulness
"""

import json
from pathlib import Path
from collections import defaultdict

results_file = Path('/Users/administrator/Documents/PetesBrain/data/cache/personal-email-scan-results.json')

with open(results_file) as f:
    findings = json.load(f)

print("=" * 80)
print("SENT EMAIL SCAN ANALYSIS - CLIENT DATA & GOOGLE SHEETS")
print("=" * 80)
print()

# Group by client
client_emails = defaultdict(list)
sheets_by_client = defaultdict(list)
unique_sheets = set()

for finding in findings:
    clients = finding.get('clients', [])
    sheets = finding.get('sheets_links', [])

    for client in clients:
        client_emails[client].append(finding)

    if sheets:
        for sheet in sheets:
            unique_sheets.add(sheet)
            if clients:
                for client in clients:
                    sheets_by_client[client].append({
                        'sheet': sheet,
                        'subject': finding['subject'],
                        'date': finding['date']
                    })
            else:
                # No client tagged - general/system sheet
                sheets_by_client['_system'].append({
                    'sheet': sheet,
                    'subject': finding['subject'],
                    'date': finding['date']
                })

# Categorize sheets by type
automated_patterns = [
    'trending search',
    'pmax placement',
    'negative keyword',
    'best sellers not eligible',
    'daily briefing',
    'weekly summary',
    'performance alert',
    'script alert'
]

manual_sheets = []
automated_sheets = []

for sheet in unique_sheets:
    # Find email with this sheet
    sheet_info = None
    for finding in findings:
        if sheet in finding.get('sheets_links', []):
            sheet_info = finding
            break

    if sheet_info:
        subject_lower = sheet_info['subject'].lower()
        is_automated = any(pattern in subject_lower for pattern in automated_patterns)

        if is_automated:
            automated_sheets.append({
                'url': sheet,
                'subject': sheet_info['subject'],
                'date': sheet_info['date']
            })
        else:
            manual_sheets.append({
                'url': sheet,
                'subject': sheet_info['subject'],
                'date': sheet_info['date'],
                'clients': sheet_info.get('clients', [])
            })

print(f"📊 SUMMARY")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"Total sent emails analyzed: {len(findings)}")
print(f"Emails with client mentions: {len([f for f in findings if f.get('clients')])}")
print(f"Unique Google Sheets found: {len(unique_sheets)}")
print(f"  - Automated reports: {len(automated_sheets)}")
print(f"  - Manual/client data: {len(manual_sheets)}")
print()

print(f"📈 MANUAL/CLIENT GOOGLE SHEETS - WORTH SAVING")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
if manual_sheets:
    for i, sheet in enumerate(manual_sheets, 1):
        print(f"\n{i}. {sheet['subject']}")
        print(f"   Date: {sheet['date']}")
        if sheet['clients']:
            print(f"   Clients: {', '.join(sheet['clients'])}")
        print(f"   URL: {sheet['url']}")
else:
    print("No manual client data sheets found")

print()
print()
print(f"🤖 AUTOMATED REPORT SHEETS - LIKELY NOT WORTH SAVING")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"(These are generated daily/weekly by scripts)")
print()
for i, sheet in enumerate(automated_sheets[:5], 1):  # Show first 5
    print(f"{i}. {sheet['subject']}")
    print(f"   {sheet['url'][:80]}...")
print(f"\n... and {len(automated_sheets) - 5} more automated sheets")

print()
print()
print(f"📧 EMAILS BY CLIENT - CLIENT-RELEVANT SENT EMAILS")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Sort clients by number of emails
sorted_clients = sorted(client_emails.items(), key=lambda x: len(x[1]), reverse=True)

for client, emails in sorted_clients[:15]:  # Top 15 clients
    print(f"\n{client.upper()}: {len(emails)} emails")

    # Show recent emails with sheets
    emails_with_sheets = [e for e in emails if e.get('sheets_links')]
    if emails_with_sheets:
        print(f"  Emails with Google Sheets: {len(emails_with_sheets)}")
        for email in emails_with_sheets[:3]:  # Show first 3
            print(f"    - {email['subject'][:60]}")
            for sheet in email['sheets_links']:
                print(f"      📊 {sheet[:70]}...")

print()
print()
print(f"💡 RECOMMENDATIONS")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()
print(f"1. MANUAL SHEETS ({len(manual_sheets)} found):")
print(f"   These appear to be custom client data/analysis")
print(f"   → Review each one and download/save to appropriate client folder")
print(f"   → Consider adding links to client CONTEXT.md 'Quick Reference' section")
print()
print(f"2. AUTOMATED SHEETS ({len(automated_sheets)} found):")
print(f"   These are daily/weekly automated reports")
print(f"   → No need to save - they regenerate automatically")
print(f"   → Data already captured in emails (which are synced to client folders)")
print()
print(f"3. CLIENT EMAILS (158 found with client mentions):")
print(f"   Your sent emails are already being synced to client folders")
print(f"   → Email sync system handles this automatically")
print(f"   → Check clients/[client-name]/emails/ for sent email archive")
print()
print(f"NEXT STEPS:")
print(f"   1. Review the {len(manual_sheets)} manual sheets above")
print(f"   2. Open each URL and determine if data should be saved locally")
print(f"   3. For valuable sheets, either:")
print(f"      a) Download as CSV/Excel to client folder")
print(f"      b) Add sheet link to client CONTEXT.md")
print()
