# Medical Content Engine - Build Specification

## PROJECT OVERVIEW

Build a Python-based medical content engine for Dr. Shailesh Singh (Interventional Cardiologist) that:

1. **Fetches** latest articles from 20+ medical/cardiology journals via RSS feeds and PubMed API
2. **Triages** each article using AI to classify as: B2C (public content), B2B (doctor content), or SKIP
3. **Generates** editorial-quality content for each audience type
4. **Delivers** via HTML email and Slack notification

**Run frequency**: Daily at 7 AM, or on-demand via command line

---

## BRAND & VOICE REQUIREMENTS

### B2C Content (For Patients & Public)
- **Style**: Peter Attia's intellectual rigor + Eric Topol's scientific accuracy
- **Tone**: Authoritative but accessible, NEVER dumbed down
- **Length**: 400-600 words per article
- **Must include**: Journal citations, actual statistics (HR, NNT, CI)
- **Avoid**: "Groundbreaking", "game-changing", oversimplification

### B2B Content (For Fellow Doctors)
- **Style**: JACC editorial perspective pieces
- **Tone**: Peer-to-peer, direct, opinionated
- **Length**: 300-500 words per article
- **Jargon**: Use freely (MACE, TLR, TVR, ST, DES, BMS, FFR, IVUS)
- **Signature phrase**: "What I'm taking to the cath lab"

---

## DATA SOURCES

### RSS Feeds (Use feedparser library)

```python
RSS_FEEDS = [
    # Tier 1: General Medical
    {"id": "nejm", "name": "NEJM", "url": "https://www.nejm.org/action/showFeed?jc=nejm&type=etoc&feed=rss", "tier": "general"},
    {"id": "lancet", "name": "The Lancet", "url": "https://www.thelancet.com/rssfeed/lancet_current.xml", "tier": "general"},
    {"id": "jama", "name": "JAMA", "url": "https://jamanetwork.com/rss/site_3/67.xml", "tier": "general"},
    {"id": "bmj", "name": "BMJ", "url": "https://www.bmj.com/rss/recent.xml", "tier": "general"},

    # Tier 2: Cardiology Core
    {"id": "jama-cardio", "name": "JAMA Cardiology", "url": "https://jamanetwork.com/rss/site_192/184.xml", "tier": "cardiology"},
    {"id": "circulation", "name": "Circulation", "url": "https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=circ", "tier": "cardiology"},
    {"id": "jacc", "name": "JACC", "url": "https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=jacc", "tier": "cardiology"},
    {"id": "ehj", "name": "European Heart Journal", "url": "https://academic.oup.com/eurheartj/rss", "tier": "cardiology"},
    {"id": "nature-cardio", "name": "Nature Reviews Cardiology", "url": "https://www.nature.com/nrcardio.rss", "tier": "cardiology"},

    # Tier 3: Interventional Cardiology (B2B Focus)
    {"id": "jacc-interventions", "name": "JACC Cardiovascular Interventions", "url": "https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=jint", "tier": "interventional"},
    {"id": "circ-interventions", "name": "Circulation Cardiovascular Interventions", "url": "https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=circinterventions", "tier": "interventional"},
    {"id": "eurointervention", "name": "EuroIntervention", "url": "https://www.pcronline.com/eurointervention/rss", "tier": "interventional"},
    {"id": "cci", "name": "Catheterization & Cardiovascular Interventions", "url": "https://onlinelibrary.wiley.com/feed/1522726x/most-recent", "tier": "interventional"},

    # Tier 4: Heart Failure & Imaging
    {"id": "jacc-hf", "name": "JACC Heart Failure", "url": "https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=heart", "tier": "heartfailure"},
    {"id": "esc-hf", "name": "European Journal of Heart Failure", "url": "https://onlinelibrary.wiley.com/feed/18790844/most-recent", "tier": "heartfailure"},
    {"id": "jacc-imaging", "name": "JACC Cardiovascular Imaging", "url": "https://www.jacc.org/action/showFeed?type=etoc&feed=rss&jc=imaging", "tier": "imaging"},

    # Tier 5: Prevention & Research
    {"id": "ejpc", "name": "European Journal of Preventive Cardiology", "url": "https://academic.oup.com/eurjpc/rss", "tier": "prevention"},
    {"id": "hypertension", "name": "Hypertension", "url": "https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=hyp", "tier": "prevention"},
    {"id": "circ-research", "name": "Circulation Research", "url": "https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=res", "tier": "research"},
    {"id": "jaha", "name": "JAHA", "url": "https://www.ahajournals.org/action/showFeed?type=etoc&feed=rss&jc=jaha", "tier": "cardiology"},
]
```

