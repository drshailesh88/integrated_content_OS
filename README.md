# Integrated Content Operating System

Single source of truth for Dr. Shailesh Singh's content creation, research,
and writing workflows.

## Fresh Machine Setup (Required)

1. Create `.env` from `.env.example` and set `NCBI_API_KEY` (plus other keys).
2. Install PubMed MCP dependencies:
   ```bash
   cd pubmed-mcp-server
   npm install
   ```
3. MCP config is already wired in `.mcp.json` and points to
   `pubmed-mcp-server/dist/index.js`.

## Quick Start

```bash
python pipelines/twitter-content/generate.py "What are statin side effects?"
python research-engine/run_pipeline.py --quick
python rag-pipeline/src/knowledge_pipeline.py --query "SGLT2 heart failure"
```

## Notes

- `.env` is intentionally not committed.
- PubMed MCP is mandatory for research outputs.
