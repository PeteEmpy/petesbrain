# PPC Industry Newsletters Directory

**Date:** 16 December 2025
**Purpose:** Comprehensive list of PPC/Google Ads/Meta Ads newsletters for Knowledge Base content capture
**Integration:** Email-sync with `ppc-newsletters` label → `roksys/knowledge-base/_inbox/emails/`

---

## ✅ Verified Newsletters - Ready to Subscribe

### Google Ads / PPC Newsletters

#### 1. Optmyzr - "Stay Updated with Optmyzr" ⭐ TIER 1
**Authority**: Frederick Vallaeys (10/10)
- **Signup URL**: https://www.optmyzr.com/blog (HubSpot form on page)
- **Description**: "Sign up for our newsletter to receive the latest insights, industry updates, and tips directly to your inbox."
- **Platform**: HubSpot
- **Frequency**: Unknown (likely weekly/monthly)
- **Content Type**: Google Ads strategies, tool updates, industry insights
- **Expected Relevance Score**: 9-10/10
- **Why Subscribe**: Direct from Google Ads book author, highest authority PPC content

#### 2. ZATO Marketing - "PPC News" ⭐ TIER 1
**Authority**: Kirk Williams (9/10)
- **Signup URL**: https://mailchi.mp/e3a679228517/zato-blog-subscribers
- **Alternative**: Footer link on https://www.zatomarketing.com
- **Description**: "ZATO Blog Subscribers" newsletter covering PPC news and insights
- **Platform**: Mailchimp
- **Frequency**: Unknown (likely weekly/bi-weekly)
- **Content Type**: PPC strategy, Google/Microsoft Ads insights
- **Expected Relevance Score**: 8-9/10
- **Why Subscribe**: ZATO founder, recognised PPC expert, strategic content

#### 3. Microsoft Advertising - "Insider Newsletter" ⭐ OFFICIAL
**Authority**: Official Microsoft platform (10/10)
- **Signup URL**: https://about.ads.microsoft.com/en/forms/microsoft-advertising-newsletter-sign-up
- **Description**: Official Microsoft Advertising insights and updates
- **Platform**: Microsoft
- **Frequency**: Unknown (likely monthly)
- **Content Type**: Platform updates, competitor perspective to Google Ads, strategic insights
- **Expected Relevance Score**: 9-10/10
- **Why Subscribe**: Official platform source, alternative perspective to Google Ads

#### 4. PPC Hero - "Weekly Blog Updates" ⭐ TIER 2
**Authority**: Community platform (7/10)
- **Signup URL**: https://www.ppchero.com (sidebar form)
- **Description**: "Save time and Become the Hero with updates from PPC Hero in your inbox!"
- **Platform**: Email (likely Mailchimp/similar)
- **Frequency**: Weekly
- **Content Type**: PPC tactics, case studies, community insights
- **Expected Relevance Score**: 7-8/10
- **Why Subscribe**: Multi-author community platform, diverse PPC perspectives

#### 5. Search Engine Land - Daily Newsletter ⭐ TIER 2
**Authority**: Industry publication (8/10)
- **Signup URL**: https://searchengineland.com/newsletters
- **Description**: "Daily SEO & PPC updates you need to know"
- **Platform**: Third Door Media
- **Frequency**: Daily
- **Content Type**: SEO + PPC combined, breaking news, expert advice, events
- **Expected Relevance Score**: 7-8/10
- **Why Subscribe**: Industry news aggregator, timely updates
- **Note**: Not PPC-exclusive, but includes significant PPC coverage

### Meta / Facebook Ads Newsletters

#### 6. Common Thread Collective - "Tactical Insights for DTC Brands" ⭐ TIER 2
**Authority**: DTC/E-commerce specialists (8/10)
- **Signup URL**: https://commonthreadco.com (homepage form)
- **Description**: "Weekly(ish) guidance from the frontlines"
- **Platform**: Email
- **Frequency**: Weekly-ish
- **Content Type**: DTC strategy, Meta Ads tactics, e-commerce growth
- **Expected Relevance Score**: 8-9/10
- **Why Subscribe**: High innovation score, data-driven DTC insights

---

## ⏭️ Alternative Sources (No Newsletter Available)

These sources have working RSS feeds (already monitored):

| Source | RSS Feed | Status | Authority |
|--------|----------|--------|-----------|
| **Brad Geddes (Adalysis)** | https://adalysis.com/feed/ | ✅ Active | 10/10 |
| **Jon Loomer Digital** | https://www.jonloomer.com/feed/ | ✅ Active | 9/10 |

These sources have no newsletter or RSS:

| Source | Reason | Alternative |
|--------|--------|-------------|
| **WordStream** | No newsletter found | RSS feed working |
| **AdEspresso** | No newsletter found | RSS feed working |
| **Social Media Examiner** | General marketing only | Category RSS working |

---

## 📋 Subscription Checklist

**Total Newsletters to Subscribe**: 6

