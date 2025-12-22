# YouTube Monitor Agent

Automated agent that monitors YouTube channels for new e-commerce, PPC, and digital marketing video content.

## What It Does

1. **Monitors YouTube channels** - Checks configured channels for new videos (default: last 7 days)
2. **Extracts transcripts** - Uses YouTube Transcript API to get full video transcripts
3. **Scores relevance** - Uses Claude to analyse and score videos (0-10 scale)
4. **Auto-imports high-value content** - Videos scoring ≥7 automatically added to knowledge base
5. **Runs on schedule** - LaunchAgent runs daily to check for new content

## How It Works

```
┌─────────────────────┐
│  YouTube Channels   │
│  (configured list)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Fetch Recent       │
│  Videos (API)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Extract Transcript │
│  (youtube-trans-api)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Score Relevance    │
│  (Claude 3.5 Haiku) │
└──────────┬──────────┘
           │
           ▼
      Score ≥7?
           │
      ┌────┴────┐
      │   YES   │
      └────┬────┘
           │
           ▼
┌─────────────────────┐
│  Create KB Article  │
│  (formatted .md)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Save to Inbox      │
│  (KB processing)    │
└─────────────────────┘
```

## Monitored Channels

Default configuration in `youtube-monitor.py`:

```python
YOUTUBE_CHANNELS = {
    "Common Thread Collective": "UCXvVJYqEqB_qwvZoQQOgT3g",
}
```

### Adding New Channels

1. Find the channel ID:
   - Go to channel page on YouTube
   - View page source (Cmd+Option+U)
   - Search for `"channelId":`
   - Copy the ID (e.g., `UCXvVJYqEqB_qwvZoQQOgT3g`)

2. Add to `YOUTUBE_CHANNELS` dict:
   ```python
   YOUTUBE_CHANNELS = {
       "Common Thread Collective": "UCXvVJYqEqB_qwvZoQQOgT3g",
       "Solutions 8": "UCgbWR43TkOF4dCFkW9jU7jQ",
       "New Channel Name": "CHANNEL_ID_HERE",
   }
   ```

## Relevance Scoring

Videos are scored 0-10 based on:

**9-10: CRITICAL** - Must-have content
- Official Google Ads announcements
- Original research with quantified data
- Advanced strategic frameworks

**7-8: HIGH VALUE** - Strongly relevant
- Tactical Google Ads/PPC how-to guides
- E-commerce strategy with case studies
- Performance analysis methodologies

**5-6: MODERATE** - Possibly useful
- General e-commerce trends
- Adjacent topics (analytics, CRO)

**3-4: LOW** - Tangentially related
- Generic marketing advice
- Platform overviews without depth

**0-2: IRRELEVANT**
- Unrelated to e-commerce/PPC
- Personal vlogs, entertainment

**Threshold**: Videos scoring ≥7 are automatically imported

## Output Format

Videos are saved to:
```
roksys/knowledge-base/_inbox/documents/YYYY-MM-DD_category_video-title-slug.md
```

Each article includes:
- YAML frontmatter (metadata, score, tags, video ID)
- Video title, description, URL
- AI relevance assessment
- Full transcript text
- Word count, language, publish date

## Schedule

**LaunchAgent runs**: Daily at 9:00 AM
**Lookback window**: 7 days (configurable via `LOOKBACK_DAYS`)
**State tracking**: Prevents re-processing same videos

## Configuration

### Environment Variables

Required in LaunchAgent plist:
- `ANTHROPIC_API_KEY` - Claude API for relevance scoring
- `YOUTUBE_API_KEY` - YouTube Data API v3 key

### Tunable Parameters

In `youtube-monitor.py`:

```python
MIN_RELEVANCE_SCORE = 7        # Minimum score to import
LOOKBACK_DAYS = 7              # How far back to check
```

## State Management

**State file**: `data/state/youtube-monitor-state.json`

Tracks:
- `processed_videos`: List of processed video IDs (last 1000)
- `last_run`: Timestamp of last execution

Prevents duplicate processing and manages memory efficiently.

## Logs

**Log file**: `data/cache/youtube-monitor.log`

Contains:
- Timestamp of each run
- Videos found and processed
- Relevance scores and reasoning
- Videos added to knowledge base
- Errors and warnings

## Testing

### Manual test run:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor

# Create virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY='your-key'
export YOUTUBE_API_KEY='your-key'

# Run agent
./youtube-monitor.py
```

### Check logs:

```bash
tail -f /Users/administrator/Documents/PetesBrain.nosync/data/cache/youtube-monitor.log
```

### Verify output:

```bash
ls -lah /Users/administrator/Documents/PetesBrain.nosync/roksys/knowledge-base/_inbox/documents/ | grep youtube
```

## Troubleshooting

### No videos found

- Check channel ID is correct
- Verify channel has published videos in last 7 days
- Check YouTube API quota (10,000 units/day default)

### Transcript extraction fails

- Not all videos have transcripts
- Some videos disable captions
- Auto-generated transcripts preferred over manual

### Low relevance scores

- Adjust `MIN_RELEVANCE_SCORE` if too strict
- Review scoring prompt in `score_video_relevance()` function
- Check transcript preview length (currently 2000 chars)

### Agent not running

```bash
# Check if loaded
launchctl list | grep youtube-monitor

# View error log
tail -50 ~/.petesbrain-youtube-monitor-error.log

# Reload agent
launchctl unload ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor.plist
launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor.plist
```

## Dependencies

- `google-api-python-client` - YouTube Data API
- `youtube-transcript-api` - Transcript extraction
- `anthropic` - Claude API for scoring
- Python 3.12+

## Integration with Knowledge Base

Videos added to `_inbox/documents/` are automatically:
1. Indexed by knowledge base system
2. Searchable via `kb-search` skill
3. Included in weekly/monthly KB updates
4. Available for strategic analysis

## Future Enhancements

**Potential improvements**:
- Playlist monitoring (not just channel uploads)
- Multi-language transcript support
- Video thumbnail extraction
- Timestamp extraction for key moments
- Integration with Granola (if video has associated meeting)
- Notification system for high-scoring videos (9-10)

## Maintenance

**Weekly**:
- Review logs for errors
- Check state file size
- Verify videos being captured

**Monthly**:
- Review relevance scores vs. actual usefulness
- Adjust `MIN_RELEVANCE_SCORE` if needed
- Add/remove channels based on content quality

**Quarterly**:
- Audit knowledge base for duplicate content
- Update scoring criteria in prompt
- Review YouTube API quota usage
