# GitHub Codespaces Setup Guide

This guide shows how to use your Content OS from anywhere via GitHub Codespaces.

---

## 🎯 What You Get

- ✅ Access from **any device** (phone browser, tablet, desktop)
- ✅ Full VS Code + Claude Code in browser
- ✅ **Uses your Claude subscription** (not API - $0 cost)
- ✅ All your skills available
- ✅ Generate content anywhere
- ✅ Publish to Notion from mobile

---

## 📋 One-Time Setup (5 minutes)

### Step 1: Add Secrets to GitHub

Your .env variables need to be added as Codespaces secrets:

1. Go to: https://github.com/drshailesh88/integrated_content_OS/settings/secrets/codespaces
2. Click **"New repository secret"**
3. Add each secret from your local `.env` file:

**Required for Notion Publishing:**
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `NOTION_NOTIFY_EMAIL`

**Optional (for advanced features):**
- `YOUTUBE_API_KEY`
- `NCBI_API_KEY`
- `GOOGLE_API_KEY` (Gemini - free tier)
- `ASTRA_DB_API_ENDPOINT`
- `ASTRA_DB_APPLICATION_TOKEN`
- `APIFY_API_KEY`

**Note:** Only add the secrets you actually use. Start with Notion secrets for basic publishing.

---

### Step 2: Create Codespace

1. Go to: https://github.com/drshailesh88/integrated_content_OS
2. Click green **"Code"** button
3. Click **"Codespaces"** tab
4. Click **"Create codespace on main"** (or your branch)

**Wait 2-3 minutes** - Codespace will:
- Build container
- Install Python packages
- Setup PubMed MCP
- Create .env file
- Make everything ready

---

### Step 3: Test It Works

In the Codespace terminal:

```bash
# Test Notion publishing
python publish.py "Test from Codespace" "Hello World!" --platform "Twitter/X"

# If it works, you'll see:
# ✅ SUCCESS! Published to Notion
# 🔗 https://notion.so/...
```

---

## 📱 Daily Usage from Mobile

### From Phone Browser:

1. Open: https://github.com/codespaces
2. Click your codespace (or create new one)
3. VS Code opens in browser
4. Open terminal (hamburger menu → Terminal → New Terminal)
5. **Talk to Claude Code** (using your subscription!)

### Example Workflow:

```bash
# In Codespace terminal on your phone:

# Start Claude Code conversation
# (Chat interface opens)

You: "Write 5 tweets about GLP-1 cardiovascular benefits"

Claude: [generates 5 tweets using your subscription]

You: "Publish to Notion"

Claude: [runs publish.py automatically]

# Result:
# ✅ Tweets in Notion
# 📱 Check Notion mobile app
# 🚀 Copy-paste to Twitter
```

---

## 💰 Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| **GitHub Codespaces** | **$0-13/mo** | Free: 60 hrs/mo<br>Paid: $0.18/hr after |
| **Claude Code** | **$0** | Uses your subscription |
| **Content Generation** | **$0** | Via subscription, not API |
| **Notion Storage** | **$0** | Free tier unlimited |

**Typical usage:** 2-3 hours/week = **$0/month** (within free tier)

---

## 🎛️ Alternative: .env File in Codespace

If you prefer NOT using GitHub Secrets:

1. Create Codespace
2. Create `.env` file in workspace
3. Copy-paste from your local `.env`
4. Works immediately

**Pros:** Simple, no GitHub settings needed
**Cons:** Lost if codespace deleted, not synced

---

## 🔄 Syncing Your Work

**Files you create in Codespace:**
- Auto-saved to GitHub when you commit/push
- OR auto-syncs if you enable auto-commit

**Content you generate:**
- Goes to Notion → access everywhere
- OR save to files → commit → push to GitHub

---

## 📱 Mobile Experience Tips

### Good Mobile UX:
- **iPad with keyboard:** ⭐⭐⭐⭐⭐ (perfect)
- **Phone landscape mode:** ⭐⭐⭐⭐ (good)
- **Phone portrait:** ⭐⭐⭐ (usable, small screen)

### Best Practices:
1. Use landscape mode on phone
2. Increase terminal font size (Settings → Text Editor → Font Size → 16)
3. Use voice typing for long prompts
4. Keep Notion app open for quick review

---

## 🆘 Troubleshooting

### "Missing NOTION_API_KEY"
→ Add secret at: Settings → Secrets → Codespaces
→ Rebuild codespace (click ... → Rebuild Container)

### "pip install failed"
→ Run manually: `pip install -r requirements.txt`

### Codespace won't start
→ Delete and create new one (Settings are preserved in secrets)

### Need to update secrets
→ GitHub Settings → Secrets → Edit secret → Rebuild codespace

---

## 🚀 Next Steps

Once working:

1. **Bookmark codespace URL** - Quick access from phone
2. **Set up Notion database** - Mobile content library
3. **Test visual generation** - Images work in Codespaces
4. **Try Content OS** - Generate all content types

**Your workflow:**
```
Anywhere → Codespace → Claude (subscription) → Notion → Mobile app
```

**Zero API costs. Full capability. True mobility.**
