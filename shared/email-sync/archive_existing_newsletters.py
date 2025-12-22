#!/usr/bin/env python3
"""
One-time script to archive existing ppc-newsletters that are already synced
Run this once to clean up existing newsletters from inbox
"""

import sys
from pathlib import Path

# Add parent directory to path to import sync_emails
sys.path.insert(0, str(Path(__file__).parent))

from sync_emails import EmailSyncer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Archive all existing newsletters (ppc-newsletters, AI_news, google-reps)."""

    logger.info("=" * 60)
    logger.info("📦 Archiving All Existing Newsletters")
    logger.info("=" * 60)

    # Initialize syncer
    syncer = EmailSyncer()

    # Authenticate
    if not syncer.authenticate():
        logger.error("❌ Authentication failed")
        return 1

    # Query for all newsletter labels
    query = "label:ppc-newsletters OR label:AI_news OR label:google-reps"
    logger.info(f"Searching for: {query}")

    try:
        results = syncer.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=500
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            logger.info("✅ No newsletters to archive - inbox already clean!")
            return 0

        logger.info(f"Found {len(messages)} newsletters to archive")
        logger.info("")

        archived_count = 0
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

                # Archive it
                if syncer._archive_email(msg_id):
                    logger.info(f"  ✓ Archived: {subject[:60]}")
                    archived_count += 1
                else:
                    logger.error(f"  ✗ Failed: {subject[:60]}")
                    failed_count += 1

            except Exception as e:
                logger.error(f"  ✗ Error processing {msg_id}: {e}")
                failed_count += 1

        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ Archive Complete")
        logger.info(f"  - Archived: {archived_count}")
        logger.info(f"  - Failed: {failed_count}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
