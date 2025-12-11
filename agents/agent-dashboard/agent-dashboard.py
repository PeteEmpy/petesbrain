#!/usr/bin/env python3
"""
PetesBrain Agent Dashboard

Interactive dashboard showing status of all LaunchAgents.
Provides quick overview and actions for managing agents.

Usage:
    python3 agents/agent-dashboard/agent-dashboard.py [--status] [--restart NAME] [--logs NAME]
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from shared.scripts.launchagent_discovery import get_all_agents_with_status
    DISCOVERY_AVAILABLE = True
except ImportError as e:
    print(f"❌ Required modules not available: {e}")
    sys.exit(1)


def check_agent_health_simple(agent: Dict) -> Dict:
    """Simple health check for dashboard"""
    import subprocess
    
    label = agent['label']
    log_path = agent.get('log_path', '')
    workflow_type = agent.get('workflow_type', 'on_demand')
    interval_seconds = agent.get('interval_seconds')
    
    checks = {}
    
    # Check if running
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True,
            text=True,
            timeout=5
        )
        checks['running'] = result.returncode == 0
    except:
        checks['running'] = False
    
    # Check log freshness
    if log_path:
        log_path = os.path.expanduser(log_path)
        if os.path.exists(log_path):
            from datetime import datetime
            log_mtime = datetime.fromtimestamp(os.path.getmtime(log_path))
            age_hours = (datetime.now() - log_mtime).total_seconds() / 3600
            
            if workflow_type == "interval" and interval_seconds:
                max_age = (interval_seconds / 3600) + 1
            elif workflow_type == "daily":
                max_age = 25
            else:
                max_age = 25
            
            checks['log_fresh'] = age_hours <= max_age
        else:
            checks['log_fresh'] = True  # No log yet is OK
    
    is_healthy = checks.get('running', False) and checks.get('log_fresh', True)
    
    return {
        'healthy': is_healthy,
        'checks': checks
    }


def format_duration(seconds):
    """Format seconds into human-readable duration"""
    if seconds is None:
        return "N/A"
    
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds//60}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def show_dashboard():
    """Show full agent dashboard"""
    print("="*80)
    print("PetesBrain Agent Dashboard")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()
    
    agents = get_all_agents_with_status()
    
    if not agents:
        print("⚠️  No agents found")
        return
    
    # Get health status for all
    print("🔍 Checking agent health...")
    health_results = {}
    for agent in agents:
        try:
            result = check_agent_health_simple(agent)
            health_results[agent['name']] = result
        except Exception as e:
            health_results[agent['name']] = {
                'healthy': False,
                'error': str(e)
            }
    
    print()
    
    # Group by status
    healthy = []
    unhealthy_critical = []
    unhealthy_non_critical = []
    
    for agent in agents:
        name = agent['name']
        health = health_results.get(name, {})
        
        if health.get('healthy', False):
            healthy.append((agent, health))
        elif agent.get('critical', False):
            unhealthy_critical.append((agent, health))
        else:
            unhealthy_non_critical.append((agent, health))
    
    # Show critical issues first
    if unhealthy_critical:
        print("🔴 CRITICAL AGENTS NEEDING ATTENTION")
        print("="*80)
        for agent, health in unhealthy_critical:
            status_icon = "❌" if not health.get('healthy') else "✅"
            print(f"\n{status_icon} {agent['name']}")
            print(f"   Description: {agent.get('description', 'N/A')}")
            print(f"   Schedule: {agent.get('schedule_type', 'N/A')}", end="")
            if agent.get('interval_seconds'):
                print(f" (every {format_duration(agent['interval_seconds'])})")
            else:
                print()
            print(f"   Log: {agent.get('log_path', 'N/A')}")
            
            checks = health.get('checks', {})
            if not checks.get('running', True):
                print(f"   ⚠️  Process NOT RUNNING")
            if not checks.get('log_fresh', True):
                print(f"   ⚠️  Log stale")
            if 'activity' in checks and not checks['activity']:
                print(f"   ⚠️  Activity check failed")
            print()
    
    # Show non-critical issues
    if unhealthy_non_critical:
        print("⚪ NON-CRITICAL AGENTS WITH ISSUES")
        print("="*80)
        for agent, health in unhealthy_non_critical[:10]:  # Limit to 10
            status_icon = "❌" if not health.get('healthy') else "✅"
            print(f"{status_icon} {agent['name']}: {agent.get('description', 'N/A')}")
            checks = health.get('checks', {})
            issues = []
            if not checks.get('running', True):
                issues.append("not running")
            if not checks.get('log_fresh', True):
                issues.append("stale log")
            if issues:
                print(f"   Issues: {', '.join(issues)}")
        print()
    
    # Show healthy agents summary
    print("✅ HEALTHY AGENTS")
    print("="*80)
    print(f"{len(healthy)} agent(s) running correctly\n")
    
    # Group healthy by category
    critical_healthy = [a for a, h in healthy if a.get('critical', False)]
    non_critical_healthy = [a for a, h in healthy if not a.get('critical', False)]
    
    if critical_healthy:
        print(f"🔴 Critical ({len(critical_healthy)}):")
        for agent in sorted(critical_healthy, key=lambda x: x['name']):
            print(f"   ✅ {agent['name']}")
        print()
    
    if non_critical_healthy:
        print(f"⚪ Non-critical ({len(non_critical_healthy)}):")
        for agent in sorted(non_critical_healthy, key=lambda x: x['name'])[:10]:  # Show first 10
            print(f"   ✅ {agent['name']}")
        if len(non_critical_healthy) > 10:
            print(f"   ... and {len(non_critical_healthy) - 10} more")
        print()
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total agents: {len(agents)}")
    print(f"Healthy: {len(healthy)}")
    print(f"Critical issues: {len(unhealthy_critical)}")
    print(f"Non-critical issues: {len(unhealthy_non_critical)}")
    print()
    
    # Quick actions
    if unhealthy_critical or unhealthy_non_critical:
        print("💡 Quick Actions:")
        print("   Run health check: python3 agents/health-check/health-check.py --verbose")
        print("   Restart unhealthy: python3 agents/health-check/health-check.py --restart-unhealthy")
        print("   View agent logs: tail -f ~/.petesbrain-AGENT-NAME.log")
        print()


def show_agent_status(name: str):
    """Show detailed status for a specific agent"""
    agents = get_all_agents_with_status()
    
    agent = next((a for a in agents if a['name'] == name), None)
    if not agent:
        print(f"❌ Agent '{name}' not found")
        return
    
    print("="*80)
    print(f"Agent: {agent['name']}")
    print("="*80)
    print()
    
    print(f"Label: {agent['label']}")
    print(f"Description: {agent.get('description', 'N/A')}")
    print(f"Schedule: {agent.get('schedule_type', 'N/A')}", end="")
    if agent.get('interval_seconds'):
        print(f" (every {format_duration(agent['interval_seconds'])})")
    else:
        print()
    print(f"Critical: {'Yes' if agent.get('critical') else 'No'}")
    print(f"Script: {agent.get('script_path', 'N/A')}")
    print(f"Log: {agent.get('log_path', 'N/A')}")
    print()
    
    # Check health
    print("Health Check:")
    print("-" * 80)
    result = check_agent_health_simple(agent)
    
    checks = result.get('checks', {})
    print(f"Running: {'✅' if checks.get('running') else '❌'}")
    if 'log_fresh' in checks:
        print(f"Log fresh: {'✅' if checks.get('log_fresh') else '❌'}")
    print()


def show_agent_logs(name: str, lines: int = 50):
    """Show recent logs for an agent"""
    agents = get_all_agents_with_status()
    
    agent = next((a for a in agents if a['name'] == name), None)
    if not agent:
        print(f"❌ Agent '{name}' not found")
        return
    
    log_path = agent.get('log_path')
    if not log_path:
        print(f"⚠️  No log file configured for {name}")
        return
    
    log_path = os.path.expanduser(log_path)
    
    if not os.path.exists(log_path):
        print(f"⚠️  Log file not found: {log_path}")
        return
    
    print("="*80)
    print(f"Recent logs for: {agent['name']}")
    print(f"File: {log_path}")
    print("="*80)
    print()
    
    try:
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            for line in recent_lines:
                print(line.rstrip())
    except Exception as e:
        print(f"❌ Error reading log: {e}")


def restart_agent(name: str):
    """Restart a specific agent"""
    import subprocess
    
    agents = get_all_agents_with_status()
    
    agent = next((a for a in agents if a['name'] == name), None)
    if not agent:
        print(f"❌ Agent '{name}' not found")
        return
    
    label = agent['label']
    
    print(f"🔄 Restarting {name}...")
    
    try:
        # Stop
        subprocess.run(['launchctl', 'stop', label], check=True, capture_output=True)
        import time
        time.sleep(1)
        
        # Start
        subprocess.run(['launchctl', 'start', label], check=True, capture_output=True)
        
        print(f"✅ Restarted {name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to restart {name}: {e}")


def generate_html_dashboard():
    """Generate HTML dashboard and open in browser"""
    import webbrowser
    import tempfile

    agents = get_all_agents_with_status()

    if not agents:
        print("❌ No agents found")
        return

    # Get health status for all
    health_results = {}
    for agent in agents:
        try:
            result = check_agent_health_simple(agent)
            health_results[agent['name']] = result
        except Exception as e:
            health_results[agent['name']] = {
                'healthy': False,
                'error': str(e)
            }

    # Group by status
    healthy = []
    unhealthy_critical = []
    unhealthy_non_critical = []

    for agent in agents:
        name = agent['name']
        health = health_results.get(name, {})

        if health.get('healthy', False):
            healthy.append((agent, health))
        elif agent.get('critical', False):
            unhealthy_critical.append((agent, health))
        else:
            unhealthy_non_critical.append((agent, health))

    # Generate HTML
    html = """
    <html>
    <head>
        <title>🧠 Pete's Brain Agent Dashboard</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 8px;
                padding: 0;
                background: #f5f5f5;
                color: #333;
                font-size: 13px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding: 5px 0;
                margin: 0 0 3px 0;
                font-size: 18px;
            }
            h2 {
                color: #34495e;
                margin: 8px 0 3px 0;
                border-left: 3px solid #e74c3c;
                padding-left: 6px;
                font-size: 14px;
            }
            h3 {
                margin: 5px 0 3px 0;
                font-size: 13px;
            }
            .critical { color: #e74c3c; font-weight: bold; }
            .healthy { color: #27ae60; font-weight: bold; }
            .agent {
                background: white;
                padding: 6px 8px;
                margin: 3px 0;
                border-radius: 3px;
                border-left: 3px solid #95a5a6;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                font-size: 12px;
            }
            .agent.critical-unhealthy {
                border-left-color: #e74c3c;
                background: #fdeaea;
            }
            .agent.healthy {
                border-left-color: #27ae60;
            }
            .summary {
                background: white;
                padding: 8px 10px;
                border-radius: 3px;
                margin: 5px 0;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                font-size: 12px;
            }
            .summary p {
                margin: 2px 0;
            }
            .time {
                color: #7f8c8d;
                font-size: 11px;
                margin: 2px 0 5px 0;
            }
            small {
                font-size: 11px;
                color: #666;
            }
            span {
                display: block;
                margin: 1px 0;
                font-size: 11px;
            }
        </style>
    </head>
    <body>
        <h1>🧠 Pete's Brain Agent Dashboard</h1>
        <p class="time">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    """

    # Quick Actions section at the top
    if unhealthy_critical or unhealthy_non_critical:
        html += """
        <div class="summary" style="background: #e8f4f8; border-left: 3px solid #3498db; padding: 6px 8px;">
            <strong>⚡ Quick Actions:</strong><br/>
        """

        html += """
        <span style="margin: 2px 0; font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 2px 4px; border-radius: 2px; display: inline-block;">
            python3 agents/health-check/health-check.py --restart-unhealthy
        </span><br/>
        <small style="display: block; margin: 1px 0;">to restart all unhealthy agents</small>
        """

        if unhealthy_critical:
            agent_names = ', '.join([a[0]['name'] for a in unhealthy_critical])
            html += f"""
            <span style="margin: 2px 0; font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 2px 4px; border-radius: 2px; display: inline-block;">
                tail -f ~/.petesbrain-AGENT-NAME.log
            </span><br/>
            <small style="display: block; margin: 1px 0;">to watch logs for: {agent_names}</small>
            """

        html += """
        </div>
        """

    # Critical issues
    if unhealthy_critical:
        html += "<h2>🔴 CRITICAL AGENTS NEEDING ATTENTION</h2>"
        for agent, health in unhealthy_critical:
            html += f'<div class="agent critical-unhealthy">'
            html += f'<strong>❌ {agent["name"]}</strong><br/>'
            html += f'<small>{agent.get("description", "N/A")}</small><br/>'
            checks = health.get('checks', {})
            if not checks.get('running', True):
                html += '<span style="color: #e74c3c;">⚠️ Process NOT RUNNING</span><br/>'
            if not checks.get('log_fresh', True):
                html += '<span style="color: #e74c3c;">⚠️ Log stale</span><br/>'
            html += '</div>'

    # Non-critical issues
    if unhealthy_non_critical:
        html += "<h2>⚪ NON-CRITICAL AGENTS WITH ISSUES</h2>"
        for agent, health in unhealthy_non_critical[:10]:
            html += f'<div class="agent">'
            html += f'<strong>❌ {agent["name"]}</strong><br/>'
            html += f'<small>{agent.get("description", "N/A")}</small><br/>'
            checks = health.get('checks', {})
            issues = []
            if not checks.get('running', True):
                issues.append("not running")
            if not checks.get('log_fresh', True):
                issues.append("stale log")
            if issues:
                html += f'<span style="color: #f39c12;">Issues: {", ".join(issues)}</span>'
            html += '</div>'

    # Healthy agents summary
    html += "<h2>✅ HEALTHY AGENTS</h2>"
    html += f'<div class="summary"><strong>{len(healthy)}</strong> agent(s) running correctly</div>'

    # Summary
    html += """
    <div class="summary">
        <h3>Summary</h3>
        <p><strong>Total agents:</strong> """ + str(len(agents)) + """</p>
        <p><strong>Healthy:</strong> """ + str(len(healthy)) + """</p>
        <p><strong>Critical issues:</strong> """ + str(len(unhealthy_critical)) + """</p>
        <p><strong>Non-critical issues:</strong> """ + str(len(unhealthy_non_critical)) + """</p>
    </div>
    """

    html += """
    </body>
    </html>
    """

    # Save to temp file and open in browser
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html)
        temp_path = f.name

    webbrowser.open(f'file://{temp_path}')
    print(f"✅ Dashboard opened in browser")


def main():
    if len(sys.argv) == 1:
        generate_html_dashboard()
    elif sys.argv[1] == '--status' and len(sys.argv) > 2:
        show_agent_status(sys.argv[2])
    elif sys.argv[1] == '--logs' and len(sys.argv) > 2:
        lines = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        show_agent_logs(sys.argv[2], lines)
    elif sys.argv[1] == '--restart' and len(sys.argv) > 2:
        restart_agent(sys.argv[2])
    else:
        print("Usage:")
        print("  python3 agent-dashboard.py                    # Show full dashboard")
        print("  python3 agent-dashboard.py --status NAME      # Show agent details")
        print("  python3 agent-dashboard.py --logs NAME [N]    # Show recent logs (N lines)")
        print("  python3 agent-dashboard.py --restart NAME     # Restart agent")


if __name__ == '__main__':
    main()

