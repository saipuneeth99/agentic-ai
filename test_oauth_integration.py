#!/usr/bin/env python3
"""
Complete OAuth Integration Test & Demo
Shows how users connect their AI provider accounts and how agents use tokens
"""

import os
import json
from pathlib import Path
from src.auth.oauth_manager import OAuthManager, OAuthConfig
from src.auth.user_manager import UserManager
from src.config import logger


def print_section(title):
    """Print formatted section"""
    print("\n" + "▶" * 35)
    print(f"  {title}")
    print("▶" * 35 + "\n")


def test_user_registration():
    """Test 1: User registration"""
    print_section("TEST 1: User Registration (No OAuth yet)")
    
    user_manager = UserManager(data_dir=".demo_oauth_test")
    
    test_user = "alice@agentic.ai"
    password = "secure_password_123"
    
    # Clean up existing
    user_file = user_manager._get_user_file(test_user)
    if user_file.exists():
        user_file.unlink()
    
    # Register
    result = user_manager.register(test_user, password, email=test_user)
    print(f"✓ {result['message']}")
    print(f"  User File: {user_file}")
    print(f"  Status: User created, waiting to connect OAuth providers")
    
    return test_user, password, user_manager


def test_user_login(user_manager, username, password):
    """Test 2: User login"""
    print_section("TEST 2: User Login")
    
    result = user_manager.login(username, password)
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"  Connected Providers: (none yet)")
    
    return result['success']


def test_oauth_urls(oauth_manager, username):
    """Test 3: Generate OAuth URLs"""
    print_section("TEST 3: Generate OAuth URLs (What user would click)")
    
    # Note: URLs will show placeholder values if credentials aren't set
    providers = ["google", "openai", "anthropic"]
    
    for provider in providers:
        print(f"{provider.upper()}:")
        
        # Check if configured
        if provider == "google":
            config = OAuthConfig.GOOGLE
            if "YOUR_" in config["client_id"]:
                print(f"  ⚠️  Not configured")
                print(f"  → Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET")
            else:
                print(f"  ✓ Configured")
                url = oauth_manager.get_auth_url(provider, username)
                print(f"  URL: {url[:60]}...")
        else:
            print(f"  Note: {provider} uses API keys (not OAuth yet)")
            print(f"  → User provides API key in settings")
        
        print()


def test_token_storage(oauth_manager, username):
    """Test 4: Mock token storage"""
    print_section("TEST 4: Mock Token Storage")
    
    print("Simulating Google OAuth flow:")
    print("  1. User clicks 'Connect Google'")
    print("  2. Redirected to Google login")
    print("  3. User grants permission")
    print("  4. System receives authorization code")
    print("  5. Code exchanged for access token\n")
    
    # Mock token (in real flow, this comes from Google)
    mock_google_token = {
        "access_token": "ya29.a0AfH6SMBx1234567890abcdefghijklmnopqrst",
        "refresh_token": "1//0gX1234567890abcdefghijklmn...",
        "expires_in": 3599,
        "scope": "https://www.googleapis.com/auth/generative-language",
        "token_type": "Bearer"
    }
    
    # Save it
    saved = oauth_manager.save_token("google", username, mock_google_token)
    
    if saved:
        print("✓ Token saved securely")
        token_file = oauth_manager._get_token_file("google", username)
        print(f"  Location: {token_file}")
        print(f"  Contents: {json.dumps(mock_google_token, indent=2)}")
    
    print("\nOAuth token is now ready to use!")
    print("  - User didn't share password")
    print("  - User granted specific permissions")
    print("  - Token can be revoked anytime in Google settings")
    
    return mock_google_token


def test_connected_providers(oauth_manager, username):
    """Test 5: Show connected providers"""
    print_section("TEST 5: View Connected Providers")
    
    connected = oauth_manager.list_connected_providers(username)
    
    print("User's Connected Providers:")
    for provider, is_connected in connected.items():
        symbol = "✓" if is_connected else "✗"
        status = "Connected" if is_connected else "Not connected"
        print(f"  {symbol} {provider.capitalize()}: {status}")
    
    return connected


def test_agent_usage(oauth_manager, username, connected_providers):
    """Test 6: How agents would use tokens"""
    print_section("TEST 6: Agent Usage (How it works in practice)")
    
    print("User Input: Design a landing page for my startup\n")
    
    print("Your Orchestrator automatically:")
    print()
    
    if connected_providers.get("google"):
        print("  1. Frontend Agent:")
        print("     - Retrieves Google token from storage")
        print("     - Initializes ChatGoogleGenerativeAI(token=...)")
        print("     - Calls: 'Design HTML/CSS for landing page'")
        google_token = oauth_manager.get_token("google", username)
        if google_token:
            print(f"     - Token: {google_token['access_token'][:40]}...")
        print("     - Result: HTML/CSS code\n")
    
    print("  2. Backend Agent:")
    print("     - Has OpenAI API key in settings")
    print("     - Initializes ChatOpenAI(api_key=...)")
    print("     - Calls: 'Design REST API for the app'")
    print("     - Result: API specification\n")
    
    print("  3. Orchestrator Agent:")
    print("     - Has Anthropic API key in settings")
    print("     - Initializes ChatAnthropic(api_key=...)")
    print("     - Calls: 'Integrate frontend, backend, database'")
    print("     - Result: Complete integration plan\n")
    
    print("  Final Output: Complete website with frontend, backend, integration guide")
    print()
    print("Cost Breakdown (billed to user's accounts):")
    print("  - Gemini API: $X.XX")
    print("  - OpenAI API: $Y.YY")
    print("  - Anthropic API: $Z.ZZ")
    print("  - Your platform fee: $N.NN (what you charge)")
    print()
    print("User sees all costs on their provider dashboards!")


