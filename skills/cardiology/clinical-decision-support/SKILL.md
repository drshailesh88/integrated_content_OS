# Clinical Decision Support

Generate professional clinical decision support documents with GRADE evidence grading and statistical analysis for cardiology content.

## Triggers

- User needs evidence-based treatment recommendations
- User is creating clinical guideline summaries
- User wants to analyze patient cohort data
- User needs to present evidence with GRADE grading
- User is developing clinical algorithms

## Document Types

### 1. Treatment Recommendation Reports

**Structure**:
1. Clinical question (PICO format)
2. Evidence summary
3. GRADE assessment
4. Recommendation statement
5. Implementation considerations

**GRADE Evidence Levels**:
| Grade | Certainty | Meaning |
|-------|-----------|---------|
| 1A | High | Strong recommendation, high-quality evidence |
| 1B | Moderate | Strong recommendation, moderate evidence |
| 2A | High | Weak recommendation, high-quality evidence |
| 2B | Moderate | Weak recommendation, moderate evidence |
| 2C | Low | Weak recommendation, low-quality evidence |

### 2. Patient Cohort Analysis

**Components**:
- Demographics and baseline characteristics
- Biomarker stratification
- Outcome comparisons with statistics
- Subgroup analyses
- Clinical implications

### 3. Guideline Summaries

**Elements**:
- Recommendation class (I, IIa, IIb, III)
- Level of evidence (A, B, C)
- Key supporting trials
- Clinical context
- Special populations

## Cardiology-Specific Applications

### Heart Failure Management
- GDMT optimization pathways
- Device therapy eligibility
- Risk stratification (MAGGIC, Seattle HF Model)
- Stage-based recommendations

### Coronary Artery Disease
- Revascularization decisions
- Medical therapy optimization
- Risk scores (SYNTAX, HEART, TIMI)
- Secondary prevention

### Arrhythmia Management
- Anticoagulation decisions (CHA₂DS₂-VASc)
- Rate vs rhythm control
- Device therapy indications
- Ablation candidacy

### Valvular Heart Disease
- Intervention timing
- Surgical vs transcatheter approach
- Risk assessment (STS, EuroSCORE)
- Surveillance recommendations

## Statistical Presentation

### Required Elements
- Hazard ratios with 95% CI
- Absolute risk differences
- Number needed to treat (NNT)
- P-values (exact, not just thresholds)
- Forest plots for multiple comparisons

### Survival Analysis Display
- Kaplan-Meier curves
- Number at risk tables
- Median survival with CI
- Landmark analyses if appropriate

## Evidence Synthesis Framework

### For Single Trial
1. Study design and population
2. Intervention and comparator
3. Primary endpoint results
4. Key secondary endpoints
5. Safety profile
6. Limitations
7. Clinical implications

### For Multiple Trials
1. Consistency of findings
2. Magnitude of effect across studies
3. Population differences
4. Statistical heterogeneity
5. Overall certainty assessment
6. Synthesized recommendation

## GRADE Assessment Process

### Factors That Lower Certainty
- Risk of bias (unblinded, high dropout)
- Inconsistency (heterogeneous results)
- Indirectness (surrogate outcomes, different population)
- Imprecision (wide CIs, few events)
- Publication bias

### Factors That Raise Certainty
- Large effect (RR >2 or <0.5)
- Dose-response gradient
- All plausible confounders would reduce effect

## Output Formatting

### Executive Summary (Always First)
- 3-5 key findings highlighted
- Primary recommendation
- Evidence grade
- Clinical bottom line

### Recommendation Statement Format
```
We recommend [intervention] for [population] with [condition]
to [outcome] (GRADE 1B: strong recommendation, moderate certainty).

Supporting evidence: [Key trials with effect sizes]
```

## Best Practices

1. **Specify patient population** precisely
2. **Use standardized outcome definitions** (RECIST, CTCAE, etc.)
3. **Report both relative and absolute effects**
4. **Include number at risk** for survival data
5. **Acknowledge funding sources** of cited trials
6. **Note guideline concordance/discordance**
7. **Address special populations** (elderly, renal impairment, etc.)

## NOT For

This skill is NOT for individual patient treatment decisions. For that, clinical judgment integrating patient preferences, comorbidities, and circumstances is required beyond evidence synthesis.
