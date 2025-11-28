---
name: markdown-browser-display
description: Displays markdown files as formatted HTML in a browser window. Use when user says "display in browser", "show in browser", "open in browser", "render markdown", or wants to view markdown as formatted HTML.
allowed-tools: Bash, Read, Write
---

# Markdown Browser Display Skill

---

## Core Workflow

When this skill is triggered:

### 1. Identify Markdown File

The skill should identify which markdown file to display:
- If user mentions a specific file path → Use that file
- If user says "this" or "it" → Use the most recently referenced/edited markdown file
- If user has a markdown file open → Use the currently open file
- If multiple files mentioned → Ask for clarification or use the most recent

### 2. Convert Markdown to HTML

Run the conversion script:

```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/display_markdown_in_browser.py [path-to-markdown-file]
```

### 3. What the Script Does

The script:
1. **Reads the markdown file** - Loads content from specified path
2. **Converts to HTML** - Uses markdown library to convert MD → HTML
3. **Applies styling** - Adds CSS for readable formatting
4. **Saves temporary HTML** - Creates HTML file in temp directory
5. **Opens in browser** - Uses `open` command (macOS) to display in default browser
6. **Cleans up** - Optionally removes temp file after viewing

### 4. Expected Output

**Success indicators**:
- ✅ HTML file created
- ✅ Browser window opens automatically
- ✅ Markdown content displayed with formatting

**File created**:
- Temporary HTML file (auto-opened, optionally auto-deleted)

---

## Integration Notes

**Works with**:
- Any markdown file in the workspace
- Files referenced in conversation
- Currently open files
- Files from recent edits

**Outputs to**:
- Browser window (default browser)
- Temporary HTML file (for viewing)

**Dependencies**:
- `markdown` Python library (or `markdown2`)
- `webbrowser` Python module (built-in)
- macOS `open` command

---

## Quick Reference

**Command to run manually**:
```bash
cd /Users/administrator/Documents/PetesBrain && \
python3 shared/scripts/display_markdown_in_browser.py [path-to-file.md]
```

**Example usage**:
- "Display this on a browser" (when markdown file is context)
- "Show briefing/2025-11-11-briefing.md in browser"
- "Open CONTEXT.md in browser"

---

## Related Documentation

- `shared/scripts/display_markdown_in_browser.py` - Main script
- Python `markdown` library documentation
- Python `webbrowser` module documentation

---

**Status**: ✅ Production Ready  
**Owner**: Peter Empson  
**Frequency**: On-demand (manual trigger)

