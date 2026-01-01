/**
 * @fileoverview Orchestrates the generation of the research plan outline
 * by directly mapping detailed client inputs to a structured output format.
 * Omits sections/steps if no relevant input is provided.
 * @module pubmedResearchAgent/logic/planOrchestrator
 */

import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../../utils/index.js";
import type { PubMedResearchAgentInput } from "./inputSchema.js";
import type {
  CrossCuttingContent,
  Phase1Step1_1_Content,
  Phase1Step1_2_Content,
  Phase1Step1_3_Content,
  Phase2Step2_1_Content,
  Phase2Step2_2_Content,
  Phase3Step3_1_Content,
  Phase3Step3_2_Content,
  Phase4Step4_1_Content,
  Phase4Step4_2_Content,
  Phase4Step4_3_Content,
  PubMedResearchPlanGeneratedOutput,
} from "./outputTypes.js";

// Helper function to conditionally add a prompt prefix or return undefined if input is empty
function C(
  userInput: string | undefined | string[],
  refinedPromptBase?: string,
  includePrompts?: boolean,
): string | undefined {
  if (!userInput || (Array.isArray(userInput) && userInput.length === 0)) {
    return undefined;
  }
  const joinedInput = Array.isArray(userInput)
    ? userInput.join("; ")
    : userInput;
  if (includePrompts && refinedPromptBase) {
    // Embed the user's input within a more directive prompt
    return `${refinedPromptBase} Based on the provided detail: "${joinedInput}". Ensure critical evaluation and consider alternative interpretations.`;
  }
  return joinedInput;
}

// Helper to generate guidance notes
function G(notes: string[], includePrompts?: boolean): string[] | undefined {
  return includePrompts && notes.length > 0 ? notes : undefined;
}

// Helper to check if all properties of an object are undefined
function allPropertiesUndefined<T extends object>(obj: T): boolean {
  return Object.values(obj as Record<string, unknown>).every(
    (value) => value === undefined,
  );
}

// Helper function to recursively remove keys with empty object or empty array values
function removeEmptyObjectsRecursively(obj: unknown): unknown {
  // Base cases for recursion
  if (typeof obj !== "object" || obj === null) {
    return obj; // Not an object or array, return as is
  }

  if (Array.isArray(obj)) {
    // If it's an array, recurse on each element and filter out empty objects/arrays
    const newArr = obj
      .map(removeEmptyObjectsRecursively)
      .filter((item: unknown) => {
        if (item === null || item === undefined) return false;
        if (Array.isArray(item) && item.length === 0) return false; // Filter out empty arrays
        if (
          typeof item === "object" &&
          !Array.isArray(item) &&
          Object.keys(item).length === 0
        ) {
          return false; // Filter out empty objects
        }
        return true;
      });
    return newArr;
  }

  // If it's an object, create a new object with non-empty properties
  const newObj: Record<string, unknown> = {};
  const objAsRecord = obj as Record<string, unknown>;
  for (const key in objAsRecord) {
    if (Object.prototype.hasOwnProperty.call(objAsRecord, key)) {
      const value = removeEmptyObjectsRecursively(objAsRecord[key]);

      // Skip null or undefined values
      if (value === null || value === undefined) {
        continue;
      }

      // Skip empty arrays
      if (Array.isArray(value) && value.length === 0) {
        continue;
      }

      // Skip empty objects
      if (
        typeof value === "object" &&
        !Array.isArray(value) &&
        Object.keys(value).length === 0
      ) {
        continue;
      }

      // If value is not empty, add it
      newObj[key] = value;
    }
  }
  return newObj;
}

