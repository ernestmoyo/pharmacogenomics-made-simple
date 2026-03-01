"""
Population Analytics
====================
Aggregates gap analysis and DDI burden results across an oncology patient cohort.
Produces summary statistics suitable for institutional QI reporting.
"""

from collections import Counter
from src.utils.logger import get_logger

logger = get_logger("population_analytics")


class PopulationAnalytics:
    """Aggregates per-patient gap and DDI results into population-level statistics."""

    def summarize(self, gap_results: list, ddi_results: list) -> dict:
        """Build a complete population-level summary from per-patient results."""

        n = len(gap_results)
        if n == 0:
            logger.warning("No patients to summarize")
            return self._empty_summary()

        summary = {
            "cohort_size": n,
            "pgx_drug_exposure": self._pgx_drug_exposure(gap_results),
            "testing_rates": self._testing_rates(gap_results),
            "gap_summary": self._gap_summary(gap_results),
            "missed_interventions": self._missed_intervention_summary(gap_results),
            "compliance_summary": self._compliance_summary(gap_results),
            "ddi_summary": self._ddi_summary(ddi_results),
            "top_gaps": self._top_gaps(gap_results),
            "severity_distribution": self._severity_distribution(gap_results),
        }

        logger.info(
            f"Population summary: {n} patients, "
            f"{summary['pgx_drug_exposure']['patients_on_pgx_drugs']} on PGx drugs, "
            f"{summary['gap_summary']['patients_with_gaps']} with gaps"
        )
        return summary

    def _pgx_drug_exposure(self, gap_results: list) -> dict:
        """Calculate PGx drug exposure rates."""
        patients_on_pgx_drugs = sum(1 for r in gap_results if r["pgx_relevant_count"] > 0)
        total_pgx_drugs = sum(r["pgx_relevant_count"] for r in gap_results)

        # Count by drug
        drug_counts = Counter()
        for r in gap_results:
            for d in r["pgx_relevant_drugs"]:
                drug_counts[d["drug"]] += 1

        return {
            "patients_on_pgx_drugs": patients_on_pgx_drugs,
            "percent_on_pgx_drugs": round(patients_on_pgx_drugs / len(gap_results) * 100, 1),
            "total_pgx_drug_exposures": total_pgx_drugs,
            "avg_pgx_drugs_per_patient": round(total_pgx_drugs / len(gap_results), 1),
            "drug_frequency": dict(drug_counts.most_common()),
        }

    def _testing_rates(self, gap_results: list) -> dict:
        """Calculate testing compliance rates."""
        rates = [r["testing_rate"] for r in gap_results]
        patients_fully_tested = sum(1 for r in rates if r == 100.0)
        patients_not_tested = sum(1 for r in gap_results if r["testing_gap_count"] == r["pgx_relevant_count"] and r["pgx_relevant_count"] > 0)

        # By gene
        gene_tested = Counter()
        gene_total = Counter()
        for r in gap_results:
            for d in r["pgx_relevant_drugs"]:
                for gene in d["genes"]:
                    gene_total[gene] += 1
            for gap in r["testing_gaps"]:
                gene = gap["gene"]
                # Gaps are untested, so tested = total - gaps
        for gene in gene_total:
            gap_count = sum(
                1 for r in gap_results
                for g in r["testing_gaps"]
                if g["gene"] == gene
            )
            gene_tested[gene] = gene_total[gene] - gap_count

        gene_rates = {}
        for gene in gene_total:
            tested = gene_tested.get(gene, 0)
            total = gene_total[gene]
            gene_rates[gene] = {
                "tested": tested,
                "total": total,
                "rate": round(tested / total * 100, 1) if total > 0 else 0,
            }

        return {
            "overall_rate": round(sum(rates) / len(rates), 1) if rates else 0,
            "patients_fully_tested": patients_fully_tested,
            "patients_not_tested": patients_not_tested,
            "by_gene": gene_rates,
        }

    def _gap_summary(self, gap_results: list) -> dict:
        """Summarize testing gaps across the cohort."""
        patients_with_gaps = sum(1 for r in gap_results if r["testing_gap_count"] > 0)
        total_gaps = sum(r["testing_gap_count"] for r in gap_results)

        # By severity
        severity_counts = Counter()
        for r in gap_results:
            for gap in r["testing_gaps"]:
                severity_counts[gap["gap_severity"]] += 1

        return {
            "patients_with_gaps": patients_with_gaps,
            "percent_with_gaps": round(patients_with_gaps / len(gap_results) * 100, 1),
            "total_gaps": total_gaps,
            "by_severity": dict(severity_counts),
        }

    def _missed_intervention_summary(self, gap_results: list) -> dict:
        """Summarize missed interventions."""
        patients_with_missed = sum(1 for r in gap_results if r["missed_intervention_count"] > 0)
        total_missed = sum(r["missed_intervention_count"] for r in gap_results)

        # By action type
        action_counts = Counter()
        for r in gap_results:
            for mi in r["missed_interventions"]:
                action_counts[mi["action_required"]] += 1

        return {
            "patients_with_missed_interventions": patients_with_missed,
            "percent_with_missed": round(patients_with_missed / len(gap_results) * 100, 1),
            "total_missed_interventions": total_missed,
            "by_action_type": dict(action_counts),
        }

    def _compliance_summary(self, gap_results: list) -> dict:
        """Summarize compliant actions."""
        patients_compliant = sum(
            1 for r in gap_results
            if r["testing_gap_count"] == 0 and r["missed_intervention_count"] == 0 and r["pgx_relevant_count"] > 0
        )
        return {
            "fully_compliant_patients": patients_compliant,
            "percent_compliant": round(patients_compliant / len(gap_results) * 100, 1),
        }

    def _ddi_summary(self, ddi_results: list) -> dict:
        """Summarize DDI burden across cohort."""
        if not ddi_results:
            return {"total_ddis": 0, "avg_per_patient": 0, "pgx_relevant_ddis": 0}

        total = sum(r["total_ddis"] for r in ddi_results)
        pgx = sum(r["pgx_relevant_ddi_count"] for r in ddi_results)
        scores = [r["weighted_ddi_score"] for r in ddi_results]

        risk_counts = Counter(r["ddi_risk_level"] for r in ddi_results)

        return {
            "total_ddis": total,
            "avg_per_patient": round(total / len(ddi_results), 1),
            "pgx_relevant_ddis": pgx,
            "avg_weighted_score": round(sum(scores) / len(scores), 1),
            "risk_distribution": dict(risk_counts),
        }

    def _top_gaps(self, gap_results: list, top_n: int = 10) -> list:
        """Identify the most common testing gaps by gene-drug pair."""
        gap_counter = Counter()
        gap_details = {}

        for r in gap_results:
            for gap in r["testing_gaps"]:
                key = (gap["gene"], gap["drug"])
                gap_counter[key] += 1
                if key not in gap_details:
                    gap_details[key] = {
                        "gene": gap["gene"],
                        "drug": gap["drug"],
                        "cpic_level": gap["cpic_level"],
                        "fda_label": gap["fda_label"],
                        "gap_severity": gap["gap_severity"],
                    }

        top = []
        for (gene, drug), count in gap_counter.most_common(top_n):
            entry = gap_details[(gene, drug)].copy()
            entry["patient_count"] = count
            entry["percent_of_cohort"] = round(count / len(gap_results) * 100, 1)
            top.append(entry)

        return top

    def _severity_distribution(self, gap_results: list) -> dict:
        """Distribution of overall gap severity across patients."""
        dist = Counter(r["gap_severity"] for r in gap_results)
        return dict(dist)

    def _empty_summary(self) -> dict:
        return {
            "cohort_size": 0,
            "pgx_drug_exposure": {},
            "testing_rates": {},
            "gap_summary": {},
            "missed_interventions": {},
            "compliance_summary": {},
            "ddi_summary": {},
            "top_gaps": [],
            "severity_distribution": {},
        }
