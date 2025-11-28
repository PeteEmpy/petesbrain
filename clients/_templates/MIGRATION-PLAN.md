# Client Folder Structure Migration Plan

## Status: Ready to Roll Out

**Template Created**: ✅ `/clients/_templates/FOLDER-STRUCTURE.md`
**Pilot Complete**: ✅ Smythson (Oct 30, 2025)

---

## Rollout Phases

### ✅ Phase 1: Documentation & Pilot (COMPLETE)
- [x] Document standard folder structure
- [x] Create template in `_templates/`
- [x] Pilot with Smythson client
- [x] Validate structure works well

### 📋 Phase 2: High-Priority Clients (NEXT)

**Priority 1 - Very Messy (Urgent)**:
- [ ] **Superspace** - 30+ files in root (CSVs, JSON, Python scripts)
  - Move CSVs to `product-feeds/aus/`, `product-feeds/uk/`, `product-feeds/us/`
  - Move scripts to `scripts/`

**Priority 2 - Some Organization Needed**:
- [ ] **Tree2mydoor** - 4 analysis files in root
  - Move `click-spike-analysis-oct-2025.md` → `documents/` or `reports/ad-hoc/`
  - Move `click-spike-explanation-email.md` → `documents/`
  - Move `products-removed-2025-10-26.md` → `documents/`

### 📋 Phase 3: Standard Clients

Review and organize as needed:
- [ ] Bright Minds
- [ ] Clear Prospects
- [ ] Devonshire Hotels
- [ ] Godshot (already clean ✅)
- [ ] National Design Academy
- [ ] OTC
- [ ] Print My PDF
- [ ] Uno Lighting
- [ ] Accessories for the Home

### 📋 Phase 4: Final Steps
- [ ] Update CLAUDE.md to reference new standard
- [ ] Update automation scripts (if needed) to respect new structure
- [ ] Document any client-specific variations

---

## Migration Checklist (Per Client)

When migrating a client, follow these steps:

1. **Backup**: Ensure git commit or backup before moving files
2. **Review**: List all files in root directory
3. **Categorize**: Determine destination folder for each file
4. **Create folders**: Make any new subdirectories needed (e.g., `reports/q4-2025/`)
5. **Move files**: Use `mv` to relocate files to proper folders
6. **Verify**: Check root directory - should only have CONTEXT.md, tasks-completed.md, and optional files
7. **Test**: Verify no broken links or scripts

---

## Quick Migration Commands

### Identify Files to Move
```bash
cd /Users/administrator/Documents/PetesBrain/clients/[client-name]
ls -la | grep -v "^d" | grep -v "CONTEXT.md" | grep -v "tasks-completed.md"
```

### Create Standard Structure
```bash
mkdir -p reports/{pmax-analysis,monthly,ad-hoc} product-feeds scripts
```

### Example Moves
```bash
# Move HTML reports
mv *.html reports/ad-hoc/

# Move CSV product data
mv *-product-ids.csv product-feeds/

# Move scripts
mv *.py scripts/
mv *.sh scripts/
```

---

## Benefits Seen (Smythson Pilot)

✅ Root directory: 15 files → 2 files (87% reduction)
✅ Clear categorization: Reports vs. Product Data
✅ Easier navigation: Know where to find specific file types
✅ Chronological grouping: Q4 2025 reports together
✅ Future-proof: Clear home for new files

---

## Next Action

**Recommend**: Start with **Superspace** (most urgent) and **Tree2mydoor** (quick win)

**Command to user**: "Ready to migrate Superspace and Tree2mydoor? Say the word and I'll clean them up!"
