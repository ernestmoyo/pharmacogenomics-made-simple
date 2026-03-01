# Quality Improvement Proposal: Evaluating Clinical Opportunities for Pharmacogenomic Interpretation in Oncology Care

**Institution:** Oregon Health & Science University (OHSU)
**Department:** Medical Genetics / Oncology
**Proposal Type:** Quality Improvement / Clinical Research

---

## Investigator Team

| Role | Name | Credentials | Affiliation |
|---|---|---|---|
| **Principal Investigator** | Ngonidzashe Faya, PhD | Board-certified Medical Geneticist (ABMGG) | OHSU, Department of Medical Genetics |
| Co-Investigator | Tapiwa Mupereki | Board-certified Medical Geneticist (ABMGG) | OHSU / PGx Clinical Solutions (Industry Partner) |
| Co-Investigator | Rangarirai Makuku, PharmD, DrPH(c) | Pharmacist, Public Health | PGx Clinical Solutions (Industry Partner) |
| Co-Investigator | Ernest Moyo, MSc, PhD(c) | Biostatistics & Epidemiology | PGx Clinical Solutions (Industry Partner) |

---

## 1. Project Title

**Evaluating the Gap Between Pharmacogenomic Testing Opportunities and Clinical Action in Patients with Advanced Solid Cancers: A Retrospective Quality Improvement Study**

---

## 2. Problem Statement

Cancer patients frequently receive medications with known pharmacogenomic implications, yet the vast majority do not receive germline pharmacogenomic (PGx) testing to guide drug selection and dosing. When testing is performed, the results are often reported as raw genotype data without actionable clinical interpretation, leaving oncologists uncertain about how to modify treatment plans.

A recent study by Shugg et al. (2022) at an academic medical center found that approximately 60% of cancer patients received medications with pharmacogenetic implications, yet only 14% had actionable pharmacogenetic instances addressed. Additionally, drug-drug interactions (DDIs) occurred in over 50% of subjects, with serious interactions involving CYP3A (24.9%), CYP2D6 (16.8%), and CYP2C19 (11.7%).

This gap between available pharmacogenomic knowledge and clinical action represents a significant quality concern, potentially contributing to adverse drug reactions, treatment failures, suboptimal dosing, and preventable patient harm.

---

## 3. Background and Significance

### 3.1 The Clinical Case for PGx in Oncology

Pharmacogenomics is the study of how genetic variation influences individual drug response. In oncology, this is particularly critical because:

- **Narrow therapeutic indices:** Many chemotherapy agents have small margins between effective and toxic doses. Genetic variants affecting drug metabolism can push patients into toxicity or subtherapeutic ranges.
- **DPYD and fluoropyrimidines:** CPIC guidelines recommend DPYD genotyping before prescribing 5-fluorouracil or capecitabine. Poor metabolizers face life-threatening toxicity, yet pre-treatment testing remains inconsistent (Amstutz et al., 2018).
- **CYP2D6 and tamoxifen:** CYP2D6 poor metabolizers have reduced conversion of tamoxifen to its active metabolite endoxifen, potentially compromising breast cancer treatment efficacy.
- **UGT1A1 and irinotecan:** UGT1A1*28 homozygotes are at significantly increased risk of severe neutropenia with standard irinotecan dosing.
- **TPMT/NUDT15 and thiopurines:** Variants in these genes necessitate dose reduction to avoid severe myelosuppression.

### 3.2 The Interpretation Gap

Even when PGx testing is available, a systemic interpretation gap exists:

- Laboratories report raw genotype results (e.g., "CYP2D6 *1/*4") without translating these into clinical recommendations specific to the patient's current medication regimen.
- Oncologists, who are experts in cancer biology but not necessarily in pharmacogenomics, receive reports that require specialized knowledge to act upon.
- No standardized workflow exists at most institutions to integrate PGx results into oncology treatment decisions at the point of care.

### 3.3 Institutional Context

OHSU is an academic medical center with access to comprehensive patient records, including medication histories, genetic testing results, and clinical outcomes. This provides an ideal environment to:

1. Quantify the scope of missed PGx opportunities in our oncology population
2. Evaluate the clinical impact of the interpretation gap
3. Pilot an AI-assisted interpretation tool to bridge this gap

---

## 4. Study Objectives

### Primary Objectives

1. **Quantify the PGx opportunity gap:** Determine the proportion of oncology patients at OHSU who received medications with pharmacogenomic implications over a defined period and assess how many had relevant PGx testing performed.

2. **Characterize missed interventions:** Among patients with available PGx data, identify instances where actionable genotype-drug interactions were present but not addressed in clinical documentation or treatment modifications.

3. **Assess drug-drug interaction burden:** Evaluate the prevalence and severity of pharmacokinetic DDIs in the study population, particularly those involving CYP enzymes with known pharmacogenomic variability.

### Secondary Objectives

