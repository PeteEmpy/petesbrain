#!/usr/bin/env python3
"""
Claude API Copywriter
Uses Claude AI to analyze websites and write professional ad copy.
This gives you the same quality as using Claude directly.
"""

import os
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
import json
import re
from typing import Dict
from pathlib import Path


class ClaudeCopywriter:
    """Professional copywriter powered by Claude AI."""

    def __init__(self, url: str):
        self.url = url
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=self.api_key)

    def _load_rok_specs(self) -> str:
        """Load ROK specifications from the text file."""
        try:
            import os
            spec_path = os.path.join(os.path.dirname(__file__), 'ROK _ Google Ads Text Asset Generation.txt')

            if os.path.exists(spec_path):
                with open(spec_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "ROK specifications not found - use best practices for Google Ads RSA copy."
        except Exception as e:
            print(f"Warning: Could not load ROK specs: {e}", flush=True)
            return "Use Google Ads best practices for RSA copy."

    def _load_specs_from_kb(self) -> Dict:
        """Load Performance Max specifications from the Google Specifications KB."""
        try:
            project_root = Path(__file__).parent.parent.parent
            specs_file = project_root / "google-specifications" / "google-ads" / "specifications" / "asset-groups" / "performance-max.json"
            
            if specs_file.exists():
                with open(specs_file, 'r') as f:
                    data = json.load(f)
                    spec_content = data.get("specification", {}).get("content", {})
                    
                    # Format for use in prompts
                    specs_text = f"""
Performance Max Asset Specifications (from Google Specifications KB):
- Short Headlines: {spec_content.get('short_headlines', {}).get('min_length', 25)}-{spec_content.get('short_headlines', {}).get('max_length', 30)} chars, Target: {spec_content.get('short_headlines', {}).get('target_length', '27-30')}, Required: {spec_content.get('short_headlines', {}).get('required_count', 50)}
- Long Headlines: {spec_content.get('long_headlines', {}).get('min_length', 80)}-{spec_content.get('long_headlines', {}).get('max_length', 90)} chars, Target: {spec_content.get('long_headlines', {}).get('target_length', '82-90')}, Required: {spec_content.get('long_headlines', {}).get('required_count', 25)}
- Descriptions: {spec_content.get('descriptions', {}).get('min_length', 80)}-{spec_content.get('descriptions', {}).get('max_length', 90)} chars, Target: {spec_content.get('descriptions', {}).get('target_length', '82-90')}, Required: {spec_content.get('descriptions', {}).get('required_count', 25)}
- Sitelinks: {spec_content.get('sitelinks', {}).get('count', {}).get('min', 4)}-{spec_content.get('sitelinks', {}).get('count', {}).get('max', 6)} required
- Callouts: {spec_content.get('callouts', {}).get('count', {}).get('min', 8)}-{spec_content.get('callouts', {}).get('count', {}).get('max', 10)} required, Max {spec_content.get('callouts', {}).get('max_length', 25)} chars each

Source: {data.get('specification', {}).get('sources', [{}])[0].get('type', 'unknown') if data.get('specification', {}).get('sources') else 'unknown'}
Last Updated: {data.get('specification', {}).get('last_updated', 'Unknown')}
"""
                    return {"specs_text": specs_text, "spec_content": spec_content}
            return {}
        except Exception as e:
            print(f"Warning: Could not load specs from KB: {e}", flush=True)
            return {}

    def fetch_website_content(self) -> str:
        """Fetch and extract clean text content from the website."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove scripts, styles, and navigation
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()

            # Extract text content
            title = soup.find('title')
            title_text = title.get_text() if title else ""

            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                       soup.find('meta', attrs={'property': 'og:description'})
            meta_text = meta_desc.get('content', '') if meta_desc else ""

            # Get main content - extract MORE to capture tone of voice
            h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')[:8]]
            h2_tags = [h2.get_text().strip() for h2 in soup.find_all('h2')[:20]]
            h3_tags = [h3.get_text().strip() for h3 in soup.find_all('h3')[:15]]
            paragraphs = [p.get_text().strip() for p in soup.find_all('p')[:35] if len(p.get_text().strip()) > 30]
            list_items = [li.get_text().strip() for li in soup.find_all('li')[:40] if len(li.get_text().strip()) > 15]

            # Get button text (often reveals tone and CTAs)
            buttons = [btn.get_text().strip() for btn in soup.find_all(['button', 'a']) if btn.get_text().strip() and len(btn.get_text().strip()) < 50]
            buttons = list(set(buttons))[:10]  # Dedupe and limit

            # Combine into clean content
            content = f"""
URL: {self.url}

TITLE: {title_text}

META DESCRIPTION: {meta_text}

MAIN HEADINGS (H1):
{chr(10).join('- ' + h for h in h1_tags if h)}

SECTION HEADINGS (H2):
{chr(10).join('- ' + h for h in h2_tags if h)}

SUB-HEADINGS (H3):
{chr(10).join('- ' + h for h in h3_tags if h)}

BUTTONS/CALLS TO ACTION:
{chr(10).join('- ' + btn for btn in buttons if btn)}

KEY POINTS/FEATURES:
{chr(10).join('- ' + item for item in list_items[:20] if item)}

MAIN BODY CONTENT (study the language style, tone, and word choices):
{chr(10).join(paragraphs[:15])}
"""
            return content.strip()

        except Exception as e:
            raise Exception(f"Failed to fetch website: {str(e)}")

    def generate_ad_copy(self, additional_context: str = "", main_keyword: str = "", social_proof_reviews: list = None) -> Dict:
        """Use Claude AI to analyze the website and generate professional ad copy.

        Args:
            additional_context: Additional user-provided context
            main_keyword: Primary keyword to target in ad copy
            social_proof_reviews: List of 2 recent customer reviews for social proof headlines
        """

        print("Fetching website content...", flush=True)
        website_content = self.fetch_website_content()

        # Default to empty list if no reviews provided
        if social_proof_reviews is None:
            social_proof_reviews = []

        # Load ROK specifications
        print("Loading ROK specifications...", flush=True)
        rok_specs = self._load_rok_specs()
        
        # Load specs from KB
        kb_specs = self._load_specs_from_kb()
        kb_specs_text = kb_specs.get("specs_text", "") if kb_specs else ""

        print("Sending to Claude AI for professional copywriting...", flush=True)

        # Build context section if provided
        context_section = ""
        context_reminder = ""
        if additional_context:
            context_section = f"""

═══════════════════════════════════════════════════════════════════
🔴 CRITICAL: USER-PROVIDED CONTEXT (READ THIS FIRST!)
═══════════════════════════════════════════════════════════════════

{additional_context}

⚠️ IMPORTANT: The above context is PROVIDED BY THE USER and must take precedence.
   - If context mentions target audience, write for THAT audience
   - If context mentions special offers, INCLUDE those in your copy
   - If context mentions brand tone, MATCH that tone exactly
   - If context mentions campaign goals, OPTIMIZE for those goals
   - If context mentions specific messaging, PRIORITIZE that messaging

This is CRITICAL context that should inform EVERY headline and description you write.

═══════════════════════════════════════════════════════════════════
"""
            context_reminder = f"""

🔴 REMINDER: Don't forget the user-provided context above! Every headline and description must consider:
{additional_context}
"""

        # Build keyword section if provided
        keyword_section = ""
        if main_keyword:
            keyword_section = f"""

═══════════════════════════════════════════════════════════════════
🎯 MAIN KEYWORD (MUST INCLUDE IN COPY)
═══════════════════════════════════════════════════════════════════

Main Keyword: "{main_keyword}"

⚠️ REQUIREMENT: You must create at least 3 headlines that include this exact keyword.
Include variations where natural (plurals, different word forms).

═══════════════════════════════════════════════════════════════════
"""

        # Build social proof section if reviews provided
        social_proof_section = ""
        if social_proof_reviews and len(social_proof_reviews) >= 2:
            social_proof_section = f"""

═══════════════════════════════════════════════════════════════════
⭐ SOCIAL PROOF - RECENT CUSTOMER REVIEWS
═══════════════════════════════════════════════════════════════════

Review 1: "{social_proof_reviews[0]}"

Review 2: "{social_proof_reviews[1]}"

⚠️ REQUIREMENT: Use these reviews to create 2 social proof headlines per section.
Extract powerful phrases, outcomes, and emotions from these reviews.

Examples of social proof headlines:
- "Customers love our [benefit from review]"
- "[Number/stat from review] customers agree"
- "[Powerful phrase from review verbatim]"

═══════════════════════════════════════════════════════════════════
"""

        prompt = f"""You are an ELITE copywriter with 20+ years experience at luxury brands like Tiffany, Hermès, and Burberry. You've written award-winning campaigns for high-end British heritage brands.

Your task: Create EXCEPTIONAL Google Ads copy that captures the exact essence of this luxury brand. This is not a rush job - take your time to craft each line with precision and care.
{context_section}
{keyword_section}
{social_proof_section}
{website_content}

ROK SPECIFICATIONS AND GUIDELINES:
{rok_specs}

{kb_specs_text}

═══════════════════════════════════════════════════════════════════
CRITICAL QUALITY STANDARDS - THIS IS YOUR PRIMARY DIRECTIVE
═══════════════════════════════════════════════════════════════════

Before you write a SINGLE word, you must:

1. Read EVERY piece of website content provided above
2. Internalize the brand's voice - how they speak, what words they choose
3. Understand their customers - who buys £200 leather notebooks?
4. Study their heritage and positioning - what makes them special?
5. Note specific product features, materials, craftsmanship details

THEN and ONLY THEN can you begin writing.

═══════════════════════════════════════════════════════════════════
STEP 1: DEEP BRAND ANALYSIS (This is not optional - do this thoroughly):

A) TONE OF VOICE ANALYSIS - Study how this brand communicates:
   - What is the formality level? (Professional/casual/friendly/authoritative)
   - What emotional tone do they use? (Warm/clinical/energetic/calm/playful)
   - What language style? (Simple/technical/poetic/direct/conversational)
   - Look at their actual word choices, sentence structure, personality
   - Are they serious or do they use humor? What kind?
   - Do they use questions, exclamations, or statements?
   - CRITICAL: Your ad copy MUST sound like it was written by the same person who wrote this website

