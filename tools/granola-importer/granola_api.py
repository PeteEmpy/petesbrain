"""
Granola API Client

Handles authentication and fetching meeting notes from Granola's API.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import requests


class GranolaAPI:
    """Client for interacting with Granola's API."""

    API_BASE = "https://api.granola.ai/v2"
    CREDENTIALS_PATH = Path.home() / "Library/Application Support/Granola/supabase.json"

    def __init__(self):
        """Initialize API client with credentials from local Granola installation."""
        self.credentials = self._load_credentials()

        # Try to extract access_token from workos_tokens (newer format)
        self.access_token = None
        if "workos_tokens" in self.credentials:
            try:
                workos_tokens = json.loads(self.credentials["workos_tokens"])
                self.access_token = workos_tokens.get("access_token")
            except (json.JSONDecodeError, TypeError):
                pass

        # Fallback to direct access_token field (older format)
        if not self.access_token:
            self.access_token = self.credentials.get("access_token")

        if not self.access_token:
            raise ValueError(
                f"Could not find access token in {self.CREDENTIALS_PATH}. "
                "Please ensure Granola desktop app is installed and you're logged in."
            )

    def _load_credentials(self) -> Dict:
        """Load Granola credentials from local storage."""
        if not self.CREDENTIALS_PATH.exists():
            raise FileNotFoundError(
                f"Granola credentials not found at {self.CREDENTIALS_PATH}. "
                "Please log into Granola desktop app first."
            )

        with open(self.CREDENTIALS_PATH, 'r') as f:
            return json.load(f)

    def _make_request(self, endpoint: str, method: str = "POST", data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Granola API."""
        url = f"{self.API_BASE}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data or {})
            else:
                response = requests.get(url, headers=headers)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise PermissionError(
                    "Granola API authentication failed. Try logging out and back into Granola app."
                )
            raise

    def get_documents(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Fetch meeting documents from Granola.

        Args:
            limit: Maximum number of documents to fetch
            offset: Number of documents to skip (for pagination)

        Returns:
            List of document dictionaries containing meeting data
        """
        data = {
            "limit": limit,
            "offset": offset
        }

        response = self._make_request("get-documents", data=data)
        return response.get("docs", [])

    def get_document_by_id(self, document_id: str) -> Optional[Dict]:
        """
        Fetch a specific meeting document by ID.

        Args:
            document_id: The Granola document ID

        Returns:
            Document dictionary or None if not found
        """
        documents = self.get_documents(limit=1000)  # Fetch more to find specific ID

        for doc in documents:
            if doc.get("id") == document_id:
                return doc

        return None

    def get_recent_documents(self, days: int = 7) -> List[Dict]:
        """
        Fetch documents from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of recent document dictionaries
        """
        from datetime import datetime, timedelta, timezone

        # Use timezone-aware datetime for comparison
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        all_docs = self.get_documents(limit=1000)

        recent_docs = []
        for doc in all_docs:
            # Parse created_at timestamp
            created_str = doc.get("created_at", "")
            if created_str:
                try:
                    created_at = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    if created_at >= cutoff_date:
                        recent_docs.append(doc)
                except ValueError:
                    continue

        return recent_docs


if __name__ == "__main__":
    # Test the API client
    try:
        api = GranolaAPI()
        print(f"✓ Successfully authenticated with Granola API")
        print(f"✓ Credentials loaded from: {api.CREDENTIALS_PATH}")

        docs = api.get_documents(limit=5)
        print(f"\n✓ Fetched {len(docs)} recent meetings:")

        for i, doc in enumerate(docs, 1):
            title = doc.get("title", "Untitled")
            created = doc.get("created_at", "Unknown date")
            print(f"  {i}. {title} ({created})")

    except Exception as e:
        print(f"✗ Error: {e}")
