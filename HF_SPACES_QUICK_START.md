# 🚀 Deploy to Hugging Face Spaces - Quick Start

## 3-Minute Setup

### Step 1: Create a HF Space
Visit https://huggingface.co/spaces/create and create:
- **Name:** `agentic-ai`
- **License:** `MIT`
- **SDK:** `Docker`
- **Visibility:** `Public`

### Step 2: Clone & Setup
```bash
# Clone your space
git clone https://huggingface.co/spaces/[YOUR_NAME]/agentic-ai
cd agentic-ai

# Add this project's files
git remote add source https://github.com/saipuneeth99/agentic-ai.git
git pull source main

# Skip the .git folder
rm -rf .git/config.old
```

### Step 3: Add Secrets
Go to your Space settings → Repository secrets:

```
GOOGLE_API_KEY = xxxxxxxxxx
OPENAI_API_KEY = xxxxxxxxxx
ANTHROPIC_API_KEY = xxxxxxxxxx
```

**Get API Keys:**
- Google: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

### Step 4: Push
```bash
git add .
git commit -m "deploy: Agentic AI"
git push
```

### ✅ Done!
Your app is live in 2-5 minutes at:
```
https://huggingface.co/spaces/[YOUR_NAME]/agentic-ai
```

---

## What You Get

✨ **Features Included:**
- 👤 User Authentication (registration/login)
- 🔑 API Keys Management
- 🚀 One-Click Project Generation
- 📁 File Browser & Download
- ⭐ Project Favorites
- 📋 Project Templates
- 📊 Project Analytics
- 🎨 Professional UI

---

## Troubleshooting

**"Build Failed"**
- Check Docker logs in Space settings
- Ensure `pip install streamlit` works

**"API Keys Not Working"**
- Go to Repository Secrets (not environment variables)
- Exact names: `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- Wait 30 seconds after adding secrets

**"Module Not Found"**
- Check `requirements.txt` has `streamlit>=1.28.0`
- Rebuild the Space

---

## File Structure

```
.
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
├── .streamlit/
│   ├── config.toml          # Streamlit settings
│   └── secrets.toml.example # API key template
├── src/                      # Source code
│   ├── agents/              # AI agents
│   ├── framework/           # Core framework
│   ├── config/              # Configuration
│   ├── auth/                # Authentication
│   ├── cli/                 # CLI tools
│   └── utils/               # Utilities
└── DEPLOYMENT.md            # Full deployment guide
```

---

## Environment Variables

The app looks for these in order:
1. HF Spaces Repository Secrets
2. `.env` file (local only)
3. System environment

Example `.env` (local development only):
```
GOOGLE_API_KEY=your-key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

---

## Features Demo

### 1. Authentication
- Register new accounts
- Login with credentials
- Session management
- Profile page

### 2. API Keys Management
- Add/update API keys
- Status indicators (✅/⚠️)
- Links to get new keys
- Secure storage

### 3. Quick Generate
- Write requirements
- Select template
- AI generates project
- Download as ZIP

### 4. My Files
Search, filter, duplicate, favorite, analyze, and download projects

### 5. Templates
6 pre-built templates:
- E-commerce Store
- SaaS Dashboard
- Blog Platform
- Portfolio Site
- Documentation
- Community Forum

---

## Performance

- **Load Time:** <1 second
- **Project Generation:** 30-60 seconds
- **Concurrent Users:** 10+ (can scale)
- **Storage:** Temporary (2GB limit) or persistent

---

## Support

📖 Full guide: See `DEPLOYMENT.md`
🐛 Issues: https://github.com/saipuneeth99/agentic-ai/issues
💬 HF Spaces: https://huggingface.co/spaces

---

**You're all set! 🎉 Your Agentic AI is now in the cloud!**
