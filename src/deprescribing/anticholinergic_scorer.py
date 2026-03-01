"""
Anticholinergic Burden Scorer
==============================
Calculates cumulative Anticholinergic Cognitive Burden (ACB) score
and classifies risk level for a patient's medication list.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.utils.logger import get_logger

logger = get_logger("anticholinergic_scorer")


class AnticholinergicScorer:
    """Calculates cumulative ACB score for a patient's medications."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def score_patient(self, patient: dict) -> dict:
        """Calculate ACB score for a patient."""
        pid = patient.get("patient_id", "?")
        medications = self._extract_medication_names(patient)

        acb_result = self.kb.get_total_acb_score(medications)
        total = acb_result["total_score"]
        risk = acb_result["risk_level"]
        contributions = acb_result["contributions"]

        if total > 0:
            logger.info(f"Patient {pid}: ACB total {total} ({risk}), "
                        f"{len(contributions)} contributing medications")

        return {
            "patient_id": pid,
            "total_acb_score": total,
            "risk_level": risk,
            "contributing_medications": contributions,
            "contributing_count": len(contributions),
            "high_acb_drugs": [c for c in contributions if c["score"] == 3],
            "moderate_acb_drugs": [c for c in contributions if c["score"] == 2],
            "low_acb_drugs": [c for c in contributions if c["score"] == 1],
        }

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]
