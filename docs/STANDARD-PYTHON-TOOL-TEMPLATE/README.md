# Tool Name

Brief description of what this tool does.

## Setup

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Add your API key**:
   Edit `.env` and add your Anthropic API key:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Install dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the tool**:
   ```bash
   python3 tool-name.py
   ```

## Usage

[Add usage instructions here]

## Configuration

All configuration is stored in the `.env` file. See `.env.example` for available options.

## Troubleshooting

**Error: "ANTHROPIC_API_KEY not set"**
- Make sure you created the `.env` file: `cp .env.example .env`
- Add your API key to the `.env` file
- The `.env` file must be in the same directory as the script

**Other issues**
[Add common issues and solutions]
