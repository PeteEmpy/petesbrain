#!/usr/bin/env python3
"""
Cross-Client Pattern Detection

Analyzes patterns across all clients to detect platform-wide issues,
seasonal trends, and systemic problems.

Patterns detected:
- Hero count drops across multiple clients (possible GMC policy change)
- Revenue spikes/drops across multiple clients (market trends)
- Label transition patterns (Zombies → Heroes across clients)
- Disapproval spikes (GMC/Google Ads policy enforcement)

Usage:
    from cross_client_detector import CrossClientDetector

    detector = CrossClientDetector()
    patterns = detector.detect_patterns(client_snapshots)
    detector.generate_alert_if_needed(patterns)
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class CrossClientPattern:
    """Detected pattern across multiple clients"""
    pattern_type: str  # hero_drop, revenue_spike, disapproval_surge, label_shift
    severity: str  # critical, warning, info
    affected_clients: List[str]
    description: str
    metric_changes: Dict[str, float]  # {client: change_value}
    possible_cause: str
    recommended_action: str
    timestamp: str


class CrossClientDetector:
    """
    Detects patterns across multiple clients to identify platform-wide issues.

    Useful for catching:
    - Google Merchant Centre policy changes
    - Google Ads algorithm updates
    - Seasonal market trends
    - Systemic technical issues
    """

    def __init__(self):
        """Initialize detector"""
        self.min_clients_threshold = 3  # Minimum clients affected to trigger pattern

    def detect_patterns(
        self,
        current_snapshots: Dict[str, Dict],
        previous_snapshots: Dict[str, Dict]
    ) -> List[CrossClientPattern]:
        """
        Detect cross-client patterns.

        Args:
            current_snapshots: Dict of {client: {metrics}}
            previous_snapshots: Dict of {client: {metrics}}

        Returns:
            List of detected patterns
        """
        patterns = []

        # Pattern 1: Hero count drops across multiple clients
        hero_drop_pattern = self._detect_hero_drops(current_snapshots, previous_snapshots)
        if hero_drop_pattern:
            patterns.append(hero_drop_pattern)

        # Pattern 2: Revenue changes across multiple clients
        revenue_pattern = self._detect_revenue_trends(current_snapshots, previous_snapshots)
        if revenue_pattern:
            patterns.append(revenue_pattern)

        # Pattern 3: Disapproval spikes
        disapproval_pattern = self._detect_disapproval_surge(current_snapshots, previous_snapshots)
        if disapproval_pattern:
            patterns.append(disapproval_pattern)

        # Pattern 4: Label transitions (Zombies → Heroes)
        label_pattern = self._detect_label_shifts(current_snapshots, previous_snapshots)
        if label_pattern:
            patterns.append(label_pattern)

        return patterns

    def _detect_hero_drops(
        self,
        current: Dict[str, Dict],
        previous: Dict[str, Dict]
    ) -> Optional[CrossClientPattern]:
        """Detect Hero count drops across multiple clients"""
        affected_clients = []
        metric_changes = {}

        for client, curr_data in current.items():
            if client not in previous:
                continue

            curr_hero_count = curr_data.get('hero_count', 0)
            prev_hero_count = previous[client].get('hero_count', 0)

            if prev_hero_count == 0:
                continue

            # Calculate percentage drop
            drop_pct = ((curr_hero_count - prev_hero_count) / prev_hero_count) * 100

            # Threshold: 20% or more drop
            if drop_pct <= -20:
                affected_clients.append(client)
                metric_changes[client] = drop_pct

        # Trigger if 3+ clients affected
        if len(affected_clients) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="hero_drop",
                severity="critical" if len(affected_clients) >= 5 else "warning",
                affected_clients=affected_clients,
                description=f"{len(affected_clients)} clients saw Hero count drops ≥20%",
                metric_changes=metric_changes,
                possible_cause="Possible Google Merchant Centre policy change or algorithm update",
                recommended_action="Review disapprovals in GMC, check for new policy announcements, verify Product Hero app status",
                timestamp=datetime.now().isoformat()
            )

        return None

    def _detect_revenue_trends(
        self,
        current: Dict[str, Dict],
        previous: Dict[str, Dict]
    ) -> Optional[CrossClientPattern]:
        """Detect significant revenue changes across multiple clients"""
        revenue_drops = []
        revenue_spikes = []
        metric_changes = {}

        for client, curr_data in current.items():
            if client not in previous:
                continue

            curr_revenue = curr_data.get('total_revenue', 0)
            prev_revenue = previous[client].get('total_revenue', 0)

            if prev_revenue == 0:
                continue

            change_pct = ((curr_revenue - prev_revenue) / prev_revenue) * 100

            # Threshold: ±30% change
            if change_pct <= -30:
                revenue_drops.append(client)
                metric_changes[client] = change_pct
            elif change_pct >= 30:
                revenue_spikes.append(client)
                metric_changes[client] = change_pct

        # Check for drops
        if len(revenue_drops) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="revenue_drop",
                severity="critical",
                affected_clients=revenue_drops,
                description=f"{len(revenue_drops)} clients saw revenue drops ≥30%",
                metric_changes=metric_changes,
                possible_cause="Market trend (seasonal decline, economic shift), or platform issue",
                recommended_action="Investigate market conditions, check for seasonal patterns, review ad delivery",
                timestamp=datetime.now().isoformat()
            )

        # Check for spikes
        if len(revenue_spikes) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="revenue_spike",
                severity="info",
                affected_clients=revenue_spikes,
                description=f"{len(revenue_spikes)} clients saw revenue spikes ≥30%",
                metric_changes=metric_changes,
                possible_cause="Seasonal trend (holiday shopping, promotions), or market opportunity",
                recommended_action="Analyse what's driving growth, consider scaling successful tactics across clients",
                timestamp=datetime.now().isoformat()
            )

        return None

    def _detect_disapproval_surge(
        self,
        current: Dict[str, Dict],
        previous: Dict[str, Dict]
    ) -> Optional[CrossClientPattern]:
        """Detect disapproval spikes across multiple clients"""
        affected_clients = []
        metric_changes = {}

        for client, curr_data in current.items():
            if client not in previous:
                continue

            curr_disapprovals = curr_data.get('disapproved_count', 0)
            prev_disapprovals = previous[client].get('disapproved_count', 0)

            # Absolute threshold: 5+ new disapprovals
            new_disapprovals = curr_disapprovals - prev_disapprovals

            if new_disapprovals >= 5:
                affected_clients.append(client)
                metric_changes[client] = new_disapprovals

        # Trigger if 3+ clients affected
        if len(affected_clients) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="disapproval_surge",
                severity="critical",
                affected_clients=affected_clients,
                description=f"{len(affected_clients)} clients saw 5+ new product disapprovals",
                metric_changes=metric_changes,
                possible_cause="Google Merchant Centre policy enforcement (new policy or algorithm change)",
                recommended_action="Check GMC policy announcements, review disapproval reasons, update product data",
                timestamp=datetime.now().isoformat()
            )

        return None

    def _detect_label_shifts(
        self,
        current: Dict[str, Dict],
        previous: Dict[str, Dict]
    ) -> Optional[CrossClientPattern]:
        """Detect significant label transitions across clients"""
        zombie_to_hero = []
        hero_to_zombie = []
        metric_changes = {}

        for client, curr_data in current.items():
            if client not in previous:
                continue

            # Count products that shifted Zombie → Hero
            curr_heroes = curr_data.get('hero_products', set())
            prev_zombies = previous[client].get('zombie_products', set())
            zombie_upgrades = len(curr_heroes & prev_zombies)

            # Count products that shifted Hero → Zombie
            curr_zombies = curr_data.get('zombie_products', set())
            prev_heroes = previous[client].get('hero_products', set())
            hero_downgrades = len(curr_zombies & prev_heroes)

            if zombie_upgrades >= 10:
                zombie_to_hero.append(client)
                metric_changes[f"{client}_upgrades"] = zombie_upgrades

            if hero_downgrades >= 10:
                hero_to_zombie.append(client)
                metric_changes[f"{client}_downgrades"] = hero_downgrades

        # Positive pattern: Multiple clients see Zombies becoming Heroes
        if len(zombie_to_hero) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="label_upgrade_wave",
                severity="info",
                affected_clients=zombie_to_hero,
                description=f"{len(zombie_to_hero)} clients saw 10+ Zombies upgrade to Heroes",
                metric_changes=metric_changes,
                possible_cause="Successful optimization, seasonal demand increase, or improved product offerings",
                recommended_action="Analyse what changed, replicate success across other clients",
                timestamp=datetime.now().isoformat()
            )

        # Negative pattern: Multiple clients see Heroes becoming Zombies
        if len(hero_to_zombie) >= self.min_clients_threshold:
            return CrossClientPattern(
                pattern_type="label_downgrade_wave",
                severity="warning",
                affected_clients=hero_to_zombie,
                description=f"{len(hero_to_zombie)} clients saw 10+ Heroes downgrade to Zombies",
                metric_changes=metric_changes,
                possible_cause="Market shift, increased competition, or Product Hero recalibration",
                recommended_action="Review product performance, check for external market changes, verify Product Hero settings",
                timestamp=datetime.now().isoformat()
            )

        return None

    def generate_html_section(self, patterns: List[CrossClientPattern]) -> str:
        """
        Generate HTML section for cross-client patterns.

        Args:
            patterns: List of detected patterns

        Returns:
            HTML string
        """
        if not patterns:
            return """
            <h3>Cross-Client Pattern Analysis</h3>
            <p>✅ No significant cross-client patterns detected. All clients performing independently.</p>
            """

        html = """
        <h3>⚠️ Cross-Client Pattern Analysis</h3>
        <p>The following patterns were detected across multiple clients:</p>
        """

        for pattern in patterns:
            severity_color = {
                'critical': '#DC2626',
                'warning': '#F59E0B',
                'info': '#059669'
            }.get(pattern.severity, '#6B7280')

            html += f"""
            <div style="border-left: 4px solid {severity_color}; background: #F9FAFB; padding: 15px; margin: 20px 0;">
                <h4 style="color: {severity_color}; margin: 0 0 10px 0;">
                    {pattern.severity.upper()}: {pattern.description}
                </h4>
                <p><strong>Affected Clients ({len(pattern.affected_clients)}):</strong> {', '.join(pattern.affected_clients)}</p>
                <p><strong>Possible Cause:</strong> {pattern.possible_cause}</p>
                <p><strong>Recommended Action:</strong> {pattern.recommended_action}</p>

                <table style="margin-top: 10px; width: 100%;">
                    <tr>
                        <th>Client</th>
                        <th>Change</th>
                    </tr>
            """

            for client, change in pattern.metric_changes.items():
                change_str = f"{change:+.1f}%" if isinstance(change, float) else str(change)
                html += f"""
                    <tr>
                        <td>{client}</td>
                        <td>{change_str}</td>
                    </tr>
                """

            html += """
                </table>
            </div>
            """

        return html


if __name__ == "__main__":
    # Test the detector
    print("Testing Cross-Client Pattern Detector...")

    # Mock data: 5 clients all see Hero drops
    current_data = {
        'Client A': {'hero_count': 40, 'total_revenue': 5000},
        'Client B': {'hero_count': 35, 'total_revenue': 4500},
        'Client C': {'hero_count': 30, 'total_revenue': 4000},
        'Client D': {'hero_count': 25, 'total_revenue': 3500},
        'Client E': {'hero_count': 20, 'total_revenue': 3000}
    }

    previous_data = {
        'Client A': {'hero_count': 50, 'total_revenue': 5100},
        'Client B': {'hero_count': 50, 'total_revenue': 4600},
        'Client C': {'hero_count': 45, 'total_revenue': 4100},
        'Client D': {'hero_count': 40, 'total_revenue': 3600},
        'Client E': {'hero_count': 35, 'total_revenue': 3100}
    }

    detector = CrossClientDetector()
    patterns = detector.detect_patterns(current_data, previous_data)

    print(f"\nDetected {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"\n  Pattern: {pattern.pattern_type}")
        print(f"  Severity: {pattern.severity}")
        print(f"  Affected: {len(pattern.affected_clients)} clients")
        print(f"  Description: {pattern.description}")
        print(f"  Possible cause: {pattern.possible_cause}")
