#!/usr/bin/env python3
"""
AI-Enhanced Inbox Processor (Enhanced Version)

Processes notes from !inbox/ with advanced AI intelligence:
- Duplicate/similar task detection
- Smarter CONTEXT.md reading (relevant sections)
- Completion detection
- Related task linking
- Batch processing with cross-note context
- Email draft generation for client notes
- Time estimation
- Follow-up detection
- Adaptive model selection (Haiku vs Sonnet)
- Dependency and blocker detection
- Urgency vs priority separation
- Calendar awareness

Runs after wispr-flow-importer but before inbox-processor.
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from difflib import SequenceMatcher

# Add project root to path (from centralized discovery)
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import centralized path discovery, ClientTasksService, and Keychain secrets
from shared.paths import get_project_root
from shared.client_tasks_service import ClientTasksService
from shared.secrets import get_secret

# Verify project root can be discovered
try:
    PROJECT_ROOT = get_project_root()
except RuntimeError as e:
    print(f"Error: {e}")
    print("Make sure PETESBRAIN_ROOT environment variable is set or run from project directory")
    sys.exit(1)

# Anthropic API
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("⚠️  anthropic package not installed. Run: pip install anthropic")
    ANTHROPIC_AVAILABLE = False

# Google Tasks integration DEPRECATED (2025-12-16)
# Duplicate checking now uses internal task system only
GOOGLE_TASKS_AVAILABLE = False

# Fuzzy string matching for duplicates
try:
    from rapidfuzz import fuzz
    FUZZ_AVAILABLE = True
except ImportError:
    # Fallback to difflib if rapidfuzz not available
    FUZZ_AVAILABLE = False

INBOX_DIR = PROJECT_ROOT / '!inbox'
PROCESSED_DIR = INBOX_DIR / 'processed'
AI_ENHANCED_DIR = INBOX_DIR / 'ai-enhanced'
PROCESSED_STATE_FILE = INBOX_DIR / '.ai-processed-state.json'

def load_processed_state() -> set:
    """Load set of already-processed filenames to prevent reprocessing"""
    if PROCESSED_STATE_FILE.exists():
        try:
            with open(PROCESSED_STATE_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_files', []))
        except:
            pass
    return set()

def save_processed_state(processed_files: set):
    """Save set of processed filenames"""
    try:
        with open(PROCESSED_STATE_FILE, 'w') as f:
            json.dump({
                'processed_files': list(processed_files),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        print(f"  ⚠️ Warning: Could not save processed state: {e}")

CLIENTS_DIR = PROJECT_ROOT / 'clients'
EMAIL_DRAFTS_DIR = CLIENTS_DIR  # Will create drafts/ subdirectory per client

# Known clients
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
    'positive-bakes',
    'print-my-pdf',
    'smythson',
    'superspace',
    'tree2mydoor',
    'uno-lighting'
]

# Completion detection patterns
COMPLETION_PATTERNS = [
    r'\b(done|completed|finished|already did|already done|just finished|just completed)\b',
    r'\b(i\'ve|i have) (done|completed|finished)\b',
    r'\b(already|just) (did|completed|finished)\b',
    r'\bno longer needed\b',
    r'\bcancel(?:led)?\b',
]

# Follow-up detection patterns
FOLLOWUP_PATTERNS = [
    r'\b(follow up|follow-up|followup|check on|status of|update on)\b',
    r'\b(re:?|regarding|about|concerning)\b',
    r'\b(yesterday\'s|last week\'s|previous)\b',
]

# Dependency/blocker patterns
DEPENDENCY_PATTERNS = [
    r'\b(waiting for|after|once|when|until|depends on|blocked by|blocking on)\b',
    r'\b(needs|requires|needing)\b',
    r'\b(can\'t|cannot) (start|begin|do) (until|before|after)\b',
]

# Action keywords for fast-path routing (pattern)
ACTION_KEYWORDS = {
    'claude': 'direct_execution',
    'ai': 'direct_execution',
    'skill': 'invoke_skill',
    'audit': 'invoke_audit_skill',
    'analyze csv': 'invoke_csv_analyzer',
    'search kb': 'invoke_kb_search',
    'quick task': 'quick_task',
    'quick todo': 'quick_task',
}

def parse_fuzzy_date(date_text: str) -> Optional[str]:
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

def similarity_score(text1: str, text2: str) -> float:
    """Calculate similarity score between two texts (0-100)"""
    if not text1 or not text2:
        return 0.0
    
    if FUZZ_AVAILABLE:
        # Use rapidfuzz for better performance
        return max(
            fuzz.ratio(text1.lower(), text2.lower()),
            fuzz.partial_ratio(text1.lower(), text2.lower()),
            fuzz.token_sort_ratio(text1.lower(), text2.lower()),
            fuzz.token_set_ratio(text1.lower(), text2.lower())
        )
    else:
        # Fallback to difflib
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio() * 100

def check_duplicate_tasks(task_title: str, task_description: str = None) -> Tuple[Optional[Dict], float]:
    """
    Check for duplicate or similar tasks in recent notes.

    Returns:
        (matching_task_dict, similarity_score) or (None, 0.0)
    """
    matches = []

    # Google Tasks checking DEPRECATED (2025-12-16)
    # Only check recent processed notes for duplicates

    # Check recent processed notes (last 7 days)
    if PROCESSED_DIR.exists():
        cutoff_date = datetime.now() - timedelta(days=7)
        for file_path in PROCESSED_DIR.glob('*.md'):
            try:
                # Check file modification time
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    continue
                
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                    # Extract task title if present
                    title_match = re.search(r'^task:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
                    if title_match:
                        existing_title = title_match.group(1).strip()
                        sim = similarity_score(task_title, existing_title)
                        
                        if sim > 70:
                            matches.append({
                                'task': None,
                                'similarity': sim,
                                'source': 'recent_note',
                                'title': existing_title,
                                'file': str(file_path)
                            })
            except Exception as e:
                continue
    
    # Return best match
    if matches:
        best_match = max(matches, key=lambda x: x['similarity'])
        return best_match, best_match['similarity']
    
    return None, 0.0

def read_context_md_smart(client: str, note_content: str) -> Optional[str]:
    """
    Read relevant sections of CONTEXT.md instead of just truncating.
    Uses AI to identify which sections are most relevant.
    """
    context_path = CLIENTS_DIR / client / 'CONTEXT.md'
    
    if not context_path.exists():
        return None
    
    try:
        with open(context_path, 'r') as f:
            full_content = f.read()
        
        # If file is small, return it all
        if len(full_content) < 3000:
            return full_content
        
        # Use AI to extract relevant sections
        api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
        if not api_key or not ANTHROPIC_AVAILABLE:
            # Fallback: return first 3000 chars
            return full_content[:3000]
        
        try:
            client_anthropic = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Extract the most relevant sections from this CONTEXT.md file for understanding this note:

NOTE CONTENT:
{note_content[:500]}

CONTEXT.MD FILE:
{full_content[:8000]}  # First 8000 chars for analysis

Identify and extract the most relevant sections such as:
- Current Strategy / Active Campaigns
- Planned Work / Current Tasks
- Recent Issues / Problems
- Client Preferences
- Business Context relevant to the note

Return ONLY the relevant sections, preserving markdown formatting. If multiple sections are relevant, include them all.
Keep total output under 4000 characters."""

            response = client_anthropic.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1500,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            relevant_sections = response.content[0].text.strip()
            return relevant_sections if relevant_sections else full_content[:3000]
            
        except Exception as e:
            print(f"  ⚠️  Error extracting relevant sections: {e}")
            return full_content[:3000]
            
    except Exception as e:
        print(f"  ⚠️  Error reading CONTEXT.md for {client}: {e}")
        return None

