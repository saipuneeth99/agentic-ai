# 🚀 Deploy to Hugging Face Spaces - NOW

Your Agentic AI is ready to deploy! Follow these steps:

## 🎯 Quick Deploy (5 minutes)

### Step 1: Create HF Space
1. **Go to:** https://huggingface.co/spaces/create
2. **Fill in:**
   - Name: `agentic-ai` (or your preferred name)
   - License: `MIT`
   - SDK: `Docker`
   - Visibility: `Public`
3. **Click:** "Create Space"

### Step 2: Get Your HF Token
1. **Go to:** https://huggingface.co/settings/tokens
2. **Click:** "New token"
3. **Select:** `write` permission
4. **Copy:** Your token (you'll need it in next step)

### Step 3: Run Automated Deploy
Open terminal in this project and run:

```bash
./deploy-hf.sh
```

Then enter:
- Your HF username
- Your space name (e.g., `agentic-ai`)
- Your HF token (from Step 2)

**That's it!** The script will:
- Clone your HF Space
- Pull code from GitHub
- Push to your Space
- Show you the URL

### Step 4: Add API Keys
1. **Go to:** `https://huggingface.co/spaces/[YOUR-USERNAME]/agentic-ai/settings`
2. **Find:** "Repository secrets"
3. **Add these secrets:**

```
GOOGLE_API_KEY = <your-key>
OPENAI_API_KEY = <your-key>
ANTHROPIC_API_KEY = <your-key>
```

**Get API Keys:**
- **Google:** https://aistudio.google.com/app/apikey
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/

### Step 5: Done! ✅
- Wait 2-5 minutes for build
- Visit your Space URL
- Your Agentic AI is live! 🎉

---

## 📊 What You Get

✨ **Features Included:**
- 👤 User Authentication (register/login)
- 🔑 API Keys Management
- 🚀 One-Click Project Generation
- 📁 File Browser with Download
- ⭐ Project Favorites
- 📋 Project Templates (6 pre-built)
- 📊 Project Analytics Dashboard
- 🔍 Search & Filter
- 📋 Project Duplication
- 🗑️ Bulk Actions
- 🎨 Professional UI

---

## 🛠️ Advanced Options

### Option A: Manual Deploy
If you prefer manual steps, see `DEPLOYMENT.md`

### Option B: Use Different SDK
By default, the deployment uses Docker. You can also use Streamlit SDK:
1. In HF Space settings, change SDK to "Streamlit"
2. Delete the `Dockerfile`
3. Create `app.py` (already exists)
4. Push to Space

### Option C: Custom Domain
Add a custom domain in Space settings

---

## 🐛 Troubleshooting

### "Clone failed - Permission denied"
- Check your HF token is correct
- Ensure token has `write` permission
- Token should start with `hf_`

### "Build failed"
- Check Space logs: Settings → Logs
- Common issues:
  - `requirements.txt` has syntax error
  - `Dockerfile` is invalid
  - API key typo (don't worry, build will work)

### "App crashes - 'streamlit' not found"
- Ensure `requirements.txt` has `streamlit>=1.28.0`
- Trigger rebuild from Space settings

### "API Keys not working"
- Go to Space Settings → Repository secrets
- Check exact key names (case-sensitive):
  - `GOOGLE_API_KEY` (not `google_api_key`)
  - `OPENAI_API_KEY` (not `openai_api_key`)
  - `ANTHROPIC_API_KEY` (not `anthropic_api_key`)
- Wait 30 seconds after adding secrets before testing

### "'Project' folder is empty"
- This is normal! Users create projects in the UI
- Projects are stored in `/tmp` (temporary per session)
- Add persistent storage in Space settings for permanent storage

---

## 📱 Testing Your Deployment

Once live, test these flows:
1. ✅ Register new account
2. ✅ Login
3. ✅ Go to API Keys page
4. ✅ Add your API key
5. ✅ Go to Dashboard
6. ✅ Click Quick Generate
7. ✅ Enter project name & requirements
8. ✅ Click "Generate Project"
9. ✅ Download the ZIP file
10. ✅ Unzip and explore the generated project!

---

## 📈 Monitor Your Space

- **View logs:** Space Settings → Logs
- **Check metrics:** Space Settings → Overview
- **Monitor usage:** Space Settings → Persistence & Storage
- **See errors:** Real-time in Logs tab

---

## 🔐 Security Notes

✅ API keys are stored securely in Repository Secrets
✅ Users can't see other users' projects
✅ HTTPS is automatic on HF Spaces
✅ XSRF protection enabled
✅ CORS configured properly

---

## 💪 Next Steps (Optional)

### Upgrade Space (More Resources)
1. Go to Space Settings
2. Upgrade to GPU (for faster generation)
3. Add persistent storage (for permanent projects)

### Custom Domain
1. Space Settings → Custom Domain
2. Add your domain

### Collaboration
1. Go to Space Settings
2. Add collaborators

### Monitor Analytics
Use Space metrics to track:
- Active users
- Build time
- Resource usage

---

## 🆘 Need Help?

📖 **Full Documentation:** See `DEPLOYMENT.md`
🐛 **Report Issues:** https://github.com/saipuneeth99/agentic-ai/issues
💬 **HF Spaces Help:** https://huggingface.co/spaces

---

## 🎉 You're Ready!

Everything is set up and ready to deploy. Just run:

```bash
./deploy-hf.sh
```

Your Agentic AI will be live in the cloud in minutes! 🚀

---

**Questions?** Check `DEPLOYMENT.md` for detailed info.
