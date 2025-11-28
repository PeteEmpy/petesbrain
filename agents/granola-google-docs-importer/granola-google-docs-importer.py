#!/usr/bin/env python3
"""
Granola Google Docs Importer

Pulls Granola meeting notes from Google Docs (created by Zapier) and processes them:
1. Finds documents matching "ROK | Granola -" pattern in Shared Drive
2. Parses meeting title, attendees, and transcript
3. Detects client using existing client detection logic
4. Saves to clients/[client]/meeting-notes/ or _unassigned
5. Extracts action items and creates Google Tasks
6. Tracks unmatched meetings for reporting

Runs automatically via LaunchAgent or manually on-demand.
"""

import os
import sys
import re
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Tuple

# Anthropic for AI analysis
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  Anthropic library not available - AI summaries will be skipped")

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import existing client detector
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "granola-importer"))
try:
    from client_detector import ClientDetector
    CLIENT_DETECTOR_AVAILABLE = True
except ImportError:
    print("⚠️  Client detector not available - client detection will be limited")
    CLIENT_DETECTOR_AVAILABLE = False

# Import Google Tasks client
try:
    from shared.google_tasks_client import GoogleTasksClient
    GOOGLE_TASKS_AVAILABLE = True
except ImportError:
    print("⚠️  Google Tasks integration not available")
    GOOGLE_TASKS_AVAILABLE = False

# Configuration
CLIENTS_DIR = PROJECT_ROOT / "clients"
UNASSIGNED_DIR = CLIENTS_DIR / "_unassigned" / "meeting-notes"
HISTORY_FILE = PROJECT_ROOT / "shared" / "data" / "granola-google-docs-history.json"
UNMATCHED_FILE = PROJECT_ROOT / "shared" / "data" / "granola-unmatched-meetings.json"

# Document name pattern: "ROK | Granola - [date] [time]"
DOC_PATTERN = re.compile(r'ROK\s*\|\s*Granola\s*-\s*(.+)', re.IGNORECASE)


