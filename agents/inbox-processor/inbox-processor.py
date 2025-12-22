#!/usr/bin/env python3
"""
PetesBrain Inbox Processor

Processes files in !inbox/ folder and routes them to appropriate locations:
- Client-related notes → clients/[client]/documents/
- Tasks → todo/
- Knowledge → roksys/knowledge-base/
- General notes → processed/ archive

Runs daily at 8:00 AM via LaunchAgent
"""

import os
import sys
import re
import json
import uuid
import time
import errno
from datetime import datetime, timedelta
from pathlib import Path
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import ClientTasksService
from shared.client_tasks_service import ClientTasksService

# Google Tasks - disabled in standalone mode (use AI inbox processor for Google Tasks)
GOOGLE_TASKS_ENABLED = False

INBOX_DIR = PROJECT_ROOT / '!inbox'
PROCESSED_DIR = INBOX_DIR / 'processed'
AI_ENHANCED_DIR = INBOX_DIR / 'ai-enhanced'
TODO_DIR = PROJECT_ROOT / 'todo'
KNOWLEDGE_BASE = PROJECT_ROOT / 'roksys' / 'knowledge-base'
CLIENTS_DIR = PROJECT_ROOT / 'clients'

# Known clients (could be loaded from clients/ directory)
CLIENTS = [
    'accessories-for-the-home',
    'bright-minds',
    'clear-prospects',
    'crowd-control',
    'devonshire-hotels',
    'go-glean',
    'godshot',
    'grain-guard',
    'just-bin-bags',
    'national-design-academy',
    'otc',
    'personal',
    'positive-bakes',
    'print-my-pdf',
    'smythson',
    'superspace',
    'tree2mydoor',
    'uno-lighting'
]

def get_timestamp():
    """Get current timestamp for filenames"""
    return datetime.now().strftime('%Y%m%d-%H%M%S')

def get_date_str():
    """Get current date for filenames"""
    return datetime.now().strftime('%Y%m%d')

def generate_descriptive_filename(note_type: str, client: str = None, content: str = "", timestamp: str = None):
    """
    Generate descriptive filename (pattern).
    Format: [type]-YYYYMMDD-[client]-[slug].md

    Examples:
      task-20251119-smythson-budget-review.md
      note-20251119-devonshire-trending-searches.md
      completion-20251119-uno-lighting-campaign-launch.md
    """
    if not timestamp:
        timestamp = get_date_str()

    # Extract first 3-5 meaningful words for slug from content
    words = re.findall(r'\b\w{3,}\b', content.lower())  # Words 3+ chars
    # Filter out common words
    stop_words = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'have', 'has', 'are', 'was', 'were', 'been'}
    slug_words = [w for w in words[:10] if w not in stop_words][:4]  # Max 4 words
    slug = '-'.join(slug_words)
    slug = re.sub(r'[^a-z0-9-]', '', slug)[:50]  # Clean and limit length

    # Build filename
    if client and slug:
        return f"{note_type}-{timestamp}-{client}-{slug}.md"
    elif client:
        return f"{note_type}-{timestamp}-{client}.md"
    elif slug:
        return f"{note_type}-{timestamp}-{slug}.md"
    else:
        return f"{note_type}-{timestamp}.md"

