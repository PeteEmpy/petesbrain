# Google Chat Processing System

**Status:** ✅ Active  
**Last Updated:** 2025-11-08

## Overview

The Google Chat Processing System automatically fetches messages from Google Chat spaces shared with you and processes them similar to inbox messages. It allocates chats to clients and creates tasks as needed.

## How It Works

### Processing Flow

```
Google Chat Spaces (shared with you)
    ↓
Google Chat Processor (fetches messages)
    ↓
AI-Enhanced Processor (optional - adds intelligence)
    ↓
!inbox/ai-enhanced/ (enhanced messages)
    ↓
Regular Inbox Processor (routes to clients/tasks)
    ↓
clients/[client]/documents/ or todo/
```

## Components

### 1. Google Chat Client (`shared/google_chat_client.py`)

Wrapper around Google Chat API that:
- Lists all accessible spaces
- Fetches messages from spaces
- Formats messages for inbox processing
- Saves messages to `!inbox/` directory

### 2. Google Chat Processor (`agents/system/google-chat-processor.py`)

Basic processor that:
- Fetches recent messages (default: last 7 days)
- Saves them to `!inbox/` for processing
- Tracks processed messages to avoid duplicates
- Runs every hour via LaunchAgent

**Usage:**
```bash
python3 agents/system/google-chat-processor.py --days 7
```

### 3. AI-Enhanced Google Chat Processor (`agents/system/ai-google-chat-processor.py`)

Intelligent processor that:
- Fetches recent messages
- Uses Claude AI to analyze and enhance messages
- Detects clients, tasks, and other intents
- Adds routing directives automatically
- Saves enhanced versions to `!inbox/ai-enhanced/`
- Runs every 30 minutes via LaunchAgent

**Usage:**
```bash
python3 agents/system/ai-google-chat-processor.py --days 7
```

## Setup

### 1. Enable Google Chat API

The system uses the same OAuth credentials as Google Tasks. Ensure:
- Google Chat API is enabled in your Google Cloud project
- OAuth credentials include Chat API scopes:
  - `https://www.googleapis.com/auth/chat.messages.readonly`
  - `https://www.googleapis.com/auth/chat.spaces.readonly`

### 2. Authenticate

If you haven't already authenticated with Chat API scopes, you may need to re-authenticate:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly"
]

credentials_path = Path("shared/mcp-servers/google-tasks-mcp-server/credentials.json")
token_path = Path("shared/mcp-servers/google-tasks-mcp-server/token.json")

flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
creds = flow.run_local_server()

with open(token_path, 'w') as f:
    f.write(creds.to_json())
```

### 3. Install LaunchAgents (Optional)

To run automatically:

```bash
# Basic processor (every hour)
ln -sf /Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.google-chat-processor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.google-chat-processor.plist

# AI-enhanced processor (every 30 minutes)
ln -sf /Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.ai-google-chat-processor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.ai-google-chat-processor.plist
```

## How Messages Are Processed

### Step 1: Fetch Messages

The processor fetches messages from all accessible Google Chat spaces (or specific spaces if filtered).

### Step 2: AI Enhancement (if using AI processor)

Each message is analyzed by Claude AI to:
- Detect client mentions
- Identify tasks vs. notes
- Extract priority and urgency
- Suggest routing
- Generate context summaries

### Step 3: Save to Inbox

Messages are saved to `!inbox/` (or `!inbox/ai-enhanced/` for AI-enhanced versions) with:
- Space name
- Sender information
- Timestamp
- Message content
- Routing directives (if AI-enhanced)

### Step 4: Regular Inbox Processing

The regular inbox processor (`agents/system/inbox-processor.py`) picks up these messages and:
- Routes client notes to `clients/[client]/documents/`
- Creates tasks in `todo/` and Google Tasks
- Saves knowledge to `roksys/knowledge-base/`
- Archives processed files

## Features

### Client Detection

The AI processor automatically detects client mentions in chat messages and routes them appropriately.

### Task Creation

Messages that contain actionable items are automatically converted to tasks with:
- Clear task titles
- Detailed descriptions
- Priority levels
- Due dates (if mentioned)
- Time estimates

### Duplicate Prevention

The system tracks processed message IDs to avoid processing the same message twice.

### Space Filtering

You can filter by specific spaces:

```bash
python3 agents/system/google-chat-processor.py --spaces "spaces/AAAAxxxxxxx" "spaces/BBBByyyyyyy"
```

## Examples

### Example 1: Client Note from Chat

**Chat Message:**
> "Hey Peter, Smythson's shopping campaigns are performing really well this week. ROAS is up to 4.5x. Should we propose a budget increase?"

**AI Processing:**
- Detects: Client = "smythson"
- Type: Client note
- Routes to: `clients/smythson/documents/inbox-capture-YYYYMMDD.md`

### Example 2: Task from Chat

**Chat Message:**
> "Can you review the Devonshire budget for next month? Need it by Friday."

**AI Processing:**
- Detects: Client = "devonshire-hotels"
- Type: Task
- Task Title: "Review Devonshire budget for next month"
- Due Date: Friday
- Routes to: `todo/` + Google Task

## Troubleshooting

### "OAuth credentials not valid"

Ensure you've authenticated with Chat API scopes. See Setup section above.

### "No messages found"

- Check that you have access to the Google Chat spaces
- Verify the spaces are shared with your account
- Try increasing `--days` parameter

### "AI enhancement not working"

- Ensure `ANTHROPIC_API_KEY` is set in environment
- Check that `anthropic` package is installed: `pip install anthropic`

## Logs

- Basic processor: `~/.petesbrain-google-chat.log`
- AI processor: `~/.petesbrain-ai-google-chat.log`
- Errors: `~/.petesbrain-*-error.log`

## State Tracking

Processed message IDs are tracked in:
- `!inbox/.google-chat-processor-state.json` (basic processor)
- `!inbox/.ai-google-chat-processor-state.json` (AI processor)

This prevents duplicate processing.

