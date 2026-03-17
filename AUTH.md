# User Authentication & API Key Management

## 🎯 Overview

Your system now supports **user accounts with personal API key management**. This enables:

- ✅ Multiple users with their own accounts
- ✅ Each user manages their own API keys  
- ✅ No backend API costs (users bring their own credits)
- ✅ Secure credential storage
- ✅ Session persistence

---

## 🚀 Getting Started (5 Minutes)

### 1. Create Account

```bash
python3 agentic auth:register
# Follow prompts:
# Username: john_dev
# Email: john@example.com
# Password: your-secure-password
```

**Output:**
```
✓ User 'john_dev' registered successfully
```

### 2. Login

```bash
python3 agentic auth:login
# Or with username directly:
python3 agentic auth:login john_dev
```

**Output:**
```
✓ Logged in as john_dev
```

### 3. Add Your API Keys

```bash
# Add Google API key
python3 agentic auth:add-key google
# Paste your API key when prompted

# Add OpenAI key
python3 agentic auth:add-key openai

# Add Anthropic key  
python3 agentic auth:add-key anthropic
```

### 4. View Your Profile

```bash
python3 agentic auth:profile
```

**Output:**
```
======================================================================
USER PROFILE - john_dev
======================================================================

Username: john_dev
Email: john@example.com
Created: 2026-03-18

API Keys:
  Google: ✓ Configured
  Openai: ✗ Not set
  Anthropic: ✗ Not set

Settings:
  default_model: gemini-pro
  logging_enabled: True
  auto_login: False

======================================================================
```

---

## 📖 Complete Command Reference

### Authentication Commands

#### `auth:register`
Create a new account

```bash
python3 agentic auth:register
```

**What it does:**
- Creates new user account
- Hashes password securely  
- Stores credentials locally in `.users/` directory
- Returns success/error message

#### `auth:login`
Login to your account

```bash
python3 agentic auth:login [username]
```

**What it does:**
- Authenticates user with password
- Creates session file (persistent login)
- Loads your API keys for current session
- Returns success/error message

#### `auth:logout`
Logout from current account

```bash
python3 agentic auth:logout
```

**What it does:**
- Clears current session
- Removes session file
- Protects your credentials

#### `auth:profile`
View your account profile

```bash
python3 agentic auth:profile
```

**What it does:**
- Shows your username, email, account creation date
- Lists configured API keys (masked for security)
- Shows your settings
- Requires login

#### `auth:add-key`
Add or update API key

```bash
python3 agentic auth:add-key [provider]
```

**Providers:**
- `google` - Google Gemini API
- `openai` - OpenAI GPT-4
- `anthropic` - Anthropic Claude

**What it does:**
- Prompts for API key (hidden input)
- Stores securely in your user file
- Activates that LLM for workflows
- Requires login

---

## 🔐 Security Features

### Password Security
- ✅ PBKDF2 hashing with salt (100,000 iterations)
- ✅ Randomly generated salt per user
- ✅ Never stored in plaintext

### API Key Security  
- ✅ Stored locally in `.users/` directory
- ✅ Not transmitted to any server
- ✅ User-controlled encryption
- ✅ Masked in profile display

### Session Management
- ✅ Session file in `.users/.session`
- ✅ Persists login state
- ✅ Auto-logout on logout command
- ✅ Cleared on account deletion

### Privacy
- ✅ No cloud storage of credentials
- ✅ No tracking of usage
- ✅ No advertisement
- ✅ Complete user control

---

## 👥 Multi-User Workflow

### Scenario: Team Development

**Developer 1 (Frontend specialist)**
```bash
# John registers
python3 agentic auth:register
# Username: john_frontend

# John adds his Google API key
python3 agentic auth:add-key google

# John uses frontend agent with his credits
python3 agentic workflow:plan "ui-project" "Design dashboard"
```

**Developer 2 (Backend specialist)**
```bash
# Jane registers (on same computer or different)
python3 agentic auth:register
# Username: jane_backend

# Jane adds her OpenAI key
python3 agentic auth:add-key openai

# Jane uses backend agent with her credits
python3 agentic auth:login jane_backend
python3 agentic workflow:plan "api-project" "Design REST API"
```

**Each uses their own API credits!** 🎯

---

## 💰 Cost Model

### Zero Platform Costs
- ✅ No subscription fee
- ✅ No platform markup
- ✅ No hidden charges

### User Pays for LLMs
- Google Gemini: Free tier + pay-as-you-go
- OpenAI: $0.03-0.15 per 1K tokens
- Anthropic: $0.003-0.024 per 1K tokens

### Cost Examples
```
Single workflow with all 3 agents:
  ≈ $0.05 - $0.20 per execution
  (depends on agents and complexity)

100 workflows per month:
  ≈ $5 - $20 per user
  (for 3 agents, low-medium complexity)
```

---

## 🔄 Account Management

### Change Settings

```python
from src.auth import UserManager

user_manager = UserManager()
user_manager.login("john_dev", "password")

# Update settings
settings = {
    "default_model": "claude-3-opus",
    "logging_enabled": True,
}
result = user_manager.update_settings(settings)
```

