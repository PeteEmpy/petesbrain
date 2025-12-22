# CSV Analyzer - Learning Notes
**Date:** 2025-11-19
**Source:** industry resources template (v2025.11.0)
**Status:** ✅ Complete

---

## 🎓 What I Learned from Mike's Implementation

### 1. Two-Script Architecture
**Mike's Pattern:**
- `analyse.py` - General CSV analyzer (works with any CSV)
- `analyse_google_ads.py` - Specialized for Google Ads exports

**Why This Is Better:**
- Separation of concerns
- Google Ads specific optimizations don't clutter general analyzer
- Easy to add more specialized analyzers (e.g., `analyse_meta_ads.py`, `analyse_ga4.py`)

**Applied to PetesBrain:**
- Kept both: Automated scripts AND instruction-based approach
- Scripts for repeatability, instructions for flexibility
- Best of both worlds

---

### 2. Auto-Detection Pattern
**Mike's Code:**
```python
def detect_google_ads_format(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        if 'report' in first_line.lower():
            second_line = f.readline()
            if any(month in second_line for month in ['January', ...]):
                return 2  # Skip first 2 header rows
    return 0
```

**Key Insight:**
Google Ads exports have 2 header rows:
1. "Ad group report" (or similar)
2. "1 October 2024 - 30 April 2025"

Most CSV libraries fail on this. Mike handles it automatically.

**Why This Matters:**
- No user intervention needed
- Works with any Google Ads export
- Prevents "column mismatch" errors

**Applied:** Integrated into `analyse.py`

---

### 3. Data Cleaning Strategy
**Mike's Approach:**
```python
# Clean numeric columns
df[col] = (df[col].astype(str)
           .str.replace(',', '')        # 1,234 → 1234
           .str.replace('--', '0')      # Google Ads null → 0
           .str.replace(' --', '0')     # Variant
           .str.strip())
df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
```

**Key Insight:**
- Chain operations for clarity
- Handle ALL variations ('--', ' --', ' -- ')
- `errors='coerce'` prevents crashes
- `.fillna(0)` for safety

