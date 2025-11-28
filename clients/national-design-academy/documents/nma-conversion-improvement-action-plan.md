# NMA Conversion Improvement - Granular Action Plan

**Account**: National Motorsport Academy (5622468019)
**Goal**: Increase conversions from 47.8/month to 120+/month
**Timeline**: 4 weeks
**Created**: November 10, 2025

---

## Week 1: Emergency Fixes (Nov 11-17)

### Day 1: Diagnose & Pause Bad Performers

**Step 1: Check Portfolio Bid Strategy** (30 minutes)
1. Go to Google Ads → Tools → Bid Strategies
2. Look for any shared/portfolio bid strategies
3. If found, check the Target CPA setting:
   - If it's £800+ → **This is your problem**
   - Change to £100 for Engineering, £150 for Management
   - OR remove campaigns from portfolio and use campaign-level bidding
4. Document current settings before changes

**Step 2: Pause Disaster Campaigns** (15 minutes)
Pause these immediately:
- ✅ NMA | P Max | UK | Management 100 (£917 for 1 conversion)
- ✅ NMA | Search | UK | Management 100 Ai 25/8 (£1,437 CPA)
- ✅ NMA | Search | ROW | Management 100 (0 conversions)

**Why**: These 3 campaigns are burning £2,500/month for 1.83 conversions. Stop the bleeding.

**Step 3: Emergency CPC Fix - Engineering Search** (20 minutes)
Campaign: NMA | Search | UK | Engineering 55 Ai 25/8

Current problem: £947 average CPC

**Option A - If using Target CPA bidding:**
1. Go to campaign settings
2. Change Target CPA from current (likely £800+) to £80
3. Monitor for 48 hours
4. If no impressions, increase to £120, then £150

**Option B - If CPC still high after 48 hours:**
1. Switch to Manual CPC bidding temporarily
2. Set max CPC to £3.00
3. Monitor for 24 hours - you should see CPC drop to £2-5 range
4. Gradually increase if not getting impressions

**Expected outcome**: CPC should drop from £947 to £50-200 within 72 hours

---

### Day 2-3: Scale the Winner

**Step 4: Boost ROW Engineering Budget** (10 minutes)
Campaign: NMA | Search | ROW | Engineering 100

Current: £10/day budget, £29.86 CPA, 10 conversions
This is performing 5x better than UK campaigns!

**Actions:**
1. Increase daily budget from £10 to £40
2. Monitor for 48 hours
3. If CPA stays under £50, increase to £60/day
4. If CPA rises above £60, pull back to £40

**Expected outcome**: 10 conversions → 40 conversions per month from this campaign alone

**Step 5: Check What's Working in ROW Engineering** (30 minutes)
1. Go to campaign → Search Terms report
2. Download last 30 days
3. Identify which keywords are converting:
   - "race car mechanic school" - 6 conversions at £8.38 CPA
   - "motorsport engineering" - 4 conversions at £50 CPA
4. Add these exact keywords to UK Engineering campaign as Exact Match
5. Set bid to £5 initially

**Why**: If these work in ROW, they should work in UK too

---

### Day 4-5: Quality Score Improvements

**Step 6: Fix Quality Score 3 Keywords** (1 hour)

