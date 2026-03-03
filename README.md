# PGx Clinical Solutions

**Clinical Pharmacogenomics Interpretation Platform**

A B2B platform that transforms raw pharmacogenomic test data into actionable, physician-ready clinical reports. The system analyzes gene-drug interactions, drug-drug interactions, and phenoconversion effects to deliver personalized medication recommendations grounded in CPIC guidelines and FDA labeling.

**Founders:** Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya

---

## Platform Modules

### Module 1: PGx Interpretation Engine
The core module. Takes raw genotyping results and a patient's medication list, then produces a clinical interpretation report.

- **21 gene-drug pairs** across 10 pharmacogenes (CYP2D6, CYP2C19, CYP2C9, CYP3A4, VKORC1, SLCO1B1, DPYD, UGT1A1, TPMT, HLA-B)
- **14 drug-drug interactions** with phenoconversion modeling
- **Risk scoring** (0-100) based on severity, evidence quality, FDA labeling, and phenoconversion compounding
- **Prioritized recommendations** with alternatives and monitoring plans
- Professional HTML clinical reports

### Module 2: Oncology PGx Gap Analysis
Identifies missed pharmacogenomic testing opportunities in oncology patient cohorts.

- Maps oncology medications to pharmacogenes with CPIC/FDA evidence
- Detects untested gene-drug pairs that have actionable clinical guidelines
- Scores DDI burden across multi-drug chemotherapy regimens
- Population-level analytics for cohort-wide PGx utilization rates
- Gap analysis reports with prioritized testing recommendations

### Module 3: Geriatric Deprescribing Engine
Screens polypharmacy patients against deprescribing criteria with a pharmacogenomic overlay.

- **2023 AGS Beers Criteria** screening for potentially inappropriate medications
- **STOPP/START v3** criteria evaluation
- **Anticholinergic Cognitive Burden (ACB)** scoring
- **Prescribing cascade detection** — identifies medications added to treat side effects of other medications
- **Composite polypharmacy risk score** (0-100) integrating all criteria
- Deprescribing recommendations prioritized by risk and PGx relevance

---

## Quick Start

```bash
# Standard PGx interpretation (25 patient reports)
python main.py

# Oncology gap analysis
python main.py --oncology-gap

# Geriatric deprescribing analysis
python main.py --deprescribing

# Full combined analysis (all 3 modules)
python main.py --full

# Interactive demo (5 clinical scenarios)
python demo.py

# Validation suite only
python main.py --validate-only
```

### Requirements

- Python 3.10+
- Jinja2 (`pip install jinja2`)

---

## Project Structure

```
pharmacogenomics-made-simple/
├── main.py                              # Pipeline orchestrator (CLI)
├── demo.py                              # Interactive demo script
├── requirements.txt
│
├── src/
│   ├── knowledge_base/                  # Clinical data (JSON)
│   │   ├── gene_drug_interactions.json      # 21 gene-drug pairs (CPIC/FDA)
│   │   ├── drug_drug_interactions.json      # 14 DDIs + CYP inhibitor/inducer tables
│   │   ├── dosing_guidelines.json           # Dosing tables, renal/hepatic adjustments
│   │   ├── pgx_drug_map.json                # Oncology drug-to-pharmacogene mapping
│   │   ├── beers_criteria.json              # 2023 AGS Beers Criteria
│   │   ├── stopp_start_criteria.json        # STOPP/START v3 rules
│   │   ├── anticholinergic_burden.json      # ACB scoring data
│   │   ├── prescribing_cascades.json        # Known prescribing cascade patterns
│   │   └── kb_loader.py                     # Knowledge base API
│   │
│   ├── data_generation/
│   │   └── synthetic_patients.py            # 25 synthetic patient profiles
│   │
│   ├── interpretation/                  # Module 1: PGx Interpretation
│   │   ├── engine.py                        # Core analysis engine
│   │   ├── risk_scorer.py                   # 0-100 risk scoring system
│   │   └── recommender.py                   # Recommendation generator
│   │
│   ├── oncology_gap/                    # Module 2: Oncology Gap Analysis
│   │   ├── gap_analyzer.py                  # PGx testing gap detection
│   │   ├── ddi_burden_scorer.py             # DDI burden scoring
│   │   └── population_analytics.py          # Cohort-level analytics
│   │
│   ├── deprescribing/                   # Module 3: Geriatric Deprescribing
│   │   ├── beers_checker.py                 # Beers Criteria screening
│   │   ├── stopp_start_checker.py           # STOPP/START evaluation
│   │   ├── anticholinergic_scorer.py        # ACB scoring
│   │   ├── cascade_detector.py              # Prescribing cascade detection
│   │   ├── polypharmacy_scorer.py           # Composite risk scoring
│   │   └── deprescribing_recommender.py     # Deprescribing recommendations
│   │
│   ├── reports/                         # Report generation
│   │   ├── generator.py                     # Report renderer
│   │   └── templates/
│   │       ├── clinical_report.html         # PGx interpretation report
│   │       ├── gap_analysis_report.html     # Oncology gap analysis report
│   │       └── deprescribing_report.html    # Deprescribing report
│   │
│   ├── validation/
│   │   └── validator.py                     # 24 clinical test cases
│   │
│   └── utils/
│       └── logger.py                        # Audit trail logging
│
├── data/
│   └── patients.json                    # Generated patient data
│
├── output/
│   ├── reports/                         # Generated HTML reports (all modules)
│   ├── analysis_summary.json
│   └── validation_report.txt
│
└── docs/
    ├── business_model.md                # Business model canvas
    ├── meetings/                        # Team meeting notes
    ├── proposals/                       # QI research proposals
    │   ├── QI-01_pgx-interpretation-oncology.md
    │   └── QI-02_polypharmacy-deprescribing-geriatrics.md
    └── research/                        # Market research & competitive intelligence
```

