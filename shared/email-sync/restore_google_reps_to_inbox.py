#!/usr/bin/env python3
"""
Restore google-reps emails to inbox (undo archive)
These emails may contain meeting invites and should stay in inbox
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sync_emails import EmailSyncer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Restore google-reps emails to inbox by adding INBOX label."""

    logger.info("=" * 60)
    logger.info("📬 Restoring Google Reps Emails to Inbox")
    logger.info("=" * 60)

    # Initialize syncer
    syncer = EmailSyncer()

    # Authenticate
    if not syncer.authenticate():
        logger.error("❌ Authentication failed")
        return 1

    # Query for google-reps emails NOT in inbox (i.e., archived)
    query = "label:google-reps -label:inbox"
    logger.info(f"Searching for: {query}")

    try:
        results = syncer.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=500
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            logger.info("✅ No google-reps emails to restore - all in inbox already!")
            return 0

        logger.info(f"Found {len(messages)} google-reps emails to restore")
        logger.info("")

        restored_count = 0
        failed_count = 0

        for msg_ref in messages:
            msg_id = msg_ref['id']

            # Get subject for display
            try:
                message = syncer.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='metadata',
                    metadataHeaders=['Subject']
                ).execute()

                headers = {h['name']: h['value'] for h in message['payload']['headers']}
                subject = headers.get('Subject', 'No Subject')

                # Restore to inbox by adding INBOX label
                syncer.service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={'addLabelIds': ['INBOX']}
                ).execute()

                logger.info(f"  ✓ Restored: {subject[:60]}")
                restored_count += 1

            except Exception as e:
                logger.error(f"  ✗ Error processing {msg_id}: {e}")
                failed_count += 1

        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ Restore Complete")
        logger.info(f"  - Restored: {restored_count}")
        logger.info(f"  - Failed: {failed_count}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
