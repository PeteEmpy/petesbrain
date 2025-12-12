# Smythson P9: More Aggressive Reallocation Options

**Analysis Date:** December 11, 2025
**Question:** Can we push the EUR reallocation harder than Scenario 2 (10%)?
**Answer:** Yes, with caveats around UK impact and EUR volume capacity

---

## The Aggressiveness Spectrum

You have three dimensions to be more aggressive:

1. **Bigger shift percentage** (10% → 15-20%)
2. **Longer window** (6 days → 11 days, extending past standard delivery cutoff)
3. **Additional sources** (reallocate from USA or ROW too)

---

## Option A: Extend Window (Dec 12-22, not just Dec 12-17)

### The Opportunity
EUR has **two delivery cutoff windows:**
- Standard delivery: ~Dec 17-18
- Express delivery: ~Dec 22-23

You could run EUR elevated for **11 days** (Dec 12-22) instead of 6 days, capturing both windows.

### Financial Impact

**Extended 10% shift (11 days vs 6 days):**

| Metric | 6-Day Window | 11-Day Window | Extra |
|--------|------|---------|-------|
| Additional EUR spend | £5,132 | £9,388 | +£4,256 |
| From UK reduction | £5,132 | £9,388 | +£4,256 |
| EUR revenue gain (892%) | £45,778 | £83,784 | +£38,006 |
| UK revenue loss (389%) | -£19,964 | -£36,535 | -£16,571 |
| **Net gain** | +£25,814 | +£47,249 | +£21,435 |

**P9 Revenue Impact:**
- Current path (no shift): £1,023,221
- With 11-day 10% shift: **£1,070,470** (+£47,249)
- vs Adjusted Target (£1,045,477): **+£24,993 (+2.4%)** ✅

**Upside:** Additional £26k net gain by extending just 5 more days

### The Risk: Post-Delivery-Cutoff ROAS
**But here's the concern:** EUR ROAS after standard delivery cutoff (Dec 18+) might drop

**2024 EUR Weekly Data:**
- Week 1 (Cyber): 341% ROAS
- Week 2 (Mid-Dec): 544% ROAS (strong)
- Week 3 (Last Order): 233% ROAS ⚠️ (collapses 57%)
- Week 4 (Christmas): 977% ROAS (Boxing Day spike)

**Key question:** Is Dec 18-22 treated as "Last Order Week" (233% ROAS) or something different?

If Dec 18-22 is treated as Last Order Week equivalent:
- EUR ROAS drops to 233% (from 892%)
- Additional 5 days of EUR spend would only generate 233% return
- **This would actually lose money vs baseline**

**Conservative approach:** Stick with 6-day window (Dec 12-17) to avoid post-standard-delivery ROAS cliff

**Aggressive approach:** Test 11 days and monitor daily (watch for ROAS drop post-Dec 17)

---

## Option B: Bigger Percentage Shift (15-20% vs 10%)

### Scenario: 15% Shift (Dec 12-17, 6 days)

**Budget reallocation:**
```
Move £12,835 from UK to EUR (6 days)

UK: £4,754/day → £3,870/day (-18.6%) for 6 days
EUR: £1,027/day → £1,520/day (+48%) for 6 days
```

**Financial Impact:**
- EUR gains: £12,835 @ 892% = +£114,334 revenue
- UK loses: £12,835 @ 389% = -£49,727 revenue
- **Net 6-day gain: +£64,607**

**P9 Total Revenue:**
- Current path: £1,023,221
- With 15% shift: **£1,087,828** (+£64,607)
- vs Target (£1,045,477): **+£42,351 (+4.0%)** ✅

**Upside:** Creates significant buffer (+£42k above target) instead of +£20k

### The Risk: UK Gets Badly Constrained

**UK Daily Budget Impact:**
- Normal: £4,754/day (during Cyber Week)
- Reduced: £3,870/day (-18.6%)
- **This is noticeable** — 40 fewer conversions per day (roughly)

