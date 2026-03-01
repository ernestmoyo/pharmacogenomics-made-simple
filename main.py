"""
PGx Clinical Solutions - Pharmacogenomics Interpretation Platform
================================================================
Main orchestrator that runs the complete pipeline:
1. Load knowledge base
2. Generate/load synthetic patient data
3. Run interpretation engine on each patient
4. Generate clinical reports
5. Run validation suite
6. Output impact metrics

Usage:
    python main.py                  # Full pipeline
    python main.py --patients-only  # Generate patient data only
    python main.py --validate-only  # Run validation only
    python main.py --report PGX001  # Generate report for specific patient
"""

import json
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger, PLATFORM_VERSION
from src.knowledge_base.kb_loader import KnowledgeBase
from src.data_generation.synthetic_patients import generate_patients, generate_oncology_gap_patients
from src.interpretation.engine import InterpretationEngine
from src.interpretation.risk_scorer import RiskScorer
from src.interpretation.recommender import Recommender
from src.reports.generator import ReportGenerator
from src.validation.validator import ClinicalValidator

logger = get_logger("main")


def write_audit_trail(output_dir: Path, module: str, patients_count: int,
                      findings_count: int, critical_count: int,
                      metrics: dict, kb: KnowledgeBase, elapsed: float):
    """Append a run record to the audit trail."""
    audit_path = output_dir / "logs" / "audit_trail.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing trail
    trail = []
    if audit_path.exists():
        try:
            with open(audit_path, "r", encoding="utf-8") as f:
                trail = json.load(f)
        except (json.JSONDecodeError, ValueError):
            trail = []

    record = {
        "run_id": f"RUN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "platform_version": PLATFORM_VERSION,
        "module": module,
        "patients_analyzed": patients_count,
        "findings_generated": findings_count,
        "critical_alerts": critical_count,
        "validation_accuracy": f"{metrics.get('accuracy', 0):.1%}" if metrics else "N/A",
        "kb_versions": kb.get_kb_versions() if kb else {},
        "execution_time_seconds": round(elapsed, 2),
    }
    trail.append(record)

    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(trail, f, indent=2)

    logger.debug(f"Audit trail updated: {record['run_id']}")


def load_or_generate_patients(data_dir: Path, force_regenerate: bool = False) -> list:
    """Load existing patient data or generate new synthetic patients."""
    patients_file = data_dir / "patients.json"

    if patients_file.exists() and not force_regenerate:
        logger.info(f"Loading existing patient data from {patients_file}")
        with open(patients_file, "r") as f:
            patients = json.load(f)
        logger.info(f"Loaded {len(patients)} patients")
        return patients

    logger.info("Generating synthetic patient profiles...")
    patients = generate_patients()
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(patients_file, "w") as f:
        json.dump(patients, f, indent=2)
    logger.info(f"Generated and saved {len(patients)} patients to {patients_file}")
    return patients


def analyze_single_patient(engine: InterpretationEngine, scorer: RiskScorer,
                           recommender: Recommender, patient: dict) -> dict:
    """Run the full interpretation pipeline for a single patient."""
    findings = engine.generate_findings(patient)
    scored_findings = scorer.score_findings(findings)
    risk_summary = scorer.get_patient_risk_summary(scored_findings)
    recommendations = recommender.generate_recommendations(scored_findings, patient)

    medications = [med if isinstance(med, str) else med.get("name", "") for med in patient.get("medications", [])]
    drug_drug_interactions = engine.kb.get_drug_drug_interactions(medications)

    return {
        "patient_id": patient.get("patient_id", "UNKNOWN"),
        "findings": findings,
        "scored_findings": scored_findings,
        "recommendations": recommendations,
        "risk_summary": risk_summary,
        "drug_drug_interactions": drug_drug_interactions,
    }