def extract_processing_metadata(content, file_path):
    """
    Extract processing metadata from AI-enhanced file or regular file.
    
    Returns dict with processing history information.
    """
    metadata = {
        'is_ai_enhanced': False,
        'original_file': None,
        'enhanced_file': None,
        'model_used': None,
        'processed_at': None,
        'client_detected': None,
        'duplicate_check': None,
        'related_tasks': [],
        'dependencies': [],
        'priority': None,
        'urgency': None,
        'estimated_time': None,
    }
    
    # Check if this is an AI-enhanced file
    if 'ai-enhanced' in str(file_path) or content.startswith('# AI-Enhanced Note'):
        metadata['is_ai_enhanced'] = True
        metadata['enhanced_file'] = file_path.name
        
        # Extract original file name
        orig_match = re.search(r'\*\*Original:\*\*\s*(.+)', content)
        if orig_match:
            metadata['original_file'] = orig_match.group(1).strip()
        
        # Extract model used
        model_match = re.search(r'\*\*Model Used:\*\*\s*(.+)', content)
        if model_match:
            metadata['model_used'] = model_match.group(1).strip()
        
        # Extract processed timestamp
        processed_match = re.search(r'\*\*Processed:\*\*\s*(.+)', content)
        if processed_match:
            metadata['processed_at'] = processed_match.group(1).strip()
        
        # Extract client
        client_match = re.search(r'\*\*Client:\*\*\s*(.+)', content)
        if client_match:
            client_val = client_match.group(1).strip()
            if client_val and client_val != 'N/A':
                metadata['client_detected'] = client_val
        
        # Extract duplicate info
        if 'DUPLICATE DETECTED' in content:
            dup_match = re.search(r'DUPLICATE DETECTED.*?Similar to:\*\*\s*(.+?)(?:\n|$)', content, re.DOTALL)
            if dup_match:
                metadata['duplicate_check'] = {
                    'found': True,
                    'similar_to': dup_match.group(1).strip()
                }
        else:
            metadata['duplicate_check'] = {'found': False}
        
        # Extract related tasks
        if '**Related Tasks:**' in content:
            related_section = re.search(r'\*\*Related Tasks:\*\*\s*\n(.*?)(?=\n\n|\n\*\*|\Z)', content, re.DOTALL)
            if related_section:
                related_lines = related_section.group(1).strip().split('\n')
                metadata['related_tasks'] = [line.strip('- ').strip() for line in related_lines if line.strip()]
        
        # Extract dependencies
        if '**Dependencies/Blockers:**' in content:
            deps_section = re.search(r'\*\*Dependencies/Blockers:\*\*\s*\n(.*?)(?=\n\n|\n\*\*|\Z)', content, re.DOTALL)
            if deps_section:
                deps_lines = deps_section.group(1).strip().split('\n')
                metadata['dependencies'] = [line.strip('- ').strip() for line in deps_lines if line.strip()]
        
        # Extract priority, urgency, estimated time
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+)', content)
        if priority_match:
            priority_val = priority_match.group(1).strip()
            if priority_val != 'N/A':
                metadata['priority'] = priority_val
        
        urgency_match = re.search(r'\*\*Urgency:\*\*\s*(.+)', content)
        if urgency_match:
            urgency_val = urgency_match.group(1).strip()
            if urgency_val != 'N/A':
                metadata['urgency'] = urgency_val
        
        time_match = re.search(r'\*\*Estimated Time:\*\*\s*(.+)', content)
        if time_match:
            time_val = time_match.group(1).strip()
            if time_val != 'N/A':
                metadata['estimated_time'] = time_val
    else:
        # Regular file - try to find original note info
        metadata['original_file'] = file_path.name
        metadata['duplicate_check'] = {'found': False}  # No duplicate check for regular files

        # Check if there's a Wispr Flow note ID
        note_id_match = re.search(r'\*Note ID:\s*(.+?)\*', content)
        if note_id_match:
            metadata['note_id'] = note_id_match.group(1).strip()

    return metadata

def build_source_chain(metadata, file_path):
    """Build source chain markdown section"""
    chain_parts = []
    
    if metadata.get('original_file'):
        # Try to find original file in processed directory
        original_name = metadata['original_file']
        if not original_name.startswith('!'):
            # Look for archived original
            processed_files = list(PROCESSED_DIR.glob(f'*{original_name}'))
            if processed_files:
                original_path = processed_files[0]
                chain_parts.append(f"**Original Note:** `{original_path.relative_to(PROJECT_ROOT)}`")
            else:
                chain_parts.append(f"**Original Note:** `!inbox/{original_name}`")
        else:
            chain_parts.append(f"**Original Note:** `{original_name}`")
    
    if metadata.get('is_ai_enhanced') and metadata.get('enhanced_file'):
        chain_parts.append(f"**AI Enhanced:** `!inbox/ai-enhanced/{metadata['enhanced_file']}`")
        if metadata.get('processed_at'):
            chain_parts[-1] += f" (processed: {metadata['processed_at']})"
    
    return '\n'.join(chain_parts) if chain_parts else None

def build_processing_history(metadata):
    """Build processing history markdown section"""
    history_parts = []
    
    if metadata.get('is_ai_enhanced'):
        history_parts.append("**AI Enhancement:** ✅ Yes")
        if metadata.get('model_used'):
            history_parts[-1] += f" ({metadata['model_used']})"
        if metadata.get('processed_at'):
            history_parts.append(f"**Processed:** {metadata['processed_at']}")
    else:
        history_parts.append("**AI Enhancement:** ❌ No")
    
    history_parts.append("\n**Skills Run:**")
    
    # Client detection
    if metadata.get('client_detected'):
        history_parts.append(f"- ✅ Client detection → `{metadata['client_detected']}`")
    else:
        history_parts.append("- ⚠️ Client detection → Not detected")
    
    # Duplicate check
    dup_info = metadata.get('duplicate_check', {})
    if dup_info.get('found'):
        history_parts.append(f"- ✅ Duplicate check → Found similar: {dup_info.get('similar_to', 'Unknown')}")
    else:
        history_parts.append("- ✅ Duplicate check → No duplicates found")
    
    # Related tasks
    related = metadata.get('related_tasks', [])
    if related:
        history_parts.append(f"- ✅ Related task finding → Found {len(related)} related task(s)")
        for task in related[:3]:  # Limit to 3
            history_parts.append(f"  - {task}")
    else:
        history_parts.append("- ✅ Related task finding → No related tasks found")
    
    # Dependencies
    deps = metadata.get('dependencies', [])
    if deps:
        history_parts.append(f"- ✅ Dependency detection → Found {len(deps)} dependency/blocker(s)")
        for dep in deps[:3]:  # Limit to 3
            history_parts.append(f"  - {dep}")
    else:
        history_parts.append("- ✅ Dependency detection → No dependencies found")
    
    # AI analysis metadata
    if metadata.get('priority') or metadata.get('urgency') or metadata.get('estimated_time'):
        history_parts.append("\n**AI Analysis:**")
        if metadata.get('priority'):
            history_parts.append(f"- Priority: {metadata['priority']}")
        if metadata.get('urgency'):
            history_parts.append(f"- Urgency: {metadata['urgency']}")
        if metadata.get('estimated_time'):
            history_parts.append(f"- Estimated time: {metadata['estimated_time']}")
    
    return '\n'.join(history_parts)

