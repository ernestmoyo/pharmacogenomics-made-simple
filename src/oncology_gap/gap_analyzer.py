"""
Oncology PGx Gap Analyzer
=========================
Identifies pharmacogenomic testing gaps in oncology patients:
- Drugs that should have PGx testing but don't
- Actionable PGx results that weren't acted upon (missed interventions)
- Testing compliance rates per gene and drug
"""

from typing import Optional
from src.knowledge_base.kb_loader import KnowledgeBase
from src.interpretation.engine import InterpretationEngine
from src.utils.logger import get_logger

logger = get_logger("oncology_gap")


class GapAnalyzer:
    """Analyzes oncology patients for PGx testing gaps and missed interventions."""

    def __init__(self, kb: KnowledgeBase, engine: InterpretationEngine):
        self.kb = kb
        self.engine = engine

    def analyze_patient(self, patient: dict) -> dict:
        """Run full gap analysis on a single oncology patient."""
        pid = patient.get("patient_id", "?")
        medications = self._extract_medication_names(patient)
        genotype = patient.get("genotype", {})

        # 1. Find PGx-relevant drugs in the patient's medication list
        pgx_drugs = self._identify_pgx_drugs(medications)

        # 2. Identify testing gaps (drugs with PGx relevance but no genotype data)
        testing_gaps = self._find_testing_gaps(pgx_drugs, genotype)

        # 3. Run interpretation engine to find actionable results
        findings = self.engine.generate_findings(patient)

        # 4. Identify missed interventions (actionable findings that weren't addressed)
        missed_interventions = self._find_missed_interventions(findings, patient)

        # 5. Summarize compliant actions
        compliant_actions = self._find_compliant_actions(pgx_drugs, genotype, findings)

        result = {
            "patient_id": pid,
            "total_medications": len(medications),
            "pgx_relevant_drugs": pgx_drugs,
            "pgx_relevant_count": len(pgx_drugs),
            "testing_gaps": testing_gaps,
            "testing_gap_count": len(testing_gaps),
            "findings": findings,
            "missed_interventions": missed_interventions,
            "missed_intervention_count": len(missed_interventions),
            "compliant_actions": compliant_actions,
            "testing_rate": self._calc_testing_rate(pgx_drugs, testing_gaps),
            "gap_severity": self._classify_gap_severity(testing_gaps, missed_interventions),
        }

        logger.info(
            f"Patient {pid}: {len(pgx_drugs)} PGx drugs, "
            f"{len(testing_gaps)} gaps, {len(missed_interventions)} missed interventions"
        )
        return result

    def analyze_cohort(self, patients: list) -> list:
        """Analyze a list of patients and return per-patient gap results."""
        results = []
        for patient in patients:
            results.append(self.analyze_patient(patient))
        logger.info(f"Cohort analysis complete: {len(results)} patients analyzed")
        return results

    def _extract_medication_names(self, patient: dict) -> list:
        """Extract medication names from patient data (handles both str and dict formats)."""
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _identify_pgx_drugs(self, medications: list) -> list:
        """Identify which medications have known PGx relevance."""
        pgx_drugs = []
        for drug in medications:
            info = self.kb.get_pgx_drug_info(drug)
            if info:
                pgx_drugs.append({
                    "drug": drug,
                    "genes": info["genes"],
                    "cpic_level": info["cpic_level"],
                    "fda_label": info["fda_label"],
                    "testing_recommendation": info["testing_recommendation"],
                    "therapeutic_area": info["therapeutic_area"],
                })
        return pgx_drugs

    def _find_testing_gaps(self, pgx_drugs: list, genotype: dict) -> list:
        """Find drugs where PGx testing should have been done but wasn't."""
        gaps = []
        tested_genes = set(genotype.keys())

        for drug_info in pgx_drugs:
            for gene in drug_info["genes"]:
                if gene not in tested_genes:
                    severity = "critical" if drug_info["testing_recommendation"] == "required_before_initiation" else \
                               "high" if drug_info["testing_recommendation"] == "recommended" else "moderate"
                    gaps.append({
                        "drug": drug_info["drug"],
                        "gene": gene,
                        "cpic_level": drug_info["cpic_level"],
                        "fda_label": drug_info["fda_label"],
                        "testing_recommendation": drug_info["testing_recommendation"],
                        "gap_severity": severity,
                        "rationale": self._gap_rationale(drug_info, gene),
                    })
                    logger.debug(f"Testing gap: {drug_info['drug']} → {gene} not tested ({severity})")
        return gaps

    def _find_missed_interventions(self, findings: list, patient: dict) -> list:
        """Identify actionable findings where no clinical action was taken.

        For the prototype, we flag all critical and high-severity findings as
        potential missed interventions, since synthetic patients don't have
        'actions taken' data. In a real system, this would compare findings
        against documented clinical actions (dose changes, drug switches, etc.).
        """
        missed = []
        for finding in findings:
            severity = finding.get("severity", "")
            if severity in ("critical", "high"):
                dosing_adj = finding.get("dosing_adjustment", "")
                missed.append({
                    "drug": finding.get("drug", ""),
                    "gene": finding.get("gene", ""),
                    "severity": severity,
                    "finding_type": finding.get("finding_type", ""),
                    "recommendation": finding.get("recommendation", ""),
                    "dosing_adjustment": dosing_adj,
                    "clinical_consequence": finding.get("clinical_consequence", ""),
                    "action_required": self._classify_required_action(finding),
                })
        return missed

    def _find_compliant_actions(self, pgx_drugs: list, genotype: dict, findings: list) -> list:
        """Identify drugs where testing was done and results are non-actionable (compliant)."""
        tested_genes = set(genotype.keys())
        actionable_drugs = {f.get("drug", "") for f in findings if f.get("severity") in ("critical", "high")}

        compliant = []
        for drug_info in pgx_drugs:
            drug = drug_info["drug"]
            genes_tested = [g for g in drug_info["genes"] if g in tested_genes]
            if genes_tested and drug not in actionable_drugs:
                compliant.append({
                    "drug": drug,
                    "genes_tested": genes_tested,
                    "status": "compliant",
                })
        return compliant

    def _calc_testing_rate(self, pgx_drugs: list, testing_gaps: list) -> float:
        """Calculate the percentage of PGx-relevant drugs with appropriate testing."""
        if not pgx_drugs:
            return 100.0
        total_gene_drug_pairs = sum(len(d["genes"]) for d in pgx_drugs)
        if total_gene_drug_pairs == 0:
            return 100.0
        gap_count = len(testing_gaps)
        tested = total_gene_drug_pairs - gap_count
        return round((tested / total_gene_drug_pairs) * 100, 1)

    def _classify_gap_severity(self, testing_gaps: list, missed_interventions: list) -> str:
        """Classify overall gap severity for a patient."""
        has_critical_gap = any(g["gap_severity"] == "critical" for g in testing_gaps)
        has_critical_missed = any(m["severity"] == "critical" for m in missed_interventions)
        has_high_gap = any(g["gap_severity"] == "high" for g in testing_gaps)

        if has_critical_gap or has_critical_missed:
            return "critical"
        if has_high_gap or missed_interventions:
            return "high"
        if testing_gaps:
            return "moderate"
        return "none"

    def _classify_required_action(self, finding: dict) -> str:
        """Classify what clinical action is needed for a finding."""
        dosing = finding.get("dosing_adjustment", "")
        if dosing == "contraindicated":
            return "stop_drug"
        if dosing in ("major_reduction", "reduce_50_percent", "reduce_to_10_percent"):
            return "reduce_dose"
        if "switch" in finding.get("recommendation", "").lower():
            return "switch_drug"
        return "review_therapy"

    def _gap_rationale(self, drug_info: dict, gene: str) -> str:
        """Generate a human-readable rationale for why testing is recommended."""
        rec = drug_info["testing_recommendation"]
        cpic = drug_info["cpic_level"]
        fda = "FDA-labeled" if drug_info["fda_label"] else "Not FDA-labeled"

        if rec == "required_before_initiation":
            return (f"{gene} testing is required before initiating {drug_info['drug']}. "
                    f"CPIC Level {cpic}. {fda}.")
        elif rec == "recommended":
            return (f"{gene} testing is recommended for {drug_info['drug']} to guide dosing. "
                    f"CPIC Level {cpic}. {fda}.")
        else:
            return (f"{gene} testing is optional for {drug_info['drug']}. "
                    f"CPIC Level {cpic}. {fda}.")
