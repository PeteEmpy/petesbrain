# PetesBrain Logging Standards

**Version**: 1.0
**Last Updated**: 2025-12-14
**Purpose**: Standardised logging patterns for all PetesBrain agents and MCP functions

---

## Core Principle

**Automated work fails invisibly. Logging makes the invisible visible.**

When a manual process fails, you see it immediately. When an automated LaunchAgent fails at 3 AM, logging is your only visibility into what happened and why.

---

## Standard Logging Configuration

### Python Logging Setup

**Every agent must include this standard configuration:**

```python
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
LOG_DIR = Path.home() / '.petesbrain-logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'{__name__}_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler()  # Also output to console for LaunchAgent logs
    ]
)

logger = logging.getLogger(__name__)
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnostic info | `logger.debug(f"Query parameters: customer_id={customer_id}, date_range={date_range}")` |
| **INFO** | Confirmation that things are working | `logger.info("✅ Daily briefing generated successfully")` |
| **WARNING** | Something unexpected but not critical | `logger.warning(f"No calendar events found for {date}")` |
| **ERROR** | Something failed but agent can continue | `logger.error(f"Failed to fetch GA4 data: {e}", exc_info=True)` |
| **CRITICAL** | Agent cannot continue | `logger.critical("OAuth token expired, cannot authenticate")` |

---

## Three-Layer Logging Pattern

### Layer 1: Entry/Exit Logs

**Purpose**: Confirm the agent started and finished

**Required for every agent:**

```python
def main():
    logger.info("=" * 60)
    logger.info("🚀 Starting Daily Budget Monitor")
    logger.info(f"📅 Date: {datetime.now():%Y-%m-%d %H:%M:%S}")
    logger.info("=" * 60)

    try:
        # Agent logic here
        result = monitor_budgets()

        logger.info("=" * 60)
        logger.info("✅ Daily Budget Monitor completed successfully")
        logger.info(f"📊 Results: {result}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ Daily Budget Monitor failed")
        logger.error(f"Error: {e}", exc_info=True)
        logger.error("=" * 60)
        raise
```

### Layer 2: Decision Point Logs

**Purpose**: Record WHY automated decisions were made

**Critical for autonomous systems:**

```python
# ❌ BAD - No context about the decision
if deviation > threshold:
    send_alert()

# ✅ GOOD - Log the decision WITH the values that led to it
logger.info(f"📊 Budget deviation check:")
logger.info(f"  - Actual spend: £{actual_spend:.2f}")
logger.info(f"  - Expected spend: £{expected_spend:.2f}")
logger.info(f"  - Deviation: {deviation:.1f}%")
logger.info(f"  - Threshold: {threshold}%")

if deviation > threshold:
    logger.warning(f"🚨 ALERT triggered: {deviation:.1f}% exceeds {threshold}% threshold")
    send_alert(client, actual_spend, expected_spend, deviation)
else:
    logger.info(f"✅ Within threshold: {deviation:.1f}% < {threshold}%")
```

### Layer 3: Error Context Logs

**Purpose**: Provide full context when errors occur

**Required for all try/except blocks:**

```python
# ❌ BAD - No context about what was being attempted
try:
    result = mcp__google_ads__run_gaql(customer_id, query)
except Exception as e:
    logger.error(f"Query failed: {e}")

# ✅ GOOD - Full context for debugging
try:
    logger.debug(f"Executing GAQL query for customer {customer_id}")
    logger.debug(f"Query: {query}")

    result = mcp__google_ads__run_gaql(
        customer_id=customer_id,
        manager_id=manager_id,
        query=query
    )

    logger.info(f"✅ Query successful: {len(result)} rows returned")

except Exception as e:
    logger.error(f"❌ GAQL query failed for customer {customer_id}")
    logger.error(f"Query attempted: {query}")
    logger.error(f"Parameters: customer_id={customer_id}, manager_id={manager_id}")
    logger.error(f"Error: {e}", exc_info=True)
    raise
