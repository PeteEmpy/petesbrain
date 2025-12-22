#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add the shared module path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync/shared')
from client_tasks_service import ClientTasksService

def add_p9_deployment_tasks():
    """Add P9 deployment tasks to Smythson's task system"""

    service = ClientTasksService()

    # Define all P9 deployment tasks
    p9_tasks = [
        {
            "title": "[Smythson] P9 Deploy Dec 22 minimal budgets (£2,000 total)",
            "due_date": "2025-12-22",
            "priority": "P1",
            "time_estimate_mins": 30,
            "notes": """**P9 Deployment - Day 1 of Sale Period**

**Deploy at**: 00:01 GMT
**Budget**: £2,000 total (minimal)
**File**: `universal-budget-deployer/p9-dec-22-minimal.csv`

**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/universal-budget-deployer
./deploy.sh dec-22
```

**Distribution**:
- UK: £860
- USA: £650
- EUR: £360
- ROW: £130

**Active campaigns**: 44
**Strategy**: Keep campaigns warm before sale""",
            "tags": ["p9", "deployment", "sale-period"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 23 minimal budgets (£2,000 total)",
            "due_date": "2025-12-23",
            "priority": "P1",
            "time_estimate_mins": 30,
            "notes": """**P9 Deployment - Day 2 (Pre-sale)**

**Deploy at**: 00:01 GMT
**Budget**: £2,000 total (maintain minimal)
**File**: `universal-budget-deployer/p9-dec-23-minimal.csv`

**Command**:
```bash
./deploy.sh dec-23
```

**Distribution**: Same as Dec 22
**Active campaigns**: 44
**Strategy**: Maintain minimal presence before 6pm sale""",
            "tags": ["p9", "deployment", "sale-period"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 24 6pm SALE LAUNCH budgets (£3,500)",
            "due_date": "2025-12-24",
            "priority": "P0",
            "time_estimate_mins": 45,
            "notes": """**🔴 CRITICAL: SALE LAUNCH DEPLOYMENT**

**Deploy at**: 17:45 GMT (15 mins before 6pm sale!)
**Budget**: £3,500 total
**File**: `universal-budget-deployer/p9-dec-24-6pm-sale-launch.csv`

**Command**:
```bash
./deploy.sh dec-24
```

**Distribution**:
- UK: £1,505
- USA: £1,085
- EUR: £630
- ROW: £280

**Active campaigns**: 49
**Strategy**: Balanced scaling approach (1.5-2.5x increases)

**CRITICAL STEPS**:
1. Test API connectivity at 17:30
2. Deploy at 17:45
3. Verify at 18:00
4. Monitor hourly until midnight""",
            "tags": ["p9", "deployment", "sale-launch", "critical"]
        },
        {
            "title": "[Smythson] P9 Monitor Dec 24 evening performance (6pm-midnight)",
            "due_date": "2025-12-24",
            "priority": "P0",
            "time_estimate_mins": 180,
            "notes": """**Monitor Sale Launch Performance**

**Time**: 18:00-24:00 GMT
**Frequency**: Hourly checks

**Check**:
- Spend rate vs expected
- ROAS by region
- Budget utilization
- Campaign saturation

**Alert thresholds**:
- 🔴 Spend >150% of expected
- 🟡 ROAS drops >30%
- 🟢 Within 10% of target with ROAS >400%""",
            "tags": ["p9", "monitoring", "sale-launch"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 25 Christmas Day budgets (£6,000)",
            "due_date": "2025-12-25",
            "priority": "P1",
            "time_estimate_mins": 30,
            "notes": """**P9 Deployment - Christmas Day Scale**

**Deploy at**: 00:01 GMT
**Budget**: £6,000 total
**File**: `universal-budget-deployer/p9-dec-25-christmas.csv`

**Command**:
```bash
./deploy.sh dec-25
```

**Distribution**:
- UK: £2,600
- USA: £1,900
- EUR: £1,100
- ROW: £400

**Active campaigns**: 51
**Strategy**: Building momentum from sale launch""",
            "tags": ["p9", "deployment", "christmas"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 26 BOXING DAY maximum (£12,000)",
            "due_date": "2025-12-26",
            "priority": "P0",
            "time_estimate_mins": 60,
            "notes": """**🔴 CRITICAL: BOXING DAY MAXIMUM BUDGET**

**Deploy at**: 00:01 GMT
**Budget**: £12,000 total (PEAK DAY)
**File**: `universal-budget-deployer/p9-dec-26-boxing-day.csv`

**Command**:
```bash
./deploy.sh dec-26
```

**Distribution**:
- UK: £5,000
- USA: £3,800
- EUR: £2,500
- ROW: £700

**Active campaigns**: 59 (maximum participation)
**Strategy**: Balanced with 3-4x max scaling

**CRITICAL**: Set up hourly monitoring!""",
            "tags": ["p9", "deployment", "boxing-day", "peak", "critical"]
        },
        {
            "title": "[Smythson] P9 Monitor Boxing Day hourly performance",
            "due_date": "2025-12-26",
            "priority": "P0",
            "time_estimate_mins": 480,
            "notes": """**Boxing Day Hourly Monitoring**

**Time**: 01:00-23:00 GMT
**Frequency**: EVERY HOUR

**Monitor**:
- Campaign saturation
- Budget exhaustion
- ROAS by hour
- Ready to shift budgets

**Expected**: £500+/hour spend rate
**Alert if**: Any campaign exhausts budget before 6pm""",
            "tags": ["p9", "monitoring", "boxing-day", "critical"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 27 sustained high (£10,000)",
            "due_date": "2025-12-27",
            "priority": "P1",
            "time_estimate_mins": 30,
            "notes": """**P9 Deployment - Sustained High**

**Deploy at**: 00:01 GMT
**Budget**: £10,000 total
**File**: `universal-budget-deployer/p9-dec-27-sustained.csv`

**Command**:
```bash
./deploy.sh dec-27
```

**Distribution**:
- UK: £4,300
- USA: £3,200
- EUR: £2,000
- ROW: £500

**Active campaigns**: 58
**Strategy**: Maintain momentum from Boxing Day""",
            "tags": ["p9", "deployment", "sustained"]
        },
        {
            "title": "[Smythson] P9 Deploy Dec 28 final budgets (£8,000)",
            "due_date": "2025-12-28",
            "priority": "P1",
            "time_estimate_mins": 30,
            "notes": """**P9 Deployment - Final Day**

**Deploy at**: 00:01 GMT
**Budget**: £8,000 total
**File**: `universal-budget-deployer/p9-dec-28-final.csv`

**Command**:
```bash
./deploy.sh dec-28
```

**Distribution**:
- UK: £3,400
- USA: £2,600
- EUR: £1,600
- ROW: £400

**Active campaigns**: 58
**Strategy**: Final push before P9 ends

**Note**: This is the LAST day of P9 period""",
            "tags": ["p9", "deployment", "final-day"]
        },
        {
            "title": "[Smythson] P9 Create performance tracking dashboard",
            "due_date": "2025-12-21",
            "priority": "P2",
            "time_estimate_mins": 90,
            "notes": """**Create P9 Performance Tracking Dashboard**

**Before sale period starts, create**:
- HTML dashboard for daily tracking
- Spend vs budget visualization
- ROAS by region charts
- Campaign performance tables
- Alert indicators

**Location**: `reports/p9-performance-tracker.html`
**Update frequency**: Daily during sale period""",
            "tags": ["p9", "dashboard", "tracking"]
        }
    ]

    # Add each task
    added_count = 0
    for task_data in p9_tasks:
        try:
            task = service.create_task(
                title=task_data["title"],
                client="smythson",
                priority=task_data["priority"],
                due_date=task_data["due_date"],
                time_estimate_mins=task_data["time_estimate_mins"],
                notes=task_data["notes"],
                tags=task_data["tags"],
                source="P9 Balanced Scaling Strategy (Dec 19)"
            )
            added_count += 1
            print(f"✅ Added: {task_data['title'][:50]}...")
        except Exception as e:
            print(f"❌ Error adding task: {e}")

    print(f"\n✅ Successfully added {added_count} P9 deployment tasks to Smythson task system")
    print("These tasks will now appear in:")
    print("- Task Manager (with due dates)")
    print("- Reminder system (when due)")
    print("- Priority views (P0/P1/P2)")

if __name__ == "__main__":
    add_p9_deployment_tasks()