B) TARGET AUDIENCE ANALYSIS - Who is actually buying this?
   - Demographics: Age range, gender, income level, location
   - Psychographics: What are their values, lifestyle, priorities?
   - Pain points: What problem are they trying to solve? What keeps them up at night?
   - Motivations: Why would they choose THIS product/service over competitors?
   - Language they use: How do THEY talk about their problem/need?
   - Decision triggers: What would make them click and buy NOW?
   - CRITICAL: Write as if you're talking directly to ONE specific person in this audience

C) BRAND POSITIONING:
   - What makes this brand different from competitors?
   - What's their unique value proposition?
   - What do they emphasize most on their website?
   - What customer benefits do they lead with?

═══════════════════════════════════════════════════════════════════
STEP 2: CRAFT 50 EXCEPTIONAL HEADLINES (10 per section)
═══════════════════════════════════════════════════════════════════
{context_reminder}
CHARACTER REQUIREMENTS - STRICTLY ENFORCED:
   ⚠ MAXIMUM: 30 characters (HARD LIMIT - Google will reject anything over 30)
   ⚠ TARGET: 27-30 characters (REQUIRED - anything under 25 chars will be rejected)
   ⚠ MINIMUM ACCEPTABLE: 25 characters (but aim for 27-30)

   🚨 CRITICAL: Headlines under 25 characters will be AUTOMATICALLY REJECTED 🚨

   Goal: Use the FULL 27-30 character space for maximum impact.
   Don't waste valuable ad space - every character counts!

