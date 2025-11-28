#!/usr/bin/env python3
"""
Ad Copy Generator V2 - Content-First Approach
Uses ACTUAL page content extensively, not generic templates.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, List
import random


class AdCopyGenerator:
    """Generates ad copy based heavily on actual website content."""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.content = ""
        self.soup = None
        self.product_info = {}
        self.product_name = ""
        self.category = ""
        self.all_phrases = []  # All usable phrases from the page

    def fetch_url_content(self) -> bool:
        """Fetch and parse URL content."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            self.content = response.text
            self.soup = BeautifulSoup(self.content, 'html.parser')

            # Remove script and style elements
            for script in self.soup(["script", "style"]):
                script.decompose()

            return True
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return False

    def extract_page_info(self) -> Dict:
        """Extract ALL useful information from the page."""
        if not self.soup:
            return {}

        info = {
            "title": "",
            "description": "",
            "h1": [],
            "h2": [],
            "h3": [],
            "keywords": [],
            "brand": "",
            "text_content": "",
            "lists": [],
            "strong_text": [],
            "all_text_phrases": []
        }

        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            info["title"] = title_tag.get_text().strip()
            title_parts = re.split(r'[|\-–]', info["title"])
            if title_parts:
                self.product_name = title_parts[0].strip()

        # Meta description
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = self.soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            info["description"] = meta_desc.get('content').strip()

        # Extract brand from domain
        domain_parts = self.domain.split('.')
        if len(domain_parts) >= 2:
            brand_part = domain_parts[-2]
            # Clean up the brand name
            info["brand"] = brand_part.replace('-', ' ').replace('_', ' ').title()

        # H1 tags - USE ALL OF THEM
        h1_tags = self.soup.find_all('h1')
        info["h1"] = [self._clean_text(h1.get_text()) for h1 in h1_tags[:10]]

        # H2 tags - USE ALL OF THEM
        h2_tags = self.soup.find_all('h2')
        info["h2"] = [self._clean_text(h2.get_text()) for h2 in h2_tags[:20]]

        # H3 tags - USE ALL OF THEM
        h3_tags = self.soup.find_all('h3')
        info["h3"] = [self._clean_text(h3.get_text()) for h3 in h3_tags[:20]]

        # Get main text content
        paragraphs = self.soup.find_all('p')
        text_content = ' '.join([p.get_text().strip() for p in paragraphs[:30]])
        info["text_content"] = text_content[:3000]

        # Extract ALL list items
        list_items = self.soup.find_all('li')
        info["lists"] = [self._clean_text(li.get_text()) for li in list_items[:30]]

        # Extract ALL strong/bold text
        strong_tags = self.soup.find_all(['strong', 'b'])
        info["strong_text"] = [self._clean_text(s.get_text()) for s in strong_tags[:20]]

        self.product_info = info
        self._extract_all_phrases()
        self.category = self._get_category()

        return info

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special chars but keep essential punctuation
        text = re.sub(r'[^\w\s&\-\',]', '', text)
        return text.strip()

    def _extract_all_phrases(self):
        """Extract ALL usable phrases from page content."""
        phrases = []
        info = self.product_info

        # Add title parts
        if info.get("title"):
            phrases.append(info["title"])
            # Split title by separators
            for part in re.split(r'[|\-–]', info["title"]):
                if part.strip() and len(part.strip()) > 3:
                    phrases.append(part.strip())

        # Add meta description (split into sentences)
        if info.get("description"):
            phrases.append(info["description"])
            for sentence in info["description"].split('.'):
                if sentence.strip() and len(sentence.strip()) > 10:
                    phrases.append(sentence.strip())

        # Add ALL headings
        phrases.extend(info.get("h1", []))
        phrases.extend(info.get("h2", []))
        phrases.extend(info.get("h3", []))

        # Add lists
        phrases.extend(info.get("lists", []))

        # Add strong text
        phrases.extend(info.get("strong_text", []))

        # Clean and deduplicate
        cleaned_phrases = []
        seen = set()
        for phrase in phrases:
            if phrase and len(phrase) > 5 and len(phrase) < 150:
                phrase_lower = phrase.lower()
                if phrase_lower not in seen:
                    seen.add(phrase_lower)
                    cleaned_phrases.append(phrase)

        self.all_phrases = cleaned_phrases
        print(f"Extracted {len(self.all_phrases)} unique phrases from page", flush=True)

    def generate_rsa_headlines(self) -> Dict[str, List[str]]:
        """Generate headlines using ACTUAL page content."""
        info = self.product_info
        brand = info.get("brand", "")

        headlines = {
            "benefits": [],
            "technical": [],
            "quirky": [],
            "cta": [],
            "brand": []
        }

        # BENEFITS - Use phrases that sound like benefits
        benefit_words = ['for', 'relief', 'comfort', 'support', 'help', 'ease', 'sooth', 'relax', 'warm', 'hot', 'cold', 'pain']
        for phrase in self.all_phrases[:30]:
            if any(word in phrase.lower() for word in benefit_words):
                headline = self._trim_to_length(phrase, 30)
                if headline and len(headline) > 10:
                    headlines["benefits"].append(headline)
                    if len(headlines["benefits"]) >= 10:
                        break

        # Fill remaining with title/H1 variations
        while len(headlines["benefits"]) < 10:
            if info.get("h1") and headlines["benefits"].count(info["h1"][0][:30]) == 0:
                headlines["benefits"].append(self._trim_to_length(info["h1"][0], 30))
            elif info.get("h2"):
                for h2 in info["h2"]:
                    h = self._trim_to_length(h2, 30)
                    if h and h not in headlines["benefits"]:
                        headlines["benefits"].append(h)
                        break
            else:
                headlines["benefits"].append(self._trim_to_length(f"{self.product_name} Products", 30))
                break

        # TECHNICAL - Use descriptive phrases about what it is
        tech_words = ['made', 'designed', 'manufactured', 'original', 'traditional', 'shaped', 'size', 'material', 'fabric']
        for phrase in self.all_phrases[:30]:
            if any(word in phrase.lower() for word in tech_words):
                headline = self._trim_to_length(phrase, 30)
                if headline and len(headline) > 10:
                    headlines["technical"].append(headline)
                    if len(headlines["technical"]) >= 10:
                        break

        # Fill with H2s
        while len(headlines["technical"]) < 10:
            if info.get("h2") and len(headlines["technical"]) < len(info["h2"]):
                h2 = info["h2"][len(headlines["technical"])]
                headlines["technical"].append(self._trim_to_length(h2, 30))
            else:
                headlines["technical"].append(self._trim_to_length(self.product_name, 30))
                break

        # QUIRKY - Use interesting combinations
        quirky_templates = [
            f"{self.product_name} Magic",
            f"Love {self.product_name}",
            f"{self.product_name} For You",
            f"Perfect {self.product_name}",
            f"Best {self.product_name} Ever",
            f"Amazing {self.product_name}",
            f"Top {self.product_name} Choice",
            f"{self.product_name} Heaven",
            f"Ultimate {self.product_name}",
            f"{self.product_name} Dreams"
        ]
        for template in quirky_templates:
            headlines["quirky"].append(self._trim_to_length(template, 30))
            if len(headlines["quirky"]) >= 10:
                break

        # CTA - Action-oriented with product name
        cta_templates = [
            f"Shop {self.product_name} Now",
            f"Buy {self.product_name} Today",
            f"Order {self.product_name}",
            f"Get {self.product_name}",
            f"Discover {self.product_name}",
            f"Find Your {self.product_name}",
            f"Browse {self.product_name}",
            f"Choose {self.product_name}",
            f"Try {self.product_name}",
            f"Explore {self.product_name}"
        ]
        for template in cta_templates:
            headlines["cta"].append(self._trim_to_length(template, 30))
            if len(headlines["cta"]) >= 10:
                break

        # BRAND - Use brand and product combinations
        if brand:
            brand_templates = [
                f"{brand} {self.category}",
                f"Official {brand} Shop",
                f"{brand} Store",
                f"{brand} Products",
                f"Buy {brand}",
                f"{brand} UK",
                f"{brand} Collection",
                f"{brand} Range",
                f"{brand} Quality",
                f"Choose {brand}"
            ]
        else:
            brand_templates = [
                self._trim_to_length(self.product_name, 30),
                f"{self.category} Shop",
                f"{self.category} Store",
                f"Buy {self.category}",
                f"{self.category} UK",
                f"Quality {self.category}",
                f"{self.category} Range",
                f"Best {self.category}",
                f"Top {self.category}",
                f"{self.category} Experts"
            ]

        for template in brand_templates:
            headlines["brand"].append(self._trim_to_length(template, 30))
            if len(headlines["brand"]) >= 10:
                break

        return headlines

    def generate_rsa_descriptions(self) -> Dict[str, List[str]]:
        """Generate descriptions using ACTUAL page content."""
        info = self.product_info
        brand = info.get("brand", "")
        description = info.get("description", "")

        descriptions = {
            "benefits": [],
            "technical": [],
            "quirky": [],
            "cta": [],
            "brand": []
        }

        # BENEFITS - Use meta description and benefit-focused phrases
        if description:
            descriptions["benefits"].append(self._trim_to_length(description, 90))

        for phrase in self.all_phrases[:40]:
            if len(phrase) > 30 and len(phrase) < 100:
                desc = self._trim_to_length(phrase, 90)
                if desc and desc not in descriptions["benefits"]:
                    descriptions["benefits"].append(desc)
                    if len(descriptions["benefits"]) >= 10:
                        break

        # Fill remaining
        while len(descriptions["benefits"]) < 10:
            desc = f"{self.product_name}. {info.get('h1', [self.product_name])[0]}. Shop now."
            descriptions["benefits"].append(self._trim_to_length(desc, 90))
            break

        # TECHNICAL - Product-specific details
        for h2 in info.get("h2", [])[:10]:
            if len(h2) > 20:
                desc = f"{h2}. Quality products from {brand if brand else 'trusted suppliers'}."
                descriptions["technical"].append(self._trim_to_length(desc, 90))
                if len(descriptions["technical"]) >= 10:
                    break

        while len(descriptions["technical"]) < 10:
            desc = f"{self.product_name}. {info.get('title', '')}."
            descriptions["technical"].append(self._trim_to_length(desc, 90))
            break

        # QUIRKY - Engaging descriptions
        quirky_templates = [
            f"Discover why everyone loves {self.product_name}. Shop our full range today.",
            f"{self.product_name} that make a difference. Experience quality you can feel.",
            f"The {self.product_name} you've been searching for. Browse our collection now.",
            f"Transform your experience with {self.product_name}. Trusted by thousands.",
            f"Premium {self.product_name} at great prices. Free UK delivery available.",
            f"Why settle for less? Choose {self.product_name} for guaranteed satisfaction.",
            f"{self.product_name} made easy. Browse, choose, and enjoy. Simple as that.",
            f"Join thousands who've switched to {self.product_name}. See the difference.",
            f"Your search for perfect {self.product_name} ends here. Quality guaranteed.",
            f"Experience the {self.product_name} difference. Shop with confidence today."
        ]
        for template in quirky_templates[:10]:
            descriptions["quirky"].append(self._trim_to_length(template, 90))

        # CTA - Action-focused with product specifics
        cta_templates = [
            f"Shop {self.product_name} now. Free UK delivery. Easy returns. Order today.",
            f"Buy {self.product_name} with confidence. Quality guaranteed. Fast dispatch.",
            f"Order {self.product_name} today. Trusted by thousands. Secure checkout.",
            f"Get your {self.product_name} delivered fast. Shop now for best selection.",
            f"Browse {self.product_name} range. Expert advice available. Order online now.",
            f"Discover {self.product_name} collection. Premium quality. Great prices. Shop now.",
            f"Find your perfect {self.product_name}. Easy ordering. Fast delivery. Buy today.",
            f"Choose from our {self.product_name} range. Secure payment. Quick dispatch.",
            f"Explore {self.product_name} options. Quality products. Competitive prices. Order now.",
            f"Try {self.product_name} risk-free. Money-back guarantee. Shop with confidence."
        ]
        for template in cta_templates[:10]:
            descriptions["cta"].append(self._trim_to_length(template, 90))

        # BRAND - Company/product focused
        if brand:
            brand_templates = [
                f"{brand} - Your trusted source for {self.product_name}. Quality guaranteed.",
                f"Discover the {brand} difference. Premium {self.product_name} for everyone.",
                f"Official {brand} store. {self.product_name} delivered direct. Shop now.",
                f"{brand} delivers quality {self.product_name}. Trusted by thousands. Order today.",
                f"Choose {brand} for {self.product_name}. Expert service. Fast delivery.",
                f"{brand} - Where quality meets value. Premium {self.product_name} at great prices.",
                f"Trust {brand} for your {self.product_name} needs. Satisfaction guaranteed.",
                f"{brand} brings you the best {self.product_name}. Shop our full range.",
                f"Experience {brand} quality. {self.product_name} that deliver results.",
                f"{brand} - Your {self.product_name} specialists. Browse our collection now."
            ]
        else:
            brand_templates = [
                f"Your trusted source for {self.product_name}. Quality guaranteed. Shop now.",
                f"Discover premium {self.product_name}. Trusted by thousands. Order today.",
                f"Official store for {self.product_name}. Quality products delivered direct.",
                f"Quality {self.product_name} at great prices. Fast delivery. Shop with confidence.",
                f"Expert {self.product_name} specialists. Browse our full range today.",
                f"Premium {self.product_name} that deliver. Satisfaction guaranteed. Buy now.",
                f"Your {self.product_name} experts. Professional service. Competitive prices.",
                f"Trusted {self.product_name} supplier. Quality products. Fast dispatch.",
                f"Experience quality {self.product_name}. Shop our complete collection now.",
                f"{self.product_name} specialists. Expert advice. Secure ordering. Shop today."
            ]

        for template in brand_templates[:10]:
            descriptions["brand"].append(self._trim_to_length(template, 90))

        return descriptions

    def _get_category(self) -> str:
        """Extract or infer the product category from page content."""
        url_lower = self.url.lower()
        title_lower = self.product_info.get("title", "").lower()
        desc_lower = self.product_info.get("description", "").lower()
        all_text = f"{url_lower} {title_lower} {desc_lower} {' '.join(self.all_phrases)}".lower()

        categories = {
            "bag": "Bags", "bags": "Bags",
            "heat": "Heat Products", "heating": "Heating Products",
            "bottle": "Bottles", "bottles": "Bottles",
            "wheat": "Wheat Products",
            "shoes": "Footwear", "shoe": "Footwear",
            "clothing": "Clothing", "clothes": "Clothing",
            "fashion": "Fashion", "apparel": "Apparel",
            "tech": "Technology", "electronic": "Electronics",
            "software": "Software", "app": "Software",
            "food": "Food", "restaurant": "Dining",
            "home": "Home", "furniture": "Furniture",
            "sport": "Sports", "fitness": "Fitness",
            "health": "Health", "beauty": "Beauty",
            "jewelry": "Jewelry", "watch": "Watches",
            "toy": "Toys", "game": "Games",
            "book": "Books", "music": "Music",
        }

        for keyword, category in categories.items():
            if keyword in all_text:
                return category

        # If no match, use product name
        if self.product_name and len(self.product_name) < 25:
            return self.product_name

        return "Products"

    def _trim_to_length(self, text: str, max_length: int) -> str:
        """Trim text to maximum length, cutting at word boundary."""
        if not text:
            return ""

        if len(text) <= max_length:
            return text

        # Cut at last space before max_length
        trimmed = text[:max_length]
        last_space = trimmed.rfind(' ')
        if last_space > max_length * 0.7:
            trimmed = trimmed[:last_space]

        return trimmed

    def generate_complete_rsa(self) -> Dict:
        """Generate complete RSA ad set."""
        if not self.product_info:
            self.extract_page_info()

        return {
            "url": self.url,
            "page_info": self.product_info,
            "headlines": self.generate_rsa_headlines(),
            "descriptions": self.generate_rsa_descriptions()
        }
