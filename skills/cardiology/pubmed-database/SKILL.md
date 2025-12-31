# PubMed Database

Direct REST API access to the National Library of Medicine's biomedical literature repository for systematic reviews and research analysis.

## Triggers

- User asks to search for medical/scientific literature
- User needs to find research papers on a cardiology topic
- User wants to build a literature review
- User requests evidence for a clinical claim
- User needs citations for an article or newsletter

## Core Capabilities

### Search Construction
Build sophisticated queries combining:
- Boolean operators (AND, OR, NOT)
- Field tags: `[mh]` for MeSH terms, `[au]` for author, `[ti]` for title, `[tiab]` for title/abstract
- Publication filters by date, type, and availability

### E-utilities API Endpoints
| Endpoint | Purpose |
|----------|---------|
| ESearch | Search and retrieve PMIDs |
| EFetch | Retrieve full records |
| ESummary | Get document summaries |
| EPost | Upload ID lists |
| ELink | Find related articles |

**Rate limits**: 3 requests/second (10 with API key)

### Filtering Options
- Publication type (clinical trials, systematic reviews, meta-analyses)
- Date ranges
- Text availability (free full text, abstracts)
- Species (human studies)

### Citation Export Formats
- NBIB (for reference managers)
- AMA, MLA, APA, Vancouver styles
- BibTeX for LaTeX

## Example Queries

### Cardiology-Specific Searches

```
# Recent SGLT2 inhibitor trials in heart failure
"SGLT2 inhibitors"[mh] AND "heart failure"[mh] AND "clinical trial"[pt] AND "2023"[dp]:present[dp]

# Interventional cardiology systematic reviews
"percutaneous coronary intervention"[mh] AND "systematic review"[pt]

# TAVR outcomes
"transcatheter aortic valve replacement"[tiab] AND (outcomes[tiab] OR mortality[tiab])
```

### Building Evidence for Content
1. Start with MeSH terms for precision
2. Add free-text synonyms for coverage
3. Filter by publication type and recency
4. Review abstracts for relevance
5. Extract key findings with PMIDs for citation

## Workflow Integration

When writing cardiology content:
1. Use this skill to find supporting evidence
2. Document PMIDs for all factual claims
3. Prefer systematic reviews and meta-analyses
4. Include recent trials (last 2-3 years) for currency
5. Cross-reference with citation-management skill for formatting

## Best Practices

- Always verify claims with primary sources
- Note study limitations when citing
- Distinguish between observational and RCT evidence
- Use MeSH terms for reproducible searches
- Document search strategy for transparency
