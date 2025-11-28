#!/usr/bin/env python3
"""
Label Inference Module - Historical Label Reconstruction

Infers Product Hero labels for historical dates (before Nov 1, 2025)
based on campaign naming conventions and performance data.

Key patterns (ROK standard across all e-commerce clients):
- "H&S" or "Heroes & Sidekicks" → heroes or sidekicks
- "Zombies" (standalone) → zombies
- "Villains" (standalone) → villains
- "H&S Zombies" → heroes, sidekicks, or zombies
- "Villains and Zombies" → villains or zombies
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class LabelConfidence(Enum):
    """Confidence levels for label inference"""
    ACTUAL = "actual"          # From Product Hero (Nov 1+)
    HIGH = "high"              # 80-90% confidence
    MEDIUM = "medium"          # 60-80% confidence
    LOW = "low"                # 40-60% confidence
    UNKNOWN = "unknown"        # No data available

@dataclass
class InferredLabel:
    """Result of label inference"""
    label: str                 # heroes, sidekicks, villains, zombies, or composite
    confidence: LabelConfidence
    method: str                # How label was determined
    evidence: Dict             # Supporting data
    caveat: Optional[str] = None  # Warning about limitations

    def __str__(self):
        if self.confidence == LabelConfidence.ACTUAL:
            return f"{self.label} (actual)"
        else:
            return f"{self.label} (inferred, {self.confidence.value} confidence)"

class LabelInferencer:
    """
    Infers Product Hero labels from campaign names and performance data.
    """

    # Campaign name patterns (case-insensitive)
    PATTERNS = {
        # Clear single-label patterns (HIGH confidence)
        "zombies_only": [
            r"\bZombies\b(?!.*(?:H&S|Heroes|Sidekicks|Villains))",
            r"\bZombie\b(?!.*(?:H&S|Heroes|Sidekicks|Villains))"
        ],
        "villains_only": [
            r"\bVillains\b(?!.*(?:H&S|Heroes|Sidekicks|Zombies))",
            r"\bVillain\b(?!.*(?:H&S|Heroes|Sidekicks|Zombies))"
        ],
        "heroes_only": [
            r"\bHeroes\b(?!.*(?:Sidekicks|Villains|Zombies))",
            r"\bHero\b(?!.*(?:Sidekicks|Villains|Zombies))"
        ],
        "sidekicks_only": [
            r"\bSidekicks\b(?!.*(?:Heroes|Villains|Zombies))",
            r"\bSidekick\b(?!.*(?:Heroes|Villains|Zombies))"
        ],

        # Two-label patterns (MEDIUM confidence)
        "heroes_sidekicks": [
            r"H&S\b",
            r"H & S\b",
            r"Heroes?\s*&\s*Sidekicks?",
            r"Heroes?\s+and\s+Sidekicks?"
        ],
        "villains_zombies": [
            r"Villains?\s*&\s*Zombies?",
            r"Villains?\s+and\s+Zombies?"
        ],

        # Three-label patterns (LOW confidence)
        "heroes_sidekicks_zombies": [
            r"H&S.*Zombies?",
            r"H & S.*Zombies?",
            r"Heroes?\s*&\s*Sidekicks?.*Zombies?",
            r"Zombies?.*H&S"
        ]
    }

    def __init__(self, assessment_window_days: int = 30):
        """
        Initialize inferencer.

        Args:
            assessment_window_days: Product Hero's assessment window
                                   (30 days standard, 60 for AFH)
        """
        self.assessment_window_days = assessment_window_days

    def infer_from_campaign_name(self, campaign_name: str) -> Tuple[List[str], LabelConfidence]:
        """
        Infer possible labels from campaign name.

        Returns: (list of possible labels, confidence level)
        """
        campaign_name = campaign_name or ""

        # Check patterns in order of specificity
        # Standalone labels first (highest confidence)
        if self._matches_any(campaign_name, self.PATTERNS["zombies_only"]):
            return (["zombies"], LabelConfidence.HIGH)

        if self._matches_any(campaign_name, self.PATTERNS["villains_only"]):
            return (["villains"], LabelConfidence.HIGH)

        if self._matches_any(campaign_name, self.PATTERNS["heroes_only"]):
            return (["heroes"], LabelConfidence.HIGH)

        if self._matches_any(campaign_name, self.PATTERNS["sidekicks_only"]):
            return (["sidekicks"], LabelConfidence.HIGH)

        # Two-label combinations
        if self._matches_any(campaign_name, self.PATTERNS["heroes_sidekicks"]):
            return (["heroes", "sidekicks"], LabelConfidence.MEDIUM)

        if self._matches_any(campaign_name, self.PATTERNS["villains_zombies"]):
            return (["villains", "zombies"], LabelConfidence.MEDIUM)

        # Three-label combinations
        if self._matches_any(campaign_name, self.PATTERNS["heroes_sidekicks_zombies"]):
            return (["heroes", "sidekicks", "zombies"], LabelConfidence.LOW)

        # No match
        return ([], LabelConfidence.UNKNOWN)

    def refine_with_performance(
        self,
        possible_labels: List[str],
        performance_data: Dict
    ) -> Tuple[str, LabelConfidence]:
        """
        Refine label guess using performance metrics.

        Args:
            possible_labels: Labels inferred from campaign name
            performance_data: {
                "clicks_30d": int,
                "conversions_30d": float,
                "revenue_30d": float
            }

        Returns: (best_guess_label, refined_confidence)
        """
        if not possible_labels:
            return ("unknown", LabelConfidence.UNKNOWN)

        if len(possible_labels) == 1:
            # Already specific, no refinement needed
            return (possible_labels[0], LabelConfidence.HIGH)

        # Extract metrics
        clicks = performance_data.get("clicks_30d", 0)
        conversions = performance_data.get("conversions_30d", 0)
        revenue = performance_data.get("revenue_30d", 0)

        # Refinement heuristics
        # Note: These are approximations, not Product Hero's exact logic

        if "heroes" in possible_labels and "sidekicks" in possible_labels:
            # Distinguish between hero and sidekick
            # Hero: High conversions + high revenue
            # Sidekick: Low/moderate conversions but converts when it gets traffic

            if conversions >= 10 and revenue >= 1000:
                return ("heroes", LabelConfidence.MEDIUM)
            elif conversions >= 1:
                return ("sidekicks", LabelConfidence.MEDIUM)
            elif clicks < 5:
                return ("zombies", LabelConfidence.LOW)  # Low traffic suggests zombie
            else:
                # Can't distinguish - return composite
                return ("heroes_or_sidekicks", LabelConfidence.MEDIUM)

        if "villains" in possible_labels and "zombies" in possible_labels:
            # Villain: Clicks but no conversions
            # Zombie: No clicks, no conversions

            if clicks > 50 and conversions == 0:
                return ("villains", LabelConfidence.MEDIUM)
            elif clicks < 10:
                return ("zombies", LabelConfidence.MEDIUM)
            else:
                return ("villains_or_zombies", LabelConfidence.LOW)

        if len(possible_labels) == 3:  # H&S Zombies
            # Try to narrow down
            if clicks > 100 and conversions >= 5:
                return ("heroes", LabelConfidence.LOW)
            elif conversions >= 1:
                return ("sidekicks", LabelConfidence.LOW)
            elif clicks < 10:
                return ("zombies", LabelConfidence.LOW)
            else:
                return ("heroes_sidekicks_or_zombies", LabelConfidence.LOW)

        # Fallback: return all possibilities as composite label
        composite = "_or_".join(possible_labels)
        return (composite, LabelConfidence.LOW)

    def infer_label(
        self,
        product_id: str,
        date: str,
        campaign_name: str,
        performance_data: Optional[Dict] = None
    ) -> InferredLabel:
        """
        Infer Product Hero label for a product on a specific date.

        Args:
            product_id: Product ID
            date: Date (YYYY-MM-DD)
            campaign_name: Name of campaign product was in
            performance_data: Performance metrics (optional, improves accuracy)

        Returns: InferredLabel with confidence and evidence
        """
        # Step 1: Infer from campaign name
        possible_labels, campaign_confidence = self.infer_from_campaign_name(campaign_name)

        evidence = {
            "campaign": campaign_name,
            "possible_labels_from_campaign": possible_labels
        }

        # Step 2: Refine with performance data if available
        if performance_data and possible_labels:
            label, refined_confidence = self.refine_with_performance(
                possible_labels,
                performance_data
            )
            evidence.update(performance_data)
        elif possible_labels:
            if len(possible_labels) == 1:
                label = possible_labels[0]
                refined_confidence = campaign_confidence
            else:
                label = "_or_".join(possible_labels)
                refined_confidence = campaign_confidence
        else:
            label = "unknown"
            refined_confidence = LabelConfidence.UNKNOWN

        # Add caveat for historical inferred labels
        caveat = (
            "Inferred from campaign name. Actual Product Hero labels "
            "not available for dates before Nov 1, 2025."
        )

        return InferredLabel(
            label=label,
            confidence=refined_confidence,
            method="campaign_name_inference",
            evidence=evidence,
            caveat=caveat
        )

    def _matches_any(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any of the given regex patterns"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

def main():
    """Test the inference logic with examples"""
    inferencer = LabelInferencer(assessment_window_days=30)

    # Test cases
    test_cases = [
        {
            "campaign": "AFH | P Max | H&S Zombies Furniture",
            "performance": {"clicks_30d": 95, "conversions_30d": 0, "revenue_30d": 0}
        },
        {
            "campaign": "Tree2mydoor | Zombies Activation",
            "performance": {"clicks_30d": 5, "conversions_30d": 0, "revenue_30d": 0}
        },
        {
            "campaign": "Superspace | Heroes & Sidekicks | Furniture",
            "performance": {"clicks_30d": 250, "conversions_30d": 12, "revenue_30d": 1800}
        },
        {
            "campaign": "AFH | Villains Budget Test",
            "performance": {"clicks_30d": 120, "conversions_30d": 0, "revenue_30d": 0}
        },
        {
            "campaign": "SMY | UK | H&S | Stationery",
            "performance": {"clicks_30d": 45, "conversions_30d": 2, "revenue_30d": 280}
        }
    ]

    print("Label Inference Test Cases")
    print("="*60)

    for i, test in enumerate(test_cases, 1):
        result = inferencer.infer_label(
            product_id=f"TEST_{i}",
            date="2025-10-22",
            campaign_name=test["campaign"],
            performance_data=test["performance"]
        )

        print(f"\nTest {i}:")
        print(f"  Campaign: {test['campaign']}")
        print(f"  Performance: {test['performance']}")
        print(f"  Inferred Label: {result.label}")
        print(f"  Confidence: {result.confidence.value}")
        print(f"  Evidence: {result.evidence}")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
