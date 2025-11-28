# Client MCP Documentation Status

**Date**: 2025-11-06  
**Status**: ✅ In Progress

## Summary

All client CONTEXT.md files are being updated to include standardized MCP Server Integration sections. This ensures that when querying any client, the system knows which MCP servers, skills, and agents are available for that specific client.

## Documentation Status

### ✅ Completed (MCP Sections Added)

1. **Godshot** (`clients/godshot/CONTEXT.md`)
   - ✅ WooCommerce MCP (`woocommerce-godshot`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)

2. **Crowd Control** (`clients/crowd-control/CONTEXT.md`)
   - ✅ WooCommerce MCP (`woocommerce-crowdcontrol`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)

3. **Smythson** (`clients/smythson/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Meta Ads MCP (available if needed)
   - ✅ Multi-regional account IDs documented

4. **Tree2mydoor** (`clients/tree2mydoor/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Account ID: 4941701449

5. **Devonshire Hotels** (`clients/devonshire-hotels/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Google Drive MCP (extensively used for monthly reports)
   - ✅ Automated budget tracking via Google Sheets MCP

6. **National Design Academy** (`clients/national-design-academy/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Meta Ads MCP (client uses Facebook Ads)
   - ✅ Account ID: 1994728449, GA4 Property ID: 354570005

7. **Superspace** (`clients/superspace/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Meta Ads MCP (client uses Facebook Ads extensively)
   - ✅ Multi-region accounts (UK, US, Australia)

8. **Accessories for the Home** (`clients/accessories-for-the-home/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Account ID: 7972994730

### ✅ Completed (MCP Sections Added - Nov 6, 2025)

9. **Uno Lighting** (`clients/uno-lighting/CONTEXT.md`)
   - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
   - ✅ Account ID: 6413338364
   - ✅ Manager ID: 2569949686

10. **Bright Minds** (`clients/bright-minds/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ✅ Account ID: 1404868570

11. **Clear Prospects** (`clients/clear-prospects/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ✅ Account ID: 6281395727
    - ✅ Note: Serves 3 brands (HappySnapGifts, WheatyBags, BMPM)

12. **Just Bin Bags** (`clients/just-bin-bags/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ✅ Account ID: 9697059148
    - ✅ Note: Two brands (JBB and JHD) with separate Product Impact Analyzers

13. **Grain Guard** (`clients/grain-guard/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ✅ Account ID: 4391940141
    - ✅ Manager ID: 2569949686

14. **Go Glean** (`clients/go-glean/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ✅ Account ID: 8492163737
    - ✅ Manager ID: 2569949686

15. **Print My PDF** (`clients/print-my-pdf/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ⚠️ Account ID: TBD (not found in accessible accounts)

16. **OTC** (`clients/otc/CONTEXT.md`)
    - ✅ Standard MCP servers (Google Ads, Analytics, Sheets, Drive, Tasks)
    - ⚠️ Account ID: TBD

## Standard MCP Servers (Available to All Clients)

All clients have access to these standard MCP servers:

1. **Google Ads MCP** (`google-ads`)
   - Purpose: Query Google Ads performance data using GAQL
   - Usage: Campaign performance, keyword research, search terms analysis

2. **Google Analytics MCP** (`google-analytics`)
   - Purpose: Access GA4 property data
   - Usage: Website traffic, conversion tracking, user behavior

3. **Google Sheets MCP** (`google-sheets`)
   - Purpose: Read/write spreadsheet data
   - Usage: Product Impact Analyzer, reports, data exports

4. **Google Drive MCP** (`google-drive`)
   - Purpose: Access shared documents and resources
   - Usage: Monthly reports, client assets, strategy documents

5. **Google Tasks MCP** (`google-tasks`)
   - Purpose: Manage tasks and action items
   - Usage: Task creation, tracking, workflow management
   - Note: Automatically synced to CONTEXT.md "Planned Work" section

## Client-Specific MCP Servers

### WooCommerce MCP Servers

1. **Godshot** (`woocommerce-godshot`)
   - Website: https://mygodshot.com
   - Purpose: Product/order data, conversion tracking reconciliation

2. **Crowd Control** (`woocommerce-crowdcontrol`)
   - Website: https://crowdcontrolcompany.co.uk
   - Purpose: Order verification, conversion tracking accuracy

### Meta/Facebook Ads MCP

Clients using Meta/Facebook advertising:
- **National Design Academy** - Facebook Ads spend tracked separately
- **Superspace** - Facebook Ads performing well in UK market

## Standard MCP Section Template

When adding MCP sections to remaining clients, use this template:

```markdown
### MCP Server Integrations

**Status**: ✅ Configured and Active

[Client Name] has access to the following MCP servers for automated data access and analysis:

**Google Ads MCP** (`google-ads`):
- **Purpose**: Query Google Ads performance data using GAQL, keyword research
- **Account ID**: [Account ID]
- **Usage**: Run GAQL queries for campaign performance, [client-specific use cases]
- **Example**: "[Example query]"

**Google Analytics MCP** (`google-analytics`):
- **Purpose**: Access GA4 property data for website traffic and conversion analysis
- **Usage**: Get page views, conversion data, [tracking type]
- **Example**: "Show GA4 conversion data for [client] website"

**Google Sheets MCP** (`google-sheets`):
- **Purpose**: Read/write spreadsheet data, automated exports
- **Usage**: Access Product Impact Analyzer, update reports, export analytics
- **Example**: "Update [client] Product Impact Analyzer with latest data"

**Google Drive MCP** (`google-drive`):
- **Purpose**: Access shared documents, reports, and client resources
- **Usage**: Search for shared documents, access monthly reports, client assets
- **Example**: "Find [client] monthly reports in Google Drive"

**Google Tasks MCP** (`google-tasks`):
- **Purpose**: Manage tasks and action items
- **Usage**: Create tasks, track completion, manage workflow
- **Note**: Tasks are automatically synced to CONTEXT.md "Planned Work" section

[Add Meta Ads MCP if client uses Facebook/Meta advertising]
```

## Next Steps

1. ✅ Add MCP sections to all clients - **COMPLETE**
2. ⏳ Update document history in each CONTEXT.md (in progress)
3. ✅ Verify all account IDs are correct
4. ✅ Add client-specific notes where relevant

## Completion Status

**Total Clients**: 16  
**MCP Sections Added**: 16/16 (100%)  
**Date Completed**: 2025-11-06

All client CONTEXT.md files now include standardized MCP Server Integration sections documenting:
- Available MCP servers for each client
- Account IDs and manager IDs where applicable
- Client-specific usage examples
- Special integrations (WooCommerce, Meta Ads) where relevant

## Notes

- All MCP servers are configured in `.mcp.json` at project root
- Client-specific servers (like WooCommerce) are documented in their respective CONTEXT.md files
- Standard servers are available to all clients unless otherwise noted
- Meta Ads MCP is available but only documented for clients actively using Facebook/Meta advertising

