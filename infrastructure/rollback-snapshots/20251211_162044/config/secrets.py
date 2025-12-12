#!/usr/bin/env python3
"""
Keychain-based secrets management for PetesBrain agents.

This module provides secure credential access via macOS Keychain instead of
plaintext environment variables or plist files.

Usage:
    from shared.secrets import get_secret

    api_key = get_secret('ANTHROPIC_API_KEY')
    if api_key is None:
        raise ValueError("ANTHROPIC_API_KEY not found in Keychain")

    client = Anthropic(api_key=api_key)
"""

import os
import subprocess
from typing import Optional


def get_secret(key_name: str, fallback_env_var: Optional[str] = None) -> Optional[str]:
    """
    Retrieve a secret from macOS Keychain.

    Args:
        key_name: The name of the secret in Keychain (e.g., 'ANTHROPIC_API_KEY')
        fallback_env_var: Optional environment variable name to fall back to if Keychain lookup fails.
                         Useful during transition period before all agents are migrated.
                         If None, only returns Keychain value.

    Returns:
        The secret value from Keychain, or fallback environment variable, or None if not found.

    Examples:
        # Get API key, fall back to environment variable
        api_key = get_secret('ANTHROPIC_API_KEY', fallback_env_var='ANTHROPIC_API_KEY')

        # Get Gmail password from Keychain only (no fallback)
        gmail_password = get_secret('GMAIL_APP_PASSWORD')

        # Get email address with fallback
        email = get_secret('GMAIL_USER', fallback_env_var='GMAIL_USER')
    """

    try:
        # Try to get from Keychain using security command
        result = subprocess.run(
            ['security', 'find-generic-password', '-w', '-a', 'petesbrain', '-s', key_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout:
            # Successfully retrieved from Keychain
            return result.stdout.strip()

    except subprocess.TimeoutExpired:
        # Keychain lookup timed out
        pass
    except Exception as e:
        # Other errors (e.g., security command not found)
        print(f"Warning: Error accessing Keychain for '{key_name}': {e}")

    # If Keychain lookup failed, try fallback environment variable
    if fallback_env_var:
        env_value = os.getenv(fallback_env_var)
        if env_value:
            return env_value

    # No secret found
    return None


def set_secret(key_name: str, value: str, account_name: str = 'petesbrain') -> bool:
    """
    Store a secret in macOS Keychain.

    Args:
        key_name: The name of the secret (e.g., 'ANTHROPIC_API_KEY')
        value: The secret value to store
        account_name: The Keychain account name (default: 'petesbrain')

    Returns:
        True if successfully stored, False otherwise

    Example:
        success = set_secret('ANTHROPIC_API_KEY', 'sk-ant-...')
        if not success:
            print("Failed to store secret in Keychain")
    """

    try:
        # Check if entry already exists
        result = subprocess.run(
            ['security', 'find-generic-password', '-a', account_name, '-s', key_name],
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0:
            # Entry exists, update it
            subprocess.run(
                ['security', 'delete-generic-password', '-a', account_name, '-s', key_name],
                capture_output=True,
                timeout=5
            )

        # Add new entry
        result = subprocess.run(
            ['security', 'add-generic-password', '-a', account_name, '-s', key_name, '-w', value],
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.returncode == 0

    except Exception as e:
        print(f"Error storing secret '{key_name}' in Keychain: {e}")
        return False


def list_secrets(account_name: str = 'petesbrain') -> list:
    """
    List all secrets stored for the petesbrain account in Keychain.

    Args:
        account_name: The Keychain account name (default: 'petesbrain')

    Returns:
        List of secret names (service names) stored for this account

    Example:
        secrets = list_secrets()
        for secret_name in secrets:
            print(f"Found secret: {secret_name}")
    """

    try:
        result = subprocess.run(
            ['security', 'dump-keychain', '-d'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            secrets = []
            for line in result.stdout.split('\n'):
                if f'"{account_name}"' in line and 'desc=' in line:
                    # Extract service name from line
                    # Format: desc="..."
                    if 'desc=' in line:
                        parts = line.split('desc=')
                        if len(parts) > 1:
                            service = parts[1].strip().strip('"')
                            if service and service not in secrets:
                                secrets.append(service)
            return secrets

    except Exception as e:
        print(f"Error listing secrets from Keychain: {e}")

    return []


def delete_secret(key_name: str, account_name: str = 'petesbrain') -> bool:
    """
    Delete a secret from macOS Keychain.

    Args:
        key_name: The name of the secret to delete
        account_name: The Keychain account name (default: 'petesbrain')

    Returns:
        True if successfully deleted, False otherwise

    Example:
        success = delete_secret('OLD_API_KEY')
        if success:
            print("Secret deleted from Keychain")
    """

    try:
        result = subprocess.run(
            ['security', 'delete-generic-password', '-a', account_name, '-s', key_name],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0

    except Exception as e:
        print(f"Error deleting secret '{key_name}' from Keychain: {e}")
        return False


if __name__ == '__main__':
    # Test script - verify Keychain access
    print("PetesBrain Keychain Secrets Manager - Test")
    print("=" * 60)

    # Test reading a secret
    test_key = 'ANTHROPIC_API_KEY'
    print(f"\nTesting: get_secret('{test_key}')")
    value = get_secret(test_key)
    if value:
        print(f"✓ Found in Keychain: {value[:20]}...")
    else:
        print(f"✗ Not found in Keychain or environment")

    # List all stored secrets
    print(f"\nStored secrets in Keychain for 'petesbrain' account:")
    secrets = list_secrets()
    if secrets:
        for i, secret in enumerate(secrets, 1):
            print(f"  {i}. {secret}")
    else:
        print("  (none found)")

    print("\n" + "=" * 60)