### Google Ads / PPC (5 newsletters)
- [ ] Optmyzr - "Stay Updated with Optmyzr"
- [ ] ZATO Marketing - "PPC News"
- [ ] Microsoft Advertising - "Insider Newsletter"
- [ ] PPC Hero - "Weekly Blog Updates"
- [ ] Search Engine Land - Daily Newsletter

### Meta / Facebook Ads (1 newsletter)
- [ ] Common Thread Collective - "Tactical Insights for DTC Brands"

**Recommended Email for Subscriptions**: `petere@roksys.co.uk`

---

## 🚀 Implementation Steps

### Step 1: Subscribe to All Newsletters (15 minutes)

**Use this email**: `petere@roksys.co.uk`

1. **Optmyzr**: Visit https://www.optmyzr.com/blog → Fill HubSpot form
2. **ZATO**: Visit https://mailchi.mp/e3a679228517/zato-blog-subscribers → Subscribe
3. **Microsoft Ads**: Visit https://about.ads.microsoft.com/en/forms/microsoft-advertising-newsletter-sign-up
4. **PPC Hero**: Visit https://www.ppchero.com → Use sidebar form
5. **Search Engine Land**: Visit https://searchengineland.com/newsletters → Subscribe
6. **Common Thread**: Visit https://commonthreadco.com → Homepage form

### Step 2: Create Gmail Label (1 minute)

**In Gmail:**
1. Create new label: `ppc-newsletters`
2. Nested under: (none) or `Roksys/` if you prefer organisation

### Step 3: Label First Emails Manually (2 minutes)

**When first newsletter arrives from each source:**
1. Apply `ppc-newsletters` label manually
2. Email-sync will pick it up automatically (runs every 6 hours)
3. Auto-label will learn the pattern for future emails

**After first email labelled:**
- Future emails auto-labelled by `shared/email-sync/auto-label-config.yaml`
- Emails sync to `roksys/knowledge-base/_inbox/emails/`
- Existing KB processor scores with 4-criteria rubric
- MIN_RELEVANCE_SCORE = 8.0 filters low-value content

### Step 4: Verify Integration (24-48 hours)

**After subscribing, check:**
1. **Gmail**: Do newsletters arrive? Apply `ppc-newsletters` label to first one
2. **File system**: Check `roksys/knowledge-base/_inbox/emails/` for synced newsletters
3. **Scoring**: Verify relevance scores ≥8.0 (should be automatic for authority newsletters)
4. **Logs**: Check `shared/email-sync/logs/` for any sync errors

---

## 📊 Expected Impact

### Authority Coverage Update

**Before Newsletter Integration:**
- Tier 1 Sources: 5 (Brad Geddes, Jon Loomer, Microsoft Ads RSS, Optmyzr RSS broken, ZATO RSS broken)
- Authority Score: 6.8/10

**After Newsletter Integration:**
- Tier 1 Sources: **7** (Brad Geddes, Jon Loomer, Microsoft Ads RSS, **Optmyzr newsletter**, **ZATO newsletter**)
- Authority Score: **7.2/10** (projected)
- Official Sources: 3 (Google Ads, Meta, **Microsoft Ads newsletter**)

### Content Quality Metrics

| Newsletter | Frequency | Authority | Expected Score | Content Type |
|------------|-----------|-----------|----------------|--------------|
| Optmyzr | Weekly-ish | 10/10 | 9-10/10 | Strategic depth, decision frameworks |
| ZATO | Weekly | 9/10 | 8-9/10 | PPC strategy, platform insights |
| Microsoft Ads | Monthly | 10/10 | 9-10/10 | Official announcements, strategic |
| PPC Hero | Weekly | 7/10 | 7-8/10 | Community tactics, case studies |
| Search Engine Land | Daily | 8/10 | 7-8/10 | Industry news, timely updates |
| Common Thread | Weekly-ish | 8/10 | 8-9/10 | DTC strategy, innovation |

**Average Expected Relevance Score**: **8.5/10** (well above MIN_RELEVANCE_SCORE of 8.0)

---

## 🔍 Monitoring & Maintenance

### Weekly Checks (5 minutes)

**Every Friday:**
1. Check Gmail `ppc-newsletters` label for new newsletters
2. Verify auto-labelling working correctly
3. Spot-check file sync to `_inbox/emails/`
4. Review relevance scores in KB inbox

### Monthly Review (15 minutes)

**First Friday of each month:**
1. **Newsletter frequency audit**: Are newsletters arriving regularly?
2. **Content quality check**: Are scores matching expectations (≥8.0)?
3. **Duplicate detection**: Any overlap with existing RSS feeds?
4. **Missing newsletters**: Did any subscriptions lapse?

**Red flags:**
- ⚠️ No newsletters received in 2+ weeks (check spam folder)
- ⚠️ Relevance scores consistently <7.0 (may need unsubscribe)
- ⚠️ Duplicate content with RSS (choose newsletter OR RSS, not both)

