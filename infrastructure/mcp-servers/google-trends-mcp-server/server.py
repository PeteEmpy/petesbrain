#!/usr/bin/env python3
"""
Google Trends MCP Server
Provides access to Google Trends data for PetesBrain

Functions:
- get_interest_over_time: Get search interest trends over time
- get_interest_by_region: Get search interest by geographic region
- get_related_queries: Get related search queries
- get_trending_searches: Get current trending searches
- compare_keywords: Compare multiple keywords
- get_suggestions: Get keyword suggestions
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import Tool, TextContent
from pytrends.request import TrendReq
import pandas as pd


class GoogleTrendsMCPServer:
    def __init__(self):
        self.app = Server("google-trends")
        self.pytrends = None
        self._setup_handlers()

    def _get_pytrends(self):
        """Get or create pytrends instance with retry logic"""
        if self.pytrends is None:
            # Add delays to avoid rate limiting
            self.pytrends = TrendReq(hl='en-GB', tz=0, timeout=(10, 25), retries=2, backoff_factor=0.5)
        return self.pytrends

    def _setup_handlers(self):
        """Setup MCP request handlers"""

        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_interest_over_time",
                    description="Get search interest trends over time for one or more keywords. Returns relative search volume (0-100) over specified time period.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords to track (max 5)",
                            },
                            "timeframe": {
                                "type": "string",
                                "default": "today 3-m",
                                "description": "Time range: 'today 3-m', 'today 12-m', 'today 5-y', 'all', or custom 'YYYY-MM-DD YYYY-MM-DD'",
                            },
                            "geo": {
                                "type": "string",
                                "default": "GB",
                                "description": "Country code (GB, US, etc.) or '' for worldwide",
                            },
                            "category": {
                                "type": "integer",
                                "default": 0,
                                "description": "Category ID (0=All categories)",
                            },
                        },
                        "required": ["keywords"],
                    },
                ),
                Tool(
                    name="get_interest_by_region",
                    description="Get search interest by geographic region. Shows where keywords are most popular.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords to analyze (max 5)",
                            },
                            "timeframe": {
                                "type": "string",
                                "default": "today 3-m",
                                "description": "Time range for analysis",
                            },
                            "resolution": {
                                "type": "string",
                                "default": "COUNTRY",
                                "description": "Geographic resolution: COUNTRY, REGION, CITY, DMA",
                            },
                            "geo": {
                                "type": "string",
                                "default": "GB",
                                "description": "Country code to drill down into regions",
                            },
                        },
                        "required": ["keywords"],
                    },
                ),
                Tool(
                    name="get_related_queries",
                    description="Get related search queries for a keyword. Shows 'rising' (fastest growing) and 'top' (most popular) related searches.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "Single keyword to analyze",
                            },
                            "timeframe": {
                                "type": "string",
                                "default": "today 3-m",
                                "description": "Time range for analysis",
                            },
                            "geo": {
                                "type": "string",
                                "default": "GB",
                                "description": "Country code",
                            },
                        },
                        "required": ["keyword"],
                    },
                ),
                Tool(
                    name="get_trending_searches",
                    description="Get current real-time trending searches for a country.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "geo": {
                                "type": "string",
                                "default": "united_kingdom",
                                "description": "Country name: united_states, united_kingdom, etc.",
                            },
                        },
                    },
                ),
                Tool(
                    name="compare_keywords",
                    description="Compare multiple keywords to identify which has highest search volume and growth. Returns comparison metrics and winner.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords to compare (2-5 keywords)",
                            },
                            "timeframe": {
                                "type": "string",
                                "default": "today 12-m",
                                "description": "Time range for comparison",
                            },
                            "geo": {
                                "type": "string",
                                "default": "GB",
                                "description": "Country code",
                            },
                        },
                        "required": ["keywords"],
                    },
                ),
                Tool(
                    name="get_suggestions",
                    description="Get keyword suggestions and autocomplete suggestions from Google Trends.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "Keyword to get suggestions for",
                            },
                        },
                        "required": ["keyword"],
                    },
                ),
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                if name == "get_interest_over_time":
                    result = await self._get_interest_over_time(**arguments)
                elif name == "get_interest_by_region":
                    result = await self._get_interest_by_region(**arguments)
                elif name == "get_related_queries":
                    result = await self._get_related_queries(**arguments)
                elif name == "get_trending_searches":
                    result = await self._get_trending_searches(**arguments)
                elif name == "compare_keywords":
                    result = await self._compare_keywords(**arguments)
                elif name == "get_suggestions":
                    result = await self._get_suggestions(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            except Exception as e:
                error_result = {"error": str(e), "tool": name}
                return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    async def _get_interest_over_time(
        self,
        keywords: List[str],
        timeframe: str = "today 3-m",
        geo: str = "GB",
        category: int = 0,
    ) -> Dict[str, Any]:
        """Get interest over time for keywords"""
        pytrends = self._get_pytrends()

        # Add delay to avoid rate limiting
        await asyncio.sleep(1)

        # Build payload
        pytrends.build_payload(
            keywords,
            cat=category,
            timeframe=timeframe,
            geo=geo,
            gprop=""
        )

        # Get data
        df = pytrends.interest_over_time()

        if df.empty:
            return {
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo,
                "message": "No data available for these keywords",
                "data": []
            }

        # Remove 'isPartial' column if present
        if 'isPartial' in df.columns:
            df = df.drop(columns=['isPartial'])

        # Convert to records
        data = []
        for date, row in df.iterrows():
            record = {"date": date.strftime("%Y-%m-%d")}
            for keyword in keywords:
                if keyword in row:
                    record[keyword] = int(row[keyword]) if not pd.isna(row[keyword]) else 0
            data.append(record)

        # Calculate summary statistics
        summary = {}
        for keyword in keywords:
            if keyword in df.columns:
                values = df[keyword].dropna()
                summary[keyword] = {
                    "average": float(values.mean()),
                    "max": int(values.max()),
                    "min": int(values.min()),
                    "current": int(values.iloc[-1]) if len(values) > 0 else 0,
                    "trend": "rising" if len(values) > 1 and values.iloc[-1] > values.iloc[0] else "falling"
                }

        return {
            "keywords": keywords,
            "timeframe": timeframe,
            "geo": geo,
            "summary": summary,
            "data": data
        }

    async def _get_interest_by_region(
        self,
        keywords: List[str],
        timeframe: str = "today 3-m",
        resolution: str = "COUNTRY",
        geo: str = "GB",
    ) -> Dict[str, Any]:
        """Get interest by region"""
        pytrends = self._get_pytrends()

        # Build payload
        pytrends.build_payload(
            keywords,
            timeframe=timeframe,
            geo=geo if resolution != "COUNTRY" else "",
        )

        # Get data
        df = pytrends.interest_by_region(resolution=resolution, inc_low_vol=True, inc_geo_code=True)

        if df.empty:
            return {
                "keywords": keywords,
                "message": "No regional data available",
                "data": []
            }

        # Convert to records
        data = []
        for region, row in df.iterrows():
            record = {"region": region}
            for keyword in keywords:
                if keyword in row:
                    record[keyword] = int(row[keyword]) if not pd.isna(row[keyword]) else 0
            data.append(record)

        # Sort by first keyword
        if keywords:
            data = sorted(data, key=lambda x: x.get(keywords[0], 0), reverse=True)

        return {
            "keywords": keywords,
            "timeframe": timeframe,
            "resolution": resolution,
            "geo": geo,
            "data": data[:50]  # Limit to top 50 regions
        }

    async def _get_related_queries(
        self,
        keyword: str,
        timeframe: str = "today 3-m",
        geo: str = "GB",
    ) -> Dict[str, Any]:
        """Get related queries"""
        pytrends = self._get_pytrends()

        # Build payload
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)

        # Get related queries
        related = pytrends.related_queries()

        if keyword not in related or related[keyword]['top'] is None:
            return {
                "keyword": keyword,
                "message": "No related queries available",
                "top": [],
                "rising": []
            }

        result = {
            "keyword": keyword,
            "timeframe": timeframe,
            "geo": geo,
            "top": [],
            "rising": []
        }

        # Top queries
        if related[keyword]['top'] is not None:
            top_df = related[keyword]['top']
            result['top'] = [
                {"query": row['query'], "value": int(row['value'])}
                for _, row in top_df.head(25).iterrows()
            ]

        # Rising queries
        if related[keyword]['rising'] is not None:
            rising_df = related[keyword]['rising']
            result['rising'] = [
                {
                    "query": row['query'],
                    "value": str(row['value']) if pd.isna(row['value']) or row['value'] == float('inf') else int(row['value'])
                }
                for _, row in rising_df.head(25).iterrows()
            ]

        return result

    async def _get_trending_searches(self, geo: str = "united_kingdom") -> Dict[str, Any]:
        """Get trending searches"""
        pytrends = self._get_pytrends()

        try:
            df = pytrends.trending_searches(pn=geo)

            if df.empty:
                return {
                    "geo": geo,
                    "message": "No trending searches available",
                    "trends": []
                }

            return {
                "geo": geo,
                "timestamp": datetime.now().isoformat(),
                "trends": df[0].tolist()[:20]  # Top 20 trends
            }
        except Exception as e:
            return {
                "geo": geo,
                "error": f"Could not fetch trending searches: {str(e)}",
                "trends": []
            }

    async def _compare_keywords(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "GB",
    ) -> Dict[str, Any]:
        """Compare keywords"""
        # Get interest over time first
        interest_data = await self._get_interest_over_time(keywords, timeframe, geo)

        if "summary" not in interest_data:
            return {
                "keywords": keywords,
                "message": "No comparison data available",
                "comparison": []
            }

        # Build comparison
        comparison = []
        for keyword in keywords:
            if keyword in interest_data["summary"]:
                stats = interest_data["summary"][keyword]
                comparison.append({
                    "keyword": keyword,
                    "average": stats["average"],
                    "max": stats["max"],
                    "current": stats["current"],
                    "trend": stats["trend"]
                })

        # Sort by average
        comparison = sorted(comparison, key=lambda x: x["average"], reverse=True)

        # Determine winner
        winner = comparison[0] if comparison else None

        return {
            "keywords": keywords,
            "timeframe": timeframe,
            "geo": geo,
            "winner": winner,
            "comparison": comparison
        }

    async def _get_suggestions(self, keyword: str) -> Dict[str, Any]:
        """Get keyword suggestions"""
        pytrends = self._get_pytrends()

        try:
            suggestions = pytrends.suggestions(keyword=keyword)

            return {
                "keyword": keyword,
                "suggestions": [
                    {
                        "title": s['title'],
                        "type": s['type']
                    }
                    for s in suggestions
                ]
            }
        except Exception as e:
            return {
                "keyword": keyword,
                "error": f"Could not fetch suggestions: {str(e)}",
                "suggestions": []
            }

    async def run(self):
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )


def main():
    """Main entry point"""
    server = GoogleTrendsMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