### PubMed API

**Search Endpoint:**
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```

**Parameters:**
```python
{
    "db": "pubmed",
    "term": '(cardiology[tiab] OR cardiovascular[tiab] OR "heart failure"[tiab] OR "coronary artery"[tiab] OR "percutaneous coronary intervention"[tiab]) AND ("last 2 days"[edat])',
    "retmax": 15,
    "retmode": "json",
    "usehistory": "y"
}
```

**Fetch Endpoint (after search):**
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

**Parameters:**
```python
{
    "db": "pubmed",
    "WebEnv": "<from_search_response>",
    "query_key": "<from_search_response>",
    "retmode": "xml",
    "rettype": "abstract"
}
```

---

## AI CONFIGURATION

### Provider: OpenRouter
- **Base URL**: `https://openrouter.ai/api/v1/chat/completions`
- **Free Model**: `meta-llama/llama-3.1-8b-instruct:free`
- **Production Model**: `anthropic/claude-3.5-sonnet`

### API Call Format:
```python
import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
)
result = response.json()
content = result["choices"][0]["message"]["content"]
```

---

## AI PROMPTS

### 1. TRIAGE PROMPT (Classification)

```python
TRIAGE_SYSTEM_PROMPT = """You are a medical content strategist for Dr. Shailesh Singh, an interventional cardiologist building a personal brand.

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
- Surgical techniques (CABG, valve surgery)"""

TRIAGE_USER_PROMPT = """Classify this article:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}

Respond with JSON only:
{{"classification": "B2C" or "B2B" or "SKIP", "confidence": 1-10, "reasoning": "brief explanation", "angle": "the unique hook for content"}}"""
```

### 2. B2C CONTENT PROMPT (Peter Attia + Eric Topol Style)

```python
B2C_SYSTEM_PROMPT = """You are Dr. Shailesh Singh, an interventional cardiologist writing editorial-level content for an educated public audience.

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
- Keep it 400-600 words"""

B2C_USER_PROMPT = """Write an editorial-level piece about this study:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}
ANGLE TO EXPLORE: {angle}

Write a 400-600 word piece that:
1. Opens with a compelling hook (why this matters NOW)
2. Explains the study design briefly
3. Presents key findings with actual numbers
4. Discusses clinical implications
5. Adds your expert perspective
6. Ends with actionable insight or thought-provoking question"""
```

### 3. B2B CONTENT PROMPT (Mini-Editorial for Interventionalists)

```python
B2B_SYSTEM_PROMPT = """You are Dr. Shailesh Singh writing a mini-editorial for fellow interventional cardiologists.

Your audience: Cath lab operators, interventional cardiology fellows, referring cardiologists.

STYLE:
- Assume reader knows PCI, FFR, IVUS, DES vs BMS
- Use abbreviations freely (MACE, TLR, TVR, ST)
- Be direct and opinionated
- Reference specific trial names if comparing
- Include NNT/NNH when calculable
- This is peer-to-peer, not patient education
- Keep it 300-500 words"""

B2B_USER_PROMPT = """Write a mini-editorial about this study:

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
7. Bottom line in 1-2 sentences"""
```

---

## DATA STRUCTURES

### Article Object
```python
{
    "source": "rss" | "pubmed",
    "title": "Article title",
    "abstract": "Full abstract text",
    "journal": "Journal name",
    "tier": "general" | "cardiology" | "interventional" | "heartfailure" | "imaging" | "prevention",
    "pub_date": "2024-12-18",
    "authors": "Smith J, Jones M, et al",
    "url": "https://...",
    "doi": "10.1234/...",

    # After triage
    "classification": "B2C" | "B2B" | "SKIP",
    "confidence": 8,
    "angle": "The hook for content",

    # After content generation
    "generated_content": "Full 400-600 word article..."
}
```

---

## EMAIL DELIVERY

