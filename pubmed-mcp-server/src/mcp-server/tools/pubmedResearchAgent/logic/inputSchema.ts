/**
 * @fileoverview Defines the Zod input schema and TypeScript types for the pubmed_research_agent tool.
 * This schema accepts detailed components of a research plan from the client,
 * which the tool will then structure into a standardized output format.
 * @module pubmedResearchAgent/logic/inputSchema
 */

import { z } from "zod";

export const PubMedResearchAgentInputSchema = z.object({
  // Overall Project Information
  project_title_suggestion: z
    .string()
    .min(5)
    .describe("A concise and descriptive title for the research project."),
  primary_research_goal: z
    .string()
    .min(10)
    .describe(
      'The main scientific objective or central question the research aims to address (e.g., "To investigate the role of TREM2 in microglial response to amyloid-beta plaques").',
    ),
  research_keywords: z
    .array(z.string().min(1))
    .min(1)
    .describe(
      'Core scientific keywords or MeSH terms defining the research domain (e.g., ["neuroinflammation", "Alzheimer\'s disease", "TREM2"]).',
    ),
  organism_focus: z
    .string()
    .optional()
    .describe(
      'Primary organism(s) or model systems (e.g., "Homo sapiens (iPSC-derived microglia)", "Mus musculus (5xFAD model)").',
    ),

  // Phase 1: Conception and Planning Inputs
  p1_introduction_and_background: z
    .string()
    .optional()
    .describe(
      "Brief overview of the research area, its significance, and relevant background information leading to this study.",
    ),
  p1_specific_research_question: z
    .string()
    .optional()
    .describe(
      "The precise, focused primary research question the study will answer.",
    ),
  p1_knowledge_gap: z
    .string()
    .optional()
    .describe(
      "Statement clearly identifying the specific gap in current knowledge this research addresses.",
    ),
  p1_primary_hypothesis: z
    .string()
    .optional()
    .describe(
      "The main, testable hypothesis. Should be clear, specific, and falsifiable.",
    ),
  p1_secondary_questions_or_hypotheses: z
    .array(z.string())
    .optional()
    .describe("Any secondary questions or hypotheses to be explored."),
  p1_pubmed_search_strategy_description: z
    .string()
    .optional()
    .describe(
      "Description of the primary literature search strategy (e.g., for PubMed), including key terms and database considerations.",
    ),

  p1_literature_review_scope: z
    .string()
    .optional()
    .describe(
      "The defined scope for the literature review (e.g., timeframes, study types, key themes).",
    ),
  p1_lit_review_databases_and_approach: z
    .string()
    .optional()
    .describe(
      "Key databases (e.g., PubMed, EMBASE) and the search approach (e.g., iterative queries, snowballing).",
    ),

  p1_experimental_paradigm: z
    .string()
    .optional()
    .describe(
      "The overarching experimental design or study type (e.g., 'comparative multi-omics analysis', 'longitudinal cohort study').",
    ),
  p1_data_acquisition_plan_existing_data: z
    .string()
    .optional()
    .describe(
      "Strategy for identifying and retrieving relevant existing datasets (databases, data types, tools).",
    ),
  p1_data_acquisition_plan_new_data: z
    .string()
    .optional()
    .describe(
      "Plan for generating novel data (data types, experimental models, key procedures, deposition plan).",
    ),
  p1_blast_utilization_plan: z
    .string()
    .optional()
    .describe(
      "If applicable, how sequence alignment services (e.g., NCBI BLAST) will be used (purpose, programs, databases).",
    ),
  p1_controls_and_rigor: z
    .string()
    .optional()
    .describe(
      "Description of key experimental controls and measures to ensure scientific rigor and reproducibility.",
    ),
  p1_methodological_challenges_and_mitigation: z
    .string()
    .optional()
    .describe(
      "Anticipated methodological challenges and proposed mitigation strategies.",
    ),

  // Phase 2: Data Collection and Processing Inputs
  p2_data_collection_methods_wet_lab: z
    .string()
    .optional()
    .describe(
      "Specific wet-lab protocols if new data is generated (sample prep, treatments, instruments).",
    ),
  p2_data_collection_methods_dry_lab: z
    .string()
    .optional()
    .describe(
      "Execution details for data retrieval from databases (queries, tools, accessioning).",
    ),
  p2_data_preprocessing_and_qc_plan: z
    .string()
    .optional()
    .describe(
      "Pipeline for data cleaning, preprocessing (e.g., alignment, normalization), and quality control (metrics, thresholds, tools).",
    ),

  // Phase 3: Analysis and Interpretation Inputs
  p3_data_analysis_strategy: z
    .string()
    .optional()
    .describe(
      "Core statistical and computational methods to analyze data and test hypotheses (tests, software, ML models if any).",
    ),
  p3_bioinformatics_pipeline_summary: z
    .string()
    .optional()
    .describe(
      "Summary of the bioinformatics pipeline for high-throughput data analysis (tools, downstream analyses).",
    ),
  p3_results_interpretation_framework: z
    .string()
    .optional()
    .describe(
      "Framework for evaluating findings against hypotheses (statistical significance, biological relevance).",
    ),
  p3_comparison_with_literature_plan: z
    .string()
    .optional()
    .describe(
      "Strategy for contextualizing results with existing literature and addressing discrepancies.",
    ),

  // Phase 4: Dissemination and Iteration Inputs
  p4_dissemination_manuscript_plan: z
    .string()
    .optional()
    .describe(
      "Plan for manuscript preparation (core message, target journal profile, key figures).",
    ),
  p4_dissemination_data_deposition_plan: z
    .string()
    .optional()
    .describe(
      "Strategy for depositing data in public repositories (types, repositories, FAIR principles).",
    ),
  p4_peer_review_and_publication_approach: z
    .string()
    .optional()
    .describe("Approach to journal submission and addressing peer review."),
  p4_future_research_directions: z
    .string()
    .optional()
    .describe(
      "Potential next steps, new questions, or translational applications arising from the research.",
    ),

  // Cross-Cutting Considerations Inputs
  cc_record_keeping_and_data_management: z
    .string()
    .optional()
    .describe(
      "Plan for record-keeping, version control, data storage, and DMP.",
    ),
  cc_collaboration_strategy: z
    .string()
    .optional()
    .describe(
      "If applicable, strategy for collaboration, communication, roles, and authorship.",
    ),
  cc_ethical_considerations: z
    .string()
    .optional()
    .describe(
      "Ethical considerations, IRB/IACUC approval plans, data privacy, RCR training.",
    ),

  // Meta-parameter from previous iterations, still useful
  include_detailed_prompts_for_agent: z
    .boolean()
    .optional()
    .default(false) // Default to false, meaning the tool primarily structures the detailed input.
    .describe(
      "If true, the tool will add more detailed instructive prompts/guidance within the output fields for a research agent. If false (default), it will primarily structure the provided inputs with minimal additional prompting.",
    ),
});

export type PubMedResearchAgentInput = z.infer<
  typeof PubMedResearchAgentInputSchema
>;
