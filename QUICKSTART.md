# Vaaniverse RAG Chatbot - Quick Start (5 Minutes)

## What You Have

✅ **Complete Free RAG Chatbot** (Open-source stack)
- Backend: Flask + LangChain + Ollama + Chroma
- Frontend: Theme-matched widget (Black #111 design)
- Form: Name, Company, Email collection
- Tracking: Supabase + Make.com webhook
- **Cost: $0/month**

## Files Included

```
rag-chatbot-backend.py      ← Python backend (do not edit)
rag-chatbot-widget.html     ← Chat widget (your theme)
requirements.txt            ← Python packages to install
Procfile                    ← Railway deployment config
runtime.txt                 ← Python version (Railway)
.env.example                ← Environment variables template
wordpress-integration.php   ← WordPress plugin
RAG-CHATBOT-SETUP.md       ← Full documentation
QUICKSTART.md              ← This file
```

---

## 🚀 Step 1: Install Ollama (5 mins)

Ollama provides the free AI model your chatbot uses.

**Download:** https://ollama.ai (Mac, Linux, Windows)

After installation:

```bash
# Open terminal and run:
ollama pull mistral
ollama pull nomic-embed-text

# These download automatically and stay on your computer (no cloud)
```

Ollama will run in background on `http://localhost:11434`

---

## 🚀 Step 2: Install Python Dependencies (2 mins)

```bash
# In the vaaniverse folder
pip install -r requirements.txt
```

---

## 🚀 Step 3: Run Locally (1 min)

**Terminal 1:** Start Ollama
```bash
ollama serve
```

**Terminal 2:** Start chatbot backend
```bash
python rag-chatbot-backend.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

## 🚀 Step 4: Test (1 min)

Open `rag-chatbot-widget.html` in your browser.

You should see the chat bubble in bottom right. Click it, fill form, and ask:
- "What are your service packages?"
- "Tell me about Growth Accelerator"
- "What's your team email?"

---

## 🌐 Deploy to Production (10 mins)

**Use Railway** (free, no credit card for first month)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Vaaniverse RAG Chatbot"
git remote add origin https://github.com/YOUR_USERNAME/vaaniverse-rag.git
git push -u origin main
```

### 2. Deploy on Railway

1. Go to https://railway.app
2. Sign up (free)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-deploys! 🎉

Your backend URL will be:
```
https://your-project.railway.app
```

### 3. Update Widget

In `rag-chatbot-widget.html`, find:
```javascript
backendUrl: 'http://localhost:5000'
```

Change to:
```javascript
backendUrl: 'https://your-project.railway.app'
```

---

## 📱 Add to WordPress (2 options)

### Option A: Simple (Copy-Paste)

1. Edit any WordPress page
2. Add "Custom HTML" block
3. Paste this (update URL):

```html
<iframe 
  src="https://your-domain.com/rag-chatbot-widget.html"
  style="max-width: 400px; width: 100%; height: 600px; border: none; border-radius: 12px;">
</iframe>
```

4. Publish

### Option B: Plugin (Recommended)

1. Create folder: `wp-content/plugins/vaaniverse-rag-chat/`
2. Copy `rag-chatbot-widget.html` into it
3. Copy `wordpress-integration.php` into it as `vaaniverse-rag-chat.php`
4. In WordPress Admin → Plugins → Activate "Vaaniverse RAG Chat"
5. Go to Settings → Vaaniverse Chat
6. Enter your Railway URL
7. Done! Chatbot appears on all pages

---

## 📊 Update Your Knowledge Base

The chatbot learns from `KB_CONTENT` in `rag-chatbot-backend.py`

To add new info (new package, new service, etc):

1. Edit `rag-chatbot-backend.py`
2. Find the `KB_CONTENT = """` section
3. Add your new text
4. Save and redeploy:

```bash
# If running locally: Just restart Python
# If on Railway: 
git add rag-chatbot-backend.py
git commit -m "Update knowledge"
git push
# Railway auto-redeploys in 1-2 mins
```

Chatbot immediately knows about it!

---

## 💰 Cost

| What | Cost |
|------|------|
| Ollama (AI model) | Free |
| LangChain (framework) | Free |
| Chroma (vector DB) | Free |
| Flask (web server) | Free |
| Railway deployment | $5/month free tier |
| Supabase logging | Free tier |
| **TOTAL** | **$0/month** |

---

## ✅ What's Working Now

- ✅ Chatbot running locally on `http://localhost:5000`
- ✅ Widget matches your exact theme
- ✅ Form collects Name, Company, Email
- ✅ Knows all your services, packages, pricing
- ✅ Answers only from your content (no hallucinations)
- ✅ Sends leads to Make.com webhook
- ✅ Logs conversations to Supabase
- ✅ Ready for WordPress

---

## 🐛 If Something Breaks

**"Backend connection error"**
→ Is Python running? Run `python rag-chatbot-backend.py` again

**"No response from chatbot"**
→ Is Ollama running? Run `ollama serve` in another terminal

**"Slow first response"**
→ Normal! First response takes 10-30s while model loads. Subsequent responses faster.

**"Railway deployment failed"**
→ Check Railway logs: https://railway.app → Your Project → Logs

---

## 📞 Next Steps

1. **Local testing** ✅ (You're here)
2. **Deploy to Railway** → Follow "Deploy to Production" above
3. **Add to WordPress** → Use Option A or B
4. **Update knowledge** → Add case studies, testimonials, new packages
5. **Monitor** → Check Supabase for conversation logs

---

## 📖 Full Documentation

See `RAG-CHATBOT-SETUP.md` for detailed info on:
- Advanced customization
- Hosting options
- Troubleshooting
- Analytics
- Scaling

---

**You're all set! Your chatbot is now live and learning from your own content.**

Questions? Email: cxo@vaaniverse.com
