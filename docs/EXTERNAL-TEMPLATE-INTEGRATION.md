# External Template Integration Guide

**Created:** November 5, 2025  
**Purpose:** Safely analyze and integrate structures/agents from external brain-type projects

---

## Safe Integration Workflow

### Phase 1: Isolation & Analysis (Zero Risk)

#### Step 1: Create Analysis Workspace
```bash
# Create temporary analysis folder OUTSIDE PetesBrain
mkdir -p ~/Documents/TemplateAnalysis
cd ~/Documents/TemplateAnalysis
```

This keeps the external template completely isolated from your working project.

#### Step 2: Import Template
```bash
# Option A: If it's a git repo
git clone <template-repo-url> external-template

# Option B: If it's a zip/download
unzip template.zip -d external-template

# Option C: If it's a folder
cp -r /path/to/template external-template
```

#### Step 3: Document Template Structure
```bash
# Generate structure overview
tree -L 3 external-template > template-structure.txt

# Find all agents/automation scripts
find external-template -name "*.py" -o -name "*.sh" | grep -i "agent\|auto\|daemon\|cron" > template-agents.txt

# Find all LaunchAgents/cron jobs
find external-template -name "*.plist" -o -name "crontab*" > template-schedulers.txt

# Find configuration files
find external-template -name "*.json" -o -name "*.yaml" -o -name "*.toml" -o -name "config*" > template-configs.txt
```

### Phase 2: Analysis & Comparison (Zero Risk)

#### Step 4: Create Comparison Report
Create a detailed analysis document comparing template vs your current setup:

```bash
# Create analysis document
cat > integration-analysis.md << 'EOF'
# Template Integration Analysis

## Template Overview
- **Source:** [Template name/URL]
- **Purpose:** [What it does]
- **Key Features:** [List main features]

## Structural Comparison

### Agents/Automation
- **Their approach:**
- **Our current approach:**
- **Potential conflicts:**
- **Integration opportunities:**

### Folder Structure
- **Their structure:**
- **Our structure:**
- **Differences:**
- **Recommendations:**

### Features We Don't Have
1. Feature A - [Description] - Priority: High/Medium/Low
2. Feature B - [Description] - Priority: High/Medium/Low

### Features We Have That They Don't
1. Feature X - [Description]

### Integration Strategy
- **Keep as-is:** [What not to change]
- **Adapt and merge:** [What to modify]
- **New additions:** [What to add fresh]
- **Skip:** [What not to use]

## Action Plan
1. [ ] Item 1
2. [ ] Item 2
EOF
```

#### Step 5: AI-Assisted Analysis
Use Claude to analyze the template:

```bash
# Generate file summaries
for file in external-template/**/*.py; do
    echo "=== $file ===" >> code-analysis.txt
    head -50 "$file" >> code-analysis.txt
done
```

Then ask Claude:
> "I have a template project with these structures [paste structure]. Compare it to my current PetesBrain setup and identify:
> 1. Novel patterns/approaches I should consider
> 2. Potential conflicts with existing setup
> 3. Features worth integrating
> 4. Safe integration strategy"

### Phase 3: Selective Integration (Controlled Risk)

#### Step 6: Create Integration Branch (Safety Net)
```bash
cd ~/Documents/PetesBrain

# Backup first (automatic with your new system!)
backup-petesbrain

# Optional: Create git branch if using version control
git checkout -b integrate-template-$(date +%Y%m%d)
```

#### Step 7: Staged Integration
Integrate ONE component at a time:

**Method A: Copy to Staging Area**
```bash
# Create staging area in your project
mkdir -p ~/Documents/PetesBrain/staging/template-integration
cd ~/Documents/TemplateAnalysis/external-template

# Copy specific items you want to integrate
cp path/to/interesting-agent.py ~/Documents/PetesBrain/staging/template-integration/
cp path/to/useful-config.json ~/Documents/PetesBrain/staging/template-integration/
```

**Method B: Create New Agents in Parallel**
```bash
# Don't overwrite - create NEW agents inspired by template
cd ~/Documents/PetesBrain/agents

# Example: Template has a "sentiment-analyzer" agent
# Create your own version inspired by it
touch agents/content-sync/sentiment-analyzer.py
# Implement based on template concepts, adapted to your needs
```

#### Step 8: Test in Isolation
```bash
# Test new agent independently before connecting it
cd ~/Documents/PetesBrain/staging/template-integration
python3 interesting-agent.py --dry-run

# Only move to /agents when confirmed working
```

### Phase 4: Integration & Validation (Managed Risk)

#### Step 9: Gradual Integration
```bash
# Move tested component to proper location
mv staging/template-integration/interesting-agent.py agents/content-sync/new-agent.py

# Create LaunchAgent if needed
cp ~/Library/LaunchAgents/com.petesbrain.template.plist \
   ~/Library/LaunchAgents/com.petesbrain.new-agent.plist

# Edit and load
launchctl load ~/Library/LaunchAgents/com.petesbrain.new-agent.plist
```