```

---

## Five-Log Minimum

**Every agent execution must log these 5 events:**

### 1. Start Log

```python
logger.info("🚀 Starting {Agent Name}")
logger.info(f"📅 Execution time: {datetime.now():%Y-%m-%d %H:%M:%S}")
logger.info(f"📋 Parameters: client={client}, date_range={date_range}")
```

### 2. Data Collection Log

```python
logger.info("📥 Collecting data...")
logger.info(f"  - Querying Google Ads API for customer {customer_id}")
logger.info(f"  - Date range: {start_date} to {end_date}")

# After collection
logger.info(f"✅ Data collected: {len(campaigns)} campaigns, {len(ad_groups)} ad groups")
```

### 3. Processing Log

```python
logger.info("⚙️  Processing data...")
logger.info(f"  - Calculating ROAS for {len(campaigns)} campaigns")
logger.info(f"  - Comparing against targets")

# Log key calculations
for campaign in campaigns:
    roas = campaign['revenue'] / campaign['cost']
    logger.debug(f"Campaign {campaign['name']}: ROAS = {roas:.2f}x (target: {campaign['target']:.2f}x)")
```

### 4. Output Log

```python
logger.info("📤 Generating output...")
logger.info(f"  - Creating email report")
logger.info(f"  - Saving to: {report_path}")

# After output
logger.info(f"✅ Report saved: {report_path}")
logger.info(f"📧 Email sent to: {recipient}")
```

### 5. End Log

```python
logger.info("=" * 60)
logger.info("✅ {Agent Name} completed successfully")
logger.info(f"⏱️  Total duration: {duration:.2f}s")
logger.info(f"📊 Summary: {summary_stats}")
logger.info("=" * 60)
```

---

## PetesBrain-Specific Patterns

### Google Ads API Calls

```python
def query_google_ads(customer_id, manager_id, query):
    """Query Google Ads API with full logging."""

    logger.info(f"📊 Google Ads Query")
    logger.info(f"  - Customer ID: {customer_id}")
    logger.info(f"  - Manager ID: {manager_id}")
    logger.debug(f"  - Query: {query}")

    try:
        result = mcp__google_ads__run_gaql(
            customer_id=customer_id,
            manager_id=manager_id,
            query=query
        )

        logger.info(f"✅ Query successful: {len(result)} rows returned")

        # Log first few rows for verification
        if result and len(result) > 0:
            logger.debug(f"Sample row: {result[0]}")

        return result

    except Exception as e:
        logger.error(f"❌ Google Ads query failed")
        logger.error(f"Customer ID: {customer_id}")
        logger.error(f"Manager ID: {manager_id}")
        logger.error(f"Query: {query}")
        logger.error(f"Error: {e}", exc_info=True)

        # Return empty result to allow agent to continue
        logger.warning("⚠️  Returning empty result, agent will continue")
        return []
```

### MCP Timeout Handling

```python
def call_mcp_with_retry(func, *args, max_retries=3, timeout=30, **kwargs):
    """Call MCP function with timeout and retry logic."""

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"🔄 MCP call attempt {attempt}/{max_retries}")
            logger.debug(f"Function: {func.__name__}")
            logger.debug(f"Args: {args}, Kwargs: {kwargs}")

            result = func(*args, **kwargs)

            logger.info(f"✅ MCP call successful on attempt {attempt}")
            return result

        except TimeoutError as e:
            logger.warning(f"⏱️  MCP timeout on attempt {attempt}/{max_retries}")
            logger.warning(f"Timeout duration: {timeout}s")

            if attempt == max_retries:
                logger.error(f"❌ MCP call failed after {max_retries} attempts")
                logger.error(f"Function: {func.__name__}")
                logger.error(f"Error: {e}", exc_info=True)
                raise

            logger.info(f"⏳ Waiting 5s before retry...")
            time.sleep(5)

        except Exception as e:
            logger.error(f"❌ MCP call failed with unexpected error")
            logger.error(f"Function: {func.__name__}")
            logger.error(f"Attempt: {attempt}/{max_retries}")
            logger.error(f"Error: {e}", exc_info=True)
            raise
