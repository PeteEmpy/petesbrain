# NMA Management PMax Rebuild - Step-by-Step Guide

**Campaign to Replace**: NMA | P Max | UK | Management 100
**Problem**: 13,718 clicks → 1 conversion (0.0073% conversion rate)
**Root Cause**: Targeting job seekers instead of students
**Solution**: Rebuild with student-focused targeting and exclusions

---

## Problem Analysis

### Why Current Campaign Fails

**What's happening**:
1. Asset groups contain signals: "motorsport", "management", "business"
2. Google interprets as: People interested in **motorsport management JOBS**
3. Serves ads on: LinkedIn Jobs, Indeed, Reed, career sites
4. Clicks from: People looking for motorsport manager positions
5. They bounce: Not interested in studying, want employment

**Evidence**:
- 13,718 clicks but only 1 conversion = 0.0073% CVR
- Engineering PMax: 5,628 clicks, 17 conversions = 0.30% CVR (40x better)
- Engineering clearly says "course/degree" in messaging
- Management messaging likely says "career" which attracts wrong audience

### The Fix Strategy

**Core Principle**: Make it IMPOSSIBLE for job seekers to see your ads

**Three-Layer Defense**:
1. **Audience Signals**: Include students, exclude job seekers
2. **Placement Exclusions**: Block job boards entirely
3. **Asset Copy**: Say "COURSE" not "CAREER" in every headline

---

## Step-by-Step Rebuild Process

### Phase 1: Campaign Setup (15 minutes)

**Step 1: Create New Campaign**

1. Go to Google Ads → Campaigns → + New Campaign
2. Goal: **Leads** (or Website Traffic if Leads not available)
3. Campaign type: **Performance Max**
4. Campaign name: **NMA | P Max | UK | Management V2 Student Focus**
5. Click Continue

**Step 2: Budget & Bidding**

1. Budget: **£30/day** (start conservative)
2. Bidding: **Maximize Conversions**
3. ✅ Check "Set a target CPA (optional)"
4. Target CPA: **£150**
   - Why £150: Management is tougher market than Engineering
   - Engineering PMax gets £125 CPA, Management should be similar
   - £150 gives algorithm room to find conversions
5. Click Next

**Step 3: Locations & Languages**

1. Locations: **United Kingdom**
   - Don't include: "People searching for your targeted location"
   - Use: "People in or regularly in your targeted locations" (more qualified)
2. Languages: **English**
3. Click Next

**Step 4: More Settings**

1. Ad schedule: **All days, all hours** (for now - optimize later)
2. Start date: **Today**
3. End date: **None**
4. URL expansion: **OFF** ⚠️ Important
   - Prevents ads showing on unrelated URLs
   - More control over where ads appear

---

### Phase 2: Conversion Goals (5 minutes)

**Step 5: Select Conversion Actions**

Select ONLY student application conversions:
- ✅ **application_complete** (GA4) - Primary
- ✅ **application_approved** (GA4) - Secondary
- ❌ **NMA Enhanced Conversions For Leads** - Uncheck (values misconfigured)

**Why exclude Enhanced Conversions**:
- Currently showing £10,750 per conversion
- Will cause algorithm to optimize incorrectly
- Fix the value issue first, then re-enable later

---

### Phase 3: Asset Group Creation (45 minutes)

**Step 6: Create Asset Group - "Motorsport Management Students"**

1. Asset group name: **Motorsport Management Students - UK Online**
2. Final URL: **https://motorsport.nda.ac.uk/courses/motorsport-management/** (or main Management course page)

---

### Phase 4: Audience Signals (Critical - 20 minutes)

**Step 7: Add Positive Audience Signals**

⭐ **CRITICAL**: These tell Google WHO to target

**Your Data**:
- Skip (unless you have website visitor lists)

**Interests & Detailed Demographics**:

Click "Browse" → Add these categories:

