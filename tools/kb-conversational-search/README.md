# PetesBrain Conversational Knowledge Search

A web-based conversational AI search interface for the PetesBrain knowledge base and client content.

## Features

### Multi-Source Search
- **Knowledge Base**: Search 1,117+ documents across Google Ads, Facebook Ads, Shopify, and methodology content
- **Client Content**: Search meeting notes, emails, documents, and completed tasks
- **Unified Search**: Intelligently combines KB and client content with relevance ranking

### Conversation Modes

1. **⚡ Quick Answer** - Fast, concise responses for specific questions
2. **🎯 Strategic Advisor** - Mike Rhodes-style strategic recommendations with:
   - Main Analysis with actionable steps
   - Recommended Reading
   - Follow-Up Questions
   - Devil's Advocate challenges
3. **🔍 Research Assistant** - Deep analysis with:
   - Executive Summary
   - Detailed Analysis
   - Synthesis across sources
   - Specific recommendations
4. **📋 Client Briefing** - Client-specific insights combining:
   - KB best practices
   - Client history (meetings, emails, tasks)
   - Tailored recommendations

### Conversation Context
- **Full session memory**: Maintains conversation history across queries
- **Follow-up questions**: AI understands context from previous exchanges
- **Session persistence**: Save and resume conversations
- **Client context**: Automatically filters by client when specified

### Source Citations
- Every response includes links to source documents
- See exactly which KB articles or client files were referenced
- Source type indicators (knowledge_base, meeting, email, document, etc.)

### Real-Time Campaign Data (NEW)
- **Direct Google Ads API Integration**: Automatically pulls campaign data using Google Ads Python library
- **Strategic Analysis**: Strategic Advisor, Research Assistant, and Client Briefing modes now include real-time metrics:
  - Google Ads spend, revenue, ROAS, conversions
  - Per-campaign performance breakdown (top 10 campaigns by spend)
  - Multi-account aggregation (UK, USA, EUR, ROW)
- **Platform IDs**: Parses client CONTEXT.md files to extract Google Ads customer IDs and manager account IDs
- **Intelligent Enrichment**: Only fetches campaign data when client is specified for relevant query types
- **Session Caching**: In-memory cache prevents redundant API calls during conversation

## Installation

1. **Navigate to the tool directory:**
```bash
cd /Users/administrator/Documents/PetesBrain/tools/kb-conversational-search
```

2. **Set up environment:**
```bash
# Make startup script executable
chmod +x start.sh

# Ensure ANTHROPIC_API_KEY is set
export ANTHROPIC_API_KEY='your-api-key-here'
```

3. **Start the server:**
```bash
./start.sh
```

The script will:
- Create a virtual environment
- Install dependencies
- Start the Flask server on `http://127.0.0.1:5555`
- Open the web interface in your browser

## Usage

### Basic Search
1. Open http://127.0.0.1:5555 in your browser
2. Select a mode (Quick Answer, Strategic Advisor, Research Assistant, or Client Briefing)
3. Optionally select a client filter
4. Type your question and press Send (or Cmd/Ctrl + Enter)

### Example Queries

**Quick Answer Mode:**
- "What's the latest on Performance Max audience signals?"
- "How do I set up conversion tracking in GA4?"
- "What are best practices for Shopping campaign structure?"

**Strategic Advisor Mode:**
- "How should I optimise budget allocation for Smythson?"
- "What's the best approach for Performance Max vs Shopping campaigns?"
- "How can we improve ROAS for luxury e-commerce?"

**Research Assistant Mode:**
- "Analyse the evolution of Google Ads bidding strategies"
- "What do we know about seasonal performance patterns?"
- "Compare Performance Max and Shopping campaign effectiveness"

**Client Briefing Mode:**
- "What have we done for Smythson related to Performance Max?"
- "Summarise Tree2MyDoor's Q4 strategy"
- "What's the history of Devonshire Hotels budget changes?"

### Follow-Up Questions
The system maintains conversation context, so you can ask follow-up questions:

```
You: "What are best practices for PMAX?"
AI: [Provides strategic recommendations]

You: "How does that apply to luxury brands?"
AI: [References previous answer and adapts for luxury context]

You: "What have we done for Smythson in this area?"
AI: [Combines PMAX strategy with Smythson client history]
```

### Client Filtering
Set the "Client" dropdown to filter all searches to specific client content. This is especially useful for:
- Client Briefing mode
- Reviewing past work
- Finding specific meetings or emails

## Architecture

