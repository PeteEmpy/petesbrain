#!/usr/bin/env python3
"""
Weekly News Digest Generator

Generates a separate weekly email focused on:
1. Google Ads industry news (automated monitoring)
2. AI news (automated monitoring)
3. AI newsletters and emails
4. New knowledge base documents

Provides clickable links to all articles and an HTML browser view.
Runs every Monday at 9 AM (after kb-weekly-summary)
"""

import os
import sys
import base64
import anthropic
from pathlib import Path
from datetime import datetime, timedelta
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

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
KB_ROOT = PROJECT_ROOT / "roksys/knowledge-base"

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def log_message(message):
    """Print and log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def authenticate():
    """Authenticate with Gmail API."""
    creds = None
    token_file = PROJECT_ROOT / 'shared/email-sync/token-weekly-summary.json'
    credentials_file = PROJECT_ROOT / 'shared/email-sync/credentials.json'

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


def get_files_from_last_week(directory, days=7):
    """Get files modified in the last N days"""
    if not directory.exists():
        return []

    cutoff_date = datetime.now() - timedelta(days=days)
    recent_files = []

    for file_path in directory.rglob("*.md"):
        if file_path.stat().st_mtime > cutoff_date.timestamp():
            recent_files.append(file_path)

    return sorted(recent_files, key=lambda x: x.stat().st_mtime, reverse=True)


def get_automated_news_articles(days=7):
    """Get articles added by automated news monitors in the last N days"""
    cutoff_date = datetime.now() - timedelta(days=days)

    google_ads_articles = []
    ai_articles = []

    # Check inbox for recently added articles
    inbox_docs = KB_ROOT / "_inbox/documents"
    if inbox_docs.exists():
        for file_path in inbox_docs.glob("*.md"):
            if file_path.stat().st_mtime > cutoff_date.timestamp():
                doc = read_markdown_file(file_path)
                if doc and 'frontmatter' in doc:
                    frontmatter = doc['frontmatter']
                    if 'category: AI News' in frontmatter:
                        ai_articles.append({'path': file_path, 'doc': doc})
                    elif 'relevance_score:' in frontmatter:
                        google_ads_articles.append({'path': file_path, 'doc': doc})

    # Also check processed KB documents
    for category in ['google-ads', 'ai-strategy', 'industry-insights']:
        category_path = KB_ROOT / category
        if category_path.exists():
            for file_path in category_path.rglob("*.md"):
                if file_path.stat().st_mtime > cutoff_date.timestamp():
                    doc = read_markdown_file(file_path)
                    if doc and 'frontmatter' in doc:
                        content = doc.get('content', '')
                        if 'fetched by industry news monitor' in content:
                            google_ads_articles.append({'path': file_path, 'doc': doc})
                        elif 'fetched by AI news monitor' in content:
                            ai_articles.append({'path': file_path, 'doc': doc})

    return google_ads_articles, ai_articles


def extract_relevance_score(frontmatter):
    """Extract relevance score from frontmatter"""
    for line in frontmatter.split('\n'):
        if line.startswith('relevance_score:'):
            try:
                return int(line.replace('relevance_score:', '').strip())
            except:
                return 0
    return 0


def extract_source(frontmatter):
    """Extract source from frontmatter"""
    for line in frontmatter.split('\n'):
        if line.startswith('source:'):
            return line.replace('source:', '').strip()
    return 'Unknown'


def extract_url(frontmatter, content):
    """Extract URL from frontmatter or content"""
    # Try frontmatter first
    for line in frontmatter.split('\n'):
        if line.startswith('url:') or line.startswith('link:'):
            url = line.split(':', 1)[1].strip()
            if url:
                return url

    # Try to find URL in content
    import re
    url_match = re.search(r'https?://[^\s\)]+', content)
    if url_match:
        return url_match.group(0)

    return None


def read_markdown_file(file_path):
    """Read markdown file and extract metadata + content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()

        if '---' in content:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]

                for line in frontmatter.split('\n'):
                    if line.startswith('title:'):
                        title = line.replace('title:', '').strip()
                        break

                return {'title': title, 'content': body, 'frontmatter': frontmatter}

        return {'title': title, 'content': content, 'frontmatter': ''}
    except Exception as e:
        log_message(f"Error reading {file_path}: {e}")
        return None


