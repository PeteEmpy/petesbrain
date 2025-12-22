#!/usr/bin/env python3
"""
PetesBrain Conversational Knowledge Base Search - Backend API Server

A Flask-based API server that provides conversational AI search across:
- Knowledge base content (roksys/knowledge-base/)
- Client-specific content (meeting notes, emails, documents, tasks)
- Multi-source synthesis with full conversation context

Modes:
- Strategic Advisor: -style strategic recommendations
- Quick Answer: Fast, concise responses
- Research Assistant: Deep analysis with multiple sources
- Client Briefing: Client-specific synthesis

Author: PetesBrain
Created: 2025-11-28
"""

import os
import sys
import json
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic

# Import Google Ads API integration for campaign data
from google_ads_integration import google_ads_client, format_campaign_data_for_prompt

# Load environment from .env file if it exists
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    print(f"Loading environment from {ENV_FILE}")
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("✅ Loaded API key from .env file")

# Configure paths
SCRIPT_DIR = Path(__file__).parent
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain")
KB_ROOT = PETESBRAIN_ROOT / "roksys" / "knowledge-base"
CLIENTS_ROOT = PETESBRAIN_ROOT / "clients"
KB_INDEX_PATH = PETESBRAIN_ROOT / "shared" / "data" / "kb-index.json"
CLIENT_INDEX_PATH = PETESBRAIN_ROOT / "shared" / "data" / "client-index.json"
SESSIONS_DIR = SCRIPT_DIR / "sessions"

# Ensure sessions directory exists
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

# Initialize Anthropic client
def get_anthropic_client():
    """Get or create Anthropic client - uses explicit API key from environment"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return anthropic.Anthropic(api_key=api_key)


@dataclass
class Message:
    """Represents a single message in the conversation"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    sources: Optional[List[Dict]] = None
    mode: Optional[str] = None


@dataclass
class Session:
    """Represents a conversation session"""
    session_id: str
    created_at: str
    last_updated: str
    messages: List[Message]
    context: Dict  # Store conversation context (client, topics, etc.)


class ConversationManager:
    """Manages conversation sessions and context"""

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self._load_active_sessions()

    def _load_active_sessions(self):
        """Load active sessions from disk"""
        if not SESSIONS_DIR.exists():
            return

        for session_file in SESSIONS_DIR.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    messages = [
                        Message(**msg) for msg in data.get('messages', [])
                    ]
                    session = Session(
                        session_id=data['session_id'],
                        created_at=data['created_at'],
                        last_updated=data['last_updated'],
                        messages=messages,
                        context=data.get('context', {})
                    )
                    self.sessions[session.session_id] = session
                    logger.info(f"Loaded session {session.session_id}")
            except Exception as e:
                logger.error(f"Error loading session {session_file}: {e}")

    def create_session(self) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        session = Session(
            session_id=session_id,
            created_at=now,
            last_updated=now,
            messages=[],
            context={}
        )

        self.sessions[session_id] = session
        self._save_session(session)

        logger.info(f"Created new session: {session_id}")
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID"""
        return self.sessions.get(session_id)

    def add_message(self, session_id: str, message: Message):
        """Add a message to a session"""
        session = self.sessions.get(session_id)
        if not session:
            logger.error(f"Session {session_id} not found")
            return

        session.messages.append(message)
        session.last_updated = datetime.now().isoformat()
        self._save_session(session)

    def update_context(self, session_id: str, context_updates: Dict):
        """Update session context"""
        session = self.sessions.get(session_id)
        if not session:
            return

        session.context.update(context_updates)
        self._save_session(session)

    def _save_session(self, session: Session):
        """Save session to disk"""
        session_file = SESSIONS_DIR / f"{session.session_id}.json"

        data = {
            'session_id': session.session_id,
            'created_at': session.created_at,
            'last_updated': session.last_updated,
            'messages': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp,
                    'sources': msg.sources,
                    'mode': msg.mode
                }
                for msg in session.messages
            ],
            'context': session.context
        }

        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for context"""
        session = self.sessions.get(session_id)
        if not session:
            return []

        # Return last N messages
        recent_messages = session.messages[-limit:]
        return [
            {
                'role': msg.role,
                'content': msg.content
            }
            for msg in recent_messages
        ]