### Backend (server.py)
- **Flask API** with CORS support
- **Session Management**: Creates, stores, and retrieves conversation sessions
- **Multi-Source Search**: Searches KB index and client index with scoring
- **AI Response Generation**: Uses Claude Sonnet 4 and Haiku models
- **File Reading**: Reads markdown content from KB and client folders
- **Google Ads Integration** (google_ads_integration.py): Direct API integration for real-time campaign data

### Frontend (static/index.html)
- **Modern chat UI** with message bubbles
- **Mode selection** and client filtering
- **Real-time updates** with loading states
- **Source citations** displayed with each response
- **Session management** (new session button)
- **Markdown rendering** for formatted responses

### Data Sources
- **KB Index**: `/Users/administrator/Documents/PetesBrain/shared/data/kb-index.json`
- **Client Index**: `/Users/administrator/Documents/PetesBrain/shared/data/client-index.json`
- **KB Content**: `/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/`
- **Client Content**: `/Users/administrator/Documents/PetesBrain/clients/`

### Sessions
- Stored in: `sessions/*.json`
- Contains full conversation history
- Includes context (client, topics)
- Persists across server restarts

## API Endpoints

### `POST /api/session/create`
Create a new conversation session
```json
Response: {
  "session_id": "uuid",
  "status": "created"
}
```

### `GET /api/session/<session_id>`
Get session details
```json
Response: {
  "session_id": "uuid",
  "created_at": "2025-11-28T10:00:00",
  "last_updated": "2025-11-28T10:05:00",
  "message_count": 4,
  "context": {"client": "smythson"}
}
```

### `GET /api/session/<session_id>/history`
Get conversation history
```json
Response: {
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "Question text",
      "timestamp": "2025-11-28T10:00:00",
      "mode": "quick"
    },
    {
      "role": "assistant",
      "content": "Response text",
      "timestamp": "2025-11-28T10:00:05",
      "sources": [...],
      "mode": "quick"
    }
  ]
}
```

### `POST /api/query`
Process a conversational query
```json
Request: {
  "session_id": "uuid",
  "query": "Question text",
  "mode": "strategic",  // quick, strategic, research, briefing
  "client": "smythson"   // optional
}

Response: {
  "response": "AI response text",
  "sources": [
    {
      "title": "Document title",
      "path": "roksys/knowledge-base/google-ads/pmax/article.md",
      "type": "knowledge_base"
    }
  ],
  "mode": "strategic",
  "timestamp": "2025-11-28T10:00:05"
}
```

### `POST /api/search`
Direct search (no conversation context)
```json
Request: {
  "query": "search term",
  "client": "smythson",  // optional
  "sources": ["kb", "client"],  // default both
  "limit": 20
}

Response: {
  "query": "search term",
  "results": [...],
  "count": 15
}
```

### `GET /api/clients`
List available clients
```json
Response: {
  "clients": ["smythson", "tree2mydoor", "devonshire-hotels", ...]
}
```

## AI Models Used

| Mode | Model | Max Tokens | Purpose |
|------|-------|------------|---------|
| Strategic Advisor | Claude Sonnet 4 | 4,000 | Deep strategic analysis |
| Research Assistant | Claude Sonnet 4 | 4,000 | Comprehensive research |
| Client Briefing | Claude Sonnet 4 | 4,000 | Client-specific synthesis |
| Quick Answer | Claude 3.5 Haiku | 1,000 | Fast, concise responses |

## Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` (required): Your Anthropic API key

### Paths (configured in server.py)
```python
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain")
KB_ROOT = PETESBRAIN_ROOT / "roksys" / "knowledge-base"
CLIENTS_ROOT = PETESBRAIN_ROOT / "clients"
KB_INDEX_PATH = PETESBRAIN_ROOT / "shared" / "data" / "kb-index.json"
CLIENT_INDEX_PATH = PETESBRAIN_ROOT / "shared" / "data" / "client-index.json"
SESSIONS_DIR = SCRIPT_DIR / "sessions"
```

### Server Configuration
```python
host='127.0.0.1'
port=5555
debug=True
```

### Google Ads API Requirements
The campaign data enrichment feature requires:
- **Google Ads Python library** (google-ads>=28.4.0) - installed in venv
- **OAuth credentials** from `/infrastructure/mcp-servers/google-ads-mcp-server/`:
  - `credentials.json` - OAuth client ID and secret
  - `google_ads_token.json` - Refresh token for API access
