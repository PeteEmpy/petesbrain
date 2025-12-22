#!/usr/bin/env python3
"""Count how many newsletters need archiving"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sync_emails import EmailSyncer

def main():
    syncer = EmailSyncer()

    if not syncer.authenticate():
        print("❌ Authentication failed")
        return 1

    labels = {
        "ppc-newsletters": "label:ppc-newsletters in:inbox",
        "AI_news": "label:AI_news in:inbox",
        "google-reps": "label:google-reps in:inbox"
    }

    print("\n" + "=" * 70)
    print("📊 Newsletter Archive Preview")
    print("=" * 70 + "\n")

    total = 0

    for label, query in labels.items():
        try:
            results = syncer.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=500
            ).execute()

            count = len(results.get('messages', []))
            total += count

            status = "✅" if count == 0 else f"📦 {count} to archive"
            print(f"{label:20s} {status}")

        except Exception as e:
            print(f"{label:20s} ❌ Error: {e}")

    print("\n" + "-" * 70)
    print(f"{'TOTAL':20s} 📦 {total} newsletters will be archived")
    print("=" * 70 + "\n")

    return 0

if __name__ == '__main__':
    sys.exit(main())
