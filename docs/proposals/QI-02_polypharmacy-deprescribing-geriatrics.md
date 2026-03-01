# Quality Improvement Proposal: Pharmacogenomics-Guided Deprescribing in Geriatric Polypharmacy

**Institution:** Oregon Health & Science University (OHSU)
**Department:** Geriatric Medicine / Clinical Pharmacy / Medical Genetics
**Proposal Type:** Quality Improvement / Clinical Research

---

## Investigator Team

| Role | Name | Credentials | Affiliation |
|---|---|---|---|
| **Principal Investigator** | Ngonidzashe Faya, PhD | Board-certified Medical Geneticist (ABMGG) | OHSU, Department of Medical Genetics |
| Co-Investigator | Rangarirai Makuku, PharmD, DrPH(c) | Pharmacist, Public Health | PGx Clinical Solutions (Industry Partner) |
| Co-Investigator | Tapiwa Mupereki | Board-certified Medical Geneticist (ABMGG) | OHSU / PGx Clinical Solutions (Industry Partner) |
| Co-Investigator | Ernest Moyo, MSc, PhD(c) | Biostatistics & Epidemiology | PGx Clinical Solutions (Industry Partner) |
| Collaborator (TBD) | Geriatrician at OHSU or partner institution | MD, Geriatric Medicine | To be identified |

---

## 1. Project Title

**Pharmacogenomics-Guided Deprescribing in Older Adults with Polypharmacy: A Retrospective Evaluation and AI-Assisted Decision Support Model**

---

## 2. Problem Statement

Polypharmacy — commonly defined as the concurrent use of five or more medications — is pervasive among older adults and is associated with increased risks of adverse drug reactions (ADRs), drug-drug interactions (DDIs), falls, hospitalizations, cognitive decline, and mortality. In the United States, over 40% of adults aged 65 and older take five or more prescription medications, and approximately 20% take ten or more.

Deprescribing — the systematic process of identifying and discontinuing medications where existing or potential harms outweigh existing or potential benefits — is an evidence-based approach to reducing polypharmacy burden. However, deprescribing decisions are complex and clinicians often lack the tools and confidence to modify long-standing medication regimens.

A critical missing component in current deprescribing practice is **pharmacogenomic information**. Genetic variation in drug-metabolizing enzymes (CYP2D6, CYP2C19, CYP2C9, CYP3A4, etc.) directly affects how older adults process their medications. A patient who is a poor metabolizer of CYP2D6 may be experiencing side effects from a medication that could be safely discontinued or replaced — but without PGx testing, the clinician cannot distinguish between age-related changes and genotype-driven drug response.

This project proposes to evaluate the intersection of polypharmacy, pharmacogenomics, and deprescribing opportunities in geriatric patients, and to pilot an AI-assisted decision support tool that integrates PGx data into deprescribing recommendations.

---

## 3. Background and Significance

### 3.1 The Polypharmacy Crisis in Geriatrics

The burden of polypharmacy in older adults is well-documented:

- **Adverse drug reactions** are responsible for approximately 10-30% of hospital admissions in patients aged 65+ (Oscanoa et al., 2017)
- **Drug-drug interactions** increase exponentially with the number of medications: patients on 5-9 drugs have a 50% risk of a DDI; those on 20+ have a near 100% risk
- **Prescribing cascades** — where side effects of one drug are treated with another drug — are common in geriatric practice and compound the polypharmacy problem
- **Age-related pharmacokinetic changes** (reduced renal clearance, hepatic metabolism, altered body composition) further complicate drug response in older adults
- **Cognitive burden** of managing multiple medications contributes to non-adherence and medication errors

### 3.2 Deprescribing: The Solution and Its Barriers

Deprescribing frameworks (e.g., the Beers Criteria, STOPP/START criteria, the Deprescribing.org algorithms) provide structured approaches to identifying potentially inappropriate medications. However, clinicians face significant barriers:

- **Inertia:** Reluctance to change regimens that appear to be "working"
- **Complexity:** Evaluating interactions across 10+ medications requires specialized knowledge
- **Uncertainty:** Difficulty predicting which patients will benefit from discontinuation
- **Time constraints:** Comprehensive medication reviews are resource-intensive
- **Lack of genetic context:** Current deprescribing frameworks do not incorporate pharmacogenomic data

