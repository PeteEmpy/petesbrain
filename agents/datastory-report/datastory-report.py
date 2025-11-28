#!/usr/bin/env python3
"""
Data Storytelling Report Agent

Transforms raw performance data into compelling narratives following expert frameworks
from Nancy Duarte, Cole Nussbaumer Knaflic, and Edward Tufte.

Usage:
    python3 datastory-report.py --client smythson --data data.json --audience client --goal diagnose_problem

Version: 1.0
Created: 2025-11-19
"""

import argparse
import json
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import anthropic

# Add shared directory to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared'))

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    sys.exit(1)

CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


class DataStoryGenerator:
    """
    5-Phase Data Storytelling Workflow

    Based on expert frameworks:
    - Nancy Duarte: DataStory (find human angle, Data Point of View)
    - Cole Nussbaumer Knaflic: Storytelling with Data (context-first, clear message)
    - Edward Tufte: Visual Display (clarity, precision, efficiency)
    """

    def __init__(self, client_name: str, data: Dict[str, Any], audience: str, goal: str):
        self.client_name = client_name
        self.data = data
        self.audience = audience
        self.goal = goal
        self.context = {}
        self.insights = []
        self.main_insight = None
        self.supporting_details = {}
        self.narrative = {}
        self.visualizations = []

    def generate_story(self) -> Dict[str, Any]:
        """Execute 5-phase workflow and return complete data story"""
        print("🎭 Generating Data Story...")
        print(f"   Client: {self.client_name}")
        print(f"   Audience: {self.audience}")
        print(f"   Goal: {self.goal}\n")

        # Phase 1: Understand Context & Audience
        print("📋 Phase 1: Understanding context and audience...")
        self.context = self._phase1_understand_context()

        # Phase 2: Ingest & Scan Data
        print("🔍 Phase 2: Scanning data for patterns...")
        self.insights = self._phase2_scan_data()

        # Phase 3: Identify Key Insight (Data Point of View)
        print("💡 Phase 3: Identifying key insight...")
        self.main_insight = self._phase3_identify_insight()

        # Phase 4: Gather Supporting Details
        print("📊 Phase 4: Gathering supporting details...")
        self.supporting_details = self._phase4_gather_details()

        # Phase 5: Structure Narrative (3-Act)
        print("📝 Phase 5: Structuring narrative...")
        self.narrative = self._phase5_structure_narrative()

        # Add visualization recommendations
        print("📈 Adding visualization recommendations...")
        self.visualizations = self._recommend_visualizations()

        print("✅ Data story generation complete!\n")

        return {
            "context": self.context,
            "insights": self.insights,
            "main_insight": self.main_insight,
            "supporting_details": self.supporting_details,
            "narrative": self.narrative,
            "visualizations": self.visualizations,
            "metadata": {
                "client": self.client_name,
                "audience": self.audience,
                "goal": self.goal,
                "generated_at": datetime.now().isoformat()
            }
        }

    def _phase1_understand_context(self) -> Dict[str, Any]:
        """
        Phase 1: Understand Context & Audience

        Determine:
        - Who is the audience? (executives, technical team, stakeholders)
        - What do they care about? (revenue, efficiency, customer satisfaction)
        - What's the goal? (find opportunities, diagnose problems, track progress)
        - What level of detail? (high-level summary vs. deep-dive)
        """
        context = {
            "audience_type": self.audience,
            "detail_level": self._determine_detail_level(),
            "priorities": self._determine_priorities(),
            "tone": self._determine_tone()
        }

        print(f"   • Audience: {context['audience_type']}")
        print(f"   • Detail level: {context['detail_level']}")
        print(f"   • Priorities: {', '.join(context['priorities'])}")

        return context

    def _determine_detail_level(self) -> str:
        """Determine appropriate detail level based on audience"""
        levels = {
            "client": "medium",  # Business-focused, some detail
            "executive": "high-level",  # Strategic overview only
            "technical": "deep-dive"  # Full implementation details
        }
        return levels.get(self.audience, "medium")

    def _determine_priorities(self) -> List[str]:
        """Determine what audience cares about"""
        priorities_map = {
            "client": ["ROI", "business outcomes", "next actions"],
            "executive": ["strategic implications", "bottom line impact", "competitive position"],
            "technical": ["implementation details", "optimization opportunities", "technical insights"]
        }
        return priorities_map.get(self.audience, ["business outcomes", "next actions"])

    def _determine_tone(self) -> str:
        """Determine appropriate tone"""
        tones = {
            "client": "professional-friendly",
            "executive": "formal-strategic",
            "technical": "detailed-analytical"
        }
        return tones.get(self.audience, "professional-friendly")

    def _phase2_scan_data(self) -> List[Dict[str, Any]]:
        """
        Phase 2: Ingest & Scan the Data

        Look for noteworthy patterns:
        - Trends: Upward/downward trajectory? Accelerations? Decelerations?
        - Anomalies: Sudden spikes or drops? Values deviating from norm?
        - Comparisons: Which categories highest/lowest? Clear winners/losers?
        - Correlations: Do two variables move together?
        - Contextual changes: Unusual high/low vs historical or expected values?
        """
        insights = []

        metrics = self.data.get('metrics', {})

        # Scan for trends
        trends = self._identify_trends(metrics)
        if trends:
            insights.extend(trends)
            print(f"   • Found {len(trends)} trend(s)")

        # Scan for anomalies
        anomalies = self._identify_anomalies(metrics)
        if anomalies:
            insights.extend(anomalies)
            print(f"   • Found {len(anomalies)} anomaly/anomalies")

        # Scan for significant comparisons
        comparisons = self._identify_comparisons(metrics)
        if comparisons:
            insights.extend(comparisons)
            print(f"   • Found {len(comparisons)} significant comparison(s)")

        return insights

    def _identify_trends(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify upward/downward trends in metrics"""
        trends = []

        # Look for percentage changes
        for metric_name, metric_value in metrics.items():
            if '_change_percent' in metric_name or '_growth' in metric_name:
                if abs(metric_value) > 10:  # Significant if >10%
                    direction = "increasing" if metric_value > 0 else "decreasing"
                    magnitude = abs(metric_value)

                    trends.append({
                        "type": "trend",
                        "metric": metric_name.replace('_change_percent', '').replace('_growth', ''),
                        "direction": direction,
                        "magnitude": magnitude,
                        "significance": "high" if magnitude > 20 else "medium",
                        "description": f"{metric_name.replace('_', ' ').title()}: {direction} by {magnitude:.1f}%"
                    })

        return trends

    def _identify_anomalies(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify anomalies (sudden spikes or drops)"""
        anomalies = []

        # Look for dramatic changes (>30%)
        for metric_name, metric_value in metrics.items():
            if '_change_percent' in metric_name:
                if abs(metric_value) > 30:
                    anomalies.append({
                        "type": "anomaly",
                        "metric": metric_name.replace('_change_percent', ''),
                        "value": metric_value,
                        "severity": "critical" if abs(metric_value) > 50 else "high",
                        "description": f"Dramatic change in {metric_name.replace('_', ' ')}: {metric_value:+.1f}%"
                    })

        return anomalies

    def _identify_comparisons(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify significant comparisons between metrics"""
        comparisons = []

        # Example: Compare ROAS current vs previous
        if 'roas_current' in metrics and 'roas_previous' in metrics:
            current = metrics['roas_current']
            previous = metrics['roas_previous']
            change_percent = ((current - previous) / previous) * 100

            if abs(change_percent) > 5:  # Significant if >5%
                comparisons.append({
                    "type": "comparison",
                    "metric": "roas",
                    "current": current,
                    "previous": previous,
                    "change_percent": change_percent,
                    "winner": "current" if current > previous else "previous",
                    "description": f"ROAS {'improved' if current > previous else 'declined'} from {previous}% to {current}% ({change_percent:+.1f}%)"
                })

        return comparisons

    def _phase3_identify_insight(self) -> Dict[str, Any]:
        """
        Phase 3: Identify the Key Insight (Story Point)

        Formulate a "Data Point of View" (Nancy Duarte):
        - The insight itself (what happened)
        - An implication or recommendation (why it matters)
        - The stakes of inaction (to drive the point home)
        """
        # Select the most impactful insight
        if not self.insights:
            return {"error": "No significant insights found"}

        # Sort by significance/magnitude
        sorted_insights = sorted(
            self.insights,
            key=lambda x: x.get('magnitude', 0) or abs(x.get('change_percent', 0)) or 0,
            reverse=True
        )

        primary_insight = sorted_insights[0]

        # Generate Data Point of View using Claude
        data_point_of_view = self._generate_data_point_of_view(primary_insight)

        print(f"   • Key insight: {data_point_of_view['headline']}")

        return {
            "primary_insight": primary_insight,
            "data_point_of_view": data_point_of_view,
            "supporting_insights": sorted_insights[1:3]  # Top 2-3 supporting insights
        }

    def _generate_data_point_of_view(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate "Data Point of View" using Claude

        Format: What happened + Why it matters + Stakes of inaction
        """
        prompt = f"""Generate a "Data Point of View" for this data insight:

Client: {self.client_name}
Audience: {self.audience}
Goal: {self.goal}

Primary Insight:
{json.dumps(insight, indent=2)}

Full Data Context:
{json.dumps(self.data, indent=2)}

Create a compelling one-sentence "Data Point of View" that includes:
1. What happened (the insight)
2. Why it matters (implication)
3. Stakes of inaction (urgency)

Format your response as JSON with these fields:
- headline: One punchy sentence summarizing the story
- what_happened: Clear statement of what the data shows
- why_matters: Business implication or opportunity
- stakes: What happens if we don't act
- recommended_action: Specific next step

Keep it concise and focused. Use British English."""

        try:
            response = CLIENT.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract JSON from response
            content = response.content[0].text
            # Find JSON in response (might be wrapped in markdown code blocks)
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()

            return json.loads(json_str)

        except Exception as e:
            print(f"   ⚠️ Error generating Data Point of View: {e}")
            # Fallback to basic structure
            return {
                "headline": insight.get('description', 'Performance change detected'),
                "what_happened": insight.get('description', ''),
                "why_matters": "This change impacts business outcomes",
                "stakes": "Action needed to maintain/improve performance",
                "recommended_action": "Review and adjust strategy"
            }

    def _phase4_gather_details(self) -> Dict[str, Any]:
        """
        Phase 4: Gather Supporting Details & Context

        Put the insight in context:
        - Time context: How does current data compare to previous periods?
        - Benchmark or target: Compare to goals/targets/industry average
        - Breakdown: Break main metric into components
        - Possible causes/correlations: Link timing with known events
        """
        details = {
            "time_context": self._get_time_context(),
            "benchmarks": self._get_benchmarks(),
            "breakdowns": self._get_breakdowns(),
            "possible_causes": self._get_possible_causes()
        }

        print(f"   • Time context: {details['time_context'].get('summary', 'N/A')}")
        if details['possible_causes']:
            print(f"   • Identified {len(details['possible_causes'])} possible cause(s)")

        return details

    def _get_time_context(self) -> Dict[str, Any]:
        """Compare current period to previous periods"""
        period = self.data.get('period', 'Current period')

        context = {
            "current_period": period,
            "summary": f"Analysis covers {period}"
        }

        # Add comparisons if available
        metrics = self.data.get('metrics', {})
        if 'roas_previous' in metrics and 'roas_current' in metrics:
            context["comparison"] = (
                f"Current ROAS of {metrics['roas_current']}% vs "
                f"previous {metrics['roas_previous']}%"
            )

        return context

    def _get_benchmarks(self) -> Dict[str, Any]:
        """Get relevant benchmarks or targets"""
        benchmarks = {}

        # Check if client goals are provided in context
        client_context = self.data.get('context', {})
        if 'client_goals' in client_context:
            benchmarks["client_goals"] = client_context['client_goals']

        # Add ROAS benchmark if applicable
        metrics = self.data.get('metrics', {})
        if 'roas_current' in metrics:
            roas = metrics['roas_current']
            if roas >= 400:
                benchmarks["roas_assessment"] = "Excellent (above 400% target)"
            elif roas >= 300:
                benchmarks["roas_assessment"] = "Good (above 300% threshold)"
            else:
                benchmarks["roas_assessment"] = "Needs improvement (below 300%)"

        return benchmarks

    def _get_breakdowns(self) -> List[Dict[str, Any]]:
        """Break main metrics into components"""
        breakdowns = []

        metrics = self.data.get('metrics', {})

        # Example: Revenue breakdown
        if 'revenue_current' in metrics and 'conversions_current' in metrics:
            avg_order_value = metrics['revenue_current'] / metrics['conversions_current']
            breakdowns.append({
                "type": "average_order_value",
                "value": avg_order_value,
                "description": f"Average order value: £{avg_order_value:,.2f}"
            })

        return breakdowns

    def _get_possible_causes(self) -> List[Dict[str, str]]:
        """Identify possible causes based on context"""
        causes = []

        client_context = self.data.get('context', {})

        # Check for recent changes
        if 'recent_changes' in client_context:
            for change in client_context['recent_changes']:
                causes.append({
                    "type": "recent_change",
                    "description": change,
                    "correlation": "timing suggests this may have impacted performance"
                })

        # Check for seasonality
        if 'seasonality' in client_context:
            causes.append({
                "type": "seasonality",
                "description": client_context['seasonality'],
                "correlation": "seasonal patterns may influence results"
            })

        return causes

    def _phase5_structure_narrative(self) -> Dict[str, str]:
        """
        Phase 5: Structure the Narrative (Story Arc)

        Three-act structure:
        - Beginning (Setup): Set scene, introduce metrics, establish baseline
        - Middle (Conflict/Insight): Present core insight as turning point
        - End (Resolution/Next Steps): Implications, recommendations, what to monitor
        """
        narrative = self._generate_narrative_with_claude()

        print(f"   • Narrative structure: {len(narrative.get('beginning', ''))} + {len(narrative.get('middle', ''))} + {len(narrative.get('end', ''))} characters")

        return narrative

    def _generate_narrative_with_claude(self) -> Dict[str, str]:
        """Generate three-act narrative structure using Claude"""
        prompt = f"""Generate a compelling data story narrative for this performance analysis:

Client: {self.client_name}
Audience: {self.audience} ({self.context['tone']} tone)
Goal: {self.goal}

Data Point of View:
{json.dumps(self.main_insight.get('data_point_of_view', {}), indent=2)}

Supporting Context:
- Time period: {self.supporting_details.get('time_context', {}).get('current_period', 'N/A')}
- Possible causes: {json.dumps(self.supporting_details.get('possible_causes', []), indent=2)}
- Benchmarks: {json.dumps(self.supporting_details.get('benchmarks', {}), indent=2)}

Full Data:
{json.dumps(self.data.get('metrics', {}), indent=2)}

Create a three-act narrative structure following these guidelines:

**Beginning (Setup):**
- Set the scene with context (what was happening before)
- Introduce the key metrics as "characters"
- Establish the baseline or normal state
- Keep factual, provide background audience needs

**Middle (Conflict/Insight):**
- Present the core insight as the "conflict" or turning point
- Describe what changed and why it's significant
- Make the magnitude vivid and clear
- This is where the interesting change happens

**End (Resolution/Next Steps):**
- Explain implications going forward
- What decision does this inform?
- Suggest specific actions or what to monitor
- Answer "So what should we do about it?"

Format your response as JSON with these fields:
- beginning: The setup paragraph (100-150 words)
- middle: The conflict/insight paragraph (100-150 words)
- end: The resolution paragraph (100-150 words)
- headline: A compelling title for the story (5-10 words)

Use:
- British English (optimise, analyse, etc.)
- Concrete numbers and comparisons
- Active voice and vivid descriptions
- {self.context['tone']} tone appropriate for {self.audience} audience
- Short sentences and clear structure"""

        try:
            response = CLIENT.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text

            # Extract JSON from response
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                json_str = content.split('```')[1].split('```')[0].strip()
            else:
                json_str = content.strip()

            narrative = json.loads(json_str)

            return narrative

        except Exception as e:
            print(f"   ⚠️ Error generating narrative: {e}")
            # Fallback to basic structure
            dpov = self.main_insight.get('data_point_of_view', {})
            return {
                "headline": dpov.get('headline', 'Performance Analysis'),
                "beginning": f"Analysis of {self.client_name} performance for {self.data.get('period', 'current period')}.",
                "middle": dpov.get('what_happened', 'Performance changed during this period.'),
                "end": dpov.get('recommended_action', 'Continue monitoring and adjust strategy as needed.')
            }

    def _recommend_visualizations(self) -> List[Dict[str, Any]]:
        """
        Recommend appropriate visualizations for the story

        Based on Cole Nussbaumer Knaflic and Edward Tufte principles:
        - Choose right chart for the data
        - Eliminate clutter
        - Maintain graphical integrity
        """
        visualizations = []

        metrics = self.data.get('metrics', {})

        # Line chart for time series trends
        if any('_previous' in k and '_current' in k for k in metrics.keys()):
            visualizations.append({
                "type": "line_chart",
                "purpose": "Show trend over time",
                "metrics": ["roas", "conversions", "spend"],
                "recommendation": "Line chart showing ROAS trend with annotation at key turning point",
                "design_notes": "Minimal gridlines, clean design, annotate anomalies with arrows"
            })

        # Bar chart for comparisons
        if 'roas_current' in metrics and 'roas_previous' in metrics:
            visualizations.append({
                "type": "bar_chart",
                "purpose": "Compare current vs previous period",
                "metrics": ["roas", "revenue", "conversions"],
                "recommendation": "Grouped bar chart comparing key metrics period-over-period",
                "design_notes": "Zero baseline, distinct color for current period, horizontal layout"
            })

        # Big number for single crucial metric
        if self.main_insight:
            primary = self.main_insight.get('primary_insight', {})
            if primary.get('type') == 'comparison':
                visualizations.append({
                    "type": "big_number",
                    "purpose": "Highlight key metric",
                    "metric": primary.get('metric', ''),
                    "value": primary.get('current', ''),
                    "recommendation": f"Display '{primary.get('metric', '').upper()}' as large number with context",
                    "design_notes": "Bold typography, show % change below, use color for sentiment"
                })

        return visualizations


def load_data(file_path: str) -> Dict[str, Any]:
    """Load data from JSON or CSV file"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    if path.suffix == '.json':
        with open(path, 'r') as f:
            return json.load(f)
    elif path.suffix == '.csv':
        # Convert CSV to structured format
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Assume CSV has columns: metric, previous, current
            data = {"metrics": {}, "period": "CSV data", "context": {}}
            for row in rows:
                metric_name = row.get('metric', '')
                if metric_name:
                    data['metrics'][f"{metric_name}_previous"] = float(row.get('previous', 0))
                    data['metrics'][f"{metric_name}_current"] = float(row.get('current', 0))
            return data
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .json or .csv")


def format_output_html(story: Dict[str, Any], client_name: str) -> str:
    """Format story as HTML report with Roksys branding"""
    narrative = story['narrative']
    dpov = story['main_insight'].get('data_point_of_view', {})
    visualizations = story['visualizations']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{narrative.get('headline', 'Data Story Report')} - {client_name.title()}</title>
    <style>
        body {{
            font-family: Verdana, Geneva, sans-serif;
            font-size: 13px;
            line-height: 1.6;
            color: #2c3e50;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        header {{
            background: linear-gradient(135deg, #2d5016 0%, #1a3009 100%);
            color: white;
            padding: 40px;
            margin: -40px -40px 40px -40px;
            border-radius: 8px 8px 0 0;
            position: relative;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        .logo {{
            position: absolute;
            top: 20px;
            right: 30px;
            width: 120px;
            background: white;
            padding: 5px;
            border-radius: 4px;
        }}
        h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .subtitle {{
            margin: 0;
            opacity: 0.95;
            font-size: 15px;
        }}
        .data-point-of-view {{
            background: #e8f5e9;
            border-left: 4px solid #6CC24A;
            padding: 20px;
            margin: 30px 0;
            border-radius: 4px;
        }}
        .data-point-of-view strong {{
            color: #2d5016;
            display: block;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        .story-section {{
            margin: 30px 0;
        }}
        .story-section h2 {{
            color: #6CC24A;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #6CC24A;
            padding-bottom: 8px;
        }}
        .visualization-recommendation {{
            background: #f8f9fa;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        .visualization-recommendation h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #495057;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #dee2e6;
            font-size: 12px;
            color: #6c757d;
            text-align: center;
        }}
        .metrics-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 3px solid #6CC24A;
        }}
        .metric-card .label {{
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .metric-card .value {{
            font-size: 24px;
            font-weight: 600;
            color: #2d5016;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="file:///Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png" alt="Roksys Logo" class="logo">
            <h1>{narrative.get('headline', 'Data Story Report')}</h1>
            <p class="subtitle">{client_name.title()} Performance Analysis</p>
        </header>

        <div class="data-point-of-view">
            <strong>📊 Data Point of View</strong>
            <p><em>{dpov.get('headline', 'Key insight from performance data')}</em></p>
        </div>

        <div class="story-section">
            <h2>The Story</h2>

            <h3 style="color: #495057; font-size: 15px; margin-top: 20px;">Beginning: The Setup</h3>
            <p>{narrative.get('beginning', '')}</p>

            <h3 style="color: #495057; font-size: 15px; margin-top: 20px;">Middle: The Turning Point</h3>
            <p>{narrative.get('middle', '')}</p>

            <h3 style="color: #495057; font-size: 15px; margin-top: 20px;">End: The Path Forward</h3>
            <p>{narrative.get('end', '')}</p>
        </div>

        <div class="story-section">
            <h2>Key Insights</h2>
            <p><strong>What Happened:</strong> {dpov.get('what_happened', 'Performance changed during this period.')}</p>
            <p><strong>Why It Matters:</strong> {dpov.get('why_matters', 'This change impacts business outcomes.')}</p>
            <p><strong>Recommended Action:</strong> {dpov.get('recommended_action', 'Continue monitoring and adjust strategy.')}</p>
        </div>

        <div class="story-section">
            <h2>Visualization Recommendations</h2>
            {''.join([f'''
            <div class="visualization-recommendation">
                <h3>{viz['type'].replace('_', ' ').title()}</h3>
                <p><strong>Purpose:</strong> {viz['purpose']}</p>
                <p><strong>Recommendation:</strong> {viz['recommendation']}</p>
                <p style="font-size: 12px; color: #6c757d; margin-top: 10px;"><em>Design notes: {viz['design_notes']}</em></p>
            </div>
            ''' for viz in visualizations])}
        </div>

        <footer>
            <p><strong>Generated:</strong> {story['metadata']['generated_at'][:10]}</p>
            <p>Data Storytelling Report • Powered by Roksys Analytics</p>
        </footer>
    </div>
</body>
</html>"""

    return html


def format_output_markdown(story: Dict[str, Any], client_name: str) -> str:
    """Format story as Markdown document"""
    narrative = story['narrative']
    dpov = story['main_insight'].get('data_point_of_view', {})
    visualizations = story['visualizations']

    md = f"""# {narrative.get('headline', 'Data Story Report')}

**Client:** {client_name.title()}
**Generated:** {story['metadata']['generated_at'][:10]}
**Audience:** {story['metadata']['audience']}
**Goal:** {story['metadata']['goal']}

---

## Data Point of View

_{dpov.get('headline', 'Key insight from performance data')}_

---

## The Story

### Beginning: The Setup

{narrative.get('beginning', '')}

### Middle: The Turning Point

{narrative.get('middle', '')}

### End: The Path Forward

{narrative.get('end', '')}

---

## Key Insights

**What Happened:** {dpov.get('what_happened', 'Performance changed during this period.')}

**Why It Matters:** {dpov.get('why_matters', 'This change impacts business outcomes.')}

**Recommended Action:** {dpov.get('recommended_action', 'Continue monitoring and adjust strategy.')}

---

## Visualization Recommendations

{''.join([f'''
### {viz['type'].replace('_', ' ').title()}

**Purpose:** {viz['purpose']}

**Recommendation:** {viz['recommendation']}

_Design notes: {viz['design_notes']}_

''' for viz in visualizations])}

---

_Data Storytelling Report • Generated by Roksys Analytics_
"""

    return md


def save_output(output: str, client_name: str, format_type: str, topic: str = None) -> str:
    """Save output to appropriate location"""
    timestamp = datetime.now().strftime('%Y-%m-%d')

    if format_type == 'html':
        folder = PROJECT_ROOT / 'clients' / client_name / 'reports'
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"datastory-{timestamp}" + (f"-{topic}" if topic else "") + ".html"
        output_path = folder / filename
    else:  # markdown
        folder = PROJECT_ROOT / 'clients' / client_name / 'documents'
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"datastory-{timestamp}" + (f"-{topic}" if topic else "") + ".md"
        output_path = folder / filename

    with open(output_path, 'w') as f:
        f.write(output)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Data Storytelling Report Agent - Transform data into compelling narratives"
    )
    parser.add_argument('--client', required=True, help="Client name (e.g., smythson)")
    parser.add_argument('--data', required=True, help="Path to data file (JSON or CSV)")
    parser.add_argument('--audience', default='client', choices=['client', 'executive', 'technical'],
                       help="Target audience (default: client)")
    parser.add_argument('--goal', default='track_progress',
                       choices=['diagnose_problem', 'track_progress', 'find_opportunities'],
                       help="Analysis goal (default: track_progress)")
    parser.add_argument('--output-format', default='html', choices=['html', 'markdown'],
                       help="Output format (default: html)")
    parser.add_argument('--topic', help="Optional topic slug for filename")
    parser.add_argument('--test-mode', action='store_true', help="Test mode (display only, don't save)")

    args = parser.parse_args()

    print("🎭 Data Storytelling Report Agent")
    print("=" * 60)
    print()

    try:
        # Load data
        print(f"📂 Loading data from: {args.data}")
        data = load_data(args.data)
        print(f"   ✓ Loaded {len(data.get('metrics', {}))} metrics\n")

        # Generate story
        generator = DataStoryGenerator(
            client_name=args.client,
            data=data,
            audience=args.audience,
            goal=args.goal
        )

        story = generator.generate_story()

        # Format output
        if args.output_format == 'html':
            output = format_output_html(story, args.client)
        else:
            output = format_output_markdown(story, args.client)

        # Save or display
        if args.test_mode:
            print("\n" + "=" * 60)
            print("TEST MODE - Output Preview:")
            print("=" * 60)
            print(output[:1000] + "...\n[truncated]")
        else:
            output_path = save_output(output, args.client, args.output_format, args.topic)
            print(f"\n✅ Data story saved to:")
            print(f"   {output_path}")

            # Open in browser if HTML
            if args.output_format == 'html':
                import subprocess
                subprocess.run(['open', output_path])
                print(f"   🌐 Opened in browser")

        print("\n✨ Data storytelling complete!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
