"""
Prescribing Cascade Detector
==============================
Identifies prescribing cascade patterns in a patient's medication list.
A cascade occurs when Drug A's side effect is treated by Drug B,
compounding polypharmacy.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.utils.logger import get_logger

logger = get_logger("cascade_detector")


class CascadeDetector:
    """Detects prescribing cascade patterns in medication lists."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def detect_cascades(self, patient: dict) -> dict:
        """Detect all prescribing cascades in a patient's medications."""
        pid = patient.get("patient_id", "?")
        medications = self._extract_medication_names(patient)

        cascades = self.kb.get_prescribing_cascades(medications)

        if cascades:
            logger.info(f"Patient {pid}: {len(cascades)} prescribing cascades detected")

        return {
            "patient_id": pid,
            "cascades": cascades,
            "cascade_count": len(cascades),
            "pgx_relevant_cascades": [c for c in cascades if c.get("pgx_relevance")],
            "medications_involved": list(set(
                drug for c in cascades
                for drug in c.get("trigger_drugs_found", []) + c.get("cascade_drugs_found", [])
            )),
        }

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]
