# Validation Methodology

How the PGx Clinical Solutions platform validates clinical accuracy.

## Overview

The platform uses a suite of pre-defined clinical test cases, each representing a known pharmacogenomic scenario with an expected clinical outcome. Test cases are run through the full interpretation pipeline (engine + scoring + recommendations) and compared against expected findings.

## Test Case Design

Each test case includes:
1. **Synthetic patient** with specific genotype and medication profile
2. **Expected findings** — which gene-drug interactions should be detected
3. **Expected severity** — the minimum severity level (critical, high, moderate)
4. **Expected action** — what clinical action should be recommended (stop, switch, reduce dose)

### Test Case Criteria
- At least one test case per high-risk gene-drug pair in the knowledge base
- Coverage across all four therapeutic areas (psychiatry, oncology, pain management, cardiology)
- DDI and phenoconversion scenarios included
- Both single-drug and multi-drug interaction scenarios

## What Constitutes a "Pass"

A test case passes when ALL of the following are true:
1. **Finding detected:** The expected gene-drug interaction is present in the output findings
2. **Severity correct:** The assigned severity matches the expected severity (critical >= high is accepted as conservative)
3. **Action appropriate:** The recommended action type is clinically appropriate for the scenario

## Metrics

| Metric | Definition |
|--------|-----------|
| **Accuracy** | % of test cases where all checks pass |
| **Sensitivity** | % of individual checks (finding + severity) that pass |
| **Critical detection rate** | % of critical-severity expected findings correctly detected |
| **Adverse events prevented** | Count of critical + high findings correctly flagged |

## Current Results (v0.2.0)

- **12 test cases** across 4 therapeutic areas
- **100% accuracy** (12/12 cases passed)
- **100% sensitivity** (15/15 individual checks passed)
- **100% critical detection rate**

## Adding New Test Cases

To add a test case, append to the `TEST_CASES` list in `src/validation/validator.py`:

```python
{
    "test_id": "TC_NEW01",
    "description": "Brief clinical description",
    "therapeutic_area": "area_name",
    "patient": {
        "patient_id": "VAL_NEW01",
        "demographics": {...},
        "genotype": {...},
        "medications": [...],
        "lab_values": {...},
        "clinical_context": {...}
    },
    "expected": [
        {
            "gene": "GENE_NAME",
            "drug": "drug_name",
            "expected_severity": "critical|high|moderate",
            "expected_action": "stop_drug|switch_drug|reduce_dose",
            "description": "What this check validates"
        }
    ]
}
```

Run `python main.py --validate-only` to execute the updated suite.
