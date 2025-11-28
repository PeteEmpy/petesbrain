# Future Development Documentation Instructions

## Overview

This skill documents incomplete work, half-finished agents, partial implementations, or blocked features into the future developments section (`docs/future-enhancements.md`) so they can be picked up later.

## When to Document

Document work as future development when:
- ✅ **Partial Implementation**: Core structure built but incomplete
- ✅ **Blocked**: Waiting on dependencies, API access, or decisions
- ✅ **Deferred**: Lower priority, can be finished later
- ✅ **Experimental**: Proof of concept but needs refinement
- ✅ **Needs Setup**: Requires configuration or external setup

## Documentation Process

### Step 1: Analyze the Work

Examine the incomplete work to identify:
- **What's Built**: Files created, functionality implemented
- **What's Missing**: Remaining work, incomplete features
- **Current Status**: Working vs. broken vs. untested
- **Dependencies**: What's needed to complete
- **Blockers**: Why it's not finished

### Step 2: Determine Priority

Use these guidelines:

**High Priority**:
- Solves current pain points
- High value when complete
- Blocking other work
- User-requested feature

**Medium Priority**:
- Useful improvement
- Enhances existing workflows
- Moderate value
- Nice to have

**Low Priority**:
- Convenience feature
- Low impact
- Experimental
- Can wait

### Step 3: Extract Information

Gather:
- **Files Created**: List all relevant files
- **Documentation**: Existing docs about the work
- **Dependencies**: APIs, services, setup needed
- **Related Systems**: Other features this connects to
- **Test Results**: What's been tested, what works

### Step 4: Format Entry

Follow the future-enhancements.md format:

```markdown
### [Feature/Agent Name]
**Status**: Partial Implementation | Blocked | Documented | In Progress
**Effort**: Low | Medium | High
**Value**: Low | Medium | High

[Description of what it does and why it's useful]

**What's Built**:
- ✅ [Completed item 1]
- ✅ [Completed item 2]
- ⚠️ [Partially working item]

**Current Limitations**:
- ⚠️ [What doesn't work]
- ⚠️ [What's missing]
- ⚠️ [Known issues]

**Future Development Tasks**:

**Phase 1: [Phase Name]**
- [ ] Task 1
- [ ] Task 2

**Phase 2: [Phase Name]**
- [ ] Task 1
- [ ] Task 2

**Benefits**:
- Benefit 1
- Benefit 2

**Implementation Requirements**: (optional)
- Requirement 1
- Requirement 2

**Decision Points Needed**: (optional)
1. Decision point 1
2. Decision point 2

**References**:
- `path/to/file.py` - Main implementation
- `docs/DOCUMENTATION.md` - Related docs
```

## Status Values

### Partial Implementation
- Core structure exists
- Some functionality works
- Needs completion or refinement
- Example: "WhatsApp processing - email-based works, Business API needs setup"

### Blocked
- Waiting on external dependency
- Requires API access or credentials
- Needs decision or approval
- Example: "Requires Meta Developer Account setup"

### Documented
- Idea fully documented
- Not yet implemented
- Ready to start
- Example: "Feature spec complete, implementation pending"

### In Progress
- Actively being worked on
- Recent commits or updates
- Should be completed soon
- Example: "Currently implementing Phase 2"

## Priority Guidelines

### High Priority Criteria
- Solves immediate problem
- High user value
- Enables other features
- User explicitly requested
- Blocking current workflows

### Medium Priority Criteria
- Useful enhancement
- Improves existing system
- Moderate value
- Can wait but would be nice
- Complements other features

### Low Priority Criteria
- Convenience feature
- Low impact
- Experimental
- Can wait indefinitely
- Nice to have

## Entry Structure

### Required Sections
1. **Status** - Current state
2. **Effort** - Estimated complexity
3. **Value** - Expected benefit
4. **Description** - What it does
5. **What's Built** - Completed items
6. **Current Limitations** - What's missing/broken
7. **Future Development Tasks** - What needs doing

### Optional Sections
- **Benefits** - Why complete it
- **Implementation Requirements** - What's needed
- **Decision Points** - Choices to make
- **Approach** - How to implement
- **References** - Related files/docs

## File Organization

### Main Entry
Add to `docs/future-enhancements.md` in appropriate priority section:
- High Priority
- Medium Priority
- Low Priority / Nice to Have

### Detailed Documentation
If complex, create detailed doc in `docs/FUTURE-DEVELOPMENT/`:
- `docs/FUTURE-DEVELOPMENT/[FEATURE-NAME].md`
- Link from main entry
- Include full technical details

## Linking Strategy

### Code References
- Use relative paths: `agents/system/feature.py`
- Link to specific files, not directories
- Include line numbers if referencing specific code

### Documentation References
- Link to relevant docs: `docs/FEATURE-GUIDE.md`
- Reference setup guides if applicable
- Link to related future development items

### Related Systems
- Mention related features
- Link to similar implementations
- Reference dependencies

## Best Practices

1. **Be Specific**: Clear about what's done vs. needed
2. **Include Context**: Why it's incomplete
3. **List Dependencies**: What's blocking completion
4. **Provide Examples**: Show what works/doesn't work
5. **Link Everything**: Connect to code, docs, related work
6. **Set Priority**: Help prioritize future work
7. **Identify Blockers**: What needs to happen first

## Common Patterns

### Pattern 1: Partial Implementation
```
**What's Built**: Core structure, basic functionality
**Current Limitations**: Missing advanced features, needs testing
**Future Development**: Complete features, add tests, refine
```

### Pattern 2: Blocked Work
```
**What's Built**: Code structure ready
**Current Limitations**: Waiting on API access, credentials, or decision
**Future Development**: Complete setup, then finish implementation
```

### Pattern 3: Deferred Feature
```
**What's Built**: Proof of concept or prototype
**Current Limitations**: Needs refinement, not priority
**Future Development**: Polish, integrate, productionize
```

## Update Existing Entries

When updating existing future development entries:
- Add new "What's Built" items as work progresses
- Update status if it changes
- Add new phases or tasks as needed
- Move to "Completed" section when done
- Update "Last Updated" date

## Completion

When work is completed:
1. Move entry to "Completed Enhancements" section
2. Add completion date
3. Note what was delivered
4. Remove from future development if fully done
5. Or update status to "Complete" if keeping for reference

