# Team Kickoff Meeting

**Date:** 8 February 2025, 6:00 AM EAT
**Attendees:**
- Ernest Moyo (ernestmoyo35@gmail.com)
- Tapiwa Mupereki (tmupereki@jewelride.com)
- Rangarirai Makuku (rangariraimakuku@gmail.com)
- Ngonidzashe Faya (ngonifaya08@gmail.com)
**Format:** Virtual (video call)

---

## Introductions

### Ernest Moyo
- Based in Tanzania, doing PhD in Mathematics
- Scholarship from Rector Atlas (offshoot of Malaria Atlas Project, Australia), funded by Gates Foundation
- Background: actuarial science > public health > MSc biostatistics & epidemiology
- Consulting for Clinton Health Access Initiative (CHAI) alongside PhD
- Previously original epidemiologist for CHAI in Namibia
- Strengths: analytics, modeling, risk estimation, data simulation

### Tapiwa Mupereki
- Board-certified by the American Board of Medical Genetics and Genomics
- Extensive experience in genetic testing: inherited diseases, cancer, pharmacogenomics, newborn screening
- Previously at Cincinnati — handled ~90% of PGx cases in-house
- Works with pathologists on genetic interpretation — translating raw genetic data into clinical meaning
- Training involved understanding disease mechanisms, inheritance patterns, and clinical recommendations
- Currently based in the US

### Rangarirai Makuku
- Pharmacist by training (~20 years experience)
- Public health masters (how he came to the US in 2010)
- Worked extensively in HIV, malaria, TB drug programs
- Brief stint in retail pharmacy (CVS)
- Currently dedicating ~60% of time to building this company
- Also a student in an executive Doctor of Public Health program (global health major)
- Deep understanding of drug interactions, medication management, and pharmacy operations

---

## MVP Demo (Moyo)

Moyo presented the PGx Clinical Solutions platform built on GitHub:

- **Synthetic data:** 25 patient profiles with diverse demographics and conditions
- **Knowledge base:** 21 gene-drug pairs, 14 drug-drug interactions
- **Interpretation engine:** Automated analysis of genotype-drug interactions
- **Clinical reports:** 25 polished HTML reports with:
  - Patient information and executive summary
  - High-priority action recommendations
  - Current medication analysis
  - Pharmacogenomic results (metabolizer status)
  - Gene-drug interaction analysis
  - Prioritized clinical recommendations
  - Methodology, evidence, and disclaimers
- **Interactive demo:** Live walkthrough of patient scenarios across psychiatry, cardiology, oncology, pain management
- **Team credited** on the reports (Ernest, Rangarirai, Tapiwa)

**Team reaction:** Tapiwa confirmed the reports are "really amazing" and aligned with real clinical needs.

---

## Key Problems Identified

### 1. Interpretation Gap
- Labs perform genetic tests but produce raw results without actionable interpretation
- Physicians receive reports that just list genotype data without clear clinical guidance
- Example: a report might say "CYP2D6 poor metabolizer" but not tell the physician what to do about the patient's current medications
- Tapiwa confirmed this is a widespread, systemic problem

### 2. Reference Genome Bias
- Current genomic databases are predominantly based on white/European populations
- Variants common in African, Asian, Pacific Islander populations are underrepresented
- Leads to "normal" classifications that may be incorrect for non-European patients
- Real-world harm: lawsuit settlements in the millions over misclassification affecting Pacific Islanders
- 19 medications have known population-specific concerns

### 3. Physician Knowledge Gap
- Many physicians don't understand how to act on pharmacogenomic results
- Medical training hasn't caught up with the pace of genetic testing availability
- Need for education and decision support at point of care

---

## Business Opportunities Discussed

| Opportunity | Description | Champion |
|---|---|---|
| Interpretation middleware | Sit between lab results and physician — provide the intelligence layer | All |
| Clinician training | Workshops teaching physicians how to use PGx results | Tapiwa, Rangarirai |
| Policy & governance consulting | Help African countries develop PGx guidelines and ensure inclusivity | Ernest |
| EMR/API integration | Connect interpretation engine to electronic health records | Ernest (technical) |
| Lab consulting | Help hospitals set up PGx testing programs | Tapiwa, Rangarirai |
| Testing + interpretation (long-term) | Eventually offer end-to-end genetic testing and reporting | All |

### Dual-Track Model Proposed (Ernest)
- **Private track:** Commercial interpretation services, consulting, training
- **Social enterprise track:** Grants for genomic equity work, government capacity building, policy support in Africa

---

## Funding Discussion

- **US presence needed:** Having US nationals on the team makes grant/funding access significantly easier
- **Grant targets:** Gates Foundation (genomic equity), NIH, USAID
- **Near-term:** Seed funding or consulting revenue while building
- **Lab equipment:** Some vendors offer free machines + reagents in exchange for multi-year consumables contracts
- **Consensus:** Start generating momentum and revenue; don't wait for perfect conditions

---

## Decisions & Action Items

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Add Tapiwa, Rangarirai, and Ngonidzashe as GitHub collaborators | Ernest | Pending |
| 2 | Tapiwa to review clinical accuracy of 25 reports | Tapiwa | Pending |
| 3 | Identify 1 lab/clinic for pilot interpretation service | Tapiwa | Pending |
| 4 | Refine business model based on meeting discussion | All | Pending |
| 5 | Explore grant opportunities (Gates Foundation, NIH) | Ernest | Pending |
| 6 | Schedule follow-up meeting focused on decisions | Ernest | Pending |

---

## Next Meeting Agenda (TBD)
- First product decision: interpretation service vs. training vs. consulting
- Target market: US labs or African health systems first
- Roles and equity discussion
- Timeline for pilot customer