### 3.3 The Pharmacogenomic Dimension

Pharmacogenomic testing adds a critical layer of information to deprescribing decisions:

- **Identifying ineffective medications:** A patient who is a CYP2D6 ultra-rapid metabolizer may be getting little benefit from codeine (rapidly converting it to morphine, risking toxicity) or no benefit from tamoxifen (insufficient endoxifen levels). Deprescribing or substitution is clearly indicated.

- **Explaining "side effects" that are actually genotype-driven:** A CYP2C19 poor metabolizer on clopidogrel is at increased risk of cardiovascular events due to insufficient drug activation. What appears to be treatment failure may be a pharmacogenomic mismatch.

- **Prioritizing deprescribing targets:** PGx data can help rank which medications are most likely causing harm based on the patient's metabolizer status, enabling more confident deprescribing decisions.

- **Preventing re-prescribing:** Understanding a patient's genetic profile prevents future prescribers from restarting medications that are pharmacogenomically inappropriate.

Alagiakrishnan et al. (2018) identified pharmacogenomics as one of the "emerging approaches" to medication therapy in older adults alongside deprescribing, noting the need for integration of these two approaches in clinical practice.

### 3.4 The AI Opportunity

No existing clinical tool integrates polypharmacy assessment, deprescribing algorithms, DDI evaluation, and pharmacogenomic interpretation into a unified decision support system. This represents a significant opportunity for AI-assisted clinical tools that can:

- Process complex multi-drug regimens against pharmacogenomic profiles
- Generate prioritized deprescribing recommendations with evidence grading
- Identify prescribing cascades that could be interrupted
- Flag genotype-driven DDIs that compound polypharmacy risk
- Present recommendations in a clinician-friendly format at the point of care

---

## 4. Study Objectives

### Primary Objectives

1. **Characterize the polypharmacy landscape:** Determine the prevalence and patterns of polypharmacy among geriatric patients at OHSU, including medication counts, therapeutic classes, and DDI burden.

2. **Quantify deprescribing opportunities:** Apply established deprescribing criteria (Beers, STOPP/START) to identify potentially inappropriate medications in the study population.

3. **Assess PGx-informed deprescribing potential:** For patients with available PGx data (or imputed pharmacogenomic profiles based on population frequencies), estimate the additional deprescribing opportunities that PGx information would reveal.

### Secondary Objectives

4. **Pilot the AI-assisted deprescribing engine:** Apply the PGx Clinical Solutions interpretation engine (extended with deprescribing logic) to retrospective patient data and evaluate its recommendations against established criteria and expert pharmacist review.

5. **Evaluate clinical outcome associations:** Assess whether patients with higher polypharmacy burden and unaddressed PGx-relevant DDIs experienced more adverse outcomes (ADRs, falls, ED visits, hospitalizations, 30-day readmissions).

6. **Develop a PGx-integrated deprescribing workflow:** Produce a clinical pathway for incorporating PGx testing into routine geriatric medication review at OHSU.

---

## 5. Study Design

### 5.1 Design Type
Retrospective, observational quality improvement study with a prospective pilot component.

**Phase A (Retrospective):** Analysis of existing EHR data to characterize polypharmacy patterns, deprescribing opportunities, and PGx relevance.

**Phase B (Prospective Pilot):** Application of the AI-assisted deprescribing tool in real-time medication review sessions with geriatricians (advisory mode only — recommendations reviewed by clinician, not directly acted upon without clinical judgment).

### 5.2 Study Population

**Inclusion Criteria:**
- Adults aged 65 years and older
- Managed by OHSU geriatric medicine, primary care geriatrics, or geriatric consultation services
- Currently prescribed 5 or more concurrent medications (polypharmacy threshold)
- At least 6 months of continuous care at OHSU (to ensure adequate medication history)

**Exclusion Criteria:**
- Patients in hospice or comfort-care-only status (where medication optimization goals differ)
- Patients with fewer than 6 months of medication records at OHSU
- Patients actively enrolled in medication-related clinical trials

