# pubmed-mcp-server - Directory Structure

Generated on: 2025-08-08 19:58:30

```
pubmed-mcp-server
├── .clinerules
│   └── clinerules.md
├── .github
│   ├── workflows
│   │   └── publish.yml
│   └── FUNDING.yml
├── docs
│   ├── api-references
│   │   └── typedoc-reference.md
│   ├── project-spec.md
│   └── tree.md
├── examples
│   ├── generate_pubmed_chart
│   │   ├── bar_chart.png
│   │   ├── doughnut_chart.png
│   │   ├── line_chart.png
│   │   ├── pie_chart.png
│   │   ├── polar_chart.png
│   │   ├── radar_chart.png
│   │   └── scatter_plot.png
│   ├── pubmed_article_connections_1.md
│   ├── pubmed_article_connections_2.md
│   ├── pubmed_fetch_contents_example.md
│   ├── pubmed_research_agent_example.md
│   └── pubmed_search_articles_example.md
├── scripts
│   ├── clean.ts
│   ├── fetch-openapi-spec.ts
│   ├── make-executable.ts
│   └── tree.ts
├── src
│   ├── config
│   │   └── index.ts
│   ├── mcp-server
│   │   ├── tools
│   │   │   ├── pubmedArticleConnections
│   │   │   │   ├── logic
│   │   │   │   │   ├── citationFormatter.ts
│   │   │   │   │   ├── elinkHandler.ts
│   │   │   │   │   ├── index.ts
│   │   │   │   │   └── types.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── registration.ts
│   │   │   ├── pubmedFetchContents
│   │   │   │   ├── index.ts
│   │   │   │   ├── logic.ts
│   │   │   │   └── registration.ts
│   │   │   ├── pubmedGenerateChart
│   │   │   │   ├── index.ts
│   │   │   │   ├── logic.ts
│   │   │   │   └── registration.ts
│   │   │   ├── pubmedResearchAgent
│   │   │   │   ├── logic
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── inputSchema.ts
│   │   │   │   │   ├── outputTypes.ts
│   │   │   │   │   └── planOrchestrator.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── logic.ts
│   │   │   │   └── registration.ts
│   │   │   └── pubmedSearchArticles
│   │   │       ├── index.ts
│   │   │       ├── logic.ts
│   │   │       └── registration.ts
│   │   ├── transports
│   │   │   ├── auth
│   │   │   │   ├── lib
│   │   │   │   │   ├── authContext.ts
│   │   │   │   │   ├── authTypes.ts
│   │   │   │   │   └── authUtils.ts
│   │   │   │   ├── strategies
│   │   │   │   │   ├── authStrategy.ts
│   │   │   │   │   ├── jwtStrategy.ts
│   │   │   │   │   └── oauthStrategy.ts
│   │   │   │   ├── authFactory.ts
│   │   │   │   ├── authMiddleware.ts
│   │   │   │   └── index.ts
│   │   │   ├── core
│   │   │   │   ├── baseTransportManager.ts
│   │   │   │   ├── headerUtils.ts
│   │   │   │   ├── honoNodeBridge.ts
│   │   │   │   ├── statefulTransportManager.ts
│   │   │   │   ├── statelessTransportManager.ts
│   │   │   │   └── transportTypes.ts
│   │   │   ├── http
│   │   │   │   ├── httpErrorHandler.ts
│   │   │   │   ├── httpTransport.ts
│   │   │   │   ├── httpTypes.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── mcpTransportMiddleware.ts
│   │   │   └── stdio
│   │   │       ├── index.ts
│   │   │       └── stdioTransport.ts
│   │   └── server.ts
│   ├── services
│   │   └── NCBI
│   │       ├── core
│   │       │   ├── ncbiConstants.ts
│   │       │   ├── ncbiCoreApiClient.ts
│   │       │   ├── ncbiRequestQueueManager.ts
│   │       │   ├── ncbiResponseHandler.ts
│   │       │   └── ncbiService.ts
│   │       └── parsing
│   │           ├── eSummaryResultParser.ts
│   │           ├── index.ts
│   │           ├── pubmedArticleStructureParser.ts
│   │           └── xmlGenericHelpers.ts
│   ├── types-global
│   │   ├── declarations.d.ts
│   │   ├── errors.ts
│   │   └── pubmedXml.ts
│   ├── utils
│   │   ├── internal
│   │   │   ├── errorHandler.ts
│   │   │   ├── index.ts
│   │   │   ├── logger.ts
│   │   │   ├── performance.ts
│   │   │   └── requestContext.ts
│   │   ├── metrics
│   │   │   ├── index.ts
│   │   │   └── tokenCounter.ts
│   │   ├── network
│   │   │   ├── fetchWithTimeout.ts
│   │   │   └── index.ts
│   │   ├── parsing
│   │   │   ├── dateParser.ts
│   │   │   ├── index.ts
│   │   │   └── jsonParser.ts
│   │   ├── scheduling
│   │   │   ├── index.ts
│   │   │   └── scheduler.ts
│   │   ├── security
│   │   │   ├── idGenerator.ts
│   │   │   ├── index.ts
│   │   │   ├── rateLimiter.ts
│   │   │   └── sanitization.ts
│   │   ├── telemetry
│   │   │   ├── instrumentation.ts
│   │   │   └── semconv.ts
│   │   └── index.ts
│   └── index.ts
├── .dockerignore
├── .gitignore
├── .ncurc.json
├── CHANGELOG.md
├── Dockerfile
├── eslint.config.js
├── LICENSE
├── mcp.json
├── package-lock.json
├── package.json
├── README.md
├── repomix.config.json
├── smithery.yaml
├── tsconfig.json
├── tsconfig.typedoc.json
├── tsdoc.json
└── typedoc.json
```

_Note: This tree excludes files and directories matched by .gitignore and default patterns._