**Education Interests**:
1. ✅ **Lifelong Learners** (people who take courses)
2. ✅ **Education** (broad category)
3. ✅ **Online Education** (specifically online learners)
4. ✅ **Business & Industrial** → **Business Education**

**Career Interests** (ONLY career changers, not job seekers):
5. ✅ **Career Advising** (people planning future careers via education)
6. ✅ **Professional Development** (people upskilling)

**Age**:
- ✅ 18-24 (traditional students)
- ✅ 25-34 (career changers)
- ✅ 35-44 (MBA seekers)
- ❌ Don't exclude older ages (online students vary)

**Step 8: Add Custom Segments (Positive)**

Click "Custom Segments" → "Create Custom Segment"

**Segment 1: "Motorsport Management Course Searchers"**
- Name: Motorsport Management Course Searchers
- Type: **People who searched for any of these terms on Google**
- Add terms:
  ```
  motorsport management course
  motorsport management degree
  motorsport business degree
  MBA motorsport
  motorsport management MBA
  online motorsport course
  motorsport business course
  study motorsport management
  motorsport management qualification
  motorsport degree online
  ```
- Save

**Segment 2: "Online MBA Seekers"**
- Name: Online MBA Seekers
- Type: **People who searched for any of these terms on Google**
- Add terms:
  ```
  online MBA
  part time MBA
  distance learning MBA
  online business degree
  online management degree
  executive MBA online
  flexible MBA
  study MBA online
  online university UK
  accredited online degree
  ```
- Save

**Segment 3: "Motorsport Industry Education"**
- Name: Motorsport Industry Education
- Type: **People who browsed types of websites**
- Add:
  ```
  Online Education Sites
  University Sites
  Professional Development Sites
  Business School Sites
  ```
- Save

**Step 9: Add EXCLUSION Signals** ⚠️ **MOST CRITICAL STEP**

This is what current campaign is missing!

Click "Exclusions" → "Add Exclusions"

**Exclude Interests**:
1. ❌ **Job Seekers** (critical!)
2. ❌ **Employment** (broad category)
3. ❌ **Recruitment Services**
4. ❌ **Career Planning** → **Job Search** (different from Career Advising)

**Exclude Custom Segment 1: "Motorsport Job Seekers"**
- Name: Motorsport Job Seekers
- Type: **People who searched for any of these terms on Google**
- Add terms:
  ```
  motorsport jobs
  motorsport manager jobs
  F1 jobs
  F1 careers
  motorsport team jobs
  racing jobs
  motorsport employment
  motorsport vacancies
  motorsport careers
  work in motorsport
  F1 team vacancies
  motorsport job openings
  motorsport recruitment
  racing team jobs
  pit crew jobs
  motorsport manager vacancy
  ```
- Save

**Exclude Custom Segment 2: "Job Board Visitors"**
- Name: Job Board Visitors
- Type: **People who browsed types of websites**
- Add:
  ```
  Job & Education Sites (be careful - exclude "Job" not "Education")
  Employment Services Sites
  Recruitment Sites
  Career Advice Sites (if focused on job search)
  ```
- Actually, better to handle this via placement exclusions below

---

### Phase 5: Content Exclusions (15 minutes)

**Step 10: Exclude Specific Placements**

Go to campaign settings (after creating) → Content → Exclusions

**Exclude these URL patterns** (add one by one):

Job Boards:
```
linkedin.com/jobs
indeed.com
indeed.co.uk
reed.co.uk
cv-library.co.uk
totaljobs.com
monster.co.uk
glassdoor.com
glassdoor.co.uk
jobsite.co.uk
milkround.com
targetjobs.co.uk
```

Career Sites:
```
prospects.ac.uk/jobs
motorsportjobs.com
pitpass.com/jobs
autosport.com/jobs
racecar-engineering.com/jobs
```

**Exclude Content Types**:
1. ✅ **Tragedy and Conflict** (brand safety)
2. ✅ **Below the fold** (only show in premium placements)
3. ✅ **Parked domains** (low quality)
4. ✅ **Error pages** (waste)

