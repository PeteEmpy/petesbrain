# PMAX Asset Optimizer - Automation Agents

**Purpose**: Automated workflow for Performance Max asset optimization

**Status**: Planning/Design phase (not yet implemented)

**Created**: 2025-11-27

---

## Overview

This directory contains agent configurations for automating the PMAX Asset Optimizer workflow. The system consists of 4 specialized agents that work together to identify, generate, review, and execute asset optimizations.

---

## Agent Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    PMAX Asset Optimizer                    │
│                    Automation Framework                    │
└────────────────────────────────────────────────────────────┘

Agent 1: Asset Performance Analyzer
     │
     │ Identifies underperformers
     ▼
Agent 2: Replacement Generator
     │
     │ Creates AI suggestions
     ▼
Agent 3: Review Sheet Manager
     │
     │ Manages selection workflow
     ▼
Agent 4: Execution Engine
     │
     │ Executes approved swaps
     ▼
  Results & Verification
```

---

## Agents

### 1. Asset Performance Analyzer

**File**: `1-asset-performance-analyzer.md`

**Purpose**: Automated data extraction and underperformer identification

**Triggers**:
- Weekly schedule (every Monday 9 AM)
- Manual: `/analyze-assets tree2mydoor`
- Event: High spend without conversions

**Responsibilities**:
- Extract asset performance from Google Ads API
- Calculate averages (CTR, conv rate, cost/conv)
- Flag underperforming assets
- Generate analysis report
- Create task if action needed

**Outputs**:
- `asset-performance-{customer_id}-{date}.csv`
- `underperforming-assets.csv`
- Analysis report
- Task notification

---

### 2. Replacement Generator

**File**: `2-replacement-generator.md`

**Purpose**: AI-powered suggestion generation with deduplication

**Triggers**:
- After Asset Performance Analyzer finds issues
- Manual: `/generate-replacements tree2mydoor`
- Scheduled: Bi-weekly

**Responsibilities**:
- Load underperforming assets
- Extract URL context (landing pages)
- Generate deduplicated suggestions via Claude API
- Validate character limits
- Create review sheet
- Upload to Google Sheets

**Outputs**:
- `replacement-candidates.csv`
- `tree2mydoor-review-sheet.csv`
- Google Sheets upload confirmation

---

### 3. Review Sheet Manager

**File**: `3-review-sheet-manager.md`

**Purpose**: Manages human-in-loop selection workflow

**Triggers**:
- After suggestions generated
- Daily check for new selections
- Manual: `/check-selections tree2mydoor`

**Responsibilities**:
- Monitor Google Sheets for selections
- Download selections when ready
- Convert to execution format
- Validate selections
- Notify user for approval

**Outputs**:
- `tree2mydoor-reviewed-selections.csv`
- `execution-ready.csv`
- Approval request notification

---

### 4. Execution Engine

**File**: `4-execution-engine.md`

**Purpose**: Safe asset swap execution (always requires approval)

**Triggers**:
- Manual ONLY: `/execute-swaps tree2mydoor --dry-run`
- After user approval: `/execute-swaps tree2mydoor --live`
- NEVER automatic

**Responsibilities**:
- Run dry-run simulation
- Generate preview report
- Request explicit approval
- Execute live swaps (if approved)
- Verify changes
- Generate execution report

**Outputs**:
- `execution-report-dry-run-{timestamp}.json`
- `execution-report-live-{timestamp}.json`
- Verification report

---

## Agent Communication

### Data Flow

```
Asset Performance Analyzer
    ↓ (asset-performance.csv)
Replacement Generator
    ↓ (replacement-candidates.csv)
Google Sheets (Human Review)
    ↓ (user selections)
Review Sheet Manager
    ↓ (execution-ready.csv)
Execution Engine
    ↓ (execution reports)
