# Medical Content Engine - Getting Started

Fetches latest medical research, uses AI to triage and generate content, and saves to Obsidian-compatible Markdown.

---

## Quick Start (Manual Run)

```bash
cd "/Users/shaileshsingh/Desktop/medical journal content/medical-content-engine"

# Run and save as Markdown (for Obsidian)
python3 main.py --no-email --no-slack --markdown

# The file will be saved to: output/digests/YYYY-MM-DD-medical-digest.md
```

---

## All Run Options

| Command | What it does |
|---------|--------------|
| `python3 main.py --markdown` | Full run, saves Markdown digest |
| `python3 main.py --test --markdown` | Test mode (3 articles only) |
| `python3 main.py --feeds-only` | Just fetch articles, no AI |
| `python3 main.py --save` | Save intermediate JSON files |

---

## API Keys (.env)

Create a `.env` file with your OpenRouter key (needed for AI triage/generation):

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
NCBI_API_KEY=optional-for-faster-pubmed
```

---

## GitHub Actions (Automated Daily Runs)

The workflow file is at `.github/workflows/daily-digest.yml`.

To enable:
1. Push this folder to a GitHub repository
2. Go to Settings > Secrets and add:
   - `OPENROUTER_API_KEY`
   - `NCBI_API_KEY` (optional)
3. The workflow runs daily at 7 AM IST
4. You can also trigger manually from Actions tab

---

## Output Location

Your digest files are saved at:
```
output/digests/YYYY-MM-DD-medical-digest.md
```

Open this folder in Obsidian as a vault, or copy files to your existing vault.

