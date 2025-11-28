# Messaging Processing Resources

## Client List Reference

### Full Client Names (for matching)
```
accessories-for-the-home
bright-minds
clear-prospects
crowd-control
devonshire-hotels
go-glean
godshot
grain-guard
just-bin-bags
national-design-academy
otc
positive-bakes
print-my-pdf
smythson
superspace
tree2mydoor
uno-lighting
```

### Client Name Variations
- **devonshire-hotels**: "Devonshire", "Devonshire Hotels", "devonshirehotels"
- **just-bin-bags**: "Just Bin Bags", "justbinbags", "JBB"
- **tree2mydoor**: "Tree2mydoor", "Tree 2 My Door", "Tree to My Door", "T2MD"
- **national-design-academy**: "National Design Academy", "NDA", "Design Academy"
- **accessories-for-the-home**: "Accessories for the Home", "AFTH"
- **bright-minds**: "Bright Minds", "brightminds"
- **clear-prospects**: "Clear Prospects", "clearprospects"
- **crowd-control**: "Crowd Control", "crowdcontrol"
- **uno-lighting**: "Uno Lighting", "Uno Lights", "unolighting"
- **print-my-pdf**: "Print My PDF", "printmypdf"

## Task Priority Indicators

### High Priority
- "urgent", "asap", "immediately", "today"
- "blocking", "critical", "important"
- Time pressure: "by end of day", "before meeting"

### Medium Priority
- "this week", "soon", "when you can"
- Standard requests without urgency

### Low Priority
- "someday", "eventually", "nice to have"
- Exploratory or research tasks

## Due Date Patterns

### Relative Dates
- "today" → Today's date
- "tomorrow" → Next day
- "this week" → End of current week (Friday)
- "next week" → Following week
- "end of month" → Last day of current month

### Day Names
- "Monday", "Tuesday", etc. → Next occurrence
- "Friday this week" → Current week's Friday
- "Friday next week" → Following week's Friday

### Absolute Dates
- "2025-11-15" → Parse directly
- "November 15" → Current year, November 15
- "15th November" → Current year, November 15

## Action Keywords

### Task Creation Keywords
- `task: [title]` → Explicit task directive
- Action verbs: review, check, update, create, analyze, implement
- Request patterns: "can you", "please", "need to", "should we"

### Client Routing Keywords
- `client: [name]` → Explicit client directive
- Client name mentions in message
- Campaign/account references

### Knowledge Keywords
- `knowledge: [topic]` → Explicit knowledge directive
- Learning content: article, guide, tutorial, documentation
- General information not client-specific

### Email Draft Keywords
- `email [client]:` → Generate email draft
- Client communication needs
- Follow-up required

## Message Format Patterns

### Google Chat Format
```
Space: [Space Name]
From: [Sender Name] <email>
Time: [Timestamp]
Message: [Content]
```

### WhatsApp Format
```
From: [Sender Name] ([Phone Number])
Time: [Timestamp]
Message: [Content]
```

### Email Notification Format
```
Subject: '[Space Name] space mention – [Preview]'
From: chat-noreply@google.com or noreply@whatsapp.com
Body: [Sender] mentioned you...
      [Message Content]
```

## Processing Scripts Reference

### Main Processors
- `agents/google-chat-processor/google-chat-processor.py` - Google Chat via Gmail
- `agents/whatsapp-processor/whatsapp-processor.py` - WhatsApp via email
- `agents/inbox-processor/inbox-processor.py` - Main inbox router
- `agents/ai-inbox-processor/ai-inbox-processor.py` - AI-enhanced inbox processing
- `agents/ai-google-chat-processor/ai-google-chat-processor.py` - AI-enhanced Chat processing

### Client Libraries
- `shared/google_chat_via_gmail_client.py` - Google Chat email client
- `shared/whatsapp_via_email_client.py` - WhatsApp email client
- `shared/google_tasks_client.py` - Google Tasks integration

### State Tracking
- `!inbox/.google-chat-processor-state.json` - Processed Chat messages
- `!inbox/.whatsapp-processor-state.json` - Processed WhatsApp messages
- `!inbox/.ai-google-chat-processor-state.json` - AI-processed Chat messages

## File Locations

### Inbox Processing
- `!inbox/` - Raw messages
- `!inbox/ai-enhanced/` - AI-enhanced messages
- `!inbox/processed/` - Archived processed messages

### Client Documents
- `clients/[client]/documents/inbox-capture-YYYYMMDD.md`
- `clients/[client]/emails/drafts/` - Email drafts

### Tasks
- `todo/YYYYMMDD-[title].md` - Local todo files
- Google Tasks - Cloud task list

### Knowledge Base
- `roksys/knowledge-base/inbox-captures/` - General knowledge

## Common Patterns

### Client Performance Update
```
Pattern: "[Client] [metric] [change]"
Example: "Smythson ROAS up to 4.5x this week"
Action: Route to client documents, add context summary
```

### Task Request
```
Pattern: "[Action] [object] [timeframe]"
Example: "Review Devonshire budget by Friday"
Action: Create task with due date, link to client
```

### Knowledge Sharing
```
Pattern: "[Resource] about [topic]"
Example: "Article about PMax best practices"
Action: Route to knowledge base
```

### Completion Update
```
Pattern: "[Past tense action] [object]"
Example: "Completed Smythson audit"
Action: Route to client documents (not tasks)
```

