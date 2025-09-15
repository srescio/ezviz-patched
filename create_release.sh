#!/bin/bash

# Script to create a new release for EZVIZ Patched

echo "EZVIZ Patched - Release Creator"
echo "==============================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository!"
    exit 1
fi

# Get version number
read -p "Enter version number (e.g., 1.0.0): " VERSION

if [ -z "$VERSION" ]; then
    echo "Error: Version number is required!"
    exit 1
fi

# Get release notes
echo ""
echo "Enter release notes (press Ctrl+D when done):"
RELEASE_NOTES=$(cat)

if [ -z "$RELEASE_NOTES" ]; then
    RELEASE_NOTES="Release $VERSION - EZVIZ Patched custom component"
fi

echo ""
echo "Creating release $VERSION..."

# Create and push tag
git tag -a "v$VERSION" -m "$RELEASE_NOTES"
git push origin "v$VERSION"

echo ""
echo "✅ Release $VERSION created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to 'Releases'"
echo "3. Click 'Create a new release'"
echo "4. Select tag 'v$VERSION'"
echo "5. Add release title: 'EZVIZ Patched v$VERSION'"
echo "6. Add release notes:"
echo "$RELEASE_NOTES"
echo "7. Click 'Publish release'"
echo ""
echo "🔗 Your repository: $(git remote get-url origin)"