### 5.3 Study Period
**Phase A:** Retrospective review of records from the most recent 2-3 years.
**Phase B:** Prospective pilot over 3 months following Phase A completion.

### 5.4 Estimated Sample Size
**Phase A:** 800-1,500 patients meeting inclusion criteria (based on OHSU geriatric patient volumes).
**Phase B:** 50-100 patients for prospective pilot with geriatrician collaboration.

---

## 6. Methodology

### 6.1 Phase A: Retrospective Analysis

#### 6.1.1 Data Collection

Data will be extracted from the OHSU EHR system (Epic) including:

| Data Element | Source |
|---|---|
| Patient demographics (age, sex, ethnicity, weight, renal function) | Patient registration / labs |
| Complete medication list (prescription + OTC if documented) | Medication records |
| Diagnosis list and comorbidity burden (Charlson Comorbidity Index) | Problem list / ICD codes |
| Existing PGx test results (if any) | Laboratory / molecular pathology |
| Adverse drug reaction documentation | Clinical notes / allergy list |
| Fall events | Incident reports / clinical notes |
| ED visits and hospitalizations | Encounter records |
| 30-day readmission events | Encounter records |
| Medication changes (additions, discontinuations, dose adjustments) | Medication audit trail |

#### 6.1.2 Polypharmacy Assessment

For each patient, we will:

1. **Count and classify medications** by therapeutic class (cardiovascular, CNS, analgesic, GI, endocrine, etc.)
2. **Score DDI burden** using a standardized severity classification (major, moderate, minor) with specific attention to pharmacokinetic interactions involving CYP enzymes
3. **Apply Beers Criteria** (2023 AGS update) to identify potentially inappropriate medications
4. **Apply STOPP/START criteria** to identify medications to stop and potentially beneficial medications not prescribed
5. **Identify prescribing cascades** — instances where a medication appears to have been added to treat the side effect of another medication
6. **Calculate anticholinergic burden** using the Anticholinergic Cognitive Burden (ACB) scale

#### 6.1.3 Pharmacogenomic Overlay

For each patient:

1. **Patients with existing PGx data:** Map genotype results to current medications using CPIC guidelines. Identify genotype-drug mismatches.

2. **Patients without PGx data:** Apply population-frequency-based pharmacogenomic risk modeling to estimate the probability of clinically significant genotype-drug interactions based on patient ethnicity and medication profile. This provides a "number needed to test" estimate.

3. **Priority scoring:** Rank medications by combined risk score incorporating:
   - Beers/STOPP criteria flags
   - DDI severity
   - PGx interaction probability or confirmed mismatch
   - Anticholinergic burden contribution
   - Availability of safer alternatives

#### 6.1.4 AI-Assisted Deprescribing Engine

The PGx Clinical Solutions platform will be extended with deprescribing logic to produce, for each patient:

- **Medication risk profile:** Comprehensive assessment of each medication's risk-benefit ratio incorporating PGx data
- **Prioritized deprescribing recommendations:** Ranked list of medications to consider discontinuing, with rationale and evidence level
- **Alternative medication suggestions:** Where deprescribing is not appropriate, suggest pharmacogenomically appropriate alternatives
- **Cascade identification:** Highlight potential prescribing cascades with recommended intervention points
- **Monitoring plan:** Suggested monitoring parameters if deprescribing is undertaken

### 6.2 Phase B: Prospective Pilot

#### 6.2.1 Geriatrician Collaboration

Working with an identified geriatrician at OHSU (or partner institution):

1. **Medication review sessions:** The AI-assisted deprescribing engine generates recommendations for selected patients before their scheduled geriatric visits
2. **Clinician review:** The geriatrician reviews the AI recommendations alongside their own clinical assessment
3. **Concordance tracking:** Agreement between AI recommendations and clinician decisions is documented
4. **Feedback loop:** Geriatrician provides feedback on recommendation quality, clinical relevance, and usability
5. **Patient outcomes:** Short-term outcomes (medication changes made, patient acceptance, adverse events) tracked for 90 days

#### 6.2.2 Usability Assessment
- Structured feedback from geriatricians on report format, recommendation clarity, and workflow integration
- Time-to-review measurement
- System Usability Scale (SUS) questionnaire

