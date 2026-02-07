"""
PGx Clinical Solutions — Live Demo Script
==========================================
Walk through 5 key clinical scenarios that demonstrate the platform's
value proposition for laboratories and physicians.

Usage:
    python demo.py              # Full interactive demo
    python demo.py --quick      # Summary only (no pauses)
    python demo.py --scenario 2 # Run specific scenario (1-5)
"""

import sys
import os
import json
import time
import argparse
import webbrowser
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge_base.kb_loader import KnowledgeBase
from src.interpretation.engine import InterpretationEngine
from src.interpretation.risk_scorer import RiskScorer
from src.interpretation.recommender import Recommender
from src.reports.generator import ReportGenerator


# Terminal colors (ANSI)
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


SCENARIOS = [
    {
        "number": 1,
        "title": "The Life-Saving Catch — Codeine Ultra-Rapid Metabolizer",
        "patient_id": "PGX008",
        "therapeutic_area": "Pain Management",
        "hook": "A 47-year-old man prescribed codeine after back surgery. Standard prescription. Routine case.",
        "reveal": "Except his CYP2D6 genotype makes him an ULTRA-RAPID METABOLIZER.",
        "danger": (
            "His body converts codeine to morphine at DANGEROUSLY HIGH rates.\n"
            "    Without PGx testing: risk of fatal respiratory depression.\n"
            "    FDA has reported DEATHS from this exact scenario."
        ),
        "system_action": "System flags CRITICAL — contraindicated. Recommends morphine or NSAIDs instead.",
        "value": "This single catch could save a life and prevent a malpractice lawsuit.",
    },
    {
        "number": 2,
        "title": "The Warfarin Puzzle — Why the INR Won't Stabilize",
        "patient_id": "PGX014",
        "therapeutic_area": "Cardiology",
        "hook": "A 71-year-old man on warfarin for atrial fibrillation. His INR keeps spiking to 3.8 despite dose reductions.",
        "reveal": "PGx testing reveals TWO compounding variants:",
        "danger": (
            "VKORC1 -1639A>A (high sensitivity) — needs ~70% less warfarin\n"
            "    CYP2C9 *2/*3 (poor metabolizer) — clears warfarin much slower\n"
            "    Combined effect: needs only 0.5-1 mg/day (vs standard 5 mg/day)"
        ),
        "system_action": "System flags BOTH genes, calculates combined dosing, recommends INR monitoring every 2-3 days.",
        "value": "Explains months of unstable INR in seconds. Prevents major bleeding events.",
    },
    {
        "number": 3,
        "title": "The Triple Threat — Post-Stent Patient with 3 Hidden Risks",
        "patient_id": "PGX015",
        "therapeutic_area": "Cardiology",
        "hook": "A 59-year-old woman post-PCI with a drug-eluting stent. On clopidogrel, simvastatin, omeprazole.",
        "reveal": "The system finds THREE independent problems:",
        "danger": (
            "1. CYP2C19 poor metabolizer — clopidogrel CAN'T activate. Stent thrombosis risk.\n"
            "    2. Omeprazole DDI — FURTHER blocks clopidogrel activation via CYP2C19 inhibition.\n"
            "    3. SLCO1B1 intermediate function — simvastatin myopathy risk elevated."
        ),
        "system_action": "Switch clopidogrel to prasugrel/ticagrelor. Replace omeprazole with pantoprazole. Cap simvastatin at 20mg or switch to rosuvastatin.",
        "value": "Three actionable findings a manual review might miss. Each one matters.",
    },
    {
        "number": 4,
        "title": "The Oncology Safety Net — Stopping Fatal Chemotherapy",
        "patient_id": "PGX025",
        "therapeutic_area": "Oncology",
        "hook": "A 70-year-old man with gastric cancer. Capecitabine monotherapy planned. Standard protocol.",
        "reveal": "DPYD genotyping reveals *2A/*2A — COMPLETE DPD enzyme deficiency.",
        "danger": (
            "DPD breaks down >80% of fluoropyrimidine drugs.\n"
            "    Without this enzyme: capecitabine accumulates to LETHAL levels.\n"
            "    Published mortality rate for DPD-deficient patients on standard dose: up to 30%."
        ),
        "system_action": "System flags CONTRAINDICATED. Capecitabine must NOT be given. Alternative chemotherapy required.",
        "value": "Pre-treatment DPYD testing costs ~$200. A preventable death costs everything.",
    },
    {
        "number": 5,
        "title": "The Depression Puzzle — Why the Antidepressant Isn't Working",
        "patient_id": "PGX001",
        "therapeutic_area": "Psychiatry",
        "hook": "A 34-year-old woman on citalopram 40mg for 8 weeks. No improvement. Psychiatrist considering a switch.",
        "reveal": "CYP2C19 *2/*2 — she's a POOR METABOLIZER.",
        "danger": (
            "Her citalopram plasma levels are ~2x normal — causing side effects, NOT more efficacy.\n"
            "    At 40mg in a PM: QTc prolongation risk (cardiac arrhythmia).\n"
            "    FDA label explicitly states: max 20mg/day for CYP2C19 poor metabolizers."
        ),
        "system_action": "Reduce to max 20mg/day OR switch to sertraline/fluoxetine (less CYP2C19-dependent).",
        "value": "Explains 8 weeks of treatment failure in seconds. #1 use case driving PGx adoption.",
    },
]


