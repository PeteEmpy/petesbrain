#!/usr/bin/env python3
"""
Create Google Docs for All Clients
Creates a Google Doc for each client's CONTEXT.md and tracks the document IDs
"""

import os
import json
from pathlib import Path
from datetime import datetime

CLIENTS_DIR = Path("/Users/administrator/Documents/PetesBrain/clients")
DOC_REGISTRY = Path("/Users/administrator/Documents/PetesBrain/data/cache/client-google-docs.json")
LOG_FILE = Path.home() / ".petesbrain-client-docs-setup.log"

# List of clients (excluding special folders)
CLIENTS = [
    "accessories-for-the-home",
    "bright-minds",
    "clear-prospects",
    "crowd-control",
    "devonshire-hotels",
    "go-glean",
    "godshot",
    "grain-guard",
    "just-bin-bags",
    "national-design-academy",
    "positive-bakes",
    "smythson",
    "superspace",
    "tree2mydoor",
    "uno-lighting"
]

def log_message(message):
    """Log message to both stdout and log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + "\n")

def load_registry():
    """Load existing document registry"""
    if DOC_REGISTRY.exists():
        with open(DOC_REGISTRY, 'r') as f:
            return json.load(f)
    return {}

def save_registry(registry):
    """Save document registry"""
    DOC_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_REGISTRY, 'w') as f:
        json.dump(registry, indent=2, fp=f)

def main():
    """Main function - outputs JSON for Claude Code to process"""

    log_message("=" * 60)
    log_message("Client Google Docs Setup")
    log_message("=" * 60)

    registry = load_registry()
    clients_to_process = []

    for client in CLIENTS:
        context_file = CLIENTS_DIR / client / "CONTEXT.md"

        if not context_file.exists():
            log_message(f"⚠️  {client}: No CONTEXT.md found")
            continue

        # Check if doc already exists
        if client in registry and registry[client].get("doc_id"):
            log_message(f"✓ {client}: Already has Google Doc ({registry[client]['doc_id']})")
            continue

        # Read content size
        with open(context_file, 'r') as f:
            content = f.read()

        clients_to_process.append({
            "client": client,
            "context_file": str(context_file),
            "content_length": len(content),
            "display_name": client.replace("-", " ").title()
        })

        log_message(f"📝 {client}: Ready to create Google Doc ({len(content)} chars)")

    # Output JSON for Claude Code to process
    result = {
        "status": "ready",
        "total_clients": len(CLIENTS),
        "existing_docs": len([c for c in CLIENTS if c in registry]),
        "needs_creation": len(clients_to_process),
        "clients_to_process": clients_to_process,
        "registry_file": str(DOC_REGISTRY),
        "message": f"Ready to create {len(clients_to_process)} Google Docs"
    }

    print("\n" + "=" * 60)
    print("JSON OUTPUT:")
    print("=" * 60)
    print(json.dumps(result, indent=2))

    log_message("=" * 60)
    log_message(f"Summary: {result['needs_creation']} docs to create, {result['existing_docs']} already exist")
    log_message("=" * 60)

    return True

if __name__ == "__main__":
    main()
