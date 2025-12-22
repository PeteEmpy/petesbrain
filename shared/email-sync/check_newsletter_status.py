#!/usr/bin/env python3
"""Check current status of ppc-newsletters in Gmail"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sync_emails import EmailSyncer

def main():
    syncer = EmailSyncer()

    if not syncer.authenticate():
        print("❌ Authentication failed")
        return 1

    queries = [
        "label:ppc-newsletters in:inbox",
        "label:ppc-newsletters",
        "from:optmyzr.com OR from:zatomarketing.com OR from:mail.beehiiv.com",
    ]

    print("\n" + "=" * 60)
    print("📧 Gmail Newsletter Status Check")
    print("=" * 60 + "\n")

    for query in queries:
        try:
            results = syncer.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10
            ).execute()

            count = len(results.get('messages', []))
            print(f"Query: {query}")
            print(f"Result: {count} emails found")
            print()

        except Exception as e:
            print(f"Error with query '{query}': {e}")
            print()

    return 0

if __name__ == '__main__':
    sys.exit(main())
