# Client Onboarding Audit Checklist

**Source**: Section 1 (FOUNDATION) of Google Ads Audit Framework
**Purpose**: Ensure tracking, analytics, and conversion setup is correct before campaign launch
**Items**: 80+ foundation checks
**Priority**: Complete HIGH-impact items before launching campaigns

---

## How to Use This Checklist

### For New Client Onboarding

1. **Create client audit document**: `clients/{client-slug}/documents/onboarding-audit-{date}.md`
2. **Copy this checklist** into the client document
3. **Check items systematically** starting with HIGH-impact
4. **Document findings** for each item (✅ Pass / ⚠️ Issue / ❌ Critical)
5. **Create P0 tasks** for HIGH-impact failures
6. **Verify before campaign launch** - don't launch with critical issues outstanding

### Priority Order

1. **HIGH Impact** - Complete these first (blocking issues)
2. **MID Impact** - Complete before launch where possible
3. **LOW Impact** - Complete for comprehensive audits
4. **Optional** - Complete based on client needs and use case

---

## 1.1 - CLARITY

### Business Understanding

- [ ] **HIGH** 💡 Complete the business rationale and messaging sheet
  - **Purpose**: Understand client's value proposition, target audience, USPs
  - **Action**: Interview client, document in `clients/{client}/CONTEXT.md`
  - **Why Critical**: Informs all campaign strategy and ad copy

---

## 1.2 - TAGS

### Google Tag Manager

- [ ] **MID** 💬 GTM (Google Tag Manager) is installed on website
  - **Verify**: Check page source for `gtm.js` script
  - **Tool**: View page source, search for "googletagmanager.com/gtm.js"

- [ ] **MID** 💬 🔗 Conversion Linker installed in GTM
  - **Verify**: Check GTM container → Tags → Google Ads Conversion Linker
  - **Why Critical**: Required for accurate conversion attribution

### Google Analytics Tracking

- [ ] **HIGH** 🔗 Google Analytics tracking code added to GTM and the code is firing on all pages
  - **Verify**: GTM Preview mode → Check GA4 Configuration tag fires on all pages
  - **Tool**: Google Tag Assistant Chrome extension

- [ ] **HIGH** 💬 Analytics is firing on dead pages (404)
  - **Verify**: Navigate to non-existent page, check if GA4 tag fires
  - **Why Critical**: Identifies tracking integrity

- [ ] **HIGH** 🔗 Check your entire site for missing Google Analytics code with one click
  - **Tool**: Google Tag Assistant or Chrome DevTools

---

## 1.3 - GOOGLE ANALYTICS 4

### Property Setup

- [ ] **HIGH** 💬 📑 Audit website for all pages and sections to be tracked
  - **Action**: Document all page types (homepage, product pages, checkout, thank you)
  - **Verify**: GA4 Events → Check events firing for each page type

- [ ] **HIGH** 💬 Provide property level access to stakeholders on GA4
  - **Action**: Add client stakeholders and Roksys team to GA4 property
  - **Access Level**: Editor for active managers, Viewer for stakeholders

- [ ] **MID** 💬 🔗 Time zone is correct
  - **Verify**: GA4 Admin → Property Settings → Reporting time zone
  - **Standard**: Use client's business time zone (UK = GMT/BST)

- [ ] **MID** 🔗 Your currency is correct
  - **Verify**: GA4 Admin → Property Settings → Currency
  - **Standard**: Match client's reporting currency (UK = GBP)

- [ ] **LOW** 💬 🔗 Define Internal Traffic rules - Exclude Internal traffic
  - **Action**: GA4 Admin → Data Streams → Configure tag settings → Define internal traffic
  - **Add**: Client office IPs, Roksys IPs

### Integration & Linking

- [ ] **HIGH** Integrate Google Search Console
  - **Action**: GA4 Admin → Product Links → Search Console → Link
  - **Why Critical**: Unlocks organic search data in GA4

- [ ] **HIGH** 💬 🔗 Link Google Ads to GA4
  - **Action**: GA4 Admin → Product Links → Google Ads → Link
  - **Why Critical**: Required for conversion import and cross-platform analysis

- [ ] **HIGH** 💬 Enable Personalised Advertising
  - **Action**: GA4 Admin → Data Settings → Data Collection → Enable
  - **Why Critical**: Required for remarketing audiences

- [ ] **HIGH** 💬 🔗 Enable Auto-Tagging
  - **Action**: Google Ads → Settings → Account settings → Auto-tagging → Enable
  - **Why Critical**: Automatic UTM parameter tracking

### Audiences & Remarketing

