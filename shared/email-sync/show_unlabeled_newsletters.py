#!/usr/bin/env python3
"""Show newsletter emails that don't have the ppc-newsletters label yet"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sync_emails import EmailSyncer

def main():
    syncer = EmailSyncer()

    if not syncer.authenticate():
        print("❌ Authentication failed")
        return 1

    # Query for newsletters WITHOUT the ppc-newsletters label
    query = "(from:optmyzr.com OR from:zatomarketing.com OR from:mail.beehiiv.com OR from:ppchero.com OR from:searchengineland.com) -label:ppc-newsletters"

    try:
        results = syncer.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=20
        ).execute()

        messages = results.get('messages', [])

        print("\n" + "=" * 70)
        print(f"📧 Unlabeled Newsletters ({len(messages)} found)")
        print("=" * 70 + "\n")

        if not messages:
            print("✅ No unlabeled newsletters - all caught!")
            return 0

        for msg_ref in messages:
            try:
                message = syncer.service.users().messages().get(
                    userId='me',
                    id=msg_ref['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject']
                ).execute()

                headers = {h['name']: h['value'] for h in message['payload']['headers']}
                from_addr = headers.get('From', 'Unknown')
                subject = headers.get('Subject', 'No Subject')

                print(f"From: {from_addr}")
                print(f"Subject: {subject}")
                print()

            except Exception as e:
                print(f"Error: {e}")
                print()

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
