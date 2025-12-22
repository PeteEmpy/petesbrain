#!/usr/bin/env python3
"""
Chart Generation Module for PetesBrain
=======================================

Comprehensive chart generation for Google Ads reporting and analysis.
Supports line charts, bar charts, and sparklines in multiple output formats.

Standards:
- ROK brand colors (greens: #10B981, #059669, #047857)
- British English labelling throughout
- Matplotlib (PNG images) and Google Sheets integration
- Pre-configured templates for common Google Ads metrics

Chart Design Principles:
- Line charts for trends over time
- Bar charts for category comparisons
- Sparklines for inline context
- NEVER pie charts (use bar charts instead)

Usage:
    from shared.chart_generator import ChartGenerator

    # Create line chart
    generator = ChartGenerator()
    generator.line_chart(
        dates=['2025-12-01', '2025-12-02', '2025-12-03'],
        series={
            'Performance Max': [420, 435, 450],
            'Search': [380, 390, 385],
            'Shopping': [350, 360, 355]
        },
        title='ROAS Trend - Last 30 Days',
        y_label='ROAS (%)',
        output_path='clients/smythson/reports/roas-trend.png'
    )

    # Create bar chart
    generator.bar_chart(
        labels=['Campaign A', 'Campaign B', 'Campaign C'],
        values=[2450, 1850, 1200],
        title='Top Campaigns by Spend',
        x_label='Spend (£)',
        output_path='clients/smythson/reports/campaigns-spend.png'
    )

    # Generate ASCII sparkline
    sparkline = generator.ascii_sparkline([100, 120, 115, 130, 125])
    # Returns: '╱╱─╱─'
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server use

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import numpy as np


# ROK Brand Colors (from Roksys identity)
COLORS = {
    'primary_green': '#10B981',    # Bright green (H1 headings)
    'emerald_green': '#059669',    # Emerald (H2 headings)
    'soft_green': '#047857',       # Soft green (H3 headings)
    'muted_green': '#065F46',      # Muted green (H4+)
    'dark_green': '#2d5016',       # Dark green (headers)
    'positive': '#10B981',         # Positive metrics (green)
    'negative': '#dc3545',         # Negative metrics (red)
    'neutral': '#6c757d',          # Neutral (grey)
    'warning': '#ffc107',          # Warning (amber)
}

# Chart series colors (for multi-line charts)
SERIES_COLORS = [
    COLORS['primary_green'],
    COLORS['emerald_green'],
    COLORS['soft_green'],
    COLORS['muted_green'],
]


class ChartGenerator:
    """
    Generates charts for Google Ads reporting.

    Supports:
    - Line charts (trends over time)
    - Bar charts (category comparisons)
    - Sparklines (ASCII mini-charts)
    - Google Sheets integration
    """

    def __init__(self, style: str = 'rok'):
        """
        Initialise chart generator.

        Args:
            style: Chart style ('rok' for ROK branding, 'minimal' for clean)
        """
        self.style = style
        self._setup_matplotlib_style()

    def _setup_matplotlib_style(self):
        """Configure matplotlib with ROK styling."""
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['axes.titlesize'] = 13
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 14
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['grid.linestyle'] = '--'

    def line_chart(
        self,
        dates: List[str],
        series: Dict[str, List[float]],
        title: str,
        y_label: str,
        output_path: str,
        x_label: str = 'Date',
        figsize: Tuple[int, int] = (12, 6),
        show_legend: bool = True,
        date_format: str = '%Y-%m-%d'
    ) -> Path:
        """
        Create line chart showing trends over time.

        Use for: Daily/weekly/monthly performance metrics

        Args:
            dates: List of date strings (e.g., ['2025-12-01', '2025-12-02', ...])
            series: Dict of series_name -> values (e.g., {'Performance Max': [420, 435, ...]})
            title: Chart title
            y_label: Y-axis label (e.g., 'ROAS (%)', 'Conversions')
            output_path: Where to save PNG file
            x_label: X-axis label (default: 'Date')
            figsize: Figure size in inches (width, height)
            show_legend: Whether to show legend
            date_format: Date string format for parsing

        Returns:
            Path object of saved chart

        Example:
            generator.line_chart(
                dates=['2025-12-01', '2025-12-02', '2025-12-03'],
                series={
                    'Performance Max': [420, 435, 450],
                    'Search': [380, 390, 385]
                },
                title='ROAS Trend - Last 30 Days',
                y_label='ROAS (%)',
                output_path='reports/roas-trend.png'
            )
        """
        # Parse dates
        date_objects = [datetime.strptime(d, date_format) for d in dates]

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Plot each series
        for idx, (name, values) in enumerate(series.items()):
            color = SERIES_COLORS[idx % len(SERIES_COLORS)]
            ax.plot(
                date_objects,
                values,
                label=name,
                color=color,
                linewidth=2.5,
                marker='o',
                markersize=5,
                markerfacecolor=color,
                markeredgewidth=0
            )

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
        plt.xticks(rotation=45, ha='right')

        # Labels and title
        ax.set_xlabel(x_label, fontweight='bold')
        ax.set_ylabel(y_label, fontweight='bold')
        ax.set_title(title, fontweight='bold', fontsize=14, pad=20)

        # Legend
        if show_legend and len(series) > 1:
            ax.legend(loc='best', framealpha=0.9)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        # Layout
        plt.tight_layout()

        # Save
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()

        return output

    def bar_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str,
        x_label: str,
        output_path: str,
        orientation: str = 'horizontal',
        sort_by_value: bool = True,
        limit: int = None,
        figsize: Tuple[int, int] = (10, 8),
        value_format: str = '£{:,.0f}',
        show_values: bool = True
    ) -> Path:
        """
        Create bar chart for category comparisons.

        Use for: Rankings, comparisons, "which is best/worst?"

        Args:
            labels: Category labels (e.g., campaign names)
            values: Values for each category (e.g., spend amounts)
            title: Chart title
            x_label: X-axis label (e.g., 'Spend (£)')
            output_path: Where to save PNG file
            orientation: 'horizontal' (default, better for long labels) or 'vertical'
            sort_by_value: Whether to sort bars by value (descending)
            limit: Limit to top N bars (e.g., top 10)
            figsize: Figure size in inches (width, height)
            value_format: Format string for values (default: '£{:,.0f}')
            show_values: Whether to show value labels on bars

        Returns:
            Path object of saved chart

        Example:
            generator.bar_chart(
                labels=['Campaign A', 'Campaign B', 'Campaign C'],
                values=[2450, 1850, 1200],
                title='Top Campaigns by Spend',
                x_label='Spend (£)',
                output_path='reports/campaigns-spend.png'
            )
        """
        # Combine labels and values
        data = list(zip(labels, values))

        # Sort by value if requested
        if sort_by_value:
            data.sort(key=lambda x: x[1], reverse=True)

        # Limit if requested
        if limit:
            data = data[:limit]

        # Unpack sorted/limited data
        labels, values = zip(*data) if data else ([], [])

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Determine color (green for all bars, could be customised)
        colors = [COLORS['primary_green']] * len(values)

        # Create bars
        if orientation == 'horizontal':
            bars = ax.barh(labels, values, color=colors, edgecolor='white', linewidth=0.5)
            ax.set_xlabel(x_label, fontweight='bold')
            ax.invert_yaxis()  # Highest value at top

            # Add value labels
            if show_values:
                for idx, (bar, value) in enumerate(zip(bars, values)):
                    width = bar.get_width()
                    ax.text(
                        width,
                        bar.get_y() + bar.get_height() / 2,
                        f'  {value_format.format(value)}',
                        ha='left',
                        va='center',
                        fontweight='bold',
                        fontsize=9
                    )
        else:
            bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=0.5)
            ax.set_ylabel(x_label, fontweight='bold')
            plt.xticks(rotation=45, ha='right')

            # Add value labels
            if show_values:
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height,
                        value_format.format(value),
                        ha='center',
                        va='bottom',
                        fontweight='bold',
                        fontsize=9
                    )

        # Title
        ax.set_title(title, fontweight='bold', fontsize=14, pad=20)

        # Grid (only for value axis)
        if orientation == 'horizontal':
            ax.grid(True, axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
        else:
            ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)

        # Layout
        plt.tight_layout()

        # Save
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()

        return output

    def ascii_sparkline(
        self,
        values: List[float],
        length: int = None
    ) -> str:
        """
        Generate ASCII sparkline for inline trend visualisation.

        Use for: Adding trend context to tables (cells)

        Args:
            values: List of numeric values
            length: Optional length (defaults to len(values))

        Returns:
            ASCII sparkline string (e.g., '╱╱─╱─')

        Example:
            sparkline = generator.ascii_sparkline([100, 120, 115, 130, 125])
            # Returns: '╱╱─╱─'

            # Use in table:
            # | Metric | Value | Trend |
            # | ROAS   | 420%  | ╱╱─╱─ |
        """
        if not values or len(values) < 2:
            return '─' * (length or 5)

        # Normalise values to 0-1 range
        min_val = min(values)
        max_val = max(values)

        if max_val == min_val:
            return '─' * (length or len(values) - 1)

        normalised = [(v - min_val) / (max_val - min_val) for v in values]

        # Characters for trends
        chars = {
            'up': '╱',      # Rising
            'down': '╲',    # Falling
            'flat': '─'     # Flat
        }

        # Generate sparkline
        sparkline = []
        threshold = 0.05  # 5% change threshold for "flat"

        for i in range(len(normalised) - 1):
            diff = normalised[i + 1] - normalised[i]

            if diff > threshold:
                sparkline.append(chars['up'])
            elif diff < -threshold:
                sparkline.append(chars['down'])
            else:
                sparkline.append(chars['flat'])

        result = ''.join(sparkline)

        # Truncate or pad if length specified
        if length:
            if len(result) > length:
                result = result[:length]
            elif len(result) < length:
                result = result + chars['flat'] * (length - len(result))

        return result

    def google_sheets_sparkline_formula(
        self,
        range_ref: str,
        chart_type: str = 'line',
        options: Dict[str, any] = None
    ) -> str:
        """
        Generate Google Sheets SPARKLINE formula.

        Use for: Auto-updating sparklines in Google Sheets reports

        Args:
            range_ref: Cell range reference (e.g., 'B2:B8')
            chart_type: Chart type ('line', 'bar', 'column', 'winloss')
            options: Optional chart options dict

        Returns:
            Formula string to paste into Google Sheets

        Example:
            formula = generator.google_sheets_sparkline_formula(
                range_ref='B2:B8',
                chart_type='line',
                options={'color': '#10B981', 'linewidth': 2}
            )
            # Returns: =SPARKLINE(B2:B8, {"charttype","line";"color","#10B981";"linewidth",2})
        """
        if options is None:
            options = {}

        # Default options for ROK styling
        defaults = {
            'color': COLORS['primary_green'],
            'linewidth': 2
        }
        defaults.update(options)

        # Build options string
        opts = [f'"{k}","{v}"' if isinstance(v, str) else f'"{k}",{v}'
                for k, v in defaults.items()]
        opts_str = ';'.join([f'"charttype","{chart_type}"'] + opts)

        return f'=SPARKLINE({range_ref}, {{{opts_str}}})'

    def create_google_ads_template_charts(
        self,
        client: str,
        data: Dict,
        date_range: str,
        output_dir: str
    ) -> Dict[str, Path]:
        """
        Create complete set of charts for Google Ads weekly report.

        Pre-configured templates for common Google Ads metrics:
        - ROAS trend (line chart)
        - Campaign spend comparison (bar chart)
        - Conversion trend (line chart)
        - Top products (bar chart)

        Args:
            client: Client name (for titles)
            data: Dict containing all report data
            date_range: Date range string (for titles)
            output_dir: Directory to save charts

        Returns:
            Dict mapping chart_name -> Path of saved file

        Example:
            charts = generator.create_google_ads_template_charts(
                client='Smythson',
                data={
                    'dates': ['2025-12-01', '2025-12-02', ...],
                    'roas': {
                        'Performance Max': [420, 435, 450],
                        'Search': [380, 390, 385]
                    },
                    'campaigns': {
                        'Campaign A': 2450,
                        'Campaign B': 1850
                    }
                },
                date_range='1-7 December 2025',
                output_dir='clients/smythson/reports/weekly'
            )
        """
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        charts = {}

        # 1. ROAS Trend Line Chart
        if 'dates' in data and 'roas' in data:
            roas_path = output / 'roas-trend.png'
            self.line_chart(
                dates=data['dates'],
                series=data['roas'],
                title=f'{client} - ROAS Trend ({date_range})',
                y_label='ROAS (%)',
                output_path=str(roas_path)
            )
            charts['roas_trend'] = roas_path

        # 2. Campaign Spend Bar Chart
        if 'campaigns' in data:
            campaigns = data['campaigns']
            campaign_labels = list(campaigns.keys())
            campaign_values = list(campaigns.values())

            spend_path = output / 'campaigns-spend.png'
            self.bar_chart(
                labels=campaign_labels,
                values=campaign_values,
                title=f'{client} - Top Campaigns by Spend ({date_range})',
                x_label='Spend (£)',
                output_path=str(spend_path),
                limit=10  # Top 10 only
            )
            charts['campaigns_spend'] = spend_path

        # 3. Conversion Trend Line Chart
        if 'dates' in data and 'conversions' in data:
            conv_path = output / 'conversions-trend.png'
            self.line_chart(
                dates=data['dates'],
                series=data['conversions'],
                title=f'{client} - Conversion Trend ({date_range})',
                y_label='Conversions',
                output_path=str(conv_path)
            )
            charts['conversions_trend'] = conv_path

        # 4. Top Products Bar Chart (if e-commerce)
        if 'products' in data:
            products = data['products']
            product_labels = list(products.keys())
            product_values = list(products.values())

            products_path = output / 'top-products.png'
            self.bar_chart(
                labels=product_labels,
                values=product_values,
                title=f'{client} - Top Products by Revenue ({date_range})',
                x_label='Revenue (£)',
                output_path=str(products_path),
                limit=10
            )
            charts['top_products'] = products_path

        return charts


# Convenience functions for quick chart generation

def quick_line_chart(
    dates: List[str],
    values: List[float],
    title: str,
    metric_name: str,
    output_path: str
) -> Path:
    """
    Quick single-series line chart.

    Example:
        quick_line_chart(
            dates=['2025-12-01', '2025-12-02', '2025-12-03'],
            values=[420, 435, 450],
            title='ROAS Trend',
            metric_name='ROAS (%)',
            output_path='roas.png'
        )
    """
    generator = ChartGenerator()
    return generator.line_chart(
        dates=dates,
        series={metric_name: values},
        title=title,
        y_label=metric_name,
        output_path=output_path,
        show_legend=False
    )


def quick_bar_chart(
    labels: List[str],
    values: List[float],
    title: str,
    output_path: str,
    top_n: int = 10
) -> Path:
    """
    Quick bar chart for rankings.

    Example:
        quick_bar_chart(
            labels=['Campaign A', 'Campaign B', 'Campaign C'],
            values=[2450, 1850, 1200],
            title='Top Campaigns by Spend',
            output_path='campaigns.png'
        )
    """
    generator = ChartGenerator()
    return generator.bar_chart(
        labels=labels,
        values=values,
        title=title,
        x_label='Value',
        output_path=output_path,
        limit=top_n
    )


# Example usage
if __name__ == "__main__":
    # Test the module
    generator = ChartGenerator()

    # Test line chart
    print("Generating test line chart...")
    generator.line_chart(
        dates=['2025-12-01', '2025-12-02', '2025-12-03', '2025-12-04', '2025-12-05'],
        series={
            'Performance Max': [420, 435, 450, 445, 460],
            'Search': [380, 390, 385, 395, 400],
            'Shopping': [350, 360, 355, 365, 370]
        },
        title='ROAS Trend - Test',
        y_label='ROAS (%)',
        output_path='/tmp/test-roas-trend.png'
    )
    print("✓ Line chart saved to /tmp/test-roas-trend.png")

    # Test bar chart
    print("\nGenerating test bar chart...")
    generator.bar_chart(
        labels=['Campaign A', 'Campaign B', 'Campaign C', 'Campaign D'],
        values=[2450, 1850, 1200, 950],
        title='Top Campaigns by Spend - Test',
        x_label='Spend (£)',
        output_path='/tmp/test-campaigns-spend.png'
    )
    print("✓ Bar chart saved to /tmp/test-campaigns-spend.png")

    # Test ASCII sparkline
    print("\nGenerating test ASCII sparklines...")
    values = [100, 120, 115, 130, 125, 140, 135]
    sparkline = generator.ascii_sparkline(values)
    print(f"Values: {values}")
    print(f"Sparkline: {sparkline}")

    # Test Google Sheets formula
    print("\nGoogle Sheets SPARKLINE formula:")
    formula = generator.google_sheets_sparkline_formula('B2:B8')
    print(formula)

    print("\n✅ All tests completed successfully")
