"""
Pharmacogenomics Interpretation Engine
======================================
Core analysis engine that evaluates patient genotype against medications
and generates clinical findings with drug-drug-gene interaction logic.
"""

from typing import Optional
from src.knowledge_base.kb_loader import KnowledgeBase


class InterpretationEngine:
    """Analyzes patient pharmacogenomic data against their medication list."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def generate_findings(self, patient: dict) -> list:
        """Run the full analysis pipeline and return all clinical findings."""
        findings = []

        medications = self._extract_medication_names(patient)
        genotype = patient.get("genotype", {})
        lab_values = patient.get("lab_values", {})

        # 1. Gene-drug interactions
        findings.extend(self._check_gene_drug_interactions(medications, genotype))

        # 2. Phenoconversion adjustments (DDI shifting functional phenotype)
        findings.extend(self._check_phenoconversion(medications, genotype))

        # 3. Drug-drug interactions
        findings.extend(self._check_drug_drug_interactions(medications))

        # 4. Renal adjustments
        egfr = lab_values.get("egfr")
        if egfr is not None:
            findings.extend(self._check_renal_adjustments(medications, egfr))

        # 5. Hepatic adjustments
        alt = lab_values.get("alt")
        if alt is not None:
            # Assume ULN for ALT is 40 U/L
            alt_ratio = alt / 40.0
            findings.extend(self._check_hepatic_adjustments(medications, alt_ratio))

        # Deduplicate findings (same gene+drug combination)
        findings = self._deduplicate_findings(findings)

        return findings

    def analyze_patient(self, patient: dict) -> dict:
        """Full analysis returning structured report data."""
        findings = self.generate_findings(patient)
        medications = self._extract_medication_names(patient)
        ddis = self.kb.get_drug_drug_interactions(medications)

        return {
            "patient_id": patient.get("patient_id"),
            "findings": findings,
            "drug_drug_interactions": ddis,
            "medications_analyzed": len(medications),
            "genes_tested": list(patient.get("genotype", {}).keys()),
        }

    def _extract_medication_names(self, patient: dict) -> list:
        """Extract medication names from patient data."""
        meds = patient.get("medications", [])
        return [m if isinstance(m, str) else m.get("name", "") for m in meds]

    def _check_gene_drug_interactions(self, medications: list, genotype: dict) -> list:
        """Check each medication against patient genotype."""
        findings = []
        for drug in medications:
            interactions = self.kb.get_all_interactions_for_drug(drug)
            for interaction in interactions:
                gene = interaction["gene"]
                gene_data = genotype.get(gene)
                if not gene_data:
                    continue

                phenotype = gene_data.get("phenotype", "")
                phenotype_impacts = interaction.get("phenotype_impacts", {})
                impact = phenotype_impacts.get(phenotype)
                if not impact:
                    continue

                risk_level = impact.get("risk_level", "low")
                if risk_level == "low":
                    # Still record but as informational
                    finding_type = "gene_drug_interaction"
                    severity = "informational"
                else:
                    finding_type = "gene_drug_interaction"
                    severity = risk_level

                dosing_adj = impact.get("dosing_adjustment", "none")
                if dosing_adj == "contraindicated":
                    finding_type = "contraindication"
                    severity = "critical"

                findings.append({
                    "finding_type": finding_type,
                    "severity": severity,
                    "gene": gene,
                    "drug": drug,
                    "phenotype": phenotype,
                    "diplotype": gene_data.get("diplotype", gene_data.get("variant", gene_data.get("allele", ""))),
                    "summary": f"{gene} {self._format_phenotype(phenotype)}: {impact.get('effect', '')}",
                    "recommendation": impact.get("recommendation", ""),
                    "clinical_consequence": impact.get("clinical_consequence", ""),
                    "dosing_adjustment": dosing_adj,
                    "evidence_level": impact.get("evidence_level", ""),
                    "fda_label": impact.get("fda_label", False),
                    "cpic_guideline": interaction.get("cpic_guideline", ""),
                    "references": interaction.get("references", []),
                    "therapeutic_area": interaction.get("therapeutic_area", ""),
                    "drug_class": interaction.get("drug_class", ""),
                    "mechanism": interaction.get("mechanism", ""),
                    "source": "genotype",
                })

        return findings

    def _check_phenoconversion(self, medications: list, genotype: dict) -> list:
        """Check if concomitant drugs shift functional phenotype via enzyme inhibition."""
        findings = []
        genes_to_check = ["CYP2D6", "CYP2C19", "CYP2C9", "CYP3A4"]

        for gene in genes_to_check:
            functional_phenotype = self.kb.get_phenoconversion(medications, gene)
            if not functional_phenotype:
                continue

            gene_data = genotype.get(gene)
            if not gene_data:
                continue

            genetic_phenotype = gene_data.get("phenotype", "")
            # Only flag if phenoconversion makes things worse
            if self._phenotype_severity(functional_phenotype) <= self._phenotype_severity(genetic_phenotype):
                continue

            # Find which drug is causing the inhibition
            inhibitors = self.kb.get_cyp_inhibitors_in_list(medications)
            gene_inhibitors = inhibitors.get(gene, [])
            inhibitor_names = [i["drug"] for i in gene_inhibitors]

            # Find which drugs are affected by this gene
            for drug in medications:
                if drug.lower() in [i.lower() for i in inhibitor_names]:
                    continue  # Skip the inhibitor itself
                interaction = self.kb.get_gene_drug_interaction(gene, drug)
                if not interaction:
                    continue

                phenotype_impacts = interaction.get("phenotype_impacts", {})
                impact = phenotype_impacts.get(functional_phenotype)
                if not impact:
                    continue

                risk_level = impact.get("risk_level", "low")
                if risk_level == "low":
                    continue

                findings.append({
                    "finding_type": "phenoconversion",
                    "severity": risk_level if risk_level != "low" else "moderate",
                    "gene": gene,
                    "drug": drug,
                    "phenotype": functional_phenotype,
                    "genetic_phenotype": genetic_phenotype,
                    "inhibitor_drugs": inhibitor_names,
                    "summary": (
                        f"Phenoconversion: {', '.join(inhibitor_names)} inhibits {gene}, "
                        f"shifting functional phenotype from {self._format_phenotype(genetic_phenotype)} "
                        f"to {self._format_phenotype(functional_phenotype)} for {drug}"
                    ),
                    "recommendation": impact.get("recommendation", ""),
                    "clinical_consequence": impact.get("clinical_consequence", ""),
                    "evidence_level": impact.get("evidence_level", ""),
                    "fda_label": False,
                    "mechanism": (
                        f"{', '.join(inhibitor_names)} {'inhibits' if 'poor' in functional_phenotype or 'intermediate' in functional_phenotype else 'induces'} "
                        f"{gene} enzyme activity, altering metabolism of {drug}"
                    ),
                    "source": "phenoconversion",
                })

        return findings

    def _check_drug_drug_interactions(self, medications: list) -> list:
        """Check all pairwise drug-drug interactions."""
        findings = []
        ddis = self.kb.get_drug_drug_interactions(medications)

        for ddi in ddis:
            severity = ddi.get("severity", "moderate")
            severity_map = {"major": "high", "moderate": "moderate", "minor": "low"}
            mapped_severity = severity_map.get(severity, severity)

            findings.append({
                "finding_type": "drug_drug_interaction",
                "severity": mapped_severity,
                "drug": f"{ddi['drug_a']} + {ddi['drug_b']}",
                "drug_a": ddi["drug_a"],
                "drug_b": ddi["drug_b"],
                "gene": ddi.get("phenoconversion", {}).get("target_gene", "") if ddi.get("phenoconversion") else "",
                "phenotype": "",
                "summary": f"Drug interaction: {ddi['drug_a']} + {ddi['drug_b']} — {ddi.get('clinical_effect', '')}",
                "recommendation": ddi.get("recommendation", ""),
                "clinical_consequence": ddi.get("clinical_effect", ""),
                "mechanism": ddi.get("mechanism", ""),
                "evidence_level": ddi.get("evidence_level", ""),
                "fda_label": False,
                "references": ddi.get("references", []),
                "source": "ddi",
            })

        return findings

    def _check_renal_adjustments(self, medications: list, egfr: float) -> list:
        """Check if any medications need renal dose adjustment."""
        findings = []
        for drug in medications:
            adjustment = self.kb.get_renal_adjustment(drug, egfr)
            if adjustment:
                findings.append({
                    "finding_type": "renal_warning",
                    "severity": "high" if egfr < 30 else "moderate",
                    "drug": drug,
                    "gene": "",
                    "phenotype": "",
                    "summary": f"Renal impairment (eGFR {egfr}): {adjustment['action']}",
                    "recommendation": adjustment["action"],
                    "clinical_consequence": f"Drug accumulation risk with eGFR {egfr} ({adjustment.get('renal_stage', '')})",
                    "evidence_level": "standard_of_care",
                    "fda_label": True,
                    "source": "renal",
                })
        return findings

    def _check_hepatic_adjustments(self, medications: list, alt_ratio: float) -> list:
        """Check if any medications need hepatic adjustment."""
        findings = []
        for drug in medications:
            adjustment = self.kb.get_hepatic_adjustment(drug, alt_ratio)
            if adjustment:
                findings.append({
                    "finding_type": "hepatic_warning",
                    "severity": "high" if adjustment["severity"] == "severe" else "moderate",
                    "drug": drug,
                    "gene": "",
                    "phenotype": "",
                    "summary": f"Hepatic concern (ALT {alt_ratio:.1f}x ULN): {adjustment['action']}",
                    "recommendation": adjustment["action"],
                    "clinical_consequence": f"Hepatotoxicity risk with ALT {alt_ratio:.1f}x ULN",
                    "evidence_level": "standard_of_care",
                    "fda_label": True,
                    "source": "hepatic",
                })
        return findings

    def _deduplicate_findings(self, findings: list) -> list:
        """Remove duplicate findings, keeping highest severity."""
        seen = {}
        for f in findings:
            key = (f.get("drug", ""), f.get("gene", ""), f.get("finding_type", ""))
            if key in seen:
                existing = seen[key]
                if self._severity_rank(f.get("severity", "")) > self._severity_rank(existing.get("severity", "")):
                    seen[key] = f
            else:
                seen[key] = f
        return list(seen.values())

    def _severity_rank(self, severity: str) -> int:
        ranks = {"critical": 5, "high": 4, "moderate": 3, "low": 2, "informational": 1}
        return ranks.get(severity, 0)

    def _phenotype_severity(self, phenotype: str) -> int:
        """Higher number = more clinically concerning metabolizer status."""
        severity = {
            "normal_metabolizer": 0, "normal_function": 0, "normal_sensitivity": 0,
            "hla_b_1502_negative": 0,
            "intermediate_metabolizer": 1, "intermediate_function": 1,
            "moderate_sensitivity": 2,
            "poor_metabolizer": 3, "poor_function": 3,
            "ultra_rapid_metabolizer": 3,
            "high_sensitivity": 4,
            "hla_b_1502_positive": 4,
        }
        return severity.get(phenotype, 0)

    def _format_phenotype(self, phenotype: str) -> str:
        """Format phenotype string for display."""
        return phenotype.replace("_", " ").title()
