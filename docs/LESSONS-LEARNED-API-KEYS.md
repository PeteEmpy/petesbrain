# Lessons Learned: API Key Management in Python Tools

**Date**: 2025-11-28
**Context**: Building kb-conversational-search tool
**Problem**: Spent excessive time debugging API key access instead of focusing on functionality

---

## What Went Wrong

### The Problem
Built a Flask web server that needed Anthropic API key access. Wasted significant time trying multiple approaches:
1. ❌ Tried to use `anthropic.Anthropic()` without explicit key (SDK version incompatibility)
2. ❌ Tried to pass API key from environment variable (not set in Flask process)
3. ❌ Tried multiple ways to "find" the key that must exist somewhere
4. ❌ Went in circles instead of using the **obvious simple solution**

### Root Cause
**Failed to follow the existing pattern used everywhere else in PetesBrain.**

---

## The Simple Solution That Should Have Been Used From The Start

### Pattern Used Everywhere in PetesBrain

Every other tool in PetesBrain uses **.env files** for API keys:

```bash
# Existing .env files in PetesBrain:
/Users/administrator/Documents/PetesBrain/tools/google-ads-generator/.env
/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/.env
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/meta-ads-mcp-server/.env
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/.env
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/quickbooks-mcp-server/.env
```

**Standard .env file format:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Standard Python Code Pattern

```python
import os
from pathlib import Path

# Load .env file at module start
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Then use the key normally
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set in .env file")

client = anthropic.Anthropic(api_key=api_key)
```

---

## What Should Have Happened

### The Right Approach (5 minutes)

1. **Check existing tools** for API key pattern → Found .env files immediately
2. **Read one .env file** to get the key → Copy the key
3. **Create .env file** in new tool directory → Paste the key
4. **Add .env loader** to Python script → Standard 10-line snippet
5. **Done** → Tool works immediately

**Total time: 5 minutes**

### What Actually Happened (90+ minutes)

1. Tried to create client without explicit key
2. Got SDK compatibility error
3. Upgraded SDK version
4. Got "no API key" error
5. Tried to read from environment variable
6. Searched for where kb-search.py gets its key
7. Tried multiple environment detection methods
8. Went in circles trying to "find" the key
9. Eventually checked for .env files
10. Created .env file solution

**Total time: 90+ minutes of wasted effort**

---

## Key Lessons

### 1. **ALWAYS Check Existing Patterns First**

Before implementing **any** external service integration:

```bash
# Search for existing usage
grep -r "SERVICE_NAME" /path/to/project --include="*.py" | head -10

# Find config files
find /path/to/project -name ".env" -o -name "*.env" | head -10

# Read existing implementation
cat /path/to/existing/tool/using/same/service.py
```

**Rule**: If 5+ other tools use .env files, the 6th tool should too.

### 2. **Use .env Files for All API Keys**

**Always use .env files for:**
- API keys
- Service credentials
- Tokens
- Secret configuration

**Never use:**
- Environment variables (not portable, not persistent)
- Hardcoded keys (security risk)
- Config files in weird locations (not discoverable)

### 3. **Create .env.example Immediately**

When creating a new tool that needs API keys:

```bash
# Create .env.example first
echo "ANTHROPIC_API_KEY=your_key_here" > .env.example

# Then create actual .env
cp /path/to/existing/tool/.env .env

# Add to .gitignore
echo ".env" >> .gitignore
```

### 4. **Add .env Loader as Standard Template**

**Save this as a snippet and use it everywhere:**

```python
# Standard .env loader - add at top of every tool that needs API keys
import os
from pathlib import Path

ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
else:
    print(f"⚠️  Warning: {ENV_FILE} not found")
    print("Create it with: cp .env.example .env")
```

### 5. **Stop Trying to Be Clever**

The temptation: "Maybe I can auto-detect the key from somewhere..."

The reality: **Just use a .env file like everything else.**

**Bad indicators:**
- Spending >10 minutes on authentication setup
- Trying multiple different approaches
- Searching for "where the key must be"
- Environment variable debugging

**Good indicator:**
- Copied .env file from existing tool in 30 seconds

---

## Standard Tool Setup Checklist

When creating a new Python tool:

- [ ] Check how existing tools handle API keys
- [ ] Copy .env file from existing tool (if same service)
- [ ] Create .env.example with placeholder
- [ ] Add .env loader code at module start
- [ ] Add .env to .gitignore
- [ ] Test that tool can read the key
- [ ] Move on to actual functionality

**Time budget: 5 minutes maximum**

If spending more than 5 minutes on API key setup, **STOP** and copy an existing pattern.

