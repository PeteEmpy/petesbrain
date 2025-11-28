# Tasks Architecture Issue - 2025-11-26

## Summary

**Issue**: Most clients are storing their general Google Ads optimization tasks in `product-feeds/tasks.json` instead of the root `clients/{client}/tasks.json` file.

**Impact**: This misplaces non-product-feed tasks in a folder intended only for feed maintenance work.

**Current State**: Only 2/19 active clients follow correct architecture (Devonshire Hotels, Smythson).

---

## Root Cause

The `generate-tasks-overview.py` script (lines 246-248) checks `product-feeds/tasks.json` FIRST as the primary location, then falls back to root `tasks.json`:

```python
# Check product-feeds location first (primary), then direct (legacy)
task_file = client_dir / 'product-feeds' / 'tasks.json'
if not task_file.exists():
    task_file = client_dir / 'tasks.json'
```

This code comment is **backwards** - it labels root as "legacy" when it should be primary.

---

## Current Client Status

| Client | Root tasks.json | product-feeds/tasks.json | Status |
|--------|----------------|--------------------------|--------|
| **Correct Architecture** ||||
| Devonshire Hotels | ✅ | ✅ | Both (correct) |
| Smythson | ✅ | ✅ | Both (correct) |
| **Incorrect Architecture** ||||
| Accessories for the Home | ❌ | ✅ | PF only (wrong) |
| Bright Minds | ❌ | ✅ | PF only (wrong) |
| Clear Prospects | ❌ | ✅ | PF only (wrong) |
| Crowd Control | ❌ | ✅ | PF only (wrong) |
| Grain Guard | ❌ | ✅ | PF only (wrong) |
| **National Motorsports Academy** | ❌ | ✅ | **PF only (wrong)** |
| Roksys | ❌ | ✅ | PF only (wrong) |
| Superspace | ❌ | ✅ | PF only (wrong) |
| Tree2MyDoor | ❌ | ✅ | PF only (wrong) |
| Uno Lighting | ❌ | ✅ | PF only (wrong) |
| **No Tasks Files** ||||
| BMPM | ❌ | ❌ | No tasks |
| Go Glean | ❌ | ❌ | No tasks |
| Godshot | ❌ | ❌ | No tasks |
| Just Bin Bags | ❌ | ❌ | No tasks |
| National Design Academy | ❌ | ❌ | No tasks |
| Positive Bakes | ❌ | ❌ | No tasks |

---

## Correct Architecture

### Root tasks.json (PRIMARY)
**Location**: `clients/{client}/tasks.json`

**Purpose**: ALL client work tasks including:
- Google Ads optimization
- Campaign reviews
- Budget adjustments
- Account audits
- Client meetings
- Strategy planning
- Performance monitoring
- ANY work related to the client account

**Example clients following this**: Devonshire Hotels, Smythson

### Product Feeds tasks.json (OPTIONAL)
**Location**: `clients/{client}/product-feeds/tasks.json`

**Purpose**: ONLY product feed maintenance tasks:
- Feed upload/sync issues
- Product data quality problems
- Merchant Centre suspensions
- Feed schema updates
- Product disapprovals

**When to have this file**: Only if client has a product feed (e.g., e-commerce clients)

**Example clients that should have this**: Smythson, Tree2MyDoor, Crowd Control (e-commerce)

**Example clients that should NOT have this**: National Motorsports Academy, National Design Academy (lead gen, no products)

---

## Why This Matters

1. **Semantic correctness**: Google Ads optimization tasks are not product feed tasks
2. **Lead gen clients**: NMA shouldn't have a product-feeds folder at all
3. **Searchability**: Looking in `/clients/nma/` for tasks should find them immediately
4. **Script logic**: The fallback comment calls root "legacy" when it should be primary
5. **Future confusion**: New agents/developers will misunderstand folder purpose

---

## Migration Plan

### Phase 1: Fix Script Logic (Immediate)
Update `generate-tasks-overview.py` lines 246-248:

