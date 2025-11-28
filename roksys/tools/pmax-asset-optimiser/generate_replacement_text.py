#!/usr/bin/env python3
"""
Replacement Text Generator - AI-powered text generation for underperforming assets

This script generates replacement text for underperforming PMAX assets while:
1. Preserving the brand's tone of voice (via website analysis)
2. Learning from winning asset patterns
3. Strictly adhering to Google Ads character limits
4. Adding product specificity based on performance data

Author: PetesBrain
Created: 2025-11-25
"""

import sys
import csv
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Add paths for imports
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/tools/google-ads-generator')

from website_analyzer import WebsiteAnalyzer

# Import Anthropic for AI generation
try:
    from anthropic import Anthropic
    import os
    from pathlib import Path

    # Try to load API key from multiple sources
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # If not in environment, try loading from .env file in generator directory
    if not ANTHROPIC_API_KEY:
        env_file = Path('/Users/administrator/Documents/PetesBrain/tools/google-ads-generator/.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        ANTHROPIC_API_KEY = line.split('=', 1)[1].strip()
                        break

    if ANTHROPIC_API_KEY:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
    else:
        client = None
except ImportError:
    client = None
    print("⚠️  Anthropic library not installed. AI generation will be limited.")


# STRICT character limits - enforced by Google Ads API
CHARACTER_LIMITS = {
    'Headline': 30,
    'Long headline': 90,
    'Description': 90
}


class ReplacementTextGenerator:
    """Generates replacement text for underperforming assets"""

    def __init__(self, config_path: str):
        """
        Initialise generator with configuration

        Args:
            config_path: Path to config.yaml file
        """
        self.config = self._load_config(config_path)
        self.client = client  # Use the module-level client (loaded with API key)
        self.website_insights = None
        self.winning_patterns = []

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def analyze_client_website(self, url: str):
        """
        Analyze client website to extract tone of voice and brand insights

        Args:
            url: Client website URL
        """
        print(f"\n🌐 Analyzing client website: {url}")
        print("   Extracting brand voice and key messaging...")

        # Use Claude to analyze the website
        prompt = f"""Analyze this website and extract:
1. Brand name
2. Tone of voice (3-4 adjectives)
3. Main products/services (list 5)
4. Key benefits/USPs (list 5)

Return as JSON only, no explanation:
{{
    "brand_name": "...",
    "tone_indicators": ["...", "..."],
    "main_products": ["...", "..."],
    "key_benefits": ["...", "..."]
}}

Website: {url}"""

        try:
            message = self.client.messages.create(
                model=self.config['generation']['model'],
                max_tokens=1024,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text.strip()
            # Extract JSON from response (may have markdown code blocks)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            self.website_insights = json.loads(response_text)
            print(f"✅ Analyzed {self.website_insights.get('brand_name', 'website')}")

        except Exception as e:
            print(f"⚠️  Website analysis failed: {e}")
            print("   Using generic insights...")
            self.website_insights = {
                'brand_name': 'Client',
                'tone_indicators': ['professional', 'friendly'],
                'main_products': [],
                'key_benefits': []
            }

    def load_winning_patterns(self, asset_report_csv: str):
        """
        Extract winning asset patterns from the full asset report

        Args:
            asset_report_csv: Path to Asset performance report CSV
        """
        print(f"\n📊 Analyzing winning assets to identify successful patterns...")

        with open(asset_report_csv, 'r', encoding='utf-8') as f:
            # Skip header rows
            next(f)
            next(f)
            reader = csv.DictReader(f)
            assets = list(reader)

        # Filter to PMAX text assets with conversions
        winners = []
        for asset in assets:
            if asset.get('Campaign type') != 'Performance Max':
                continue
            if asset.get('Asset type') not in ['Headline', 'Description', 'Long headline']:
                continue
            if asset.get('Added by') == 'Google AI':
                continue

            # Parse conversions
            try:
                conv = float(asset.get('Conversions', '0').replace(',', ''))
            except:
                conv = 0

            if conv > 0:
                winners.append({
                    'text': asset.get('Asset', ''),
                    'type': asset.get('Asset type', ''),
                    'conversions': conv
                })

        # Sort by conversions
        winners.sort(key=lambda x: x['conversions'], reverse=True)
        self.winning_patterns = winners[:20]  # Top 20

        print(f"   Found {len(self.winning_patterns)} top-performing assets")
        print(f"   Top 3 winners:")
        for i, winner in enumerate(self.winning_patterns[:3], 1):
            print(f"   {i}. [{winner['type']}] {winner['text'][:50]}... ({winner['conversions']:.2f} conv)")

    def generate_replacements(
        self,
        underperformer: Dict,
        num_alternatives: int = 3,
        avoid_texts: List[str] = None
    ) -> List[Dict]:
        """
        Generate replacement text alternatives for an underperforming asset

        Args:
            underperformer: Dictionary with underperformer details
            num_alternatives: Number of alternatives to generate
            avoid_texts: List of texts already generated (to avoid duplicates)

        Returns:
            List of dictionaries with replacement options
        """
        if avoid_texts is None:
            avoid_texts = []
        asset_text = underperformer['Asset']
        asset_type = underperformer['Asset Type']
        impressions = underperformer['Impressions']
        flag_reason = underperformer['Flag Reason']
        campaign = underperformer.get('Campaign', '')
        asset_group = underperformer.get('Asset Group', '')
        asset_group_url = underperformer.get('Asset Group URL', '')

        # Get character limit for this asset type
        char_limit = CHARACTER_LIMITS.get(asset_type, 90)

        print(f"\n🎨 Generating replacements for:")
        print(f"   Campaign: {campaign}")
        print(f"   Asset Group: {asset_group}")
        print(f"   Landing Page: {asset_group_url}")
        print(f"   Current: \"{asset_text[:60]}...\"")
        print(f"   Type: {asset_type} (max {char_limit} chars)")
        print(f"   Issue: {flag_reason}")

        # Build context for AI
        context = self._build_generation_context(
            asset_text,
            asset_type,
            flag_reason,
            char_limit,
            campaign,
            asset_group,
            asset_group_url,
            num_alternatives,
            avoid_texts
        )

        # Generate alternatives using AI
        alternatives = self._generate_with_ai(
            context,
            asset_type,
            char_limit,
            num_alternatives
        )

        # POST-GENERATION DUPLICATE CHECK (2025-11-27)
        # If AI generated duplicates despite being told not to, regenerate with stronger warning
        if avoid_texts:
            duplicates_found = [alt for alt in alternatives if alt in avoid_texts]
            if duplicates_found:
                print(f"   ⚠️  AI generated {len(duplicates_found)} duplicate(s) despite being told to avoid them!")
                print(f"      Duplicates: {duplicates_found}")
                print(f"   🔄 Regenerating with STRONGER anti-duplicate instruction...")

                # Build even stronger avoid context
                stronger_context = context.replace(
                    "**CRITICAL: AVOID DUPLICATES**",
                    "**❌ STRICT PROHIBITION - DO NOT DUPLICATE ❌**"
                ).replace(
                    "You MUST generate COMPLETELY DIFFERENT alternatives.",
                    "You are ABSOLUTELY FORBIDDEN from generating ANY of these texts. If you generate ANY duplicate, the entire generation FAILS. Generate COMPLETELY DIFFERENT text."
                )

                # Retry with stronger instruction
                alternatives = self._generate_with_ai(
                    stronger_context,
                    asset_type,
                    char_limit,
                    num_alternatives
                )

                # Check again
                still_duplicates = [alt for alt in alternatives if alt in avoid_texts]
                if still_duplicates:
                    print(f"   ❌ AI STILL generated duplicates: {still_duplicates}")
                    print(f"      This is an AI compliance issue - will accept but log warning")

        # Validate and format results
        validated_alternatives = []
        for i, alt_text in enumerate(alternatives, 1):
            # Strict character validation
            actual_length = len(alt_text)
            if actual_length > char_limit:
                print(f"   ⚠️  Option {i} REJECTED: {actual_length} chars (limit: {char_limit})")
                # Try to truncate intelligently
                alt_text = self._smart_truncate(alt_text, char_limit)
                actual_length = len(alt_text)
                print(f"      Truncated to: \"{alt_text}\" ({actual_length} chars)")

            validated_alternatives.append({
                'option_number': i,
                'text': alt_text,
                'char_count': actual_length,
                'char_limit': char_limit,
                'valid': actual_length <= char_limit,
                'tone_match': 'preserved',  # Based on website analysis
                'specificity': 'enhanced'    # Added product details
            })

        return validated_alternatives

    def _build_generation_context(
        self,
        current_text: str,
        asset_type: str,
        flag_reason: str,
        char_limit: int,
        campaign: str = '',
        asset_group: str = '',
        asset_group_url: str = '',
        num_alternatives: int = 3,
        avoid_texts: List[str] = None
    ) -> str:
        """Build context prompt for AI generation"""

        # Extract winning examples of same type
        winning_examples = [
            w['text'] for w in self.winning_patterns
            if w['type'] == asset_type
        ][:5]

        # Extract tone indicators
        tone_indicators = []
        brand_name = ""
        key_benefits = []
        main_products = []

        if self.website_insights:
            tone_indicators = self.website_insights.get('tone_indicators', [])
            brand_name = self.website_insights.get('brand_name', '')
            key_benefits = self.website_insights.get('key_benefits', [])[:5]
            main_products = self.website_insights.get('main_products', [])[:10]

        # Extract product focus from landing page URL using AI
        product_focus = self._extract_product_from_url_ai(asset_group_url, asset_group)

        # Build avoid list section
        avoid_section = ""
        if avoid_texts and len(avoid_texts) > 0:
            avoid_section = f"""
**CRITICAL: AVOID DUPLICATES**
The following {len(avoid_texts)} texts have ALREADY been generated for other assets in this asset group.
You MUST generate COMPLETELY DIFFERENT alternatives. DO NOT use any of these:
{chr(10).join(['- "' + text[:60] + ('..." ' if len(text) > 60 else '" ') + '(' + str(len(text)) + ' chars)' for text in avoid_texts[-20:]])}

Your new alternatives MUST be unique and different from ALL of the above.
"""

        context = f"""You are generating replacement text for a Google Ads Performance Max asset.

**CRITICAL CONSTRAINTS**:
- Asset Type: {asset_type}
- CHARACTER LIMIT: {char_limit} characters MAXIMUM (STRICTLY ENFORCED)
- Every character counts, including spaces and punctuation
- Text exceeding {char_limit} characters will be REJECTED by Google Ads API

**Campaign Context**:
Campaign: {campaign}
Asset Group: {asset_group}
Landing Page: {asset_group_url}
Product Focus: {product_focus}

**CRITICAL: Your replacement text MUST be relevant to "{product_focus}" ONLY.**
The landing page is {asset_group_url} - analyze this to understand the exact product being promoted.
DO NOT mention other products (e.g., no Christmas trees in olive tree groups, no lemon trees in rose groups).

**Current Underperforming Text**:
"{current_text}"
Character count: {len(current_text)}

**Why it's underperforming**:
{flag_reason}

**Brand Voice to Preserve** (from website analysis):
Tone: {', '.join(tone_indicators) if tone_indicators else 'warm, professional, welcoming'}
Brand name: {brand_name or 'Client'}

**What IS Working** (successful {asset_type} examples):
{chr(10).join(['- "' + ex + '" (' + str(len(ex)) + ' chars)' for ex in winning_examples[:3]]) if winning_examples else 'N/A'}

**Key Benefits to Consider**:
{chr(10).join(['- ' + b[:80] for b in key_benefits]) if key_benefits else 'Analyze the landing page URL to extract relevant benefits'}
{avoid_section}
**Your Task**:
Generate {num_alternatives} alternative {asset_type} options that:
1. ONLY mention "{product_focus}" - NO other products allowed
2. FIX the underperformance issue (add product specificity if generic, improve CTR)
3. PRESERVE the brand's warm, caring, ethical tone
4. MATCH the patterns that are working (see successful examples above)
5. STRICTLY stay within {char_limit} characters INCLUDING SPACES

**Examples of CORRECT product focus**:
- If product_focus = "olive trees": ✅ "Mediterranean olive trees" / ❌ "Lemon & olive trees"
- If product_focus = "rose bushes": ✅ "Anniversary rose bushes" / ❌ "Roses & Christmas trees"

**Output Format**:
Provide ONLY the {num_alternatives} text alternatives, one per line, with character count.
Example format:
"Rose bushes that bloom forever" (30)
"Ethical olive tree gifts" (25)
"Living lemon trees since 2003" (29)

Generate alternatives now:
"""

        return context

    def _generate_with_ai(
        self,
        context: str,
        asset_type: str,
        char_limit: int,
        num_alternatives: int
    ) -> List[str]:
        """
        Use AI to generate replacement text

        Args:
            context: Context prompt for AI
            asset_type: Type of asset
            char_limit: Character limit
            num_alternatives: Number of alternatives to generate

        Returns:
            List of alternative text strings
        """
        if not self.client:
            # Fallback to template-based generation
            print("   ⚠️  AI generation unavailable, using template fallback...")
            return self._generate_fallback_templates(asset_type, char_limit, num_alternatives)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # Claude Sonnet 4
                max_tokens=1024,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": context}
                ]
            )

            # Parse response
            response_text = response.content[0].text
            alternatives = self._parse_ai_response(response_text, char_limit)

            if len(alternatives) < num_alternatives:
                print(f"   ⚠️  Only got {len(alternatives)} alternatives, regenerating to get {num_alternatives}...")
                # Try ONE more time to get the full number - don't use templates
                try:
                    response2 = self.client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1024,
                        temperature=0.9,  # Higher temperature for more variety
                        messages=[{"role": "user", "content": context}]
                    )
                    response_text2 = response2.content[0].text
                    alternatives2 = self._parse_ai_response(response_text2, char_limit)

                    # Combine and deduplicate
                    all_alternatives = list(dict.fromkeys(alternatives + alternatives2))
                    alternatives = all_alternatives[:num_alternatives]

                    if len(alternatives) < num_alternatives:
                        print(f"   ⚠️  Still only got {len(alternatives)} - accepting partial results")
                except Exception as e:
                    print(f"   ⚠️  Retry failed: {e} - accepting partial results")

            return alternatives[:num_alternatives]

        except Exception as e:
            print(f"   ❌ AI generation failed: {e}")
            return self._generate_fallback_templates(asset_type, char_limit, num_alternatives)

    def _parse_ai_response(self, response_text: str, char_limit: int) -> List[str]:
        """Parse AI response to extract text alternatives"""
        alternatives = []

        for line in response_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('**'):
                continue

            # Extract text from quotes if present
            if '"' in line:
                parts = line.split('"')
                if len(parts) >= 2:
                    text = parts[1].strip()
                else:
                    # Try without quotes
                    text = line.split('(')[0].strip()
            else:
                # No quotes, split by character count indicator
                text = line.split('(')[0].strip()

            # Remove common prefixes
            for prefix in ['- ', '• ', '1. ', '2. ', '3. ', '4. ', '5. ']:
                if text.startswith(prefix):
                    text = text[len(prefix):].strip()

            # Validate
            if text and len(text) <= char_limit and len(text) > 5:
                alternatives.append(text)

        return alternatives

    def _generate_fallback_templates(
        self,
        asset_type: str,
        char_limit: int,
        num_alternatives: int
    ) -> List[str]:
        """
        Generate template-based alternatives when AI is unavailable

        Args:
            asset_type: Type of asset
            char_limit: Character limit
            num_alternatives: Number to generate

        Returns:
            List of template-based alternatives
        """
        templates = {
            'Headline': [
                "Ethical Tree Gifts Since 2003",  # 28 chars
                "Living Rose Bush Happiness",      # 26 chars
                "Tree2mydoor Olive Trees",         # 23 chars
                "Sustainable Plant Gifts",         # 23 chars
                "Send A Living Tree Gift"          # 23 chars
            ],
            'Long headline': [
                "Beautiful living gifts for anniversaries, birthdays & special occasions",  # 72 chars
                "Ethical tree & plant gifts delivered next day. Shop our collection now",   # 70 chars
                "Rose bushes, olive trees & more. Living gifts that bloom year after year" # 74 chars
            ],
            'Description': [
                "Living tree & plant gifts since 2003. Ethical, sustainable & gift wrapped with love",  # 85 chars
                "Rose bushes for birthdays & anniversaries. Delivered next day, gift wrapped with care", # 88 chars
                "Olive trees, lemon trees & more. Perfect for patios & conservatories. Shop now"        # 79 chars
            ]
        }

        asset_templates = templates.get(asset_type, templates['Headline'])

        # Filter by character limit and return requested number
        valid_templates = [t for t in asset_templates if len(t) <= char_limit]
        return valid_templates[:num_alternatives]

    def _extract_product_from_url(self, url: str) -> str:
        """
        Extract the primary product focus from landing page URL

        Args:
            url: Landing page URL

        Returns:
            Product category string with additional context from URL
        """
        if not url:
            return "living tree and plant gifts"

        url_lower = url.lower()

        # Extract from URL path - this is much more reliable than asset group names
        if 'olive-tree' in url_lower or '/olive' in url_lower:
            return "olive trees (Mediterranean olive varieties for patios and gardens)"
        elif 'lemon-tree' in url_lower or '/lemon' in url_lower:
            return "lemon trees (citrus trees for patios and conservatories)"
        elif 'rose' in url_lower and ('anniversary' in url_lower or 'memorial' in url_lower or 'birthday' in url_lower or 'sympathy' in url_lower):
            # Rose bushes with occasion context
            if 'anniversary' in url_lower:
                return "rose bushes (anniversary roses for romantic gifts)"
            elif 'memorial' in url_lower or 'sympathy' in url_lower:
                return "rose bushes (memorial and sympathy roses)"
            elif 'birthday' in url_lower:
                return "rose bushes (birthday rose gifts)"
            else:
                return "rose bushes"
        elif 'rose' in url_lower or '/roses' in url_lower:
            return "rose bushes (flowering rose varieties for gardens)"
        elif 'bay-tree' in url_lower or '/bay' in url_lower:
            return "bay trees (culinary bay laurel trees)"
        elif 'fig-tree' in url_lower or '/fig' in url_lower:
            return "fig trees (fruit-bearing fig varieties)"
        elif 'magnolia' in url_lower:
            return "magnolia trees (ornamental flowering magnolias)"
        elif 'christmas' in url_lower:
            return "Christmas trees (living Christmas tree gifts)"
        elif 'birthday' in url_lower:
            return "birthday tree and plant gifts"
        elif 'anniversary' in url_lower:
            return "anniversary tree and plant gifts"
        elif 'sympathy' in url_lower or 'memorial' in url_lower:
            return "sympathy and memorial trees"
        elif url_lower.endswith('.com') or url_lower.endswith('.com/'):
            # Homepage - allow broad range
            return "premium living tree and plant gifts"
        else:
            return "living tree and plant gifts"

    def _extract_product_from_url_ai(self, url: str, asset_group_name: str) -> str:
        """
        Use AI to extract the product/service focus from a landing page URL

        Args:
            url: Landing page URL
            asset_group_name: Asset group name for additional context

        Returns:
            Product/service description string
        """
        if not url:
            return "the product or service"

        if not self.client:
            # Fallback if AI not available
            return f"{asset_group_name} services"

        try:
            prompt = f"""Analyze this landing page URL and asset group name to identify what product or service is being promoted.

URL: {url}
Asset Group: {asset_group_name}

Return ONLY a concise product/service description (5-10 words maximum) that would be used in Google Ads text.

Examples of good responses:
- "luxury spa hotel in Yorkshire Dales"
- "boutique country house hotel"
- "4-star Derbyshire hotel with spa"
- "traditional Peak District inn"

Return only the description, nothing else:"""

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            product_focus = response.content[0].text.strip().strip('"').strip("'")
            return product_focus if product_focus else f"{asset_group_name} services"

        except Exception as e:
            print(f"   ⚠️  AI product extraction failed: {e}")
            return f"{asset_group_name} services"

    def _smart_truncate(self, text: str, max_length: int) -> str:
        """
        Intelligently truncate text to fit character limit

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        # Try to truncate at word boundary
        truncated = text[:max_length]

        # If last character is a space, remove it
        if truncated[-1] == ' ':
            return truncated[:-1]

        # Find last space before limit
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # Only truncate at word if close to limit
            return truncated[:last_space]

        # Otherwise just hard truncate
        return truncated

    def generate_all_replacements(
        self,
        underperformers_csv: str,
        output_csv: str,
        client_url: str,
        asset_report_csv: str
    ):
        """
        Generate replacements for all underperformers

        Args:
            underperformers_csv: Path to underperformers CSV
            output_csv: Path to save replacement candidates
            client_url: Client website URL for tone analysis
            asset_report_csv: Full asset report for winning pattern analysis
        """
        print("=" * 80)
        print("REPLACEMENT TEXT GENERATION")
        print("=" * 80)

        # Step 1: Analyze website for brand voice
        if client_url:
            self.analyze_client_website(client_url)
        else:
            print("⚠️  No client URL provided, skipping website analysis")

        # Step 2: Load winning patterns
        if asset_report_csv:
            self.load_winning_patterns(asset_report_csv)
        else:
            print("⚠️  No asset report provided, skipping winning pattern analysis")

        # Step 3: Load underperformers
        print(f"\n📋 Loading underperformers from: {underperformers_csv}")
        with open(underperformers_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            underperformers = list(reader)

        print(f"   Found {len(underperformers)} underperforming assets")

        # Step 3.5: Group by Asset Group URL + Asset Type for efficient batching
        print(f"\n🔄 Grouping assets by Asset Group + URL + Type for efficient generation...")
        from collections import defaultdict

        groups = defaultdict(list)
        for underperformer in underperformers:
            # Key: (Asset Group URL, Asset Type) - one AI call per unique combination
            key = (
                underperformer.get('Asset Group URL', ''),
                underperformer.get('Asset Type', '')
            )
            groups[key].append(underperformer)

        print(f"   Grouped {len(underperformers)} assets into {len(groups)} batches for organization")
        print(f"   Will make {len(underperformers)} individual AI calls to ensure uniqueness\n")

        # Step 4: Generate replacements (one call per asset for uniqueness)
        print(f"\n🎨 Generating replacement alternatives...")
        print(f"   This will take approximately {len(underperformers) * 3} seconds (~3s per asset)\n")

        results = []
        batch_num = 0

        for (asset_group_url, asset_type), group_assets in groups.items():
            batch_num += 1
            print(f"\n[Batch {batch_num}/{len(groups)}] Processing {len(group_assets)} assets:")
            print(f"   Asset Type: {asset_type}")
            print(f"   Landing Page: {asset_group_url}")
            print(f"   Assets in batch: {len(group_assets)}")

            # Track already-generated suggestions in this batch to avoid duplicates
            batch_generated_texts = []

            # Generate unique alternatives for EACH asset individually
            # This ensures truly unique suggestions and better quality than asking for 42 at once
            for asset_num, underperformer in enumerate(group_assets, 1):
                print(f"     - [{asset_num}/{len(group_assets)}] {underperformer['Asset'][:60]}...")

                # Generate 3 unique alternatives specifically for THIS asset
                # Pass already-generated texts to avoid duplicates
                alternatives = self.generate_replacements(
                    underperformer,
                    num_alternatives=3,
                    avoid_texts=batch_generated_texts
                )

                # Add new alternatives to the batch tracker
                batch_generated_texts.extend([alt['text'] for alt in alternatives])

                for alt in alternatives:
                    results.append({
                        'Campaign_ID': underperformer.get('Campaign ID', ''),
                        'Campaign': underperformer.get('Campaign', ''),
                        'Asset_Group_ID': underperformer.get('Asset Group ID', ''),
                        'Asset_Group': underperformer.get('Asset Group', ''),
                        'Original_Text': underperformer['Asset'],
                        'Asset_Type': underperformer['Asset Type'],
                        'Impressions': underperformer['Impressions'],
                        'CTR': underperformer['CTR'],
                        'Conv_Rate': underperformer['Conv Rate'],
                        'Flag_Reason': underperformer['Flag Reason'],
                        'Priority': underperformer['Priority'],
                        'Option_Number': alt['option_number'],
                        'Replacement_Text': alt['text'],
                        'Char_Count': alt['char_count'],
                        'Char_Limit': alt['char_limit'],
                        'Valid': alt['valid'],
                        'Action': 'REVIEW'  # User will change to SWAP or SKIP
                    })

        # Step 5: Save results
        print(f"\n💾 Saving {len(results)} replacement candidates to: {output_csv}")

        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Campaign_ID', 'Campaign', 'Asset_Group_ID', 'Asset_Group',
                'Original_Text', 'Asset_Type', 'Impressions', 'CTR', 'Conv_Rate',
                'Flag_Reason', 'Priority', 'Option_Number', 'Replacement_Text',
                'Char_Count', 'Char_Limit', 'Valid', 'Action'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n✅ Generation complete!")
        print(f"\n📊 Summary:")
        print(f"   - Underperformers processed: {len(underperformers)}")
        print(f"   - Total alternatives generated: {len(results)}")
        print(f"   - Valid alternatives: {sum(1 for r in results if r['Valid'])}")
        print(f"   - Invalid (over limit): {sum(1 for r in results if not r['Valid'])}")

        # Character limit violations report
        violations = [r for r in results if not r['Valid']]
        if violations:
            print(f"\n⚠️  WARNING: {len(violations)} alternatives exceeded character limits!")
            print(f"   These have been auto-truncated but should be reviewed manually.")

        print(f"\n📁 Next steps:")
        print(f"   1. Open in Google Sheets: {output_csv}")
        print(f"   2. Review 'Replacement_Text' column")
        print(f"   3. Edit as needed (ensure Char_Count ≤ Char_Limit)")
        print(f"   4. Set 'Action' to SWAP or SKIP for each row")
        print(f"   5. Download reviewed CSV")
        print(f"   6. Run execution script: python3 execute_asset_optimisation.py")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate AI replacement text for underperforming assets')
    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--csv', required=True, help='Path to underperformers CSV file')
    parser.add_argument('--output', help='Output CSV file path (optional)')
    args = parser.parse_args()

    print("=" * 80)
    print("PMAX ASSET REPLACEMENT TEXT GENERATOR")
    print("=" * 80)
    print()

    # Paths
    base_dir = Path(__file__).parent
    config_path = base_dir / 'config.yaml'
    underperformers_csv = Path(args.csv)

    # Determine output path
    if args.output:
        output_csv = Path(args.output)
    else:
        output_csv = underperformers_csv.parent / 'replacement-candidates.csv'

    # Check files exist
    if not underperformers_csv.exists():
        print(f"❌ Underperformers CSV not found: {underperformers_csv}")
        print(f"   Run: python3 analyse_asset_performance.py first")
        sys.exit(1)

    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)

    # Client URL detection from CSV (read first data row to get Asset Group URL)
    client_url = None
    with open(underperformers_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Asset Group URL' in row and row['Asset Group URL']:
                # Extract domain from URL
                from urllib.parse import urlparse
                parsed = urlparse(row['Asset Group URL'])
                client_url = f"{parsed.scheme}://{parsed.netloc}"
                break

    if not client_url:
        print(f"⚠️  Could not detect client URL from CSV, using fallback")
        client_url = "https://example.com"

    print(f"🌐 Client URL: {client_url}")

    # Initialize generator
    generator = ReplacementTextGenerator(str(config_path))

    # Generate replacements (asset_report_csv not needed as we have URL context)
    generator.generate_all_replacements(
        str(underperformers_csv),
        str(output_csv),
        client_url,
        None  # We don't need full asset report - URL context is enough
    )


if __name__ == "__main__":
    main()
