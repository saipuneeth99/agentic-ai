"""User authentication and credential management"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import hashlib
import hmac
import secrets

from src.config import logger


class UserManager:
    """Manage user accounts and credentials"""

    def __init__(self, data_dir: str = ".users"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.current_user: Optional[str] = None
        self.session_file = self.data_dir / ".session"
        self._load_session()

    def _get_user_file(self, username: str) -> Path:
        """Get user data file path"""
        # Sanitize username
        safe_username = "".join(c for c in username if c.isalnum() or c in "-_")
        return self.data_dir / f"{safe_username}.json"

    def _hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password with salt"""
        if not salt:
            salt = secrets.token_hex(16)
        
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return hashed.hex(), salt

    def _save_session(self) -> None:
        """Save current session"""
        if self.current_user:
            with open(self.session_file, 'w') as f:
                json.dump({"current_user": self.current_user}, f)
        elif self.session_file.exists():
            self.session_file.unlink()

    def _load_session(self) -> None:
        """Load previous session"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.current_user = data.get("current_user")
                    if self.current_user and not self._user_exists(self.current_user):
                        self.current_user = None
            except Exception as e:
                logger.error(f"Failed to load session: {e}")
                self.current_user = None

    def _user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return self._get_user_file(username).exists()

    def register(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        """Register a new user account"""
        
        # Validate
        if not username or len(username) < 3:
            return {"success": False, "error": "Username must be at least 3 characters"}
        
        if not password or len(password) < 6:
            return {"success": False, "error": "Password must be at least 6 characters"}
        
        if self._user_exists(username):
            return {"success": False, "error": "Username already exists"}
        
        # Hash password
        hashed_password, salt = self._hash_password(password)
        
        # Create user record
        user_data = {
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "password_salt": salt,
            "created_at": datetime.now().isoformat(),
            "credits": {
                "total_allocated": 1000,  # Initial credits for new users
                "total_used": 0,
                "available": 1000,
                "plan": "starter",  # starter, pro, enterprise
                "plan_updated_at": datetime.now().isoformat(),
            },
            "settings": {
                "default_model": "gemini-pro",
                "logging_enabled": True,
                "auto_login": False,
            }
        }
        
        # Save user
        user_file = self._get_user_file(username)
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        logger.info(f"User registered: {username}")
        return {"success": True, "message": f"User '{username}' registered successfully"}

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user"""
        
        if not self._user_exists(username):
            return {"success": False, "error": "User not found"}
        
        # Load user
        user_file = self._get_user_file(username)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        # Verify password
        hashed_password, _ = self._hash_password(password, user_data["password_salt"])
        if hashed_password != user_data["password_hash"]:
            return {"success": False, "error": "Invalid password"}
        
        # Set current user
        self.current_user = username
        self._save_session()
        
        logger.info(f"User logged in: {username}")
        return {
            "success": True,
            "message": f"Logged in as {username}",
            "user": username
        }

    def logout(self) -> Dict[str, Any]:
        """Logout current user"""
        if not self.current_user:
            return {"success": False, "error": "No user logged in"}
        
        user = self.current_user
        self.current_user = None
        self._save_session()
        
        logger.info(f"User logged out: {user}")
        return {"success": True, "message": f"Logged out {user}"}

    def add_api_key(self, provider: str, api_key: str) -> Dict[str, Any]:
        """Deprecated: API keys no longer required. System uses backend credits."""
        return {"success": False, "error": "API keys not required. Use credit-based system instead."}

    def get_api_key(self, provider: str) -> Optional[str]:
        """Deprecated: API keys no longer required."""
        return None

    def list_api_keys(self) -> Dict[str, Any]:
        """Deprecated: Use get_credits() instead."""
        return {}

    def get_credits(self) -> Dict[str, Any]:
        """Get current user's credit balance and usage"""
        if not self.current_user:
            return {"success": False, "error": "Not logged in"}
        
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        credits = user_data.get("credits", {})
        return {
            "success": True,
            "user": self.current_user,
            "credits": {
                "available": credits.get("available", 0),
                "total_allocated": credits.get("total_allocated", 0),
                "total_used": credits.get("total_used", 0),
                "plan": credits.get("plan", "starter"),
                "usage_percentage": (credits.get("total_used", 0) / credits.get("total_allocated", 1)) * 100
            }
        }

    def deduct_credits(self, amount: float, operation: str = "api_call") -> Dict[str, Any]:
        """Deduct credits from current user account"""
        if not self.current_user:
            return {"success": False, "error": "Not logged in"}
        
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        credits = user_data.get("credits", {})
        available = credits.get("available", 0)
        
        if available < amount:
            return {
                "success": False,
                "error": f"Insufficient credits. Required: {amount}, Available: {available}"
            }
        
        # Deduct credits
        credits["available"] -= amount
        credits["total_used"] += amount
        user_data["credits"] = credits
        
        # Save
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        logger.info(f"Credits deducted from {self.current_user}: {amount} ({operation})")
        return {
            "success": True,
            "message": f"Deducted {amount} credits for {operation}",
            "remaining_credits": credits["available"]
        }

    def add_credits(self, amount: float, reason: str = "purchase") -> Dict[str, Any]:
        """Add credits to current user account (admin/purchase)"""
        if not self.current_user:
            return {"success": False, "error": "Not logged in"}
        
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        credits = user_data.get("credits", {})
        credits["available"] += amount
        credits["total_allocated"] += amount
        user_data["credits"] = credits
        
        # Save
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        logger.info(f"Credits added to {self.current_user}: {amount} ({reason})")
        return {
            "success": True,
            "message": f"Added {amount} credits ({reason})",
            "total_credits": credits["available"]
        }

    def get_current_user(self) -> Optional[str]:
        """Get currently logged in user"""
        return self.current_user

    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """Get current user profile"""
        
        if not self.current_user:
            return None
        
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        credits = user_data.get("credits", {})
        
        return {
            "username": user_data["username"],
            "email": user_data.get("email", ""),
            "created_at": user_data["created_at"],
            "credits": {
                "available": credits.get("available", 0),
                "total_allocated": credits.get("total_allocated", 0),
                "total_used": credits.get("total_used", 0),
                "plan": credits.get("plan", "starter"),
            },
            "settings": user_data["settings"],
        }

    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update user settings"""
        
        if not self.current_user:
            return {"success": False, "error": "Not logged in"}
        
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        # Update settings
        user_data["settings"].update(settings)
        
        # Save
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        logger.info(f"Settings updated: {self.current_user}")
        return {"success": True, "message": "Settings updated"}

    def delete_account(self, password: str) -> Dict[str, Any]:
        """Delete user account (requires password confirmation)"""
        
        if not self.current_user:
            return {"success": False, "error": "Not logged in"}
        
        # Verify password
        user_file = self._get_user_file(self.current_user)
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        hashed_password, _ = self._hash_password(password, user_data["password_salt"])
        if hashed_password != user_data["password_hash"]:
            return {"success": False, "error": "Invalid password"}
        
        # Delete account
        username = self.current_user
        user_file.unlink()
        self.current_user = None
        self._save_session()
        
        logger.info(f"Account deleted: {username}")
        return {"success": True, "message": f"Account '{username}' deleted"}
