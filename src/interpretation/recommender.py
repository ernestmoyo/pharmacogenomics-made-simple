"""
Recommendation Generator
========================
Generates structured, prioritized clinical recommendations from scored findings.
"""

from src.utils.logger import get_logger

logger = get_logger("recommender")


class Recommender:
    """Generates actionable clinical recommendations from pharmacogenomic findings."""

    ACTION_MAP = {
        "contraindicated": "stop_drug",
        "switch_drug": "switch_drug",
        "reduce_50_percent": "reduce_dose",
        "reduce_25_percent": "reduce_dose",
        "reduce_30_percent": "reduce_dose",
        "reduce_30_to_50_percent": "reduce_dose",
        "reduce_90_percent": "reduce_dose",
        "reduce_major": "reduce_dose",
        "reduce_moderate": "reduce_dose",
        "reduce_dose": "reduce_dose",
        "reduce_dose_or_switch": "switch_drug",
        "increase_dose": "increase_monitoring",
        "increase_dose_or_switch": "switch_drug",
        "switch_or_increase": "switch_drug",
        "use_alternative_preferred": "switch_drug",
        "monitor": "increase_monitoring",
        "none": "no_change",
    }

    ALTERNATIVE_DRUGS = {
        "codeine": ["morphine", "hydromorphone", "acetaminophen", "ketorolac"],
        "tramadol": ["morphine", "hydromorphone", "acetaminophen", "ketorolac"],
        "citalopram": ["sertraline", "fluoxetine", "bupropion"],
        "escitalopram": ["sertraline", "fluoxetine", "bupropion"],
        "clopidogrel": ["prasugrel (10 mg/day)", "ticagrelor (90 mg BID)"],
        "simvastatin": ["rosuvastatin", "pravastatin"],
        "tamoxifen": ["aromatase inhibitor (anastrozole/letrozole)", "raloxifene"],
        "fluorouracil": ["alternative chemotherapy regimen per oncologist"],
        "capecitabine": ["alternative chemotherapy regimen per oncologist"],
        "nortriptyline": ["sertraline", "bupropion", "mirtazapine"],
        "warfarin": ["dose adjustment per pharmacogenomic algorithm"],
        "carbamazepine": ["valproate", "lamotrigine", "lithium"],
        "atomoxetine": ["methylphenidate", "lisdexamfetamine"],
        "mercaptopurine": ["dose-adjusted mercaptopurine (10% of standard)"],
        "irinotecan": ["dose-reduced irinotecan (70% of standard)"],
        "ondansetron": ["granisetron"],
    }

    DOSE_ADJUSTMENTS = {
        "reduce_50_percent": "Reduce dose by 50%",
        "reduce_25_percent": "Reduce dose by 25%",
        "reduce_30_percent": "Reduce dose by 30%",
        "reduce_30_to_50_percent": "Reduce dose by 30-50%",
        "reduce_90_percent": "Reduce dose to 10% of standard",
        "reduce_major": "Major dose reduction required (see pharmacogenomic dosing table)",
        "reduce_moderate": "Moderate dose reduction required",
    }

    def generate_recommendations(self, scored_findings: list, patient: dict) -> list:
        """Generate prioritized clinical recommendations from scored findings."""
        recommendations = []

        for finding in scored_findings:
            severity = finding.get("severity", "low")
            if severity == "informational":
                continue

            rec = self._build_recommendation(finding, patient)
            if rec:
                recommendations.append(rec)

        # Deduplicate by drug (keep highest priority)
        recommendations = self._deduplicate(recommendations)

        # Sort by priority
        recommendations.sort(key=lambda r: r["priority"])

        return recommendations

    def _build_recommendation(self, finding: dict, patient: dict) -> dict:
        """Build a single recommendation from a finding."""
        severity = finding.get("severity", "low")
        drug = finding.get("drug", "")
        finding_type = finding.get("finding_type", "")
        dosing_adj = finding.get("dosing_adjustment", "none")

        # Determine priority
        priority = self._get_priority(severity, finding_type)

        # Determine action type
        if finding_type == "contraindication":
            action_type = "stop_drug"
        elif finding_type in ("drug_drug_interaction", "phenoconversion"):
            action_type = self._get_ddi_action(finding)
        elif finding_type in ("renal_warning", "hepatic_warning"):
            action_type = "increase_monitoring"
        else:
            action_type = self.ACTION_MAP.get(dosing_adj, "inform_only")

        # Get alternatives
        base_drug = drug.split(" + ")[0] if " + " in drug else drug
        alternatives = self.ALTERNATIVE_DRUGS.get(base_drug.lower(), [])

        # Build dose suggestion
        dose_suggestion = self.DOSE_ADJUSTMENTS.get(dosing_adj, "")

        # Build monitoring plan
        monitoring = self._get_monitoring_plan(finding, action_type)

        # Time frame
        time_frame = self._get_time_frame(severity, action_type)

        # Rationale
        rationale = self._build_rationale(finding)

        return {
            "priority": priority,
            "action_type": action_type,
            "drug": drug,
            "gene": finding.get("gene", ""),
            "phenotype": finding.get("phenotype", ""),
            "finding_type": finding_type,
            "severity": severity,
            "suggested_alternatives": alternatives,
            "suggested_dose": dose_suggestion,
            "rationale": rationale,
            "monitoring_plan": monitoring,
            "time_frame": time_frame,
            "recommendation_text": finding.get("recommendation", ""),
            "evidence_level": finding.get("evidence_level", ""),
            "fda_label": finding.get("fda_label", False),
            "risk_score": finding.get("risk_score", 0),
            "therapeutic_area": finding.get("therapeutic_area", ""),
        }

    def _get_priority(self, severity: str, finding_type: str) -> int:
        """Assign priority 1-4 based on severity and type."""
        if severity == "critical" or finding_type == "contraindication":
            return 1
        elif severity == "high":
            return 2
        elif severity == "moderate":
            return 3
        else:
            return 4

    def _get_ddi_action(self, finding: dict) -> str:
        """Determine action for DDI findings."""
        severity = finding.get("severity", "")
        if severity in ("critical", "high"):
            return "switch_drug"
        return "increase_monitoring"

    def _get_monitoring_plan(self, finding: dict, action_type: str) -> str:
        """Generate monitoring plan based on finding type and action."""
        drug = finding.get("drug", "").lower()
        gene = finding.get("gene", "")

        if "warfarin" in drug:
            return "Monitor INR every 2-3 days until stable, then weekly. Target INR 2.0-3.0."
        elif action_type == "stop_drug":
            return "Discontinue medication. Monitor for withdrawal effects. Initiate alternative therapy."
        elif action_type == "reduce_dose":
            return f"Implement dose reduction. Monitor for therapeutic response and side effects at 2 and 4 weeks."
        elif action_type == "switch_drug":
            return "Transition to alternative medication. Monitor for efficacy and tolerability at 2-4 weeks."
        elif "tamoxifen" in drug:
            return "Consider endoxifen level monitoring after dose change. Reassess at 3 months."
        elif gene == "DPYD":
            return "If dose-reduced fluoropyrimidine used, monitor CBC and mucositis assessment before each cycle."
        elif gene == "TPMT":
            return "Monitor TGN levels and CBC weekly for first month, then biweekly."
        elif gene == "UGT1A1":
            return "Monitor CBC and assess for diarrhea before each chemotherapy cycle."
        elif "statin" in finding.get("drug_class", "") or "simvastatin" in drug:
            return "Monitor for muscle symptoms (pain, weakness). Check CK if symptomatic."
        elif gene == "SLCO1B1":
            return "Monitor for muscle symptoms. Check CK if symptomatic."
        else:
            return "Monitor for therapeutic response and adverse effects per standard of care."

    def _get_time_frame(self, severity: str, action_type: str) -> str:
        """Determine recommended time frame for action."""
        if severity == "critical" or action_type == "stop_drug":
            return "immediate"
        elif severity == "high":
            return "next_visit"
        else:
            return "routine"

    def _build_rationale(self, finding: dict) -> str:
        """Build clinical rationale text."""
        parts = []

        if finding.get("gene") and finding.get("phenotype"):
            gene = finding["gene"]
            phenotype = finding["phenotype"].replace("_", " ")
            parts.append(f"Patient is a {phenotype} for {gene}.")

        if finding.get("mechanism"):
            parts.append(finding["mechanism"])

        if finding.get("clinical_consequence"):
            parts.append(f"Clinical risk: {finding['clinical_consequence']}.")

        if finding.get("evidence_level"):
            parts.append(f"Evidence: {finding['evidence_level']}.")

        return " ".join(parts)

    def _deduplicate(self, recommendations: list) -> list:
        """Deduplicate recommendations by drug, keeping highest priority."""
        seen = {}
        for rec in recommendations:
            drug_key = rec["drug"].lower()
            if drug_key in seen:
                if rec["priority"] < seen[drug_key]["priority"]:
                    seen[drug_key] = rec
                elif rec["priority"] == seen[drug_key]["priority"] and rec["risk_score"] > seen[drug_key]["risk_score"]:
                    seen[drug_key] = rec
            else:
                seen[drug_key] = rec
        return list(seen.values())
