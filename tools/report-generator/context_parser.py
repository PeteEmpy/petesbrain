"""
Client Context Parser

Reads and parses clients/*/CONTEXT.md files to extract strategic information
for campaign analysis. Helps avoid false positives by understanding client-
specific strategies, known issues, and performance targets.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class ClientContextParser:
    """Parse client CONTEXT.md files to extract strategic information"""

    def __init__(self, clients_base_path: str = None):
        """
        Initialize parser

        Args:
            clients_base_path: Path to clients/ directory. Defaults to auto-detection.
        """
        if clients_base_path is None:
            # Auto-detect based on current file location
            current_file = Path(__file__).resolve()
            # From tools/report-generator/context_parser.py
            # Go up: context_parser.py -> report-generator -> tools -> PetesBrain.nosync
            repo_root = current_file.parent.parent.parent
            self.clients_base_path = repo_root / "clients"
        else:
            self.clients_base_path = Path(clients_base_path)

    def load_client_context(self, client_slug: str) -> Optional[Dict[str, Any]]:
        """
        Load and parse CONTEXT.md for a client

        Args:
            client_slug: Client folder name (e.g., 'smythson', 'tree2mydoor')

        Returns:
            Parsed context dictionary or None if file not found
        """
        context_path = self.clients_base_path / client_slug / "CONTEXT.md"

        if not context_path.exists():
            logger.warning(f"CONTEXT.md not found for {client_slug} at {context_path}")
            return None

        try:
            content = context_path.read_text(encoding='utf-8')

            return {
                'client_slug': client_slug,
                'raw_content': content,
                'strategic_approach': self._extract_strategic_approach(content),
                'performance_targets': self._extract_performance_targets(content),
                'known_issues': self._extract_known_issues(content),
                'budget_info': self._extract_budget_info(content),
                'platform_info': self._extract_platform_info(content),
                'account_ids': self._extract_account_ids(content),
                'business_context': self._extract_business_context(content),
                'multi_account': self._detect_multi_account(content)
            }

        except Exception as e:
            logger.error(f"Error parsing CONTEXT.md for {client_slug}: {e}")
            return None

    def _extract_strategic_approach(self, content: str) -> Dict[str, str]:
        """Extract strategic approach information"""
        strategy = {}

        # Find Strategic Context section
        strategy_section = self._extract_section(content, r'##\s*Strategic Context')
        if not strategy_section:
            return strategy

        # Extract campaign structure
        campaign_structure_match = re.search(
            r'\*\*Campaign Structure\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            strategy_section,
            re.DOTALL
        )
        if campaign_structure_match:
            strategy['campaign_structure'] = campaign_structure_match.group(1).strip()

        # Extract bidding strategy
        bidding_match = re.search(
            r'\*\*Bidding Strategy\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            strategy_section,
            re.DOTALL
        )
        if bidding_match:
            strategy['bidding_strategy'] = bidding_match.group(1).strip()

        # Extract key focus areas
        focus_match = re.search(
            r'\*\*Key Focus Areas?\*\*:?\s*(.+?)(?:\n\*\*|\n##|\n\n\n|$)',
            strategy_section,
            re.DOTALL
        )
        if focus_match:
            strategy['key_focus_areas'] = focus_match.group(1).strip()

        # Check for Product Hero integration
        if 'product hero' in strategy_section.lower():
            strategy['uses_product_hero'] = True
            # Extract product hero details
            ph_match = re.search(
                r'\*\*Product Hero.*?\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
                strategy_section,
                re.DOTALL | re.IGNORECASE
            )
            if ph_match:
                strategy['product_hero_details'] = ph_match.group(1).strip()

        return strategy

    def _extract_performance_targets(self, content: str) -> Dict[str, Any]:
        """Extract performance targets (ROAS, CPA, etc.)"""
        targets = {}

        # Find Goals & KPIs section
        goals_section = self._extract_section(content, r'###\s*Goals?\s*(&|and)?\s*KPIs?')
        if not goals_section:
            return targets

        # Extract target ROAS
        roas_patterns = [
            r'Target ROAS\*\*:?\s*(\d+\.?\d*)\s*[x×]?',
            r'ROAS target:?\s*(\d+\.?\d*)\s*[x×]?',
            r'Target:?\s*(\d+\.?\d*)\s*[x×]?\s*ROAS'
        ]
        for pattern in roas_patterns:
            match = re.search(pattern, goals_section, re.IGNORECASE)
            if match:
                targets['target_roas'] = float(match.group(1))
                break

        # Extract target CPA
        cpa_patterns = [
            r'Target CPA\*\*:?\s*[£\$](\d+\.?\d*)',
            r'CPA target:?\s*[£\$](\d+\.?\d*)'
        ]
        for pattern in cpa_patterns:
            match = re.search(pattern, goals_section, re.IGNORECASE)
            if match:
                targets['target_cpa'] = float(match.group(1))
                break

        # Extract primary goal
        primary_goal_match = re.search(
            r'\*\*Primary Goal\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            goals_section,
            re.DOTALL
        )
        if primary_goal_match:
            targets['primary_goal'] = primary_goal_match.group(1).strip()

        # Extract other KPIs
        other_kpis = []
        kpi_section_match = re.search(
            r'\*\*Other KPIs\*\*:?\s*(.+?)(?:\n\*\*|\n##|$)',
            goals_section,
            re.DOTALL
        )
        if kpi_section_match:
            kpi_text = kpi_section_match.group(1)
            # Extract bullet points
            for line in kpi_text.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    other_kpis.append(line[1:].strip())

        if other_kpis:
            targets['other_kpis'] = other_kpis

        return targets

    def _extract_known_issues(self, content: str) -> List[str]:
        """Extract known issues and anomalies to avoid flagging as new problems"""
        known_issues = []

        # Find Known Anomalies section
        anomalies_section = self._extract_section(content, r'###\s*Known Anomalies')
        if anomalies_section:
            # Extract bullet points
            for line in anomalies_section.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('•') or line.startswith('**'):
                    # Clean up markdown formatting
                    issue = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
                    issue = issue.lstrip('- •').strip()
                    if issue:
                        known_issues.append(issue)

        # Also check for active notices/warnings at top of file
        active_notices = re.findall(
            r'##\s*🚨\s*ACTIVE:?\s*(.+?)(?:\n##|$)',
            content,
            re.DOTALL
        )
        for notice in active_notices:
            # Extract first line as issue description
            first_line = notice.split('\n')[0].strip()
            known_issues.append(f"ACTIVE: {first_line}")

        return known_issues

    def _extract_budget_info(self, content: str) -> Dict[str, Any]:
        """Extract budget information"""
        budget = {}

        # Find monthly budget
        monthly_budget_patterns = [
            r'\*\*Monthly Budget\*\*:?\s*[~]?[£\$]([0-9,]+)',
            r'Monthly Budget:?\s*[~]?[£\$]([0-9,]+)',
            r'Budget:?\s*[~]?[£\$]([0-9,]+)/month'
        ]
        for pattern in monthly_budget_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                budget_str = match.group(1).replace(',', '')
                budget['monthly_budget'] = float(budget_str)
                break

        # Check for variable budget
        if 'variable' in content.lower() and 'budget' in content.lower():
            budget['variable_budget'] = True

        # Check for budget constraints/special situations
        if 'budget constraint' in content.lower() or 'lost is budget' in content.lower():
            budget['has_budget_constraints'] = True

        return budget

    def _extract_platform_info(self, content: str) -> Dict[str, Any]:
        """Extract platform and technology information"""
        platform = {}

        # Check for e-commerce platforms
        platforms_map = {
            'shopify': r'shopify',
            'woocommerce': r'woocommerce',
            'magento': r'magento',
            'bigcommerce': r'bigcommerce',
            'prestashop': r'prestashop'
        }

        for platform_name, pattern in platforms_map.items():
            if re.search(pattern, content, re.IGNORECASE):
                platform['ecommerce_platform'] = platform_name
                break

        # Check for feed management tools
        feed_tools_map = {
            'channable': r'channable',
            'datafeedwatch': r'datafeedwatch|data feed watch',
            'feedonomics': r'feedonomics',
            'producthero': r'product\s*hero'
        }

        for tool_name, pattern in feed_tools_map.items():
            if re.search(pattern, content, re.IGNORECASE):
                platform['feed_management'] = tool_name
                break

        # Check for profit tracking tools
        if re.search(r'profitmetrics|profit\s*metrics', content, re.IGNORECASE):
            platform['uses_profit_metrics'] = True

        if re.search(r'northbeam', content, re.IGNORECASE):
            platform['uses_northbeam'] = True

        return platform

    def _extract_account_ids(self, content: str) -> Dict[str, Any]:
        """Extract Google Ads account IDs and structure"""
        account_info = {}

        # Extract customer ID(s)
        customer_ids = re.findall(r'Customer ID\*\*:?\s*(\d{10})', content)
        if customer_ids:
            account_info['customer_ids'] = customer_ids

        # Extract manager ID
        manager_match = re.search(r'Manager.*?ID\*\*:?\s*(\d{10})', content, re.IGNORECASE)
        if manager_match:
            account_info['manager_id'] = manager_match.group(1)

        # Extract merchant centre ID
        merchant_match = re.search(r'Merchant.*?ID\*\*:?\s*(\d+)', content, re.IGNORECASE)
        if merchant_match:
            account_info['merchant_centre_id'] = merchant_match.group(1)

        # Extract GA4 property ID
        ga4_match = re.search(r'GA4.*?ID\*\*:?\s*(\d+)', content, re.IGNORECASE)
        if ga4_match:
            account_info['ga4_property_id'] = ga4_match.group(1)

        return account_info

    def _extract_business_context(self, content: str) -> Dict[str, str]:
        """Extract business context (industry, type, etc.)"""
        business = {}

        # Find Account Overview section
        overview_section = self._extract_section(content, r'##\s*Account Overview')
        if not overview_section:
            return business

        # Extract business type
        business_type_match = re.search(
            r'\*\*Business Type\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            overview_section
        )
        if business_type_match:
            business['business_type'] = business_type_match.group(1).strip()

        # Extract industry
        industry_match = re.search(
            r'\*\*Industry\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            overview_section
        )
        if industry_match:
            business['industry'] = industry_match.group(1).strip()

        # Extract geographic focus
        geo_match = re.search(
            r'\*\*Geographic Focus\*\*:?\s*(.+?)(?:\n\*\*|\n-|\n\n|$)',
            overview_section
        )
        if geo_match:
            business['geographic_focus'] = geo_match.group(1).strip()

        return business

    def _detect_multi_account(self, content: str) -> bool:
        """Detect if client has multiple Google Ads accounts"""
        # Look for multiple account IDs or multi-account structure
        multi_account_indicators = [
            r'multiple.*?accounts?',
            r'separate.*?accounts?',
            r'four.*?accounts?',
            r'Account ID:.*?\d{10}.*?\d{10}',  # Two account IDs close together
            r'UK.*?Account.*?\n.*?USA.*?Account',  # Regional accounts
        ]

        for pattern in multi_account_indicators:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return True

        return False

    def _extract_section(self, content: str, heading_pattern: str) -> Optional[str]:
        """
        Extract content of a markdown section

        Args:
            content: Full markdown content
            heading_pattern: Regex pattern for section heading

        Returns:
            Section content or None if not found
        """
        # Find the heading
        match = re.search(heading_pattern, content, re.IGNORECASE)
        if not match:
            return None

        start_pos = match.end()

        # Find the next heading of same or higher level
        # Assuming ## for main sections, ### for subsections
        heading_level = content[match.start():match.end()].count('#')
        next_heading_pattern = r'\n#{1,' + str(heading_level) + r'}\s+'

        next_match = re.search(next_heading_pattern, content[start_pos:])
        if next_match:
            end_pos = start_pos + next_match.start()
            return content[start_pos:end_pos].strip()
        else:
            # No next heading found, take rest of content
            return content[start_pos:].strip()

    def should_ignore_issue(self, client_context: Dict[str, Any], issue_description: str) -> bool:
        """
        Check if an issue should be ignored based on client context

        Args:
            client_context: Parsed client context
            issue_description: Description of the detected issue

        Returns:
            True if issue matches a known issue and should be ignored
        """
        known_issues = client_context.get('known_issues', [])

        # Check for fuzzy match
        issue_lower = issue_description.lower()
        for known_issue in known_issues:
            known_lower = known_issue.lower()
            # Simple substring matching
            if known_lower in issue_lower or issue_lower in known_lower:
                logger.info(f"Ignoring issue '{issue_description}' - matches known issue: {known_issue}")
                return True

        return False

    def get_applicable_threshold(self, client_context: Dict[str, Any], metric: str) -> Optional[float]:
        """
        Get client-specific threshold for a metric

        Args:
            client_context: Parsed client context
            metric: Metric name ('roas', 'cpa', etc.)

        Returns:
            Threshold value or None if not specified
        """
        targets = client_context.get('performance_targets', {})

        if metric.lower() == 'roas':
            return targets.get('target_roas')
        elif metric.lower() == 'cpa':
            return targets.get('target_cpa')

        return None


# Example usage and testing
if __name__ == '__main__':
    import sys
    import json

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = ClientContextParser()

    # Test with a client if provided
    if len(sys.argv) > 1:
        client_slug = sys.argv[1]
        context = parser.load_client_context(client_slug)
        if context:
            # Remove raw_content for cleaner output
            context_display = {k: v for k, v in context.items() if k != 'raw_content'}
            print(json.dumps(context_display, indent=2))
        else:
            print(f"Could not load context for {client_slug}")
    else:
        print("Usage: python context_parser.py <client-slug>")
        print("Example: python context_parser.py smythson")
