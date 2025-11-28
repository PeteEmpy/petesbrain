#!/usr/bin/env python3
"""
Email Attachment Helper for Weekly Review Script
Adds CSV attachment capability to weekly meeting review emails
"""

import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def create_message_with_attachment(to, subject, html_content, attachments=None):
    """
    Create email message with optional attachments.

    Args:
        to: Recipient email address
        subject: Email subject
        html_content: HTML body content
        attachments: List of file paths to attach (optional)

    Returns:
        Dict with 'raw' key containing base64 encoded message
    """
    # Use 'mixed' instead of 'alternative' to support attachments
    message = MIMEMultipart('mixed')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    # Create alternative container for text/html
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    # Add HTML content
    html_part = MIMEText(html_content, 'html')
    msg_alternative.attach(html_part)

    # Add attachments if provided
    if attachments:
        for file_path in attachments:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Warning: Attachment not found: {file_path}")
                continue

            # Read the file
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Create attachment part
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_data)
            encoders.encode_base64(part)

            # Add header with filename
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{file_path.name}"'
            )

            message.attach(part)
            print(f"Attached: {file_path.name}")

    # Encode the message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def should_attach_devonshire_budget_csv(tasks):
    """
    Check if any tasks are related to Devonshire November budget changes.

    Args:
        tasks: List of task dictionaries

    Returns:
        Boolean indicating whether to attach the CSV
    """
    for task in tasks:
        title = task.get('title', '').lower()
        if 'devonshire' in title and 'november' in title and 'budget' in title:
            return True
    return False


def get_devonshire_budget_csv_path():
    """
    Get the path to the Devonshire November budget CSV file.

    Returns:
        Path object or None if not found
    """
    csv_path = Path("/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/spreadsheets/devonshire-november-2025-budgets.csv")

    if csv_path.exists():
        return csv_path

    return None
