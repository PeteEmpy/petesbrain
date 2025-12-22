# Pre-Commit Hook System

**Created**: 2025-12-22
**Purpose**: Automated secret scanning to prevent credential exposure
**Status**: ✅ Active and tested

---

## Overview

Following the security incidents of December 22, 2025 (Anthropic API key exposure and Google service account exposure), a pre-commit hook system was implemented to prevent future credential leaks to GitHub.

**What it does:**
- Automatically scans staged files for secrets before each commit
- Blocks commits containing exposed credentials
- Provides clear feedback on what was detected and how to fix it
- Works alongside .gitignore to provide defense-in-depth

---

## How It Works

### Two-Layer Protection

**Layer 1: Git Pre-Commit Hook**
- Location: `.git/hooks/pre-commit`
- Runs automatically before every `git commit`
- Performs two checks:
  1. Blocks product-feeds/tasks.json files (legacy artifact prevention)
  2. Scans for secrets using gitleaks (security check)

**Layer 2: Gitleaks Secret Scanner**
- Tool: gitleaks 8.30.0 (installed via Homebrew)
- Detects: API keys, private keys, tokens, passwords, and 100+ secret types
- Built-in rules: AWS, Google, GitHub, Anthropic, Slack, and many more

### Detection Capabilities

**What Gitleaks Detects:**
- ✅ RSA/EC private keys (Google service accounts)
- ✅ API keys (Anthropic, AWS, etc.)
- ✅ OAuth tokens (GitHub, GitLab, etc.)
- ✅ Database connection strings
- ✅ Slack webhooks
- ✅ JWT tokens
- ✅ SSH private keys
- ✅ 100+ other secret patterns

**What Gitleaks Ignores (Correctly):**
- ❌ Well-known example secrets from documentation (e.g., "AKIAIOSFODNN7EXAMPLE")
- ❌ Test/dummy values explicitly marked as examples
- ❌ Public information

**Verified Detection:**
Testing confirmed gitleaks successfully detects real Google service account private keys:
```
Finding:     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQ..."
RuleID:      private-key
Entropy:     6.010170
File:        infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json
```

---

## What Happens When Secrets Are Detected

### Example Output

When you attempt to commit a file containing secrets, the pre-commit hook blocks the commit:

```
🔍 Scanning for secrets...

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

❌ PRE-COMMIT HOOK BLOCKED (Check 2/2 Failed)

Secrets or credentials detected in staged files!

What was found:
Finding:     "private_key": "-----BEGIN PRIVATE KEY-----..."
Secret:      -----BEGIN PRIVATE KEY-----...
RuleID:      private-key
Entropy:     6.010170
File:        config/credentials.json
Line:        5

Why this is blocked:
  Credentials should NEVER be committed to the repository.
  This prevents exposure of API keys, passwords, tokens, and private keys.

What to do:
  1. Remove the secret from the file
  2. Use environment variables or .env files (gitignored)
  3. For credentials.json files, ensure they're in .gitignore
  4. Re-commit after removing secrets

To bypass this check (NOT RECOMMENDED):
  git commit --no-verify
```

---

## How to Use the System

### Normal Workflow (No Changes Required)

```bash
# Stage your changes
git add my-file.py

# Commit (hook runs automatically)
git commit -m "Update configuration"

# If no secrets: commit succeeds
✅ All pre-commit checks passed

# If secrets detected: commit blocked
❌ PRE-COMMIT HOOK BLOCKED
```

### If You Get Blocked

**Step 1: Review the output**
- Read what secret was detected (file, line number, secret type)
- Confirm it's actually a secret (not a false positive)

**Step 2: Remove the secret**
```bash
# Edit the file to remove the secret
vim config/my-file.py

# Replace hardcoded secret with environment variable
# Before: API_KEY = "sk-ant-api03-abc123..."
# After:  API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# OR ensure credentials file is in .gitignore
echo "config/credentials.json" >> .gitignore
```

**Step 3: Re-commit**
```bash
# Stage the fixed file
git add config/my-file.py

# Commit again (should succeed now)
git commit -m "Update configuration (secrets removed)"
✅ All pre-commit checks passed
```

---

## Bypass Instructions (Use Only When Necessary)

### When Bypass is Acceptable

