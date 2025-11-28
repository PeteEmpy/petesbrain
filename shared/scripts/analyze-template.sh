#!/bin/bash
#
# Template Analysis Helper Script
# Safely analyze external templates before integration
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ANALYSIS_DIR="$HOME/Documents/TemplateAnalysis"
TEMPLATE_PATH="$1"

if [ -z "$TEMPLATE_PATH" ]; then
    echo -e "${RED}Usage: $0 <path-to-template>${NC}"
    echo ""
    echo "Example:"
    echo "  $0 /path/to/downloaded/template"
    echo "  $0 ~/Downloads/brain-template"
    exit 1
fi

if [ ! -d "$TEMPLATE_PATH" ] && [ ! -f "$TEMPLATE_PATH" ]; then
    echo -e "${RED}Error: Template path not found: $TEMPLATE_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Template Analysis Tool${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Create analysis workspace
echo -e "${YELLOW}→ Setting up analysis workspace...${NC}"
cd "$ANALYSIS_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ANALYSIS_NAME="template-analysis-${TIMESTAMP}"
mkdir -p "$ANALYSIS_NAME"
cd "$ANALYSIS_NAME"

# Copy template
echo -e "${YELLOW}→ Copying template for analysis...${NC}"
if [ -d "$TEMPLATE_PATH" ]; then
    cp -r "$TEMPLATE_PATH" ./template
elif [ -f "$TEMPLATE_PATH" ]; then
    # It's a zip or tar file
    if [[ "$TEMPLATE_PATH" == *.zip ]]; then
        unzip -q "$TEMPLATE_PATH" -d ./template
    elif [[ "$TEMPLATE_PATH" == *.tar.gz ]] || [[ "$TEMPLATE_PATH" == *.tgz ]]; then
        tar -xzf "$TEMPLATE_PATH" -C ./
        mv $(ls -d */ | head -1) ./template 2>/dev/null || true
    fi
fi

echo -e "${GREEN}✓ Template copied to: ${ANALYSIS_DIR}/${ANALYSIS_NAME}/template${NC}"
echo ""

# Analyze structure
echo -e "${YELLOW}→ Analyzing template structure...${NC}"

# Overall structure
tree -L 3 template > structure.txt 2>/dev/null || find template -type d | head -50 > structure.txt

# Find Python files
echo -e "${YELLOW}→ Finding Python scripts...${NC}"
find template -name "*.py" -type f > python-files.txt
PYTHON_COUNT=$(wc -l < python-files.txt)
echo -e "${GREEN}  Found ${PYTHON_COUNT} Python files${NC}"

# Find shell scripts
echo -e "${YELLOW}→ Finding shell scripts...${NC}"
find template -name "*.sh" -type f > shell-scripts.txt
SHELL_COUNT=$(wc -l < shell-scripts.txt)
echo -e "${GREEN}  Found ${SHELL_COUNT} shell scripts${NC}"

# Find agents/automation
echo -e "${YELLOW}→ Identifying agents and automation...${NC}"
find template -name "*.py" -o -name "*.sh" | xargs grep -l -i "agent\|daemon\|cron\|schedule\|background" 2>/dev/null > potential-agents.txt || touch potential-agents.txt
AGENT_COUNT=$(wc -l < potential-agents.txt)
echo -e "${GREEN}  Found ${AGENT_COUNT} potential agents${NC}"

# Find LaunchAgents
echo -e "${YELLOW}→ Finding LaunchAgents and schedulers...${NC}"
find template -name "*.plist" -o -name "crontab*" > schedulers.txt 2>/dev/null || touch schedulers.txt
SCHEDULER_COUNT=$(wc -l < schedulers.txt)
echo -e "${GREEN}  Found ${SCHEDULER_COUNT} scheduler files${NC}"

# Find configs
echo -e "${YELLOW}→ Finding configuration files...${NC}"
find template -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*config*" | grep -v node_modules | grep -v ".git" > configs.txt 2>/dev/null || touch configs.txt
CONFIG_COUNT=$(wc -l < configs.txt)
echo -e "${GREEN}  Found ${CONFIG_COUNT} configuration files${NC}"

