# Medical Content Engine - Complete Specification

## Overview

A dual-purpose content generation system for Dr. Shailesh Singh (Interventional Cardiologist) that:
1. Fetches articles from 20+ medical/cardiology journals
2. AI-triages each article into B2C (public), B2B (doctors), or Skip
3. Generates editorial-quality content for each audience
4. Delivers via Email + Slack

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  TRIGGER: Daily 7 AM or Manual                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: DATA COLLECTION                                       │
│  ├── PubMed API (keyword search)                                │
│  └── RSS Feeds (20+ journals)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: AI TRIAGE (per article)                               │
│  ├── Read title + abstract                                      │
│  ├── Classify: B2C / B2B / SKIP                                 │
│  ├── Assign confidence score (1-10)                             │
│  └── Extract content angle/hook                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
         ┌────────┐     ┌────────┐      ┌────────┐
         │  B2C   │     │  B2B   │      │  SKIP  │
         │ Queue  │     │ Queue  │      │ (Log)  │
         └───┬────┘     └───┬────┘      └────────┘
             │               │
             ▼               ▼
┌─────────────────┐  ┌─────────────────────────────┐
│  STAGE 3A:      │  │  STAGE 3B:                  │
│  B2C CONTENT    │  │  B2B CONTENT                │
│  Peter Attia +  │  │  Mini-Editorial for         │
│  Eric Topol     │  │  Interventionalists         │
│  Style          │  │                             │
└────────┬────────┘  └─────────────┬───────────────┘
         │                         │
         └───────────┬─────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: FORMAT & DELIVER                                      │
│  ├── HTML Email (both B2C + B2B sections)                       │
│  └── Slack notifications                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Sources

### PubMed API

**Search Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```

**Parameters:**
- `db`: pubmed
- `term`: (cardiology[tiab] OR cardiovascular[tiab] OR "heart failure"[tiab] OR "coronary artery"[tiab] OR "percutaneous coronary intervention"[tiab]) AND ("last 2 days"[edat])
- `retmax`: 15
- `retmode`: json
- `usehistory`: y

**Fetch Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

**Parameters:**
- `db`: pubmed
- `WebEnv`: (from search response)
- `query_key`: (from search response)
- `retmode`: xml
- `rettype`: abstract

### RSS Feeds (20 Journals)

#### Tier 1: General Medical (High Public Interest)
| Journal | RSS Feed URL |
|---------|--------------|
| NEJM | `https://www.nejm.org/action/showFeed?jc=nejm&type=etoc&feed=rss` |
| The Lancet | `https://www.thelancet.com/rssfeed/lancet_current.xml` |
| JAMA | `https://jamanetwork.com/rss/site_3/67.xml` |
| BMJ | `https://www.bmj.com/rss/recent.xml` |

#### Tier 2: Cardiology Core
| Journal | RSS Feed URL |
|---------|--------------|
| JAMA Cardiology | `https://jamanetwork.com/rss/site_192/184.xml` |
| Circulation | `https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=circ` |
| JACC | `https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=jacc` |
| European Heart Journal | `https://academic.oup.com/eurheartj/rss` |
| Nature Reviews Cardiology | `https://www.nature.com/nrcardio.rss` |

#### Tier 3: Interventional Cardiology (B2B Focus)
| Journal | RSS Feed URL |
|---------|--------------|
| JACC Cardiovascular Interventions | `https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=jint` |
| Circulation: Cardiovascular Interventions | `https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=circinterventions` |
| EuroIntervention | `https://www.pcronline.com/eurointervention/rss` |
| Catheterization & Cardiovascular Interventions | `https://onlinelibrary.wiley.com/feed/1522726x/most-recent` |

#### Tier 4: Heart Failure & Imaging
| Journal | RSS Feed URL |
|---------|--------------|
| JACC Heart Failure | `https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=heart` |
| European Journal of Heart Failure | `https://onlinelibrary.wiley.com/feed/18790844/most-recent` |
| JACC Cardiovascular Imaging | `https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=imaging` |

#### Tier 5: Prevention & Research
| Journal | RSS Feed URL |
|---------|--------------|
| European Journal of Preventive Cardiology | `https://academic.oup.com/eurjpc/rss` |
| Hypertension | `https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=hyp` |
| Circulation Research | `https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=res` |
| JAHA | `https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=jaha` |