---

## 7. Outcomes and Deliverables

### 7.1 Primary Outcomes

| Outcome | Metric |
|---|---|
| Polypharmacy prevalence | Mean and median medication count; % on 5+, 10+, 15+ medications |
| DDI burden | Mean DDIs per patient; % with at least one major DDI |
| Beers Criteria flags | Mean potentially inappropriate medications per patient |
| Deprescribing opportunity rate | % of patients with at least one deprescribing recommendation |
| PGx-added value | Additional deprescribing opportunities identified by PGx overlay vs. standard criteria alone |
| AI-clinician concordance | Cohen's kappa for Phase B pilot |
| Adverse outcome associations | Odds ratios for ADRs, falls, ED visits, hospitalizations by polypharmacy severity |

### 7.2 Deliverables

1. **Peer-reviewed publication** in a geriatric or clinical pharmacology journal (target: *Journal of the American Geriatrics Society*, *Age and Ageing*, *Drugs & Aging*, or *Pharmacogenomics Journal*)
2. **Second publication** focused on the AI-assisted deprescribing tool validation (target: *Journal of Medical Internet Research*, *JAMIA*, or *npj Digital Medicine*)
3. **Internal QI report** to OHSU geriatric medicine and pharmacy leadership
4. **Validated deprescribing engine** with measured performance on real-world geriatric data
5. **Clinical workflow protocol** for PGx-integrated medication review in geriatric care
6. **Conference presentations** at AGS Annual Meeting, ASHP Midyear, or AMCP

---

## 8. Timeline

| Phase | Activity | Duration |
|---|---|---|
| Phase 1 | Protocol development, QI/IRB approval, geriatrician recruitment | Months 1-2 |
| Phase 2 | Deprescribing engine development and testing | Months 1-3 (parallel) |
| Phase 3 | Retrospective data extraction and cleaning | Months 2-3 |
| Phase 4 | Polypharmacy characterization and deprescribing analysis | Months 3-5 |
| Phase 5 | AI model application and PGx overlay analysis | Months 5-6 |
| Phase 6 | Prospective pilot with geriatrician | Months 6-9 |
| Phase 7 | Statistical analysis and manuscript preparation | Months 9-11 |
| Phase 8 | Submission and revision | Month 12 |

**Total estimated duration: 12 months**

---

## 9. Ethical Considerations

### 9.1 QI Determination
Phase A is a retrospective quality improvement analysis evaluating current practice against established criteria (Beers, STOPP/START, CPIC). Phase B involves prospective observation of clinical decision-making with an advisory tool, where the treating clinician retains full authority over all prescribing decisions. Both may qualify as QI under OHSU policy; if determined to be research, full IRB approval will be obtained.

### 9.2 Patient Safety
- Phase B: The AI tool provides recommendations only. All deprescribing decisions are made by the treating geriatrician based on their clinical judgment.
- No medications will be changed solely based on AI recommendations.
- Any deprescribing undertaken as part of routine clinical care will follow established tapering protocols and monitoring guidelines.

### 9.3 Data Protection
- All Phase A data will be de-identified before analysis
- Phase B data will be managed under clinical care protocols with appropriate consent
- Industry partner access limited to de-identified, aggregated datasets
- All investigators will complete required CITI training
- Data stored on OHSU-approved secure infrastructure

### 9.4 Industry Partnership Disclosure
PGx Clinical Solutions serves as an industry partner providing the AI interpretation and deprescribing technology. The relationship will be fully disclosed in all publications and presentations. The industry partner will have no influence over study findings, clinical decisions, or publication decisions.

---

## 10. Budget Estimate

| Item | Estimated Cost |
|---|---|
| PI effort (10% FTE, 12 months) | Institution-supported |
| Geriatrician collaborator effort (5% FTE) | $10,000 - $15,000 |
| Co-investigator effort | Industry partner-supported |
| Clinical pharmacist for medication review validation | $15,000 - $25,000 |
| Data analyst support | $15,000 - $25,000 |
| Deprescribing engine development | Industry partner-supported |
| Statistical software / computing | $2,000 - $5,000 |
| Publication fees (open access, 2 papers) | $6,000 - $10,000 |
| Conference presentations (2 conferences) | $5,000 - $8,000 |
| **Total estimated external funding needed** | **$53,000 - $88,000** |

