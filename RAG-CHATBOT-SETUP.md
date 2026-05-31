# Vaaniverse RAG Chatbot - Complete Setup Guide

**Free Stack:** Ollama + LangChain + Chroma + Flask
**Zero API Costs • Zero External Dependencies • Completely Self-Hosted**

---

## 📋 What You're Getting

✅ **RAG Chatbot Backend** - Python Flask app with LangChain + Chroma  
✅ **Smart Frontend Widget** - Matches your exact theme (Black #111)  
✅ **Form Collection** - Name, Company, Email before chat  
✅ **Lead Tracking** - Sends to Supabase + Make.com  
✅ **Completely Free** - Ollama, LangChain, Chroma all open-source  
✅ **WordPress Ready** - Single iframe embed  

---

## 🚀 Quick Start (5 mins)

### Step 1: Install Ollama (Free LLM)

Download from: https://ollama.ai

```bash
# After installation, pull the models
ollama pull mistral
ollama pull nomic-embed-text

# Ollama will run on http://localhost:11434 automatically
```

### Step 2: Install Python & Dependencies

```bash
# Install Python 3.10+
pip install -r requirements.txt
```

### Step 3: Run Backend Locally

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Flask app
python rag-chatbot-backend.py
```

Backend runs at `http://localhost:5000`

### Step 4: Test the Chatbot

Open `rag-chatbot-widget.html` in your browser, click the chat bubble.

---

## 🌐 Deploy to Railway (Free Tier)

Railway gives you $5/month free credit (enough for this chatbot).

### Step 1: Prepare Deployment

```bash
# Create .gitignore
echo "chroma_db/" > .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore

# Create runtime.txt (tells Railway to use Python)
echo "python-3.11.0" > runtime.txt
```

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Vaaniverse RAG Chatbot"
git remote add origin https://github.com/YOUR_USERNAME/vaaniverse-rag.git
git push -u origin main
```

### Step 3: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your `vaaniverse-rag` repository
4. Railway auto-detects `Procfile` and `requirements.txt`
5. Add environment variable:
   - `PORT` = `5000`
6. Deploy!

Your backend URL: `https://your-project.railway.app`

### Step 4: Update Frontend

In `rag-chatbot-widget.html`, change:

```javascript
backendUrl: 'https://your-project.railway.app'  // Replace with your Railway URL
```

---

## 📱 WordPress Integration

### Option 1: Iframe Embed (Simplest)

Add this to any WordPress page/post:

```html
<iframe 
  src="https://your-domain.com/rag-chatbot-widget.html"
  width="100%"
  height="600"
  frameborder="0"
  style="max-width: 400px; margin: 20px auto; display: block;">
</iframe>
```

Or use WordPress code block:
1. Add Custom HTML block
2. Paste the iframe code
3. Publish

### Option 2: WordPress Plugin (More Control)

Create file: `wp-content/plugins/vaaniverse-rag-chat/vaaniverse-rag.php`

```php
<?php
/**
 * Plugin Name: Vaaniverse RAG Chat
 * Version: 1.0
 */

add_action('wp_footer', 'vaaniverse_rag_chat_footer');

function vaaniverse_rag_chat_footer() {
  if (is_user_logged_in()) return;
  
  echo '<script>
    const RAG_CONFIG = {
      backendUrl: "https://your-railway-url.railway.app",
      supabaseUrl: "https://fbdfmozeqmjunmhnesbv.supabase.co",
      supabaseKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZGZtb3plcW1qdW5taG5lc2J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyNDgxMjAsImV4cCI6MjA5NDgyNDEyMH0.WTz11nlIfEDuwY5SU8IRAHaVZIbkWNbAiE9w5xSwdwM"
    };
  </script>';
  wp_enqueue_script('vaaniverse-rag-chat', plugin_dir_url(__FILE__) . 'rag-chatbot-widget.html');
}
?>
```

Then:
1. Upload folder to wp-content/plugins/
2. Activate plugin in WordPress admin
3. Chatbot appears on all pages

### Option 3: Hostinger Custom HTML Widget

If using Hostinger WordPress builder:
1. Add HTML block to any page
2. Paste widget HTML directly
3. Change `backendUrl` to your Railway URL

---

## 📊 How to Update Knowledge Base

RAG chatbot learns from `KB_CONTENT` in `rag-chatbot-backend.py`.

### To Add New Content:

1. Edit `rag-chatbot-backend.py`
2. Update `KB_CONTENT` variable with new text
3. Redeploy:

```bash
# If local: Just restart Python
# If Railway: Push to GitHub, Railway auto-redeploys
git add rag-chatbot-backend.py
git commit -m "Update knowledge base"
git push
```

**Example: Adding new pricing**

```python
KB_CONTENT = """
... existing content ...

NEW PACKAGE - Growth Starter Pro - ₹1,75,000/month
Best For: Growing SaaS companies
Includes:
- Everything in Growth Starter PLUS
- Custom AI agent
- Priority support
...
"""
```

Then redeploy. Chatbot immediately knows about it!

---

## 🔌 Integration Points

### Supabase Chat Logging

Chatbot logs all conversations to Supabase table `chat_logs`:
- `user_message` - What user asked
- `bot_response` - What bot answered
- `visitor_email` - Email from form
- `visitor_name` - Name from form
- `timestamp` - When it happened

View in Supabase dashboard: https://app.supabase.com

### Make.com Lead Webhook

When user fills form, data is sent to Make.com:
```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Corp",
  "source": "Vaaniverse RAG Chatbot",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

Webhook URL: `https://hook.eu1.make.com/yrevc45uuonvga6q2anaf4arekjvqcmp`

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Is Flask running? Check `python rag-chatbot-backend.py`
- Is Ollama running? Check `ollama serve`
- Is port 5000 open?
- For Railway: Check deployment logs

### "No response from bot"
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Check Flask logs for errors
- Try simpler question first
- Restart Ollama and Flask

### "Slow responses"
- First response takes 10-30s while model loads
- Subsequent responses faster
- This is normal with free Ollama
- To improve: Upgrade to paid Ollama hosting or Claude API

### "Knowledge base not updating"
- After editing KB_CONTENT, you MUST restart Flask
- Chroma cache may need clearing: `rm -rf chroma_db/`
- Then restart Flask

---

## 📈 What's Next

1. **Customize Styling** - Edit CSS in `rag-chatbot-widget.html`
2. **Add More Content** - Update `KB_CONTENT` with case studies, testimonials
3. **Connect CRM** - Use webhook data in Make.com to create Salesforce/HubSpot records
4. **Analytics** - View Supabase logs to see what questions users ask most
5. **Upgrade Models** - Switch from Mistral to Llama 2 for better quality

---

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| Ollama (Free LLM) | $0 |
| LangChain (Open Source) | $0 |
| Chroma (Self-Hosted Vector DB) | $0 |
| Flask (Web Server) | $0 |
| Railway Deployment | $5/month free tier |
| Supabase (First 500 requests) | $0 |
| **TOTAL** | **$0/month** |

---

## 📞 Support

- **For questions about services**: cxo@vaaniverse.com
- **For technical issues**: Check this guide first, then contact dev team
- **Deploy issues**: Railway support at https://railway.app/support

---

**Built with ❤️ for Vaaniverse | Powered by Open Source**
