#!/usr/bin/env python3
"""
Smart Keyword Generator for Google Ads Campaign Builder
Generates high-quality keywords with deduplication and quality scoring.
"""

import os
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
import json
from typing import Dict, List, Set
import re


class KeywordGenerator:
    """Intelligent keyword generator with quality scoring and deduplication."""

    # Model pricing (per 1M tokens)
    MODEL_COSTS = {
        'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
        'claude-3-5-sonnet-20241022': {'input': 3.00, 'output': 15.00}
    }

    def __init__(self, url: str, client_name: str = None, model: str = 'claude-3-haiku-20240307'):
        self.url = url
        self.client_name = client_name
        self.model = model  # Default to Haiku (12x cheaper than Sonnet)
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=self.api_key)

        # Cost tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def fetch_page_content(self) -> str:
        """Fetch and extract relevant content from landing page."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove scripts, styles, and navigation
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()

            # Extract key content
            title = soup.find('title')
            title_text = title.get_text() if title else ""

            meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                       soup.find('meta', attrs={'property': 'og:description'})
            meta_text = meta_desc.get('content', '') if meta_desc else ""

            h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')[:5]]
            h2_tags = [h2.get_text().strip() for h2 in soup.find_all('h2')[:10]]
            paragraphs = [p.get_text().strip() for p in soup.find_all('p')[:15] if len(p.get_text().strip()) > 30]
            list_items = [li.get_text().strip() for li in soup.find_all('li')[:20] if len(li.get_text().strip()) > 10]

            content = f"""
URL: {self.url}

TITLE: {title_text}

META DESCRIPTION: {meta_text}

MAIN HEADINGS:
{chr(10).join('- ' + h for h in h1_tags if h)}

SECTION HEADINGS:
{chr(10).join('- ' + h for h in h2_tags if h)}

KEY FEATURES/POINTS:
{chr(10).join('- ' + item for item in list_items[:15] if item)}

MAIN CONTENT:
{chr(10).join(paragraphs[:10])}
"""
            return content.strip()

        except Exception as e:
            raise Exception(f"Failed to fetch landing page: {str(e)}")

    def generate_keywords(self, max_keywords: int = 25) -> List[Dict]:
        """
        Generate high-quality keywords using Claude AI.

        Returns list of keyword dictionaries:
        {
            'keyword': str,
            'match_type': 'EXACT' | 'BROAD' | 'PHRASE',
            'intent': 'high' | 'medium' | 'low',
            'relevance_score': float (0-1),
            'rationale': str
        }
        """
        print("Fetching landing page content...", flush=True)
        page_content = self.fetch_page_content()

        print("Analyzing page and generating smart keywords with Claude...", flush=True)

        prompt = f"""You are a Google Ads keyword research specialist focused on QUALITY over quantity.

Analyze this landing page and generate {max_keywords} HIGH-CONVERTING keywords.

CRITICAL REQUIREMENTS:
1. CONVERSION INTENT: Only suggest keywords that indicate BUYING INTENT, not just research
2. RELEVANCE: Keywords must be highly relevant to the specific product/service on this page
3. COMMERCIAL VALUE: Focus on keywords users search when ready to purchase/convert
4. MATCH TYPES: Prefer EXACT and BROAD. Only use PHRASE if there's a strong case.

LANDING PAGE CONTENT:
{page_content}

For each keyword, provide:
1. The keyword text (lowercase, 2-5 words typically)
2. Match type (EXACT, BROAD, or rarely PHRASE)
3. Conversion intent (high/medium/low)
4. Relevance score (0-1)
5. Brief rationale (why this keyword will convert)

FOCUS ON:
- Product/service specific terms (not generic)
- Commercial modifiers (buy, price, best, cheap, premium, professional, etc.)
- Location + product (if applicable)
- Brand + product variations
- Problem-solving queries (if product solves specific problem)

AVOID:
- Generic single-word keywords
- Informational keywords (how to, what is, guide to)
- Research-phase keywords
- Overly broad terms
- Keywords with low commercial intent

Return as JSON array:
[
  {{
    "keyword": "premium leather diary",
    "match_type": "EXACT",
    "intent": "high",
    "relevance_score": 0.95,
    "rationale": "Specific product with quality modifier - high purchase intent"
  }},
  ...
]