- [ ] **HIGH** 🔗 Setup Remarketing Audiences
  - **Action**: GA4 → Audiences → Create audiences (All Users, Converters, Cart Abandoners)
  - **Link to**: Google Ads for remarketing campaigns

- [ ] **HIGH** 🔗 Import conversions from GA4 property to your Google Ads account
  - **Action**: Google Ads → Tools → Conversions → Import → GA4
  - **Why Critical**: Enables GA4 conversion tracking in Google Ads

- [ ] **MID** 💬 🔗 Create custom or Suggested Audiences
  - **Action**: GA4 → Audiences → Use suggested audiences or create custom
  - **Examples**: High-value users, engaged shoppers, product viewers

- [ ] **HIGH** 💬 🔗 Migrate Audiences from Universal Analytics to GA4
  - **Action**: If client had UA audiences, recreate in GA4
  - **Note**: Only applicable for existing clients migrating from UA

- [ ] **MID** 💬 🔗 Create Audience Triggers
  - **Action**: GA4 → Audiences → Set up audience triggers for automation
  - **Use Case**: Trigger email campaigns when users join specific audiences

### Attribution

- [ ] **HIGH** 💬 🔗 Setup correct attribution model
  - **Action**: GA4 → Admin → Attribution settings → Choose model
  - **Default**: Data-driven (if enough conversions), otherwise Cross-channel last click

- [ ] **MID** 💬 🔗 Change Attribution Model Through Advertising Snapshot
  - **Action**: GA4 → Advertising → Advertising snapshot → Model comparison
  - **Purpose**: Compare different attribution models

### Enhanced Measurements

