# Changelog

All notable changes to the PGx Clinical Solutions platform will be documented in this file.

Format follows [Semantic Versioning](https://semver.org/).

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