def run_full_pipeline(args):
    """Execute the complete PGx interpretation pipeline."""
    start_time = time.time()
    output_dir = PROJECT_ROOT / "output"
    reports_dir = output_dir / "reports"
    data_dir = PROJECT_ROOT / "data"
    reports_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("PGx Clinical Solutions - Interpretation Platform v%s", PLATFORM_VERSION)
    logger.info("=" * 60)

    # Step 1: Load knowledge base
    logger.info("[1/6] Loading pharmacogenomics knowledge base...")
    kb = KnowledgeBase(base_path=PROJECT_ROOT / "src" / "knowledge_base")

    # Step 2: Load or generate patients
    logger.info("[2/6] Preparing patient data...")
    patients = load_or_generate_patients(data_dir, force_regenerate=args.regenerate)

    # Step 3: Initialize interpretation components
    logger.info("[3/6] Initializing interpretation engine...")
    engine = InterpretationEngine(kb)
    scorer = RiskScorer()
    recommender = Recommender()
    logger.info("Engine, scorer, and recommender initialized")

    # Step 4: Analyze all patients
    logger.info("[4/6] Analyzing patients...")
    all_results = {}
    total_findings = 0
    total_critical = 0
    total_recommendations = 0

    for i, patient in enumerate(patients):
        pid = patient.get("patient_id", f"UNKNOWN_{i}")
        results = analyze_single_patient(engine, scorer, recommender, patient)
        all_results[pid] = results

        n_findings = len(results["findings"])
        n_critical = results["risk_summary"].get("critical_count", 0)
        n_recs = len(results["recommendations"])
        total_findings += n_findings
        total_critical += n_critical
        total_recommendations += n_recs

        risk_cat = results["risk_summary"].get("category", "Unknown")
        logger.info(f"[{i+1}/{len(patients)}] {pid}: {n_findings} findings, "
                    f"{n_critical} critical, {n_recs} recommendations [{risk_cat}]")

    logger.info(f"Analysis complete: {total_findings} total findings, "
                f"{total_critical} critical alerts, {total_recommendations} recommendations")

    # Step 5: Generate reports
    logger.info("[5/6] Generating clinical reports...")
    report_gen = ReportGenerator(template_dir=PROJECT_ROOT / "src" / "reports" / "templates")

    if args.report:
        if args.report in all_results:
            patient = next(p for p in patients if p.get("patient_id") == args.report)
            results = all_results[args.report]
            report_path = reports_dir / f"report_{args.report}.html"
            report_gen.generate_and_save(patient, results, report_path)
            logger.info(f"Generated report: {report_path}")
        else:
            logger.warning(f"Patient {args.report} not found!")
    else:
        for patient in patients:
            pid = patient.get("patient_id", "UNKNOWN")
            if pid in all_results:
                report_path = reports_dir / f"report_{pid}.html"
                report_gen.generate_and_save(patient, all_results[pid], report_path)
        logger.info(f"Generated {len(all_results)} clinical reports in {reports_dir}")

    # Save analysis summary
    summary_path = output_dir / "analysis_summary.json"
    summary_data = {}
    for pid, results in all_results.items():
        summary_data[pid] = {
            "risk_summary": results["risk_summary"],
            "finding_count": len(results["findings"]),
            "recommendation_count": len(results["recommendations"]),
            "critical_findings": [
                f.get("summary", "") for f in results["scored_findings"]
                if f.get("severity") == "critical"
            ],
        }
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    logger.info(f"Saved analysis summary to {summary_path}")

    # Step 6: Run validation
    logger.info("[6/6] Running clinical validation suite...")
    validator = ClinicalValidator()
    validation_results = validator.run_validation(engine, scorer, recommender)
    metrics = validator.calculate_metrics(validation_results)
    impact_report = validator.generate_impact_report(validation_results, metrics)

    validation_path = output_dir / "validation_report.txt"
    with open(validation_path, "w") as f:
        f.write(impact_report)
    logger.info(f"Validation report saved to {validation_path}")

    # Final summary
    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Patients analyzed:          {len(patients)}")
    logger.info(f"Total findings:             {total_findings}")
    logger.info(f"Critical alerts:            {total_critical}")
    logger.info(f"Actionable recommendations: {total_recommendations}")
    logger.info(f"Reports generated:          {len(all_results)}")
    logger.info(f"Validation accuracy:        {metrics.get('accuracy', 0):.1%}")
    logger.info(f"Critical detection rate:    {metrics.get('critical_finding_detection_rate', 0):.1%}")
    logger.info(f"Adverse events preventable: {metrics.get('adverse_events_prevented', 0)}")
    logger.info(f"Est. time saved per report: {metrics.get('time_saved_per_report_hours', 0):.1f} hours")
    logger.info(f"Pipeline execution time:    {elapsed:.1f} seconds")
    logger.info(f"Output directory: {output_dir}")
    logger.info("=" * 60)

    # Write audit trail
    write_audit_trail(output_dir, "standard", len(patients),
                      total_findings, total_critical, metrics, kb, elapsed)

    return all_results, metrics


