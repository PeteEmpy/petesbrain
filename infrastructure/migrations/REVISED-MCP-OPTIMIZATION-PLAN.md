# REVISED MCP Optimization Plan
## Based on Actual Codebase Analysis (15 Dec 2025)

---

## 🎯 **Key Discovery**

**Initial audit suggested:** 546 MCP calls, 25 servers built but only 6 configured → massive untapped potential

**Reality after deep analysis:** Your codebase architecture is already well-designed. Most "missing MCP usage" is intentional use of direct Python imports (which is correct for agents).

**The real opportunities are different than expected.**

---

## ✅ **What's Already Correct (Don't Change)**

### 1. **Agents Use Direct Python Imports** ✓
- 50 agents use `from shared.platform_ids import get_client_platform_ids`
- **This is CORRECT** - faster than MCP, no serialization overhead
- Agents run in Python environment → direct imports are optimal

### 2. **Skills Use MCP Appropriately** ✓
- 34 MCP calls in skills
- Claude Code skills can only use MCP (can't import Python modules)
- **This is CORRECT** architecture

### 3. **Client Scripts Use Direct APIs** ✓
- 54 instances of direct Google Ads API usage
- For complex, multi-step operations (budget deployments, asset updates)
- **This is CORRECT** - more control, better error handling for one-off scripts

---

## 🚀 **REAL Optimization Opportunities** (Revised)

### **Priority 1: Activate High-Value MCP Servers** ⭐⭐⭐⭐⭐

**Impact:** Unlock new automation capabilities

#### A. **Google Sheets MCP** (15 minutes setup)

**Current state:** Built but not configured
**Impact:** High - eliminates manual CSV → Sheets workflow

**Enable it:**
```bash
# Add to .mcp.json:
"google-sheets": {
  "command": "/path/to/venv/bin/python",
  "args": ["/path/to/google-sheets-mcp-server/server.py"],
  "env": {
    "GOOGLE_SHEETS_OAUTH_CONFIG_PATH": "/path/to/credentials.json"
  }
}
```

**Immediate use cases:**
1. **Weekly reports auto-update dashboards**
   ```python
   # Current: Manual CSV export → Manual Sheet upload
   # With MCP: Direct write
   mcp__google_sheets__write_cells(
       spreadsheet_id='client_dashboard_id',
       range='Weekly!A2:Z2',
       data=performance_data
   )
   ```

2. **Budget tracker writes directly**
3. **Product performance exports update automatically**

**ROI:** Saves 30 mins/week per client (360 mins/week across 12 clients)

---

#### B. **Google Tasks MCP** (10 minutes setup)

**Current state:** Using Python helper `google_tasks_client.py`
**Impact:** Medium - enables task creation from skills

**Enable it:**
```bash
# Add to .mcp.json
```

**Benefit:** Skills can create tasks without Python imports

**Example:**
```python
# In google-ads-weekly-report skill
if roas < target_roas * 0.85:
    mcp__google_tasks__create_task(
        tasklist_id=client_tasklist,
        title=f'[{client}] ROAS 15% below target - investigate',
        priority='P1'
    )
```

**ROI:** Automated task creation from skills (currently manual)

---

#### C. **Merchant Center MCP** (30 minutes setup)

**Current state:** Built, not configured
**Impact:** HIGH - Product feed monitoring + Shopping campaign optimization

**Enable it:**
```bash
# Build and configure merchant-center MCP server
```

**Game-changing workflow:**
```python
# Weekly product feed audit (automated)
products = mcp__merchant_center__get_products(merchant_id='...')

disapproved = [p for p in products if p['status'] == 'disapproved']
low_stock = [p for p in inventory if p['quantity'] < 5]

# Cross-reference with Shopping ads
shopping_spend = mcp__google_ads__run_gaql(
    query="SELECT product_item_id, metrics.cost_micros FROM shopping_performance_view..."
)

# Auto-create tasks for:
# 1. Disapproved products with >£10/week spend
# 2. Low-stock products still running ads
# 3. High-margin products not in Shopping campaigns
```

**ROI:** Prevents wasted spend, catches feed issues automatically

---

### **Priority 2: Create Universal Tools** ⭐⭐⭐⭐

**Current problem:** 50+ client-specific scripts for repetitive tasks

#### **Universal Budget Deployer** (2 hours build time)

**Replaces:** 20+ client-specific budget scripts (Smythson alone has 6)

**Design:**
```bash
python tools/budget-deployer/deploy.py \
  --client smythson \
  --csv p9-budget-changes.csv \
  --dry-run  # Preview first

# Then execute
python tools/budget-deployer/deploy.py \
  --client smythson \
  --csv p9-budget-changes.csv
```

**Features:**
- Change Protection Protocol built-in
- Works for ALL clients (no new script per client)
- Backup → Execute → Verify → Rollback workflow
- Audit trail logging

**ROI:**
- Future budget changes: 3 mins (vs 30 mins per client)
- One script to maintain (vs 50+)
- Reusable across all scenarios

---

#### **Universal Asset Replacer** (3 hours build time)

**Replaces:** Multiple client-specific asset update scripts

**Design:**
```bash
python tools/asset-replacer/replace.py \
  --client smythson \
  --campaign-id 12345 \
  --asset-type rsa \
  --csv new-headlines.csv \
  --dry-run
```

**Features:**
- Handles RSAs, PMax asset groups, sitelinks, callouts
- Dry-run mode shows changes
- Automatic backup/verify/rollback
- Works for all clients

**ROI:**
- Asset updates: 5 mins (vs 30 mins)
- Eliminates client-specific scripts
- Safer (always preview first)

---

### **Priority 3: Cross-Platform Workflows** ⭐⭐⭐⭐

**Opportunity:** Combine MCP servers for intelligent automation

#### **Inventory-Aware Shopping Optimizer** (4 hours build)

**Combines 5 MCP servers:**
1. platform-ids (client lookup)
2. shopify/woocommerce (live inventory)
3. merchant-center (product feed)
4. google-ads (Shopping performance)
5. google-tasks (auto-task creation)

**Logic:**
```python
# Weekly automation
for client in ecommerce_clients:
    # Get inventory from Shopify/WooCommerce
    inventory = mcp__shopify__get_inventory_levels(...)

    # Get Shopping campaign spend
    shopping_data = mcp__google_ads__run_gaql(...)

    # Find: Low stock + High spend = Waste
    for product in shopping_data:
        stock = inventory.get(product['sku'], {}).get('quantity', 0)
        spend = product['cost_micros'] / 1_000_000

        if stock < 5 and spend > 10:  # <5 units, >£10/week spend
            # Auto-create P1 task
            mcp__google_tasks__create_task(
                title=f'[{client}] Pause Shopping ads - low stock: {product["title"]}',
                priority='P1',
                notes=f'Only {stock} units, spending £{spend}/week'
            )
```

**ROI:**
- Prevents wasted spend on out-of-stock products
- Catches issues within 24 hours (vs manual weekly checks)
- Estimated savings: £500-£2000/month across clients

---

#### **Seasonal Budget Optimizer** (3 hours build)

**Combines:**
- google-trends (search volume forecasting)
- google-ads (current budgets)
- google-tasks (recommendations)

**Logic:**
```python
# Monthly check (1st of each month)
for client in clients:
    # Get client's core keywords from CONTEXT.md
    keywords = extract_keywords(f'clients/{client}/CONTEXT.md')

    # Check next 90 days trend forecast
    trends = mcp__google_trends__get_interest_over_time(
        keywords=keywords,
        geo='GB',
        timeframe='today 12-m'
    )

    # Seasonal pattern detection
    for keyword in keywords:
        next_month_forecast = trends[keyword]['forecast_next_30d']
        current_volume = trends[keyword]['current']

        if next_month_forecast > current_volume * 1.3:  # 30% increase
            # Recommend budget increase
            mcp__google_tasks__create_task(
                title=f'[{client}] Budget increase recommended - {keyword} +30% next month',
                priority='P2',
                notes=f'Trend data: {trends[keyword]}\nSuggest: +20% budget increase'
            )
```

**ROI:**
- Proactive seasonal planning (vs reactive)
- Capture seasonal opportunities
- Data-driven budget recommendations

---

### **Priority 4: Documentation Updates** ⭐⭐

**Effort:** 15 minutes
**Impact:** Medium - clarity for future development

**Execute:**
```bash
chmod +x infrastructure/migrations/update-docs-platform-ids.sh
./infrastructure/migrations/update-docs-platform-ids.sh
```

**Updates:**
- `.claude/CLAUDE.md` → Reference centralized platform-ids
- Skill documentation → Standardize pattern
- Tool docs → Use centralized server

---

## 📊 **Impact Summary (Revised)**

### **Quick Wins (This Week)**

| Action | Time | ROI |
|--------|------|-----|
| Enable Google Sheets MCP | 15 mins | 6 hours/week saved |
| Enable Google Tasks MCP | 10 mins | Automated task creation |
| Enable Merchant Center MCP | 30 mins | Catch feed issues automatically |
| Documentation updates | 15 mins | Future clarity |
| **Total** | **70 mins** | **6+ hours/week saved** |

### **High-Value Projects (Next 2 Weeks)**

| Project | Build Time | ROI |
|---------|------------|-----|
| Universal Budget Deployer | 2 hours | 90% faster budget changes |
| Universal Asset Replacer | 3 hours | 85% faster asset updates |
| Inventory-Aware Optimizer | 4 hours | £500-£2K/month waste prevention |
| Seasonal Budget Optimizer | 3 hours | Proactive seasonal planning |
| **Total** | **12 hours** | **Massive operational efficiency** |

---

## ❌ **What NOT to Do (Based on Analysis)**

### 1. **Don't Convert Agents to MCP**
- Agents correctly use direct Python imports
- MCP would add overhead for no benefit
- Current architecture is optimal

### 2. **Don't Convert Client Scripts to MCP**
- Complex scripts need direct API control
- MCP abstracts away necessary detail
- Keep direct API usage for deployment scripts

### 3. **Don't Mass-Migrate "546 MCP Calls"**
- Most are already correct patterns
- No broken code that needs fixing
- Documentation updates only

---

## 🎯 **Recommended Execution Order**

### **This Week (70 minutes total)**
1. ✅ **DONE:** Added platform-ids to .mcp.json
2. **Enable Google Sheets MCP** (15 mins)
   - Add to `.mcp.json`
   - Test with one client dashboard
3. **Enable Google Tasks MCP** (10 mins)
   - Add to `.mcp.json`
   - Test task creation from skill
4. **Enable Merchant Center MCP** (30 mins)
   - Configure credentials
   - Test product query
5. **Update documentation** (15 mins)
   - Run `update-docs-platform-ids.sh`
   - Review changes

### **Next Week (12 hours)**
1. **Build Universal Budget Deployer** (2 hours)
   - Test on Smythson
   - Document usage
2. **Build Universal Asset Replacer** (3 hours)
   - Test on one client
   - Create CSV template
3. **Build Inventory-Aware Optimizer** (4 hours)
   - Test on e-commerce client
   - Schedule as LaunchAgent
4. **Build Seasonal Budget Optimizer** (3 hours)
   - Test trend forecasting
   - Schedule monthly run

### **Week 3 (Monitoring & Refinement)**
- Monitor new automations
- Gather savings data
- Refine thresholds
- Add more clients to workflows

---

## 💡 **The Bigger Insight**

**Your MCP architecture is ALREADY well-designed.**

The audit revealed that your codebase makes intelligent choices:
- **Agents use direct imports** (optimal for Python execution)
- **Skills use MCP** (only option for Claude Code)
- **Scripts use direct APIs** (necessary for complex operations)

**The opportunity isn't "fix broken architecture"** - it's **"unlock new capabilities"** by:
1. Activating built-but-unused servers
2. Creating universal tools (eliminate script proliferation)
3. Building cross-platform workflows (combine data sources)

**You're not in Phase 3 trying to reach Phase 4.**
**You're in Phase 5 approaching Phase 6** - autonomous execution with intelligent guardrails.

---

## 📋 **Next Action**

Want me to:

1. ✅ **COMPLETED:** Platform-ids server added, migration analyzed
2. **Build the Google Sheets MCP config** → Enable automated dashboard updates
3. **Build the Universal Budget Deployer** → Eliminate client-specific scripts
4. **Build the Inventory-Aware Optimizer** → Cross-platform automation proof-of-concept
5. **Create MCP usage guide** → When to use MCP vs direct imports (decision framework)

Which delivers the most value for you right now?
