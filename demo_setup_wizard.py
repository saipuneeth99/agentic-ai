#!/usr/bin/env python3
"""
Setup Wizard Demo - Shows how it works (automated version)
"""

from src.auth.user_manager import UserManager
from src.auth.oauth_manager import OAuthManager
from pathlib import Path
import shutil


def print_header(title):
    """Print formatted header"""
    print("\n" + "█" * 70)
    print(f"  {title}".center(70))
    print("█" * 70 + "\n")


def print_step(step_num, title):
    """Print step"""
    print(f"\n{'▶' * 35}")
    print(f"  STEP {step_num}: {title}")
    print(f"{'▶' * 35}\n")


def demo_setup_wizard():
    """Demonstrate the setup wizard flow"""
    
    print_header("🎉 Agentic AI - First Run Setup Wizard Demo")
    
    # Clean demo data
    demo_dir = Path(".demo_setup_wizard")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    
    user_manager = UserManager(data_dir=str(demo_dir))
    oauth_manager = OAuthManager(data_dir=str(demo_dir))
    
    # ===============================================================
    print_step(1, "Welcome & Agreement")
    # ===============================================================
    
    print("""
Welcome to Agentic AI!

Agentic AI is a multi-agent system that:
  ✓ Automatically designs websites
  ✓ Generates complete frontend code
  ✓ Creates backend APIs
  ✓ Provides deployment guides

We need to connect your AI provider accounts so we can use:
  • Google Gemini (for UI/UX design)
  • OpenAI GPT-4 (for backend architecture)
  • Anthropic Claude (for integration & planning)

Total setup time: ~2 minutes
Your credentials are stored securely.
    """)
    
    input("Press ENTER to continue...")
    
    # ===============================================================
    print_step(2, "Create Account or Login")
    # ===============================================================
    
    print("""
Do you have an Agentic AI account?

1. Create new account
2. Login to existing account

(For demo, we'll create a new account)
    """)
    
    # Auto demo
    print("Demo: Creating new account...")
    
    demo_username = "alice@startup.ai"
    demo_password = "SecurePassword123"
    demo_email = "alice@startup.ai"
    
    print(f"  Username: {demo_username}")
    print(f"  Email: {demo_email}")
    print(f"  Password: {'*' * len(demo_password)}")
    
    result = user_manager.register(demo_username, demo_password, demo_email)
    print(f"\n✅ {result['message']}\n")
    
    # Auto login
    login_result = user_manager.login(demo_username, demo_password)
    print(f"✅ {login_result['message']}\n")
    
    input("Press ENTER to continue...")
    
    # ===============================================================
    print_step(3, "Connect Google Gemini")
    # ===============================================================
    
    print("""
Step 1: Your browser will open Google login
Step 2: Log in with your Google account
Step 3: Grant permission to access Gemini API
Step 4: We'll automatically save your token

In real usage:
  - App opens browser automatically
  - You log in
  - You grant permission
  - Token is saved securely
    """)
    
    print("Demo: Simulating Google OAuth...\n")
    
    # Mock Google token
    mock_google_token = {
        "access_token": "ya29.a0AfH6SMBx_abcd1234567890xyz",
        "refresh_token": "1//0gYz_abcd1234567890xyz",
        "expires_in": 3599,
        "scope": "https://www.googleapis.com/auth/generative-language",
        "token_type": "Bearer"
    }
    
    oauth_manager.save_token("google", demo_username, mock_google_token)
    
    print(f"✅ Google Gemini Connected!")
    print(f"   Token: {mock_google_token['access_token'][:40]}...")
    
    input("\nPress ENTER to continue...")
    
    # ===============================================================
    print_step(4, "Connect OpenAI GPT-4")
    # ===============================================================
    
    print("""
Step 1: We'll open your OpenAI account page
Step 2: You create an API key (30 seconds)
Step 3: You copy the key
Step 4: You paste it here
Step 5: We save it securely

Browser opens: https://platform.openai.com/account/api-keys

In real usage:
  - App opens browser automatically
  - You create a key
  - You copy/paste it back
  - Done!
    """)
    
    print("Demo: Simulating OpenAI key input...\n")
    
    # Mock OpenAI key
    mock_openai_key = {
        "api_key": "sk-proj-1234567890abcdefghijk",
        "type": "api_key",
        "models": ["gpt-4", "gpt-3.5-turbo"]
    }
    
    oauth_manager.save_token("openai", demo_username, mock_openai_key)
    
    print(f"✅ OpenAI GPT-4 Connected!")
    print(f"   Key: {mock_openai_key['api_key'][:30]}...")
    
    input("\nPress ENTER to continue...")
    
    # ===============================================================
    print_step(5, "Connect Anthropic Claude")
    # ===============================================================
    
    print("""
Step 1: We'll open your Anthropic account page
Step 2: You create an API key (30 seconds)
Step 3: You copy the key
Step 4: You paste it here
Step 5: We save it securely

Browser opens: https://console.anthropic.com/account/keys

In real usage:
  - App opens browser automatically
  - You create a key
  - You copy/paste it back
  - Done!
    """)
    
    print("Demo: Simulating Anthropic key input...\n")
    
    # Mock Anthropic key
    mock_anthropic_key = {
        "api_key": "sk-ant-1234567890abcdefghijk",
        "type": "api_key",
        "model": "claude-3-opus-20240229"
    }
    
    oauth_manager.save_token("anthropic", demo_username, mock_anthropic_key)
    
    print(f"✅ Anthropic Claude Connected!")
    print(f"   Key: {mock_anthropic_key['api_key'][:30]}...")
    
    input("\nPress ENTER to continue...")
    
    # ===============================================================
    print_step(6, "Setup Complete - Summary")
    # ===============================================================
    
    print("🎉 All providers connected!\n")
    
    connected = oauth_manager.list_connected_providers(demo_username)
    print("Connected Providers:\n")
    
    for provider, is_connected in connected.items():
        symbol = "✓" if is_connected else "✗"
        status = "Connected" if is_connected else "Not connected"
        print(f"  {symbol} {provider.capitalize()}: {status}")
    
    print(f"""

Your Account:
  Username: {demo_username}
  Email: {demo_email}
  Connected Providers: 3 ✓

You're all set! You can now:
  1. Create workflow projects
  2. Generate websites automatically
  3. Get complete code (frontend + backend)
  4. Deploy to production

What happens next:
  • When you create a project, our orchestrator will:
    - Route design tasks to Google Gemini
    - Route backend tasks to OpenAI GPT-4
    - Route integration to Anthropic Claude
  • Costs are billed directly to your provider accounts
  • No hidden fees or markups

Getting Started:
  $ python3 agentic workflow:plan --topic "Landing page for my startup"
    """)
    
    print("\n" + "="*70)
    print("Setup Complete! Ready to Use Agentic AI".center(70))
    print("="*70 + "\n")
    
    input("Press ENTER to finish...")


if __name__ == "__main__":
    demo_setup_wizard()