---

## AI Prompts

### Triage Prompt (Classification)

```
SYSTEM:
You are a medical content strategist for Dr. Shailesh Singh, an interventional cardiologist building a personal brand.

Analyze articles and classify them. Respond ONLY with valid JSON, no markdown.

CLASSIFICATION CRITERIA:

**B2C (Public-Facing Content)**
- Lifestyle factors (diet, exercise, sleep, stress)
- Prevention strategies the public can act on
- Major trial results that change clinical practice
- Misconceptions being debunked
- Risk factor insights (cholesterol, BP, diabetes)
- New treatments patients might ask about
- Heart failure management patients can understand

**B2B (Doctor-Facing Content)**
- PCI techniques, stent comparisons, access site trials
- Interventional outcomes data
- Complex lesion management
- IVUS/OCT/FFR technical studies
- Operator technique comparisons
- Complication management
- Hemodynamic support device trials
- Structural heart interventions

**SKIP**
- Basic science without clinical application
- Animal studies
- Small case series (<50 patients)
- Methods papers
- Duplicate/follow-up analyses of known trials
- Topics outside cardiology scope
- Pediatric cardiology (unless breakthrough)
- Surgical techniques (CABG, valve surgery)

USER:
Classify this article:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}

Respond with JSON only:
{"classification": "B2C" or "B2B" or "SKIP", "confidence": 1-10, "reasoning": "brief explanation", "angle": "the unique hook for content"}
```

### B2C Content Prompt (Peter Attia + Eric Topol Style)

```
SYSTEM:
You are Dr. Shailesh Singh, an interventional cardiologist writing editorial-level content for an educated public audience.

Your voice combines:
- The intellectual rigor of Peter Attia
- The scientific accuracy of Eric Topol's Ground Truths
- Accessible but NEVER dumbed down
- Always cite the study with journal name
- Include actual statistics (HR, NNT, CI when meaningful)

RULES:
- Never say "groundbreaking" or "game-changing"
- Don't oversimplify - your audience is educated
- Include caveats and limitations
- Cite the journal: "In this week's NEJM..."
- No medical advice disclaimers mid-text
- Write as an authority, not a reporter
- Keep it 400-600 words

USER:
Write an editorial-level piece about this study:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}
ANGLE TO EXPLORE: {angle from triage}

Write a 400-600 word piece that:
1. Opens with a compelling hook (why this matters NOW)
2. Explains the study design briefly
3. Presents key findings with actual numbers
4. Discusses clinical implications
5. Adds your expert perspective
6. Ends with actionable insight or thought-provoking question
```

### B2B Content Prompt (Mini-Editorial for Interventionalists)

```
SYSTEM:
You are Dr. Shailesh Singh writing a mini-editorial for fellow interventional cardiologists.

Your audience: Cath lab operators, interventional cardiology fellows, referring cardiologists.

STYLE:
- Assume reader knows PCI, FFR, IVUS, DES vs BMS
- Use abbreviations freely (MACE, TLR, TVR, ST)
- Be direct and opinionated
- Reference specific trial names if comparing
- Include NNT/NNH when calculable
- This is peer-to-peer, not patient education
- Keep it 300-500 words

USER:
Write a mini-editorial about this study:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}

Write a 300-500 word mini-editorial that:
1. States the clinical question this addresses
2. Summarizes the trial design (N, endpoints, follow-up)
3. Presents primary and key secondary outcomes with statistics
4. Critically appraises: strengths and limitations
5. Compares to existing evidence if relevant
6. Gives your take: "What I'm taking to the cath lab"
7. Bottom line in 1-2 sentences
```

---

## Article Data Structure

```json
{
  "source": "rss" | "pubmed",
  "feedId": "jacc" | "nejm" | "pubmed" | etc,
  "title": "Article title",
  "abstract": "Full abstract text (up to 3000 chars)",
  "journal": "JACC Cardiovascular Interventions",
  "tier": "general" | "cardiology" | "interventional" | "heartfailure" | "imaging" | "prevention",
  "pubDate": "2024-12-14",
  "authors": "Smith J, Jones M, et al",
  "url": "https://...",
  "doi": "10.1234/...",
  "pmid": "12345678" (if from PubMed),

  // After triage
  "triage": {
    "classification": "B2C" | "B2B" | "SKIP",
    "confidence": 8,
    "reasoning": "Major lifestyle intervention trial with public health implications",
    "angle": "The Mediterranean diet debate gets new evidence"
  },

  // After content generation
  "generatedContent": "Full 400-600 word article...",
  "contentType": "B2C" | "B2B"
}
```

