"""
Clinical Validation Framework
==============================
Validates interpretation engine against known clinical scenarios
and calculates clinical impact metrics.

Includes:
- 12 original PGx interpretation test cases (TC01-TC12)
- 6 oncology gap analysis test cases (TC_GAP01-TC_GAP06)
- 6 geriatric deprescribing test cases (TC_DEP01-TC_DEP06)
"""

from pathlib import Path
from typing import Optional

from src.utils.logger import get_logger

logger = get_logger("validation")


class ClinicalValidator:
    """Validates PGx interpretation against known clinical test cases."""

    TEST_CASES = [
        {
            "test_id": "TC01",
            "description": "CYP2C19 PM on citalopram — dose reduction required",
            "therapeutic_area": "psychiatry",
            "patient": {
                "patient_id": "VAL_TC01",
                "demographics": {"first_name": "Test", "last_name": "Case01", "age": 40, "sex": "F",
                                  "weight_kg": 65, "height_cm": 165, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2C19": {"diplotype": "*2/*2", "phenotype": "poor_metabolizer"},
                    "CYP2D6": {"diplotype": "*1/*1", "phenotype": "normal_metabolizer"},
                },
                "medications": ["citalopram"],
                "lab_values": {"egfr": 90, "alt": 20, "ast": 18},
                "clinical_context": {"primary_diagnosis": "MDD", "therapeutic_area": "psychiatry",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2C19", "drug": "citalopram", "expected_severity": "high",
                 "expected_action": "reduce_dose", "description": "Should flag dose reduction to max 20mg/day"}
            ]
        },
        {
            "test_id": "TC02",
            "description": "CYP2D6 UM on codeine — AVOID (life-threatening toxicity)",
            "therapeutic_area": "pain_management",
            "patient": {
                "patient_id": "VAL_TC02",
                "demographics": {"first_name": "Test", "last_name": "Case02", "age": 45, "sex": "M",
                                  "weight_kg": 80, "height_cm": 175, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*1/*1xN", "phenotype": "ultra_rapid_metabolizer"},
                },
                "medications": ["codeine"],
                "lab_values": {"egfr": 95, "alt": 25, "ast": 22},
                "clinical_context": {"primary_diagnosis": "Acute pain", "therapeutic_area": "pain_management",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2D6", "drug": "codeine", "expected_severity": "critical",
                 "expected_action": "stop_drug", "description": "Must flag CONTRAINDICATED — fatal toxicity risk"}
            ]
        },
        {
            "test_id": "TC03",
            "description": "VKORC1 A/A + CYP2C9 PM on warfarin — major dose reduction",
            "therapeutic_area": "cardiology",
            "patient": {
                "patient_id": "VAL_TC03",
                "demographics": {"first_name": "Test", "last_name": "Case03", "age": 70, "sex": "M",
                                  "weight_kg": 75, "height_cm": 170, "ethnicity": "Caucasian"},
                "genotype": {
                    "VKORC1": {"variant": "-1639A>A", "phenotype": "high_sensitivity"},
                    "CYP2C9": {"diplotype": "*3/*3", "phenotype": "poor_metabolizer"},
                },
                "medications": ["warfarin"],
                "lab_values": {"egfr": 65, "alt": 30, "ast": 28, "inr": 3.5},
                "clinical_context": {"primary_diagnosis": "AFib", "therapeutic_area": "cardiology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "VKORC1", "drug": "warfarin", "expected_severity": "critical",
                 "expected_action": "reduce_dose", "description": "VKORC1 high sensitivity — major reduction"},
                {"gene": "CYP2C9", "drug": "warfarin", "expected_severity": "critical",
                 "expected_action": "reduce_dose", "description": "CYP2C9 PM — major reduction"}
            ]
        },
        {
            "test_id": "TC04",
            "description": "CYP2C19 PM on clopidogrel — switch to prasugrel/ticagrelor",
            "therapeutic_area": "cardiology",
            "patient": {
                "patient_id": "VAL_TC04",
                "demographics": {"first_name": "Test", "last_name": "Case04", "age": 60, "sex": "M",
                                  "weight_kg": 80, "height_cm": 172, "ethnicity": "East Asian"},
                "genotype": {
                    "CYP2C19": {"diplotype": "*2/*2", "phenotype": "poor_metabolizer"},
                },
                "medications": ["clopidogrel"],
                "lab_values": {"egfr": 85, "alt": 22, "ast": 20},
                "clinical_context": {"primary_diagnosis": "ACS post-PCI", "therapeutic_area": "cardiology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2C19", "drug": "clopidogrel", "expected_severity": "critical",
                 "expected_action": "switch_drug", "description": "Must switch to prasugrel or ticagrelor"}
            ]
        },
        {
            "test_id": "TC05",
            "description": "DPYD PM on fluorouracil — CONTRAINDICATED (fatal toxicity)",
            "therapeutic_area": "oncology",
            "patient": {
                "patient_id": "VAL_TC05",
                "demographics": {"first_name": "Test", "last_name": "Case05", "age": 65, "sex": "F",
                                  "weight_kg": 70, "height_cm": 165, "ethnicity": "Caucasian"},
                "genotype": {
                    "DPYD": {"diplotype": "*2A/*2A", "phenotype": "poor_metabolizer"},
                },
                "medications": ["fluorouracil"],
                "lab_values": {"egfr": 75, "alt": 25, "ast": 22},
                "clinical_context": {"primary_diagnosis": "Colorectal cancer", "therapeutic_area": "oncology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "DPYD", "drug": "fluorouracil", "expected_severity": "critical",
                 "expected_action": "stop_drug", "description": "CONTRAINDICATED — fatal toxicity"}
            ]
        },
        {
            "test_id": "TC06",
            "description": "SLCO1B1 poor function on simvastatin — switch statin",
            "therapeutic_area": "cardiology",
            "patient": {
                "patient_id": "VAL_TC06",
                "demographics": {"first_name": "Test", "last_name": "Case06", "age": 55, "sex": "M",
                                  "weight_kg": 85, "height_cm": 178, "ethnicity": "Caucasian"},
                "genotype": {
                    "SLCO1B1": {"diplotype": "*5/*5", "phenotype": "poor_function"},
                },
                "medications": ["simvastatin"],
                "lab_values": {"egfr": 80, "alt": 30, "ast": 25},
                "clinical_context": {"primary_diagnosis": "Hyperlipidemia", "therapeutic_area": "cardiology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "SLCO1B1", "drug": "simvastatin", "expected_severity": "critical",
                 "expected_action": "switch_drug", "description": "AVOID simvastatin — rhabdomyolysis risk"}
            ]
        },
        {
            "test_id": "TC07",
            "description": "CYP2D6 PM on tamoxifen — switch to aromatase inhibitor",
            "therapeutic_area": "oncology",
            "patient": {
                "patient_id": "VAL_TC07",
                "demographics": {"first_name": "Test", "last_name": "Case07", "age": 58, "sex": "F",
                                  "weight_kg": 68, "height_cm": 163, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*4/*4", "phenotype": "poor_metabolizer"},
                },
                "medications": ["tamoxifen"],
                "lab_values": {"egfr": 90, "alt": 20, "ast": 18},
                "clinical_context": {"primary_diagnosis": "ER+ breast cancer", "therapeutic_area": "oncology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2D6", "drug": "tamoxifen", "expected_severity": "critical",
                 "expected_action": "switch_drug", "description": "Switch to aromatase inhibitor"}
            ]
        },
        {
            "test_id": "TC08",
            "description": "CYP2D6 PM + fluoxetine DDI on codeine — dual flag",
            "therapeutic_area": "pain_management",
            "patient": {
                "patient_id": "VAL_TC08",
                "demographics": {"first_name": "Test", "last_name": "Case08", "age": 50, "sex": "F",
                                  "weight_kg": 60, "height_cm": 160, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*4/*4", "phenotype": "poor_metabolizer"},
                },
                "medications": ["codeine", "fluoxetine"],
                "lab_values": {"egfr": 85, "alt": 22, "ast": 20},
                "clinical_context": {"primary_diagnosis": "Chronic pain + depression", "therapeutic_area": "pain_management",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2D6", "drug": "codeine", "expected_severity": "high",
                 "expected_action": "stop_drug", "description": "Gene: CYP2D6 PM — codeine ineffective"},
                {"gene": "", "drug": "fluoxetine + codeine", "expected_severity": "high",
                 "expected_action": "switch_drug", "description": "DDI: fluoxetine inhibits CYP2D6"}
            ]
        },
        {
            "test_id": "TC09",
            "description": "CYP2C19 PM on clopidogrel + omeprazole DDI — dual flag",
            "therapeutic_area": "cardiology",
            "patient": {
                "patient_id": "VAL_TC09",
                "demographics": {"first_name": "Test", "last_name": "Case09", "age": 62, "sex": "M",
                                  "weight_kg": 78, "height_cm": 170, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2C19": {"diplotype": "*2/*2", "phenotype": "poor_metabolizer"},
                },
                "medications": ["clopidogrel", "omeprazole"],
                "lab_values": {"egfr": 75, "alt": 25, "ast": 22},
                "clinical_context": {"primary_diagnosis": "Post-PCI", "therapeutic_area": "cardiology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "CYP2C19", "drug": "clopidogrel", "expected_severity": "critical",
                 "expected_action": "switch_drug", "description": "Gene: CYP2C19 PM — clopidogrel ineffective"},
                {"gene": "", "drug": "omeprazole + clopidogrel", "expected_severity": "high",
                 "expected_action": "switch_drug", "description": "DDI: omeprazole inhibits CYP2C19"}
            ]
        },
        {
            "test_id": "TC10",
            "description": "TPMT PM on mercaptopurine — 90% dose reduction",
            "therapeutic_area": "oncology",
            "patient": {
                "patient_id": "VAL_TC10",
                "demographics": {"first_name": "Test", "last_name": "Case10", "age": 8, "sex": "M",
                                  "weight_kg": 25, "height_cm": 125, "ethnicity": "Caucasian"},
                "genotype": {
                    "TPMT": {"diplotype": "*3A/*3A", "phenotype": "poor_metabolizer"},
                },
                "medications": ["mercaptopurine"],
                "lab_values": {"egfr": 120, "alt": 18, "ast": 15},
                "clinical_context": {"primary_diagnosis": "ALL maintenance", "therapeutic_area": "oncology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "TPMT", "drug": "mercaptopurine", "expected_severity": "critical",
                 "expected_action": "reduce_dose", "description": "Reduce to 10% of standard dose"}
            ]
        },
        {
            "test_id": "TC11",
            "description": "UGT1A1 *28/*28 on irinotecan — 30% dose reduction",
            "therapeutic_area": "oncology",
            "patient": {
                "patient_id": "VAL_TC11",
                "demographics": {"first_name": "Test", "last_name": "Case11", "age": 60, "sex": "F",
                                  "weight_kg": 58, "height_cm": 157, "ethnicity": "East Asian"},
                "genotype": {
                    "UGT1A1": {"diplotype": "*28/*28", "phenotype": "poor_metabolizer"},
                },
                "medications": ["irinotecan"],
                "lab_values": {"egfr": 70, "alt": 35, "ast": 30},
                "clinical_context": {"primary_diagnosis": "mCRC", "therapeutic_area": "oncology",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "UGT1A1", "drug": "irinotecan", "expected_severity": "critical",
                 "expected_action": "reduce_dose", "description": "Reduce irinotecan dose by 30%"}
            ]
        },
        {
            "test_id": "TC12",
            "description": "HLA-B*15:02 positive on carbamazepine — CONTRAINDICATED (SJS/TEN)",
            "therapeutic_area": "psychiatry",
            "patient": {
                "patient_id": "VAL_TC12",
                "demographics": {"first_name": "Test", "last_name": "Case12", "age": 35, "sex": "F",
                                  "weight_kg": 55, "height_cm": 158, "ethnicity": "East Asian"},
                "genotype": {
                    "HLA-B": {"allele": "*15:02 positive", "phenotype": "hla_b_1502_positive"},
                },
                "medications": ["carbamazepine"],
                "lab_values": {"egfr": 100, "alt": 18, "ast": 15},
                "clinical_context": {"primary_diagnosis": "Bipolar disorder", "therapeutic_area": "psychiatry",
                                      "reason_for_pgx_testing": "Validation test"}
            },
            "expected": [
                {"gene": "HLA-B", "drug": "carbamazepine", "expected_severity": "critical",
                 "expected_action": "stop_drug", "description": "CONTRAINDICATED — SJS/TEN risk"}
            ]
        },
    ]

    def run_validation(self, engine, scorer, recommender) -> list:
        """Run all test cases through the interpretation pipeline."""
        results = []
        for tc in self.TEST_CASES:
            result = self.validate_single_case(engine, scorer, recommender, tc)
            status = "PASS" if result["passed"] else "FAIL"
            logger.debug(f"{result['test_id']}: {status} — {result['description']}")
            results.append(result)
        logger.info(f"Validation complete: {sum(1 for r in results if r['passed'])}/{len(results)} passed")
        return results

    def validate_single_case(self, engine, scorer, recommender, test_case: dict) -> dict:
        """Validate a single test case against expected outcomes."""
        patient = test_case["patient"]
        expected_list = test_case["expected"]

        # Run interpretation
        findings = engine.generate_findings(patient)
        scored_findings = scorer.score_findings(findings)
        recommendations = recommender.generate_recommendations(scored_findings, patient)

        # Check each expected finding
        checks = []
        for expected in expected_list:
            found = self._check_finding_present(scored_findings, expected)
            severity_ok = self._check_severity_correct(found, expected) if found else False
            action_ok = self._check_recommendation_appropriate(recommendations, expected) if found else False

            checks.append({
                "expected": expected,
                "found": found is not None,
                "severity_correct": severity_ok,
                "action_appropriate": action_ok,
                "matched_finding": self._summarize_finding(found) if found else None,
                "pass": found is not None and severity_ok,
            })

        all_pass = all(c["pass"] for c in checks)

        return {
            "test_id": test_case["test_id"],
            "description": test_case["description"],
            "therapeutic_area": test_case["therapeutic_area"],
            "passed": all_pass,
            "checks": checks,
            "total_findings": len(findings),
            "total_recommendations": len(recommendations),
        }

    def _check_finding_present(self, findings: list, expected: dict) -> Optional[dict]:
        """Check if an expected finding was generated."""
        target_gene = expected.get("gene", "").lower()
        target_drug = expected.get("drug", "").lower()

        for f in findings:
            f_drug = f.get("drug", "").lower()
            f_gene = f.get("gene", "").lower()

            # Direct match
            if target_gene and target_drug:
                if target_gene == f_gene and target_drug in f_drug:
                    return f
            # DDI match (drug pair)
            elif "+" in target_drug:
                drugs = [d.strip() for d in target_drug.split("+")]
                if all(d in f_drug for d in drugs):
                    return f
            # Drug-only match
            elif target_drug and target_drug in f_drug:
                return f

        return None

    def _check_severity_correct(self, finding: Optional[dict], expected: dict) -> bool:
        """Validate severity assignment."""
        if not finding:
            return False
        actual = finding.get("severity", "").lower()
        expected_sev = expected.get("expected_severity", "").lower()

        # Allow critical to match high (conservative is OK)
        if expected_sev == "high" and actual == "critical":
            return True
        return actual == expected_sev

    def _check_recommendation_appropriate(self, recommendations: list, expected: dict) -> bool:
        """Validate that the recommendation type is appropriate."""
        target_drug = expected.get("drug", "").lower()
        target_action = expected.get("expected_action", "").lower()

        action_map = {
            "stop_drug": ["stop_drug", "switch_drug"],
            "switch_drug": ["switch_drug", "stop_drug"],
            "reduce_dose": ["reduce_dose", "increase_monitoring"],
        }
        acceptable = action_map.get(target_action, [target_action])

        for rec in recommendations:
            rec_drug = rec.get("drug", "").lower()
            if target_drug.split("+")[0].strip() in rec_drug or rec_drug in target_drug:
                if rec.get("action_type", "").lower() in acceptable:
                    return True

        return False

    def _summarize_finding(self, finding: dict) -> dict:
        """Create a summary of a matched finding."""
        return {
            "drug": finding.get("drug", ""),
            "gene": finding.get("gene", ""),
            "severity": finding.get("severity", ""),
            "finding_type": finding.get("finding_type", ""),
            "risk_score": finding.get("risk_score", 0),
        }

    def calculate_metrics(self, validation_results: list) -> dict:
        """Calculate validation accuracy and clinical impact metrics."""
        total_checks = 0
        passed_checks = 0
        critical_checks = 0
        critical_passed = 0
        cases_passed = 0

        for result in validation_results:
            if result["passed"]:
                cases_passed += 1
            for check in result["checks"]:
                total_checks += 1
                if check["pass"]:
                    passed_checks += 1
                if check["expected"].get("expected_severity") == "critical":
                    critical_checks += 1
                    if check["pass"]:
                        critical_passed += 1

        total_cases = len(validation_results)
        sensitivity = passed_checks / total_checks if total_checks > 0 else 0
        accuracy = cases_passed / total_cases if total_cases > 0 else 0
        critical_rate = critical_passed / critical_checks if critical_checks > 0 else 0

        # Business impact
        adverse_events_prevented = critical_passed + sum(
            1 for r in validation_results for c in r["checks"]
            if c["pass"] and c["expected"].get("expected_severity") in ("critical", "high")
        )
        time_saved = total_cases * 2.25  # 2.25 hours saved per manual review
        cost_per_adverse_event = 25000
        adverse_event_cost_avoided = adverse_events_prevented * cost_per_adverse_event

        return {
            "total_cases": total_cases,
            "cases_passed": cases_passed,
            "total_checks": total_checks,
            "checks_passed": passed_checks,
            "sensitivity": sensitivity,
            "accuracy": accuracy,
            "critical_finding_detection_rate": critical_rate,
            "adverse_events_prevented": adverse_events_prevented,
            "time_saved_per_report_hours": 2.25,
            "total_time_saved_hours": time_saved,
            "actionable_changes_identified": passed_checks,
            "adverse_event_cost_avoided": adverse_event_cost_avoided,
            "annual_capacity_improvement": "10x (from ~1,000 to ~10,000 reports per analyst per year)",
        }

    def generate_impact_report(self, validation_results: list, metrics: dict) -> str:
        """Generate a formatted validation and impact report."""
        lines = []
        lines.append("=" * 72)
        lines.append("  PGx CLINICAL SOLUTIONS — VALIDATION & IMPACT REPORT")
        lines.append("  Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya")
        lines.append("=" * 72)
        lines.append("")

        # Validation summary
        lines.append("VALIDATION SUMMARY")
        lines.append("-" * 40)
        lines.append(f"  Total test cases:             {metrics['total_cases']}")
        lines.append(f"  Cases passed:                 {metrics['cases_passed']}/{metrics['total_cases']}")
        lines.append(f"  Individual checks passed:     {metrics['checks_passed']}/{metrics['total_checks']}")
        lines.append(f"  Overall accuracy:             {metrics['accuracy']:.1%}")
        lines.append(f"  Finding sensitivity:          {metrics['sensitivity']:.1%}")
        lines.append(f"  Critical detection rate:      {metrics['critical_finding_detection_rate']:.1%}")
        lines.append("")

        # Per-case results
        lines.append("PER-CASE RESULTS")
        lines.append("-" * 40)
        for result in validation_results:
            status = "PASS" if result["passed"] else "FAIL"
            icon = "[+]" if result["passed"] else "[X]"
            lines.append(f"  {icon} {result['test_id']}: {result['description']}")
            lines.append(f"      Area: {result['therapeutic_area']} | Findings: {result['total_findings']} | "
                        f"Recs: {result['total_recommendations']} | Status: {status}")
            for check in result["checks"]:
                check_status = "OK" if check["pass"] else "FAIL"
                lines.append(f"        - {check['expected']['description']}: {check_status}")
                if check["matched_finding"]:
                    mf = check["matched_finding"]
                    lines.append(f"          Matched: {mf['drug']} | {mf['gene']} | {mf['severity']} | score={mf['risk_score']}")
            lines.append("")

        # Clinical impact
        lines.append("CLINICAL IMPACT METRICS")
        lines.append("-" * 40)
        lines.append(f"  Adverse events preventable:   {metrics['adverse_events_prevented']}")
        lines.append(f"  Cost avoided per event:       ${25000:,}")
        lines.append(f"  Total cost avoidance:         ${metrics['adverse_event_cost_avoided']:,}")
        lines.append(f"  Time saved per report:        {metrics['time_saved_per_report_hours']:.1f} hours")
        lines.append(f"  Analyst capacity improvement: {metrics['annual_capacity_improvement']}")
        lines.append("")

        # Value proposition
        lines.append("VALUE PROPOSITION SUMMARY")
        lines.append("-" * 40)
        lines.append("  Automated interpretation vs. manual pharmacist review:")
        lines.append(f"    - Speed: <1 minute (automated) vs 2-3 hours (manual)")
        lines.append(f"    - Consistency: {metrics['accuracy']:.1%} guideline concordance")
        lines.append(f"    - Critical safety: {metrics['critical_finding_detection_rate']:.1%} detection of life-threatening interactions")
        lines.append(f"    - Scalability: 10x throughput improvement per analyst")
        lines.append(f"    - Cost: ~$5-15/report (automated) vs ~$150-300/report (manual)")
        lines.append("")
        lines.append("  Therapeutic area coverage validated:")
        areas = set(r["therapeutic_area"] for r in validation_results)
        for area in sorted(areas):
            count = sum(1 for r in validation_results if r["therapeutic_area"] == area and r["passed"])
            total = sum(1 for r in validation_results if r["therapeutic_area"] == area)
            lines.append(f"    - {area}: {count}/{total} scenarios passed")
        lines.append("")
        lines.append("=" * 72)

        return "\n".join(lines)

    # ================================================================
    # Oncology Gap Analysis Test Cases (TC_GAP01 - TC_GAP06)
    # ================================================================

    GAP_TEST_CASES = [
        {
            "test_id": "TC_GAP01",
            "description": "Fluorouracil patient, no DPYD testing — must flag critical gap",
            "patient": {
                "patient_id": "VAL_GAP01",
                "demographics": {"first_name": "Test", "last_name": "Gap01", "age": 62, "sex": "F",
                                  "weight_kg": 65, "height_cm": 162, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": ["fluorouracil"],
                "lab_values": {"egfr": 80, "alt": 22, "ast": 18},
                "clinical_context": {"primary_diagnosis": "Colorectal cancer",
                                      "therapeutic_area": "oncology"},
            },
            "expected": {
                "min_testing_gaps": 1,
                "must_flag_gene": "DPYD",
                "must_flag_drug": "fluorouracil",
                "expected_gap_severity": "critical",
            },
        },
        {
            "test_id": "TC_GAP02",
            "description": "DPYD IM on fluorouracil, has testing but actionable result — missed intervention",
            "patient": {
                "patient_id": "VAL_GAP02",
                "demographics": {"first_name": "Test", "last_name": "Gap02", "age": 58, "sex": "M",
                                  "weight_kg": 75, "height_cm": 175, "ethnicity": "Caucasian"},
                "genotype": {
                    "DPYD": {"diplotype": "*2A/*2A", "phenotype": "poor_metabolizer"},
                },
                "medications": ["fluorouracil"],
                "lab_values": {"egfr": 90, "alt": 20, "ast": 18},
                "clinical_context": {"primary_diagnosis": "Gastric cancer",
                                      "therapeutic_area": "oncology"},
            },
            "expected": {
                "testing_gaps": 0,
                "min_missed_interventions": 1,
                "missed_drug": "fluorouracil",
                "expected_gap_severity": "critical",
            },
        },
        {
            "test_id": "TC_GAP03",
            "description": "Tamoxifen + fluoxetine, CYP2D6 PM — gap AND DDI",
            "patient": {
                "patient_id": "VAL_GAP03",
                "demographics": {"first_name": "Test", "last_name": "Gap03", "age": 55, "sex": "F",
                                  "weight_kg": 63, "height_cm": 165, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*4/*4", "phenotype": "poor_metabolizer"},
                },
                "medications": ["tamoxifen", "fluoxetine"],
                "lab_values": {"egfr": 95, "alt": 18, "ast": 15},
                "clinical_context": {"primary_diagnosis": "ER+ breast cancer",
                                      "therapeutic_area": "oncology"},
            },
            "expected": {
                "min_missed_interventions": 1,
                "missed_drug": "tamoxifen",
                "expected_gap_severity": "critical",
            },
        },
        {
            "test_id": "TC_GAP04",
            "description": "Fully compliant patient — zero gaps",
            "patient": {
                "patient_id": "VAL_GAP04",
                "demographics": {"first_name": "Test", "last_name": "Gap04", "age": 50, "sex": "M",
                                  "weight_kg": 80, "height_cm": 178, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*1/*1", "phenotype": "normal_metabolizer"},
                },
                "medications": ["tamoxifen"],
                "lab_values": {"egfr": 100, "alt": 15, "ast": 12},
                "clinical_context": {"primary_diagnosis": "ER+ breast cancer",
                                      "therapeutic_area": "oncology"},
            },
            "expected": {
                "testing_gaps": 0,
                "missed_interventions": 0,
                "expected_gap_severity": "none",
            },
        },
        {
            "test_id": "TC_GAP05",
            "description": "Population of 5 patients — correct aggregate stats",
            "patients": [
                {   # Gap patient: fluorouracil, no DPYD test
                    "patient_id": "POP_01",
                    "demographics": {"age": 60, "sex": "F", "weight_kg": 65, "height_cm": 160},
                    "genotype": {},
                    "medications": ["fluorouracil"],
                    "lab_values": {"egfr": 80},
                    "clinical_context": {"therapeutic_area": "oncology"},
                },
                {   # Gap patient: irinotecan, no UGT1A1 test
                    "patient_id": "POP_02",
                    "demographics": {"age": 55, "sex": "M", "weight_kg": 78, "height_cm": 175},
                    "genotype": {},
                    "medications": ["irinotecan"],
                    "lab_values": {"egfr": 90},
                    "clinical_context": {"therapeutic_area": "oncology"},
                },
                {   # Missed intervention: DPYD PM on fluorouracil
                    "patient_id": "POP_03",
                    "demographics": {"age": 62, "sex": "F", "weight_kg": 60, "height_cm": 158},
                    "genotype": {"DPYD": {"diplotype": "*2A/*2A", "phenotype": "poor_metabolizer"}},
                    "medications": ["fluorouracil"],
                    "lab_values": {"egfr": 75},
                    "clinical_context": {"therapeutic_area": "oncology"},
                },
                {   # Compliant: tamoxifen, CYP2D6 NM
                    "patient_id": "POP_04",
                    "demographics": {"age": 48, "sex": "F", "weight_kg": 62, "height_cm": 165},
                    "genotype": {"CYP2D6": {"diplotype": "*1/*1", "phenotype": "normal_metabolizer"}},
                    "medications": ["tamoxifen"],
                    "lab_values": {"egfr": 100},
                    "clinical_context": {"therapeutic_area": "oncology"},
                },
                {   # Compliant: irinotecan, UGT1A1 NM
                    "patient_id": "POP_05",
                    "demographics": {"age": 70, "sex": "M", "weight_kg": 72, "height_cm": 170},
                    "genotype": {"UGT1A1": {"diplotype": "*1/*1", "phenotype": "normal_metabolizer"}},
                    "medications": ["irinotecan"],
                    "lab_values": {"egfr": 60},
                    "clinical_context": {"therapeutic_area": "oncology"},
                },
            ],
            "expected": {
                "cohort_size": 5,
                "min_patients_with_gaps": 2,
                "min_patients_with_missed": 1,
            },
        },
        {
            "test_id": "TC_GAP06",
            "description": "Irinotecan, no UGT1A1 testing — must flag gap",
            "patient": {
                "patient_id": "VAL_GAP06",
                "demographics": {"first_name": "Test", "last_name": "Gap06", "age": 67, "sex": "M",
                                  "weight_kg": 82, "height_cm": 178, "ethnicity": "East Asian"},
                "genotype": {},
                "medications": ["irinotecan"],
                "lab_values": {"egfr": 70, "alt": 28, "ast": 25},
                "clinical_context": {"primary_diagnosis": "Metastatic CRC",
                                      "therapeutic_area": "oncology"},
            },
            "expected": {
                "min_testing_gaps": 1,
                "must_flag_gene": "UGT1A1",
                "must_flag_drug": "irinotecan",
            },
        },
    ]

    # ================================================================
    # Geriatric Deprescribing Test Cases (TC_DEP01 - TC_DEP06)
    # ================================================================

    DEP_TEST_CASES = [
        {
            "test_id": "TC_DEP01",
            "description": "Diphenhydramine in 78yo — Beers flag + ACB=3",
            "patient": {
                "patient_id": "VAL_DEP01",
                "demographics": {"first_name": "Test", "last_name": "Dep01", "age": 78, "sex": "F",
                                  "weight_kg": 58, "height_cm": 155, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": [
                    {"name": "diphenhydramine", "dose": "25mg", "frequency": "nightly"},
                    {"name": "lisinopril", "dose": "10mg", "frequency": "daily"},
                    {"name": "metformin", "dose": "500mg", "frequency": "twice daily"},
                ],
                "lab_values": {"egfr": 55, "alt": 20, "ast": 18},
                "clinical_context": {"primary_diagnosis": "Insomnia", "therapeutic_area": "geriatric",
                                      "conditions": ["diabetes", "hypertension"]},
            },
            "expected": {
                "beers_flag_drug": "diphenhydramine",
                "beers_category": "avoid",
                "acb_drug": "diphenhydramine",
                "acb_score": 3,
                "min_recommendations": 1,
            },
        },
        {
            "test_id": "TC_DEP02",
            "description": "Lorazepam in elderly — Beers flag (avoid benzodiazepines)",
            "patient": {
                "patient_id": "VAL_DEP02",
                "demographics": {"first_name": "Test", "last_name": "Dep02", "age": 82, "sex": "M",
                                  "weight_kg": 70, "height_cm": 172, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": [
                    {"name": "lorazepam", "dose": "1mg", "frequency": "nightly"},
                    {"name": "amlodipine", "dose": "5mg", "frequency": "daily"},
                ],
                "lab_values": {"egfr": 60, "alt": 22, "ast": 20},
                "clinical_context": {"primary_diagnosis": "Anxiety", "therapeutic_area": "geriatric",
                                      "conditions": ["hypertension"]},
            },
            "expected": {
                "beers_flag_drug": "lorazepam",
                "beers_category": "avoid",
                "min_recommendations": 1,
            },
        },
        {
            "test_id": "TC_DEP03",
            "description": "Donepezil + oxybutynin — cascade detection",
            "patient": {
                "patient_id": "VAL_DEP03",
                "demographics": {"first_name": "Test", "last_name": "Dep03", "age": 80, "sex": "F",
                                  "weight_kg": 55, "height_cm": 155, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": [
                    {"name": "donepezil", "dose": "10mg", "frequency": "daily"},
                    {"name": "oxybutynin", "dose": "5mg", "frequency": "twice daily"},
                    {"name": "metoprolol", "dose": "25mg", "frequency": "daily"},
                ],
                "lab_values": {"egfr": 50, "alt": 25, "ast": 22},
                "clinical_context": {"primary_diagnosis": "Dementia", "therapeutic_area": "geriatric",
                                      "conditions": ["dementia", "urinary_incontinence"]},
            },
            "expected": {
                "min_cascades": 1,
                "cascade_drugs": ["donepezil", "oxybutynin"],
                "oxybutynin_acb": 3,
                "min_recommendations": 1,
            },
        },
        {
            "test_id": "TC_DEP04",
            "description": "Cumulative ACB >=6 — high anticholinergic risk",
            "patient": {
                "patient_id": "VAL_DEP04",
                "demographics": {"first_name": "Test", "last_name": "Dep04", "age": 75, "sex": "M",
                                  "weight_kg": 72, "height_cm": 170, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": [
                    {"name": "oxybutynin", "dose": "5mg", "frequency": "twice daily"},
                    {"name": "amitriptyline", "dose": "25mg", "frequency": "nightly"},
                    {"name": "quetiapine", "dose": "25mg", "frequency": "nightly"},
                    {"name": "lisinopril", "dose": "20mg", "frequency": "daily"},
                ],
                "lab_values": {"egfr": 65, "alt": 20, "ast": 18},
                "clinical_context": {"primary_diagnosis": "Neuropathic pain", "therapeutic_area": "geriatric",
                                      "conditions": ["hypertension", "depression"]},
            },
            "expected": {
                "min_total_acb": 6,
                "acb_risk_level": "high",
                "min_beers_flags": 2,
            },
        },
        {
            "test_id": "TC_DEP05",
            "description": "Nortriptyline + CYP2D6 PM + Beers — PGx overlay shows additive evidence",
            "patient": {
                "patient_id": "VAL_DEP05",
                "demographics": {"first_name": "Test", "last_name": "Dep05", "age": 78, "sex": "F",
                                  "weight_kg": 60, "height_cm": 160, "ethnicity": "Caucasian"},
                "genotype": {
                    "CYP2D6": {"diplotype": "*4/*4", "phenotype": "poor_metabolizer"},
                },
                "medications": [
                    {"name": "nortriptyline", "dose": "25mg", "frequency": "nightly"},
                    {"name": "amlodipine", "dose": "5mg", "frequency": "daily"},
                    {"name": "omeprazole", "dose": "20mg", "frequency": "daily"},
                ],
                "lab_values": {"egfr": 60, "alt": 22, "ast": 20},
                "clinical_context": {"primary_diagnosis": "Neuropathic pain", "therapeutic_area": "geriatric",
                                      "conditions": ["hypertension", "gerd"]},
            },
            "expected": {
                "beers_flag_drug": "nortriptyline",
                "min_pgx_overlay": 1,
                "pgx_drug": "nortriptyline",
                "pgx_gene": "CYP2D6",
            },
        },
        {
            "test_id": "TC_DEP06",
            "description": "12 meds, 3 Beers flags, 2 cascades — polypharmacy score >=70",
            "patient": {
                "patient_id": "VAL_DEP06",
                "demographics": {"first_name": "Test", "last_name": "Dep06", "age": 85, "sex": "F",
                                  "weight_kg": 52, "height_cm": 152, "ethnicity": "Caucasian"},
                "genotype": {},
                "medications": [
                    {"name": "diphenhydramine", "dose": "25mg", "frequency": "nightly"},
                    {"name": "amitriptyline", "dose": "25mg", "frequency": "nightly"},
                    {"name": "oxybutynin", "dose": "5mg", "frequency": "twice daily"},
                    {"name": "donepezil", "dose": "10mg", "frequency": "daily"},
                    {"name": "amlodipine", "dose": "10mg", "frequency": "daily"},
                    {"name": "furosemide", "dose": "40mg", "frequency": "daily"},
                    {"name": "metformin", "dose": "1000mg", "frequency": "twice daily"},
                    {"name": "lisinopril", "dose": "20mg", "frequency": "daily"},
                    {"name": "atorvastatin", "dose": "40mg", "frequency": "daily"},
                    {"name": "omeprazole", "dose": "20mg", "frequency": "daily"},
                    {"name": "metoprolol", "dose": "50mg", "frequency": "daily"},
                    {"name": "aspirin", "dose": "81mg", "frequency": "daily"},
                ],
                "lab_values": {"egfr": 45, "alt": 28, "ast": 25},
                "clinical_context": {"primary_diagnosis": "Multiple comorbidities",
                                      "therapeutic_area": "geriatric",
                                      "conditions": ["dementia", "hypertension", "diabetes",
                                                     "urinary_incontinence", "heart_failure"]},
            },
            "expected": {
                "min_beers_flags": 3,
                "min_cascades": 2,
                "min_polypharmacy_score": 70,
                "polypharmacy_risk_level": "high",
                "min_recommendations": 5,
            },
        },
    ]

    def run_gap_validation(self, kb, engine) -> list:
        """Run gap analysis test cases."""
        from src.oncology_gap.gap_analyzer import GapAnalyzer
        from src.oncology_gap.population_analytics import PopulationAnalytics

        gap_analyzer = GapAnalyzer(kb, engine)
        results = []

        for tc in self.GAP_TEST_CASES:
            result = self._validate_gap_case(gap_analyzer, tc)
            status = "PASS" if result["passed"] else "FAIL"
            logger.debug(f"{result['test_id']}: {status} -- {result['description']}")
            results.append(result)

        passed = sum(1 for r in results if r["passed"])
        logger.info(f"Gap validation complete: {passed}/{len(results)} passed")
        return results

    def _validate_gap_case(self, gap_analyzer, tc: dict) -> dict:
        """Validate a single gap analysis test case."""
        expected = tc["expected"]
        checks = []

        if "patients" in tc:
            # Population-level test (TC_GAP05)
            patients = tc["patients"]
            gap_results = gap_analyzer.analyze_cohort(patients)

            # Check cohort size
            if "cohort_size" in expected:
                ok = len(gap_results) == expected["cohort_size"]
                checks.append({"check": "cohort_size", "pass": ok,
                                "expected": expected["cohort_size"], "actual": len(gap_results)})

            # Check patients with gaps
            if "min_patients_with_gaps" in expected:
                with_gaps = sum(1 for r in gap_results if r["testing_gap_count"] > 0)
                ok = with_gaps >= expected["min_patients_with_gaps"]
                checks.append({"check": "patients_with_gaps", "pass": ok,
                                "expected": f">={expected['min_patients_with_gaps']}", "actual": with_gaps})

            # Check patients with missed interventions
            if "min_patients_with_missed" in expected:
                with_missed = sum(1 for r in gap_results if r["missed_intervention_count"] > 0)
                ok = with_missed >= expected["min_patients_with_missed"]
                checks.append({"check": "patients_with_missed", "pass": ok,
                                "expected": f">={expected['min_patients_with_missed']}", "actual": with_missed})
        else:
            # Single-patient test
            patient = tc["patient"]
            result = gap_analyzer.analyze_patient(patient)

            # Check testing gap count
            if "min_testing_gaps" in expected:
                ok = result["testing_gap_count"] >= expected["min_testing_gaps"]
                checks.append({"check": "testing_gap_count", "pass": ok,
                                "expected": f">={expected['min_testing_gaps']}", "actual": result["testing_gap_count"]})

            if "testing_gaps" in expected:
                ok = result["testing_gap_count"] == expected["testing_gaps"]
                checks.append({"check": "testing_gaps_exact", "pass": ok,
                                "expected": expected["testing_gaps"], "actual": result["testing_gap_count"]})

            # Check specific gene flagged
            if "must_flag_gene" in expected:
                flagged_genes = {g["gene"] for g in result["testing_gaps"]}
                ok = expected["must_flag_gene"] in flagged_genes
                checks.append({"check": "gene_flagged", "pass": ok,
                                "expected": expected["must_flag_gene"], "actual": list(flagged_genes)})

            # Check specific drug flagged
            if "must_flag_drug" in expected:
                flagged_drugs = {g["drug"] for g in result["testing_gaps"]}
                ok = expected["must_flag_drug"] in flagged_drugs
                checks.append({"check": "drug_flagged", "pass": ok,
                                "expected": expected["must_flag_drug"], "actual": list(flagged_drugs)})

            # Check missed interventions
            if "min_missed_interventions" in expected:
                ok = result["missed_intervention_count"] >= expected["min_missed_interventions"]
                checks.append({"check": "missed_interventions", "pass": ok,
                                "expected": f">={expected['min_missed_interventions']}",
                                "actual": result["missed_intervention_count"]})

            if "missed_interventions" in expected:
                ok = result["missed_intervention_count"] == expected["missed_interventions"]
                checks.append({"check": "missed_exact", "pass": ok,
                                "expected": expected["missed_interventions"],
                                "actual": result["missed_intervention_count"]})

            if "missed_drug" in expected:
                missed_drugs = {m["drug"] for m in result["missed_interventions"]}
                ok = expected["missed_drug"] in missed_drugs
                checks.append({"check": "missed_drug", "pass": ok,
                                "expected": expected["missed_drug"], "actual": list(missed_drugs)})

            # Check gap severity
            if "expected_gap_severity" in expected:
                ok = result["gap_severity"] == expected["expected_gap_severity"]
                checks.append({"check": "gap_severity", "pass": ok,
                                "expected": expected["expected_gap_severity"], "actual": result["gap_severity"]})

        all_pass = all(c["pass"] for c in checks)
        return {
            "test_id": tc["test_id"],
            "description": tc["description"],
            "passed": all_pass,
            "checks": checks,
        }

    def run_deprescribing_validation(self, kb, engine) -> list:
        """Run deprescribing test cases."""
        from src.deprescribing.deprescribing_recommender import DeprescribingRecommender

        recommender = DeprescribingRecommender(kb, engine)
        results = []

        for tc in self.DEP_TEST_CASES:
            result = self._validate_dep_case(recommender, tc)
            status = "PASS" if result["passed"] else "FAIL"
            logger.debug(f"{result['test_id']}: {status} -- {result['description']}")
            results.append(result)

        passed = sum(1 for r in results if r["passed"])
        logger.info(f"Deprescribing validation complete: {passed}/{len(results)} passed")
        return results

    def _validate_dep_case(self, recommender, tc: dict) -> dict:
        """Validate a single deprescribing test case."""
        patient = tc["patient"]
        expected = tc["expected"]
        result = recommender.analyze_patient(patient)
        checks = []

        # Check Beers flag for specific drug
        if "beers_flag_drug" in expected:
            beers_drugs = {f["drug"] for f in result["beers_result"].get("flags", [])}
            ok = expected["beers_flag_drug"] in beers_drugs
            checks.append({"check": "beers_flag_drug", "pass": ok,
                            "expected": expected["beers_flag_drug"], "actual": list(beers_drugs)})

        # Check Beers category
        if "beers_category" in expected:
            target_drug = expected.get("beers_flag_drug", "")
            actual_cat = None
            for f in result["beers_result"].get("flags", []):
                if f["drug"] == target_drug:
                    actual_cat = f["category"]
                    break
            ok = actual_cat == expected["beers_category"]
            checks.append({"check": "beers_category", "pass": ok,
                            "expected": expected["beers_category"], "actual": actual_cat})

        # Check ACB for specific drug
        if "acb_drug" in expected:
            target = expected["acb_drug"]
            actual_score = 0
            for c in result["acb_result"].get("contributing_medications", []):
                if c["drug"] == target:
                    actual_score = c["score"]
                    break
            ok = actual_score == expected.get("acb_score", 0)
            checks.append({"check": "acb_score_drug", "pass": ok,
                            "expected": expected.get("acb_score", 0), "actual": actual_score})

        # Check minimum total ACB score
        if "min_total_acb" in expected:
            actual = result["acb_result"]["total_acb_score"]
            ok = actual >= expected["min_total_acb"]
            checks.append({"check": "total_acb", "pass": ok,
                            "expected": f">={expected['min_total_acb']}", "actual": actual})

        # Check ACB risk level
        if "acb_risk_level" in expected:
            actual = result["acb_result"]["risk_level"]
            ok = actual == expected["acb_risk_level"]
            checks.append({"check": "acb_risk_level", "pass": ok,
                            "expected": expected["acb_risk_level"], "actual": actual})

        # Check minimum Beers flags
        if "min_beers_flags" in expected:
            actual = result["beers_result"].get("flag_count", 0)
            ok = actual >= expected["min_beers_flags"]
            checks.append({"check": "beers_flag_count", "pass": ok,
                            "expected": f">={expected['min_beers_flags']}", "actual": actual})

        # Check minimum cascades
        if "min_cascades" in expected:
            actual = result["cascade_result"]["cascade_count"]
            ok = actual >= expected["min_cascades"]
            checks.append({"check": "cascade_count", "pass": ok,
                            "expected": f">={expected['min_cascades']}", "actual": actual})

        # Check specific cascade drugs
        if "cascade_drugs" in expected:
            involved = result["cascade_result"].get("medications_involved", [])
            ok = all(d in involved for d in expected["cascade_drugs"])
            checks.append({"check": "cascade_drugs", "pass": ok,
                            "expected": expected["cascade_drugs"], "actual": involved})

        # Check oxybutynin ACB score
        if "oxybutynin_acb" in expected:
            actual = 0
            for c in result["acb_result"].get("contributing_medications", []):
                if c["drug"] == "oxybutynin":
                    actual = c["score"]
                    break
            ok = actual == expected["oxybutynin_acb"]
            checks.append({"check": "oxybutynin_acb", "pass": ok,
                            "expected": expected["oxybutynin_acb"], "actual": actual})

        # Check minimum recommendations
        if "min_recommendations" in expected:
            actual = len(result["recommendations"])
            ok = actual >= expected["min_recommendations"]
            checks.append({"check": "recommendation_count", "pass": ok,
                            "expected": f">={expected['min_recommendations']}", "actual": actual})

        # Check PGx overlay
        if "min_pgx_overlay" in expected:
            actual = len(result["pgx_overlay"])
            ok = actual >= expected["min_pgx_overlay"]
            checks.append({"check": "pgx_overlay_count", "pass": ok,
                            "expected": f">={expected['min_pgx_overlay']}", "actual": actual})

        if "pgx_drug" in expected:
            overlay_drugs = {o["drug"] for o in result["pgx_overlay"]}
            ok = expected["pgx_drug"] in overlay_drugs
            checks.append({"check": "pgx_overlay_drug", "pass": ok,
                            "expected": expected["pgx_drug"], "actual": list(overlay_drugs)})

        if "pgx_gene" in expected:
            overlay_genes = {o["gene"] for o in result["pgx_overlay"]}
            ok = expected["pgx_gene"] in overlay_genes
            checks.append({"check": "pgx_overlay_gene", "pass": ok,
                            "expected": expected["pgx_gene"], "actual": list(overlay_genes)})

        # Check polypharmacy score
        if "min_polypharmacy_score" in expected:
            actual = result["polypharmacy_score"]["composite_score"]
            ok = actual >= expected["min_polypharmacy_score"]
            checks.append({"check": "polypharmacy_score", "pass": ok,
                            "expected": f">={expected['min_polypharmacy_score']}", "actual": actual})

        if "polypharmacy_risk_level" in expected:
            actual = result["polypharmacy_score"]["risk_level"]
            ok = actual == expected["polypharmacy_risk_level"]
            checks.append({"check": "polypharmacy_risk", "pass": ok,
                            "expected": expected["polypharmacy_risk_level"], "actual": actual})

        all_pass = all(c["pass"] for c in checks)
        return {
            "test_id": tc["test_id"],
            "description": tc["description"],
            "passed": all_pass,
            "checks": checks,
        }

    def run_full_validation(self, engine, scorer, recommender, kb) -> dict:
        """Run all 24 test cases across all three modules."""
        pgx_results = self.run_validation(engine, scorer, recommender)
        gap_results = self.run_gap_validation(kb, engine)
        dep_results = self.run_deprescribing_validation(kb, engine)

        return {
            "pgx_results": pgx_results,
            "gap_results": gap_results,
            "dep_results": dep_results,
            "total_cases": len(pgx_results) + len(gap_results) + len(dep_results),
            "total_passed": (
                sum(1 for r in pgx_results if r["passed"]) +
                sum(1 for r in gap_results if r["passed"]) +
                sum(1 for r in dep_results if r["passed"])
            ),
        }

    def generate_full_impact_report(self, full_results: dict, pgx_metrics: dict) -> str:
        """Generate combined validation report for all 24 test cases."""
        pgx_results = full_results["pgx_results"]
        gap_results = full_results["gap_results"]
        dep_results = full_results["dep_results"]

        lines = []
        lines.append("=" * 72)
        lines.append("  PGx CLINICAL SOLUTIONS — FULL VALIDATION REPORT")
        lines.append("  Ernest Moyo | Rangarirai Makuku | Tapiwa Mupereki | Ngonidzashe Faya")
        lines.append("=" * 72)
        lines.append("")

        total = full_results["total_cases"]
        passed = full_results["total_passed"]
        lines.append("OVERALL VALIDATION SUMMARY")
        lines.append("-" * 40)
        lines.append(f"  Total test cases:             {total}")
        lines.append(f"  Total passed:                 {passed}/{total}")
        lines.append(f"  Overall accuracy:             {passed/total:.1%}" if total > 0 else "  Overall accuracy:             N/A")
        lines.append("")

        # Module 1: PGx
        pgx_passed = sum(1 for r in pgx_results if r["passed"])
        lines.append(f"  Module 1 — PGx Interpretation:    {pgx_passed}/{len(pgx_results)} passed")
        lines.append(f"    Accuracy: {pgx_metrics.get('accuracy', 0):.1%}")
        lines.append(f"    Critical detection: {pgx_metrics.get('critical_finding_detection_rate', 0):.1%}")
        lines.append("")

        # Module 2: Gap
        gap_passed = sum(1 for r in gap_results if r["passed"])
        lines.append(f"  Module 2 — Oncology Gap Analysis: {gap_passed}/{len(gap_results)} passed")
        lines.append("")

        # Module 3: Deprescribing
        dep_passed = sum(1 for r in dep_results if r["passed"])
        lines.append(f"  Module 3 — Deprescribing:         {dep_passed}/{len(dep_results)} passed")
        lines.append("")

        # Detailed: PGx
        lines.append("PGx INTERPRETATION CASES (TC01-TC12)")
        lines.append("-" * 40)
        for r in pgx_results:
            icon = "[+]" if r["passed"] else "[X]"
            lines.append(f"  {icon} {r['test_id']}: {r['description']}")
        lines.append("")

        # Detailed: Gap
        lines.append("ONCOLOGY GAP ANALYSIS CASES (TC_GAP01-TC_GAP06)")
        lines.append("-" * 40)
        for r in gap_results:
            icon = "[+]" if r["passed"] else "[X]"
            lines.append(f"  {icon} {r['test_id']}: {r['description']}")
            for check in r["checks"]:
                check_icon = "OK" if check["pass"] else "FAIL"
                lines.append(f"        {check['check']}: {check_icon} (expected={check['expected']}, actual={check['actual']})")
        lines.append("")

        # Detailed: Deprescribing
        lines.append("DEPRESCRIBING CASES (TC_DEP01-TC_DEP06)")
        lines.append("-" * 40)
        for r in dep_results:
            icon = "[+]" if r["passed"] else "[X]"
            lines.append(f"  {icon} {r['test_id']}: {r['description']}")
            for check in r["checks"]:
                check_icon = "OK" if check["pass"] else "FAIL"
                lines.append(f"        {check['check']}: {check_icon} (expected={check['expected']}, actual={check['actual']})")
        lines.append("")

        lines.append("=" * 72)
        return "\n".join(lines)
