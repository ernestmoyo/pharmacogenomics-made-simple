"""
DDI Burden Scorer
=================
Quantifies drug-drug interaction burden per oncology patient.
Weights DDIs by severity and flags PGx-relevant interactions specifically.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.utils.logger import get_logger

logger = get_logger("ddi_burden")

# Severity weights for DDI burden scoring
DDI_WEIGHTS = {"major": 3, "moderate": 2, "minor": 1}


class DDIBurdenScorer:
    """Scores DDI burden for individual patients and across cohorts."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def score_patient(self, patient: dict) -> dict:
        """Calculate DDI burden score for a single patient."""
        medications = self._extract_medication_names(patient)
        ddis = self.kb.get_drug_drug_interactions(medications)

        # Categorize DDIs
        by_severity = {"major": [], "moderate": [], "minor": []}
        pgx_relevant_ddis = []

        for ddi in ddis:
            severity = ddi.get("severity", "moderate")
            by_severity.setdefault(severity, []).append(ddi)

            # Flag PGx-relevant DDIs (those involving CYP enzyme phenoconversion)
            if ddi.get("phenoconversion"):
                pgx_relevant_ddis.append({
                    "drug_a": ddi["drug_a"],
                    "drug_b": ddi["drug_b"],
                    "target_gene": ddi["phenoconversion"].get("target_gene", ""),
                    "effect": ddi["phenoconversion"].get("effect", ""),
                    "severity": severity,
                })

        # Calculate weighted score
        weighted_score = sum(
            DDI_WEIGHTS.get(sev, 1) * len(items)
            for sev, items in by_severity.items()
        )

        result = {
            "patient_id": patient.get("patient_id", "?"),
            "total_medications": len(medications),
            "total_ddis": len(ddis),
            "ddis_by_severity": {sev: len(items) for sev, items in by_severity.items()},
            "weighted_ddi_score": weighted_score,
            "pgx_relevant_ddis": pgx_relevant_ddis,
            "pgx_relevant_ddi_count": len(pgx_relevant_ddis),
            "ddi_risk_level": self._classify_risk(weighted_score),
            "ddi_details": ddis,
        }

        logger.debug(
            f"Patient {patient.get('patient_id', '?')}: "
            f"{len(ddis)} DDIs, weighted score {weighted_score}, "
            f"{len(pgx_relevant_ddis)} PGx-relevant"
        )
        return result

    def score_cohort(self, patients: list) -> list:
        """Score DDI burden for a list of patients."""
        results = []
        for patient in patients:
            results.append(self.score_patient(patient))
        return results

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _classify_risk(self, weighted_score: int) -> str:
        if weighted_score >= 9:
            return "high"
        elif weighted_score >= 4:
            return "moderate"
        elif weighted_score >= 1:
            return "low"
        return "none"