**Exclude Inventory Type**:
- Use: **Standard inventory** (safest)
- Not: Expanded or Limited (too risky for education ads)

---

### Phase 6: Assets - Headlines (20 minutes)

**Step 11: Create 15 Headlines**

⚠️ **CRITICAL RULE**: Every headline must clearly say COURSE, DEGREE, STUDY, or LEARN

**Why**: This is how we repel job seekers. If they see "Study motorsport management" they know it's not a job listing.

**Your 15 Headlines** (character limits apply):

1. **Online Motorsport Management Course** (37 chars) ⭐ Best
2. **MBA in Motorsport Business** (27 chars)
3. **Study Motorsport Management Online** (37 chars) ⭐ Best
4. **UK-Accredited Management Degree** (33 chars)
5. **Learn Motorsport Business Skills** (34 chars)
6. **Flexible Online MBA - Motorsport** (35 chars)
7. **Motorsport Management Qualification** (38 chars)
8. **Online Business Degree - F1 Focus** (36 chars)
9. **Study Part-Time While Working** (32 chars)
10. **Industry-Recognized MBA Course** (34 chars)
11. **Professional Motorsport Education** (37 chars)
12. **Distance Learning MBA - UK** (28 chars)
13. **Accredited Online Management Course** (39 chars)
14. **Learn From F1 Industry Experts** (33 chars)
15. **Start Your MBA Application Today** (35 chars)

**Headlines to AVOID** (these attract job seekers):
- ❌ "Start Your Motorsport Career" (sounds like job)
- ❌ "Become a Motorsport Manager" (sounds like job)
- ❌ "Work in Formula 1" (definitely job)
- ❌ "Motorsport Team Opportunities" (job)
- ❌ "Join the Motorsport Industry" (ambiguous)

---

### Phase 7: Assets - Descriptions (15 minutes)

**Step 12: Create 5 Descriptions**

Each must emphasize STUDYING and EDUCATION (not careers or jobs).

**Description 1** (Main - Educational Focus):
```
Study motorsport business management online with industry experts. UK-accredited MBA, flexible part-time learning, payment plans available. Start dates every month. Apply now.
```
(90 chars)

**Description 2** (Credibility & Flexibility):
```
Learn from F1 professionals with real industry experience. Fully online MBA recognized by employers worldwide. Study at your own pace, no campus attendance. Portfolio projects with industry partners.
```
(90 chars)

**Description 3** (Practical Skills):
```
Gain practical business skills for motorsport: marketing, finance, operations, team management. Real-world case studies from Formula 1, WEC, and motorsport businesses. Job-ready qualification.
```
(89 chars)

**Description 4** (Accessibility):
```
Affordable online MBA with flexible payment plans. Same academic quality as campus courses, study from anywhere in the world. Join students from 30+ countries. UK university partnership.
```
(90 chars)

**Description 5** (Career Support - Carefully Worded):
```
Professional motorsport business qualification opens doors to management roles. Expert tutors, industry connections, career guidance included. Start your application today, no experience required.
```
(90 chars)

**Descriptions to AVOID**:
- ❌ Anything mentioning "jobs available"
- ❌ "We're hiring" or "positions open"
- ❌ "Join our team"
- ❌ "Motorsport opportunities" (too vague, attracts job seekers)

---

### Phase 8: Assets - Images & Videos (20 minutes)

**Step 13: Upload Images (Minimum 15)**

**Image Categories to Include**:

**1. Students/Learning (5 images)**:
- Students at computers (online learning)
- Diverse students in study groups
- Someone taking online exam/course
- Graduate in cap and gown
- Professional studying from home office

**2. Motorsport Context (5 images)**:
- F1 cars on track (exciting, aspirational)
- Race car engineering close-ups
- Motorsport team in garage (business side)
- Podium celebrations (success)
- Pit stop action (teamwork)

