"""
Client Name Detector

Automatically detects which client a meeting belongs to based on meeting title
using fuzzy string matching.
"""

import os
from pathlib import Path
from typing import Optional, List, Tuple, Dict
from thefuzz import fuzz, process
import yaml


class ClientDetector:
    """Detects client names from meeting titles using fuzzy matching."""

    def __init__(self, clients_dir: Optional[Path] = None):
        """
        Initialize client detector.

        Args:
            clients_dir: Path to clients directory (defaults to ../../clients from this file)
        """
        if clients_dir is None:
            # Default to clients/ directory relative to this tool
            tool_dir = Path(__file__).parent
            self.clients_dir = tool_dir.parent.parent / "clients"
        else:
            self.clients_dir = Path(clients_dir)

        self.tool_dir = Path(__file__).parent
        self.clients = self._load_clients()
        self.client_variations = self._build_client_variations()
        self.domain_mappings = self._load_domain_mappings()
        self.title_mappings = self._load_title_mappings()

    def _load_clients(self) -> List[str]:
        """
        Load list of client folder names from the clients directory.

        Returns:
            List of client folder names (slugs)
        """
        if not self.clients_dir.exists():
            print(f"Warning: Clients directory not found at {self.clients_dir}")
            return []

        clients = []
        for item in self.clients_dir.iterdir():
            if item.is_dir() and not item.name.startswith(("_", ".")):
                clients.append(item.name)

        return sorted(clients)

    def _load_domain_mappings(self) -> Dict[str, str]:
        """
        Load manual email domain to client mappings from YAML file.

        Returns:
            Dictionary mapping email domains to client slugs
        """
        mappings_file = self.tool_dir / "domain_mappings.yaml"

        if not mappings_file.exists():
            return {}

        try:
            with open(mappings_file, 'r') as f:
                mappings = yaml.safe_load(f)
                if not isinstance(mappings, dict):
                    return {}
                return {k.lower(): v for k, v in mappings.items() if k and v}
        except Exception as e:
            print(f"Warning: Could not load domain mappings: {e}")
            return {}

    def _load_title_mappings(self) -> Dict[str, str]:
        """
        Load manual title pattern to client mappings from YAML file.

        These are exact pattern matches (case-insensitive) that override fuzzy matching.
        Useful for abbreviations like "NDA" → "national-design-academy".

        Returns:
            Dictionary mapping title patterns to client slugs
        """
        mappings_file = self.tool_dir / "title_mappings.yaml"

        if not mappings_file.exists():
            return {}

        try:
            with open(mappings_file, 'r') as f:
                mappings = yaml.safe_load(f)
                if not isinstance(mappings, dict):
                    return {}
                return {k.lower(): v for k, v in mappings.items() if k and v}
        except Exception as e:
            print(f"Warning: Could not load title mappings: {e}")
            return {}

    def _build_client_variations(self) -> dict:
        """
        Build a mapping of client names to their variations for better matching.

        Returns:
            Dictionary mapping client slugs to list of name variations
        """
        variations = {}

        for client_slug in self.clients:
            # Generate variations
            client_variations = [
                client_slug,  # e.g., "bright-minds"
                client_slug.replace("-", " "),  # e.g., "bright minds"
                client_slug.replace("-", ""),  # e.g., "brightminds"
                client_slug.title().replace("-", " "),  # e.g., "Bright Minds"
                client_slug.title().replace("-", ""),  # e.g., "BrightMinds"
            ]

            # Add individual words for partial matching
            words = client_slug.split("-")
            if len(words) > 1:
                # Add capitalized version of each word
                for word in words:
                    if len(word) > 3:  # Only add significant words
                        client_variations.append(word.capitalize())

            variations[client_slug] = list(set(client_variations))

        return variations

    def detect_client(self, meeting_title: str, threshold: int = 60,
                     meeting_content: Optional[str] = None, content_threshold: int = 70,
                     attendee_emails: Optional[List[str]] = None) -> Optional[str]:
        """
        Detect which client a meeting belongs to based on attendee emails, title, and content.

        Args:
            meeting_title: The meeting title to analyze
            threshold: Minimum fuzzy match score (0-100) for title matching
            meeting_content: Optional meeting content to analyze if title fails
            content_threshold: Minimum score for content-based matching (higher threshold)
            attendee_emails: Optional list of attendee email addresses

        Returns:
            Client slug (folder name) or None if no match found
        """
        if not meeting_title or not self.clients:
            return None

        # PRIORITY 1: Match by attendee email domains (most accurate!)
        if attendee_emails:
            email_match = self._match_email_domains(attendee_emails)
            if email_match:
                return email_match

        # PRIORITY 2: Match against title
        best_match, best_score = self._match_text(meeting_title, threshold)

        if best_match:
            return best_match

        # PRIORITY 3: Match against content if provided
        if meeting_content:
            content_match, content_score = self._match_content(meeting_content, content_threshold)
            if content_match:
                return content_match

        return None

    def _match_email_domains(self, emails: List[str]) -> Optional[str]:
        """
        Match client based on attendee email domains.
        This is the most accurate method when Granola folders are used.

        Args:
            emails: List of attendee email addresses

        Returns:
            Client slug if matched, None otherwise
        """
        if not emails:
            return None

        # PRIORITY 1: Check manual domain mappings first (most accurate!)
        for email in emails:
            if '@' in email:
                domain = email.split('@')[1].lower()
                if domain in self.domain_mappings:
                    mapped_client = self.domain_mappings[domain]
                    # Verify the mapped client exists
                    if mapped_client in self.clients:
                        return mapped_client

        # PRIORITY 2: Extract domains and do fuzzy matching
        domains = []
        for email in emails:
            if '@' in email:
                domain = email.split('@')[1].lower()
                # Remove common TLDs to get company name
                domain_parts = domain.replace('.com', '').replace('.co.uk', '').replace('.net', '').replace('.org', '')
                domains.append(domain_parts)

        # Try to match each domain against client names
        for domain in domains:
            # Direct match attempt
            for client_slug in self.clients:
                client_name_clean = client_slug.replace('-', '').lower()
                domain_clean = domain.replace('.', '').replace('-', '').lower()

                # Check if domain contains client name or vice versa
                if client_name_clean in domain_clean or domain_clean in client_name_clean:
                    # Verify it's a strong match (not just a substring)
                    if len(client_name_clean) >= 4:  # Avoid short false positives
                        return client_slug

            # Fuzzy match as fallback
            for client_slug, variations in self.client_variations.items():
                for variation in variations:
                    variation_clean = variation.replace(' ', '').replace('-', '').lower()
                    domain_clean = domain.replace('.', '').replace('-', '').lower()

                    similarity = fuzz.ratio(variation_clean, domain_clean)
                    if similarity >= 80:  # High threshold for email matching
                        return client_slug

        return None

    def _match_text(self, text: str, threshold: int = 60) -> Tuple[Optional[str], int]:
        """
        Match text against client variations.

        Args:
            text: Text to analyze
            threshold: Minimum score to consider a match

        Returns:
            Tuple of (client_slug, score)
        """
        if not text:
            return None, 0

        # PRIORITY 1: Check title mappings for exact pattern matches (case-insensitive)
        # This catches abbreviations and ambiguous cases before fuzzy matching
        text_lower = text.lower()
        for pattern, client_slug in self.title_mappings.items():
            if pattern in text_lower:
                # Verify the mapped client exists
                if client_slug in self.clients:
                    return client_slug, 100  # Perfect match via title mapping

        best_match = None
        best_score = 0

        # PRIORITY 2: Try matching against each client's variations using fuzzy matching
        for client_slug, variations in self.client_variations.items():
            for variation in variations:
                # Try different fuzzy matching algorithms
                scores = [
                    fuzz.partial_ratio(text.lower(), variation.lower()),
                    fuzz.token_sort_ratio(text.lower(), variation.lower()),
                    fuzz.token_set_ratio(text.lower(), variation.lower()),
                ]

                max_score = max(scores)

                if max_score > best_score:
                    best_score = max_score
                    best_match = client_slug

        # Return match only if it exceeds threshold
        if best_score >= threshold:
            return best_match, best_score

        return None, best_score

    def _match_content(self, content: str, threshold: int = 70) -> Tuple[Optional[str], int]:
        """
        Analyze meeting content to detect client mentions.
        Uses a higher threshold since content matching is less reliable.

        Args:
            content: Meeting content (notes or transcript)
            threshold: Minimum score to consider a match

        Returns:
            Tuple of (client_slug, score)
        """
        if not content or len(content) < 50:  # Need sufficient content
            return None, 0

        # Take first 1000 chars for analysis (avoid processing huge transcripts)
        content_sample = content[:1000].lower()

        best_match = None
        best_score = 0
        match_count = {}  # Count mentions of each client

        # Count how many times each client variation appears
        for client_slug, variations in self.client_variations.items():
            count = 0
            total_score = 0

            for variation in variations:
                variation_lower = variation.lower()

                # Count direct mentions
                count += content_sample.count(variation_lower)

                # Also check fuzzy match for phrases containing the variation
                sentences = content_sample.split(".")
                for sentence in sentences:
                    if len(sentence) > 10:  # Only check substantial sentences
                        score = fuzz.partial_ratio(sentence, variation_lower)
                        if score > 80:  # High confidence phrase match
                            total_score += score

            if count > 0:
                match_count[client_slug] = (count, total_score)

        # Find client with most mentions
        if match_count:
            best_client = max(match_count.items(), key=lambda x: (x[1][0], x[1][1]))
            client_slug, (count, total_score) = best_client

            # Calculate confidence score based on mentions and fuzzy scores
            confidence = min(100, (count * 20) + (total_score // len(match_count)))

            if confidence >= threshold:
                return client_slug, confidence

        return None, 0

    def detect_with_confidence(self, meeting_title: str, meeting_content: Optional[str] = None,
                              attendee_emails: Optional[List[str]] = None) -> Tuple[Optional[str], int, str]:
        """
        Detect client and return confidence score with detection method.

        Args:
            meeting_title: The meeting title to analyze
            meeting_content: Optional meeting content for fallback detection
            attendee_emails: Optional list of attendee email addresses

        Returns:
            Tuple of (client_slug, confidence_score, detection_method) where:
            - client_slug: Detected client or None
            - confidence_score: 0-100
            - detection_method: "email", "title", "content", or "none"
        """
        if not meeting_title or not self.clients:
            return None, 0, "none"

        # PRIORITY 1: Try email domain matching (most accurate!)
        if attendee_emails:
            email_match = self._match_email_domains(attendee_emails)
            if email_match:
                return email_match, 95, "email"  # High confidence for email matches

        # PRIORITY 2: Try title-based detection
        title_match, title_score = self._match_text(meeting_title)

        if title_match:
            return title_match, title_score, "title"

        # PRIORITY 3: Fall back to content-based detection
        if meeting_content:
            content_match, content_score = self._match_content(meeting_content)
            if content_match:
                return content_match, content_score, "content"

        return None, 0, "none"

    def get_all_clients(self) -> List[str]:
        """
        Get list of all available clients.

        Returns:
            List of client slugs
        """
        return self.clients.copy()

    def get_client_display_name(self, client_slug: str) -> str:
        """
        Convert client slug to display name.

        Args:
            client_slug: Client folder name (e.g., "bright-minds")

        Returns:
            Display name (e.g., "Bright Minds")
        """
        return client_slug.replace("-", " ").title()


def interactive_client_selection(detector: ClientDetector, meeting_title: str) -> Optional[str]:
    """
    Interactively prompt user to select a client when auto-detection fails.

    Args:
        detector: ClientDetector instance
        meeting_title: Meeting title for context

    Returns:
        Selected client slug or None for unassigned
    """
    print(f"\n🔍 Could not auto-detect client for: '{meeting_title}'")
    print("\nAvailable clients:")

    clients = detector.get_all_clients()
    for i, client_slug in enumerate(clients, 1):
        display_name = detector.get_client_display_name(client_slug)
        print(f"  {i}. {display_name}")

    print(f"  0. Leave unassigned (save to _unassigned folder)")

    while True:
        try:
            choice = input("\nSelect client number (0-{}): ".format(len(clients)))
            choice_num = int(choice)

            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(clients):
                return clients[choice_num - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None


if __name__ == "__main__":
    # Test client detection
    detector = ClientDetector()

    print(f"Loaded {len(detector.get_all_clients())} clients:")
    for client in detector.get_all_clients():
        print(f"  - {detector.get_client_display_name(client)}")

    # Test some meeting titles
    test_titles = [
        "Bright Minds Q4 Strategy Review",
        "Uno Lighting Product Launch Discussion",
        "Call with Devonshire Hotels team",
        "Weekly standup",
        "Smythson Brand Guidelines Review",
        "Tree2mydoor Logistics Planning",
    ]

    print("\n" + "=" * 60)
    print("Testing client detection:")
    print("=" * 60)

    for title in test_titles:
        client, confidence, method = detector.detect_with_confidence(title)
        if client:
            display = detector.get_client_display_name(client)
            print(f"✓ '{title}'")
            print(f"  → {display} ({confidence}% confidence via {method})")
        else:
            print(f"✗ '{title}'")
            print(f"  → No match found")
        print()

    # Test content-based detection
    print("\n" + "=" * 60)
    print("Testing content-based detection:")
    print("=" * 60)

    test_content = """
    We had a great discussion about the upcoming Bright Minds campaign.
    The team at Bright Minds is excited about the Q4 launch.
    We'll be working closely with their marketing director.
    """

    client, confidence, method = detector.detect_with_confidence(
        "Weekly Strategy Call",  # Generic title
        meeting_content=test_content
    )

    if client:
        display = detector.get_client_display_name(client)
        print(f"✓ Generic title + content analysis")
        print(f"  → {display} ({confidence}% confidence via {method})")
    else:
        print(f"✗ Could not detect client from content")
    print()
