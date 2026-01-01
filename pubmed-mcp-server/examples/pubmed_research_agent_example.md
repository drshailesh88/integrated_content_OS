Tool Call Arguments:

```json
{
  "project_title_suggestion": "Investigating the Role of TREM2 Variants in Microglial Activation and Amyloid-beta Clearance in Alzheimer's Disease Pathogenesis",
  "primary_research_goal": "To determine how specific TREM2 genetic variants affect microglial phagocytic capacity for amyloid-beta and subsequent inflammatory responses in the context of Alzheimer's Disease.",
  "research_keywords": [
    "Alzheimer's Disease",
    "TREM2",
    "Microglia",
    "Neuroinflammation",
    "Amyloid-beta",
    "Genetic Variants",
    "Phagocytosis"
  ],
  "organism_focus": "Human iPSC-derived microglia (from patients with different TREM2 genotypes) and Mus musculus (transgenic AD models with human TREM2 knock-in)",
  "p1_introduction_and_background": "Alzheimer's disease (AD) is a progressive neurodegenerative disorder. Genome-wide association studies (GWAS) have identified variants in the Triggering Receptor Expressed on Myeloid cells 2 (TREM2) gene as significant risk factors for late-onset AD. TREM2 is expressed on microglia, the brain's resident immune cells, and plays a crucial role in microglial activation, survival, proliferation, and phagocytosis. Understanding how AD-associated TREM2 variants impair these functions is critical for developing targeted therapies.",
  "p1_specific_research_question": "How do specific AD-associated TREM2 variants (e.g., R47H, R62H, D87N) alter microglial phagocytosis of amyloid-beta (A&#x3b2;) oligomers and fibrils, and modulate subsequent pro-inflammatory and anti-inflammatory cytokine release profiles compared to common TREM2 variants?",
  "p1_knowledge_gap": "While TREM2's role in AD is established, the precise molecular mechanisms by which different AD-risk variants differentially affect microglial A&#x3b2; clearance and inflammatory signaling remain incompletely understood, particularly in human-relevant cellular models.",
  "p1_primary_hypothesis": "AD-associated TREM2 risk variants (R47H, R62H, D87N) will exhibit reduced A&#x3b2; phagocytic capacity and a skewed pro-inflammatory cytokine profile in human iPSC-derived microglia upon A&#x3b2; stimulation, compared to the common TREM2 variant.",
  "p1_secondary_questions_or_hypotheses": [
    "Do TREM2 variants affect microglial lipid metabolism, and does this correlate with phagocytic defects?",
    "How do TREM2 variants influence microglial transcriptional signatures in response to A&#x3b2; (e.g., DAM signature)?",
    "Can TREM2 agonistic antibodies rescue phagocytic defects observed in risk-variant expressing microglia?"
  ],
  "p1_pubmed_search_strategy_description": "Systematic search of PubMed using MeSH terms and keywords: ('TREM2' OR 'Triggering Receptor Expressed on Myeloid cells 2') AND ('Alzheimer Disease' OR 'AD') AND ('microglia' OR 'microglial cells') AND ('amyloid beta-peptides' OR 'Abeta' OR 'amyloid plaques') AND ('genetic variation' OR 'polymorphism, single nucleotide' OR 'mutation') AND ('phagocytosis' OR 'inflammation' OR 'cytokines'). Filters: English language, last 10 years.",
  "p1_literature_review_scope": "Focus on studies investigating TREM2 function in microglia, impact of AD-associated TREM2 variants, mechanisms of A&#x3b2; clearance, and microglial inflammatory responses in AD. Include both in vitro and in vivo studies.",
  "p1_lit_review_databases_and_approach": "Primary: PubMed. Secondary: Scopus, Web of Science. Approach: Initial broad search followed by iterative refinement. Snowballing from key review articles and highly cited papers. Critical appraisal of methodologies and findings.",
  "p1_experimental_paradigm": "Comparative functional genomics study using human iPSC-derived microglia carrying different TREM2 variants and corresponding transgenic mouse models.",
  "p1_data_acquisition_plan_existing_data": "Retrieve publicly available RNA-seq/scRNA-seq datasets of human AD brain tissue and TREM2 variant mouse models from GEO/ArrayExpress to correlate in vitro findings with in vivo expression patterns. Utilize ADNI database for clinical correlations if applicable.",
  "p1_data_acquisition_plan_new_data": "Generate human iPSC lines from AD patients with known TREM2 genotypes (R47H, R62H, D87N, common variant) and differentiate into microglia. Perform A&#x3b2; phagocytosis assays, cytokine profiling (Luminex/ELISA), RNA-seq, and lipidomics. In vivo: Utilize TREM2-R47H knock-in mice crossed with 5xFAD model for behavioral, immunohistochemical, and biochemical analyses.",
  "p1_blast_utilization_plan": "Verify TREM2 variant sequences in generated iPSC lines and mouse models. Analyze TREM2 orthologs across species if comparative studies are needed.",
  "p1_controls_and_rigor": "Isogenic iPSC lines as controls where possible. Age- and sex-matched littermate controls for mouse studies. Blinding for behavioral and immunohistochemical analyses. Multiple biological and technical replicates. Statistical power analysis.",
  "p1_methodological_challenges_and_mitigation": "Challenge: Variability in iPSC differentiation. Mitigation: Standardized protocols, multiple clones per genotype, rigorous quality control of differentiated microglia. Challenge: Off-target effects of CRISPR editing. Mitigation: Whole-genome sequencing of edited lines.",
  "p2_data_collection_methods_wet_lab": "iPSC culture and differentiation, CRISPR/Cas9 gene editing, flow cytometry for phagocytosis, Luminex/ELISA for cytokines, RNA extraction and library preparation for RNA-seq, lipid extraction for mass spectrometry. Mouse behavioral testing (Morris water maze, Y-maze), tissue collection, immunohistochemistry, Western blotting.",
  "p2_data_collection_methods_dry_lab": "Data retrieval from GEO/ArrayExpress using their respective APIs/web interfaces. Accessioning of all generated high-throughput data.",
  "p2_data_preprocessing_and_qc_plan": "RNA-seq: FastQC, Trimmomatic, STAR alignment, featureCounts. scRNA-seq: Cell Ranger, Seurat/Scanpy for QC and normalization. Lipidomics: XCMS/MZmine for peak picking and alignment. Rigorous QC metrics at each step.",
  "p3_data_analysis_strategy": "Differential gene expression analysis (DESeq2/edgeR). Pathway analysis (GSEA, IPA). Statistical tests: ANOVA, t-tests with appropriate corrections for multiple comparisons. Machine learning for integrating multi-omics data if applicable.",
  "p3_bioinformatics_pipeline_summary": "Custom scripts (R/Python) integrating standard bioinformatics tools for RNA-seq, scRNA-seq, and lipidomics data. Visualization using ggplot2, Seurat, custom plotting.",
  "p3_results_interpretation_framework": "Evaluate findings against primary and secondary hypotheses. Assess statistical significance (p < 0.05) and biological relevance (effect size, pathway enrichment). Correlate in vitro findings with in vivo data and existing literature.",
  "p3_comparison_with_literature_plan": "Systematically compare results with published studies on TREM2 variants and AD. Discuss consistencies and discrepancies, potential reasons for differences (model systems, methodologies).",
  "p4_dissemination_manuscript_plan": "Core message: TREM2 risk variants impair microglial A&#x3b2; clearance and promote detrimental neuroinflammation. Target journals: Nature Neuroscience, Cell, Neuron, Immunity. Key figures: Phagocytosis assays, cytokine profiles, RNA-seq heatmaps/volcano plots, in vivo pathology.",
  "p4_dissemination_data_deposition_plan": "Deposit all raw and processed high-throughput sequencing data in GEO. Share iPSC lines and mouse models through appropriate repositories (e.g., WiCell, JAX). Adhere to FAIR data principles.",
  "p4_peer_review_and_publication_approach": "Submit to target journal, respond thoroughly to reviewer comments. Consider preprint server (bioRxiv) prior to peer-reviewed publication.",
  "p4_future_research_directions": "Investigate downstream signaling pathways affected by TREM2 variants. Explore therapeutic potential of TREM2 agonists in variant-specific contexts. Assess impact of TREM2 variants on other microglial functions (e.g., synaptic pruning).",
  "cc_record_keeping_and_data_management": "Electronic lab notebook (ELN) for experimental records. Version control (Git/GitHub) for code and analysis scripts. Secure, backed-up server for raw and processed data. Data Management Plan (DMP) as per funding agency requirements.",
  "cc_collaboration_strategy": "Collaborate with iPSC core facility for cell line generation, genomics core for sequencing, and biostatistics core for complex data analysis. Regular meetings and shared data platforms.",
  "cc_ethical_considerations": "Human iPSC work approved by Institutional Review Board (IRB). Animal studies approved by Institutional Animal Care and Use Committee (IACUC). Adherence to ARRIVE guidelines for animal research. Data de-identification where applicable. Responsible Conduct of Research (RCR) training for all personnel.",
  "include_detailed_prompts_for_agent": true
}
```

