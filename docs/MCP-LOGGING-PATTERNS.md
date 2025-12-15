# MCP Server Logging Patterns

**Version**: 1.0
**Last Updated**: 2025-12-14
**Purpose**: Practical examples of applying PetesBrain logging standards to MCP server functions

---

## Overview

MCP servers use the **Context (`ctx`) parameter** for logging instead of the standard Python `logger`. The patterns from `LOGGING-STANDARDS.md` still apply, but are adapted for MCP's context-based logging.

**Key Difference:**
```python
# Standard Python logging
logger.info("Processing data...")
logger.error(f"Failed: {e}", exc_info=True)

# MCP context logging
ctx.info("Processing data...")
ctx.error(f"Failed: {e}")  # Note: No exc_info parameter
```

---

## MCP Context Logging Methods

| Method | When to Use | Example |
|--------|-------------|---------|
| `ctx.info()` | Normal operation confirmation | `ctx.info("✅ Campaign created successfully")` |
| `ctx.warning()` | Unexpected but not critical | `ctx.warning("⚠️  No location targets found")` |
| `ctx.error()` | Operation failed | `ctx.error(f"❌ API call failed: {e}")` |
| `ctx.debug()` | Detailed diagnostic info | `ctx.debug(f"Query: {query}")` |

**Note**: MCP context logging automatically includes timestamps and routing to Claude Code. You don't need to configure handlers.

---

## Pattern 1: Enhanced Entry/Exit Logging

### Current Pattern (Good)

```python
@mcp.tool
def create_campaign(
    customer_id: str,
    campaign_name: str,
    daily_budget_micros: int,
    ctx: Context = None
):
    if ctx:
        ctx.info(f"Creating campaign '{campaign_name}' for customer {customer_id}")

    # ... operation ...

    if ctx:
        ctx.info(f"✅ Campaign created successfully! ID: {campaign_id}")

    return result
```

### Enhanced Pattern (Better)

```python
@mcp.tool
def create_campaign(
    customer_id: str,
    campaign_name: str,
    daily_budget_micros: int,
    target_roas: float = None,
    locations: List[str] = None,
    campaign_type: str = "SEARCH",
    status: str = "PAUSED",
    ctx: Context = None
):
    if ctx:
        ctx.info("=" * 60)
        ctx.info(f"🚀 Creating Campaign")
        ctx.info(f"  - Name: {campaign_name}")
        ctx.info(f"  - Customer ID: {customer_id}")
        ctx.info(f"  - Budget: £{daily_budget_micros / 1000000:.2f}/day")
        ctx.info(f"  - Type: {campaign_type}")
        ctx.info(f"  - Status: {status}")
        if target_roas:
            ctx.info(f"  - Target ROAS: {target_roas:.1f}x ({target_roas * 100:.0f}%)")
        if locations:
            ctx.info(f"  - Locations: {len(locations)} targets")
        ctx.info("=" * 60)

    try:
        # ... operation ...

        if ctx:
            ctx.info("=" * 60)
            ctx.info("✅ Campaign Created Successfully")
            ctx.info(f"  - Campaign ID: {campaign_id}")
            ctx.info(f"  - Resource Name: {campaign_resource_name}")
            ctx.info(f"  - Budget Resource: {budget_resource_name}")
            ctx.info(f"  - Google Ads UI: https://ads.google.com/aw/campaigns?campaignId={campaign_id}")
            ctx.info("=" * 60)

        return result

    except Exception as e:
        if ctx:
            ctx.error("=" * 60)
            ctx.error("❌ Campaign Creation Failed")
            ctx.error(f"  - Error: {e}")
            ctx.error("=" * 60)
        raise
```

**What Changed:**
- Added visual separators for clarity
- Log ALL input parameters (helps debugging)
- Show calculated values (budget in £, ROAS as percentage)
- Structured success/error messages with context

---

## Pattern 2: Decision Point Logging with Values

### Current Pattern (Missing Context)

