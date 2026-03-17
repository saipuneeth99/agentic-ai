"""
OAuth 2.0 Integration for Gemini, GPT, and Claude
Allows users to authenticate securely without sharing passwords
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
import requests
from src.config import logger


class OAuthConfig:
    """OAuth configuration for each provider"""
    
    # Google OAuth (for Gemini API)
    GOOGLE = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"),
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scopes": ["https://www.googleapis.com/auth/generative-language"],
        "redirect_uri": "http://localhost:8000/callback/google",
    }
    
    # OpenAI OAuth (for GPT/Codex)
    OPENAI = {
        "client_id": os.getenv("OPENAI_CLIENT_ID", "YOUR_OPENAI_CLIENT_ID"),
        "client_secret": os.getenv("OPENAI_CLIENT_SECRET", "YOUR_OPENAI_CLIENT_SECRET"),
        "auth_url": "https://platform.openai.com/login/oauth/authorize",
        "token_url": "https://api.openai.com/oauth/token",
        "scopes": ["openid", "email", "profile"],
        "redirect_uri": "http://localhost:8000/callback/openai",
    }
    
    # Anthropic OAuth (for Claude)
    ANTHROPIC = {
        "client_id": os.getenv("ANTHROPIC_CLIENT_ID", "YOUR_ANTHROPIC_CLIENT_ID"),
        "client_secret": os.getenv("ANTHROPIC_CLIENT_SECRET", "YOUR_ANTHROPIC_CLIENT_SECRET"),
        "auth_url": "https://auth.anthropic.com/authorize",
        "token_url": "https://auth.anthropic.com/token",
        "scopes": ["claude-api"],
        "redirect_uri": "http://localhost:8000/callback/anthropic",
    }


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from providers"""
    
    oauth_code = None
    oauth_error = None
    
    def do_GET(self):
        """Handle GET request (OAuth callback)"""
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Check for authorization code
        if "code" in query_params:
            OAuthCallbackHandler.oauth_code = query_params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h1>Success!</h1><p>You can close this window and return to the app.</p>"
            )
            logger.info(f"Received OAuth authorization code")
        elif "error" in query_params:
            OAuthCallbackHandler.oauth_error = query_params["error"][0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<h1>Error</h1><p>{query_params['error'][0]}</p>".encode()
            )
            logger.error(f"OAuth error: {query_params['error'][0]}")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Invalid request</h1>")
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


