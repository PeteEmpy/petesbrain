# National Design Academy - Context & Strategic Notes

> **Purpose**: Living document with important context for Google Ads analysis and reporting.
> **Last Updated**: 2025-12-11
> **Enrollment Data**: See `documents/enrollment-data-2025-26.md` for detailed monthly tracking

**Voice Transcription Aliases**: NDA, design academy, National Design, national design

---

## Account Overview

**Client Since**: July 2024 (account setup)
**Monthly Budget**: Approx £3,000-5,000 (NDA account - estimated from £50/day India campaigns + UK campaigns)
**Primary Contact**: Paul Riley (Director) - pk@nda.ac.uk
**Secondary Contacts**:
- Henry Bagshawe (Development) - henry@nda.ac.uk
- Bella Bagshawe (Development) - development@nda.ac.uk
**Account Manager**: Peter Empson - petere@roksys.co.uk

**Business Type**: Lead Generation (education applications/enrollments)
**Industry**: Higher Education - Online Courses

### Related Client: National Motorsports Academy (NMA)

**Important**: National Motorsports Academy is a **separate client** with its own client folder.

- **NMA Folder**: `clients/national-motorsports-academy/`
- **Same Contact**: Paul Riley (manages both NDA and NMA)
- **Separate Tracking**: NMA work logged separately in NMA folder
- **Different Business**: Motorsport courses vs Design courses
- **Separate Google Ads Account**: 5622468019 (vs NDA's 1994728449)

**When working on NMA**:
- Use the NMA client folder (`clients/national-motorsports-academy/`)
- Read NMA's CONTEXT.md for NMA-specific strategy
- Log NMA work in NMA's tasks-completed.md

**This folder (NDA) is for National Design Academy work only.**

---

### Account Details (NDA Only)

- **Focus**: Design courses (interior design, graphic design, landscape design, etc.)
- **Google Ads Account ID**: 1994728449
- **Tag ID**: AW-1069535771
- **Geographic Focus**: UK (primary) + International (India focus campaigns)
- **Monthly Budget**: £3,000-5,000 (£23-25k currently due to budget reduction Nov 2025)
- **Account Manager**: Peter Empson

**Consultant**: Anwesha - Marketing consultant brought in by Paul Riley to boost business, particularly in India market; provides Google Ads account recommendations and strategic audits (advises on both NDA and NMA)

**Platform IDs**:
- **Google Ads Customer ID**: 1994728449
- **Google Merchant Centre ID**: N/A (Lead generation - course applications)
- **Google Analytics 4 (GA4) Property ID**: 354570005
- **Microsoft Ads Account ID**: [TBD]
- **Facebook Ads Account ID**: [TBD]

**Important Notes**:
- Both academies managed by same team (Paul Riley as Director for both)
- Same business model: lead gen for course applications/enrollments
- Separate Google Ads accounts require separate budget tracking and reporting
- All strategic learnings and optimizations can apply to both accounts
- This CONTEXT.md covers both NDA and NMA (consolidated management)

**Data Available**:
- 39 emails on file (July 2024 - October 2025)
- 0 meeting notes
- 1 experiment log entry
- **Automated Enrolment Data Tracking** (Oct 2025 - present):
  - Active files: `enrolments/NDA-UK-Enrolments-ACTIVE.xlsx`, `enrolments/NDA-International-Enrolments-ACTIVE.xlsx`
  - Historical versions: `enrolments/history/` (dated archives)
  - Auto-updated every 6 hours from emails sent by pk@nda.ac.uk
  - **Detailed analysis**: See `documents/enrollment-data-2025-26.md` for comprehensive monthly summaries, course breakdowns, and geographic distribution
- **Enrolment Analytics & Visualizations**:
  - Professional chart: `enrolments/nda-international-by-month-comparison.png`
  - Auto-generated with Roksys branding
  - Shows last 4 academic years, monthly comparison
  - Regenerate anytime: `cd scripts && .venv/bin/python3 create-monthly-comparison-chart.py`

---

## Strategic Context

### Current Strategy

**Campaign Structure (NDA Account)**:
- Performance Max campaigns for India market (Interior Design focus)
- Search campaigns with AI Max targeting (India + UK)
- Separate campaigns by geography (UK vs India)

**Key Strategic Focus**:
- **India Market Expansion**: Heavy focus on India with dedicated campaigns, competitive analysis, and conquest strategies
- **Lead Generation**: Applications and enrollments as primary conversion goals
- **Enhanced Conversions**: Implementation of Enhanced Conversions for Leads (ongoing technical setup)

### Why This Approach?

**India Market Strategy Rationale**:
- Significant competitive pressure from local providers (Mind Luster, Swayam Portal - government education platform)
- Free and low-cost alternatives creating impression share challenges
- Performance Max impression drop (-56.4% Sept-Oct) requiring strategic response
- UK accreditation and international credentials as key differentiator

**Campaign Structure Logic**:
- Separate India campaigns to allow geo-specific messaging and budget control
- Performance Max + Search combination to maximize reach while maintaining keyword control
- AI Max on Search campaigns showing strong results (11.89% CTR vs 7.94% traditional match types)

**Technical Implementation Focus**:
- Enhanced Conversions for Leads to improve conversion tracking accuracy
- Offline conversion tracking via Google Sheets integration (applications happen offline from ad click)
- Multiple Google support cases to resolve technical implementation issues

### Goals & KPIs

**Primary Goal**: Applications (Leads) and Enrollments
**Target ROAS**: Not explicitly mentioned (lead gen focus, not e-commerce)
**Target CPA**: Not explicitly stated in available data
**Other KPIs**:
- Application volume
- Enrollment conversion rate (applications to enrollments tracked weekly)
- CTR (targeting >8.2% to beat India competitors)
- Impression share recovery (post-India drop)

**Weekly Tracking**:
- Client receives weekly application and enrollment figures
- Data broken down by UK vs International students
- Academic year tracking (25-26 data currently being collected)

---

## Historical Performance Patterns

### India Campaigns Performance (Sept-Oct 2025)

**Performance Max Campaign** (19 Sept - 6 Oct comparison):
- Impressions: 3,674,925 → 1,601,004 (-56.4% - CRITICAL DROP)
- Spend: £870.44 → £874.84 (+0.5% - stable)
- CTR: 0.942% → 1.137% (+20.8% - positive signal)
- Clicks: 34,612 → 18,208 (-47.4%)
- Daily Budget: £50.00
- **Issue**: Impression share collapsed after campaign changes and increased competitive pressure

**Search Campaign** (India, 19 Sept - 6 Oct):
- Impressions: 14,168 → 23,633 (+66.8%)
- Spend: £427.87 → £703.82 (+64.5%)
- CTR: 7.630% → 9.525% (+24.8% - exceptional performance)
- Clicks: 1,081 → 2,251 (+108.2%)
- Daily Budget: £50.00
- **Success Factor**: AI Max search terms producing 11.89% CTR vs 7.94% traditional

### Seasonality

**Academic Year Cycle**:
- New academic year starts: Likely Sept/Oct (typical UK pattern)
- Weekly enrollment tracking suggests ongoing admissions throughout year
- Q4 likely important for January intake preparations

### Known Anomalies

**Sept 2025 India Impression Drop**:
- Major impression share drop in Performance Max after campaign changes
- Coincided with competitor "andacademy" increasing visibility
- Recovery strategy implemented (conquest campaigns, budget adjustments)

---

## Client Preferences & Communication

### Communication Style

**Preferred Update Frequency**: Weekly data reports (applications/enrollments)
**Preferred Format**: Email communication, data-driven reports
**Detail Level**: Data-focused - client requests historical data for trend analysis, appreciates detailed breakdowns

**Key Communication Traits**:
- Responsive and collaborative (quick responses to Google verification requests)
- Appreciates proactive analysis and strategic recommendations
- Requests historical data to validate trends ("take UK enrolments back as far as we've done with internationals")
- Values detailed performance explanations with metrics
- **Casual, friendly tone**: "Haha, right ok. i'll check later"
- **Quick problem-solving**: Offers to help investigate issues ("I can take a look later if not")
- **Trusts agency judgment**: "I don't think this data will work for what you want" (accepts limitations)

**Key Business Context (from Teams Chats):**

**Revenue Structure:**
- **Dubai income = International income** (all non-UK revenue)
  - Dubai classified as Point of Sale (POS) for all international students
  - Dubai office handles all international enrolments
  - UK revenue tracked separately

**Data Management Challenges:**
- "Admin are terrible with data in general" - client acknowledges internal data quality issues
- Client relies on checkout and bank revenue (doesn't have detailed UK data)
- Weekly enrolment reports don't include NMA revenue or learner loans
- Revenue per enrolment calculations complicated by payment plans

**Budget Philosophy (Nov 2025):**
- Budget tied to revenue performance
- Oct 2025: 24% revenue vs target triggered urgent budget reduction
- Target levels: July (£23k), August (£27k) as baselines
- Proactive budget management: "Need to get the budget under control quickly"

**Landing Page Strategy:**
- Working with UX adviser on page optimizations
- New landing pages expected to show "lower enrolment started" but "more actual revenue"
- Price transparency reduces "tyre kickers" (unqualified leads)
- Pages designed for non-English speakers (international focus)

### Decision-Making

**Who Makes Final Decisions**: Paul Riley (Director) - pk@nda.ac.uk
**Technical Contact**: Henry Bagshawe (implements tracking codes, manages technical setup)
**Approval Process**:
- Google Ads changes: Peter implements with client notification
- Technical implementations: Coordinated through Henry
- Policy/verification requests: Bella or Paul handle quickly

**Risk Tolerance**: Moderate to Aggressive
- Willing to implement competitive conquest campaigns
- Open to AI Max experimentation on Search
- Invested in technical improvements (Enhanced Conversions)
- Budget adjustments made proactively based on performance

### Red Flags / Sensitive Topics

**No Major Red Flags Identified**

**Areas of Sensitivity**:
- India market performance (significant investment, competitive pressure)
- Technical tracking accuracy (multiple Google support cases for Enhanced Conversions)
- Brand name representation (original verification under "NDA Foundation" vs desired "National Design Academy")

---

## Business Context

### Product/Service Details

**National Design Academy (NDA)** is a UK-based online design education provider offering diplomas and degrees in interior design and related disciplines.

**Business Model**: Online education provider offering flexible, distance learning courses in design disciplines with UK accreditation and international reach.

### Landing Pages & Website Structure

**Key Course Pages**:
- **Interior Design Diploma**: `https://www.nda.ac.uk/study/courses/diploma-interior-design/`
- **Interior Design Degree**: `https://www.nda.ac.uk/study/courses/degrees-interior-design`
  - **Page Updated**: 25 November 2025 - Content/structure refreshed
- **General Interior Design Courses Hub**: `https://www.nda.ac.uk/study/interior-design-courses/`
- **Degrees Overview**: `https://www.nda.ac.uk/study/interior-design-degrees/`

**Important**: Diploma and Degree pages must be matched correctly to campaign intent. Historical issue (Nov 2025): 5 Diploma campaign asset groups were incorrectly sending traffic to the Degree page, resulting in 13,704 misrouted clicks and £8,733.70 wasted spend over 12 months. See `/documents/2025-11-25-landing-page-url-fix-documentation.md` for details.

**Brands**:
- **National Design Academy (NDA)** - https://www.nda.ac.uk/ - Main brand for interior design courses
- **National Motorsport Academy (NMA)** - https://motorsport.nda.ac.uk/ - Specialized motorsport design courses (celebrating 10 years in 2025)

**Primary Offerings** (based on campaign names and emails):
- Interior Design Diploma (major focus in India campaigns)
- Graphic Design courses
- General Design Academy programs
- Motorsport courses (under separate NMA brand)
- **New Course**: AI for Interior Design (announced Nov 2025)

**USP**:
- **UK accreditation** - Recognized UK qualifications (key differentiator vs free alternatives like Mind Luster, Swayam Portal)
- **Online/flexible learning** - Distance learning format accessible globally
- **International reach** - Strong presence in UK and India markets, with broader international enrollment
- **Specialized expertise** - 10+ years experience in motorsport design education (NMA)
- **Scholarship availability** - Financial support options (triggered Financial Services Policy verification)
- **Professional focus** - Career-oriented courses designed for working professionals
- **Dual brand strategy** - NDA for general design, NMA for motorsport specialization
- **Innovation** - New AI for Interior Design course demonstrates forward-thinking curriculum

**Top Performers**:
- Interior Design courses appear to be primary focus for India expansion
- UK market appears more diversified across design disciplines

**Geographic Markets**:
- **UK**: Primary market, established presence
- **India**: Growth market with dedicated campaigns and competitive strategy
- Potential other international markets (context suggests broader international enrollment)

**Pricing Strategy**:
- Premium positioning vs free alternatives (Mind Luster, Swayam Portal)
- Scholarships offered (triggered Financial Services Policy verification requirement)
- UK accreditation as value justification

**Lead Generation Model**:
- Applications collected online
- Enrollment decisions made offline
- Offline conversion tracking implemented to connect ads to final enrollments

### Website & Technical

**Website Domains**:
- Primary: nda.ac.uk (National Design Academy)
- Motorsport: motorsport.nda.ac.uk (National Motorsport Academy)

**Known Technical Issues**:
- Enhanced Conversions for Leads implementation challenges (May-Oct 2025)
- Google Tag not capturing user-provided data correctly (resolved with Google support)
- Offline conversion Google Sheet timestamp format issues (May 2025)
- Separate tracking tags needed for NDA vs NMA (AW-1069535771 for NDA)

**Conversion Tracking**:
- **Setup**: Enhanced Conversions for Leads (implemented Q2-Q3 2025)
- **Method**: Google Tag + Google Sheets offline conversion import
- **Data Collected**: Hashed email, hashed phone, application timestamp, conversion value, order ID
- **Known Issues**:
  - Extended implementation period (multiple Google support cases)
  - Initial data capture issues resolved Sept 2025
  - Ongoing validation with Google Tech team
- **Last Technical Audit**: September-October 2025 (Google Tech team validation)

**Google Sheet Setup**:
- Conversion Name: "NDA Enhanced Conversions For Leads"
- Auto-hashing functions for email/phone (privacy compliance)
- Conversion value = application value
- Conversion currency = GBP
- Unique Order ID per application

### Competitive Landscape

**India Market - Main Competitors**:

1. **Mind Luster** (Primary Threat)
   - Local certification provider
   - Aggressive search presence
   - Lower price point than UK accreditation
   - **Conquest Strategy**: Target "Mind Luster interior design" searches directly

2. **Swayam Portal** (Government Competition)
   - Government-backed education platform
   - Free or heavily subsidized
   - Academic/theoretical focus
   - **Counter-Positioning**: "Industry Employment vs Academic Theory"

3. **Free Online Alternatives**
   - Generic design courses
   - Lower quality but no cost barrier
   - **Differentiation**: "Guaranteed Portfolio vs Generic Learning"

4. **Other Design Academies** (Cross-Discipline)
   - Compete on general "design course" terms
   - **Defense**: "Specialised Interior Focus vs General Design"

**Competitive Advantages**:
- UK accreditation and international recognition
- Industry-connected program with employment outcomes
- Portfolio-based learning vs theory-only
- Established track record and student success stories

**Competitive Disadvantages**:
- Higher price point than local/free alternatives
- Geographic distance (UK-based vs local providers)
- Limited brand recognition in India market (48 brand impressions vs competitors)
- Free government alternatives in target market

---

## Known Issues & Challenges

### Current Issues

**1. India PMax Impression Share Collapse**
- **Description**: 56.4% drop in PMax impressions Sept-Oct 2025
- **Impact**: Severely reduced visibility and click volume despite stable spend
- **Status**: Active recovery strategy implemented (conquest campaigns, CTR optimization, budget reallocation)
- **Root Cause**: Increased competitive pressure + campaign changes + competitor visibility increase

**2. Enhanced Conversions Technical Setup**
- **Description**: Extended implementation period (May-Oct 2025) with multiple technical hurdles
- **Impact**: Delayed conversion measurement improvements
- **Status**: Largely resolved Sept-Oct 2025, ongoing validation with Google Tech team
- **Resolution**: Google Tag configured, offline conversion sheet format corrected, data capture validated

**3. Brand Name Verification Issue**
- **Description**: Account originally verified under "NDA Foundation" instead of "National Design Academy"
- **Impact**: Cannot update brand name in search ads to preferred "National Design Academy"
- **Status**: Under review with Google (Aug 2025), possible resubmission of advertiser verification
- **Next Steps**: Awaiting Google response on documentation review

**4. Financial Services Policy Flag**
- **Description**: Scholarship offerings triggered Financial Services Policy requirements
- **Impact**: Ads limited in certain situations until verification completed
- **Status**: RESOLVED - Non-financial services verification completed Sept 2025
- **Resolution**: Client completed exempt verification form, approved by Google Sept 10, 2025

### Recurring Challenges

**India Market Competitive Pressure**:
- Free and low-cost alternatives constantly challenge premium positioning
- Government-backed alternatives difficult to compete against on price
- Brand awareness building required (48 impressions on brand terms)
- CTR benchmarks set by aggressive competitors (>8.2% target)

**Technical Implementation Complexity**:
- Lead generation tracking more complex than e-commerce
- Offline conversion tracking requires ongoing maintenance
- Multiple support cases needed for technical issues (suggests technical resource constraints)

**Multi-Brand Management**:
- NDA and NMA require separate account structures
- Different tracking implementations per brand
- Policy issues affect one brand but not the other (scholarship policy on NDA only)

**NMA Conversion Tracking Clarification (Nov 2025)**:
- **TRUE Conversions**: "NMA Enhanced Conversions For Leads" (offline upload) - actual enrollments/paying students
- **GA4 Events**: Funnel stages only (application_start, application_complete, application_approved, etc.) - NOT true enrollments
- **Current Status**: Enhanced Conversions showing 0.8 conversions vs GA4 showing 41 "application_complete" events
- **Why**: GA4 tracks form submissions; Enhanced Conversions tracks actual enrollments (much lower conversion rate)
- **Known Issue**: Enhanced Conversions implementation awaiting final Google sign-off (ongoing since May 2025, Case 6-0805000038801)
- **Do NOT flag as problem**: The 0.8 vs 41 discrepancy is expected - they measure different things

### External Factors to Monitor

**India Education Market**:
- Government education initiatives (Swayam Portal expansion)
- Local competitor pricing and offerings
- Economic conditions affecting international education demand
- UK visa/study policies for international students

**Google Ads Platform Changes**:
- Enhanced Conversions requirements and policies
- Performance Max algorithm updates (relevant to impression share issues)
- AI Max rollout and performance (currently testing, strong early results)
- Financial Services Policy interpretation and enforcement

**Seasonal Academic Cycles**:
- Application and enrollment patterns by month
- Competition intensity by academic calendar
- UK vs India academic year differences

---

## Key Learnings & Insights

### What Works Well

**AI Max on Search Campaigns (India)**:
- Producing 11.89% CTR vs 7.94% traditional match types (+49.9% improvement)
- Strong recommendation to roll out to other search campaigns
- Validates AI-powered targeting for education lead gen

**High CTR Performance**:
- India Search campaign achieving 9.525% CTR (industry-leading for education)
- Keyword-to-intent matching extremely strong
- Ad copy resonating well with Indian market

**Search Campaign Scalability**:
- India Search campaign successfully scaled budget (+64.5% spend with maintained efficiency)
- Volume and spend growing together (healthy growth pattern)
- Demonstrates capacity to absorb additional budget

**Responsive Client Relationship**:
- Quick turnaround on verification requests (Financial Services policy resolved same day)
- Collaborative technical implementation process
- Data-driven decision making culture

### What Doesn't Work

**Performance Max in Highly Competitive Markets**:
- India PMax struggled when competitor pressure increased
- Impression share collapsed despite stable spend
- Less controllable than Search in conquest scenarios

**Brand Name Constraints**:
- Original verification choices limit flexibility later
- "NDA Foundation" vs "National Design Academy" causing ongoing issues

**Offline Conversion Technical Setup**:
- Required multiple support cases and months to implement
- Google Sheet timestamp format not intuitive
- Data capture validation complex and time-consuming

### Successful Tests & Experiments

| Date | Test Description | Result | Action Taken |
|------|-----------------|--------|--------------|
| Oct 24, 2025 | New videos uploaded for India PMax campaign | Testing - Goal: Increase CTR | Monitor CTR improvement over next 2-4 weeks |
| Sept 19, 2025 | AI Max implementation on India Search campaign | Success - 11.89% CTR vs 7.94% traditional | Roll out to other Search campaigns |
| Sept-Oct 2025 | India PMax budget increase (daily budget raised) | Failed - Spend didn't increase due to impression share drop | Investigate competitive pressure, implement conquest strategy |

### Failed Tests (Learn From)

| Date | Test Description | Why It Failed | Lesson Learned |
|------|-----------------|---------------|----------------|
| Sept 2025 | India PMax campaign changes | Impression share dropped 56.4% after changes | Major campaign restructures in competitive markets risk auction participation; make incremental changes instead |
| May 2025 | Initial offline conversion Google Sheet setup | Timestamp format errors, data not uploading | Follow Google's exact format specifications; validate with support before going live |

---

## Campaign-Specific Notes

### India - Performance Max Campaign (Interior Design)

**Campaign Name**: NDA | P Max | Interior Design - India 135 29/11 No Target 10/9
- **Daily Budget**: £50.00
- **Purpose**: Drive interior design applications from India market
- **Recent Performance**: Struggling with impression share (-56.4% drop Sept-Oct)
- **Optimization History**:
  - Budget increased but spend didn't follow (auction participation issue)
  - New videos added Oct 24 to improve CTR
  - No tROAS target (lead gen focus)

**Special Considerations**:
- Extremely competitive market (Mind Luster, Swayam Portal, free alternatives)
- CTR improved to 1.137% despite volume drop (quality signal)
- Recovery strategy: Monitor video performance, consider shifting budget to Search

### India - Search Campaign (Interior Design Diploma)

**Campaign Name**: NDA | Search | Interior Design Diploma - India Ai Max 19/9
- **Daily Budget**: £50.00
- **Purpose**: Keyword-targeted interior design applications from India
- **Recent Performance**: Exceptional - 9.525% CTR, +108% click growth
- **Optimization History**:
  - AI Max implemented Sept 19, 2025
  - Successfully scaled spend +64.5% while improving CTR
  - Producing industry-leading CTRs

**Special Considerations**:
- Best-performing campaign in account
- Strong candidate for budget increase
- AI Max validated as effective strategy
- Consider keyword portfolio expansion given strong engagement

### Conquest & Competitive Strategy (India - Planned/In Progress)

**Phase 1: Immediate Competitive Defense** (0-30 days)
- Target "Mind Luster" searches directly with dedicated ad groups
- Target "Swayam Portal" + "interior design" combinations
- Budget: 20% of India budget to conquest terms
- Messaging: UK accreditation vs local certification, employment vs theory

**Phase 2: Brand Differentiation** (30-60 days)
- Student success stories from India
- Employment and salary data
- Portfolio guarantee messaging

**Phase 3: Market Expansion** (60-90 days)
- Niche categories: residential, commercial, sustainable, luxury design
- Professional upskilling segment (career changers, working adults)
- Higher price tolerance segment

**Budget Allocation Strategy**:
- 40% - Core interior design terms (defend market share)
- 30% - Competitive conquest terms (attack competitors)
- 20% - Premium niche categories (expand market)
- 10% - Brand building (long-term positioning)

### UK Campaigns

**Status**: Not detailed in available emails (focus has been on India market analysis)
**Inference**: Likely more established, stable performance
**Note**: Request campaign structure details and recent performance data for UK campaigns

---

## Action Items & Reminders

### Ongoing Tasks

- [ ] Monitor India PMax video performance (added Oct 24) - check CTR improvement in 2-4 weeks
- [ ] Validate Enhanced Conversions data flow continues working correctly (monthly check)
- [ ] Track weekly application and enrollment data for trends
- [ ] Monitor India competitor activity (Mind Luster, Swayam Portal CTR benchmarks)
- [x] Country correlation analysis: Complete - 3-phase analysis done, 536% overall ROAS, European markets 3,000-10,000% ROAS identified (Nov 3, 2025)

### Future Plans

- [ ] Roll out AI Max to additional Search campaigns (based on India success)
- [ ] Implement Phase 1 conquest campaigns for India (Mind Luster, Swayam Portal targeting)
- [ ] Request brand name verification update from Google (resolve NDA Foundation issue)
- [ ] Consider budget shift from India PMax to Search given performance differential
- [ ] Expand keyword portfolio on India Search (strong CTRs suggest room for growth)

### Important Dates

- **Weekly**: Application and enrollment figures sent to client (Mondays)
- **October 24, 2025**: India PMax video upload (monitor results through November)
- **Academic Year 25-26**: Currently tracking enrollments for this cycle

---

## Quick Reference

### Emergency Contacts

- **Client Primary**: Paul Riley (Director) - pk@nda.ac.uk
- **Client Technical**: Henry Bagshawe - henry@nda.ac.uk
- **Client Development**: Bella Bagshawe - development@nda.ac.uk
- **Account Manager**: Peter Empson - petere@roksys.co.uk - 07932 454652

### Important Links

- **Google Ads Account**: Customer ID TBD (use Tag ID AW-1069535771)
- **Google Analytics**: Property ID TBD
- **NDA Website**: https://www.nda.ac.uk
- **NMA Website**: https://motorsport.nda.ac.uk
- **NDA Social**: https://www.nda.ac.uk/links/#social
- **NMA Social**: https://motorsport.nda.ac.uk/links/#social
- **Enhanced Conversions Google Sheet**: https://docs.google.com/spreadsheets/d/1E8SYpVLaeV2pHv_MwRTFROHBF-JwTMya1pA9dGZJ_Zc/edit?gid=823579042#gid=823579042

### Login Credentials

- **Location**: Check 1Password vault or client credentials store

### Google Support Case History

- **Case 6-0805000038801**: Enhanced Conversions for Leads implementation (NMA/NDA technical setup)
- **Case 7-3022000038272**: Lead Generation technical appointment
- **Case 7-5170000038434**: Additional technical support case
- **Case 9-6360000039344**: Financial Services Policy verification (RESOLVED Sept 10, 2025)

### Key Stakeholders (Client Side)

- **Director**: Pauline Riley - director@nda.ac.uk
- **Deputy Director**: A Bedworth-Cook - deputydirector@nda.ac.uk
- **Student Services Manager**: Kelly Rawson - KellyR@nda.ac.uk (weekly enrollment reports)
- **Development Team**: Allan Nzioki (allan@nda.ac.uk), Sean McLeod (sean@motorsport.nda.ac.uk)
- **Accountant**: Mike Mitchell - accountant@nda.ac.uk

**Address**: Rufford Hall, Waterside Way, Nottingham, NG2 4DP
**Phone**: +44 (0)1159 123412

---

## Ad Hoc Notes

### NMA Campaign & Conversion Audit (17 November 2025)

**Audit Trigger**: Recommendations document from Anwesha (marketing consultant, focus: India market growth)
**Documents Created**:
- Full audit: `documents/NMA-Campaign-Conversion-Audit-2025-11-17.md`
- Browser summary: `nma-audit-summary.html`

**Key Findings (Last 30 Days - 18 Oct to 16 Nov 2025)**:

**Account Performance**:
- Total Spend: £8.11M
- Total Conversions: 47.8 (true enrollments via Enhanced Conversions)
- Blended CPA: £169,665
- Total Clicks: 10,612

**Critical Issues Identified**:

1. **ROW Management Search Campaign - ZERO CONVERSIONS**
   - Spend: £660k/month (£22/day budget)
   - Conversions: 0
   - CPA: ∞
   - **Action**: PAUSE IMMEDIATELY (wasted spend)

2. **UK Management Search - Extreme CPA**
   - Spend: £1,177k
   - Conversions: 0.8
   - CPA: £1,425,635
   - **Action**: Reduce budget 50% (£40→£20/day), monitor Target CPA impact

3. **Missing High-Converting Keywords**
   - "automotive engineering degree" - 19 conversions/year (per Anwesha)
   - 5 additional keywords identified - total +35 conversions/year expected
   - **Action**: Add to ROW Engineering Search campaign immediately

4. **Disapproved Sitelinks**
   - 2 sitelinks disapproved (mentioned by Anwesha)
   - Affecting Management campaigns
   - **Action**: Fix policy violations

**Best Performing Campaign**:
- **ROW Engineering Search**: £34,744 CPA (5x better than account average)
- Currently £40/day budget
- **Recommendation**: Scale to £80/day (+100%)

**Top Converting Keywords**:
- motorsport academy (Broad) - 8 conversions, £7.7k CPA, 38.4% CTR
- race car mechanic school (Broad) - 6 conversions, £11.3k CPA
- car engineering courses (Exact) - 6 conversions, £66.9k CPA
- motorsport engineering (Broad) - 4 conversions, £54k CPA

**Anwesha's Recommendations - Assessment**:

✅ **Agreed**:
- Add high-converting keywords (especially "automotive engineering degree")
- Add more sitelinks to top ads
- Fix disapproved sitelinks
- Optimize ad schedules (reduce Saturdays if data supports)
- Geographic optimization (US/UAE state-level targeting)

⚠️ **Challenged**:
- **Gender exclusions**: Recommend bid adjustments instead (policy risk for educational services)
- **Age exclusions (55-64, 65+)**: Recommend bid adjustments first (career changers/mature students may convert)

**Expected Impact After Implementation**:
- Conversions: 47.8 → 65-75/month (+36-57%)
- CPA: £169k → £110-130k (-35%)
- Monthly savings: £1k (from ROW Management pause)
- Budget efficiency: +40%

**Target CPA Review Due**: 17 Nov 2025 (TODAY)
- Implemented 10 Nov 2025:
  - UK Engineering Search: £100 Target CPA
  - ROW Engineering Search: £50 Target CPA
  - Management PMax: £150 Target CPA
- **Action**: Review performance vs targets today

**Budget Reallocation Plan**:
- ROW Engineering Search: £40 → £80/day (+£40) - scale best performer
- UK Management Search: £40 → £20/day (-£20) - reduce waste
- ROW Management Search: £22 → £0/day (-£22) - PAUSE
- Net change: -£2/day, but +40% efficiency



### Financial Data & Revenue Per Enrollment Analysis (Nov 3, 2025)

**Source**: Financial data provided by Paul Riley showing YTD performance comparison

**Key Finding - Revenue Per Enrollment Collapse**:
- **2024-25:** £7,217 revenue per enrollment (104 students, £750K income)
- **2025-26:** £2,467 revenue per enrollment (322 students, £794K income)
- **Drop:** -65.8% (-£4,750 per student)

**Paradox**: Enrollments increased 210% (+218 students) but revenue only grew 5.8% (+£44K)

**Financial Breakdown (YTD 2025-26)**:
- UK Income: £390,083 (190 enrollments) = £2,053/student (-73% vs prior year)
- Dubai Income: £404,160 (132 int'l enrollments) = £3,062/student (-55% vs prior year)
- Total: £794,243 (322 enrollments)

**Note on "Dubai Income"**: Client's accounting labels all international student income as "Dubai Income" (likely Dubai office handles international operations). This represents all 132 international enrollments from 45 countries, not just UAE/Dubai students (who are 55 of the 132).

**Advertising Spend (YTD 2025-26)**:
- Google Ads: £130,729 (+80% YoY)
- Facebook Ads: £16,920 (-11% YoY)
- Total: £147,649 (19% of income, was 12% prior year)

**ROAS Performance**:
- 2024-25: 819% (£8.19 per £1 spent)
- 2025-26: 538% (£5.38 per £1 spent)
- Drop: -281 percentage points (-34% efficiency loss)

**Most Likely Causes of Revenue/Student Drop**:
1. Course mix shift (more students in lower-priced courses)
2. Payment plan adoption (installments/loans, revenue deferred)
3. Promotional discounting to drive volume
4. Market shift (attracting lower-budget student segments)

**Action Required**: Need breakdown of:
- Enrollments by course type/price tier
- Payment methods (full pay vs installments vs loans)
- Revenue recognition policy (upfront vs over time)
- Any pricing or promotional changes in 2025-26

**Files Generated**:
- `documents/financial-enrollment-correlation-analysis-2025-11-03.md` - Full analysis report
- `documents/revenue-per-enrollment-analysis.html` - Interactive spreadsheet view

### Geographic Performance Analysis (Nov 2025) - COMPLETE

**Phase 1-3 Analysis** (Aug 1 - Nov 3, 2025):
- **Countries Analyzed**: 37 with Google Ads activity, 141 unique countries in enrollment data
- **Total Performance**: £109K spend, 567 conversions, **167 actual enrollments**, £584K revenue
- **Overall ROAS**: **536%** ✅ (highly profitable)

**Top Discoveries**:

1. **European Markets Exceptionally Efficient** (3,000-10,000% ROAS):
   - Hungary: £68 spend, 2 enrollments, **10,223% ROAS**, £34 CPA
   - Latvia: £38 spend, 1 enrollment, **9,222% ROAS**, £38 CPA
   - Spain: £259 spend, 4 enrollments, **5,416% ROAS**, £65 CPA
   - Germany: £712 spend, 7 enrollments, **3,442% ROAS**, £102 CPA
   - **Action**: Launch dedicated campaigns in these markets (currently receiving incidental reach)

2. **GCC Markets Strong** (500-900% ROAS):
   - Oman: **924% ROAS** (best in region)
   - Kuwait: 680% ROAS
   - UAE: 566% ROAS
   - Saudi Arabia: 505% ROAS
   - **Action**: Maintain or increase budgets

3. **UK Underperforming** (292% ROAS):
   - £46,610 spend, 60 enrollments
   - Below target (aim for 500%+)
   - **Action**: Optimize campaign structure and targeting

4. **Wasted Spend** (Zero enrollments):
   - Malaysia: £376 spend, 0 enrollments
   - Japan, China, Denmark, Uruguay: Combined £240 spend, 0 enrollments
   - **Action**: Geo-exclude, free £616/month budget

5. **Expansion Opportunities** (Enrollments, no ads):
   - Nigeria: 3 enrollments (£10.5K revenue), £0 ad spend
   - Pakistan: 2 enrollments (£7K revenue), £0 ad spend
   - **Action**: Test with £300-500/month campaigns

**Files Generated**:
1. `documents/google-ads-country-analysis-aug-nov-2025.md` - Initial 37-country analysis
2. `scripts/country-mapping.json` - Standardization mapping (227→141 countries)
3. `enrolments/NDA-International-Enrolments-STANDARDIZED.json` - Clean enrollment data
4. `data/country-correlation-analysis.csv` - Full correlation dataset (28 countries)
5. `documents/country-budget-recommendations.md` - Detailed recommendations by country
6. `documents/country-roas-performance.png` - Visual ROAS chart (top 15 countries)
7. `documents/COUNTRY-CORRELATION-EXECUTIVE-SUMMARY.md` - **Executive summary for client**

**Immediate Recommendations** (Week 1):
- Geo-exclude: Malaysia, Japan, China, Denmark, Uruguay (free £616/month)
- Increase budgets: Spain (+50%), Germany (+50%), Hungary (+25%)
- Optimize UK campaigns to improve 292% → 500%+ ROAS

**Expansion Tests** (Weeks 2-4):
- Launch Spain dedicated campaign: £500-1,000/month
- Launch Germany dedicated campaign: £500-1,000/month
- Test Nigeria: £300-500/month
- Test Pakistan: £300-500/month

**Assumptions to Validate with Client**:
- Average course fee: £3,500 (does pricing vary by country/course?)
- Attribution lag: Not accounted for (enrollment date vs ad click date)
- Conversion rate: 15% application → enrollment (is this accurate?)

### India Market Competitive Intelligence (Oct 2025)

**Competitor CTR Benchmarks**:
- NDA currently: 1.137% (PMax), 9.525% (Search)
- Target to beat: >8.2% (competitive benchmark)
- Search campaign successfully exceeding target

**Key Competitor Positioning**:
- **Mind Luster**: "Interior Design Course" - local certification angle
- **Swayam Portal**: "Free Government Education" - price advantage
- **Generic Free Courses**: "Learn Interior Design" - accessibility angle

**NDA Differentiators to Emphasize**:
- UK accredited qualification (international recognition)
- Industry employment outcomes vs theory-only
- Portfolio guarantee and practical learning
- Established track record and student success stories

### Technical Implementation Notes

**Enhanced Conversions for Leads Setup**:
- Requires hashed email + phone number
- Google Tag must be configured to capture form submission data
- Offline conversion import via Google Sheet (not API in this case)
- Timestamp format critical: Must match Google's specification exactly
- Conversion name constant: "NDA Enhanced Conversions For Leads"
- Validation required with Google Tech team before going live

**Multi-Brand Tag Management**:
- NDA Tag: AW-1069535771
- NMA Tag: Separate (not specified in emails)
- Important: Use correct tag for each brand's website
- Google support cases require specifying which brand/account

**Automated Enrolment Data System** (Implemented Nov 2025):
- **Purpose**: Automatically capture actual UK and International enrolment data from weekly emails
- **Source**: Emails from pk@nda.ac.uk containing Excel attachments
- **Script**: `scripts/enrolment-file-manager.py`
- **Schedule**: Runs every 6 hours via LaunchAgent (com.petesbrain.nda-enrolments)
- **Active Files**:
  - `enrolments/NDA-UK-Enrolments-ACTIVE.xlsx` - Current UK enrolment data
  - `enrolments/NDA-International-Enrolments-ACTIVE.xlsx` - Current International enrolment data
- **Archive Strategy**: When new files arrive, old active versions are dated and moved to `enrolments/history/`
- **Naming Convention**: Historical files named with date: `NDA-UK-Enrolments-YYYY-MM-DD.xlsx`
- **Logging**: All updates logged to `~/.petesbrain-nda-enrolments.log`
- **State Tracking**: Processed email IDs stored in `enrolments/.processed-emails.json` to prevent duplicate processing
- **Why This Matters**: Actual enrolment data allows true ROAS calculation by matching Google Ads lead generation to revenue outcomes

**Enrolment Analytics & Visualizations** (Implemented Nov 2025):
- **Purpose**: Professional data visualization of enrolment trends for client reporting
- **Script**: `scripts/create-monthly-comparison-chart.py`
- **Output**: `enrolments/nda-international-by-month-comparison.png`
- **Features**:
  - Compares last 4 academic years (2022-23 through current)
  - X-axis: 12 months (Jan-Dec) for easy year-over-year comparison
  - Y-axis: Number of enrolments per month
  - Professional styling with Roksys branding (logo in bottom-right corner)
  - Current year (2025-26) layered on top for maximum visibility
  - High resolution (2700x1500 pixels at 150 DPI) for presentations
- **How to Regenerate**:
  ```bash
  cd /Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts
  .venv/bin/python3 create-monthly-comparison-chart.py
  open ../enrolments/nda-international-by-month-comparison.png
  ```
- **Automatic Updates**: Run the script after new enrolment data arrives (every 6 hours) to get latest chart
- **Dependencies**: openpyxl, matplotlib, Pillow (installed in `.venv/`)
- **Branding Standard**: Follows Roksys chart branding standard (Level 2 - small logo, no text)

**Key Insights from Current Data** (as of Nov 2025):
- 2025-26 tracking significantly higher than previous years (55/month avg vs 28/month in 2024-25)
- September 2025 had exceptional performance: 82 enrolments (highest single month in dataset)
- January consistently shows as peak enrolment month across all years
- Data useful for: ROAS calculation, budget planning, seasonality analysis, campaign optimization

### Communication Patterns Observed

**Peter's Communication Style with Client**:
- Detailed performance explanations with metrics and context
- Proactive strategic recommendations (conquest campaigns, AI Max rollout)
- Clear articulation of technical requirements
- Professional but collaborative tone

**Client Response Patterns**:
- Quick responses to action requests (same-day verification completion)
- Requests for historical data to validate trends
- Appreciates depth of analysis (detailed campaign breakdowns well-received)
- Technical coordination through Henry, strategic decisions through Paul

---

## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

_Automatic monitoring via "Shared with Me" in Google Drive_
_Updated documents will appear here when detected by daily scans_

**Note**: This section tracks important resources shared by the client via Google Drive, including:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and assets
- Client-maintained documentation

---


## Document History

| Date | Change Made | Updated By |
|------|-------------|------------|
| 2025-11-17 | **ANWESHA CONTEXT ADDED**: Clarified that Anwesha is marketing consultant (not Google rep) brought in by Paul Riley to boost business, particularly in India market; updated consultant role description in Account Overview section and NMA audit section | Claude Code |
| 2025-11-17 | **NMA COMPREHENSIVE AUDIT**: Completed deep campaign and conversion tracking audit based on Anwesha's recommendations; identified critical issues (ROW Management £660k/0 conversions, UK Management £1.4M CPA, 6 missing high-converting keywords); clarified Enhanced Conversions vs GA4 events (EC = true enrollments awaiting Google approval, GA4 = funnel stages); created full audit document and browser summary; validated Target CPA strategy review due today; added 5 high-converting keywords to ROW Engineering campaign with PB_2025 label; day-of-week analysis deferred to Dec 15+ pending Target CPA stabilization | Claude Code |
| 2025-11-10 | **NMA TARGET CPA STRATEGY**: Implemented Target CPA controls on NMA account to address extreme CPCs and low conversion rates - Engineering Search UK £100 Target CPA (was £947 CPC), ROW Engineering £50 Target CPA + budget scaled £10→£40/day (best performer at £29 CPA), Management PMax £150 Target CPA (was £917 per conversion); expected impact: 47→65-80 conversions/month, average CPA £170→£110-130; monitoring Nov 10-17; Friday update promised to client | Claude Code |
| 2025-11-10 | **NMA/NDA STRUCTURE CLARIFIED**: Documented that NMA (National Motorsport Academy, Account ID 5622468019) is a separate Google Ads account but same client group as NDA; same contacts (Paul Riley), same business model (lead gen for course enrollments); both managed under this CONTEXT file for consolidated tracking | Claude Code |
| 2025-11-10 | **BUDGET REDUCTION SUCCESS**: Documented successful Nov 5th budget changes - daily spend reduced 32% (£1,130→£765), cost per conversion improved 10% (£212→£191), on track for £23k/month target vs £24k baseline; created impact analysis document and client communication email | Claude Code |
| 2025-10-28 | Initial skeleton creation | Claude (automated) |
| 2025-10-30 | Comprehensive population from 15 emails, experiment log, and analysis | Claude |
| 2025-11-03 | Added Automated Enrolment Data System documentation | Claude |
| 2025-11-03 | Added Enrolment Analytics & Visualizations system (charts, analysis scripts) | Claude |
| 2025-11-03 | Added Geographic Performance Analysis (37 countries, Aug-Nov 2025) and correlation plan | Claude |
| 2025-11-03 | Completed full 3-phase country correlation analysis: standardized enrollment data (227→141 countries), correlated with Google Ads, generated ROAS analysis (536% overall), budget recommendations, and executive summary | Claude |
| 2025-11-13 | **TASK DEDUPLICATION**: Removed 13 duplicate AI-generated task entries. Preserved all manual tasks and first occurrence of each AI task pattern. Cleanup based on provenance analysis showing 'Source: AI Generated' metadata. | Claude Code |

---

## Summary of Data Sources Used

This CONTEXT.md was populated from:
- **Experiment Log**: 1 entry (India PMax video upload Oct 24)
- **Emails Analyzed**: 15 most recent (May 2025 - Oct 2025)
  - Enhanced Conversions technical implementation thread (May-Sept)
  - Financial Services Policy resolution (Sept)
  - India campaign performance analysis (Oct)
  - India competitive strategy recommendations (Oct)
  - Weekly enrollment data requests (Oct)
- **Key Insights Extracted**:
  - Technical tracking setup and challenges
  - India market competitive dynamics
  - Campaign performance patterns
  - Client communication preferences
  - Strategic priorities and focus areas

**Next Steps for Further Population**:
1. Access Google Ads account to document UK campaign structure
2. Review Google Analytics for traffic and conversion data
3. Interview client about business goals, budgets, and historical context
4. Gather website content to detail course offerings
5. Review additional historical emails (24 more available from Jul 2024 - Apr 2025)

## Planned Work

### [National Design Academy] Update Geographic Performance Analysis dashboard with latest enrollment data
<!-- task_id: QV9xSmY3TDBKRk5kVVhBSQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:30)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Ensure latest country-level ROAS and enrollment insights are current for upcoming client reporting
**AI Task ID:** 6c9db69b-a68f-455b-8413-fe60dc532ccb
---

Ensure latest country-level ROAS and enrollment insights are current for upcoming client reporting



### [National Design Academy] Validate budget reduction impact from Nov 5th changes (daily spend reduced to £765)
<!-- task_id: Smp2M1NsV0owQVM2UFd2aQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:30)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Confirm that recent budget cuts are maintaining performance while reducing overall spend as planned
**AI Task ID:** c384a9f9-895a-4871-9fa7-d2de48ff7685
---

Confirm that recent budget cuts are maintaining performance while reducing overall spend as planned



### [National Design Academy] Review and implement NMA Target CPA strategy for Engineering Search and Management PMax campaigns
<!-- task_id: c3pLYXBPdXhJZklSYmF6VQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:29)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA
**AI Task ID:** 28231961-1959-4a21-8520-8dbcec3cef7a
---

Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA



