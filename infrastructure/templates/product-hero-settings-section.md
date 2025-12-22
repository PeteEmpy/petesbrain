# Product Hero Settings Section - Template for Client CONTEXT.md

**Location in CONTEXT.md**: Add after "Campaign Analysis & Context" section, before "Action Items & Reminders"

**Purpose**: Track Product Hero platform configuration changes for clients using the Labelizer system.

---

## Template

```markdown
## Product Hero Settings

### Current Configuration (Last Updated: YYYY-MM-DD)

**Target ROAS**: [current%]
**Previous**: [previous%] (changed YYYY-MM-DD)
**Actual ROAS Achieved**: [actual%]
**Click Impact**: [before] → [after] (monitoring for volume increase/decrease)

**Rationale**: [Why this change was made - e.g., "Actual ROAS (X%) significantly exceeded target (Y%), indicating room to reduce target to unlock more volume while maintaining strong profitability."]

**Related Methodology**: [Product Hero Labelizer System](/Users/administrator/Documents/PetesBrain.nosync/roksys/knowledge-base/rok-methodologies/product-hero-labelizer-system.md)

### Settings Change History

| Date | Setting | Previous | New | Rationale | Result |
|------|---------|----------|-----|-----------|--------|
| YYYY-MM-DD | Target ROAS | X% | Y% | [Brief reason] | [Monitoring / Result observed] |

**Note**: Product Hero automatically classifies products daily as Heroes/Sidekicks/Villains/Zombies based on performance. These labels sync to Google Merchant Center and guide campaign structure. Target ROAS settings control the algorithm's bidding aggressiveness.
```

---

## Usage Instructions

### When to Add This Section

Add to client CONTEXT.md if:
- Client uses Product Hero Labelizer system
- Campaigns structured around Heroes/Sidekicks/Villains/Zombies labels
- Product Hero platform settings are actively managed

### When to Update

**Add new row to table when**:
- Target ROAS changed in Product Hero platform
- Other Product Hero settings modified (filters, thresholds, etc.)
- Label distribution strategy changes

**Update "Current Configuration" when**:
- Most recent setting change occurs
- Reviewing monthly performance (update actual ROAS achieved)

### Fields Explained

**Target ROAS**: The ROAS target configured in Product Hero platform
**Previous**: Previous target (for context on magnitude of change)
**Actual ROAS Achieved**: What the campaign/products actually delivered (justifies the setting change)
**Click Impact**: Before/after click volume (immediate observable impact)
**Rationale**: Strategic reasoning for the change
**Result**: Monitoring status or observed outcome after sufficient time

---

## Cross-Client Rollout

When rolling out to multiple clients:

1. **Identify Product Hero clients** - grep for "Product Hero", "Heroes & Sidekicks", "H&S", custom_label_0 references
2. **Check current campaign structure** - verify they're actually using Labelizer (not just have access)
3. **Add template section** - customize with client-specific current settings
4. **Backfill if possible** - if recent setting changes are documented in emails/notes, add to history table
5. **Document in CONTEXT.md history** - note when section was added

---

## Related Documentation

- [Product Hero Labelizer System](/Users/administrator/Documents/PetesBrain.nosync/roksys/knowledge-base/rok-methodologies/product-hero-labelizer-system.md) - Full methodology
- Client CONTEXT.md files - Individual client implementations
- Product Hero platform: https://www.producthero.com/labelizer

---

**Created**: 2025-12-15
**Template Version**: 1.0
