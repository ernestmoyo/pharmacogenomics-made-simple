"""
Risk Scoring System
===================
Scores individual findings and overall patient risk on a 0-100 scale.
"""

from src.utils.logger import get_logger

logger = get_logger("risk_scorer")


class RiskScorer:
    """Scores pharmacogenomic findings by clinical severity and evidence quality."""

    SEVERITY_RANGES = {
        "critical": (90, 100),
        "high": (70, 89),
        "moderate": (40, 69),
        "low": (10, 39),
        "informational": (1, 9),
    }

    EVIDENCE_MULTIPLIER = {
        "CPIC Level A": 1.0,
        "CPIC Level B": 0.85,
        "CPIC Level C": 0.65,
        "strong": 1.0,
        "moderate": 0.85,
        "weak": 0.65,
        "standard_of_care": 0.95,
    }

    def score_findings(self, findings: list) -> list:
        """Score and sort all findings by clinical risk."""
        scored = []
        for finding in findings:
            score = self._calculate_score(finding)
            scored_finding = {**finding, "risk_score": score}
            scored.append(scored_finding)

        # Sort by risk score descending
        scored.sort(key=lambda f: f["risk_score"], reverse=True)
        return scored

    def _calculate_score(self, finding: dict) -> float:
        """Calculate a 0-100 risk score for a single finding."""
        severity = finding.get("severity", "low")
        low, high = self.SEVERITY_RANGES.get(severity, (10, 39))
        base_score = (low + high) / 2

        # Evidence level adjustment
        evidence = finding.get("evidence_level", "")
        multiplier = self.EVIDENCE_MULTIPLIER.get(evidence, 0.75)
        score = base_score * multiplier

        # FDA label bonus (+5 points for FDA-recognized)
        if finding.get("fda_label"):
            score += 5

        # Contraindication escalation
        if finding.get("finding_type") == "contraindication":
            score = max(score, 92)

        # Phenoconversion compounds gene effect (+8 points)
        if finding.get("source") == "phenoconversion":
            score += 8

        # DDI compounding (if DDI affects same gene as a gene-drug finding)
        if finding.get("finding_type") == "drug_drug_interaction":
            if finding.get("gene"):
                score += 5

        # Renal/hepatic warnings are clinically actionable
        if finding.get("finding_type") in ("renal_warning", "hepatic_warning"):
            score = max(score, 45)

        return min(round(score, 1), 100)

    def get_patient_risk_summary(self, scored_findings: list) -> dict:
        """Generate overall patient risk summary from scored findings."""
        if not scored_findings:
            return {
                "category": "Low - Informational",
                "overall_score": 0,
                "critical_count": 0,
                "high_count": 0,
                "moderate_count": 0,
                "low_count": 0,
                "informational_count": 0,
                "total_findings": 0,
                "actionable_count": 0,
                "max_score": 0,
            }

        critical = [f for f in scored_findings if f.get("severity") == "critical"]
        high = [f for f in scored_findings if f.get("severity") == "high"]
        moderate = [f for f in scored_findings if f.get("severity") == "moderate"]
        low = [f for f in scored_findings if f.get("severity") == "low"]
        info = [f for f in scored_findings if f.get("severity") == "informational"]

        actionable = [f for f in scored_findings if f.get("severity") in ("critical", "high", "moderate")]

        max_score = max(f.get("risk_score", 0) for f in scored_findings)
        avg_score = sum(f.get("risk_score", 0) for f in scored_findings) / len(scored_findings)

        # Overall category based on highest finding
        if critical:
            category = "Critical - Immediate Action Required"
        elif high:
            category = "High - Action Recommended"
        elif moderate:
            category = "Moderate - Monitor Closely"
        else:
            category = "Low - Informational"

        return {
            "category": category,
            "overall_score": round(max_score, 1),
            "average_score": round(avg_score, 1),
            "critical_count": len(critical),
            "high_count": len(high),
            "moderate_count": len(moderate),
            "low_count": len(low),
            "informational_count": len(info),
            "total_findings": len(scored_findings),
            "actionable_count": len(actionable),
            "max_score": round(max_score, 1),
        }
