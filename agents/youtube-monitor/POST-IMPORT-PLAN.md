# Post 60-Day Import Plan

**Date**: 16 December 2025
**Status**: 60-day historical import scheduled for 4 AM, 17 December 2025

---

## After Import Completes (Expected: 17 Dec ~3:30 PM)

### 1. Verify Import Success

```bash
# Check how many videos were successfully added
grep "Added to KB" ~/Documents/PetesBrain.nosync/data/cache/youtube-monitor.log | wc -l

# View new articles
ls -lt ~/Documents/PetesBrain.nosync/roksys/knowledge-base/_inbox/documents/ | grep "2025-12-17" | head -20

# Check processed videos count
cat ~/Documents/PetesBrain.nosync/data/state/youtube-monitor-state.json
```

Expected result: 8-12 high-value articles from 60-day window (46 videos processed)

---

### 2. Revert LOOKBACK_DAYS to 7 Days

**File**: `youtube-monitor.py` line 57

Change from:
```python
LOOKBACK_DAYS = 60
```

To:
```python
LOOKBACK_DAYS = 7
```

---

### 3. Set PERMANENT Rate Limiting to 10 Minutes

**File**: `youtube-monitor.py` line 395-397

Change from:
```python
# Rate limiting: wait 15 minutes between videos to avoid YouTube blocks
# (Longer delay for initial 60-day historical import)
time.sleep(900)
```

To:
```python
# Rate limiting: wait 10 minutes between videos to avoid YouTube blocks
# PERMANENT - NEVER reduce below 5 minutes (YouTube will block IP)
time.sleep(600)
```

**Rationale**:
- Daily operation checks 7 days of uploads
- Typical daily volume: 5-15 videos across 5 channels
- 10 minutes × 15 videos = 150 minutes (2.5 hours) - very manageable
- Eliminates risk of YouTube IP blocks
- **LESSON LEARNED 16 Dec 2025**: 3-second delays triggered immediate IP block

---

### 4. Remove One-Time 4 AM Job

```bash
launchctl unload ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor-4am.plist
rm ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor-4am.plist
```

---

### 5. Verify Regular Daily Job Still Active

```bash
launchctl list | grep youtube-monitor
# Should show: co.roksys.petesbrain.youtube-monitor (the 9 AM daily job)
```

---

## Daily Operation Configuration (Final State)

| Setting | Value | Reason |
|---------|-------|--------|
| **LOOKBACK_DAYS** | 7 | Check last week's uploads |
| **Rate Limit** | 10 minutes (600 sec) | Prevent YouTube IP blocks |
| **Schedule** | Daily at 9 AM | Normal operation |
| **MIN_RELEVANCE_SCORE** | 7 | High-value content only |
| **Channels** | 5 active | Monitored via channels.json |

---

## Expected Daily Performance

**Typical day**:
- 5-15 new videos across 5 channels (in 7-day window)
- Processing time: 50-150 minutes
- Articles added: 1-3 high-value videos (score ≥7)
- Zero risk of YouTube IP blocks

---

## Manual Run Command (If Needed)

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/youtube-monitor
export ANTHROPIC_API_KEY=$(security find-generic-password -s "ANTHROPIC_API_KEY" -w)
./venv/bin/python3 youtube-monitor.py
```

---

**IMPORTANT**: Never reduce rate limiting below 5 minutes. YouTube's transcript API is aggressive with IP blocking.
