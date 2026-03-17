#!/usr/bin/env python3
"""
OAuth Authentication Demo
Shows how users authenticate with their Google, OpenAI, and Anthropic accounts
"""

import os
import sys
from src.auth.oauth_manager import OAuthManager, OAuthConfig
from src.config import logger


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")


def check_credentials():
    """Check if OAuth credentials are configured"""
    print_header("Checking OAuth Credentials")
    
    credentials = {
        "Google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        },
        "OpenAI": {
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
        "Anthropic": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
        },
    }
    
    all_configured = True
    for provider, creds in credentials.items():
        configured = all(v for v in creds.values())
        status = "✓ Configured" if configured else "✗ Not configured"
        print(f"{provider}: {status}")
        
        if not configured and provider == "Google":
            print(f"  → Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET")
            all_configured = False
        elif not configured and provider == "OpenAI":
            print(f"  → Set OPENAI_API_KEY")
            all_configured = False
        elif not configured and provider == "Anthropic":
            print(f"  → Set ANTHROPIC_API_KEY")
            all_configured = False
    
    print()
    return all_configured


def demo_oauth_flow():
    """Demonstrate OAuth authentication flow"""
    
    print_header("OAuth Authentication Demo")
    
    # Check credentials
    if not check_credentials():
        print("📝 Setup Instructions:")
        print("-" * 70)
        print("Run: python3 OAUTH_SETUP.py")
        print("This will show detailed setup instructions for each provider.")
        print()
        print("For testing, you can use:")
        print("  1. Real Google OAuth (recommended for demo)")
        print("  2. Dummy API keys (for CI/testing)")
        return
    
    # Initialize OAuth manager
    oauth_manager = OAuthManager()
    
    # Demo user
    test_user = "demo_user_oauth"
    
    print("Demo User: demo_user_oauth")
    print()
    
    # Check connected providers
    print("Connected Providers:")
    print("-" * 70)
    connected = oauth_manager.list_connected_providers(test_user)
    for provider, is_connected in connected.items():
        status = "✓ Connected" if is_connected else "✗ Not connected"
        print(f"  {provider.capitalize()}: {status}")
    print()
    
    # Ask if user wants to connect
    response = input("Would you like to test OAuth authentication? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\n📱 OAuth Flow Demo")
        print("-" * 70)
        print("""
This would normally:
1. Open your browser
2. Redirect to Google/OpenAI/Anthropic login
3. Ask for permission to access APIs
4. Return authorization code to this app
5. Exchange code for access token
6. Store token securely
7. Use token for API calls automatically

Providers available:
  - Google (for Gemini API)
  - OpenAI (GPT-4, GPT-3.5, Codex)
  - Anthropic (Claude)
        """)
        
        provider = input("\nSelect provider to test (google/openai/anthropic): ").lower().strip()
        
        if provider in ["google", "openai", "anthropic"]:
            print(f"\n🔄 Starting {provider} OAuth flow...")
            print("(In a real app, your browser would open for login)")
            
            # Check if we can actually run OAuth
            if provider == "google":
                config = OAuthConfig.GOOGLE
                if "YOUR_" in config["client_id"]:
                    print(f"⚠️  Setup required: Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET")
                    print(f"Then run: python3 OAUTH_SETUP.py for detailed instructions")
                else:
                    print(f"✓ Google credentials configured")
                    print(f"\nAuth URL that would be opened:")
                    auth_url = oauth_manager.get_auth_url(provider, test_user)
                    print(f"{auth_url[:80]}...")
            else:
                print(f"✓ {provider} credentials configured")
                print(f"(OAuth flow would initiate here)")
        else:
            print("Invalid provider")
    
    # Show mock flow
    print("\n📋 Mock Authentication Flow (For Testing)")
    print("-" * 70)
    print("""
Normally:
  User clicks "Connect Google"
    ↓
  Browser opens: accounts.google.com/o/oauth2/v2/auth?...
    ↓
  User logs in & grants permission
    ↓
  Redirected to: http://localhost:8000/callback/google?code=auth_code
    ↓
  App exchanges code for access token
    ↓
  Token stored securely in ~/.oauth_tokens/user_google_token.json
    ↓
  Access token used automatically for all API calls
    ↓
  Token auto-refreshes when expires
    ↓
  No storing of passwords!
    """)


def demo_token_management():
    """Show how tokens are managed"""
    
    print_header("Token Management")
    
    oauth_manager = OAuthManager()
    test_user = "demo_user_oauth"
    
    print("Token Storage Location: .oauth_tokens/")
    print()
    
    print("File Structure:")
    print("""
    .oauth_tokens/
    ├── demo_user_oauth_google_token.json    (Gemini API)
    ├── demo_user_oauth_openai_token.json    (GPT-4 API)
    └── demo_user_oauth_anthropic_token.json (Claude API)
    """)
    
    print("Token Contents (encrypted):")
    print("""
    {
        "access_token": "...",           (Used for API calls)
        "refresh_token": "...",          (Auto-refresh when expired)
        "expires_in": 3599,              (Seconds until expiry)
        "token_type": "Bearer",          (Always Bearer)
        "scope": "..."                   (Granted permissions)
    }
    """)
    
    print("Security Features:")
    print("""
    ✓ Tokens encrypted at rest (in production)
    ✓ No plaintext passwords stored
    ✓ Tokens auto-refresh before expiring
    ✓ Each user has separate tokens
    ✓ Easy to revoke: user can remove token via settings
    """)


def demo_agent_usage():
    """Show how agents use OAuth tokens"""
    
    print_header("Agent Usage with OAuth")
    
    print("""
User Flow in Your App:

1. User registers:
   Registration Form → Sends to /auth/register
   
2. User connects providers:
   Click "Connect Google" → Opens OAuth
   Click "Connect OpenAI" → Opens OAuth
   Click "Connect Claude" → Opens OAuth
   
3. User runs workflows:
   Input: "Design a landing page website"
   ↓
   Your Orchestrator Agent:
   ├─ Frontend Agent: Uses GOOGLE token → Calls Gemini API
   ├─ Backend Agent:  Uses OPENAI token → Calls GPT-4 API  
   └─ Orchestrator:   Uses ANTHROPIC token → Calls Claude API
   ↓
   Receives integrated results
   ↓
   Shows to user

4. Cost tracking:
   ✓ All API calls billed to USER's accounts
   ✓ User sees charges on Google Cloud, OpenAI, Anthropic dashboards
   ✓ Your app shows usage breakdown
   ✓ No markup, no hidden costs


Your Business Model:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Charge for: Multi-agent orchestration software
            ├─ Workflow automation
            ├─ Model optimization  
            ├─ Integration features
            └─ Priority support

User pays: Their own LLM API costs directly to providers
           ├─ Gemini API (Google)
           ├─ OpenAI API (OpenAI)
           └─ Claude API (Anthropic)

You never touch user money!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


def main():
    """Run all demos"""
    
    print("\n")
    print("█" * 70)
    print("  AGENTIC AI - OAuth Authentication Demo".center(70))
    print("█" * 70)
    
    # Demo 1: Check credentials
    demo_oauth_flow()
    
    # Demo 2: Token management
    demo_token_management()
    
    # Demo 3: Agent usage
    demo_agent_usage()
    
    print_header("Demo Complete")
    print("Next Steps:")
    print("1. Run: python3 OAUTH_SETUP.py  (for setup instructions)")
    print("2. Set up OAuth credentials with Google/OpenAI/Anthropic")
    print("3. Users can then authenticate seamlessly in your app")
    print("4. Your agents automatically use their API keys")
    print()


if __name__ == "__main__":
    main()
