# WhatsApp Processing System

**Status:** ✅ Active (Email-Based)  
**Last Updated:** 2025-11-09

## Overview

The WhatsApp Processing System automatically processes WhatsApp messages via email notifications and routes them similar to inbox messages. It allocates chats to clients and creates tasks as needed.

## How It Works

### Processing Flow

```
WhatsApp Messages
    ↓
Email Notifications (if enabled in WhatsApp)
    ↓
Gmail API (fetches notification emails)
    ↓
WhatsApp Processor (extracts messages)
    ↓
!inbox/ (saved messages)
    ↓
Regular Inbox Processor (routes to clients/tasks)
    ↓
clients/[client]/documents/ or todo/
```

## Setup

### Step 1: Enable Email Notifications in WhatsApp

1. Open WhatsApp Settings
2. Go to **Notifications**
3. Enable **Email Notifications** (if available)
4. Or ensure WhatsApp sends email notifications for new messages

**Note:** WhatsApp may not send email notifications by default. You may need to:
- Use WhatsApp Business (which has better notification options)
- Forward important messages manually to email
- Use WhatsApp Business API (more complex setup)

### Step 2: Test the Processor

```bash
python3 agents/system/whatsapp-processor.py --days 30
```

## Components

### 1. WhatsApp via Email Client (`shared/whatsapp_via_email_client.py`)

Processes WhatsApp notification emails from Gmail:
- Searches for WhatsApp notification emails
- Extracts message content and sender info
- Formats messages for inbox processing
- Saves to `!inbox/` directory

### 2. WhatsApp Processor (`agents/system/whatsapp-processor.py`)

Basic processor that:
- Fetches recent WhatsApp notification emails (default: last 7 days)
- Extracts message content
- Saves them to `!inbox/` for processing
- Tracks processed messages to avoid duplicates

**Usage:**
```bash
# Process via email notifications (default)
python3 agents/system/whatsapp-processor.py --days 7

# Process via WhatsApp Business API webhook
python3 agents/system/whatsapp-processor.py --webhook < webhook.json
```

### 3. WhatsApp Business API Client (`shared/whatsapp_business_client.py`)

For advanced users who want to use WhatsApp Business API:
- Requires Meta Developer Account
- Requires WhatsApp Business App setup
- Uses webhooks for real-time message delivery

## Features

### Client Detection

Messages are processed through the regular inbox processor, which automatically detects client mentions and routes them appropriately.

### Task Creation

Messages that contain actionable items are automatically converted to tasks with:
- Clear task titles
- Detailed descriptions
- Priority levels
- Due dates (if mentioned)

### Duplicate Prevention

The system tracks processed message IDs to avoid processing the same message twice.

## Limitations

### Email-Based Approach

- **Requires email notifications enabled** in WhatsApp
- May not capture all messages (depends on notification settings)
- Message extraction depends on email format

### WhatsApp Business API Approach

- Requires business setup with Meta
- More complex configuration
- Better for high-volume business use

## Alternative Approaches

### Option 1: Manual Forwarding

Forward important WhatsApp messages to a dedicated email address, then process via email sync.

### Option 2: WhatsApp Business API

For business use, set up WhatsApp Business API for real-time webhook delivery.

### Option 3: WhatsApp Web Automation

Not recommended (violates ToS, unreliable).

## Examples

### Example 1: Client Message from WhatsApp

**WhatsApp Message:**
> "Hey Peter, Smythson's campaigns are performing well. Should we increase budget?"

**Processing:**
- Saved to `!inbox/`
- Regular inbox processor detects "Smythson"
- Routes to `clients/smythson/documents/inbox-capture-YYYYMMDD.md`

### Example 2: Task from WhatsApp

**WhatsApp Message:**
> "Can you review the Devonshire budget? Need it by Friday."

**Processing:**
- Saved to `!inbox/`
- AI-enhanced processor detects task
- Creates Google Task with due date

## Troubleshooting

### "No WhatsApp notification emails found"

- Check that email notifications are enabled in WhatsApp
- Verify emails are being sent to your Gmail account
- Try increasing `--days` parameter
- Check Gmail search query matches your notification format

### "Message extraction failed"

- WhatsApp email format may vary
- Check raw email body in logs
- May need to adjust extraction patterns

## Logs

- Processor output: Console output
- State tracking: `!inbox/.whatsapp-processor-state.json`

## Next Steps

1. **Enable email notifications** in WhatsApp (if not already)
2. **Test the processor:** `python3 agents/system/whatsapp-processor.py --days 30`
3. **Set up automation** (optional): Create LaunchAgent for periodic processing
4. **Messages will route** through regular inbox processor automatically

The system is ready to use! WhatsApp messages will be processed just like inbox messages, automatically allocated to clients, and tasks will be created when needed.