Tool Response:

```json
{
  "plan_title": "Investigating the Role of TREM2 Variants in Microglial Activation and Amyloid-beta Clearance in Alzheimer's Disease Pathogenesis",
  "overall_instructions_for_research_agent": "This document is a structured research plan outline, primarily assembled from detailed inputs for project: \"Investigating the Role of TREM2 Variants in Microglial Activation and Amyloid-beta Clearance in Alzheimer's Disease Pathogenesis\". As the research agent, critically evaluate this plan. Your primary function is to fulfill the user's research request by leveraging this structured information alongside your comprehensive knowledge and all available tools (e.g., PubMed search, web search, data analysis, file operations). \nKey responsibilities:\n- Synthesize information to generate scientifically sound content, analyses, or answers.\n- Adapt the level of detail in your final response to precisely match the user's specific query. If a concise answer is requested, use this plan as foundational background.\n- Proactively identify and address potential ambiguities, biases, or limitations in the provided plan or data.\n- Ensure methodological rigor: consider controls, statistical power, reproducibility, and alternative explanations.\n- If critical information is missing or ambiguities hinder robust execution, formulate specific, targeted follow-up questions for the user before proceeding with extensive investigation.\n- Always prioritize accuracy, objectivity, and adherence to scientific best practices.",
  "input_summary": {
    "keywords_received": [
      "Alzheimer's Disease",
      "TREM2",
      "Microglia",
      "Neuroinflammation",
      "Amyloid-beta",
      "Genetic Variants",
      "Phagocytosis"
    ],
    "primary_goal_stated_or_inferred": "To determine how specific TREM2 genetic variants affect microglial phagocytic capacity for amyloid-beta and subsequent inflammatory responses in the context of Alzheimer's Disease.",
    "organism_focus": "Human iPSC-derived microglia (from patients with different TREM2 genotypes) and Mus musculus (transgenic AD models with human TREM2 knock-in)",
    "included_detailed_prompts_for_agent": true
  },
  "phase_1_conception_and_planning": {
    "title": "Phase 1: Conception and Planning",
    "step_1_1_research_question_and_hypothesis": {
      "primary_research_question": "Critically evaluate and refine the primary research question for clarity, focus, and feasibility Based on the provided detail: \"How do specific AD-associated TREM2 variants (e.g., R47H, R62H, D87N) alter microglial phagocytosis of amyloid-beta (A&#x3b2;) oligomers and fibrils, and modulate subsequent pro-inflammatory and anti-inflammatory cytokine release profiles compared to common TREM2 variants?\". Ensure critical evaluation and consider alternative interpretations.",
      "knowledge_gap_statement": "Validate and expand on the identified knowledge gap, ensuring it's well-supported by current literature Based on the provided detail: \"While TREM2's role in AD is established, the precise molecular mechanisms by which different AD-risk variants differentially affect microglial A&#x3b2; clearance and inflammatory signaling remain incompletely understood, particularly in human-relevant cellular models.\". Ensure critical evaluation and consider alternative interpretations.",
      "primary_hypothesis": "Assess the primary hypothesis for testability, specificity, and falsifiability. Consider alternative hypotheses Based on the provided detail: \"AD-associated TREM2 risk variants (R47H, R62H, D87N) will exhibit reduced A&#x3b2; phagocytic capacity and a skewed pro-inflammatory cytokine profile in human iPSC-derived microglia upon A&#x3b2; stimulation, compared to the common TREM2 variant.\". Ensure critical evaluation and consider alternative interpretations.",
      "pubmed_search_strategy": "Develop a comprehensive PubMed search strategy. Consider MeSH terms, keywords, Boolean operators, and inclusion/exclusion criteria Based on the provided detail: \"Systematic search of PubMed using MeSH terms and keywords: ('TREM2' OR 'Triggering Receptor Expressed on Myeloid cells 2') AND ('Alzheimer Disease' OR 'AD') AND ('microglia' OR 'microglial cells') AND ('amyloid beta-peptides' OR 'Abeta' OR 'amyloid plaques') AND ('genetic variation' OR 'polymorphism, single nucleotide' OR 'mutation') AND ('phagocytosis' OR 'inflammation' OR 'cytokines'). Filters: English language, last 10 years.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Ensure the research question is SMART (Specific, Measurable, Achievable, Relevant, Time-bound).",
        "Verify the knowledge gap is current and significant.",
        "The hypothesis should directly address the research question.",
        "Consider publication type filters and date ranges for the literature search."
      ]
    },
    "step_1_2_literature_review_strategy": {
      "literature_review_scope": "Define and justify the scope of the literature review, including timeframes, study types, and key themes to investigate Based on the provided detail: \"Focus on studies investigating TREM2 function in microglia, impact of AD-associated TREM2 variants, mechanisms of A&#x3b2; clearance, and microglial inflammatory responses in AD. Include both in vitro and in vivo studies.\". Ensure critical evaluation and consider alternative interpretations.",
      "key_databases_and_search_approach": "Detail the systematic search approach across specified databases (e.g., PubMed, EMBASE, Scopus). Include strategy for citation searching or snowballing Based on the provided detail: \"Primary: PubMed. Secondary: Scopus, Web of Science. Approach: Initial broad search followed by iterative refinement. Snowballing from key review articles and highly cited papers. Critical appraisal of methodologies and findings.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Document search queries and results for reproducibility.",
        "Consider using reference management software.",
        "Plan for screening and selection of articles based on predefined criteria."
      ]
    },
    "step_1_3_experimental_design_and_data_acquisition": {
      "experimental_paradigm": "Elaborate on the chosen experimental paradigm, justifying its appropriateness for testing the hypothesis Based on the provided detail: \"Comparative functional genomics study using human iPSC-derived microglia carrying different TREM2 variants and corresponding transgenic mouse models.\". Ensure critical evaluation and consider alternative interpretations.",
      "data_acquisition_plan_existing_data": "Strategize the identification, retrieval, and validation of relevant existing datasets. Specify databases, data types, and access protocols Based on the provided detail: \"Retrieve publicly available RNA-seq/scRNA-seq datasets of human AD brain tissue and TREM2 variant mouse models from GEO/ArrayExpress to correlate in vitro findings with in vivo expression patterns. Utilize ADNI database for clinical correlations if applicable.\". Ensure critical evaluation and consider alternative interpretations.",
      "data_acquisition_plan_new_data": "Outline the plan for generating novel data, including experimental models, key procedures, sample size considerations, and data deposition strategy Based on the provided detail: \"Generate human iPSC lines from AD patients with known TREM2 genotypes (R47H, R62H, D87N, common variant) and differentiate into microglia. Perform A&#x3b2; phagocytosis assays, cytokine profiling (Luminex/ELISA), RNA-seq, and lipidomics. In vivo: Utilize TREM2-R47H knock-in mice crossed with 5xFAD model for behavioral, immunohistochemical, and biochemical analyses.\". Ensure critical evaluation and consider alternative interpretations.",
      "blast_utilization_plan": "Specify how sequence alignment tools (e.g., NCBI BLAST) will be employed, including purpose, programs, databases, and interpretation of results Based on the provided detail: \"Verify TREM2 variant sequences in generated iPSC lines and mouse models. Analyze TREM2 orthologs across species if comparative studies are needed.\". Ensure critical evaluation and consider alternative interpretations.",
      "controls_and_rigor_measures": "Detail crucial experimental controls (positive, negative, internal) and measures to ensure scientific rigor, reproducibility, and minimization of bias Based on the provided detail: \"Isogenic iPSC lines as controls where possible. Age- and sex-matched littermate controls for mouse studies. Blinding for behavioral and immunohistochemical analyses. Multiple biological and technical replicates. Statistical power analysis.\". Ensure critical evaluation and consider alternative interpretations.",
      "methodological_challenges_and_mitigation": "Anticipate potential methodological challenges, their impact, and robust mitigation strategies Based on the provided detail: \"Challenge: Variability in iPSC differentiation. Mitigation: Standardized protocols, multiple clones per genotype, rigorous quality control of differentiated microglia. Challenge: Off-target effects of CRISPR editing. Mitigation: Whole-genome sequencing of edited lines.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Ensure sample sizes are adequately powered.",
        "Consider blinding and randomization where appropriate.",
        "Define clear endpoints and outcome measures.",
        "Address potential confounders in the experimental design."
      ]
    }
  },
  "phase_2_data_collection_and_processing": {
    "title": "Phase 2: Data Collection and Processing",
    "step_2_1_data_collection_retrieval": {
      "data_collection_methods_wet_lab": "Provide detailed wet-lab protocols, including sample preparation, experimental treatments, instrument settings, and data recording procedures Based on the provided detail: \"iPSC culture and differentiation, CRISPR/Cas9 gene editing, flow cytometry for phagocytosis, Luminex/ELISA for cytokines, RNA extraction and library preparation for RNA-seq, lipid extraction for mass spectrometry. Mouse behavioral testing (Morris water maze, Y-maze), tissue collection, immunohistochemistry, Western blotting.\". Ensure critical evaluation and consider alternative interpretations.",
      "data_collection_methods_dry_lab": "Specify execution details for computational data retrieval, including precise queries, API usage, versioning of tools, and data provenance tracking Based on the provided detail: \"Data retrieval from GEO/ArrayExpress using their respective APIs/web interfaces. Accessioning of all generated high-throughput data.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Standardize protocols to ensure consistency.",
        "Implement robust data labeling and organization from the outset.",
        "Document any deviations from planned protocols."
      ]
    },
    "step_2_2_data_preprocessing_and_qc": {
      "data_preprocessing_and_qc_plan": "Describe the comprehensive pipeline for data cleaning, normalization, transformation, and quality control. Specify metrics, thresholds, and tools for each step Based on the provided detail: \"RNA-seq: FastQC, Trimmomatic, STAR alignment, featureCounts. scRNA-seq: Cell Ranger, Seurat/Scanpy for QC and normalization. Lipidomics: XCMS/MZmine for peak picking and alignment. Rigorous QC metrics at each step.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Define criteria for outlier detection and handling.",
        "Assess data quality before and after preprocessing.",
        "Ensure preprocessing steps are appropriate for downstream analyses."
      ]
    }
  },
  "phase_3_analysis_and_interpretation": {
    "title": "Phase 3: Analysis and Interpretation",
    "step_3_1_data_analysis_plan": {
      "data_analysis_strategy": "Outline the core statistical and computational methods for data analysis. Specify tests, software, parameters, and how they address the hypotheses Based on the provided detail: \"Differential gene expression analysis (DESeq2/edgeR). Pathway analysis (GSEA, IPA). Statistical tests: ANOVA, t-tests with appropriate corrections for multiple comparisons. Machine learning for integrating multi-omics data if applicable.\". Ensure critical evaluation and consider alternative interpretations.",
      "bioinformatics_pipeline_summary": "Summarize the bioinformatics pipeline for high-throughput data, detailing tools, algorithms, parameter settings, and workflow for downstream analyses Based on the provided detail: \"Custom scripts (R/Python) integrating standard bioinformatics tools for RNA-seq, scRNA-seq, and lipidomics data. Visualization using ggplot2, Seurat, custom plotting.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Justify the choice of statistical tests based on data distribution and assumptions.",
        "Address multiple testing corrections if applicable.",
        "Consider sensitivity analyses to assess robustness of findings."
      ]
    },
    "step_3_2_results_interpretation": {
      "results_interpretation_framework": "Establish a clear framework for interpreting analytical findings in the context of the hypotheses, considering statistical significance, effect sizes, and biological relevance Based on the provided detail: \"Evaluate findings against primary and secondary hypotheses. Assess statistical significance (p < 0.05) and biological relevance (effect size, pathway enrichment). Correlate in vitro findings with in vivo data and existing literature.\". Ensure critical evaluation and consider alternative interpretations.",
      "comparison_with_literature_plan": "Develop a strategy for systematically contextualizing results with existing literature, addressing consistencies, discrepancies, and novel contributions Based on the provided detail: \"Systematically compare results with published studies on TREM2 variants and AD. Discuss consistencies and discrepancies, potential reasons for differences (model systems, methodologies).\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Distinguish correlation from causation.",
        "Acknowledge limitations of the study and their impact on interpretation.",
        "Discuss clinical or translational implications if relevant."
      ]
    }
  },
  "phase_4_dissemination_and_iteration": {
    "title": "Phase 4: Dissemination and Iteration",
    "step_4_1_dissemination_strategy": {
      "dissemination_manuscript_plan": "Formulate a plan for manuscript preparation, including core message, target journal profile, key figures/tables, and authorship contributions Based on the provided detail: \"Core message: TREM2 risk variants impair microglial A&#x3b2; clearance and promote detrimental neuroinflammation. Target journals: Nature Neuroscience, Cell, Neuron, Immunity. Key figures: Phagocytosis assays, cytokine profiles, RNA-seq heatmaps/volcano plots, in vivo pathology.\". Ensure critical evaluation and consider alternative interpretations.",
      "dissemination_data_deposition_plan": "Outline a strategy for depositing research data in public repositories, specifying data types, repository choices, metadata standards, and adherence to FAIR principles Based on the provided detail: \"Deposit all raw and processed high-throughput sequencing data in GEO. Share iPSC lines and mouse models through appropriate repositories (e.g., WiCell, JAX). Adhere to FAIR data principles.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Follow journal-specific author guidelines.",
        "Ensure data is de-identified if it contains sensitive information.",
        "Obtain DOIs or accession numbers for deposited data."
      ]
    },
    "step_4_2_peer_review_and_publication": {
      "peer_review_and_publication_approach": "Describe the approach to journal submission, navigating peer review, and addressing reviewer comments constructively for publication Based on the provided detail: \"Submit to target journal, respond thoroughly to reviewer comments. Consider preprint server (bioRxiv) prior to peer-reviewed publication.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Prepare a compelling cover letter.",
        "Respond to reviewer comments point-by-point and respectfully.",
        "Consider pre-print servers for early dissemination."
      ]
    },
    "step_4_3_further_research_and_iteration": {
      "future_research_directions": "Identify and articulate potential next steps, new research questions, or translational applications arising from the current study's findings and limitations Based on the provided detail: \"Investigate downstream signaling pathways affected by TREM2 variants. Explore therapeutic potential of TREM2 agonists in variant-specific contexts. Assess impact of TREM2 variants on other microglial functions (e.g., synaptic pruning).\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Base future directions on the study's actual outcomes.",
        "Consider how new technologies or approaches could address remaining questions."
      ]
    }
  },
  "cross_cutting_considerations": {
    "title": "Cross-Cutting Considerations",
    "content": {
      "record_keeping_and_data_management": "Detail the comprehensive plan for meticulous record-keeping, version control (code, data, manuscripts), secure data storage, backup strategy, and Data Management Plan (DMP) adherence Based on the provided detail: \"Electronic lab notebook (ELN) for experimental records. Version control (Git/GitHub) for code and analysis scripts. Secure, backed-up server for raw and processed data. Data Management Plan (DMP) as per funding agency requirements.\". Ensure critical evaluation and consider alternative interpretations.",
      "collaboration_strategy": "If applicable, describe the strategy for effective collaboration, including communication channels, role delineation, data sharing protocols, and authorship agreements Based on the provided detail: \"Collaborate with iPSC core facility for cell line generation, genomics core for sequencing, and biostatistics core for complex data analysis. Regular meetings and shared data platforms.\". Ensure critical evaluation and consider alternative interpretations.",
      "ethical_considerations": "Thoroughly outline all ethical considerations, including plans for IRB/IACUC approval, informed consent, data privacy/anonymization, responsible conduct of research (RCR) training, and conflict of interest management Based on the provided detail: \"Human iPSC work approved by Institutional Review Board (IRB). Animal studies approved by Institutional Animal Care and Use Committee (IACUC). Adherence to ARRIVE guidelines for animal research. Data de-identification where applicable. Responsible Conduct of Research (RCR) training for all personnel.\". Ensure critical evaluation and consider alternative interpretations.",
      "guidance_notes": [
        "Ensure compliance with institutional and funding agency requirements.",
        "Regularly review and update the DMP.",
        "Promote open science practices where appropriate."
      ]
    }
  }
}
```
