# NMA - 3-Week Account Improvement Plan
**Created:** 2025-11-17
**Based on:** NMA Campaign & Conversion Audit (Nov 17, 2025)
**Review Date:** Nov 29, 2025 (Target CPA check-in)

---

## Current State (Nov 17, 2025)

**Account Performance (Last 30 Days):**
- Spend: £8.11M
- Conversions: 47.8
- CPA: £169,465 (blended)
- Click-Through Rate: 7.84%
- Conversion Rate: 1.61%

**Target CPA Implementation:**
- Implemented: Nov 10, 2025
- Targets: UK £100 | ROW £50 | UK Management £150
- First review: Nov 29, 2025 (3 weeks post-implementation)

**Recent Optimizations:**
- ✅ Added 5 high-converting keywords to ROW Engineering Search (Nov 17)
- ✅ Label PB_2025 applied for tracking
- Expected impact: +35 conversions/year from keywords alone

---

## 3-Week Targets

**Primary Metrics:**
- Conversions: 47.8 → **55-65/month** (+15% to +36%)
- CPA: £169k → **£130-150k** (-11% to -23%)

**Optimization Targets:**
- Remove 150+ zero-impression keywords
- Add 30+ sitelinks across active campaigns
- Add 40+ callouts
- Launch 2 country-specific ROW campaigns (US, UAE)
- Fix 2 disapproved sitelinks
- Apply conservative demographic adjustments

**Quality Improvements:**
- Improve ad relevance with targeted sitelinks
- Enhance account structure with geo-specific campaigns
- Increase impression share for high-converting keywords

---

## Week 1 (Nov 18-24): Quick Wins & Data Gathering

### 1. Fix Disapproved Sitelinks
**Time:** 30 minutes
**Action:**
- Sitelink 1: "Course Guide Download" - Change "Earn as Your Learn" to "Earn as You Learn"
- Sitelink 2: "Motorsport Engineering" - Change "Find Out More" to specific benefit (e.g., "Start Your Application")
- Re-enable both sitelinks after edits

**Expected Impact:**
- Minor quality score improvement
- Remove policy warning from account

---

### 2. Add Sitelinks to Active Campaigns
**Time:** 2 hours
**Target:** 4-6 sitelinks per campaign

**Priority Campaigns:**
1. NMA | Search | ROW | Engineering (currently 0 conversions)
2. NMA | Search | UK | Engineering Management (3.97 conv/30 days)
3. NMA | Search | UK | Motorsport (1.99 conv/30 days)

**Sitelink Ideas:**
- Course Guides (program-specific)
- Application Process
- Career Outcomes
- Alumni Success Stories
- Flexible Study Options
- Financial Aid / Payment Plans

**Expected Impact:**
- +10-15% CTR improvement
- +5-8% conversion rate improvement
- Better ad position (improved quality score)

---

### 3. Pull Demographic Performance Data
**Time:** 1 hour

**GAQL Query:**
```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.gender.type,
  ad_group_criterion.age_range.type,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM gender_view, age_range_view
WHERE
  campaign.status = 'ENABLED'
  AND segments.date DURING LAST_90_DAYS
ORDER BY metrics.cost_micros DESC
```

**Analysis Focus:**
- Identify underperforming age/gender segments
- Calculate CPA by demographic
- Prepare conservative bid adjustments (NOT exclusions)

