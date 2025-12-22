# Blog Content Selection Rules
**Last Updated**: 15th December 2025
**Status**: MANDATORY
**Severity**: CRITICAL (Client Confidentiality)

## ABSOLUTE RULE: EXTERNAL SOURCES ONLY

**The roksys.co.uk blog MUST use EXTERNAL NEWS SOURCES ONLY.**

### ✅ ALLOWED Sources

1. **External RSS Feeds**:
   - Search Engine Journal (`https://www.searchenginejournal.com/feed/`)
   - Marketing Dive (`https://www.marketingdive.com/news/`)
   - Other industry publications (publicly available)

2. **Public Announcements**:
   - Official Google Ads blog posts
   - Public platform updates
   - Industry conference announcements

3. **General Industry Trends**:
   - Market research (publicly available)
   - Platform feature rollouts (public)
   - Industry statistics (published)

### ❌ FORBIDDEN Sources

**NEVER use content from**:

1. **Knowledge Base** (`roksys/knowledge-base/`)
   - Contains client emails
   - Contains meeting notes
   - Contains internal strategies
   - Contains confidential discussions

2. **Client Folders** (`clients/*/`)
   - Client-specific work
   - Campaign strategies
   - Performance data
   - Meeting transcripts

3. **Google Rep Emails**
   - Often mention client names
   - Contain confidential strategies
   - Include internal discussions

4. **Meeting Notes**
   - Client names and contexts
   - Specific campaign details
   - Internal methodologies

5. **Internal Methodologies**
   - Proprietary processes
   - Client-specific approaches
   - Competitive strategies

## PRE-PUBLISH VALIDATION

**MANDATORY**: Every blog post MUST pass validation before publishing.

### Validation Process

```bash
# Run validation before publishing
cd /Users/administrator/Documents/PetesBrain.nosync
python3 shared/blog_content_validator.py "Blog Post Title" content.html
```

### What Validation Checks

1. **Client Names** (CRITICAL):
   - Devonshire, Smythson, Tree2MyDoor, Superspace, etc.
   - ANY client name, past or present

2. **Client References** (HIGH):
   - "my client", "our client", "a client"
   - "hotel client", "fashion client"
   - "client's account", "client's campaign"

3. **Internal Language** (MEDIUM):
   - "our Google rep", "meeting with Google"
   - "internal meeting", "during the call"
   - "discussed with", "in our meeting"

4. **Specific Campaigns** (HIGH):
   - References to specific campaign implementations
   - "I uploaded", "I tested this with"
   - "Performance Max campaign for a [specific business]"

### Validation Results

**✅ PASSED** = Safe to publish
**🔴 FAILED** = DO NOT PUBLISH - remove client info first

## CONTENT WRITING GUIDELINES

### ✅ GOOD Examples

**Professional Industry Observation**:
> "I've been watching this rollout closely, and the industry consensus seems to be that..."

**General Professional Perspective**:
> "Based on what we're seeing in the industry data, this change affects e-commerce businesses by..."

**News Reporting**:
> "Google announced this week that Performance Max campaigns will now include..."

### ❌ BAD Examples

**Client-Specific Story**:
> "I tested this last week with a hotel client and CTR dropped 40%"
❌ FORBIDDEN: Mentions specific client type + specific results

**Campaign Implementation**:
> "I uploaded 23 videos for a fashion client and saw..."
❌ FORBIDDEN: Specific implementation + client type

**Meeting Reference**:
> "My Google rep mentioned in our call about Devonshire that..."
❌ FORBIDDEN: Client name + internal meeting

## TONE & LANGUAGE RULES

### What to Write About

✅ **News**: What's happening in Google Ads world
✅ **Industry Trends**: What we're seeing across the industry
✅ **Platform Changes**: Official feature rollouts
✅ **Best Practices**: General professional guidance
✅ **Business Impact**: How changes affect e-commerce businesses

### How to Write It

✅ **First Person Professional**: "I've been watching..." "I'm interested to see..."
✅ **Industry Perspective**: "Industry patterns suggest..." "We're seeing..."
✅ **Forward-Looking**: "This will likely impact..." "Worth keeping tabs on..."

❌ **NEVER**:
- Specific client stories or case studies
- Client names (never, even generic like "a luxury brand")
- Specific campaign test results from client work
- Meeting discussions or Google rep conversations
- Implementation details for specific clients

## EXCEPTION HANDLING

**Q: What if a client is mentioned in PUBLIC news?**
A: You may reference the public news story, but add NO internal knowledge or commentary beyond what's publicly available.

**Q: What if an industry trend matches our client work?**
A: Write about the industry trend from PUBLIC sources only. Do not reference your client work even if it's similar.

**Q: What if I want to use a client as a case study?**
A: Get explicit written permission from the client first. Even then, use the validation system.

## AUTOMATED SAFEGUARDS

### Blog Generator Script

**File**: `agents/weekly-blog-generator/weekly-blog-generator.py`

**Safeguards**:
1. Only fetches from external RSS feeds
2. NO access to knowledge base
3. NO access to client folders
4. Runs validation before publishing

### LaunchAgent Configuration

**File**: `agents/launchagents/com.petesbrain.weekly-blog-generator.plist`

**Schedule**: Monday 7:30 AM only
**Manual Runs**: Should trigger confirmation prompt

### Skill Documentation

**File**: `.claude/skills/blog-article-generator/skill.md`

**Updated**: 15th December 2025
**Status**: Reflects external sources only

## INCIDENT RESPONSE

**If client information appears in a published post**:

1. **IMMEDIATE**: Delete the post from WordPress
2. **AUDIT**: Check all recent posts for similar issues
3. **ROOT CAUSE**: Investigate how client info was selected
4. **FIX**: Update code/validation to prevent recurrence
5. **DOCUMENT**: Record in `/docs/INCIDENTS.md`

**See**: `/docs/BLOG-GENERATOR-INCIDENT-2025-12-15.md` for example

## MAINTENANCE

### Monthly Review

- [ ] Verify external RSS feeds are working
- [ ] Test validation system with sample content
- [ ] Review published posts for any issues
- [ ] Update CLIENT_NAMES list if new clients added

### Quarterly Review

- [ ] Audit all published posts (manual scan)
- [ ] Update validation keywords if needed
- [ ] Review skill documentation for accuracy
- [ ] Test LaunchAgent workflow end-to-end

## RELATED DOCUMENTATION

- `/docs/BLOG-GENERATOR-INCIDENT-2025-12-15.md` - Dec 2025 incident details
- `/docs/INCIDENTS.md` - All historical incidents
- `/docs/DATA-VERIFICATION-PROTOCOL.md` - Data accuracy standards
- `agents/weekly-blog-generator/weekly-blog-generator.py` - Main script
- `.claude/skills/blog-article-generator/skill.md` - Skill documentation
- `shared/blog_content_validator.py` - Validation module

## OWNER

**Responsibility**: Peter Empson / Claude Code
**Enforcement**: MANDATORY - no exceptions
**Review Frequency**: After every incident, minimum quarterly
**Last Incident**: 15th December 2025 (4 posts with client info)

---

**CRITICAL REMINDER**: The purpose of the roksys.co.uk blog is to build trust with potential customers by demonstrating expertise in Google Ads and e-commerce. Client confidentiality is paramount. If in doubt, don't publish it.
