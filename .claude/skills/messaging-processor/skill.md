---
name: messaging-processor
description: Processes and routes messages from Google Chat, WhatsApp, and other messaging platforms to appropriate clients and creates tasks. Use when processing Google Chat messages, WhatsApp messages, extracting tasks from messages, or routing inbox communications.
allowed-tools: Bash, Read, Write, mcp__google-tasks__list_task_lists, mcp__google-tasks__list_tasks, mcp__google-tasks__create_task
---

# Messaging Processing Skill

**Capabilities**:
- Analyze message content to detect client mentions
- Identify actionable items and convert to tasks
- Extract context and route to appropriate client folders
- Process messages through inbox system automatically
- Handle multiple messaging platforms (Google Chat, WhatsApp, email notifications)

**Progressive Context Loading**:
1. **Metadata**: Skill purpose and trigger patterns
2. **Instructions**: How to process messages, detect clients, create tasks
3. **Resources**: Client list, routing rules, task creation patterns

**Integration Points**:
- Google Chat processor (`agents/google-chat-processor/google-chat-processor.py`)
- WhatsApp processor (`agents/whatsapp-processor/whatsapp-processor.py`)
- Inbox processor (`agents/system/inbox-processor.py`)
- AI-enhanced processors (`agents/system/ai-inbox-processor.py`, `agents/system/ai-google-chat-processor.py`)
- Google Tasks client (`shared/google_tasks_client.py`)

**Example Usage**:
- "Process the Google Chat messages from Collaber PPC Chat"
- "Extract tasks from WhatsApp messages about Smythson"
- "Route this message to the right client folder"
- "Create a task from this WhatsApp message"

**Output**:
- Client-allocated messages in appropriate folders
- Tasks created in Google Tasks and local todo files
- Context summaries for CONTEXT.md updates
- Email drafts when appropriate