---

## Processing Limits

- Max articles to fetch: 40 total
- Max articles per RSS feed: 5
- Max B2C articles to generate: 5
- Max B2B articles to generate: 5
- Sort by: triage confidence score (highest first)

---

## API Credentials Required

### OpenRouter (for AI)
- **API Key**: `sk-or-v1-...`
- **Header**: `Authorization: Bearer {api_key}`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Model (free)**: `meta-llama/llama-3.1-8b-instruct:free`
- **Model (production)**: `anthropic/claude-3.5-sonnet`

### Gmail SMTP (for email)
- **Host**: `smtp.gmail.com`
- **Port**: `465`
- **SSL**: `true`
- **User**: Your Gmail address (from .env)
- **Password**: App Password (16 chars from Google)

### Slack API (for notifications)
- **Bot Token**: `xoxb-...`
- **Channel**: `#medical-content` or channel ID

---

## Email Template

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: 'Georgia', serif;
      max-width: 750px;
      margin: 0 auto;
      padding: 20px;
      background: #fafafa;
      color: #1a1a1a;
      line-height: 1.7;
    }
    .header {
      background: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
      color: white;
      padding: 35px;
      border-radius: 12px 12px 0 0;
      text-align: center;
    }
    .header h1 {
      margin: 0 0 8px 0;
      font-size: 28px;
    }
    .content {
      background: white;
      padding: 30px;
      border-radius: 0 0 12px 12px;
    }

    /* B2C Section - Blue theme */
    .section.b2c .article {
      border-left: 4px solid #0ea5e9;
      background: #f0f9ff;
    }

    /* B2B Section - Gold theme */
    .section.b2b .article {
      border-left: 4px solid #ca8a04;
      background: #fefce8;
    }

    .article {
      margin: 25px 0;
      padding: 20px;
      border-radius: 8px;
    }
    .article-title {
      font-size: 18px;
      font-weight: 600;
      color: #1a365d;
    }
    .article-meta {
      font-size: 13px;
      color: #64748b;
      margin: 8px 0 15px 0;
    }
    .article-content {
      font-size: 15px;
      line-height: 1.8;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>Dr. Shailesh Singh's Medical Insights</h1>
    <p>{date} | {b2c_count} Public Articles | {b2b_count} Clinical Editorials</p>
  </div>

  <div class="content">
    <!-- B2C Section -->
    <div class="section b2c">
      <h2>📚 For My Patients & Followers</h2>
      <p><em>Evidence-based insights for the health-conscious</em></p>

      {for each b2c_article}
      <div class="article">
        <div class="article-title">
          <a href="{url}">{title}</a>
        </div>
        <div class="article-meta">{journal} | {authors}</div>
        <div class="article-content">{generatedContent}</div>
      </div>
      {/for}
    </div>

    <!-- B2B Section -->
    <div class="section b2b">
      <h2>🏥 For My Colleagues</h2>
      <p><em>Mini-editorials on interventional cardiology</em></p>

      {for each b2b_article}
      <div class="article">
        <div class="article-title">
          <a href="{url}">{title}</a>
        </div>
        <div class="article-meta">{journal} | {authors}</div>
        <div class="article-content">{generatedContent}</div>
      </div>
      {/for}
    </div>
  </div>
</body>
</html>
```

---

## Python Implementation (Claude Code / Script)

### Dependencies
```
pip install feedparser requests anthropic openai
```

### Core Functions

```python
import feedparser
import requests
import json
from datetime import datetime

# 1. Fetch RSS feeds
def fetch_rss(url, max_items=5):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:max_items]:
        articles.append({
            'title': entry.get('title', ''),
            'abstract': entry.get('summary', entry.get('description', '')),
            'url': entry.get('link', ''),
            'pubDate': entry.get('published', ''),
            'authors': entry.get('author', 'Unknown')
        })
    return articles