### Delete Account

```bash
# Login first
python3 agentic auth:login john_dev

# Then delete (requires password confirmation)
# (CLI command coming soon)

# Or via Python
user_manager.delete_account("your-password")
```

---

## 📁 File Structure

### User Data Storage
```
.users/
├── .session                 # Current session info
├── john_dev.json           # John's user file
├── jane_backend.json       # Jane's user file
└── admin.json              # Admin user
```

### User File Contents
```json
{
  "username": "john_dev",
  "email": "john@example.com",
  "password_hash": "...",
  "password_salt": "...",
  "created_at": "2026-03-18T...",
  "api_keys": {
    "google_api_key": "sk-...",
    "openai_api_key": "sk-...",
    "anthropic_api_key": "sk-..."
  },
  "settings": {
    "default_model": "gemini-pro",
    "logging_enabled": true,
    "auto_login": false
  }
}
```

### Session File
```json
{
  "current_user": "john_dev"
}
```

---

## 🔗 Integration with Workflows

### Automatic API Key Loading

When you execute a workflow as a logged-in user:

```bash
python3 agentic auth:login john_dev
python3 agentic workflow:execute ".workflows/project-*.json"
```

The system automatically:
1. Loads your API keys from `.users/john_dev.json`
2. Injects them into agents
3. Agents use your account/credits
4. No secrets in environment variables

### Workflow Example

```python
from src.auth import UserManager
from src.framework.workflow import WorkflowManager
import asyncio

async def main():
    user_manager = UserManager()
    workflow_manager = WorkflowManager()
    
    # Login
    user_manager.login("john_dev", "password")
    
    # Get your API keys
    google_key = user_manager.get_api_key("google")
    openai_key = user_manager.get_api_key("openai")
    
    # Use in workflow...
    # System automatically uses your keys
    
asyncio.run(main())
```

---

## ✅ Best Practices

### 1. Create Account First
```bash
python3 agentic auth:register
# Create personal account
```

### 2. Add API Keys Securely
```bash
python3 agentic auth:add-key google
# Don't share keys
# Don't commit to git
# API keys stay local
```

### 3. Login Before Workflows
```bash
python3 agentic auth:login
# Always login before executing workflows
python3 agentic workflow:execute "..."
```

### 4. Manage Credentials
- Review stored keys: `auth:profile`
- Rotate keys periodically
- Delete account when done: `delete-account`

### 5. Never Expose Keys
- ✅ Not in `.env` (optional, for backward compatibility)
- ✅ Only in `.users/` directory
- ✅ Never in git commits
- ✅ Never in logs or console output

---

## 🔄 Migration from .env

### Old Way (Still Supported)
```bash
# .env file (not recommended with multi-user)
GOOGLE_API_KEY=sk-...
OPENAI_API_KEY=sk-...
```

### New Way (Recommended)
```bash
# Create account and add keys
python3 agentic auth:register
python3 agentic auth:login
python3 agentic auth:add-key google
python3 agentic auth:add-key openai
```

### Priority
System checks in this order:
1. User's stored API keys (if logged in)
2. Environment variables (.env)
3. Mock agents (if no real keys)

---

## 🚀 Production Deployment

### Multi-Machine Setup

**Server 1 (Shared Repository)**
```bash
git clone <repo>
cd agentic
python3 agentic help
```

**Developer 1**
```bash
python3 agentic auth:register
python3 agentic auth:add-key google
python3 agentic workflow:execute "..."
```

**Developer 2**
```bash
python3 agentic auth:register
python3 agentic auth:add-key openai
python3 agentic workflow:execute "..."
```

Each developer's credentials stored locally in `.users/`

---

## 📊 Monitoring & Analytics

### Track Your Usage

```bash
python3 agentic auth:profile
# Shows all your configured services
```

### Per-User Usage

Each user can monitor:
- Which API keys are configured
- Account creation date
- Settings preferences

---

## ❓ FAQ

**Q: Are my API keys safe?**
A: Yes. Stored locally in `.users/`, never transmitted, never on servers.

**Q: Can I use on multiple computers?**
A: Yes. Create an account on each computer, add your own API keys.

**Q: What if I lose my password?**
A: Delete `.users/username.json` and create new account.

**Q: Can I share my account?**
A: Not recommended. Each user should create their own account.

**Q: Do you store my keys on a server?**
A: No. Everything stored locally in `.users/` directory.

**Q: What if I want to backup my account?**
A: Backup `.users/username.json` file. Include your API keys!

---

## 🎓 Next Steps

1. ✅ Create your account: `auth:register`
2. ✅ Get API keys from providers:
   - [Google Gemini](https://aistudio.google.com/app/apikeys)
   - [OpenAI](https://platform.openai.com/api-keys)
   - [Anthropic](https://console.anthropic.com/)
3. ✅ Add your keys: `auth:add-key google`
4. ✅ Start using: `workflow:execute "..."`

**You're in control of your data and costs!** 🚀

---

_Last Updated: March 18, 2026_  
_Status: Ready for Multi-User Use_
