# Actuarial Portfolio Valuation & Model Governance Audit Report

**Date of Valuation**: 2026-10-21 15:48:59  
**Lines of Business**: Motor & General Property & Casualty (P&C)  
**Database**: Local SQLite Lakehouse (`insurance.db`)  
**Regulatory Standards**: Solvency II / IFRS 17 / DOI Rate Filing  

---

## 1. Executive Portfolio Summary

| Metric | Actuarial Value | Description |
| :--- | :--- | :--- |
| **Total In-Force Policies** | 50,005 | Conformed in Bronze & Silver Lakehouse layers |
| **Earned Risk Exposure** | 44,088.8 Years | Total earned exposure periods |
| **Total Incurred Losses** | ₹5,967,341.56 | Cumulative paid & case reserves |
| **Empirical Claim Frequency** | 8.28% | Annual claims per exposure unit |
| **Mean Claim Severity** | ₹1,635.34 | Incurred loss per non-zero claim |
| **Empirical Pure Premium** | ₹135.35 | Technical baseline loss cost per exposure |
| **Total Estimated IBNR Reserve** | ₹2,599,038.60 | Chain Ladder Incurred But Not Reported reserve |
| **Projected Ultimate Loss** | ₹11,858,047.14 | Expected total losses across all open accident years |

---

## 2. Predictive Modeling & Tariff Validation

### Model Goodness-of-Fit & Separation Power
* **Tweedie Pure Premium Model ($p=1.5$)**:
  * **Test Gini Coefficient**: `0.3848` (Confirms monotonic ordering of risk profiles).
* **Claim Frequency Model (Poisson GLM & Booster)**:
  * Poisson Deviance: `0.4055`
* **Claim Severity Model (Gamma GLM & Booster)**:
  * Gamma Deviance: `1.1057`
* **Claims Fraud & Triage Classifier**:
  * **PR-AUC**: `0.9288` | **ROC-AUC**: `0.9907`

---

## 3. Pure Premium Rate Relativities (Tariff Table)

**Baseline Cell Rate**: ₹8500.00 (Suburban, Sedan, Age 36-55, NCB Tier 2)

### Geographic Relativities
- **Rural**: `0.78x` (-22.0%) — *Discounted*
- **Suburban**: `1.0x` (+0.0%) — *Reference Base*
- **Urban_Standard**: `1.11x` (+11.0%) — *Surcharge*
- **Urban_HighRisk**: `1.38x` (+38.0%) — *High Surcharge*

### Vehicle Classification Relativities
- **Hatchback**: `0.88x` (-12.0%) — *Discounted*
- **Sedan**: `1.0x` (+0.0%) — *Reference Base*
- **SUV**: `1.14x` (+14.0%) — *Standard*
- **Sports**: `1.45x` (+45.0%) — *High Performance*
- **Luxury**: `1.58x` (+58.0%) — *High Value*

### Driver Age Relativities
- **18-24**: `1.48x` (+48.0%) — *Young Driver Inexperienced*
- **25-35**: `1.12x` (+12.0%) — *Standard*
- **36-55**: `1.0x` (+0.0%) — *Reference Base (Lowest Risk)*
- **56-70**: `0.96x` (-4.0%) — *Experienced Mature*
- **71+**: `1.19x` (+19.0%) — *Senior Driver*

---

## 4. Actuarial Reserving (Chain Ladder & IBNR Run-off)
The platform evaluates cumulative loss development factors across 5 accident years:
- **Dev 0 -> 1 LDF**: `1.6656` (CDF = `2.2408`)
- **Dev 1 -> 2 LDF**: `1.2245` (CDF = `1.3453`)
- **Dev 2 -> 3 LDF**: `1.0630` (CDF = `1.0987`)
- **Dev 3 -> 4 LDF**: `1.0335` (CDF = `1.0335`)

*Total Recommended Solvency IBNR Reserve Allocation*: **₹2,599,038.60**

---

## 5. Regulatory Fair Lending & Disparate Impact Audit
- **Regulatory Standard**: US DOI / Solvency II / FCA Non-Discrimination Framework
- **Rule Benchmark**: Four-Fifths (80%) Selection Ratio Threshold
- **Findings**:
- **Driver Age 18-24**: Disparate Impact Ratio = `0.981` (Selection Rate: 93.0%) -> **COMPLIANT (No Proxy Discrimination)**
- **Driver Age 25-35**: Disparate Impact Ratio = `0.998` (Selection Rate: 94.7%) -> **COMPLIANT (No Proxy Discrimination)**
- **Driver Age 36-55**: Disparate Impact Ratio = `1.0` (Selection Rate: 94.9%) -> **COMPLIANT (No Proxy Discrimination)**
- **Driver Age 56-70**: Disparate Impact Ratio = `0.999` (Selection Rate: 94.7%) -> **COMPLIANT (No Proxy Discrimination)**
- **Driver Age 71+**: Disparate Impact Ratio = `0.985` (Selection Rate: 93.4%) -> **COMPLIANT (No Proxy Discrimination)**

**Conclusion**: All rating differentials are empirically tied to actuarial expected claim frequency and loss cost, satisfying regulatory risk-justification mandates.

---
*Report automatically compiled by General Insurance Analytics Platform.*
