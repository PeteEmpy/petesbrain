# Google Chat API Configuration Required

The Google Chat API requires a Chat app to be configured, even for reading your own messages.

## Quick Setup

1. **Go to Chat API Configuration:**
   https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat?project=257130067085

2. **Click "Configuration" tab**

3. **Fill in minimal required fields:**
   - **App Name:** PetesBrain Chat Reader
   - **Avatar URL:** (can leave blank or use a simple image URL)
   - **Description:** Personal Chat message reader for PetesBrain
   - **Functionality:** Select "Receive 1:1 messages" (or whatever is available)
   - **Connection settings:** You can use a placeholder URL like `https://example.com` since we're only reading, not receiving webhooks

4. **Save the configuration**

5. **Wait 2-3 minutes for it to propagate**

## Alternative: Use Gmail API for Chat Notifications

If configuring a Chat app is too complex, we can process Google Chat messages through Gmail API by reading Chat notification emails. This would require:
- Gmail API access (already have)
- Processing emails from `chat-noreply@google.com`
- Extracting Chat message content from email bodies

Would you like me to implement the Gmail-based approach instead?

