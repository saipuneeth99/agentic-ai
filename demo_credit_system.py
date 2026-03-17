#!/usr/bin/env python3
"""
Demo: Credit-Based SaaS System (No API Keys Required)

Shows how users:
1. Register with just username/password
2. Receive initial credits
3. Run AI tasks that deduct credits
4. Monitor their usage
"""

import json
from pathlib import Path
from src.auth.user_manager import UserManager
from src.config.backend_api import BackendAPIClient
from src.config import logger


def demo_credit_system():
    """Demonstrate the credit-based SaaS system"""
    
    print("\n" + "="*70)
    print("AGENTIC AI - CREDIT-BASED SAAS DEMO")
    print("(No API Keys Required - Uses Your Account Credits)")
    print("="*70)
    
    # Initialize
    user_manager = UserManager(data_dir=".demo_users")
    api_client = BackendAPIClient(user_manager)
    
    # Test user
    test_user = "demo_user"
    test_email = "demo@agentic.ai"
    test_password = "demo123456"
    
    # Step 1: Register
    print("\n[STEP 1] Register New User")
    print("-" * 70)
    
    # Clean up any existing test user
    user_file = user_manager._get_user_file(test_user)
    if user_file.exists():
        user_file.unlink()
    
    reg_result = user_manager.register(test_user, test_password, test_email)
    print(f"✓ {reg_result['message']}")
    print(f"  Initial Credits: 1,000")
    
    # Step 2: Login
    print("\n[STEP 2] User Login")
    print("-" * 70)
    
    login_result = user_manager.login(test_user, test_password)
    if login_result['success']:
        print(f"✓ {login_result['message']}")
    
    # Step 3: Check initial credits
    print("\n[STEP 3] Check Credit Balance")
    print("-" * 70)
    
    credits = user_manager.get_credits()
    if credits['success']:
        cred_info = credits['credits']
        print(f"✓ User: {test_user}")
        print(f"  Available Credits: {cred_info['available']:.1f}")
        print(f"  Plan: {cred_info['plan']}")
        print(f"  Usage: {cred_info['usage_percentage']:.1f}%")
    
    # Step 4: Make API calls (with credit deduction)
    print("\n[STEP 4] Make LLM API Calls (With Auto Credit Deduction)")
    print("-" * 70)
    
    # Call 1: Small query
    print("\n  Task 1: Frontend Design Query")
    result1 = api_client.call_llm(
        model="gemini",
        prompt="Design a landing page for an AI startup",
        system_prompt="You are a UI/UX designer"
    )
    
    if result1['success']:
        print(f"  ✓ Success")
        print(f"  Model: {result1['model']}")
        print(f"  Credits Used: {result1['credits_used']:.1f}")
        print(f"  Response: {result1['response'][:150]}...")
    
    # Call 2: Medium query
    print("\n  Task 2: Backend API Design Query")
    result2 = api_client.call_llm(
        model="gpt-3.5",
        prompt="Design a REST API for user authentication and authorization",
        system_prompt="You are a backend architect"
    )
    
    if result2['success']:
        print(f"  ✓ Success")
        print(f"  Model: {result2['model']}")
        print(f"  Credits Used: {result2['credits_used']:.1f}")
        print(f"  Response: {result2['response'][:150]}...")
    
    # Call 3: Large query
    print("\n  Task 3: Complex Integration Query")
    result3 = api_client.call_llm(
        model="claude",
        prompt="Create a comprehensive integration plan for frontend, backend, and database components including error handling, authentication, and deployment strategy",
        system_prompt="You are a system architect"
    )
    
    if result3['success']:
        print(f"  ✓ Success")
        print(f"  Model: {result3['model']}")
        print(f"  Credits Used: {result3['credits_used']:.1f}")
        print(f"  Response: {result3['response'][:150]}...")
    
    # Step 5: Check final credits and usage
    print("\n[STEP 5] View Final Credit Status & Usage Analytics")
    print("-" * 70)
    
    final_credits = user_manager.get_credits()
    if final_credits['success']:
        cred_info = final_credits['credits']
        print(f"✓ User: {test_user}")
        print(f"  Total Allocated: {cred_info['total_allocated']:.1f}")
        print(f"  Credits Used: {cred_info['total_allocated'] - cred_info['available']:.1f}")
        print(f"  Credits Remaining: {cred_info['available']:.1f}")
        print(f"  Usage: {cred_info['usage_percentage']:.1f}%")
    
    usage_stats = api_client.get_usage_stats()
    print(f"\n  Plan: {usage_stats['plan']}")
    print(f"  Total API Calls Cost: {usage_stats['credits_used']:.1f} credits")
    
    # Step 6: Purchase more credits
    print("\n[STEP 6] Purchase Additional Credits")
    print("-" * 70)
    
    purchase = user_manager.add_credits(500, reason="premium_subscription")
    if purchase['success']:
        print(f"✓ {purchase['message']}")
    
    # Final status
    print("\n[FINAL STATUS]")
    print("-" * 70)
    
    final_creds = user_manager.get_credits()
    if final_creds['success']:
        cred_info = final_creds['credits']
        print(f"✓ Current Balance: {cred_info['available']:.1f} credits")
        print(f"✓ Total Allocated: {cred_info['total_allocated']:.1f} credits")
    
    # Step 7: Logout
    print("\n[STEP 7] User Logout")
    print("-" * 70)
    
    logout_result = user_manager.logout()
    print(f"✓ {logout_result['message']}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nKey Benefits of Credit-Based System:")
    print("  ✓ No API keys needed from users")
    print("  ✓ Single login per user")
    print("  ✓ Automatic credit deduction per API call")
    print("  ✓ Purchase additional credits as needed")
    print("  ✓ Track usage and costs")
    print("  ✓ Scale to multiple AI models")
    print()


if __name__ == "__main__":
    demo_credit_system()