def detect_completion(note_content: str) -> bool:
    """Detect if note indicates something is already completed"""
    content_lower = note_content.lower()
    
    for pattern in COMPLETION_PATTERNS:
        if re.search(pattern, content_lower, re.IGNORECASE):
            return True
    
    return False

def detect_followup(note_content: str) -> Tuple[bool, Optional[str]]:
    """Detect if note is a follow-up and extract what it's following up on"""
    content_lower = note_content.lower()
    
    for pattern in FOLLOWUP_PATTERNS:
        if re.search(pattern, content_lower, re.IGNORECASE):
            # Try to extract what it's following up on
            # Simple extraction - could be improved
            return True, None  # Could enhance to extract specific reference
    
    return False, None

def detect_dependencies(note_content: str) -> List[str]:
    """Detect dependencies and blockers mentioned in note"""
    dependencies = []
    content_lower = note_content.lower()
    
    for pattern in DEPENDENCY_PATTERNS:
        matches = re.finditer(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            # Extract context around match
            start = max(0, match.start() - 50)
            end = min(len(note_content), match.end() + 50)
            context = note_content[start:end]
            dependencies.append(context.strip())
    
    return dependencies

def find_related_tasks(client: str, note_content: str) -> List[Dict]:
    """Find related tasks in CONTEXT.md"""
    related = []

    # Check CONTEXT.md for planned work
    context_path = CLIENTS_DIR / client / 'CONTEXT.md'
    if context_path.exists():
        try:
            with open(context_path, 'r') as f:
                context = f.read()

            # Look for "Planned Work" or "Current Tasks" sections
            planned_match = re.search(
                r'(?:Planned Work|Current Tasks|Active Tasks)[\s\S]*?(?=\n##|\Z)',
                context,
                re.IGNORECASE
            )

            if planned_match:
                planned_section = planned_match.group(0)
                # Extract task-like items
                task_items = re.findall(r'[-*]\s*(.+?)(?:\n|$)', planned_section)
                for task in task_items[:5]:  # Limit to 5 most recent
                    if len(task) > 10:  # Only substantial tasks
                        related.append({
                            'title': task,
                            'source': 'context_md',
                            'type': 'planned_work'
                        })
        except Exception as e:
            pass

    # Google Tasks checking DEPRECATED (2025-12-16)
    # Only check CONTEXT.md for related tasks

    return related[:5]  # Return top 5 related items

def estimate_complexity(note_content: str) -> str:
    """Estimate note complexity to choose appropriate model"""
    word_count = len(note_content.split())
    sentence_count = len(re.split(r'[.!?]+', note_content))
    
    # Simple heuristics
    if word_count > 100 or sentence_count > 5:
        return 'complex'
    elif word_count > 50:
        return 'medium'
    else:
        return 'simple'

def get_client_from_content(content: str) -> Optional[str]:
    """Detect client name in content"""
    content_lower = content.lower()

    # Check for explicit client: prefix
    if content_lower.startswith('client:'):
        match = re.search(r'client:\s*(.+)', content_lower)
        if match:
            client_name = match.group(1).strip().split()[0]
            client_name = client_name.replace(' ', '-').replace('_', '-')
            for client in CLIENTS:
                if client_name in client or client in client_name:
                    return client

    # Check for client mentions in text
    for client in CLIENTS:
        client_variations = [
            client,
            client.replace('-', ' '),
            client.replace('-', ''),
        ]
        for variation in client_variations:
            if variation in content_lower:
                return client

    return None

def detect_action_keyword(content: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect action keyword in first 1-3 words (pattern).
    Returns (action_type, payload) or (None, None)
    """
    # Clean content and get first few words
    content_clean = content.strip()
    first_words_lower = ' '.join(content_clean.lower().split()[:3])

    # Check each keyword (order matters - longer keywords first)
    for keyword, action in sorted(ACTION_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if first_words_lower.startswith(keyword):
            # Extract remainder as payload
            keyword_len = len(keyword.split())
            payload = ' '.join(content_clean.split()[keyword_len:]).strip()
            return action, payload

    return None, None

def execute_claude_prompt(payload: str, note_filename: str) -> bool:
    """
    Fast-path: Execute Claude prompt directly (pattern).
    Voice: "claude analyze Superspace performance last 30 days"
    → Executes immediately, saves response, skips normal processing
    """
    if not ANTHROPIC_AVAILABLE:
        print("  ⚠️  Anthropic library not available for direct execution")
        return False

    api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set for direct execution (check Keychain or environment)")
        return False

    print(f"  ⚡ Fast-path: Direct Claude execution")
    print(f"  📝 Prompt: {payload[:100]}{'...' if len(payload) > 100 else ''}")

    try:
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": payload
            }]
        )

        result = response.content[0].text

        # Detect client from payload
        client_name = get_client_from_content(payload)

        # Create descriptive filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        slug = '-'.join(payload.split()[:5])  # First 5 words as slug
        slug = re.sub(r'[^a-z0-9-]', '', slug.lower())

        if client_name:
            filename = f"claude-{timestamp}-{client_name}-{slug}.md"
            dest_dir = CLIENTS_DIR / client_name / 'documents'
        else:
            filename = f"claude-{timestamp}-{slug}.md"
            dest_dir = PROJECT_ROOT / 'roksys' / 'documents'

        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename

        # Save result
        with open(dest_path, 'w') as f:
            f.write(f"# Claude Direct Execution\n")
            f.write(f"**Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Source Note:** {note_filename}\n\n")
            f.write(f"## Prompt\n\n{payload}\n\n")
            f.write(f"## Response\n\n{result}\n")

        print(f"  ✅ Executed and saved: {dest_path}")
        return True

    except Exception as e:
        print(f"  ❌ Error executing Claude prompt: {e}")
        return False

def invoke_skill_from_note(payload: str, note_filename: str) -> bool:
    """
    Fast-path: Invoke skill directly from note.
    Examples:
      "skill google-ads-campaign-audit smythson"
      "audit smythson"
    """
    print(f"  ⚡ Fast-path: Skill invocation")
    print(f"  📝 Payload: {payload}")

    # Parse skill name and args from payload
    parts = payload.split()
    if not parts:
        print("  ⚠️  No skill specified")
        return False

    # Determine skill based on context
    skill_name = None
    skill_args = ' '.join(parts[1:]) if len(parts) > 1 else ''

    # Direct skill name provided
    if parts[0] in ['google-ads-campaign-audit', 'csv-analyzer', 'kb-search']:
        skill_name = parts[0]
    # Shorthand mappings
    elif 'audit' in payload.lower():
        skill_name = 'google-ads-campaign-audit'
        skill_args = payload.replace('audit', '').strip()
    elif 'csv' in payload.lower():
        skill_name = 'csv-analyzer'
        skill_args = payload.replace('analyze csv', '').replace('csv', '').strip()
    elif 'search' in payload.lower() or 'kb' in payload.lower():
        skill_name = 'kb-search'
        skill_args = payload.replace('search kb', '').replace('kb', '').strip()

    if not skill_name:
        print(f"  ⚠️  Could not determine skill from: {payload}")
        return False

    print(f"  🎯 Skill: {skill_name}")
    print(f"  📌 Args: {skill_args}")

    # Save instruction to invoke skill (Claude Code will see this)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    slug = re.sub(r'[^a-z0-9-]', '', '-'.join(payload.split()[:4]).lower())
    filename = f"skill-invoke-{timestamp}-{slug}.md"

    dest_dir = PROJECT_ROOT / 'roksys' / 'documents'
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename

    with open(dest_path, 'w') as f:
        f.write(f"# Skill Invocation Request\n")
        f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Source Note:** {note_filename}\n\n")
        f.write(f"## Skill to Invoke\n\n")
        f.write(f"**Skill:** `{skill_name}`\n")
        f.write(f"**Arguments:** {skill_args}\n\n")
        f.write(f"## Instructions\n\n")
        f.write(f"Run the following in Claude Code:\n\n")
        f.write(f"```\n")
        f.write(f"Skill(skill=\"{skill_name}\")\n")
        f.write(f"```\n\n")
        f.write(f"With arguments: {skill_args}\n")

    print(f"  ✅ Skill invocation request saved: {dest_path}")
    print(f"  💡 Run manually in Claude Code when ready")
    return True

def create_quick_task(payload: str, note_filename: str) -> bool:
    """
    Fast-path: Create simple task without AI enhancement.
    Example: "quick task review Smythson budget tomorrow"

    Creates task ONLY in internal clients/[client]/tasks.json file.
    NO Google Tasks API calls - keeps everything local and fast.
    """
    print(f"  ⚡ Fast-path: Quick task creation")
    print(f"  📝 Task: {payload}")

    try:
        import uuid

        # Simple parsing
        task_title = payload
        due_date = None
        client_name = get_client_from_content(payload)

        if not client_name:
            print("  ⚠️  No client detected - cannot create client task")
            return False

        # Use fuzzy date parser to detect and parse date expressions
        # Try to parse the entire payload for date patterns
        due_date = parse_fuzzy_date(payload)

        # If we found a date, remove date keywords from title
        if due_date:
            # Remove common date expressions from title
            date_patterns = [
                r'\btomorrow\b', r'\btoday\b', r'\bnext week\b',
                r'\bin\s+\d+\s+days?\b', r'\bin\s+\d+\s+weeks?\b', r'\bin\s+\d+\s+months?\b',
                r'\bwithin\s+(?:a|the|next|1)\s+week\b', r'\bin\s+a\s+week\b',
                r'\bnext\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
            ]
            for pattern in date_patterns:
                task_title = re.sub(pattern, '', task_title, flags=re.IGNORECASE).strip()

        # Create task using ClientTasksService
        task_service = ClientTasksService()

        task_id = task_service.create_task(
            title=task_title,
            client=client_name,
            priority="P1",  # Default to P1 for quick tasks
            due_date=due_date,
            time_estimate_mins=None,
            notes=f"Source: Quick capture from voice note\nOriginal note: {note_filename}\n\nQuick task created without AI analysis.",
            source="Quick Capture",
            tags=[client_name],
            task_type="standalone"
        )

        print(f"  ✅ Quick task created: {task_title}")
        print(f"  📁 Saved to: clients/{client_name}/tasks.json (via ClientTasksService)")
        if due_date:
            print(f"  📅 Due: {due_date}")

        return True

    except Exception as e:
        print(f"  ❌ Error creating quick task: {e}")
        return False

def generate_descriptive_filename(note_type: str, client: Optional[str], content: str, timestamp: str = None) -> str:
    """
    Generate descriptive filename (pattern).
    Format: [type]-YYYYMMDD-[client]-[slug].md

    Examples:
      task-20251119-smythson-budget-review.md
      note-20251119-devonshire-trending-searches.md
      completion-20251119-uno-lighting-campaign-launch.md
    """
    if not timestamp:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Extract first 3-5 meaningful words for slug
    words = re.findall(r'\b\w{3,}\b', content.lower())  # Words 3+ chars
    slug_words = [w for w in words[:5] if w not in ['the', 'and', 'for', 'with', 'from']]
    slug = '-'.join(slug_words[:4])  # Max 4 words
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

def enhance_note_with_ai(
    note_content: str,
    note_filename: str,
    batch_context: List[Dict] = None,
    duplicate_info: Dict = None,
    related_tasks: List[Dict] = None
) -> Dict:
    """
    Use Claude API to analyze and enhance the note with all advanced features.
    
    Returns enhanced note dict with all metadata.
    """
    if not ANTHROPIC_AVAILABLE:
        return {'type': 'general', 'enhanced_content': note_content}

    api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set, skipping AI enhancement (check Keychain or environment)")
        return {'type': 'general', 'enhanced_content': note_content}

    # Detect if this is client-related
    client = get_client_from_content(note_content)
    context_content = None

    if client:
        context_content = read_context_md_smart(client, note_content)

    # Estimate complexity for model selection
    complexity = estimate_complexity(note_content)
    model = "claude-sonnet-4-5-20250929" if complexity == 'complex' else "claude-3-5-haiku-20241022"

    # Check for completion
    is_completion = detect_completion(note_content)
    
    # Check for follow-up
    is_followup, followup_ref = detect_followup(note_content)
    
    # Detect dependencies
    dependencies = detect_dependencies(note_content)

    # Build comprehensive prompt
    prompt = f"""Analyze this note captured via voice (Wispr Flow) and enhance it with intelligent processing:

NOTE CONTENT:
{note_content}

FILENAME: {note_filename}"""

    if client and context_content:
        prompt += f"""

DETECTED CLIENT: {client}

RELEVANT CONTEXT (from {client}/CONTEXT.md):
{context_content}"""

    if duplicate_info and duplicate_info['similarity'] > 70:
        prompt += f"""

⚠️ DUPLICATE DETECTION:
Found similar existing task: "{duplicate_info.get('title', 'Unknown')}"
Similarity: {duplicate_info['similarity']:.1f}%
Source: {duplicate_info.get('source', 'unknown')}
Consider if this is a duplicate or if it should be merged."""

    if related_tasks:
        prompt += f"""

RELATED TASKS/PROJECTS:
{chr(10).join([f"- {r.get('title', 'Unknown')} ({r.get('source', 'unknown')})" for r in related_tasks[:3]])}"""

    if batch_context:
        prompt += f"""

BATCH CONTEXT (other notes being processed today):
{len(batch_context)} other note(s) being processed. Consider if there are patterns or relationships."""

    if is_completion:
        prompt += "\n\n⚠️ COMPLETION DETECTED: This note appears to describe something already completed."

    if is_followup:
        prompt += "\n\n⚠️ FOLLOW-UP DETECTED: This appears to be a follow-up on something. Link to original if possible."

    if dependencies:
        prompt += f"\n\n⚠️ DEPENDENCIES DETECTED: {len(dependencies)} dependency/blocker mention(s) found."

    prompt += """

Analyze this note and provide comprehensive enhancement:

1. TYPE: Is this a:
   - client note (specific to a client's work)
   - task (something to be done)
   - knowledge (information to save for reference)
   - general (personal note)
   - completion (something already done - route to documents, not tasks)

2. ENHANCED CONTENT: Rewrite the note to be clear and actionable, fixing any voice transcription errors

3. If this is CLIENT-RELATED:
   - Which client? (use exact folder name from context)
   - What context is needed from CONTEXT.md?
   - Summary for CONTEXT.md update
   - Should an email draft be generated? (yes/no)

4. If this is a TASK:
   - Clear task title
   - Detailed description of what needs to be done
   - Priority (high/medium/low)
   - Urgency (urgent/time-sensitive or normal)
   - Estimated time (e.g., "30 min", "2 hours", "half day")
   - Suggested due date (if mentioned or implied)
   - Any blockers or dependencies (list them)
   - Related tasks/projects (if any)

5. If DUPLICATE detected:
   - Should this be merged with existing task? (yes/no)
   - If yes, suggest how to merge
   - If no, explain why it's different

6. ROUTING: Where should this go?
   - clients/[client]/documents/
   - todo/ + Google Task
   - roksys/knowledge-base/
   - General archive

7. If COMPLETION detected:
   - Route to client documents (not tasks)
   - Include completion summary

Respond in JSON format:
{
  "type": "client|task|knowledge|general|completion",
  "client": "client-folder-name or null",
  "enhanced_content": "cleaned up note content",
  "task_title": "clear task title or null",
  "task_description": "detailed task description or null",
  "priority": "high|medium|low or null",
  "urgency": "urgent|normal or null",
  "estimated_time": "time estimate or null",
  "due_date": "natural language due date or null",
  "dependencies": ["list of dependencies/blockers"],
  "related_tasks": ["list of related task titles"],
  "is_duplicate": true|false,
  "duplicate_action": "merge|create_new|review",
  "routing": "where to route this",
  "context_summary": "1-2 sentence summary for CONTEXT.md or null",
  "generate_email_draft": true|false,
  "email_draft_subject": "suggested email subject or null",
  "reasoning": "brief explanation of analysis"
}"""

    try:
        client_anthropic = anthropic.Anthropic(api_key=api_key)

        response = client_anthropic.messages.create(
            model=model,
            max_tokens=2000 if complexity == 'complex' else 1000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract JSON from response
        response_text = response.content[0].text

        # Try to find JSON in response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
            
            # Add detected metadata
            result['is_completion'] = is_completion
            result['is_followup'] = is_followup
            result['detected_dependencies'] = dependencies
            result['model_used'] = model
            
            return result
        else:
            print(f"  ⚠️  Could not parse AI response as JSON")
            return {'type': 'general', 'enhanced_content': note_content, 'is_completion': is_completion}

    except Exception as e:
        print(f"  ⚠️  AI enhancement error: {e}")
        return {'type': 'general', 'enhanced_content': note_content, 'is_completion': is_completion}

def generate_email_draft(client: str, note_content: str, enhanced_info: Dict, context_content: str = None) -> Optional[str]:
    """Generate email draft for client notes"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key or not ANTHROPIC_AVAILABLE:
        return None
    
    try:
        client_anthropic = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Generate a professional email draft for {client} based on this note:

ORIGINAL NOTE:
{note_content}

ENHANCED ANALYSIS:
{json.dumps(enhanced_info, indent=2)}

CONTEXT:
{context_content[:2000] if context_content else 'No additional context available'}

Generate a professional, concise email draft that:
- Uses appropriate tone for client communication
- References relevant context if available
- Is actionable and clear
- Includes a clear subject line
- Is ready to send (but mark as draft)

Format as:
SUBJECT: [subject line]

[email body]

Return only the email draft, no additional commentary."""

        response = client_anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            temperature=0.4,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text.strip()
        
    except Exception as e:
        print(f"  ⚠️  Error generating email draft: {e}")
        return None

def process_inbox():
    """Process all files in inbox with AI enhancement (with batch processing)"""

    # Ensure directories exist
    AI_ENHANCED_DIR.mkdir(exist_ok=True)

    # Get all markdown files in inbox (not in subdirectories)
    inbox_files = list(INBOX_DIR.glob('*.md'))

    if not inbox_files:
        print("📭 Inbox is empty - nothing to process\n")
        return

    print(f"📬 Found {len(inbox_files)} file(s) to process with AI\n")

    # Load state to prevent reprocessing files that got stuck
    processed_state = load_processed_state()

    # Read all notes for batch context
    batch_notes = []
    for file_path in inbox_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                batch_notes.append({
                    'filename': file_path.name,
                    'content': content[:200]  # Preview for context
                })
        except Exception as e:
            continue

    for file_path in inbox_files:
        # Skip if already processed (prevents reprocessing stuck files)
        if file_path.name in processed_state:
            print(f"⏭️  Skipping {file_path.name} - already processed (check !inbox/processed/ for archived version)")
            continue

        print(f"🤖 AI Processing: {file_path.name}")

        # Read original content
        try:
            with open(file_path, 'r') as f:
                original_content = f.read()
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            continue

        # === FAST-PATH DETECTION (pattern) ===
        # Check for action keywords BEFORE deep AI processing
        action, payload = detect_action_keyword(original_content)

        if action:
            print(f"  🚀 Action keyword detected: {action}")

            # Route to fast-path handler
            handled = False
            if action == 'direct_execution':
                handled = execute_claude_prompt(payload, file_path.name)
            elif action in ['invoke_skill', 'invoke_audit_skill', 'invoke_csv_analyzer', 'invoke_kb_search']:
                handled = invoke_skill_from_note(payload, file_path.name)
            elif action == 'quick_task':
                handled = create_quick_task(payload, file_path.name)

            # Archive original and skip full processing if handled
            if handled:
                try:
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                    archived_filename = f"{timestamp}-fastpath-{file_path.name}"
                    archived_path = PROCESSED_DIR / archived_filename
                    PROCESSED_DIR.mkdir(exist_ok=True)
                    file_path.rename(archived_path)
                    print(f"  📦 Archived: {archived_filename}")
                    # Mark as processed to prevent reprocessing
                    processed_state.add(file_path.name)
                    save_processed_state(processed_state)
                    print(f"  ⚡ Fast-path complete - skipped full AI processing\n")
                    continue  # Skip to next file
                except Exception as e:
                    print(f"  ⚠️  Error archiving: {e}")
                    # Still mark as processed to prevent infinite reprocessing
                    processed_state.add(file_path.name)
                    save_processed_state(processed_state)
            else:
                print(f"  ⚠️  Fast-path handler failed, falling back to full processing")

        # === NORMAL PROCESSING (if no fast-path or fast-path failed) ===

        # Pre-processing checks
        client = get_client_from_content(original_content)
        
        # Check for duplicates if this is a task
        duplicate_info = None
        if 'task' in original_content.lower() or 'do' in original_content.lower() or 'need' in original_content.lower():
            # Extract potential task title for duplicate check
            temp_enhanced = enhance_note_with_ai(original_content, file_path.name)
            task_title = temp_enhanced.get('task_title') or original_content[:50]
            duplicate_info, sim_score = check_duplicate_tasks(task_title, original_content)
            
            if duplicate_info and sim_score > 70:
                print(f"  ⚠️  Potential duplicate detected: {sim_score:.1f}% similar to '{duplicate_info.get('title', 'Unknown')}'")
        
        # Find related tasks
        related_tasks = []
        if client:
            related_tasks = find_related_tasks(client, original_content)

        # Enhance with AI (pass batch context)
        batch_context = [n for n in batch_notes if n['filename'] != file_path.name]
        enhanced = enhance_note_with_ai(
            original_content,
            file_path.name,
            batch_context=batch_context,
            duplicate_info=duplicate_info,
            related_tasks=related_tasks
        )

        # Handle completion detection
        if enhanced.get('is_completion') or enhanced.get('type') == 'completion':
            enhanced['type'] = 'completion'
            print(f"  ✅ Completion detected - routing to documents (not tasks)")

        # Display results
        print(f"  📊 Type: {enhanced.get('type', 'unknown')}")
        if enhanced.get('client'):
            print(f"  👤 Client: {enhanced.get('client')}")
        if enhanced.get('task_title'):
            print(f"  ✓ Task: {enhanced.get('task_title')}")
            print(f"  📝 Priority: {enhanced.get('priority', 'medium')}")
            if enhanced.get('urgency'):
                print(f"  ⚡ Urgency: {enhanced.get('urgency')}")
            if enhanced.get('estimated_time'):
                print(f"  ⏱️  Estimated time: {enhanced.get('estimated_time')}")
        if enhanced.get('is_duplicate'):
            print(f"  🔄 Duplicate: {enhanced.get('duplicate_action', 'review')}")
        if enhanced.get('routing'):
            print(f"  📍 Route to: {enhanced.get('routing')}")
        if enhanced.get('reasoning'):
            print(f"  💡 Reasoning: {enhanced.get('reasoning')}")

        # Generate email draft if requested
        email_draft = None
        if enhanced.get('generate_email_draft') and client:
            print(f"  📧 Generating email draft...")
            context_content = read_context_md_smart(client, original_content) if client else None
            email_draft = generate_email_draft(client, original_content, enhanced, context_content)
            
            if email_draft:
                # Save email draft
                drafts_dir = CLIENTS_DIR / client / 'emails' / 'drafts'
                drafts_dir.mkdir(parents=True, exist_ok=True)
                
                draft_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-draft.md"
                draft_path = drafts_dir / draft_filename
                
                with open(draft_path, 'w') as f:
                    f.write(f"# Email Draft - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                    f.write(f"**Source Note:** {file_path.name}\n\n")
                    f.write("---\n\n")
                    f.write(email_draft)
                
                print(f"  ✓ Email draft saved: {draft_path}")

        # Create enhanced file
        enhanced_filename = f"enhanced-{file_path.name}"
        enhanced_path = AI_ENHANCED_DIR / enhanced_filename

        # Build enhanced file content with metadata
        enhanced_file_content = f"""# AI-Enhanced Note
**Original:** {file_path.name}
**Type:** {enhanced.get('type', 'unknown')}
**Client:** {enhanced.get('client', 'N/A')}
**Priority:** {enhanced.get('priority', 'N/A')}
**Urgency:** {enhanced.get('urgency', 'N/A')}
**Estimated Time:** {enhanced.get('estimated_time', 'N/A')}
**Model Used:** {enhanced.get('model_used', 'haiku')}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""

        # Add duplicate warning if detected
        if enhanced.get('is_duplicate'):
            enhanced_file_content += f"""⚠️ **DUPLICATE DETECTED**: {enhanced.get('duplicate_action', 'review')}
**Similar to:** {duplicate_info.get('title', 'Unknown')} ({duplicate_info.get('similarity', 0):.1f}% similar)

"""

        # Add dependencies if detected
        if enhanced.get('dependencies') or enhanced.get('detected_dependencies'):
            deps = enhanced.get('dependencies', []) or enhanced.get('detected_dependencies', [])
            enhanced_file_content += f"""**Dependencies/Blockers:**
{chr(10).join([f"- {dep}" for dep in deps])}

"""

        # Add related tasks if found
        if enhanced.get('related_tasks') or related_tasks:
            related = enhanced.get('related_tasks', []) or [r.get('title') for r in related_tasks]
            enhanced_file_content += f"""**Related Tasks:**
{chr(10).join([f"- {rt}" for rt in related[:5]])}

"""

        # Add routing directive for regular inbox processor
        if enhanced.get('type') == 'completion':
            # Completions go to documents, not tasks
            if enhanced.get('client'):
                enhanced_file_content += f"client: {enhanced.get('client')}\n\n"
            enhanced_file_content += f"**COMPLETION NOTE** - Route to documents folder\n\n"
        elif enhanced.get('type') == 'task' and enhanced.get('task_title'):
            # For tasks, add task directive first
            enhanced_file_content += f"task: {enhanced.get('task_title')}\n"
            if enhanced.get('due_date'):
                enhanced_file_content += f"due: {enhanced.get('due_date')}\n"
            if enhanced.get('estimated_time'):
                enhanced_file_content += f"time: {enhanced.get('estimated_time')}\n"
            if enhanced.get('urgency') == 'urgent':
                enhanced_file_content += f"urgent: true\n"
            # Add client as a note field (not routing directive) if present
            if enhanced.get('client'):
                enhanced_file_content += f"client: {enhanced.get('client')}\n"
            enhanced_file_content += "\n"
        elif enhanced.get('type') == 'client' and enhanced.get('client'):
            enhanced_file_content += f"client: {enhanced.get('client')}\n\n"
        elif enhanced.get('type') == 'knowledge':
            enhanced_file_content += "knowledge: General\n\n"

        # Add enhanced content
        if enhanced.get('task_description'):
            enhanced_file_content += f"{enhanced.get('task_description')}\n\n"
        else:
            enhanced_file_content += f"{enhanced.get('enhanced_content', original_content)}\n\n"

        # Add context summary if available
        if enhanced.get('context_summary'):
            enhanced_file_content += f"---\n\n**Context Summary:** {enhanced.get('context_summary')}\n"

        # Add original for reference
        enhanced_file_content += f"\n---\n\n**Original Note:**\n{original_content}\n"

        # Save enhanced version
        try:
            with open(enhanced_path, 'w') as f:
                f.write(enhanced_file_content)
            print(f"  ✓ Saved enhanced version: {enhanced_filename}")
        except Exception as e:
            print(f"  ❌ Error saving enhanced file: {e}")
            continue

        # Move original to processed
        try:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            archived_filename = f"{timestamp}-original-{file_path.name}"
            archived_path = PROCESSED_DIR / archived_filename
            PROCESSED_DIR.mkdir(exist_ok=True)

            file_path.rename(archived_path)
            print(f"  📦 Archived original: {archived_filename}")
            # Mark as processed to prevent reprocessing if file gets stuck
            processed_state.add(file_path.name)
            save_processed_state(processed_state)
        except Exception as e:
            print(f"  ⚠️  Error archiving original: {e}")
            # Still mark as processed to prevent infinite reprocessing
            processed_state.add(file_path.name)
            save_processed_state(processed_state)

        print()

    print(f"✅ AI processing complete")
    print(f"   Enhanced notes → !inbox/ai-enhanced/")
    print(f"   Ready for regular inbox processor")

if __name__ == '__main__':
    print("============================================================")
    print("  AI-Enhanced Inbox Processor (Enhanced Version)")
    print("============================================================\n")

    process_inbox()

    print("\n============================================================")