**What could go wrong:**
1. UK campaigns might lose impression share during peak period
2. Smart Bidding algorithms might underperform on reduced budget
3. UK ROAS might actually improve (less saturation) — but that's a hope, not a guarantee
4. If UK ROAS improves while EUR dropped, you've made the wrong call

**Historical precedent:** In P8, when UK ran higher budgets during Black Friday, it achieved only 514% ROAS (vs 705% target). More budget didn't help. So removing budget might actually hurt UK's efficiency further.

**Assessment:** 🔴 **Risky** — UK is already struggling. Cutting it 18.6% during peak period might break it entirely.

---

## Option C: Multi-Source Reallocation

### Could you also reallocate from USA?

**USA Status:**
- Current ROAS: 689% (vs 527% target)
- Status: 13% **above** target
- Volume: Large account, stable performer

**Theoretical option:** Pull 5% from USA too, add to EUR

```
Move from both regions:
- 10% from UK: £8,556
- 5% from USA: £3,337
- Total to EUR: £11,893

EUR would get: £1,027 + (£11,893/6 days) = £2,017/day
```

**Financial Impact:**
- EUR gain: £11,893 @ 892% = +£106,154
- UK loss: £8,556 @ 389% = -£33,184
- USA loss: £3,337 @ 689% = -£22,990
- **Net gain: +£49,980**

**Upside:** Same revenue benefit as 15% UK shift, but spread the pain across two regions

**Downside:** USA is performing well. Why constrain it? Its higher ROAS (689% vs 389% UK) means you're making an inefficient trade.

**Math check:**
- Taking £1 from USA at 689% ROAS = lose £6.89 revenue
- Putting £1 into EUR at 892% ROAS = gain £8.92 revenue
- **Net gain: £2.03 per £1 shifted** ✅

So yes, this works. But USA is working, UK is broken. More logical to fix UK's problem by reallocating FROM UK.

**Assessment:** ⚠️ **Okay but inefficient** — The math works, but you're constraining a performer to fund another performer. Better to just cut the underperformer (UK).

---

## Option D: Dual-Phase Approach (Smart Combination)

### Do 10% shift (Dec 12-17) PLUS Boxing Day spike (Dec 26)

This separates concerns:

**Phase 1 (Dec 12-17): Core reallocation**
- 10% UK → EUR (addresses the main gap)
- Modest, low-risk, reversible
- Expected net gain: +£42k

**Phase 2 (Dec 26): Boxing Day independent spike**
- Increase EUR budget specifically for Boxing Day
- 2024 data: EUR Boxing Day hit 2,929% ROAS
- Separate from the Dec 12-17 reallocation
- Can maintain normal budgets through Dec 25, then spike just Dec 26

**Dec 26 Boxing Day Spike Scenario:**
```
EUR Boxing Day budget: £1,027 × 2.5x = £2,568 (normal + £1,541 extra)

Expected revenue @ 2,929% ROAS: £75,153 (just on Dec 26!)
vs Normal day @ 892% ROAS: £9,157
Incremental gain: +£65,996 from one day
```

**Total upside if you do both:**
- Dec 12-17 reallocation: +£42k
- Dec 26 Boxing Day spike: +£66k
- **Combined: +£108k additional revenue**

**P9 Revenue with both:**
- Current path: £1,023,221
- With both optimizations: **£1,131,221** (+£108k!)
- vs Target (£1,045,477): **+£85,744 (+8.2%)** ✅ Major buffer

**The appeal:** Two separate, targeted optimizations rather than one aggressive bet

**Risk profile:** Low — both are reversible/isolated decisions

**Execution:**
1. Execute 10% reallocation Dec 12-17 (low risk, tested)
2. Monitor EUR ROAS daily Dec 12-17
3. If EUR performs well, confidently increase Dec 26 Boxing Day budget
4. If EUR underperforms, still have full budget on Dec 26 via normal allocation

**Assessment:** 🟢 **Elegant** — Separates the core reallocation (which you need) from a bonus optimization (which amplifies upside)

---

## The Tension: Aggressiveness vs Control

