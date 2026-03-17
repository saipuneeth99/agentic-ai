"""
OAuth Credentials Setup Guide
Follow these steps to set up automated authentication with Google, OpenAI, and Anthropic
"""

SETUP_GUIDE = """
================================================================================
OAUTH SETUP - 3 Steps to Connect Your AI Providers
================================================================================

You need to create OAuth applications with each provider. Here's how:


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Google OAuth (for Gemini API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://console.cloud.google.com/
2. Create a new project (name it "Agentic AI")
3. Enable APIs:
   - Go to "APIs & Services" → "Library"
   - Search and enable: "Generative Language API"
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: "Web application"
   - Name: "Agentic AI"
   - Authorized redirect URIs: Add "http://localhost:8000/callback/google"
   - Create
   - Copy: Client ID and Client Secret
5. Set environment variables:
   export GOOGLE_CLIENT_ID="your-client-id-here"
   export GOOGLE_CLIENT_SECRET="your-secret-here"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: OpenAI OAuth (for GPT-4, GPT-3.5, Codex)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTE: OpenAI doesn't have official OAuth yet. Two options:

Option A: Use API Key directly (simple, traditional)
- Go to: https://platform.openai.com/account/api-keys
- Create a new API key
- Add to .env: OPENAI_API_KEY="sk-..."

Option B: Wait for OpenAI OAuth (in beta)
- Check: https://platform.openai.com/docs/guides/oauth
- Get credentials when available

For now, we'll use the API key method with encryption.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Anthropic OAuth (for Claude)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTE: Anthropic doesn't have OAuth yet. Use API Key:

1. Go to: https://console.anthropic.com/
2. Create API key
3. Set environment variable:
   export ANTHROPIC_API_KEY="sk-ant-..."


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quick Setup (All in One)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add to your .env file:

# Google OAuth
GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="your-secret-key"

# OpenAI (API Key for now)
OPENAI_API_KEY="sk-your-key-here"

# Anthropic (API Key for now)
ANTHROPIC_API_KEY="sk-ant-your-key-here"


Then users can:
1. Register on your platform
2. Click "Connect Google" → Auto-authenticate
3. Click "Connect OpenAI" → Copy/paste API key OR wait for OAuth
4. Click "Connect Claude" → Copy/paste API key OR wait for OAuth

Your system will automatically use the connected providers!


================================================================================
TESTING
================================================================================

Run the OAuth demo:
    python3 demo_oauth.py

This will:
1. Guide you through setting up credentials
2. Test the OAuth flow
3. Save tokens securely
4. Show connected providers

"""

# Print setup guide when script is run
if __name__ == "__main__":
    print(SETUP_GUIDE)
