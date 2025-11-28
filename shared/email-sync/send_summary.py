#!/usr/bin/env python3
"""
Send AI News Summary Email
"""

import os
import sys
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Authenticate with Gmail API."""
    creds = None
    script_dir = Path(__file__).parent
    # Use separate token file for send_summary to avoid scope conflicts with sync_emails.py
    token_file = script_dir / 'token-weekly-summary.json'
    credentials_file = script_dir / 'credentials.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_file.exists():
                print(f"Error: credentials.json not found at {credentials_file}")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

def create_message(to, subject, html_content):
    """Create email message."""
    message = MIMEMultipart('alternative')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, message):
    """Send email message."""
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()
        return sent_message
    except Exception as e:
        print(f'Error sending message: {e}')
        return None

def main():
    # Email content
    subject = "AI News Summary - Past 7 Days (Oct 21-28, 2025)"

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 25px; border-left: 4px solid #3498db; padding-left: 10px; }
            h3 { color: #555; margin-top: 20px; }
            ul { margin-left: 20px; }
            li { margin-bottom: 8px; }
            .date { color: #7f8c8d; font-style: italic; }
            .highlight { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>🤖 AI News Summary</h1>
        <p class="date">Week of October 21-28, 2025</p>

        <div class="highlight">
            <strong>📊 This Week's Coverage:</strong> 9 newsletters analyzed covering major developments in AI products, regulations, hardware, and industry moves.
        </div>

        <h2>🚀 Major Product Launches</h2>

        <h3>OpenAI ChatGPT Atlas Browser <span class="date">(Oct 22)</span></h3>
        <ul>
            <li><strong>What:</strong> OpenAI launched ChatGPT Atlas, a web browser with ChatGPT built directly into it</li>
            <li><strong>Key Features:</strong> Agent mode for automation, browser memory for context recall, ability to complete tasks without leaving the page</li>
            <li><strong>Significance:</strong> OpenAI's entry into the browser market, positioning ChatGPT as a complete workspace blending browsing and automation</li>
            <li><strong>Available to:</strong> Plus, Pro, and Business users (agent mode in preview)</li>
        </ul>

        <h3>Microsoft AI Launch <span class="date">(Oct 24)</span></h3>
        <ul>
            <li>Microsoft launched new AI capabilities days after OpenAI's Atlas announcement</li>
            <li>Signals intensifying competition in the AI browser/workspace space</li>
        </ul>

        <h2>🏢 Enterprise & Industry</h2>

        <h3>Anthropic Claude for Life Sciences <span class="date">(Oct 21)</span></h3>
        <ul>
            <li><strong>Target Market:</strong> $2 trillion biotech industry</li>
            <li><strong>Purpose:</strong> Automate drug discovery tasks including hypothesis generation, literature review, and regulatory drafting</li>
            <li><strong>Goal:</strong> Reduce time-to-market for potentially life-saving treatments</li>
        </ul>

        <h3>Alibaba Targets Consumer Market <span class="date">(Oct 24)</span></h3>
        <ul>
            <li>Alibaba making strategic moves into consumer-facing AI applications</li>
            <li>Expanding beyond enterprise and cloud services</li>
        </ul>

        <h2>💰 Major Deals & Investments</h2>

        <h3>AMD $1B AI Supercomputer Agreement <span class="date">(Oct 28)</span></h3>
        <ul>
            <li>AMD secures massive $1 billion contract for AI supercomputer infrastructure</li>
            <li>Demonstrates AMD's growing competitiveness against NVIDIA in AI hardware</li>
        </ul>

        <h3>Mercor Valuation Quintuples to $10B <span class="date">(Oct 28)</span></h3>
        <ul>
            <li>AI recruitment/talent platform sees explosive growth</li>
            <li>Signals strong investor confidence in AI-powered workforce solutions</li>
        </ul>

        <h2>🏭 Manufacturing & Hardware</h2>

        <h3>Nvidia & TSMC First US-Built AI Chip <span class="date">(Oct 20)</span></h3>
        <ul>
            <li>Historic milestone: First AI chip manufactured in the United States</li>
            <li>Partnership between Nvidia (design) and TSMC (manufacturing)</li>
            <li><strong>Strategic Importance:</strong> Reduces dependency on Asian manufacturing, strengthens US AI infrastructure</li>
        </ul>

        <h2>⚖️ Regulation & Legal Issues</h2>

        <h3>AI Copyright Problems <span class="date">(Oct 21)</span></h3>
        <ul>
            <li><strong>Adobe's Solution:</strong> Launched AI Foundry program for enterprises to build custom models trained on licensed data</li>
            <li><strong>Industry Context:</strong> Anthropic, OpenAI, Meta, and Perplexity all facing copyright-related legal challenges</li>
            <li><strong>Creative Industry Concerns:</strong> AI video tools (Sora, Veo, xAI Imagine) facing backlash from entertainment industry</li>
        </ul>

        <h3>Anthropic Weighs In on Regulation <span class="date">(Oct 22)</span></h3>
        <ul>
            <li>Anthropic providing input on AI regulation frameworks</li>
            <li>Positioning as responsible AI development leader</li>
        </ul>

        <h2>🎭 Deepfakes & Content Authenticity</h2>

        <h3>OpenAI & MLK Controversy <span class="date">(Oct 20)</span></h3>
        <ul>
            <li>Backlash over OpenAI's Sora video model and deepfake concerns</li>
            <li><strong>Response:</strong> Partnership with SAG-AFTRA, talent agencies, and Bryan Cranston</li>
            <li><strong>New Features:</strong> Public figures and copyright holders can opt out of likeness being used</li>
        </ul>

        <h3>YouTube Likeness Detection <span class="date">(Oct 22)</span></h3>
        <ul>
            <li>YouTube launches AI-powered likeness detection tools</li>
            <li>Aims to protect content creators from unauthorized AI-generated content using their likeness</li>
        </ul>

        <h2>💼 Workforce & Training</h2>

        <h3>OpenAI Pays Ex-Bankers $150/hr <span class="date">(Oct 23)</span></h3>
        <ul>
            <li>OpenAI hiring financial professionals at premium rates</li>
            <li>Cutting out traditional data labeling companies</li>
            <li>Signals shift toward specialized, high-quality training data</li>
        </ul>

        <h3>Google Trains AI Workforce <span class="date">(Oct 22)</span></h3>
        <ul>
            <li>Google expanding AI training and certification programs</li>
            <li>Preparing workforce for AI-integrated jobs</li>
        </ul>

        <h2>📈 Key Themes This Week</h2>
        <ol>
            <li><strong>Browser Wars Heat Up:</strong> OpenAI and Microsoft racing to integrate AI into web browsing</li>
            <li><strong>Copyright Crisis:</strong> Industry grappling with legal framework for AI training and content generation</li>
            <li><strong>US Manufacturing Push:</strong> First US-made AI chip and major infrastructure investments</li>
            <li><strong>Enterprise Adoption:</strong> Specialized AI tools for biotech, recruitment, and business workflows</li>
            <li><strong>Content Protection:</strong> Platforms implementing deepfake detection and creator protection tools</li>
            <li><strong>Hardware Competition:</strong> AMD challenging NVIDIA's dominance with billion-dollar deals</li>
        </ol>

        <div class="footer">
            <p><strong>Source:</strong> Compiled from The Deep View and The AI Report newsletters</p>
            <p><strong>Period Covered:</strong> October 21-28, 2025 (9 newsletters)</p>
            <p><em>This summary was generated from your automatically synced AI newsletters in Pete's Brain.</em></p>
        </div>
    </body>
    </html>
    """

    # Authenticate and send
    print("🔐 Authenticating with Gmail...")
    creds = authenticate()

    if not creds:
        print("❌ Authentication failed")
        return 1

    try:
        service = build('gmail', 'v1', credentials=creds)

        print("📧 Composing email...")
        message = create_message(
            to='petere@roksys.co.uk',
            subject=subject,
            html_content=html_content
        )

        print("📤 Sending email...")
        result = send_message(service, message)

        if result:
            print(f"✅ Email sent successfully! Message ID: {result['id']}")
            return 0
        else:
            print("❌ Failed to send email")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