CAPITALIZATION - MANDATORY (ROK Standard, Nov 2025):
   ✓ USE SENTENCE CASE for all headlines
   ✓ Capitalize ONLY the first word and proper nouns (brand names, place names)
   ✓ Keep all other words lowercase

   Examples:
   ✓ CORRECT: "Handcrafted leather diaries" (sentence case)
   ✓ CORRECT: "Shop Smythson Christmas gifts" (sentence case, brand name capitalized)
   ✗ WRONG: "Handcrafted Leather Diaries" (title case - do not use)
   ✗ WRONG: "HANDCRAFTED LEATHER DIARIES" (all caps - policy violation)

   Why: Research on 1M+ ads shows sentence case performs better on CTR, ROAS, and CPA
   because it looks more natural and resembles organic search results.

QUALITY STANDARDS - CRITICAL:
   ✓ MUST use ACTUAL product names, materials, and features from THIS SPECIFIC PAGE
   ✓ MUST reference REAL details from the website content above (not generic placeholders)
   ✓ Look at the H1, H2, H3 tags - use those EXACT product names and categories
   ✓ Look at the paragraphs - extract REAL features, materials, specifications
   ✓ If the page mentions specific sizes, colors, materials, prices, or offers - USE THEM
   ✓ Each headline must sound like it came from THIS brand's copywriters
   ✓ No generic phrases - every line should be unique to THIS page
   ✓ Match the sophistication level - luxury brands don't shout
   ✓ Include numbers, heritage dates, or specific benefits where relevant

REMINDER: These are EXAMPLES only - your headlines MUST be specific to the page you're analyzing!

GOOD HEADLINE STRUCTURE (but adapt to the actual page):
   - "[Specific Product Type] [Key Material/Feature]" (28-30 chars)
   - "[Actual Number/Date] [Real Product Category]" (28-30 chars)
   - "[Exact Brand Feature] | [Real Offer]" (28-30 chars)

BAD HEADLINES - NEVER DO THIS:
   - "Shop Now" (9) ✗ LAZY - not specific to the page!
   - "Quality Products" (17) ✗ GENERIC - could be any page!
   - "Buy Premium Goods Today" (23) ✗ VAGUE - no specific product details!

SECTIONS (10 headlines each) - WITH STRUCTURED MIX RATIOS:

   a) BENEFITS (10 headlines total):
      - 3 headlines featuring the main keyword{' "' + main_keyword + '"' if main_keyword else ' (if provided)'}
      - 2 headlines with social proof{' from customer reviews' if social_proof_reviews else ' (if reviews provided)'}
      - 3 headlines with specific benefits from website content
      - 1 headline with a compelling emotional benefit
      - 1 headline that addresses a pain point or desire

   b) TECHNICAL (10 headlines total):
      - 3 headlines featuring specific materials/craftsmanship from website
      - 2 headlines with technical specifications or features
      - 2 headlines combining technical + benefit
      - 2 headlines with product categories/types
      - 1 headline with manufacturing/origin details

   c) QUIRKY (10 headlines total):
      - 1 headline with a clever pun (sophisticated, not cheesy)
      - 3 headlines with elegant wordplay or wit
      - 3 headlines with unexpected angles or perspectives
      - 2 headlines with personality and brand character
      - 1 headline that makes the reader smile

   d) CTA (10 headlines total - MUST use imperative verbs):
      - ALL 10 headlines must start with action verbs
      - Suggested verbs: Discover, Shop, Explore, Find, Browse, Experience, Get, Order, View, Buy, Choose, Compare, See, Try, Start, Join, Learn, Book
      - 4 headlines focused on "Shop/Browse/Explore" actions
      - 3 headlines focused on "Discover/Experience/Find" actions
      - 2 headlines focused on "Order/Get/Buy" actions
      - 1 headline with urgency ("Shop now", "Order today", etc.)

   e) BRAND (10 headlines total):
      - 3 headlines featuring brand heritage/history
      - 2 headlines with brand positioning/what makes them unique
      - 2 headlines with brand values or promises
      - 2 headlines with awards, recognition, or authority
      - 1 headline with brand personality