```python
if target_roas:
    campaign_create['biddingStrategyType'] = 'TARGET_ROAS'
    campaign_create['targetRoas'] = {'targetRoas': target_roas}
elif target_cpa_micros:
    campaign_create['biddingStrategyType'] = 'TARGET_CPA'
    campaign_create['targetCpa'] = {'targetCpaMicros': str(target_cpa_micros)}
else:
    campaign_create['biddingStrategyType'] = 'MAXIMIZE_CLICKS'
```

### Enhanced Pattern (With Decision Context)

```python
if ctx:
    ctx.info("🎯 Determining bidding strategy...")

if target_roas:
    if ctx:
        ctx.info(f"  ✓ Using Target ROAS")
        ctx.info(f"    - Target: {target_roas:.1f}x")
        ctx.info(f"    - Percentage: {target_roas * 100:.0f}%")
    campaign_create['biddingStrategyType'] = 'TARGET_ROAS'
    campaign_create['targetRoas'] = {'targetRoas': target_roas}

elif target_cpa_micros:
    if ctx:
        ctx.info(f"  ✓ Using Target CPA")
        ctx.info(f"    - Target: £{target_cpa_micros / 1000000:.2f}")
    campaign_create['biddingStrategyType'] = 'TARGET_CPA'
    campaign_create['targetCpa'] = {'targetCpaMicros': str(target_cpa_micros)}

else:
    if ctx:
        ctx.info(f"  ✓ Using Maximize Clicks (no target specified)")
    campaign_create['biddingStrategyType'] = 'MAXIMIZE_CLICKS'
```

**What Changed:**
- Log the decision being made
- Show the actual values being used
- Show converted values (micros → £, decimal → %)
- Makes it clear WHY this bidding strategy was chosen

---

## Pattern 3: Error Context with Full Debugging Package

### Current Pattern (Basic Error)

```python
try:
    result = execute_gaql(customer_id, query, manager_id)
except Exception as e:
    if ctx:
        ctx.error(f"Query failed: {str(e)}")
    raise
```

### Enhanced Pattern (Complete Debugging Package)

```python
try:
    if ctx:
        ctx.debug(f"Executing GAQL query...")
        ctx.debug(f"Query: {query}")

    result = execute_gaql(customer_id, query, manager_id)

    if ctx:
        ctx.info(f"✅ Query successful: {len(result.get('results', []))} rows returned")
        if result.get('results'):
            ctx.debug(f"Sample row: {result['results'][0]}")

except Exception as e:
    if ctx:
        ctx.error("=" * 60)
        ctx.error("❌ GAQL Query Failed - Debugging Package")
        ctx.error("=" * 60)

        # 1. What was being attempted
        ctx.error("1. Operation Context:")
        ctx.error(f"   - Function: execute_gaql")
        ctx.error(f"   - Customer ID: {customer_id}")
        ctx.error(f"   - Manager ID: {manager_id}")

        # 2. Exact error
        ctx.error("2. Error Details:")
        ctx.error(f"   - Type: {type(e).__name__}")
        ctx.error(f"   - Message: {str(e)}")

        # 3. Data that caused the error
        ctx.error("3. Query Attempted:")
        ctx.error(f"{query}")

        # 4. Additional context
        ctx.error("4. Possible Causes:")
        if "PERMISSION_DENIED" in str(e):
            ctx.error("   - OAuth token may be expired")
            ctx.error("   - Action: Run oauth-refresh skill")
        elif "INVALID_CUSTOMER_ID" in str(e):
            ctx.error("   - Customer ID may be incorrect")
            ctx.error(f"   - Provided: {customer_id}")
        elif "DEADLINE_EXCEEDED" in str(e):
            ctx.error("   - Query timeout (too complex or too much data)")
            ctx.error("   - Action: Add date filter or reduce query scope")

        ctx.error("=" * 60)
    raise
```

**What Changed:**
- Complete debugging package (4 sections: context, error, data, causes)
- Specific remediation steps based on error type
- Show the actual query that failed
- Visual separators for easy log scanning

