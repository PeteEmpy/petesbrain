# Knowledge Base Inbox

**Drop Zone for Unprocessed Knowledge Materials**

## How to Use

### Simply drop files here and they'll be automatically processed every 6 hours

This inbox is monitored by an automated script that:
1. Reads each file in the inbox
2. Extracts and analyzes the content
3. Categorizes by topic (Google Ads, AI, Analytics, etc.)
4. Moves to the appropriate knowledge base folder
5. Updates the knowledge base index
6. Clears the processed file from the inbox

## What to Add

### Emails (`emails/`)
- Google Ads newsletter updates
- Partner insights from trusted sources
- Industry updates from thought leaders
- Platform announcement emails
- Case study emails

**Formats**: .eml, .msg, .md, .txt

### Documents (`documents/`)
- PDF research papers
- Industry reports
- White papers
- Article exports
- Strategic guides

**Formats**: .pdf, .docx, .txt, .md

### Videos (`videos/`)
- YouTube URLs (transcripts fetched automatically!)
- Webinar notes
- Conference talk summaries
- Video tutorial key points

**Formats**: .txt, .md

**YouTube Auto-Fetch**: Just paste the URL!
1. Copy YouTube URL: `https://www.youtube.com/watch?v=VIDEO_ID`
2. Save as `video-name.txt` in this folder
3. System automatically fetches transcript, analyzes, and organizes

**Multiple videos**: Create a queue file with multiple URLs (one per line)

## File Naming Tips

Use descriptive, dated filenames:
- `2025-10-29-google-pmax-update.pdf`
- `smart-bidding-strategies-2025.txt`
- `youtube-transcript-ai-in-google-ads.txt`

## Email Auto-Import

Configure the email sync system to automatically pull certain emails here:

```python
# In shared/email-sync/config.py or similar
KNOWLEDGE_BASE_LABELS = [
    'google-ads-updates',
    'industry-insights',
    'trusted-sources',
    'knowledge-base'
]

# Emails with these labels → saved to _inbox/emails/
```

## Manual Processing

If you want immediate processing instead of waiting for the 6-hour cycle:

```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/knowledge-base-processor.py
```

## What Happens After Processing

1. **Content extracted** and formatted as markdown
2. **File moved** to appropriate category folder
3. **Index updated** in main knowledge-base/README.md
4. **Original file** removed from inbox (content preserved in organized location)
5. **Processing log** created showing what was filed where

---

**Status**: Automated processing enabled (every 6 hours)
**Last Processing Run**: Never (system just set up)
**Next Scheduled Run**: Will start once LaunchAgent is configured
