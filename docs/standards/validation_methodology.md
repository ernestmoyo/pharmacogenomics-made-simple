# Validation Methodology

How the PGx Clinical Solutions platform validates clinical accuracy across all three modules.

## Overview

The platform uses 24 pre-defined clinical test cases across three modules, each representing a known clinical scenario with expected outcomes. Test cases are run through the relevant analysis pipelines and compared against expected findings.

## Module 1: PGx Interpretation (12 Test Cases)

### Test Case Design
Each test case includes:
1. **Synthetic patient** with specific genotype and medication profile
2. **Expected findings** — which gene-drug interactions should be detected
3. **Expected severity** — the minimum severity level (critical, high, moderate)
4. **Expected action** — what clinical action should be recommended (stop, switch, reduce dose)

### What Constitutes a "Pass"
A test case passes when ALL of the following are true:
1. **Finding detected:** The expected gene-drug interaction is present in the output findings
2. **Severity correct:** The assigned severity matches expected (critical >= high is accepted as conservative)
3. **Action appropriate:** The recommended action type is clinically appropriate

### Test Cases (TC01-TC12)

| ID | Scenario | Area | Key Check |
|----|----------|------|-----------|
| TC01 | CYP2C19 PM on citalopram | Psychiatry | Dose reduction |
| TC02 | CYP2D6 UM on codeine | Pain | CONTRAINDICATED |
| TC03 | VKORC1 A/A + CYP2C9 PM on warfarin | Cardiology | Major dose reduction |
| TC04 | CYP2C19 PM on clopidogrel | Cardiology | Switch drug |
| TC05 | DPYD PM on fluorouracil | Oncology | CONTRAINDICATED |
| TC06 | SLCO1B1 poor on simvastatin | Cardiology | Switch statin |
| TC07 | CYP2D6 PM on tamoxifen | Oncology | Switch drug |
| TC08 | CYP2D6 PM + fluoxetine DDI on codeine | Pain | Dual flag |
| TC09 | CYP2C19 PM + omeprazole DDI on clopidogrel | Cardiology | Dual flag |
| TC10 | TPMT PM on mercaptopurine | Oncology | 90% dose reduction |
| TC11 | UGT1A1 *28/*28 on irinotecan | Oncology | 30% dose reduction |
| TC12 | HLA-B*15:02 on carbamazepine | Psychiatry | CONTRAINDICATED (SJS/TEN) |

---

## Module 2: Oncology Gap Analysis (6 Test Cases)

### Test Case Design
Each test case validates the gap analysis engine's ability to:
- Detect PGx-relevant drugs in a patient's medication list
- Identify testing gaps (PGx-relevant drug with no corresponding genotype)
- Detect missed interventions (actionable results not acted upon)
- Correctly classify gap severity
- Aggregate statistics across a patient cohort

### What Constitutes a "Pass"
- **Testing gap detected:** Correct gene flagged as untested for PGx-relevant drug
- **Missed intervention detected:** Critical/high findings correctly identified as missed actions
- **Gap severity correct:** Overall severity classification matches expected
- **Population stats correct:** Aggregate counts match expected values

### Test Cases (TC_GAP01-TC_GAP06)

| ID | Scenario | Key Check |
|----|----------|-----------|
| TC_GAP01 | Fluorouracil, no DPYD testing | Critical gap flagged |
| TC_GAP02 | DPYD PM on fluorouracil, has testing | Missed intervention detected |
| TC_GAP03 | Tamoxifen + fluoxetine, CYP2D6 PM | Missed intervention + DDI |
| TC_GAP04 | Fully compliant patient (NM, tested) | Zero gaps, severity=none |
| TC_GAP05 | Population of 5 patients | Correct aggregate counts |
| TC_GAP06 | Irinotecan, no UGT1A1 testing | Gap flagged for UGT1A1 |

---

## Module 3: Geriatric Deprescribing (6 Test Cases)

### Test Case Design
Each test case validates the deprescribing engine's ability to:
- Screen medications against 2023 AGS Beers Criteria (age >= 65)
- Apply STOPP/START v3 criteria with condition-aware filtering
- Calculate cumulative Anticholinergic Cognitive Burden (ACB) scores
- Detect prescribing cascade patterns
- Compute composite polypharmacy risk scores (0-100)
- Generate PGx overlay insights (unique findings not caught by standard criteria)

### What Constitutes a "Pass"
- **Beers flag detected:** Drug correctly flagged with expected category (avoid/caution)
- **ACB score correct:** Per-drug and cumulative ACB scores match expected values
- **Cascade detected:** Known cascade patterns identified in medication list
- **Polypharmacy score correct:** Composite score falls in expected range/risk level
- **PGx overlay present:** Gene-drug findings correctly attributed as unique or additive

### Test Cases (TC_DEP01-TC_DEP06)

| ID | Scenario | Key Check |
|----|----------|-----------|
| TC_DEP01 | Diphenhydramine in 78yo | Beers=avoid, ACB=3 |
| TC_DEP02 | Lorazepam in 82yo | Beers=avoid (benzodiazepine) |
| TC_DEP03 | Donepezil + oxybutynin | Cascade detected, ACB for oxybutynin |
| TC_DEP04 | 3 high-ACB drugs (oxybutynin + amitriptyline + quetiapine) | Cumulative ACB>=6, risk=high |
| TC_DEP05 | Nortriptyline + CYP2D6 PM | Beers flag + PGx overlay (additive evidence) |
| TC_DEP06 | 12 meds, 3 Beers, 2+ cascades | Polypharmacy score>=70, risk=high |

---

## Metrics

| Metric | Definition |
|--------|-----------|
| **Accuracy** | % of test cases where all checks pass |
| **Sensitivity** | % of individual checks that pass (PGx module) |
| **Critical detection rate** | % of critical-severity expected findings correctly detected |
| **Adverse events prevented** | Count of critical + high findings correctly flagged |

## Current Results (v0.5.0-validated)

- **24 test cases** across 3 modules
- **100% accuracy** (24/24 cases passed)
- **100% sensitivity** (all individual checks passed)
- **100% critical detection rate** (PGx module)
- Execution time: < 0.2 seconds

### By Module
| Module | Cases | Passed | Accuracy |
|--------|-------|--------|----------|
| PGx Interpretation | 12 | 12 | 100% |
| Oncology Gap Analysis | 6 | 6 | 100% |
| Geriatric Deprescribing | 6 | 6 | 100% |

## Adding New Test Cases

### PGx Test Cases
Append to `TEST_CASES` in `src/validation/validator.py`:

```python
{
    "test_id": "TC13",
    "description": "Brief clinical description",
    "therapeutic_area": "area_name",
    "patient": { ... },
    "expected": [
        {"gene": "GENE", "drug": "drug", "expected_severity": "critical",
         "expected_action": "stop_drug", "description": "What this validates"}
    ]
}
```

### Gap Analysis Test Cases
Append to `GAP_TEST_CASES` in `src/validation/validator.py`:

```python
{
    "test_id": "TC_GAP07",
    "description": "Brief description",
    "patient": { ... },  # or "patients": [...] for population tests
    "expected": {
        "min_testing_gaps": 1,
        "must_flag_gene": "DPYD",
        "must_flag_drug": "fluorouracil",
        "expected_gap_severity": "critical",
    }
}
```

### Deprescribing Test Cases
Append to `DEP_TEST_CASES` in `src/validation/validator.py`:

```python
{
    "test_id": "TC_DEP07",
    "description": "Brief description",
    "patient": { ... },
    "expected": {
        "beers_flag_drug": "drug_name",
        "beers_category": "avoid",
        "min_total_acb": 6,
        "min_recommendations": 1,
    }
}
```

Run `python main.py --validate-only` to execute the full 24-case suite.