---

## Pattern 4: Safety Check Logging (Asset Replacement)

### Current Pattern (Good Safety Checks)

```python
# Calculate counts after removals
final_counts = {
    'HEADLINE': asset_counts['HEADLINE'] - removal_counts['HEADLINE'],
    'LONG_HEADLINE': asset_counts['LONG_HEADLINE'] - removal_counts['LONG_HEADLINE'],
    'DESCRIPTION': asset_counts['DESCRIPTION'] - removal_counts['DESCRIPTION']
}

# Check if any type falls below minimum
if safety_violations:
    if ctx:
        ctx.error(f"SAFETY CHECK FAILED: {len(safety_violations)} violations detected")
    return {
        'success': False,
        'safety_check': 'FAILED',
        'violations': safety_violations
    }
```

### Enhanced Pattern (With Detailed Logging)

```python
if ctx:
    ctx.info("🔒 Running safety checks...")
    ctx.info("Current asset counts:")
    for asset_type, count in asset_counts.items():
        ctx.info(f"  - {asset_type}: {count}")

    ctx.info("Planned removals:")
    for asset_type, count in removal_counts.items():
        if count > 0:
            ctx.info(f"  - {asset_type}: -{count}")

    ctx.info("Final counts (after removals):")
    for asset_type, final_count in final_counts.items():
        minimum = minimums[asset_type]
        status = "✅" if final_count >= minimum else "❌"
        ctx.info(f"  {status} {asset_type}: {final_count} (minimum: {minimum})")

# Check if any type falls below minimum
if safety_violations:
    if ctx:
        ctx.error("=" * 60)
        ctx.error("🚨 SAFETY CHECK FAILED")
        ctx.error("=" * 60)

        for violation in safety_violations:
            ctx.error(f"❌ {violation['asset_type']}:")
            ctx.error(f"   - Current: {violation['current']}")
            ctx.error(f"   - Removing: {violation['removing']}")
            ctx.error(f"   - Would leave: {violation['final']}")
            ctx.error(f"   - Minimum required: {violation['minimum']}")
            ctx.error(f"   - Shortfall: {violation['minimum'] - violation['final']}")

        ctx.error("")
        ctx.error("⚠️  Cannot proceed - would violate Google Ads minimums")
        ctx.error("Action required: Reduce removals or add more assets first")
        ctx.error("=" * 60)

    return {
        'success': False,
        'safety_check': 'FAILED',
        'violations': safety_violations,
        'current_counts': asset_counts,
        'removal_counts': removal_counts,
        'final_counts': final_counts,
        'minimums': minimums
    }

# Safety check passed
if ctx:
    ctx.info("=" * 60)
    ctx.info("✅ Safety Check PASSED")
    ctx.info("All minimum requirements will be maintained after replacements")
    ctx.info("=" * 60)
```

**What Changed:**
- Show the math being performed (current - removals = final)
- Visual indicators (✅/❌) for each asset type
- Calculate and show shortfall (how many more needed)
- Clear action required message
- Structured output for easy understanding

---

## Pattern 5: Multi-Step Operation Logging

### Current Pattern (Basic Step Logging)

```python
# Step 1: Create budget
if ctx:
    ctx.info(f"Creating budget: £{daily_budget_micros / 1000000:.2f}/day")

budget_resp = requests.post(budget_url, headers=headers, json=budget_payload)

# Step 2: Create campaign
if ctx:
    ctx.info(f"Creating campaign with type: {campaign_type}, status: {status}")

campaign_resp = requests.post(campaign_url, headers=headers, json=campaign_payload)

# Step 3: Add location targeting
if ctx:
    ctx.info(f"Adding {len(locations)} location target(s)")

location_resp = requests.post(location_url, headers=headers, json=location_payload)
```

### Enhanced Pattern (Progress Tracking)