═══════════════════════════════════════════════════════════════════
STEP 3: WRITE 50 MASTERFUL DESCRIPTIONS (10 per section)
═══════════════════════════════════════════════════════════════════
{context_reminder}
CHARACTER REQUIREMENTS - STRICTLY ENFORCED:
   ⚠ MAXIMUM: 90 characters (HARD LIMIT - Google will reject anything over 90)
   ⚠ TARGET: 82-90 characters (REQUIRED - anything under 80 chars will be rejected)
   ⚠ MINIMUM ACCEPTABLE: 80 characters (but aim for 82-90)

CAPITALIZATION - MANDATORY (ROK Standard, Nov 2025):
   ✓ USE SENTENCE CASE for all descriptions
   ✓ Capitalize ONLY the first word and proper nouns (brand names, place names)
   ✓ Keep all other words lowercase

   Examples:
   ✓ CORRECT: "Explore our collection of handcrafted leather goods made in Britain since 1887"
   ✓ CORRECT: "Shop Smythson's Christmas collection online with free UK delivery available"
   ✗ WRONG: "Explore Our Collection Of Handcrafted Leather Goods" (title case - do not use)

   Why: Sentence case performs better on CTR, ROAS, and CPA for RSAs and asset groups.

   🚨 CRITICAL: Descriptions under 80 characters will be AUTOMATICALLY REJECTED 🚨

   Goal: Use the FULL 82-90 character space for compelling, complete sentences.
   This is your chance to persuade - don't waste a single character!

WRITING STYLE - CRITICAL:
   ✓ Write as ONE COMPLETE SENTENCE - this is essential for readability
   ✓ No choppy fragments, no multiple disconnected thoughts
   ✓ Each description should be a single, elegant, flowing sentence
   ✓ Use sophisticated language: "Discover...", "Experience...", "Crafted with..."
   ✓ One cohesive message from start to finish, using full 80-90 character space
   ✓ Match the brand's actual writing style from their website

GOOD DESCRIPTION STRUCTURE - SINGLE SENTENCE:
   Write ONE complete sentence that flows naturally from beginning to end.
   Structure: [Opening hook] + [supporting detail] + [benefit/CTA], all flowing together.

   Example structure: "Discover hand-stitched Italian leather bags with lifetime warranty."
   NOT: "Premium bags. Italian leather. Shop now." (too choppy!)

REMINDER: These are EXAMPLES only - your descriptions MUST use REAL details from THIS page!

GOOD DESCRIPTION STRUCTURE (but use actual page content):
   - Start with specific product category from the page (not "products" or "items")
   - Include actual materials, sizes, features mentioned on the page
   - Reference real offers, prices, or benefits shown on the page
   - Use the exact terminology the brand uses (check H1, H2, paragraphs)

BAD DESCRIPTIONS - NEVER DO THIS:
   - "Premium products. Shop now." ✗ Could apply to ANY page!
   - "Quality items. Great prices." ✗ No specific page details!
   - Generic descriptions that don't reference THIS specific page's content

   ✓ Mirror the website's exact tone of voice
   ✓ Use their specific terminology and product names
   ✓ Include real numbers, dates, or specifications from the website
   ✓ Address what THEIR customers actually care about

═══════════════════════════════════════════════════════════════════
STEP 4: CREATE 5 WEBSITE HEADLINES (Landing Page Headlines)
═══════════════════════════════════════════════════════════════════

Now create 5 landing page headlines that match the ad headlines above.
These will be used on the website landing page to improve Quality Score and relevance.

CRITICAL REQUIREMENTS - "FOUR WORDS TO VALUE" RULE:
   ✓ Customer must understand the value within the FIRST 4 WORDS
   ✓ Use subject/predicate structure for cognitive momentum
   ✓ START with an action verb (Discover, Shop, Explore, Get, Find, etc.)
   ✓ Make the CUSTOMER the subject - use "you" language, NOT "we"
   ✓ Emphasize how EASY it is - no work implied, only value received
   ✓ Match the tone and terminology from your ad headlines above

GOOD WEBSITE HEADLINE STRUCTURE:
   - "Discover handcrafted leather goods | Free UK delivery" (value clear in "Discover handcrafted leather goods")
   - "Shop luxury diaries made in Britain since 1887" (value clear in "Shop luxury diaries made")
   - "Experience British craftsmanship | Premium leather notebooks" (value clear in "Experience British craftsmanship")

