#!/bin/bash

# Since the video was just processed manually, let's clear the state first
rm -f /Users/administrator/Documents/PetesBrain.nosync/data/state/youtube-monitor-state.json

# Run with correct API keys
# Note: Get the key from wherever it's stored
export ANTHROPIC_API_KEY="YOUR_KEY_HERE"
export YOUTUBE_API_KEY="AIzaSyDowdeXxrfH2TLrgxfxM70_javptOVYv4U"

venv/bin/python3 youtube-monitor.py
