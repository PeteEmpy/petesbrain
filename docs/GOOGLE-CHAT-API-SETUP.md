# Google Chat API Setup Instructions

## Step 1: Enable Google Chat API

The Google Chat API needs to be enabled in your Google Cloud project.

**Quick Enable:**
Visit: https://console.developers.google.com/apis/api/chat.googleapis.com/overview?project=257130067085

Click the **"ENABLE"** button.

**Or manually:**
1. Go to https://console.cloud.google.com/
2. Select project: **petesbrain-emailsync** (ID: 257130067085)
3. Go to **APIs & Services** > **Library**
4. Search for "Google Chat API"
5. Click on it
6. Click **"Enable"**
7. Wait 2-3 minutes for it to propagate

## Step 2: Verify Authentication

After enabling the API, test the connection:

```bash
python3 -c "from shared.google_chat_client import GoogleChatClient; client = GoogleChatClient(); spaces = client.list_spaces(); print(f'Found {len(spaces)} spaces')"
```

## Step 3: Test the Processor

Once the API is enabled, test fetching messages:

```bash
python3 agents/system/google-chat-processor.py --days 7
```

Or with AI enhancement:

```bash
python3 agents/system/ai-google-chat-processor.py --days 7
```

## Troubleshooting

If you still get errors after enabling:
- Wait a few minutes for the API to propagate
- Check that OAuth consent screen includes Chat API scopes
- Verify you have access to Google Chat spaces (they must be shared with you)

