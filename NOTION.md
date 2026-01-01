# Notion Publishing Setup

This system can push every generated output into a dedicated Notion database.
Use the steps below to wire it up once and leave it on.

## 1) Create a Notion integration
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it (e.g., "Content Publisher") and save
4. Copy the integration token

## 2) Share a parent page with the integration
1. Open the Notion page where the database should live
2. Click "Share"
3. Invite your new integration to the page

## 3) Add env vars
Add these to your `.env`:
```
NOTION_API_KEY=your_notion_integration_token
NOTION_PARENT_PAGE_ID=your_parent_page_id_or_url
```

## 4) Create the database
Run:
```
python scripts/notion_setup.py --parent "your_parent_page_url"
```
This prints a database ID. Add it to `.env`:
```
NOTION_DATABASE_ID=your_database_id
```

## 5) Optional defaults and notifications
```
NOTION_AUTO_PUBLISH=1
NOTION_DEFAULT_STATUS=Draft
NOTION_DEFAULT_PLATFORM=Twitter/X
NOTION_NOTIFY_EMAIL=you@example.com
```

For Notion-native notifications, click "Follow" on the database page.

## 6) Publish manually (if needed)
```
python scripts/notion_publisher.py \
  --title "SGLT2 in HFpEF" \
  --content "Your markdown content here" \
  --platform "Twitter/X" \
  --status Draft \
  --output-type Thread \
  --source twitter-content
```

## 7) Publish from pipelines
Twitter pipeline (direct mode):
```
python pipelines/twitter-content/generate.py "Your question" --notion
```

Journal fetch digest:
```
python pipelines/journal-fetch/main.py --markdown --notion
```

## 8) Auto-sync everything
With `NOTION_AUTO_PUBLISH=1`, the system will push outputs automatically from:
- `pipelines/twitter-content` (threads/tweets)
- `pipelines/journal-fetch` (daily digest)
- `research-engine` outputs
- `rag-pipeline` queries
 - `research-engine/data/scraped` (raw research JSON)

You can also sync manually:
```
python scripts/notion_sync.py --path output
python scripts/notion_sync.py --path research-engine/output
python scripts/notion_sync.py --path research-engine/content-calendar
```

To limit large files, set:
```
NOTION_MAX_FILE_KB=500
```