export function generateFullResearchPlanOutline(
  input: PubMedResearchAgentInput,
  parentRequestContext: RequestContext,
): PubMedResearchPlanGeneratedOutput {
  const logContext = requestContextService.createRequestContext({
    parentRequestId: parentRequestContext.requestId,
    operation: "generateFullResearchPlanOutlineLog",
    input: sanitizeInputForLogging({ input }), // Add sanitized input here
  });
  logger.debug("Generating full research plan outline.", logContext);

  const inferredGoal =
    input.primary_research_goal ||
    `to investigate the roles and mechanisms of ${input.research_keywords.join(" and ")}${input.organism_focus ? ` in ${input.organism_focus}` : ""}.`;

  const planTitle =
    input.project_title_suggestion || `Research Plan Outline: ${inferredGoal}`;
  const addPrompts = input.include_detailed_prompts_for_agent;

  const overallInstructions = `This document is a structured research plan outline, primarily assembled from detailed inputs for project: "${planTitle}". As the research agent, critically evaluate this plan. Your primary function is to fulfill the user's research request by leveraging this structured information alongside your comprehensive knowledge and all available tools (e.g., PubMed search, web search, data analysis, file operations). 
Key responsibilities:
- Synthesize information to generate scientifically sound content, analyses, or answers.
- Adapt the level of detail in your final response to precisely match the user's specific query. If a concise answer is requested, use this plan as foundational background.
- Proactively identify and address potential ambiguities, biases, or limitations in the provided plan or data.
- Ensure methodological rigor: consider controls, statistical power, reproducibility, and alternative explanations.
- If critical information is missing or ambiguities hinder robust execution, formulate specific, targeted follow-up questions for the user before proceeding with extensive investigation.
- Always prioritize accuracy, objectivity, and adherence to scientific best practices.`;

  const p1s1Content: Phase1Step1_1_Content = {
    primary_research_question: C(
      input.p1_specific_research_question,
      "Critically evaluate and refine the primary research question for clarity, focus, and feasibility",
      addPrompts,
    ),
    knowledge_gap_statement: C(
      input.p1_knowledge_gap,
      "Validate and expand on the identified knowledge gap, ensuring it's well-supported by current literature",
      addPrompts,
    ),
    primary_hypothesis: C(
      input.p1_primary_hypothesis,
      "Assess the primary hypothesis for testability, specificity, and falsifiability. Consider alternative hypotheses",
      addPrompts,
    ),
    pubmed_search_strategy: C(
      input.p1_pubmed_search_strategy_description,
      "Develop a comprehensive PubMed search strategy. Consider MeSH terms, keywords, Boolean operators, and inclusion/exclusion criteria",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Ensure the research question is SMART (Specific, Measurable, Achievable, Relevant, Time-bound).",
        "Verify the knowledge gap is current and significant.",
        "The hypothesis should directly address the research question.",
        "Consider publication type filters and date ranges for the literature search.",
      ],
      addPrompts,
    ),
  };

  const p1s2Content: Phase1Step1_2_Content = {
    literature_review_scope: C(
      input.p1_literature_review_scope,
      "Define and justify the scope of the literature review, including timeframes, study types, and key themes to investigate",
      addPrompts,
    ),
    key_databases_and_search_approach: C(
      input.p1_lit_review_databases_and_approach,
      "Detail the systematic search approach across specified databases (e.g., PubMed, EMBASE, Scopus). Include strategy for citation searching or snowballing",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Document search queries and results for reproducibility.",
        "Consider using reference management software.",
        "Plan for screening and selection of articles based on predefined criteria.",
      ],
      addPrompts,
    ),
  };

  const p1s3Content: Phase1Step1_3_Content = {
    experimental_paradigm: C(
      input.p1_experimental_paradigm,
      "Elaborate on the chosen experimental paradigm, justifying its appropriateness for testing the hypothesis",
      addPrompts,
    ),
    data_acquisition_plan_existing_data: C(
      input.p1_data_acquisition_plan_existing_data,
      "Strategize the identification, retrieval, and validation of relevant existing datasets. Specify databases, data types, and access protocols",
      addPrompts,
    ),
    data_acquisition_plan_new_data: C(
      input.p1_data_acquisition_plan_new_data,
      "Outline the plan for generating novel data, including experimental models, key procedures, sample size considerations, and data deposition strategy",
      addPrompts,
    ),
    blast_utilization_plan: C(
      input.p1_blast_utilization_plan,
      "Specify how sequence alignment tools (e.g., NCBI BLAST) will be employed, including purpose, programs, databases, and interpretation of results",
      addPrompts,
    ),
    controls_and_rigor_measures: C(
      input.p1_controls_and_rigor,
      "Detail crucial experimental controls (positive, negative, internal) and measures to ensure scientific rigor, reproducibility, and minimization of bias",
      addPrompts,
    ),
    methodological_challenges_and_mitigation: C(
      input.p1_methodological_challenges_and_mitigation,
      "Anticipate potential methodological challenges, their impact, and robust mitigation strategies",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Ensure sample sizes are adequately powered.",
        "Consider blinding and randomization where appropriate.",
        "Define clear endpoints and outcome measures.",
        "Address potential confounders in the experimental design.",
      ],
      addPrompts,
    ),
  };

  const p2s1Content: Phase2Step2_1_Content = {
    data_collection_methods_wet_lab: C(
      input.p2_data_collection_methods_wet_lab,
      "Provide detailed wet-lab protocols, including sample preparation, experimental treatments, instrument settings, and data recording procedures",
      addPrompts,
    ),
    data_collection_methods_dry_lab: C(
      input.p2_data_collection_methods_dry_lab,
      "Specify execution details for computational data retrieval, including precise queries, API usage, versioning of tools, and data provenance tracking",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Standardize protocols to ensure consistency.",
        "Implement robust data labeling and organization from the outset.",
        "Document any deviations from planned protocols.",
      ],
      addPrompts,
    ),
  };

  const p2s2Content: Phase2Step2_2_Content = {
    data_preprocessing_and_qc_plan: C(
      input.p2_data_preprocessing_and_qc_plan,
      "Describe the comprehensive pipeline for data cleaning, normalization, transformation, and quality control. Specify metrics, thresholds, and tools for each step",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Define criteria for outlier detection and handling.",
        "Assess data quality before and after preprocessing.",
        "Ensure preprocessing steps are appropriate for downstream analyses.",
      ],
      addPrompts,
    ),
  };

  const p3s1Content: Phase3Step3_1_Content = {
    data_analysis_strategy: C(
      input.p3_data_analysis_strategy,
      "Outline the core statistical and computational methods for data analysis. Specify tests, software, parameters, and how they address the hypotheses",
      addPrompts,
    ),
    bioinformatics_pipeline_summary: C(
      input.p3_bioinformatics_pipeline_summary,
      "Summarize the bioinformatics pipeline for high-throughput data, detailing tools, algorithms, parameter settings, and workflow for downstream analyses",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Justify the choice of statistical tests based on data distribution and assumptions.",
        "Address multiple testing corrections if applicable.",
        "Consider sensitivity analyses to assess robustness of findings.",
      ],
      addPrompts,
    ),
  };

  const p3s2Content: Phase3Step3_2_Content = {
    results_interpretation_framework: C(
      input.p3_results_interpretation_framework,
      "Establish a clear framework for interpreting analytical findings in the context of the hypotheses, considering statistical significance, effect sizes, and biological relevance",
      addPrompts,
    ),
    comparison_with_literature_plan: C(
      input.p3_comparison_with_literature_plan,
      "Develop a strategy for systematically contextualizing results with existing literature, addressing consistencies, discrepancies, and novel contributions",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Distinguish correlation from causation.",
        "Acknowledge limitations of the study and their impact on interpretation.",
        "Discuss clinical or translational implications if relevant.",
      ],
      addPrompts,
    ),
  };

  const p4s1Content: Phase4Step4_1_Content = {
    dissemination_manuscript_plan: C(
      input.p4_dissemination_manuscript_plan,
      "Formulate a plan for manuscript preparation, including core message, target journal profile, key figures/tables, and authorship contributions",
      addPrompts,
    ),
    dissemination_data_deposition_plan: C(
      input.p4_dissemination_data_deposition_plan,
      "Outline a strategy for depositing research data in public repositories, specifying data types, repository choices, metadata standards, and adherence to FAIR principles",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Follow journal-specific author guidelines.",
        "Ensure data is de-identified if it contains sensitive information.",
        "Obtain DOIs or accession numbers for deposited data.",
      ],
      addPrompts,
    ),
  };

  const p4s2Content: Phase4Step4_2_Content = {
    peer_review_and_publication_approach: C(
      input.p4_peer_review_and_publication_approach,
      "Describe the approach to journal submission, navigating peer review, and addressing reviewer comments constructively for publication",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Prepare a compelling cover letter.",
        "Respond to reviewer comments point-by-point and respectfully.",
        "Consider pre-print servers for early dissemination.",
      ],
      addPrompts,
    ),
  };

  const p4s3Content: Phase4Step4_3_Content = {
    future_research_directions: C(
      input.p4_future_research_directions,
      "Identify and articulate potential next steps, new research questions, or translational applications arising from the current study's findings and limitations",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Base future directions on the study's actual outcomes.",
        "Consider how new technologies or approaches could address remaining questions.",
      ],
      addPrompts,
    ),
  };

  const ccContent: CrossCuttingContent = {
    record_keeping_and_data_management: C(
      input.cc_record_keeping_and_data_management,
      "Detail the comprehensive plan for meticulous record-keeping, version control (code, data, manuscripts), secure data storage, backup strategy, and Data Management Plan (DMP) adherence",
      addPrompts,
    ),
    collaboration_strategy: C(
      input.cc_collaboration_strategy,
      "If applicable, describe the strategy for effective collaboration, including communication channels, role delineation, data sharing protocols, and authorship agreements",
      addPrompts,
    ),
    ethical_considerations: C(
      input.cc_ethical_considerations,
      "Thoroughly outline all ethical considerations, including plans for IRB/IACUC approval, informed consent, data privacy/anonymization, responsible conduct of research (RCR) training, and conflict of interest management",
      addPrompts,
    ),
    guidance_notes: G(
      [
        "Ensure compliance with institutional and funding agency requirements.",
        "Regularly review and update the DMP.",
        "Promote open science practices where appropriate.",
      ],
      addPrompts,
    ),
  };

  const plan = {
    plan_title: planTitle,
    overall_instructions_for_research_agent: addPrompts
      ? overallInstructions
      : undefined,
    input_summary: {
      keywords_received: input.research_keywords,
      primary_goal_stated_or_inferred: inferredGoal,
      organism_focus: input.organism_focus || "Not Specified",
      // Correctly use the input flag name
      included_detailed_prompts_for_agent:
        input.include_detailed_prompts_for_agent,
    },
    phase_1_conception_and_planning: {
      title: "Phase 1: Conception and Planning",
      step_1_1_research_question_and_hypothesis: allPropertiesUndefined(
        p1s1Content,
      )
        ? {}
        : p1s1Content,
      step_1_2_literature_review_strategy: allPropertiesUndefined(p1s2Content)
        ? {}
        : p1s2Content,
      step_1_3_experimental_design_and_data_acquisition: allPropertiesUndefined(
        p1s3Content,
      )
        ? {}
        : p1s3Content,
    },
    phase_2_data_collection_and_processing: {
      title: "Phase 2: Data Collection and Processing",
      step_2_1_data_collection_retrieval: allPropertiesUndefined(p2s1Content)
        ? {}
        : p2s1Content,
      step_2_2_data_preprocessing_and_qc: allPropertiesUndefined(p2s2Content)
        ? {}
        : p2s2Content,
    },
    phase_3_analysis_and_interpretation: {
      title: "Phase 3: Analysis and Interpretation",
      step_3_1_data_analysis_plan: allPropertiesUndefined(p3s1Content)
        ? {}
        : p3s1Content,
      step_3_2_results_interpretation: allPropertiesUndefined(p3s2Content)
        ? {}
        : p3s2Content,
    },
    phase_4_dissemination_and_iteration: {
      title: "Phase 4: Dissemination and Iteration",
      step_4_1_dissemination_strategy: allPropertiesUndefined(p4s1Content)
        ? {}
        : p4s1Content,
      step_4_2_peer_review_and_publication: allPropertiesUndefined(p4s2Content)
        ? {}
        : p4s2Content,
      step_4_3_further_research_and_iteration: allPropertiesUndefined(
        p4s3Content,
      )
        ? {}
        : p4s3Content,
    },
    cross_cutting_considerations: {
      title: "Cross-Cutting Considerations",
      content: allPropertiesUndefined(ccContent) ? {} : ccContent,
    },
  };

  return removeEmptyObjectsRecursively(
    plan,
  ) as PubMedResearchPlanGeneratedOutput;
}
