# PetesBrain Sync V2: Quick Start Guide

**⚡ Ultra-Simple Guide - 3 Commands to Sync**

---

## Desktop → Laptop Sync (Most Common)

### On Desktop (When Done Working)

```bash
cd ~/Documents/PetesBrain.nosync
./shared/scripts/sync-petesbrain-v2.sh push
```

**What it does**: Pushes all your changes to GitHub

**Time**: 15-40 seconds

**Success**: You'll see "✓ PUSH sync completed successfully"

---

### On Laptop (Before Starting Work)

```bash
cd ~/Documents/PetesBrain
./shared/scripts/sync-petesbrain-v2.sh pull
```

**What it does**: Pulls latest changes from GitHub

**Time**: 15-40 seconds

**Success**: You'll see "✓ PULL sync completed successfully"

---

## Check What's Happening

```bash
./shared/scripts/sync-petesbrain-v2.sh status
```

**Shows**:
- Are you in sync with remote?
- Any uncommitted changes?
- Desktop or laptop machine?

---

## Emergency Rollback

**If sync went wrong** (data looks corrupted):

```bash
./shared/scripts/rollback-sync.sh
```

**Time**: <30 seconds

**What it does**: Restores everything to pre-sync state

---

## That's It! 🎉

**Three commands**:
1. `sync-petesbrain-v2.sh push` (desktop → GitHub)
2. `sync-petesbrain-v2.sh pull` (laptop ← GitHub)
3. `sync-petesbrain-v2.sh status` (check sync status)

**Bonus**: `rollback-sync.sh` (emergency undo)

---

## What Makes This Foolproof?

✅ **Checksums verify data integrity** (no silent corruption)
✅ **Automatic rollback if anything goes wrong** (<30 sec)
✅ **macOS notifications tell you immediately** (no silent failures)
✅ **Snapshot created before every sync** (instant undo)
✅ **All-or-nothing sync** (no partial states)

---

## When Things Go Wrong

### "Merge Conflict" Error

**Rare** - Means you edited same file on both machines.

**Fix**:
1. Look at the conflicted file (Git tells you which one)
2. Edit it manually to keep what you want
3. Run `git add <file>` then `git commit -m "Fixed conflict"`
4. Re-run sync

**Or**: Just use desktop version (easier):
```bash
git checkout --theirs <file>  # Keep desktop version
git add <file>
git commit -m "Resolved conflict - using desktop version"
./shared/scripts/sync-petesbrain-v2.sh push
```

### "Corruption Detected" Alert

**Automatic rollback happens** - check what went wrong:

```bash
tail -50 ~/.petesbrain-sync-v2-error.log
```

Usually a network interruption. Just re-run sync.

### Sync Takes Forever

**Normal first time** - Pushing 11GB of data takes time.

**After that**: Only changes sync (much faster).

---

## Detailed Documentation

For everything else: `docs/SYNC-SYSTEM-V2.md`

---

**Last Updated**: 2026-01-04