def run_validation_only(args):
    """Run validation suite only."""
    start_time = time.time()
    logger.info("Loading knowledge base and running validation...")
    kb = KnowledgeBase(base_path=PROJECT_ROOT / "src" / "knowledge_base")
    engine = InterpretationEngine(kb)
    scorer = RiskScorer()
    recommender = Recommender()
    validator = ClinicalValidator()

    validation_results = validator.run_validation(engine, scorer, recommender)
    metrics = validator.calculate_metrics(validation_results)
    impact_report = validator.generate_impact_report(validation_results, metrics)

    # Print to console for visibility
    print(impact_report)

    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "validation_report.txt", "w") as f:
        f.write(impact_report)

    elapsed = time.time() - start_time
    write_audit_trail(output_dir, "validation", 0, 0, 0, metrics, kb, elapsed)


def run_oncology_gap(args):
    """Run oncology PGx gap analysis on synthetic oncology cohort."""
    start_time = time.time()
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("PGx Clinical Solutions - Oncology Gap Analysis v%s", PLATFORM_VERSION)
    logger.info("=" * 60)

    # Step 1: Load knowledge base
    logger.info("[1/5] Loading pharmacogenomics knowledge base...")
    kb = KnowledgeBase(base_path=PROJECT_ROOT / "src" / "knowledge_base")

    # Step 2: Generate oncology gap patients
    logger.info("[2/5] Generating oncology gap analysis cohort...")
    patients = generate_oncology_gap_patients()
    logger.info(f"Generated {len(patients)} oncology gap analysis patients")

    # Step 3: Initialize analysis components
    logger.info("[3/5] Initializing gap analysis engine...")
    from src.oncology_gap.gap_analyzer import GapAnalyzer
    from src.oncology_gap.ddi_burden_scorer import DDIBurdenScorer
    from src.oncology_gap.population_analytics import PopulationAnalytics

    engine = InterpretationEngine(kb)
    gap_analyzer = GapAnalyzer(kb, engine)
    ddi_scorer = DDIBurdenScorer(kb)
    pop_analytics = PopulationAnalytics()

    # Step 4: Analyze cohort
    logger.info("[4/5] Analyzing oncology cohort for PGx gaps...")
    gap_results = gap_analyzer.analyze_cohort(patients)
    ddi_results = ddi_scorer.score_cohort(patients)
    population_summary = pop_analytics.summarize(gap_results, ddi_results)

    # Step 5: Output results
    logger.info("[5/5] Generating gap analysis output...")

    # Save detailed results
    gap_output_dir = output_dir / "oncology_gap"
    gap_output_dir.mkdir(parents=True, exist_ok=True)

    with open(gap_output_dir / "gap_results.json", "w", encoding="utf-8") as f:
        json.dump(gap_results, f, indent=2, default=str)

    with open(gap_output_dir / "ddi_burden.json", "w", encoding="utf-8") as f:
        json.dump(ddi_results, f, indent=2, default=str)

    with open(gap_output_dir / "population_summary.json", "w", encoding="utf-8") as f:
        json.dump(population_summary, f, indent=2, default=str)

    # Print console summary
    elapsed = time.time() - start_time
    _print_gap_summary(population_summary, gap_results, elapsed)

    # Audit trail
    total_gaps = population_summary.get("gap_summary", {}).get("total_gaps", 0)
    total_missed = population_summary.get("missed_interventions", {}).get("total_missed_interventions", 0)
    write_audit_trail(output_dir, "oncology_gap", len(patients),
                      total_gaps + total_missed, total_missed, {}, kb, elapsed)

    return gap_results, population_summary


