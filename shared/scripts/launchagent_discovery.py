#!/usr/bin/env python3
"""
LaunchAgent Discovery System

Automatically discovers and monitors all PetesBrain LaunchAgents by:
1. Scanning ~/Library/LaunchAgents/ for com.petesbrain.*.plist files
2. Parsing plist files to extract configuration
3. Determining schedule type (interval/daily/weekly)
4. Identifying log file paths
5. Detecting critical vs non-critical agents

This enables automatic health monitoring without manual configuration.
"""

import os
import sys
import subprocess
import plistlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# LaunchAgents directory
LAUNCH_AGENTS_DIR = Path.home() / 'Library' / 'LaunchAgents'

# PetesBrain project root (inferred from common paths)
PROJECT_ROOT = Path(__file__).parent.parent.parent if __file__ else Path('/Users/administrator/Documents/PetesBrain')


def discover_launch_agents() -> List[Dict]:
    """
    Discover all PetesBrain LaunchAgents by scanning plist files.
    
    Returns:
        List of agent configurations with all metadata
    """
    agents = []
    
    if not LAUNCH_AGENTS_DIR.exists():
        return agents
    
    # Find all com.petesbrain.*.plist files
    plist_files = list(LAUNCH_AGENTS_DIR.glob('com.petesbrain.*.plist'))
    
    for plist_path in plist_files:
        try:
            agent_info = parse_plist(plist_path)
            if agent_info:
                agents.append(agent_info)
        except Exception as e:
            print(f"⚠️  Error parsing {plist_path.name}: {e}", file=sys.stderr)
            continue
    
    return agents


