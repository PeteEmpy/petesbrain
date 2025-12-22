# Blog Generator Incident - Client Information Exposure
## Date: 15th December 2025

## INCIDENT SUMMARY

**What Happened**: Four blog posts were published on 15th December 2025 containing client-specific information, including mentions of "hotel client" and specific Performance Max campaign issues.

**Root Cause**: The blog generator was pulling content from the knowledge base (including client emails and meeting notes) instead of external news sources only.

**Business Impact**:
- Client confidentiality potentially compromised
- Professional reputation risk
- Posts publicly visible on roksys.co.uk

## TIMELINE

- **Before Dec 12**: Blog generator pulled from knowledge base with insufficient filtering
- **Dec 7 08:04-15:58**: Script ran 4 times, creating duplicate posts
- **Dec 8 & Dec 15**: Posts published to WordPress
- **Dec 12**: Script fixed to use external RSS feeds only (but too late)
- **Dec 15**: Issue discovered by user

## TECHNICAL DETAILS

### Old System (Before Dec 12)
```python
def get_recent_articles(days=7, limit=7):
    """Get recent articles from knowledge base"""  # ← PROBLEM
    # Pulled from KB with keyword filtering only
    # NO exclusions for client folders, emails, or meeting notes
```

### Problem Areas
1. **Knowledge Base Sources Included**:
   - Client folders (`clients/*/`)
   - Google Rep emails (contain client names, strategies)
   - Meeting notes (contain confidential discussions)
   - Internal methodologies

2. **Insufficient Filtering**:
   - Only keyword-based (e.g., "google ads", "ppc")
   - No path-based exclusions
   - No content validation

3. **Multiple Runs**:
   - Script ran 4 times on Dec 7 (08:04, 12:00, 15:51, 15:58)
   - Created duplicate posts
   - Likely manual invocations via blog-article-generator skill

### Fixed System (Dec 12)
```python
def get_external_news_articles(days=7, limit=7):
    """Get recent articles from external news sources only (no internal data)"""
    # Now pulls from:
    # - Search Engine Journal RSS
    # - Marketing Dive RSS
    # NO knowledge base access
```

## AFFECTED POSTS

### Confirmed Client Information Leakage

**Post ID 575** - "When Your Google Rep Goes Silent: What Performance Max Problems Really Tell Us About AI Advertising"
- **Published**: 2025-12-15 09:00
- **Contains**: "hotel client", Performance Max campaign issues, Google rep communication delays
- **Status**: MUST DELETE
- **URL**: https://roksys.co.uk/wp-admin/post.php?post=575&action=edit

### Duplicate Posts (Same Day)

**Post ID 579, 581, 582** - Various titles
- **Published**: 2025-12-15 09:00
- **Status**: Review and delete duplicates
- **May contain**: References to "nda" (needs manual review)

### Earlier Posts (Needs Review)

**Post IDs 580, 551, 518, 504** - November/early December posts
- **Contains**: Possible "nda" references (may be false positives)
- **Action**: Manual content review required

## IMMEDIATE ACTIONS TAKEN

1. ✅ Audit completed - 8 posts flagged
2. ⏳ Manual deletion required (Application Password lacks delete permissions)

## PERMANENT FIXES REQUIRED

### 1. Update blog-article-generator Skill
**Current State**: Skill documentation still references knowledge base
**Required Fix**: Update skill.md to reflect external RSS feeds only

```bash
# Old (WRONG):
"Fetches Recent Articles: Pulls top 5-7 Google Ads articles from knowledge base"

# New (CORRECT):
"Fetches Recent Articles: Pulls from external news sources (Search Engine Journal, Marketing Dive)"
```

### 2. Add Pre-Publish Validation
Create validation script to detect:
- Client names (list of all client names)
- Keywords like "client", "our client", "hotel client"
- References to specific campaigns or strategies
- Meeting-specific language