class MultiSourceSearch:
    """Searches across KB and client content with intelligent ranking"""

    def __init__(self):
        self.kb_index = self._load_kb_index()
        self.client_index = self._load_client_index()

    def _load_kb_index(self) -> Dict:
        """Load knowledge base index"""
        if not KB_INDEX_PATH.exists():
            logger.warning(f"KB index not found: {KB_INDEX_PATH}")
            return {'files': []}

        with open(KB_INDEX_PATH, 'r') as f:
            return json.load(f)

    def _load_client_index(self) -> Dict:
        """Load client content index"""
        if not CLIENT_INDEX_PATH.exists():
            logger.warning(f"Client index not found: {CLIENT_INDEX_PATH}")
            return {'files': []}

        with open(CLIENT_INDEX_PATH, 'r') as f:
            return json.load(f)

    def search(
        self,
        query: str,
        client: Optional[str] = None,
        sources: List[str] = ['kb', 'client'],
        limit: int = 20
    ) -> List[Dict]:
        """
        Search across multiple sources

        Args:
            query: Search query
            client: Optional client filter
            sources: List of sources to search ('kb', 'client')
            limit: Maximum results to return

        Returns:
            List of search results with scores
        """
        results = []

        # Search KB if requested
        if 'kb' in sources:
            kb_results = self._search_kb(query, limit)
            results.extend(kb_results)

        # Search client content if requested
        if 'client' in sources:
            client_results = self._search_client(query, client, limit)
            results.extend(client_results)

        # Sort by relevance score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:limit]

    def _search_kb(self, query: str, limit: int) -> List[Dict]:
        """Search knowledge base"""
        query_lower = query.lower()
        results = []

        for file_info in self.kb_index.get('files', []):
            score = 0

            # Title matching (highest weight)
            title = file_info.get('title', '').lower()
            if query_lower in title:
                score += 10

            # Category matching
            category = file_info.get('category', '').lower()
            if query_lower in category:
                score += 5

            # Preview matching
            preview = file_info.get('preview', '').lower()
            if query_lower in preview:
                score += 3

            # Filename matching
            filename = file_info.get('filename', '').lower()
            if query_lower in filename:
                score += 2

            if score > 0:
                results.append({
                    'source': 'kb',
                    'type': 'knowledge_base',
                    'title': file_info.get('title', file_info.get('filename')),
                    'path': file_info.get('path'),
                    'category': file_info.get('category'),
                    'preview': file_info.get('preview', '')[:200],
                    'date': file_info.get('date'),
                    'score': score
                })

        return results

    def _search_client(
        self,
        query: str,
        client: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Search client content"""
        query_lower = query.lower()
        results = []

        for file_info in self.client_index.get('files', []):
            # Filter by client if specified
            if client and file_info.get('client', '').lower() != client.lower():
                continue

            score = 0

            # Title/subject matching
            title = file_info.get('title', file_info.get('subject', '')).lower()
            if query_lower in title:
                score += 10

            # Content type matching
            content_type = file_info.get('type', '').lower()

            # Preview matching
            preview = file_info.get('preview', '').lower()
            if query_lower in preview:
                score += 5

            # Client name matching
            if query_lower in file_info.get('client', '').lower():
                score += 3

            if score > 0:
                results.append({
                    'source': 'client',
                    'type': content_type,
                    'client': file_info.get('client'),
                    'title': title,
                    'path': file_info.get('path'),
                    'preview': file_info.get('preview', '')[:200],
                    'date': file_info.get('date'),
                    'score': score
                })

        return results

    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        full_path = PETESBRAIN_ROOT / file_path

        if not full_path.exists():
            logger.error(f"File not found: {full_path}")
            return ""

        try:
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading {full_path}: {e}")
            return ""


class ConversationalAI:
    """Handles AI-powered conversational responses"""

    def __init__(self, search_engine: MultiSourceSearch):
        self.search = search_engine
        self.model = "claude-sonnet-4-20250514"
        self.model_quick = "claude-3-5-haiku-20241022"

    def generate_response(
        self,
        query: str,
        mode: str,
        conversation_history: List[Dict],
        client: Optional[str] = None
    ) -> Tuple[str, List[Dict]]:
        """
        Generate AI response based on mode

        Args:
            query: User query
            mode: Response mode (strategic, quick, research, briefing)
            conversation_history: Previous messages for context
            client: Optional client context

        Returns:
            Tuple of (response_text, sources_used)
        """
        # Search for relevant content
        search_results = self.search.search(
            query=query,
            client=client,
            sources=['kb', 'client'],
            limit=15
        )

        # Read top results
        sources_content = []
        for i, result in enumerate(search_results[:10]):
            content = self.search.read_file(result['path'])
            if content:
                sources_content.append({
                    'title': result['title'],
                    'path': result['path'],
                    'type': result['type'],
                    'content': content[:3000],  # Limit content length
                    'score': result['score']
                })

        # Generate response based on mode
        if mode == 'strategic':
            response, sources = self._strategic_mode(
                query, sources_content, conversation_history, client
            )
        elif mode == 'quick':
            response, sources = self._quick_mode(
                query, sources_content, conversation_history
            )
        elif mode == 'research':
            response, sources = self._research_mode(
                query, sources_content, conversation_history, client
            )
        elif mode == 'briefing':
            response, sources = self._briefing_mode(
                query, sources_content, conversation_history, client
            )
        else:
            response, sources = self._quick_mode(
                query, sources_content, conversation_history
            )

        return response, sources

    def _strategic_mode(
        self,
        query: str,
        sources: List[Dict],
        history: List[Dict],
        client: Optional[str]
    ) -> Tuple[str, List[Dict]]:
        """-style strategic advisor mode"""

        # Build context
        context = self._build_context(sources)
        history_text = self._format_history(history)

        client_context = f"\n\nClient Context: {client}" if client else ""

        # Fetch real-time campaign data if client is specified
        campaign_data_text = ""
        if client:
            logger.info(f"Fetching campaign data for {client} to enrich strategic analysis")
            try:
                campaign_data = google_ads_client.get_complete_client_data(client, days=30)
                campaign_data_text = "\n\n" + format_campaign_data_for_prompt(campaign_data)
                logger.info(f"✅ Added campaign data to strategic prompt")
            except Exception as e:
                logger.warning(f"Could not fetch campaign data for {client}: {e}")
                campaign_data_text = "\n\n*Campaign data unavailable - basing recommendations on knowledge base only.*"

        prompt = f"""You are , a world-class Google Ads strategist with deep expertise in Performance Max, Shopping, and Search campaigns. You're known for your strategic thinking and challenging conventional wisdom.

Previous Conversation:
{history_text}

Current Query: {query}{client_context}

Available Knowledge:
{context}{campaign_data_text}

Provide a strategic response in this format:

## Main Analysis
[Your strategic analysis with specific, actionable recommendations. Be direct and opinionated.]

## Recommended Reading
[List 2-3 most relevant sources with brief context on why they matter]

## Follow-Up Questions
[3-4 strategic questions to explore this topic deeper]

## Devil's Advocate
[Challenge an assumption or common belief related to this topic]

Use British English spelling throughout."""

        try:
            client = get_anthropic_client()
            response = client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            # Extract sources used
            sources_used = [
                {
                    'title': s['title'],
                    'path': s['path'],
                    'type': s['type']
                }
                for s in sources[:5]
            ]

            return response_text, sources_used

        except Exception as e:
            logger.error(f"Error generating strategic response: {e}")
            return f"Error generating response: {str(e)}", []

    def _quick_mode(
        self,
        query: str,
        sources: List[Dict],
        history: List[Dict]
    ) -> Tuple[str, List[Dict]]:
        """Quick, concise answer mode"""

        context = self._build_context(sources)
        history_text = self._format_history(history)

        prompt = f"""You are a knowledgeable digital marketing assistant with expertise in Google Ads, Facebook Ads, and e-commerce.

Previous Conversation:
{history_text}

Current Query: {query}

Available Knowledge:
{context}

Provide a concise, direct answer (2-3 paragraphs maximum). Include specific facts and recommendations. Cite sources when appropriate.

Use British English spelling."""

        try:
            client = get_anthropic_client()
            response = client.messages.create(
                model=self.model_quick,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            sources_used = [
                {
                    'title': s['title'],
                    'path': s['path'],
                    'type': s['type']
                }
                for s in sources[:3]
            ]

            return response_text, sources_used

        except Exception as e:
            logger.error(f"Error generating quick response: {e}")
            return f"Error generating response: {str(e)}", []

    def _research_mode(
        self,
        query: str,
        sources: List[Dict],
        history: List[Dict],
        client: Optional[str]
    ) -> Tuple[str, List[Dict]]:
        """Deep research and analysis mode"""

        context = self._build_context(sources)
        history_text = self._format_history(history)

        client_context = f"\n\nClient Context: {client}" if client else ""

        # Fetch campaign data if client specified
        campaign_data_text = ""
        if client:
            logger.info(f"Fetching campaign data for {client} research")
            try:
                campaign_data = google_ads_client.get_complete_client_data(client, days=30)
                campaign_data_text = "\n\n" + format_campaign_data_for_prompt(campaign_data)
                logger.info(f"✅ Added campaign data to research prompt")
            except Exception as e:
                logger.warning(f"Could not fetch campaign data: {e}")
                campaign_data_text = ""

        prompt = f"""You are a research analyst specialising in digital marketing and e-commerce. Provide comprehensive, well-researched analysis.

Previous Conversation:
{history_text}

Current Query: {query}{client_context}

Available Knowledge:
{context}{campaign_data_text}

Provide a thorough research response with:

1. **Executive Summary**: Key findings in 2-3 sentences
2. **Detailed Analysis**: Comprehensive breakdown with evidence from sources
3. **Synthesis**: How different sources relate and what patterns emerge
4. **Recommendations**: Specific, actionable next steps
5. **Sources**: Full list of sources consulted with relevance notes

Use British English spelling throughout."""

        try:
            client = get_anthropic_client()
            response = client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            sources_used = [
                {
                    'title': s['title'],
                    'path': s['path'],
                    'type': s['type']
                }
                for s in sources[:8]
            ]

            return response_text, sources_used

        except Exception as e:
            logger.error(f"Error generating research response: {e}")
            return f"Error generating response: {str(e)}", []

    def _briefing_mode(
        self,
        query: str,
        sources: List[Dict],
        history: List[Dict],
        client: Optional[str]
    ) -> Tuple[str, List[Dict]]:
        """Client-specific briefing mode"""

        if not client:
            return "Client briefing mode requires a client to be specified.", []

        context = self._build_context(sources)
        history_text = self._format_history(history)

        # Fetch current campaign data - CRITICAL for briefing mode
        campaign_data_text = ""
        logger.info(f"Fetching campaign data for {client} briefing")
        try:
            campaign_data = google_ads_client.get_complete_client_data(client, days=30)
            campaign_data_text = "\n\n" + format_campaign_data_for_prompt(campaign_data)
            logger.info(f"✅ Added campaign data to briefing prompt")
        except Exception as e:
            logger.warning(f"Could not fetch campaign data: {e}")
            campaign_data_text = "\n\n*Campaign data unavailable.*"

        prompt = f"""You are creating a client briefing for {client}. Combine knowledge base best practices with client-specific history and current campaign performance.

Previous Conversation:
{history_text}

Current Query: {query}

Client: {client}

Available Knowledge (KB + Client History):
{context}{campaign_data_text}

Provide a client briefing with:

## Current Performance Summary
[Summary of current campaign metrics if available - spend, ROAS, key trends]

## Client Overview
[Brief summary of client context from sources]

## Strategic Recommendations
[Specific, data-driven recommendations for {client} based on current performance, history, and KB best practices]

## What We've Done Before
[Relevant past work from meeting notes, emails, tasks]

## Next Steps
[Concrete action items tailored to {client} with priority ranking]

## Knowledge Base References
[Relevant KB articles they should know about]

Use British English spelling throughout."""

        try:
            client = get_anthropic_client()
            response = client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text

            sources_used = [
                {
                    'title': s['title'],
                    'path': s['path'],
                    'type': s['type']
                }
                for s in sources[:10]
            ]

            return response_text, sources_used

        except Exception as e:
            logger.error(f"Error generating briefing response: {e}")
            return f"Error generating response: {str(e)}", []

    def _build_context(self, sources: List[Dict]) -> str:
        """Build context string from sources"""
        if not sources:
            return "No relevant sources found."

        context_parts = []
        for i, source in enumerate(sources, 1):
            context_parts.append(f"""
Source {i}: {source['title']} ({source['type']})
Path: {source['path']}
Content:
{source['content']}
---
""")

        return "\n".join(context_parts)

    def _format_history(self, history: List[Dict]) -> str:
        """Format conversation history"""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            formatted.append(f"{role}: {msg['content']}")

        return "\n".join(formatted)


# Initialize managers
conversation_manager = ConversationManager()
search_engine = MultiSourceSearch()
ai_engine = ConversationalAI(search_engine)


# API Endpoints

@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Create a new conversation session"""
    session_id = conversation_manager.create_session()
    return jsonify({
        'session_id': session_id,
        'status': 'created'
    })


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session details"""
    session = conversation_manager.get_session(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    return jsonify({
        'session_id': session.session_id,
        'created_at': session.created_at,
        'last_updated': session.last_updated,
        'message_count': len(session.messages),
        'context': session.context
    })


@app.route('/api/session/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """Get conversation history"""
    session = conversation_manager.get_session(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    messages = [
        {
            'role': msg.role,
            'content': msg.content,
            'timestamp': msg.timestamp,
            'sources': msg.sources,
            'mode': msg.mode
        }
        for msg in session.messages
    ]

    return jsonify({
        'session_id': session_id,
        'messages': messages
    })


@app.route('/api/query', methods=['POST'])
def query():
    """Process a conversational query"""
    data = request.json

    session_id = data.get('session_id')
    query_text = data.get('query')
    mode = data.get('mode', 'quick')  # strategic, quick, research, briefing
    client = data.get('client')

    if not session_id or not query_text:
        return jsonify({'error': 'session_id and query are required'}), 400

    # Verify session exists
    session = conversation_manager.get_session(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    # Add user message
    user_message = Message(
        role='user',
        content=query_text,
        timestamp=datetime.now().isoformat(),
        mode=mode
    )
    conversation_manager.add_message(session_id, user_message)

    # Get conversation history
    history = conversation_manager.get_conversation_history(session_id)

    # Generate AI response
    try:
        response_text, sources = ai_engine.generate_response(
            query=query_text,
            mode=mode,
            conversation_history=history,
            client=client
        )

        # Add assistant message
        assistant_message = Message(
            role='assistant',
            content=response_text,
            timestamp=datetime.now().isoformat(),
            sources=sources,
            mode=mode
        )
        conversation_manager.add_message(session_id, assistant_message)

        # Update context if client specified
        if client:
            conversation_manager.update_context(
                session_id,
                {'client': client}
            )

        return jsonify({
            'response': response_text,
            'sources': sources,
            'mode': mode,
            'timestamp': assistant_message.timestamp
        })

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search():
    """Direct search endpoint (no conversation context)"""
    data = request.json

    query_text = data.get('query')
    client = data.get('client')
    sources = data.get('sources', ['kb', 'client'])
    limit = data.get('limit', 20)

    if not query_text:
        return jsonify({'error': 'query is required'}), 400

    try:
        results = search_engine.search(
            query=query_text,
            client=client,
            sources=sources,
            limit=limit
        )

        return jsonify({
            'query': query_text,
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        logger.error(f"Error in search: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clients', methods=['GET'])
def list_clients():
    """List available clients"""
    clients = []

    if CLIENTS_ROOT.exists():
        for client_dir in CLIENTS_ROOT.iterdir():
            if client_dir.is_dir() and (client_dir / "CONTEXT.md").exists():
                clients.append(client_dir.name)

    return jsonify({
        'clients': sorted(clients)
    })


@app.route('/')
def index():
    """Serve the web interface"""
    return send_from_directory(SCRIPT_DIR / 'static', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return send_from_directory(SCRIPT_DIR / 'static', path)


if __name__ == '__main__':
    logger.info("Starting PetesBrain Conversational Search Server")
    logger.info(f"KB Root: {KB_ROOT}")
    logger.info(f"Clients Root: {CLIENTS_ROOT}")
    logger.info(f"Sessions: {SESSIONS_DIR}")

    # Run server
    app.run(
        host='127.0.0.1',
        port=5555,
        debug=True
    )
