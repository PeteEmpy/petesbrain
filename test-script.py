#!/usr/bin/env python3
"""
Test script with hardcoded secrets - should be blocked by pre-commit hook
"""

# This AWS access key should be detected by gitleaks
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# This GitHub token should be detected
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

# This Slack webhook should be detected
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"

def main():
    print("This script should never be committed with these secrets!")

if __name__ == "__main__":
    main()
