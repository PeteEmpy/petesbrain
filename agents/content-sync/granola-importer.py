#!/usr/bin/env python3
"""
Granola Sync Daemon

Background service that automatically imports new Granola meetings at regular intervals.

Usage with venv:
    source venv/bin/activate
    python3 sync_daemon.py
"""

import signal
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

from import_meeting import MeetingImporter

# Email reporter (optional)
try:
    from email_reporter import EmailReporter
    EMAIL_AVAILABLE = True
except:
    EMAIL_AVAILABLE = False


# Configuration
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
LOG_FILE = Path.home() / ".petesbrain-granola-importer.log"


class SyncDaemon:
    """Background daemon for continuous meeting import."""

    def __init__(self, check_interval: int = CHECK_INTERVAL, enable_email: bool = True):
        """
        Initialize sync daemon.

        Args:
            check_interval: Seconds between checks (default: 300 = 5 minutes)
            enable_email: Whether to send email alerts (requires config.yaml)
        """
        self.check_interval = check_interval
        self.running = False
        self.importer = None
        self.enable_email = enable_email

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE)
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Setup email reporter if available
        self.email_reporter = None
        if enable_email and EMAIL_AVAILABLE:
            try:
                self.email_reporter = EmailReporter()
                self.logger.info(f"✓ Email alerts enabled for: {self.email_reporter.config['email']['recipient']}")
            except (FileNotFoundError, ValueError):
                self.logger.info("Email alerts disabled (config.yaml not found or email disabled)")

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        signal_name = signal.Signals(signum).name
        self.logger.info(f"Received {signal_name}, shutting down gracefully...")
        self.running = False

    def _initialize_importer(self):
        """Initialize the meeting importer (with retry logic)."""
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                self.importer = MeetingImporter()
                self.logger.info("✓ Successfully initialized Granola API connection")
                return True

            except FileNotFoundError as e:
                self.logger.error(f"✗ Granola credentials not found: {e}")
                self.logger.error("Please ensure Granola desktop app is installed and you're logged in.")
                return False

            except Exception as e:
                self.logger.warning(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("✗ Failed to initialize after maximum retries")
                    return False

        return False

    def _sync_meetings(self):
        """Perform a single sync operation."""
        try:
            self.logger.info("🔄 Starting sync cycle...")

            # Import meetings from last 7 days (catches any missed ones)
            count = self.importer.import_recent(days=7, limit=50)

            if count > 0:
                self.logger.info(f"✓ Imported {count} new meetings")
            else:
                self.logger.info("✓ No new meetings to import")

            return True

        except Exception as e:
            self.logger.error(f"✗ Sync failed: {e}")

            # Send email alert if enabled
            if self.email_reporter:
                try:
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    self.email_reporter.send_sync_failure_alert(error_msg)
                    self.logger.info("✓ Sent failure alert email")
                except Exception as email_err:
                    self.logger.warning(f"Could not send email alert: {email_err}")

            return False

    def start(self):
        """Start the sync daemon."""
        self.logger.info("=" * 70)
        self.logger.info("Granola Meeting Sync Daemon")
        self.logger.info("=" * 70)
        self.logger.info(f"Check interval: {self.check_interval} seconds ({self.check_interval // 60} minutes)")
        self.logger.info(f"Log file: {LOG_FILE}")
        self.logger.info("")

        # Initialize importer
        if not self._initialize_importer():
            self.logger.error("Failed to start daemon - initialization error")
            sys.exit(1)

        self.running = True
        sync_count = 0

        self.logger.info("✓ Daemon started successfully")
        self.logger.info("Press Ctrl+C to stop")
        self.logger.info("")

        # Initial sync
        self._sync_meetings()
        sync_count += 1

        # Main loop
        while self.running:
            try:
                # Calculate next sync time
                next_sync = datetime.now().timestamp() + self.check_interval
                next_sync_time = datetime.fromtimestamp(next_sync).strftime("%H:%M:%S")

                self.logger.info(f"💤 Sleeping until next sync at {next_sync_time}")

                # Sleep but check running flag periodically for responsive shutdown
                sleep_interval = 10  # Check every 10 seconds
                elapsed = 0

                while elapsed < self.check_interval and self.running:
                    sleep_time = min(sleep_interval, self.check_interval - elapsed)
                    time.sleep(sleep_time)
                    elapsed += sleep_time

                if not self.running:
                    break

                # Perform sync
                self._sync_meetings()
                sync_count += 1

            except KeyboardInterrupt:
                # Already handled by signal handler, but catch here to prevent traceback
                break

            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                self.logger.info("Continuing after error...")
                time.sleep(60)  # Wait a minute before retrying

        # Cleanup
        self.logger.info("")
        self.logger.info(f"✓ Daemon stopped after {sync_count} sync cycles")
        self.logger.info("=" * 70)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Background daemon for automatic Granola meeting import"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=CHECK_INTERVAL,
        help=f"Check interval in seconds (default: {CHECK_INTERVAL})"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (no continuous loop)"
    )

    args = parser.parse_args()

    daemon = SyncDaemon(check_interval=args.interval)

    if args.once:
        # Run a single sync and exit
        if daemon._initialize_importer():
            daemon._sync_meetings()
        sys.exit(0)
    else:
        # Start continuous daemon
        daemon.start()


if __name__ == "__main__":
    main()