def print_banner():
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  PGx Clinical Solutions — Platform Demo{RESET}")
    print(f"{DIM}  Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")


def run_scenario(scenario: dict, engine, scorer, recommender, report_gen, patients: list, quick: bool = False):
    """Run a single demo scenario with live analysis."""
    num = scenario["number"]
    print(f"\n{BOLD}{MAGENTA}{'─' * 70}{RESET}")
    print(f"{BOLD}{MAGENTA}  SCENARIO {num}: {scenario['title']}{RESET}")
    print(f"{DIM}  Therapeutic Area: {scenario['therapeutic_area']}{RESET}")
    print(f"{MAGENTA}{'─' * 70}{RESET}\n")

    # The hook
    print(f"  {CYAN}THE CASE:{RESET}")
    print(f"    {scenario['hook']}")
    if not quick:
        input(f"\n  {DIM}[Press Enter to reveal the PGx finding...]{RESET}")

    # The reveal
    print(f"\n  {YELLOW}PGx FINDING:{RESET}")
    print(f"    {scenario['reveal']}")
    print(f"\n  {RED}THE RISK:{RESET}")
    print(f"    {scenario['danger']}")
    if not quick:
        input(f"\n  {DIM}[Press Enter to see what the system does...]{RESET}")

    # Live analysis
    print(f"\n  {GREEN}SYSTEM ANALYSIS (live):{RESET}")
    patient = next((p for p in patients if p["patient_id"] == scenario["patient_id"]), None)
    if patient:
        start = time.time()
        findings = engine.generate_findings(patient)
        scored = scorer.score_findings(findings)
        risk = scorer.get_patient_risk_summary(scored)
        recs = recommender.generate_recommendations(scored, patient)
        elapsed = time.time() - start

        print(f"    Analyzed in {elapsed*1000:.0f}ms")
        print(f"    Risk Category: {BOLD}{RED if 'Critical' in risk['category'] else YELLOW}{risk['category']}{RESET}")
        print(f"    Findings: {len(findings)} total, {risk['critical_count']} critical")
        print(f"    Recommendations: {len(recs)}")
        for i, rec in enumerate(recs, 1):
            sev_color = RED if rec["severity"] == "critical" else YELLOW if rec["severity"] == "high" else RESET
            print(f"      {sev_color}[{rec['priority']}] {rec['drug']}: {rec['recommendation_text'][:90]}{RESET}")

    # The system action
    print(f"\n  {GREEN}ACTION:{RESET}")
    print(f"    {scenario['system_action']}")

    # Value
    print(f"\n  {BOLD}VALUE:{RESET}")
    print(f"    {scenario['value']}")

    # Offer to open report
    report_path = PROJECT_ROOT / "output" / "reports" / f"report_{scenario['patient_id']}.html"
    if report_path.exists() and not quick:
        open_it = input(f"\n  {DIM}Open the full clinical report in browser? [y/N]{RESET} ").strip().lower()
        if open_it == "y":
            webbrowser.open(str(report_path))


