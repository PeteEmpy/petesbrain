# Messaging Processing Instructions

## Overview

This skill processes messages from various messaging platforms (Google Chat, WhatsApp, email notifications) and routes them intelligently to clients, creates tasks, or saves to knowledge base.

## Processing Flow

1. **Receive Message** → Extract content, sender, timestamp
2. **Detect Client** → Match against known client list
3. **Identify Intent** → Task, note, knowledge, completion
4. **Route Appropriately** → Client folder, todo, knowledge base
5. **Create Tasks** → Google Tasks + local todo files

## Client Detection

### Known Clients
- accessories-for-the-home
- bright-minds
- clear-prospects
- crowd-control
- devonshire-hotels
- go-glean
- godshot
- grain-guard
- just-bin-bags
- national-design-academy
- otc
- positive-bakes
- print-my-pdf
- smythson
- superspace
- tree2mydoor
- uno-lighting

### Detection Methods
1. Explicit mention in message (e.g., "Smythson", "Devonshire")
2. Client name variations (e.g., "devonshire-hotels" → "Devonshire Hotels")
3. Context clues (campaign names, account references)
4. Sender domain analysis (if available)

## Intent Detection

### Task Indicators
- Action verbs: "review", "check", "update", "create"
- Time references: "by Friday", "this week", "urgent"
- Request patterns: "can you", "please", "need to"

### Client Note Indicators
- Performance updates: "ROAS", "conversions", "budget"
- Strategic discussions: "strategy", "plan", "proposal"
- Status updates: "campaign", "account", "performance"

### Knowledge Indicators
- Learning content: "article", "guide", "best practice"
- Reference material: "documentation", "tutorial"
- General information not tied to specific client

### Completion Indicators
- Past tense: "completed", "finished", "done"
- Status updates: "already did", "just finished"

## Routing Rules

### Client Notes → `clients/[client]/documents/inbox-capture-YYYYMMDD.md`
- Client mentioned in message
- Contains client-specific context
- Performance updates or strategic discussions

### Tasks → `todo/YYYYMMDD-[title].md` + Google Tasks
- Contains actionable items
- Has time references or urgency
- Requires follow-up

### Knowledge → `roksys/knowledge-base/inbox-captures/`
- General learning content
- Not client-specific
- Reference material

### Completions → Client documents (not tasks)
- Something already done
- Status update
- Historical record

## Task Creation

### Required Fields
- **Title**: Clear, actionable task description
- **Description**: Full context from message
- **Due Date**: Extract from message if mentioned
- **Priority**: Detect from urgency indicators

### Google Tasks Integration
- Create task via `shared/google_tasks_client.py`
- Save task ID to local todo file
- Link to original message source

## Message Sources

### Google Chat
- Processed via `agents/google-chat-processor/google-chat-processor.py`
- Messages saved from Gmail notifications
- Space name indicates context

### WhatsApp
- Processed via `agents/whatsapp-processor/whatsapp-processor.py`
- Messages from email notifications
- Sender phone/name indicates context

### Email Notifications
- Chat/WhatsApp notifications in Gmail
- Extracted via Gmail API
- Formatted for inbox processing

## AI Enhancement

When AI-enhanced processing is available:
- Use Claude to analyze message intent
- Extract structured data (client, task, priority)
- Generate context summaries
- Create email drafts when appropriate

## Error Handling

- Unknown client → General todo or knowledge base
- Unclear intent → Save to inbox for manual review
- Missing context → Preserve original message for reference
- Processing errors → Log and continue with next message

## Best Practices

1. **Preserve Original**: Always keep original message content
2. **Add Metadata**: Include source, timestamp, sender info
3. **Link Tasks**: Reference original message in task notes
4. **Context Summary**: Generate brief summary for CONTEXT.md
5. **Deduplication**: Check for similar existing tasks/notes

