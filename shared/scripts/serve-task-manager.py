#!/usr/bin/env python3
"""
Simple HTTP server to serve Task Manager HTML files.
This allows the browser to connect to the backend task notes server (localhost:8766)
without CORS/mixed-content issues that occur with file:// origins.

Usage:
    python3 serve-task-manager.py [--port 8767]
"""

import http.server
import socketserver
import os
import sys
import argparse
import atexit
from pathlib import Path

DEFAULT_PORT = 8767
DIRECTORY = "/Users/administrator/Documents/PetesBrain.nosync"
PID_FILE = Path.home() / '.petesbrain-task-manager-server.pid'

class TaskManagerHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers for cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress most logging except errors
        if '200' not in str(args):
            super().log_message(format, *args)

def check_already_running():
    """Check if server already running via PID file"""
    if PID_FILE.exists():
        try:
            with open(PID_FILE) as f:
                old_pid = int(f.read().strip())

            # Check if process still exists
            os.kill(old_pid, 0)

            # Process exists - server already running
            print(f"ℹ️  Task Manager Server already running (PID {old_pid})")
            print(f"💡 If stuck, kill it: kill {old_pid}")
            sys.exit(0)  # Exit cleanly (not a failure)

        except (ProcessLookupError, ValueError):
            # Stale PID file - process doesn't exist
            print(f"🧹 Removing stale PID file")
            PID_FILE.unlink()
        except PermissionError:
            # Process exists but owned by another user
            print(f"❌ Server running as different user (PID {old_pid})")
            sys.exit(1)

    # Write current PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    print(f"✅ PID file created: {PID_FILE}")

def cleanup_pid_file():
    """Remove PID file on shutdown"""
    if PID_FILE.exists():
        PID_FILE.unlink()
        print(f"🧹 PID file removed")

def main():
    # Check for duplicate instance FIRST
    check_already_running()

    # Register cleanup handler
    atexit.register(cleanup_pid_file)

    parser = argparse.ArgumentParser(description='Serve Task Manager via HTTP')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                       help=f'Port to serve on (default: {DEFAULT_PORT})')
    args = parser.parse_args()

    os.chdir(DIRECTORY)

    try:
        with socketserver.TCPServer(("", args.port), TaskManagerHTTPRequestHandler) as httpd:
            print(f"🌐 Task Manager Server running on http://localhost:{args.port}/tasks-overview-priority.html")
            print(f"📁 Serving from: {DIRECTORY}")
            print("\n✅ You can now save task notes without browser security issues")
            print("\nPress Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {args.port} is already in use")
            print(f"💡 Try: lsof -ti :{args.port} | xargs kill")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