Verification & Notification
```

### State Tracking

**Location**: `data/state/pmax-asset-optimizer-state.json`

```json
{
  "tree2mydoor": {
    "last_analysis": "2025-11-27",
    "underperformers_count": 154,
    "suggestions_generated": "2025-11-27",
    "review_status": "pending_selection",
    "last_execution": "2025-11-26",
    "next_scheduled_analysis": "2025-12-02"
  }
}
```

### Notification System

Agents send notifications via:
- Slack (preferred for team visibility)
- Email (for critical approvals)
- Task system (for action required)

---

## Implementation Plan

### Phase 1: Core Agents (Week 1)

- [ ] Agent 1: Asset Performance Analyzer
  - [ ] Google Ads API integration
  - [ ] Analysis logic
  - [ ] Report generation
  - [ ] Task creation

- [ ] Agent 2: Replacement Generator
  - [ ] Claude API integration
  - [ ] URL context extraction
  - [ ] Deduplication logic
  - [ ] Google Sheets upload

### Phase 2: Workflow Management (Week 2)

- [ ] Agent 3: Review Sheet Manager
  - [ ] Google Sheets monitoring
  - [ ] Selection detection
  - [ ] Format conversion
  - [ ] Approval notifications

- [ ] Agent 4: Execution Engine
  - [ ] Dry-run automation
  - [ ] Approval workflow
  - [ ] Live execution
  - [ ] Verification checks

### Phase 3: Integration & Testing (Week 3)

- [ ] End-to-end testing
- [ ] Error handling
- [ ] Rollback procedures
- [ ] Monitoring dashboards
- [ ] Documentation finalization

### Phase 4: Production Deployment (Week 4)

- [ ] Production credentials
- [ ] Monitoring setup
- [ ] Alert configuration
- [ ] Team training
- [ ] Go-live

---

## Configuration

### Environment Variables

```bash
# Google Ads API
GOOGLE_ADS_DEVELOPER_TOKEN=xxxxx
GOOGLE_ADS_CLIENT_ID=xxxxx
GOOGLE_ADS_CLIENT_SECRET=xxxxx
GOOGLE_ADS_REFRESH_TOKEN=xxxxx

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Google Sheets API
GOOGLE_SHEETS_CREDENTIALS_PATH=/path/to/credentials.json

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/xxxxx
NOTIFICATION_EMAIL=peter@roksys.co.uk
```

### Agent Schedules

```yaml
schedules:
  asset_performance_analyzer:
    cron: "0 9 * * 1"  # Every Monday 9 AM
    timezone: "Europe/London"

  replacement_generator:
    cron: "0 10 * * 2,4"  # Tuesday & Thursday 10 AM
    timezone: "Europe/London"

  review_sheet_manager:
    cron: "0 */4 * * *"  # Every 4 hours
    timezone: "Europe/London"

  # Execution Engine: Manual only (no schedule)
```

---

## Safety & Governance

### Human-in-Loop Requirements

**Mandatory approval for**:
- Generation of suggestions (review quality)
- Selection of assets (choose which to swap)
- Live execution (final approval before changes)

**Automatic actions**:
- Data extraction (safe, read-only)
- Analysis (no changes made)
- Dry-run execution (simulation only)

### Rollback Procedures

**If execution goes wrong**:

1. **Immediate**: Pause all agents
   ```bash
   /pause-agent execution-engine
   ```

2. **Assess**: Check execution report
   ```bash
   cat logs/execution-report-live-{timestamp}.json
   ```

3. **Revert**: Use revert script or manual Google Ads UI changes

4. **Document**: Create investigation report

5. **Fix**: Update code/logic

6. **Resume**: Test with dry-run first

### Audit Trail

All agent actions logged to:
- `logs/agent-actions-{date}.log`
- State file: `data/state/pmax-asset-optimizer-state.json`
- Execution reports: `logs/execution-report-*.json`

Retention: 90 days minimum

---

## Monitoring

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Analysis completion time | < 5 min | > 10 min |
| Generation completion time | < 10 min | > 15 min |
| Suggestion quality (user acceptance) | > 70% | < 50% |
| Execution success rate | > 95% | < 90% |
| API error rate | < 1% | > 5% |

### Dashboards

**Proposed tools**:
- Grafana (metrics visualization)
- Google Sheets (agent status dashboard)
- Slack (real-time notifications)

**Key views**:
- Agent health status
- Pipeline progress
- Success/failure rates
- API usage & costs
- User engagement (selections made)

---

## Cost Estimation

### API Costs

**Claude API** (Sonnet 4):
- ~154 assets × 3 suggestions = 462 API calls per run
- ~$0.003 per call (estimated)
- ~$1.39 per full generation
- Bi-weekly: ~$2.78/week, ~$12/month

**Google Ads API**:
- Free (within quota limits)
- 10,000 operations/day free

**Google Sheets API**:
- Free (within quota limits)

**Total estimated cost**: ~$15-20/month for one client

**Scaling**: Add ~$15/month per additional client

---

## Next Steps

### To Implement

1. **Create individual agent files** (1-4) with detailed specs
2. **Set up agent framework** (LaunchAgent or cron)
3. **Implement Agent 1** (Asset Performance Analyzer) first
4. **Test end-to-end** with Tree2mydoor
5. **Iterate based on results**
6. **Scale to other clients**

### Questions to Answer

- [ ] Which agent framework to use? (LaunchAgent vs cron vs custom)
- [ ] Where to host? (Local Mac vs server)
- [ ] Notification preferences? (Slack vs email vs Tasks)
- [ ] Approval workflow? (Slack buttons vs CLI vs UI)
- [ ] Monitoring setup? (Grafana vs simple logs)

---

## Resources

**Related documentation**:
- `../../tools/pmax-asset-optimiser/WORKFLOW.md` - Complete manual workflow
- `../../tools/pmax-asset-optimiser/logs/investigation-report-*.md` - Problem analysis
- `../../tools/pmax-asset-optimiser/logs/resolution-summary-*.md` - Fix summaries

**External links**:
- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

**Status**: Planning phase
**Next Review**: 2025-12-01
**Owner**: Peter Empson / PetesBrain
