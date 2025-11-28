# Staging Area

**Purpose:** Safe testing ground for external templates and experimental features before integration into production

---

## What This Folder Is For

This is your **sandbox** for:
- Testing external template features
- Experimenting with new agents
- Validating integrations before deployment
- Adapting code from other projects

**Nothing in this folder affects production agents or workflows.**

---

## Workflow

### 1. Analyze Template (Isolated)
```bash
# Use the analysis tool
/Users/administrator/Documents/PetesBrain/shared/scripts/analyze-template.sh /path/to/template

# This creates analysis in ~/Documents/TemplateAnalysis (completely isolated)
```

### 2. Copy Features to Staging
```bash
# Copy interesting components here for testing
cp ~/Documents/TemplateAnalysis/template-analysis-*/template/some-agent.py \
   staging/template-name/test-agent.py
```

### 3. Test in Isolation
```bash
cd staging/template-name
python3 test-agent.py --dry-run

# Fix issues, adapt to your environment
# Test thoroughly before moving to production
```

### 4. Move to Production
```bash
# Only after successful testing
mv staging/template-name/test-agent.py agents/appropriate-category/new-agent.py

# Update documentation
# Create LaunchAgent if needed
```

---

## Current Staging Projects

Add folders here for each template/experiment:

```
staging/
├── README.md (this file)
├── template-name-1/
│   ├── README.md (notes about this integration)
│   ├── test-agent.py
│   └── test-results.txt
└── template-name-2/
    └── ...
```

---

## Safety Rules

✅ **DO:**
- Test everything here first
- Keep organized with subfolders
- Document what you're testing
- Run backups before moving to production

❌ **DON'T:**
- Put production code here
- Run untested code in production
- Skip the analysis phase
- Forget to clean up after successful integration

---

## Cleanup

After successful integration:
```bash
# Remove staging folder
rm -rf staging/template-name/

# Or keep for reference
mv staging/template-name/ staging/archived/template-name-$(date +%Y%m%d)/
```

---

## Related Documentation

- [External Template Integration Guide](../docs/EXTERNAL-TEMPLATE-INTEGRATION.md)
- [Agents README](../agents/README.md)
- [Backup System](../docs/BACKUP-SYSTEM.md)

---

**Remember:** You have automated backups now. Experiment safely!