# Find README/docs
echo -e "${YELLOW}→ Finding documentation...${NC}"
find template -name "README*" -o -name "*.md" | head -20 > docs.txt 2>/dev/null || touch docs.txt
DOC_COUNT=$(wc -l < docs.txt)
echo -e "${GREEN}  Found ${DOC_COUNT} documentation files${NC}"

# Create analysis summary
cat > ANALYSIS-SUMMARY.md << EOF
# Template Analysis Summary
**Generated:** $(date '+%Y-%m-%d %H:%M:%S')  
**Template Source:** $TEMPLATE_PATH  
**Analysis Location:** ${ANALYSIS_DIR}/${ANALYSIS_NAME}

---

## Quick Stats

- **Python Files:** ${PYTHON_COUNT}
- **Shell Scripts:** ${SHELL_COUNT}
- **Potential Agents:** ${AGENT_COUNT}
- **Scheduler Files:** ${SCHEDULER_COUNT}
- **Config Files:** ${CONFIG_COUNT}
- **Documentation Files:** ${DOC_COUNT}

---

## Directory Structure

\`\`\`
$(cat structure.txt | head -50)
\`\`\`

---

## Potential Agents/Automation

$(if [ -s potential-agents.txt ]; then cat potential-agents.txt | head -20; else echo "None found"; fi)

---

## Configuration Files

$(if [ -s configs.txt ]; then cat configs.txt | head -20; else echo "None found"; fi)

---

## Documentation Files

$(if [ -s docs.txt ]; then cat docs.txt; else echo "None found"; fi)

---

## Next Steps

1. **Review this analysis:** Read through the files listed above
2. **Read template docs:** Check README files in docs.txt
3. **Examine agents:** Look at potential-agents.txt for automation
4. **Check configs:** Review configuration files for patterns
5. **Create integration plan:** Use docs/EXTERNAL-TEMPLATE-INTEGRATION.md

## Integration Checklist

- [ ] Read template documentation
- [ ] Identify valuable features
- [ ] Check for conflicts with PetesBrain
- [ ] Create integration plan
- [ ] Backup PetesBrain (\`backup-petesbrain\`)
- [ ] Test in staging area
- [ ] Document integration

---

## Files Generated

- \`structure.txt\` - Directory tree
- \`python-files.txt\` - All Python scripts
- \`shell-scripts.txt\` - All shell scripts
- \`potential-agents.txt\` - Scripts that might be agents
- \`schedulers.txt\` - LaunchAgents/cron files
- \`configs.txt\` - Configuration files
- \`docs.txt\` - Documentation files
- \`ANALYSIS-SUMMARY.md\` - This file

---

**Template is safely isolated in:** ${ANALYSIS_DIR}/${ANALYSIS_NAME}/template/

**To integrate features:**
1. Read integration guide: ~/Documents/PetesBrain/docs/EXTERNAL-TEMPLATE-INTEGRATION.md
2. Create plan based on this analysis
3. Test in staging: ~/Documents/PetesBrain/staging/
4. Move to production after validation
EOF

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Analysis Complete${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Analysis saved to:${NC}"
echo "  ${ANALYSIS_DIR}/${ANALYSIS_NAME}"
echo ""
echo -e "${YELLOW}Summary file:${NC}"
echo "  ${ANALYSIS_DIR}/${ANALYSIS_NAME}/ANALYSIS-SUMMARY.md"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. cd ${ANALYSIS_DIR}/${ANALYSIS_NAME}"
echo "  2. cat ANALYSIS-SUMMARY.md"
echo "  3. Review template/ folder"
echo "  4. Read ~/Documents/PetesBrain/docs/EXTERNAL-TEMPLATE-INTEGRATION.md"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Open analysis in default text editor (optional)
# open ANALYSIS-SUMMARY.md

