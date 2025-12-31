# YouTube Comment Analyzer

**Trigger phrases:**
- "Analyze comments for [URL]"
- "Analyze this video: [URL]"
- "What are people asking about [URL]"
- "Comment analysis for [VIDEO_ID]"
- "YouTube comment insights for [URL]"

---

## What This Does

When the user gives you a YouTube URL or video ID and asks for comment analysis, you:

1. **Extract the video ID** from the URL
2. **Run the analyzer** (handles 2000+ comments with map-reduce)
3. **Read the output** and present a clean summary
4. **Save to file** for future reference

---

## How to Use (Claude Instructions)

### Step 1: Extract Video ID

From URL patterns:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID&...`
- Just `VIDEO_ID` (11 characters, alphanumeric with - and _)

### Step 2: Run the Analyzer

```bash
cd "/Users/shaileshsingh/integrated cowriting system/research-engine" && python analyze_chunked.py VIDEO_ID
```

**Options if needed:**
- `--model gemini-2-flash` — Faster analysis
- `--force-map-reduce` — For thorough analysis
- `--max-comments 500` — Limit comments scraped

### Step 3: Read the Output

The script tells you where the output was saved. Read that file:
```
output/chunked_analysis_VIDEO_ID_TIMESTAMP.json
```

### Step 4: Present Summary

Extract and present to user:
- **Top 5 Questions** people are asking
- **Top 5 Myths** that need addressing
- **Top 3 Pain Points** viewers have
- **Content Recommendations** (what to make next)
- **Overall Sentiment** summary

---

## Example Workflow

**User says:** "Analyze comments for https://youtube.com/watch?v=abc123xyz"

**Claude does:**

1. Extract: `abc123xyz`
2. Run:
   ```bash
   cd "/Users/shaileshsingh/integrated cowriting system/research-engine" && python analyze_chunked.py abc123xyz
   ```
3. Wait for completion (shows progress)
4. Read the output JSON
5. Present clean summary

---

## Output Format for User

```
## Comment Analysis: [Video Title or ID]

**Analyzed:** 1,847 comments | **Time:** 45 seconds

### Top Questions (What viewers want to know)
1. [Question] — HIGH urgency
2. [Question] — MEDIUM urgency
3. ...

### Top Myths (Misconceptions to address)
1. [Myth] — HIGH danger
2. [Myth] — MEDIUM danger
3. ...

### Pain Points (Viewer frustrations)
1. [Pain point]
2. [Pain point]
3. ...

### Content Recommendations
- **Must Address:** [topics]
- **Content Gaps:** [topics]
- **Viral Potential:** [topics]

### Sentiment
Positive: X | Negative: Y | Neutral: Z
Summary: [one line]
```

---

## Error Handling

- **No comments found:** Tell user the video might have comments disabled
- **API error:** Suggest trying again or using `--model gemini-2-flash`
- **Rate limited:** Wait and retry, or try a different model

---

## Notes

- Uses **free LLMs** via OpenRouter (no cost)
- Handles **2000+ comments** via map-reduce chunking
- Output saved to file for future reference
- Works with any YouTube video with comments enabled
