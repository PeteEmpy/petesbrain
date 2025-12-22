#!/usr/bin/env python3
"""
Visualize NDA enrollment trends by academic year
- UK: Current academic year (2025/26)
- International: Compare 2024/25 vs 2025/26
"""

import openpyxl
from datetime import datetime
from collections import defaultdict
import json

# Read UK enrollments
print("📊 Reading UK Enrollments...")
uk_wb = openpyxl.load_workbook('../enrolments/NDA-UK-Enrolments-ACTIVE.xlsx')
uk_ws = uk_wb.active
uk_rows = list(uk_ws.rows)

# Read International enrollments from BOTH academic year sheets
print("📊 Reading International Enrollments...")
intl_wb = openpyxl.load_workbook('../enrolments/NDA-International-Enrolments-ACTIVE.xlsx')

# Read 2025-26 sheet
intl_ws_2526 = intl_wb['Year 2025-26']
intl_rows_2526 = list(intl_ws_2526.rows)

# Read 2024-25 sheet
intl_ws_2425 = intl_wb['Year 2024-25']
intl_rows_2425 = list(intl_ws_2425.rows)

print(f"   - Year 2025-26: {len(intl_rows_2526)-1} rows")
print(f"   - Year 2024-25: {len(intl_rows_2425)-1} rows")

# Combine all international rows (skip header from second sheet)
intl_rows = intl_rows_2526 + intl_rows_2425[1:]

# Academic year helper function
def get_academic_year(date):
    """Return academic year (e.g., '2025/26' for Sept 2025 - Aug 2026)"""
    if date.month >= 9:  # Sept-Dec
        return f"{date.year}/{str(date.year + 1)[-2:]}"
    else:  # Jan-Aug
        return f"{date.year - 1}/{str(date.year)[-2:]}"

def get_week_key(date):
    """Return week key for grouping (e.g., '2025-W37')"""
    return date.strftime('%Y-W%U')

# Process UK enrollments by week
uk_by_week = defaultdict(int)
uk_by_academic_year = defaultdict(lambda: defaultdict(int))

for row in uk_rows[1:]:
    if len(row) > 1 and row[1].value:
        date_val = row[1].value
        try:
            if isinstance(date_val, datetime):
                week_key = get_week_key(date_val)
                academic_year = get_academic_year(date_val)

                uk_by_week[week_key] += 1
                uk_by_academic_year[academic_year][week_key] += 1
        except:
            continue

# Process International enrollments by week
intl_by_week = defaultdict(int)
intl_by_academic_year = defaultdict(lambda: defaultdict(int))

for row in intl_rows[1:]:
    if len(row) > 6 and row[1].value:
        date_val = row[1].value
        try:
            if isinstance(date_val, datetime):
                week_key = get_week_key(date_val)
                academic_year = get_academic_year(date_val)

                intl_by_week[week_key] += 1
                intl_by_academic_year[academic_year][week_key] += 1
        except:
            continue

# Prepare data for Chart.js
data_export = {
    'uk': {},
    'international': {}
}

# UK data (all academic years found)
for academic_year in sorted(uk_by_academic_year.keys()):
    weeks = uk_by_academic_year[academic_year]
    sorted_weeks = sorted(weeks.items())

    data_export['uk'][academic_year] = {
        'weeks': [w[0] for w in sorted_weeks],
        'enrollments': [w[1] for w in sorted_weeks],
        'cumulative': []
    }

    # Calculate cumulative
    cumulative = 0
    for week, count in sorted_weeks:
        cumulative += count
        data_export['uk'][academic_year]['cumulative'].append(cumulative)

# International data (all academic years found)
for academic_year in sorted(intl_by_academic_year.keys()):
    weeks = intl_by_academic_year[academic_year]
    sorted_weeks = sorted(weeks.items())

    data_export['international'][academic_year] = {
        'weeks': [w[0] for w in sorted_weeks],
        'enrollments': [w[1] for w in sorted_weeks],
        'cumulative': []
    }

    # Calculate cumulative
    cumulative = 0
    for week, count in sorted_weeks:
        cumulative += count
        data_export['international'][academic_year]['cumulative'].append(cumulative)

# Print summary
print("\n" + "=" * 70)
print("📈 ENROLLMENT TRENDS BY ACADEMIC YEAR")
print("=" * 70)

