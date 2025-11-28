# WhatsApp Processing System Setup Guide

**Status:** ⚠️ Requires Setup  
**Last Updated:** 2025-11-09

## Overview

WhatsApp processing can be implemented using the **WhatsApp Business API**, which is the official way to programmatically access WhatsApp messages. However, it requires business setup with Meta/Facebook.

## Options

### Option 1: WhatsApp Business API (Recommended for Business Use)

**Pros:**
- Official API from Meta
- Reliable and supported
- Real-time webhook delivery
- Suitable for business communications

**Cons:**
- Requires Meta Developer Account
- Requires WhatsApp Business App setup
- Requires business verification
- May have costs for high volume

**Setup Steps:**

1. **Create Meta Developer Account**
   - Go to https://developers.facebook.com
   - Create a developer account

2. **Create WhatsApp Business App**
   - In Developer Dashboard, create new app
   - Add "WhatsApp" product
   - Follow setup wizard

3. **Get API Credentials**
   - Access Token (temporary, then permanent)
   - Phone Number ID
   - Business Account ID

4. **Set Up Webhook**
   - Configure webhook URL
   - Verify webhook token
   - Subscribe to message events

5. **Configure Environment Variables**
   ```bash
   export WHATSAPP_ACCESS_TOKEN="your_access_token"
   export WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id"
   export WHATSAPP_VERIFY_TOKEN="your_verify_token"
   ```

### Option 2: Email Notifications (Simple Alternative)

If you enable email notifications in WhatsApp, you can process them via Gmail API (similar to Google Chat approach).

**Setup:**
1. Enable email notifications in WhatsApp settings
2. Use Gmail API to fetch WhatsApp notification emails
3. Extract message content from emails
4. Process similar to Google Chat messages

### Option 3: Manual Forwarding (Simplest)

Forward important WhatsApp messages to a dedicated email address, then process via email sync.

## Implementation Status

✅ **Created:**
- `shared/whatsapp_business_client.py` - WhatsApp Business API client
- `agents/system/whatsapp-processor.py` - Message processor
- Webhook handler for real-time processing

⚠️ **Requires:**
- WhatsApp Business API setup
- Webhook endpoint configuration
- Environment variables configuration

## Webhook Setup

Once you have WhatsApp Business API credentials, set up a webhook endpoint:

```python
# Example Flask webhook endpoint
from flask import Flask, request, jsonify
from agents.system.whatsapp_processor import process_whatsapp_message
from shared.whatsapp_business_client import WhatsAppBusinessClient

app = Flask(__name__)

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        client = WhatsAppBusinessClient()
        challenge = client.verify_webhook(
            request.args.get('hub.mode'),
            request.args.get('hub.verify_token'),
            request.args.get('hub.challenge')
        )
        return challenge or 'Verification failed', 403
    
    # Process incoming message
    webhook_data = request.json
    client = WhatsAppBusinessClient()
    message_data = client.process_webhook(webhook_data)
    
    if message_data:
        process_whatsapp_message(message_data)
        return jsonify({'status': 'ok'}), 200
    
    return jsonify({'status': 'no message'}), 200
```

## Testing

Once set up, test with:

```bash
# Process a test message
python3 agents/system/whatsapp-processor.py --file test_message.json

# Or process webhook data
echo '{"entry":[...]}' | python3 agents/system/whatsapp-processor.py --webhook
```

## Alternative: Email-Based Approach

If WhatsApp Business API is too complex, we can implement an email-based approach similar to Google Chat:

1. Enable WhatsApp email notifications
2. Process emails from WhatsApp via Gmail API
3. Extract message content
4. Route to inbox system

Would you like me to implement the email-based approach instead?

