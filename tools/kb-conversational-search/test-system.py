#!/usr/bin/env python3
"""
Test script to validate the conversational search system setup

Checks:
- Required files and directories exist
- Indexes are valid
- Dependencies are installed
- API connectivity
"""

import sys
from pathlib import Path
import json

SCRIPT_DIR = Path(__file__).parent
PETESBRAIN_ROOT = Path("/Users/administrator/Documents/PetesBrain")

def test_files_exist():
    """Test that required files exist"""
    print("\n📁 Checking required files...")

    checks = [
        ("Server script", SCRIPT_DIR / "server.py"),
        ("Web interface", SCRIPT_DIR / "static" / "index.html"),
        ("Requirements", SCRIPT_DIR / "requirements.txt"),
        ("Startup script", SCRIPT_DIR / "start.sh"),
        ("KB index", PETESBRAIN_ROOT / "shared" / "data" / "kb-index.json"),
        ("Client index", PETESBRAIN_ROOT / "shared" / "data" / "client-index.json"),
    ]

    all_good = True
    for name, path in checks:
        if path.exists():
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name}: {path} - NOT FOUND")
            all_good = False

    return all_good


def test_indexes():
    """Test that indexes are valid JSON and have content"""
    print("\n📊 Checking indexes...")

    kb_index_path = PETESBRAIN_ROOT / "shared" / "data" / "kb-index.json"
    client_index_path = PETESBRAIN_ROOT / "shared" / "data" / "client-index.json"

    all_good = True

    # KB Index
    try:
        with open(kb_index_path) as f:
            kb_index = json.load(f)

        file_count = len(kb_index.get('files', []))
        print(f"  ✅ KB index: {file_count} documents indexed")

        if file_count == 0:
            print(f"  ⚠️  Warning: KB index is empty")
            all_good = False

    except Exception as e:
        print(f"  ❌ KB index error: {e}")
        all_good = False

    # Client Index
    try:
        with open(client_index_path) as f:
            client_index = json.load(f)

        file_count = len(client_index.get('files', []))
        print(f"  ✅ Client index: {file_count} items indexed")

        if file_count == 0:
            print(f"  ⚠️  Warning: Client index is empty")

    except Exception as e:
        print(f"  ❌ Client index error: {e}")
        all_good = False

    return all_good


def test_dependencies():
    """Test that Python dependencies are installed"""
    print("\n📦 Checking dependencies...")

    all_good = True

    try:
        import flask
        print(f"  ✅ Flask {flask.__version__}")
    except ImportError:
        print(f"  ❌ Flask not installed")
        all_good = False

    try:
        import flask_cors
        print(f"  ✅ Flask-CORS installed")
    except ImportError:
        print(f"  ❌ Flask-CORS not installed")
        all_good = False

    try:
        import anthropic
        print(f"  ✅ Anthropic SDK {anthropic.__version__}")
    except ImportError:
        print(f"  ❌ Anthropic SDK not installed")
        all_good = False

    return all_good


def test_env():
    """Test environment configuration"""
    print("\n🔐 Checking environment...")

    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        print(f"  ✅ ANTHROPIC_API_KEY is set ({api_key[:8]}...)")
        return True
    else:
        print(f"  ⚠️  ANTHROPIC_API_KEY not set (required for AI responses)")
        print(f"     Set with: export ANTHROPIC_API_KEY='your-key-here'")
        return False


def test_directories():
    """Test that content directories exist"""
    print("\n📂 Checking content directories...")

    checks = [
        ("KB root", PETESBRAIN_ROOT / "roksys" / "knowledge-base"),
        ("Clients root", PETESBRAIN_ROOT / "clients"),
        ("Sessions dir", SCRIPT_DIR / "sessions"),
    ]

    all_good = True
    for name, path in checks:
        if path.exists():
            if path.is_dir():
                # Count items
                items = list(path.iterdir())
                print(f"  ✅ {name}: {len(items)} items")
            else:
                print(f"  ❌ {name}: exists but is not a directory")
                all_good = False
        else:
            print(f"  ⚠️  {name}: {path} - Creating...")
            path.mkdir(parents=True, exist_ok=True)

    return all_good


def main():
    """Run all tests"""
    print("=" * 60)
    print("PetesBrain Conversational Search - System Validation")
    print("=" * 60)

    results = []

    results.append(("Files", test_files_exist()))
    results.append(("Indexes", test_indexes()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Environment", test_env()))
    results.append(("Directories", test_directories()))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("✅ All checks passed! System is ready.")
        print("\nTo start the server, run:")
        print("  ./start.sh")
        print("\nOr from Python:")
        print("  python3 server.py")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
