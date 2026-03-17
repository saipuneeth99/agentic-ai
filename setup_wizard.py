#!/usr/bin/env python3
"""
First Run Setup Wizard
Automatically guides users through connecting all AI providers
Runs on first startup, can be re-run anytime
"""

import os
import sys
import webbrowser
from pathlib import Path
from src.auth.user_manager import UserManager
from src.auth.oauth_manager import OAuthManager
from src.config import logger


class SetupWizard:
    """Interactive setup wizard for connecting AI providers"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.oauth_manager = OAuthManager()
        self.username = None
        self.is_new_user = False
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title):
        """Print formatted header"""
        self.clear_screen()
        print("\n" + "█" * 70)
        print(f"  {title}".center(70))
        print("█" * 70 + "\n")
    
    def print_section(self, title):
        """Print section separator"""
        print("\n" + "▶" * 35)
        print(f"  {title}")
        print("▶" * 35 + "\n")
    
    def step_welcome(self):
        """Welcome screen"""
        self.print_header("🎉 Welcome to Agentic AI!")
        
        print("""
Agentic AI is a multi-agent system that automatically designs and builds
complete websites by orchestrating the best AI models.

You need to connect your AI provider accounts so we can:
  ✓ Use your Google account for Gemini (UI/UX design)
  ✓ Use your OpenAI account for GPT-4 (Backend architecture)
  ✓ Use your Anthropic account for Claude (Integration & planning)

Total setup time: ~2 minutes
Your credentials are stored securely and never shared.

Let's get started!
        """)
        
        input("\nPress ENTER to continue...")
    
    def step_register_or_login(self):
        """Register new user or login existing"""
        while True:
            self.print_header("Create Account or Login")
            
            print("""
Do you have an Agentic AI account?

1. Create new account
2. Login to existing account
            """)
            
            choice = input("Select (1 or 2): ").strip()
            
            if choice == "1":
                return self.step_register()
            elif choice == "2":
                return self.step_login()
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def step_register(self):
        """Register new user account"""
        self.print_header("Create Your Account")
        
        while True:
            username = input("Choose a username (min 3 chars): ").strip()
            if len(username) < 3:
                print("❌ Username must be at least 3 characters")
                continue
            
            if self.user_manager._user_exists(username):
                print("❌ Username already taken")
                continue
            
            break
        
        email = input("Enter your email: ").strip()
        
        while True:
            password = input("Choose a password (min 6 chars): ").strip()
            if len(password) < 6:
                print("❌ Password must be at least 6 characters")
                continue
            
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("❌ Passwords don't match")
                continue
            
            break
        
        # Register
        result = self.user_manager.register(username, password, email)
        
        if result['success']:
            print(f"\n✅ {result['message']}")
            
            # Auto login
            login_result = self.user_manager.login(username, password)
            if login_result['success']:
                self.username = username
                self.is_new_user = True
                print(f"✅ Logged in as {username}")
                input("\nPress ENTER to continue...")
                return True
        else:
            print(f"\n❌ {result['error']}")
            input("\nPress ENTER to continue...")
            return False
    
    def step_login(self):
        """Login to existing account"""
        self.print_header("Login to Your Account")
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        result = self.user_manager.login(username, password)
        
        if result['success']:
            print(f"\n✅ {result['message']}")
            self.username = username
            self.is_new_user = False
            input("\nPress ENTER to continue...")
            return True
        else:
            print(f"\n❌ {result['error']}")
            input("\nPress ENTER to continue...")
            return False
    
    def step_connect_google(self):
        """Connect Google Gemini API (Manual key paste)"""
        self.print_section("Connect to Google Gemini")
        
        print("""
Step 1: We'll open your Google AI Studio page
Step 2: You'll create an API key (takes 30 seconds)
Step 3: Copy the key and paste it here
Step 4: We'll save it securely

This is the simplest and most secure method.
        """)
        
        proceed = input("Open Google AI Studio page? (y/n): ").lower().strip()
        
        if proceed == 'y':
            print("\n🔗 Opening Google AI Studio page...")
            webbrowser.open("https://aistudio.google.com/app/apikey")
            
            print("""
✓ Browser opened at: https://aistudio.google.com/app/apikey

Instructions:
1. Log in with your Google account
2. Click "Create API key"
3. Copy the key (looks like a long string)
4. Come back here and paste it
            """)
            
            api_key = input("\nPaste your Google Gemini API key: ").strip()
            
            if api_key and len(api_key) > 10:
                # Save it
                token_data = {
                    "api_key": api_key,
                    "type": "api_key",
                    "models": ["gemini-pro", "gemini-1.5-pro", "gemini-vision"]
                }
                
                self.oauth_manager.save_token("google", self.username, token_data)
                print(f"\n✅ Google Gemini API key saved successfully!")
                print(f"   Key: {api_key[:20]}...")
                input("\nPress ENTER to continue...")
                return True
            else:
                print("\n❌ Invalid API key. Please paste a valid key.")
                input("\nPress ENTER to continue...")
                return False
        
        return False
    
    def step_connect_openai(self):
        """Connect OpenAI API (Manual key paste)"""
        self.print_section("Connect to OpenAI GPT-4")
        
        print("""