**✅ Safe to bypass:**
- False positives (gitleaks flagged something that isn't actually a secret)
- Documentation files containing redacted/example secrets
- Test files with fake secrets for testing purposes
- Public configuration values mistakenly flagged

**❌ NEVER bypass for:**
- Real API keys, tokens, or passwords
- Private keys (RSA, EC, SSH)
- Database credentials
- OAuth secrets
- Service account credentials

### How to Bypass

```bash
# Use --no-verify flag
git commit --no-verify -m "Commit message"

# ⚠️ WARNING: Only use this if you're absolutely certain the flagged
# content is not a real secret. When in doubt, ask for review.
```

---

## Maintenance

### Updating Gitleaks

```bash
# Check current version
gitleaks version

# Update via Homebrew
brew upgrade gitleaks

# Verify update
gitleaks version
```

### Checking What Would Be Detected

```bash
# Scan a specific file without committing
gitleaks detect --source my-file.py --verbose --no-git

# Scan all staged files
gitleaks protect --staged --verbose
```

### Customising Detection Rules

If you need to add custom rules or allowlist specific patterns, create `.gitleaks.toml` in the repository root:

```toml
title = "PetesBrain Gitleaks Configuration"

# Add custom rules
[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''CUSTOM_KEY_[A-Za-z0-9]{32}'''

# Allowlist specific files or patterns
[allowlist]
paths = [
  '''docs/examples/''',  # Ignore example files
]

regexes = [
  '''EXAMPLE_KEY_.*''',  # Ignore keys with EXAMPLE prefix
]
```

---

## Integration with .gitignore

The pre-commit hook works alongside .gitignore for defense-in-depth:

**Protected by .gitignore** (can't be staged at all):
```
**/credentials.json
**/*-credentials.json
infrastructure/rollback-snapshots/
.env
.env.local
```

**Scanned by gitleaks** (if accidentally staged):
- Any file containing secrets that bypassed .gitignore
- Code files with hardcoded secrets
- Documentation files with exposed credentials
- Configuration files with embedded secrets

---

## Incident History

**December 22, 2025 - Dual Credential Exposure**
- **Issue 1**: Anthropic API key hardcoded in 3 skill.md files (8 occurrences)
- **Issue 2**: Google service account credentials in rollback snapshots (28 files)
- **Root cause**: No automated secret scanning before commits
- **Resolution**: Implemented pre-commit hook with gitleaks integration
- **Prevention**: This system now blocks similar exposures

Full details:
- `docs/SECURITY-INCIDENT-2025-12-22-API-KEY-EXPOSURE.md`
- `docs/SECURITY-INCIDENT-2025-12-22-GOOGLE-SERVICE-ACCOUNTS-EXPOSURE.md`

---

## Testing & Verification

### Verification Tests Performed

**Test 1: Real Private Key Detection ✅**
```bash
gitleaks detect --source infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json
# Result: ✅ Detected RSA private key
```

**Test 2: Example Secret Filtering ✅**
```bash
# Created test-script.py with AWS example keys
git add test-script.py && git commit
# Result: ✅ Gitleaks correctly ignored example secrets
```

**Test 3: Hook Integration ✅**
```bash
# Staged and committed multiple files
git commit -m "Test commit"
# Result: ✅ Hook executed automatically, scanned all staged files
```

### Manual Testing

To verify the system is working on your machine:

```bash
# Create test file with fake (but realistic-looking) secret
echo 'API_KEY="sk-proj-abc123xyz789"' > test-secret.sh

# Try to commit it
git add test-secret.sh
git commit -m "Test"

# Should be blocked if gitleaks recognises the pattern
# Clean up
rm test-secret.sh
```

---

## Troubleshooting

### Hook Not Running

**Check if hook is executable:**
```bash
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable permissions)

# If not executable:
chmod +x .git/hooks/pre-commit
```

**Verify hook exists:**
```bash
cat .git/hooks/pre-commit
# Should show the full hook script
```

### Gitleaks Not Installed

**Install via Homebrew:**
```bash
brew install gitleaks

# Verify installation
gitleaks version
# Should show: version 8.30.0 or higher
```

### False Positives

If gitleaks flags something that isn't actually a secret:

1. **Review the detection**: Is it really not a secret?
2. **Use --no-verify if confirmed safe**: `git commit --no-verify`
3. **Consider adding to allowlist**: Create `.gitleaks.toml` with allowlist rules

### Hook Performance

Gitleaks is very fast, typically scanning in <100ms:
```
scanned ~623 bytes (623 bytes) in 82.8ms
```

If commits become slow:
- Check repository size (large commits take longer)
- Consider using `gitleaks protect` instead of `gitleaks detect` (only scans staged changes)

---

## Additional Security Measures

### Complementary Protections

**1. .gitignore patterns** (prevent staging)
```
**/credentials.json
infrastructure/rollback-snapshots/
.env*
token.json
*.pem
*.key
```

**2. macOS Keychain** (for storing credentials securely)
```bash
# Store API key in Keychain
security add-generic-password -s "PetesBrain" -a "ANTHROPIC_API_KEY" -w "sk-ant-..."

# Retrieve from Keychain in code
security find-generic-password -s "PetesBrain" -a "ANTHROPIC_API_KEY" -w
```

**3. Environment variables** (for runtime credentials)
```python
import os
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
```

**4. MCP server .env files** (gitignored)
```bash
# infrastructure/mcp-servers/my-server/.env
ANTHROPIC_API_KEY=sk-ant-api03-...
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Best Practices

### DO:
- ✅ Use environment variables for all credentials
- ✅ Store credentials in .env files (gitignored)
- ✅ Use macOS Keychain for permanent credential storage
- ✅ Reference credentials via variables in code: `$ANTHROPIC_API_KEY`
- ✅ Keep credentials.json files in .gitignore
- ✅ Review gitleaks output before bypassing

### DON'T:
- ❌ Hardcode API keys in source files
- ❌ Commit credentials.json files
- ❌ Use `--no-verify` without reviewing the detection
- ❌ Store secrets in configuration files committed to git
- ❌ Bypass the hook for convenience

---

## References

- **Gitleaks Documentation**: https://github.com/gitleaks/gitleaks
- **Gitleaks Rules**: https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml
- **GitHub Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning
- **Security Incident Reports**:
  - `docs/SECURITY-INCIDENT-2025-12-22-API-KEY-EXPOSURE.md`
  - `docs/SECURITY-INCIDENT-2025-12-22-GOOGLE-SERVICE-ACCOUNTS-EXPOSURE.md`

---

## Summary

**What**: Automated secret scanning using gitleaks in a git pre-commit hook
**Why**: Prevent credential exposure to GitHub (following December 22 incidents)
**How**: Scans all staged files before commit, blocks if secrets detected
**Status**: ✅ Active, tested, and verified working
**Maintenance**: Update gitleaks via `brew upgrade gitleaks` periodically

**The system successfully prevents the type of credential exposure that occurred on December 22, 2025, providing automated defense-in-depth alongside .gitignore protection.**
