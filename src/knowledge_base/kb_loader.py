"""
Knowledge Base Loader
====================
Loads and provides lookup methods for the pharmacogenomics knowledge base.
"""

import json
from pathlib import Path
from typing import Optional

from src.utils.logger import get_logger

logger = get_logger("knowledge_base")


class KnowledgeBase:
    """Loads all PGx knowledge base JSON files and provides lookup methods."""

    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent
        self.base_path = Path(base_path)

        # Core KB files
        self.gene_drug_data = self._load_json("gene_drug_interactions.json")
        self.ddi_data = self._load_json("drug_drug_interactions.json")
        self.dosing_data = self._load_json("dosing_guidelines.json")

        # Extended KB files (geriatric deprescribing + oncology gap)
        self.pgx_drug_map_data = self._load_json("pgx_drug_map.json")
        self.beers_data = self._load_json("beers_criteria.json")
        self.stopp_start_data = self._load_json("stopp_start_criteria.json")
        self.acb_data = self._load_json("anticholinergic_burden.json")
        self.cascades_data = self._load_json("prescribing_cascades.json")

        # Build core lookup indexes
        self._gene_drug_index = {}
        for entry in self.gene_drug_data.get("gene_drug_interactions", []):
            key = (entry["gene"].lower(), entry["drug"].lower())
            self._gene_drug_index[key] = entry

        self._ddi_index = {}
        for entry in self.ddi_data.get("drug_drug_interactions", []):
            key_ab = (entry["drug_a"].lower(), entry["drug_b"].lower())
            key_ba = (entry["drug_b"].lower(), entry["drug_a"].lower())
            self._ddi_index[key_ab] = entry
            self._ddi_index[key_ba] = entry

        # Build extended indexes
        self._pgx_drug_index = {}
        for drug, info in self.pgx_drug_map_data.get("pgx_drug_map", {}).items():
            self._pgx_drug_index[drug.lower()] = info

        self._beers_index = {}
        for entry in self.beers_data.get("beers_criteria", []):
            self._beers_index[entry["drug"].lower()] = entry

        self._acb_index = self.acb_data.get("acb_scores", {})

        # Log KB metadata
        all_kb = [
            ("gene_drug_interactions", self.gene_drug_data),
            ("drug_drug_interactions", self.ddi_data),
            ("dosing_guidelines", self.dosing_data),
            ("pgx_drug_map", self.pgx_drug_map_data),
            ("beers_criteria", self.beers_data),
            ("stopp_start_criteria", self.stopp_start_data),
            ("anticholinergic_burden", self.acb_data),
            ("prescribing_cascades", self.cascades_data),
        ]
        for name, data in all_kb:
            meta = data.get("_metadata", {})
            if meta:
                logger.debug(f"{name} v{meta.get('version', '?')} (updated {meta.get('last_updated', '?')})")

        logger.info(f"Knowledge base loaded: {len(self._gene_drug_index)} gene-drug pairs, "
                    f"{len(self._ddi_index) // 2} DDIs, "
                    f"{len(self._pgx_drug_index)} PGx-mapped drugs, "
                    f"{len(self._beers_index)} Beers entries, "
                    f"{len(self._acb_index)} ACB-scored medications")

    def _load_json(self, filename: str) -> dict:
        filepath = self.base_path / filename
        if not filepath.exists():
            logger.warning(f"{filepath} not found, using empty dict")
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_kb_versions(self) -> dict:
        """Return version metadata for all loaded KB files."""
        versions = {}
        for name, data in [("gene_drug_interactions", self.gene_drug_data),
                           ("drug_drug_interactions", self.ddi_data),
                           ("dosing_guidelines", self.dosing_data),
                           ("pgx_drug_map", self.pgx_drug_map_data),
                           ("beers_criteria", self.beers_data),
                           ("stopp_start_criteria", self.stopp_start_data),
                           ("anticholinergic_burden", self.acb_data),
                           ("prescribing_cascades", self.cascades_data)]:
            meta = data.get("_metadata", {})
            versions[name] = meta.get("version", "unknown")
        return versions

    def get_gene_drug_interaction(self, gene: str, drug: str) -> Optional[dict]:
        """Get interaction entry for a gene-drug pair."""
        return self._gene_drug_index.get((gene.lower(), drug.lower()))

    def get_all_interactions_for_drug(self, drug: str) -> list:
        """Get all gene-drug interactions involving a specific drug."""
        results = []
        for entry in self.gene_drug_data.get("gene_drug_interactions", []):
            if entry["drug"].lower() == drug.lower():
                results.append(entry)
        return results

    def get_drug_drug_interactions(self, drug_list: list) -> list:
        """Find all pairwise DDIs among a list of drugs."""
        drug_list_lower = [d.lower() for d in drug_list]
        found = []
        seen = set()
        for i, drug_a in enumerate(drug_list_lower):
            for j, drug_b in enumerate(drug_list_lower):
                if i >= j:
                    continue
                pair_key = tuple(sorted([drug_a, drug_b]))
                if pair_key in seen:
                    continue
                ddi = self._ddi_index.get((drug_a, drug_b))
                if ddi:
                    found.append(ddi)
                    seen.add(pair_key)
        return found

    def get_dosing_guideline(self, drug: str) -> Optional[dict]:
        """Get dosing guideline for a specific drug."""
        guidelines = self.dosing_data.get("dosing_guidelines", {})
        return guidelines.get(drug.lower())

    def get_phenoconversion(self, drug_list: list, gene: str) -> Optional[str]:
        """
        Check if any drug in the list inhibits/induces the given gene's enzyme,
        returning the functional phenotype shift.
        """
        drug_list_lower = [d.lower() for d in drug_list]
        inhibitors = self.ddi_data.get("cyp_inhibitors", {}).get(gene, {})
        inducers = self.ddi_data.get("cyp_inducers", {}).get(gene, [])

        # Check strong inhibitors first
        for drug in drug_list_lower:
            if drug in [i.lower() for i in inhibitors.get("strong", [])]:
                return "poor_metabolizer"

        # Check moderate inhibitors
        for drug in drug_list_lower:
            if drug in [i.lower() for i in inhibitors.get("moderate", [])]:
                return "intermediate_metabolizer"

        # Check inducers
        for drug in drug_list_lower:
            if drug in [i.lower() for i in inducers]:
                return "ultra_rapid_metabolizer"

        return None

    def get_renal_adjustment(self, drug: str, egfr: float) -> Optional[dict]:
        """Check if drug needs renal dose adjustment based on eGFR."""
        renal = self.dosing_data.get("renal_adjustments", {})
        drugs = renal.get("drugs_requiring_renal_adjustment", {})
        drug_info = drugs.get(drug.lower())
        if not drug_info:
            return None
        cutoff = drug_info.get("egfr_cutoff", 0)
        if egfr < cutoff:
            return {
                "drug": drug,
                "egfr": egfr,
                "cutoff": cutoff,
                "action": drug_info.get("action", "Review dosing"),
                "renal_stage": self._get_renal_stage(egfr, renal),
            }
        return None

    def get_hepatic_adjustment(self, drug: str, alt_ratio: float) -> Optional[dict]:
        """Check if drug needs hepatic adjustment based on ALT/ULN ratio."""
        hepatic = self.dosing_data.get("hepatic_adjustments", {})
        drugs = hepatic.get("drugs_requiring_hepatic_adjustment", {})
        drug_info = drugs.get(drug.lower())
        if not drug_info:
            return None
        if alt_ratio > 3.0:
            return {
                "drug": drug,
                "alt_ratio": alt_ratio,
                "action": drug_info if isinstance(drug_info, str) else str(drug_info),
                "severity": "severe" if alt_ratio > 5.0 else "moderate",
            }
        return None

    def _get_renal_stage(self, egfr: float, renal: dict) -> str:
        thresholds = renal.get("egfr_thresholds", {})
        if egfr >= 90:
            return thresholds.get("normal", {}).get("label", "Normal")
        elif egfr >= 60:
            return thresholds.get("mild_impairment", {}).get("label", "Mild impairment")
        elif egfr >= 30:
            return thresholds.get("moderate_impairment", {}).get("label", "Moderate impairment")
        elif egfr >= 15:
            return thresholds.get("severe_impairment", {}).get("label", "Severe impairment")
        else:
            return thresholds.get("kidney_failure", {}).get("label", "Kidney failure")

    # ---- Extended KB lookup methods (geriatric deprescribing + oncology gap) ----

    def get_pgx_relevant_genes(self, drug: str) -> list:
        """Return list of pharmacogenes relevant to a drug, from pgx_drug_map."""
        entry = self._pgx_drug_index.get(drug.lower())
        if entry:
            logger.debug(f"PGx lookup: {drug} → {entry['genes']}")
            return entry["genes"]
        return []

    def get_pgx_drug_info(self, drug: str) -> Optional[dict]:
        """Return full PGx drug map entry (genes, cpic_level, fda_label, testing_recommendation)."""
        return self._pgx_drug_index.get(drug.lower())

    def get_beers_flag(self, drug: str) -> Optional[dict]:
        """Return Beers Criteria entry for a drug, or None if not flagged."""
        entry = self._beers_index.get(drug.lower())
        if entry:
            logger.debug(f"Beers flag: {drug} → {entry['category']} ({entry['severity']})")
        return entry

    def get_stopp_flags(self, drug: str, conditions: list = None) -> list:
        """Return STOPP criteria triggered by a drug, optionally filtered by patient conditions."""
        conditions = [c.lower() for c in (conditions or [])]
        drug_lower = drug.lower()
        flags = []
        for criterion in self.stopp_start_data.get("stopp_criteria", []):
            if drug_lower in [d.lower() for d in criterion.get("drugs", [])]:
                # If criterion has conditions, check at least one matches (or no conditions = always applies)
                crit_conditions = criterion.get("conditions", [])
                if not crit_conditions or any(c in conditions for c in crit_conditions):
                    flags.append(criterion)
        if flags:
            logger.debug(f"STOPP flags for {drug}: {len(flags)} criteria triggered")
        return flags

    def get_start_flags(self, conditions: list, current_drugs: list) -> list:
        """Return START criteria — medications that SHOULD be prescribed but aren't."""
        conditions_lower = [c.lower() for c in conditions]
        current_lower = [d.lower() for d in current_drugs]
        flags = []
        for criterion in self.stopp_start_data.get("start_criteria", []):
            crit_conditions = criterion.get("conditions", [])
            if any(c in conditions_lower for c in crit_conditions):
                # Check if patient is already on a recommended drug
                recommended = [d.lower() for d in criterion.get("recommended_drugs", [])]
                if not any(d in current_lower for d in recommended):
                    flags.append(criterion)
        if flags:
            logger.debug(f"START flags: {len(flags)} missing recommended medications")
        return flags

    def get_acb_score(self, drug: str) -> int:
        """Return ACB (Anticholinergic Cognitive Burden) score for a drug (0-3)."""
        entry = self._acb_index.get(drug.lower())
        if entry:
            return entry["score"]
        return 0

    def get_total_acb_score(self, drug_list: list) -> dict:
        """Calculate cumulative ACB score for a medication list."""
        total = 0
        contributions = []
        for drug in drug_list:
            score = self.get_acb_score(drug)
            if score > 0:
                total += score
                contributions.append({"drug": drug, "score": score})
        if total >= 6:
            risk_level = "high"
        elif total >= 3:
            risk_level = "moderate"
        else:
            risk_level = "low"
        logger.debug(f"ACB total: {total} ({risk_level}) from {len(contributions)} medications")
        return {"total_score": total, "risk_level": risk_level, "contributions": contributions}

    def get_prescribing_cascades(self, drug_list: list) -> list:
        """Detect prescribing cascade patterns in a medication list."""
        drug_list_lower = [d.lower() for d in drug_list]
        detected = []
        for cascade in self.cascades_data.get("cascades", []):
            trigger_drugs = [d.lower() for d in cascade.get("trigger_drugs", [])]
            cascade_drugs = [d.lower() for d in cascade.get("cascade_drugs", [])]
            has_trigger = any(d in drug_list_lower for d in trigger_drugs)
            has_cascade = any(d in drug_list_lower for d in cascade_drugs)
            if has_trigger and has_cascade:
                # Find the specific drugs involved
                trigger_found = [d for d in drug_list if d.lower() in trigger_drugs]
                cascade_found = [d for d in drug_list if d.lower() in cascade_drugs]
                detected.append({
                    "cascade_id": cascade["id"],
                    "name": cascade["name"],
                    "trigger_drugs_found": trigger_found,
                    "cascade_drugs_found": cascade_found,
                    "severity": cascade["severity"],
                    "recommendation": cascade["recommendation"],
                    "pgx_relevance": cascade.get("pgx_relevance"),
                })
        if detected:
            logger.debug(f"Prescribing cascades detected: {len(detected)} patterns in {len(drug_list)} medications")
        return detected

    # ---- Original helper methods ----

    def get_cyp_inhibitors_in_list(self, drug_list: list) -> dict:
        """Identify all CYP inhibitors present in the drug list."""
        drug_list_lower = [d.lower() for d in drug_list]
        found = {}
        all_inhibitors = self.ddi_data.get("cyp_inhibitors", {})
        for gene, strengths in all_inhibitors.items():
            for strength, drugs in strengths.items():
                for drug in drugs:
                    if drug.lower() in drug_list_lower:
                        if gene not in found:
                            found[gene] = []
                        found[gene].append({
                            "drug": drug,
                            "strength": strength,
                            "gene": gene,
                        })
        return found