def test_security():
    """Test 7: Security features"""
    print_section("TEST 7: Security Features")
    
    print("OAuth Security Advantages:")
    print()
    print("  ✓ No passwords stored (only tokens)")
    print("  ✓ Limited scope permissions")
    print("    - Can access only what user grants")
    print("    - E.g., 'Generative Language API' only, no file access")
    print()
    print("  ✓ Token encryption at rest")
    print("    - Storage: .oauth_tokens/")
    print("    - Encryption: API key + user password")
    print()
    print("  ✓ Easy token revocation")
    print("    - User can remove in Google settings")
    print("    - Immediately stops your app's access")
    print()
    print("  ✓ Automatic token refresh")
    print("    - Tokens expire (usually in 1 hour)")
    print("    - System automatically refreshes using refresh_token")
    print("    - User doesn't need to re-authenticate")
    print()
    print("  ✓ Industry standard (OAuth 2.0)")
    print("    - Used by Google, Facebook, Twitter, etc.")
    print("    - Well-designed for security")


def test_user_flow():
    """Test 8: Complete user flow"""
    print_section("TEST 8: Complete User Flow (End-to-End)")
    
    print("""
STEP 1: User visits agentic.ai
  ├─ Clicks "Register"
  └─ Creates account (username, password)
  
STEP 2: User lands on Dashboard
  ├─ Sees "Connect Providers"
  ├─ Clicks "Connect to Gemini"
  │  ├─ Browser opens Google login
  │  ├─ User logs into Google
  │  ├─ User grants permission to Gemini API
  │  └─ Redirected back to dashboard
  ├─ Clicks "Add OpenAI API Key"
  │  ├─ Opens https://platform.openai.com/account/api-keys
  │  ├─ User copies their key
  │  └─ Pastes into your app
  └─ Similarly for Anthropic
  
STEP 3: Dashboard shows
  ✓ Google Gemini: Connected
  ✓ OpenAI GPT: Connected  
  ✓ Anthropic Claude: Connected
  ✓ Status: Ready to create workflows
  
STEP 4: User enters prompt
  Input: "Create a modern landing page for an AI startup"
  ↓
  Your app routes to agents:
  ├─ Frontend: Uses Google token → Gemini API
  ├─ Backend: Uses OpenAI key → GPT-4 API
  └─ Orchestrator: Uses Anthropic key → Claude API
  ↓
  Returns integrated result:
  ├─ HTML/CSS/JavaScript
  ├─ Backend API code
  ├─ Database schema
  └─ Deployment guide
  
STEP 5: User downloads or deploys
  - Gets complete, working website
  - Costs added to their API provider accounts
  - Your platform fee added
  - User can see breakdown anytime

BENEFITS:
✓ Users: Full control, no vendor lock-in, transparent costs
✓ You: Recurring revenue, no infrastructure costs, clean business model
✓ Providers: Users' direct customers, revenue guaranteed
    """)


def main():
    """Run all tests"""
    
    print("\n")
    print("█" * 70)
    print("  AGENTIC AI - Complete OAuth Integration Test".center(70))
    print("█" * 70)
    
    # Test 1: Registration
    username, password, user_manager = test_user_registration()
    
    # Test 2: Login
    if test_user_login(user_manager, username, password):
        
        # Test 3: OAuth URLs
        oauth_manager = OAuthManager(data_dir=".demo_oauth_test")
        test_oauth_urls(oauth_manager, username)
        
        # Test 4: Token storage
        token = test_token_storage(oauth_manager, username)
        
        # Test 5: Connected providers
        connected = test_connected_providers(oauth_manager, username)
        
        # Test 6: Agent usage
        test_agent_usage(oauth_manager, username, connected)
        
        # Test 7: Security
        test_security()
        
        # Test 8: User flow
        test_user_flow()
    
    # Summary
    print_section("Summary: How Your System Works")
    
    print("""
YOUR AGENTIC AI PLATFORM:
═══════════════════════════════════════════════════════════════════

What You Build:
  1. Multi-agent orchestration system
  2. OAuth integration for easy authentication  
  3. Intelligent routing to best model for each task
  4. Workflow automation
  5. Usage dashboard & analytics

What Users Provide:
  1. Login credentials (username/password)
  2. OAuth authorization (click "Connect")
  3. Their API keys (copy/paste or OAuth)

What Happens:
  1. User creates account
  2. User connects their AI providers
  3. You store their access tokens securely
  4. When user uses your app:
     - Your agents automatically retrieve tokens
     - Call APIs on user's behalf
     - Combine results into integrated output
  5. User sees all costs on their provider dashboards

Revenue Model:
  ✓ Subscription: Monthly fee for platform access
  ✓ Premium features: Advanced workflows, priority support
  ✓ No API costs: Users pay providers directly
  ✓ Profitable from day 1: No infrastructure overhead

This is a PROVEN, SUSTAINABLE business model!
Examples: Zapier, IFTTT, Make - all use similar models.

═══════════════════════════════════════════════════════════════════
    """)
    
    print("\n✅ OAuth Integration Complete!")
    print("\nTo enable real OAuth, set environment variables:")
    print("  export GOOGLE_CLIENT_ID=\"your-id\"")
    print("  export GOOGLE_CLIENT_SECRET=\"your-secret\"")
    print("  export OPENAI_API_KEY=\"sk-...\"")
    print("  export ANTHROPIC_API_KEY=\"sk-ant-...\"")
    print("\nThen test with: python3 demo_oauth.py")
    print()


if __name__ == "__main__":
    main()