BAD WEBSITE HEADLINES (don't do this):
   - "We make premium products" (starts with "we", not customer-focused)
   - "Learn about our heritage and history" (implies work, not value)
   - "Quality goods available for purchase" (passive, no clear value)

Create 5 website headlines (no character limit, but keep under 100 chars for readability).

═══════════════════════════════════════════════════════════════════
STEP 5: ADD SENTIMENT ANALYSIS
═══════════════════════════════════════════════════════════════════

For EVERY headline and description, analyze the sentiment and assign a score:
   - "positive" - Uplifting, aspirational, beneficial, exciting
   - "neutral" - Factual, informational, descriptive
   - "negative" - Problem-focused, pain-highlighting (avoid unless strategic)

REQUIREMENT: Aim for 90%+ positive sentiment across all copy.
Only use neutral for pure facts. Avoid negative sentiment.

═══════════════════════════════════════════════════════════════════
FINAL QUALITY CHECKLIST - Review before submitting:
═══════════════════════════════════════════════════════════════════
{context_reminder}
Before you return your JSON, verify:
   □ Have I fully incorporated ALL user-provided context into my copy?
   □ Have I included the main keyword in at least 3 headlines?{'  ✓ Keyword: "' + main_keyword + '"' if main_keyword else ''}
   □ Have I used social proof from customer reviews in 2+ headlines per section?{' ✓ Reviews provided' if social_proof_reviews else ''}
   □ Do I have EXACTLY 50 headlines? (10 per section)
   □ Do I have EXACTLY 50 descriptions? (10 per section)
   □ Do I have EXACTLY 5 website headlines? (following 4-word value rule)
   □ Have I assigned sentiment scores to EVERY headline and description?
   □ Are 100% of headlines 25-30 characters? (anything under 25 WILL BE REJECTED)
   □ Are 100% of descriptions 80-90 characters? (anything under 80 WILL BE REJECTED)
   □ Is each description ONE complete sentence? (no choppy fragments!)
   □ Does each line maximize the available character space?
   □ Does each line sound like THIS brand wrote it?
   □ Have I used SPECIFIC REAL product names from THIS PAGE (not generic terms)?
   □ Have I referenced ACTUAL materials, features, or details from THIS PAGE?
   □ Can I point to where in the website content I found each detail?
   □ Are descriptions complete, flowing sentences?
   □ Would someone reading my ad know it's about THIS SPECIFIC page/product?
   □ Have I avoided all generic phrases that could apply to any page?
   □ Does this reflect 20+ years of copywriting mastery?

If you answer "no" to ANY of these, revise before submitting.

REMEMBER: Someone should be able to read your headlines/descriptions and say "this is clearly about [SPECIFIC PRODUCT/PAGE]", not just "this is about some product".

ABSOLUTE REQUIREMENTS - STRICTLY ENFORCED:
   ✓ Headlines: 25-30 characters (ANYTHING UNDER 25 WILL BE REJECTED)
   ✓ Descriptions: 80-90 characters (ANYTHING UNDER 80 WILL BE REJECTED)
   ✓ ONE COMPLETE SENTENCE per description - no choppy fragments, no multiple sentences
   ✓ Maximize character space - use full 80-90 chars for descriptions, 25-30 for headlines
   ✓ Brand-specific terminology and features
   ✓ Sophisticated, luxury-appropriate tone
   ✓ 50 headlines + 50 descriptions + 5 website headlines + sentiment scores
   ✓ Main keyword included in 3+ headlines{' ("' + main_keyword + '")' if main_keyword else ' (if provided)'}
   ✓ Social proof from reviews in 2+ headlines per section{' (reviews provided)' if social_proof_reviews else ' (if provided)'}

Return ONLY a valid JSON object in this exact format:
{{
  "headlines": {{
    "benefits": [
      {{"text": "headline 1", "sentiment": "positive"}},
      {{"text": "headline 2", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "technical": [
      {{"text": "headline 1", "sentiment": "neutral"}},
      ...  // 10 total
    ],
    "quirky": [
      {{"text": "headline 1", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "cta": [
      {{"text": "headline 1", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "brand": [
      {{"text": "headline 1", "sentiment": "positive"}},
      ...  // 10 total
    ]
  }},
  "descriptions": {{
    "benefits": [
      {{"text": "description 1", "sentiment": "positive"}},
      {{"text": "description 2", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "technical": [
      {{"text": "description 1", "sentiment": "neutral"}},
      ...  // 10 total
    ],
    "quirky": [
      {{"text": "description 1", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "cta": [
      {{"text": "description 1", "sentiment": "positive"}},
      ...  // 10 total
    ],
    "brand": [
      {{"text": "description 1", "sentiment": "positive"}},
      ...  // 10 total
    ]
  }},
  "website_headlines": [
    "Website headline 1 (follows 4-word value rule)",
    "Website headline 2",
    "Website headline 3",
    "Website headline 4",
    "Website headline 5"
  ],
  "page_info": {{
    "brand": "Brand Name",
    "product": "Main Product/Service",
    "category": "Business Category"
  }}
}}

Return ONLY the JSON, no other text before or after."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                temperature=0.7,  # Lower temperature for more focused, page-specific output
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text

            print("Received response from Claude, parsing...", flush=True)

            # Extract JSON from response (in case Claude added any text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            # Validate and ensure we have all required sections
            required_sections = ["benefits", "technical", "quirky", "cta", "brand"]

            for section in required_sections:
                if section not in result["headlines"]:
                    result["headlines"][section] = []
                if section not in result["descriptions"]:
                    result["descriptions"][section] = []

            # CRITICAL: Filter out any items that exceed character limits
            print("Validating character limits...", flush=True)

            headlines_removed = 0
            descriptions_removed = 0
            headlines_too_short = 0
            descriptions_too_short = 0

            for section in required_sections:
                # Filter headlines: 20-30 chars (Google's hard limit is 30)
                valid_headlines = []
                for item in result["headlines"][section]:
                    # Handle both old format (string) and new format (object with text/sentiment)
                    if isinstance(item, dict):
                        headline = item.get("text", "")
                        sentiment = item.get("sentiment", "positive")
                    else:
                        headline = item
                        sentiment = "positive"  # Default sentiment

                    char_count = len(headline)
                    if char_count > 30:
                        headlines_removed += 1
                        print(f"  ✗ Removed headline (too long: {char_count} chars): {headline[:50]}", flush=True)
                    elif char_count < 20:  # Minimum for meaningful content
                        headlines_too_short += 1
                        print(f"  ⚠ Removed headline (too short: {char_count} chars): {headline}", flush=True)
                    else:
                        valid_headlines.append({"text": headline, "sentiment": sentiment})

                result["headlines"][section] = valid_headlines

                # Filter descriptions: 70-90 chars (Google's hard limit is 90)
                valid_descriptions = []
                for item in result["descriptions"][section]:
                    # Handle both old format (string) and new format (object with text/sentiment)
                    if isinstance(item, dict):
                        description = item.get("text", "")
                        sentiment = item.get("sentiment", "positive")
                    else:
                        description = item
                        sentiment = "positive"  # Default sentiment

                    char_count = len(description)
                    if char_count > 90:
                        descriptions_removed += 1
                        print(f"  ✗ Removed description (too long: {char_count} chars): {description[:60]}...", flush=True)
                    elif char_count < 70:  # Minimum for complete sentences
                        descriptions_too_short += 1
                        print(f"  ⚠ Removed description (too short: {char_count} chars): {description}", flush=True)
                    else:
                        valid_descriptions.append({"text": description, "sentiment": sentiment})

                result["descriptions"][section] = valid_descriptions

            result["url"] = self.url

            # Report results
            total_headlines = sum(len(v) for v in result['headlines'].values())
            total_descriptions = sum(len(v) for v in result['descriptions'].values())

            print(f"\nSuccessfully generated ad copy!", flush=True)
            print(f"Valid Headlines: {total_headlines}", flush=True)
            print(f"Valid Descriptions: {total_descriptions}", flush=True)

            if headlines_removed > 0 or descriptions_removed > 0:
                print(f"\nFiltered out:", flush=True)
                if headlines_removed > 0:
                    print(f"  - {headlines_removed} headlines (over 30 chars)", flush=True)
                if descriptions_removed > 0:
                    print(f"  - {descriptions_removed} descriptions (over 90 chars)", flush=True)
                if headlines_too_short > 0:
                    print(f"  - {headlines_too_short} headlines (under 25 chars - too short!)", flush=True)
                if descriptions_too_short > 0:
                    print(f"  - {descriptions_too_short} descriptions (under 80 chars - too short!)", flush=True)

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response: {e}", flush=True)
            print(f"Response was: {response_text[:500]}", flush=True)
            raise Exception("Failed to parse Claude's response as JSON")

        except Exception as e:
            print(f"Error calling Claude API: {e}", flush=True)
            raise

    def generate_asset_group(self, additional_context: str = "") -> Dict:
        """Use Claude AI to generate Performance Max asset group content."""

        print("Fetching website content...", flush=True)
        website_content = self.fetch_website_content()

        # Load ROK specifications
        print("Loading ROK specifications...", flush=True)
        rok_specs = self._load_rok_specs()
        
        # Load specs from KB
        kb_specs = self._load_specs_from_kb()
        kb_specs_text = kb_specs.get("specs_text", "") if kb_specs else ""

        print("Sending to Claude AI for asset group generation...", flush=True)

        # Build context section if provided
        context_section = ""
        context_reminder = ""
        if additional_context:
            context_section = f"""

═══════════════════════════════════════════════════════════════════
🔴 CRITICAL: USER-PROVIDED CONTEXT (READ THIS FIRST!)
═══════════════════════════════════════════════════════════════════

{additional_context}

⚠️ IMPORTANT: The above context is PROVIDED BY THE USER and must take precedence.
   - If context mentions target audience, write for THAT audience
   - If context mentions special offers, INCLUDE those in your copy
   - If context mentions brand tone, MATCH that tone exactly
   - If context mentions campaign goals, OPTIMIZE for those goals
   - If context mentions specific messaging, PRIORITIZE that messaging

This is CRITICAL context that should inform EVERY asset you write.

═══════════════════════════════════════════════════════════════════
"""
            context_reminder = f"""

🔴 REMINDER: Don't forget the user-provided context above! Every asset must consider:
{additional_context}
"""

        prompt = f"""You are a professional copywriter with 20 years of experience writing Google Ads copy.

I need you to analyze this website and create a complete Performance Max Asset Group following ROK specifications.
{context_section}
{website_content}

ROK SPECIFICATIONS AND GUIDELINES:
{rok_specs}

{kb_specs_text}

IMPORTANT INSTRUCTIONS:

STEP 1: DEEPLY ANALYZE THE WEBSITE (same as before - tone, audience, positioning)

STEP 2: Generate HEADLINES & DESCRIPTIONS
{context_reminder}
⚠️ CHARACTER LIMITS ⚠️

SHORT HEADLINES (50 total - 10 per category):
- MAXIMUM: 30 characters (Google's hard limit)
- TARGET: 27-30 characters (STRICTLY ENFORCED - anything under 25 will be REJECTED)
- MINIMUM: 25 characters (REQUIRED)
- CAPITALIZATION: SENTENCE CASE ONLY (first word + proper nouns capitalized, rest lowercase)
- Focus: Punchy, impactful messages - use the full 27-30 chars
- Categories: Benefits (10), Technical (10), Quirky (10), CTA (10), Brand (10)
- Examples: ✓ "Handcrafted leather diaries" ✗ "Handcrafted Leather Diaries"

LONG HEADLINES (25 total - 5 per category):
- MAXIMUM: 90 characters (Google's hard limit)
- TARGET: 82-90 characters (STRICTLY ENFORCED - anything under 80 will be REJECTED)
- MINIMUM: 80 characters (REQUIRED)
- CAPITALIZATION: SENTENCE CASE ONLY (first word + proper nouns capitalized, rest lowercase)
- WRITING STYLE: ONE complete sentence for maximum readability
- Focus: More detailed, complete statements that expand on products/benefits
- Categories: Benefits (5), Technical (5), Quirky (5), CTA (5), Brand (5)
- Examples: ✓ "Discover handcrafted leather goods..." ✗ "Discover Handcrafted Leather Goods..."

DESCRIPTIONS (25 total - 5 per category):
- MAXIMUM: 90 characters (Google's hard limit)
- TARGET: 82-90 characters (STRICTLY ENFORCED - anything under 80 will be REJECTED)
- MINIMUM: 80 characters (REQUIRED)
- CAPITALIZATION: SENTENCE CASE ONLY (first word + proper nouns capitalized, rest lowercase)
- WRITING STYLE: ONE complete, flowing sentence for maximum readability
- Focus: Complete, flowing sentences with persuasive details - NO choppy fragments
- Categories: Benefits (5), Technical (5), Quirky (5), CTA (5), Brand (5)
- Examples: ✓ "Shop our collection..." ✗ "Shop Our Collection..."

🚨 CRITICAL: Use the FULL 80-90 character space and write as SINGLE SENTENCES for readability! 🚨

STEP 3: Generate SITELINKS (4-6 sitelinks)
{context_reminder}
For each sitelink generate:
- Headline: MAXIMUM 25 characters (SENTENCE CASE)
- Description line 1: MAXIMUM 35 characters (SENTENCE CASE)
- Description line 2: MAXIMUM 35 characters (SENTENCE CASE)
- Landing page URL: Must be relevant page on the website

Sitelinks should link to:
- Similar/related products
- Same category pages
- Key sections of the website
- Complementary offerings

STEP 4: Generate STRUCTURED SNIPPETS (3-5 snippet groups)

Format: Header + list of values
Common headers: "Brands", "Services", "Types", "Styles", "Models", "Amenities", "Courses", "Degrees", "Destinations", "Featured hotels", "Insurance coverage", "Neighborhoods", "Service catalog", "Shows", "Types"

Choose appropriate header(s) for this business and provide 3-10 values per header.

STEP 5: Generate CALLOUTS (8-10 callouts)

MAXIMUM 25 characters each (SENTENCE CASE).
Highlight key benefits, features, offers, USPs.

STEP 6: Generate SEARCH THEMES (50 search terms)

Create 50 search terms/phrases that:
- Cover all different ways visitors search for this product/service
- Include variations (singular/plural, formal/casual)
- Mix broad and specific terms
- Include brand and non-brand terms
- Match search intent for THIS specific page/product
- Use language the target audience actually uses

CRITICAL RULES FOR ALL ASSETS:
{context_reminder}
- Apply same tone-of-voice analysis as before
- Match brand's communication style precisely
- Write for the specific target audience
- Use actual content from website, not generic templates
- Maximize character limits where applicable
- Be specific, not generic
- No clichés
- Fully incorporate ALL user-provided context (if any)

Return ONLY a valid JSON object in this exact format:
{{
  "short_headlines": {{
    "benefits": ["...", ...],    // 10 short headlines, 25-30 chars each (UNDER 25 = REJECTED)
    "technical": ["...", ...],   // 10 short headlines, 25-30 chars
    "quirky": ["...", ...],      // 10 short headlines, 25-30 chars
    "cta": ["...", ...],         // 10 short headlines, 25-30 chars
    "brand": ["...", ...]        // 10 short headlines, 25-30 chars
  }},
  "long_headlines": {{
    "benefits": ["...", ...],    // 5 long headlines, 80-90 chars each (UNDER 80 = REJECTED)
    "technical": ["...", ...],   // 5 long headlines, 80-90 chars
    "quirky": ["...", ...],      // 5 long headlines, 80-90 chars
    "cta": ["...", ...],         // 5 long headlines, 80-90 chars
    "brand": ["...", ...]        // 5 long headlines, 80-90 chars
  }},
  "descriptions": {{
    "benefits": ["...", ...],    // 5 descriptions, 80-90 chars each (UNDER 80 = REJECTED)
    "technical": ["...", ...],   // 5 descriptions, 80-90 chars
    "quirky": ["...", ...],      // 5 descriptions, 80-90 chars
    "cta": ["...", ...],         // 5 descriptions, 80-90 chars
    "brand": ["...", ...]        // 5 descriptions, 80-90 chars
  }},
  "sitelinks": [
    {{
      "headline": "...",           // max 25 chars
      "description_1": "...",      // max 35 chars
      "description_2": "...",      // max 35 chars
      "url": "https://..."
    }},
    ...                            // 4-6 sitelinks total
  ],
  "structured_snippets": [
    {{
      "header": "Services",        // e.g., "Brands", "Types", "Services"
      "values": ["...", "...", ...]  // 3-10 values
    }},
    ...                            // 3-5 snippet groups
  ],
  "callouts": ["...", ...],        // 8-10 callouts, max 25 chars each
  "search_themes": ["...", ...],   // 50 search terms
  "page_info": {{
    "brand": "Brand Name",
    "product": "Main Product/Service",
    "category": "Business Category"
  }}
}}

Return ONLY the JSON, no other text before or after."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                temperature=0.7,  # Lower temperature for more focused, page-specific output
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text

            print("Received response from Claude, parsing...", flush=True)

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            result = json.loads(response_text)

            # Validate and ensure we have all required sections
            required_sections = ["benefits", "technical", "quirky", "cta", "brand"]

            for section in required_sections:
                if section not in result.get("short_headlines", {}):
                    result.setdefault("short_headlines", {})[section] = []
                if section not in result.get("long_headlines", {}):
                    result.setdefault("long_headlines", {})[section] = []
                if section not in result.get("descriptions", {}):
                    result.setdefault("descriptions", {})[section] = []

            # Validate character limits for headlines and descriptions
            print("Validating character limits...", flush=True)

            short_headlines_removed = 0
            long_headlines_removed = 0
            descriptions_removed = 0

            for section in required_sections:
                # Filter short headlines: 20-30 chars (Google's hard limit is 30)
                valid_short_headlines = []
                for headline in result["short_headlines"].get(section, []):
                    char_count = len(headline)
                    if 20 <= char_count <= 30:
                        valid_short_headlines.append(headline)
                    else:
                        short_headlines_removed += 1
                        print(f"  ✗ Removed short headline ({char_count} chars): {headline[:40]}", flush=True)
                result["short_headlines"][section] = valid_short_headlines

                # Filter long headlines: 70-90 chars (Google's hard limit is 90)
                valid_long_headlines = []
                for headline in result["long_headlines"].get(section, []):
                    char_count = len(headline)
                    if 70 <= char_count <= 90:
                        valid_long_headlines.append(headline)
                    else:
                        long_headlines_removed += 1
                        print(f"  ✗ Removed long headline ({char_count} chars): {headline[:50]}", flush=True)
                result["long_headlines"][section] = valid_long_headlines

                # Filter descriptions: 70-90 characters (Google's hard limit is 90)
                valid_descriptions = []
                for description in result["descriptions"].get(section, []):
                    char_count = len(description)
                    if 70 <= char_count <= 90:
                        valid_descriptions.append(description)
                    else:
                        descriptions_removed += 1
                        print(f"  ✗ Removed description ({char_count} chars): {description[:50]}...", flush=True)
                result["descriptions"][section] = valid_descriptions

            # Validate sitelinks
            valid_sitelinks = []
            for sitelink in result.get("sitelinks", []):
                if (len(sitelink.get("headline", "")) <= 25 and
                    len(sitelink.get("description_1", "")) <= 35 and
                    len(sitelink.get("description_2", "")) <= 35):
                    valid_sitelinks.append(sitelink)
                else:
                    print(f"  ✗ Removed sitelink (over limit): {sitelink.get('headline', '')[:30]}", flush=True)
            result["sitelinks"] = valid_sitelinks

            # Validate callouts (max 25 chars)
            valid_callouts = [c for c in result.get("callouts", []) if len(c) <= 25]
            result["callouts"] = valid_callouts

            result["url"] = self.url

            # Report results
            print(f"\nSuccessfully generated asset group!", flush=True)
            print(f"Short Headlines: {sum(len(v) for v in result['short_headlines'].values())}", flush=True)
            print(f"Long Headlines: {sum(len(v) for v in result['long_headlines'].values())}", flush=True)
            print(f"Descriptions: {sum(len(v) for v in result['descriptions'].values())}", flush=True)
            print(f"Sitelinks: {len(result.get('sitelinks', []))}", flush=True)
            print(f"Structured Snippets: {len(result.get('structured_snippets', []))}", flush=True)
            print(f"Callouts: {len(result.get('callouts', []))}", flush=True)
            print(f"Search Themes: {len(result.get('search_themes', []))}", flush=True)

            if short_headlines_removed > 0 or long_headlines_removed > 0 or descriptions_removed > 0:
                print(f"\nFiltered out:", flush=True)
                if short_headlines_removed > 0:
                    print(f"  - {short_headlines_removed} short headlines", flush=True)
                if long_headlines_removed > 0:
                    print(f"  - {long_headlines_removed} long headlines", flush=True)
                if descriptions_removed > 0:
                    print(f"  - {descriptions_removed} descriptions", flush=True)

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response: {e}", flush=True)
            print(f"Response was: {response_text[:500]}", flush=True)
            raise Exception("Failed to parse Claude's response as JSON")

        except Exception as e:
            print(f"Error calling Claude API: {e}", flush=True)
            raise


if __name__ == "__main__":
    # Test
    import sys

    if len(sys.argv) < 2:
        print("Usage: python claude_copywriter.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        copywriter = ClaudeCopywriter(url)
        result = copywriter.generate_ad_copy()

        print("\n" + "="*80)
        print("AD COPY GENERATED")
        print("="*80)

        print("\nBRAND INFO:")
        print(f"  Brand: {result['page_info']['brand']}")
        print(f"  Product: {result['page_info']['product']}")
        print(f"  Category: {result['page_info']['category']}")

        print("\nHEADLINES:")
        for section, headlines in result['headlines'].items():
            print(f"\n{section.upper()} ({len(headlines)} headlines):")
            for i, h in enumerate(headlines[:3], 1):
                print(f"  {i}. {h} [{len(h)}/30]")

        print("\nDESCRIPTIONS:")
        for section, descriptions in result['descriptions'].items():
            print(f"\n{section.upper()} ({len(descriptions)} descriptions):")
            for i, d in enumerate(descriptions[:2], 1):
                print(f"  {i}. {d} [{len(d)}/90]")

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