### Gmail SMTP Configuration
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(html_content, subject, to_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
```

### HTML Email Template
```html
<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Georgia, serif; max-width: 700px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
.header { background: linear-gradient(135deg, #1a365d, #2d5a87); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
.header h1 { margin: 0; font-size: 24px; }
.content { background: white; padding: 25px; border-radius: 0 0 10px 10px; }
.section h2 { color: #1a365d; border-bottom: 2px solid; padding-bottom: 8px; }
.section.b2c h2 { border-color: #0ea5e9; }
.section.b2b h2 { border-color: #ca8a04; }
.article { margin: 20px 0; padding: 20px; border-radius: 8px; border-left: 4px solid; }
.article.b2c { background: #f0f9ff; border-color: #0ea5e9; }
.article.b2b { background: #fefce8; border-color: #ca8a04; }
.article h3 { margin: 0 0 8px 0; font-size: 16px; }
.article h3 a { color: #1a365d; text-decoration: none; }
.meta { font-size: 12px; color: #666; margin-bottom: 12px; }
.text { font-size: 14px; line-height: 1.7; }
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
    <h2>For Patients & Public</h2>
    {b2c_articles_html}
  </div>

  <!-- B2B Section -->
  <div class="section b2b">
    <h2>For Colleagues</h2>
    {b2b_articles_html}
  </div>
</div>
</body>
</html>
```

---

## SLACK DELIVERY

### Slack API
```python
import requests

def send_slack(message, blocks=None):
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": SLACK_CHANNEL,
            "text": message,
            "blocks": blocks
        }
    )
```

---

## ENVIRONMENT VARIABLES

Create a `.env` file:
```
# OpenRouter (AI)
OPENROUTER_API_KEY=your_openrouter_key_here

# Gmail
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Slack (optional)
SLACK_BOT_TOKEN=your_slack_bot_token_here
SLACK_CHANNEL=your_channel_id

# Optional: NCBI for higher PubMed rate limits
NCBI_API_KEY=your_ncbi_key_here
```

---

## PROJECT STRUCTURE

```
medical-content-engine/
├── .env                      # API keys (DO NOT COMMIT)
├── .gitignore
├── requirements.txt
├── main.py                   # Entry point
├── config.py                 # Configuration & constants
├── fetchers/
│   ├── __init__.py
│   ├── rss_fetcher.py       # RSS feed fetching
│   └── pubmed_fetcher.py    # PubMed API
├── ai/
│   ├── __init__.py
│   ├── triage.py            # Article classification
│   └── content_generator.py  # B2C/B2B content generation
├── delivery/
│   ├── __init__.py
│   ├── email_sender.py      # Gmail SMTP
│   └── slack_sender.py      # Slack notifications
├── templates/
│   └── email_template.html
└── output/                   # Generated content (optional)
    └── digests/
```

---

## IMPLEMENTATION STEPS

1. **Set up project structure** with virtual environment
2. **Create config.py** with all RSS feeds and prompts
3. **Build RSS fetcher** using feedparser
4. **Build PubMed fetcher** using requests + XML parsing
5. **Build AI triage** function
6. **Build B2C content generator**
7. **Build B2B content generator**
8. **Build email sender** with HTML template
9. **Build Slack sender**
10. **Create main.py** orchestrating the full pipeline
11. **Add CLI arguments** for manual runs
12. **Test with a few feeds first**

---

## DEPENDENCIES

```
# requirements.txt
feedparser>=6.0.0
requests>=2.28.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

---

## RUNNING THE ENGINE

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python main.py

# Run with options
python main.py --test          # Test mode (only 3 articles)
python main.py --no-email      # Skip email sending
python main.py --feeds-only    # Only fetch, don't generate content
```

---

## SUCCESS METRICS

- Fetches from 15+ working RSS feeds
- Triages articles with >80% accuracy
- Generates 3-5 B2C pieces per run
- Generates 2-3 B2B pieces per run
- Sends formatted email successfully
- Posts Slack notification
- Completes full run in <5 minutes

---

## NOTES FOR CLAUDE

1. Start with a simple working version, then iterate
2. Use feedparser for RSS - it handles most edge cases
3. Some RSS feeds may fail (403, timeout) - handle gracefully, continue with others
4. Test AI calls with one article before looping through all
5. The free Llama model works but is slower - be patient
6. Save intermediate results to JSON for debugging
7. Configure your email in the .env file (GMAIL_USER)
