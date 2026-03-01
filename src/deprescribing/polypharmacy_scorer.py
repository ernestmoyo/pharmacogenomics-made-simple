"""
Polypharmacy Risk Scorer
========================
Combines multiple risk signals into a single 0-100 polypharmacy risk score:
- Medication count
- DDI burden
- Beers flags
- STOPP flags
- ACB score
- Prescribing cascades
"""

from src.utils.logger import get_logger

logger = get_logger("polypharmacy_scorer")

# Component weights for the composite score (total = 100)
WEIGHTS = {
    "medication_count": 15,   # Raw polypharmacy count
    "ddi_burden": 20,         # Drug-drug interactions
    "beers_flags": 20,        # Beers Criteria violations
    "stopp_flags": 15,        # STOPP criteria
    "acb_score": 20,          # Anticholinergic burden
    "cascades": 10,           # Prescribing cascades
}


class PolypharmacyScorer:
    """Calculates a composite polypharmacy risk score (0-100)."""

    def score_patient(self, medication_count: int, ddi_count: int,
                      beers_count: int, stopp_count: int,
                      acb_score: int, cascade_count: int) -> dict:
        """Calculate composite polypharmacy risk score from component signals."""

        # Normalize each component to 0-1 range
        med_score = min(medication_count / 15, 1.0)     # 15+ meds = max
        ddi_score = min(ddi_count / 5, 1.0)              # 5+ DDIs = max
        beers_score = min(beers_count / 4, 1.0)           # 4+ Beers = max
        stopp_score = min(stopp_count / 3, 1.0)           # 3+ STOPP = max
        acb_norm = min(acb_score / 6, 1.0)                # 6+ ACB = max
        cascade_score = min(cascade_count / 3, 1.0)       # 3+ cascades = max

        # Weighted composite
        composite = (
            med_score * WEIGHTS["medication_count"] +
            ddi_score * WEIGHTS["ddi_burden"] +
            beers_score * WEIGHTS["beers_flags"] +
            stopp_score * WEIGHTS["stopp_flags"] +
            acb_norm * WEIGHTS["acb_score"] +
            cascade_score * WEIGHTS["cascades"]
        )
        composite = round(min(composite, 100), 1)

        # Risk classification
        if composite >= 70:
            risk_level = "high"
        elif composite >= 40:
            risk_level = "moderate"
        elif composite >= 15:
            risk_level = "low"
        else:
            risk_level = "minimal"

        result = {
            "composite_score": composite,
            "risk_level": risk_level,
            "components": {
                "medication_count": {"value": medication_count, "normalized": round(med_score, 2), "weighted": round(med_score * WEIGHTS["medication_count"], 1)},
                "ddi_burden": {"value": ddi_count, "normalized": round(ddi_score, 2), "weighted": round(ddi_score * WEIGHTS["ddi_burden"], 1)},
                "beers_flags": {"value": beers_count, "normalized": round(beers_score, 2), "weighted": round(beers_score * WEIGHTS["beers_flags"], 1)},
                "stopp_flags": {"value": stopp_count, "normalized": round(stopp_score, 2), "weighted": round(stopp_score * WEIGHTS["stopp_flags"], 1)},
                "acb_score": {"value": acb_score, "normalized": round(acb_norm, 2), "weighted": round(acb_norm * WEIGHTS["acb_score"], 1)},
                "cascades": {"value": cascade_count, "normalized": round(cascade_score, 2), "weighted": round(cascade_score * WEIGHTS["cascades"], 1)},
            },
        }

        logger.debug(f"Polypharmacy score: {composite} ({risk_level})")
        return result