- **Developer token**: VrzEP-PTSY01pm1BJidERQ (configured in google_ads_integration.py)
- **Client CONTEXT.md files** with Google Ads customer IDs and manager account ID

If OAuth credentials are not configured, campaign data will be unavailable but the system will function normally with KB and client content only.

## Troubleshooting

### "Session not found" error
The session has expired or doesn't exist. Click "🔄 New Session" to start fresh.

### Empty search results
1. Check that KB and client indexes are up to date:
   ```bash
   python3 /Users/administrator/Documents/PetesBrain/agents/knowledge-base-indexer/knowledge-base-indexer.py
   python3 /Users/administrator/Documents/PetesBrain/agents/client-indexer/client-indexer.py
   ```
2. Verify indexes exist:
   ```bash
   ls -lh /Users/administrator/Documents/PetesBrain/shared/data/*.json
   ```

### API errors
1. Check `ANTHROPIC_API_KEY` is set correctly
2. Check server logs in terminal for specific error messages
3. Verify internet connection (API calls require network access)

### Port already in use
If port 5555 is already in use, edit `server.py`:
```python
app.run(
    host='127.0.0.1',
    port=5556,  # Change to different port
    debug=True
)
```

## Integration with Existing Tools

This conversational search interface **complements** the existing command-line tools:

| Tool | Use Case |
|------|----------|
| `kb-search.py` | Quick CLI searches, scripting, automation |
| `client-search.py` | CLI client content searches |
| **Conversational Search** | Interactive exploration, multi-turn questions, strategic analysis |

All tools use the same indexes and content sources, ensuring consistency.

## Google Ads Integration Details

### How Campaign Data Enrichment Works

When you ask a strategic question with a client specified, the system:

1. **Detects Client Context**: Checks if a client is selected in the UI
2. **Parses CONTEXT.md**: Extracts Google Ads customer IDs and manager account ID using regex
3. **Initialises Google Ads Client**: Creates GoogleAdsClient with OAuth credentials and login_customer_id
4. **Executes GAQL Queries**: Runs Google Ads Query Language queries for customer-level and campaign-level data
5. **Aggregates Multi-Account Data**: Sums metrics across all regional accounts (UK, USA, EUR, ROW)
6. **Enriches Prompt**: Adds formatted campaign data to the AI prompt
7. **Data-Driven Response**: AI generates recommendations based on real performance metrics

### Campaign Data Included

- **Google Ads Summary** (last 30 days):
  - Spend, Revenue, ROAS, Conversions
  - Clicks, Impressions, CTR, CPC, CPA
- **Campaign Performance** (last 7 days):
  - Top 10 campaigns by spend
  - Per-campaign ROAS and metrics
- **GA4 Summary** (last 30 days):
  - Sessions, Users, Pageviews
  - Conversions and Revenue

### Example Strategic Query with Campaign Data

```
Mode: Strategic Advisor
Client: smythson
Query: "How should we optimise our Performance Max campaigns?"

AI Response Includes:
- Current ROAS analysis (£150k spend, 3.2 ROAS)
- Specific campaign performance breakdown
- Strategic recommendations based on actual data
- KB best practices applied to current situation
```

### Fallback Behaviour

If campaign data is unavailable (OAuth credentials invalid, platform IDs not configured, API errors), the system:
- Logs a warning
- Continues with KB and client content only
- Adds note: "*Campaign data unavailable - basing recommendations on knowledge base only.*"

### CONTEXT.md Format Requirements

For Google Ads integration to work, client CONTEXT.md files must include:

```markdown
Manager Account ID: 2569949686

- UK: 8573235780
- USA: 7808690871
- EUR: 7679616761
- ROW: 5556710725
```

The regex parser looks for:
- `Manager Account ID: NNNNNNNNNN` or `Manager ID: NNNNNNNNNN`
- Regional patterns: `UK: NNNNNNNNNN`, `USA: NNNNNNNNNN`, etc.
- Standalone IDs in list format: `- NNNNNNNNNN`

## Future Enhancements

Potential improvements:
- [ ] Campaign data visualisation (charts in web UI)
- [ ] Historical trend analysis (compare week-over-week, month-over-month)
- [ ] Export conversation to markdown
- [ ] Share conversations via URL
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Saved favourite queries
- [ ] Integration with task creation
- [ ] Email/Slack notifications for important findings
- [ ] Advanced filtering (date ranges, content types)
- [ ] Conversation analytics and insights

## Author

Created by PetesBrain on 2025-11-28

## License

Internal tool for PetesBrain use only.