Pause these immediately (they're wasting money):
- "mechanical engineering degree" (QS 3)
- "automotive engineering universities uk" (QS 3)
- "international business management" (QS 3)
- "how to become an f1 engineer" (QS 3)

**Step 7: Improve Quality Score 5 Keywords** (2 hours)

For each of these high-impression, low QS keywords:
1. "car engineering courses" (4,808 impr, QS 5)
2. "motorsport engineering degree" (5,369 impr, QS 5)
3. "online engineering degree" (3,561 impr, QS 5)

**Actions per keyword:**
1. Create new ad with keyword in headline:
   - Headline 1: "Car Engineering Courses Online"
   - Headline 2: "Accredited Motorsport Degrees"
   - Headline 3: "Study Online - UK Qualification"
   - Description: "Learn car engineering from industry experts. Flexible online learning, UK-accredited qualification. Start your motorsport career."

2. Ensure landing page headline matches:
   - Check https://motorsport.nda.ac.uk/
   - If headline doesn't mention "car engineering courses", request change from Henry/Paul

3. Monitor QS after 7 days - should improve to 6-7

**Expected outcome**: 20-30% CPC reduction on these keywords = 20-30% more clicks for same budget

---

### Day 6-7: Conversion Tracking Audit

**Step 8: Check Enhanced Conversions Setup** (1 hour)

Current issue: 0.825657 conversions = £8,875.81 value (£10,750 per conversion)

**Actions:**
1. Go to Tools → Conversions → "NMA Enhanced Conversions For Leads"
2. Check "Value" settings - is it set to "Use different values for each conversion"?
3. If yes, check what value is being passed from backend:
   - Contact Henry Bagshawe (technical contact)
   - Ask: "What conversion value is being passed for NMA applications?"
   - Should be: £50-200 (reasonable CPA target), NOT £10,750
4. If £10,750 is correct (actual course value), then bidding strategies are working correctly
5. If incorrect, fix backend to pass correct value

**Expected outcome**: Correct values = better bidding optimization

**Step 9: Investigate Management PMax Tracking** (45 minutes)

Current issue: 13,718 clicks → 1 conversion (0.0073% conversion rate is statistically improbable)

**Actions:**
1. Go to campaign → Insights → Conversion Tracking
2. Check if "application_complete" conversion is enabled for this campaign
3. Check Search Terms report - are people searching for jobs, not courses?
   - If yes → Add negative keywords: job, jobs, hiring, vacancy, career, employed
4. Check asset groups:
   - Go to Asset Groups tab
   - Look at Search Categories - are they related to "motorsport management course" or "motorsport jobs"?
   - If showing job-related categories, assets are targeting wrong audience

**Test hypothesis:**
1. Go to website https://motorsport.nda.ac.uk/
2. Click on a Management course
3. Try to complete application
4. Check if conversion fires (use Google Tag Assistant Chrome extension)
5. If conversion doesn't fire → Tracking issue, contact Henry

**Expected outcome**: Identify why 13k clicks aren't converting

---

## Week 2: Optimization & Expansion (Nov 18-24)

### Step 10: Reactivate Management Search (Fixed) (Day 8)

Campaign: NMA | Search | UK | Management 100 Ai 25/8

**Before reactivating:**
1. Check Engineering Search CPC - has it normalized to £50-200?
2. If yes, apply same bid strategy fix to Management:
   - Set Target CPA to £150 (higher than Engineering as Management converts less)
   - OR set Manual CPC to £5 if Target CPA didn't work
3. Add negative keywords from Step 9:
   - job, jobs, hiring, vacancy, career, employed, salary, wage
4. Reactivate and monitor daily

**Budget**: Start at £20/day (was £40)
**Target**: £200 CPA or better
**Monitor**: If CPA exceeds £300 after 7 days, pause again

---

### Step 11: Engineering PMax Asset Refresh (Day 9-10)

Campaign: NMA | P Max | UK | Engineering Max Conv 46 100 19/11

Current: 0.78% CTR (very low), £125 CPA (acceptable)

**Goal**: Improve CTR from 0.78% to 1.5%+ to get more volume

**Actions:**

**Day 9 - Add New Headlines (30 mins):**
1. Go to Asset Groups → Add Assets → Headlines
2. Add these 10 new headlines:
   - "Online Motorsport Engineering Degree"
   - "UK-Accredited Engineering Course"
   - "Study F1 Engineering From Home"
   - "Flexible Motorsport Qualifications"
   - "Learn Race Car Engineering"
   - "Motorsport Academy - Online"
   - "Become a Motorsport Engineer"
   - "Part-Time Engineering Degree"
   - "Professional Motorsport Training"
   - "Start Your F1 Career Today"

**Day 10 - Add New Descriptions (30 mins):**
1. Add 5 new descriptions focusing on benefits:
   - "Industry-expert tutors with F1 experience. Flexible online learning fits around your life. UK-accredited qualification recognized worldwide."
   - "Learn from professionals who've worked in Formula 1 and motorsport. Study at your own pace, 100% online, no campus attendance required."
   - "Practical engineering skills for real motorsport careers. Portfolio projects, industry connections, job-ready qualification."
   - "Affordable online degree, payment plans available. Same quality as campus courses, study from anywhere in the world."
   - "Join students from 30+ countries studying motorsport engineering online. Start dates every month, no waiting."

**Day 10 - Check/Add Images (1 hour):**
1. Go to Asset Groups → Images
2. Do you have at least 15 images?
3. If not, request from Paul/Henry:
   - F1 cars
   - Race car engineering close-ups
   - Students working on engines
   - Successful graduates
   - Motorsport events/races
4. Upload all images (PMax needs variety)

**Expected outcome**: CTR improves to 1.2-1.5% within 14 days = 50% more clicks = 8 more conversions

---

### Step 12: Keyword Expansion (Day 11-12)

**Goal**: Find new high-intent keywords from search terms report

**Day 11 - Mine Search Terms (1 hour):**
1. Go to each Search campaign → Search Terms
2. Download last 30 days, filter by conversions > 0
3. Look for terms not already in keyword list
4. Add as Exact Match keywords with £5 bid

**Day 12 - Add Negative Keywords (45 mins):**
1. Look for search terms with 10+ clicks, 0 conversions
2. Add as negative keywords
3. Common patterns to exclude:
   - Apprenticeship terms (if you don't offer apprenticeships)
   - Job-seeking terms (job, hiring, career, salary)
   - Free course terms (free, without paying, no cost)
   - Competitor names (unless conquest strategy)

**Expected outcome**: 10-15% improvement in conversion rate

---

### Step 13: Landing Page Optimization Request (Day 13)

**Contact**: Henry Bagshawe (henry@nda.ac.uk) and Paul Riley (pk@nda.ac.uk)

**Issue**: Management PMax has 0.0073% conversion rate (13k clicks, 1 conversion)

**Email to send:**

```
Subject: NMA Landing Page Optimization - Urgent

Hi Henry/Paul,

I've been analyzing the NMA Google Ads performance and found a critical issue:

The Management campaigns are getting excellent traffic (13,718 clicks in 30 days) but almost zero conversions (1 conversion = 0.0073% conversion rate).

Engineering campaigns with similar traffic convert at 0.6% (80x better).

This suggests the Management landing page may not be optimized for paid traffic visitors.

Could we test these changes to the Management course landing page:

1. **Clear Call-to-Action above fold**: "Apply Now" button visible without scrolling
2. **Headline matching ad copy**: "Online Motorsport Management Degree - UK Accredited"
3. **Trust signals higher up**: Industry partnerships, accreditation logos, graduate success stats
4. **Simpler application form**: Reduce fields from X to 5 max (name, email, course interest, phone, submit)
5. **Remove distractions**: Hide navigation menu on landing page version (keep focus on application)

Engineering page likely converts better because it has clearer CTAs/simpler flow.

Can we implement and A/B test by end of November?

Best,
Pete
```

**Expected outcome**: If implemented, could improve Management conversion rate from 0.0073% to 0.3% = 40 conversions instead of 1

---

## Week 3: Rebuild & Test (Nov 25 - Dec 1)

### Step 14: Rebuild Management PMax (Day 15-16)

Campaign: NMA | P Max | UK | Management 100 (currently paused)

**Why rebuild**: 13,718 clicks for 1 conversion suggests fundamental targeting issue

**Day 15 - Create New Asset Group (2 hours):**

1. Create new PMax campaign: "NMA | P Max | UK | Management V2"
2. Budget: £20/day
3. Bidding: Maximize Conversions (no Target CPA initially)
4. Conversion goal: "application_complete" only

**Asset Group 1: "Motorsport Business Management Students"**

**Audience Signals** (Critical - this is why V1 failed):
- Add interests: "Business Education", "Online Education", "Career Development"
- **EXCLUDE** these: "Job Search", "Employment Services", "Job Listings"
- Add custom segments:
  - People who searched for: "motorsport management course", "motorsport business degree", "MBA motorsport"
  - **EXCLUDE** people who searched for: "motorsport manager jobs", "motorsport team jobs", "F1 jobs"

**Headlines** (15 required):
1. "Online Motorsport Management Degree"
2. "MBA in Motorsport Business"
3. "UK-Accredited Management Course"
4. "Study Motorsport Business Online"
5. "Flexible Management Qualification"
6. "Learn F1 Business Management"
7. "Motorsport MBA - Part Time"
8. "Professional Motorsport Training"
9. "Become a Motorsport Manager"
10. "Industry-Recognized MBA"
11. "Online Business Management Degree"
12. "Study With Industry Experts"
13. "Start Your Motorsport Career"
14. "Flexible Online Learning"
15. "UK University Partnership"

**Descriptions** (5 required):
1. "Study motorsport business management online with industry experts. UK-accredited MBA, flexible learning, payment plans available. Start dates every month."
2. "Learn from F1 professionals. Online MBA in motorsport management recognized by industry. Study part-time while working. No campus attendance required."
3. "Practical business skills for motorsport careers. Marketing, finance, operations, team management. Real-world projects with industry partners."
4. "Affordable online MBA with payment plans. Same quality as campus courses. Study from anywhere. Join students from 30+ countries."
5. "Professional motorsport business qualification. Industry connections, career support, job-ready skills. Start your application today."

**Images**: Minimum 15 (use business/management focused imagery, not just race cars)

**Day 16 - Set Up Exclusions:**
1. Go to campaign settings → Content Exclusions
2. Exclude: "Below the fold", "Parked domains", "Error pages"
3. Add negative keywords at campaign level:
   - job, jobs, hiring, employed, employment, career, vacancy, wage, salary
   - free, without paying, no cost, gratis

**Launch & Monitor**:
- Day 17-23: Monitor daily
- Target: 5 conversions in first week
- If 0 conversions after 7 days → Pause and investigate further

**Expected outcome**: New targeting should get 5-10 conversions in first week vs 1 conversion in 30 days

---

### Step 15: ROW Market Expansion (Day 17-18)

Current success: ROW Engineering gets £29 CPA
Opportunity: Test ROW Management

**Day 17 - Create ROW Management Campaign (1 hour):**

Copy existing "NMA | Search | ROW | Engineering 100" campaign:
1. Duplicate campaign
2. Rename: "NMA | Search | ROW | Management 50"
3. Budget: £15/day (test budget)
4. Change ad groups to Management keywords:
   - "motorsport management degree"
   - "MBA motorsport"
   - "motorsport business course"
   - "motorsport management MBA"
5. Update ad copy to mention Management not Engineering

**Day 18 - Add Smart Targeting:**
1. Enable AI Max (since it works on Engineering)
2. Add audience signals: Career changers, MBA searchers, business students
3. Set Target CPA: £100 (conservative)

**Monitor**: First 7 days, target 3 conversions minimum

**Expected outcome**: If ROW works for Engineering, should work for Management too

---

## Week 4: Scale & Optimize (Dec 2-8)

### Step 16: Budget Reallocation Based on Results (Day 22)

By now you should have 3 weeks of data on the fixes.

**Review performance:**
1. Calculate CPA for each campaign
2. Identify campaigns with CPA under £100
3. Identify campaigns with CPA over £200

**Reallocation formula:**

**Winners (CPA under £100):**
- Increase budget by 50%
- Monitor for 1 week
- If CPA stays under £150, increase another 25%

**Good (CPA £100-150):**
- Keep budget same
- Focus on Quality Score improvements

**Struggling (CPA £150-200):**
- Reduce budget by 25%
- Review search terms for negatives
- Check ad copy relevance

**Failing (CPA over £200):**
- Pause immediately
- Don't waste budget on non-performers

**Expected budget allocation after Week 4:**

| Campaign | Current Budget | New Budget | Rationale |
|----------|----------------|------------|-----------|
| ROW Engineering | £10/day | £80/day | £29 CPA is exceptional ✅ |
| Engineering PMax | £70/day | £100/day | £125 CPA after improvements |
| Engineering Search | £100/day | £60/day | £152 CPA, needs more work |
| Management PMax V2 | £20/day | £40/day | If getting 5-10 conv/week |
| Management Search | £20/day | £40/day | If CPA under £150 |
| ROW Management | £15/day | £30/day | If converting at £80-100 |

**Total budget**: £350/day = ~£10,500/month (vs current £8,100)

---

### Step 17: Advanced Optimizations (Day 23-28)

**Day 23 - Implement Ad Scheduling:**
1. Go to each campaign → Ad Schedule
2. Review performance by Hour of Day
3. If certain hours have 0 conversions but high spend:
   - Add bid adjustments: -50% for 0 conversion hours
   - +20% for high conversion hours

**Day 24 - Device Optimization:**
1. Review performance by Device
2. If mobile CPA is 2x+ higher than desktop:
   - Add -30% mobile bid adjustment
3. If tablet has 0 conversions:
   - Exclude tablets entirely

**Day 25 - Location Optimization:**
1. Go to Locations report
2. Check CPA by country (for ROW campaigns)
3. Exclude countries with 20+ clicks, 0 conversions
4. Increase bids +20% for countries with CPA under £50

**Day 26 - Remarketing List Creation:**
1. Go to Tools → Audience Manager
2. Create list: "NMA Website Visitors - Last 30 Days"
3. Add to all campaigns as "Observation" (bid adjustment +30%)
4. Past visitors 3x more likely to convert

**Day 27 - Competitor Conquest:**
1. Research competitor schools (e.g., other motorsport management courses)
2. Add competitor brand keywords:
   - [Competitor] alternative
   - [Competitor] vs NMA
   - Better than [Competitor]
3. Create dedicated ad group with comparison messaging
4. Budget: £10/day test

**Day 28 - Final Performance Review:**
1. Compare Week 4 to Week 1:
   - Conversions should be 2-3x higher
   - CPA should be 30-50% lower
   - Wasted spend should be eliminated
2. Create report for Paul Riley
3. Plan next month's optimization priorities

---

## Expected Results Timeline

### Week 1 Results:
- Conversions: 47.8 → 65 (pausing waste + CPC fix)
- CPA: £170 → £120
- Wasted spend: £2,500 → £500

### Week 2 Results:
- Conversions: 65 → 85 (ROW scaling + QS improvements)
- CPA: £120 → £95
- CTR improvements: +20% from better ads

### Week 3 Results:
- Conversions: 85 → 105 (PMax rebuild + expansion)
- CPA: £95 → £80
- Management campaigns starting to work

### Week 4 Results:
- Conversions: 105 → 130 (budget reallocation to winners)
- CPA: £80 → £65
- All campaigns profitable

### Month-End (Dec 8):
- **Conversions**: 47.8 → 130+ (2.7x increase)
- **CPA**: £170 → £65 (62% reduction)
- **Spend**: £8,100 → £10,500 (budget increased to winners)
- **Efficiency**: 10x improvement (2.7x volume at 0.38x cost)

---

## Quick Reference Checklist

### Daily Checks (5 mins/day):
- [ ] Check CPC on Engineering Search (should be £50-200, not £900+)
- [ ] Check conversions - are we trending toward 4+/day?
- [ ] Check any new search terms that need negative keyword adds
- [ ] Check ROW Engineering - still getting £30-50 CPA?

### Weekly Checks (30 mins/week):
- [ ] Quality Score improvements - any QS 5s moving to 6-7?
- [ ] Search terms report - any new winners to add as keywords?
- [ ] CPA by campaign - any over £200 that need pausing?
- [ ] Budget pacing - are winners limited by budget?

### Red Flags to Watch For:
🚩 CPC spikes above £500 → Bid strategy broke again
🚩 0 conversions for 3+ days → Check tracking
🚩 CTR drops below 5% on Search → Ads need refresh
🚩 Quality Scores dropping → Landing page issue

---

## Tools & Scripts Needed

### Google Ads Scripts to Set Up:

**1. CPC Alert Script:**
```javascript
// Alerts if any keyword CPC exceeds £200
// Run daily at 9am
```

**2. Zero Conversion Alert:**
```javascript
// Alerts if account gets 0 conversions for 24 hours
// Possible tracking issue
```

**3. Budget Pacing Script:**
```javascript
// Alerts if top campaigns hitting budget limits
// Time to increase budget on winners
```

### Spreadsheet Tracking:
Create Google Sheet: "NMA Weekly Performance Tracker"
- Columns: Week, Conversions, CPA, Spend, Top Performer, Issue Resolved
- Update every Monday
- Share with Paul Riley for transparency

---

## Communication with Client

### Week 1 Email (Nov 11):
"Paul - Found critical issues in NMA campaigns. Have paused 3 underperformers burning £2,500/month. Fixing CPC crisis on Engineering Search (currently £947 CPC, should be £50-200). Will update Friday with results."

### Week 2 Email (Nov 18):
"Paul - Week 1 fixes working. CPC down from £947 to £XXX. Scaled ROW Engineering (your best performer at £29 CPA). Added new assets to PMax. Conversions up XX%."

### Week 3 Email (Nov 25):
"Paul - Management campaigns rebuilt with better targeting. Early results: X conversions vs 1 previously. Landing page optimization request sent to Henry (critical for Management performance)."

### Week 4 Email (Dec 2):
"Paul - 4 week results: Conversions up from 47.8 to XXX, CPA down from £170 to £XX. Have reallocated budget to winning campaigns. Full report attached."

---

## Success Metrics

### Must Achieve (Minimum):
- ✅ Conversions: 47.8 → 90+ (2x increase)
- ✅ CPA: £170 → £100 (40% reduction)
- ✅ Engineering Search CPC: £947 → £200 (fix crisis)
- ✅ Eliminate £2,500/month wasted spend

### Target (Good Result):
- ✅ Conversions: 47.8 → 120 (2.5x increase)
- ✅ CPA: £170 → £70 (60% reduction)
- ✅ Engineering Search CPC: £947 → £100
- ✅ Management PMax: 1 → 20 conversions

### Stretch (Excellent Result):
- ✅ Conversions: 47.8 → 150+ (3x increase)
- ✅ CPA: £170 → £50 (70% reduction)
- ✅ All campaigns profitable (under £150 CPA)
- ✅ ROW markets outperforming UK

---

**Next Review**: December 8, 2025
**Owner**: Peter Empson
**Client Contact**: Paul Riley (pk@nda.ac.uk)
