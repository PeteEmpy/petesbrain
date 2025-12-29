#!/usr/bin/env python3
"""
Smart Zombie Reactivation Scorer

Scores Zombie products on "reactivation probability" to prioritise which ones
are worth re-investing in (vs permanently retiring).

Scoring Factors:
- Historical Hero status (+50 points) - Was this a Hero in past 90 days?
- Historical conversion rate (+30 points) - High conversion rate when active?
- Stock recently restored (+20 points) - Back in stock after outage?
- Price competitive vs baseline (+20 points) - Pricing not the issue?
- Recent click activity (+10 points) - Still getting organic interest?

Output: "Top 10 Zombies to Reactivate" weekly report

Usage:
    from zombie_reactivation_scorer import ZombieReactivationScorer

    scorer = ZombieReactivationScorer()
    scored_zombies = scorer.score_zombies(client_name, zombie_products)
    top_candidates = scored_zombies[:10]
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class ZombieScore:
    """Zombie reactivation score result"""
    product_id: str
    product_title: str
    total_score: int
    max_score: int
    reactivation_probability: str  # high, medium, low
    score_breakdown: Dict[str, int]
    historical_hero: bool
    historical_conversion_rate: float
    stock_status: str
    price_competitive: bool
    recent_clicks: int
    recommendation: str


class ZombieReactivationScorer:
    """
    Scores Zombie products on reactivation potential.

    Uses historical performance data to identify which Zombies are worth
    re-investing in vs which should be retired.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize scorer"""
        self.base_dir = base_dir or Path(__file__).parent

        # Scoring weights
        self.WEIGHTS = {
            'historical_hero': 50,
            'high_conversion_rate': 30,
            'stock_restored': 20,
            'price_competitive': 20,
            'recent_clicks': 10
        }

        self.MAX_SCORE = sum(self.WEIGHTS.values())

    def score_zombies(
        self,
        client: str,
        zombie_products: Dict[str, Dict],
        lookback_days: int = 90
    ) -> List[ZombieScore]:
        """
        Score all Zombie products for reactivation potential.

        Args:
            client: Client name
            zombie_products: Dict of {product_id: current_metrics}
            lookback_days: How far back to look for historical data

        Returns:
            List of ZombieScore objects, sorted by total_score (descending)
        """
        scores = []

        for product_id, current_metrics in zombie_products.items():
            # Calculate score for this zombie
            score = self._score_single_zombie(
                client,
                product_id,
                current_metrics,
                lookback_days
            )

            if score:
                scores.append(score)

        # Sort by total score (descending)
        scores.sort(key=lambda x: x.total_score, reverse=True)

        return scores

    def _score_single_zombie(
        self,
        client: str,
        product_id: str,
        current_metrics: Dict,
        lookback_days: int
    ) -> Optional[ZombieScore]:
        """Score a single Zombie product"""
        score_breakdown = {}
        total_score = 0

        # Factor 1: Was this a Hero in the past 90 days?
        was_hero = self._check_historical_hero_status(client, product_id, lookback_days)
        if was_hero:
            score_breakdown['historical_hero'] = self.WEIGHTS['historical_hero']
            total_score += self.WEIGHTS['historical_hero']
        else:
            score_breakdown['historical_hero'] = 0

        # Factor 2: Historical conversion rate
        historical_conv_rate = self._get_historical_conversion_rate(client, product_id, lookback_days)
        if historical_conv_rate >= 0.03:  # 3%+ conversion rate
            score_breakdown['high_conversion_rate'] = self.WEIGHTS['high_conversion_rate']
            total_score += self.WEIGHTS['high_conversion_rate']
        elif historical_conv_rate >= 0.01:  # 1-3% partial credit
            score_breakdown['high_conversion_rate'] = int(self.WEIGHTS['high_conversion_rate'] * 0.5)
            total_score += int(self.WEIGHTS['high_conversion_rate'] * 0.5)
        else:
            score_breakdown['high_conversion_rate'] = 0

        # Factor 3: Stock recently restored?
        stock_status = current_metrics.get('availability', 'unknown')
        stock_restored = self._check_stock_restoration(client, product_id, stock_status)
        if stock_restored:
            score_breakdown['stock_restored'] = self.WEIGHTS['stock_restored']
            total_score += self.WEIGHTS['stock_restored']
        else:
            score_breakdown['stock_restored'] = 0

        # Factor 4: Price competitive vs historical baseline?
        price_competitive = self._check_price_competitiveness(client, product_id, current_metrics)
        if price_competitive:
            score_breakdown['price_competitive'] = self.WEIGHTS['price_competitive']
            total_score += self.WEIGHTS['price_competitive']
        else:
            score_breakdown['price_competitive'] = 0

        # Factor 5: Recent click activity (organic interest)?
        recent_clicks = current_metrics.get('clicks', 0)
        if recent_clicks >= 10:  # 10+ clicks in last 24 hours
            score_breakdown['recent_clicks'] = self.WEIGHTS['recent_clicks']
            total_score += self.WEIGHTS['recent_clicks']
        elif recent_clicks >= 5:  # 5-10 clicks partial credit
            score_breakdown['recent_clicks'] = int(self.WEIGHTS['recent_clicks'] * 0.5)
            total_score += int(self.WEIGHTS['recent_clicks'] * 0.5)
        else:
            score_breakdown['recent_clicks'] = 0

        # Determine reactivation probability
        score_pct = (total_score / self.MAX_SCORE) * 100

        if score_pct >= 70:
            probability = "high"
            recommendation = "Strong candidate for reactivation - invest in this product"
        elif score_pct >= 40:
            probability = "medium"
            recommendation = "Moderate candidate - test with small budget increase"
        else:
            probability = "low"
            recommendation = "Low priority - consider retiring or leaving as-is"

        return ZombieScore(
            product_id=product_id,
            product_title=current_metrics.get('product_title', 'Unknown'),
            total_score=total_score,
            max_score=self.MAX_SCORE,
            reactivation_probability=probability,
            score_breakdown=score_breakdown,
            historical_hero=was_hero,
            historical_conversion_rate=historical_conv_rate,
            stock_status=stock_status,
            price_competitive=price_competitive,
            recent_clicks=recent_clicks,
            recommendation=recommendation
        )

    def _check_historical_hero_status(
        self,
        client: str,
        product_id: str,
        lookback_days: int
    ) -> bool:
        """Check if product was a Hero in the past N days"""
        # Load historical label transitions
        client_slug = client.replace(' ', '-').lower()
        labels_dir = self.base_dir / 'history' / 'label-transitions' / client_slug

        if not labels_dir.exists():
            return False

        # Check monthly transition files
        cutoff_date = datetime.now() - timedelta(days=lookback_days)

        # Check current and previous months
        for month_offset in [0, 1, 2]:
            target_date = datetime.now() - timedelta(days=30 * month_offset)
            transition_file = labels_dir / f"{target_date.strftime('%Y-%m')}.json"

            if transition_file.exists():
                with open(transition_file) as f:
                    data = json.load(f)

                # Check if this product ever had 'heroes' label
                for date_str, transitions in data.get('transitions', {}).items():
                    for transition in transitions:
                        if transition.get('product_id') == product_id:
                            if 'heroes' in [transition.get('from_label', ''), transition.get('to_label', '')]:
                                return True

        return False

    def _get_historical_conversion_rate(
        self,
        client: str,
        product_id: str,
        lookback_days: int
    ) -> float:
        """Get historical conversion rate for this product"""
        # Load historical product performance data
        client_slug = client.replace(' ', '-').lower()
        baselines_file = self.base_dir / 'data' / 'product_baselines' / f"{client}.json"

        if not baselines_file.exists():
            return 0.0

        with open(baselines_file) as f:
            baselines = json.load(f)

        product_baseline = baselines.get('products', {}).get(product_id, {})

        clicks = product_baseline.get('clicks', 0)
        conversions = product_baseline.get('conversions', 0)

        if clicks > 0:
            return conversions / clicks
        else:
            return 0.0

    def _check_stock_restoration(
        self,
        client: str,
        product_id: str,
        current_stock: str
    ) -> bool:
        """Check if stock was recently restored (was out, now in stock)"""
        if current_stock != 'in stock':
            return False

        # Load recent product feed history
        client_slug = client.replace(' ', '-').lower()
        feed_history_dir = self.base_dir / 'data' / 'product_feed_history' / client_slug

        if not feed_history_dir.exists():
            return False

        # Check last 7 days for "out of stock" status
        for days_ago in range(1, 8):
            target_date = datetime.now() - timedelta(days=days_ago)
            feed_file = feed_history_dir / f"{target_date.strftime('%Y-%m-%d')}.json"

            if feed_file.exists():
                with open(feed_file) as f:
                    feed_data = json.load(f)

                # Handle both list and dict formats
                products = feed_data if isinstance(feed_data, list) else feed_data.get('products', [])

                for product in products:
                    if product.get('product_id') == product_id:
                        if product.get('availability', '').lower() == 'out of stock':
                            return True  # Was out of stock, now back in stock

        return False

    def _check_price_competitiveness(
        self,
        client: str,
        product_id: str,
        current_metrics: Dict
    ) -> bool:
        """Check if current price is competitive vs baseline"""
        # Load price baselines
        client_slug = client.replace(' ', '-').lower()
        baselines_file = self.base_dir / 'data' / 'product_baselines' / f"{client}.json"

        if not baselines_file.exists():
            return True  # Assume competitive if no baseline

        with open(baselines_file) as f:
            baselines = json.load(f)

        product_baseline = baselines.get('products', {}).get(product_id, {})
        baseline_price = product_baseline.get('avg_price', 0)

        if baseline_price == 0:
            return True  # No baseline price

        # Get current price (would need to be in current_metrics)
        current_price = current_metrics.get('price', baseline_price)

        # Competitive if within ±20% of baseline
        price_diff_pct = abs((current_price - baseline_price) / baseline_price * 100)

        return price_diff_pct <= 20

    def generate_html_report(
        self,
        client: str,
        top_zombies: List[ZombieScore]
    ) -> str:
        """
        Generate HTML section for top Zombie reactivation candidates.

        Args:
            client: Client name
            top_zombies: Top N scored zombies

        Returns:
            HTML string
        """
        if not top_zombies:
            return f"""
            <h3>{client} - Zombie Reactivation Analysis</h3>
            <p>No Zombie products requiring reactivation analysis.</p>
            """

        html = f"""
        <h3>{client} - Top 10 Zombies to Reactivate</h3>
        <p>Zombies with highest reactivation potential (scored on historical performance, stock status, pricing):</p>

        <table>
            <tr>
                <th>Product</th>
                <th>Score</th>
                <th>Probability</th>
                <th>Key Factors</th>
                <th>Recommendation</th>
            </tr>
        """

        for zombie in top_zombies[:10]:
            # Build key factors list
            factors = []
            if zombie.historical_hero:
                factors.append("Former Hero")
            if zombie.historical_conversion_rate >= 0.03:
                factors.append(f"{zombie.historical_conversion_rate*100:.1f}% CVR")
            if zombie.stock_status == 'in stock':
                factors.append("In Stock")
            if zombie.price_competitive:
                factors.append("Price OK")
            if zombie.recent_clicks > 0:
                factors.append(f"{zombie.recent_clicks} clicks")

            factors_str = ", ".join(factors) if factors else "None"

            # Color code probability
            prob_color = {
                'high': '#059669',
                'medium': '#F59E0B',
                'low': '#6B7280'
            }.get(zombie.reactivation_probability, '#6B7280')

            html += f"""
            <tr>
                <td>{zombie.product_title[:50]}</td>
                <td><strong>{zombie.total_score}/{zombie.max_score}</strong> ({zombie.total_score/zombie.max_score*100:.0f}%)</td>
                <td style="color: {prob_color}; font-weight: 600;">{zombie.reactivation_probability.upper()}</td>
                <td><em>{factors_str}</em></td>
                <td>{zombie.recommendation}</td>
            </tr>
            """

        html += """
        </table>
        <p><em>High probability (≥70%) = Strong candidate for budget increase or campaign reactivation</em></p>
        <p><em>Medium probability (40-70%) = Test with small budget to validate</em></p>
        <p><em>Low probability (<40%) = Consider retiring or leaving as-is</em></p>
        """

        return html


if __name__ == "__main__":
    # Test the scorer
    print("Testing Zombie Reactivation Scorer...")

    # Mock zombie data
    test_zombies = {
        'zombie_1': {
            'product_title': 'High Potential Zombie (former Hero, good CVR)',
            'availability': 'in stock',
            'clicks': 15,
            'conversions': 0,
            'revenue': 0
        },
        'zombie_2': {
            'product_title': 'Medium Potential Zombie (some activity)',
            'availability': 'in stock',
            'clicks': 7,
            'conversions': 0,
            'revenue': 0
        },
        'zombie_3': {
            'product_title': 'Low Potential Zombie (no activity)',
            'availability': 'out of stock',
            'clicks': 0,
            'conversions': 0,
            'revenue': 0
        }
    }

    scorer = ZombieReactivationScorer()
    scores = scorer.score_zombies('Test Client', test_zombies, lookback_days=90)

    print(f"\nScored {len(scores)} zombies:")
    for score in scores:
        print(f"\n  {score.product_title}")
        print(f"  Score: {score.total_score}/{score.max_score} ({score.total_score/score.max_score*100:.0f}%)")
        print(f"  Probability: {score.reactivation_probability}")
        print(f"  Recommendation: {score.recommendation}")
        print(f"  Breakdown: {score.score_breakdown}")