#### Step 10: Monitor & Validate
```bash
# Check it's running
launchctl list | grep new-agent

# Monitor logs
tail -f ~/.petesbrain-new-agent.log

# Verify no conflicts with existing agents
python3 agents/system/health-check.py
```

---

## Safety Checklist

Before integrating ANY component:

- [ ] Current project backed up (`backup-petesbrain`)
- [ ] Template analyzed in isolation (~/Documents/TemplateAnalysis)
- [ ] Integration plan documented
- [ ] No file path conflicts identified
- [ ] No naming conflicts with existing agents
- [ ] Dependencies documented and available
- [ ] Testing completed in staging area
- [ ] Rollback plan ready

---

## Conflict Resolution

### Common Conflicts & Solutions

**1. Same filename/agent name**
- ✅ Rename template version: `their-agent.py` → `enhanced-their-agent.py`
- ✅ Merge functionality into existing agent
- ❌ Don't overwrite existing files

**2. Different folder structure**
- ✅ Adapt to your structure: Map their folders to your `/agents` categories
- ✅ Document mapping in integration-analysis.md
- ❌ Don't restructure your entire project to match template

**3. Conflicting LaunchAgent schedules**
- ✅ Adjust schedules to avoid overlap
- ✅ Check existing schedules: `grep -r "StartCalendarInterval" ~/Library/LaunchAgents/com.petesbrain.*`
- ❌ Don't run heavy operations simultaneously

**4. Dependency conflicts**
- ✅ Use virtual environments: Create template-specific venv
- ✅ Document version requirements
- ✅ Test compatibility before committing

**5. Configuration conflicts**
- ✅ Namespace configs: `template-config.json` vs `petesbrain-config.json`
- ✅ Merge compatible settings
- ✅ Keep separate config files initially

---

## Integration Patterns

### Pattern 1: Inspired Addition
**Use when:** Template has a completely new capability you want

**Process:**
1. Analyze template implementation
2. Design your own version adapted to PetesBrain
3. Build fresh in `/agents` or `/tools`
4. Test independently
5. Document in `agents/README.md`

**Example:** Template has Twitter monitoring → Build your own social-media-monitor.py

### Pattern 2: Feature Enhancement
**Use when:** Template improves something you already have

**Process:**
1. Identify existing component to enhance
2. Extract relevant code from template
3. Add to staging for testing
4. Merge into existing file with clear comments
5. Test thoroughly
6. Keep backup of original

**Example:** Template has better error handling → Enhance your existing agents

### Pattern 3: Parallel Implementation
**Use when:** Template approach conflicts with yours but both are valuable

**Process:**
1. Keep both implementations
2. Rename template version distinctly
3. Test both approaches
4. Compare results over time
5. Eventually deprecate one

**Example:** Two different backup strategies → Run both, compare, pick winner

### Pattern 4: Configuration Adoption
**Use when:** Template has useful configs/patterns

**Process:**
1. Copy config to staging
2. Adapt values to your environment
3. Test with one agent
4. Gradually roll out to others

**Example:** Better logging configuration → Apply to all agents

---

## Rollback Procedures

### If Something Goes Wrong

**Immediate rollback:**
```bash
# Stop problematic agent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.new-agent.plist

# Remove integrated files
rm agents/category/new-agent.py

# Restore from backup if needed
cd /Users/administrator/Documents
tar -xzf PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz --strip-components=1 -C PetesBrain/
```

**Selective rollback:**
```bash
# Restore just one file from backup
tar -xzf PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz \
    PetesBrain/path/to/specific/file.py \
    --strip-components=1
```

---

## Documentation Requirements

After ANY integration, update:

1. **agents/README.md** - Add new agents to appropriate section
2. **docs/AUTOMATION.md** - Document new workflows
3. **Create integration doc:** `docs/TEMPLATE-INTEGRATION-[NAME]-[DATE].md`
4. **Update main README.md** if adding major features

---

## Example Integration Session

Here's how I'd help you integrate a template:

```
1. You provide template location/files
2. I analyze in TemplateAnalysis folder (isolated)
3. I create comparison report showing:
   - What's new/different
   - What conflicts exist
   - What's worth integrating
4. We discuss priorities
5. I create integration plan
6. I implement ONE component at a time
7. Test, validate, document
8. Move to next component
9. Final documentation update
```

---

## Ready to Analyze a Template?

**Provide me with:**
1. Template location (path, URL, or files)
2. What specifically interested you about it
3. Your priority features to consider
4. Your risk tolerance (conservative/moderate/aggressive)

I'll analyze it safely in isolation and create an integration plan!

---

## Quick Command Reference

```bash
# Before starting
backup-petesbrain

# Create analysis workspace
mkdir -p ~/Documents/TemplateAnalysis && cd ~/Documents/TemplateAnalysis

# Analyze template structure
tree -L 3 template/ > structure.txt
find template -type f -name "*.py" | head -20 > python-files.txt

# Create staging in your project
mkdir -p ~/Documents/PetesBrain/staging/template-name

# After successful integration
backup-petesbrain
rm -rf ~/Documents/TemplateAnalysis  # Clean up
```

---

**Remember:** We have excellent backups now. You can experiment safely!

