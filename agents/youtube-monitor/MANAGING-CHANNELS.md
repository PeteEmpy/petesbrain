# Managing YouTube Channels

## 🎯 Quick Reference

**Add a channel** (interactive):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor
./add-channel.py
```

**List monitored channels**:
```bash
./add-channel.py list
```

**Search for a channel**:
```bash
./add-channel.py search "Solutions 8"
```

**Add channel directly** (if you know the ID):
```bash
./add-channel.py add "Solutions 8" "UCgbWR43TkOF4dCFkW9jU7jQ" "Google Ads" "Technical strategy"
```

---

## 📋 Current Configuration

Channels are stored in: `agents/youtube-monitor/channels.json`

**Structure**:
```json
{
  "channels": [
    {
      "name": "Common Thread Collective",
      "channel_id": "UCjtbFqsqVORPBJMein0zLWQ",
      "added_date": "2025-12-16",
      "category": "E-commerce Strategy",
      "notes": "Primary e-commerce/DTC strategy channel"
    }
  ],
  "suggested_channels": [
    {
      "name": "Solutions 8",
      "channel_id": "UCgbWR43TkOF4dCFkW9jU7jQ",
      "category": "Google Ads",
      "notes": "Google Ads optimization and strategy"
    }
  ]
}
```

---

## 🔍 Finding Channel IDs

### Method 1: Use the add-channel script (Easiest)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor
./add-channel.py
```

Enter the channel name, select from search results, and it's added automatically.

### Method 2: Manual search

```bash
./add-channel.py search "channel name"
```

This will show channel IDs without adding them.

### Method 3: From YouTube page source

1. Go to the channel's YouTube page
2. View page source (Cmd+Option+U on Mac)
3. Search for `"channelId":`
4. Copy the ID (format: `UCxxxxxxxxxxxxxxxxxx`)

---

## ➕ Adding Channels

### Interactive Mode (Recommended)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor
./add-channel.py
```

**Workflow**:
1. Enter channel name (e.g., "Solutions 8")
2. See search results
3. Select the correct channel
4. Enter category (e.g., "Google Ads")
5. Optional: Add notes
6. Done! Channel added

**Example**:
```
🔍 YouTube Channel Search
============================================================

Enter channel name to search: Solutions 8

Searching for 'Solutions 8'...

Found 3 channels:

1. Solutions 8
   ID: UCgbWR43TkOF4dCFkW9jU7jQ
   Google Ads strategies and optimization...

2. Solutions 8 - Live
   ID: UCabc123...
   Live streams from Solutions 8

Select channel (1-3) or 0 to cancel: 1

Category (e.g., Google Ads, E-commerce, Analytics): Google Ads
Notes (optional): Technical deep dives

✅ Added channel: Solutions 8
   Channel ID: UCgbWR43TkOF4dCFkW9jU7jQ
   Category: Google Ads

✅ Channel added successfully!
Next run of youtube-monitor will include this channel.
```

### Direct Add (If you know the ID)

```bash
./add-channel.py add "Channel Name" "CHANNEL_ID" "Category" "Optional notes"
```

**Example**:
```bash
./add-channel.py add "Solutions 8" "UCgbWR43TkOF4dCFkW9jU7jQ" "Google Ads" "Technical strategy"
```

---

## 📝 Editing Channels Manually

You can also edit `channels.json` directly:

```bash
nano /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor/channels.json
```

**To add a channel**, add to the `channels` array:

```json
{
  "channels": [
    {
      "name": "Your Channel Name",
      "channel_id": "UCyourChannelIdHere",
      "added_date": "2025-12-16",
      "category": "Category",
      "notes": "Optional notes"
    }
  ]
}
```

**No restart needed** - Changes take effect on next scheduled run (9 AM daily).

---

## 🗑️ Removing Channels

Edit `channels.json` and remove the channel object from the `channels` array:

```bash
nano /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor/channels.json
```

Or use a script:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor

# Remove channel by name
python3 << 'EOF'
import json
from pathlib import Path

channels_file = Path("channels.json")
config = json.load(open(channels_file))

# Remove by name
channel_to_remove = "Channel Name Here"
config['channels'] = [ch for ch in config['channels'] if ch['name'] != channel_to_remove]

with open(channels_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ Removed: {channel_to_remove}")
EOF
```