### 3. Knowledge Base Content Rules (If Ever Used Again)
If KB is EVER used for blogs in future:
```python
EXCLUDED_PATHS = [
    'clients/',
    'google-rep/',
    'meetings/',
    'methodologies/',
    'strategies/'
]

EXCLUDED_KEYWORDS = [
    'client', 'hotel', 'fashion', 'devonshire', 'smythson',
    # ... all client names
]
```

### 4. Duplicate Prevention
Add WordPress duplicate detection:
- Check for posts scheduled within 24 hours of each other
- Prevent multiple runs on same day
- Add lock file mechanism

## PREVENTION MEASURES

1. **Content Source Policy**:
   - **ONLY external news sources** (RSS feeds from industry publications)
   - **NEVER** knowledge base content (contains client data)
   - **NEVER** emails, meeting notes, or internal documents

2. **Skill Documentation**:
   - Update all skill descriptions to reflect external-only policy
   - Remove references to knowledge base as source

3. **Validation System**:
   - Pre-publish content scan for client keywords
   - Automated flagging system
   - Manual review for flagged content

4. **Run Frequency**:
   - LaunchAgent only (Mon 7:30 AM)
   - Prevent manual invocations
   - Or add confirmation prompt for manual runs

## LESSONS LEARNED

1. **Systemic Issue**: One blog post issue → audit ALL posts (found 8 affected)
2. **Documentation Drift**: Code was fixed Dec 12, but skill docs still referenced old behaviour
3. **Validation Gaps**: No pre-publish content validation system
4. **Duplicate Detection**: WordPress API doesn't prevent duplicate titles/content

## RECOMMENDED WORKFLOW CHANGES

### New Blog Generation Process
1. **Source Selection**: External RSS feeds ONLY
2. **Content Generation**: Claude API synthesizes news into post
3. **Pre-Publish Validation**:
   - Scan for client keywords
   - Check for duplicates
   - Flag for manual review if suspicious
4. **Manual Review**: User approves before publishing
5. **Publish**: WordPress API with scheduled date

### Manual Invocation Safety
If user says "generate blog post":
1. **Confirm source**: "Generating from external news sources (not KB)"
2. **Show preview**: Display title + first 200 words
3. **User approval**: "Publish this post? (yes/no)"
4. **Validate**: Run content scan
5. **Publish**: Only after approval

## FILES TO UPDATE

1. `.claude/skills/blog-article-generator/skill.md` - Update source description
2. `agents/weekly-blog-generator/weekly-blog-generator.py` - Already fixed (Dec 12)
3. `agents/weekly-blog-generator/agent.md` - Update documentation
4. **NEW**: `shared/blog_content_validator.py` - Create validation module

## OWNER ACTIONS REQUIRED

### Immediate (User Must Do)
1. Log in to WordPress: https://roksys.co.uk/wp-admin
2. Delete these posts:
   - Post ID 575 (CONFIRMED client info)
   - Post IDs 579, 581, 582 (duplicates)
3. Review posts 580, 551, 518, 504 for false positives

### Review Before Next Blog Post
- Verify external RSS feeds are working
- Check LaunchAgent configuration
- Test validation system (once implemented)

## STATUS

- [x] Incident identified
- [x] Root cause analysis complete
- [x] Audit completed (8 posts flagged)
- [ ] Posts deleted (requires manual action)
- [ ] Skill documentation updated
- [ ] Validation system implemented
- [ ] Prevention measures documented

## RELATED INCIDENTS

See `/Users/administrator/Documents/PetesBrain.nosync/docs/INCIDENTS.md` for:
- Data Verification Protocol (BMPM Oct 2025)
- Date Verification Protocol
- Task Data Loss incidents

**Common Pattern**: Insufficient validation before public-facing output

---

**Document Owner**: Claude Code (via ultrathink investigation)
**Last Updated**: 2025-12-15
**Severity**: HIGH (client confidentiality)
**Resolution**: IN PROGRESS
