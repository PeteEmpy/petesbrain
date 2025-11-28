#!/usr/bin/env python3
"""
Knowledge Base AI Search

AI-powered semantic search across Pete's Brain knowledge base.
Uses Claude to find and summarize relevant knowledge.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Optional import for AI features
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent
KB_ROOT = PROJECT_ROOT / "roksys" / "knowledge-base"
GOOGLE_SPECS_ROOT = PROJECT_ROOT / "google-specifications"
FACEBOOK_SPECS_ROOT = PROJECT_ROOT / "facebook-specifications"
INDEX_FILE = PROJECT_ROOT / "shared" / "data" / "kb-index.json"
GOOGLE_SPECS_INDEX_FILE = GOOGLE_SPECS_ROOT / "index.json"
FACEBOOK_SPECS_INDEX_FILE = FACEBOOK_SPECS_ROOT / "index.json"


def load_index() -> Dict[str, Any]:
    """Load the knowledge base index"""
    if not INDEX_FILE.exists():
        print("❌ Knowledge base index not found!")
        print(f"   Run: python3 agents/knowledge-base-indexer/knowledge-base-indexer.py")
        sys.exit(1)
    
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)


def load_google_specs_index() -> Optional[Dict[str, Any]]:
    """Load the Google specifications knowledge base index"""
    if not GOOGLE_SPECS_INDEX_FILE.exists():
        return None
    
    with open(GOOGLE_SPECS_INDEX_FILE, 'r') as f:
        return json.load(f)


def load_facebook_specs_index() -> Optional[Dict[str, Any]]:
    """Load the Facebook specifications knowledge base index"""
    if not FACEBOOK_SPECS_INDEX_FILE.exists():
        return None
    
    with open(FACEBOOK_SPECS_INDEX_FILE, 'r') as f:
        return json.load(f)


def keyword_search(query: str, index: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
    """Basic keyword search across titles and content"""
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    results = []
    
    for file_data in index["files"]:
        score = 0
        
        # Search in title (higher weight)
        title_lower = file_data["title"].lower()
        for term in query_terms:
            if term in title_lower:
                score += 10
        
        # Search in preview
        preview_lower = file_data.get("content_preview", "").lower()
        for term in query_terms:
            if term in preview_lower:
                score += 1
        
        # Search in path/category
        path_lower = file_data["path"].lower()
        for term in query_terms:
            if term in path_lower:
                score += 5
        
        if score > 0:
            results.append({
                **file_data,
                "score": score
            })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:limit]


def search_specs_index(query: str, specs_index: Dict[str, Any], source_filter: Optional[str] = None, limit: int = 20, platform: str = "google") -> List[Dict[str, Any]]:
    """Search specifications index"""
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    results = []
    
    # Determine categories based on platform
    if platform == "facebook":
        categories = ["facebook_ads", "meta_business_suite"]
    else:  # google
        categories = ["google_ads", "ga4", "rok_methodologies"]
    
    # Search through all categories
    for category_key in categories:
        if category_key not in specs_index:
            continue
        
        category_data = specs_index[category_key]
        
        # Search specifications
        for subcategory, specs_dict in category_data.get("specifications", {}).items():
            for spec_name, spec_data in specs_dict.items():
                score = 0
                
                # Search in title
                title = spec_data.get("title", "").lower()
                summary = spec_data.get("summary", "").lower()
                file_path = spec_data.get("file", "").lower()
                
                for term in query_terms:
                    if term in title:
                        score += 10
                    if term in summary:
                        score += 5
                    if term in file_path:
                        score += 3
                
                # Filter by source if specified
                if source_filter:
                    sources = spec_data.get("sources", [])
                    if source_filter.lower() not in [s.lower() for s in sources]:
                        continue
                
                if score > 0:
                    results.append({
                        "title": spec_data.get("title", spec_name),
                        "category": f"{category_key}/{subcategory}",
                        "path": spec_data.get("file", ""),
                        "preview": spec_data.get("summary", ""),
                        "score": score,
                        "type": "specification",
                        "sources": spec_data.get("sources", []),
                        "version": spec_data.get("version", ""),
                        "last_updated": spec_data.get("last_updated", "")
                    })
        
        # Search best practices
        for subcategory, bp_list in category_data.get("best_practices", {}).items():
            for bp_data in bp_list:
                score = 0
                
                title = bp_data.get("title", "").lower()
                file_path = bp_data.get("file", "").lower()
                
                for term in query_terms:
                    if term in title:
                        score += 10
                    if term in file_path:
                        score += 3
                
                # Filter by source if specified
                if source_filter:
                    source_type = bp_data.get("source_type", "").lower()
                    if source_filter.lower() not in source_type:
                        continue
                
                if score > 0:
                    results.append({
                        "title": bp_data.get("title", "Untitled"),
                        "category": f"{category_key}/{subcategory}",
                        "path": bp_data.get("file", ""),
                        "preview": "",
                        "score": score,
                        "type": "best_practice",
                        "source_type": bp_data.get("source_type", ""),
                        "date_added": bp_data.get("date_added", "")
                    })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:limit]


def read_file_content(file_path: str) -> str:
    """Read full content of a knowledge base file"""
    full_path = KB_ROOT / file_path
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"


def read_specs_file_content(file_path: str, platform: str = "google") -> str:
    """Read full content of a specifications file"""
    if platform == "facebook":
        full_path = FACEBOOK_SPECS_ROOT / file_path
    else:
        full_path = GOOGLE_SPECS_ROOT / file_path
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"


def ai_search(query: str, keyword_results: List[Dict[str, Any]], detailed: bool = False) -> str:
    """Use Claude to analyze and summarize relevant knowledge"""

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
**Category:** {result['category']}
**File:** {result['path']}

{content[:2000]}  # First 2000 chars
""")
    else:
        # Use previews for all results
        for result in keyword_results[:10]:
            context_parts.append(f"""
- **{result['title']}** ({result['category']})
  {result.get('preview', result.get('content_preview', '')[:200])}
""")

    context = "\n".join(context_parts)

    prompt = f"""You are searching Pete's Brain knowledge base to answer a question.

QUERY: {query}

RELEVANT KNOWLEDGE BASE FILES:
{context}

Please provide a helpful answer to the query based on the knowledge base content above.

Format your response as:
1. Direct answer to the query
2. Key points from the knowledge base
3. Which specific files to read for more details

Be concise but informative. If the knowledge base doesn't contain relevant information, say so."""

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


