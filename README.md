# PGx Clinical Solutions

**Clinical Pharmacogenomics Interpretation Platform**

A B2B platform that transforms raw pharmacogenomic test data into actionable, physician-ready clinical reports. The system analyzes gene-drug interactions, drug-drug interactions, and phenoconversion effects to deliver personalized medication recommendations grounded in CPIC guidelines and FDA labeling.

**Founders:** Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya

---

## What It Does

Laboratories send us raw PGx genotyping results. We return a clinical interpretation report that tells the physician:

- Which drugs are **unsafe** for this patient's genotype
- Which drugs need **dose adjustments**
- Which **drug-drug interactions** compound genetic risk
- What **alternatives** to prescribe instead
- How urgently to act (priority-ranked recommendations)

### Therapeutic Areas

| Area | Example Scenario |
|------|-----------------|
| **Psychiatry** | CYP2C19 poor metabolizer on citalopram — reduce dose 50% or switch SSRI |
| **Pain Management** | CYP2D6 ultra-rapid metabolizer on codeine — AVOID (fatal toxicity risk) |
| **Cardiology** | CYP2C19 PM on clopidogrel — switch to prasugrel/ticagrelor (stent thrombosis risk) |
| **Oncology** | DPYD deficient on fluorouracil — CONTRAINDICATED (30% mortality at standard dose) |

---

## Quick Start

```bash
# Run the full pipeline (generates 25 patient reports)
python main.py

# Run the interactive demo (5 clinical scenarios with live analysis)
python demo.py

# Quick demo (no pauses)
python demo.py --quick

# Run a single demo scenario
python demo.py --scenario 1

# Validation only
python main.py --validate-only
```

### Requirements

- Python 3.10+
- Jinja2 (`pip install jinja2`)

---

## Project Structure

```
pharmacogenomics-made-simple/
├── main.py                          # Pipeline orchestrator
├── demo.py                          # Interactive demo script
├── requirements.txt
│
├── src/
│   ├── knowledge_base/
│   │   ├── gene_drug_interactions.json   # 21 gene-drug pairs (CPIC/FDA)
│   │   ├── drug_drug_interactions.json   # 14 DDIs + CYP inhibitor/inducer tables
│   │   ├── dosing_guidelines.json        # Dosing tables, renal/hepatic adjustments
│   │   └── kb_loader.py                  # Knowledge base API
│   │
│   ├── data_generation/
│   │   └── synthetic_patients.py         # 25 synthetic patient profiles
│   │
│   ├── interpretation/
│   │   ├── engine.py                     # Core analysis engine
│   │   ├── risk_scorer.py                # 0-100 risk scoring system
│   │   └── recommender.py               # Recommendation generator
│   │
│   ├── reports/
│   │   ├── generator.py                  # Report renderer
│   │   └── templates/
│   │       └── clinical_report.html      # Professional clinical report template
│   │
│   └── validation/
│       └── validator.py                  # 12 clinical test cases
│
├── data/
│   └── patients.json                     # Generated patient data
│
├── output/
│   ├── reports/                          # 25 HTML clinical reports
│   ├── analysis_summary.json
│   └── validation_report.txt
│
└── docs/
    └── business_model.md                 # Business model canvas
```

---

## How It Works

### 1. Knowledge Base
Curated from CPIC guidelines, FDA pharmacogenomic labels, and PharmGKB annotations:
- **21 gene-drug interactions** across CYP2D6, CYP2C19, CYP2C9, CYP3A4, VKORC1, SLCO1B1, DPYD, UGT1A1, TPMT, HLA-B
- **14 drug-drug interactions** with phenoconversion modeling (e.g., fluoxetine inhibiting CYP2D6 shifts a normal metabolizer to functional poor metabolizer)
- **Pharmacogenomic dosing tables** for warfarin, citalopram, codeine, tamoxifen, and more

### 2. Interpretation Engine
For each patient, the engine:
1. Checks every medication against the patient's genotype
2. Identifies drug-drug interactions from the full medication list
3. Applies **phenoconversion logic** (concomitant CYP inhibitors shifting functional phenotype)
4. Evaluates renal and hepatic function for dose-sensitive drugs
5. Deduplicates and ranks findings by clinical severity

### 3. Risk Scoring
Each finding is scored 0-100 based on:
- Severity (critical/high/moderate/low)
- Evidence quality (CPIC Level A/B/C)
- FDA label recognition (+5 points)
- Phenoconversion compounding (+8 points)
- Contraindication escalation (floor of 92)

### 4. Clinical Reports
Professional HTML reports modeled after clinical laboratory reports, featuring:
- Color-coded risk assessment dashboard
- Genotype results table with clinical significance
- Detailed gene-drug interaction cards with evidence badges
- Prioritized recommendation list with alternatives and monitoring plans
- Evidence methodology and clinical disclaimers

---

## Validation Results

```
Total test cases:             12/12 passed
Overall accuracy:             100%
Critical detection rate:      100%
Finding sensitivity:          100%

Therapeutic areas validated:
  - Cardiology:        4/4
  - Oncology:          4/4
  - Pain Management:   2/2
  - Psychiatry:        2/2
```

### Clinical Test Cases Include
- Codeine + CYP2D6 ultra-rapid metabolizer (fatal toxicity)
- Clopidogrel + CYP2C19 poor metabolizer (stent thrombosis)
- Warfarin + VKORC1/CYP2C9 double variant (major bleeding)
- Fluorouracil + DPYD deficiency (fatal chemotoxicity)
- Tamoxifen + CYP2D6 PM (breast cancer recurrence)
- Simvastatin + SLCO1B1 poor function (rhabdomyolysis)
- Carbamazepine + HLA-B*15:02 (Stevens-Johnson syndrome)
- Phenoconversion scenarios (fluoxetine + codeine, omeprazole + clopidogrel)

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

## Business Model

See [docs/business_model.md](docs/business_model.md) for the full canvas including:
- Per-report pricing ($75-300)
- Laboratory partnership model
- ROI projections ($650K adverse event cost avoidance in test cohort)
- Competitive landscape analysis
- Regulatory considerations (HIPAA, CLIA, FDA CDS exemption)

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

## Future Roadmap

- [ ] FastAPI web service for laboratory integration
- [ ] HL7 FHIR interface for EHR connectivity
- [ ] PDF report generation (WeasyPrint)
- [ ] Real-time PharmGKB API integration
- [ ] Panel curation for African/Zimbabwean populations
- [ ] Machine learning for complex multi-gene interaction prediction

---

## License

Proprietary. All rights reserved.

**PGx Clinical Solutions** — Precision medicine, made actionable.
