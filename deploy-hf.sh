#!/bin/bash
# 🚀 Agentic AI - Hugging Face Spaces One-Command Deployment
# This script automates the deployment to HF Spaces

set -e

echo "========================================"
echo "🚀 Agentic AI - HF Spaces Deployment"
echo "========================================"
echo ""

# Check dependencies
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

check_command "git"
echo "✓ Git is installed"

# Get user input
echo ""
echo "📝 Please provide the following information:"
echo ""

read -p "Your Hugging Face username: " HF_USERNAME
read -p "Space name (e.g., agentic-ai): " SPACE_NAME
read -s -p "Your Hugging Face token (get from https://huggingface.co/settings/tokens): " HF_TOKEN
echo ""

# Validate inputs
if [ -z "$HF_USERNAME" ] || [ -z "$SPACE_NAME" ] || [ -z "$HF_TOKEN" ]; then
    echo "❌ All fields are required"
    exit 1
fi

SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
REPO_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

echo ""
echo "========================================"
echo "🔧 Setup Information"
echo "========================================"
echo "Username: $HF_USERNAME"
echo "Space: $SPACE_NAME"
echo "URL: $SPACE_URL"
echo ""

# Create temporary directory
TMP_DIR=$(mktemp -d)
echo "📂 Working in: $TMP_DIR"

cd "$TMP_DIR"

# Clone the space repo
echo ""
echo "📥 Cloning HF Space repository..."
git clone "https://$HF_USERNAME:$HF_TOKEN@huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
cd "$SPACE_NAME"

# Add GitHub repo as source
echo "📡 Adding GitHub as source..."
git remote add github https://github.com/saipuneeth99/agentic-ai.git

# Pull from GitHub
echo "📥 Pulling code from GitHub..."
git pull github main --allow-unrelated-histories

# Configure git
git config user.email "deploy@agentic.ai"
git config user.name "Agentic AI Deployer"

# Push to HF Spaces
echo "🚀 Pushing to Hugging Face Spaces..."
git push -u origin main --force

echo ""
echo "========================================"
echo "✅ Deployment Complete!"
echo "========================================"
echo ""
echo "📍 Your app is live at:"
echo "   $SPACE_URL"
echo ""
echo "⏱️  Build time: 2-5 minutes"
echo ""
echo "🔑 Next: Add API Keys"
echo "   1. Go to: $SPACE_URL/settings"
echo "   2. Scroll to 'Repository secrets'"
echo "   3. Add these secrets:"
echo "      - GOOGLE_API_KEY"
echo "      - OPENAI_API_KEY"
echo "      - ANTHROPIC_API_KEY"
echo ""
echo "💡 Get API Keys:"
echo "   • Google: https://aistudio.google.com/app/apikey"
echo "   • OpenAI: https://platform.openai.com/api-keys"
echo "   • Anthropic: https://console.anthropic.com/"
echo ""
echo "📂 Cleaning up temporary files..."
cd /
rm -rf "$TMP_DIR"

echo "✨ Done! Check your Space URL in 2-5 minutes for deployment status."
echo ""
