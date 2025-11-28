"""
Email Reporter

Sends email summaries and alerts for the Granola Meeting Importer.
"""

import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class EmailReporter:
    """Handles email notifications for meeting imports."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize email reporter.

        Args:
            config_path: Path to config.yaml (defaults to config.yaml in tool directory)
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"

        self.config_path = config_path
        self.config = self._load_config()

        # Validate config
        if not self.config.get("email", {}).get("enabled", False):
            raise ValueError("Email is not enabled in config.yaml")

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found at {self.config_path}. "
                "Please copy config.example.yaml to config.yaml and configure it."
            )

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _send_email(self, subject: str, body_html: str, body_text: Optional[str] = None):
        """
        Send an email via SMTP.

        Args:
            subject: Email subject
            body_html: HTML email body
            body_text: Plain text fallback (optional)
        """
        email_config = self.config["email"]
        smtp_config = email_config["smtp"]

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_config["username"]
        msg["To"] = email_config["recipient"]

        # Add plain text version
        if body_text:
            part1 = MIMEText(body_text, "plain")
            msg.attach(part1)

        # Add HTML version
        part2 = MIMEText(body_html, "html")
        msg.attach(part2)

        # Send email
        try:
            if smtp_config.get("use_tls", True):
                server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])

            server.login(smtp_config["username"], smtp_config["password"])
            server.sendmail(
                smtp_config["username"],
                email_config["recipient"],
                msg.as_string()
            )
            server.quit()

            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def _load_import_history(self) -> Dict:
        """Load import history from .import_history.json."""
        history_file = Path(__file__).parent / ".import_history.json"

        if not history_file.exists():
            return {"imported": {}}

        with open(history_file, 'r') as f:
            return json.load(f)

    def _get_recent_imports(self, days: int = 7) -> List[Tuple[str, Dict]]:
        """
        Get imports from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of (document_id, import_data) tuples
        """
        history = self._load_import_history()
        cutoff = datetime.now() - timedelta(days=days)

        recent = []
        for doc_id, import_data in history.get("imported", {}).items():
            imported_at = import_data.get("imported_at", "")
            try:
                import_time = datetime.fromisoformat(imported_at)
                if import_time >= cutoff:
                    recent.append((doc_id, import_data))
            except ValueError:
                continue

        # Sort by import time (newest first)
        recent.sort(key=lambda x: x[1].get("imported_at", ""), reverse=True)
        return recent

    def _group_by_client(self, imports: List[Tuple[str, Dict]]) -> Dict[str, List[Dict]]:
        """
        Group imports by client.

        Args:
            imports: List of (document_id, import_data) tuples

        Returns:
            Dictionary mapping client names to list of imports
        """
        grouped = {}

        for doc_id, import_data in imports:
            client = import_data.get("client")
            if not client:
                client = "_unassigned"

            if client not in grouped:
                grouped[client] = []

            # Extract filename from path
            file_path = import_data.get("file_path", "")
            filename = Path(file_path).name if file_path else "Unknown"

            grouped[client].append({
                "filename": filename,
                "file_path": file_path,
                "imported_at": import_data.get("imported_at", "")
            })

        return grouped

    def _format_client_name(self, client_slug: str) -> str:
        """Convert client slug to display name."""
        if client_slug == "_unassigned":
            return "⚠️ Unassigned"
        return client_slug.replace("-", " ").title()

    def send_weekly_summary(self) -> bool:
        """
        Send weekly summary email of imported meetings.

        Returns:
            True if email sent successfully, False otherwise
        """
        # Get imports from last 7 days
        recent_imports = self._get_recent_imports(days=7)

        if not recent_imports:
            # No imports to report
            return True

        # Group by client
        grouped = self._group_by_client(recent_imports)

        # Build email content
        subject = f"📊 Weekly Meeting Import Summary - {datetime.now().strftime('%B %d, %Y')}"

        # HTML body
        html_parts = [
            "<html><body style='font-family: Arial, sans-serif;'>",
            f"<h2>Weekly Meeting Import Summary</h2>",
            f"<p><strong>Period:</strong> Last 7 days</p>",
            f"<p><strong>Total meetings imported:</strong> {len(recent_imports)}</p>",
            "<hr>",
        ]

        # Plain text body
        text_parts = [
            "WEEKLY MEETING IMPORT SUMMARY",
            "=" * 50,
            f"Period: Last 7 days",
            f"Total meetings imported: {len(recent_imports)}",
            "",
        ]

        # Add each client section
        for client_slug in sorted(grouped.keys(), key=lambda x: (x == "_unassigned", x)):
            client_display = self._format_client_name(client_slug)
            meetings = grouped[client_slug]

            # HTML section
            html_parts.append(f"<h3>{client_display} ({len(meetings)} meetings)</h3>")
            html_parts.append("<ul>")

            # Text section
            text_parts.append(f"{client_display} ({len(meetings)} meetings)")
            text_parts.append("-" * 40)

            for meeting in meetings:
                # Parse timestamp
                try:
                    imported_at = datetime.fromisoformat(meeting["imported_at"])
                    time_str = imported_at.strftime("%b %d, %H:%M")
                except:
                    time_str = "Unknown time"

                html_parts.append(
                    f"<li><strong>{meeting['filename']}</strong><br>"
                    f"<small style='color: #666;'>Imported: {time_str}</small></li>"
                )

                text_parts.append(f"  • {meeting['filename']}")
                text_parts.append(f"    Imported: {time_str}")

            html_parts.append("</ul>")
            text_parts.append("")

        # Add unassigned warning if present
        if "_unassigned" in grouped:
            unassigned_count = len(grouped["_unassigned"])
            html_parts.append(
                f"<div style='background-color: #fff3cd; border-left: 4px solid #ffc107; "
                f"padding: 10px; margin: 20px 0;'>"
                f"<strong>⚠️ Action Required:</strong> {unassigned_count} meeting(s) could not be "
                f"automatically assigned to a client. Please review and move them to the correct "
                f"client folder manually."
                f"</div>"
            )

            text_parts.append("⚠️ ACTION REQUIRED:")
            text_parts.append(
                f"{unassigned_count} meeting(s) could not be automatically assigned."
            )
            text_parts.append("Please review clients/_unassigned/meeting-notes/ and organize manually.")
            text_parts.append("")

        # Footer
        html_parts.append("<hr>")
        html_parts.append(
            "<p style='color: #666; font-size: 12px;'>"
            "This is an automated email from Pete's Brain - Granola Meeting Importer<br>"
            f"View import history: {Path(__file__).parent / '.import_history.json'}"
            "</p>"
        )
        html_parts.append("</body></html>")

        text_parts.append("=" * 50)
        text_parts.append("This is an automated email from Pete's Brain - Granola Meeting Importer")

        html_body = "\n".join(html_parts)
        text_body = "\n".join(text_parts)

        # Send email
        return self._send_email(subject, html_body, text_body)

    def send_unassigned_alert(self, meeting_title: str, file_path: str) -> bool:
        """
        Send alert when a meeting couldn't be assigned to a client.

        Args:
            meeting_title: Title of the meeting
            file_path: Path where the meeting was saved

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.config.get("email", {}).get("alerts", {}).get("unassigned_meetings", False):
            return True  # Alert disabled

        subject = f"⚠️ Unassigned Meeting: {meeting_title}"

        html_body = f"""
        <html><body style='font-family: Arial, sans-serif;'>
        <h2>⚠️ Meeting Requires Manual Assignment</h2>
        <p>A meeting could not be automatically assigned to a client.</p>

        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
        <p><strong>Meeting Title:</strong> {meeting_title}</p>
        <p><strong>Saved To:</strong> {file_path}</p>
        <p><strong>Time:</strong> {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </div>

        <p><strong>Action Required:</strong></p>
        <ol>
        <li>Review the meeting notes at the path above</li>
        <li>Determine the correct client</li>
        <li>Move the file to the appropriate client folder</li>
        </ol>

        <hr>
        <p style='color: #666; font-size: 12px;'>
        This is an automated alert from Pete's Brain - Granola Meeting Importer
        </p>
        </body></html>
        """

        text_body = f"""
UNASSIGNED MEETING ALERT
========================

A meeting could not be automatically assigned to a client.

Meeting Title: {meeting_title}
Saved To: {file_path}
Time: {datetime.now().strftime("%B %d, %Y at %H:%M")}

ACTION REQUIRED:
1. Review the meeting notes at the path above
2. Determine the correct client
3. Move the file to the appropriate client folder

---
This is an automated alert from Pete's Brain - Granola Meeting Importer
        """

        return self._send_email(subject, html_body, text_body)

    def send_sync_failure_alert(self, error_message: str) -> bool:
        """
        Send alert when sync daemon encounters an error.

        Args:
            error_message: Error details

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.config.get("email", {}).get("alerts", {}).get("sync_failures", False):
            return True  # Alert disabled

        subject = "🚨 Granola Sync Daemon Error"

        html_body = f"""
        <html><body style='font-family: Arial, sans-serif;'>
        <h2>🚨 Sync Daemon Error</h2>
        <p>The Granola meeting sync daemon encountered an error.</p>

        <div style='background-color: #f8d7da; padding: 15px; border-radius: 5px; border-left: 4px solid #dc3545;'>
        <p><strong>Error:</strong></p>
        <pre style='background-color: #fff; padding: 10px; border-radius: 3px; overflow-x: auto;'>{error_message}</pre>
        <p><strong>Time:</strong> {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </div>

        <p><strong>Troubleshooting Steps:</strong></p>
        <ol>
        <li>Check if Granola app is running and you're logged in</li>
        <li>Verify credentials at: ~/Library/Application Support/Granola/supabase.json</li>
        <li>Check daemon logs: tail -f ~/.petesbrain-granola-importer.log</li>
        <li>Restart the daemon if needed: launchctl restart com.petesbrain.granola-importer</li>
        </ol>

        <hr>
        <p style='color: #666; font-size: 12px;'>
        This is an automated alert from Pete's Brain - Granola Meeting Importer
        </p>
        </body></html>
        """

        text_body = f"""
SYNC DAEMON ERROR
=================

The Granola meeting sync daemon encountered an error.

Error:
{error_message}

Time: {datetime.now().strftime("%B %d, %Y at %H:%M")}

TROUBLESHOOTING STEPS:
1. Check if Granola app is running and you're logged in
2. Verify credentials at: ~/Library/Application Support/Granola/supabase.json
3. Check daemon logs: tail -f ~/.petesbrain-granola-importer.log
4. Restart the daemon if needed: launchctl restart com.petesbrain.granola-importer

---
This is an automated alert from Pete's Brain - Granola Meeting Importer
        """

        return self._send_email(subject, html_body, text_body)


if __name__ == "__main__":
    # Test email reporter
    try:
        reporter = EmailReporter()
        print("✓ Email reporter initialized successfully")
        print(f"✓ Recipient: {reporter.config['email']['recipient']}")

        # Test weekly summary
        print("\nSending test weekly summary...")
        if reporter.send_weekly_summary():
            print("✓ Weekly summary sent successfully")
        else:
            print("✗ Failed to send weekly summary")

    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("\nTo enable email reporting:")
        print("1. Copy config.example.yaml to config.yaml")
        print("2. Fill in your email settings")
        print("3. Run this script again")

    except Exception as e:
        print(f"✗ Error: {e}")
