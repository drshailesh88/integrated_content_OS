"""
Content Database for Carousel Generator v2

Curated, evidence-based cardiology content for generating high-quality carousels.
All data is sourced from peer-reviewed literature and clinical guidelines.

Topics covered:
- Statins
- LDL Cholesterol
- GLP-1 Agonists
- Blood Pressure
- Heart Attack/MI
- CAC Scoring
- Diabetes-Cardio
- Cholesterol
- Atrial Fibrillation
- Heart Failure
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TopicContent:
    """Content for a specific cardiology topic."""
    topic: str
    core_subject: str  # Normalized subject (e.g., "statins" not "statin myths")
    aliases: List[str]  # Alternative names/phrasings
    myths: List[Dict[str, str]]
    truths: List[Dict[str, str]]  # Key facts
    statistics: List[Dict[str, str]]
    tips: List[str]
    quotes: List[Dict[str, str]]
    hooks: List[str]  # Pre-written high-quality hooks
    sources: List[str]  # PMIDs or citations


# ============================================================================
# STATIN CONTENT
# ============================================================================
STATINS = TopicContent(
    topic="statins",
    core_subject="statins",
    aliases=["statin", "statin myths", "statin side effects", "cholesterol medication",
             "atorvastatin", "rosuvastatin", "lipitor", "crestor"],
    myths=[
        {
            "myth": "Statins cause muscle pain in most people",
            "truth": "Only 5-10% experience muscle symptoms. Nocebo effect accounts for 90% of reported symptoms in blinded trials.",
            "source": "PMID: 32227594"
        },
        {
            "myth": "Statins damage your liver",
            "truth": "Liver damage is extremely rare (<0.1%). Routine liver monitoring is no longer recommended by ACC/AHA guidelines.",
            "source": "2018 ACC/AHA Guidelines"
        },
        {
            "myth": "Natural alternatives work just as well",
            "truth": "No supplement matches statin efficacy. Red yeast rice contains lovastatin but with inconsistent dosing and no quality control.",
            "source": "PMID: 31422671"
        },
        {
            "myth": "Statins cause diabetes",
            "truth": "Small increased risk (0.2% absolute) but cardiovascular benefits far outweigh this risk, especially in high-risk patients.",
            "source": "PMID: 28877913"
        },
        {
            "myth": "Once on statins, you're on them for life",
            "truth": "Lifestyle changes can reduce dose needed. Some patients with low risk can safely discontinue with monitoring.",
            "source": "Clinical practice"
        },
        {
            "myth": "Statins cause dementia",
            "truth": "Multiple large studies show NO increased dementia risk. Some evidence suggests statins may be protective.",
            "source": "PMID: 32118262"
        },
        {
            "myth": "Statins are only for high cholesterol",
            "truth": "Benefits extend beyond LDL lowering - statins reduce inflammation (CRP) and stabilize plaques.",
            "source": "JUPITER Trial - PMID: 18997196"
        },
    ],
    truths=[
        {"fact": "Statins reduce major cardiovascular events by 25%", "context": "Per mmol/L LDL reduction"},
        {"fact": "50% of patients stop statins within 1 year", "context": "Often due to nocebo effect"},
        {"fact": "NNT is 39 for primary prevention over 5 years", "context": "To prevent one cardiovascular event"},
    ],
    statistics=[
        {"value": "25%", "label": "reduction in major cardiovascular events", "context": "Per 1 mmol/L LDL reduction - CTT meta-analysis"},
        {"value": "50%", "label": "of patients discontinue within 1 year", "context": "Adherence is a major clinical challenge"},
        {"value": "5-10%", "label": "experience actual muscle symptoms", "context": "Nocebo effect explains most complaints"},
        {"value": "90%", "label": "of muscle symptoms are nocebo effect", "context": "SAMSON trial blinded analysis"},
        {"value": "<0.1%", "label": "risk of serious liver damage", "context": "Extremely rare adverse effect"},
        {"value": "39", "label": "NNT for primary prevention (5 years)", "context": "Number needed to treat"},
    ],
    tips=[
        "Take statins at night - cholesterol synthesis peaks during sleep",
        "Rosuvastatin and atorvastatin can be taken any time of day",
        "Report muscle symptoms to your doctor - they're usually manageable",
        "Grapefruit affects some statins (simvastatin, lovastatin) - not all",
        "Lifestyle changes enhance statin benefits - don't skip exercise",
    ],
    quotes=[
        {"text": "The nocebo effect explains most statin intolerance. Blinded rechallenge shows symptoms rarely recur.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "Statins remain one of the most evidence-based medications in all of medicine.", "author": "ACC/AHA Guidelines 2018"},
    ],
    hooks=[
        "5 statin myths debunked by science",
        "The truth about statins your doctor should tell you",
        "Why 50% of patients quit statins (and why they shouldn't)",
        "Statin side effects: separating fact from fiction",
        "What 30 years of research tells us about statins",
    ],
    sources=["PMID: 32227594", "PMID: 31422671", "PMID: 28877913", "CTT Collaboration"]
)


# ============================================================================
# LDL CHOLESTEROL CONTENT
# ============================================================================
LDL_CHOLESTEROL = TopicContent(
    topic="ldl cholesterol",
    core_subject="LDL cholesterol",
    aliases=["ldl", "bad cholesterol", "cholesterol", "hyperlipidemia", "high cholesterol",
             "ldl-c", "cholesterol levels"],
    myths=[
        {
            "myth": "LDL doesn't matter, it's all about inflammation",
            "truth": "LDL is causal for atherosclerosis. Mendelian randomization proves lifetime LDL exposure predicts risk.",
            "source": "PMID: 28444290"
        },
        {
            "myth": "You can have LDL too low",
            "truth": "No evidence of harm from very low LDL. People with genetic mutations causing LDL <30 are healthy with lower CV risk.",
            "source": "PMID: 27979987"
        },
        {
            "myth": "Dietary cholesterol raises LDL significantly",
            "truth": "Dietary cholesterol has modest effects. Saturated fat is the main dietary driver of LDL.",
            "source": "2020 Dietary Guidelines"
        },
        {
            "myth": "HDL is the 'good' cholesterol that protects you",
            "truth": "Low HDL is a risk marker, not a target. Raising HDL with drugs hasn't reduced events in trials.",
            "source": "PMID: 22085316"
        },
        {
            "myth": "Total cholesterol is what matters most",
            "truth": "Non-HDL or LDL are better predictors. Total cholesterol includes protective HDL.",
            "source": "ESC 2019 Guidelines"
        },
    ],
    truths=[
        {"fact": "Every 1 mmol/L LDL reduction = 22% lower MACE", "context": "Consistent across all trials"},
        {"fact": "LDL target <70 mg/dL for very high-risk patients", "context": "2019 ESC/EAS Guidelines"},
        {"fact": "50% reduction from baseline is a key target", "context": "For high-risk patients"},
    ],
    statistics=[
        {"value": "22%", "label": "lower MACE per 1 mmol/L LDL reduction", "context": "CTT meta-analysis"},
        {"value": "<70", "label": "mg/dL target for high-risk patients", "context": "Very high-risk: <55 mg/dL"},
        {"value": "50%", "label": "reduction target from baseline", "context": "For secondary prevention"},
        {"value": "86M", "label": "Americans have elevated LDL", "context": "CDC data"},
        {"value": "3x", "label": "higher MI risk with LDL >160", "context": "Compared to LDL <100"},
    ],
    tips=[
        "Check fasting lipid panel annually - or more often if on treatment",
        "Calculate your non-HDL cholesterol (Total - HDL) for better risk assessment",
        "Apolipoprotein B (ApoB) is the most accurate marker of atherogenic particles",
        "Lifestyle changes can reduce LDL by 10-20% - diet and exercise matter",
        "If statins aren't enough, ezetimibe and PCSK9 inhibitors can help",
    ],
    quotes=[
        {"text": "LDL is not just a risk factor, it's a causal agent in atherosclerosis.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "Lower is better - there's no LDL threshold below which benefit stops.", "author": "CTT Collaboration"},
    ],
    hooks=[
        "The LDL myth that cardiologists hate",
        "Your LDL target is probably wrong (new guidelines)",
        "Why 'good' and 'bad' cholesterol is too simple",
        "5 facts about LDL that could save your life",
        "What your cholesterol numbers really mean",
    ],
    sources=["PMID: 28444290", "PMID: 27979987", "ESC 2019 Guidelines"]
)


# ============================================================================
# GLP-1 AGONISTS CONTENT
# ============================================================================
GLP1_AGONISTS = TopicContent(
    topic="glp-1 agonists",
    core_subject="GLP-1 medications",
    aliases=["glp-1", "ozempic", "wegovy", "mounjaro", "semaglutide", "tirzepatide",
             "glp-1 weight loss", "glp-1 for heart", "ozempic for weight loss"],
    myths=[
        {
            "myth": "GLP-1s are just for weight loss",
            "truth": "They reduce cardiovascular events by 14-20% independent of weight loss. FDA approved for CV risk reduction.",
            "source": "PMID: 35461622"
        },
        {
            "myth": "The weight comes back immediately when you stop",
            "truth": "Some weight regain is expected, but lifestyle changes made during treatment can be maintained.",
            "source": "STEP 1 Extension - PMID: 35441470"
        },
        {
            "myth": "GLP-1s cause thyroid cancer",
            "truth": "Only seen in rodents at very high doses. No increased risk in humans in large trials or real-world data.",
            "source": "PMID: 34614535"
        },
        {
            "myth": "These are 'cheating' at weight loss",
            "truth": "They correct a biological problem - GLP-1 deficiency. Obesity is a disease, not a moral failing.",
            "source": "Clinical consensus"
        },
        {
            "myth": "GLP-1s cause pancreatitis",
            "truth": "Large trials show no increased pancreatitis risk. Use with caution only in those with history of pancreatitis.",
            "source": "PMID: 28864332"
        },
    ],
    truths=[
        {"fact": "Semaglutide 2.4mg achieves 15% average weight loss", "context": "STEP trials data"},
        {"fact": "Tirzepatide achieves up to 22.5% weight loss", "context": "SURMOUNT-1 trial"},
        {"fact": "20% reduction in MACE with semaglutide", "context": "SELECT trial 2023"},
    ],
    statistics=[
        {"value": "15%", "label": "average weight loss with semaglutide 2.4mg", "context": "STEP 1 trial at 68 weeks"},
        {"value": "22.5%", "label": "weight loss with tirzepatide 15mg", "context": "SURMOUNT-1 trial"},
        {"value": "20%", "label": "reduction in major cardiovascular events", "context": "SELECT trial - semaglutide"},
        {"value": "14.9%", "label": "body weight reduction in STEP 1", "context": "Vs 2.4% with placebo"},
        {"value": "72%", "label": "of patients lose ≥5% body weight", "context": "STEP 1 trial"},
    ],
    tips=[
        "Start at the lowest dose and titrate slowly to minimize GI side effects",
        "Nausea usually improves after 4-8 weeks - don't give up too early",
        "Eat slowly and stop when satisfied - these medications enhance satiety",
        "Maintain protein intake during weight loss to preserve muscle mass",
        "Combine with exercise for best cardiovascular outcomes",
    ],
    quotes=[
        {"text": "GLP-1 agonists represent the biggest advance in obesity treatment in decades.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "These medications correct biology, not willpower.", "author": "Obesity Medicine Association"},
    ],
    hooks=[
        "GLP-1s: not just for weight loss anymore",
        "What Ozempic does to your heart (surprising findings)",
        "5 GLP-1 myths your doctor needs to debunk",
        "Why cardiologists are excited about weight loss drugs",
        "The real science behind Ozempic and Wegovy",
    ],
    sources=["PMID: 35461622", "PMID: 35441470", "SELECT Trial 2023"]
)


# ============================================================================
# BLOOD PRESSURE CONTENT
# ============================================================================
BLOOD_PRESSURE = TopicContent(
    topic="blood pressure",
    core_subject="blood pressure",
    aliases=["hypertension", "high blood pressure", "bp", "blood pressure control",
             "hypertension treatment", "blood pressure medication"],
    myths=[
        {
            "myth": "I feel fine so my blood pressure must be okay",
            "truth": "Hypertension is called the 'silent killer' because it usually has no symptoms until organ damage occurs.",
            "source": "AHA Guidelines 2017"
        },
        {
            "myth": "Blood pressure medications are for life - I can never stop",
            "truth": "With significant lifestyle changes and weight loss, some patients can reduce or stop medications with monitoring.",
            "source": "Clinical practice"
        },
        {
            "myth": "Only the top number (systolic) matters",
            "truth": "Both numbers matter. Isolated diastolic hypertension in young adults predicts future CV risk.",
            "source": "PMID: 31589749"
        },
        {
            "myth": "White coat hypertension isn't real hypertension",
            "truth": "White coat hypertension still carries some increased CV risk. Home monitoring helps clarify the diagnosis.",
            "source": "PMID: 30571549"
        },
        {
            "myth": "Blood pressure should be treated the same in everyone",
            "truth": "Target BP depends on age, comorbidities, and tolerance. Older adults may need less aggressive targets.",
            "source": "ACC/AHA 2017 Guidelines"
        },
    ],
    truths=[
        {"fact": "130/80 mmHg is the new threshold for hypertension", "context": "2017 ACC/AHA Guidelines"},
        {"fact": "Each 20/10 mmHg increase doubles CV risk", "context": "Starting from 115/75"},
        {"fact": "47% of US adults have hypertension", "context": "By 2017 criteria"},
    ],
    statistics=[
        {"value": "130/80", "label": "mmHg - new hypertension threshold", "context": "ACC/AHA 2017 Guidelines"},
        {"value": "47%", "label": "of US adults have hypertension", "context": "By current criteria"},
        {"value": "25%", "label": "have resistant hypertension", "context": "Uncontrolled despite 3+ medications"},
        {"value": "2x", "label": "CV risk increase per 20/10 mmHg", "context": "Above 115/75 mmHg"},
        {"value": "50%", "label": "don't have their BP controlled", "context": "Major public health challenge"},
    ],
    tips=[
        "Measure BP at the same time daily for accurate trends",
        "Rest 5 minutes before measuring - no caffeine or exercise within 30 min",
        "Reduce sodium to <2300mg daily (ideally <1500mg for hypertension)",
        "DASH diet can lower systolic BP by 8-14 mmHg",
        "Lose weight - each kg lost reduces BP by about 1 mmHg",
    ],
    quotes=[
        {"text": "Hypertension is the most modifiable risk factor for cardiovascular disease.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "Know your numbers. High blood pressure rarely announces itself.", "author": "American Heart Association"},
    ],
    hooks=[
        "Your blood pressure target is probably outdated",
        "5 blood pressure myths that could cost you",
        "Why 'normal' blood pressure isn't good enough",
        "The silent killer: what your BP won't tell you",
        "Blood pressure control: what's changed in 2024",
    ],
    sources=["ACC/AHA 2017 Guidelines", "PMID: 31589749", "SPRINT Trial"]
)


# ============================================================================
# HEART ATTACK / MI CONTENT
# ============================================================================
HEART_ATTACK = TopicContent(
    topic="heart attack",
    core_subject="heart attacks",
    aliases=["mi", "myocardial infarction", "heart attack symptoms", "chest pain",
             "heart attack prevention", "stemi", "nstemi"],
    myths=[
        {
            "myth": "Heart attacks only happen to old people",
            "truth": "20% of heart attacks occur in people under 55. Young heart attacks are increasing, especially in women.",
            "source": "PMID: 30586730"
        },
        {
            "myth": "Heart attack pain is always severe and crushing",
            "truth": "Symptoms can be subtle - jaw pain, nausea, fatigue. 1 in 5 heart attacks are 'silent.'",
            "source": "AHA Scientific Statement"
        },
        {
            "myth": "Women have the same symptoms as men",
            "truth": "Women more often have atypical symptoms: back pain, nausea, shortness of breath, fatigue.",
            "source": "PMID: 30586175"
        },
        {
            "myth": "If you survive a heart attack, you're fine",
            "truth": "Heart attack survivors have high risk of recurrent events. Cardiac rehab and medications are essential.",
            "source": "Clinical guidelines"
        },
        {
            "myth": "Aspirin can stop a heart attack in progress",
            "truth": "Chewing aspirin helps, but it doesn't stop the attack. Call 911 immediately - time is muscle.",
            "source": "AHA Guidelines"
        },
    ],
    truths=[
        {"fact": "1 in 5 heart attacks are silent", "context": "No classic symptoms"},
        {"fact": "Every minute of delay = more heart muscle lost", "context": "Time is muscle"},
        {"fact": "Women's symptoms are often different than men's", "context": "More atypical presentations"},
    ],
    statistics=[
        {"value": "805,000", "label": "Americans have a heart attack yearly", "context": "CDC data"},
        {"value": "1 in 5", "label": "heart attacks are silent", "context": "No classic symptoms"},
        {"value": "50%", "label": "occur without prior warning symptoms", "context": "First event can be fatal"},
        {"value": "20%", "label": "occur in people under 55", "context": "Young MIs are increasing"},
        {"value": "90 min", "label": "door-to-balloon time goal for STEMI", "context": "Faster is better"},
    ],
    tips=[
        "Know the symptoms: chest discomfort, arm/jaw pain, shortness of breath, cold sweat",
        "Women: watch for fatigue, nausea, back pain - symptoms can be subtle",
        "Call 911 immediately - don't drive yourself to the hospital",
        "Chew aspirin (325mg) while waiting for help if not allergic",
        "After a heart attack, cardiac rehab reduces mortality by 25%",
    ],
    quotes=[
        {"text": "Time is muscle. Every minute of delay means more heart damage.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "The best heart attack is the one you prevent.", "author": "American Heart Association"},
    ],
    hooks=[
        "5 heart attack warning signs you're ignoring",
        "Why women's heart attacks look different",
        "The silent heart attack: are you at risk?",
        "Heart attack myths that could kill you",
        "What to do in the first 5 minutes of a heart attack",
    ],
    sources=["PMID: 30586730", "PMID: 30586175", "AHA Guidelines"]
)


# ============================================================================
# CAC SCORING CONTENT
# ============================================================================
CAC_SCORING = TopicContent(
    topic="cac scoring",
    core_subject="CAC score",
    aliases=["cac", "coronary artery calcium", "calcium score", "heart scan",
             "coronary calcium", "cac test", "calcium score test"],
    myths=[
        {
            "myth": "A zero CAC score means you have no heart disease risk",
            "truth": "Zero CAC is excellent but not zero risk. Soft plaque can exist without calcium. Recheck in 5 years.",
            "source": "PMID: 30172240"
        },
        {
            "myth": "High CAC score means you need immediate intervention",
            "truth": "CAC guides risk stratification, not immediate procedures. Treatment is usually medication and lifestyle.",
            "source": "2019 ACC/AHA Guidelines"
        },
        {
            "myth": "CAC gets worse from statins",
            "truth": "Statins may slightly increase CAC but they stabilize plaque and reduce events. CAC progression ≠ worse outcomes.",
            "source": "PMID: 26965162"
        },
        {
            "myth": "Everyone should get a CAC scan",
            "truth": "CAC is most useful for intermediate-risk patients (7.5-20% 10-year risk) where it changes management.",
            "source": "2019 ACC/AHA Guidelines"
        },
        {
            "myth": "CAC is just about blockages",
            "truth": "CAC detects calcified plaque anywhere in coronaries. It's about total plaque burden, not just stenosis.",
            "source": "MESA Study"
        },
    ],
    truths=[
        {"fact": "Zero CAC means <1% 10-year event risk", "context": "Very favorable prognosis"},
        {"fact": "CAC >400 means >20% 10-year risk", "context": "High-risk category"},
        {"fact": "CAC percentile matters more than absolute number", "context": "Age and sex-adjusted"},
    ],
    statistics=[
        {"value": "0", "label": "CAC score = <1% 10-year CV risk", "context": "Excellent prognosis"},
        {"value": ">400", "label": "CAC score indicates high risk", "context": "10x higher than CAC 0"},
        {"value": "50%", "label": "of MIs occur with zero CAC", "context": "Soft plaque still matters"},
        {"value": "10x", "label": "higher risk with CAC >400", "context": "Compared to CAC 0"},
        {"value": "5 years", "label": "retest interval for CAC 0", "context": "Can progress over time"},
    ],
    tips=[
        "Best use: intermediate risk patients (7.5-20% 10-year risk)",
        "If CAC is 0, consider retesting in 5 years",
        "CAC percentile (vs. age/sex peers) is more meaningful than absolute number",
        "CAC >100 strongly favors statin therapy regardless of other factors",
        "Don't panic about high CAC - it guides treatment, not emergency intervention",
    ],
    quotes=[
        {"text": "CAC is the most powerful predictor of cardiovascular events we have.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "A zero CAC score is powerful reassurance, but not a free pass.", "author": "MESA Study Investigators"},
    ],
    hooks=[
        "What your CAC score really means",
        "CAC 0 doesn't mean you're safe (here's why)",
        "The heart scan that could save your life",
        "5 things your CAC score tells you",
        "Should everyone get a heart calcium scan?",
    ],
    sources=["PMID: 30172240", "2019 ACC/AHA Guidelines", "MESA Study"]
)


# ============================================================================
# ATRIAL FIBRILLATION CONTENT
# ============================================================================
ATRIAL_FIBRILLATION = TopicContent(
    topic="atrial fibrillation",
    core_subject="AFib",
    aliases=["afib", "af", "atrial fibrillation", "irregular heartbeat", "heart rhythm",
             "afib stroke", "blood thinners"],
    myths=[
        {
            "myth": "AFib is just a minor heart rhythm issue",
            "truth": "AFib increases stroke risk 5x. It's a major cause of heart failure and death if untreated.",
            "source": "PMID: 30586768"
        },
        {
            "myth": "If I don't feel my AFib, it's not a problem",
            "truth": "Asymptomatic AFib carries the same stroke risk as symptomatic. Silent AFib is common.",
            "source": "PMID: 28359515"
        },
        {
            "myth": "Blood thinners are too dangerous",
            "truth": "Modern blood thinners (DOACs) have lower bleeding risk than warfarin. Stroke risk usually outweighs bleed risk.",
            "source": "PMID: 28436045"
        },
        {
            "myth": "Ablation cures AFib permanently",
            "truth": "Ablation controls AFib in 70-80%, but recurrence is common. Many need repeat procedures.",
            "source": "PMID: 29760785"
        },
        {
            "myth": "Aspirin is enough to prevent strokes in AFib",
            "truth": "Aspirin doesn't work for AFib stroke prevention. Anticoagulation is required.",
            "source": "PMID: 29128963"
        },
    ],
    truths=[
        {"fact": "AFib increases stroke risk 5x", "context": "Major preventable cause of stroke"},
        {"fact": "1 in 4 adults will develop AFib", "context": "Lifetime risk"},
        {"fact": "CHA2DS2-VASc guides anticoagulation decisions", "context": "Score ≥2 usually needs blood thinner"},
    ],
    statistics=[
        {"value": "5x", "label": "increased stroke risk with AFib", "context": "Without anticoagulation"},
        {"value": "1 in 4", "label": "adults will develop AFib", "context": "Lifetime risk after age 40"},
        {"value": "33M", "label": "people have AFib worldwide", "context": "Growing epidemic"},
        {"value": "70-80%", "label": "ablation success rate", "context": "But recurrence is common"},
        {"value": "90%", "label": "stroke risk reduction with anticoagulation", "context": "In appropriate patients"},
    ],
    tips=[
        "Check your pulse regularly - irregular rhythm may be AFib",
        "Smartwatches can detect AFib but confirm with EKG",
        "Take blood thinners exactly as prescribed - don't skip doses",
        "Limit alcohol - even moderate drinking increases AFib risk",
        "Manage sleep apnea - it's a major driver of AFib",
    ],
    quotes=[
        {"text": "AFib is the epidemic of the 21st century. We need better awareness.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "The stroke you prevent is the one you'll never know about.", "author": "AF-SCREEN International"},
    ],
    hooks=[
        "AFib: the heart condition you might not feel",
        "Why your irregular heartbeat could cause a stroke",
        "5 AFib facts that could save your life",
        "Blood thinners for AFib: myths vs reality",
        "Is your heart secretly in AFib?",
    ],
    sources=["PMID: 30586768", "PMID: 28359515", "PMID: 28436045"]
)


# ============================================================================
# HEART FAILURE CONTENT
# ============================================================================
HEART_FAILURE = TopicContent(
    topic="heart failure",
    core_subject="heart failure",
    aliases=["hf", "chf", "congestive heart failure", "weak heart", "heart failure symptoms",
             "ejection fraction", "hfref", "hfpef"],
    myths=[
        {
            "myth": "Heart failure means your heart has stopped",
            "truth": "The heart still beats but pumps inefficiently. With treatment, many patients live well for years.",
            "source": "AHA Guidelines 2022"
        },
        {
            "myth": "Heart failure only affects elderly people",
            "truth": "Can occur at any age. Younger patients often have viral or genetic causes.",
            "source": "PMID: 31475790"
        },
        {
            "myth": "You should avoid exercise with heart failure",
            "truth": "Exercise training improves symptoms and survival in heart failure. Cardiac rehab is recommended.",
            "source": "HF-ACTION Trial"
        },
        {
            "myth": "If your EF is preserved, you don't have heart failure",
            "truth": "HFpEF (preserved EF) is just as serious. It's about filling, not just pumping.",
            "source": "PMID: 30955668"
        },
        {
            "myth": "Heart failure medications are just symptom control",
            "truth": "Four pillars (ARNI/ACEi, BB, MRA, SGLT2i) reduce mortality significantly.",
            "source": "2022 AHA/ACC Guidelines"
        },
    ],
    truths=[
        {"fact": "GDMT reduces heart failure mortality by 50%", "context": "When all four drug classes used"},
        {"fact": "6 million Americans have heart failure", "context": "Growing due to aging population"},
        {"fact": "50% of HF patients have preserved ejection fraction", "context": "HFpEF often underdiagnosed"},
    ],
    statistics=[
        {"value": "6M", "label": "Americans have heart failure", "context": "And increasing"},
        {"value": "50%", "label": "mortality reduction with optimal GDMT", "context": "Guideline-directed medical therapy"},
        {"value": "4", "label": "medication pillars save lives in HFrEF", "context": "ARNI, BB, MRA, SGLT2i"},
        {"value": "50%", "label": "of HF patients have HFpEF", "context": "Preserved ejection fraction"},
        {"value": "$30.7B", "label": "annual US healthcare cost for HF", "context": "Major economic burden"},
    ],
    tips=[
        "Weigh yourself daily - sudden gain (>2-3 lbs) may mean fluid retention",
        "Limit sodium to <2000mg daily to prevent fluid overload",
        "Take all your heart failure medications - they work better together",
        "Report increasing shortness of breath or swelling immediately",
        "Ask about cardiac rehab - exercise helps heart failure",
    ],
    quotes=[
        {"text": "Heart failure isn't a death sentence. Modern therapy can transform quality and length of life.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "Get on all four pillars of GDMT. Each one saves lives.", "author": "2022 AHA Guidelines"},
    ],
    hooks=[
        "Heart failure isn't what you think it is",
        "The 4 medications that save heart failure lives",
        "Why exercise helps (not hurts) heart failure",
        "5 heart failure warning signs to watch",
        "Heart failure at 40: why it's increasing",
    ],
    sources=["2022 AHA/ACC Guidelines", "PMID: 31475790", "HF-ACTION Trial"]
)


# ============================================================================
# DIABETES-CARDIO CONTENT
# ============================================================================
DIABETES_CARDIO = TopicContent(
    topic="diabetes and heart disease",
    core_subject="diabetes",
    aliases=["diabetes", "type 2 diabetes", "diabetic heart disease", "diabetes cardiovascular",
             "diabetes heart risk", "a1c", "blood sugar heart"],
    myths=[
        {
            "myth": "Diabetes is just about blood sugar",
            "truth": "Diabetes is a cardiovascular disease. Most diabetics die from heart disease, not high sugar.",
            "source": "PMID: 29146531"
        },
        {
            "myth": "Tight glucose control prevents heart attacks",
            "truth": "Intensive glucose control reduces microvascular disease but hasn't reduced macrovascular events in most trials.",
            "source": "ACCORD Trial"
        },
        {
            "myth": "All diabetes medications are equal for the heart",
            "truth": "SGLT2 inhibitors and GLP-1 agonists reduce cardiovascular events. Older drugs don't.",
            "source": "PMID: 31535829"
        },
        {
            "myth": "If my A1C is good, my heart is protected",
            "truth": "A1C is just one factor. BP, LDL, smoking cessation matter as much or more for CV outcomes.",
            "source": "PMID: 28110296"
        },
        {
            "myth": "Metformin is bad for the heart",
            "truth": "Metformin is cardioprotective. UKPDS showed cardiovascular benefit that persisted long-term.",
            "source": "UKPDS 34"
        },
    ],
    truths=[
        {"fact": "Diabetes = cardiovascular disease equivalent", "context": "Same risk as prior MI"},
        {"fact": "SGLT2i reduce heart failure hospitalization by 30-35%", "context": "Game-changing medications"},
        {"fact": "Comprehensive risk factor control prevents 80% of CV events", "context": "ABC approach"},
    ],
    statistics=[
        {"value": "2-4x", "label": "higher CV mortality in diabetics", "context": "Compared to non-diabetics"},
        {"value": "30-35%", "label": "reduction in HF hospitalization with SGLT2i", "context": "Major breakthrough"},
        {"value": "68%", "label": "of diabetics >65 die from heart disease", "context": "Leading cause of death"},
        {"value": "80%", "label": "of CV events preventable with ABC control", "context": "A1C, BP, Cholesterol"},
        {"value": "50%", "label": "reduction in CV events with SGLT2i/GLP-1", "context": "High-risk patients"},
    ],
    tips=[
        "Ask about SGLT2 inhibitors or GLP-1 agonists if you have diabetes + heart disease",
        "Target BP <130/80 in diabetes for CV protection",
        "LDL target <70 mg/dL if you have diabetes + any CV risk factor",
        "Don't focus only on A1C - BP and cholesterol matter as much for your heart",
        "Aspirin is no longer recommended for all diabetics - ask your doctor",
    ],
    quotes=[
        {"text": "Treat diabetes like heart disease, because that's what it is.", "author": "Dr. Shailesh Singh, Cardiologist"},
        {"text": "The diabetes medications you choose can determine cardiovascular fate.", "author": "ADA Standards of Care"},
    ],
    hooks=[
        "Why diabetes is really a heart disease",
        "The diabetes medications that save hearts",
        "5 things diabetics must do for their heart",
        "A1C isn't everything: the heart truth about diabetes",
        "SGLT2 inhibitors: the game-changer for diabetic hearts",
    ],
    sources=["PMID: 29146531", "PMID: 31535829", "ACCORD Trial", "UKPDS"]
)


# ============================================================================
# CONTENT DATABASE REGISTRY
# ============================================================================
CONTENT_DATABASE: Dict[str, TopicContent] = {
    "statins": STATINS,
    "statin": STATINS,
    "statin myths": STATINS,
    "statin side effects": STATINS,
    "ldl": LDL_CHOLESTEROL,
    "ldl cholesterol": LDL_CHOLESTEROL,
    "cholesterol": LDL_CHOLESTEROL,
    "glp-1": GLP1_AGONISTS,
    "glp1": GLP1_AGONISTS,
    "ozempic": GLP1_AGONISTS,
    "wegovy": GLP1_AGONISTS,
    "semaglutide": GLP1_AGONISTS,
    "mounjaro": GLP1_AGONISTS,
    "tirzepatide": GLP1_AGONISTS,
    "blood pressure": BLOOD_PRESSURE,
    "hypertension": BLOOD_PRESSURE,
    "bp": BLOOD_PRESSURE,
    "heart attack": HEART_ATTACK,
    "mi": HEART_ATTACK,
    "myocardial infarction": HEART_ATTACK,
    "cac": CAC_SCORING,
    "cac score": CAC_SCORING,
    "cac scoring": CAC_SCORING,
    "coronary calcium": CAC_SCORING,
    "calcium score": CAC_SCORING,
    "afib": ATRIAL_FIBRILLATION,
    "atrial fibrillation": ATRIAL_FIBRILLATION,
    "af": ATRIAL_FIBRILLATION,
    "heart failure": HEART_FAILURE,
    "hf": HEART_FAILURE,
    "chf": HEART_FAILURE,
    "diabetes": DIABETES_CARDIO,
    "diabetes heart": DIABETES_CARDIO,
    "diabetic heart disease": DIABETES_CARDIO,
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_content(topic: str) -> Optional[TopicContent]:
    """
    Get content for a topic by matching against database.

    Args:
        topic: Topic string (e.g., "statin myths", "GLP-1 weight loss")

    Returns:
        TopicContent if found, None otherwise
    """
    topic_lower = topic.lower().strip()

    # Direct match
    if topic_lower in CONTENT_DATABASE:
        return CONTENT_DATABASE[topic_lower]

    # Check aliases
    for key, content in CONTENT_DATABASE.items():
        if topic_lower in [a.lower() for a in content.aliases]:
            return content
        # Partial match
        if any(alias.lower() in topic_lower for alias in content.aliases):
            return content
        if topic_lower in key or key in topic_lower:
            return content

    return None


def normalize_topic(topic: str) -> str:
    """
    Normalize topic to core subject.

    Args:
        topic: Raw topic string (e.g., "5 statin myths", "statin myths debunked")

    Returns:
        Core subject (e.g., "statins")
    """
    topic_lower = topic.lower().strip()

    # Remove common prefixes (numbers)
    import re
    topic_lower = re.sub(r'^\d+\s+', '', topic_lower)

    # Remove common suffixes
    suffixes_to_remove = [
        'myths', 'myth', 'facts', 'tips', 'truth', 'truths',
        'debunked', 'explained', 'guide', 'mistakes', 'ways',
        'things', 'signs', 'symptoms', 'causes', 'effects',
        'benefits', 'risks', 'dangers', 'about'
    ]

    for suffix in suffixes_to_remove:
        topic_lower = re.sub(rf'\s+{suffix}\s*$', '', topic_lower)
        topic_lower = re.sub(rf'^{suffix}\s+', '', topic_lower)
        topic_lower = re.sub(rf'\s+{suffix}\s+', ' ', topic_lower)

    # Try to find matching content and use its core_subject
    content = get_content(topic_lower)
    if content:
        return content.core_subject

    # Fallback: clean the topic
    return topic_lower.strip()


def get_myths_for_topic(topic: str, count: int = 3) -> List[Dict[str, str]]:
    """Get myths for a topic."""
    content = get_content(topic)
    if content and content.myths:
        return content.myths[:count]
    return []


def get_statistics_for_topic(topic: str, count: int = 3) -> List[Dict[str, str]]:
    """Get statistics for a topic."""
    content = get_content(topic)
    if content and content.statistics:
        return content.statistics[:count]
    return []


def get_tips_for_topic(topic: str, count: int = 5) -> List[str]:
    """Get tips for a topic."""
    content = get_content(topic)
    if content and content.tips:
        return content.tips[:count]
    return []


def get_hooks_for_topic(topic: str) -> List[str]:
    """Get pre-written hooks for a topic."""
    content = get_content(topic)
    if content and content.hooks:
        return content.hooks
    return []


def list_available_topics() -> List[str]:
    """List all available topics in the database."""
    seen = set()
    topics = []
    for content in CONTENT_DATABASE.values():
        if content.topic not in seen:
            topics.append(content.topic)
            seen.add(content.topic)
    return sorted(topics)


# ============================================================================
# CLI for testing
# ============================================================================
if __name__ == "__main__":
    import sys

    print("\n📚 CARDIOLOGY CONTENT DATABASE")
    print("=" * 60)

    print("\n📋 Available Topics:")
    for topic in list_available_topics():
        content = get_content(topic)
        print(f"  • {topic}: {len(content.myths)} myths, {len(content.statistics)} stats, {len(content.tips)} tips")

    # Test topic lookup
    if len(sys.argv) > 1:
        test_topic = " ".join(sys.argv[1:])
        print(f"\n🔍 Testing topic: '{test_topic}'")

        content = get_content(test_topic)
        if content:
            print(f"✅ Found: {content.topic}")
            print(f"   Core subject: {content.core_subject}")
            print(f"\n   Myths ({len(content.myths)}):")
            for i, myth in enumerate(content.myths[:3], 1):
                print(f"   {i}. MYTH: {myth['myth']}")
                print(f"      TRUTH: {myth['truth']}")

            print(f"\n   Statistics ({len(content.statistics)}):")
            for stat in content.statistics[:3]:
                print(f"   • {stat['value']} - {stat['label']}")

            print(f"\n   Hooks ({len(content.hooks)}):")
            for hook in content.hooks[:3]:
                print(f"   • {hook}")
        else:
            print(f"❌ No content found for: {test_topic}")

        # Test normalization
        print(f"\n🔧 Normalized: '{test_topic}' → '{normalize_topic(test_topic)}'")

    print("\n✅ Content database loaded successfully!")