def detect_action_keyword(content):
    """
    Detect action keywords in content
    
    Returns: (action_type, target, cleaned_content)
    """
    lines = content.split('\n')
    if not lines:
        return None, None, content

    first_line = lines[0].strip().lower()

    # Check for action keywords - search ENTIRE content, not just first line
    # Priority order: task > client > knowledge > email

    # Check for task: directive anywhere in content (highest priority)
    task_match = re.search(r'^task:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
    if task_match:
        task_title = task_match.group(1).strip()
        return 'task', task_title, content

    # Check for knowledge: directive
    knowledge_match = re.search(r'^knowledge:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
    if knowledge_match:
        topic = knowledge_match.group(1).strip()
        return 'knowledge', topic, content

    # Check for email directive
    email_match = re.search(r'^email\s+(.+?):.*$', content, re.MULTILINE | re.IGNORECASE)
    if email_match:
        client_name = email_match.group(1).strip().lower()
        client_name = client_name.replace(' ', '-').replace('_', '-')
        return 'email', client_name, content

    # Check for client: directive (lower priority than task)
    client_match = re.search(r'^client:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
    if client_match:
        client_name = client_match.group(1).strip().lower()
        client_name = client_name.replace(' ', '-').replace('_', '-')
        return 'client', client_name, content

    return None, None, content

def is_rok_systems_note(content):
    """Check if note is about Rok Systems (internal company context)"""
    import re
    content_lower = content.lower()
    
    # Rok Systems variations (correct spelling: "Rok", but also handle "Rock" typo)
    rok_patterns = [
        r'\brok\s+systems\b',  # "Rok Systems" or "rok systems" (correct)
        r'\brock\s+systems\b',  # "Rock Systems" (common typo - treat as Rok Systems)
        r'\broksys\b',  # "Roksys" or "roksys"
    ]
    
    # Check for Rok Systems mentions
    for pattern in rok_patterns:
        if re.search(pattern, content_lower):
            return True
    
    return False

def process_rok_systems_note(content, original_file):
    """Save Rok Systems note to roksys/documents/"""
    roksys_dir = PROJECT_ROOT / 'roksys' / 'documents'
    roksys_dir.mkdir(parents=True, exist_ok=True)

    # Generate descriptive filename
    filename = generate_descriptive_filename('note', 'roksys', content)
    target_path = roksys_dir / filename

    # If file exists, append number
    counter = 1
    while target_path.exists():
        base_name = filename.rsplit('.', 1)[0]
        filename = f"{base_name}-{counter}.md"
        target_path = roksys_dir / filename
        counter += 1
    
    # Write content with metadata
    full_content = f"""# Inbox Capture - {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Source:** {original_file.name}  
**Context:** Rok Systems (Internal)

---

{content}
"""
    
    with open(target_path, 'w') as f:
        f.write(full_content)
    
    print(f"  ✓ Saved to: roksys/documents/{filename}")
    return True

def find_client_in_content(content):
    """Try to detect client name in content with intelligent matching"""
    import re
    
    content_lower = content.lower()
    
    # Exclude Rok Systems (internal company context) from client detection
    # This prevents "Rok Systems" notes from being routed to client folders
    # Also handles "Rock Systems" typo
    rok_patterns = [r'\brok\s+systems\b', r'\brock\s+systems\b', r'\broksys\b']
    for pattern in rok_patterns:
        if re.search(pattern, content_lower):
            return None  # Don't treat Rok Systems as a client
    
    # Common client name mappings for better matching
    client_aliases = {
        'devonshire-hotels': ['devonshire', 'devonshire hotels', 'devonshirehotels'],
        'just-bin-bags': ['just bin bags', 'justbinbags', 'jbb'],
        'tree2mydoor': ['tree2mydoor', 'tree 2 my door', 'tree to my door', 't2md'],
        'national-design-academy': ['national design academy', 'nda', 'design academy'],
        'accessories-for-the-home': ['accessories for the home', 'accessoriesforthehome', 'afth'],
        'bright-minds': ['bright minds', 'brightminds'],
        'clear-prospects': ['clear prospects', 'clearprospects'],
        'crowd-control': ['crowd control', 'crowdcontrol'],
        'uno-lighting': ['uno lighting', 'uno lights', 'unolighting'],
        'print-my-pdf': ['print my pdf', 'printmypdf'],
    }
    
    for client in CLIENTS:
        # Build all possible variations to check
        variations = [
            client,  # Full name: "just-bin-bags"
            client.replace('-', ' '),  # With spaces: "just bin bags"
            client.replace('-', ''),  # No separators: "justbinbags"
        ]
        
        # Add base name (first part before hyphen) for partial matching
        # e.g., "devonshire" from "devonshire-hotels"
        base_name = client.split('-')[0]
        if len(base_name) > 3:  # Only for meaningful base names (avoid "otc", "nda")
            variations.append(base_name)
        
        # Add known aliases if they exist
        if client in client_aliases:
            variations.extend(client_aliases[client])
        
        # Check each variation
        for variation in variations:
            if not variation:
                continue
            
            # Use word boundary matching for better accuracy
            # This prevents "devonshire" matching "devonshirehotels" incorrectly
            pattern = r'\b' + re.escape(variation.lower()) + r'\b'
            if re.search(pattern, content_lower):
                return client
            
            # Also check simple substring match (fallback for edge cases)
            if len(variation) > 4 and variation.lower() in content_lower:
                return client
    
    return None

def process_client_note(client_name, content, original_file):
    """Save note to client documents folder with full traceability"""
    # Find matching client
    matched_client = None
    for client in CLIENTS:
        if client_name in client or client in client_name:
            matched_client = client
            break
    
    if not matched_client:
        print(f"  ⚠️  Unknown client: {client_name}")
        return False
    
    client_dir = CLIENTS_DIR / matched_client / 'documents'
    client_dir.mkdir(parents=True, exist_ok=True)

    # Generate descriptive filename with client and content
    filename = generate_descriptive_filename('note', matched_client, content)
    target_path = client_dir / filename

    # If file exists, append number
    counter = 1
    while target_path.exists():
        base_name = filename.rsplit('.', 1)[0]
        filename = f"{base_name}-{counter}.md"
        target_path = client_dir / filename
        counter += 1
    
    # Extract processing metadata
    processing_metadata = extract_processing_metadata(content, original_file)
    
    # Build source chain
    source_chain = build_source_chain(processing_metadata, original_file)
    
    # Build processing history
    processing_history = build_processing_history(processing_metadata)
    
    # Check if any tasks were created from this note
    tasks_created = []
    # This will be populated if we can detect task creation from the content
    # For now, we'll add a placeholder that can be updated later
    
    # Write content with metadata and traceability
    full_content = f"""# Inbox Capture - {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Source:** {original_file.name}  
**Client:** {matched_client}

## Source Chain

{source_chain if source_chain else f"**Source:** `{original_file.relative_to(PROJECT_ROOT) if original_file.is_relative_to(PROJECT_ROOT) else original_file.name}`"}

**This Note:** `clients/{matched_client}/documents/{filename}`

## Processing History

{processing_history}

{f"**Tasks Created:**\n" + "\n".join([f"- ✅ {task}" for task in tasks_created]) if tasks_created else "**Tasks Created:** None"}

---

{content}
"""
    
    with open(target_path, 'w') as f:
        f.write(full_content)
    
    print(f"  ✓ Saved to: clients/{matched_client}/documents/{filename}")
    return True

def parse_fuzzy_date(date_text: str):
    """
    Parse natural language date expressions into YYYY-MM-DD format.

    Handles expressions like:
    - "tomorrow", "today"
    - "next week", "within next week", "in a week"
    - "in X days/weeks/months"
    - "next Monday/Tuesday/etc"
    - "in 2 weeks", "in 3 days"

    Returns:
        YYYY-MM-DD formatted date string, or None if cannot parse
    """
    if not date_text or not isinstance(date_text, str):
        return None

    date_text_lower = date_text.lower().strip()
    today = datetime.now()

    # Simple cases
    if date_text_lower in ['tomorrow', 'tmrw', 'tommorow']:
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')

    if date_text_lower in ['today', 'now']:
        return today.strftime('%Y-%m-%d')

    if date_text_lower in ['yesterday']:
        return (today - timedelta(days=1)).strftime('%Y-%m-%d')

    # Week-based expressions
    week_patterns = [
        r'(?:within|in)\s+(?:a|the|next|1)\s+week',
        r'next\s+week',
        r'in\s+a\s+week',
    ]
    for pattern in week_patterns:
        if re.search(pattern, date_text_lower):
            return (today + timedelta(days=7)).strftime('%Y-%m-%d')

    # "in X days/weeks/months" pattern
    time_delta_match = re.search(r'in\s+(\d+)\s+(day|week|month)s?', date_text_lower)
    if time_delta_match:
        amount = int(time_delta_match.group(1))
        unit = time_delta_match.group(2)

        if unit == 'day':
            return (today + timedelta(days=amount)).strftime('%Y-%m-%d')
        elif unit == 'week':
            return (today + timedelta(weeks=amount)).strftime('%Y-%m-%d')
        elif unit == 'month':
            # Approximate: 30 days per month
            return (today + timedelta(days=amount * 30)).strftime('%Y-%m-%d')

    # "next [day of week]" pattern
    days_of_week = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1, 'tues': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3, 'thurs': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6,
    }

    for day_name, day_num in days_of_week.items():
        if re.search(rf'\bnext\s+{day_name}\b', date_text_lower):
            # Calculate days until next occurrence of this day
            current_day = today.weekday()
            days_ahead = day_num - current_day
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

    # If we can't parse it, return None (will be handled upstream)
    return None

def extract_due_date(content):
    """
    Extract due date from content and parse fuzzy dates into YYYY-MM-DD format.

    Extracts date text from patterns like:
    - due: tomorrow
    - due: within next week
    - due: in 3 days

    Then parses natural language expressions into proper date format.
    """
    due_patterns = [
        r'due:?\s*(.+?)(?:\n|$)',
        r'deadline:?\s*(.+?)(?:\n|$)',
        r'by:?\s*(.+?)(?:\n|$)',
    ]

    for pattern in due_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            date_text = match.group(1).strip()

            # If it's already in YYYY-MM-DD format, return as-is
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_text):
                return date_text

            # Otherwise, try to parse it as a fuzzy date
            parsed_date = parse_fuzzy_date(date_text)
            if parsed_date:
                print(f"  📅 Parsed fuzzy date: '{date_text}' → {parsed_date}")
                return parsed_date

            # If we can't parse it, return the original text (for manual review)
            print(f"  ⚠️  Could not parse date expression: '{date_text}'")
            return date_text

    return None


def normalize_for_comparison(text):
    """Normalize text for duplicate comparison"""
    import difflib
    # Lowercase and strip
    text = text.lower().strip()
    # Remove common prefixes like [Client], [Personal], [Roksys]
    text = re.sub(r'^\[[^\]]+\]\s*', '', text)
    # Remove timestamps and dates
    text = re.sub(r'\d{8}[-_]?\d{6}', '', text)  # 20251123-090757
    text = re.sub(r'\d{4}-\d{2}-\d{2}', '', text)  # 2025-11-23
    # Remove "wispr quick note" prefix
    text = re.sub(r'wispr\s*(quick\s*)?note\s*', '', text)
    # Remove trailing numbers (like "-1", "-2", etc.)
    text = re.sub(r'[-_]\d+$', '', text)
    # Collapse whitespace
    text = ' '.join(text.split())
    return text.strip()


def find_similar_task(task_title, tasks_json_path, threshold=0.8):
    """
    Check if a similar task already exists in tasks.json

    Returns: (is_duplicate, similar_task_title) or (False, None)
    """
    import difflib

    if not tasks_json_path.exists():
        return False, None

    try:
        with open(tasks_json_path, 'r') as f:
            tasks_data = json.load(f)
    except:
        return False, None

    normalized_new = normalize_for_comparison(task_title)

    for existing_task in tasks_data.get('tasks', []):
        if existing_task.get('status') != 'active':
            continue

        existing_title = existing_task.get('title', '')
        normalized_existing = normalize_for_comparison(existing_title)

        # Exact match after normalization
        if normalized_new == normalized_existing:
            return True, existing_title

        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, normalized_new, normalized_existing).ratio()
        if ratio >= threshold:
            return True, existing_title

        # Also check if one contains the other (for short titles)
        if len(normalized_new) > 10 and len(normalized_existing) > 10:
            if normalized_new in normalized_existing or normalized_existing in normalized_new:
                return True, existing_title

    return False, None


