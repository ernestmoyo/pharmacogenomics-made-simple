"""
Deprescribing Recommender
=========================
The main orchestrator for geriatric deprescribing analysis.
Aggregates all signals (Beers, STOPP, ACB, cascades, PGx) per medication,
prioritizes deprescribing recommendations, and generates the PGx overlay
that shows what pharmacogenomic data adds beyond standard criteria.
"""

from src.knowledge_base.kb_loader import KnowledgeBase
from src.interpretation.engine import InterpretationEngine
from src.deprescribing.beers_checker import BeersChecker
from src.deprescribing.stopp_start_checker import StoppStartChecker
from src.deprescribing.anticholinergic_scorer import AnticholinergicScorer
from src.deprescribing.cascade_detector import CascadeDetector
from src.deprescribing.polypharmacy_scorer import PolypharmacyScorer
from src.utils.logger import get_logger

logger = get_logger("deprescribing")


class DeprescribingRecommender:
    """Full deprescribing analysis for geriatric patients."""

    def __init__(self, kb: KnowledgeBase, engine: InterpretationEngine):
        self.kb = kb
        self.engine = engine
        self.beers_checker = BeersChecker(kb)
        self.stopp_start_checker = StoppStartChecker(kb)
        self.acb_scorer = AnticholinergicScorer(kb)
        self.cascade_detector = CascadeDetector(kb)
        self.polypharmacy_scorer = PolypharmacyScorer()

    def analyze_patient(self, patient: dict) -> dict:
        """Run complete deprescribing analysis on a single patient."""
        pid = patient.get("patient_id", "?")
        medications = self._extract_medication_names(patient)

        # 1. Run all checkers
        beers_result = self.beers_checker.check_patient(patient)
        stopp_start_result = self.stopp_start_checker.check_patient(patient)
        acb_result = self.acb_scorer.score_patient(patient)
        cascade_result = self.cascade_detector.detect_cascades(patient)

        # 2. Run PGx interpretation
        pgx_findings = self.engine.generate_findings(patient)

        # 3. DDI check
        ddis = self.kb.get_drug_drug_interactions(medications)

        # 4. Calculate polypharmacy score
        poly_score = self.polypharmacy_scorer.score_patient(
            medication_count=len(medications),
            ddi_count=len(ddis),
            beers_count=beers_result.get("flag_count", 0),
            stopp_count=stopp_start_result.get("stopp_count", 0),
            acb_score=acb_result.get("total_acb_score", 0),
            cascade_count=cascade_result.get("cascade_count", 0),
        )

        # 5. Build per-medication flag summary
        med_flags = self._build_medication_flags(
            medications, beers_result, stopp_start_result,
            acb_result, cascade_result, pgx_findings
        )

        # 6. Prioritize deprescribing recommendations
        recommendations = self._prioritize_recommendations(med_flags)

        # 7. Generate PGx overlay (key differentiator)
        pgx_overlay = self._generate_pgx_overlay(pgx_findings, beers_result, med_flags)

        result = {
            "patient_id": pid,
            "demographics": patient.get("demographics", {}),
            "medication_count": len(medications),
            "medications": medications,
            "polypharmacy_score": poly_score,
            "beers_result": beers_result,
            "stopp_start_result": stopp_start_result,
            "acb_result": acb_result,
            "cascade_result": cascade_result,
            "pgx_findings": pgx_findings,
            "ddis": ddis,
            "medication_flags": med_flags,
            "recommendations": recommendations,
            "pgx_overlay": pgx_overlay,
        }

        logger.info(
            f"Patient {pid}: score {poly_score['composite_score']} ({poly_score['risk_level']}), "
            f"{len(recommendations)} recommendations, "
            f"{len(pgx_overlay)} PGx overlay insights"
        )
        return result

    def analyze_cohort(self, patients: list) -> list:
        """Analyze a list of geriatric patients."""
        results = []
        for patient in patients:
            results.append(self.analyze_patient(patient))
        logger.info(f"Deprescribing cohort analysis complete: {len(results)} patients")
        return results

    def _extract_medication_names(self, patient: dict) -> list:
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _build_medication_flags(self, medications, beers_result, stopp_start_result,
                                 acb_result, cascade_result, pgx_findings):
        """Build a per-medication summary of all flags."""
        flags_by_drug = {}

        for drug in medications:
            flags_by_drug[drug] = {
                "drug": drug,
                "beers_flag": None,
                "stopp_flags": [],
                "acb_score": 0,
                "cascade_involvement": [],
                "pgx_findings": [],
                "total_flag_count": 0,
                "priority_score": 0,
            }

        # Beers flags
        for flag in beers_result.get("flags", []):
            drug = flag["drug"]
            if drug in flags_by_drug:
                flags_by_drug[drug]["beers_flag"] = flag

        # STOPP flags
        for flag in stopp_start_result.get("stopp_flags", []):
            drug = flag["drug"]
            if drug in flags_by_drug:
                flags_by_drug[drug]["stopp_flags"].append(flag)

        # ACB scores
        for contrib in acb_result.get("contributing_medications", []):
            drug = contrib["drug"]
            if drug in flags_by_drug:
                flags_by_drug[drug]["acb_score"] = contrib["score"]

        # Cascade involvement
        for cascade in cascade_result.get("cascades", []):
            for drug in cascade.get("trigger_drugs_found", []) + cascade.get("cascade_drugs_found", []):
                if drug in flags_by_drug:
                    flags_by_drug[drug]["cascade_involvement"].append(cascade["name"])

        # PGx findings
        for finding in pgx_findings:
            drug = finding.get("drug", "")
            if drug in flags_by_drug:
                flags_by_drug[drug]["pgx_findings"].append(finding)

        # Calculate totals and priority
        for drug, info in flags_by_drug.items():
            count = 0
            priority = 0

            if info["beers_flag"]:
                count += 1
                priority += 3 if info["beers_flag"]["category"] == "avoid" else 1

            count += len(info["stopp_flags"])
            priority += sum(2 if f["severity"] == "high" else 1 for f in info["stopp_flags"])

            if info["acb_score"] >= 3:
                count += 1
                priority += 3
            elif info["acb_score"] >= 2:
                count += 1
                priority += 2

            count += len(info["cascade_involvement"])
            priority += len(info["cascade_involvement"])

            for f in info["pgx_findings"]:
                count += 1
                sev = f.get("severity", "")
                priority += {"critical": 5, "high": 3, "moderate": 2}.get(sev, 1)

            info["total_flag_count"] = count
            info["priority_score"] = priority

        return flags_by_drug

    def _prioritize_recommendations(self, med_flags: dict) -> list:
        """Generate prioritized deprescribing recommendations sorted by urgency."""
        recommendations = []

        for drug, info in sorted(med_flags.items(), key=lambda x: -x[1]["priority_score"]):
            if info["total_flag_count"] == 0:
                continue

            reasons = []
            actions = []
            alternatives = []

            if info["beers_flag"]:
                bf = info["beers_flag"]
                reasons.append(f"Beers Criteria: {bf['category']} — {bf['rationale']}")
                if bf.get("alternatives"):
                    alternatives.extend(bf["alternatives"])
                if bf["category"] == "avoid":
                    actions.append("discontinue")
                else:
                    actions.append("review_and_reduce")

            for sf in info["stopp_flags"]:
                reasons.append(f"STOPP {sf['criterion_id']}: {sf['criterion']}")
                actions.append(sf["action"])

            if info["acb_score"] >= 2:
                reasons.append(f"Anticholinergic burden: ACB score {info['acb_score']}")
                actions.append("switch_to_lower_acb_alternative")

            for cascade_name in info["cascade_involvement"]:
                reasons.append(f"Prescribing cascade: {cascade_name}")
                actions.append("review_cascade_origin")

            for pf in info["pgx_findings"]:
                reasons.append(f"PGx: {pf.get('summary', '')}")
                if pf.get("recommendation"):
                    actions.append(pf["recommendation"])

            # Deduplicate actions
            unique_actions = list(dict.fromkeys(actions))
            unique_alternatives = list(dict.fromkeys(alternatives))

            recommendations.append({
                "drug": drug,
                "priority_score": info["priority_score"],
                "flag_count": info["total_flag_count"],
                "reasons": reasons,
                "recommended_actions": unique_actions,
                "alternatives": unique_alternatives,
                "acb_score": info["acb_score"],
                "urgency": "high" if info["priority_score"] >= 5 else
                           "moderate" if info["priority_score"] >= 3 else "low",
            })

        return recommendations

    def _generate_pgx_overlay(self, pgx_findings, beers_result, med_flags) -> list:
        """Generate the PGx overlay — insights ONLY visible with PGx data.

        This is the key differentiator: what does pharmacogenomics reveal
        that standard Beers/STOPP/ACB criteria alone would miss?
        """
        overlay = []

        beers_drugs = {f["drug"] for f in beers_result.get("flags", [])}

        for finding in pgx_findings:
            drug = finding.get("drug", "")
            severity = finding.get("severity", "")
            gene = finding.get("gene", "")

            if severity in ("critical", "high", "moderate"):
                is_new_insight = drug not in beers_drugs
                overlay.append({
                    "drug": drug,
                    "gene": gene,
                    "severity": severity,
                    "finding_type": finding.get("finding_type", ""),
                    "summary": finding.get("summary", ""),
                    "recommendation": finding.get("recommendation", ""),
                    "unique_to_pgx": is_new_insight,
                    "adds_to_beers": not is_new_insight,
                    "clinical_value": (
                        f"PGx UNIQUE: {gene} finding for {drug} — NOT flagged by standard criteria"
                        if is_new_insight else
                        f"PGx ADDITIVE: {gene} finding strengthens Beers flag for {drug}"
                    ),
                })

        if overlay:
            unique = sum(1 for o in overlay if o["unique_to_pgx"])
            additive = sum(1 for o in overlay if o["adds_to_beers"])
            logger.info(f"PGx overlay: {unique} unique insights, {additive} additive to Beers")

        return overlay