**Applied:** Adopted this exact pattern (it's robust!)

---

### 4. Enabled vs Paused Separation
**Mike's Code:**
```python
enabled_df = df[df['Ad group status'] == 'Enabled']
paused_df = df[df['Ad group status'] == 'Paused']
```

**Why This Is Critical:**
- Paused ad groups distort averages
- Can't calculate ROI on paused items
- Performance metrics should only include enabled

**Example Impact:**
- 10 enabled ad groups @ £1000 spend, 292% ROAS
- 50 paused ad groups @ £0 spend
- WITHOUT separation: Looks like 60 ad groups, avg ROAS is wrong
- WITH separation: Accurate 292% ROAS on enabled only

**Applied:** Adopted this pattern

---

### 5. Campaign-Level Aggregation
**Mike's Code:**
```python
campaign_perf = enabled_df.groupby('Campaign').agg({
    'Cost': 'sum',
    'Clicks': 'sum',
    'Conversions': 'sum',
    'Conv. value': 'sum'
})
campaign_perf['ROAS'] = campaign_perf['Conv. value'] / campaign_perf['Cost']
```

**Key Insight:**
- Ad group level = too granular for quick insights
- Campaign level = perfect for decision-making
- Aggregation AFTER filtering enabled = accurate metrics

**Applied:** Included in Google Ads analyzer

---

### 6. "No Questions" Philosophy
**Mike's Documentation:**
```
DO NOT ASK THE USER WHAT THEY WANT TO DO.
IMMEDIATELY: Run analysis, Generate ALL visualizations, Present results
```

**Why This Matches PetesBrain:**
- Operational efficiency (don't wait for answers)
- Decisive action (just analyze it!)
- Consistent output (same analysis every time)

**Applied:** Embedded in skill.md behavior guidelines

---

### 7. ROAS Format Adaptation
**Mike's Original:**
```python
print(f'ROAS: {roas:.2f}x (£{roas:.2f} revenue per £1 spent)')
# Output: "ROAS: 2.92x (£2.92 revenue per £1 spent)"
```

**PetesBrain Standard:**
```python
roas_pct = roas_ratio * 100
print(f'ROAS: {roas_pct:.0f}% ({roas_ratio:.2f}x revenue per £1 spent)')
# Output: "ROAS: 292% (2.92x revenue per £1 spent)"
```

**Key Adaptation:**
- Primary format: 292%
- Secondary format: (2.92x) in parentheses
- Both are technically correct, client preference is %

**Applied:** All Google Ads analyzer output uses % first

---

### 8. Visualization Strategy
**Mike Creates 4 Specific Charts:**
1. **Top 15 by spend** - Horizontal bar chart (green if converting, red if not)
2. **Campaign performance** - 4-panel (spend, conversions, ROAS, cost/conv)
3. **Status distribution** - Pie chart (enabled vs paused)
4. **Cost vs conversions scatter** - Bubble size = conversion value

**Why These 4:**
- Cover the critical questions clients ask
- Visual hierarchy: spend → conversions → efficiency
- Colors indicate action needed (red = investigate)

**What I Would Add:**
- Time series (if date column present)
- Impression share analysis
- Quality score indicators (CTR as proxy)

**Applied:** Kept Mike's 4, can extend later

---

## 📊 Script-Based vs Instruction-Based

**Kept BOTH approaches:**

### Script-Based (Mike's contribution)
**Pros:**
- ✅ Consistent output every time
- ✅ Fast execution (direct Python)
- ✅ Automatic visualizations
- ✅ Handles messy data robustly
- ✅ Perfect for standard reports

**Cons:**
- ❌ Less flexible
- ❌ Requires code changes for customization
- ❌ Fixed output format

### Instruction-Based (My existing approach)
**Pros:**
- ✅ Extremely flexible
- ✅ Adapts to any question
- ✅ Custom insights
- ✅ No code changes needed

**Cons:**
- ❌ Results vary (depends on Claude's interpretation)
- ❌ Slower (more thinking required)
- ❌ May not generate visualizations consistently

**Decision:** Use scripts for Google Ads, instructions for everything else.

---

## 🎯 Key Takeaways

### 1. **Robustness Over Cleverness**
Mike's code handles edge cases:
- Spaces in file paths → fuzzy matching
- '--' values → clean to zero
- Missing columns → graceful degradation
- Various formats → auto-detection

**Lesson:** Production code needs to handle messy real-world data

### 2. **User Experience Decisions**
"No questions" philosophy = decisive, operational
- Not appropriate for exploratory analysis
- Perfect for standard reports
- Matches agency workflow

**Lesson:** UX decisions should match user's workflow style

### 3. **Separation of Concerns**
General analyzer vs specialized analyzer
- Keeps code clean
- Easy to maintain
- Simple to extend

**Lesson:** Don't try to make one function do everything

### 4. **Standards Matter**
ROAS as % vs x notation
- Client preference > technical correctness
- Consistency across reports
- Document the standard

**Lesson:** Adapt tools to match client communication style

### 5. **Combine Approaches**
Script-based + instruction-based = best of both
- Scripts for repeatability
- Instructions for flexibility
- Clear guidance on which to use when

**Lesson:** Don't replace, enhance

---

## 🔄 Next Steps

**Testing:**
1. Test with real Google Ads export (ad group report)
2. Test with non-Google Ads CSV
3. Verify visualizations are created correctly
4. Check ROAS format in output

**Enhancements:**
1. Add more specialized analyzers as needed (Meta, GA4)
2. Create wrapper script that chooses analyzer automatically
3. Add output format options (HTML, PDF)
4. Integration with existing report generator tools

**Documentation:**
1. Add examples to `examples/` folder
2. Create QUICKSTART.md for common use cases
3. Document ROAS calculation methodology

---

## 📈 Impact Assessment

**Time Investment:** 3 hours (study + implementation + documentation)

**Expected ROI:**
- 30-60 min saved per client report (automated analysis)
- Consistent output (same analysis every time)
- Better insights (4 visualizations vs 0 previously)
- Reduced errors (handles messy data automatically)

**Payback Period:** 3-6 client reports (~1 week)

---

**Learning captured:** 2025-11-19
**Next review:** After first real-world usage