def parse_plist(plist_path: Path) -> Optional[Dict]:
    """
    Parse a LaunchAgent plist file and extract configuration.
    
    Returns:
        Dict with agent configuration or None if not a PetesBrain agent
    """
    try:
        with open(plist_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        label = plist_data.get('Label', '')
        if not label.startswith('com.petesbrain.'):
            return None
        
        # Extract basic info
        agent_name = label.replace('com.petesbrain.', '')
        
        # Get program arguments
        program_args = plist_data.get('ProgramArguments', [])
        script_path = program_args[-1] if len(program_args) > 1 else None
        
        # Determine schedule type
        schedule_type, interval_seconds = detect_schedule_type(plist_data)
        
        # Get log paths
        stdout_log = plist_data.get('StandardOutPath', '')
        stderr_log = plist_data.get('StandardErrorPath', '')
        
        # Use stdout log as primary, fallback to stderr
        log_path = stdout_log if stdout_log else stderr_log
        
        # Determine if critical (based on name patterns and schedule)
        is_critical = determine_criticality(agent_name, schedule_type, interval_seconds)
        
        # Get description from script path or agent name
        description = infer_description(agent_name, script_path)
        
        # Determine workflow type for health checking
        workflow_type = determine_workflow_type(schedule_type, interval_seconds)
        
        return {
            'name': agent_name,
            'label': label,
            'plist_path': str(plist_path),
            'script_path': script_path,
            'schedule_type': schedule_type,
            'interval_seconds': interval_seconds,
            'log_path': log_path,
            'stdout_log': stdout_log,
            'stderr_log': stderr_log,
            'critical': is_critical,
            'description': description,
            'workflow_type': workflow_type,
            'working_directory': plist_data.get('WorkingDirectory', ''),
            'environment_vars': plist_data.get('EnvironmentVariables', {}),
        }
        
    except Exception as e:
        print(f"⚠️  Error parsing {plist_path}: {e}", file=sys.stderr)
        return None


def detect_schedule_type(plist_data: Dict) -> Tuple[str, Optional[int]]:
    """
    Detect schedule type from plist data.
    
    Returns:
        (schedule_type, interval_seconds)
        schedule_type: 'interval', 'daily', 'weekly', 'on_demand', 'unknown'
    """
    # Check for StartInterval (interval-based)
    if 'StartInterval' in plist_data:
        interval = plist_data['StartInterval']
        return 'interval', interval
    
    # Check for StartCalendarInterval (scheduled)
    if 'StartCalendarInterval' in plist_data:
        interval = plist_data['StartCalendarInterval']
        
        # If it has Hour and Minute, it's daily
        if 'Hour' in interval and 'Minute' in interval:
            # Check if it's weekly (has Weekday)
            if 'Weekday' in interval:
                return 'weekly', None
            return 'daily', None
        
        return 'scheduled', None
    
    # Check for KeepAlive (daemon/continuous)
    if plist_data.get('KeepAlive'):
        return 'daemon', None
    
    # Default: on-demand
    return 'on_demand', None


def determine_criticality(agent_name: str, schedule_type: str, interval_seconds: Optional[int]) -> bool:
    """
    Determine if an agent is critical based on name patterns and schedule.
    
    Critical agents:
    - Run frequently (interval < 1 hour)
    - Core automation (email-sync, inbox-processor, wispr-flow, etc.)
    - Monitoring agents (anomaly-detector, health-check)
    """
    # Critical name patterns
    critical_patterns = [
        'email-sync', 'email-auto-label',
        'inbox-processor', 'ai-inbox-processor',
        'wispr-flow', 'granola',
        'anomaly', 'health-check',
        'tasks-monitor', 'knowledge-base',
        'industry-news', 'ai-news',
    ]
    
    # Check name patterns
    for pattern in critical_patterns:
        if pattern in agent_name.lower():
            return True
    
    # High-frequency intervals are critical
    if schedule_type == 'interval' and interval_seconds:
        if interval_seconds < 3600:  # Less than 1 hour
            return True
    
    # Daemons are critical
    if schedule_type == 'daemon':
        return True
    
    return False


def infer_description(agent_name: str, script_path: Optional[str]) -> str:
    """
    Infer a human-readable description from agent name and script path.
    """
    # Common descriptions
    descriptions = {
        'ai-inbox-processor': 'AI inbox processor (every 10 min)',
        'email-sync': 'Email sync workflow (every 6 hours)',
        'email-auto-label': 'Email auto-labeling (deprecated - use email-sync)',
        'wispr-flow-importer': 'Wispr Flow notes importer (every 30 min)',
        'inbox-processor': 'Inbox processor (daily 8 AM)',
        'daily-briefing': 'Daily briefing generator (daily 7 AM)',
        'granola-google-docs-importer': 'Granola meeting importer (every 1 hour)',
        'trend-monitor': 'Google Trends monitor (weekly)',
        'weekly-blog-generator': 'Weekly blog generator (weekly)',
        'tasks-monitor': 'Google Tasks sync (every 6 hours)',
        'knowledge-base': 'Knowledge base processor (every 6 hours)',
        'industry-news': 'Industry news monitor (every 6 hours)',
        'ai-news': 'AI news monitor (every 6 hours)',
        'daily-anomaly-alerts': 'Daily anomaly detector (daily 9 AM)',
        'budget-monitor': 'Budget monitor (daily 10 AM)',
        'devonshire-budget': 'Devonshire budget tracker (every 6 hours)',
        'kb-weekly-summary': 'KB weekly summary (Mon 8:30 AM)',
        'granola-weekly-summary': 'Meeting weekly review (Mon 9 AM)',
        'product-data-fetcher': 'Product data fetcher (daily 6 AM)',
        'label-snapshots': 'Product label snapshots (daily)',
        'weekly-label-reports': 'Weekly label reports (Mon)',
        'smythson-dashboard': 'Smythson Q4 dashboard (daily)',
        'populate-spreadsheets': 'Populate spreadsheets (daily 4 AM)',
        'merchant-center': 'Merchant Center monitor (every 6 hours)',
        'nda-enrolments': 'NDA enrolments tracker (daily 7 AM)',
        'kb-indexer': 'Knowledge base indexer',
        'tree2mydoor-context-upload': 'Tree2MyDoor context upload',
        'product-impact-analyzer': 'Product impact analyzer',
        'shared-drives': 'Shared drives monitor',
    }
    
    # Check exact match first
    if agent_name in descriptions:
        return descriptions[agent_name]
    
    # Try partial matches
    for key, desc in descriptions.items():
        if key in agent_name or agent_name in key:
            return desc
    
    # Fallback: generate from name
    readable_name = agent_name.replace('-', ' ').title()
    return f"{readable_name} agent"


def determine_workflow_type(schedule_type: str, interval_seconds: Optional[int]) -> str:
    """
    Determine workflow type for health checking.
    
    Returns: 'daemon', 'interval', 'daily', 'weekly', 'on_demand'
    """
    if schedule_type == 'daemon':
        return 'daemon'
    elif schedule_type == 'interval':
        return 'interval'
    elif schedule_type == 'daily' or schedule_type == 'scheduled':
        return 'daily'
    elif schedule_type == 'weekly':
        return 'weekly'
    else:
        return 'on_demand'


def get_agent_status(label: str) -> Dict:
    """
    Get current status of a LaunchAgent.
    
    Returns:
        Dict with status information
    """
    try:
        result = subprocess.run(
            ['launchctl', 'list', label],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        is_loaded = result.returncode == 0
        
        # Parse output if loaded
        last_exit_status = None
        if is_loaded:
            # Extract LastExitStatus from plutil output
            try:
                plist_path = LAUNCH_AGENTS_DIR / f"{label}.plist"
                if plist_path.exists():
                    with open(plist_path, 'rb') as f:
                        plist_data = plistlib.load(f)
                    # Note: LastExitStatus is runtime info, not in plist
                    # We'd need to query launchctl for this
            except:
                pass
        
        return {
            'loaded': is_loaded,
            'last_exit_status': last_exit_status,
            'error': None if is_loaded else result.stderr.strip()
        }
        
    except subprocess.TimeoutExpired:
        return {
            'loaded': False,
            'last_exit_status': None,
            'error': 'Timeout checking status'
        }
    except Exception as e:
        return {
            'loaded': False,
            'last_exit_status': None,
            'error': str(e)
        }


def get_all_agents_with_status() -> List[Dict]:
    """
    Discover all agents and add their current status.
    
    Returns:
        List of agents with status information
    """
    agents = discover_launch_agents()
    
    for agent in agents:
        status = get_agent_status(agent['label'])
        agent['status'] = status
        agent['is_healthy'] = status['loaded']
    
    return agents


if __name__ == '__main__':
    """Test the discovery system"""
    print("="*80)
    print("LaunchAgent Discovery System")
    print("="*80)
    print()
    
    agents = get_all_agents_with_status()
    
    print(f"Found {len(agents)} PetesBrain LaunchAgent(s)\n")
    
    for agent in sorted(agents, key=lambda x: x['name']):
        status_icon = "✅" if agent['is_healthy'] else "❌"
        critical_icon = "🔴" if agent['critical'] else "⚪"
        
        print(f"{status_icon} {critical_icon} {agent['name']}")
        print(f"   Label: {agent['label']}")
        print(f"   Description: {agent['description']}")
        print(f"   Schedule: {agent['schedule_type']}", end="")
        if agent['interval_seconds']:
            hours = agent['interval_seconds'] / 3600
            print(f" (every {hours:.1f}h)" if hours >= 1 else f" (every {agent['interval_seconds']/60:.0f}m)")
        else:
            print()
        print(f"   Log: {agent['log_path']}")
        print(f"   Status: {'Loaded' if agent['status']['loaded'] else 'NOT LOADED'}")
        if agent['status']['error']:
            print(f"   Error: {agent['status']['error']}")
        print()