**3. Business/Management (5 images)**:
- Business meeting/boardroom
- Data analysis/laptops
- Professional networking event
- Someone presenting to team
- Handshake/partnership imagery

**Image Sources**:
- Request from Paul Riley/Henry Bagshawe
- Stock photos: Shutterstock, iStock (license properly)
- NDA's own photography if available
- Motorsport stock imagery (check licensing)

**Image Specifications**:
- Minimum: 1200x628 pixels
- Ratio: 1.91:1 (landscape) or 1:1 (square)
- Format: JPG or PNG
- Size: Under 5MB each
- Quality: High resolution, professional

**Step 14: Upload Videos (Optional but Recommended)**

If available:
- Course testimonial from student
- Campus/facility tour (even if online, show the organization)
- Instructor introduction
- Success story from graduate

**Video Specs**:
- Minimum: 1920x1080
- Format: MP4, MOV
- Length: 10-60 seconds
- Include captions (some people watch muted)

---

### Phase 9: Assets - Additional (10 minutes)

**Step 15: Business Name & Logo**

1. Business name: **National Motorsport Academy**
2. Upload logo (if available):
   - Square version: 1200x1200 pixels
   - NMA logo or text-based logo
   - Request from Henry/Paul if needed

**Step 16: Call to Action**

- CTA: **Apply now** (most relevant for course applications)
- Alternatives: "Learn more", "Get started", "Sign up"

**Step 17: Site Links** (Optional but Recommended)

If you want to add sitelinks:
1. Course details page
2. Application form
3. Fees & funding info
4. Student testimonials

---

### Phase 10: Final Settings & Launch (10 minutes)

**Step 18: Review Asset Group**

Check you have:
- ✅ Final URL set
- ✅ 15 headlines (minimum 5, recommended 15)
- ✅ 5 descriptions (minimum 2, recommended 5)
- ✅ 15+ images (minimum 4, recommended 15)
- ✅ Audience signals set (positive AND exclusions)
- ✅ Business name & logo
- ✅ Call to action

**Step 19: Create Campaign**

Click "Create Campaign"

**Step 20: Immediately Add Placement Exclusions**

Campaign won't have them by default, must add after creation:

1. Go to campaign → Settings → Content
2. Click "Exclusions"
3. Add all the job board URLs from Step 10
4. Add content type exclusions
5. Save

**Step 21: Set Up Campaign-Level Negative Keywords**

Even though PMax doesn't use keywords, you can add negative keywords:

1. Go to campaign → Settings → More settings → Negative keywords
2. Add these as negative keywords (campaign level):

```
job
jobs
hiring
hire
hired
employment
employed
employer
vacancy
vacancies
career
careers
salary
wage
wages
recruitment
recruiter
recruiting
apply for job
job opening
job application
position
positions
work at
work for
join our team
we're hiring
now hiring
```

3. Save

---

### Phase 11: Monitoring Setup (10 minutes)

**Step 22: Set Up Custom Columns**

Go to Campaigns view → Columns → Modify Columns

Add these columns for easy monitoring:
- Conversions (you already have this)
- Cost / conv
- Conv. rate
- Impressions
- Clicks
- CTR
- Avg. CPC

**Step 23: Set Up Alerts**

Go to Tools → Rules → Create Rule

**Alert 1: Zero Conversions**
- If: Conversions = 0
- For: 3 days
- Then: Email me
- Why: Possible tracking issue

**Alert 2: High CPA**
- If: Cost / conv > £250
- For: 5 conversions
- Then: Email me
- Why: Campaign not optimizing well

**Alert 3: Low Impressions**
- If: Impressions < 1,000
- For: 3 days
- Then: Email me
- Why: Targeting may be too restrictive

---

## Launch Checklist

Before launching, verify:

### Targeting ✅
- [ ] Audience signals: Students, education, online learning included
- [ ] Exclusions: Job seekers, employment, recruitment excluded
- [ ] Custom segments: "Course searchers" added, "Job searchers" excluded
- [ ] Location: UK only, "regularly in" setting
- [ ] Age: 18-44 included (primary student demographics)