---

## How It Works

### PGx Interpretation Engine
For each patient, the engine:
1. Checks every medication against the patient's genotype
2. Identifies drug-drug interactions from the full medication list
3. Applies **phenoconversion logic** (concomitant CYP inhibitors shifting functional phenotype)
4. Evaluates renal and hepatic function for dose-sensitive drugs
5. Deduplicates and ranks findings by clinical severity

### Oncology Gap Analyzer
For oncology cohorts:
1. Maps each patient's medications to pharmacogenes with CPIC/FDA evidence
2. Checks which gene-drug pairs have been tested vs. untested
3. Scores the clinical impact of each untested pair
4. Generates cohort-wide statistics on PGx utilization rates

### Deprescribing Engine
For geriatric patients on 5+ medications:
1. Screens against Beers Criteria and STOPP/START rules
2. Calculates anticholinergic burden across the full medication list
3. Detects prescribing cascades (drug A side effect treated by drug B)
4. Overlays pharmacogenomic data to identify genotype-driven deprescribing targets
5. Produces a composite polypharmacy risk score (0-100) with prioritized recommendations

---

## Validation Results

```
Total test cases:             24/24 passed
Overall accuracy:             100%
Critical detection rate:      100%
Finding sensitivity:          100%

Modules validated:
  - PGx Interpretation:     12/12
  - Oncology Gap Analysis:    6/6
  - Geriatric Deprescribing:  6/6

Therapeutic areas:
  - Psychiatry
  - Cardiology
  - Oncology
  - Pain Management
  - Geriatrics
```

---

## Pipeline Performance

| Metric | Value |
|--------|-------|
| Patients analyzed | 25 |
| Total findings | 47 |
| Critical alerts | 15 |
| Actionable recommendations | 32 |
| Pipeline execution time | 0.1 seconds |
| Manual equivalent per report | 2-3 hours |
| Automated time per report | < 1 second |

---

## Genes Covered

| Gene | Drugs Affected | Clinical Impact |
|------|---------------|----------------|
| CYP2D6 | Codeine, tramadol, oxycodone, tamoxifen, nortriptyline, atomoxetine, ondansetron | Opioid toxicity, antidepressant dosing, cancer treatment efficacy |
| CYP2C19 | Citalopram, escitalopram, sertraline, clopidogrel | Antidepressant response, antiplatelet efficacy |
| CYP2C9 | Warfarin | Anticoagulation dosing |
| VKORC1 | Warfarin | Warfarin sensitivity |
| SLCO1B1 | Simvastatin, atorvastatin | Statin myopathy risk |
| DPYD | Fluorouracil, capecitabine | Fatal chemotoxicity prevention |
| UGT1A1 | Irinotecan | Chemotherapy toxicity |
| TPMT | Mercaptopurine | Thiopurine myelosuppression |
| HLA-B | Carbamazepine | Stevens-Johnson syndrome |
| CYP3A4 | Tacrolimus | Immunosuppressant dosing |

---

## Research & Proposals

- [QI-01: PGx Interpretation in Oncology](docs/proposals/QI-01_pgx-interpretation-oncology.md) — Retrospective study evaluating PGx testing gaps in cancer patients
- [QI-02: Polypharmacy Deprescribing in Geriatrics](docs/proposals/QI-02_polypharmacy-deprescribing-geriatrics.md) — PGx-guided deprescribing in elderly patients on 5+ medications
- [Market Research](docs/research/Pharmacogenomics_Research_Complete.md) — Competitive intelligence across 6 research blocks, 22 sub-topics

---

## Future Roadmap

- [ ] FastAPI web service for laboratory integration
- [ ] HL7 FHIR interface for EHR connectivity (OpenMRS/KenyaEMR)
- [ ] PDF report generation
- [ ] Real-time PharmGKB/CPIC API integration
- [ ] African population allele frequency panels
- [ ] AiBST GenoPharm panel compatibility
- [ ] Machine learning for complex multi-gene interaction prediction

---

## License

Proprietary. All rights reserved.

**PGx Clinical Solutions** — Precision medicine, made actionable.
