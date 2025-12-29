#!/usr/bin/env python3
"""
Predictive Alert System

Forecasts performance trends and generates early-warning alerts BEFORE issues occur.

Key Features:
- Trend analysis using linear regression on 7-day/14-day/30-day windows
- Predicts revenue, ROAS, conversion rate, click trends
- Generates alerts when negative trends detected
- Confidence scoring based on data quality and trend strength
- Differentiates between temporary fluctuations and sustained trends

Usage:
    from predictive_alerts import PredictiveAlerter

    alerter = PredictiveAlerter()
    alerts = alerter.generate_predictive_alerts(
        historical_data={'2025-12-20': {...}, '2025-12-21': {...}},
        product_id='12345'
    )
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json
import statistics


@dataclass
class PredictiveAlert:
    """Predictive alert for future performance issues"""
    alert_type: str  # revenue_decline, roas_decline, conversion_decline, click_decline
    product_id: str
    product_title: str
    current_value: float
    predicted_value: float
    predicted_change_pct: float
    trend_strength: str  # strong, moderate, weak
    confidence: str  # high, medium, low
    forecast_days: int  # Days ahead forecast is for
    reason: str
    recommended_action: str
    timestamp: str


class PredictiveAlerter:
    """
    Generates predictive alerts based on trend forecasting.

    Uses simple linear regression to detect trends and predict future values.
    """

    def __init__(self):
        """Initialize predictive alerter"""

        # Alert thresholds
        self.REVENUE_DECLINE_THRESHOLD = 0.20  # 20% predicted decline
        self.ROAS_DECLINE_THRESHOLD = 0.15  # 15% predicted decline
        self.CVR_DECLINE_THRESHOLD = 0.10  # 10% predicted decline
        self.CLICK_DECLINE_THRESHOLD = 0.15  # 15% predicted decline

        # Forecast windows
        self.FORECAST_WINDOWS = {
            'short_term': 7,  # 7 days
            'medium_term': 14,  # 14 days
            'long_term': 30  # 30 days
        }

    def generate_predictive_alerts(
        self,
        historical_data: Dict[str, Dict],
        product_id: str,
        product_title: str,
        target_roas: float = 4.0
    ) -> List[PredictiveAlert]:
        """
        Generate predictive alerts based on historical trends.

        Args:
            historical_data: Dict of {date_str: {revenue, spend, clicks, conversions, ...}}
            product_id: Product ID
            product_title: Product title
            target_roas: Target ROAS

        Returns:
            List of PredictiveAlert objects
        """
        alerts = []

        if len(historical_data) < 7:
            # Insufficient data for trend analysis
            return alerts

        # Sort by date
        sorted_dates = sorted(historical_data.keys())

        # Extract time series data
        revenue_series = [historical_data[date].get('revenue', 0) for date in sorted_dates]
        spend_series = [historical_data[date].get('spend', 0) for date in sorted_dates]
        click_series = [historical_data[date].get('clicks', 0) for date in sorted_dates]
        conversion_series = [historical_data[date].get('conversions', 0) for date in sorted_dates]

        # Calculate ROAS series
        roas_series = [
            (revenue / spend) if spend > 0 else 0
            for revenue, spend in zip(revenue_series, spend_series)
        ]

        # Calculate CVR series
        cvr_series = [
            (conversions / clicks) if clicks > 0 else 0
            for conversions, clicks in zip(conversion_series, click_series)
        ]

        # Check for revenue decline trend
        revenue_alert = self._check_metric_decline(
            revenue_series,
            sorted_dates,
            product_id,
            product_title,
            'revenue',
            self.REVENUE_DECLINE_THRESHOLD,
            '£'
        )
        if revenue_alert:
            alerts.append(revenue_alert)

        # Check for ROAS decline trend
        roas_alert = self._check_metric_decline(
            roas_series,
            sorted_dates,
            product_id,
            product_title,
            'roas',
            self.ROAS_DECLINE_THRESHOLD,
            suffix='x',
            target=target_roas
        )
        if roas_alert:
            alerts.append(roas_alert)

        # Check for conversion rate decline
        cvr_alert = self._check_metric_decline(
            cvr_series,
            sorted_dates,
            product_id,
            product_title,
            'conversion',
            self.CVR_DECLINE_THRESHOLD,
            suffix='%',
            multiplier=100
        )
        if cvr_alert:
            alerts.append(cvr_alert)

        # Check for click decline
        click_alert = self._check_metric_decline(
            click_series,
            sorted_dates,
            product_id,
            product_title,
            'click',
            self.CLICK_DECLINE_THRESHOLD
        )
        if click_alert:
            alerts.append(click_alert)

        return alerts

    def _check_metric_decline(
        self,
        metric_series: List[float],
        dates: List[str],
        product_id: str,
        product_title: str,
        metric_name: str,
        threshold: float,
        prefix: str = '',
        suffix: str = '',
        multiplier: float = 1.0,
        target: Optional[float] = None
    ) -> Optional[PredictiveAlert]:
        """Check if metric has declining trend"""

        # Calculate trend
        trend = self._calculate_linear_trend(metric_series)

        if trend is None:
            return None

        slope, intercept, r_squared = trend

        # Predict value 7 days ahead
        forecast_days = 7
        current_value = metric_series[-1]
        predicted_value = slope * (len(metric_series) + forecast_days) + intercept

        # Ensure predicted value doesn't go negative
        predicted_value = max(predicted_value, 0)

        if current_value == 0:
            return None

        # Calculate predicted change percentage
        predicted_change_pct = ((predicted_value - current_value) / current_value) * 100

        # Check if decline exceeds threshold
        if predicted_change_pct < -(threshold * 100):
            # Determine trend strength based on R-squared
            if r_squared >= 0.7:
                trend_strength = "strong"
            elif r_squared >= 0.4:
                trend_strength = "moderate"
            else:
                trend_strength = "weak"

            # Calculate confidence
            confidence = self._calculate_forecast_confidence(
                metric_series,
                r_squared,
                slope
            )

            # Generate reason
            reason = self._generate_forecast_reason(
                metric_name,
                current_value,
                predicted_value,
                predicted_change_pct,
                trend_strength,
                multiplier,
                target
            )

            # Generate recommended action
            recommended_action = self._generate_forecast_action(
                metric_name,
                trend_strength,
                confidence
            )

            return PredictiveAlert(
                alert_type=f"{metric_name}_decline",
                product_id=product_id,
                product_title=product_title,
                current_value=current_value * multiplier,
                predicted_value=predicted_value * multiplier,
                predicted_change_pct=predicted_change_pct,
                trend_strength=trend_strength,
                confidence=confidence,
                forecast_days=forecast_days,
                reason=reason,
                recommended_action=recommended_action,
                timestamp=datetime.now().isoformat()
            )

        return None

    def _calculate_linear_trend(
        self,
        values: List[float]
    ) -> Optional[Tuple[float, float, float]]:
        """
        Calculate linear trend using least squares regression.

        Returns:
            Tuple of (slope, intercept, r_squared) or None if insufficient data
        """
        if len(values) < 3:
            return None

        # Remove zeros to avoid skewing trend
        filtered_values = [(i, v) for i, v in enumerate(values) if v > 0]

        if len(filtered_values) < 3:
            return None

        x_values = [x for x, _ in filtered_values]
        y_values = [y for _, y in filtered_values]

        n = len(x_values)

        # Calculate means
        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(y_values)

        # Calculate slope
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator = sum((x - mean_x) ** 2 for x in x_values)

        if denominator == 0:
            return None

        slope = numerator / denominator
        intercept = mean_y - slope * mean_x

        # Calculate R-squared
        ss_tot = sum((y - mean_y) ** 2 for y in y_values)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_values, y_values))

        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return slope, intercept, r_squared

    def _calculate_forecast_confidence(
        self,
        metric_series: List[float],
        r_squared: float,
        slope: float
    ) -> str:
        """Calculate confidence level for forecast"""

        # High confidence requires:
        # 1. Strong R-squared (≥0.7)
        # 2. Sufficient data points (≥14)
        # 3. Consistent trend (low variance)

        data_points = len(metric_series)

        # Calculate coefficient of variation (if possible)
        non_zero_values = [v for v in metric_series if v > 0]

        if len(non_zero_values) >= 3:
            mean_val = statistics.mean(non_zero_values)
            std_val = statistics.stdev(non_zero_values)
            cv = (std_val / mean_val) if mean_val > 0 else 999
        else:
            cv = 999

        if r_squared >= 0.7 and data_points >= 14 and cv < 0.5:
            return "high"
        elif r_squared >= 0.4 and data_points >= 7 and cv < 1.0:
            return "medium"
        else:
            return "low"

    def _generate_forecast_reason(
        self,
        metric_name: str,
        current_value: float,
        predicted_value: float,
        predicted_change_pct: float,
        trend_strength: str,
        multiplier: float,
        target: Optional[float]
    ) -> str:
        """Generate human-readable reason for forecast alert"""

        metric_display = {
            'revenue': 'Revenue',
            'roas': 'ROAS',
            'conversion': 'Conversion rate',
            'click': 'Clicks'
        }.get(metric_name, metric_name.capitalize())

        reason = f"{trend_strength.capitalize()} declining trend detected. "
        reason += f"{metric_display} predicted to drop from {current_value * multiplier:.1f} to {predicted_value * multiplier:.1f} "
        reason += f"({predicted_change_pct:.0f}%) within 7 days"

        if target and metric_name == 'roas':
            if predicted_value < target:
                reason += f" (below {target:.1f}x target)"

        return reason

    def _generate_forecast_action(
        self,
        metric_name: str,
        trend_strength: str,
        confidence: str
    ) -> str:
        """Generate recommended action for forecast alert"""

        if confidence == "low":
            return "Monitor closely - trend confidence is low, may be temporary fluctuation"

        actions = {
            'revenue': "Review product availability, pricing, ad copy. Consider increasing budget if performance otherwise strong.",
            'roas': "Investigate rising costs or declining conversion rate. Review bidding strategy and negative keywords.",
            'conversion': "Review landing page experience, product pricing, competitive landscape. Test new ad copy variations.",
            'click': "Review impression share, ad position, search term relevance. Consider expanding keyword targeting."
        }

        action = actions.get(metric_name, "Investigate root cause and take corrective action")

        if trend_strength == "strong":
            return f"⚠️ URGENT: {action}"
        else:
            return action

    def generate_html_section(
        self,
        client: str,
        alerts: List[PredictiveAlert]
    ) -> str:
        """
        Generate HTML section for predictive alerts.

        Args:
            client: Client name
            alerts: List of predictive alerts

        Returns:
            HTML string
        """
        if not alerts:
            return f"""
            <h3>{client} - Predictive Alerts</h3>
            <p>✅ No negative trends detected. All metrics stable or improving.</p>
            """

        html = f"""
        <h3>{client} - Predictive Alerts (7-Day Forecast)</h3>
        <p>⚠️ {len(alerts)} potential issue(s) detected based on trend analysis:</p>

        <table>
            <tr>
                <th>Product</th>
                <th>Alert Type</th>
                <th>Current Value</th>
                <th>Predicted (7d)</th>
                <th>Change</th>
                <th>Trend Strength</th>
                <th>Confidence</th>
                <th>Recommended Action</th>
            </tr>
        """

        for alert in alerts:
            # Color code based on trend strength and confidence
            if alert.trend_strength == "strong" and alert.confidence == "high":
                row_color = "#FEE2E2"  # Red background
            elif alert.trend_strength == "moderate" or alert.confidence == "medium":
                row_color = "#FEF3C7"  # Yellow background
            else:
                row_color = "#FFFFFF"  # White background

            alert_type_display = alert.alert_type.replace('_', ' ').title()

            html += f"""
            <tr style="background-color: {row_color};">
                <td>{alert.product_title[:50]}</td>
                <td><strong>{alert_type_display}</strong></td>
                <td>{alert.current_value:.1f}</td>
                <td>{alert.predicted_value:.1f}</td>
                <td style="color: #DC2626; font-weight: 600;">{alert.predicted_change_pct:.0f}%</td>
                <td>{alert.trend_strength.capitalize()}</td>
                <td>{alert.confidence.capitalize()}</td>
                <td><em>{alert.recommended_action}</em></td>
            </tr>
            """

        html += """
        </table>
        <p><em>Predictions based on 7-14 day historical trend analysis using linear regression.</em></p>
        <p><em>Strong trends with high confidence require immediate attention.</em></p>
        """

        return html


if __name__ == "__main__":
    # Test the predictive alerter
    print("Testing Predictive Alert System...")

    # Mock historical data with declining trend
    historical_data = {}
    base_revenue = 100
    base_clicks = 200

    for day in range(14):
        date_str = (datetime.now() - timedelta(days=14-day)).strftime('%Y-%m-%d')
        # Simulate declining revenue trend
        revenue = base_revenue - (day * 5)  # £5/day decline
        spend = 50
        clicks = base_clicks - (day * 10)  # 10 clicks/day decline
        conversions = 10 - (day * 0.5)  # Declining conversions

        historical_data[date_str] = {
            'revenue': max(revenue, 0),
            'spend': spend,
            'clicks': max(clicks, 0),
            'conversions': max(conversions, 0)
        }

    alerter = PredictiveAlerter()
    alerts = alerter.generate_predictive_alerts(
        historical_data=historical_data,
        product_id='test_123',
        product_title='Test Product with Declining Trend',
        target_roas=4.0
    )

    print(f"\nGenerated {len(alerts)} predictive alerts:\n")
    for alert in alerts:
        print(f"  Alert Type: {alert.alert_type}")
        print(f"  Product: {alert.product_title}")
        print(f"  Current: {alert.current_value:.1f} → Predicted (7d): {alert.predicted_value:.1f}")
        print(f"  Predicted Change: {alert.predicted_change_pct:.0f}%")
        print(f"  Trend Strength: {alert.trend_strength}")
        print(f"  Confidence: {alert.confidence}")
        print(f"  Reason: {alert.reason}")
        print(f"  Action: {alert.recommended_action}")
        print()