4. **Pilot an AI-assisted interpretation model:** Apply the PGx Clinical Solutions interpretation engine to retrospective patient data and compare its recommendations against actual clinical decisions made.

5. **Evaluate clinical outcome correlations:** Where data permits, assess whether patients with unaddressed PGx findings experienced higher rates of adverse drug reactions, treatment modifications, emergency department visits, or hospitalizations.

6. **Generate evidence for clinical workflow integration:** Produce data to support the development of a standardized PGx interpretation workflow for OHSU oncology services.

---

## 5. Study Design

### 5.1 Design Type
Retrospective, observational quality improvement study using existing electronic health record (EHR) data.

### 5.2 Study Population

**Inclusion Criteria:**
- Adult patients (age 18+) with a diagnosis of advanced solid cancer (Stage III or IV)
- Treated at OHSU oncology services during the study period
- Received at least one systemic therapy (chemotherapy, targeted therapy, or hormonal therapy) with known pharmacogenomic implications per CPIC guidelines

**Exclusion Criteria:**
- Patients enrolled in blinded clinical trials where treatment assignment is predetermined
- Patients with incomplete medication records
- Pediatric patients (separate PGx considerations)

### 5.3 Study Period
Retrospective review of records spanning the most recent 3-5 years (exact dates to be determined based on data availability and IRB/QI committee guidance).

### 5.4 Estimated Sample Size
Based on OHSU oncology patient volumes, we anticipate a study population of 500-1,000 patients meeting inclusion criteria. This is comparable to the Shugg et al. study (n=481) and provides adequate power for descriptive analyses and subgroup comparisons.

---

## 6. Methodology

### 6.1 Data Collection

Data will be extracted from the OHSU EHR system (Epic) including:

| Data Element | Source |
|---|---|
| Patient demographics (age, sex, ethnicity) | Patient registration |
| Cancer diagnosis, stage, histology | Problem list / pathology |
| Medication history (systemic therapies + concomitant medications) | Medication administration records |
| Existing genetic/genomic test results | Laboratory results / molecular pathology |
| Metabolizer status (if PGx testing was done) | Pharmacogenomic test reports |
| Adverse drug reactions documented | Clinical notes / adverse event reports |
| ED visits, hospitalizations, treatment changes | Encounter records |

### 6.2 PGx Opportunity Assessment

For each patient, we will:

1. **Map medications to pharmacogenes** using CPIC guidelines and FDA pharmacogenomic biomarker tables. Priority genes: CYP2D6, CYP2C19, CYP2C9, CYP3A4/5, DPYD, UGT1A1, TPMT, NUDT15.

2. **Determine PGx testing status:** Was germline PGx testing ordered? If so, what was tested and what were the results?

3. **Identify actionable interactions:** For patients with PGx results, were there gene-drug interactions that warranted dose adjustment, drug substitution, or enhanced monitoring?

4. **Assess clinical action taken:** Was the PGx information reflected in documented clinical decisions?

5. **Score DDI burden:** Catalogue all pharmacokinetic DDIs using a standardized severity classification.

### 6.3 AI-Assisted Interpretation Model

The PGx Clinical Solutions interpretation engine will be applied to the de-identified dataset to:

- Generate automated clinical recommendations for each patient based on their genotype and medication profile
- Compare AI-generated recommendations against actual clinical decisions
- Measure concordance, discordance, and identify cases where the AI model detected clinically significant findings that were missed

**Important:** The AI model will be used retrospectively on de-identified data only. No real-time clinical decisions will be influenced during the study period. The model has been validated against 12 clinical test scenarios with 100% accuracy across psychiatry, oncology, pain management, and cardiology therapeutic areas.

### 6.4 Statistical Analysis