```python
total_steps = 3
current_step = 0

# Step 1: Create budget
current_step += 1
if ctx:
    ctx.info("=" * 60)
    ctx.info(f"Step {current_step}/{total_steps}: Creating Campaign Budget")
    ctx.info(f"  - Daily budget: £{daily_budget_micros / 1000000:.2f}")
    ctx.info(f"  - Delivery method: STANDARD")

try:
    budget_resp = requests.post(budget_url, headers=headers, json=budget_payload)
    budget_resp.raise_for_status()
    budget_resource_name = budget_resp.json()['results'][0]['resourceName']

    if ctx:
        ctx.info(f"✅ Budget created: {budget_resource_name}")

except Exception as e:
    if ctx:
        ctx.error(f"❌ Step {current_step} failed: Budget creation")
        ctx.error(f"Error: {e}")
        ctx.error(f"Response: {budget_resp.text if budget_resp else 'No response'}")
    raise

# Step 2: Create campaign
current_step += 1
if ctx:
    ctx.info("=" * 60)
    ctx.info(f"Step {current_step}/{total_steps}: Creating Campaign")
    ctx.info(f"  - Name: {campaign_name}")
    ctx.info(f"  - Type: {campaign_type}")
    ctx.info(f"  - Status: {status}")
    ctx.info(f"  - Budget: {budget_resource_name}")

try:
    campaign_resp = requests.post(campaign_url, headers=headers, json=campaign_payload)
    campaign_resp.raise_for_status()
    campaign_resource_name = campaign_resp.json()['results'][0]['resourceName']
    campaign_id = campaign_resource_name.split('/')[-1]

    if ctx:
        ctx.info(f"✅ Campaign created: {campaign_id}")

except Exception as e:
    if ctx:
        ctx.error(f"❌ Step {current_step} failed: Campaign creation")
        ctx.error(f"Error: {e}")
        ctx.error(f"Response: {campaign_resp.text if campaign_resp else 'No response'}")
        ctx.error(f"Note: Budget was created successfully ({budget_resource_name})")
        ctx.error(f"Action: May need manual cleanup in Google Ads UI")
    raise

# Step 3: Add location targeting
current_step += 1
if ctx:
    ctx.info("=" * 60)
    ctx.info(f"Step {current_step}/{total_steps}: Adding Location Targeting")
    ctx.info(f"  - Locations: {locations}")
    ctx.info(f"  - Campaign: {campaign_resource_name}")

try:
    location_resp = requests.post(location_url, headers=headers, json=location_payload)
    location_resp.raise_for_status()

    if ctx:
        ctx.info(f"✅ {len(locations)} location target(s) added")

except Exception as e:
    # Non-fatal error - campaign is already created
    if ctx:
        ctx.warning(f"⚠️  Step {current_step} failed: Location targeting")
        ctx.warning(f"Error: {e}")
        ctx.warning(f"Note: Campaign was created successfully")
        ctx.warning(f"Action: Add location targets manually in Google Ads UI")
```

**What Changed:**
- Progress tracking (Step X/Y)
- Clear step boundaries with separators
- Try/except per step (not just overall)
- Error messages include what succeeded before failure
- Guidance on cleanup/recovery when mid-operation failures occur

---

## Pattern 6: API Response Validation

### Current Pattern (Basic Success Check)

```python
resp = requests.post(url, headers=headers, json=payload)
if not resp.ok:
    error_msg = f"Error: {resp.status_code} - {resp.text}"
    if ctx:
        ctx.error(error_msg)
    raise Exception(error_msg)
```

### Enhanced Pattern (Detailed Validation)