**Decision Criteria:**
- Apply -20% bid adjustment if CPA >2x account average
- Do NOT exclude demographics entirely (Anwesha's recommendation was too aggressive)

---

### 4. Monitor New Keywords Performance
**Time:** 15 minutes daily (5 days = 1.25 hours total)

**Keywords to Track:**
- automotive engineering degree (Broad)
- automotive design courses (Broad)
- masters in motorsport engineering (Exact)
- automotive engineering master (Broad)
- degree in automotive engineering (Broad)

**Tracking Metrics:**
- Impressions (should see immediate increase)
- Average position
- Quality Score (check after 7 days)
- Clicks, CTR
- Conversions (may take 2-3 weeks)

**Review Date:** Nov 24, 2025 (1 week post-implementation)

**Success Criteria:**
- Quality Score 7+ by Nov 24
- CTR >5%
- Impressions >100/day for broad match keywords

---

### 5. Review Zero-Impression Keywords
**Time:** 1 hour

**GAQL Query:**
```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.historical_quality_score
FROM keyword_view
WHERE
  campaign.status = 'ENABLED'
  AND segments.date DURING LAST_90_DAYS
  AND metrics.impressions = 0
ORDER BY campaign.name, ad_group.name
```

**Analysis:**
- Identify keywords with 0 impressions in 90 days
- Check Quality Scores (if <3, likely not serving)
- Categorize: Low search volume vs Poor relevance vs Budget constraint

**Action for Week 2:**
- Pause keywords with QS <3 and 0 impressions
- Keep keywords with QS 7+ (may serve in future)
- Target: Remove ~150 dead keywords

---

## Week 2 (Nov 25-Dec 1): Strategic Adjustments

### 6. Review Target CPA Performance (Nov 29)
**Time:** 1 hour
**Review Date:** Nov 29, 2025 (3 weeks post-implementation)

**Analysis:**
- Pull 3-week performance: Nov 10-29
- Compare CPAs to targets:
  - UK Search: Target £100, Current?
  - ROW Search: Target £50, Current?
  - UK Management: Target £150, Current?

**Decision Framework:**
- If CPA within 20% of target: Continue, no changes
- If CPA 20-50% above target: Reduce budget 10-15%
- If CPA 50%+ above target: Review campaign structure

**Budget Adjustment Criteria:**
- ROW Engineering: If performing well, increase budget £40→£80/day
- UK Management: If still >£1M CPA, consider pausing (despite user's earlier decision)
- ROW Management: Monitor closely (currently 0 conversions)

---

### 7. Apply Demographic Bid Adjustments
**Time:** 30 minutes
**Based on:** Week 1 demographic analysis

**Conservative Approach:**
- Apply -20% bid adjustment (NOT exclusions) to segments with CPA >2x average
- Test for 2 weeks before further adjustments
- Do NOT exclude any demographics entirely

**Expected Segments:**
- Likely: 18-24 (students, lower conversion intent)
- Possible: 65+ (less relevant for engineering education)

**Expected Impact:**
- Shift budget to higher-converting demographics
- Reduce wasted spend by 5-8%
- Maintain reach (no exclusions)

---

### 8. Create Country-Specific ROW Campaigns
**Time:** 4 hours
**Priority Countries:** US, UAE

**Current Problem:**
- ROW Management: £660k spend, 0 conversions
- ROW campaigns too broad, lack localization

**New Campaign Structure:**

**Campaign 1: NMA | Search | US | Engineering**
- Daily Budget: £30
- Target CPA: £60
- Keywords: US-focused engineering terms
- Ad copy: Reference US career outcomes, accreditation
- Sitelinks: US application process, alumni in US

**Campaign 2: NMA | Search | UAE | Engineering**
- Daily Budget: £20
- Target CPA: £40
- Keywords: Middle East engineering education terms
- Ad copy: Reference UAE partnerships, regional relevance
- Sitelinks: International student support

**Migration Strategy:**
- Do NOT pause ROW Management immediately
- Run country campaigns alongside for 2 weeks
- Compare performance Nov 29-Dec 13
- Pause ROW Management only if country campaigns prove superior

**Expected Impact:**
- Better ad relevance for US/UAE audiences
- Lower CPCs (improved quality scores)
- 2-4 conversions from US campaign in first month
- 1-2 conversions from UAE campaign in first month

---

### 9. Remove Zero-Impression Keywords
**Time:** 30 minutes

**Action:**
- Pause ~150 keywords identified in Week 1 review
- Focus on keywords with QS <3 and 0 impressions in 90 days
- Export list before pausing (for audit trail)

**Expected Impact:**
- Cleaner account structure
- Slightly improved account-level quality score
- Easier performance monitoring

---

## Week 3 (Dec 2-8): Optimization & Scaling

### 10. Add Callout Extensions
**Time:** 1 hour
**Target:** 40+ callouts across active campaigns

**Callout Categories:**
- Program Benefits: "Industry Partnerships", "Practical Experience", "Career Support"
- Study Flexibility: "Online & On-Campus Options", "Flexible Payment Plans", "Study While You Work"
- Credibility: "Accredited Programs", "Expert Tutors", "Award-Winning Institution"
- Outcomes: "95% Employment Rate", "Global Alumni Network", "Professional Accreditation"

**Implementation:**
- Create shared callout set (apply to all campaigns)
- Focus on unique selling points vs generic claims
- Ensure compliance with Google Ads policy (substantiate claims)

**Expected Impact:**
- +5-8% CTR improvement
- Better ad real estate (callouts increase ad size)
- Improved quality score

---

### 11. Expand ROW Engineering Keyword Portfolio
**Time:** 2 hours

**Strategy:**
- ROW Engineering is best-performing campaign (£34,744 CPA vs £169k average)
- Add 15-20 related keywords based on Nov 17 additions

**New Keywords to Consider:**
- automotive engineering courses
- motorsport engineering online
- automotive technology degree
- vehicle engineering programs
- racing engineering courses
- automotive design degree
- motorsport management degree
- automotive engineering masters online

**Match Type Strategy:**
- 70% Broad (capture wider intent)
- 30% Exact (high-intent converters)

**Budget Consideration:**
- Current: £40/day (recommend £80/day if Nov 29 review shows strong performance)

**Expected Impact:**
- +10-15 additional conversions/month from ROW Engineering
- Reduced CPA as campaign scales (better data for Target CPA)

---

### 12. Create Separate Engineering Asset Group (PMax)
**Time:** 3 hours

**Current Problem:**
- UK PMax campaign may be diluting performance across multiple degree types
- Engineering degrees have different audience, creative needs

**New Asset Group Structure:**

**Asset Group: Engineering Programs**
- Headlines (15):
  - "Motorsport Engineering Degrees"
  - "Start Your Engineering Career"
  - "BSc Automotive Engineering Online"
  - "Masters in Motorsport Engineering"
  - [+ 11 more engineering-specific headlines]

- Long Headlines (5):
  - "Study Motorsport Engineering with Industry Leaders"
  - [+ 4 more]

- Descriptions (5):
  - "Accredited engineering degrees combining theory and practice..."
  - [+ 4 more]

- Images: Engineering-specific (labs, cars, projects)
- Videos: Engineering student testimonials
- Final URLs: Engineering landing pages only

**Expected Impact:**
- Better audience segmentation (engineering-interested signals)
- Improved ad relevance for engineering searches
- +5-10 conversions/month from PMax
- Lower CPA for engineering-specific leads

---

### 13. Progress Report & Next Phase Planning
**Time:** 2 hours

**Report Contents:**
- 3-week performance summary (Nov 17-Dec 8)
- Conversion change: 47.8 → ? (target: 55-65)
- CPA change: £169k → ? (target: £130-150k)
- Optimizations completed (13 action items)
- Wins and learnings
- Recommendations for next phase (Dec 9-29)

**Share With:**
- Paul Riley (client)
- Anwesha (consultant)
- Internal team

**Next Phase Preview:**
- Scale winning campaigns (if Target CPA performing)
- Launch additional country campaigns (if US/UAE successful)
- Implement day-of-week bid adjustments (deferred from Nov 17)
- Enhanced Conversions tag verification (pending Google meeting)

---

## Decision Log

### Decisions Made (Nov 17)

1. **ROW Management Campaign:** NOT pausing (user decision, contrary to audit recommendation)
   - Rationale: Want to give Target CPA more time to optimize
   - Review again: Nov 29, 2025

2. **Day-of-Week Bid Adjustments:** DEFERRED to Dec 15-20
   - Rationale: Need stable Target CPA baseline before layering in schedules
   - Saturday shows £293k CPA (3x average), but attribution lag is 72% same-day
   - Will re-analyze with 90 days post-Target CPA data

3. **Target CPA Review:** Nov 29, 2025 (week on Friday)
   - Review 3-week performance
   - Decide on budget adjustments at that point

4. **Demographic Exclusions:** Using bid adjustments (-20%), NOT exclusions
   - Anwesha recommended excluding 18-24, 55-64, Unknown gender
   - Too aggressive - maintains reach while optimizing budget allocation

5. **Enhanced Conversions Tag Verification:** DEFERRED
   - Waiting on confirmation from Henry re: Google meeting
   - Current discrepancy (0.8 vs 41) is expected (different metrics)

---

## Success Metrics (3-Week Review: Dec 8)

### Primary KPIs
- [ ] Conversions increased to 55-65/month (+15% to +36%)
- [ ] CPA reduced to £130-150k (-11% to -23%)
- [ ] Target CPA showing directional improvement toward targets

### Optimization KPIs
- [ ] 150+ zero-impression keywords removed
- [ ] 30+ sitelinks added across active campaigns
- [ ] 40+ callouts added (shared set)
- [ ] 2 country-specific campaigns launched (US, UAE)
- [ ] 2 disapproved sitelinks fixed
- [ ] 5 new keywords showing QS 7+
- [ ] Demographic bid adjustments applied (-20% to underperformers)

### Quality Improvements
- [ ] CTR improved 10-15% from sitelinks/callouts
- [ ] ROW Engineering budget doubled (if performance supports)
- [ ] Engineering asset group created in PMax
- [ ] US/UAE campaigns generating conversions (2-6 combined)

---

## Risk Mitigation

### Risk 1: Target CPA Not Optimizing
**Likelihood:** Medium
**Impact:** High (continues £169k CPA)
**Mitigation:**
- Nov 29 review will show directional trend
- If not improving, consider switching to Manual CPC with bid strategies
- Ensure conversion tracking is verified (Enhanced Conversions check)

### Risk 2: New Keywords Don't Perform
**Likelihood:** Low
**Impact:** Low (small budget allocation)
**Mitigation:**
- Daily monitoring Week 1
- Pause underperformers by Nov 24
- Label PB_2025 allows easy isolation

### Risk 3: Country Campaigns Cannibalize ROW Management
**Likelihood:** High (desired outcome)
**Impact:** Neutral (intentional migration)
**Mitigation:**
- Run both for 2 weeks to compare
- Gradual budget shift, not immediate pause
- Document performance difference

### Risk 4: Client Budget Constraints
**Likelihood:** Unknown
**Impact:** High (limits optimization pace)
**Mitigation:**
- Confirm budget availability with Paul before scaling
- Focus on efficiency gains first (removing waste)
- Scale only after Target CPA proves stable

---

## Notes

- Plan created: Nov 17, 2025
- Based on audit by Anwesha (consultant, India market focus)
- Conservative approach prioritizing stability over aggressive changes
- All changes logged to tasks-completed.md
- Label PB_2025 tracks all 2025 optimizations
- Next major review: Nov 29, 2025 (Target CPA check-in)
- Day-of-week changes deferred to Dec 15-20 (after Target CPA stabilizes)
