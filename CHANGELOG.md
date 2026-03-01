# Changelog

All notable changes to the PGx Clinical Solutions platform will be documented in this file.

Format follows [Semantic Versioning](https://semver.org/).

---

## [0.3.0] - 2026-03-01

### Added
- **Oncology Gap Analysis Module** (`src/oncology_gap/`):
  - `gap_analyzer.py` — identifies PGx testing gaps and missed interventions per patient
  - `ddi_burden_scorer.py` — quantifies DDI load with severity-weighted scoring
  - `population_analytics.py` — aggregates gap statistics across patient cohorts
- 15 synthetic oncology gap analysis patients in `synthetic_patients.py`:
  - 5 gap patients (PGx-relevant drugs, no testing)
  - 5 missed intervention patients (testing done, actionable results, no action)
  - 3 compliant patients (fully tested, results appropriate)
  - 2 complex DDI patients (multiple PGx interactions)
- `--oncology-gap` CLI mode in `main.py`
- JSON output to `output/oncology_gap/` (gap_results, ddi_burden, population_summary)
- Formatted console report with cohort overview, testing rates, gap analysis, missed interventions

---

## [0.3.0-kb] - 2026-03-01

### Added
- `pgx_drug_map.json` — 39 drugs mapped to pharmacogenes across 7 therapeutic areas with CPIC levels, FDA label status, and testing recommendations
- `beers_criteria.json` — 45 entries from the 2023 AGS Beers Criteria for potentially inappropriate medications in older adults
- `stopp_start_criteria.json` — 20 STOPP criteria (medications to stop) + 10 START criteria (medications to start) from STOPP/START v3
- `anticholinergic_burden.json` — 97 medications scored on the Anticholinergic Cognitive Burden (ACB) scale (0-3) with risk thresholds
- `prescribing_cascades.json` — 15 well-documented prescribing cascade patterns with PGx relevance annotations
- New `KnowledgeBase` lookup methods: `get_pgx_relevant_genes()`, `get_pgx_drug_info()`, `get_beers_flag()`, `get_stopp_flags()`, `get_start_flags()`, `get_acb_score()`, `get_total_acb_score()`, `get_prescribing_cascades()`

### Changed
- `kb_loader.py` now loads all 8 knowledge base files and builds indexes for fast lookups
- `get_kb_versions()` includes all KB files in version tracking
- KB load summary now reports PGx-mapped drug count, Beers entries, and ACB-scored medications

---

## [0.2.0] - 2026-03-01

### Added
- Centralized logging system (`src/utils/logger.py`) with console + file handlers
- Audit trail system — every pipeline run recorded to `output/logs/audit_trail.json`
- Version metadata (`_metadata`) on all knowledge base JSON files
- `CHANGELOG.md` for version tracking
- `docs/standards/` directory with clinical references, validation methodology, and data provenance documentation
- `get_kb_versions()` method on KnowledgeBase class
- Platform version constant (`PLATFORM_VERSION`) as single source of truth

### Changed
- Replaced all `print()` statements with Python `logging` module across all modules
- Report metadata now uses `PLATFORM_VERSION` instead of hardcoded version string
- `.gitignore` updated to exclude `output/` directory and `nul` artifact

### Removed
- `nul` file (Windows artifact) from project root

---

## [0.1.0] - 2026-02-08

### Added
- Initial MVP release
- Knowledge base: 21 gene-drug interactions across 10 genes, 14 DDIs, dosing guidelines
- Interpretation engine with gene-drug, DDI, phenoconversion, renal/hepatic analysis
- Risk scoring system (0-100 scale) with evidence quality weighting
- Clinical recommendation generator with prioritization and alternatives
- 25 synthetic patients across 4 therapeutic areas (psychiatry, oncology, pain management, cardiology)
- Professional HTML clinical report generation via Jinja2
- Clinical validation suite: 12 test cases, 100% accuracy
- Business model documentation
- CSV data exports
