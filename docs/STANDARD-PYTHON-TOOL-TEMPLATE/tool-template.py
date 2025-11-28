#!/usr/bin/env python3
"""
PetesBrain Tool Template

A template for creating new Python tools in PetesBrain.
Copy this file and customize for your needs.

Author: PetesBrain
Created: 2025-11-28
"""

import os
import sys
from pathlib import Path

# ============================================================================
# STANDARD .ENV LOADER - Include this in every tool
# ============================================================================
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    print(f"Loading environment from {ENV_FILE}")
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("✅ Loaded configuration from .env file")
else:
    print(f"⚠️  Warning: {ENV_FILE} not found")
    print("Create it with: cp .env.example .env")
    print("Then add your API keys to the .env file")
# ============================================================================


def main():
    """Main function"""

    # Check for required API keys
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        print("Add it to .env file:")
        print("  ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print("✅ All configuration loaded")
    print("Starting tool...")

    # Your tool logic here
    # ...


if __name__ == "__main__":
    main()
