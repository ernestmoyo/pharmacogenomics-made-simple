"""
Knowledge Base Loader
====================
Loads and provides lookup methods for the pharmacogenomics knowledge base.
"""

import json
from pathlib import Path
from typing import Optional


class KnowledgeBase:
    """Loads all PGx knowledge base JSON files and provides lookup methods."""

    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent
        self.base_path = Path(base_path)

        self.gene_drug_data = self._load_json("gene_drug_interactions.json")
        self.ddi_data = self._load_json("drug_drug_interactions.json")
        self.dosing_data = self._load_json("dosing_guidelines.json")

        # Build lookup indexes
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

    def _load_json(self, filename: str) -> dict:
        filepath = self.base_path / filename
        if not filepath.exists():
            print(f"  Warning: {filepath} not found, using empty dict")
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

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
