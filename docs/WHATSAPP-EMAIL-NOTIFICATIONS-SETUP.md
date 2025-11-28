# WhatsApp Email Notifications Setup

**Status:** Agent configured and running
**Agent:** `com.petesbrain.whatsapp-processor`
**Schedule:** Every 30 minutes
**Log:** `~/.petesbrain-whatsapp.log`

---

## Important Note

WhatsApp's email notification feature availability varies:
- **WhatsApp Business** may have email integration features
- **Regular WhatsApp** has limited/no email notifications in recent versions
- WhatsApp Web/Desktop notifications go to your device, not email

## Alternative Approach: WhatsApp Business API

If standard email notifications aren't available, you have two options:

### Option 1: Forward WhatsApp Messages Manually
When you receive important client messages:
1. Forward the message to your email (petere@roksys.co.uk)
2. Use subject line: "WhatsApp: [Client Name]"
3. The processor will detect these forwarded messages

### Option 2: WhatsApp Business API (Complex Setup)
- Requires Meta Business verification
- Paid service
- Would need separate `whatsapp_business_client.py` implementation
- Code structure already supports this (see line 29-33 of whatsapp-processor.py)

---

## Current Implementation

The processor searches Gmail for:
```python
query = 'from:noreply@whatsapp.com OR from:whatsapp.com OR subject:"WhatsApp"'
```

This will catch:
- Official WhatsApp notification emails (if enabled)
- Manually forwarded messages with "WhatsApp" in subject
- Any emails from whatsapp.com domain

---

## Testing Current Setup

### 1. Check if WhatsApp sends emails to your Gmail:
```bash
# Search your Gmail for WhatsApp emails
python3 -c "
from shared.whatsapp_via_email_client import WhatsAppViaEmailClient
client = WhatsAppViaEmailClient()
emails = client.get_whatsapp_notification_emails(days_back=30)
print(f'Found {len(emails)} WhatsApp-related emails in last 30 days')
"
```

### 2. Monitor processor logs:
```bash
tail -f ~/.petesbrain-whatsapp.log
```

### 3. Test with manual forward:
1. Forward a WhatsApp message to petere@roksys.co.uk
2. Put "WhatsApp: [Client Name]" in subject
3. Within 30 minutes, check if processor picks it up

---

## What Gets Processed

When the processor finds WhatsApp messages, it:
1. **Extracts:** Sender name, phone number, message text
2. **AI Analysis (Haiku):** Determines if client-related, extracts tasks
3. **Routes to:** `!inbox/` for ai-inbox-processor
4. **Final destination:** Client folders or Google Tasks

---

## Cost Impact

- **Gmail API:** Free (covered by Google OAuth)
- **Anthropic API:** Only when messages found
  - Haiku for extraction: ~$0.0001 per message
  - Minimal cost for typical usage

---

## Status Check Commands

```bash
# Check if agent is running
launchctl list | grep whatsapp

# View recent logs
tail -50 ~/.petesbrain-whatsapp.log

# Test processor manually
python3 agents/whatsapp-processor/whatsapp-processor.py --days 7
```

---

**Recommendation:** Start with manual forwarding approach to test the workflow. If it proves valuable and you process many WhatsApp messages daily, consider WhatsApp Business API setup.
