#!/usr/bin/env python3
"""
Google Ads Feature Email Processor

Processes Google Ads feature announcement emails:
1. Fetches emails from Gmail with 'google-ads-features' label
2. Deduplicates using content hashing
3. Extracts links from email body
4. Fetches content from linked pages
5. Processes with Claude API to extract specifications
6. Saves to Google Specifications KB

Runs automatically every 2 hours via LaunchAgent.
"""

import os
import sys
import json
import re
import hashlib
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse
import anthropic
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    print("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
SPECS_ROOT = PROJECT_ROOT / "google-specifications"
STATE_FILE = PROJECT_ROOT / "data/cache/google-ads-feature-emails-processed.json"
LOG_FILE = PROJECT_ROOT / "data/cache/google-ads-feature-email-processor.log"
EMAIL_SYNC_DIR = PROJECT_ROOT / "shared/email-sync"

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Batch sizes
BATCH_SIZE = 6  # Emails per Claude API call
HTTP_CONCURRENT = 10  # Concurrent link fetches


def log_message(message: str):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    print(log_entry.strip())
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_processed_emails() -> Dict[str, Any]:
    """Load state of processed emails"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "processed_hashes": [],
        "processed_message_ids": [],
        "last_run": None
    }


def save_processed_emails(state: Dict[str, Any]):
    """Save state of processed emails"""
    state["last_run"] = datetime.now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    token_file = EMAIL_SYNC_DIR / 'token.json'
    credentials_file = EMAIL_SYNC_DIR / 'credentials.json'

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_file.exists():
                log_message("ERROR: credentials.json not found in shared/email-sync/")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def decode_email_body(part: Dict) -> str:
    """Decode email body from base64"""
    if 'data' in part.get('body', {}):
        data = part['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ''


def get_email_body(payload: Dict) -> tuple[str, str]:
    """Extract plain text and HTML body from email"""
    plain_text = ''
    html_text = ''

    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            if mime_type == 'text/plain':
                plain_text += decode_email_body(part)
            elif mime_type == 'text/html':
                html_text += decode_email_body(part)
            elif 'parts' in part:
                pt, ht = get_email_body(part)
                plain_text += pt
                html_text += ht
    else:
        mime_type = payload.get('mimeType', '')
        if mime_type == 'text/plain':
            plain_text = decode_email_body(payload)
        elif mime_type == 'text/html':
            html_text = decode_email_body(payload)

    return plain_text, html_text


def extract_links(text: str, html: str) -> List[str]:
    """Extract URLs from email text and HTML"""
    urls = set()
    
    # Extract from HTML
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            # Filter to Google domains
            if any(domain in url for domain in ['google.com', 'developers.google.com', 'support.google.com', 'blog.google.com']):
                urls.add(url)
    
    # Extract from plain text using regex
    url_pattern = r'https?://(?:[-\w.])+(?:google\.com|developers\.google\.com|support\.google\.com|blog\.google\.com)[^\s<>"{}|\\^`\[\]]*'
    for match in re.finditer(url_pattern, text):
        urls.add(match.group(0))
    
    return list(urls)


def fetch_link_content(url: str) -> Optional[Dict[str, Any]]:
    """Fetch content from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts and styles
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        content = soup.get_text()
        
        return {
            "url": url,
            "content": content[:10000],  # Limit content size
            "title": soup.find('title').get_text() if soup.find('title') else url
        }
    except Exception as e:
        log_message(f"Error fetching {url}: {e}")
        return None


def generate_email_hash(subject: str, body_preview: str) -> str:
    """Generate hash for deduplication"""
    content = f"{subject}|{body_preview[:500]}"
    return hashlib.sha256(content.encode()).hexdigest()


def batch_process_with_claude(emails_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process batch of emails with Claude API"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return []
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build batch prompt
    emails_text = ""
    for i, email_data in enumerate(emails_data, 1):
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')[:2000]
        links_content = email_data.get('links_content', [])
        
        links_text = ""
        for link in links_content[:3]:  # Limit to first 3 links
            links_text += f"\n\nLink: {link.get('url', '')}\nTitle: {link.get('title', '')}\nContent: {link.get('content', '')[:1500]}"
        
        emails_text += f"\n\n--- EMAIL {i} ---\nSubject: {subject}\nBody: {body}{links_text}"
    
    prompt = f"""Analyze these Google Ads feature announcement emails and extract specifications and best practices.

{emails_text}

For EACH email, extract:
1. New features announced (names, descriptions, capabilities)
2. Specifications (character limits, requirements, setup procedures)
3. Best practices recommended
4. Category (google-ads, ga4, or rok-methodologies)
5. Subcategory (asset-groups, merchant-center, platform-updates, etc.)

Respond in JSON format as an array, one object per email:
[
    {{
        "email_index": 1,
        "subject": "Email subject",
        "source_type": "google_feature_email",
        "date": "YYYY-MM-DD",
        "category": "google-ads|ga4|rok-methodologies",
        "subcategory": "platform-updates|asset-groups|merchant-center|etc",
        "specifications": {{
            "title": "Feature name or specification title",
            "requirements": {{}},
            "character_limits": {{}},
            "required_counts": {{}}
        }},
        "best_practices": [
            "Best practice point 1",
            "Best practice point 2"
        ],
        "tags": ["tag1", "tag2"]
    }},
    ...
]"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        
        # Extract JSON array
        if '[' in response_text and ']' in response_text:
            json_start = response_text.index('[')
            json_end = response_text.rindex(']') + 1
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            log_message("Could not parse JSON array from Claude response")
            return []
    
    except Exception as e:
        log_message(f"Error in batch processing: {e}")
        return []


def save_specification(category: str, subcategory: str, filename: str, specs_data: Dict[str, Any], source_info: Dict[str, Any]):
    """Save specification to KB"""
    spec_file = SPECS_ROOT / category / "specifications" / subcategory / filename
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing if exists
    existing_spec = {}
    if spec_file.exists():
        with open(spec_file, 'r') as f:
            existing_spec = json.load(f)
    
    # Create source metadata
    source_metadata = {
        "type": "google_feature_email",
        "source": source_info.get("subject", "Google Ads Feature Email"),
        "date": source_info.get("date", datetime.now().strftime("%Y-%m-%d")),
        "email_id": source_info.get("message_id", ""),
        "verified": True
    }
    
    # Merge with existing
    existing_sources = existing_spec.get("specification", {}).get("sources", [])
    if source_metadata not in existing_sources:
        existing_sources.append(source_metadata)
    
    spec_data = {
        "specification": {
            "title": specs_data.get("title", existing_spec.get("specification", {}).get("title", "Untitled")),
            "version": str(float(existing_spec.get("specification", {}).get("version", "1.0")) + 0.1),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "sources": existing_sources,
            "content": {**existing_spec.get("specification", {}).get("content", {}), **specs_data.get("requirements", {})}
        }
    }
    
    with open(spec_file, 'w') as f:
        json.dump(spec_data, f, indent=2)
    
    log_message(f"✓ Saved specification: {spec_file.relative_to(PROJECT_ROOT)}")


def save_best_practice(category: str, subcategory: str, filename: str, title: str, content: List[str], source_info: Dict[str, Any]):
    """Save best practice to KB"""
    bp_file = SPECS_ROOT / category / "best-practices" / subcategory / filename
    bp_file.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter = f"""---
title: {title}
source: {source_info.get('subject', 'Google Ads Feature Email')}
date_added: {today}
last_updated: {today}
tags: {json.dumps(source_info.get('tags', []))}
source_type: google_feature_email
---

## Summary

{chr(10).join(['- ' + point for point in content[:5]])}

## Full Content

{chr(10).join(['- ' + point for point in content])}

---

*Extracted from Google Ads feature email*
*Email Subject: {source_info.get('subject', 'Unknown')}*
*Date: {today}*
"""
    
    with open(bp_file, 'w') as f:
        f.write(frontmatter)
    
    log_message(f"✓ Saved best practice: {bp_file.relative_to(PROJECT_ROOT)}")


def process_feature_emails():
    """Main processing function"""
    log_message("=" * 60)
    log_message("Google Ads Feature Email Processor Started")
    log_message("=" * 60)
    
    # Authenticate Gmail
    service = authenticate_gmail()
    if not service:
        log_message("ERROR: Failed to authenticate with Gmail")
        return
    
    # Load processed emails state
    state = load_processed_emails()
    processed_hashes = set(state.get("processed_hashes", []))
    processed_message_ids = set(state.get("processed_message_ids", []))
    
    # Search for emails with google-ads-features label
    try:
        # First, get label ID
        labels = service.users().labels().list(userId='me').execute()
        label_id = None
        for label in labels.get('labels', []):
            if label['name'] == 'google-ads-features':
                label_id = label['id']
                break
        
        if not label_id:
            log_message("Label 'google-ads-features' not found. Run auto-labeler first.")
            return
        
        # Search for emails with this label (last 30 days)
        query = f"label:google-ads-features newer_than:30d"
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=50
        ).execute()
        
        messages = results.get('messages', [])
        log_message(f"Found {len(messages)} emails with google-ads-features label")
        
        if not messages:
            log_message("No new emails to process")
            return
        
        # Process emails
        emails_to_process = []
        
        for msg_ref in messages:
            msg_id = msg_ref['id']
            
            # Skip if already processed
            if msg_id in processed_message_ids:
                continue
            
            try:
                # Fetch full message
                message = service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()
                
                # Extract headers
                headers = {h['name']: h['value'] for h in message['payload']['headers']}
                subject = headers.get('Subject', '')
                from_email = headers.get('From', '')
                date_str = headers.get('Date', '')
                
                # Parse date
                try:
                    email_date = parsedate_to_datetime(date_str)
                except:
                    email_date = datetime.now()
                
                # Get body
                payload = message['payload']
                plain_text, html_text = get_email_body(payload)
                body = plain_text or html_text
                
                # Generate hash for deduplication
                email_hash = generate_email_hash(subject, body)
                
                # Skip if duplicate
                if email_hash in processed_hashes:
                    log_message(f"Skipping duplicate: {subject[:60]}")
                    processed_message_ids.add(msg_id)
                    continue
                
                # Extract links
                links = extract_links(plain_text, html_text)
                log_message(f"Email: {subject[:60]} - Found {len(links)} links")
                
                # Fetch link content
                links_content = []
                if links:
                    with ThreadPoolExecutor(max_workers=HTTP_CONCURRENT) as executor:
                        futures = {executor.submit(fetch_link_content, url): url for url in links}
                        for future in as_completed(futures):
                            result = future.result()
                            if result:
                                links_content.append(result)
                
                emails_to_process.append({
                    "message_id": msg_id,
                    "subject": subject,
                    "from": from_email,
                    "date": email_date.strftime("%Y-%m-%d"),
                    "body": body[:2000],  # Limit body size
                    "links": links,
                    "links_content": links_content,
                    "hash": email_hash
                })
                
            except Exception as e:
                log_message(f"Error processing email {msg_id}: {e}")
                continue
        
        if not emails_to_process:
            log_message("No new emails to process after deduplication")
            return
        
        log_message(f"Processing {len(emails_to_process)} new emails in batches of {BATCH_SIZE}...")
        
        # Process in batches
        all_extracted = []
        for i in range(0, len(emails_to_process), BATCH_SIZE):
            batch = emails_to_process[i:i+BATCH_SIZE]
            log_message(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch)} emails)...")
            
            extracted = batch_process_with_claude(batch)
            all_extracted.extend(extracted)
        
        # Save extracted data
        saved_count = 0
        for extracted in all_extracted:
            email_index = extracted.get("email_index", 1) - 1
            if email_index < len(emails_to_process):
                email_data = emails_to_process[email_index]
                
                specs = extracted.get("specifications", {})
                best_practices = extracted.get("best_practices", [])
                
                source_info = {
                    "subject": email_data["subject"],
                    "date": email_data["date"],
                    "message_id": email_data["message_id"],
                    "tags": extracted.get("tags", [])
                }
                
                if specs:
                    category = specs.get("category", "google-ads")
                    subcategory = specs.get("subcategory", "platform-updates")
                    spec_content = specs.get("specs", {})
                    
                    if spec_content:
                        title = spec_content.get("title", email_data["subject"][:50])
                        filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".json"
                        
                        save_specification(category, subcategory, filename, spec_content, source_info)
                        saved_count += 1
                
                if best_practices:
                    category = specs.get("category", "google-ads") if specs else "google-ads"
                    subcategory = specs.get("subcategory", "platform-updates") if specs else "platform-updates"
                    title = email_data["subject"][:50]
                    filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".md"
                    
                    save_best_practice(category, subcategory, filename, title, best_practices, source_info)
                    saved_count += 1
                
                # Mark as processed
                processed_hashes.add(email_data["hash"])
                processed_message_ids.add(email_data["message_id"])
        
        # Save state
        state["processed_hashes"] = list(processed_hashes)
        state["processed_message_ids"] = list(processed_message_ids)
        save_processed_emails(state)
        
        log_message("=" * 60)
        log_message(f"Processing Complete: {len(emails_to_process)} emails processed, {saved_count} files saved")
        log_message("=" * 60)
    
    except Exception as e:
        log_message(f"ERROR: {e}")
        import traceback
        log_message(traceback.format_exc())


if __name__ == "__main__":
    process_feature_emails()

