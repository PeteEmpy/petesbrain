# P9 Universal Budget Deployer Files
**Created**: December 19, 2025
**Strategy**: Balanced scaling approach to avoid algorithm shock

## 📁 Files Ready for Deployment

### CSV Files (7 deployment stages)
1. ✅ `p9-dec-22-minimal.csv` - £2,000 minimal budgets
2. ✅ `p9-dec-23-minimal.csv` - £2,000 maintain minimal
3. ✅ `p9-dec-24-6pm-sale-launch.csv` - £3,500 sale launch (6pm)
4. ✅ `p9-dec-25-christmas.csv` - £6,000 Christmas Day
5. ✅ `p9-dec-26-boxing-day.csv` - £12,000 Boxing Day maximum
6. ✅ `p9-dec-27-sustained.csv` - £10,000 sustained high
7. ✅ `p9-dec-28-final.csv` - £8,000 final P9 day

### Deployment Tools
- ✅ `deploy.sh` - Simple deployment script for each date
- ✅ `p9-deployment-schedule.md` - Complete schedule with timing

## 🚀 Quick Deploy Commands

### Option 1: Use the deployment script
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/universal-budget-deployer

# Deploy for specific date
./deploy.sh dec-24  # For Dec 24 (will prompt for confirmation)
./deploy.sh dec-26  # For Boxing Day (will prompt for confirmation)
./deploy.sh check   # Check current status
```

### Option 2: Direct Universal Budget Deployer
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer

# Deploy specific CSV
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-24-6pm-sale-launch.csv \
  --mode apply \
  --verify
```

## ⏰ Critical Timing

| Date | Deploy Time | Budget | Critical? |
|------|-------------|--------|-----------|
| Dec 22 | 00:01 GMT | £2,000 | No |
| Dec 23 | 00:01 GMT | £2,000 | No |
| **Dec 24** | **17:45 GMT** | **£3,500** | **YES - Before 6pm sale!** |
| Dec 25 | 00:01 GMT | £6,000 | No |
| **Dec 26** | **00:01 GMT** | **£12,000** | **YES - Peak day!** |
| Dec 27 | 00:01 GMT | £10,000 | No |
| Dec 28 | 00:01 GMT | £8,000 | No |

## 📊 Strategy Summary

### Why Balanced Approach?
- **50+ campaigns** get budget (vs only 20 in concentrated approach)
- **Maximum 3-4x scaling** (vs risky 20x jumps)
- **Algorithm-friendly** gradual changes
- **Risk distributed** across portfolio
- **Natural optimization** by Google's Smart Bidding

### Tiered Distribution
- **Tier 1 (>1000% ROAS)**: 40% of budget
- **Tier 2 (700-1000%)**: 30% of budget
- **Tier 3 (500-700%)**: 20% of budget
- **Tier 4 (400-500%)**: 10% of budget

### Expected Results
- **ROAS**: 850-950% (reliable delivery)
- **Revenue**: £110-130k
- **Risk**: Significantly reduced
- **Flexibility**: Can shift budgets easily

## 🔄 Monitoring & Adjustments

### After Each Deployment
1. Verify budgets applied correctly
2. Check spend rate after 1 hour
3. Monitor top performers for budget exhaustion
4. Be ready to shift budget between campaigns

### Boxing Day (Dec 26) Special Monitoring
- Check hourly from 01:00 to 23:00
- Watch for campaigns hitting limits
- Ready to reallocate from underperformers
- Alert if spend rate >150% expected

## 📞 Support

**Primary**: Execute deployments as scheduled
**Dashboard**: `p9-balanced-deployment-dashboard.html`
**Tracking**: `p9-deployment-schedule.md`

## ✅ Pre-deployment Checklist

Before running any deployment:
1. Check current budgets match CSV "current_budget_gbp"
2. Verify API access to all 4 accounts
3. Have monitoring dashboard open
4. Keep this README handy

---

**Remember**: This is a balanced strategy designed to maximise opportunity while minimising risk. The system can handle the 3-4x scaling without shocking the algorithms.