class GranolaGoogleDocsImporter:
    """Imports Granola meetings from Google Docs created by Zapier."""

    def __init__(self, enable_granola_api: bool = True, enable_ai_analysis: bool = True):
        """Initialize importer."""
        self.clients_dir = CLIENTS_DIR
        self.unassigned_dir = UNASSIGNED_DIR
        self.unassigned_dir.mkdir(parents=True, exist_ok=True)

        # Initialize client detector
        if CLIENT_DETECTOR_AVAILABLE:
            self.detector = ClientDetector(self.clients_dir)
        else:
            self.detector = None

        # Load history
        self.history = self._load_history()
        self.unmatched = self._load_unmatched()

        # Initialize Google Tasks client
        self.tasks_client = None
        if GOOGLE_TASKS_AVAILABLE:
            try:
                self.tasks_client = GoogleTasksClient()
            except Exception as e:
                print(f"⚠️  Could not initialize Google Tasks: {e}")

        # Initialize Granola API for attendee enrichment
        self.granola_api = None
        if enable_granola_api:
            try:
                sys.path.insert(0, str(PROJECT_ROOT / "tools" / "granola-importer"))
                from granola_api import GranolaAPI
                self.granola_api = GranolaAPI()
                print("✓ Granola API initialized for attendee enrichment")
            except Exception as e:
                print(f"⚠️  Granola API not available: {e}")

        # Initialize Anthropic client for AI analysis
        self.anthropic_client = None
        self.enable_ai_analysis = enable_ai_analysis
        if enable_ai_analysis and ANTHROPIC_AVAILABLE:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                print("✓ Claude AI initialized for meeting analysis")
            else:
                print("⚠️  ANTHROPIC_API_KEY not set - AI analysis disabled")

    def _load_history(self) -> Dict:
        """Load import history."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"imported": {}, "last_check": None}

    def _save_history(self):
        """Save import history."""
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)

    def _load_unmatched(self) -> List[Dict]:
        """Load unmatched meetings list."""
        if UNMATCHED_FILE.exists():
            try:
                with open(UNMATCHED_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_unmatched(self):
        """Save unmatched meetings list."""
        UNMATCHED_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(UNMATCHED_FILE, 'w') as f:
            json.dump(self.unmatched, f, indent=2)

    def _is_imported(self, doc_id: str) -> bool:
        """Check if document has been imported."""
        return doc_id in self.history.get("imported", {})

    def _mark_imported(self, doc_id: str, file_path: str, client_slug: Optional[str]):
        """Mark document as imported."""
        if "imported" not in self.history:
            self.history["imported"] = {}
        
        self.history["imported"][doc_id] = {
            "file_path": str(file_path),
            "client": client_slug,
            "imported_at": datetime.now().isoformat()
        }
        self._save_history()

    def parse_google_doc(self, doc_content: str, doc_name: str) -> Dict:
        """
        Parse Google Doc content to extract meeting information.
        
        Expected format:
        - Title at top
        - Attendees section
        - Full transcript
        
        Args:
            doc_content: Full text content of Google Doc
            doc_name: Name of the document (for date/time extraction)
        
        Returns:
            Dictionary with meeting metadata
        """
        lines = doc_content.split('\n')
        
        # Extract date/time from document name
        # Format: "ROK | Granola - 2025-11-07 14:30"
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})', doc_name)
        meeting_date = None
        meeting_time = None
        
        if date_match:
            meeting_date = date_match.group(1)
            meeting_time = date_match.group(2)
        else:
            # Try other date formats
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', doc_name)
            if date_match:
                try:
                    dt = datetime.strptime(f"{date_match.group(1)} {date_match.group(2)}", "%d/%m/%Y %H:%M")
                    meeting_date = dt.strftime("%Y-%m-%d")
                    meeting_time = dt.strftime("%H:%M")
                except ValueError:
                    pass
        
        # Default to today if no date found
        if not meeting_date:
            meeting_date = datetime.now().strftime("%Y-%m-%d")
            meeting_time = datetime.now().strftime("%H:%M")
        
        # Extract title (usually first non-empty line or first heading)
        title = None
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) > 5:  # Skip very short lines
                # Skip common headers
                if not re.match(r'^(Attendees?|Participants?|Transcript|Meeting|Date|Time):', line, re.IGNORECASE):
                    title = line
                    break
        
        if not title:
            title = doc_name.replace("ROK | Granola -", "").strip()
        
        # Extract attendees
        attendees = []
        in_attendees_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Detect attendees section
            if re.match(r'^(attendees?|participants?):', line_lower):
                in_attendees_section = True
                continue
            
            # Stop at transcript section
            if re.match(r'^(transcript|conversation|meeting notes?):', line_lower):
                in_attendees_section = False
                break
            
            # Extract attendees while in section
            if in_attendees_section and line.strip():
                # Remove bullets/dashes
                attendee = re.sub(r'^[-*•]\s*', '', line.strip())
                if attendee:
                    attendees.append(attendee)
        
        # Extract transcript (everything after "Transcript" or "Conversation" header)
        transcript_start = None
        for i, line in enumerate(lines):
            if re.match(r'^(transcript|conversation|meeting notes?|full transcript):', line.lower()):
                transcript_start = i + 1
                break
        
        if transcript_start:
            transcript = '\n'.join(lines[transcript_start:]).strip()
        else:
            # If no explicit transcript header, assume everything after title/attendees is transcript
            transcript = '\n'.join(lines[5:]).strip()
        
        return {
            "title": title,
            "date": meeting_date,
            "time": meeting_time,
            "attendees": attendees,
            "transcript": transcript,
            "full_content": doc_content
        }

    def enrich_with_granola_attendees(self, meeting_data: Dict, doc_name: str) -> Dict:
        """
        Enrich meeting data with attendee information from Granola API.

        Args:
            meeting_data: Parsed meeting data from Google Doc
            doc_name: Original document name

        Returns:
            Enriched meeting data with attendees
        """
        if not self.granola_api:
            return meeting_data

        try:
            # Extract timestamp from document name
            # Format: "ROK | Granola - 2025-11-07T17:41:50+00:00"
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', doc_name)
            if not timestamp_match:
                return meeting_data

            doc_timestamp = timestamp_match.group(1)
            # Make timezone-aware (UTC)
            from datetime import timezone
            doc_datetime = datetime.fromisoformat(doc_timestamp).replace(tzinfo=timezone.utc)

            # Get recent meetings from Granola
            granola_docs = self.granola_api.get_recent_documents(days=14)

            # Find matching meeting by timestamp (within 2 hours)
            for doc in granola_docs:
                created_at = doc.get('created_at', '')
                if not created_at:
                    continue

                try:
                    # Parse Granola timestamp: "2025-11-07T12:55:52.827Z"
                    granola_datetime = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

                    # Check if timestamps are within 2 hours
                    time_diff = abs((doc_datetime - granola_datetime).total_seconds())
                    if time_diff <= 7200:  # 2 hours in seconds
                        # Extract attendees from Granola data
                        people = doc.get('people', {})
                        attendees_data = people.get('attendees', [])

                        attendees = []
                        attendee_emails = []
                        for att in attendees_data:
                            email = att.get('email', '')
                            if email and email != 'petere@roksys.co.uk':  # Skip self
                                attendee_emails.append(email)

                                # Get full name if available
                                details = att.get('details', {})
                                person = details.get('person', {})
                                name_data = person.get('name', {})
                                full_name = name_data.get('fullName', '')

                                if full_name:
                                    attendees.append(f"{full_name} ({email})")
                                else:
                                    attendees.append(email)

                        if attendees:
                            meeting_data['attendees'] = attendees
                            meeting_data['attendee_emails'] = attendee_emails
                            granola_title = doc.get('title', 'Unknown')
                            print(f"   ✓ Matched Granola meeting: '{granola_title}'")
                            print(f"   ✓ Enriched with {len(attendees)} attendee(s) from Granola API")

                        # CRITICAL: Extract actual meeting date from Google Calendar event
                        calendar_event = doc.get('google_calendar_event', {})
                        if calendar_event:
                            start_info = calendar_event.get('start', {})
                            meeting_start = start_info.get('dateTime', '')

                            if meeting_start:
                                try:
                                    # Parse: "2025-11-10T10:00:00Z" or "2025-11-10T10:00:00+00:00"
                                    actual_datetime = datetime.fromisoformat(meeting_start.replace('Z', '+00:00'))

                                    # Update meeting_data with ACTUAL meeting date, not import date
                                    meeting_data['date'] = actual_datetime.strftime('%Y-%m-%d')
                                    meeting_data['time'] = actual_datetime.strftime('%H:%M')
                                    meeting_data['actual_meeting_date'] = actual_datetime.strftime('%Y-%m-%d')

                                    print(f"   ✓ Updated to ACTUAL meeting date: {meeting_data['date']} {meeting_data['time']}")
                                except (ValueError, AttributeError) as e:
                                    print(f"   ⚠️  Could not parse calendar event date: {e}")

                        break

                except (ValueError, AttributeError):
                    continue

        except Exception as e:
            print(f"   ⚠️  Could not enrich attendees from Granola: {e}")

        return meeting_data

    def detect_client(self, meeting_data: Dict) -> Tuple[Optional[str], float, str]:
        """
        Detect client from meeting data using existing client detector.

        Returns:
            (client_slug, confidence, method)
        """
        if not self.detector:
            # Fallback: simple keyword matching
            content = f"{meeting_data['title']}\n{meeting_data['transcript']}"
            return self._simple_client_match(content), 50.0, "keyword"

        # Extract attendee emails if available
        attendee_emails = meeting_data.get('attendee_emails', [])

        if not attendee_emails:
            # Try to extract from attendees strings
            for attendee in meeting_data.get("attendees", []):
                # Try to extract email from attendee string
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', attendee)
                if email_match:
                    attendee_emails.append(email_match.group(0))

        # Use existing detector
        client_slug, confidence, method = self.detector.detect_with_confidence(
            meeting_data['title'],
            meeting_content=meeting_data['transcript'],
            attendee_emails=attendee_emails if attendee_emails else None
        )

        return client_slug, confidence, method

    def _simple_client_match(self, content: str) -> Optional[str]:
        """Simple fallback client matching."""
        content_lower = content.lower()

        # Load client list
        clients = []
        if self.clients_dir.exists():
            for item in self.clients_dir.iterdir():
                if item.is_dir() and not item.name.startswith("_"):
                    clients.append(item.name)

        # Simple keyword matching
        for client in clients:
            client_variations = [
                client,
                client.replace("-", " "),
                client.replace("-", "")
            ]
            for variation in client_variations:
                if variation.lower() in content_lower:
                    return client

        return None

    def analyze_meeting_with_ai(self, meeting_data: Dict, client_slug: Optional[str]) -> Optional[Dict]:
        """
        Analyze meeting transcript with Claude AI to extract insights.

        Args:
            meeting_data: Parsed meeting data
            client_slug: Detected client slug (or None)

        Returns:
            Dictionary with analysis results or None if AI unavailable
        """
        if not self.anthropic_client or not self.enable_ai_analysis:
            return None

        try:
            client_name = client_slug.replace("-", " ").title() if client_slug else "Unknown Client"

            prompt = f"""Analyze this meeting transcript and extract key insights.

