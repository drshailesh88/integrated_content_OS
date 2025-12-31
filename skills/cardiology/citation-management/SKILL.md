# Citation Management

Systematic citation management for accurate referencing in scientific and medical content.

## Triggers

- User needs to format citations
- User asks for references in a specific style
- User needs to verify citation accuracy
- User wants to build a bibliography
- User is managing references for an article

## Core Capabilities

### Citation Discovery

**Search Strategies by Database**:

| Database | Best For | Search Tips |
|----------|----------|-------------|
| PubMed | Biomedical | Use MeSH terms, [au], [ti] tags |
| Google Scholar | Broad coverage | Use exact phrases, author: operator |
| Semantic Scholar | AI-powered relevance | Natural language queries |
| CrossRef | DOI lookup | Search by DOI or metadata |

### Metadata Extraction

From any identifier, extract:
- Authors (full names, order)
- Title (exact, including subtitles)
- Journal (official name, abbreviation)
- Year, volume, issue, pages
- DOI
- PMID (for PubMed articles)

### Citation Style Formats

**AMA (American Medical Association)** - Used by JAMA, NEJM:
```
Yusuf S, Pitt B, Davis CE, et al. Effect of enalapril on survival in patients with reduced left ventricular ejection fractions and congestive heart failure. N Engl J Med. 1991;325(5):293-302. doi:10.1056/NEJM199108013250501
```

**Vancouver (Numbered)** - Common in medical journals:
```
1. Yusuf S, Pitt B, Davis CE, et al. Effect of enalapril on survival in patients with reduced left ventricular ejection fractions and congestive heart failure. N Engl J Med 1991;325:293-302.
```

**APA 7th Edition**:
```
Yusuf, S., Pitt, B., Davis, C. E., Hood, W. B., & Cohn, J. N. (1991). Effect of enalapril on survival in patients with reduced left ventricular ejection fractions and congestive heart failure. New England Journal of Medicine, 325(5), 293-302. https://doi.org/10.1056/NEJM199108013250501
```

**Nature Style**:
```
Yusuf, S. et al. Effect of enalapril on survival in patients with reduced left ventricular ejection fractions and congestive heart failure. N. Engl. J. Med. 325, 293-302 (1991).
```

### BibTeX Format

```bibtex
@article{yusuf1991effect,
  author = {Yusuf, Salim and Pitt, Bertram and Davis, Clarence E and Hood, William B and Cohn, Jay N},
  title = {Effect of enalapril on survival in patients with reduced left ventricular ejection fractions and congestive heart failure},
  journal = {New England Journal of Medicine},
  volume = {325},
  number = {5},
  pages = {293--302},
  year = {1991},
  doi = {10.1056/NEJM199108013250501},
  pmid = {2057034}
}
```

## Citation Validation

### Required Checks
- [ ] DOI resolves correctly
- [ ] Author names spelled correctly
- [ ] Year matches publication
- [ ] Journal name official (not abbreviated incorrectly)
- [ ] Page numbers accurate
- [ ] No duplicate entries

### Common Errors to Catch
- Incorrect author order
- Missing co-authors (et al. threshold varies by style)
- Wrong publication year
- Journal abbreviation vs full name inconsistency
- Missing DOI when available
- PMID/DOI mismatch

## Workflow Integration

### For Newsletter Writing
1. Identify claims needing citation
2. Search PubMed for supporting evidence
3. Extract DOI/PMID from best sources
4. Format in consistent style (usually AMA for medical)
5. Verify each citation before publishing

### For Academic Content
1. Maintain running bibliography as you write
2. Use consistent identifier (DOI preferred)
3. Cross-reference with literature-review skill
4. Verify against CrossRef before submission
5. Format per target journal requirements

## Quick Reference

### Convert DOI to Citation
1. Go to doi.org/[DOI]
2. Extract metadata from landing page
3. Format per required style
4. Verify author count and order

### Convert PMID to Citation
1. Search PubMed with PMID
2. Use "Cite" button for formatted output
3. Select desired format
4. Verify completeness

### Handling Preprints
- Note preprint server (bioRxiv, medRxiv)
- Include "Preprint" designation
- Add DOI (preprint DOIs differ from published)
- Update citation if peer-reviewed version publishes

## Best Practices

1. **Always include DOI** when available
2. **Verify primary sources** - don't cite citations
3. **Update preprint citations** when published
4. **Use consistent style** throughout document
5. **Check et al. thresholds** - varies by style (3, 6, or 7 authors)
6. **Include access dates** for online-only sources
7. **Note retractions** - check Retraction Watch