def get_all_existing_tasks():
    """
    Load all existing tasks from all tasks.json files for deduplication.
    Returns a list of normalized task titles.
    """
    all_tasks = []

    # Check all client tasks.json files
    for client_dir in CLIENTS_DIR.iterdir():
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            # Check root location ONLY (product-feeds is legacy and no longer used)
            task_path = client_dir / 'tasks.json'
            if task_path.exists():
                try:
                    with open(task_path, 'r') as f:
                        data = json.load(f)
                    for task in data.get('tasks', []):
                        if task.get('status') == 'active':
                            all_tasks.append(task.get('title', ''))
                except:
                    pass

    # Also check roksys tasks
    roksys_tasks = PROJECT_ROOT / 'roksys' / 'tasks.json'
    if roksys_tasks.exists():
        try:
            with open(roksys_tasks, 'r') as f:
                data = json.load(f)
            for task in data.get('tasks', []):
                if task.get('status') == 'active':
                    all_tasks.append(task.get('title', ''))
        except:
            pass

    return all_tasks


def is_duplicate_task_globally(task_title, threshold=0.8):
    """
    Check if a similar task exists anywhere in the system.

    Returns: (is_duplicate, similar_task_title) or (False, None)
    """
    import difflib

    all_tasks = get_all_existing_tasks()
    normalized_new = normalize_for_comparison(task_title)

    for existing_title in all_tasks:
        normalized_existing = normalize_for_comparison(existing_title)

        # Exact match after normalization
        if normalized_new == normalized_existing:
            return True, existing_title

        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, normalized_new, normalized_existing).ratio()
        if ratio >= threshold:
            return True, existing_title

        # Also check if one contains the other (for short titles)
        if len(normalized_new) > 10 and len(normalized_existing) > 10:
            if normalized_new in normalized_existing or normalized_existing in normalized_new:
                return True, existing_title

    return False, None

