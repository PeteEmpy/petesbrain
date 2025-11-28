#!/usr/bin/env python3
"""
AI-Enhanced Google Chat Processor

Processes Google Chat messages with AI intelligence before routing:
- Fetches messages from Google Chat spaces
- Uses AI to analyze and enhance messages
- Detects clients, tasks, and other intents
- Routes to appropriate locations (clients, tasks, knowledge base)

This runs before the regular inbox-processor to add intelligence.
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Anthropic API
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("⚠️  anthropic package not installed. Run: pip install anthropic")
    ANTHROPIC_AVAILABLE = False

# Google Chat and Tasks integration (via Gmail)
try:
    from shared.google_chat_via_gmail_client import GoogleChatViaGmailClient
    GOOGLE_CHAT_ENABLED = True
except Exception as e:
    print(f"⚠️  Google Chat integration not available: {e}")
    GOOGLE_CHAT_ENABLED = False

try:
    from shared.google_tasks_client import GoogleTasksClient
    GOOGLE_TASKS_AVAILABLE = True
except ImportError:
    GOOGLE_TASKS_AVAILABLE = False

INBOX_DIR = PROJECT_ROOT / '!inbox'
AI_ENHANCED_DIR = INBOX_DIR / 'ai-enhanced'
PROCESSED_CHATS_DIR = PROJECT_ROOT / '!inbox' / 'processed-chats'
STATE_FILE = PROJECT_ROOT / '!inbox' / '.ai-google-chat-processor-state.json'
CLIENTS_DIR = PROJECT_ROOT / 'clients'

# Known clients (same as inbox processor)
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


def load_processed_message_ids() -> set:
    """Load set of already processed message IDs"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                return set(state.get('processed_message_ids', []))
        except Exception:
            return set()
    return set()


def save_processed_message_ids(message_ids: set):
    """Save set of processed message IDs"""
    try:
        PROCESSED_CHATS_DIR.mkdir(parents=True, exist_ok=True)
        
        state = {
            'processed_message_ids': list(message_ids),
            'last_run': datetime.now().isoformat()
        }
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving state: {e}")


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
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key or not ANTHROPIC_AVAILABLE:
            # Fallback: return first 3000 chars
            return full_content[:3000]
        
        try:
            client_anthropic = anthropic.Anthropic(api_key=api_key)
            
            prompt = f"""Extract the most relevant sections from this CONTEXT.md file for understanding this Google Chat message:

CHAT MESSAGE:
{note_content[:500]}

CONTEXT.MD FILE:
{full_content[:8000]}

Identify and extract the most relevant sections such as:
- Current Strategy / Active Campaigns
- Planned Work / Current Tasks
- Recent Issues / Problems
- Client Preferences
- Business Context relevant to the message

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


def enhance_chat_message_with_ai(
    message_text: str,
    space_name: str,
    sender_name: str,
    sender_email: str = None
) -> Dict:
    """
    Use Claude API to analyze and enhance a Google Chat message.
    
    Returns enhanced message dict with all metadata.
    """
    if not ANTHROPIC_AVAILABLE:
        return {'type': 'general', 'enhanced_content': message_text}

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set, skipping AI enhancement")
        return {'type': 'general', 'enhanced_content': message_text}

    # Detect if this is client-related
    client = get_client_from_content(message_text)
    context_content = None

    if client:
        context_content = read_context_md_smart(client, message_text)

    # Build comprehensive prompt
    prompt = f"""Analyze this Google Chat message and enhance it with intelligent processing:

MESSAGE CONTENT:
{message_text}

CONTEXT:
- Space: {space_name}
- From: {sender_name} {f'({sender_email})' if sender_email else ''}
- Source: Google Chat"""

    if client and context_content:
        prompt += f"""

DETECTED CLIENT: {client}

RELEVANT CONTEXT (from {client}/CONTEXT.md):
{context_content}"""

    prompt += """

