#!/usr/bin/env python3
"""
Client Content AI Search

AI-powered semantic search across all client content including CONTEXT.md,
meetings, emails, documents, reports, tasks-completed.md, and Roksys content.

Uses the same pattern as kb-search.py but for client folders.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Optional import for AI features
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_FILE = PROJECT_ROOT / "shared" / "data" / "client-index.json"


def load_index() -> Dict[str, Any]:
    """Load the client content index"""
    if not INDEX_FILE.exists():
        print("❌ Client content index not found!")
        print(f"   Run: python3 agents/client-indexer/client-indexer.py")
        sys.exit(1)
    
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)


def keyword_search(
    query: str, 
    index: Dict[str, Any], 
    client: str = None,
    content_type: str = None,
    date_from: str = None,
    date_to: str = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """Advanced keyword search with filtering"""
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    results = []
    
    for file_data in index["files"]:
        # Apply filters first
        if client and client.lower() not in file_data["client"].lower():
            continue
        
        if content_type and content_type.lower() not in file_data["content_type"].lower():
            continue
        
        if date_from or date_to:
            file_date = file_data.get("date")
            if file_date:
                if date_from and file_date < date_from:
                    continue
                if date_to and file_date > date_to:
                    continue
        
        # Calculate search score
        score = 0
        
        # Search in title (highest weight)
        title_lower = file_data["title"].lower()
        for term in query_terms:
            if term in title_lower:
                score += 10
        
        # Search in preview/content
        preview_lower = file_data.get("content_preview", "").lower()
        for term in query_terms:
            if term in preview_lower:
                score += 1
        
        # Search in client name (medium weight)
        client_lower = file_data["client"].lower()
        for term in query_terms:
            if term in client_lower:
                score += 5
        
        # Search in content type
        content_type_lower = file_data["content_type"].lower()
        for term in query_terms:
            if term in content_type_lower:
                score += 3
        
        # Search in path
        path_lower = file_data["path"].lower()
        for term in query_terms:
            if term in path_lower:
                score += 2
        
        if score > 0:
            results.append({
                **file_data,
                "score": score
            })
    
    # Sort by score (descending), then by date (most recent first)
    results.sort(key=lambda x: (
        x["score"],
        x.get("date") or "1970-01-01"
    ), reverse=True)
    
    return results[:limit]


def read_file_content(file_path: str) -> str:
    """Read full content of a file"""
    full_path = PROJECT_ROOT / file_path
    try:
        if full_path.suffix == '.html':
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Basic HTML stripping for readability
            import re
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content)
            return content
        else:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"


def ai_search(query: str, keyword_results: List[Dict[str, Any]], detailed: bool = False) -> str:
    """Use Claude to analyze and summarize relevant client content"""
    
    # Check if anthropic is available
    if not ANTHROPIC_AVAILABLE:
        return "❌ Anthropic library not installed. Install with: pip install anthropic"
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return "❌ ANTHROPIC_API_KEY not set. Set it to use AI search."
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build context from top results
    context_parts = []
    
    if detailed:
        # Read full content of top 3 results
        for result in keyword_results[:3]:
            content = read_file_content(result["path"])
            context_parts.append(f"""
### {result['title']}
**Client:** {result['client']}
**Type:** {result['content_type']}
**Date:** {result.get('date', 'N/A')}
**File:** {result['path']}

{content[:3000]}  # First 3000 chars
""")
    else:
        # Use previews for all results
        for result in keyword_results[:10]:
            context_parts.append(f"""
- **{result['title']}** ({result['client']} - {result['content_type']})
  Date: {result.get('date', 'N/A')}
  {result.get('preview', result.get('content_preview', '')[:200])}
""")
    
    context = "\n".join(context_parts)
    
    prompt = f"""You are searching Pete's Brain client content to answer a question about client work, 
meetings, strategies, or past activities.

QUERY: {query}

RELEVANT CLIENT CONTENT:
{context}

Please provide a helpful answer to the query based on the client content above. 

Format your response as:
1. Direct answer to the query
2. Key points from the client content
3. Which specific files to read for more details
4. Recommendations or next steps (if applicable)

