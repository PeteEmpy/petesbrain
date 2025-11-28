---
name: experiment-review
description: Reviews experiments from ROK experiments CSV and migrates completed ones to client CONTEXT.md files. Use when user says "review experiments", "experiment review", "check experiments", or on Friday for weekly experiment outcomes review.
allowed-tools: Bash, Read, Edit
---

# Experiment Review Skill

---

## What This Skill Does

Reviews experiments from `roksys/spreadsheets/rok-experiments-client-notes.csv` that are:
- Older than 14 days
- Not yet reviewed
- Within the last 60 days

For each experiment, prompts the user to categorize:
1. **Still monitoring** - Check again next week
2. **Successful** - Add to CONTEXT.md Successful Tests table
3. **Failed** - Add to CONTEXT.md Failed Tests table
4. **Inconclusive** - Archive with notes
5. **Skip** - Mark reviewed but don't add to CONTEXT.md

Automatically updates the relevant client CONTEXT.md file with outcomes.

---

## Instructions

**Simply run the script:**

```bash
/usr/local/bin/python3 shared/scripts/weekly-experiment-review.py
```

The script is **interactive** and will:
1. Show summary of experiments to review
2. Prompt for each experiment one by one
3. Ask follow-up questions based on outcome
4. Update CONTEXT.md files automatically
5. Track progress so you don't see the same experiment twice

---

## Example Session

```
================================================================================
WEEKLY EXPERIMENT REVIEW
================================================================================

📊 24 experiment(s) ready for review

Clients with experiments to review: Uno Lighting, Bright Minds, Smythson...

Press Enter to start review...

================================================================================
CLIENT: Uno Lighting
DATE: 15/10/2025 08:47 (27 days ago)
EXPERIMENT:
  Decrease the target ROAS by 10% on main PMax campaigns
================================================================================

What happened with this experiment?

  1. Still monitoring (check again next week)
  2. Successful (add to CONTEXT.md Successful Tests)
  3. Failed (add to CONTEXT.md Failed Tests)
  4. Inconclusive (archive, note in CONTEXT.md)
  5. Skip (mark as reviewed, don't add to CONTEXT.md)

Enter choice (1-5) or 'q' to quit: 2

What was the RESULT? (e.g., '+22% revenue', 'Improved CTR by 15%')
> Increased impressions by 15% while maintaining ROAS above 200%

What ACTION was taken? (e.g., 'Monitoring for optimization', 'Rolled out to other campaigns')
> Monitoring performance, may reduce further if continues to perform

✅ Added successful experiment to Uno Lighting CONTEXT.md
```

---

## State Management

**Tracks reviewed experiments** in `shared/data/experiment-review-state.json` so you won't be prompted about the same experiment multiple times.

**To reset and review all again** (rare):
```bash
rm shared/data/experiment-review-state.json
```

---

## Configuration

Edit thresholds in `shared/scripts/weekly-experiment-review.py`:

```python
MIN_DAYS_BEFORE_REVIEW = 14  # Review experiments older than 14 days
REVIEW_LOOKBACK_DAYS = 60     # Look at experiments from last 60 days
```

---

## Automation

**Runs automatically** every Friday at 9:30 AM via LaunchAgent.

**To disable automatic run**:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.experiment-review.plist
```

**To re-enable**:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.experiment-review.plist
```

---

## Troubleshooting

**Issue: "No experiments found"**
- Check that `roksys/spreadsheets/rok-experiments-client-notes.csv` exists
- Verify Google Sheets export is running (every 6 hours)

**Issue: "Client folder not found"**
- Ensure client name in CSV matches folder name in `clients/`
- Client folders should be lowercase with hyphens (e.g., `uno-lighting`)

**Issue: "CONTEXT.md table not found"**
- Check that client CONTEXT.md has the standard tables:
  - `### Successful Tests & Experiments`
  - `### Failed Tests (Learn From)`

---

## Related Files

- **Script**: `shared/scripts/weekly-experiment-review.py`
- **CSV**: `roksys/spreadsheets/rok-experiments-client-notes.csv`
- **State**: `shared/data/experiment-review-state.json`
- **Logs**: `shared/data/experiment-review.log`
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.experiment-review.plist`
