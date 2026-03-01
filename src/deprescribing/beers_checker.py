"""
Beers Criteria Checker
======================
Screens patient medications against the 2023 AGS Beers Criteria.
Only applies to patients aged 65 and older.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.utils.logger import get_logger

logger = get_logger("beers_checker")


class BeersChecker:
    """Screens medications against 2023 AGS Beers Criteria."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def check_patient(self, patient: dict) -> dict:
        """Screen all medications for a patient against Beers Criteria."""
        age = patient.get("demographics", {}).get("age", 0)
        pid = patient.get("patient_id", "?")

        if age < 65:
            logger.debug(f"Patient {pid}: age {age}, Beers Criteria not applicable")
            return {
                "patient_id": pid,
                "applicable": False,
                "reason": "Patient under 65 years old",
                "flags": [],
                "flag_count": 0,
            }

        medications = self._extract_medication_names(patient)
        conditions = self._extract_conditions(patient)
        flags = []

        for drug in medications:
            flag = self.kb.get_beers_flag(drug)
            if flag:
                # Check if condition-specific criteria apply
                crit_conditions = flag.get("conditions", [])
                if crit_conditions and not any(c in conditions for c in crit_conditions):
                    continue  # Condition-specific criterion doesn't apply

                flags.append({
                    "drug": drug,
                    "drug_class": flag.get("drug_class", ""),
                    "category": flag["category"],
                    "rationale": flag["rationale"],
                    "severity": flag["severity"],
                    "quality_of_evidence": flag.get("quality_of_evidence", ""),
                    "strength_of_recommendation": flag.get("strength_of_recommendation", ""),
                    "alternatives": flag.get("alternatives", []),
                    "acb_score": flag.get("acb_score", 0),
                })

        if flags:
            logger.info(f"Patient {pid}: {len(flags)} Beers flags from {len(medications)} medications")

        return {
            "patient_id": pid,
            "applicable": True,
            "age": age,
            "flags": flags,
            "flag_count": len(flags),
            "avoid_count": sum(1 for f in flags if f["category"] == "avoid"),
            "caution_count": sum(1 for f in flags if f["category"] == "caution"),
        }

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _extract_conditions(self, patient: dict) -> list:
        """Extract conditions from clinical context for condition-specific Beers criteria."""
        context = patient.get("clinical_context", {})
        conditions = context.get("conditions", [])
        # Also extract from comorbidities if present
        conditions.extend(context.get("comorbidities", []))
        return [c.lower() for c in conditions]
