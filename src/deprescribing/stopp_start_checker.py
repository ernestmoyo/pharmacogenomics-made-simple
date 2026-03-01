"""
STOPP/START Criteria Checker
============================
Screens medications against STOPP v3 (drugs to stop) and
START v3 (drugs that should be prescribed) criteria.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.utils.logger import get_logger

logger = get_logger("stopp_start_checker")


class StoppStartChecker:
    """Screens medications against STOPP/START v3 criteria."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def check_patient(self, patient: dict) -> dict:
        """Run full STOPP/START screening for a patient."""
        pid = patient.get("patient_id", "?")
        age = patient.get("demographics", {}).get("age", 0)

        if age < 65:
            return {
                "patient_id": pid,
                "applicable": False,
                "stopp_flags": [],
                "start_flags": [],
            }

        medications = self._extract_medication_names(patient)
        conditions = self._extract_conditions(patient)

        # STOPP screening
        stopp_flags = []
        for drug in medications:
            flags = self.kb.get_stopp_flags(drug, conditions)
            for flag in flags:
                stopp_flags.append({
                    "criterion_id": flag["id"],
                    "section": flag["section"],
                    "drug": drug,
                    "criterion": flag["criterion"],
                    "rationale": flag["rationale"],
                    "severity": flag["severity"],
                    "action": flag["action"],
                })

        # START screening
        start_flags = self.kb.get_start_flags(conditions, medications)
        start_results = []
        for flag in start_flags:
            start_results.append({
                "criterion_id": flag["id"],
                "section": flag["section"],
                "criterion": flag["criterion"],
                "recommended_drugs": flag.get("recommended_drugs", []),
                "rationale": flag["rationale"],
                "severity": flag["severity"],
            })

        if stopp_flags or start_results:
            logger.info(f"Patient {pid}: {len(stopp_flags)} STOPP, {len(start_results)} START flags")

        return {
            "patient_id": pid,
            "applicable": True,
            "stopp_flags": stopp_flags,
            "stopp_count": len(stopp_flags),
            "start_flags": start_results,
            "start_count": len(start_results),
        }

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _extract_conditions(self, patient: dict) -> list:
        context = patient.get("clinical_context", {})
        conditions = list(context.get("conditions", []))
        conditions.extend(context.get("comorbidities", []))

        # Infer common conditions from medications and context
        medications = self._extract_medication_names(patient)
        age = patient.get("demographics", {}).get("age", 0)

        if age >= 65:
            conditions.append("age_65_plus")

        # Check lab-based conditions
        lab_values = patient.get("lab_values", {})
        egfr = lab_values.get("egfr")
        if egfr is not None:
            if egfr < 30:
                conditions.append("egfr_below_30")
            if egfr < 50:
                conditions.append("egfr_below_50")

        return [c.lower() for c in conditions]