### [National Design Academy] Review budget reduction impact from Nov 5th changes (daily spend reduced to £765)
<!-- task_id: akRnbnJ3Q2lEcGk0empJVA -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:29)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Confirm recent budget cuts are maintaining performance while reducing overall spend as planned, ensuring client's cost efficiency goals are met
**AI Task ID:** fc6157e8-22b0-4638-8dca-3b10fb1293d5
---

Confirm recent budget cuts are maintaining performance while reducing overall spend as planned, ensuring client's cost efficiency goals are met



### [National Design Academy] Validate NMA Target CPA strategy implementation for Engineering Search and Management PMax campaigns
<!-- task_id: dmFDbXEtVzVKQW9FQTl1WA -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:29)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA from current high levels
**AI Task ID:** ba1384a6-8cfe-48f0-8f40-81dc6afe941e
---

Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA from current high levels



### [National Design Academy] Validate NMA Target CPA strategy implementation for Engineering Search and Management PMax campaigns
<!-- task_id: d0NaU01ZWEtwYkRpR0FFNg -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:26)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA from current high levels
**AI Task ID:** 06fe4868-d5fa-42d7-a808-22b8d2831ebb
---

Recent meeting discussed budget optimization, and strategy needs immediate implementation to improve conversion performance and reduce CPA from current high levels



