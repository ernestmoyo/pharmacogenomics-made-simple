# Data Provenance

Source documentation for all knowledge base datasets in the PGx Clinical Solutions platform.

## Knowledge Base Files

### gene_drug_interactions.json (v1.0.0)
- **Content:** 21 gene-drug interaction pairs across 10 pharmacogenes
- **Primary sources:** CPIC Guidelines, FDA Pharmacogenomic Biomarkers Table, PharmGKB
- **Date of extraction:** February 2026
- **Coverage:**
  - CYP2D6: codeine, tramadol, oxycodone, nortriptyline, tamoxifen, ondansetron, atomoxetine
  - CYP2C19: citalopram, escitalopram, sertraline, clopidogrel
  - CYP2C9: warfarin
  - VKORC1: warfarin
  - SLCO1B1: simvastatin, atorvastatin
  - DPYD: fluorouracil, capecitabine
  - UGT1A1: irinotecan
  - TPMT: mercaptopurine
  - CYP3A4: tacrolimus
  - HLA-B: carbamazepine
- **Simplifications:** Phenotype categories simplified to major metabolizer groups (poor, intermediate, normal, ultra-rapid). Sub-populations (e.g., CYP2D6 *10 allele frequency in Asian populations) not yet modeled.

### drug_drug_interactions.json (v1.0.0)
- **Content:** 14 drug-drug interaction pairs + CYP inhibitor/inducer tables
- **Primary sources:** CPIC Guidelines, FDA Drug Interaction Labeling, Clinical pharmacology references
- **Date of extraction:** February 2026
- **Scope:** Focused on pharmacokinetic interactions involving CYP enzymes with known pharmacogenomic variability
- **Simplifications:** Only major and moderate DDIs included. Pharmacodynamic interactions (e.g., serotonin syndrome) not yet modeled.

### dosing_guidelines.json (v1.0.0)
- **Content:** Drug-specific dosing tables, renal adjustments, hepatic adjustments
- **Primary sources:** CPIC Dosing Guidelines, FDA Approved Labeling, KDIGO Guidelines
- **Date of extraction:** February 2026
- **Simplifications:** Warfarin dosing uses simplified table rather than full IWPC algorithm. Renal adjustments use eGFR cutoffs rather than continuous functions.

## Synthetic Patient Data

### data/patients.json
- **Content:** 25 synthetic patients
- **Generation:** Deterministic algorithm with seed=42 for reproducibility
- **NOT derived from real patient data** — all demographics, genotypes, and medication profiles are fictional
- **Design intent:** Cover a range of metabolizer phenotypes, ethnic backgrounds, and therapeutic scenarios across 4 areas

## Update Process

When clinical guidelines are updated:
1. Update the relevant JSON file with new data
2. Increment the `_metadata.version` field
3. Update `_metadata.last_updated` date
4. Update `_metadata.sources` if new references are added
5. Run `python main.py --validate-only` to confirm no regressions
6. Document changes in `CHANGELOG.md`