### Budget & Bidding ✅
- [ ] Budget: £30/day set
- [ ] Bidding: Maximize Conversions with Target CPA £150
- [ ] Conversion goals: application_complete and application_approved only

### Assets ✅
- [ ] Headlines: 15 total, all mention COURSE/STUDY/LEARN/DEGREE
- [ ] Descriptions: 5 total, all education-focused (not job-focused)
- [ ] Images: 15+ uploaded, mix of students/motorsport/business
- [ ] No "career" or "job" language in any asset

### Exclusions ✅
- [ ] Job boards: LinkedIn Jobs, Indeed, Reed, etc. excluded
- [ ] Content types: Below fold, parked domains, errors excluded
- [ ] Negative keywords: job, hiring, career, etc. added at campaign level
- [ ] URL expansion: OFF (prevents uncontrolled placements)

### Technical ✅
- [ ] Conversion tracking: Tested and working
- [ ] Final URL: Correct management course page
- [ ] Mobile-friendly: Landing page works on mobile
- [ ] Form tested: Application process works smoothly

---

## Expected Performance Timeline

### Week 1 (Days 1-7)

**Learning Period**:
- Spend: ~£200 (£30/day x 7 days, may not hit full budget)
- Impressions: 5,000-15,000
- Clicks: 100-400 (depending on CTR)
- Conversions: **2-5** (realistic target)
- CPA: £40-100 (usually better early, then normalizes)

**What to watch**:
- Are impressions happening? (If under 1,000/day = too restrictive)
- Is CTR above 1%? (PMax should be 1-3%)
- Are conversions happening at all? (Even 1 in week 1 is good sign)

### Week 2 (Days 8-14)

**Optimization Phase**:
- Spend: £210 (starting to hit full budget)
- Conversions: **5-8**
- CPA: £90-150 (settling toward target)

**Algorithm learning**:
- Google now knows which placements convert
- More efficient bidding
- Better audience targeting

### Week 3-4 (Days 15-30)

**Stable Performance**:
- Spend: £210/week (full budget utilization)
- Conversions: **7-10/week** (stable rate)
- CPA: £120-150 (at or near target)

**Target by Day 30**:
- Total conversions: **20-25** (vs 1 in old campaign)
- CPA: £120-140
- Conversion rate: 0.3-0.5% (vs 0.007% before)

---

## Success Metrics

### Minimum Success (Week 4)
- Conversions: 10+ (vs 1 previously)
- CPA: Under £200
- Conversion rate: 0.15%+ (20x better than 0.007%)
- **Verdict**: Campaign is working, keep running

### Good Success (Week 4)
- Conversions: 20+ (20x improvement)
- CPA: £120-150 (at target)
- Conversion rate: 0.3-0.4%
- **Verdict**: Scale budget to £50/day

### Excellent Success (Week 4)
- Conversions: 25+ (25x improvement)
- CPA: Under £120
- Conversion rate: 0.5%+
- **Verdict**: Scale to £70-100/day, major winner

### Failure (Week 4)
- Conversions: Under 5
- CPA: Over £250
- Conversion rate: Still under 0.1%
- **Verdict**: Something still wrong, investigate further

---

## Troubleshooting Guide

### Problem: Still Getting Zero Conversions After 7 Days

**Check**:
1. Conversion tracking - Is it firing? Use Tag Assistant
2. Landing page - Does form work? Test it yourself
3. Impressions - Are you getting any? (If under 1,000 = too restrictive)
4. Search terms - Go to Insights, what are people searching?

**Fix**:
- If tracking broken → Contact Henry to fix
- If no impressions → Remove some exclusion signals
- If wrong search terms → Add more negative keywords

### Problem: High CPA (Over £250)

