# Batch 3 Migration Plan

**Status**: Ready for execution
**Agents in Batch**: 20
**Type**: Non-critical monitoring and background tasks
**Estimated Time**: 20-25 minutes

## Agents for Batch 3

1. agent-loader - Agent management utility
2. ai-google-chat-processor - Chat message processing
3. ai-news - News aggregation
4. baseline-calculator - Metrics calculation
5. booking-processor - Booking management
6. business-context-sync - Context synchronization
7. cleanup-completed-tasks - Task cleanup
8. critical-tasks-backup - Task backup
9. daily-anomaly-alerts - Alert detection
10. daily-backup - Daily system backup
11. devonshire-budget - Client-specific budget (Devonshire Hotels)
12. diagnostics-monitor - System diagnostics
13. document-archival - Document archiving
14. draft-cleanup - Draft email cleanup
15. email-auto-label - Email labeling
16. experiment-review - A/B test tracking
17. facebook-news-monitor - Facebook monitoring
18. facebook-specs-processor - Feed processor
19. fetch-client-performance - Performance data retrieval
20. file-organizer - File organization

## What Will Happen

For each agent:
1. **Plist Update**: Add `PETESBRAIN_ROOT` environment variable
2. **Agent Reload**: `launchctl unload` → `launchctl load`
3. **Health Check**: Verify exit code 0 via `launchctl list`

## Execution Command

```bash
python3 scripts/migrate-batch.py \
  agent-loader ai-google-chat-processor ai-news baseline-calculator \
  booking-processor business-context-sync cleanup-completed-tasks critical-tasks-backup \
  daily-anomaly-alerts daily-backup devonshire-budget diagnostics-monitor \
  document-archival draft-cleanup email-auto-label experiment-review \
  facebook-news-monitor facebook-specs-processor fetch-client-performance file-organizer
```

## After Migration

- Verify all agents healthy: `launchctl list | grep petesbrain | grep "^- 0" | wc -l`
- Expected: ~90 healthy agents (70 from before + 20 from Batch 3)
- Next: Batch 4 (remaining 36 agents)