Meeting: {meeting_data['title']}
Date: {meeting_data['date']}
Client: {client_name}
Attendees: {', '.join(meeting_data.get('attendees', []))}

Transcript:
{meeting_data['transcript'][:8000]}

Please extract the following in JSON format:

{{
  "executive_summary": ["bullet point 1", "bullet point 2", "bullet point 3"],
  "strategic_decisions": ["decision 1", "decision 2"],
  "key_learnings": ["learning 1", "learning 2"],
  "client_preferences": ["preference 1", "preference 2"],
  "action_items_mentioned": ["action 1", "action 2"],
  "context_md_suggestions": {{
    "strategic_context": ["suggested update 1"],
    "key_learnings": ["suggested learning 1"],
    "client_preferences": ["suggested preference 1"]
  }}
}}

Focus on:
- Strategic decisions about campaigns, budgets, or direction
- Key insights about performance or strategy
- Client preferences or constraints mentioned
- Important context that should be remembered

Be concise. If a section has no relevant content, use empty array."""

            message = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",  # Fast, cheap model
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Try to find JSON in response (may be wrapped in markdown)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group(0))
                print(f"   ✓ AI analysis complete ({len(analysis.get('executive_summary', []))} key points)")
                return analysis
            else:
                print(f"   ⚠️  Could not parse AI response as JSON")
                return None

        except Exception as e:
            print(f"   ⚠️  AI analysis failed: {e}")
            return None

    def extract_action_items_comprehensive(self, meeting_data: Dict) -> List[Dict]:
        """
        Extract action items using Claude API multi-pass analysis.

        Returns list of action items with:
        - task: Task text
        - priority: P0 (urgent/today), P1 (this week), P2 (this month), P3 (tracking)
        - due_date: Calculated due date string
        - context: 2-3 sentences of context
        - type: 'action' (for Pete), 'external' (waiting on others), 'strategic' (CONTEXT.md note)
        - meeting_title: Meeting title
        - meeting_date: Meeting date
        """
        # Get meeting details
        transcript = meeting_data.get('transcript', '') + '\n' + meeting_data.get('full_content', '')
        meeting_title = meeting_data.get('title', 'Untitled Meeting')
        meeting_date = meeting_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        attendees = meeting_data.get('attendees', [])

        # Prepare Claude API request
        system_prompt = """You are an expert task extraction assistant for a Google Ads consultant.
Analyze meeting transcripts to extract ALL action items and commitments.

CRITICAL: These are important client meetings. Do not miss ANY commitments,
whether explicit or implicit. Pete often commits conversationally without formal language.

Extract 3 types of items:

1. **ACTIONS** (for Pete): Tasks Pete committed to do
   - Explicit commitments: "Pete to...", "Pete: [action]", "I'll...", "I will..."
   - Conversational commitments: "what I might do", "what I'll do", "I'm going to...", "I can do that", "I'll create", "I'll track"
   - Softer commitments: "We need to... I can...", "Should... I'll...", "Let's... [Pete agrees]"
   - Questions that turn into actions: "Can I ask..." followed by agreement
   - Verbs: analyze, review, email, update, implement, fix, optimize, check, send, create, track, download

2. **EXTERNAL** (waiting on others): Tasks assigned to others or dependencies
   - Explicit: "[Name] to...", "[Name]: [action]"
   - Dependencies: "Once [X] happens, then..."
   - Follow-ups: "After [person] sends..."

3. **STRATEGIC** (for CONTEXT.md): Important business context, not tasks
   - Strategic decisions or direction changes
   - Key insights about client business
   - Performance patterns or anomalies
   - Important dates or deadlines

For each item, provide:
- **task**: Clear, actionable task text (start with verb for actions)
- **priority**:
  - P0: Urgent/ASAP/today (words: urgent, ASAP, immediately, today, now)
  - P1: This week (words: this week, soon, shortly, by [day this week])
  - P2: This month (words: this month, by [date this month])
  - P3: Future/tracking (words: next month, eventually, when, after)
- **due_date**: YYYY-MM-DD or "TBD"
- **context**: 2-3 sentences explaining what/why/background
- **type**: "action", "external", or "strategic"

EXAMPLES OF CONVERSATIONAL COMMITMENTS TO CATCH:
- "what I might do is... I'm going to track..." → ACTION (Pete committing to track)
- "I can do that and run it and see..." → ACTION (Pete agreeing to investigate)
- "Can I ask if we could just do a simple thing..." [Client agrees] → ACTION (Pete requesting and getting agreement)
- "[Client] will create a checklist" → EXTERNAL (waiting on client)

DO NOT MISS: Soft commitments, "might do" followed by "going to", requests that get approved.

Output ONLY valid JSON array with no markdown formatting or code blocks. Start with [ and end with ]."""

        user_prompt = f"""Meeting Title: {meeting_title}
