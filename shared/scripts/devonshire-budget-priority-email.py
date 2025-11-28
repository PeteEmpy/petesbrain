#!/usr/bin/env python3
"""
One-off high-priority email for Devonshire November budget changes.
Send for Monday, November 3rd morning.

Usage:
    GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
      shared/email-sync/.venv/bin/python3 shared/scripts/devonshire-budget-priority-email.py
"""

import sys
from pathlib import Path
from datetime import datetime
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Gmail API imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def authenticate():
    """Authenticate with Gmail API."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    email_sync_dir = Path(__file__).parent.parent / 'email-sync'
    token_file = email_sync_dir / 'token.json'
    credentials_file = email_sync_dir / 'credentials.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        else:
            raise Exception(f"No valid credentials found at {token_file}")

    return creds

def create_message_with_attachment(to, subject, html_content, attachment_path):
    """Create email message with CSV attachment."""
    message = MIMEMultipart('mixed')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    # Add HTML content
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)
    html_part = MIMEText(html_content, 'html')
    msg_alternative.attach(html_part)

    # Add CSV attachment
    attachment_path = Path(attachment_path)
    if attachment_path.exists():
        with open(attachment_path, 'rb') as f:
            file_data = f.read()

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path.name}"')
        message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def main():
    print("=" * 80)
    print("🚨 HIGH PRIORITY: Devonshire Budget Changes - Monday Nov 3rd")
    print("=" * 80)

    subject = "🚨 HIGH PRIORITY: Devonshire Budget Changes - Action Required Monday 10am"

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .header { background: #d32f2f; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .alert-box { background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0; }
            .numbers { background: #e3f2fd; padding: 15px; margin: 20px 0; border-radius: 5px; }
            .action-box { background: #c8e6c9; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0; }
            .table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            .table th { background: #2196f3; color: white; padding: 10px; text-align: left; }
            .table td { padding: 10px; border-bottom: 1px solid #ddd; }
            .reduced { color: #d32f2f; font-weight: bold; }
            .footer { background: #f5f5f5; padding: 15px; margin-top: 20px; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚨 HIGH PRIORITY ACTION REQUIRED</h1>
            <p style="margin: 0; font-size: 1.2em;">Devonshire Hotels - November Budget Changes</p>
        </div>

        <div class="content">
            <div class="alert-box">
                <h2 style="margin-top: 0;">⏰ ACTION REQUIRED: Monday, November 3rd at 10:00 AM</h2>
                <p><strong>Implementation delayed from Nov 1st to Nov 3rd.</strong></p>
                <p>Current high budgets (£200/£200/£150 on top 3 campaigns) will run Friday-Saturday Nov 1-2, requiring adjusted budgets for the remaining 28 days of November.</p>
            </div>

            <h2>📊 Budget Impact</h2>
            <div class="numbers">
                <p><strong>November 1-2 Spend (at current rates):</strong></p>
                <ul>
                    <li>Main Properties: £1,480 (2 days @ £740/day)</li>
                    <li>Self-Catering: £92 (2 days @ £46/day)</li>
                    <li>The Hide: £136 (2 days @ £68/day)</li>
                    <li><strong>Total Nov 1-2: £1,708</strong></li>
                </ul>

                <p><strong>November 3-30 (28 days remaining):</strong></p>
                <ul>
                    <li>Main + Self-Catering: £7,428 remaining = £265/day</li>
                    <li>The Hide: £1,864 remaining = £67/day</li>
                    <li><strong>Total Nov 3-30: £9,296</strong></li>
                </ul>

                <p style="font-size: 1.1em; margin-top: 15px;"><strong>November Grand Total: £11,004 (£4 over £11,000 target - negligible variance) ✅</strong></p>
            </div>

            <h2>🚀 Fast Implementation Method (Recommended)</h2>
            <div class="action-box">
                <p><strong>✨ CSV file attached to this email!</strong></p>
                <ol>
                    <li>Open <strong>Google Ads Editor</strong></li>
                    <li>Select <strong>Devonshire Hotels account</strong></li>
                    <li>Go to <strong>Account → Import → From file</strong></li>
                    <li>Select the attached file: <code>devonshire-november-2025-budgets.csv</code></li>
                    <li>Review all 12 budget changes</li>
                    <li>Click <strong>Post</strong> to apply to Google Ads</li>
                </ol>
                <p><strong>⏱️ Time: ~2 minutes</strong> (vs 15 minutes manual)</p>
            </div>

            <h2>📋 New Daily Budgets (Nov 3-30)</h2>
            <p><strong>Note:</strong> These budgets are <span class="reduced">SLIGHTLY LOWER</span> than originally planned because Nov 1-2 spending at current high rates uses part of the monthly budget.</p>

            <table class="table">
                <thead>
                    <tr>
                        <th>Campaign</th>
                        <th>New Budget (Nov 3-30)</th>
                        <th>Original Plan (Nov 1-30)</th>
                        <th>Difference</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: #e8eaf6;">
                        <td colspan="4"><strong>MAIN PROPERTIES (9 campaigns)</strong></td>
                    </tr>
                    <tr>
                        <td>P Max All</td>
                        <td class="reduced">£66</td>
                        <td>£75</td>
                        <td>-£9</td>
                    </tr>
                    <tr>
                        <td>Devonshire Arms Hotel</td>
                        <td class="reduced">£42</td>
                        <td>£48</td>
                        <td>-£6</td>
                    </tr>
                    <tr>
                        <td>Cavendish</td>
                        <td class="reduced">£40</td>
                        <td>£45</td>
                        <td>-£5</td>
                    </tr>
                    <tr>
                        <td>The Beeley Inn</td>
                        <td class="reduced">£29</td>
                        <td>£33</td>
                        <td>-£4</td>
                    </tr>
                    <tr>
                        <td>Chatsworth Inns</td>
                        <td class="reduced">£25</td>
                        <td>£28</td>
                        <td>-£3</td>
                    </tr>
                    <tr>
                        <td>The Pilsley Inn</td>
                        <td class="reduced">£24</td>
                        <td>£27</td>
                        <td>-£3</td>
                    </tr>
                    <tr>
                        <td>The Fell</td>
                        <td class="reduced">£21</td>
                        <td>£24</td>
                        <td>-£3</td>
                    </tr>
                    <tr>
                        <td>Chatsworth Locations</td>
                        <td class="reduced">£16</td>
                        <td>£18</td>
                        <td>-£2</td>
                    </tr>
                    <tr>
                        <td>Bolton Abbey Locations</td>
                        <td class="reduced">£11</td>
                        <td>£12</td>
                        <td>-£1</td>
                    </tr>
                    <tr>
                        <td colspan="4" style="padding-top: 10px;"><strong>Subtotal: £239/day</strong></td>
                    </tr>

                    <tr style="background: #e8eaf6;">
                        <td colspan="4"><strong>SELF-CATERING (2 campaigns)</strong></td>
                    </tr>
                    <tr>
                        <td>Bolton Abbey Self Catering</td>
                        <td class="reduced">£9</td>
                        <td>£10</td>
                        <td>-£1</td>
                    </tr>
                    <tr>
                        <td>Chatsworth Self Catering</td>
                        <td class="reduced">£18</td>
                        <td>£20</td>
                        <td>-£2</td>
                    </tr>
                    <tr>
                        <td colspan="4" style="padding-top: 10px;"><strong>Subtotal: £27/day</strong></td>
                    </tr>

                    <tr style="background: #e8eaf6;">
                        <td colspan="4"><strong>THE HIDE (Separate Budget)</strong></td>
                    </tr>
                    <tr>
                        <td>The Hide</td>
                        <td>£67</td>
                        <td>£67</td>
                        <td>±£0</td>
                    </tr>
                </tbody>
            </table>

            <h2>📄 Additional Documentation</h2>
            <p>Full details available in:</p>
            <ul>
                <li><code>clients/devonshire-hotels/documents/november-2025-budget-changes.md</code></li>
                <li><code>clients/devonshire-hotels/documents/november-budget-changes-checklist.md</code></li>
            </ul>

            <h2>❓ Questions?</h2>
            <p>If you have any questions or issues with the CSV import, refer to the documentation above.</p>
        </div>

        <div class="footer">
            <p><strong>📅 Implementation Date:</strong> Monday, November 3rd, 2025 at 10:00 AM</p>
            <p><strong>⏱️ Estimated Time:</strong> 2 minutes (CSV import) or 15 minutes (manual)</p>
            <p><strong>🎯 Target:</strong> £11,000 total November spend (projected: £11,004)</p>
        </div>
    </body>
    </html>
    """

    csv_path = Path(__file__).parent.parent.parent / 'clients' / 'devonshire-hotels' / 'spreadsheets' / 'devonshire-november-2025-budgets.csv'

    if not csv_path.exists():
        print(f"❌ ERROR: CSV file not found at {csv_path}")
        sys.exit(1)

    print(f"📎 Attaching CSV: {csv_path.name}")

    # Authenticate
    print("🔐 Authenticating with Gmail...")
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # Create message
    print("📧 Creating message with attachment...")
    message = create_message_with_attachment(
        to='petere@roksys.co.uk',
        subject=subject,
        html_content=html_content,
        attachment_path=csv_path
    )

    # Send
    print("📤 Sending email to petere@roksys.co.uk...")
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print("✅ Email sent successfully!")
        print(f"   Message ID: {sent_message['id']}")
        print(f"   Subject: {subject}")
        print(f"   Attachment: {csv_path.name}")
        print("=" * 80)

    except Exception as e:
        print(f"❌ ERROR sending email: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
