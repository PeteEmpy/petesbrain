#!/usr/bin/env python3
"""
Deep Website Analyzer
Analyzes entire website to understand brand, voice, products, and value proposition.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from typing import Dict, List, Set
import time


class WebsiteAnalyzer:
    """Deep analysis of a website to understand brand and create compelling ad copy."""

    def __init__(self, url: str):
        self.base_url = url
        self.domain = urlparse(url).netloc
        self.visited_pages = set()
        self.max_pages = 5  # Limit to avoid taking too long

        # Comprehensive site data
        self.all_text = []
        self.headings = {"h1": [], "h2": [], "h3": []}
        self.lists = []
        self.meta_descriptions = []
        self.page_titles = []

        # Analyzed insights
        self.brand_name = ""
        self.product_category = ""
        self.main_products = []
        self.key_benefits = []
        self.technical_features = []
        self.value_propositions = []
        self.tone_indicators = []
        self.target_audience_hints = []

    def analyze_site(self):
        """Perform deep analysis of the website."""
        print(f"Starting deep analysis of {self.base_url}...", flush=True)

        # Analyze homepage
        self._analyze_page(self.base_url)

        # Find and analyze key pages
        key_pages = self._find_key_pages()
        for page_url in key_pages[:self.max_pages]:
            if page_url not in self.visited_pages:
                time.sleep(0.5)  # Be polite
                self._analyze_page(page_url)

        # Synthesize insights
        self._synthesize_insights()

        print(f"Analysis complete! Analyzed {len(self.visited_pages)} pages.", flush=True)
        print(f"Found {len(self.main_products)} products", flush=True)
        print(f"Identified {len(self.key_benefits)} key benefits", flush=True)
        print(f"Extracted {len(self.technical_features)} technical features", flush=True)

    def _analyze_page(self, url: str):
        """Analyze a single page."""
        if url in self.visited_pages:
            return

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            self.visited_pages.add(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove noise
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()

            # Extract structured data
            self._extract_titles(soup)
            self._extract_headings(soup)
            self._extract_lists(soup)
            self._extract_paragraphs(soup)
            self._extract_meta(soup)

        except Exception as e:
            print(f"Error analyzing {url}: {e}", flush=True)

    def _extract_titles(self, soup):
        """Extract page title."""
        title = soup.find('title')
        if title:
            self.page_titles.append(title.get_text().strip())

    def _extract_headings(self, soup):
        """Extract all headings."""
        for tag in ['h1', 'h2', 'h3']:
            headings = soup.find_all(tag)
            self.headings[tag].extend([h.get_text().strip() for h in headings if h.get_text().strip()])

    def _extract_lists(self, soup):
        """Extract list items (often contain features/benefits)."""
        items = soup.find_all('li')
        self.lists.extend([item.get_text().strip() for item in items if item.get_text().strip() and len(item.get_text().strip()) > 10])

    def _extract_paragraphs(self, soup):
        """Extract paragraph text."""
        paragraphs = soup.find_all('p')
        self.all_text.extend([p.get_text().strip() for p in paragraphs if p.get_text().strip() and len(p.get_text().strip()) > 20])

    def _extract_meta(self, soup):
        """Extract meta descriptions."""
        meta = soup.find('meta', attrs={'name': 'description'})
        if not meta:
            meta = soup.find('meta', attrs={'property': 'og:description'})
        if meta and meta.get('content'):
            self.meta_descriptions.append(meta.get('content').strip())

    def _find_key_pages(self) -> List[str]:
        """Find important pages to analyze (About, Products, etc.)."""
        try:
            response = requests.get(self.base_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            keywords = ['about', 'product', 'shop', 'service', 'what-we-do', 'our-products']

            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_url = urljoin(self.base_url, href)

                # Only analyze pages on same domain
                if urlparse(full_url).netloc == self.domain:
                    # Prioritize key pages
                    if any(keyword in full_url.lower() or keyword in link.get_text().lower() for keyword in keywords):
                        if full_url not in links:
                            links.append(full_url)

            return links[:5]  # Limit to 5 additional pages
        except:
            return []

    def _synthesize_insights(self):
        """Analyze collected data to extract insights."""
        # Identify brand name
        if self.page_titles:
            title_parts = re.split(r'[|\-–]', self.page_titles[0])
            self.brand_name = title_parts[-1].strip() if len(title_parts) > 1 else title_parts[0].strip()

        # Extract products from headings
        all_headings = self.headings['h1'] + self.headings['h2'] + self.headings['h3']
        self.main_products = [h for h in all_headings if len(h) > 10 and len(h) < 60][:15]

        # Identify benefits (keywords that indicate benefits)
        benefit_keywords = [
            'relief', 'comfort', 'support', 'help', 'ease', 'sooth', 'relax',
            'improve', 'reduce', 'prevent', 'natural', 'safe', 'effective',
            'fast', 'quick', 'easy', 'simple', 'convenient', 'affordable',
            'quality', 'premium', 'best', 'guaranteed', 'free'
        ]

        all_content = ' '.join(self.lists + self.all_text + all_headings).lower()

        for keyword in benefit_keywords:
            # Find sentences containing benefit keywords
            for text in self.lists + self.all_text:
                if keyword in text.lower() and len(text) < 150:
                    if text not in self.key_benefits:
                        self.key_benefits.append(text)
                        if len(self.key_benefits) >= 15:
                            break

        # Identify technical features
        tech_keywords = [
            'made', 'designed', 'manufactured', 'material', 'fabric',
            'size', 'weight', 'dimension', 'specification', 'certified',
            'tested', 'approved', 'standard', 'grade', 'quality'
        ]

        for keyword in tech_keywords:
            for text in self.lists + self.all_text:
                if keyword in text.lower() and len(text) < 150:
                    if text not in self.technical_features:
                        self.technical_features.append(text)
                        if len(self.technical_features) >= 15:
                            break

        # Extract value propositions from meta descriptions
        self.value_propositions = self.meta_descriptions[:3]

        # Analyze tone (look for emotional/personality words)
        tone_words = {
            'warm': ['warm', 'cozy', 'comfort', 'soothing', 'gentle'],
            'professional': ['professional', 'expert', 'quality', 'premium', 'certified'],
            'friendly': ['love', 'happy', 'enjoy', 'wonderful', 'amazing'],
            'trustworthy': ['trust', 'reliable', 'guaranteed', 'safe', 'secure'],
            'innovative': ['innovative', 'unique', 'new', 'advanced', 'modern']
        }

        for tone, words in tone_words.items():
            if any(word in all_content for word in words):
                self.tone_indicators.append(tone)

    def get_insights_summary(self) -> Dict:
        """Get summary of all insights."""
        return {
            'brand_name': self.brand_name,
            'product_category': self.product_category,
            'main_products': self.main_products[:10],
            'key_benefits': self.key_benefits[:10],
            'technical_features': self.technical_features[:10],
            'value_propositions': self.value_propositions,
            'tone_indicators': self.tone_indicators,
            'all_headings': (self.headings['h1'] + self.headings['h2'])[:20]
        }


if __name__ == "__main__":
    # Test
    analyzer = WebsiteAnalyzer("https://wheatybags.co.uk/")
    analyzer.analyze_site()

    insights = analyzer.get_insights_summary()
    print("\n" + "="*80)
    print("INSIGHTS SUMMARY")
    print("="*80)
    for key, value in insights.items():
        print(f"\n{key.upper().replace('_', ' ')}:")
        if isinstance(value, list):
            for item in value[:5]:
                print(f"  - {item}")
        else:
            print(f"  {value}")