Meeting Date: {meeting_date}
Attendees: {', '.join(attendees) if attendees else 'Not specified'}

Transcript:
{transcript[:15000]}

Extract ALL action items, external dependencies, and strategic notes from this meeting."""

        try:
            print(f"  🤖 Analyzing with Claude API...")

            # Call Claude API
            response = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Parse JSON response
            response_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = re.sub(r'^```(?:json)?\n', '', response_text)
                response_text = re.sub(r'\n```$', '', response_text)

            extracted_items = json.loads(response_text)

            print(f"  ✅ Extracted {len(extracted_items)} items")

            # Filter and format for Google Tasks
            action_items = []
            external_count = 0
            strategic_count = 0

            for item in extracted_items:
                # Only create tasks for Pete's actions (type='action')
                if item.get('type') == 'action':
                    action_items.append({
                        'task': item['task'],
                        'priority': item.get('priority', 'P2'),
                        'due_date': item.get('due_date', 'TBD'),
                        'context': item.get('context', ''),
                        'meeting_title': meeting_title,
                        'meeting_date': meeting_date
                    })
                    print(f"    📋 [{item.get('priority', 'P2')}] {item['task']}")

                # Log external dependencies (don't create tasks, just track)
                elif item.get('type') == 'external':
                    external_count += 1
                    print(f"    📌 External: {item['task']}")

                # Log strategic notes (add to meeting frontmatter or CONTEXT.md)
                elif item.get('type') == 'strategic':
                    strategic_count += 1
                    print(f"    💡 Strategic: {item['task']}")

            print(f"  📊 Summary: {len(action_items)} actions, {external_count} external, {strategic_count} strategic")

            return action_items

        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse Claude response as JSON: {e}")
            print(f"  Response was: {response_text[:200]}...")
            print(f"  Falling back to basic regex extraction...")
            return self.extract_action_items_basic(meeting_data)

        except Exception as e:
            print(f"⚠️  Claude API extraction failed: {e}")
            print(f"  Falling back to basic regex extraction...")
            return self.extract_action_items_basic(meeting_data)

    def extract_action_items_basic(self, meeting_data: Dict) -> List[Dict]:
        """
        Fallback: Basic regex extraction.

        Uses same logic as generate_daily_tasks.py
        """
        content = meeting_data.get('transcript', '') + '\n' + meeting_data.get('full_content', '')
        action_items = []

        # Look for action item sections
        action_patterns = [
            r'###\s*Action\s+Items?\s*\n(.*?)(?=\n###|\n---|\Z)',
            r'###\s*Next\s+Steps?\s*\n(.*?)(?=\n###|\n---|\Z)',
            r'###\s*Action\s+Points?\s*\n(.*?)(?=\n###|\n---|\Z)',
            r'###\s*To\s*-?\s*Do\s*\n(.*?)(?=\n###|\n---|\Z)',
            r'Action\s+Items?:\s*\n(.*?)(?=\n\n|\Z)',
            r'Next\s+Steps?:\s*\n(.*?)(?=\n\n|\Z)',
        ]

        for pattern in action_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)

            for match in matches:
                action_section = match.group(1)

                # Extract bullet points
                bullet_items = re.findall(r'^[-*•]\s+(.+?)$', action_section, re.MULTILINE)

                for item in bullet_items:
                    # Check if this is for Peter
                    is_for_peter = False
                    task_text = item

                    # Pattern 1: "Peter: Do something"
                    if re.match(r'^Peter\s*:\s*(.+)', item, re.IGNORECASE):
                        is_for_peter = True
                        task_text = re.sub(r'^Peter\s*:\s*', '', item, flags=re.IGNORECASE)

                    # Pattern 2: General team items (no specific person mentioned)
                    elif not re.match(r'^[A-Z][a-z]+\s*:', item):
                        is_for_peter = True
                        task_text = item

                    # Pattern 3: "Team:" items
                    elif re.match(r'^Team\s*:\s*(.+)', item, re.IGNORECASE):
                        is_for_peter = True
                        task_text = re.sub(r'^Team\s*:\s*', '', item, flags=re.IGNORECASE)

                    if is_for_peter:
                        action_items.append({
                            'task': task_text.strip(),
                            'priority': 'P2',  # Default priority for fallback
                            'due_date': 'TBD',
                            'context': '',
                            'meeting_title': meeting_data['title'],
                            'meeting_date': meeting_data['date']
                        })

        return action_items

    def create_meeting_file(self, meeting_data: Dict, client_slug: Optional[str], 
                          ai_analysis: Optional[Dict] = None, 
                          tasks_created: List[Dict] = None,
                          client_detection: Dict = None) -> Path:
        """
        Create markdown file for meeting.
        
        Args:
            meeting_data: Parsed meeting data
            client_slug: Client slug or None for unassigned
        
        Returns:
            Path to created file
        """
        if client_slug:
            output_dir = self.clients_dir / client_slug / "meeting-notes"
        else:
            output_dir = self.unassigned_dir
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        date = meeting_data['date']
        title_slug = re.sub(r'[^a-z0-9-]', '-', meeting_data['title'].lower())
        title_slug = re.sub(r'-+', '-', title_slug)[:50]
        
        if client_slug:
            filename = f"{date}-{title_slug}-{client_slug}.md"
        else:
            filename = f"{date}-{title_slug}.md"
        
        file_path = output_dir / filename
        
        # Handle duplicates
        counter = 1
        while file_path.exists():
            if client_slug:
                filename = f"{date}-{title_slug}-{client_slug}-{counter}.md"
            else:
                filename = f"{date}-{title_slug}-{counter}.md"
            file_path = output_dir / filename
            counter += 1
        
        # Build markdown content
        metadata = {
            "title": meeting_data['title'],
            "date": meeting_data['date'],
            "time": meeting_data['time'],
            "attendees": meeting_data['attendees'],
            "client": client_slug,
            "source": "Google Docs (Zapier)",
            "imported_at": datetime.now().isoformat()
        }

        # Add tasks_generated flag to prevent duplicate generation in daily briefing
        if tasks_created and len(tasks_created) > 0:
            metadata['tasks_generated'] = True
            metadata['tasks_generated_date'] = datetime.now().isoformat()
            metadata['tasks_created_count'] = len(tasks_created)

        # Add processing metadata to frontmatter
        if client_detection:
            metadata['processing'] = {
                'client_detection': {
                    'detected': client_slug,
                    'confidence': client_detection.get('confidence'),
                    'method': client_detection.get('method')
                },
                'ai_analysis': bool(ai_analysis),
                'model': 'claude-3-5-haiku-20241022' if ai_analysis else None,
                'action_items_extracted': len(tasks_created) if tasks_created else 0,
                'tasks_created': len(tasks_created) if tasks_created else 0
            }
        
        content_parts = [
            "---",
            yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip(),
            "---",
            "",
            f"# {meeting_data['title']}",
            "",
            f"**Date:** {meeting_data['date']} {meeting_data.get('time', '')}",
            "",
        ]

        # Add processing history section
        content_parts.extend([
            "## Processing History",
            "",
            f"**Imported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Source:** Google Doc (Zapier) → Granola API enrichment",
        ])
        
        if ai_analysis:
            content_parts.append("**AI Analysis:** ✅ Yes (claude-3-5-haiku-20241022)")
        else:
            content_parts.append("**AI Analysis:** ❌ No")
        
        if client_detection:
            content_parts.append(f"**Client Detection:** {client_slug or 'Not detected'} ({client_detection.get('confidence', 0)}% via {client_detection.get('method', 'unknown')})")
        
        action_items_count = len(tasks_created) if tasks_created else 0
        content_parts.append(f"**Action Items Extracted:** {action_items_count}")
        content_parts.append(f"**Google Tasks Created:** {action_items_count}")
        
        if tasks_created:
            content_parts.extend([
                "",
                "**Tasks Created:**",
            ])
            for task in tasks_created:
                task_id = task.get('id', 'N/A')
                task_title = task.get('title', 'Unknown')
                task_type = task.get('type', 'unknown')
                content_parts.append(f"- ✅ {task_title} (Google Task: `{task_id}`, Type: {task_type})")
        
        content_parts.extend(["", "---", ""])

        # Add AI-generated executive summary
        if ai_analysis and ai_analysis.get('executive_summary'):
            content_parts.extend([
                "## Executive Summary",
                "",
            ])
            for point in ai_analysis['executive_summary']:
                content_parts.append(f"- {point}")
            content_parts.append("")

        if meeting_data.get('attendees'):
            content_parts.extend([
                "## Attendees",
                "",
            ])
            for attendee in meeting_data['attendees']:
                content_parts.append(f"- {attendee}")
            content_parts.append("")

        # Add strategic insights if available
        if ai_analysis:
            if ai_analysis.get('strategic_decisions'):
                content_parts.extend([
                    "## Strategic Decisions",
                    "",
                ])
                for decision in ai_analysis['strategic_decisions']:
                    content_parts.append(f"- {decision}")
                content_parts.append("")

            if ai_analysis.get('key_learnings'):
                content_parts.extend([
                    "## Key Learnings",
                    "",
                ])
                for learning in ai_analysis['key_learnings']:
                    content_parts.append(f"- {learning}")
                content_parts.append("")

        if meeting_data.get('transcript'):
            content_parts.extend([
                "## Transcript",
                "",
                meeting_data['transcript'],
                ""
            ])
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        
        return file_path

    def task_already_exists(self, task_title: str, tasklist_id: str) -> bool:
        """Check if task with similar title already exists in Google Tasks."""
        try:
            existing_tasks = self.tasks_client.list_tasks(tasklist_id, show_completed=False)

            for existing_task in existing_tasks:
                # Normalize titles for comparison
                existing_normalized = existing_task['title'].lower().strip()
                new_normalized = task_title.lower().strip()

                # Check for exact match
                if existing_normalized == new_normalized:
                    return True

                # Check for substring match (covers "[HIGH]" prefix variations)
                # Remove common prefixes for better matching
                existing_clean = re.sub(r'^\[(urgent|high|tracking)\]\s*', '', existing_normalized, flags=re.IGNORECASE)
                new_clean = re.sub(r'^\[(urgent|high|tracking)\]\s*', '', new_normalized, flags=re.IGNORECASE)

                if existing_clean == new_clean:
                    return True

            return False
        except Exception as e:
            print(f"⚠️  Error checking for duplicate tasks: {e}")
            return False  # If check fails, allow creation (safer than blocking)

    def create_google_tasks(self, action_items: List[Dict], client_slug: Optional[str]) -> List[Dict]:
        """Create Google Tasks from action items with priority and due dates.

        Returns:
            List of created task dictionaries with 'title' and 'id'
        """
        created_tasks = []
        if not self.tasks_client or not action_items:
            return created_tasks

        try:
            # Get or create task list
            tasklist_name = "Client Action Items"
            tasklist_id = self.tasks_client.get_or_create_tasklist(tasklist_name)

            for item in action_items:
                # Build task title with priority
                priority_label = {
                    'P0': '[URGENT]',
                    'P1': '[HIGH]',
                    'P2': '',
                    'P3': '[TRACKING]'
                }.get(item.get('priority', 'P2'), '')

                if client_slug:
                    title = f"{priority_label} [{client_slug}] {item['task']}"
                else:
                    title = f"{priority_label} [Unassigned] {item['task']}"

                title = title.strip()  # Remove leading space if no priority label

                # Check for duplicates
                if self.task_already_exists(title, tasklist_id):
                    print(f"  ⏭️  Skipping duplicate: {title}")
                    continue

                # Build notes with context
                notes = f"From: {item['meeting_title']}\n"
                notes += f"Date: {item['meeting_date']}\n"
                notes += f"AI Generated ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

                if item.get('context'):
                    notes += f"\n\nContext:\n{item['context']}"

                # Calculate due date
                due_date = None
                if item.get('due_date') and item['due_date'] != 'TBD':
                    due_date = item['due_date']
                elif item.get('priority') == 'P0':
                    # Urgent: due today
                    due_date = datetime.now().strftime('%Y-%m-%d')
                elif item.get('priority') == 'P1':
                    # High: due end of week (Friday)
                    today = datetime.now()
                    days_until_friday = (4 - today.weekday()) % 7
                    if days_until_friday == 0:  # Today is Friday
                        days_until_friday = 7  # Next Friday
                    friday = today + timedelta(days=days_until_friday)
                    due_date = friday.strftime('%Y-%m-%d')

                # Create task with due date
                task = self.tasks_client.create_task(
                    tasklist_id=tasklist_id,
                    title=title,
                    notes=notes,
                    due=due_date
                )

                if task:
                    created_tasks.append({
                        'title': title,
                        'id': task.get('id'),
                        'type': 'action_item',
                        'priority': item.get('priority', 'P2'),
                        'due_date': due_date
                    })
                    print(f"  ✅ Created: {title}")

        except Exception as e:
            print(f"⚠️  Error creating Google Tasks: {e}")

        return created_tasks

    def send_p0_notifications(self, p0_tasks: List[Dict], meeting_data: Dict, client_slug: Optional[str]):
        """
        Send email and macOS notifications for P0 urgent tasks.

        Args:
            p0_tasks: List of P0 priority tasks
            meeting_data: Meeting data dictionary
            client_slug: Client slug (or None for unassigned)
        """
        if not p0_tasks:
            return

        print(f"\n  🚨 Sending P0 notifications for {len(p0_tasks)} urgent task(s)...")

        # Send macOS notification (immediate visual alert)
        self._send_macos_notification(p0_tasks, meeting_data)

        # Send email notification (persistent record)
        self._send_email_notification(p0_tasks, meeting_data, client_slug)

    def _send_macos_notification(self, p0_tasks: List[Dict], meeting_data: Dict):
        """Send macOS notification for P0 tasks"""
        import subprocess

        meeting_title = meeting_data.get('title', 'Unknown Meeting')

        for task in p0_tasks:
            title = "⚠️ URGENT Task from Meeting"
            task_text = task.get('task', 'Unknown task')
            message = f"{task_text}\\n\\nFrom: {meeting_title}"

            # Use macOS osascript to show notification
            script = f'display notification "{message}" with title "{title}" sound name "Basso"'

            try:
                subprocess.run(['osascript', '-e', script], check=False, capture_output=True)
                print(f"    ✅ macOS notification sent")
            except Exception as e:
                print(f"    ⚠️  Failed to send macOS notification: {e}")

    def _send_email_notification(self, p0_tasks: List[Dict], meeting_data: Dict, client_slug: Optional[str]):
        """Send email notification for P0 tasks"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Email config (use environment variables)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('GMAIL_USER')
        sender_password = os.getenv('GMAIL_APP_PASSWORD')
        recipient_email = sender_email  # Send to self

        if not sender_email or not sender_password:
            print("    ⚠️  Email credentials not configured - skipping email notification")
            return

        # Build email
        meeting_title = meeting_data.get('title', 'Unknown Meeting')
        meeting_date = meeting_data.get('date', 'Unknown Date')
        attendees = meeting_data.get('attendees', [])

        subject = f"⚠️ URGENT: {len(p0_tasks)} Task(s) from Meeting - {meeting_title}"

        body = f"""URGENT TASK ALERT

{len(p0_tasks)} high-priority P0 task(s) were created from your meeting:

Meeting: {meeting_title}
Date: {meeting_date}
Attendees: {', '.join(attendees) if attendees else 'Not specified'}
Client: {client_slug.replace('-', ' ').title() if client_slug else 'Unassigned'}

═══════════════════════════════════════════════════════════════

"""

        for i, task in enumerate(p0_tasks, 1):
            task_title = task.get('task', 'Unknown task')
            context = task.get('context', 'No context provided')
            due_date = task.get('due_date', 'TBD')

            body += f"""
🔴 URGENT TASK {i}:
{task_title}

Due: {due_date if due_date != 'TBD' else 'TODAY'}
Time Estimate: {task.get('time_estimate', 'Not specified')}

Context:
{context[:300]}{'...' if len(context) > 300 else ''}

───────────────────────────────────────────────────────────────

"""

        body += """
═══════════════════════════════════════════════════════════════

These tasks require immediate attention and have been added to your Google Tasks.

View all tasks in priority order by running "view tasks" in Claude Code.

─ Automated notification from Pete's Brain
"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"    ✅ Email notification sent to {recipient_email}")
        except Exception as e:
            print(f"    ⚠️  Failed to send email: {e}")

    def create_review_task(self, meeting_data: Dict, client_slug: Optional[str],
                          file_path: Path, ai_analysis: Optional[Dict] = None) -> Optional[Dict]:
        """
        Create a review task for updating CONTEXT.md with meeting insights.

        Args:
            meeting_data: Meeting data dictionary
            client_slug: Client slug (or None for unassigned)
            file_path: Path to meeting file
            ai_analysis: AI analysis results (optional)
        
        Returns:
            Task dictionary with 'title' and 'id', or None if not created
        """
        if not self.tasks_client:
            return None

        try:
            # Get or create task list
            tasklist_name = "Client Action Items"
            tasklist_id = self.tasks_client.get_or_create_tasklist(tasklist_name)

            # Build task title
            meeting_title = meeting_data['title'][:50]  # Truncate if too long
            if client_slug:
                client_display = client_slug.replace("-", " ").title()
                title = f"[{client_slug}] Review meeting: {meeting_title}"
            else:
                title = f"Review meeting: {meeting_title}"

            # Build task notes with AI-suggested updates
            notes_parts = [
                f"Meeting: {meeting_data['title']}",
                f"Date: {meeting_data['date']}",
                f"File: {file_path}",
                "",
            ]

            if ai_analysis:
                context_suggestions = ai_analysis.get('context_md_suggestions', {})

                if context_suggestions.get('strategic_context'):
                    notes_parts.extend([
                        "SUGGESTED CONTEXT.MD UPDATES:",
                        "",
                        "Strategic Context:",
                    ])
                    for item in context_suggestions['strategic_context']:
                        notes_parts.append(f"- {item}")
                    notes_parts.append("")

                if context_suggestions.get('key_learnings'):
                    notes_parts.extend([
                        "Key Learnings:",
                    ])
                    for item in context_suggestions['key_learnings']:
                        notes_parts.append(f"- {item}")
                    notes_parts.append("")

                if context_suggestions.get('client_preferences'):
                    notes_parts.extend([
                        "Client Preferences:",
                    ])
                    for item in context_suggestions['client_preferences']:
                        notes_parts.append(f"- {item}")
                    notes_parts.append("")

                if ai_analysis.get('strategic_decisions'):
                    notes_parts.extend([
                        "Strategic Decisions:",
                    ])
                    for decision in ai_analysis['strategic_decisions'][:3]:  # Limit to 3
                        notes_parts.append(f"- {decision}")
                    notes_parts.append("")

            notes_parts.append("Review meeting notes and update CONTEXT.md with key insights.")

            # Set due date (2 days from now)
            from datetime import timezone
            due_date = datetime.now(timezone.utc) + timedelta(days=2)
            due_str = due_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            # Create task
            task = self.tasks_client.create_task(
                tasklist_id=tasklist_id,
                title=title,
                notes='\n'.join(notes_parts),
                due=due_str
            )

            print(f"   ✓ Created review task (due in 2 days)")
            
            if task:
                return {
                    'title': title,
                    'id': task.get('id'),
                    'type': 'review_task'
                }
            return None

        except Exception as e:
            print(f"   ⚠️  Error creating review task: {e}")
            return None

    def import_google_doc(self, doc_id: str, doc_name: str, doc_content: str) -> Optional[Path]:
        """
        Import a single Google Doc.
        
        Args:
            doc_id: Google Doc ID
            doc_name: Document name
            doc_content: Full text content
        
        Returns:
            Path to created file or None if skipped
        """
        # Check if already imported
        if self._is_imported(doc_id):
            print(f"⊘ Skipping '{doc_name}' (already imported)")
            return None
        
        # Check if matches pattern
        if not DOC_PATTERN.search(doc_name):
            return None
        
        print(f"\n📄 Processing: '{doc_name}'")

        # Parse document
        try:
            meeting_data = self.parse_google_doc(doc_content, doc_name)
        except Exception as e:
            print(f"   ✗ Error parsing document: {e}")
            return None

        # Enrich with Granola API attendees
        meeting_data = self.enrich_with_granola_attendees(meeting_data, doc_name)

        # Detect client
        client_slug, confidence, method = self.detect_client(meeting_data)

        if client_slug:
            client_display = client_slug.replace("-", " ").title()
            print(f"   ✓ Detected client: {client_display} ({confidence}% via {method})")
        else:
            print(f"   ⚠ No client detected - saving to _unassigned")
            # Add to unmatched list
            self.unmatched.append({
                "title": meeting_data['title'],
                "date": meeting_data['date'],
                "doc_id": doc_id,
                "doc_name": doc_name,
                "detected_at": datetime.now().isoformat()
            })
            self._save_unmatched()

        # Analyze meeting with AI
        ai_analysis = self.analyze_meeting_with_ai(meeting_data, client_slug)

        # Extract and create action items with comprehensive Claude analysis
        action_items = self.extract_action_items_comprehensive(meeting_data)
        created_action_tasks = []
        if action_items:
            print(f"   ✓ Found {len(action_items)} action item(s)")
            created_action_tasks = self.create_google_tasks(action_items, client_slug)

            # Send notifications for P0 urgent tasks
            if created_action_tasks:
                p0_tasks = [task for task in action_items if task.get('priority') == 'P0']
                if p0_tasks:
                    self.send_p0_notifications(p0_tasks, meeting_data, client_slug)

        # Create meeting file with AI summary and processing history (before review task so we have file_path)
        file_path = self.create_meeting_file(
            meeting_data, 
            client_slug, 
            ai_analysis,
            tasks_created=created_action_tasks,  # Will add review task after
            client_detection={'confidence': confidence, 'method': method}
        )
        print(f"   ✓ Saved to: {file_path}")

        # Create review task for CONTEXT.md updates (now we have file_path)
        review_task = self.create_review_task(meeting_data, client_slug, file_path, ai_analysis)
        
        # Update meeting file with review task if it was created
        if review_task:
            # Re-read the file, add review task to processing history, and save
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find the Tasks Created section and add review task
                if "**Tasks Created:**" in content:
                    # Add review task to the list
                    review_task_line = f"- ✅ {review_task['title']} (Google Task: `{review_task.get('id', 'N/A')}`, Type: {review_task.get('type', 'review_task')})"
                    # Insert before the closing "---"
                    content = content.replace("---", f"{review_task_line}\n---", 1)
                    
                    # Update task count
                    import re
                    content = re.sub(
                        r'\*\*Google Tasks Created:\*\*\s*\d+',
                        f"**Google Tasks Created:** {len(created_action_tasks) + 1}",
                        content
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                print(f"   ⚠️  Could not update meeting file with review task: {e}")
        
        # Mark as imported
        self._mark_imported(doc_id, file_path, client_slug)
        
        return file_path

    def find_google_docs(self, days: int = 7) -> List[Dict]:
        """
        Find Google Docs matching Granola pattern in Shared Drive.
        
        Uses Google Drive API directly (works standalone, not requiring MCP).
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of document dictionaries with 'id', 'name', 'modified_time', 'content'
        """
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
            import json
            
            # Load OAuth credentials
            creds_file = PROJECT_ROOT / "infrastructure" / "mcp-servers" / "google-drive-mcp-server" / "gcp-oauth.keys.json"
            token_file = Path.home() / ".config" / "google-drive-mcp" / "tokens.json"

            # Fallback to local token.json if MCP token not found
            if not token_file.exists():
                token_file = PROJECT_ROOT / "infrastructure" / "mcp-servers" / "google-drive-mcp-server" / "token.json"

            if not creds_file.exists():
                print(f"⚠️  OAuth credentials not found at {creds_file}")
                print("   Please complete Google Drive MCP setup first")
                return []

            if not token_file.exists():
                print(f"⚠️  Token file not found at {token_file}")
                print("   Please run: npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json")
                return []

            # Load OAuth keys (client_id, client_secret)
            with open(creds_file, 'r') as f:
                oauth_keys = json.load(f)
                # Handle both "installed" and "web" key types
                if "installed" in oauth_keys:
                    client_info = oauth_keys["installed"]
                elif "web" in oauth_keys:
                    client_info = oauth_keys["web"]
                else:
                    client_info = oauth_keys

            # Load token data (access_token, refresh_token, etc.)
            with open(token_file, 'r') as f:
                token_data = json.load(f)

            # Merge OAuth keys with token data
            merged_info = {
                "client_id": client_info.get("client_id"),
                "client_secret": client_info.get("client_secret"),
                "refresh_token": token_data.get("refresh_token"),
                "token_uri": client_info.get("token_uri", "https://oauth2.googleapis.com/token"),
            }

            # Add access_token if available
            if "access_token" in token_data:
                merged_info["token"] = token_data["access_token"]

            # Create credentials
            creds = Credentials.from_authorized_user_info(merged_info)
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save refreshed token
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
            
            # Build Drive API service
            service = build('drive', 'v3', credentials=creds)
            
            # Calculate date threshold
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_rfc3339 = cutoff_date.strftime('%Y-%m-%dT%H:%M:%S')
            
            # Search for documents matching pattern
            # Search in "Shared with me" or Shared Drive
            query = (
                "name contains 'ROK | Granola -' "
                "and mimeType = 'application/vnd.google-apps.document' "
                f"and modifiedTime >= '{cutoff_rfc3339}' "
                "and trashed = false"
            )
            
            print(f"   Searching Google Drive for: 'ROK | Granola -'")
            print(f"   Modified after: {cutoff_date.strftime('%Y-%m-%d')}")
            
            # Search for files
            results = service.files().list(
                q=query,
                fields="files(id, name, modifiedTime, mimeType)",
                orderBy="modifiedTime desc",
                pageSize=100
            ).execute()
            
            files = results.get('files', [])
            print(f"   Found {len(files)} matching document(s)")
            
            if not files:
                return []
            
            # Fetch content for each document
            docs = []
            docs_service = build('docs', 'v1', credentials=creds)
            
            for file_info in files:
                doc_id = file_info['id']
                doc_name = file_info['name']
                
                try:
                    # Get document content using Docs API
                    doc = docs_service.documents().get(documentId=doc_id).execute()
                    
                    # Extract text content
                    content_parts = []
                    if 'body' in doc and 'content' in doc['body']:
                        for element in doc['body']['content']:
                            if 'paragraph' in element:
                                para = element['paragraph']
                                if 'elements' in para:
                                    for elem in para['elements']:
                                        if 'textRun' in elem:
                                            text = elem['textRun'].get('content', '')
                                            content_parts.append(text)
                    
                    content = ''.join(content_parts)
                    
                    docs.append({
                        'id': doc_id,
                        'name': doc_name,
                        'modified_time': file_info.get('modifiedTime', ''),
                        'content': content
                    })
                    
                    print(f"   ✓ Fetched: {doc_name}")
                    
                except HttpError as e:
                    print(f"   ⚠️  Error fetching {doc_name}: {e}")
                    continue
                except Exception as e:
                    print(f"   ⚠️  Unexpected error fetching {doc_name}: {e}")
                    continue
            
            return docs
            
        except ImportError as e:
            print(f"⚠️  Google API libraries not installed: {e}")
            print("   Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return []
        except Exception as e:
            print(f"⚠️  Error searching Google Drive: {e}")
            import traceback
            traceback.print_exc()
            return []

    def import_recent(self, days: int = 7) -> int:
        """
        Import recent Granola Google Docs.
        
        Args:
            days: Number of days to look back
        
        Returns:
            Number of documents imported
        """
        print(f"\n🔍 Finding Granola Google Docs from last {days} days...")
        
        # Find documents
        docs = self.find_google_docs(days=days)
        
        if not docs:
            print("   No documents found")
            return 0
        
        print(f"   Found {len(docs)} document(s)")
        
        imported_count = 0
        for doc in docs:
            result = self.import_google_doc(
                doc_id=doc['id'],
                doc_name=doc['name'],
                doc_content=doc['content']
            )
            if result:
                imported_count += 1
        
        # Update last check time
        self.history["last_check"] = datetime.now().isoformat()
        self._save_history()
        
        return imported_count


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Import Granola meetings from Google Docs (Zapier)"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Import documents from last N days (default: 7)"
    )
    
    parser.add_argument(
        "--doc-id",
        help="Import a specific Google Doc by ID"
    )
    
    parser.add_argument(
        "--doc-name",
        help="Document name (required with --doc-id)"
    )
    
    parser.add_argument(
        "--doc-content",
        help="Document content (required with --doc-id)"
    )
    
    args = parser.parse_args()
    
    try:
        importer = GranolaGoogleDocsImporter()
        
        if args.doc_id:
            # Import specific document
            if not args.doc_content:
                print("✗ Error: --doc-content required with --doc-id")
                sys.exit(1)
            
            result = importer.import_google_doc(
                doc_id=args.doc_id,
                doc_name=args.doc_name or f"Document {args.doc_id}",
                doc_content=args.doc_content
            )
            
            if result:
                print(f"\n✓ Imported: {result}")
            else:
                print("\n✗ Import failed or document already imported")
        else:
            # Import recent documents
            count = importer.import_recent(days=args.days)
            print(f"\n✓ Imported {count} document(s)")
            
            # Report unmatched meetings
            if importer.unmatched:
                print(f"\n⚠️  {len(importer.unmatched)} unmatched meeting(s) found")
                print("   These will be included in daily/weekly summary reports")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

