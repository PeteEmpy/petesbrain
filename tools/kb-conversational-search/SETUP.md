# Setup Instructions

## Quick Setup

1. **Create API Key Configuration File**:
   ```bash
   cd /Users/administrator/Documents/PetesBrain/tools/kb-conversational-search
   cp .env.example .env
   ```

2. **Add Your Anthropic API Key**:
   Edit `.env` and replace `your_api_key_here` with your actual API key:
   ```bash
   nano .env
   ```

   Or use this command (replace with your actual key):
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-your-actual-key-here" > .env
   ```

3. **Start the Server**:
   ```bash
   ./start.sh
   ```

The server will automatically read your API key from the `.env` file.

## Alternative: Use Environment Variable

If you prefer to set it in your shell:
```bash
export ANTHROPIC_API_KEY='your-key-here'
./start.sh
```

## Finding Your API Key

Your Anthropic API key is the same one used by `kb-search.py`.

To find where it's stored:
```bash
# Check if it's in your shell environment
echo $ANTHROPIC_API_KEY

# Or run kb-search.py and it will tell you if it's missing
python3 /Users/administrator/Documents/PetesBrain/tools/kb-search.py --stats
```

If kb-search.py works, your key is already configured somewhere in your environment.