---

## 🎯 Success Criteria (3 Month Target)

| Metric | Baseline | Target | Current | Status |
|--------|----------|--------|---------|--------|
| **Newsletters Active** | 0 | 6 | 0 | ⏳ Pending |
| **Newsletter Score Avg** | N/A | ≥8.0 | N/A | ⏳ Pending |
| **Tier 1 Authority Sources** | 5 | 7+ | 5 | ⏳ Pending |
| **KB Authority Score** | 6.8 | 8.0+ | 6.8 | ⏳ Pending |
| **Newsletter Frequency** | N/A | ≥1/week | N/A | ⏳ Pending |

**3-Month Evaluation (March 2026):**
- If newsletters delivering high-quality content (≥8.0 avg) → Keep all
- If newsletters overlap with RSS (duplicates) → Keep newsletter, remove RSS
- If newsletters below threshold (<8.0 avg) → Unsubscribe, refocus on working sources

---

## 💡 Rationale: Newsletters vs RSS

### Why Newsletters > RSS for These Sources

**Advantages of Email Newsletter Approach:**

1. **✅ Works When RSS Doesn't**
   - Optmyzr RSS: 404 error
   - ZATO RSS: Malformed XML
   - Newsletters: Reliable delivery guaranteed

2. **✅ Uses Existing Infrastructure**
   - Email-sync already working for AI news
   - Auto-labelling configured
   - KB processor handles emails natively

3. **✅ Higher Signal-to-Noise**
   - Newsletters = curated content
   - RSS = all blog posts (including low-value)
   - Newsletter editors pre-filter for quality

4. **✅ Strategic Long-Form Content**
   - Newsletters typically contain strategic analysis
   - More "when/why" vs "how-to"
   - Better alignment with 4-criteria scoring rubric

5. **✅ Easier Debugging**
   - Emails visible in Gmail
   - Can manually review before processing
   - Clear sender identification

**Disadvantages:**
- ⚠️ Lower frequency (weekly vs daily for RSS)
- ⚠️ Depends on newsletter editor quality
- ⚠️ May include promotional content

**Verdict**: For authorities without working RSS, newsletters are best alternative.

---

## 📁 Related Files

**Email-Sync Configuration:**
- `shared/email-sync/config.yaml` - Label mappings (line 24: `"ppc-newsletters"`)
- `shared/email-sync/auto-label-config.yaml` - Auto-labelling rules (lines 365-426)

**Documentation:**
- `docs/KB-CONTENT-STRATEGY-UPGRADE.md` - Master strategy document
- `docs/KB-CONTENT-UPGRADE-IMPLEMENTATION-SUMMARY.md` - Phase 1-3 results
- `docs/KB-CONTENT-UPGRADE-PHASE-3-SUMMARY.md` - Alternative sources research
- `docs/KB-CONTENT-UPGRADE-PHASE-4-NEWSLETTER-RESEARCH.md` - Newsletter investigation

**Monitors:**
- `agents/industry-news-monitor/industry-news-monitor.py` - RSS monitoring (Google Ads/PPC)
- `agents/facebook-news-monitor/facebook-news-monitor.py` - RSS monitoring (Meta Ads)

---

## 🆘 Troubleshooting

### Newsletter Not Arriving

**Check:**
1. Spam folder in Gmail
2. Promotions tab in Gmail
3. Subscription confirmation email (check inbox for "confirm subscription")
4. Email address typo during signup

**Fix:**
- Re-subscribe with correct email
- Whitelist sender domain
- Move from Promotions/Spam to Primary

### Auto-Labelling Not Working

**Check:**
1. `shared/email-sync/auto-label-config.yaml` - domains and keywords correct?
2. Email-sync logs: `shared/email-sync/logs/auto-label.log`
3. Manually apply label to first email to "seed" the system

**Fix:**
- Add sender email to `emails:` array in config
- Add newsletter name to `keywords:` array
- Restart email-sync agent

### Emails Not Syncing to File System

**Check:**
1. Email-sync agent running: `launchctl list | grep email-sync`
2. Gmail label correctly applied: `ppc-newsletters`
3. Config mapping: `config.yaml` line 24

**Fix:**
- Restart email-sync: `launchctl unload/load ~/Library/LaunchAgents/co.roksys.petesbrain.email-sync.plist`
- Check logs: `tail -50 ~/.petesbrain-email-sync-error.log`

### Relevance Scores Too Low

**Check:**
1. Newsletter content quality (promotional vs strategic)
2. Scoring rubric accuracy
3. Newsletter contains actual strategic content vs just links

**Fix:**
- If consistently <8.0: Unsubscribe (not valuable)
- If 6.0-7.9: Keep for 3 months, re-evaluate
- If promotional only: Unsubscribe immediately

---

**Document Status:** Ready for Implementation
**Last Updated:** 16 December 2025 17:00
**Next Steps:** Subscribe to all 6 newsletters, label first emails
**Owner:** Peter Empson
