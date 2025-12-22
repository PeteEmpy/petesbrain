#!/usr/bin/env python3
"""
Simple HTTP server to receive task notes from browser and save to fixed location.
This allows the HTML workflow to save directly to PetesBrain without browser download dialogs.

Usage:
    python3 save-task-notes.py

Then update tasks-overview.html to POST to http://localhost:8765/save-notes
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
import atexit
from datetime import datetime
from pathlib import Path

# Fixed location within PetesBrain (use .nosync directory for active data)
NOTES_FILE = "/Users/administrator/Documents/PetesBrain.nosync/data/state/manual-task-notes.json"
PID_FILE = Path.home() / '.petesbrain-save-task-notes-server.pid'

class TaskNotesHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save-notes':
            # Read the JSON data from request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Parse and validate JSON
                notes_data = json.loads(post_data.decode('utf-8'))

                # Save to fixed location
                os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
                with open(NOTES_FILE, 'w') as f:
                    json.dump(notes_data, f, indent=2)

                # Success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow from file://
                self.end_headers()

                response = {
                    'success': True,
                    'message': f'Saved {len(notes_data)} task note(s)',
                    'file': NOTES_FILE,
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

                print(f"✅ Saved {len(notes_data)} task note(s) to {NOTES_FILE}")

            except Exception as e:
                # Error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                response = {
                    'success': False,
                    'error': str(e)
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

                print(f"❌ Error: {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def check_already_running():
    """Check if server already running via PID file"""
    if PID_FILE.exists():
        try:
            with open(PID_FILE) as f:
                old_pid = int(f.read().strip())

            # Check if process still exists
            os.kill(old_pid, 0)

            # Process exists - server already running
            print(f"ℹ️  Task Notes Server already running (PID {old_pid})")
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

def run_server(port=8766):
    # Check for duplicate instance FIRST
    check_already_running()

    # Register cleanup handler
    atexit.register(cleanup_pid_file)
    server_address = ('localhost', port)
    # Allow reuse of port if previous instance hasn't fully closed
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(server_address, TaskNotesHandler)

    print(f"🚀 Task Notes Server running on http://localhost:{port}")
    print(f"📁 Saving to: {NOTES_FILE}")
    print(f"💡 Tip: Keep this running in background while using task notes workflow")
    print(f"\nPress Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")

if __name__ == '__main__':
    run_server()
