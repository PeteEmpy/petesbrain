# Knowledge Base Quick Start Guide

Get started with the automated knowledge base system in 3 easy steps.

## 🚀 Initial Setup (One-Time)

### 1. Run the setup script

```bash
cd /Users/administrator/Documents/PetesBrain/roksys/knowledge-base
./setup-automation.sh
```

This will:
- Configure your ANTHROPIC_API_KEY
- Load the LaunchAgent for automatic processing
- Set up 6-hour automation

### 2. Verify it's running

```bash
launchctl list | grep knowledge-base
```

You should see: `com.petesbrain.knowledge-base`

### 3. Check logs

```bash
tail -f ~/.petesbrain-knowledge-base.log
```

## 📥 Daily Usage

### Just Drop Files Into the Inbox!

The inbox is located at:
```
/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/_inbox/
```

**Three folders:**
- `_inbox/emails/` - Email exports (.md, .eml, .txt)
- `_inbox/documents/` - PDFs, articles, docs
- `_inbox/videos/` - Video transcripts, notes

### What Happens Next?

Every 6 hours, the system automatically:
1. ✅ Reads each file in the inbox
2. 🤖 Analyzes content with Claude API
3. 📂 Categorizes by topic (Google Ads, AI, Analytics, etc.)
4. 📝 Creates formatted markdown document
5. 🗂️ Moves to appropriate category folder
6. 🧹 Clears the inbox

## 💡 Quick Examples

### Example 1: Adding a Google Ads Article

1. Save article as text or copy URL into a .txt file
2. Drop into `_inbox/documents/google-ads-pmax-update.txt`
3. Wait for next processing cycle (or run manually)
4. File appears in `google-ads/performance-max/` folder

### Example 2: Adding a YouTube Video

**Super Easy**: Just paste the URL!

1. Copy the YouTube URL (e.g., `https://www.youtube.com/watch?v=kFpLzCVLA20`)
2. Save as `_inbox/videos/video-name.txt` with just the URL inside
3. The system automatically:
   - Fetches the full transcript from YouTube
   - Analyzes the content
   - Categorizes and organizes it

**Or even simpler**: Create a "queue" file with multiple URLs:
```
_inbox/videos/youtube-queue.txt

https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
https://www.youtube.com/watch?v=video3
```

All videos will be processed automatically!

### Example 3: Adding an Email

**Option A - Manual:**
1. Copy email content
2. Save as `_inbox/emails/2025-10-29-google-update.md`
3. Let it process

**Option B - Automatic:**
1. Set up email auto-export (see EMAIL-INTEGRATION.md)
2. Emails with `knowledge-base/*` labels auto-export to inbox
3. Fully automated!

## ⚡ Manual Processing (Don't Wait 6 Hours)

Want to process inbox immediately?

```bash
cd /Users/administrator/Documents/PetesBrain
shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-processor.py
```

## 📊 Checking What's in the Knowledge Base

View the index:
```bash
cat /Users/administrator/Documents/PetesBrain/roksys/knowledge-base/README.md
```

Browse by category:
```bash
ls -la /Users/administrator/Documents/PetesBrain/roksys/knowledge-base/google-ads/
```

## 🔧 Troubleshooting

### Processing isn't working

Check the logs:
```bash
tail -50 ~/.petesbrain-knowledge-base.log
```

### API key issues

Make sure ANTHROPIC_API_KEY is set:
```bash
echo $ANTHROPIC_API_KEY
```

If empty, add to `~/.bashrc` or `~/.zshrc`:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Then reload and re-run setup:
```bash
source ~/.bashrc  # or ~/.zshrc
./setup-automation.sh
```

### Files not being processed

1. Check file permissions (should be readable)
2. Verify files are in correct inbox subfolder
3. Check logs for errors
4. Try manual processing to see error messages

### Want to stop automation

```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist
```

### Want to restart automation

```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.knowledge-base.plist
```

## 📚 Knowledge Base Categories

Your files will be organized into:

- **google-ads/**
  - `performance-max/` - PMax campaigns, strategies
  - `shopping/` - Shopping feeds, merchant center
  - `search/` - Search campaigns, keywords
  - `platform-updates/` - Official Google updates
  - `bidding-automation/` - Smart Bidding, tROAS

- **ai-strategy/** - AI in marketing and ads
- **analytics/** - GA4, tracking, attribution
- **industry-insights/** - Market trends, research
- **rok-methodologies/** - ROK's internal processes

## 🎯 How Claude Code Uses This

When you ask Claude Code about:
- "What's the latest on Performance Max?"
- "Best practices for Smart Bidding?"
- "How should we approach this client's campaign?"

Claude Code will:
1. Check the relevant knowledge base folder
2. Reference specific documents
3. Provide advice based on up-to-date, curated information
4. Cite sources from the knowledge base

**This ensures strategic recommendations are always grounded in current best practices, not generic advice.**

## 🔄 Maintenance

### Weekly
- Review the knowledge base index
- Check for duplicate content
- Verify files are well-organized

### Monthly
- Update email auto-label rules if new sources emerge
- Review and archive outdated information
- Check logs for any persistent errors

### As Needed
- Add new trusted email sources to auto-label config
- Update categories if new topic areas emerge
- Adjust processing frequency if needed

---

**You're all set!** Just drop files into the inbox and let the system organize your knowledge base automatically.

For advanced setup (email integration), see: `EMAIL-INTEGRATION.md`
