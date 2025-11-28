# Pete's Brain

> AI-powered marketing and advertising tools built with Claude AI

Pete's Brain is a collection of intelligent tools designed to supercharge marketing and advertising workflows. Each tool leverages Anthropic's Claude AI to generate high-quality, optimized content.

## Overview

This project follows a modular architecture where each tool is self-contained and can be run independently. All tools are built with Python and offer multiple interfaces (web, desktop, CLI) for maximum flexibility.

### Current Tools

#### 🎯 [Google Ads Text Generator](tools/google-ads-generator/)

AI-powered ad copy generation for Google Ads campaigns. Creates headlines, descriptions, sitelinks, callouts, and search themes optimized for ROAS following ROK specifications.

**Features:**
- URL-based analysis and copy generation
- Multiple content sections (Benefits, Technical, Quirky, CTA, Brand)
- Strict character limit enforcement
- Tone-of-voice matching
- Export to CSV or copy to clipboard

**Interfaces:**
- 🌐 Web App - Browser-based interface
- 💻 Desktop App - Native macOS application
- ⌨️ CLI Tool - Command-line interface

**Quick Start:**
```bash
cd tools/google-ads-generator
./start.sh
# Open http://localhost:5001
```

See [full documentation](tools/google-ads-generator/README.md)

#### 📝 [Granola Meeting Importer](tools/granola-importer/)

Automatically imports meeting transcripts and AI-generated notes from Granola AI into your client folders.

**Features:**
- Background sync daemon (checks every 5 minutes)
- Two-stage client detection (title + content analysis)
- Saves both AI notes and full transcripts
- Markdown export with YAML frontmatter
- Automatic organization by client

**Quick Start:**
```bash
cd tools/granola-importer
./start.sh  # Starts background daemon
```

See [full documentation](tools/granola-importer/README.md)

---

## Automated Workflows

Pete's Brain includes several automated workflows that run in the background to keep your client data organized and actionable.

### 📧 Weekly Meeting Review
Automatically reviews all meetings from the past week and sends a comprehensive summary email with action items. Runs every Monday at 9 AM.

**What it analyzes:**
- Key decisions and strategic insights
- Client concerns and requests
- Performance discussions
- Action items (automatically added to Google Tasks)

### 📊 Google Sheets Export
Exports the ROK Experiments tracking sheet to local CSV files every 6 hours, keeping your client experiment data fresh and accessible.

### 🔄 Email Sync
Monitors Gmail for client communications and automatically saves them as markdown files in the appropriate client folders.

### 📝 Meeting Import
Continuously syncs meeting notes from Granola AI, automatically detecting which client each meeting belongs to and organizing accordingly.

---

## Integrations

Pete's Brain integrates with several Google services via MCP (Model Context Protocol) servers:

- **Google Ads** - Query campaign data, run keyword research
- **Google Analytics** - Access GA4 metrics and reports
- **Google Sheets** - Read/write spreadsheet data
- **Google Tasks** - Manage tasks and action items
- **Gmail** - Send emails and sync communications

These integrations allow Claude Code to directly access your marketing data for analysis and reporting.

---

## Project Structure

```
PetesBrain/
├── tools/              # AI-powered tools (Google Ads Generator, etc.)
├── clients/            # Client work and materials
├── roksys/             # Rok Systems business documents and operations
├── personal/           # Personal documents and materials
├── shared/             # Shared utilities and scripts
│   ├── scripts/        # Automation scripts
│   ├── mcp-servers/    # MCP server integrations
│   └── email-sync/     # Email synchronization
├── docs/               # Project documentation
├── .claude/            # Claude Code configuration
├── .mcp.json           # MCP server configuration
└── README.md           # This file
```

### Directory Overview

- **tools/** - Self-contained AI-powered tools for marketing and advertising
- **clients/** - Organized folders for each client with emails, documents, briefs, etc.
- **roksys/** - Internal Rok Systems business documents and operations
- **personal/** - Personal documents and materials
- **shared/** - Shared resources, scripts, utilities, and integrations
  - **scripts/** - Automation scripts (weekly review, meeting validation, etc.)
  - **mcp-servers/** - MCP server implementations for Google services
  - **email-sync/** - Email synchronization system
- **docs/** - Project-wide documentation

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Anthropic API key (for AI-powered tools)

### Installation

Each tool manages its own dependencies. Navigate to the tool directory and follow its README:

```bash
cd tools/[tool-name]
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Tools that use Claude AI require an API key:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Add this to your `~/.bashrc` or `~/.zshrc` for persistence.

## Available Tools

### Google Ads Text Generator
**Status**: ✅ Production Ready
**Location**: [`tools/google-ads-generator/`](tools/google-ads-generator/)
**Purpose**: Generate optimized Google Ads copy from any URL

[View Documentation →](tools/google-ads-generator/README.md)

### Granola Meeting Importer
**Status**: ✅ Production Ready
**Location**: [`tools/granola-importer/`](tools/granola-importer/)
**Purpose**: Automatically import meeting transcripts from Granola AI

[View Documentation →](tools/granola-importer/README.md)

---

*More tools coming soon!*

## Development

### Adding a New Tool

1. Create directory: `tools/[tool-name]/`
2. Add tool files and `requirements.txt`
3. Create `README.md` with usage instructions
4. Create `TOOL_CLAUDE.md` for AI assistance
5. Add documentation to `docs/[tool-name]/`
6. Update this README

### Project Guidelines

- Each tool is independent and self-contained
- Follow PEP 8 for Python code
- Add comprehensive documentation
- Never commit API keys or secrets
- Test thoroughly before committing

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## Documentation

- **Project Overview**: [CLAUDE.md](CLAUDE.md) - Architecture and guidelines
- **Tool Docs**: Each tool has its own README and documentation
- **Detailed Guides**: Check `docs/[tool-name]/` for in-depth guides

## Technology Stack

- **Language**: Python 3.6+
- **AI**: Anthropic Claude API
- **Web Framework**: Flask
- **Desktop Framework**: PyWebView
- **Packaging**: PyInstaller

## Contributing

This is a personal project, but contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Proprietary - All rights reserved

## Contact

For questions or issues, please create an issue in this repository.

---

**Pete's Brain** - Making marketing smarter, one tool at a time.
