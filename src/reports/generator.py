"""
Clinical Report Generator
=========================
Generates professional HTML clinical pharmacogenomics reports.
"""

import uuid
from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    """Generates clinical PGx interpretation reports."""

    def __init__(self, template_dir: Path = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True,
        )
        self.env.filters["phenotype_display"] = self._phenotype_display
        self.env.filters["severity_color"] = self._severity_color
        self.env.filters["priority_label"] = self._priority_label
        self.env.filters["action_label"] = self._action_label
        self.env.filters["time_frame_label"] = self._time_frame_label

    def generate_html_report(self, patient: dict, analysis_results: dict) -> str:
        """Render the full clinical report as HTML."""
        template = self.env.get_template("clinical_report.html")

        report_metadata = {
            "report_id": f"RPT-{patient.get('patient_id', 'UNK')}-{datetime.now().strftime('%Y%m%d')}",
            "generated_date": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            "generated_iso": datetime.now().isoformat(),
            "version": "1.0.0",
            "platform": "PGx Clinical Solutions",
        }

        # Separate gene-drug findings from other findings
        scored_findings = analysis_results.get("scored_findings", [])
        gene_drug_findings = [f for f in scored_findings if f.get("finding_type") in ("gene_drug_interaction", "contraindication", "phenoconversion")]
        ddi_findings = [f for f in scored_findings if f.get("finding_type") == "drug_drug_interaction"]
        organ_findings = [f for f in scored_findings if f.get("finding_type") in ("renal_warning", "hepatic_warning")]

        html = template.render(
            patient=patient,
            findings=analysis_results.get("findings", []),
            scored_findings=scored_findings,
            gene_drug_findings=gene_drug_findings,
            ddi_findings=ddi_findings,
            organ_findings=organ_findings,
            recommendations=analysis_results.get("recommendations", []),
            risk_summary=analysis_results.get("risk_summary", {}),
            drug_drug_interactions=analysis_results.get("drug_drug_interactions", []),
            report_metadata=report_metadata,
        )
        return html

    def generate_and_save(self, patient: dict, analysis_results: dict, output_path: Path):
        """Generate report and save to file."""
        html = self.generate_html_report(patient, analysis_results)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def generate_summary(self, patient: dict, analysis_results: dict) -> str:
        """Generate plain-text executive summary."""
        pid = patient.get("patient_id", "Unknown")
        name = f"{patient.get('demographics', {}).get('first_name', '')} {patient.get('demographics', {}).get('last_name', '')}"
        risk = analysis_results.get("risk_summary", {})
        recs = analysis_results.get("recommendations", [])

        lines = [
            f"PHARMACOGENOMICS REPORT SUMMARY — {pid}",
            f"Patient: {name}",
            f"Risk Category: {risk.get('category', 'Unknown')}",
            f"Total Findings: {risk.get('total_findings', 0)} "
            f"(Critical: {risk.get('critical_count', 0)}, High: {risk.get('high_count', 0)}, Moderate: {risk.get('moderate_count', 0)})",
            "",
            "PRIORITY RECOMMENDATIONS:",
        ]

        for i, rec in enumerate(recs, 1):
            lines.append(f"  {i}. [{rec.get('time_frame', 'routine').upper()}] {rec.get('drug', '')}: {rec.get('recommendation_text', '')}")

        return "\n".join(lines)

    def generate_all_reports(self, patients_with_results: list, output_dir: Path):
        """Batch generate reports for multiple patients."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for patient, results in patients_with_results:
            pid = patient.get("patient_id", "UNKNOWN")
            path = output_dir / f"report_{pid}.html"
            self.generate_and_save(patient, results, path)

    @staticmethod
    def _phenotype_display(phenotype: str) -> str:
        return phenotype.replace("_", " ").title() if phenotype else ""

    @staticmethod
    def _severity_color(severity: str) -> str:
        colors = {
            "critical": "#dc2626",
            "high": "#ea580c",
            "moderate": "#d97706",
            "low": "#16a34a",
            "informational": "#2563eb",
        }
        return colors.get(severity, "#6b7280")

    @staticmethod
    def _priority_label(priority: int) -> str:
        labels = {1: "URGENT", 2: "HIGH", 3: "MODERATE", 4: "LOW"}
        return labels.get(priority, "INFO")

    @staticmethod
    def _action_label(action_type: str) -> str:
        labels = {
            "stop_drug": "DISCONTINUE",
            "switch_drug": "SWITCH MEDICATION",
            "reduce_dose": "ADJUST DOSE",
            "increase_monitoring": "INCREASE MONITORING",
            "add_monitoring": "ADD MONITORING",
            "no_change": "NO CHANGE NEEDED",
            "inform_only": "INFORMATIONAL",
        }
        return labels.get(action_type, action_type.upper())

    @staticmethod
    def _time_frame_label(time_frame: str) -> str:
        labels = {
            "immediate": "Immediate Action",
            "next_visit": "Next Clinical Visit",
            "routine": "Routine Follow-up",
        }
        return labels.get(time_frame, time_frame)