def _print_gap_summary(summary: dict, gap_results: list, elapsed: float):
    """Print a formatted gap analysis summary to the console."""
    n = summary.get("cohort_size", 0)
    exposure = summary.get("pgx_drug_exposure", {})
    testing = summary.get("testing_rates", {})
    gaps = summary.get("gap_summary", {})
    missed = summary.get("missed_interventions", {})
    compliance = summary.get("compliance_summary", {})
    ddi = summary.get("ddi_summary", {})

    print()
    print("=" * 72)
    print("  PGx CLINICAL SOLUTIONS — ONCOLOGY GAP ANALYSIS REPORT")
    print("  Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya")
    print("=" * 72)
    print()
    print("COHORT OVERVIEW")
    print("-" * 40)
    print(f"  Patients analyzed:            {n}")
    print(f"  Patients on PGx-relevant drugs: {exposure.get('patients_on_pgx_drugs', 0)} "
          f"({exposure.get('percent_on_pgx_drugs', 0)}%)")
    print(f"  Avg PGx drugs per patient:    {exposure.get('avg_pgx_drugs_per_patient', 0)}")
    print()
    print("TESTING RATES")
    print("-" * 40)
    print(f"  Overall testing rate:         {testing.get('overall_rate', 0)}%")
    print(f"  Patients fully tested:        {testing.get('patients_fully_tested', 0)}")
    print(f"  Patients with NO testing:     {testing.get('patients_not_tested', 0)}")

    by_gene = testing.get("by_gene", {})
    if by_gene:
        print()
        print("  Testing by Gene:")
        for gene, info in sorted(by_gene.items()):
            print(f"    {gene:10s}: {info['tested']}/{info['total']} tested ({info['rate']}%)")

    print()
    print("GAP ANALYSIS")
    print("-" * 40)
    print(f"  Patients with testing gaps:   {gaps.get('patients_with_gaps', 0)} "
          f"({gaps.get('percent_with_gaps', 0)}%)")
    print(f"  Total testing gaps:           {gaps.get('total_gaps', 0)}")
    by_sev = gaps.get("by_severity", {})
    if by_sev:
        for sev in ["critical", "high", "moderate"]:
            if sev in by_sev:
                print(f"    {sev:10s}: {by_sev[sev]}")

    print()
    print("MISSED INTERVENTIONS")
    print("-" * 40)
    print(f"  Patients with missed actions: {missed.get('patients_with_missed_interventions', 0)} "
          f"({missed.get('percent_with_missed', 0)}%)")
    print(f"  Total missed interventions:   {missed.get('total_missed_interventions', 0)}")
    by_action = missed.get("by_action_type", {})
    if by_action:
        for action, count in sorted(by_action.items(), key=lambda x: -x[1]):
            print(f"    {action:20s}: {count}")

    print()
    print("COMPLIANCE")
    print("-" * 40)
    print(f"  Fully compliant patients:     {compliance.get('fully_compliant_patients', 0)} "
          f"({compliance.get('percent_compliant', 0)}%)")

    print()
    print("DDI BURDEN")
    print("-" * 40)
    print(f"  Total DDIs detected:          {ddi.get('total_ddis', 0)}")
    print(f"  PGx-relevant DDIs:            {ddi.get('pgx_relevant_ddis', 0)}")
    print(f"  Avg weighted DDI score:       {ddi.get('avg_weighted_score', 0)}")

    # Top gaps
    top_gaps = summary.get("top_gaps", [])
    if top_gaps:
        print()
        print("TOP TESTING GAPS")
        print("-" * 40)
        for gap in top_gaps[:5]:
            print(f"  {gap['gene']:10s} — {gap['drug']:15s} "
                  f"[CPIC {gap['cpic_level']}] "
                  f"{'FDA' if gap['fda_label'] else '   '} "
                  f"{gap['patient_count']} patients ({gap['percent_of_cohort']}%)")

    # Per-patient summary
    print()
    print("PER-PATIENT RESULTS")
    print("-" * 40)
    for r in gap_results:
        pid = r["patient_id"]
        sev = r["gap_severity"]
        n_gaps = r["testing_gap_count"]
        n_missed = r["missed_intervention_count"]
        rate = r["testing_rate"]
        icon = {"critical": "!!!", "high": "!!", "moderate": "!", "none": "OK"}
        print(f"  [{icon.get(sev, '?'):3s}] {pid:8s}: "
              f"{n_gaps} gaps, {n_missed} missed, "
              f"{rate}% tested [{sev}]")

    print()
    print(f"  Execution time: {elapsed:.2f} seconds")
    print("  Output: output/oncology_gap/")
    print("=" * 72)


def run_patients_only(args):
    """Generate patient data only."""
    data_dir = PROJECT_ROOT / "data"
    patients = load_or_generate_patients(data_dir, force_regenerate=True)
    logger.info(f"Generated {len(patients)} patients")
    for p in patients:
        pid = p.get("patient_id", "?")
        area = p.get("clinical_context", {}).get("therapeutic_area", "unknown")
        n_meds = len(p.get("medications", []))
        logger.info(f"  {pid}: {area}, {n_meds} medications")


def main():
    parser = argparse.ArgumentParser(
        description="PGx Clinical Solutions - Pharmacogenomics Interpretation Platform"
    )
    parser.add_argument("--patients-only", action="store_true",
                        help="Generate patient data only")
    parser.add_argument("--validate-only", action="store_true",
                        help="Run validation suite only")
    parser.add_argument("--report", type=str, default=None,
                        help="Generate report for specific patient ID")
    parser.add_argument("--regenerate", action="store_true",
                        help="Force regeneration of patient data")
    parser.add_argument("--oncology-gap", action="store_true",
                        help="Run oncology PGx gap analysis")

    args = parser.parse_args()

    if args.patients_only:
        run_patients_only(args)
    elif args.validate_only:
        run_validation_only(args)
    elif args.oncology_gap:
        run_oncology_gap(args)
    else:
        run_full_pipeline(args)


if __name__ == "__main__":
    main()