```python
if ctx:
    ctx.debug(f"Making API request to: {url}")
    ctx.debug(f"Payload: {json.dumps(payload, indent=2)}")

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)

    if ctx:
        ctx.debug(f"Response status: {resp.status_code}")

    # Check for success
    if not resp.ok:
        error_data = None
        try:
            error_data = resp.json()
        except:
            pass

        if ctx:
            ctx.error("=" * 60)
            ctx.error("❌ API Request Failed")
            ctx.error("=" * 60)
            ctx.error(f"Status Code: {resp.status_code}")
            ctx.error(f"URL: {url}")

            if error_data:
                ctx.error("Error Response:")
                ctx.error(f"{json.dumps(error_data, indent=2)}")

                # Parse Google Ads specific errors
                if 'error' in error_data:
                    google_error = error_data['error']
                    if 'message' in google_error:
                        ctx.error(f"Google Ads Error: {google_error['message']}")
                    if 'details' in google_error:
                        for detail in google_error['details']:
                            ctx.error(f"Detail: {detail}")
            else:
                ctx.error(f"Raw Response: {resp.text[:500]}")  # First 500 chars

            # Common error remediation
            if resp.status_code == 401:
                ctx.error("Authentication failed - check OAuth token")
            elif resp.status_code == 403:
                ctx.error("Permission denied - check account access")
            elif resp.status_code == 429:
                ctx.error("Rate limit exceeded - wait before retrying")
            elif resp.status_code == 500:
                ctx.error("Google Ads API error - may be temporary")

            ctx.error("=" * 60)

        raise Exception(f"API request failed: {resp.status_code}")

    # Parse successful response
    result = resp.json()

    if ctx:
        ctx.debug(f"Response contains {len(result.get('results', []))} results")

    return result

except requests.Timeout as e:
    if ctx:
        ctx.error(f"❌ API request timeout after 30s")
        ctx.error(f"URL: {url}")
        ctx.error("Action: Reduce payload size or check network connection")
    raise

except requests.RequestException as e:
    if ctx:
        ctx.error(f"❌ Network error during API request")
        ctx.error(f"URL: {url}")
        ctx.error(f"Error: {e}")
    raise
```

**What Changed:**
- Log request details (URL, payload) at DEBUG level
- Parse and display Google Ads error structure
- Specific remediation for HTTP status codes
- Separate timeout handling from other network errors
- Truncate very long error responses (first 500 chars)

---

## Pattern 7: Dry Run Mode Logging

### Current Pattern (Basic Dry Run)

```python
if dry_run:
    if ctx:
        ctx.info("Dry run mode - no changes will be made")
    return result
```

### Enhanced Pattern (Clear Dry Run Output)

```python
if dry_run:
    if ctx:
        ctx.info("=" * 60)
        ctx.info("🧪 DRY RUN MODE - No Changes Will Be Made")
        ctx.info("=" * 60)
        ctx.info("Safety checks completed successfully")
        ctx.info("")
        ctx.info("Planned changes:")
        for i, replacement in enumerate(replacements, 1):
            ctx.info(f"  {i}. {replacement['field_type']}:")
            ctx.info(f"     - Old: '{replacement['old_text']}'")
            ctx.info(f"     - New: '{replacement['new_text']}'")
        ctx.info("")
        ctx.info("Final asset counts (after changes):")
        for asset_type, count in final_counts.items():
            minimum = minimums[asset_type]
            status = "✅" if count >= minimum else "❌"
            ctx.info(f"  {status} {asset_type}: {count} (minimum: {minimum})")
        ctx.info("")
        ctx.info("To execute these changes, call again with dry_run=False")
        ctx.info("=" * 60)

    return {
        'success': True,
        'dry_run': True,
        'safety_check': 'PASSED',
        'planned_changes': replacements,
        'final_counts': final_counts,
        'message': 'Dry run completed - no changes made'
    }
```

**What Changed:**
- Clear visual indication this is a dry run
- Show exactly what WOULD happen
- Show before/after for each change
- Final validation of counts
- Explicit instruction on how to execute for real

---

## Quick Reference: Logging Checklist for MCP Functions

### Entry Log ✅
```python
if ctx:
    ctx.info("=" * 60)
    ctx.info("🚀 [Operation Name]")
    ctx.info(f"  - Parameter1: {param1}")
    ctx.info(f"  - Parameter2: {param2}")
    ctx.info("=" * 60)
```