print("\n🇬🇧 UK Enrollments by Academic Year:")
for academic_year in sorted(uk_by_academic_year.keys()):
    total = sum(uk_by_academic_year[academic_year].values())
    weeks = len(uk_by_academic_year[academic_year])
    avg_per_week = total / weeks if weeks > 0 else 0
    print(f"   {academic_year}: {total:>4} enrollments across {weeks:>2} weeks (avg {avg_per_week:.1f}/week)")

print("\n🌍 International Enrollments by Academic Year:")
for academic_year in sorted(intl_by_academic_year.keys()):
    total = sum(intl_by_academic_year[academic_year].values())
    weeks = len(intl_by_academic_year[academic_year])
    avg_per_week = total / weeks if weeks > 0 else 0
    print(f"   {academic_year}: {total:>4} enrollments across {weeks:>2} weeks (avg {avg_per_week:.1f}/week)")

# Save data for visualization
with open('../documents/enrollment-trends-data.json', 'w') as f:
    json.dump(data_export, f, indent=2)

print("\n✅ Data saved to: documents/enrollment-trends-data.json")
print("✅ Creating HTML visualization...")

# Create HTML with Chart.js
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>NDA Enrollment Trends by Academic Year</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #10B981;
            border-bottom: 3px solid #10B981;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #059669;
            border-bottom: 2px solid #D1FAE5;
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        .chart-container {
            position: relative;
            height: 400px;
            margin: 30px 0;
        }
        .summary {
            background: #F0FDF4;
            border-left: 4px solid #10B981;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .summary h3 {
            color: #059669;
            margin-top: 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #D1FAE5;
        }
        .stat-card h4 {
            margin: 0 0 10px 0;
            color: #065F46;
            font-size: 14px;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: bold;
            color: #10B981;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 NDA Enrollment Trends by Academic Year</h1>

        <div class="summary">
            <h3>Analysis Period</h3>
            <p><strong>UK:</strong> Academic year 2025/26 (September 2025 onwards)</p>
            <p><strong>International:</strong> Comparing 2024/25 vs 2025/26 academic years</p>
            <p><strong>Data Source:</strong> Kelly Rawson enrollment reports (last updated 16 Dec 2025)</p>
        </div>

        <h2>🇬🇧 UK Enrollments - Cumulative Trend</h2>
        <div class="chart-container">
            <canvas id="ukChart"></canvas>
        </div>

        <h2>🌍 International Enrollments - Year-on-Year Comparison</h2>
        <div class="chart-container">
            <canvas id="intlChart"></canvas>
        </div>

        <h2>📊 Summary Statistics</h2>
        <div class="stats" id="statsContainer"></div>
    </div>

    <script>
        const data = """ + json.dumps(data_export, indent=2) + """;

        // UK Chart - Cumulative with aligned week numbers
        const ukAcademicYears = Object.keys(data.uk).sort();

        // Create aligned week labels (Week 1, Week 2, etc.) for better comparison
        const maxUkWeeks = Math.max(...ukAcademicYears.map(year => data.uk[year].weeks.length));
        const ukWeekLabels = Array.from({length: maxUkWeeks}, (_, i) => `Week ${i + 1}`);

        const ukDatasets = ukAcademicYears.map((year, index) => {
            const yearData = data.uk[year];
            // Pad data with nulls if shorter than max weeks
            const paddedData = [...yearData.cumulative];
            while (paddedData.length < maxUkWeeks) {
                paddedData.push(null);
            }

            const colors = ['#10B981', '#3B82F6', '#8B5CF6'];
            return {
                label: 'Academic Year ' + year,
                data: paddedData,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '20',
                tension: 0.3,
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6,
                spanGaps: false
            };
        });

        const ukCtx = document.getElementById('ukChart').getContext('2d');
        const ukChart = new Chart(ukCtx, {
            type: 'line',
            data: {
                labels: ukWeekLabels,
                datasets: ukDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'UK Cumulative Enrollments - Week-by-Week Comparison',
                        font: { size: 16 }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cumulative Enrollments'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Week of Academic Year'
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });

        // International Chart - Comparison
        const intlAcademicYears = Object.keys(data.international).sort();
        const intlDatasets = intlAcademicYears.map((year, index) => {
            const yearData = data.international[year];
            const colors = ['#10B981', '#3B82F6', '#8B5CF6'];
            return {
                label: 'Academic Year ' + year,
                data: yearData.cumulative,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '20',
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
            };
        });

        // Get the longest week array for x-axis
        let longestWeeks = [];
        intlAcademicYears.forEach(year => {
            if (data.international[year].weeks.length > longestWeeks.length) {
                longestWeeks = data.international[year].weeks;
            }
        });

        const intlCtx = document.getElementById('intlChart').getContext('2d');
        const intlChart = new Chart(intlCtx, {
            type: 'line',
            data: {
                labels: longestWeeks,
                datasets: intlDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'International Cumulative Enrollments - Year-on-Year Comparison',
                        font: { size: 16 }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cumulative Enrollments'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Week'
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });

        // Generate summary statistics
        const statsContainer = document.getElementById('statsContainer');

        // UK stats
        ukAcademicYears.forEach(year => {
            const total = data.uk[year].cumulative[data.uk[year].cumulative.length - 1];
            const weeks = data.uk[year].weeks.length;
            const avgPerWeek = (total / weeks).toFixed(1);

            statsContainer.innerHTML += `
                <div class="stat-card">
                    <h4>UK ${year}</h4>
                    <div class="value">${total}</div>
                    <p>${weeks} weeks • ${avgPerWeek} avg/week</p>
                </div>
            `;
        });

        // International stats
        intlAcademicYears.forEach(year => {
            const total = data.international[year].cumulative[data.international[year].cumulative.length - 1];
            const weeks = data.international[year].weeks.length;
            const avgPerWeek = (total / weeks).toFixed(1);

            statsContainer.innerHTML += `
                <div class="stat-card">
                    <h4>International ${year}</h4>
                    <div class="value">${total}</div>
                    <p>${weeks} weeks • ${avgPerWeek} avg/week</p>
                </div>
            `;
        });

        // Year-on-year comparison for UK
        if (ukAcademicYears.length > 1) {
            const current = ukAcademicYears[ukAcademicYears.length - 1];
            const previous = ukAcademicYears[ukAcademicYears.length - 2];

            const currentTotal = data.uk[current].cumulative[data.uk[current].cumulative.length - 1];
            const currentWeeks = data.uk[current].weeks.length;
            const currentAvg = currentTotal / currentWeeks;

            const previousTotal = data.uk[previous].cumulative[data.uk[previous].cumulative.length - 1];
            const previousWeeks = data.uk[previous].weeks.length;
            const previousAvg = previousTotal / previousWeeks;

            const avgChange = currentAvg - previousAvg;
            const avgChangePercent = ((avgChange / previousAvg) * 100).toFixed(1);

            statsContainer.innerHTML += `
                <div class="stat-card" style="grid-column: span 2; background: ${avgChange >= 0 ? '#F0FDF4' : '#FEF2F2'};">
                    <h4>UK Growth Rate (${previous} → ${current})</h4>
                    <div class="value" style="color: ${avgChange >= 0 ? '#10B981' : '#EF4444'};">
                        ${currentAvg.toFixed(1)} avg/week (${avgChangePercent >= 0 ? '+' : ''}${avgChangePercent}% vs ${previous})
                    </div>
                    <p>Current year showing ${currentTotal} enrollments over ${currentWeeks} weeks</p>
                </div>
            `;
        }

        // Year-on-year comparison for international
        if (intlAcademicYears.length > 1) {
            const current = intlAcademicYears[intlAcademicYears.length - 1];
            const previous = intlAcademicYears[intlAcademicYears.length - 2];

            const currentTotal = data.international[current].cumulative[data.international[current].cumulative.length - 1];
            const previousTotal = data.international[previous].cumulative[data.international[previous].cumulative.length - 1];

            const change = currentTotal - previousTotal;
            const changePercent = ((change / previousTotal) * 100).toFixed(1);

            statsContainer.innerHTML += `
                <div class="stat-card" style="grid-column: span 2; background: ${change >= 0 ? '#F0FDF4' : '#FEF2F2'};">
                    <h4>International YoY Change (${previous} → ${current})</h4>
                    <div class="value" style="color: ${change >= 0 ? '#10B981' : '#EF4444'};">
                        ${change >= 0 ? '+' : ''}${change} (${changePercent >= 0 ? '+' : ''}${changePercent}%)
                    </div>
                    <p>Comparing same period in academic year</p>
                </div>
            `;
        }
    </script>
</body>
</html>"""

with open('../documents/enrollment-trends-visualization.html', 'w') as f:
    f.write(html_content)

print("✅ Visualization created: documents/enrollment-trends-visualization.html")
print("=" * 70)
