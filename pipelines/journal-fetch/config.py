"""
Medical Content Engine Configuration
Contains RSS feeds, AI prompts, and constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# =============================================================================
# API CONFIGURATION
# =============================================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL_FREE = "meta-llama/llama-3.1-8b-instruct:free"
AI_MODEL_PRODUCTION = "anthropic/claude-3.5-sonnet"

# Use free model by default, switch to production for better quality
AI_MODEL = AI_MODEL_FREE

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "shailesh.greatest@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# PubMed API
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

# =============================================================================
# RSS FEEDS
# =============================================================================

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

# =============================================================================
# PUBMED CONFIGURATION
# =============================================================================

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

PUBMED_SEARCH_QUERY = (
    '(cardiology[tiab] OR cardiovascular[tiab] OR "heart failure"[tiab] OR '
    '"coronary artery"[tiab] OR "percutaneous coronary intervention"[tiab]) '
    'AND ("last 2 days"[edat])'
)

PUBMED_MAX_RESULTS = 15

# =============================================================================
# AI PROMPTS
# =============================================================================

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

# -----------------------------------------------------------------------------

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
- Incorporate evidence from the provided guideline snippets if relevant (cite as "current guidelines" or "standard textbooks")
- Keep it 400-600 words"""

B2C_USER_PROMPT = """Write an editorial-level piece about this study:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}
ANGLE TO EXPLORE: {angle}
RELEVANT GUIDELINES/TEXTBOOKS:
{guidelines}

Write a 400-600 word piece that:
1. Opens with a compelling hook (why this matters NOW)
2. Explains the study design briefly
3. Presents key findings with actual numbers
4. Discusses clinical implications
5. Adds your expert perspective
6. Ends with actionable insight or thought-provoking question"""

# -----------------------------------------------------------------------------

B2B_SYSTEM_PROMPT = """You are Dr. Shailesh Singh writing a mini-editorial for fellow interventional cardiologists.

Your audience: Cath lab operators, interventional cardiology fellows, referring cardiologists.

STYLE:
- Assume reader knows PCI, FFR, IVUS, DES vs BMS
- Use abbreviations freely (MACE, TLR, TVR, ST)
- Be direct and opinionated
- Reference specific trial names if comparing
- Include NNT/NNH when calculable
- This is peer-to-peer, not patient education
- Incorporate evidence from the provided guideline snippets to provide clinical context or contrast (cite as "contemporary guidelines" or "standard references")
- Keep it 300-500 words"""

B2B_USER_PROMPT = """Write a mini-editorial about this study:

TITLE: {title}
JOURNAL: {journal}
ABSTRACT: {abstract}
RELEVANT GUIDELINES/TEXTBOOKS:
{guidelines}

Write a 300-500 word mini-editorial that:
1. States the clinical question this addresses
2. Summarizes the trial design (N, endpoints, follow-up)
3. Presents primary and key secondary outcomes with statistics
4. Critically appraises: strengths and limitations
5. Compares to existing evidence if relevant
6. Gives your take: "What I'm taking to the cath lab"
7. Bottom line in 1-2 sentences"""

# =============================================================================
# DEFAULTS
# =============================================================================

DEFAULT_RECIPIENT_EMAIL = "shailesh.greatest@gmail.com"
REQUEST_TIMEOUT = 30  # seconds
RSS_FETCH_TIMEOUT = 15  # seconds