- [ ] **HIGH** 💬 Enhanced Measurements (Enabled by default; don't change it)
  - **Verify**: GA4 → Admin → Data Streams → Enhanced measurement → Check enabled
  - **Tracks**: Page views, scrolls, outbound clicks, site search, video engagement, file downloads

- [ ] **MID** 💬 🔗 Create custom definitions (with custom dimensions)
  - **Action**: GA4 → Admin → Custom definitions → Create custom dimensions
  - **Examples**: User type (B2B/B2C), Product category viewed, Member tier

- [ ] **MID** 💬 🔗 Bot Filtering (Know bots are Automatically Excluded in GA4)
  - **Verify**: Bots automatically filtered in GA4 (no action needed)
  - **Note**: Not configurable like in UA

### Site Search

- [ ] **HIGH** 💬 🔗 Site Search feature (Enabled by default, but it may require further configuration)
  - **Verify**: GA4 → Events → Check "view_search_results" event
  - **Configure**: If custom search parameters, add in Enhanced measurement settings

- [ ] **MID** 💬 🔗 Custom search query parameters
  - **Action**: GA4 → Admin → Data Streams → Enhanced measurement → Site search
  - **Add**: Custom query parameters (e.g., s=, search=, q=)

### Account Linking (Duplicate Check)

- [ ] **HIGH** 🔗 Google Ads account linking
  - **Note**: Duplicate of line 19 above - verify once

- [ ] **HIGH** Analytics remarketing audiences
  - **Note**: Duplicate of line 22 above - verify once

### Privacy & Data Collection

- [ ] **HIGH** 💬 🔗 Google Signals - Analytics Demographics and Interests reports
  - **Action**: GA4 → Admin → Data Settings → Data Collection → Google signals → Activate
  - **Why Critical**: Required for demographic and interest reporting

- [ ] **HIGH** 💬 🔗 Verify Data Retention time period to match your privacy policies
  - **Action**: GA4 → Admin → Data Settings → Data Retention → Set to 14 months (maximum)
  - **Why Critical**: GDPR compliance

- [ ] **HIGH** 💬 🔗 Set up Scroll Tracking
  - **Verify**: Enhanced measurement includes scroll tracking (90% scroll depth)
  - **Note**: Enabled by default in Enhanced measurement

### Referral Exclusions

- [ ] **LOW** 💬 🔗 Spam referrals are excluded (unwanted lists)
  - **Action**: GA4 → Admin → Data Streams → Configure tag settings → Unwanted referrals
  - **Add**: Known spam domains (semalt.com, etc.)

- [ ] **LOW** 💬 🔗 Self-referrals excluded
  - **Action**: GA4 → Admin → Data Streams → Configure tag settings → Unwanted referrals
  - **Add**: Client's own domain(s)

- [ ] **HIGH** 💬 🔗 Payment gateway referrals excluded
  - **Action**: GA4 → Admin → Data Streams → Configure tag settings → Unwanted referrals
  - **Add**: PayPal, Stripe, Worldpay domains
  - **Why Critical**: Prevents payment gateways appearing as referral sources

### Advanced Tracking

- [ ] **MID** 🔗 Cross-domain tracking in place
  - **Action**: If client has multiple domains, configure cross-domain tracking
  - **Configure**: GA4 → Admin → Data Streams → Configure tag settings → Configure your domains
  - **Optional**: Only needed for multi-domain setups

- [ ] **HIGH** 🔗 UTM tagging is implemented correctly
  - **Verify**: Check campaign URLs include utm_source, utm_medium, utm_campaign
  - **Tool**: Google's Campaign URL Builder
  - **Why Critical**: Required for campaign attribution

- [ ] **HIGH** 💬 🔗 Upload data from external sources via Data Import
  - **Action**: GA4 → Admin → Data Import → Create data source
  - **Use Cases**: CRM data, product costs, offline conversions
  - **Ongoing**: Set up regular import schedule

- [ ] **MID** 🔗 Enable Google signals data collection to get cross-device and demographic data
  - **Note**: Duplicate of line 36 above - verify once

- [ ] **MID** 💬 🔗 Configure session timeout setting (default is 30 mins)
  - **Action**: GA4 → Admin → Data Streams → Configure tag settings → Adjust session timeout
  - **Standard**: 30 minutes (default) - only change if specific need

### E-commerce Tracking

- [ ] **HIGH** 💬 📑 🔗 Setup ecommerce tracking (where appropriate)
  - **Action**: Implement GA4 e-commerce events (view_item, add_to_cart, purchase)
  - **Required Events**: purchase (minimum), view_item, add_to_cart, begin_checkout (recommended)
  - **E-commerce Only**: Skip for lead gen clients

- [ ] **HIGH** 🔗 Ecommerce data is correct and accurate (where appropriate)
  - **Verify**: GA4 → Monetisation → Ecommerce purchases → Check revenue, transactions, items
  - **Test**: Make test purchase, verify data appears correctly

- [ ] **MID** 💬 🔗 Create Predictive Metrics for ecommerce
  - **Action**: GA4 → Audiences → Create predictive audiences (likely 7-day purchasers)
  - **Requires**: 1,000+ purchasers and 1,000+ non-purchasers in last 28 days

- [ ] **MID** 💬 Importing Predictive Audiences into Google Ads
  - **Action**: Google Ads → Tools → Audience Manager → GA4 audiences → Select predictive audiences
  - **Requires**: Predictive audiences created in GA4 first

- [ ] **MID** 💬 Setup GA4 data transfer to BigQuery
  - **Action**: GA4 → Admin → Product Links → BigQuery → Link
  - **Use Case**: Advanced analysis, ML, long-term data retention
  - **Optional**: Only for large clients with data analysis needs

---

## 1.4 - CONVERSION

### Conversion Strategy

- [ ] **HIGH** 💬 📑 💡 Are you using Micro conversions? Don't skip this
  - **Action**: Define micro conversions (email signup, video view, PDF download)
  - **Why Critical**: Provides more conversion data for optimisation
  - **Document**: In `clients/{client}/CONTEXT.md`

- [ ] **HIGH** 💬 📑 Review Micro conversion reference guide for ideas and examples
  - **Action**: Brainstorm micro conversions based on client's funnel
  - **Examples**: Form submission (not purchase), phone click, chat initiation, product page view (MOFU)

### Conversion Setup

- [ ] **HIGH** 💬 Google Ads conversion tag has at least 1 Macro conversion configured
  - **Verify**: Google Ads → Tools → Conversions → Check at least 1 primary conversion
  - **Examples**: Purchase, Lead form submission, Phone call

- [ ] **HIGH** 💬 Analytics has at least 1 Macro conversion configured
  - **Verify**: GA4 → Admin → Events → Mark as conversion
  - **Standard**: "purchase" event marked as conversion (e-commerce)

- [ ] **HIGH** Setup Micro conversions based on your analysis of visitor behaviour
  - **Action**: Google Ads → Tools → Conversions → Import from GA4
  - **Select**: Micro conversion events (e.g., email_signup, video_play)

- [ ] **MID** 💬 🔗 Setup video triggers within GTM for micro engagement conversions
  - **Action**: GTM → Create video engagement trigger → YouTube video tracking
  - **Track**: Video plays, progress (25%, 50%, 75%, 100%)
  - **Optional**: Only if video is important conversion funnel element

- [ ] **MID** 💬 Analytics Macro and Micro conversion goals imported to Ads
  - **Verify**: Google Ads → Tools → Conversions → Check GA4 imports
  - **Ensure**: Both macro and micro conversions imported

### Conversion Configuration

- [ ] **HIGH** 💬 Each unique conversion is set to report in Conversion columns - no duplicates!
  - **Verify**: Google Ads → Tools → Conversions → Check "Include in Conversions" column
  - **Fix**: If duplicates exist (e.g., GA4 + gTag tracking same action), exclude one from reporting

- [ ] **HIGH** 💬 📑 Conversion attribution is configured where appropriate
  - **Verify**: Google Ads → Tools → Conversions → Check attribution model per conversion
  - **Standard**: Data-driven (if available), otherwise Last click for most conversions
  - **Cross-reference**: Section 2 - Attribution for model selection guidance

- [ ] **HIGH** 💬 Have you tried to 'convert' yourself? Go through the steps/enquiry form/checkout
  - **Action**: Complete conversion process end-to-end
  - **Verify**: Conversion fires in Google Ads (Tools → Conversions → Recent conversions)
  - **Why Critical**: Catches tracking issues before launch

---

## 1.5 - DESTINATION (Website Quality)

### Technical Setup

- [ ] **HIGH** 💬 🔗 Website is using an SSL so pages load as https and http pages redirect to their secure equivalent
  - **Verify**: Check all pages load as HTTPS, test HTTP → HTTPS redirect
  - **Why Critical**: Google Ads policy requirement, user trust

- [ ] **HIGH** 💬 🔗 Sitespeed is good to great
  - **Tool**: Google PageSpeed Insights, GTmetrix
  - **Target**: Mobile > 60, Desktop > 80 (PageSpeed score)
  - **Why Critical**: Impacts Quality Score and conversion rate

- [ ] **HIGH** 💬 Remove any scripts or tags you don't need or use
  - **Action**: GTM → Review all tags → Disable/delete unused tags
  - **Why Critical**: Improves page speed, reduces tracking errors

### Search Console Integration

- [ ] **MID** 🔗 Search console is linked to Analytics
  - **Action**: GA4 → Admin → Product Links → Search Console → Link
  - **Why Important**: Unlocks organic search query data

- [ ] **MID** 🔗 Website sitemap submitted via search console and website is indexed
  - **Verify**: Search Console → Sitemaps → Check sitemap submitted
  - **Verify**: Search Console → Coverage → Check pages indexed

- [ ] **HIGH** 🔗 Basic on-page SEO structure is done right
  - **Check**: Title tags, meta descriptions, H1 tags, URL structure
  - **Why Important**: Impacts Quality Score (landing page experience)

---

## 1.6 - SHOPPING SPECIFIC (E-commerce Clients Only)

### Merchant Centre Setup

- [ ] **HIGH** 🔗 Google Merchant Centre account is setup
  - **Verify**: merchant.google.com → Check account exists
  - **Action**: Create account if needed, link to Google Ads

- [ ] **HIGH** 🔗 Verified and claimed your domain in Google Merchant Centre
  - **Action**: Merchant Centre → Settings → Website verification → Verify and claim
  - **Why Critical**: Required to run Shopping campaigns

- [ ] **HIGH** 🔗 Product feed created and uploaded it to Google Merchant Centre
  - **Verify**: Merchant Centre → Products → Check products in feed
  - **Method**: Scheduled fetch (preferred) or manual upload

- [ ] **HIGH** 🔗 Merchant Centre diagnostics tab and fix any critical errors
  - **Action**: Merchant Centre → Products → Diagnostics → Fix all critical errors
  - **Why Critical**: Products with errors won't show in Shopping ads

### E-commerce Integration

- [ ] **HIGH** 🔗 Ecommerce tracking in enabled in Analytics
  - **Note**: Duplicate of line 47/48 above - verify once

- [ ] **HIGH** 🔗 Google Merchant Centre is linked to Google Ads
  - **Action**: Google Ads → Tools → Linked accounts → Google Merchant Centre → Link
  - **Why Critical**: Required to run Shopping and Performance Max campaigns

---

## 1.7 - PERFORMANCE MAX

### Conversion Accuracy

- [ ] **HIGH** 💬 For Accurate conversions use GTag not GA imports
  - **Action**: Use Google Ads conversion tags (gTag) for primary conversions
  - **Why**: gTag is more accurate than GA4 imports for conversion tracking
  - **Note**: Can use GA4 imports for secondary/micro conversions

- [ ] **HIGH** 🔗 Enhanced conversions are setup and accurate
  - **Action**: Google Ads → Tools → Conversions → Check Enhanced conversions enabled
  - **Method**: Use GTM or gTag to pass first-party data (email, phone)
  - **Why Critical**: Improves conversion attribution accuracy by 5-15%
  - **Ongoing**: Verify enhanced conversions passing data correctly

- [ ] **HIGH** 💬 🔗 Monitor macro vs micro conversions against other campaign types
  - **Action**: Create report comparing PMax conversions to Search/Shopping
  - **Watch For**: Micro conversion inflation (PMax over-optimising to low-value actions)
  - **Ongoing**: Weekly review

- [ ] **HIGH** 💬 🔗 Lead gen quality measurement with first part data
  - **Action**: Track lead quality (not just quantity) using CRM integration
  - **Method**: Import offline conversions or conversion adjustments
  - **Why Critical**: Prevents optimising to low-quality leads
  - **Ongoing**: Weekly/monthly review

### Conversion Configuration

- [ ] **MID** Set values for your qualified conversions
  - **Action**: Google Ads → Tools → Conversions → Set conversion value
  - **Method**: Average order value (e-commerce) or estimated lifetime value (lead gen)
  - **Ongoing**: Review and adjust quarterly

- [ ] **HIGH** 💬 🔗 Update your conversion goals to Not Account Default
  - **Action**: Google Ads → Tools → Conversions → Set "Include in Conversions" to No for micro conversions
  - **Why Critical**: Prevents micro conversions counting as primary goals
  - **Note**: Micro conversions should NOT be in "Conversions" column

- [ ] **HIGH** 💬 🔗 🚨 Be careful when adding "Converted Leads" to account default goals
  - **Warning**: Only add "Converted Leads" to account default if lead quality is verified
  - **Why Critical**: Can cause optimisation to low-quality leads
  - **Note**: Requires CRM integration to track lead quality

---

## Onboarding Audit Summary Template

After completing checklist, document summary:

```markdown
# {Client Name} - Onboarding Audit Summary

**Date**: {Date}
**Auditor**: Peter Empson
**Account ID**: {Google Ads Customer ID}
**Property ID**: {GA4 Property ID}

---

## Completion Summary

- **Total Items Checked**: {X}/82
- **HIGH Impact**: {X}/38 ✅
- **MID Impact**: {X}/30 ⚠️
- **LOW Impact**: {X}/4 ⚠️
- **Optional**: {X}/10

---

## Critical Issues (P0 - Block Launch)

1. ❌ {Issue description with framework reference}
2. ❌ {Issue description with framework reference}

**Resolution Required Before Campaign Launch**

---

## Important Issues (P1 - Complete Within 1 Week)

1. ⚠️ {Issue description with framework reference}
2. ⚠️ {Issue description with framework reference}

---

## Minor Issues (P2 - Complete Within 1 Month)

1. ⚠️ {Issue description with framework reference}

---

## Verified Items ✅

- ✅ GA4 tracking configured correctly
- ✅ Conversion actions firing accurately
- ✅ Enhanced conversions enabled
- [List all passing HIGH-impact items]

---

## E-commerce Specific Notes

**Applicable**: Yes/No

{If Yes, summarise Merchant Centre setup status}

---

## Recommendations

1. {Recommendation with priority}
2. {Recommendation with priority}

---

## Sign-Off

- [ ] All P0 issues resolved
- [ ] All HIGH-impact items verified
- [ ] Account ready for campaign launch

**Approved By**: Peter Empson
**Date**: {Date}
```

---

## Quick Reference: Most Critical Items

### Absolute Must-Haves Before Launch (P0)

1. ✅ **GA4 tracking firing on all pages** (Line 9)
2. ✅ **Google Ads linked to GA4** (Line 19)
3. ✅ **At least 1 Macro conversion configured in Google Ads** (Line 55)
4. ✅ **Conversion tracking tested end-to-end** (Line 62)
5. ✅ **Website using HTTPS** (Line 64)
6. ✅ **Enhanced conversions enabled** (Line 79) - for PMax clients
7. ✅ **Merchant Centre linked** (Line 76) - for e-commerce clients

### Complete Within First Week (P1)

1. ⚠️ **Remarketing audiences setup** (Line 22)
2. ⚠️ **Micro conversions configured** (Line 57)
3. ⚠️ **Auto-tagging enabled** (Line 21)
4. ⚠️ **Payment gateway referrals excluded** (Line 41)
5. ⚠️ **Personalised advertising enabled** (Line 20)

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `docs/AUDIT-FRAMEWORK-GUIDE.md` | Complete framework guide (all 6 sections) |
| `docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv` | Master framework file (457 items) |
| `docs/ADDING-A-NEW-CLIENT.md` | Client onboarding workflow |
| `clients/{client}/CONTEXT.md` | Client-specific context and platform IDs |

---

**Complete this checklist for EVERY new client before campaign launch. Don't skip HIGH-impact items.**