Be concise but informative. If the content doesn't contain relevant information, say so.
Focus on actionable insights."""

    print("🤖 Analyzing with Claude...")
    print()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    return message.content[0].text


def print_results(results: List[Dict[str, Any]], show_preview: bool = True):
    """Print search results"""
    print(f"📚 Found {len(results)} relevant file(s)")
    print()
    
    for i, result in enumerate(results[:15], 1):
        print(f"{i}. {result['title']}")
        print(f"   👤 {result['client']}")
        print(f"   📁 {result['content_type']}")
        if result.get('date'):
            print(f"   📅 {result['date']}")
        print(f"   📄 {result['path']}")
        if show_preview and result.get('preview'):
            print(f"   💭 {result['preview']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Search client content across Pete\'s Brain',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  client-search "Q4 strategy"
  
  # Filter by client
  client-search --client smythson "performance max"
  
  # Filter by content type
  client-search --type meeting "budget discussion"
  
  # Date range search
  client-search --from 2025-11-01 "weekly meeting"
  
  # AI-powered search with summary
  client-search --ai "what did we decide about Q4 budgets"
  
  # Detailed AI search (reads full content)
  client-search --ai --detailed "smythson conversion tracking issues"
  
  # Multiple filters
  client-search --client smythson --type meeting --from 2025-10-01 "strategy"
  
  # Show statistics
  client-search --stats
        """
    )
    
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--client', help='Filter by client name')
    parser.add_argument('--type', help='Filter by content type (meeting, email, document, etc.)')
    parser.add_argument('--from', dest='date_from', help='Filter by date from (YYYY-MM-DD)')
    parser.add_argument('--to', dest='date_to', help='Filter by date to (YYYY-MM-DD)')
    parser.add_argument('--ai', action='store_true', help='Use AI to analyze and summarize results')
    parser.add_argument('--detailed', action='store_true', help='Read full content for AI analysis (slower but better)')
    parser.add_argument('--stats', action='store_true', help='Show client content statistics')
    parser.add_argument('--limit', type=int, default=15, help='Number of results to show (default: 15)')
    
    args = parser.parse_args()
    
    # Load index
    index = load_index()
    
    # Show stats
    if args.stats:
        print("=" * 60)
        print("  Client Content Statistics")
        print("=" * 60)
        print()
        print(f"📊 Total files: {index['total_files']}")
        print(f"📝 Total words: {index['total_words']:,}")
        print(f"📅 Last indexed: {index['generated'][:19]}")
        print()
        print("👥 Clients:")
        print()
        for client, stats in sorted(index["clients"].items(), key=lambda x: x[1]["count"], reverse=True):
            print(f"  {client:30} {stats['count']:3} files  ({stats['total_words']:,} words)")
        print()
        print("📂 Content Types:")
        print()
        for content_type, stats in sorted(index["content_types"].items(), key=lambda x: x[1]["count"], reverse=True):
            print(f"  {content_type:30} {stats['count']:3} files  ({stats['total_words']:,} words)")
        print()
        return
    
    # Require query
    if not args.query:
        parser.print_help()
        return
    
    print("=" * 60)
    print(f"  Searching: {args.query}")
    if args.client:
        print(f"  Client: {args.client}")
    if args.type:
        print(f"  Type: {args.type}")
    if args.date_from:
        print(f"  From: {args.date_from}")
    if args.date_to:
        print(f"  To: {args.date_to}")
    print("=" * 60)
    print()
    
    # Keyword search with filters
    results = keyword_search(
        args.query, 
        index, 
        client=args.client,
        content_type=args.type,
        date_from=args.date_from,
        date_to=args.date_to,
        limit=args.limit
    )
    
    if not results:
        print("❌ No results found")
        print()
        print("💡 Try:")
        print("  - Broader search terms")
        print("  - Different keywords")
        print("  - Remove filters (--client, --type, --from, --to)")
        print("  - Check --stats to see available clients and content types")
        return
    
    # Show results
    print_results(results, show_preview=not args.ai)
    
    # AI analysis
    if args.ai:
        print("=" * 60)
        print("  AI Analysis")
        print("=" * 60)
        print()
        
        answer = ai_search(args.query, results, detailed=args.detailed)
        print(answer)
        print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Search cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