### Where's the Real Constraint?

**Not budget** — you have £171,127 to deploy

**Not EUR volume** — it can handle +30% budget increase easily, probably +50%

**The real constraint: UK's already failing**

If you take more from UK (15-20% shift), you're:
1. Hoping UK doesn't get worse
2. Gambling that the EUR gain outweighs the UK loss
3. Leaving no budget flexibility for Dec 18+ when UK could recover

**If you keep it at 10%:**
1. You hit target with breathing room
2. You preserve UK ability to recover Dec 18+
3. You can still do Boxing Day spike independently
4. Lower risk of unintended consequences

---

## My Recommendation: The Smart Aggressive Approach

### Execute **Option D: Dual-Phase (10% shift + Boxing Day spike)**

**Why this is the most aggressive AND smartest:**

1. **Dec 12-17: 10% reallocation (core optimization)**
   - Closes the £22k gap
   - Low risk, proven approach
   - Easily reversible Dec 18

2. **Dec 26: Boxing Day spike (bonus optimization)**
   - Uses EUR's exceptional 2,929% ROAS from 2024
   - Independent decision (not coupled to reallocation)
   - Separate budget spike (not shift)
   - Even if Dec 12-17 reallocation disappoints, you still have full Boxing Day opportunity

3. **Total upside potential: +£108k** (vs just +£42k with 10% shift alone)

4. **Risk profile: Low**
   - Core shift is tested and reversible
   - Boxing Day is a separate, targeted decision
   - If EUR ROAS drops post-Dec-18, you still have options
   - UK gets fully funded Dec 18+ for last order window

5. **Flexibility: Maximum**
   - After Dec 12-17 results, you'll know if EUR can absorb more
   - Can adjust Boxing Day budget up/down based on Dec 1-17 performance
   - Can still reverse Dec 18 if needed

---

## If You Want To Be REALLY Aggressive

**Try 15% shift (Dec 12-17) + Boxing Day spike:**

- Dec 12-17: 15% UK → EUR (+£64.6k revenue)
- Dec 26: Boxing Day spike (+£66k revenue)
- **Combined: +£130.6k additional revenue**
- **P9 Total: £1,153.8k** (vs £1,045.5k target = +10.4% above target) 🔥

**But this requires:**
1. Confidence that UK can survive -18.6% budget during peak period
2. Willingness to accept that UK might degrade further
3. Clear signal from Dec 12-14 that EUR is absorbing the budget successfully before committing to full 6 days

**How to de-risk this:** Commit to 10% shift for 6 days, monitor daily, if EUR is crushing it (800%+ ROAS) on Dec 13-14, extend to 15% on Dec 15-17

---

## Decision Matrix

| Approach | Upside | Risk | Effort | Recommendation |
|----------|--------|------|--------|---------|
| **10% (6 days)** | +£42k | ✅ Low | Low | Safe default |
| **15% (6 days)** | +£65k | 🟡 Medium | Low | Only if UK ROAS improves |
| **10% extended (11 days)** | +£47k | 🟡 Medium | Low | Only if post-delivery ROAS holds |
| **10% + Boxing Day** | +£108k | ✅ Low | Medium | 🟢 **Recommended** |
| **15% + Boxing Day** | +£131k | 🟡 Medium | Medium | Aggressive but doable |

---

## Final Assessment

**You can be more aggressive.** The question is which dimension:

- **More aggressive on EUR reallocation amount?** ⚠️ Only if you're OK with UK getting worse
- **More aggressive on window length?** ⚠️ Risky if ROAS drops post-standard-delivery
- **More aggressive on ancillary opportunities?** ✅ **Yes — Boxing Day spike is a clean win**

**My take:** 10% shift (Dec 12-17) + Boxing Day spike is the "sweet spot" aggressive play. It gives you +£108k upside while maintaining tight control and reversibility at each stage.

If EUR crushes it Dec 12-17 (maintains 800%+ ROAS) and Alex is confident, then you could upgrade to 15% shift + Boxing Day in future years.
