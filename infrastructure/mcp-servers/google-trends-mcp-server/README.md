# Google Trends MCP Server

MCP server providing access to Google Trends data for PetesBrain.

## Features

### Core Functions

1. **get_interest_over_time**
   - Track search interest trends over time
   - Compare up to 5 keywords
   - Customizable timeframes (3 months, 1 year, 5 years, all time)
   - Returns time-series data with summary statistics

2. **get_interest_by_region**
   - Identify where keywords are most popular
   - Country, region, city, or DMA resolution
   - Top 50 locations by search volume

3. **get_related_queries**
   - Discover "top" (most popular) related searches
   - Find "rising" (fastest growing) related searches
   - Up to 25 queries in each category

4. **get_trending_searches**
   - Real-time trending searches by country
   - Top 20 current trends

5. **compare_keywords**
   - Side-by-side keyword comparison
   - Identifies winner by average search volume
   - Trend direction (rising/falling)

6. **get_suggestions**
   - Keyword suggestions and autocomplete
   - Category and type information

## Installation

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-trends": {
      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/.venv/bin/python",
      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/server.py"]
    }
  }
}
```

## Usage Examples

### Track Product Interest Over Time

```python
# Via MCP
mcp__google_trends__get_interest_over_time(
    keywords=["luxury notebooks", "leather diaries", "stationery gifts"],
    timeframe="today 12-m",
    geo="GB"
)
```

Returns:
```json
{
  "keywords": ["luxury notebooks", "leather diaries", "stationery gifts"],
  "summary": {
    "luxury notebooks": {
      "average": 45.2,
      "max": 78,
      "min": 12,
      "current": 56,
      "trend": "rising"
    }
  },
  "data": [
    {"date": "2024-11-06", "luxury notebooks": 56, "leather diaries": 34}
  ]
}
```

### Identify Geographic Opportunities

```python
mcp__google_trends__get_interest_by_region(
    keywords=["christmas trees"],
    timeframe="today 3-m",
    resolution="REGION",
    geo="GB"
)
```

### Discover Related Keywords

```python
mcp__google_trends__get_related_queries(
    keyword="sustainable clothing",
    timeframe="today 3-m",
    geo="GB"
)
```

### Compare Product Categories

```python
mcp__google_trends__compare_keywords(
    keywords=["notebooks", "planners", "journals", "diaries"],
    timeframe="today 12-m",
    geo="GB"
)
```

## Timeframe Options

- `today 3-m` - Last 3 months
- `today 12-m` - Last 12 months (default for comparisons)
- `today 5-y` - Last 5 years
- `all` - All available data (2004-present)
- `YYYY-MM-DD YYYY-MM-DD` - Custom date range

## Geographic Codes

- `GB` - United Kingdom
- `US` - United States
- `""` - Worldwide
- Any ISO 2-letter country code

## Limitations

- Maximum 5 keywords per request (Google Trends API limit)
- Rate limiting applies (handled automatically by pytrends)
- Data is relative (0-100 scale), not absolute search volumes
- Real-time data may have slight delays

## Use Cases for PetesBrain

### 1. Seasonal Planning
```python
# Identify Q4 peak for "Christmas trees"
get_interest_over_time(
    keywords=["christmas trees"],
    timeframe="today 5-y",
    geo="GB"
)
```

### 2. Keyword Research
```python
# Find rising related queries for campaign expansion
get_related_queries(
    keyword="sustainable fashion",
    timeframe="today 12-m"
)
```

### 3. Geographic Targeting
```python
# Identify top UK regions for "luxury hotels"
get_interest_by_region(
    keywords=["luxury hotels"],
    resolution="REGION",
    geo="GB"
)
```

### 4. Product Prioritization
```python
# Compare product categories to inform budget allocation
compare_keywords(
    keywords=["stationery", "notebooks", "pens", "paper"],
    timeframe="today 12-m"
)
```

### 5. Performance Context
```python
# Check if declining performance matches declining interest
get_interest_over_time(
    keywords=["client-product-name"],
    timeframe="today 3-m"
)
```

## Integration with Agents

### Automated Trend Monitoring Agent
Create `agents/performance-monitoring/trend-monitor.py` to:
- Track keyword trends for all clients weekly
- Alert on significant trend changes (>20% movement)
- Correlate trends with campaign performance
- Add insights to client CONTEXT.md

### Budget Allocation Agent
Use trends data to:
- Suggest budget increases for rising trends
- Flag budget cuts for declining interest
- Identify seasonal patterns for pacing adjustments

## Data Structure

All functions return structured JSON with:
- **keywords**: List of queried keywords
- **timeframe**: Time period analyzed
- **geo**: Geographic scope
- **data**: Detailed results array
- **summary**: Aggregate statistics (where applicable)

## Error Handling

The server handles:
- Rate limiting (automatic backoff)
- No data available scenarios
- Invalid parameters
- Network issues

All errors return structured responses:
```json
{
  "error": "Description of error",
  "tool": "function_name"
}
```

## Dependencies

- **pytrends** (4.9.2): Unofficial Google Trends API wrapper
- **mcp** (1.1.0): Model Context Protocol server
- **pandas** (2.2.0): Data manipulation

## Maintenance

No authentication required - Google Trends is a public API.

Check for pytrends updates quarterly:
```bash
source .venv/bin/activate
pip install --upgrade pytrends
```

## Support

Part of PetesBrain MCP servers ecosystem.
See: `shared/mcp-servers/README.md`