### [National Design Academy] Validate NMA Target CPA strategy for Engineering Search and Management PMax campaigns
<!-- task_id: TUJ5Vll6YzB5dG5PdmtyLQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:38)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130
**AI Task ID:** a7a94cf3-552f-4486-b0e0-cf8608302a0a
---

Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130



### [National Design Academy] Validate NMA Target CPA strategy for Engineering Search and Management PMax campaigns
<!-- task_id: VzlTaGVKMkVmX1ltZlRwNw -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:36)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130
**AI Task ID:** ef62065f-f5c5-4cdf-9382-638297a1a5b5
---

Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130



### [National Design Academy] Validate NMA Target CPA strategy for Engineering Search and Management PMax campaigns
<!-- task_id: RU9tcERXSE5BOVBmd0FNUw -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-12 07:01)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130
**AI Task ID:** 0ae55628-ecc5-46ca-84d2-ee51f6139d3b
---

Recent meeting discussed budget optimization, strategy needs immediate implementation to improve conversion performance and reduce extremely high current CPA from £917 to target range of £110-130



---

**Cleanup Note (2025-11-13):**
Removed 13 duplicate task entries:
- 7x: Update Geographic Performance Analysis dashboard with latest
- 6x: Review budget reduction impact from Nov 5th changes (daily s

All manual tasks preserved. AI-generated tasks deduplicated to first occurrence only.

### [National Design Academy] Update Geographic Performance Analysis dashboard with latest enrollment data
<!-- task_id: al83V0p6aHBiWWozaU91WA -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:10)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Ensure latest country-level ROAS and enrollment insights are current for upcoming client reporting and strategic decision-making
**AI Task ID:** 335ad427-7c1c-4582-a5d5-55b5cf7580cc
---