def analyze_news_with_claude(google_ads_news, ai_news, ai_emails, kb_documents):
    """Use Claude API to analyze and summarize the news"""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return None

    anthropic_client = anthropic.Anthropic(api_key=api_key)

    # Prepare automated news summaries with URLs
    google_ads_summaries = []
    for article in google_ads_news[:15]:
        doc = article['doc']
        score = extract_relevance_score(doc.get('frontmatter', ''))
        source = extract_source(doc.get('frontmatter', ''))
        url = extract_url(doc.get('frontmatter', ''), doc.get('content', ''))
        url_display = f" | {url}" if url else ""
        google_ads_summaries.append(f"[{score}/10] {doc['title']} - {source}{url_display}")

    ai_news_summaries = []
    for article in ai_news[:15]:
        doc = article['doc']
        score = extract_relevance_score(doc.get('frontmatter', ''))
        source = extract_source(doc.get('frontmatter', ''))
        url = extract_url(doc.get('frontmatter', ''), doc.get('content', ''))
        url_display = f" | {url}" if url else ""
        ai_news_summaries.append(f"[{score}/10] {doc['title']} - {source}{url_display}")

    # Prepare email summaries
    email_summaries = []
    for email in ai_emails[:10]:
        doc = read_markdown_file(email)
        if doc:
            email_summaries.append(f"{doc['title']}\n{doc['content'][:500]}")

    kb_summaries = []
    for kb_doc in kb_documents[:10]:
        doc = read_markdown_file(kb_doc)
        if doc:
            kb_summaries.append(f"{doc['title']}\n{doc['content'][:500]}")

    prompt = f"""You are analyzing industry news and knowledge base updates for Pete's weekly news digest.

**AUTOMATED GOOGLE ADS INDUSTRY NEWS** ({len(google_ads_news)} articles):
{chr(10).join(google_ads_summaries) if google_ads_summaries else 'No articles this week'}

**AUTOMATED AI NEWS** ({len(ai_news)} articles):
{chr(10).join(ai_news_summaries) if ai_news_summaries else 'No articles this week'}

**AI NEWSLETTERS/EMAILS** ({len(ai_emails)} total):
{chr(10).join(email_summaries) if email_summaries else 'No emails this week'}

**NEW KNOWLEDGE BASE DOCUMENTS** ({len(kb_documents)} total):
{chr(10).join(kb_summaries) if kb_summaries else 'No documents this week'}

Create a comprehensive news digest with the following sections:

1. **🔥 Top Stories This Week** - 5-7 most important articles across all sources
   - Prioritize high-scoring articles (8+/10)
   - Include one-sentence summary of why each matters
   - Include clickable source link

2. **🤖 AI & Machine Learning Updates**
   - Product launches and features
   - Industry trends and research
   - Regulation and policy updates

3. **💡 Google Ads & Paid Search News**
   - Platform updates and new features
   - Best practices and case studies
   - Industry insights

4. **📚 Knowledge Base Additions**
   - Categorize by type (Google Ads, AI Strategy, Analytics, etc.)
   - Brief description of each addition

5. **🎯 Key Takeaways for Digital Marketers**
   - 3-5 actionable insights from this week's news
   - Focus on what Pete should know or act on

Format as HTML suitable for email. Use clean, professional styling with #2c3e50 for headings and #3498db for accents.
Include clickable links for all articles where URLs are provided.
Use badges to highlight high-scoring articles (8+/10).

CRITICAL: Do NOT use background colors or text colors on section content - only on headings, badges, and accents.
"""

    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except Exception as e:
        log_message(f"Error analyzing with Claude: {e}")
        return None