**Potential funding sources:**
- OHSU internal QI grants and pharmacy research funds
- NIA (National Institute on Aging) R21 Exploratory/Developmental Grant
- AHRQ (Agency for Healthcare Research and Quality) patient safety grants
- AGS (American Geriatrics Society) research awards
- John A. Hartford Foundation (geriatric care improvement)
- NIH CTSA pilot grants
- ASHP Foundation research grants
- PhRMA Foundation research starter grants in pharmacology/clinical pharmacology

---

## 11. Innovation and Significance

### 11.1 What Makes This Novel

This project is the first to:

1. **Integrate pharmacogenomics into deprescribing frameworks.** Current deprescribing guidelines (Beers, STOPP/START) do not incorporate PGx data. This project adds a genetic dimension to medication optimization.

2. **Apply AI to PGx-informed deprescribing.** No existing clinical decision support tool combines polypharmacy assessment, deprescribing algorithms, DDI evaluation, and pharmacogenomic interpretation in a single engine.

3. **Quantify the "PGx value-add" in geriatric deprescribing.** By comparing deprescribing opportunities identified with and without PGx data, this study directly measures the incremental clinical value of pharmacogenomic testing in older adults.

### 11.2 Clinical Impact

- **For patients:** Safer medication regimens tailored to individual genetic profiles, reduced pill burden, fewer adverse drug reactions, improved quality of life
- **For clinicians:** Evidence-based, AI-assisted decision support that reduces the cognitive burden of complex medication reviews and provides genetic context for deprescribing decisions
- **For health systems:** Reduced ADR-related hospitalizations, ED visits, and healthcare costs. Potential for significant savings given that ADRs in older adults cost the US healthcare system an estimated $30+ billion annually.

### 11.3 Scalability

The deprescribing engine, once validated, can be:
- Deployed as a SaaS tool for geriatric practices, long-term care facilities, and pharmacy services
- Integrated with EHR systems via API
- Extended to other populations (e.g., HIV patients on multi-drug regimens, psychiatric polypharmacy)
- Adapted for resource-limited settings where geriatric pharmacology expertise is scarce

---

## 12. References

1. Alagiakrishnan K, Mah D, Padwal R. Classic challenges and emerging approaches to medication therapy in older adults. *Discovery Medicine*. 2018;26(143):137-146. PMID: 30586537.

2. Shugg T, Ly RC, Rowe EJ, et al. Clinical Opportunities for Germline Pharmacogenetics and Management of Drug-Drug Interactions in Patients With Advanced Solid Cancers. *JCO Precision Oncology*. 2022. PMID: 35201852.

3. American Geriatrics Society Beers Criteria Update Expert Panel. American Geriatrics Society 2023 Updated AGS Beers Criteria for Potentially Inappropriate Medication Use in Older Adults. *Journal of the American Geriatrics Society*. 2023;71(7):2052-2081.

4. O'Mahony D, O'Sullivan D, Byrne S, et al. STOPP/START criteria for potentially inappropriate prescribing in older people: version 3. *European Geriatric Medicine*. 2023;14:625-632.

5. Scott IA, Hilmer SN, Reeve E, et al. Reducing inappropriate polypharmacy: the process of deprescribing. *JAMA Internal Medicine*. 2015;175(5):827-834.

6. Reeve E, Shakib S, Hendrix I, et al. Review of deprescribing processes and development of an evidence-based, patient-centred deprescribing process. *British Journal of Clinical Pharmacology*. 2014;78(4):738-747.

7. Clinical Pharmacogenetics Implementation Consortium (CPIC). CPIC Guidelines. https://cpicpgx.org/guidelines/

8. Oscanoa TJ, Lizaraso F, Carvajal A. Hospital admissions due to adverse drug reactions in the elderly. A meta-analysis. *European Journal of Clinical Pharmacology*. 2017;73(6):759-770.

---

*Prepared by PGx Clinical Solutions in collaboration with OHSU investigators.*
*Date: March 2026*
*Version: 1.0 — Draft for internal review*
