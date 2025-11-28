#!/usr/bin/env python3
"""
Google Ads Text Generator - Desktop Application
Desktop GUI wrapper using PyWebView for native window experience.
"""

import webview
import threading
import time
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app


class DesktopApp:
    """Desktop application wrapper for the Google Ads Text Generator."""

    def __init__(self):
        self.server_thread = None
        self.port = 5001
        self.host = '127.0.0.1'

    def start_flask(self):
        """Start Flask server in background thread."""
        # Disable debug mode and reloader for desktop app
        app.run(
            host=self.host,
            port=self.port,
            debug=False,
            use_reloader=False,
            threaded=True
        )

    def start_server_thread(self):
        """Launch Flask in a daemon thread."""
        self.server_thread = threading.Thread(
            target=self.start_flask,
            daemon=True
        )
        self.server_thread.start()

        # Wait for server to start
        time.sleep(2)
        print(f"Flask server started on http://{self.host}:{self.port}")

    def run(self):
        """Launch the desktop application."""
        print("=" * 80)
        print("GOOGLE ADS TEXT GENERATOR - DESKTOP APP")
        print("=" * 80)
        print("\nStarting application...")

        # Start Flask server
        self.start_server_thread()

        # Create desktop window
        print("Opening desktop window...")
        window = webview.create_window(
            title='Google Ads Text Generator',
            url=f'http://{self.host}:{self.port}',
            width=1200,
            height=900,
            resizable=True,
            min_size=(800, 600)
        )

        # Start the webview (blocks until window is closed)
        webview.start()

        print("\nApplication closed.")


def main():
    """Main entry point for desktop application."""
    desktop_app = DesktopApp()
    desktop_app.run()


if __name__ == '__main__':
    main()
