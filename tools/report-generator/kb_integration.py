"""
Knowledge Base Integration Module

Wraps tools/kb-search.py functionality for easy integration with campaign analysis.
Provides convenient methods to query the Knowledge Base for optimization insights,
best practices, and platform updates.
"""

import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Add parent directory to path for kb-search imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

try:
    # Import kb-search.py using importlib (handles hyphenated filenames)
    import importlib.util
    kb_search_path = REPO_ROOT / "tools" / "kb-search.py"
    spec = importlib.util.spec_from_file_location("kb_search", kb_search_path)
    kb_search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kb_search)

    # Now we can access functions from the module
    load_index = kb_search.load_index
    load_google_specs_index = kb_search.load_google_specs_index
    keyword_search = kb_search.keyword_search
    search_specs_index = kb_search.search_specs_index
    read_file_content = kb_search.read_file_content
    ai_search = kb_search.ai_search
    ai_strategic_recommendation = kb_search.ai_strategic_recommendation

    KB_SEARCH_AVAILABLE = True
except Exception as e:
    logger.warning(f"Could not import kb-search module: {e}")
    KB_SEARCH_AVAILABLE = False


class KBIntegration:
    """Integration layer for Knowledge Base search functionality"""

    def __init__(self):
        """Initialize KB integration"""
        self.kb_index = None
        self.google_specs_index = None

        if KB_SEARCH_AVAILABLE:
            try:
                self.kb_index = load_index()
                logger.info(f"Loaded KB index with {len(self.kb_index.get('files', []))} files")
            except Exception as e:
                logger.error(f"Failed to load KB index: {e}")

            try:
                self.google_specs_index = load_google_specs_index()
                if self.google_specs_index:
                    logger.info("Loaded Google Specs index")
            except Exception as e:
                logger.warning(f"Could not load Google Specs index: {e}")

    def search_optimization_insights(
        self,
        campaign_type: str,
        issue_type: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for optimization insights for a specific campaign type and issue

        Args:
            campaign_type: Campaign type (e.g., 'Performance Max', 'Shopping', 'Search')
            issue_type: Issue description (e.g., 'low ROAS', 'high CPC', 'poor CTR')
            limit: Maximum number of results

        Returns:
            List of relevant KB articles with titles, paths, and previews
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return []

        # Construct search query
        query = f"{campaign_type} {issue_type} optimization"

        try:
            results = keyword_search(query, self.kb_index, limit=limit)
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error searching for optimization insights: {e}")
            return []

    def get_best_practices(self, topic: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get best practices for a specific topic

        Args:
            topic: Topic to search (e.g., 'Shopping campaign structure', 'keyword research')
            limit: Maximum number of results

        Returns:
            List of relevant KB articles
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return []

        try:
            query = f"{topic} best practices strategy"
            results = keyword_search(query, self.kb_index, limit=limit)
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error getting best practices: {e}")
            return []

    def get_platform_updates(self, days: int = 30, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent Google Ads platform updates

        Args:
            days: How many days back to search
            limit: Maximum number of results

        Returns:
            List of recent platform update articles
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return []

        try:
            # Search for platform updates category
            query = "google ads platform update changes announcement"
            all_results = keyword_search(query, self.kb_index, limit=limit * 2)

            # Filter for recent updates (if date metadata available)
            # For now, just return top results from platform-updates category
            recent_updates = [
                r for r in all_results
                if 'platform-update' in r.get('path', '').lower()
                or 'changelog' in r.get('path', '').lower()
            ]

            return self._format_results(recent_updates[:limit])
        except Exception as e:
            logger.error(f"Error getting platform updates: {e}")
            return []

    def analyze_with_kb(
        self,
        metrics: Dict[str, float],
        campaign_type: str,
        context: str = ""
    ) -> Optional[str]:
        """
        AI-powered analysis using KB context

        Args:
            metrics: Performance metrics dict (e.g., {'roas': 2.5, 'cpa': 45.0})
            campaign_type: Type of campaign
            context: Additional context about the situation

        Returns:
            AI-generated analysis and recommendations, or None if unavailable
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return None

        # Check if ANTHROPIC_API_KEY is available
        if not os.getenv('ANTHROPIC_API_KEY'):
            logger.warning("ANTHROPIC_API_KEY not set - AI analysis unavailable")
            return None

        try:
            # Build query from metrics and context
            metrics_str = ", ".join([f"{k}={v}" for k, v in metrics.items()])
            query = f"{campaign_type} campaign performance analysis: {metrics_str}. {context}"

            # Get relevant KB articles
            keyword_results = keyword_search(query, self.kb_index, limit=10)

            # Get AI analysis
            analysis = ai_search(query, keyword_results, detailed=True)

            return analysis
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return None

    def get_strategic_recommendation(
        self,
        issue_description: str,
        campaign_type: Optional[str] = None,
        client_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get structured strategic recommendation using brain-advisor pattern

        Args:
            issue_description: Description of the issue or question
            campaign_type: Optional campaign type for context
            client_name: Optional client name for context

        Returns:
            Dict with structured recommendation, or None if unavailable
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return None

        if not os.getenv('ANTHROPIC_API_KEY'):
            logger.warning("ANTHROPIC_API_KEY not set - strategic recommendations unavailable")
            return None

        try:
            # Build query
            query = issue_description
            if campaign_type:
                query = f"{campaign_type}: {query}"

            # Get relevant KB articles
            keyword_results = keyword_search(query, self.kb_index, limit=10)

            # Get strategic recommendation
            recommendation = ai_strategic_recommendation(
                query,
                keyword_results,
                client_name=client_name
            )

            return recommendation
        except Exception as e:
            logger.error(f"Error getting strategic recommendation: {e}")
            return None

    def search_by_category(
        self,
        category: str,
        search_term: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search within a specific KB category

        Args:
            category: Category path (e.g., 'google-ads/performance-max')
            search_term: Optional search term within category
            limit: Maximum number of results

        Returns:
            List of relevant KB articles
        """
        if not KB_SEARCH_AVAILABLE or not self.kb_index:
            logger.warning("KB search not available")
            return []

        try:
            # Filter results by category
            all_files = self.kb_index.get('files', [])
            category_files = [
                f for f in all_files
                if category.lower() in f.get('path', '').lower()
            ]

            if search_term:
                # Score by search term
                query_terms = search_term.lower().split()
                scored_files = []

                for file_data in category_files:
                    score = 0
                    title_lower = file_data["title"].lower()
                    preview_lower = file_data.get("content_preview", "").lower()

                    for term in query_terms:
                        if term in title_lower:
                            score += 10
                        if term in preview_lower:
                            score += 1

                    if score > 0:
                        scored_files.append({**file_data, "score": score})

                scored_files.sort(key=lambda x: x["score"], reverse=True)
                return self._format_results(scored_files[:limit])
            else:
                # Return all category files
                return self._format_results(category_files[:limit])

        except Exception as e:
            logger.error(f"Error searching by category: {e}")
            return []

    def get_google_specs(self, spec_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Google Ads specifications

        Args:
            spec_name: Specification to search for
            limit: Maximum number of results

        Returns:
            List of relevant specification documents
        """
        if not KB_SEARCH_AVAILABLE or not self.google_specs_index:
            logger.warning("Google Specs index not available")
            return []

        try:
            results = search_specs_index(
                spec_name,
                self.google_specs_index,
                limit=limit,
                platform="google"
            )
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Error searching Google specs: {e}")
            return []

    def _format_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format KB search results for consistent output

        Args:
            results: Raw search results

        Returns:
            Formatted results with consistent structure
        """
        formatted = []

        for result in results:
            formatted.append({
                'title': result.get('title', 'Untitled'),
                'path': result.get('path', ''),
                'category': result.get('category', 'Unknown'),
                'preview': result.get('preview', result.get('content_preview', ''))[:300],
                'score': result.get('score', 0),
                'type': result.get('type', 'article')
            })

        return formatted


# Example usage and testing
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    kb = KBIntegration()

    # Test optimization insights search
    print("\n" + "="*60)
    print("TEST: Optimization Insights - Performance Max Low ROAS")
    print("="*60)
    results = kb.search_optimization_insights("Performance Max", "low ROAS", limit=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Category: {result['category']}")
        print(f"   Preview: {result['preview'][:150]}...")

    # Test best practices
    print("\n" + "="*60)
    print("TEST: Best Practices - Shopping Campaign Structure")
    print("="*60)
    results = kb.get_best_practices("Shopping campaign structure", limit=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Category: {result['category']}")

    # Test platform updates
    print("\n" + "="*60)
    print("TEST: Platform Updates (Last 30 Days)")
    print("="*60)
    results = kb.get_platform_updates(days=30, limit=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Category: {result['category']}")

    # Test category search
    print("\n" + "="*60)
    print("TEST: Category Search - Performance Max")
    print("="*60)
    results = kb.search_by_category("google-ads/performance-max", limit=3)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Path: {result['path']}")
