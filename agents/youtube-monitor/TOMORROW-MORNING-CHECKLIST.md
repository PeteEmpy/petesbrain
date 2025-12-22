# Tomorrow Morning Checklist - YouTube 60-Day Import

**Date Created**: 17 December 2025, 09:15 AM
**Expected Completion**: Tonight ~8:00 PM
**Check Time**: Tomorrow morning (18 December 2025)

---

## ✅ Step 1: Verify Import Completed

```bash
# Check if process finished
ps aux | grep youtube-monitor.py | grep -v grep
# Should show: NO processes running (if completed)

# Count successful imports
grep "Added to KB" ~/Documents/PetesBrain.nosync/data/cache/youtube-monitor.log | grep "2025-12-17" | wc -l
# Expected: 8-12 articles

# View completion summary
tail -20 ~/Documents/PetesBrain.nosync/data/cache/youtube-monitor.log
# Should show: "YouTube Monitor Agent - Complete"
```

---

## ✅ Step 2: Review New Articles

```bash
# List all imported articles
ls -lt ~/Documents/PetesBrain.nosync/roksys/knowledge-base/_inbox/documents/ | grep "2025-12-17"

# Count total
ls ~/Documents/PetesBrain.nosync/roksys/knowledge-base/_inbox/documents/ | grep "2025-12-17" | wc -l
```

---

## ✅ Step 3: Revert Settings (IMPORTANT!)

**Follow**: `POST-IMPORT-PLAN.md`

### 3a. Revert Lookback Period

Edit `youtube-monitor.py` line 57:
```python
# Change from:
LOOKBACK_DAYS = 60

# To:
LOOKBACK_DAYS = 7
```

### 3b. Revert Rate Limiting to 10 Minutes

Edit `youtube-monitor.py` lines 395-397:
```python
# Change from:
# Rate limiting: wait 15 minutes between videos to avoid YouTube blocks
# (Longer delay for initial 60-day historical import)
time.sleep(900)

# To:
# Rate limiting: wait 10 minutes between videos to avoid YouTube blocks
# PERMANENT - NEVER reduce below 5 minutes (YouTube will block IP)
time.sleep(600)
```

---

## ✅ Step 4: Clean Up One-Time Jobs

```bash
# Remove 4 AM one-time job
launchctl unload ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor-4am.plist
rm ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor-4am.plist
```

---

## ✅ Step 5: Re-enable Regular 9 AM Job

```bash
# Load the regular daily job
launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.youtube-monitor.plist

# Verify it's loaded
launchctl list | grep youtube-monitor
# Should show: co.roksys.petesbrain.youtube-monitor
```

---

## ✅ Step 6: VPN Status

**You can disconnect your VPN now** - daily operation doesn't need it:
- 7-day lookback = ~10 videos per day
- 10-minute delays = 100 minutes total
- Too gentle to trigger YouTube blocks
- Original IP should be clean after 24-48 hours

**Keep VPN available** for future bulk imports if needed.

---

## 📊 Expected Final Results

**60-day window** (17 Oct → 16 Dec 2025):
- Videos checked: ~46 across 5 channels
- Articles imported: 8-12 high-value (score ≥7)
- Topics: Q5 strategy, BFCM analysis, Meta optimization, forecasting
- Size: ~50KB per article (includes full transcripts)

---

## 🔄 Daily Operation Confirmed

**After these steps, normal operation resumes**:
- Runs daily at 9:00 AM
- Checks last 7 days of uploads
- 10-minute delays between videos
- ~10 videos per day (1-3 typically score ≥7)
- Processing time: ~100 minutes
- No VPN needed

---

## ⚠️ If Import Failed or Still Running

**If process is still running tomorrow morning**:
- Let it finish (might take until afternoon)
- Then follow steps above

**If import failed (no new articles)**:
- Check logs for errors
- Verify VPN was still connected
- May need to retry with different VPN server

---

**All documentation**: See `POST-IMPORT-PLAN.md` for full details