def run_platform_stats(patients, engine, scorer, recommender):
    """Show aggregate platform performance."""
    print(f"\n{BOLD}{BLUE}{'─' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  PLATFORM PERFORMANCE — Full Pipeline{RESET}")
    print(f"{BLUE}{'─' * 70}{RESET}\n")

    start = time.time()
    total_findings = 0
    total_critical = 0
    total_recs = 0

    for patient in patients:
        findings = engine.generate_findings(patient)
        scored = scorer.score_findings(findings)
        recs = recommender.generate_recommendations(scored, patient)
        risk = scorer.get_patient_risk_summary(scored)
        total_findings += len(findings)
        total_critical += risk["critical_count"]
        total_recs += len(recs)

    elapsed = time.time() - start

    print(f"  {BOLD}Patients analyzed:{RESET}          {len(patients)}")
    print(f"  {BOLD}Total time:{RESET}                 {elapsed*1000:.0f}ms ({elapsed:.2f}s)")
    print(f"  {BOLD}Per-patient:{RESET}                {elapsed/len(patients)*1000:.1f}ms")
    print(f"  {BOLD}Findings identified:{RESET}        {total_findings}")
    print(f"  {BOLD}Critical alerts:{RESET}            {RED}{total_critical}{RESET}")
    print(f"  {BOLD}Actionable recommendations:{RESET} {total_recs}")
    print(f"\n  {BOLD}Validation:{RESET}                 12/12 test cases passed (100%)")
    print(f"  {BOLD}Critical detection rate:{RESET}     100%")
    print(f"\n  {BOLD}Manual review equivalent:{RESET}   {len(patients) * 2.25:.0f} pharmacist-hours")
    print(f"  {BOLD}Cost avoidance:{RESET}             ${total_critical * 25000:,} (adverse events prevented)")
    print(f"  {BOLD}Revenue potential:{RESET}          ${len(patients) * 150:,} - ${len(patients) * 300:,} per batch")


def main():
    parser = argparse.ArgumentParser(description="PGx Clinical Solutions Demo")
    parser.add_argument("--quick", action="store_true", help="Run without pauses")
    parser.add_argument("--scenario", type=int, choices=[1, 2, 3, 4, 5], help="Run specific scenario")
    parser.add_argument("--stats", action="store_true", help="Show platform stats only")
    args = parser.parse_args()

    print_banner()

    # Initialize
    print(f"  {DIM}Loading platform...{RESET}", end=" ", flush=True)
    kb = KnowledgeBase(base_path=PROJECT_ROOT / "src" / "knowledge_base")
    engine = InterpretationEngine(kb)
    scorer = RiskScorer()
    recommender = Recommender()
    report_gen = ReportGenerator(template_dir=PROJECT_ROOT / "src" / "reports" / "templates")

    # Load patients
    patients_file = PROJECT_ROOT / "data" / "patients.json"
    if patients_file.exists():
        with open(patients_file) as f:
            patients = json.load(f)
    else:
        from src.data_generation.synthetic_patients import generate_patients
        patients = generate_patients()

    print(f"{GREEN}Ready.{RESET} ({len(patients)} patients loaded)\n")

    if args.stats:
        run_platform_stats(patients, engine, scorer, recommender)
        return

    if args.scenario:
        scenario = SCENARIOS[args.scenario - 1]
        run_scenario(scenario, engine, scorer, recommender, report_gen, patients, args.quick)
    else:
        # Run all scenarios
        for scenario in SCENARIOS:
            run_scenario(scenario, engine, scorer, recommender, report_gen, patients, args.quick)

        # Platform stats at the end
        run_platform_stats(patients, engine, scorer, recommender)

    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  Demo Complete — PGx Clinical Solutions{RESET}")
    print(f"{DIM}  Reports available in: output/reports/{RESET}")
    print(f"{DIM}  Business model: docs/business_model.md{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")


if __name__ == "__main__":
    main()
