# Unified Twitter Content Pipeline

## One Workflow: Idea → Research → Content

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED TWITTER CONTENT PIPELINE                               │
│                    Peter Attia Rigor × Eric Topol Accuracy                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌────────┐  │
│  │ 1.TRIGGER│───►│ 2.HARVEST│───►│ 3-5.RESEARCH │───►│6-7.SYNTH │───►│8-9.WRITE│ │
│  │ Schedule │    │ Twitter  │    │   PARALLEL   │    │ Knowledge│    │ Content │ │
│  │ /Manual  │    │ Ideas    │    │              │    │   Base   │    │         │ │
│  └──────────┘    └──────────┘    └──────────────┘    └──────────┘    └────────┘  │
│                       │                │                                  │       │
│                       ▼                ▼                                  ▼       │
│                  ┌─────────┐    ┌─────────────┐                    ┌──────────┐  │
│                  │ Apify   │    │ PubMed (Q1) │                    │  SLACK   │  │
│                  │ Scraper │    │     +       │                    │  OUTPUT  │  │
│                  │         │    │ AstraDB RAG │                    │          │  │
│                  └─────────┘    └─────────────┘                    └──────────┘  │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Pipeline Stages

### Stage 1: Trigger
- **Daily at 8 AM** - Automatic idea harvesting
- **Manual webhook** - On-demand with optional direct question

### Stage 2: Idea Harvesting (Apify)
- Scrapes tweets from inspiration accounts
- Filters by engagement (likes + retweets)
- Extracts top 3 high-potential ideas

### Stage 3-5: Dual Research Pipeline (PARALLEL)
```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│     PUBMED PIPELINE         │     │     ASTRADB RAG PIPELINE    │
├─────────────────────────────┤     ├─────────────────────────────┤
│ 1. Search PubMed            │     │ 1. Generate HyDE document   │
│ 2. Filter Q1 journals only  │     │ 2. Create embedding         │
│    - NEJM, Lancet, JAMA     │     │ 3. Vector search AstraDB    │
│    - Circulation, Eur Heart │     │    - ACC Guidelines         │
│    - JACC, BMJ              │     │    - ESC Guidelines         │
│ 3. Fetch abstracts          │     │    - ADA Guidelines         │
│ 4. Extract citations        │     │    - Medical textbooks      │
└─────────────────────────────┘     └─────────────────────────────┘
                    │                           │
                    └───────────┬───────────────┘
                                ▼
                    ┌─────────────────────────────┐
                    │    MERGE RESEARCH RESULTS   │
                    └─────────────────────────────┘
```

### Stage 6-7: Knowledge Synthesis
- Claude 3.5 Sonnet synthesizes all research
- Generates structured brief with:
  - Executive summary
  - Key evidence with citations
  - Guideline perspective (ACC/ESC/ADA)
  - Nuances & controversies
  - Content angles

### Stage 8-9: Content Writing
- AI determines optimal format (tweet/thread/long post)
- Writes in Peter Attia + Eric Topol voice
- Quality review for medical safety
- Output to Slack with full draft

---

## Inspiration Accounts (DYNAMIC)

Edit the `1. Load Config` node to add/remove accounts:

```javascript
accounts: [
  { handle: 'paddygbarrett', name: 'Dr Paddy Barrett', enabled: true },
  { handle: 'DrLipid', name: 'Dr Thomas Dayspring', enabled: true },
  { handle: 'davidludwigmd', name: 'Dr David Ludwig', enabled: true },
  { handle: 'NutritionMadeS1', name: 'Dr Gil Carvalho', enabled: true },
  { handle: 'scottissacmd', name: 'Dr Scott Issac', enabled: true }
  // Add more here...
]
```

---

## Setup Instructions

### 1. Required Credentials in n8n

Create these credentials (Settings → Credentials):

| Credential Name | Type | Header | Value |
|----------------|------|--------|-------|
| `OpenRouter Header Auth` | Header Auth | `Authorization` | `Bearer YOUR_OPENROUTER_KEY` |
| `Apify API Token` | Header Auth | `Authorization` | `Bearer YOUR_APIFY_KEY` |
| `OpenAI Header Auth` | Header Auth | `Authorization` | `Bearer YOUR_OPENAI_KEY` |
| `AstraDB Token` | Header Auth | `Token` | `YOUR_ASTRA_TOKEN` |
| `Slack Bot` | Slack API | - | Your bot token |