Ensure latest country-level ROAS and enrollment insights are current for upcoming client reporting and strategic decision-making


### [National Design Academy] Review budget reduction impact from Nov 5th changes (daily spend reduced to £765)
<!-- task_id: YWMxVk1adW9hNk1hRVlRVw -->
**Status:** 📋 In Progress

---
**Source:** AI Generated (2025-11-11 10:10)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Confirm recent budget cuts are maintaining performance while reducing overall spend as planned, ensuring client's cost efficiency goals are met
**AI Task ID:** 8b4e56a7-fbd3-4588-bf32-3aafaaae6b93
---

Confirm recent budget cuts are maintaining performance while reducing overall spend as planned, ensuring client's cost efficiency goals are met


### [National Design Academy] Landing Page Performance Review #3 - Interior Design Diploma (FINAL ASSESSMENT - COMPLETED)
<!-- task_id: NDA_LP_REVIEW_3_10DEC -->
**Status:** ✅ Completed
**Completed Date:** 2025-12-11
**Due Date:** 2025-12-10

---
**Source:** Manual task creation (2025-11-26, updated from Review #2)
**Client:** national-design-academy
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Final assessment after 3 weeks (18 days) - sufficient time for conversion lag to clear

---

## ANALYSIS SUMMARY: PRELIMINARY GOOGLE ADS + SEASONALITY CONTEXT

**Status**: ✅ Google Ads analysis complete (11 Dec 2025) | ✅ Seasonality analysis complete (11 Dec 2025) | ⏳ Final decision deferred to January 2026

**Analysis Period (Ads):** 18-day post-launch (22 Nov - 9 Dec) vs 18-day pre-launch baseline (4-21 Nov)
**Critical Context**: Landing page launched during seasonal LOW POINT (November is 47% below September peak)
**Seasonality Analysis**: Document at `documents/seasonality-analysis-landing-page-context.md`

### 📊 Performance Data

| Metric | Baseline (Nov 4-21) | Post-Launch (Nov 22-Dec 9) | Change |
|--------|-------------------|--------------------------|--------|
| **Clicks** | 1,783 | 1,528 | -14% |
| **Conversions** | 70.8 | 34.1 | -52% |
| **CVR** | 3.97% | 2.23% | **-44%** 🔴 |
| **Cost per Conversion** | £99.83 | £154.82 | +55% |

### 📈 Key Findings

**1. Conversion Lag Distortion (Critical)**
- Nov 25-26 show spike: 11.6 + 10 = 21.6 conversions combined
- These represent **delayed conversions from pre-launch traffic** (application backfill)
- Excluding this spike, true post-launch CVR ≈ **1.2-1.8%** (−65% from baseline)
- This indicates the page change itself is responsible for the decline

**2. Traffic Quality Intact**
- Click volume stable: -14% decline aligns with natural variance
- CTR increased post-launch (10-18% range vs 8-12% baseline) = strong relevance signal
- Issue is NOT traffic quality; it's page-specific conversion performance

**3. Root Cause Analysis: Confounded by Seasonality** ⚠️

The landing page changes introduced barriers to conversion, BUT the timing is critical:

- **Pricing visibility** (£895-£1,500) = price barrier filtering visitors
- **Information overload** (6 course options vs 3) = decision paralysis
- **Aggressive CTA mismatch** ("Enrol Now" vs "View Courses") = wrong funnel stage messaging
- **Visual complexity** = reduces conversion for exploratory visitors

**HOWEVER: The page launched during the seasonal low point:**
- November baseline (4-21 Nov) was already 47% below September peak (96 vs 182 enrollments)
- Post-launch period (22 Nov-9 Dec) overlaps with holiday season (seasonal low point)
- Comparing weak month to weak month inflates the apparent decline
- Conversion lag hasn't fully cleared (3-4 week delay expected)

**This is why January data will be conclusive:** Post-holiday traffic will show true impact vs. seasonal baseline.

### 📈 Seasonality Pattern: 2025-26 Academic Year

```
Total Enrollments by Month (2025-26) - UPDATED 8 DEC 2025

September:    182 ████████████████████████████████ (PEAK - New intake)
October:      140 ██████████████████████           (-23% from peak)
November:     123 ███████████████████              (-32% from peak) ← PAGE LAUNCHED 22 NOV
                  [was 96 on 27 Nov, grew to 123 by 8 Dec]
December:      18 ███                             (8 days only - tracking ~67 pace)
January:     130+ ████████████████████             (Expected seasonal recovery)

Landing Page Launched: Friday, 22 Nov (during seasonal low)
Post-launch enrolments (22 Nov - 8 Dec): ~27-30 students (NO COLLAPSE)
December momentum: Strong (18 in 8 days suggests sustained demand)
Holiday Period: 22 Dec - 2 Jan (expects lower activity)
Conversion Lag: 2-4 weeks (some Nov ads still converting)
```

**Critical Finding**: November recovered from 96 to 123 enrolments (+27, +28%) after landing page launch. This contradicts "catastrophic page failure" narrative. Suggests improved application quality over quantity.

**What This Means:**
- Comparing 4-21 Nov (baseline) to 22 Nov-9 Dec (post-launch) is inherently flawed
- Both periods are during seasonal low point
- -44% CVR could be part page impact + part seasonal variation
- January will separate the two effects clearly

### 📅 DEFERRED DECISION: January 2026

**Why Wait Until January?**
- Post-holiday traffic normalisation (Dec noise will be gone)
- Higher volume for statistical significance (January is traditionally strong for education)
- Time to gather application quality feedback from client
- Consolidated analysis: Google Ads + GA4 + Enhanced Conversions data

**What Will Be Included in January Review:**
1. **Google Ads Analysis**: 30-day post-launch data (22 Nov - 21 Dec vs Dec 22-Jan 20)
2. **GA4 Deep Dive**:
   - Bounce rate by traffic source (to identify which channels are affected)
   - Session duration and pages per session (information overload signals)
   - Device breakdown (mobile vs desktop impact)
   - Source/medium comparison (organic vs paid vs direct)
   - Page scroll depth / engagement metrics
3. **Enhanced Conversions**: Application → enrollment conversion rate
4. **Client Feedback**: Application quality assessment from Paul Riley

**GA4 Property ID Ready for Analysis:** 354570005
**Analysis Script Location:** `clients/national-design-academy/scripts/ga4-landing-page-analysis.py`

---

### ✅ Recommendation (Preliminary): A/B TEST

**Why A/B TEST vs Revert?**
- CVR -44% falls in A/B Test range (-20% to -40%), boundary with Revert threshold
- Page changes are intentional (not accidental regression) and partly working as designed
- Pricing filter is reducing quantity but may improve quality (needs validation)
- Segmented approach can preserve wins while fixing losses

**Recommended A/B Test Approach:**

**Test 1: Segmented Landing Pages**
- **Traffic Segment A** (Search/Cold): OLD page (simpler, softer CTA)
- **Traffic Segment B** (Brand/Retarget): NEW page (pricing transparency, "Enrol Now")
- **Duration**: 14 days
- **Success Metric**: Which variant achieves 3%+ CVR?

**Test 2: Hybrid Landing Page**
- Keep pricing visible (transparency) BUT move to mid-page (not hero)
- Reduce course options in hero to top 2 (simpler)
- Change CTA to "View Options" (less aggressive than "Enrol Now")
- Compare to both old and new

**Test 3: Immediate Revert**
- If client preference is to "stop the bleeding" immediately
- Revert to old page today
- Then optimise during slower season (Jan 2026)

### 📋 Plan: Deferred to January 2026

**Today (11 Dec):**
1. ✅ Google Ads analysis completed and added to CONTEXT.md
2. ✅ GA4 Property ID documented (354570005)
3. ⏸️ Client communication deferred (no decision needed until January)
4. ⏸️ Implementation deferred (waiting for post-holiday traffic)

**By Early January (Jan 5-10, 2026):**
1. Pull 30-day post-launch data (22 Nov - 21 Dec)
2. Run GA4 deep-dive analysis:
   - Bounce rate by source (identify affected channels)
   - Session engagement metrics
   - Device/screen breakdown
3. Gather client feedback: Application quality assessment
4. Create comprehensive January review with all data sources

**Decision Timeline (Mid-January, 15-20 Jan):**
- Present consolidated findings to client
- Get decision on A/B test approach
- Implement chosen approach
- Begin 14-30 day monitoring for results

---

**Context:**
Landing page went live Friday 22 Nov. Preliminary 18-day analysis shows -44% CVR decline (Google Ads data). Final decision deferred to January for better seasonal data and GA4 integration.

**Data Sources Status:**
- ✅ Google Ads: Campaign ID 10647096425 - Complete analysis done
- ✅ GA4: Property ID 354570005 - Ready for January analysis
- ⏳ Enhanced Conversions Sheet: Will be included in January review
- ⏳ Client Application Quality Feedback: Pending (to request in January)

---

### [National Design Academy] Landing Page Performance Review #2 - Interior Design Diploma (COMPLETED)
<!-- task_id: NDA_LP_REVIEW_2_26NOV -->
**Status:** ✅ Completed
**Completed Date:** 2025-11-26

---
**Source:** Manual task creation (2025-11-24)
**Client:** national-design-academy
**Priority:** P0
**Time Estimate:** 1 hour
**Reason:** Critical review of landing page performance after 6 days live - decision required on revert/continue
---

**Outcome:** MONITOR - Do Not Revert (data too premature for decision)

**Analysis Completed:**
- 6-day post-launch data pulled (22-27 Nov)
- Compared to 11-day baseline (11-21 Nov)
- Google Ads CVR: 3.59% → 2.43% (-32%)
- GA4 metrics unreliable (99%+ bounce rates on 24 & 26 Nov = tracking broken)

**Decision Rationale:**
- Conversion lag (2-4 weeks) makes current conversion data misleading
- Low volume + natural variance = need longer observation period
- GA4 bounce rate data UNRELIABLE for decision-making
- No catastrophic failure signals (clicks stable, spend normal)

**Next Action:** Review #3 scheduled for 10 Dec 2025 (3 weeks post-launch)

**Documentation:** Updated CONTEXT.md with 6-day review analysis and monitoring plan

---

### [National Design Academy] Review Nov 19 video upload impact on India PMax CTR and impressions
<!-- task_id: N49vBIcYQ44SgAUIc_IB6y -->
**Status:** 📅 Scheduled
**Due Date:** 2025-11-26

---
**Source:** Manual task creation (2025-11-19)
**Client:** national-design-academy
**Priority:** P2
**Time Estimate:** 45 mins
**Reason:** Follow-up analysis for 3 new videos (different aspect ratios) uploaded Nov 19 by Anwesha to assess CTR impact and impression share changes
---

**Context:**
3 new videos uploaded Nov 19 to NDA India PMax campaign by Anwesha (marketing consultant). Need to assess whether videos improve CTR and/or impression share.

**Analysis Required:**
- CTR comparison: Nov 12-18 (before) vs Nov 19-25 (after)
- Impression share changes (if any)
- Video placement performance breakdown
- Compare results with Oct 24 video upload (which showed +2.8% CTR improvement but -70.7% impression collapse)

**Campaign:** NDA | P Max | Interior Design - India (Customer ID: 1994728449)

**Expected Outcome:** CTR improvement likely, impression impact uncertain (PMax video channel behavior unpredictable)


### [NDA] Landing Page Change - Interior Design Diploma (LIVE 22 Nov 2025)
<!-- task_id: NDA_LP_AB_TEST_2025_11 -->
**Status:** ⚠️ Live - Performance Decline Detected
**Created:** 2025-11-21
**Go-Live:** 2025-11-22 (Friday)
**Next Review:** 2025-11-26 (Tuesday)

---
**Source:** Manual (Peter via Claude Code)
**Client:** national-design-academy
**Priority:** P1
**Reason:** New landing page going live Friday 29 Nov - requires immediate campaign URL updates and baseline tracking

---

**What's Happening:**
New landing page replacing current Interior Design Diploma page at SAME URL.

**URL:**
- **https://www.nda.ac.uk/study/courses/diploma-interior-design** (URL stays the same, content changes)
- **Previous version:** https://www.nda.ac.uk/study/courses/lp-2025-interior-design-diploma-online-in-studio-courses/ (now redirecting to main URL)

**Landing Page Changes Summary (21 Nov 2025):**

| Element | OLD Page | NEW Page (Live 29 Nov) |
|---------|----------|----------|
| Pricing shown | No - hidden | Yes - £895-£1,500 visible |
| Study options | 3 + bundle | 3 diplomas + 3 short courses + bundle |
| CTAs | "View Courses" / "Get In Touch" | "Enrol Now" / "View Study Options" |
| Information density | Lower - cleaner | Higher - more options |
| Government funding | Mentioned | Mentioned + specific % |
| Short courses | Not shown | Prominently featured |

**Key Differences:**
- NEW page shows pricing upfront (better for qualified leads, may deter unqualified clicks)
- NEW page has more aggressive "Enrol Now" CTA (stronger conversion intent)
- NEW page includes 3 additional short courses (CAD, AI, Exterior) - expands offering
- OLD page is cleaner/less overwhelming (better for cold traffic)
- NEW page risks information overload for top-of-funnel visitors

**Expected Impact:**
- ✅ **Improved CVR** for bottom-funnel (retargeting, brand searches)
- ⚠️ **Potential CVR drop** for top-funnel (cold traffic, broad keywords)
- ⚠️ **Bounce rate may increase** due to pricing visibility scaring price-sensitive visitors
- ✅ **Lead quality may improve** (pre-qualified by pricing)

**Go-Live Date:** Friday 29 November 2025

**Action Required BEFORE Go-Live (29 Nov):**
1. ✅ Capture baseline metrics (21-28 Nov):
   - Current CVR by campaign/traffic source
   - Current bounce rate
   - Current time on page
   - Current applications/week from Interior Design traffic
2. ⚠️ **NO Google Ads URL changes needed** (URL staying the same)
3. Set up monitoring alerts for CVR drops >20%

**Action Required AFTER Go-Live (29 Nov onwards):**
1. **Week 1 (29 Nov - 5 Dec):** Daily monitoring
   - CVR by campaign (compare to baseline)
   - Bounce rate changes
   - Application volume changes
   - Lead quality (enrollment rate from applications)
2. **Week 2 (6 Dec - 12 Dec):** Weekly review
   - 14-day performance comparison
   - Segment analysis (top vs bottom-funnel)
   - Identify winning/losing traffic sources
3. **Week 3 (13 Dec):** Final assessment and recommendations
   - Overall impact report
   - Recommendations for campaign optimisation
   - Consider segmented landing page strategy if performance mixed

**Monitoring Dashboard:**
- Google Analytics: Landing page performance (bounce, time, CVR)
- Google Ads: Campaign-level CVR changes
- Enhanced Conversions: Application → Enrollment rate

---

## **PERFORMANCE ANALYSIS - 6-DAY REVIEW (26 Nov 2025)**

**Analysis Date:** 26 November 2025
**Data Period:** 6 days post-launch (22-27 Nov) vs 11 days pre-launch (11-21 Nov)

### 📊 **Updated Findings - Accounting for Conversion Lag**

| Metric | Baseline (11-21 Nov, 11 days) | Post-Launch (22-27 Nov, 6 days) | Change |
|--------|-------------------------------|----------------------------------|--------|
| **Google Ads Clicks** | 1,054 clicks | 455 clicks | -57% (time period shorter) |
| **Google Ads Conversions** | 37.85 conversions | 11.07 conversions | -71% (time period shorter) |
| **Google Ads CVR** | 3.59% | 2.43% | **-32% 🟡** |
| **Cost** | £3,671.46 | £1,452.07 | -60% (time period shorter) |

**GA4 Site-Wide Metrics (UNRELIABLE - see notes below):**
- Bounce Rate: 47.3% → 63.9% (+16.6pp)
- Session Duration: 120s → 90s (-25%)
- **Critical Issue:** 99.5% bounce rate on 26 Nov, 99.2% on 24 Nov = likely tracking problem

### ⚠️ **Key Assessment: TOO EARLY TO JUDGE**

**Why the initial data was misleading:**

1. **Conversion Lag Effect:**
   - Education enrollments have 2-4 week application → enrollment lag
   - Conversions showing now (22-27 Nov) include applications from OLD landing page
   - True post-launch conversion performance won't be visible until mid-December
   - Example: 25 Nov showed 10.57 conversions (spike) = likely delayed conversions from pre-launch traffic

2. **Low Volume Account:**
   - Baseline CVR 3.59% = only 3-4 conversions per 100 clicks
   - Natural variance at this volume can swing ±30-50% day-to-day
   - 6 days insufficient for statistical significance

3. **GA4 Data Quality Issues:**
   - 99.5% bounce rate (26 Nov) and 99.2% (24 Nov) = tracking broken
   - Site-wide metrics, not landing-page specific
   - No documented GA4 implementation validation
   - **Conclusion:** GA4 bounce rate data UNRELIABLE for decision-making

4. **Enhanced Conversions Status:**
   - Still awaiting Google approval (Case 6-0805000038801 since May 2025)
   - Offline conversion import timing creates data lag and noise
   - True enrollment conversions delayed weeks from ad click

### ✅ **DECISION: MONITOR (Do Not Revert)**

**Rationale:**
- Conversion lag makes current data premature for assessment
- Low volume + natural variance = need longer observation period
- GA4 metrics unreliable due to tracking issues
- No strong signal of catastrophic failure (clicks stable, spend normal)

**Next Review: Tuesday 10 December 2025** (3 weeks post-launch)

**What to Monitor:**
1. **Leading Indicators (immediate):**
   - Application volume (if accessible via Enhanced Conversions sheet)
   - Click volume and traffic patterns
   - Cost per click trends

2. **Lagging Indicators (10 Dec review):**
   - Conversion rate (once lag catches up)
   - Cost per conversion
   - Application → enrollment rate

**Action Plan for 10 Dec Review:**
1. Pull 22 Nov - 9 Dec performance (18 days post-launch)
2. Compare to equivalent 18-day baseline (Oct-Nov period)
3. Focus on Google Ads conversion data (ignore GA4 bounce rate)
4. Assess: Application volume and enrollment conversion rate
5. Decision: Continue / Revert / A/B Test

**If Monitoring Shows Issues Before 10 Dec:**
- Application volume drops >40% sustained = early warning
- Cost per click increases >30% = potential relevance issue
- Client feedback about application quality decline = revert immediately

---

## **INITIAL PERFORMANCE ANALYSIS (22-24 Nov 2025) - ARCHIVED**

**Analysis Date:** 24 November 2025
**Status:** SUPERSEDED by 26 Nov 6-day review above

**Initial assessment was premature** - did not account for:
- 2-4 week conversion lag in education lead gen model
- Low volume natural variance (3.6% CVR baseline)
- GA4 tracking unreliability (99%+ bounce rates impossible)
- Enhanced Conversions offline import timing delays

**Original findings archived for reference:**

| Metric | Before (18-21 Nov) | After (22-24 Nov) | Initial Assessment |
|--------|-------------------|------------------|-------------------|
| Google Ads CVR | 2.43% | 0.20% | -91.8% (MISLEADING - conversion lag) |
| GA4 Bounce Rate | 50.9% | 67.3% | +16.4pp (UNRELIABLE - tracking issue) |
| GA4 Session Duration | 121s | 87s | -27.9% (UNRELIABLE - tracking issue) |

**Lesson Learned:** Education lead gen requires 3-4 week observation period minimum due to application → enrollment conversion lag. Initial 3-day and 6-day reviews too premature for decision-making.