---

## PetesBrain-Specific Patterns

### Standard File Locations

```
tool-name/
├── .env                    # API keys (gitignored)
├── .env.example           # Template for users
├── .gitignore             # Must include .env
├── requirements.txt       # Dependencies
├── README.md             # Setup instructions
└── tool-name.py          # Main script with .env loader
```

### Standard Requirements

All PetesBrain Python tools should include:

```python
# requirements.txt
anthropic>=0.72.0    # Always use latest
flask>=3.0.0         # For web tools
flask-cors>=4.0.0    # For API servers
```

### Standard .env File

```bash
# .env - Used by all PetesBrain tools
ANTHROPIC_API_KEY=sk-ant-api03-...

# Other common keys in PetesBrain:
# GOOGLE_ADS_DEVELOPER_TOKEN=...
# GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
```

---

## Red Flags to Watch For

### Signs You're Going in Circles

1. **Trying >2 different approaches** for the same problem
2. **Debugging environment variables** for >10 minutes
3. **Searching for "where the key must be"**
4. **SDK version compatibility issues** (should have checked existing tools first)
5. **"But it works for kb-search.py..."** (then use the same pattern!)

### When to Stop and Reset

If you hit any of these, **STOP** and go back to basics:

```bash
# 1. Find existing working example
find . -name "*.env" | head -1

# 2. Read how it's used
cat $(find . -name "*.py" -exec grep -l "ANTHROPIC_API_KEY" {} \; | head -1)

# 3. Copy the pattern exactly
cp existing-tool/.env new-tool/.env
cp existing-tool/env-loader-code.py new-tool/
```

---

## Future Prevention

### For Building Similar Systems

**Step 1: Research Phase (2 minutes)**
- Search for existing implementations in codebase
- Read 1-2 examples of similar tools
- Identify common patterns

**Step 2: Copy Pattern (3 minutes)**
- Copy .env file structure
- Copy .env loader code
- Copy requirements.txt patterns

**Step 3: Customize (Rest of time)**
- Focus on actual functionality
- Not on authentication/configuration

### Template for Future AI Responses

When building a new tool that needs API access:

```
Before implementing, let me check existing patterns:
1. Search for existing .env files: find . -name ".env"
2. Check how similar tools authenticate
3. Copy the working pattern
4. Implement the actual functionality

Following existing pattern from [tool-name]:
- Using .env file for API keys
- Standard .env loader code
- Same requirements.txt pattern
```

---

## Documentation Updates Needed

### 1. Create: `/docs/STANDARD-PYTHON-TOOL-TEMPLATE/`

```
STANDARD-PYTHON-TOOL-TEMPLATE/
├── .env.example
├── .gitignore
├── requirements.txt
├── tool-template.py          # With .env loader
├── README-TEMPLATE.md        # Standard setup instructions
└── SETUP-CHECKLIST.md       # Copy this for each new tool
```

### 2. Update: `/docs/DEVELOPMENT-GUIDELINES.md`

Add section: "API Key Management - Always Use .env Files"

### 3. Create: `/docs/COMMON-PATTERNS.md`

Document all repeated patterns:
- .env file loading
- Flask server setup
- Anthropic client initialization
- Google API authentication
- MCP server structure

---

## Success Metrics

**Next time we build a similar tool:**

- [ ] API key setup completed in <5 minutes
- [ ] No debugging of environment variables
- [ ] No SDK version issues (checked existing tools first)
- [ ] No "where is the key?" discussions
- [ ] Used existing .env pattern immediately
- [ ] Total auth setup time: 5 minutes or less

**If any of these fail, revisit this document.**

---

## Summary

### The One Rule

**"If existing tools use .env files, your new tool uses .env files. Period."**

No exceptions. No cleverness. No "but maybe this time...".

Just copy the working pattern and move on to building actual functionality.

### Time Saved

- **Old approach**: 90+ minutes debugging API keys
- **Right approach**: 5 minutes copying .env pattern
- **Time saved**: 85 minutes per tool
- **Better**: Focus on functionality, not configuration

---

## Action Items

- [x] Create this lessons-learned document
- [ ] Create standard Python tool template directory
- [ ] Update all existing tools to use consistent .env pattern
- [ ] Add .env examples to all tools missing them
- [ ] Update DEVELOPMENT-GUIDELINES.md
- [ ] Create COMMON-PATTERNS.md reference
- [ ] Add to CLAUDE.md: "Always check for existing .env files first"

---

**Remember**: Configuration should be the easiest part. If it's not, you're doing it wrong.
