# Mobile Workflow Setup Guide

**Goal:** Talk to Claude Code → Content goes to Notion → Get notified

---

## Step 1: Get Notion API Key (2 minutes)

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Name it: "Claude Code Publisher"
4. Click **"Submit"**
5. Copy the **"Internal Integration Token"** (starts with `secret_`)

---

## Step 2: Create Notion Database (3 minutes)

1. Open Notion (desktop or web)
2. Create a new page called **"Content Library"**
3. Type `/database` and select **"Table - Inline"**
4. Add these columns (properties):
   - **Title** (already exists)
   - **Platform** (Select)
   - **Status** (Select: Draft, Final, Published)
   - **Tags** (Multi-select)
   - **Output Type** (Select)
   - **Source Pipeline** (Select)
   - **Date** (Date)
   - **Word Count** (Number)

5. Click **"..."** (top right) → **"Add connections"**
6. Select your **"Claude Code Publisher"** integration
7. Copy the database ID from URL:
   - URL looks like: `https://notion.so/yourworkspace/DATABASE_ID?v=...`
   - Copy the 32-character ID (between workspace name and `?v=`)

---

## Step 3: Configure .env File (1 minute)

Open `.env` file and add:

```bash
# Notion Integration
NOTION_API_KEY=secret_your_key_here
NOTION_DATABASE_ID=your_database_id_here
NOTION_NOTIFY_EMAIL=your_email@gmail.com
NOTION_DEFAULT_STATUS=Draft
NOTION_DEFAULT_PLATFORM=Multi-Platform
```

**IMPORTANT:** `.env` is in `.gitignore` - it will NEVER go to GitHub. This is secure and local to your machine.

---

## Step 4: Test the Workflow (30 seconds)

Run this from Claude Code:

```bash
python publish.py "Test from Claude Code" "This is my first mobile-ready content!" \
  --platform "Twitter/X" \
  --tags "cardiology,test" \
  --type "tweet"
```

You should see:
- ✅ Success message with Notion URL
- 📱 Content in your Notion mobile app
- 📧 Email notification (if configured)

---

## Daily Usage

### From Claude Code - Just tell me:

**"Publish this to Notion: [title]"** and paste your content

I'll automatically run:
```bash
python publish.py "Your Title" "Your content" --platform "Twitter/X"
```

### From Notion Mobile App:

1. Open Notion app on your phone
2. Go to "Content Library" database
3. See all your content
4. Edit, change status, publish

---

## Example Workflows

### YouTube Script
```
You: "Write a YouTube script about statins for Indians"
Claude: [writes script]
You: "Publish this to Notion"
Claude: [runs publish.py]
Result: Script in Notion, accessible on mobile
```

### Twitter Thread
```
You: "Content OS: GLP-1 cardiovascular effects - just tweets"
Claude: [generates 5 tweets]
You: "Publish to Notion"
Claude: [publishes]
Result: Tweets in Notion database, ready to copy-paste on mobile
```

### Newsletter
```
You: "Write newsletter about CAC scoring"
Claude: [writes newsletter]
You: "Publish to Notion"
Claude: [publishes]
Result: Newsletter in Notion, review on mobile, publish when ready
```

---

## Troubleshooting

### Error: "Missing NOTION_API_KEY"
- Check `.env` file has `NOTION_API_KEY=secret_...`
- Make sure no spaces around `=`

### Error: "Missing NOTION_DATABASE_ID"
- Copy the 32-character ID from your Notion database URL
- Remove any dashes when copying

### No email notifications
- Add `GMAIL_USER` and `GMAIL_APP_PASSWORD` to `.env`
- Use App-Specific Password (not regular Gmail password)
- Get it from: https://myaccount.google.com/apppasswords

---

## Next Steps

Once this works, you can:
- Use Content OS to generate all content types → auto-publish to Notion
- Access everything from Notion mobile app
- Schedule posts from your phone
- Track what's Draft vs Published

**Simple workflow: Claude Code (create) → Notion (store + access) → Mobile (publish)**