```

### OAuth Token Expiration

```python
def check_oauth_token(service_name):
    """Check OAuth token validity before API calls."""

    logger.info(f"🔐 Checking OAuth token for {service_name}")

    try:
        # Attempt a simple API call to verify token
        test_result = test_api_connection()

        logger.info(f"✅ OAuth token valid for {service_name}")
        return True

    except AuthenticationError as e:
        logger.error(f"🔑 OAuth token expired for {service_name}")
        logger.error(f"Error: {e}")
        logger.error(f"Action required: Run oauth-refresh skill")

        # Exit with specific code for LaunchAgent monitoring
        logger.critical("Exiting with code 78 (OAuth failure)")
        sys.exit(78)

    except Exception as e:
        logger.error(f"❌ Unexpected error checking OAuth token")
        logger.error(f"Service: {service_name}")
        logger.error(f"Error: {e}", exc_info=True)
        raise
```

### Email Processing

```python
def process_email(message):
    """Process email with full context logging."""

    logger.info("=" * 60)
    logger.info(f"📧 Processing email")
    logger.info(f"  - From: {message['from']}")
    logger.info(f"  - Subject: {message['subject']}")
    logger.info(f"  - Date: {message['date']}")
    logger.info(f"  - Thread ID: {message['thread_id']}")

    try:
        # Determine client from sender
        client = detect_client(message['from'])
        logger.info(f"🏷️  Detected client: {client}")

        # Apply labels
        labels_applied = apply_labels(message, client)
        logger.info(f"✅ Labels applied: {labels_applied}")

        # Save to client folder
        save_path = save_email_to_folder(message, client)
        logger.info(f"💾 Saved to: {save_path}")

        logger.info("=" * 60)
        return True

    except Exception as e:
        logger.error(f"❌ Email processing failed")
        logger.error(f"Message ID: {message['id']}")
        logger.error(f"From: {message['from']}")
        logger.error(f"Subject: {message['subject']}")
        logger.error(f"Error: {e}", exc_info=True)
        logger.error("=" * 60)
        return False
```

---

## Common Logging Anti-Patterns

### ❌ Anti-Pattern 1: Silent Failures

```python
# BAD
try:
    result = fetch_data()
except:
    pass  # Silent failure, no visibility

# GOOD
try:
    result = fetch_data()
except Exception as e:
    logger.error(f"Failed to fetch data: {e}", exc_info=True)
    result = None  # Explicit fallback
```

### ❌ Anti-Pattern 2: Missing Context

```python
# BAD
logger.error(f"Query failed: {e}")

# GOOD
logger.error(f"GAQL query failed for customer {customer_id}")
logger.error(f"Query: {query}")
logger.error(f"Error: {e}", exc_info=True)
```

### ❌ Anti-Pattern 3: Print Instead of Logging

```python
# BAD
print("Processing data...")

# GOOD
logger.info("⚙️  Processing data...")
```

### ❌ Anti-Pattern 4: No Decision Context

```python
# BAD
if roas < target:
    create_task()

# GOOD
logger.info(f"ROAS check: {roas:.2f}x vs target {target:.2f}x")
if roas < target:
    logger.warning(f"🚨 ROAS below target, creating task")
    create_task()
else:
    logger.info(f"✅ ROAS on target")
```

---

## Debugging Package Template

**When an agent fails, these logs create a complete debugging package:**

```python
def create_debugging_package(error, context):
    """Generate debugging package for failed execution."""

    logger.error("=" * 60)
    logger.error("🐛 DEBUGGING PACKAGE")
    logger.error("=" * 60)

    # 1. Script identification
    logger.error(f"Script: {__file__}")
    logger.error(f"Function: {context['function']}")
    logger.error(f"Execution time: {datetime.now():%Y-%m-%d %H:%M:%S}")

    # 2. Exact error
    logger.error(f"Error type: {type(error).__name__}")
    logger.error(f"Error message: {str(error)}")
    logger.error("Stack trace:", exc_info=True)

    # 3. Logs before error (already in log file)
    logger.error(f"See full log: {LOG_DIR / f'{__name__}_{datetime.now():%Y%m%d}.log'}")

    # 4. Sample data that caused error
    logger.error("Context data:")
    for key, value in context.items():
        logger.error(f"  - {key}: {value}")

    logger.error("=" * 60)
```

---

## Migration Guide

### Converting Existing Agents

**Step 1: Replace print() with logging**

```python
# Before
print("Starting agent...")
print(f"Processing {len(items)} items")

# After
logger.info("🚀 Starting agent...")
logger.info(f"⚙️  Processing {len(items)} items")
```

**Step 2: Add error context**

```python
# Before
try:
    result = process()