---

## 💡 Suggested Channels

The `channels.json` file includes a `suggested_channels` section with channels you might want to monitor.

**To activate a suggested channel**:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor

# This will move it from "suggested" to "channels"
./add-channel.py add "Solutions 8" "UCgbWR43TkOF4dCFkW9jU7jQ" "Google Ads"
```

**Current suggestions**:
- **Solutions 8** - Google Ads optimization and strategy
- **MeasurementMarketing.io** - GA4, tracking, and measurement
- **Tier11** - Google Ads technical deep dives

---

## 🔄 Changes Take Effect Immediately

**No restart needed!**

The youtube-monitor agent reads `channels.json` fresh on each run. Changes are effective on the next scheduled run (9 AM daily) or if you trigger manually:

```bash
launchctl start co.roksys.petesbrain.youtube-monitor
```

---

## 📊 Recommended Channels

### Google Ads & PPC
- **Solutions 8** - UCgbWR43TkOF4dCFkW9jU7jQ (Advanced Google Ads)
- **Tier11** - UCFCwxxZwECerfhIgbq0xQ4w (Technical deep dives)
- **Kirk Williams** - Search for "ZATO Marketing"

### E-commerce Strategy
- **Common Thread Collective** - UCjtbFqsqVORPBJMein0zLWQ ✅ (Already added)
- **Ezra Firestone** - Search for "Smart Marketer"

### Analytics & Measurement
- **MeasurementMarketing.io** - UCjD8ZUO0UmNUYGP6vPZ5bQQ
- **Simo Ahava** - Search for "Simo Ahava"

### Meta/Facebook Ads
- **Ben Heath** - Search for "Ben Heath"
- **Charley T** - Search for "Charley T"

---

## 🧪 Testing After Adding

After adding a channel, test if it's working:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor

# Trigger manual run
source .env
./youtube-monitor.py

# Check logs
tail -50 ../../data/cache/youtube-monitor.log
```

Look for:
```
Checking channel: [New Channel Name]
Found X recent videos
```

---

## 📈 Monitoring Performance

**Check which channels are providing value**:

```bash
# Count articles by channel
cd /Users/administrator/Documents/PetesBrain.nosync/roksys/knowledge-base/_inbox/documents

grep -h "^author:" *.md | sort | uniq -c | sort -rn
```

**Example output**:
```
   15 author: Common Thread Collective
    8 author: Solutions 8
    3 author: MeasurementMarketing.io
```

This shows which channels are producing the most relevant content (scoring ≥7).

---

## ⚠️ Important Notes

1. **API Quota** - YouTube Data API has 10,000 units/day quota
   - Each channel check = ~1 unit
   - 20 channels = ~20 units/day
   - You can monitor ~500 channels before hitting quota

2. **Relevance Threshold** - Videos must score ≥7 to be imported
   - Adjust in `youtube-monitor.py` if needed
   - Lower threshold = more videos imported

3. **Transcript Availability** - Not all videos have transcripts
   - Auto-generated transcripts preferred
   - Videos without transcripts are skipped

4. **Schedule** - Agent runs daily at 9 AM
   - Checks last 7 days of uploads
   - Processes only new videos (state tracking)

5. **Rate Limiting** - 10-minute delays between videos (PERMANENT)
   - Prevents YouTube IP blocks (learned 16 Dec 2025)
   - Daily operation typically processes 5-15 videos (50-150 minutes total)
   - NEVER reduce below 5 minutes - YouTube will block the IP
   - Configured in `youtube-monitor.py` line 397: `time.sleep(600)`

---

## 🆘 Troubleshooting

**Channel not being monitored**:
1. Check `channels.json` - is it in the `channels` array (not `suggested_channels`)?
2. Check channel ID is correct
3. Manually trigger: `launchctl start co.roksys.petesbrain.youtube-monitor`
4. Check logs: `tail -50 ~/.petesbrain-youtube-monitor.log`

**No videos found**:
- Channel may not have published videos in last 7 days
- Increase `LOOKBACK_DAYS` in `youtube-monitor.py` if needed

**Script not working**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor
source venv/bin/activate
python3 add-channel.py list
```

If you see errors, the virtual environment may need reinstalling:
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

---

**Questions?** See `agent.md` or `DEPLOYMENT-GUIDE.md` for full documentation.