Generate exactly {max_keywords} keywords focused on CONVERSIONS."""

        try:
            print(f"Using model: {self.model}", flush=True)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Track usage
            self.total_input_tokens += response.usage.input_tokens
            self.total_output_tokens += response.usage.output_tokens
            cost = self.calculate_cost()
            print(f"API usage: {response.usage.input_tokens} input + {response.usage.output_tokens} output tokens = ${cost:.4f}", flush=True)

            # Extract JSON from response
            response_text = response.content[0].text

            # Find JSON array in response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                keywords_data = json.loads(json_match.group())

                print(f"Generated {len(keywords_data)} keywords with conversion focus", flush=True)
                return keywords_data
            else:
                raise Exception("Could not parse keywords from Claude response")

        except Exception as e:
            print(f"Error generating keywords: {e}", flush=True)
            raise

    def calculate_cost(self) -> float:
        """Calculate total cost based on token usage."""
        if self.model not in self.MODEL_COSTS:
            return 0.0

        costs = self.MODEL_COSTS[self.model]
        input_cost = (self.total_input_tokens / 1_000_000) * costs['input']
        output_cost = (self.total_output_tokens / 1_000_000) * costs['output']
        return input_cost + output_cost

    def check_existing_keywords(self, keywords: List[str], customer_id: str) -> Dict[str, Dict]:
        """
        Check which keywords already exist in account using GAQL.

        Returns dict mapping keyword -> {'exists': bool, 'ad_group': str, 'match_type': str}

        TODO: Replace with real MCP tool call once activated (Dec 15)
        """
        # Placeholder - will be replaced with actual MCP call
        print(f"Checking {len(keywords)} keywords against account {customer_id}...", flush=True)

        # TODO: Use mcp__google-ads__run_gaql to query:
        # SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
        # FROM keyword_view
        # WHERE ad_group_criterion.keyword.text IN (keywords)

        # Mock response for now
        return {}

    def check_pmax_search_terms(self, keywords: List[str], customer_id: str) -> Dict[str, Dict]:
        """
        Check which keywords appear in PMax search terms with conversions.

        Returns dict mapping keyword -> {'covered': bool, 'campaign': str, 'conversions': int}

        TODO: Replace with real MCP tool call once activated (Dec 15)
        """
        # Placeholder - will be replaced with actual MCP call
        print(f"Checking keywords against PMax search terms...", flush=True)

        # TODO: Use mcp__google-ads__run_gaql to query:
        # SELECT campaign.name, search_term_view.search_term, metrics.conversions
        # FROM search_term_view
        # WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        # AND search_term_view.search_term IN (keywords)

        # Mock response for now
        return {}

    def get_search_volume(self, keywords: List[str], customer_id: str) -> Dict[str, int]:
        """
        Get search volume estimates using Keyword Planner.

        Returns dict mapping keyword -> monthly search volume

        TODO: Replace with real MCP tool call once activated (Dec 15)
        """
        # Placeholder - will be replaced with actual MCP call
        print(f"Getting search volume for {len(keywords)} keywords...", flush=True)

        # TODO: Use mcp__google-ads__run_keyword_planner

        # Mock response for now
        return {kw: 1000 for kw in keywords}

    def deduplicate_and_score(
        self,
        generated_keywords: List[Dict],
        customer_id: str = None
    ) -> Dict:
        """
        Deduplicate keywords and return with filtering stats.

        Returns:
        {
            'keywords': [filtered keyword dicts],
            'stats': {
                'total_generated': int,
                'filtered_existing': int,
                'filtered_pmax': int,
                'returned': int
            }
        }
        """
        keyword_texts = [kw['keyword'] for kw in generated_keywords]

        stats = {
            'total_generated': len(generated_keywords),
            'filtered_existing': 0,
            'filtered_pmax': 0,
            'returned': 0
        }

        if customer_id:
            # Check against existing keywords
            existing = self.check_existing_keywords(keyword_texts, customer_id)

            # Check against PMax search terms
            pmax_terms = self.check_pmax_search_terms(keyword_texts, customer_id)

            # Get search volume
            volumes = self.get_search_volume(keyword_texts, customer_id)

            # Filter out duplicates
            filtered_keywords = []
            for kw_dict in generated_keywords:
                kw = kw_dict['keyword']

                # Skip if exists in account
                if kw in existing and existing[kw]['exists']:
                    stats['filtered_existing'] += 1
                    continue

                # Skip if well-covered by PMax with conversions
                if kw in pmax_terms and pmax_terms[kw].get('conversions', 0) > 5:
                    stats['filtered_pmax'] += 1
                    continue

                # Add search volume to keyword dict
                kw_dict['search_volume'] = volumes.get(kw, 0)
                filtered_keywords.append(kw_dict)
        else:
            # No deduplication without customer_id
            filtered_keywords = generated_keywords

        stats['returned'] = len(filtered_keywords)

        return {
            'keywords': filtered_keywords,
            'stats': stats
        }

    def generate_and_deduplicate(self, customer_id: str = None, max_keywords: int = 25) -> Dict:
        """
        Full workflow: Generate keywords → Deduplicate → Return with stats.

        This is the main entry point for the API endpoint.
        """
        # Generate keywords with Claude
        generated = self.generate_keywords(max_keywords=max_keywords)

        # Deduplicate and score
        result = self.deduplicate_and_score(generated, customer_id)

        # Add cost tracking
        cost = self.calculate_cost()
        result['stats']['cost'] = cost
        result['stats']['model'] = self.model
        result['stats']['input_tokens'] = self.total_input_tokens
        result['stats']['output_tokens'] = self.total_output_tokens

        print(f"\nKeyword Generation Complete:", flush=True)
        print(f"  Generated: {result['stats']['total_generated']}", flush=True)
        print(f"  Filtered (existing): {result['stats']['filtered_existing']}", flush=True)
        print(f"  Filtered (PMax): {result['stats']['filtered_pmax']}", flush=True)
        print(f"  Returned: {result['stats']['returned']}", flush=True)
        print(f"  Model: {self.model}", flush=True)
        print(f"  Cost: ${cost:.4f}", flush=True)

        return result