### 2. Environment Variables

Add to n8n (Settings → Variables):

```
ASTRA_DB_API_ENDPOINT = https://YOUR-DB-ID-REGION.apps.astra.datastax.com
ASTRA_DB_KEYSPACE = default_keyspace
```

### 3. Import Workflow

1. Open n8n: http://localhost:5678
2. Workflows → Import from File
3. Select: `workflows/unified-twitter-content-pipeline.json`
4. Update credential references in nodes
5. Activate workflow

### 4. Create Slack Channel

Create: `#content-drafts`

---

## Usage

### Automatic Mode (Daily Harvesting)
Workflow runs daily at 8 AM:
1. Scrapes tweets from all enabled accounts
2. Picks top 3 high-engagement ideas
3. Researches each via PubMed + AstraDB
4. Writes content drafts
5. Posts all drafts to Slack

### Manual Mode (Direct Question)

```bash
curl -X POST http://localhost:5678/webhook/content-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "customQuestion": "What is the latest evidence on SGLT2 inhibitors in HFpEF?",
    "format": "thread"
  }'
```

### Test the Pipeline

```bash
# Test with direct question
curl -X POST http://localhost:5678/webhook/content-pipeline \
  -H "Content-Type: application/json" \
  -d '{"customQuestion": "Why do beta-blockers improve outcomes in heart failure?"}'
```

---

## AstraDB Collection Schema

Your `medical_knowledge` collection should have:

```json
{
  "_id": "unique-id",
  "content": "The text content of the chunk",
  "source_name": "ACC Guidelines 2023",
  "source_type": "guideline",
  "chapter": "Heart Failure Management",
  "section": "Pharmacotherapy",
  "$vector": [0.123, 0.456, ...]  // text-embedding-3-small
}
```

---

## Content Voice Configuration

The pipeline writes content that:

**DOES:**
- Cites specific Q1 journals (NEJM, Lancet, JAMA, Circulation)
- Includes statistics, effect sizes, NNT
- Presents nuanced takes on complex topics
- References guidelines with class/level of evidence
- Maintains scholarly but accessible tone

**AVOIDS:**
- Oversimplification
- Medical advice
- Clickbait language
- Hashtag spam (except #MedTwitter occasionally)
- Hedging excessively

---

## Output Formats

| Format | When Used | Structure |
|--------|-----------|-----------|
| **Tweet** | Simple insight, single statistic | 280 chars max |
| **Thread** | Complex topic, multiple evidence points | 5-10 numbered tweets |
| **Long Post** | Deep dive, editorial style | 2500 chars, mini-essay with citations |

The AI automatically selects the best format based on:
- Complexity of the topic
- Amount of evidence available
- Potential for engagement

---

## Troubleshooting

### Apify Not Working
- Verify API key in credentials
- Check Twitter handles (no @ symbol)
- Ensure Apify account has credits

### AstraDB Vector Search Failing
- Check endpoint URL format
- Verify token permissions
- Confirm collection name matches

### No PubMed Results
- Broaden the search query
- Check journal filter isn't too restrictive
- Verify date range

### Content Quality Issues
- Adjust temperature in writing node (default 0.7)
- Modify system prompts
- Review synthesis quality first

---

## File Structure

```
fetch journal articles/
├── config/
│   ├── config.json
│   └── twitter-content-config.json
├── workflows/
│   └── unified-twitter-content-pipeline.json  ← THE UNIFIED WORKFLOW
├── .env
└── SETUP-TWITTER-CONTENT.md
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Run full pipeline | `curl -X POST http://localhost:5678/webhook/content-pipeline` |
| Direct question | Add `{"customQuestion": "..."}` to body |
| Force format | Add `{"format": "thread"}` to body |
| Add account | Edit `1. Load Config` node |
| Change schedule | Edit `Daily 8AM` trigger node |