- **Descriptive statistics** for prevalence of PGx-relevant medications, testing rates, actionable findings, and DDI burden
- **Chi-square / Fisher's exact tests** for categorical comparisons between tested vs. untested patients
- **Logistic regression** to identify predictors of PGx testing (demographics, cancer type, treatment setting)
- **Concordance analysis** (Cohen's kappa) comparing AI-generated recommendations to clinician decisions
- **Subgroup analyses** by cancer type, ethnicity (to assess population-specific variant prevalence), and treatment setting

Analysis will be conducted using Python (scipy, statsmodels) and R as appropriate.

---

## 7. Outcomes and Deliverables

### 7.1 Primary Outcomes

| Outcome | Metric |
|---|---|
| PGx opportunity prevalence | % of patients receiving medications with PGx implications |
| PGx testing rate | % of eligible patients who received PGx testing |
| Actionable finding rate | % of tested patients with clinically actionable genotype-drug interactions |
| Clinical action rate | % of actionable findings that resulted in documented treatment modifications |
| DDI prevalence | % of patients with significant pharmacokinetic DDIs |

### 7.2 Deliverables

1. **Peer-reviewed publication** in a high-impact journal (target: JCO Precision Oncology, JAMA Oncology, or Journal of Clinical Oncology)
2. **Internal QI report** to OHSU oncology leadership with recommendations for PGx integration
3. **Validated interpretation model** demonstrated on real-world data with measured performance metrics
4. **Clinical workflow proposal** for integrating PGx interpretation into OHSU oncology practice
5. **Conference presentation** at relevant meetings (ASHG, AMP, ASCO)

---

## 8. Timeline

| Phase | Activity | Duration |
|---|---|---|
| Phase 1 | Protocol development, IRB/QI committee approval, data access agreements | Months 1-2 |
| Phase 2 | Data extraction and cleaning | Months 2-3 |
| Phase 3 | PGx opportunity mapping and DDI analysis | Months 3-4 |
| Phase 4 | AI model application and concordance analysis | Months 4-5 |
| Phase 5 | Statistical analysis and interpretation | Month 5 |
| Phase 6 | Manuscript preparation and submission | Month 6 |

**Total estimated duration: 6 months**

---

## 9. Ethical Considerations

### 9.1 QI vs. Research Determination
This project may qualify as a Quality Improvement initiative under OHSU policy, as it:
- Evaluates current practice against established clinical guidelines (CPIC)
- Aims to improve the quality of care delivery
- Uses retrospective data with no intervention on current patients

If determined to be research, a full IRB protocol will be submitted. In either case, the following protections apply:

### 9.2 Data Protection
- All patient data will be de-identified before analysis
- Data will be stored on OHSU-approved secure servers
- No patient identifiers will leave the institution
- Industry partner access will be limited to de-identified, aggregated datasets
- All investigators will complete required CITI training

### 9.3 Industry Partnership
PGx Clinical Solutions serves as an industry partner providing the interpretation technology. The relationship will be disclosed in all publications. The industry partner will:
- Provide the AI interpretation engine for retrospective analysis
- Contribute biostatistical and bioinformatics expertise
- Have no access to identifiable patient data
- Have no influence over study findings or publication decisions

---

## 10. Budget Estimate

| Item | Estimated Cost |
|---|---|
| PI effort (5-10% FTE, 6 months) | Institution-supported |
| Co-investigator effort | Industry partner-supported |
| Data analyst support (if needed) | $10,000 - $20,000 |
| Statistical software / computing | $2,000 - $5,000 |
| Publication fees (open access) | $3,000 - $5,000 |
| Conference presentation (travel, registration) | $3,000 - $5,000 |
| **Total estimated external funding needed** | **$18,000 - $35,000** |

**Potential funding sources:**
- OHSU internal QI grants
- OHSU Knight Cancer Institute pilot funding
- NIH CTSA (Clinical and Translational Science Award) pilot grants
- Institutional pharmacy research funds
- ASHP Foundation research grants

---

## 11. Significance and Impact

### 11.1 For OHSU
- Establishes baseline data on PGx utilization in oncology
- Identifies specific areas where PGx testing and interpretation can improve patient outcomes
- Positions OHSU as a leader in precision oncology implementation

### 11.2 For the Field
- Replicates and extends the Shugg et al. (2022) findings in a different academic medical center
- Provides the first evaluation of an AI-assisted PGx interpretation tool against real-world clinical decisions
- Contributes to the evidence base for clinical PGx implementation in oncology

### 11.3 For Future Development
- Generates the validation data needed to transition from a QI tool to a clinical decision support system
- Creates a pathway for prospective implementation studies
- Establishes the industry-academic partnership model for future collaboration

---

## 12. References

1. Shugg T, Ly RC, Rowe EJ, et al. Clinical Opportunities for Germline Pharmacogenetics and Management of Drug-Drug Interactions in Patients With Advanced Solid Cancers. *JCO Precision Oncology*. 2022. PMID: 35201852.

2. Amstutz U, Henricks LM, Offer SM, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) Guideline for Dihydropyrimidine Dehydrogenase Genotype and Fluoropyrimidine Dosing: 2017 Update. *Clinical Pharmacology and Therapeutics*. 2018;103(2):210-216. PMID: 29152729.

3. Relling MV, Evans WE. Pharmacogenomics in the clinic. *Nature*. 2015;526(7573):343-350.

4. Hertz DL, Rae J. Pharmacogenetics of cancer drugs. *Annual Review of Medicine*. 2015;66:65-81.

5. Bousman CA, Dunlop BW. Genotype, phenotype, and medication recommendation agreement among commercial pharmacogenomic-based decision support tools. *Pharmacogenomics Journal*. 2018;18(5):613-622.

6. Clinical Pharmacogenetics Implementation Consortium (CPIC). CPIC Guidelines. https://cpicpgx.org/guidelines/

7. FDA Table of Pharmacogenomic Biomarkers in Drug Labeling. https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling

---

*Prepared by PGx Clinical Solutions in collaboration with OHSU investigators.*
*Date: March 2026*
*Version: 1.0 — Draft for internal review*
