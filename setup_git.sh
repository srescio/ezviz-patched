#!/bin/bash

# Simple script to set up Git remote for EZVIZ Patched HACS component

echo "EZVIZ Patched - Git Setup"
echo "========================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository!"
    exit 1
fi

echo "This script will help you set up the remote repository for your HACS component."
echo ""

# Get the repository URL
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/ezviz-patched.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "Error: Repository URL is required!"
    exit 1
fi

echo ""
echo "Setting up remote repository..."

# Add the remote
git remote add origin "$REPO_URL"

# Push to the remote repository
echo "Pushing to remote repository..."
git push -u origin main

echo ""
echo "✅ Repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Your repository is now available at: $REPO_URL"
echo "2. Install in HACS by adding the repository URL"
echo "3. In HACS, go to 'Custom Repositories' and add: $REPO_URL"
echo "4. Then install 'EZVIZ Patched' from the HACS store"