def ai_strategic_recommendation(query: str, keyword_results: List[Dict[str, Any]], client_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Provide structured strategic recommendation (Mike Rhodes brain-advisor pattern).

    Returns four-part response:
    1. Main Analysis - Direct answer with synthesis, actionable steps, data/frameworks, citations
    2. Recommended Reading - 1-3 KB articles with context
    3. Follow-Up Questions - 2-3 natural follow-ups to facilitate dialogue
    4. Devil's Advocate - Why approach might fail, wrong assumptions, alternatives

    Based on brain-advisor pattern from Mike Rhodes' template.

    Args:
        query: User's strategic question
        keyword_results: Relevant KB files from search
        client_name: Optional client context

    Returns:
        Dict with main_analysis, recommended_reading, follow_ups, devils_advocate
    """
    # Check if anthropic is available
    if not ANTHROPIC_AVAILABLE:
        return {"error": "Anthropic library not installed"}

    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set"}

    client = anthropic.Anthropic(api_key=api_key)

    # Read FULL content of top 10 results (Mike's pattern: read all, don't summarize)
    kb_files_content = []
    for result in keyword_results[:10]:
        try:
            # Check KB type to determine how to read file
            kb_type = result.get('kb_type', 'news')
            if kb_type == 'google_specs' or kb_type == 'facebook_specs':
                platform = 'facebook' if kb_type == 'facebook_specs' else 'google'
                content = read_specs_file_content(result["path"], platform=platform)
            else:
                content = read_file_content(result["path"])

            kb_files_content.append({
                "title": result['title'],
                "category": result['category'],
                "file": result['path'],
                "content": content
            })
        except Exception as e:
            print(f"   ⚠️ Error reading {result['title']}: {e}")
            continue

    print("🤖 Generating structured strategic recommendation...")
    print(f"   Read {len(kb_files_content)} full KB files")
    print()

    # Build context
    files_context = ""
    for kb_file in kb_files_content:
        files_context += f"""
### {kb_file['title']}
**Category:** {kb_file['category']}
**File:** {kb_file['file']}

{kb_file['content']}

---
"""

    # Add client context if provided
    client_context = ""
    if client_name:
        context_file = PROJECT_ROOT / "clients" / client_name / "CONTEXT.md"
        if context_file.exists():
            try:
                with open(context_file, 'r') as f:
                    context_content = f.read()
                    client_context = f"""
## CLIENT CONTEXT: {client_name.title()}

{context_content[:3000]}  # First 3000 chars of CONTEXT.md
"""
                print(f"   ✓ Loaded client context: {client_name}")
            except Exception:
                pass

    prompt = f"""You are providing a structured strategic recommendation for Pete's Google Ads agency (Roksys).

Pete runs Roksys - specializing in Google Ads shopping campaigns and ecommerce clients.
{client_context}

**STRATEGIC QUESTION:**
{query}

**KNOWLEDGE BASE CONTEXT:**
{files_context}

Your task: Provide a comprehensive structured strategic recommendation following this exact format:

## MAIN ANALYSIS

Provide a direct answer to Pete's question with:
- **Direct Answer:** Clear response to the question (2-3 sentences)
- **Synthesis:** Synthesize insights across multiple KB sources (don't just list - synthesize!)
- **Actionable Steps:** Specific numbered steps Pete can take
- **Data Points & Frameworks:** Include specific numbers, percentages, frameworks from KB
- **Source Citations:** Reference specific KB files by name (e.g., "According to [title] in [category]...")

## RECOMMENDED READING

Suggest 1-3 specific KB articles Pete should read for deeper understanding:
1. **[Title]** (from [category])
   - **Why relevant:** [Explain how it relates to the question]
   - **Key takeaway:** [One sentence summary of main point]

## FOLLOW-UP QUESTIONS

Suggest 2-3 natural follow-up questions Pete might ask to dig deeper:
- [Question 1 that naturally follows from this analysis]
- [Question 2 exploring implications]
- [Question 3 about specific implementation]

## DEVIL'S ADVOCATE

Challenge your own recommendation with 2-3 counterpoints:
- **Why this might NOT work:** [Specific reason the approach could fail]
- **Assumptions that could be wrong:** [Key assumptions you're making]
- **Alternative perspectives:** [Different approaches from KB sources]

**IMPORTANT:**
- Use British English (optimise, analyse, etc.)
- Be specific with numbers and data from KB
- Cite sources properly
- Be conversational but thorough
- Challenge your own assumptions in Devil's Advocate

Format your response as clean markdown with the four sections above."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response = message.content[0].text

        # Parse response into sections
        sections = {
            "full_response": response,
            "kb_files_used": [{"title": f["title"], "category": f["category"], "file": f["file"]} for f in kb_files_content]
        }

        print(f"   ✓ Generated structured recommendation ({len(response)} chars)")

        return sections

    except Exception as e:
        print(f"   ❌ Error generating recommendation: {e}")
        return {"error": str(e)}


def ai_semantic_rank(query: str, keyword_results: List[Dict[str, Any]], limit: int = 15) -> List[Dict[str, Any]]:
    """
    Use Claude to semantically rank keyword search results by relevance.

    This is a two-stage search:
    1. Keyword search narrows to candidates (fast)
    2. AI semantic ranking reorders by true relevance (accurate)

    Args:
        query: User's search query
        keyword_results: Results from keyword search
        limit: Maximum results to return (default: 15)

    Returns:
        Reordered list of results ranked by semantic relevance
    """
    # Check if anthropic is available
    if not ANTHROPIC_AVAILABLE:
        print("⚠️  Anthropic library not installed. Falling back to keyword ranking.")
        return keyword_results[:limit]

    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set. Falling back to keyword ranking.")
        return keyword_results[:limit]

    if not keyword_results:
        return []

    # Process in batches to avoid huge prompts (similar to Mike's approach)
    batch_size = 50
    all_ranked_results = []

    print("🤖 AI semantic ranking...")
    print(f"   Analyzing {len(keyword_results)} candidates in batches of {batch_size}")

    client = anthropic.Anthropic(api_key=api_key)

    for i in range(0, len(keyword_results), batch_size):
        batch = keyword_results[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(keyword_results) + batch_size - 1) // batch_size

        print(f"   Batch {batch_num}/{total_batches}...")

        # Build file list with previews
        file_list = []
        for idx, result in enumerate(batch):
            title = result.get('title', 'Untitled')
            category = result.get('category', 'Unknown')
            preview = result.get('preview', result.get('content_preview', ''))[:300]

            file_list.append(f"{idx}. [{category}] {title}\n   Preview: {preview}...")

        files_text = "\n\n".join(file_list)

        prompt = f"""You are a search ranking agent for Pete's Brain knowledge base.

Pete runs Roksys - a Google Ads agency specializing in shopping campaigns and ecommerce clients.

Question: "{query}"

Your task: Analyze these {len(batch)} files and identify which ones are most relevant to answering this question.

Files:
{files_text}

Respond with ONLY a JSON array of file indices ranked by relevance (most relevant first).
Include only files that are actually relevant (don't force a ranking if nothing matches).
Maximum {limit} results.

Format: [0, 5, 12, 3]"""

        try:
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",  # Use Haiku for speed + cost
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response = message.content[0].text.strip()

            # Parse JSON response
            try:
                ranked_indices = json.loads(response)

                # Map indices back to result objects
                ranked_batch = [batch[idx] for idx in ranked_indices if idx < len(batch)]
                all_ranked_results.extend(ranked_batch)

            except json.JSONDecodeError:
                print(f"   ⚠️  Could not parse AI response, keeping keyword order for this batch")
                all_ranked_results.extend(batch[:limit])

        except Exception as e:
            print(f"   ⚠️  Error ranking batch: {str(e)[:100]}")
            all_ranked_results.extend(batch[:limit])

    # Return top results
    final_results = all_ranked_results[:limit]
    print(f"   ✓ Ranked {len(final_results)} results by semantic relevance")

    return final_results


def print_results(results: List[Dict[str, Any]], show_preview: bool = True, is_specs: bool = False):
    """Print search results"""
    kb_type = "specifications" if is_specs else "knowledge base"
    print(f"📚 Found {len(results)} relevant {kb_type} file(s)")
    print()
    
    for i, result in enumerate(results[:15], 1):
        print(f"{i}. {result['title']}")
        print(f"   📁 {result['category']}")
        print(f"   📄 {result['path']}")
        
        if is_specs:
            if result.get('type') == 'specification':
                print(f"   📋 Type: Specification")
                if result.get('version'):
                    print(f"   🔢 Version: {result['version']}")
                if result.get('sources'):
                    print(f"   📌 Sources: {', '.join(result['sources'][:3])}")
            else:
                print(f"   📋 Type: Best Practice")
                if result.get('source_type'):
                    print(f"   📌 Source: {result['source_type']}")
        
        if show_preview and result.get('preview'):
            print(f"   💭 {result['preview']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Search Pete\'s Brain knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search (news KB)
  kb-search "performance max strategies"
  
  # Search specifications KB only
  kb-search --specs "headline requirements"
  
  # Search both KBs
  kb-search --include-specs "performance max"
  
  # Filter by source (specs KB)
  kb-search --specs "headlines" --source "official_documentation"
  
  # AI-powered search with summary
  kb-search --ai "how to optimize shopping campaigns"
  
  # Detailed AI search (reads full content)
  kb-search --ai --detailed "what are the latest google ads updates"

  # AI semantic ranking (understands meaning, not just keywords)
  kb-search --semantic "how to price enterprise services"

  # Semantic + AI summary (best of both)
  kb-search --semantic --ai "performance max best practices"

  # List all files in a category
  kb-search --category "google-ads/performance-max"
  
  # Show statistics
  kb-search --stats
        """
    )
    
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--ai', action='store_true', help='Use AI to analyze and summarize results')
    parser.add_argument('--detailed', action='store_true', help='Read full content for AI analysis (slower but better)')
    parser.add_argument('--semantic', action='store_true', help='Use AI to semantically rank results (understands meaning, not just keywords)')
    parser.add_argument('--strategic', action='store_true', help='Provide structured strategic recommendation (Main Analysis + Recommended Reading + Follow-Ups + Devil\'s Advocate)')
    parser.add_argument('--client', help='Client name for context (used with --strategic)')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--stats', action='store_true', help='Show knowledge base statistics')
    parser.add_argument('--limit', type=int, default=15, help='Number of results to show (default: 15)')
    parser.add_argument('--specs', action='store_true', help='Search specifications KB only (Google by default)')
    parser.add_argument('--facebook-specs', action='store_true', help='Search Facebook specifications KB only')
    parser.add_argument('--include-specs', action='store_true', help='Search both knowledge bases (includes Google specs)')
    parser.add_argument('--include-all-specs', action='store_true', help='Search both knowledge bases AND all specs (Google + Facebook)')
    parser.add_argument('--source', help='Filter by source type (for specs KB: official_documentation, meta_rep_recommendation, google_rep_recommendation, etc.)')
    
    args = parser.parse_args()
    
    # Load indexes
    index = load_index()
    google_specs_index = load_google_specs_index()
    facebook_specs_index = load_facebook_specs_index()
    
    # Show stats
    if args.stats:
        print("=" * 60)
        print("  Knowledge Base Statistics")
        print("=" * 60)
        print()
        print(f"📊 Total files: {index['total_files']}")
        print(f"📝 Total words: {index['total_words']:,}")
        print(f"📅 Last indexed: {index['generated'][:19]}")
        print()
        print("📂 Categories:")
        print()
        for category, stats in sorted(index["categories"].items(), key=lambda x: x[1]["count"], reverse=True):
            print(f"  {category:35} {stats['count']:3} files  ({stats['total_words']:,} words)")
        print()
        
        if google_specs_index:
            print("=" * 60)
            print("  Google Specifications Knowledge Base Statistics")
            print("=" * 60)
            print()
            print(f"📅 Last updated: {google_specs_index.get('last_updated', 'Unknown')[:19]}")
            print()
            for category_key in ["google_ads", "ga4", "rok_methodologies"]:
                if category_key in google_specs_index:
                    cat_data = google_specs_index[category_key]
                    total_specs = sum(len(specs) for specs in cat_data.get("specifications", {}).values())
                    total_bp = sum(len(bp) for bp in cat_data.get("best_practices", {}).values())
                    print(f"  {category_key.replace('_', '-').title()}: {total_specs} specs, {total_bp} best practices")
            print()
        
        if facebook_specs_index:
            print("=" * 60)
            print("  Facebook Specifications Knowledge Base Statistics")
            print("=" * 60)
            print()
            print(f"📅 Last updated: {facebook_specs_index.get('last_updated', 'Unknown')[:19]}")
            print()
            for category_key in ["facebook_ads", "meta_business_suite"]:
                if category_key in facebook_specs_index:
                    cat_data = facebook_specs_index[category_key]
                    total_specs = sum(len(specs) for specs in cat_data.get("specifications", {}).values())
                    total_bp = sum(len(bp) for bp in cat_data.get("best_practices", {}).values())
                    print(f"  {category_key.replace('_', '-').title()}: {total_specs} specs, {total_bp} best practices")
            print()
        return
    
    # Require query
    if not args.query:
        parser.print_help()
        return
    
    print("=" * 60)
    print(f"  Searching: {args.query}")
    if args.facebook_specs:
        print("  📋 Searching: Facebook Specifications KB only")
    elif args.specs:
        print("  📋 Searching: Google Specifications KB only")
    elif args.include_all_specs:
        print("  📚 Searching: News KB + Google Specs + Facebook Specs")
    elif args.include_specs:
        print("  📚 Searching: News KB + Google Specs")
    print("=" * 60)
    print()
    
    # Determine which KBs to search
    search_facebook_specs_only = args.facebook_specs
    search_google_specs_only = args.specs
    search_both = args.include_specs
    search_all_specs = args.include_all_specs
    
    results = []
    google_specs_results = []
    facebook_specs_results = []
    
    # Search news KB (unless specs-only)
    if not search_google_specs_only and not search_facebook_specs_only:
        results = keyword_search(args.query, index, limit=args.limit)
    
    # Search Google specs KB
    if search_google_specs_only or search_both or search_all_specs:
        if not google_specs_index:
            print("⚠️  Google specifications index not found!")
            print(f"   Run: python3 tools/google-specs-indexer.py")
            if search_google_specs_only:
                return
        else:
            google_specs_results = search_specs_index(args.query, google_specs_index, source_filter=args.source, limit=args.limit, platform="google")
    
    # Search Facebook specs KB
    if search_facebook_specs_only or search_all_specs:
        if not facebook_specs_index:
            print("⚠️  Facebook specifications index not found!")
            print(f"   Run: python3 tools/facebook-specs-indexer.py")
            if search_facebook_specs_only:
                return
        else:
            facebook_specs_results = search_specs_index(args.query, facebook_specs_index, source_filter=args.source, limit=args.limit, platform="facebook")
    
    # Combine results
    if search_all_specs:
        # Mark all results
        for r in google_specs_results:
            r['kb_type'] = 'google_specs'
        for r in facebook_specs_results:
            r['kb_type'] = 'facebook_specs'
        for r in results:
            r['kb_type'] = 'news'
        
        # Combine and re-sort by score
        all_results = results + google_specs_results + facebook_specs_results
        all_results.sort(key=lambda x: x["score"], reverse=True)
        results = all_results[:args.limit]
    elif search_both:
        # Mark specs results
        for r in google_specs_results:
            r['kb_type'] = 'google_specs'
        for r in results:
            r['kb_type'] = 'news'
        
        # Combine and re-sort by score
        all_results = results + google_specs_results
        all_results.sort(key=lambda x: x["score"], reverse=True)
        results = all_results[:args.limit]
    elif search_facebook_specs_only:
        results = facebook_specs_results
    elif search_google_specs_only:
        results = google_specs_results
    
    if not results:
        print("❌ No results found")
        print()
        print("💡 Try:")
        print("  - Broader search terms")
        print("  - Different keywords")
        print("  - Check --stats to see available categories")
        return
    
    # Filter by category if specified
    if args.category:
        results = [r for r in results if args.category.lower() in r['category'].lower()]
        if not results:
            print(f"❌ No results in category: {args.category}")
            return

    # AI semantic ranking (optional, preserves all existing functionality)
    if args.semantic:
        print()
        print("=" * 60)
        print("  AI Semantic Ranking")
        print("=" * 60)
        print()
        results = ai_semantic_rank(args.query, results, limit=args.limit)
        print()

    # Show results
    is_specs = search_google_specs_only or search_facebook_specs_only
    print_results(results, show_preview=not (args.ai or args.strategic), is_specs=is_specs)

    # Strategic recommendation (Priority 2 implementation)
    if args.strategic:
        print("=" * 60)
        print("  Strategic Recommendation")
        print("=" * 60)
        print()

        recommendation = ai_strategic_recommendation(args.query, results, client_name=args.client)

        if "error" in recommendation:
            print(f"❌ {recommendation['error']}")
        else:
            print(recommendation["full_response"])
            print()
            print("=" * 60)
            print(f"  KB Files Used: {len(recommendation['kb_files_used'])}")
            print("=" * 60)
            for kb_file in recommendation['kb_files_used']:
                print(f"  • {kb_file['title']} ({kb_file['category']})")
        print()

    # AI analysis (original functionality preserved)
    elif args.ai:
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