Analyze this message and provide comprehensive enhancement:

1. TYPE: Is this a:
   - client note (specific to a client's work)
   - task (something to be done)
   - knowledge (information to save for reference)
   - general (personal note or conversation)
   - completion (something already done - route to documents, not tasks)

2. ENHANCED CONTENT: Rewrite the message to be clear and actionable, fixing any typos or unclear parts

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

5. ROUTING: Where should this go?
   - clients/[client]/documents/
   - todo/ + Google Task
   - roksys/knowledge-base/
   - General archive

Respond in JSON format:
{
  "type": "client|task|knowledge|general|completion",
  "client": "client-folder-name or null",
  "enhanced_content": "cleaned up message content",
  "task_title": "clear task title or null",
  "task_description": "detailed task description or null",
  "priority": "high|medium|low or null",
  "urgency": "urgent|normal or null",
  "estimated_time": "time estimate or null",
  "due_date": "natural language due date or null",
  "routing": "where to route this",
  "context_summary": "1-2 sentence summary for CONTEXT.md or null",
  "generate_email_draft": true|false,
  "email_draft_subject": "suggested email subject or null",
  "reasoning": "brief explanation of analysis"
}"""

    try:
        client_anthropic = anthropic.Anthropic(api_key=api_key)

        response = client_anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1500,
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
            return result
        else:
            print(f"  ⚠️  Could not parse AI response as JSON")
            return {'type': 'general', 'enhanced_content': message_text}

    except Exception as e:
        print(f"  ⚠️  AI enhancement error: {e}")
        return {'type': 'general', 'enhanced_content': message_text}


def process_google_chats_with_ai(days_back: int = 7, space_filter: list = None):
    """
    Fetch and process Google Chat messages with AI enhancement.
    
    Args:
        days_back: Number of days to look back for messages
        space_filter: Optional list of space names to filter by
    """
    if not GOOGLE_CHAT_ENABLED:
        print("❌ Google Chat integration not available")
        return
    
    # Ensure directories exist
    AI_ENHANCED_DIR.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("  AI-Enhanced Google Chat Processor")
    print("=" * 60)
    print()
    
    # Load already processed messages
    processed_ids = load_processed_message_ids()
    print(f"📋 Already processed: {len(processed_ids)} message(s)")
    print()
    
    try:
        # Initialize client
        client = GoogleChatViaGmailClient()
        
        # Fetch recent messages from Gmail
        print(f"🔍 Fetching Chat notification emails from last {days_back} day(s)...")
        chat_messages = client.get_chat_notification_emails(
            days_back=days_back
        )
        
        print()
        print(f"📬 Found {len(chat_messages)} Chat message(s)")
        print()
        
        if not chat_messages:
            print("✅ No new Chat messages to process")
            return
        
        # Filter out already processed messages
        new_messages = []
        for msg in chat_messages:
            email_id = msg.get('email_id', '')
            if email_id and email_id not in processed_ids:
                new_messages.append(msg)
        
        print(f"🆕 New messages: {len(new_messages)}")
        print()
        
        if not new_messages:
            print("✅ No new messages to process")
            return
        
        # Process each new message with AI
        processed_count = 0
        new_processed_ids = set(processed_ids)
        
        for msg in new_messages:
            email_id = msg.get('email_id', '')
            space_display = msg.get('space_name', 'Unknown Space')
            sender_name = msg.get('sender_name', 'Unknown')
            sender_email = msg.get('sender_email', '')
            message_text = msg.get('message_text', '')
            
            print(f"🤖 AI Processing: {space_display} - {sender_name}")
            
            # Skip empty messages
            if not message_text.strip():
                print(f"  ⚠️  Empty message, skipping")
                if email_id:
                    new_processed_ids.add(email_id)
                continue
            
            # Enhance with AI
            enhanced = enhance_chat_message_with_ai(
                message_text,
                space_display,
                sender_name,
                sender_email
            )
            
            # Display results
            print(f"  📊 Type: {enhanced.get('type', 'unknown')}")
            if enhanced.get('client'):
                print(f"  👤 Client: {enhanced.get('client')}")
            if enhanced.get('task_title'):
                print(f"  ✓ Task: {enhanced.get('task_title')}")
                print(f"  📝 Priority: {enhanced.get('priority', 'medium')}")
            if enhanced.get('routing'):
                print(f"  📍 Route to: {enhanced.get('routing')}")
            
            # Create enhanced file
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            enhanced_filename = f"enhanced-{timestamp}-google-chat-{email_id[:8] if email_id else 'unknown'}.md"
            enhanced_path = AI_ENHANCED_DIR / enhanced_filename
            
            # Build enhanced file content
            enhanced_file_content = f"""# AI-Enhanced Google Chat Message
**Original Source:** Google Chat - {space_display}
**From:** {sender_name} {f'<{sender_email}>' if sender_email else ''}
**Type:** {enhanced.get('type', 'unknown')}
**Client:** {enhanced.get('client', 'N/A')}
**Priority:** {enhanced.get('priority', 'N/A')}
**Urgency:** {enhanced.get('urgency', 'N/A')}
**Estimated Time:** {enhanced.get('estimated_time', 'N/A')}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
            
            # Add routing directive for regular inbox processor
            if enhanced.get('type') == 'completion':
                if enhanced.get('client'):
                    enhanced_file_content += f"client: {enhanced.get('client')}\n\n"
                enhanced_file_content += f"**COMPLETION NOTE** - Route to documents folder\n\n"
            elif enhanced.get('type') == 'task' and enhanced.get('task_title'):
                enhanced_file_content += f"task: {enhanced.get('task_title')}\n"
                if enhanced.get('due_date'):
                    enhanced_file_content += f"due: {enhanced.get('due_date')}\n"
                if enhanced.get('estimated_time'):
                    enhanced_file_content += f"time: {enhanced.get('estimated_time')}\n"
                if enhanced.get('urgency') == 'urgent':
                    enhanced_file_content += f"urgent: true\n"
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
                enhanced_file_content += f"{enhanced.get('enhanced_content', message_text)}\n\n"
            
            # Add context summary if available
            if enhanced.get('context_summary'):
                enhanced_file_content += f"---\n\n**Context Summary:** {enhanced.get('context_summary')}\n"
            
            # Add original for reference
            enhanced_file_content += f"\n---\n\n**Original Chat Message:**\n{message_text}\n"
            enhanced_file_content += f"\n**Space:** {space_display}\n"
            enhanced_file_content += f"**From:** {sender_name} {f'<{sender_email}>' if sender_email else ''}\n"
            enhanced_file_content += f"**Email ID:** {email_id}\n"
            
            # Save enhanced version
            try:
                with open(enhanced_path, 'w') as f:
                    f.write(enhanced_file_content)
                print(f"  ✓ Saved enhanced version: {enhanced_filename}")
                processed_count += 1
                
                # Mark as processed
                if email_id:
                    new_processed_ids.add(email_id)
            except Exception as e:
                print(f"  ❌ Error saving enhanced file: {e}")
            
            print()
        
        # Save updated state
        save_processed_message_ids(new_processed_ids)
        
        print("=" * 60)
        print(f"✅ Processed {processed_count}/{len(new_messages)} message(s)")
        print(f"   Enhanced notes → !inbox/ai-enhanced/")
        print(f"   Ready for regular inbox processor")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error processing Google Chats: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Process Google Chat messages with AI')
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (default: 7)'
    )
    parser.add_argument(
        '--spaces',
        nargs='+',
        help='Filter by specific space names (optional)'
    )
    
    args = parser.parse_args()
    
    process_google_chats_with_ai(
        days_back=args.days,
        space_filter=args.spaces
    )