Step 1: We'll open your OpenAI account page
Step 2: You'll create an API key (takes 30 seconds)
Step 3: Copy the key and paste it here
Step 4: We'll save it securely

This is the simplest and most secure method.
        """)
        
        proceed = input("Open OpenAI account page? (y/n): ").lower().strip()
        
        if proceed == 'y':
            print("\n🔗 Opening OpenAI account page...")
            webbrowser.open("https://platform.openai.com/account/api-keys")
            
            print("""
✓ Browser opened at: https://platform.openai.com/account/api-keys

Instructions:
1. Log in to your OpenAI account
2. Click "Create new secret key"
3. Copy the key (starts with sk-)
4. Come back here and paste it
            """)
            
            api_key = input("\nPaste your OpenAI API key: ").strip()
            
            if api_key.startswith("sk-"):
                # Save it
                token_data = {
                    "api_key": api_key,
                    "type": "api_key",
                    "models": ["gpt-4", "gpt-3.5-turbo", "gpt-4-vision"]
                }
                
                self.oauth_manager.save_token("openai", self.username, token_data)
                print(f"\n✅ OpenAI API key saved successfully!")
                print(f"   Key: {api_key[:20]}...")
                input("\nPress ENTER to continue...")
                return True
            else:
                print("\n❌ Invalid API key. Must start with 'sk-'")
                input("\nPress ENTER to continue...")
                return False
        
        return False
    
    def step_connect_anthropic(self):
        """Connect Anthropic API (Manual key paste)"""
        self.print_section("Connect to Anthropic Claude")
        
        print("""
Step 1: We'll open your Anthropic account page
Step 2: You'll create an API key (takes 30 seconds)
Step 3: Copy the key and paste it here
Step 4: We'll save it securely

This is the simplest and most secure method.
        """)
        
        proceed = input("Open Anthropic account page? (y/n): ").lower().strip()
        
        if proceed == 'y':
            print("\n🔗 Opening Anthropic account page...")
            webbrowser.open("https://console.anthropic.com/account/keys")
            
            print("""
✓ Browser opened at: https://console.anthropic.com/account/keys

Instructions:
1. Log in to your Anthropic account
2. Click "Create Key"
3. Copy the key (starts with sk-ant-)
4. Come back here and paste it
            """)
            
            api_key = input("\nPaste your Anthropic API key: ").strip()
            
            if api_key.startswith("sk-ant-"):
                # Save it
                token_data = {
                    "api_key": api_key,
                    "type": "api_key",
                    "model": "claude-3-opus-20240229"
                }
                
                self.oauth_manager.save_token("anthropic", self.username, token_data)
                print(f"\n✅ Anthropic API key saved successfully!")
                print(f"   Key: {api_key[:20]}...")
                input("\nPress ENTER to continue...")
                return True
            else:
                print("\n❌ Invalid API key. Must start with 'sk-ant-'")
                input("\nPress ENTER to continue...")
                return False
        
        return False
    
    def step_summary(self):
        """Show connected providers summary"""
        self.print_section("Setup Summary")
        
        connected = self.oauth_manager.list_connected_providers(self.username)
        
        print("Connected Providers:\n")
        
        for provider, is_connected in connected.items():
            symbol = "✓" if is_connected else "✗"
            status = "Connected" if is_connected else "Not connected"
            print(f"  {symbol} {provider.capitalize()}: {status}")
        
        print("""

Your Agentic AI is now ready to use!

You can:
  1. Create workflows
  2. Design websites automatically
  3. Get complete frontend + backend code
  4. Deploy to production

All API calls will use your connected accounts.
Costs are billed directly to your API providers.
        """)
        
        input("\nPress ENTER to finish setup...")
    
    def run(self):
        """Run the complete setup wizard"""
        self.step_welcome()
        
        # Register or login
        while not self.step_register_or_login():
            pass
        
        if not self.username:
            print("❌ Failed to create/login account")
            sys.exit(1)
        
        print(f"\n✅ Logged in as: {self.username}\n")
        
        # Connect providers
        self.step_connect_google()
        self.step_connect_openai()
        self.step_connect_anthropic()
        
        # Summary
        self.step_summary()
        
        print("\n✅ Setup complete! Starting Agentic AI...\n")
        
        return self.username


def check_if_first_run():
    """Check if this is the first run"""
    session_file = Path(".users/.session")
    return not session_file.exists()


def main():
    """Main entry point"""
    
    if check_if_first_run():
        print("\n🚀 Starting Agentic AI for the first time...\n")
        wizard = SetupWizard()
        username = wizard.run()
    else:
        print("\n✅ Welcome back to Agentic AI!\n")
        print("Run 'python3 setup_wizard.py' anytime to reconfigure providers.\n")


if __name__ == "__main__":
    main()