class OAuthManager:
    """Manage OAuth authentication for multiple providers"""
    
    def __init__(self, data_dir: str = ".oauth_tokens"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def _get_token_file(self, provider: str, username: str) -> Path:
        """Get token storage path"""
        safe_username = "".join(c for c in username if c.isalnum() or c in "-_")
        return self.data_dir / f"{safe_username}_{provider}_token.json"
    
    def _encrypt_token(self, token: str) -> str:
        """Simple encryption (in production, use proper encryption like cryptography)"""
        # For now, just return as-is. In production, use Fernet or similar.
        return token
    
    def _decrypt_token(self, encrypted_token: str) -> str:
        """Simple decryption"""
        return encrypted_token
    
    def get_auth_url(self, provider: str, username: str) -> str:
        """Generate OAuth authorization URL"""
        if provider.lower() == "google":
            config = OAuthConfig.GOOGLE
        elif provider.lower() == "openai":
            config = OAuthConfig.OPENAI
        elif provider.lower() == "anthropic":
            config = OAuthConfig.ANTHROPIC
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        params = {
            "client_id": config["client_id"],
            "redirect_uri": config["redirect_uri"],
            "response_type": "code",
            "scope": " ".join(config["scopes"]),
            "state": username,  # Use username as state for security
        }
        
        return f"{config['auth_url']}?{urlencode(params)}"
    
    def exchange_code_for_token(self, provider: str, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        if provider.lower() == "google":
            config = OAuthConfig.GOOGLE
        elif provider.lower() == "openai":
            config = OAuthConfig.OPENAI
        elif provider.lower() == "anthropic":
            config = OAuthConfig.ANTHROPIC
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        try:
            response = requests.post(
                config["token_url"],
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": config["client_id"],
                    "client_secret": config["client_secret"],
                    "redirect_uri": config["redirect_uri"],
                },
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                logger.info(f"Successfully obtained {provider} access token")
                return token_data
            else:
                logger.error(f"Token exchange failed: {response.text}")
                return {"error": response.text}
        
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            return {"error": str(e)}
    
    def save_token(self, provider: str, username: str, token: Dict[str, Any]) -> bool:
        """Save access token securely"""
        try:
            token_file = self._get_token_file(provider, username)
            with open(token_file, 'w') as f:
                json.dump(token, f)
            logger.info(f"Saved {provider} token for {username}")
            return True
        except Exception as e:
            logger.error(f"Failed to save token: {e}")
            return False
    
    def get_token(self, provider: str, username: str) -> Optional[Dict[str, Any]]:
        """Get stored access token"""
        try:
            token_file = self._get_token_file(provider, username)
            if not token_file.exists():
                return None
            
            with open(token_file, 'r') as f:
                token = json.load(f)
            return token
        except Exception as e:
            logger.error(f"Failed to load token: {e}")
            return None
    
    def refresh_token(self, provider: str, username: str) -> Optional[Dict[str, Any]]:
        """Refresh access token using refresh token"""
        if provider.lower() == "google":
            config = OAuthConfig.GOOGLE
        elif provider.lower() == "openai":
            config = OAuthConfig.OPENAI
        elif provider.lower() == "anthropic":
            config = OAuthConfig.ANTHROPIC
        else:
            return None
        
        token = self.get_token(provider, username)
        if not token or "refresh_token" not in token:
            return None
        
        try:
            response = requests.post(
                config["token_url"],
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": token["refresh_token"],
                    "client_id": config["client_id"],
                    "client_secret": config["client_secret"],
                },
                timeout=10
            )
            
            if response.status_code == 200:
                new_token = response.json()
                self.save_token(provider, username, new_token)
                logger.info(f"Refreshed {provider} token for {username}")
                return new_token
            else:
                logger.error(f"Token refresh failed: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return None
    
    def authenticate(self, provider: str, username: str) -> Dict[str, Any]:
        """Full OAuth flow: open browser, wait for callback, exchange code"""
        logger.info(f"Starting OAuth flow for {provider}")
        
        # Generate auth URL
        auth_url = self.get_auth_url(provider, username)
        logger.info(f"Auth URL: {auth_url}")
        
        # Start callback server
        server = HTTPServer(("localhost", 8000), OAuthCallbackHandler)
        server.timeout = 1
        
        print(f"\n🔗 Opening {provider} login in your browser...")
        print(f"If browser doesn't open, visit: {auth_url}\n")
        
        # Open browser
        webbrowser.open(auth_url)
        
        # Wait for callback
        code = None
        tries = 0
        max_tries = 300  # 5 minutes timeout
        
        while tries < max_tries:
            server.handle_request()
            if OAuthCallbackHandler.oauth_code:
                code = OAuthCallbackHandler.oauth_code
                OAuthCallbackHandler.oauth_code = None
                break
            if OAuthCallbackHandler.oauth_error:
                error = OAuthCallbackHandler.oauth_error
                OAuthCallbackHandler.oauth_error = None
                server.server_close()
                return {"success": False, "error": f"Authentication failed: {error}"}
            tries += 1
        
        server.server_close()
        
        if not code:
            return {"success": False, "error": "Authorization timeout"}
        
        # Exchange code for token
        token_data = self.exchange_code_for_token(provider, code)
        if "error" in token_data:
            return {"success": False, "error": token_data["error"]}
        
        # Save token
        if self.save_token(provider, username, token_data):
            return {
                "success": True,
                "message": f"Successfully connected to {provider}",
                "provider": provider,
                "access_token": token_data.get("access_token", "")[:20] + "..."
            }
        else:
            return {"success": False, "error": "Failed to save token"}
    
    def list_connected_providers(self, username: str) -> Dict[str, bool]:
        """List which providers user has connected"""
        providers = {}
        for provider in ["google", "openai", "anthropic"]:
            token = self.get_token(provider, username)
            providers[provider] = token is not None
        return providers
