Tool Call Arguments:

```json
{
  "queryTerm": "neuroinflammation AND (Alzheimer's OR Parkinson's) AND microglia",
  "maxResults": 15,
  "sortBy": "pub_date",
  "dateRange": {
    "minDate": "2023/01/01",
    "maxDate": "2024/12/31",
    "dateType": "pdat"
  },
  "filterByPublicationTypes": ["Review", "Journal Article"],
  "fetchBriefSummaries": 5
}
```

Tool Response:

```json
{
  "searchParameters": {
    "queryTerm": "neuroinflammation AND (Alzheimer's OR Parkinson's) AND microglia",
    "maxResults": 15,
    "sortBy": "pub_date",
    "dateRange": {
      "minDate": "2023/01/01",
      "maxDate": "2024/12/31",
      "dateType": "pdat"
    },
    "filterByPublicationTypes": ["Review", "Journal Article"],
    "fetchBriefSummaries": 5
  },
  "effectiveESearchTerm": "neuroinflammation AND (Alzheimer's OR Parkinson's) AND microglia AND (2023/01/01[pdat] : 2024/12/31[pdat]) AND (\"Review\"[Publication Type] OR \"Journal Article\"[Publication Type])",
  "totalFound": 1290,
  "retrievedPmidCount": 15,
  "pmids": [
    39715098, 39359093, 39704040, 39653749, 39648189, 39075895, 40256246,
    39761611, 39726135, 39719687, 39718073, 39514171, 39433702, 39400857,
    39029776
  ],
  "briefSummaries": [
    {
      "pmid": "39715098",
      "title": "The compound (E)-2-(3,4-dihydroxystyryl)-3-hydroxy-4H-pyran-4-one alleviates neuroinflammation and cognitive impairment in a mouse model of Alzheimer's disease.",
      "authors": "Liu X, Wu W, Li X, et al.",
      "source": "Neural Regen Res",
      "doi": "",
      "pubDate": "2025-11-01",
      "epubDate": "2024-07-10"
    },
    {
      "pmid": "39359093",
      "title": "The cGAS-STING-interferon regulatory factor 7 pathway regulates neuroinflammation in Parkinson's disease.",
      "authors": "Zhou S, Li T, Zhang W, et al.",
      "source": "Neural Regen Res",
      "doi": "",
      "pubDate": "2025-08-01",
      "epubDate": "2024-06-03"
    },
    {
      "pmid": "39704040",
      "title": "&#x3b1;-Synuclein in Parkinson's Disease: From Bench to Bedside.",
      "authors": "Bellini G, D'Antongiovanni V, Palermo G, et al.",
      "source": "Med Res Rev",
      "doi": "",
      "pubDate": "2026-05-20",
      "epubDate": "2024-12-20"
    },
    {
      "pmid": "39653749",
      "title": "Neuroinflammation in Alzheimer disease.",
      "authors": "Heneka MT, van der Flier WM, Jessen F, et al.",
      "source": "Nat Rev Immunol",
      "doi": "",
      "pubDate": "2026-05-20",
      "epubDate": "2024-12-09"
    },
    {
      "pmid": "39648189",
      "title": "Unveiling the Involvement of Herpes Simplex Virus-1 in Alzheimer's Disease: Possible Mechanisms and Therapeutic Implications.",
      "authors": "Chauhan P, Begum MY, Narapureddy BR, et al.",
      "source": "Mol Neurobiol",
      "doi": "",
      "pubDate": "2026-05-20",
      "epubDate": "2024-12-09"
    }
  ],
  "eSearchUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=neuroinflammation+AND+%28Alzheimer%27s+OR+Parkinson%27s%29+AND+microglia+AND+%282023%2F01%2F01%5Bpdat%5D+%3A+2024%2F12%2F31%5Bpdat%5D%29+AND+%28%22Review%22%5BPublication+Type%5D+OR+%22Journal+Article%22%5BPublication+Type%5D%29&retmax=15&sort=pub_date&usehistory=y",
  "eSummaryUrl": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&version=2.0&retmode=xml&WebEnv=MCID_6832175795dfc79c7001d173&query_key=1&retmax=5"
}
```