def create_full_html_news_digest(google_ads_news, ai_news, ai_emails, kb_documents, summary_content):
    """Create full expandable HTML version with ALL articles and clickable links"""

    today = datetime.now()
    week_start = today - timedelta(days=7)
    date_range = f"{week_start.strftime('%b %d')} - {today.strftime('%b %d, %Y')}"

    # Build article sections with clickable links
    google_ads_html = "<h3>Google Ads & PPC Industry News</h3>\n<ul>\n"
    for article in google_ads_news:
        doc = article['doc']
        score = extract_relevance_score(doc.get('frontmatter', ''))
        source = extract_source(doc.get('frontmatter', ''))
        url = extract_url(doc.get('frontmatter', ''), doc.get('content', ''))

        score_badge = f'<span class="score score-{score}">{score}/10</span>'
        if url:
            google_ads_html += f'<li>{score_badge} <a href="{url}" target="_blank">{doc["title"]}</a> - <em>{source}</em></li>\n'
        else:
            google_ads_html += f'<li>{score_badge} {doc["title"]} - <em>{source}</em></li>\n'
    google_ads_html += "</ul>\n"

    ai_news_html = "<h3>AI & Machine Learning News</h3>\n<ul>\n"
    for article in ai_news:
        doc = article['doc']
        score = extract_relevance_score(doc.get('frontmatter', ''))
        source = extract_source(doc.get('frontmatter', ''))
        url = extract_url(doc.get('frontmatter', ''), doc.get('content', ''))

        score_badge = f'<span class="score score-{score}">{score}/10</span>'
        if url:
            ai_news_html += f'<li>{score_badge} <a href="{url}" target="_blank">{doc["title"]}</a> - <em>{source}</em></li>\n'
        else:
            ai_news_html += f'<li>{score_badge} {doc["title"]} - <em>{source}</em></li>\n'
    ai_news_html += "</ul>\n"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Weekly News Digest - {date_range}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        ul {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 12px;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .score {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 8px;
        }}
        .score-10, .score-9 {{
            background-color: #22c55e;
            color: white;
        }}
        .score-8, .score-7 {{
            background-color: #3b82f6;
            color: white;
        }}
        .score-6, .score-5 {{
            background-color: #a3a3a3;
            color: white;
        }}
        .timestamp {{
            color: #6b7280;
            font-style: italic;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>📰 Weekly News Digest</h1>
    <p class="timestamp">Week of {date_range}</p>
    <p class="timestamp">Full Expanded View - All Articles with Clickable Links</p>

    <hr>

    {summary_content}

    <hr>

    <h2>📋 Complete Article List</h2>

    {google_ads_html}
    {ai_news_html}

    <hr>

    <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p class="timestamp">Automated news monitoring runs every 6 hours</p>
</body>
</html>
"""

    return html


def create_message(to, subject, html_content):
    """Create email message."""
    message = MIMEMultipart('alternative')
    message['To'] = to
    message['From'] = 'me'
    message['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

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
    log_message("=" * 60)
    log_message("Weekly News Digest Generation Started")
    log_message("=" * 60)

    # Gather automated news
    log_message("🤖 Gathering automated news...")
    google_ads_news, ai_news = get_automated_news_articles(days=7)
    log_message(f"  Google Ads: {len(google_ads_news)} articles")
    log_message(f"  AI News: {len(ai_news)} articles")

    # Gather AI emails
    log_message("📧 Gathering AI newsletters...")
    ai_emails_dir = PROJECT_ROOT / "roksys/news/emails"
    ai_emails = get_files_from_last_week(ai_emails_dir, days=7) if ai_emails_dir.exists() else []
    log_message(f"  Found {len(ai_emails)} AI emails")

    # Gather KB documents
    log_message("📚 Gathering KB documents...")
    kb_documents = []
    kb_categories = ['google-ads', 'ai-strategy', 'analytics', 'industry-insights']
    for category in kb_categories:
        category_path = KB_ROOT / category
        if category_path.exists():
            docs = get_files_from_last_week(category_path, days=7)
            kb_documents.extend(docs)
    log_message(f"  Found {len(kb_documents)} new KB documents")

    if len(google_ads_news) == 0 and len(ai_news) == 0 and len(ai_emails) == 0:
        log_message("⚠️  No news content this week. Skipping email.")
        return 0

    # Analyze with Claude
    log_message("🤖 Analyzing news with Claude API...")
    summary_content = analyze_news_with_claude(google_ads_news, ai_news, ai_emails, kb_documents)

    if not summary_content:
        log_message("❌ Failed to generate summary")
        return 1

    # Create full HTML version
    log_message("📄 Creating full HTML news digest...")
    full_html = create_full_html_news_digest(google_ads_news, ai_news, ai_emails, kb_documents, summary_content)

    # Save HTML file
    html_file = PROJECT_ROOT / 'briefing' / f"weekly-news-{datetime.now().strftime('%Y-%m-%d')}.html"
    html_file.parent.mkdir(exist_ok=True)
    with open(html_file, 'w') as f:
        f.write(full_html)

    log_message(f"📄 HTML file: {html_file}")

    # Create email with link to full version
    today = datetime.now()
    week_start = today - timedelta(days=7)
    date_range = f"{week_start.strftime('%b %d')} - {today.strftime('%b %d, %Y')}"

    email_html = f"""<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .view-full {{ background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 20px 0; }}
        .view-full:hover {{ background-color: #2980b9; }}
    </style>
</head>
<body>
    <h1>📰 Weekly News Digest</h1>
    <p>Week of {date_range}</p>

    <a href="file://{html_file}" class="view-full">📄 View Full Digest with All Links</a>

    <hr>

    {summary_content}

    <hr>

    <p style="color: #7f8c8d; font-style: italic; font-size: 0.9em;">
        Click "View Full Digest" above to see all articles with clickable links to sources.
    </p>
</body>
</html>
"""

    subject = f"📰 Weekly News Digest - {today.strftime('%b %d')}"

    # Authenticate and send
    log_message("🔐 Authenticating with Gmail...")
    creds = authenticate()

    if not creds:
        log_message("❌ Authentication failed")
        return 1

    try:
        service = build('gmail', 'v1', credentials=creds)

        log_message("📤 Sending email...")
        message = create_message(
            to='petere@roksys.co.uk',
            subject=subject,
            html_content=email_html
        )

        result = send_message(service, message)

        if result:
            log_message(f"✅ Email sent successfully! Message ID: {result['id']}")
            log_message(f"📄 Full digest: file://{html_file}")
            log_message("=" * 60)
            return 0
        else:
            log_message("❌ Failed to send email")
            return 1

    except Exception as e:
        log_message(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