except Exception as e:
    print(f"Error: {e}")

# After
try:
    logger.info("⚙️  Processing data...")
    result = process()
    logger.info("✅ Processing complete")
except Exception as e:
    logger.error("❌ Processing failed")
    logger.error(f"Error: {e}", exc_info=True)
    raise
```

**Step 3: Add decision point logging**

```python
# Before
if value > threshold:
    take_action()

# After
logger.info(f"Threshold check: {value} vs {threshold}")
if value > threshold:
    logger.warning(f"🚨 Threshold exceeded: {value} > {threshold}")
    take_action()
else:
    logger.info(f"✅ Within threshold: {value} <= {threshold}")
```

---

## Testing Your Logs

### Manual Testing

1. **Run agent locally with DEBUG level:**
   ```bash
   LOG_LEVEL=DEBUG python3 agent.py
   ```

2. **Check log output includes:**
   - ✅ Start/end logs
   - ✅ Data collection confirmation
   - ✅ Processing steps
   - ✅ Decision points with values
   - ✅ Output confirmation

3. **Trigger an error intentionally:**
   ```python
   # Temporarily break something to test error logging
   customer_id = "INVALID_ID"
   ```

4. **Verify debugging package is complete:**
   - ✅ Error type and message
   - ✅ Full stack trace
   - ✅ Context data (what was being processed)
   - ✅ Logs before error (in log file)

### LaunchAgent Testing

```bash
# Unload agent
launchctl unload ~/Library/LaunchAgents/co.roksys.petesbrain.{agent}.plist

# Run manually to see logs
/path/to/venv/bin/python3 /path/to/agent.py

# Check log file
tail -100 ~/.petesbrain-logs/{agent}_$(date +%Y%m%d).log

# Reload agent
launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.{agent}.plist
```

---

## Log Retention

**Retention policy:**
- Daily logs: Keep 30 days
- Error logs: Keep 90 days
- Critical failure logs: Keep indefinitely

**Cleanup script** (add to weekly maintenance):

```python
def cleanup_old_logs():
    """Remove logs older than retention period."""

    log_dir = Path.home() / '.petesbrain-logs'
    now = datetime.now()

    for log_file in log_dir.glob('*.log'):
        # Parse date from filename: agent_YYYYMMDD.log
        file_date = datetime.strptime(log_file.stem.split('_')[-1], '%Y%m%d')
        age_days = (now - file_date).days

        # Check if file contains errors
        has_errors = 'ERROR' in log_file.read_text() or 'CRITICAL' in log_file.read_text()

        if has_errors and age_days > 90:
            logger.info(f"Deleting error log (90+ days old): {log_file}")
            log_file.unlink()
        elif not has_errors and age_days > 30:
            logger.info(f"Deleting log (30+ days old): {log_file}")
            log_file.unlink()
```

---

## Quick Reference

### Emoji Conventions

| Emoji | Meaning | When to Use |
|-------|---------|-------------|
| 🚀 | Start | Beginning of agent execution |
| ✅ | Success | Successful operation |
| ❌ | Failure | Failed operation |
| ⚠️ | Warning | Unexpected but not critical |
| 📊 | Data | Data collection/analysis |
| 📧 | Email | Email operations |
| 🔐 | Auth | Authentication/authorisation |
| ⚙️ | Processing | Data processing |
| 📤 | Output | Generating output |
| 🚨 | Alert | Critical alert triggered |
| 🐛 | Debug | Debugging information |

### Log Level Quick Reference

```python
logger.debug()    # Detailed diagnostic (only in DEBUG mode)
logger.info()     # Normal operation confirmation
logger.warning()  # Unexpected but handled situation
logger.error()    # Error occurred, operation failed
logger.critical() # Agent cannot continue
```

---

**Related Documentation:**
- `/docs/AGENT-MONITORING-GUIDE.md` - Agent health monitoring
- `/docs/SYSTEM-HEALTH-MONITORING.md` - System-wide monitoring
- `/infrastructure/hooks/google-ads-change-verification/` - Change verification logging

**Version History:**
- v1.0 (2025-12-14): Initial logging standards based on industry resources template patterns