def process_task(task_title, content, original_file):
    """Create task in tasks.json for task manager AND local todo file"""
    TODO_DIR.mkdir(parents=True, exist_ok=True)

    # Check for duplicates FIRST before doing any processing
    is_dup, similar_task = is_duplicate_task_globally(task_title)
    if is_dup:
        print(f"  ⏭️  DUPLICATE DETECTED - skipping task creation")
        print(f"      Similar to: {similar_task[:70]}...")
        print(f"      (File will still be archived)")
        return True  # Return True so file gets archived

    # Extract processing metadata from enhanced file
    processing_metadata = extract_processing_metadata(content, original_file)

    # Extract client from content or metadata
    client_name = None

    # Check for client: directive in content
    client_match = re.search(r'^client:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
    if client_match:
        client_name = client_match.group(1).strip().lower().replace(' ', '-')

    # Or from processing metadata
    if not client_name and processing_metadata.get('client_detected'):
        client_name = processing_metadata['client_detected'].lower().replace(' ', '-')

    # Or try to detect from content
    if not client_name:
        client_name = find_client_in_content(content)

    # Extract due date if present
    due_date = extract_due_date(content)

    # For quick notes without explicit due date, default to today (makes it a reminder)
    # This ensures phone captures like "Red Crouch" become reminders, not tasks
    if not due_date:
        due_date = datetime.now().strftime('%Y-%m-%d')

    # Extract priority from content
    # Default to P2 for quick notes (changed from P0)
    # Quick phone captures shouldn't default to urgent
    priority = 'P2'  # Default for quick notes
    priority_match = re.search(r'priority:\s*(high|medium|low|P[0-3])', content, re.IGNORECASE)
    if priority_match:
        p = priority_match.group(1).lower()
        if p == 'high' or p == 'p0':
            priority = 'P0'
        elif p == 'medium' or p == 'p1':
            priority = 'P1'
        elif p == 'low' or p == 'p2':
            priority = 'P2'
        elif p == 'p3':
            priority = 'P3'

    # Extract urgency (can upgrade to P0 if not already)
    is_urgent = bool(re.search(r'urgent:\s*true', content, re.IGNORECASE))
    if is_urgent:
        priority = 'P0'

    # Extract time estimate
    time_estimate = None
    time_match = re.search(r'time:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if time_match:
        time_str = time_match.group(1).strip()
        # Convert to minutes
        if 'hour' in time_str.lower():
            hours = re.search(r'(\d+)', time_str)
            if hours:
                time_estimate = int(hours.group(1)) * 60
        elif 'min' in time_str.lower():
            mins = re.search(r'(\d+)', time_str)
            if mins:
                time_estimate = int(mins.group(1))

    # Clean content for notes (remove metadata lines)
    notes_content = re.sub(r'^(client|task|due|time|urgent|priority):\s*.+\n?', '', content, flags=re.MULTILINE | re.IGNORECASE)
    notes_content = notes_content.strip()

    # Create task using ClientTasksService
    task_created_in_json = False

    # Default to 'personal' for quick notes without client context
    # (Changed from 'roksys' December 18, 2025 to separate personal from business)
    if not client_name:
        client_name = 'personal'

    # Use ClientTasksService to create task
    try:
        task_service = ClientTasksService()

        task_id = task_service.create_task(
            title=task_title,
            client=client_name,
            priority=priority,
            due_date=due_date,
            time_estimate_mins=time_estimate,
            notes=f"Source: Inbox processor (iOS Capture)\nOriginal file: {original_file.name}\n\n{notes_content}",
            source="iOS Inbox Capture → Processor",
            tags=[client_name, "inbox-capture"],
            task_type="standalone"
        )

        task_created_in_json = True
        print(f"  ✅ Created reminder in: {client_name}/tasks.json (due: {due_date})")
    except Exception as e:
        print(f"  ⚠️ Could not create task via ClientTasksService: {e}")

    # Also create local todo file for reference
    safe_title = re.sub(r'[^a-z0-9-]', '-', task_title.lower())
    safe_title = re.sub(r'-+', '-', safe_title).strip('-')[:50]

    filename = f"{get_date_str()}-{safe_title}.md"
    target_path = TODO_DIR / filename

    if target_path.exists():
        filename = f"{get_timestamp()}-{safe_title}.md"
        target_path = TODO_DIR / filename

    # Build source chain
    source_chain = build_source_chain(processing_metadata, original_file)

    # Build processing history
    processing_history = build_processing_history(processing_metadata)

    # Write local todo with traceability
    full_content = f"""# {task_title}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Task Manager:** {'✅ Added to tasks.json' if task_created_in_json else '❌ Not added'}
**Client:** {client_name or 'None detected'}
**Priority:** {priority}
**Due Date:** {due_date or 'Not set'}

## Source Chain

{source_chain if source_chain else f"**Source:** `{original_file.relative_to(PROJECT_ROOT) if original_file.is_relative_to(PROJECT_ROOT) else original_file.name}`"}

**This Task:** `todo/{filename}`

## Processing History

{processing_history}

**Actions Taken:**
- ✅ Local todo file created: `todo/{filename}`
{f"- ✅ Task added to task manager: `{client_name}/tasks.json`" if task_created_in_json else "- ⚠️ Task NOT added to task manager"}

## Details

{notes_content}

## Status

- [ ] Todo

## Notes

"""

    with open(target_path, 'w') as f:
        f.write(full_content)

    print(f"  ✓ Created todo: todo/{filename}")
    return True

def process_knowledge(topic, content, original_file):
    """Add to knowledge base"""
    # Create knowledge base entry
    kb_general = KNOWLEDGE_BASE / 'inbox-captures'
    kb_general.mkdir(parents=True, exist_ok=True)
    
    # Create filename from topic
    safe_topic = re.sub(r'[^a-z0-9-]', '-', topic.lower())
    safe_topic = re.sub(r'-+', '-', safe_topic).strip('-')[:50]
    
    filename = f"{get_date_str()}-{safe_topic}.md"
    target_path = kb_general / filename
    
    # If file exists, append to it
    if target_path.exists():
        with open(target_path, 'a') as f:
            f.write(f"\n\n---\n\n## Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{content}\n")
        print(f"  ✓ Appended to: roksys/knowledge-base/inbox-captures/{filename}")
    else:
        full_content = f"""# {topic}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Source:** {original_file.name}

---

{content}
"""
        with open(target_path, 'w') as f:
            f.write(full_content)
        print(f"  ✓ Created knowledge: roksys/knowledge-base/inbox-captures/{filename}")
    
    return True

def process_email_draft(client_name, content, original_file):
    """Save email draft to client emails folder"""
    # Find matching client
    matched_client = None
    for client in CLIENTS:
        if client_name in client or client in client_name:
            matched_client = client
            break
    
    if not matched_client:
        print(f"  ⚠️  Unknown client: {client_name}")
        return False
    
    client_dir = CLIENTS_DIR / matched_client / 'emails'
    client_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"draft-{get_date_str()}.md"
    target_path = client_dir / filename
    
    # If file exists, append number
    counter = 1
    while target_path.exists():
        filename = f"draft-{get_date_str()}-{counter}.md"
        target_path = client_dir / filename
        counter += 1
    
    # Write email draft
    full_content = f"""# Email Draft - {matched_client}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Source:** {original_file.name}  
**Status:** Draft

---

{content}
"""
    
    with open(target_path, 'w') as f:
        f.write(full_content)
    
    print(f"  ✓ Email draft: clients/{matched_client}/emails/{filename}")
    return True

def archive_processed(inbox_file, max_retries=5, base_delay=0.5):
    """Move processed file to archive with retry logic for iCloud locks
    
    Enhanced version with:
    - More retries (5 instead of 3)
    - Shorter initial delay (0.5s instead of 1s)
    - Better error reporting
    - Handles both EDEADLK and general OSErrors
    """
    PROCESSED_DIR.mkdir(exist_ok=True)

    timestamp = get_timestamp()
    archived_name = f"{timestamp}-{inbox_file.name}"
    target_path = PROCESSED_DIR / archived_name

    # Small initial delay to let iCloud sync settle
    time.sleep(0.1)

    for attempt in range(max_retries):
        try:
            shutil.move(str(inbox_file), str(target_path))
            print(f"  📦 Archived: !inbox/processed/{archived_name}")
            return True
        except OSError as e:
            # Retry on deadlock (errno 11) or "Resource temporarily unavailable" (errno 35)
            if (e.errno in [errno.EDEADLK, 35]) and attempt < max_retries - 1:
                # Resource deadlock or temporary lock - wait and retry
                delay = base_delay * (1.5 ** attempt)  # 0.5s, 0.75s, 1.1s, 1.7s, 2.5s
                print(f"  ⏳ File locked (iCloud sync), retrying in {delay:.1f}s... ({attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            else:
                # Either not a lock error, or out of retries
                print(f"  ⚠️  Failed to archive after {attempt + 1} attempts")
                print(f"      Error: [{e.errno}] {e}")
                print(f"      File: {inbox_file.name}")
                # Don't fail completely - log and continue
                return False

    return False

def process_inbox():
    """Process all files in inbox"""
    
    print("=" * 60)
    print("  PetesBrain Inbox Processor")
    print("=" * 60)
    print()
    
    if not INBOX_DIR.exists():
        print("❌ Inbox directory not found")
        return
    
    # Get all markdown and text files (except README)
    # First check ai-enhanced folder (priority), then regular inbox
    ai_md_files = []
    ai_txt_files = []
    if AI_ENHANCED_DIR.exists():
        ai_md_files = [f for f in AI_ENHANCED_DIR.glob('*.md') if f.name != 'README.md']
        ai_txt_files = [f for f in AI_ENHANCED_DIR.glob('*.txt')]

    md_files = [f for f in INBOX_DIR.glob('*.md') if f.name != 'README.md']
    txt_files = [f for f in INBOX_DIR.glob('*.txt')]

    # Process AI-enhanced files first, then regular inbox
    inbox_files = ai_md_files + ai_txt_files + md_files + txt_files
    
    if not inbox_files:
        print("📭 Inbox is empty - nothing to process")
        return
    
    print(f"📬 Found {len(inbox_files)} file(s) to process")
    print()
    
    processed_count = 0
    
    for inbox_file in inbox_files:
        print(f"📄 Processing: {inbox_file.name}")
        
        try:
            with open(inbox_file, 'r') as f:
                content = f.read().strip()
            
            # Small delay after reading to let iCloud sync settle (fixes deadlock)
            time.sleep(0.05)
            
            if not content:
                print(f"  ⚠️  Empty file, archiving")
                archive_processed(inbox_file)
                continue
            
            # Detect action keyword
            action_type, target, cleaned_content = detect_action_keyword(content)
            
            if action_type == 'client':
                if process_client_note(target, cleaned_content, inbox_file):
                    archive_processed(inbox_file)
                    processed_count += 1
            
            elif action_type == 'task':
                if process_task(target, cleaned_content, inbox_file):
                    archive_processed(inbox_file)
                    processed_count += 1
            
            elif action_type == 'knowledge':
                if process_knowledge(target, cleaned_content, inbox_file):
                    archive_processed(inbox_file)
                    processed_count += 1
            
            elif action_type == 'email':
                if process_email_draft(target, cleaned_content, inbox_file):
                    archive_processed(inbox_file)
                    processed_count += 1
            
            else:
                # No action keyword - check if Rok Systems note first
                if is_rok_systems_note(content):
                    print(f"  🏢 Detected Rok Systems context")
                    if process_rok_systems_note(content, inbox_file):
                        archive_processed(inbox_file)
                        processed_count += 1
                else:
                    # Try to detect client in content
                    detected_client = find_client_in_content(content)
                    
                    if detected_client:
                        print(f"  🔍 Detected client: {detected_client}")
                        if process_client_note(detected_client, content, inbox_file):
                            archive_processed(inbox_file)
                            processed_count += 1
                    else:
                        # Default: treat as personal reminder
                        print(f"  📝 No clear action - creating personal reminder")
                        title = inbox_file.stem.replace('-', ' ').title()
                        if process_task(title, content, inbox_file):
                            archive_processed(inbox_file)
                            processed_count += 1
            
            print()
            
        except Exception as e:
            print(f"  ❌ Error processing {inbox_file.name}: {str(e)}")
            print()
    
    print("=" * 60)
    print(f"✅ Processed {processed_count}/{len(inbox_files)} file(s)")
    print("=" * 60)

if __name__ == '__main__':
    try:
        process_inbox()
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

