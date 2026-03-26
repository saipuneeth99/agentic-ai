#!/bin/bash
# Quick Deploy to Hugging Face Spaces
# Usage: ./hf-deploy.sh [space-name] [hf-username]

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./hf-deploy.sh [space-name] [hf-username]"
    echo "Example: ./hf-deploy.sh agentic-ai john-doe"
    exit 1
fi

SPACE_NAME=$1
HF_USERNAME=$2
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

echo "==================================="
echo "🚀 Agentic AI - HF Spaces Deploy"
echo "==================================="
echo ""
echo "Space Name: $SPACE_NAME"
echo "Username: $HF_USERNAME"
echo "Space URL: $SPACE_URL"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run this from the project root."
    exit 1
fi

# Check for required files
echo "✓ Checking files..."
required_files=("app.py" "requirements.txt" "Dockerfile" ".streamlit/config.toml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

# Add files to git
echo "✓ Staging files..."
git add app.py requirements.txt Dockerfile .streamlit/ .dockerignore

# Commit
echo "✓ Committing changes..."
git commit -m "deploy: Push Agentic AI to HF Spaces" || echo "⚠ Nothing to commit"

# Push to HF Space
echo "✓ Pushing to HF Spaces..."
git push

echo ""
echo "=================================="
echo "✅ Deploy Complete!"
echo "=================================="
echo ""
echo "📍 Your app is live at:"
echo "   $SPACE_URL"
echo ""
echo "📝 Next steps:"
echo "   1. Go to Space settings"
echo "   2. Add Repository Secrets:"
echo "      - GOOGLE_API_KEY"
echo "      - OPENAI_API_KEY"
echo "      - ANTHROPIC_API_KEY"
echo "   3. Wait for build to complete"
echo "   4. Share your Space URL!"
echo ""
echo "📖 For help, see DEPLOYMENT.md"
echo ""