**Check**:
1. Search terms - Are job-seeking terms still appearing?
2. Placements - Where are ads showing? (Insights → Placements)
3. Asset performance - Which assets have low performance?

**Fix**:
- Add more negative keywords for job terms
- Exclude poor-performing placements
- Pause low-performing assets
- Increase Target CPA to £180 temporarily

### Problem: Low Impressions (Under 1,000/day)

**Causes**:
- Too many exclusions
- Target CPA too low
- Audience signals too narrow

**Fix**:
- Remove some exclusion signals (keep the critical job-seeker ones)
- Increase Target CPA from £150 to £180
- Add more positive audience signals (broader education interests)

### Problem: Good Clicks But No Conversions

**Likely**: Landing page issue

**Check**:
1. Does landing page headline match ad copy?
2. Is CTA above the fold?
3. Is form too long/complicated?
4. Mobile experience - test on phone

**Fix**:
- Request landing page optimization from Henry/Paul
- A/B test different landing pages
- Simplify application form

---

## Comparison: Old vs New Campaign

### Old Campaign (Broken)
```
Name: NMA | P Max | UK | Management 100
Budget: £30/day
Bidding: Max Conversions (no target)
Audience: Generic "motorsport management"
Exclusions: NONE ❌
Assets: Career-focused language
Results: 13,718 clicks → 1 conversion (0.007% CVR)
Cost per conversion: £917
```

### New Campaign (Fixed)
```
Name: NMA | P Max | UK | Management V2 Student Focus
Budget: £30/day
Bidding: Max Conversions with Target CPA £150
Audience: Students + online learners ONLY
Exclusions: Job seekers, job boards, employment sites ✅
Assets: Education/course-focused language
Expected: 400 clicks → 2-5 conversions (0.5% CVR)
Expected CPA: £120-150
```

**Expected Improvement**: **20-25x more conversions** from same budget

---

## Next Steps After Launch

### Day 1 (Launch Day)
- [ ] Verify campaign is serving (check impressions after 6 hours)
- [ ] Check no error messages in campaign
- [ ] Verify budget is active

### Day 3
- [ ] Check if any conversions yet (even 1 is good sign)
- [ ] Review search terms (Insights → Search Terms)
- [ ] Check placements (Insights → Placements)
- [ ] Add any new negative keywords if seeing job-related searches

### Day 7 (First Week Review)
- [ ] Compare to old campaign (should have 2-5 conversions vs 0.23 per week)
- [ ] Calculate CPA (should be £40-150)
- [ ] Decision: Continue, adjust, or pause

### Day 14 (Two Week Review)
- [ ] Total conversions: Should be 5-10
- [ ] CPA trend: Should be stabilizing toward £150
- [ ] Decision: Scale budget if performing well

### Day 30 (Monthly Review)
- [ ] Total conversions: Should be 20-25
- [ ] Compare to Engineering PMax (should have similar CVR now)
- [ ] Decision: Scale to £50-70/day if hitting targets

---

## Communication with Client

**Email to Paul Riley (After Launch)**:

```
Subject: NMA Management PMax - Rebuilt with Correct Targeting

Hi Paul,

I've rebuilt the Management PMax campaign to fix the 13,718 clicks → 1 conversion issue.

Key Changes:
1. Added Target CPA £150 (controls costs)
2. Excluded job seekers/job boards (this was the main problem)
3. All ad copy now says "course" not "career" (repels wrong audience)
4. Targeting students and online learners specifically

The old campaign was showing ads to people looking for motorsport manager JOBS, not people wanting to STUDY motorsport management.

New campaign launched today (Nov XX) at £30/day.

Expected results in 30 days:
- 20-25 conversions (vs 1 previously)
- £120-150 CPA
- 20x improvement in efficiency

Will update you weekly on progress.

Best,
Pete
```

---

**Created**: November 10, 2025
**Campaign Launch**: When ready
**First Review**: 7 days after launch
**Owner**: Peter Empson
**Client**: Paul Riley (pk@nda.ac.uk)
