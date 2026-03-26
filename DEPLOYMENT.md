# 🚀 Deploy Agentic AI to Hugging Face Spaces

This guide walks you through deploying the Agentic AI Streamlit frontend to Hugging Face Spaces.

## Prerequisites

- Hugging Face account (https://huggingface.co)
- GitHub account with this repository cloned
- API keys for:
  - Google Generative AI (Gemini)
  - OpenAI (GPT-4)
  - Anthropic (Claude)

## Step 1: Create a Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Configure:
   - **Space name:** `agentic-ai` (or your preferred name)
   - **License:** `mit`
   - **Space SDK:** `Docker` or `Streamlit`
   - **Visibility:** `Public`

## Step 2: Clone the Space Repo

```bash
# After creating the space, clone it
git clone https://huggingface.co/spaces/[YOUR_USERNAME]/agentic-ai
cd agentic-ai
```

## Step 3: Copy Project Files

Copy these files/folders from this repo to your Space repo:

```bash
# Copy the main app
cp app.py .

# Copy source code
cp -r src .

# Copy requirements
cp requirements.txt .

# Copy Streamlit config
cp -r .streamlit .

# Copy README
cp DEPLOYMENT.md README.md
```

## Step 4: Configure API Keys in HF Spaces

1. Go to your Space settings: `https://huggingface.co/spaces/[YOUR_USERNAME]/agentic-ai/settings`
2. Scroll to "Repository secrets"
3. Add these secrets:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

**How to get API keys:**
- **Google:** https://aistudio.google.com/app/apikey
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/

## Step 5: Create Dockerfile (if using Docker)

Create `Dockerfile` in your Space root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
```

## Step 6: Commit and Push

```bash
git add .
git commit -m "deploy: Add Agentic AI to HF Spaces"
git push
```

## Step 7: Monitor Deployment

1. Go to your Space: `https://huggingface.co/spaces/[YOUR_USERNAME]/agentic-ai`
2. Watch the "Logs" tab during build
3. Once built, your app will be live at the Space URL

## Step 8: Test Your Deployment

1. Open your Space URL
2. Test features:
   - Register a new account
   - Log in
   - Go to API Keys tab
   - Configure your API keys
   - Try Quick Generate
   - Create a project

## Environment Variables

The app reads environment variables from:
1. `.env` file (local development)
2. HF Spaces Repository Secrets (production)
3. `.streamlit/secrets.toml` (Streamlit session state)

The app automatically checks HF Spaces secrets first, then falls back to .env.

## Features Available

- ✅ User authentication (registration/login)
- ✅ API Keys management (Google, OpenAI, Anthropic)
- ✅ Quick Generate (one-click project generation)
- ✅ My Files (browse, search, download projects)
- ✅ Project Templates (6 pre-built templates)
- ✅ Project Favorites (star/unstar projects)
- ✅ Project Duplication (clone projects)
- ✅ Project Analytics (statistics dashboard)
- ✅ Bulk Actions (select and delete multiple)
- ✅ Professional Streamlit UI
- ✅ Mobile-responsive design

## File Storage

Projects are stored in:
- **HF Space:** `/tmp/.projects/[username]/` (temporary)
- **Persistent (optional):** Use HF Spaces persistent storage

For persistent storage, create `.gitignore`:
```
.projects/
.users/
.workflows/
.favorites/
.env
```

Then enable in Space settings: "Persistent storage"

## Troubleshooting

### "API Key not found"
- Check Repository Secrets in Space settings
- Ensure secret names match exactly: `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

### "Module not found"
- Check `requirements.txt` is in root
- Ensure all dependencies are listed

### "Permission denied"
- Make sure Space is public or you have access
- Check GitHub token has correct permissions

### "Build fails"
- Check Logs tab in Space
- Ensure `app.py` has no syntax errors
- Verify `requirements.txt` syntax

## Performance Tips

1. **Use persistent storage** for `.projects/` directory
2. **Cache projects** in memory when possible
3. **Limit upload size** to 200MB (configured in .streamlit/config.toml)
4. **Enable gzip compression** in HF Spaces settings

## Security Recommendations

1. ✅ Never commit API keys to GitHub
2. ✅ Use HF Spaces secrets for sensitive data
3. ✅ Enable XSRF protection (already configured)
4. ✅ Disable CORS for specific origins
5. ✅ Use HTTPS only (automatic on HF Spaces)
6. ✅ Implement rate limiting for API calls

## Custom Domain

To use a custom domain:
1. Go to Space settings
2. Add custom domain
3. Update DNS records

## Monitoring & Logs

Monitor your Space:
1. **Real-time logs:** HF Spaces dashboard
2. **Performance:** Check server load
3. **Errors:** Monitor Python errors in logs
4. **Users:** Track active sessions

## Scaling Tips

- HF Spaces has auto-scaling
- Use persistent storage for large projects
- Consider upgrading to GPU if needed
- Monitor resource usage in settings

## Rollback Deployment

To revert to a previous version:

```bash
git log --oneline
git revert [commit-hash]
git push
```

## Questions & Support

- GitHub Issues: https://github.com/saipuneeth99/agentic-ai/issues
- HF Spaces Forum: https://huggingface.co/spaces
- Documentation: See README.md

---

**Enjoy your Agentic AI deployment on Hugging Face Spaces! 🚀**
