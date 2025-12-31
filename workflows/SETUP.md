# Medical Journal Digest - Setup Guide

## Quick Start

### 1. Import Workflow to n8n

1. Open your n8n instance (localhost:5678 or Hostinger)
2. Go to **Workflows** > **Import from File**
3. Select `workflows/medical-journal-digest.json`

### 2. Configure Credentials in n8n

You need to set up these credentials in n8n (Settings > Credentials):

#### OpenRouter API (Required for AI)
- **Type:** Header Auth
- **Name:** `OpenRouter Header Auth`
- **Header Name:** `Authorization`
- **Header Value:** `Bearer YOUR_OPENROUTER_API_KEY`

#### Gmail OAuth2 (For email delivery)
1. Create a Google Cloud project
2. Enable Gmail API
3. Create OAuth2 credentials
4. In n8n, add Gmail OAuth2 credential
5. Authorize with your Google account

#### Slack Bot (For Slack notifications)
1. Go to https://api.slack.com/apps
2. Create New App > From Scratch
3. Add Bot Token Scopes: `chat:write`, `commands`
4. Install to Workspace
5. Copy Bot User OAuth Token
6. In n8n, add Slack API credential with the token

### 3. Set Up Slack Slash Command (Optional - for on-demand trigger)

1. In your Slack App, go to **Slash Commands**
2. Create New Command:
   - Command: `/digest`
   - Request URL: `YOUR_N8N_URL/webhook/slack-digest`
   - Description: "Get latest medical journal digest"
3. Save and reinstall app to workspace

### 4. Update Configuration

Edit the `Load Configuration` node in n8n to update:
- Your email recipients
- Slack channel name
- PubMed search queries (if needed)
- RSS feed URLs (if needed)

### 5. Test the Workflow

1. In n8n, click **Test Workflow** button
2. Check that articles are fetched from PubMed and RSS
3. Verify AI summaries are generated
4. Confirm email and Slack delivery

### 6. Activate for Daily Run

1. Toggle the workflow to **Active**
2. The schedule trigger runs daily at 7:00 AM

---

## File Structure

```
fetch journal articles/
├── .env                    # API keys (update with your keys)
├── .mcp.json               # n8n-mcp config for Claude Code
├── config/
│   └── config.json         # Topics, RSS feeds, settings
├── workflows/
│   └── medical-journal-digest.json  # Main n8n workflow
└── SETUP.md                # This file
```

---

## API Keys Required

| Service | Purpose | Get It From |
|---------|---------|-------------|
| OpenRouter | AI summaries | https://openrouter.ai/keys |
| NCBI (optional) | Higher PubMed rate limits | https://www.ncbi.nlm.nih.gov/account/ |
| Gmail | Email delivery | Google Cloud Console |
| Slack | Notifications | https://api.slack.com/apps |

---

## Customization

### Add More Topics

Edit the `topics` array in the `Load Configuration` node:

```javascript
{
  id: 'oncology',
  name: 'Oncology',
  enabled: true,
  pubmedQuery: '(oncology[tiab] OR cancer[tiab])'
}
```

### Add More RSS Feeds

Add to the `rssFeeds` array:

```javascript
{
  name: 'European Heart Journal',
  url: 'https://academic.oup.com/rss/site_5375/3212.xml',
  topic: 'cardiology'
}
```

### Change AI Model

In the `AI Doctor Summary` and `AI Patient Summary` nodes, update the model:

**Free models:**
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

**Production models:**
- `openai/gpt-4o-mini` (recommended)
- `anthropic/claude-3-haiku`

**Premium models:**
- `openai/gpt-4o`
- `anthropic/claude-3.5-sonnet`

---

## Troubleshooting

### No articles fetched
- Check PubMed query syntax
- Verify RSS feed URLs are accessible
- Try increasing `daysBack` to 7 for testing

### AI summaries failing
- Verify OpenRouter API key is correct
- Check you have credits/quota
- Try a different model

### Email not sending
- Re-authorize Gmail OAuth2 credential
- Check recipient email addresses

### Slack not posting
- Verify bot is installed in workspace
- Check channel name matches exactly
- Ensure bot has `chat:write` scope

---

## Support

- n8n Docs: https://docs.n8n.io
- OpenRouter: https://openrouter.ai/docs
- PubMed API: https://www.ncbi.nlm.nih.gov/books/NBK25500/