# 2. Fetch PubMed
def fetch_pubmed(query, max_results=15):
    # Search
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json',
        'usehistory': 'y'
    }
    search_resp = requests.get(search_url, params=params).json()

    # Fetch
    if search_resp['esearchresult']['idlist']:
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'WebEnv': search_resp['esearchresult']['webenv'],
            'query_key': search_resp['esearchresult']['querykey'],
            'retmode': 'xml',
            'rettype': 'abstract'
        }
        # Parse XML and extract articles...
    return articles

# 3. AI Triage
def triage_article(article, client):
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {"role": "system", "content": TRIAGE_SYSTEM_PROMPT},
            {"role": "user", "content": f"TITLE: {article['title']}\nJOURNAL: {article['journal']}\nABSTRACT: {article['abstract']}"}
        ]
    )
    return json.loads(response.choices[0].message.content)

# 4. Generate Content
def generate_b2c_content(article, client):
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {"role": "system", "content": B2C_SYSTEM_PROMPT},
            {"role": "user", "content": f"TITLE: {article['title']}\nJOURNAL: {article['journal']}\nABSTRACT: {article['abstract']}\nANGLE: {article['triage']['angle']}"}
        ]
    )
    return response.choices[0].message.content

# 5. Send Email (using smtplib)
def send_email(html_content, subject, to_email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = to_email
    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_APP_PASSWORD'))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
```

---

## n8n Troubleshooting Guide

### Common Issues & Fixes

**1. "Credentials not set" error (red triangle on nodes)**
- Click the node with red triangle
- Click "Credential to connect with" dropdown
- Select existing credential OR create new one
- For HTTP Request nodes using OpenRouter: Choose "Header Auth"

**2. "Header Auth" credential setup**
- Name: `Authorization`
- Value: `Bearer ${OPENROUTER_API_KEY}` (from your .env file)

**3. SMTP credential setup**
- Host: `smtp.gmail.com`
- Port: `465`
- User: Your Gmail address
- Password: 16-char app password from Google
- SSL/TLS: ON

**4. Slack credential setup** (optional)
- Access Token: Your Slack bot token from api.slack.com

**5. "DNS error" or network issues**
- Retry - usually temporary
- Check if n8n has internet access
- Some RSS feeds block non-browser requests

**6. "Type mismatch" errors**
- Usually in IF nodes comparing strings to numbers
- Change typeValidation from "strict" to "loose"

**7. Loop not progressing**
- Check if the loop output connects back to the loop input
- Ensure there's a "done" branch connecting to next stage

---

## Quick Start with Claude Code

If you want to run this as a Python script instead of n8n:

```bash
# In a new chat, say:
"Build a Python script that:
1. Fetches articles from these RSS feeds: [paste feed URLs]
2. Searches PubMed for cardiology articles from last 2 days
3. Uses OpenRouter API to triage each article as B2C/B2B/SKIP
4. Generates content using the prompts in MEDICAL-CONTENT-ENGINE-SPEC.md
5. Sends HTML email via Gmail SMTP
6. Posts summary to Slack

Use the exact prompts and data structures from MEDICAL-CONTENT-ENGINE-SPEC.md"
```

---

## Environment Variables

```env
# OpenRouter
OPENROUTER_API_KEY=your_openrouter_key_here

# Gmail
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Slack (optional)
SLACK_BOT_TOKEN=your_slack_bot_token_here
SLACK_CHANNEL=your_channel_id

# Optional: NCBI API key for higher rate limits
NCBI_API_KEY=your_ncbi_key_here
```

---

## Success Metrics

- Daily output: 3-5 B2C pieces, 2-3 B2B pieces
- Triage accuracy: >80% appropriate classification
- Content quality: Ready to post with minimal editing
- Zero hallucinated citations

---

## Brand Voice Summary

### B2C Voice (Public Content)
- **Like**: Peter Attia's intellectual rigor + Eric Topol's Ground Truths
- **Tone**: Authoritative but accessible, never dumbed down
- **Citations**: Always cite journal name
- **Statistics**: Include HR, NNT, CI when meaningful
- **Avoid**: "Groundbreaking", "game-changing", oversimplification

### B2B Voice (Doctor Content)
- **Like**: JACC editorial perspective pieces
- **Tone**: Peer-to-peer, direct, opinionated
- **Jargon**: Use freely (MACE, TLR, TVR, ST, DES, BMS, FFR, IVUS)
- **Structure**: Clinical question → Trial design → Results → Critique → Bottom line
- **Signature**: "What I'm taking to the cath lab"
