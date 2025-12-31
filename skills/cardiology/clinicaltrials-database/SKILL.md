# ClinicalTrials.gov Database

Query the U.S. National Library of Medicine's clinical trials registry through API v2. Public access, no authentication required.

## Triggers

- User asks about ongoing or completed clinical trials
- User needs trial details for a specific drug/intervention
- User wants to track recruitment status
- User is analyzing trial landscape for a cardiology topic
- User needs NCT numbers for references

## Core Capabilities

| Function | Description |
|----------|-------------|
| Condition search | Find trials for specific diseases |
| Intervention tracking | Identify trials testing drugs/devices |
| Geographic filtering | Locate trials by region/facility |
| Sponsor lookup | Search by conducting organization |
| Status filtering | Filter by recruitment stage |
| NCT detail retrieval | Full study information via NCT ID |
| CSV export | Download data for analysis |

## API Technical Details

- **Rate limit**: ~50 requests/minute
- **Response formats**: JSON, CSV
- **Max page size**: 1000 studies per request
- **Date format**: ISO 8601

## Example Searches

### Cardiology Trial Discovery

```python
# Find active heart failure trials
GET /studies?query.cond=heart+failure&filter.overallStatus=RECRUITING

# SGLT2 inhibitor trials in cardiology
GET /studies?query.intr=SGLT2+inhibitor&query.cond=cardiovascular

# Trials at major academic centers
GET /studies?query.locn=Cleveland+Clinic&query.cond=coronary+artery+disease

# Phase 3 trials for new anticoagulants
GET /studies?query.intr=anticoagulant&filter.phase=PHASE3
```

### Common Status Values
- `RECRUITING` - Currently enrolling
- `ACTIVE_NOT_RECRUITING` - Ongoing, enrollment closed
- `COMPLETED` - Trial finished
- `TERMINATED` - Stopped early
- `WITHDRAWN` - Never started enrollment

## Workflow Integration

### For Newsletter/Editorial Content
1. Search for recent trial results in target area
2. Identify landmark trials by enrollment size and phase
3. Pull NCT IDs for proper citation
4. Cross-reference with PubMed for published results
5. Note primary endpoints and key secondary outcomes

### For Trial Analysis Pieces
1. Retrieve full study record via NCT ID
2. Extract: design, enrollment, endpoints, sponsor
3. Compare with published results if available
4. Assess trial quality (blinding, randomization, sample size)
5. Contextualize within existing evidence

## Key Fields to Extract

| Field | Use Case |
|-------|----------|
| `briefTitle` | Quick reference |
| `officialTitle` | Full citation |
| `studyType` | Interventional vs observational |
| `phases` | Development stage |
| `enrollmentInfo` | Sample size |
| `primaryOutcomes` | Main endpoints |
| `startDate` / `completionDate` | Timeline |
| `leadSponsor` | Industry vs academic |

## Best Practices

- Always cite NCT number when discussing trials
- Note enrollment numbers for context on power
- Distinguish between primary and secondary endpoints
- Check for related publications in PubMed
- Note funding source for potential bias assessment
