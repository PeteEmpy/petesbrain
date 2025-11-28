#!/usr/bin/env python3
"""
MCP Integration Script for Daily Task Generator

This script is called by Claude Code (with MCP tools available) to actually create
tasks in Google Tasks. It reads the daily-tasks.json file and creates tasks using
the Google Tasks MCP tools.

This is separate from generate_daily_tasks.py to allow that script to run standalone
for testing without requiring MCP tools.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_daily_tasks():
    """Load tasks from daily-tasks.json"""
    tasks_file = Path(__file__).parent / "daily-tasks.json"

    if not tasks_file.exists():
        print("❌ No daily-tasks.json file found. Run generate_daily_tasks.py first.")
        sys.exit(1)

    with open(tasks_file) as f:
        data = json.load(f)

    return data


def main():
    """
    This function is intended to be called from Claude Code with MCP tools available.

    It will:
    1. Load tasks from daily-tasks.json
    2. Get or create a "Client Action Items" task list
    3. Create tasks using mcp__google-tasks__create_task
    """

    print("=" * 80)
    print("MCP GOOGLE TASKS INTEGRATION")
    print("=" * 80)
    print()

    # Load tasks
    data = load_daily_tasks()
    action_items = data.get('action_items', [])

    if not action_items:
        print("No action items found in daily-tasks.json")
        return

    print(f"📋 Found {len(action_items)} action items to create")
    print()

    # Instructions for Claude Code
    print("=" * 80)
    print("INSTRUCTIONS FOR CLAUDE CODE")
    print("=" * 80)
    print()
    print("Please use the following MCP tools to create these tasks:")
    print()
    print("1. mcp__google-tasks__list_task_lists()")
    print("   → Get existing task lists")
    print()
    print("2. If 'Client Action Items' list doesn't exist:")
    print("   mcp__google-tasks__create_task_list(title='Client Action Items')")
    print()
    print("3. For each action item below, call:")
    print("   mcp__google-tasks__create_task(")
    print("       tasklist_id='...',")
    print("       title='[client] task',")
    print("       notes='From: ...\\nDate: ...\\nFile: ...'")
    print("   )")
    print()
    print("=" * 80)
    print("ACTION ITEMS TO CREATE")
    print("=" * 80)
    print()

    # Group by client for display
    by_client = {}
    for item in action_items:
        client = item['client']
        if client not in by_client:
            by_client[client] = []
        by_client[client].append(item)

    # Display tasks
    for client, items in sorted(by_client.items()):
        print(f"🏢 {client.upper()} ({len(items)} tasks)")
        print("-" * 80)

        for item in items:
            title = f"[{client}] {item['task']}"
            notes = f"From: {item['meeting_title']}\n"
            notes += f"Date: {item['meeting_date']}\n"
            notes += f"File: {item['file']}"

            print(f"Title: {title}")
            print(f"Notes:\n{notes}")
            print()

    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