**BEFORE:**
```python
# Check product-feeds location first (primary), then direct (legacy)
task_file = client_dir / 'product-feeds' / 'tasks.json'
if not task_file.exists():
    task_file = client_dir / 'tasks.json'
```

**AFTER:**
```python
# Check root location first (primary for all client work)
task_file = client_dir / 'tasks.json'
if not task_file.exists():
    # Fallback: check product-feeds (legacy misplaced location)
    task_file = client_dir / 'product-feeds' / 'tasks.json'
```

**Impact**: Script will prioritize root location, making migrations simpler

---

### Phase 2: Migrate Clients (By Priority)

#### Immediate Priority (Lead Gen Clients - Should NOT Have Product Feeds Folder)

**National Motorsports Academy**
- Move: `product-feeds/tasks.json` → `tasks.json`
- Reason: Lead generation client, no products, entire product-feeds folder is wrong

**National Design Academy** (when tasks created)
- Create: `tasks.json` in root
- Reason: Lead generation client, no products

#### High Priority (E-commerce Clients - Separate Feed vs General Tasks)

**Tree2MyDoor, Crowd Control, Uno Lighting, Accessories for the Home, Superspace**
- Create new: `clients/{client}/tasks.json`
- Review existing: `product-feeds/tasks.json`
- Migrate: General optimization tasks → root tasks.json
- Keep: Only actual feed tasks in product-feeds/tasks.json
- Reason: E-commerce clients should have both files with clear separation

#### Medium Priority (Non-E-commerce Without Products)

**Roksys, Bright Minds, Grain Guard, Clear Prospects**
- Move: `product-feeds/tasks.json` → `tasks.json`
- Remove: Empty product-feeds folder if no actual feed files
- Reason: If no products, shouldn't have product-feeds tasks

---

### Phase 3: Establish Standards

1. **New client setup**: Always create root `tasks.json`, only create `product-feeds/tasks.json` if client has products
2. **Task creation**: Default to root `tasks.json` unless explicitly feed-related
3. **Documentation**: Update client setup docs with correct structure
4. **Validation**: Add script to check for misplaced tasks

---

## Immediate Action Required

**For NMA specifically** (your original question):
1. ✅ **CONFIRMED**: NMA tasks ARE in a tasks.json file (`product-feeds/tasks.json`)
2. ❌ **PROBLEM**: They're in the wrong location (should be in root)
3. ⚠️ **BIGGER ISSUE**: 10 other clients have same architectural problem

**Recommendation**: Start with NMA migration as proof-of-concept, then batch-migrate other clients.

---

## Migration Script (For NMA)

```bash
# 1. Move tasks.json to root
mv /Users/administrator/Documents/PetesBrain/clients/national-motorsports-academy/product-feeds/tasks.json \
   /Users/administrator/Documents/PetesBrain/clients/national-motorsports-academy/tasks.json

# 2. Verify product-feeds folder is empty (except standard .gitkeep)
ls -la /Users/administrator/Documents/PetesBrain/clients/national-motorsports-academy/product-feeds/

# 3. If empty, remove folder (lead gen client shouldn't have it)
rm -rf /Users/administrator/Documents/PetesBrain/clients/national-motorsports-academy/product-feeds/

# 4. Regenerate overview to confirm
python3 /Users/administrator/Documents/PetesBrain/generate-tasks-overview.py
```

---

## Questions to Answer

1. **Do we migrate all clients at once or incrementally?**
   - Recommendation: Incremental (start with NMA, then lead gen, then e-commerce)

2. **Do we update the script first or migrate clients first?**
   - Recommendation: Script first (makes migrations easier to test)

3. **What do we do with clients that genuinely need both files?**
   - Keep both, but enforce separation: root = client work, product-feeds = feed maintenance

4. **Should we add validation to prevent future misplacement?**
   - Yes - add to task creation workflow

---

**Status**: Awaiting user decision on migration approach
