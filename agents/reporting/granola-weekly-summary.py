#!/usr/bin/env python3
"""
Weekly Summary Sender

Standalone script to send weekly meeting import summary.
Can be run manually or scheduled via cron/LaunchAgent.

Usage:
    python3 send_weekly_summary.py
"""

import sys
from pathlib import Path

from email_reporter import EmailReporter


def main():
    """Send weekly summary email."""
    print("=" * 60)
    print("Granola Meeting Importer - Weekly Summary")
    print("=" * 60)
    print()

    try:
        # Initialize email reporter
        reporter = EmailReporter()
        print(f"✓ Email configured for: {reporter.config['email']['recipient']}")
        print()

        # Send weekly summary
        print("📧 Sending weekly summary email...")
        success = reporter.send_weekly_summary()

        if success:
            print("✓ Weekly summary sent successfully!")
            print()
            print("Check your email inbox for the summary.")
            return 0
        else:
            print("✗ Failed to send email. Check SMTP settings in config.yaml")
            return 1

    except FileNotFoundError as e:
        print(f"✗ Configuration Error: {e}")
        print()
        print("Setup Instructions:")
        print("1. Copy config.example.yaml to config.yaml")
        print("2. Edit config.yaml with your email settings")
        print("3. Run this script again")
        print()
        print("For Gmail users:")
        print("- Use an App Password: https://support.google.com/accounts/answer/185833")
        print("- Don't use your regular Gmail password")
        return 1

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