### Decision Point Log ✅
```python
if ctx:
    ctx.info(f"Decision: {decision_being_made}")
    ctx.info(f"  - Value being checked: {actual_value}")
    ctx.info(f"  - Threshold: {threshold}")
    ctx.info(f"  - Result: {chosen_action}")
```

### Success Log ✅
```python
if ctx:
    ctx.info("=" * 60)
    ctx.info("✅ [Operation] Completed Successfully")
    ctx.info(f"  - Result1: {result1}")
    ctx.info(f"  - Result2: {result2}")
    ctx.info("=" * 60)
```

### Error Log ✅
```python
except Exception as e:
    if ctx:
        ctx.error("=" * 60)
        ctx.error("❌ [Operation] Failed")
        ctx.error(f"  - Error: {e}")
        ctx.error(f"  - Context: {what_was_being_attempted}")
        ctx.error(f"  - Data: {data_that_caused_error}")
        ctx.error("=" * 60)
    raise
```

---

## Migration Strategy

### Phase 1: High-Risk Functions (Priority)
Apply enhanced logging to functions that:
- Make destructive changes (replace_*, update_*, delete_*)
- Have complex safety checks (asset replacement, budget changes)
- Are frequently called by automation

**Target functions:**
1. `replace_asset_group_text_assets()`
2. `replace_rsa_text_assets()`
3. `update_campaign_budget()`
4. `update_campaign_target_roas()`
5. `update_campaign_status()`

### Phase 2: Creation Functions
Apply enhanced logging to functions that create resources:
- `create_campaign()`
- `create_ad_group()`
- `create_asset_group()`
- `create_responsive_search_ad()`

### Phase 3: Query Functions
Apply enhanced logging to data retrieval:
- `run_gaql()` (already has good logging)
- `get_campaign_performance()`

### Phase 4: Helper Functions
Apply to internal helpers:
- `execute_gaql()`
- API request wrappers
- Authentication functions

---

## Testing Enhanced Logging

### 1. Test Entry/Exit Logs

```python
# Call the function
result = mcp__google_ads__create_campaign(
    customer_id="1234567890",
    campaign_name="Test Campaign",
    daily_budget_micros=50000000
)

# Check logs show:
# ✅ Start log with all parameters
# ✅ Each step in the operation
# ✅ Success log with results
```

### 2. Test Error Logging

```python
# Trigger an error intentionally
result = mcp__google_ads__create_campaign(
    customer_id="INVALID_ID",
    campaign_name="Test Campaign",
    daily_budget_micros=50000000
)

# Check logs show:
# ✅ Error debugging package
# ✅ Context (what was being attempted)
# ✅ Exact error message
# ✅ Remediation steps
```

### 3. Test Decision Point Logs

```python
# Call with different parameters to test different code paths
result1 = create_campaign(target_roas=4.0)  # Should log ROAS chosen
result2 = create_campaign(target_cpa_micros=10000000)  # Should log CPA chosen
result3 = create_campaign()  # Should log Maximize Clicks chosen

# Check logs show:
# ✅ Decision being made
# ✅ Values being compared
# ✅ Chosen path
```

### 4. Test Safety Check Logs

```python
# Trigger safety violation
result = mcp__google_ads__replace_asset_group_text_assets(
    replacements=[...],  # Remove too many assets
    dry_run=True
)

# Check logs show:
# ✅ Current counts
# ✅ Planned removals
# ✅ Final counts
# ✅ Safety violations with details
# ✅ Clear remediation steps
```

---

## Related Documentation

- `/docs/LOGGING-STANDARDS.md` - Core logging patterns for PetesBrain
- `/docs/GOOGLE-ADS-PROTOCOL.md` - Google Ads change protection workflow
- `/infrastructure/mcp-servers/google-ads-mcp-server/README.md` - MCP server documentation

**Version History:**
- v1.0 (2025-12-14): Initial MCP logging patterns based on LOGGING-STANDARDS.md
